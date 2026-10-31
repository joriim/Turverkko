"""Kokoaa GitHub Pages -sivun docs/index.html pohjasta site/template.html.

Aineisto upotetaan sivuun, jotta sivu toimii myös ilman palvelinta (tiedostona avattuna).
Samat tiedostot kopioidaan docs/data/-kansioon ladattaviksi.

Aja:  python scripts/site.py   (aja ensin build.py ja analyze.py)
Repon osoite luetaan ympäristömuuttujasta REPO_URL tai tiedostosta site/repo.txt.
"""
import json, os, shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    data = ROOT / "data"
    ds = json.loads((data / "dataset.json").read_text(encoding="utf-8"))
    net = json.loads((data / "network.json").read_text(encoding="utf-8"))
    an = json.loads((data / "analysis.json").read_text(encoding="utf-8"))
    country = {n["id"]: n.get("country") for n in net["nodes"]}
    ds["overlaps"] = sorted(
        [dict(a=e["source"], b=e["target"], score=e["weight"], shared=e["note"].split(","),
              kind="sama maa" if country[e["source"]] == country[e["target"]] else "maiden välinen")
         for e in net["edges"] if e["kind"] == "teemapaallekkaisyys"],
        key=lambda o: -o["score"])
    ds["network"] = net
    ds["analysis"] = an

    repo = os.environ.get("REPO_URL") or (ROOT / "site" / "repo.txt").read_text(encoding="utf-8").strip()
    name = repo.rstrip("/").split("github.com/")[-1]
    html = (ROOT / "site" / "template.html").read_text(encoding="utf-8")
    payload = json.dumps(ds, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    if "OMISTAJA" in repo:  # repoa ei vielä asetettu: jätetään repolinkki pois
        import re
        html = re.sub(r'\s*<p class="note">Aineisto, analyysiskriptit[^\n]*</p>', "", html)
    html = html.replace("__DATA__", payload).replace("__REPO_URL__", repo).replace("__REPO_NAME__", name)

    docs = ROOT / "docs"
    (docs / "data").mkdir(parents=True, exist_ok=True)
    (docs / "index.html").write_text(html, encoding="utf-8")
    (docs / ".nojekyll").write_text("", encoding="utf-8")
    for f in ["nodes.csv", "edges.csv", "network.graphml", "network.json", "dataset.json", "analysis.json"]:
        shutil.copy(data / f, docs / "data" / f)
    print(f"docs/index.html {len(html)//1024} kt")


if __name__ == "__main__":
    main()
