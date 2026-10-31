"""Yhteysanalyysi verkostoaineistosta (data/network.json).

Yhteistyöverkko = organisaatiot, hankkeet, osaamiskeskukset ja vertailukohteet, joita yhdistää
osallistuminen, keskukseen kuuluminen tai dokumentoitu yhteistyö. Rahoitussuhteet ja
teemapäällekkäisyys eivät ole yhteistyötä, joten ne jätetään tästä verkosta pois.

Tuottaa:
  analysis/organisaatiot.csv   – keskeisyys ja ulottuvuus organisaatioittain
  analysis/komponentit.csv     – toisistaan erilliset yhteistyösaarekkeet
  analysis/puuttuvat_yhteydet.csv – samaa tekevät toimijat ilman yhteyttä
  analysis/raportti.md         – luettava yhteenveto
  data/analysis.json           – visualisoinnin syöte

Aja:  python scripts/analyze.py   (aja ensin scripts/build.py)
"""
import csv, json
from collections import Counter, defaultdict
from pathlib import Path

import networkx as nx

ROOT = Path(__file__).resolve().parents[1]
ACTOR_KINDS = {"organisaatio", "hanke", "osaamiskeskus", "vertailukohde"}
COLLAB_EDGES = {"osallistuu", "kuuluu_keskukseen", "yhteistyo"}
MAX_HOPS = 3          # polku ≤ 3 askelta = toimijat tuntevat toisensa (esim. yhteinen organisaatio = 2)
MISSING_MIN_J = 0.5   # teemojen Jaccard-raja puuttuvalle yhteydelle


def load():
    net = json.loads((ROOT / "data" / "network.json").read_text(encoding="utf-8"))
    return {n["id"]: n for n in net["nodes"]}, net["edges"]


def collab_graph(nodes, edges, include_unverified=True):
    G = nx.Graph()
    for i, n in nodes.items():
        if n["kind"] in ACTOR_KINDS:
            G.add_node(i, **n)
    for e in edges:
        if e["kind"] in COLLAB_EDGES and e["source"] in G and e["target"] in G:
            if not include_unverified and e["evidence"] == "vahvistamatta":
                continue
            G.add_edge(e["source"], e["target"], kind=e["kind"], evidence=e["evidence"])
    return G


def main():
    nodes, edges = load()
    G = collab_graph(nodes, edges)
    Gv = collab_graph(nodes, edges, include_unverified=False)
    out = ROOT / "analysis"; out.mkdir(exist_ok=True)

    # 1. Komponentit
    comps = sorted(nx.connected_components(Gv), key=len, reverse=True)  # vain vahvistetut yhteydet
    comp_of = {}
    comp_rows = []
    for k, c in enumerate(comps, 1):
        countries = sorted({nodes[i].get("country", "") for i in c} - {""})
        acts = [i for i in c if nodes[i]["kind"] != "organisaatio"]
        for i in c:
            comp_of[i] = k
        comp_rows.append(dict(komponentti=k, solmuja=len(c), maita=len(countries), maat=" ".join(countries),
                              hankkeet_ja_keskukset=" ".join(sorted(acts))))
    write_csv(out / "komponentit.csv", comp_rows)

    # 2. Organisaatioiden keskeisyys
    btw = nx.betweenness_centrality(Gv, normalized=True)
    org_rows = []
    for i, n in nodes.items():
        if n["kind"] != "organisaatio" or i not in G:
            continue
        acts = list(Gv.neighbors(i))
        reach = {nodes[x].get("country") for a in acts for x in nx.single_source_shortest_path_length(Gv, a, cutoff=2)}
        hubs = sorted({h for a in acts for h in G.neighbors(a) if nodes[h]["kind"] == "osaamiskeskus"} |
                      {a for a in acts if nodes[a]["kind"] == "osaamiskeskus"})
        org_rows.append(dict(id=i, nimi=n["label"], maa=n["country"], tyyppi=n["org_type"],
                             hankkeita=len(acts), keskuksia=len(hubs), keskukset=" ".join(hubs),
                             tavoittaa_maita=len(reach - {None}), valityskeskeisyys=round(btw.get(i, 0), 4),
                             komponentti=comp_of.get(i)))
    org_rows.sort(key=lambda r: (-r["valityskeskeisyys"], -r["hankkeita"]))
    write_csv(out / "organisaatiot.csv", org_rows)

    # 3. Puuttuvat yhteydet: teemallisesti päällekkäiset toimijat, joiden välillä ei ole lyhyttä polkua
    overlaps = [e for e in edges if e["kind"] == "teemapaallekkaisyys" and e["weight"] >= MISSING_MIN_J]
    miss = []
    for e in overlaps:
        a, b = e["source"], e["target"]
        try:
            d = nx.shortest_path_length(Gv, a, b)
        except (nx.NetworkXNoPath, nx.NodeNotFound):
            d = None
        if d is None or d > MAX_HOPS:
            na, nb = nodes[a], nodes[b]
            ev = max(int(na.get("evidence_level") or 0), int(nb.get("evidence_level") or 0))
            miss.append(dict(a=a, a_nimi=na["label"], a_maa=na.get("country"), b=b, b_nimi=nb["label"],
                             b_maa=nb.get("country"), jaccard=e["weight"], yhteiset_teemat=e["note"],
                             etaisyys="ei polkua" if d is None else d,
                             tyyppi="maiden välinen" if na.get("country") != nb.get("country") else "sama maa",
                             paras_naytto=ev))
    miss.sort(key=lambda r: (-r["jaccard"], r["tyyppi"] != "maiden välinen", -r["paras_naytto"]))
    write_csv(out / "puuttuvat_yhteydet.csv", miss)

    # 4. Maiden väliset dokumentoidut yhteydet
    cross, cross_unv = Counter(), Counter()
    for u, v, d in G.edges(data=True):
        cu, cv = nodes[u].get("country"), nodes[v].get("country")
        if cu and cv and cu != cv and d["evidence"] == "vahvistamatta":
            cross_unv[tuple(sorted((cu, cv)))] += 1
    for u, v, d in Gv.edges(data=True):
        cu, cv = nodes[u].get("country"), nodes[v].get("country")
        if cu and cv and cu != cv:
            cross[tuple(sorted((cu, cv)))] += 1

    # 5. Keskusten jaetut organisaatiot
    hub_orgs = defaultdict(set)
    for h, n in nodes.items():
        if n["kind"] != "osaamiskeskus":
            continue
        members = [x for x in G.neighbors(h) if G.edges[h, x]["kind"] != "yhteistyo"] + [h]
        for m in members:
            for o in G.neighbors(m):
                if nodes[o]["kind"] == "organisaatio" and G.edges[m, o]["kind"] == "osallistuu":
                    hub_orgs[h].add(o)
    shared = []
    hl = sorted(hub_orgs)
    for i, a in enumerate(hl):
        for b in hl[i + 1:]:
            s = hub_orgs[a] & hub_orgs[b]
            if s:
                shared.append(dict(a=a, b=b, organisaatiot=sorted(s)))

    analysis = dict(
        params=dict(max_hops=MAX_HOPS, missing_min_jaccard=MISSING_MIN_J),
        summary=dict(actors=Gv.number_of_nodes(), collab_edges=Gv.number_of_edges(), unverified_edges=G.number_of_edges() - Gv.number_of_edges(), components=len(comps),
                     largest_component=len(comps[0]), multi_country_components=sum(1 for r in comp_rows if r["maita"] > 1),
                     cross_country_edges=sum(cross.values()), missing_links=len(miss),
                     missing_cross_country=sum(1 for m in miss if m["tyyppi"] == "maiden välinen")),
        components=comp_rows, organisations=org_rows, missing_links=miss,
        cross_country={f"{a}–{b}": n for (a, b), n in cross.items()},
        cross_country_unverified={f"{a}–{b}": n for (a, b), n in cross_unv.items()}, hub_shared_orgs=shared,
        positions=layout(G),
    )
    (ROOT / "data" / "analysis.json").write_text(json.dumps(analysis, ensure_ascii=False, indent=1), encoding="utf-8")
    report(analysis, nodes)
    print(json.dumps(analysis["summary"], ensure_ascii=False))


def layout(G):
    """Vakaa asettelu visualisointia varten (sama tulos joka ajolla)."""
    pos = nx.spring_layout(G, seed=42, k=0.35, iterations=300)
    return {k: [round(float(v[0]), 4), round(float(v[1]), 4)] for k, v in pos.items()}


def write_csv(path, rows):
    if not rows:
        path.write_text("", encoding="utf-8"); return
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)


def report(a, nodes):
    s = a["summary"]
    L = ["# Yhteysanalyysi", "",
         "_Generoitu skriptillä `scripts/analyze.py`. Älä muokkaa käsin._", "",
         "## Yhteenveto", "",
         f"- Toimijoita yhteistyöverkossa: **{s['actors']}**, vahvistettuja yhteistyösärmiä **{s['collab_edges']}** (lisäksi {s['unverified_edges']} vahvistamatonta, jotka eivät ole mukana saarekkeissa eikä keskeisyydessä).",
         f"- Erillisiä yhteistyösaarekkeita: **{s['components']}**. Suurin kattaa {s['largest_component']} toimijaa.",
         f"- Usean maan saarekkeita: **{s['multi_country_components']}**. Maiden välisiä vahvistettuja yhteistyösärmiä: **{s['cross_country_edges']}**.",
         f"- Puuttuvia yhteyksiä (teemat Jaccard ≥ {a['params']['missing_min_jaccard']}, ei polkua ≤ {a['params']['max_hops']} askelta): **{s['missing_links']}**, joista maiden välisiä **{s['missing_cross_country']}**.",
         "", "## Maiden väliset yhteydet", ""]
    L += [f"- {k}: {v} (lähteellä vahvistettu)" for k, v in sorted(a["cross_country"].items())] or ["- Ei vahvistettuja."]
    L += [f"- {k}: {v} (kumppani vahvistamatta)" for k, v in sorted(a["cross_country_unverified"].items())]
    L += ["", "## Välittäjäorganisaatiot (välityskeskeisyys)", "",
          "| Organisaatio | Maa | Hankkeita | Keskuksia | Välityskeskeisyys |", "|---|---|---|---|---|"]
    for r in a["organisations"][:10]:
        L.append(f"| {r['nimi']} | {r['maa']} | {r['hankkeita']} | {r['keskuksia']} | {r['valityskeskeisyys']} |")
    L += ["", "## Osaamiskeskusten yhteiset organisaatiot", ""]
    L += [f"- {x['a']} ↔ {x['b']}: {', '.join(x['organisaatiot'])}" for x in a["hub_shared_orgs"]] or ["- Ei yhteisiä."]
    L += ["", "## Puuttuvat yhteydet (20 vahvinta)", "",
          "| A | B | Jaccard | Yhteiset teemat | Tyyppi |", "|---|---|---|---|---|"]
    for m in a["missing_links"][:20]:
        L.append(f"| {m['a']} {m['a_nimi'][:45]} | {m['b']} {m['b_nimi'][:45]} | {m['jaccard']} | {m['yhteiset_teemat']} | {m['tyyppi']} |")
    L += ["", "## Saarekkeet", "", "| # | Solmuja | Maat | Hankkeet ja keskukset |", "|---|---|---|---|"]
    for c in a["components"]:
        L.append(f"| {c['komponentti']} | {c['solmuja']} | {c['maat']} | {c['hankkeet_ja_keskukset']} |")
    (ROOT / "analysis" / "raportti.md").write_text("\n".join(L) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
