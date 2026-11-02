"""Kokoaa GitHub Pages -sivuston kansioon docs/.

  docs/index.html    etusivu (site/pages/index.html)
  docs/kartta.html   käsitekartta ja verkosto (site/template.html, aineisto upotettuna)
  docs/haku.html     haku ja hankekortit
  docs/ehdota.html   täydennyslomake → GitHub-issue
  docs/assets/       yhteinen tyyli ja skriptit
  docs/data/         ladattavat ja sivujen käyttämät aineistot

Aja:  python scripts/site.py   (aja ensin build.py ja analyze.py)
Repon osoite luetaan ympäristömuuttujasta REPO_URL tai tiedostosta site/repo.txt.
"""
import json, os, re, shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_FILES = ["nodes.csv", "edges.csv", "network.graphml", "network.json", "dataset.json", "analysis.json"]

HEAD = """<!doctype html>
<html lang="fi">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<link rel="stylesheet" href="assets/style.css">
"""
# Kartan oma tyyli määrittelee body-paddingin; navigaatio venytetään reunasta reunaan.
NAV_FIX = """<style>body>.nav{margin-top:-20px;margin-bottom:8px;margin-inline:calc(-1*max(16px,env(safe-area-inset-left,0px)))}</style>
</head>
<body>
"""


def kartta(repo, name, ds, net, an):
    ds = dict(ds)
    ds["overlaps"] = [dict(a=o["a"], b=o["b"], score=o["score"], shared=[t for t in o["yhteiset"].split(", ") if t],
                           kind=o["tyyppi"], same_time=o["samaan_aikaan"], actors=o["yhteiset_toimijat"])
                      for o in an.get("overlaps", [])]
    ds["network"] = net
    ds["analysis"] = an
    html = (ROOT / "site" / "template.html").read_text(encoding="utf-8")
    payload = json.dumps(ds, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    if "OMISTAJA" in repo:
        html = re.sub(r'\s*<p class="note">Aineisto, analyysiskriptit[^\n]*</p>', "", html)
    html = html.replace("__DATA__", payload).replace("__REPO_URL__", repo).replace("__REPO_NAME__", name)
    html = html.replace("<title>Turverkko</title>", "<title>Kartta ja verkosto – Turverkko</title>", 1)
    i = html.index('<div class="wrap">')
    head, body = html[:i], html[i:]
    body = body.replace("<script>", '<script src="assets/common.js"></script>\n<script>TV.nav("kartta.html");</script>\n<script>', 1)
    return HEAD + head + NAV_FIX + body + "\n</body>\n</html>\n"


# --- Verkostotyökalujen tiedostot (Gephi Lite: GEXF, Cytoscape Web: CX2) --------------------
COLORS = {"FI": "#2f6f86", "SE": "#b38a14", "EE": "#3d7a5a", "LV": "#8b3a52", "IE": "#5b7f2a",
          "DE-NI": "#7a4b2a", "DE-SH": "#8a8f86", "EU": "#5a6b8c"}
KIND_SIZE = {"osaamiskeskus": 14, "hanke": 6, "vertailukohde": 6, "organisaatio": 5, "julkaisu": 3}
COLLAB = {"osallistuu", "kuuluu_keskukseen", "yhteistyo"}
NODE_ATTRS = ["kind", "country", "fund", "period", "org_type", "eur_total", "eur_eu", "evidence_level", "start", "end",
              "year", "pub_type", "status", "url", "themes"]


def tool_graph(ds, net, an):
    """Yhteistyöverkko työkaluja varten: toimijat ja julkaisut, yhteistyö-, tuotos- ja puuttuvat yhteydet."""
    keep = {"organisaatio", "hanke", "osaamiskeskus", "vertailukohde", "julkaisu"}
    themes = {}
    for e in net["edges"]:
        if e["kind"] == "teema":
            themes.setdefault(e["source"], []).append(e["target"])
    pos = an.get("positions", {})
    nodes = []
    for n in net["nodes"]:
        if n["kind"] not in keep:
            continue
        a = {k: n.get(k) for k in NODE_ATTRS if n.get(k) not in (None, "")}
        a["themes"] = ",".join(sorted(themes.get(n["id"], [])))
        a["label"] = n["label"]
        nodes.append((n["id"], a, pos.get(n["id"])))
    ids = {i for i, _, _ in nodes}
    edges = []
    for e in net["edges"]:
        if e["source"] in ids and e["target"] in ids and (e["kind"] in COLLAB or e["kind"] == "tuotos"):
            edges.append((e["source"], e["target"], {"kind": e["kind"], "evidence": e["evidence"] or "", "role": e["note"] or "", "url": e["url"] or ""}))
    for m in an.get("missing_links", []):
        if m["a"] in ids and m["b"] in ids:
            edges.append((m["a"], m["b"], {"kind": "puuttuva_yhteys", "evidence": "laskettu", "role": f'{m["tyyppi"]}: {m["yhteiset"]}',
                                           "url": "", "jaccard": float(m["score"])}))
    # julkaisuille sijainti tekijähankkeen viereen
    for i, (nid, a, p) in enumerate(nodes):
        if p is None:
            src = next((s for s, t, d in edges if t == nid and d["kind"] == "tuotos"), None)
            base = pos.get(src, [0, 0])
            nodes[i] = (nid, a, [base[0] + 0.012 * ((i % 5) - 2), base[1] + 0.02])
    return nodes, edges


def hex_rgb(h):
    h = h.lstrip("#"); return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)


def write_gexf(path, nodes, edges):
    import networkx as nx
    G = nx.MultiDiGraph(name="Turverkko")
    for nid, a, p in nodes:
        r, g, b = hex_rgb(COLORS.get(a.get("country"), "#8a8f86"))
        viz = {"color": {"r": r, "g": g, "b": b, "a": 1.0}, "size": KIND_SIZE.get(a["kind"], 4)}
        if p:
            viz["position"] = {"x": round(p[0] * 1000, 1), "y": round(-p[1] * 1000, 1), "z": 0.0}
        G.add_node(nid, **{k: v for k, v in a.items()}, viz=viz)
    for k, (s, t, d) in enumerate(edges):
        w = d.get("jaccard", 1.0)
        G.add_edge(s, t, key=k, weight=w, **{x: y for x, y in d.items() if x != "jaccard"})
    nx.write_gexf(G, path, version="1.2draft")


def write_cx2(path, nodes, edges, title):
    idmap = {nid: i for i, (nid, _, _) in enumerate(nodes)}
    ntypes = {"name": "string", "label": "string", "kind": "string", "country": "string", "fund": "string", "period": "string",
              "org_type": "string", "url": "string", "themes": "string", "status": "string", "pub_type": "string",
              "eur_total": "double", "eur_eu": "double", "evidence_level": "integer", "start": "integer", "end": "integer",
              "year": "integer", "color": "string", "size": "double"}
    etypes = {"interaction": "string", "evidence": "string", "role": "string", "url": "string", "jaccard": "double"}
    def cast(t, v):
        try:
            return {"double": float, "integer": int}.get(t, str)(v)
        except (TypeError, ValueError):
            return None
    cx_nodes = []
    for nid, a, p in nodes:
        v = {"name": nid}
        for k, val in a.items():
            if k in ntypes and val not in (None, ""):
                c = cast(ntypes[k], val)
                if c is not None:
                    v[k] = c
        v["color"] = COLORS.get(a.get("country"), "#8a8f86")
        v["size"] = float(KIND_SIZE.get(a["kind"], 4) * 4)
        p = p or [0, 0]
        cx_nodes.append({"id": idmap[nid], "x": round(p[0] * 1000, 1), "y": round(p[1] * 1000, 1), "v": v})
    cx_edges = []
    for k, (s, t, d) in enumerate(edges):
        v = {"interaction": d["kind"]}
        for x in ("evidence", "role", "url"):
            if d.get(x):
                v[x] = d[x]
        if "jaccard" in d:
            v["jaccard"] = d["jaccard"]
        cx_edges.append({"id": k, "s": idmap[s], "t": idmap[t], "v": v})
    doc = [
        {"CXVersion": "2.0", "hasFragments": False},
        {"metaData": [{"name": "attributeDeclarations", "elementCount": 1}, {"name": "networkAttributes", "elementCount": 1},
                      {"name": "nodes", "elementCount": len(cx_nodes)}, {"name": "edges", "elementCount": len(cx_edges)}]},
        {"attributeDeclarations": [{"networkAttributes": {"name": {"d": "string"}, "description": {"d": "string"},
                                                          "url": {"d": "string"}, "license": {"d": "string"}},
                                    "nodes": {k: {"d": t} for k, t in ntypes.items()},
                                    "edges": {k: {"d": t} for k, t in etypes.items()}}]},
        {"networkAttributes": [{"name": title, "url": "https://github.com/joriim/Turverkko", "license": "CC BY 4.0",
                                "description": "Turvemaihin ja maaperään liittyvän julkisen TKI-rahoituksen toimijaverkosto. "
                                               "Reunan interaction: osallistuu, kuuluu_keskukseen, yhteistyo, tuotos tai puuttuva_yhteys."}]},
        {"nodes": cx_nodes},
        {"edges": cx_edges},
        {"status": [{"error": "", "success": True}]},
    ]
    path.write_text(json.dumps(doc, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")


def main():
    data = ROOT / "data"
    ds = json.loads((data / "dataset.json").read_text(encoding="utf-8"))
    net = json.loads((data / "network.json").read_text(encoding="utf-8"))
    an = json.loads((data / "analysis.json").read_text(encoding="utf-8"))
    an["positions"] = json.loads((data / "layout.json").read_text(encoding="utf-8"))
    repo = os.environ.get("REPO_URL") or (ROOT / "site" / "repo.txt").read_text(encoding="utf-8").strip()
    name = repo.rstrip("/").split("github.com/")[-1]

    docs = ROOT / "docs"
    if docs.exists():
        shutil.rmtree(docs)
    (docs / "data").mkdir(parents=True)
    (docs / ".nojekyll").write_text("", encoding="utf-8")

    pages = ROOT / "site" / "pages"
    for src in pages.rglob("*"):
        if src.is_dir():
            continue
        dst = docs / src.relative_to(pages)
        dst.parent.mkdir(parents=True, exist_ok=True)
        if src.suffix in (".html", ".js", ".css"):
            dst.write_text(src.read_text(encoding="utf-8").replace("__REPO_URL__", repo), encoding="utf-8")
        else:
            shutil.copy(src, dst)

    (docs / "kartta.html").write_text(kartta(repo, name, ds, net, an), encoding="utf-8")
    for f in DATA_FILES:
        shutil.copy(data / f, docs / "data" / f)
    (docs / "data" / "analysis.json").write_text(json.dumps(an, ensure_ascii=False, indent=1), encoding="utf-8")
    tn, te = tool_graph(ds, net, an)
    write_gexf(docs / "data" / "turverkko.gexf", tn, te)
    write_cx2(docs / "data" / "turverkko.cx2", tn, te, "Turverkko")
    total = sum(p.stat().st_size for p in docs.rglob("*") if p.is_file())
    print(f"docs/: {len(list(docs.rglob('*.html')))} sivua, {total // 1024} kt")


if __name__ == "__main__":
    main()
