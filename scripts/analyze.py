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

import overlap as OV

ROOT = Path(__file__).resolve().parents[1]
ACTOR_KINDS = {"organisaatio", "hanke", "osaamiskeskus", "vertailukohde"}
COLLAB_EDGES = {"osallistuu", "kuuluu_keskukseen", "yhteistyo"}
COPUB_EDGE = "yhteisjulkaisu"   # organisaatioiden yhteisjulkaisut: erillinen näyttö, raportoidaan rinnakkain
THIS_YEAR = 2026     # päättyneet hankkeet = loppuvuosi ennen tätä (kiinteä, jotta tulokset ovat toistettavia)
MAX_HOPS = 3          # polku ≤ 3 askelta = toimijat tuntevat toisensa (esim. yhteinen organisaatio = 2)


def load():
    net = json.loads((ROOT / "data" / "network.json").read_text(encoding="utf-8"))
    return {n["id"]: n for n in net["nodes"]}, net["edges"]


def collab_graph(nodes, edges, include_unverified=True, copubs=False):
    G = nx.Graph()
    for i, n in nodes.items():
        if n["kind"] in ACTOR_KINDS:
            G.add_node(i, **n)
    for e in edges:
        if (e["kind"] in COLLAB_EDGES or (copubs and e["kind"] == COPUB_EDGE)) and e["source"] in G and e["target"] in G:
            if not include_unverified and e["evidence"] == "vahvistamatta":
                continue
            G.add_edge(e["source"], e["target"], kind=e["kind"], evidence=e["evidence"])
    return G


def duplicates(projects, actors, pairs):
    """Hankeparit, jotka ovat todennäköisesti sama hanke: sama maa ja samat alku- ja loppuvuodet sekä
    yhteinen organisaatio tai hyvin samankaltainen teksti. Lähteet eri (tai toinen käsin kuratoitu)."""
    texts = {i: OV.text_of(p) for i, p in projects.items()}
    vec, cvec = OV.vectors(texts), OV.concept_vectors(texts)
    sim = lambda a, b: OV.cosine(vec[a], vec[b]) if a in vec and b in vec else 0.0
    csim = lambda a, b: OV.cosine(cvec[a], cvec[b]) if a in cvec and b in cvec else 0.0
    src = lambda p: (p.get("imported_from") or "käsin").split("-")[0]
    ids = sorted(i for i, p in projects.items() if p.get("start") and p.get("end"))
    out = []
    for x, a in enumerate(ids):
        for b in ids[x + 1:]:
            pa, pb = projects[a], projects[b]
            if pa.get("country") != pb.get("country") or (pa["start"], pa["end"]) != (pb["start"], pb["end"]):
                continue
            if src(pa) == src(pb) != "käsin":
                continue
            shared = actors.get(a, set()) & actors.get(b, set())
            s, c = round(sim(a, b), 3), round(csim(a, b), 3)
            if (shared and (s >= 0.12 or c >= 0.6)) or s >= 0.35:
                out.append(dict(a=a, a_nimi=pa["name"], a_lahde=src(pa), b=b, b_nimi=pb["name"], b_lahde=src(pb),
                                vuodet=f'{pa["start"]}–{pa["end"]}', yhteiset_toimijat=" ".join(sorted(shared)), samankaltaisuus=s, kasitteet=c,
                                peruste="yhteinen toimija ja samat vuodet" if shared else "samankaltainen teksti ja samat vuodet"))
    return out


def hectares(ds, this_year):
    """Ennallistavien toimenpiteiden hehtaarit: tavoite, raportoitu toteuma ja päättyneiden hankkeiden tavoitteet."""
    import statistics
    R = {"ennallistaminen", "vettäminen", "kosteikko"}
    ps = [p for p in ds["projects"] if p.get("hectares")]
    by_country, by_action, cost = {}, {}, []
    for p in ps:
        c = by_country.setdefault(p["country"], dict(tavoite=0, toteuma=0, paattyneet_tavoite=0, hankkeita=0))
        c["hankkeita"] += 1
        for h in p["hectares"]:
            if h["kind"] == "ohitettu":
                continue
            a = by_action.setdefault(h["action"], dict(tavoite=0, toteuma=0))
            a[h["kind"]] += h["ha"]
            if h["action"] in R:
                c[h["kind"]] += h["ha"]
                if h["kind"] == "tavoite" and (p.get("end") or 9999) < this_year:
                    c["paattyneet_tavoite"] += h["ha"]
        eur = p.get("eur_total") or p.get("eur_eu")
        ha_basis = p.get("ha_target") or p.get("ha_realised")
        if eur and ha_basis:
            cost.append(dict(id=p["id"], nimi=p["name"], maa=p["country"], rahasto=p["fund"], toimenpide=p.get("ha_action") or "",
                             alku=p.get("start") or "", loppu=p.get("end") or "",
                             eur=eur, eur_lahde="kokonaisbudjetti" if p.get("eur_total") else "EU-osuus",
                             ha_tavoite=p.get("ha_target") or "", ha_toteuma=p.get("ha_realised") or "",
                             peruste="tavoite" if p.get("ha_target") else "toteuma",
                             eur_per_ha=round(eur / ha_basis),
                             eur_per_ha_toteuma=round(eur / p["ha_realised"]) if p.get("ha_realised") else "",
                             vertailukelpoinen="kyllä" if p.get("ha_primary") else "ei",
                             huom="; ".join(sorted({h["primary_note"] for h in p["hectares"] if h.get("primary_note")}))))
    cost.sort(key=lambda r: (r["toimenpide"], r["eur_per_ha"]))
    comp = [r for r in cost if r["vertailukelpoinen"] == "kyllä"]

    def stats(rows):
        v = sorted(r["eur_per_ha"] for r in rows)
        if not v:
            return None
        q = statistics.quantiles(v, n=4, method="inclusive") if len(v) >= 2 else [v[0], v[0], v[0]]
        tot_eur, tot_ha = sum(r["eur"] for r in rows), sum(r["ha_tavoite"] or r["ha_toteuma"] for r in rows)
        return dict(n=len(v), mediaani=round(statistics.median(v)), q1=round(q[0]), q3=round(q[2]), min=v[0], max=v[-1],
                    painotettu=round(tot_eur / tot_ha), eur=round(tot_eur), ha=round(tot_ha))
    price_action = {a: stats([r for r in comp if r["toimenpide"] == a]) for a in sorted({r["toimenpide"] for r in comp})}
    by_action_country = {f"{a}|{c}": stats([r for r in comp if r["toimenpide"] == a and r["maa"] == c])
                         for a in sorted({r["toimenpide"] for r in comp}) for c in sorted({r["maa"] for r in comp if r["toimenpide"] == a})}
    med = {c: round(statistics.median([r["eur_per_ha"] for r in comp if r["maa"] == c]))
           for c in sorted({r["maa"] for r in comp})}
    refs = []
    for k in ("programmes", "hubs"):
        for x in ds[k]:
            for h in x.get("hectares", []):
                refs.append(dict(id=x["id"], taso=k, ha=h["ha"], laji=h["kind"], toimenpide=h["action"], vuosi=h["year"], lainaus=h["quote"]))
    return dict(projects_with_ha=len(ps), target_ha=sum(v["tavoite"] for v in by_country.values()),
                realised_ha=sum(v["toteuma"] for v in by_country.values()),
                ended_target_ha=sum(v["paattyneet_tavoite"] for v in by_country.values()),
                by_country=by_country, by_action=by_action, cost_per_ha=cost, median_eur_per_ha=med,
                price_by_action=price_action, price_by_action_country=by_action_country, programme_refs=refs)


def main():
    nodes, edges = load()
    G = collab_graph(nodes, edges)
    Gv = collab_graph(nodes, edges, include_unverified=False)
    Gp = collab_graph(nodes, edges, include_unverified=False, copubs=True)  # hankkeet + yhteisjulkaisut
    comps_p = list(nx.connected_components(Gp))
    copub_cross = sum(1 for e in edges if e["kind"] == COPUB_EDGE and nodes[e["source"]].get("country") != nodes[e["target"]].get("country"))
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

    # 3. Sisällöllinen päällekkäisyys (teksti, ks. scripts/overlap.py) ja puuttuvat yhteydet
    ds = json.loads((ROOT / "data" / "dataset.json").read_text(encoding="utf-8"))
    projects = {p["id"]: p for p in ds["projects"]}
    projects.update({c["id"]: dict(c, start=None, end=None) for c in ds["context"]})
    actors = defaultdict(set)
    for e in edges:
        if e["kind"] == "osallistuu" and nodes.get(e["source"], {}).get("kind") == "organisaatio":
            actors[e["target"]].add(e["source"])

    def distance(a, b):  # yhteys hankkeiden tai yhteisjulkaisujen kautta
        try:
            return nx.shortest_path_length(Gp, a, b)
        except (nx.NetworkXNoPath, nx.NodeNotFound):
            return None

    pairs, sensitivity, compared = OV.compute(projects, distance, lambda i: actors.get(i, set()), max_hops=MAX_HOPS)
    miss = [dict(m, paras_naytto=max(int(projects[m["a"]].get("evidence") or 0), int(projects[m["b"]].get("evidence") or 0)))
            for m in pairs if m["tyyppi"] not in ("yhteydessä", "saman kokonaisuuden osat")]
    write_csv(out / "paallekkaisyydet.csv", pairs)
    write_csv(out / "puuttuvat_yhteydet.csv", miss)
    write_csv(out / "herkkyys.csv", sensitivity)

    # 3b. Kaksoisehdokkaat: sama hanke eri lähteistä eri nimillä (esim. EURA suomeksi, Kohesio englanniksi)
    dups = duplicates(projects, actors, pairs)
    import datetime
    ha = hectares(ds, THIS_YEAR)
    write_csv(out / "hehtaarit.csv", [dict(maa=c, **v) for c, v in sorted(ha["by_country"].items())])
    write_csv(out / "hehtaarihinta.csv", ha["cost_per_ha"])
    write_csv(out / "kaksoisehdokkaat.csv", dups)

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
                linked = any(nx.has_path(Gp, x, y) and nx.shortest_path_length(Gp, x, y) <= MAX_HOPS
                             for x in A for y in B if x in Gp and y in Gp)
                gaps.append(dict(teema=t, a=ca, b=cb, hankkeita_a=len(A), hankkeita_b=len(B), yhteys=linked))
    gaps.sort(key=lambda g: (g["yhteys"], -(g["hankkeita_a"] * g["hankkeita_b"])))

    analysis = dict(
        params=dict(max_hops=MAX_HOPS, overlap_threshold=OV.DEFAULT_THRESHOLD, overlap_method="tekstin TF-IDF + monikielinen käsitesanasto, kosini",
                    compared_projects=compared),
        summary=dict(actors=Gv.number_of_nodes(), collab_edges=Gv.number_of_edges(), unverified_edges=G.number_of_edges() - Gv.number_of_edges(), components=len(comps),
                     largest_component=len(comps[0]),
                     components_multi=sum(1 for r in comp_rows if len(r["hankkeet_ja_keskukset"].split()) > 1), multi_country_components=sum(1 for r in comp_rows if r["maita"] > 1),
                     cross_country_edges=sum(cross.values()), overlap_pairs=len(pairs), missing_links=len(miss),
                     missing_cross_country=sum(1 for m in miss if m["tyyppi"] == "puuttuva yhteys"),
                     parallel_unlinked=sum(1 for m in miss if m["tyyppi"] == "rinnakkainen ilman yhteyttä"),
                     sequential_unlinked=sum(1 for m in miss if m["tyyppi"] == "peräkkäiset samassa maassa"),
                     overlap_connected=sum(1 for m in pairs if m["tyyppi"] == "yhteydessä"),
                     overlap_family=sum(1 for m in pairs if m["tyyppi"] == "saman kokonaisuuden osat"),
                     duplicate_candidates=len(dups),
                     copub_edges=sum(1 for e in edges if e["kind"] == COPUB_EDGE), copub_cross_country=copub_cross,
                     components_with_copubs=len(comps_p),
                     multi_country_components_with_copubs=sum(1 for c in comps_p if len({nodes[i].get("country") for i in c} - {"", None}) > 1), theme_country_pairs=len(gaps), theme_country_pairs_unlinked=sum(1 for g in gaps if not g["yhteys"])),
        components=comp_rows, organisations=org_rows, overlaps=pairs, missing_links=miss, sensitivity=sensitivity,
        overlap_types=OV.TYPES, duplicate_candidates=dups, hectares=ha,
        cross_country={f"{a}–{b}": n for (a, b), n in cross.items()},
        cross_country_unverified={f"{a}–{b}": n for (a, b), n in cross_unv.items()}, hub_shared_orgs=shared,
        theme_country_gaps=gaps,
    )
    # Asettelu omaan tiedostoonsa: liukulukutulokset voivat vaihdella ympäristöittäin
    (ROOT / "data" / "layout.json").write_text(json.dumps(layout(G), ensure_ascii=False, sort_keys=True), encoding="utf-8")
    (ROOT / "data" / "analysis.json").write_text(json.dumps(analysis, ensure_ascii=False, indent=1), encoding="utf-8")
    report(analysis, nodes)
    print(json.dumps(analysis["summary"], ensure_ascii=False))
    import kattavuus
    kattavuus.main()


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


def fi(v):
    return f"{round(v):,}".replace(",", "\u00a0")


def report(a, nodes):
    s = a["summary"]
    L = ["# Yhteysanalyysi", "",
         "_Generoitu skriptillä `scripts/analyze.py`. Älä muokkaa käsin._", "",
         "## Yhteenveto", "",
         f"- Toimijoita yhteistyöverkossa: **{s['actors']}**, vahvistettuja yhteistyösärmiä **{s['collab_edges']}** (lisäksi {s['unverified_edges']} vahvistamatonta, jotka eivät ole mukana saarekkeissa eikä keskeisyydessä).",
         f"- Erillisiä yhteistyösaarekkeita: **{s['components']}**, joista **{s['components_multi']}** sisältää vähintään kaksi hanketta tai keskusta (loput ovat yksittäisiä hankkeita toteuttajineen). Suurin kattaa {s['largest_component']} toimijaa.",
         f"- Usean maan saarekkeita: **{s['multi_country_components']}**. Maiden välisiä vahvistettuja yhteistyösärmiä: **{s['cross_country_edges']}**.",
         f"- Yhteisjulkaisut mukaan lukien (organisaatioiden yhteiset turvemaa- ja maaperäjulkaisut, OpenAIRE): yhteisjulkaisusärmiä **{s['copub_edges']}**, joista maiden välisiä **{s['copub_cross_country']}**; saarekkeita **{s['components_with_copubs']}**, joista usean maan **{s['multi_country_components_with_copubs']}**. Päällekkäisyysparien yhteys lasketaan tässä verkossa.",
         f"- Sisällöltään samankaltaisia hankepareja (tekstin samankaltaisuus ≥ {a['params']['overlap_threshold']}, {a['params']['compared_projects']} vertailtavaa hanketta): **{s['overlap_pairs']}**. Niistä",
         f"  - rinnakkaisia ilman yhteyttä (sama maa, samaan aikaan, ei yhteistä toimijaa eikä polkua ≤ {a['params']['max_hops']}); kohdekohtaisissa toteutushankkeissa tämä on usein tarkoituksellista, menetelmä- ja suunnitteluhankkeissa se viittaa päällekkäiseen työhön: **{s["parallel_unlinked"]}**",
         f"  - peräkkäisiä samassa maassa ilman yhteyttä: **{s['sequential_unlinked']}**",
         f"  - puuttuvia maiden välisiä yhteyksiä: **{s['missing_cross_country']}**",
         f"  - yhteydessä olevia (yhteinen toimija tai lyhyt polku): **{s['overlap_connected']}**",
         f"  - saman hankekokonaisuuden osia: **{s['overlap_family']}**",
         f"- Todennäköisiä kaksoiskappaleita eri lähteistä (sama maa ja vuodet, yhteinen toimija tai samankaltainen teksti): **{s['duplicate_candidates']}**. Ne tarkistetaan ja yhdistetään `src/tuonti.py`:n `MATCH_EXISTING`-listalla (`analysis/kaksoisehdokkaat.csv`).",
         "", "## Ennallistetut hehtaarit", "",
         f"Hehtaaritieto on **{a['hectares']['projects_with_ha']}** hankkeella. Ennallistavien toimenpiteiden (ennallistaminen, vettäminen, kosteikko) tavoitteita on yhteensä **{fi(a['hectares']['target_ha'])} ha** ja raportoitua toteumaa **{fi(a['hectares']['realised_ha'])} ha**. Jo päättyneiden hankkeiden tavoitteita, joiden toteumaa lähde ei raportoi, on {fi(a['hectares']['ended_target_ha'])} ha.", "",
         "Hehtaarit on kirjattu käsin lainauksineen tiedostoon `hakulahteet/tulokset/hehtaarit/hehtaarit.csv`. Inventoinnit, suunnitelmat, metsitys ja muu pinta-ala näytetään erikseen, eikä niitä lasketa ennallistettuihin.", "",
         "| Maa | Hankkeita | Tavoite ha | Toteuma ha | Päättyneiden tavoite ha |", "|---|---|---|---|---|"]
    L += [f"| {c} | {v['hankkeita']} | {round(v['tavoite'])} | {round(v['toteuma'])} | {round(v['paattyneet_tavoite'])} |" for c, v in sorted(a["hectares"]["by_country"].items())]
    H = a["hectares"]
    L += ["", "### Hinta hehtaaria kohden toimenpiteittäin", "",
          "Budjetti jaettuna hankkeen ennallistavalla hehtaaritavoitteella (tai toteumalla, jos tavoitetta ei ole). Mukana vain hankkeet, joissa hehtaarit ovat päätuotos; pilotit ja kehityshankkeet näkyvät hanketaulukossa mutta eivät mediaaneissa. Budjetti sisältää usein myös suunnittelun, maanhankinnan, seurannan ja viestinnän, joten luku on hankkeen hinta hehtaaria kohden, ei ennallistamistyön yksikköhinta. Summat ovat nimellisiä euroja.", "",
          "| Toimenpide | Hankkeita | Mediaani €/ha | Kvartiiliväli €/ha | Vaihteluväli €/ha | Painotettu €/ha (Σ€ / Σha) |", "|---|---|---|---|---|---|"]
    L += [f"| {k} | {v['n']} | {fi(v['mediaani'])} | {fi(v['q1'])}–{fi(v['q3'])} | {fi(v['min'])}–{fi(v['max'])} | {fi(v['painotettu'])} |" for k, v in H["price_by_action"].items() if v]
    L += ["", "| Toimenpide · maa | Hankkeita | Mediaani €/ha | Painotettu €/ha |", "|---|---|---|---|"]
    L += [f"| {k.replace('|', ' · ')} | {v['n']} | {fi(v['mediaani'])} | {fi(v['painotettu'])} |" for k, v in H["price_by_action_country"].items() if v]
    L += ["", "| Hanke | Maa | Toimenpide | € | ha | €/ha | Vertailukelpoinen |", "|---|---|---|---|---|---|---|"]
    L += [f"| {r['id']} {r['nimi'][:45]} | {r['maa']} | {r['toimenpide']} | {fi(r['eur'])} | {fi(r['ha_tavoite'] or r['ha_toteuma'])} ({r['peruste']}) | {fi(r['eur_per_ha'])} | {r['vertailukelpoinen']}{(': ' + r['huom']) if r['huom'] else ''} |" for r in H["cost_per_ha"]]
    L += ["",
          "", "## Maiden väliset yhteydet", ""]
    L += [f"- {k}: {v} (lähteellä vahvistettu)" for k, v in sorted(a["cross_country"].items())] or ["- Ei vahvistettuja."]
    L += [f"- {k}: {v} (kumppani vahvistamatta)" for k, v in sorted(a["cross_country_unverified"].items())]
    L += ["", "## Välittäjäorganisaatiot (välityskeskeisyys)", "",
          "| Organisaatio | Maa | Hankkeita | Keskuksia | Välityskeskeisyys |", "|---|---|---|---|---|"]
    for r in a["organisations"][:10]:
        L.append(f"| {r['nimi']} | {r['maa']} | {r['hankkeita']} | {r['keskuksia']} | {r['valityskeskeisyys']} |")
    L += ["", "## Osaamiskeskusten yhteiset organisaatiot", ""]
    L += [f"- {x['a']} ↔ {x['b']}: {', '.join(x['organisaatiot'])}" for x in a["hub_shared_orgs"]] or ["- Ei yhteisiä."]
    L += ["", "## Päällekkäisyyden menetelmä", "",
          "Hankkeiden nimi, kuvaus ja tuotokset verrataan TF-IDF-painotettuina. Monikielinen käsitesanasto yhdistää saman asian eri kielillä (esim. turve, peat, torv, kūdra, Torf). Samankaltaisuus on kosini väliltä 0–1. Kynnys on valittu tarkastelemalla pareja käsin, joten alla on tulokset usealla kynnyksellä. Eri kielillä kuvatut ja eri maiden hankkeet saavat järjestelmällisesti matalampia arvoja, koska paikannimet ja kielikohtaiset sanat eivät osu yhteen.", "",
          "Lähdeaineiston kuvaukset ovat lyhyitä (keskimäärin noin 200 merkkiä), mikä heikentää erottelukykyä. Tulokset ovat ehdokkaita tarkistettavaksi, eivät todettuja päällekkäisyyksiä.", "",
          "| Kynnys | Pareja | " + " | ".join(a["overlap_types"]) + " |", "|---|---|" + "---|" * len(a["overlap_types"])]
    for r in a["sensitivity"]:
        L.append(f"| {r['kynnys']} | {r['pareja']} | " + " | ".join(str(r[k]) for k in a["overlap_types"]) + " |")
    for typ in ["rinnakkainen ilman yhteyttä", "puuttuva yhteys", "peräkkäiset samassa maassa"]:
        rows = [m for m in a["missing_links"] if m["tyyppi"] == typ][:15]
        L += ["", f"## {typ.capitalize()} (15 samankaltaisinta)", "", "_" + a["overlap_types"][typ] + "._", "",
              "| A | B | Samankaltaisuus | Yhteiset käsitteet ja sanat | Samaan aikaan |", "|---|---|---|---|---|"]
        L += [f"| {m['a']} {m['a_nimi'][:50]} | {m['b']} {m['b_nimi'][:50]} | {m['score']} | {m['yhteiset']} | {m['samaan_aikaan']} |" for m in rows] or ["| – | – | – | – | – |"]
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
