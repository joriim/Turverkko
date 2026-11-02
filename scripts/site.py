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
    country = {n["id"]: n.get("country") for n in net["nodes"]}
    ds = dict(ds)
    ds["overlaps"] = sorted(
        [dict(a=e["source"], b=e["target"], score=e["weight"], shared=e["note"].split(","),
              kind="sama maa" if country[e["source"]] == country[e["target"]] else "maiden välinen")
         for e in net["edges"] if e["kind"] == "teemapaallekkaisyys"],
        key=lambda o: -o["score"])
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


def main():
    data = ROOT / "data"
    ds = json.loads((data / "dataset.json").read_text(encoding="utf-8"))
    net = json.loads((data / "network.json").read_text(encoding="utf-8"))
    an = json.loads((data / "analysis.json").read_text(encoding="utf-8"))
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
    total = sum(p.stat().st_size for p in docs.rglob("*") if p.is_file())
    print(f"docs/: {len(list(docs.rglob('*.html')))} sivua, {total // 1024} kt")


if __name__ == "__main__":
    main()
