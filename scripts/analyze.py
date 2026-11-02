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
MISSING_MIN_J = 0.6   # teemojen Jaccard-raja puuttuvalle yhteydelle (ja ≥2 yhteistä teemaa, ks. build.py)
CROSS_COUNTRY_ONLY = True  # puuttuvat yhteydet vain maiden välillä


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
        na, nb = nodes[a], nodes[b]
        if CROSS_COUNTRY_ONLY and na.get("country") == nb.get("country"):
            continue
        if d is None or d > MAX_HOPS:
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

    # 6. Teema × maapari: onko maiden toimijoiden välillä yhtään vahvistettua yhteistyötä teemassa
    theme_of = defaultdict(set)
    for e in edges:
        if e["kind"] == "teema" and nodes[e["source"]]["kind"] in ("hanke", "vertailukohde"):
            theme_of[e["source"]].add(e["target"])
    countries = sorted({n.get("country") for n in nodes.values() if n["kind"] == "hanke" and n.get("country") not in (None, "", "EU")})
    gaps = []
    for t in sorted({t for s in theme_of.values() for t in s}):
        per = {c: [p for p, ts in theme_of.items() if t in ts and nodes[p].get("country") == c] for c in countries}
        for i, ca in enumerate(countries):
            for cb in countries[i + 1:]:
                A, B = per[ca], per[cb]
                if not A or not B:
                    continue
                linked = any(nx.has_path(Gv, x, y) and nx.shortest_path_length(Gv, x, y) <= MAX_HOPS
                             for x in A for y in B if x in Gv and y in Gv)
                gaps.append(dict(teema=t, a=ca, b=cb, hankkeita_a=len(A), hankkeita_b=len(B), yhteys=linked))
    gaps.sort(key=lambda g: (g["yhteys"], -(g["hankkeita_a"] * g["hankkeita_b"])))

    analysis = dict(
        params=dict(max_hops=MAX_HOPS, missing_min_jaccard=MISSING_MIN_J),
        summary=dict(actors=Gv.number_of_nodes(), collab_edges=Gv.number_of_edges(), unverified_edges=G.number_of_edges() - Gv.number_of_edges(), components=len(comps),
                     largest_component=len(comps[0]), multi_country_components=sum(1 for r in comp_rows if r["maita"] > 1),
                     cross_country_edges=sum(cross.values()), missing_links=len(miss),
                     missing_cross_country=sum(1 for m in miss if m["tyyppi"] == "maiden välinen"),
                     theme_country_pairs=len(gaps), theme_country_pairs_unlinked=sum(1 for g in gaps if not g["yhteys"])),
        components=comp_rows, organisations=org_rows, missing_links=miss,
        cross_country={f"{a}–{b}": n for (a, b), n in cross.items()},
        cross_country_unverified={f"{a}–{b}": n for (a, b), n in cross_unv.items()}, hub_shared_orgs=shared,
        theme_country_gaps=gaps,
    )
    # Asettelu omaan tiedostoonsa: liukulukutulokset voivat vaihdella ympäristöittäin
    (ROOT / "data" / "layout.json").write_text(json.dumps(layout(G), ensure_ascii=False, sort_keys=True), encoding="utf-8")
    (ROOT / "data" / "analysis.json").write_text(json.dumps(analysis, ensure_ascii=False, indent=1), encoding="utf-8")
    report(analysis, nodes)
    print(json.dumps(analysis["summary"], ensure_ascii=False))


# Maiden ankkuripisteet asettelussa (x, y välillä −1…1): saarekkeet ryhmittyvät maittain
ANCHORS = {"FI": (-0.55, -0.15), "SE": (-0.2, -0.75), "EE": (0.15, -0.8), "LV": (0.5, -0.5),
           "EU": (0.0, 0.05), "IE": (0.6, 0.45), "DE-NI": (-0.25, 0.65), "DE-SH": (0.25, 0.85)}


def layout(G):
    """Vakaa asettelu: jokainen yhteistyösaareke asetellaan erikseen ja sijoitetaan
    hallitsevan maansa ankkurin ympärille spiraaliin. Sama tulos joka ajolla."""
    import math
    comps = sorted(nx.connected_components(G), key=lambda c: (-len(c), sorted(c)[0]))
    placed = {k: 0 for k in ANCHORS}
    pos = {}
    for c in comps:
        sub = G.subgraph(c)
        countries = Counter(G.nodes[n].get("country") for n in c if G.nodes[n].get("country") in ANCHORS)
        home = countries.most_common(1)[0][0] if countries else "EU"
        if len(countries) > 1:
            home = "EU" if "EU" in countries else home
        ax, ay = ANCHORS[home]
        k = placed[home]; placed[home] += 1
        ang = k * 2.4; rad = 0.0 if k == 0 else 0.06 + 0.045 * math.sqrt(k)
        cx, cy = ax + rad * math.cos(ang), ay + rad * math.sin(ang)
        scale = 0.02 + 0.045 * math.sqrt(len(c))
        if len(c) == 1:
            p = {next(iter(c)): (0.0, 0.0)}
        else:
            p = nx.spring_layout(sub, seed=42, k=1.8 / math.sqrt(len(c)), iterations=200)
        rot = ang * 1.7  # kierretään saarekkeita, jotta pienet parit eivät osoita samaan suuntaan
        cr, sr = math.cos(rot), math.sin(rot)
        for n, (x0, y0) in p.items():
            x, y = x0 * cr - y0 * sr, x0 * sr + y0 * cr
            pos[n] = [round(float(cx + x * scale), 4), round(float(cy + y * scale), 4)]
    return pos


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
    L += ["", "## Teema × maapari", "",
          f"Maaparit, joilla on hankkeita samassa teemassa: **{s['theme_country_pairs']}**, joista ilman yhtään vahvistettua yhteistyöpolkua **{s['theme_country_pairs_unlinked']}**.", "",
          "| Teema | Maat | Hankkeita | Yhteys |", "|---|---|---|---|"]
    for g in a["theme_country_gaps"][:25]:
        L.append(f"| {g['teema']} | {g['a']}–{g['b']} | {g['hankkeita_a']} + {g['hankkeita_b']} | {'kyllä' if g['yhteys'] else 'ei'} |")
    L += ["", "## Saarekkeet", "", "| # | Solmuja | Maat | Hankkeet ja keskukset |", "|---|---|---|---|"]
    for c in a["components"]:
        L.append(f"| {c['komponentti']} | {c['solmuja']} | {c['maat']} | {c['hankkeet_ja_keskukset']} |")
    (ROOT / "analysis" / "raportti.md").write_text("\n".join(L) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
