"""Rakentaa verkostoaineiston lähdetiedostosta src/source.py.

Tuottaa:
  data/nodes.csv, data/edges.csv   – taulukkomuoto (Excel, R, pandas)
  data/network.graphml             – Gephi, Cytoscape, yEd
  data/network.json                – visualisoinnin syöte (kopio docs/data/)
  data/dataset.json                – alkuperäinen hankeaineisto rakenteisena

Aja:  python scripts/build.py
"""
import csv, itertools, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
import source as S  # noqa: E402

# Päällekkäisyys lasketaan tekstistä tiedostossa scripts/overlap.py (ajetaan analyze.py:ssä)


def jaccard(a, b):
    a, b = set(a), set(b)
    return len(a & b) / len(a | b) if a | b else 0.0


def build():
    nodes, edges = [], []
    seen = set()

    def node(id, kind, label, **attrs):
        if id in seen:
            raise SystemExit(f"Kaksi solmua samalla tunnisteella: {id}")
        seen.add(id)
        nodes.append(dict(id=id, kind=kind, label=label, **attrs))

    def edge(src, dst, kind, evidence="", url="", weight=1.0, note=""):
        edges.append(dict(source=src, target=dst, kind=kind, weight=weight,
                          evidence=evidence, url=url, note=note))

    for k, v in S.THEMES.items():
        node(k, "teema", v)
    for p in S.PROGRAMMES:
        node(p["id"], "ohjelma", f'{p["fund"]} {S.COUNTRIES.get(p["country"], p["country"])} {p["period"]}',
             country=p["country"], fund=p["fund"], eur=p["eur"] or "", url=p["url"])
    for p in S.PROJECTS:
        node(p["id"], "hanke", p["name"], country=p["country"], fund=p["fund"], period=p["period"],
             eur_total=p["eur_total"] or "", eur_eu=p["eur_eu"] or "", evidence_level=p["evidence"],
             start=p["start"] or "", end=p["end"] or "", url=p["url"],
             auto_themes=bool(p.get("auto_themes")), imported_from=p.get("imported_from", ""),
             rajaus=p.get("rajaus", "turvemaa"))
        for t in p["themes"]:
            edge(p["id"], t, "teema")
    for c in S.CONTEXT:
        node(c["id"], "vertailukohde", c["name"], country=c["country"], fund=c["fund"], url=c["url"])
        for t in c["themes"]:
            edge(c["id"], t, "teema")
    for h in S.HUBS:
        node(h["id"], "osaamiskeskus", h["name"], country=h["country"], fund=h["fund"],
             status=h["status"], years=h["years"], url=h["url"])
        for pid in h["projects"]:
            edge(pid, h["id"], "kuuluu_keskukseen", evidence="lähde", url=h["url"])
    for o in S.ORGS:
        node(o["id"], "organisaatio", o["name"], country=o["country"], org_type=o["type"])
    for pub in S.PUBS:
        node(pub["id"], "julkaisu", pub["title"], year=pub["year"] or "", pub_type=pub["type"],
             verified=pub["verified"], venue=pub["venue"], url=pub["url"])
        edge(pub["project"], pub["id"], "tuotos", evidence="lähde" if pub["verified"] else "vahvistamatta", url=pub["url"])
        for t in pub["themes"]:
            edge(pub["id"], t, "teema")

    for org, target, role, url in S.PARTICIPATION:
        conf = "päätelty" if "päätelty" in role else "lähde"
        edge(org, target, "osallistuu", evidence=conf, url=url, note=role.replace(" (päätelty)", ""))
    for prog, target in S.FUNDED_BY:
        edge(prog, target, "rahoittaa", evidence="lähde")
    for l in S.LINKS:
        b = l["b"] if l["b"] != "IE" else "IE"
        if b == "IE":  # kumppani vahvistamatta: kytketään Irlannin keskuksiin heikkona
            for h in [h for h in S.HUBS if h["country"] == "IE"]:
                edge(l["a"], h["id"], "yhteistyo", evidence="vahvistamatta", weight=0.3, note=l["note"])
        elif l["kind"] == "dokumentoitu":
            edge(l["a"], b, "yhteistyo", evidence="lähde", note=l["note"])
        else:
            edge(l["a"], b, "ei_kytkosta", evidence="haku", weight=0, note=l["note"])
    dup = {d["a"]: f'{d["alias"]} – {d["note"]}' for d in S.DUPLICATES}
    for n in nodes:
        if n["id"] in dup:
            n["duplicate_note"] = dup[n["id"]]

    items = S.PROJECTS + S.CONTEXT

    ids = {n["id"] for n in nodes}
    bad = [e for e in edges if e["source"] not in ids or e["target"] not in ids]
    if bad:
        raise SystemExit("Särmä viittaa puuttuvaan solmuun: " + json.dumps(bad[:3], ensure_ascii=False))
    return nodes, edges


def write(nodes, edges):
    import networkx as nx
    data = ROOT / "data"
    data.mkdir(exist_ok=True)
    ncols = sorted({k for n in nodes for k in n}, key=lambda k: (k not in ("id", "kind", "label"), k))
    with open(data / "nodes.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=ncols); w.writeheader(); w.writerows(nodes)
    ecols = ["source", "target", "kind", "weight", "evidence", "note", "url"]
    with open(data / "edges.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=ecols); w.writeheader(); w.writerows(edges)

    G = nx.MultiDiGraph()
    for n in nodes:
        G.add_node(n["id"], **{k: ("" if v is None else v) for k, v in n.items() if k != "id"})
    for e in edges:
        G.add_edge(e["source"], e["target"], **{k: ("" if v is None else v) for k, v in e.items() if k not in ("source", "target")})
    nx.write_graphml_xml(G, data / "network.graphml")  # ElementTree: sama tulos lxml:n kanssa ja ilman

    dataset = dict(themes=S.THEMES, countries=S.COUNTRIES, programmes=S.PROGRAMMES, projects=S.PROJECTS,
                   context=S.CONTEXT, hubs=S.HUBS, pubs=S.PUBS, links=S.LINKS, duplicates=S.DUPLICATES,
                   orgs=S.ORGS)
    (data / "dataset.json").write_text(json.dumps(dataset, ensure_ascii=False, indent=1), encoding="utf-8")
    (data / "network.json").write_text(json.dumps(dict(nodes=nodes, edges=edges), ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"Solmuja {len(nodes)}, särmiä {len(edges)}")


def guide():
    """Hakuohjeen rajaus ja ydinsanat src/rajaus.py:stä (yksi lähde)."""
    import rajaus
    p = ROOT / "hakulahteet" / "README.md"
    old = p.read_text(encoding="utf-8")
    new = rajaus.render_guide(old)
    if new != old:
        p.write_text(new, encoding="utf-8")
    miss = rajaus.check()
    if miss:
        print("Ydinsanat, joita koneellinen rajaus ei tunnista (src/rajaus.py):", miss)


if __name__ == "__main__":
    n, e = build()
    write(n, e)
    guide()
