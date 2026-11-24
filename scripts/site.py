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
import csv, json, os, re, shutil
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
    body = body.replace("<script>", '<script src="assets/common.js"></script>\n<script>TV.nav("kartta.html"); addEventListener("DOMContentLoaded", () => TV.footer());</script>\n<script>', 1)
    return HEAD + head + NAV_FIX + body + "\n</body>\n</html>\n"


# --- Englanninkielinen versio (docs/en/) ----------------------------------------------------
# Käännökset: site/i18n/en.tsv, sarakkeet: tiedosto (index.html, kartta.html, common.js tai *) TAB suomi TAB englanti.
# Katkelmat sisältävät ympäröivät merkit (lainausmerkit, tagit), jotta logiikassa käytetyt arvot eivät muutu.
# Jokaisen katkelman on löydyttävä vähintään kerran, muuten rakennus pysähtyy.
EN_PAGES = ["index.html", "kartta.html", "haku.html", "esitys.html", "ehdota.html"]


def load_tsv():
    rows = []
    for n, line in enumerate((ROOT / "site" / "i18n" / "en.tsv").read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip() or line.startswith("#"):
            continue
        parts = line.split("\t")
        if len(parts) != 3:
            raise SystemExit(f"en.tsv rivi {n}: odotettiin 3 saraketta, saatiin {len(parts)}")
        f, fi, en = (x.replace("\\n", "\n") for x in parts)
        rows.append((f, fi, en, n))
    return rows


def translate(text, key, rows, missing):
    for f, fi, en, n in sorted((r for r in rows if r[0] in (key, "*")), key=lambda r: -len(r[1])):
        if fi in text:
            text = text.replace(fi, en)
        elif f == key:
            missing.append(f"{key}: rivi {n}: {fi[:70]}")
    return text


def build_en(docs):
    rows = load_tsv()
    missing = []
    en = docs / "en"
    en.mkdir()
    js = (docs / "assets" / "common.js").read_text(encoding="utf-8")
    (docs / "assets" / "common.en.js").write_text(translate(js, "common.js", rows, missing), encoding="utf-8")
    for page in EN_PAGES:
        t = (docs / page).read_text(encoding="utf-8")
        t = translate(t, page, rows, missing)
        t = (t.replace('<html lang="fi">', '<html lang="en">').replace('href="assets/', 'href="../assets/')
              .replace('src="assets/common.js"', 'src="../assets/common.en.js"').replace('"fi-FI"', '"en-GB"')
              .replace('href="data/', 'href="../data/').replace('new URL("data/"', 'new URL("../data/"'))
        alt = lambda fi, en: f'<link rel="alternate" hreflang="fi" href="{fi}"><link rel="alternate" hreflang="en" href="{en}">'
        t = t.replace("</head>", alt("../" + page, page) + "</head>", 1) if "</head>" in t else t.replace("<title>", alt("../" + page, page) + "<title>", 1)
        (en / page).write_text(t, encoding="utf-8")
        fi = (docs / page).read_text(encoding="utf-8")
        fi = fi.replace("</head>", alt(page, "en/" + page) + "</head>", 1) if "</head>" in fi else fi.replace("<title>", alt(page, "en/" + page) + "<title>", 1)
        (docs / page).write_text(fi, encoding="utf-8")
    if missing:
        raise SystemExit("Käännöskatkelmia ei löytynyt (päivitä site/i18n/en.tsv):\n  " + "\n  ".join(missing))


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
    vocab = json.loads((ROOT / "site" / "i18n" / "vocab_en.json").read_text(encoding="utf-8"))
    # SEAMK-tunnus vain originaalitiedostona (Kuvapankki): värillinen ja valinnainen valkoinen tummaan tilaan
    find = lambda stem: next((f.name for ext in (".svg", ".png") for f in [pages / "assets" / (stem + ext)] if f.exists()), "")
    logo, logo_dark = find("seamk-tunnus"), find("seamk-tunnus-valkoinen")
    if not logo:
        print("Huom: SEAMK-tunnusta ei ole (site/pages/assets/seamk-tunnus.svg tai .png). Alatunnisteessa näkyy vain julkaisijan nimi.")
    # Kattavuusilmoitus jokaisen sivun yläosaan: hakulahteet/lahteet.csv (sarakkeet haku, aineistossa)
    with open(ROOT / "hakulahteet" / "lahteet.csv", encoding="utf-8") as f:
        src_rows = list(csv.DictReader(f))
    cov = dict(total=len(src_rows),
               full=sum(r["aineistossa"] == "kyllä" and r["haku"] == "haettu" for r in src_rows),
               partial=sum(r["aineistossa"] == "kyllä" and r["haku"] != "haettu" for r in src_rows),
               linked=sum(r["aineistossa"] == "osittain" for r in src_rows),
               searched_not_in=sum(r["aineistossa"] == "ei" and r["haku"] != "hakematta" for r in src_rows),
               todo=sum(r["haku"] == "hakematta" for r in src_rows))
    for src in pages.rglob("*"):
        if src.is_dir():
            continue
        dst = docs / src.relative_to(pages)
        dst.parent.mkdir(parents=True, exist_ok=True)
        if src.suffix in (".html", ".js", ".css"):
            dst.write_text(src.read_text(encoding="utf-8").replace("__REPO_URL__", repo)
                           .replace("__V_EN__", json.dumps(vocab["exact"], ensure_ascii=False))
                           .replace("__V_PREFIX_EN__", json.dumps(list(vocab["prefix"].items()), ensure_ascii=False))
                           .replace("__KATTAVUUS__", json.dumps(cov))
                           .replace("__SEAMK_LOGO__", logo).replace("__SEAMK_LOGO_DARK__", logo_dark), encoding="utf-8")
        else:
            shutil.copy(src, dst)

    (docs / "kartta.html").write_text(kartta(repo, name, ds, net, an), encoding="utf-8")
    for f in DATA_FILES:
        shutil.copy(data / f, docs / "data" / f)
    (docs / "data" / "analysis.json").write_text(json.dumps(an, ensure_ascii=False, indent=1), encoding="utf-8")
    build_en(docs)
    for f in ("turverkko.gexf", "turverkko.cx2"):
        (docs / "data" / f).unlink(missing_ok=True)
    total = sum(p.stat().st_size for p in docs.rglob("*") if p.is_file())
    print(f"docs/: {len(list(docs.rglob('*.html')))} sivua, {total // 1024} kt")


if __name__ == "__main__":
    main()
