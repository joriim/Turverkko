"""Linkkitarkistus: sivuston (docs/) sisäiset linkit ja kaikki ulkoiset osoitteet, myös aineiston lähde-URLit.

Sisäiset linkit tarkistetaan tiedostoina kummassakin julkaisumuodossa (sivusto juuressa ja docs/-polussa).
Ulkoiset osoitteet haetaan verkosta. 401/403/429 merkitään "estetty": sivusto torjuu automaattiset haut,
mutta linkki voi toimia selaimessa.

Aja:  python scripts/linkit.py [--vain-sisaiset]
Tulos: analysis/linkit.md (vain verkkohaun kanssa) ja yhteenveto tulosteeseen.
"""
import concurrent.futures as cf, html, json, re, sys, urllib.error, urllib.parse, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
ATTR = re.compile(r'''(?:href|src)=["']([^"'#]+)(?:#[^"']*)?["']''')
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36 Turverkko-linkkitarkistus"
SKIP = ("mailto:", "javascript:", "data:", "tel:")
IGNORE_HOSTS = {"fonts.googleapis.com", "fonts.gstatic.com"}


def site_links():
    """Palauttaa (sisäiset puuttuvat, ulkoiset {url: {sivut}})."""
    missing, external = [], {}
    for page in sorted(DOCS.rglob("*.html")):
        rel = page.relative_to(DOCS).as_posix()
        for raw in ATTR.findall(page.read_text(encoding="utf-8")):
            url = html.unescape(raw.strip())
            if not url or url.startswith(SKIP) or "${" in url or "__" in url:
                continue
            if url.startswith(("http://", "https://")):
                external.setdefault(url, set()).add(rel)
                continue
            target = (page.parent / urllib.parse.unquote(url.split("?")[0])).resolve()
            if target.is_dir():
                target = target / "index.html"
            if not target.exists() or DOCS.resolve() not in target.parents and target != DOCS.resolve():
                missing.append((rel, url))
    return missing, external


def data_links(external):
    ds = json.loads((ROOT / "data" / "dataset.json").read_text(encoding="utf-8"))
    for key in ("projects", "hubs", "pubs", "context", "programmes", "links"):
        for row in ds.get(key, []):
            if isinstance(row, dict) and row.get("url", "").startswith("http"):
                external.setdefault(row["url"], set()).add(f"aineisto:{key}:{row.get('id', row.get('a', ''))}")


def check(url):
    for method in ("HEAD", "GET"):
        try:
            req = urllib.request.Request(url, method=method, headers={"User-Agent": UA, "Accept": "*/*"})
            with urllib.request.urlopen(req, timeout=25) as r:
                return r.status, r.geturl()
        except urllib.error.HTTPError as e:
            if method == "HEAD" and e.code in (400, 403, 404, 405, 429, 500, 501):
                continue
            return e.code, url
        except Exception as e:
            if method == "HEAD":
                continue
            return type(e).__name__ + ": " + str(e)[:80], url
    return "?", url


def classify(code):
    if code == 200 or (isinstance(code, int) and 200 <= code < 400):
        return "ok"
    if code in (401, 403, 429):
        return "estetty"
    return "rikki"


def main():
    missing, external = site_links()
    print(f"Sisäiset linkit: {len(missing)} rikki")
    for page, url in missing:
        print(f"  RIKKI {page} -> {url}")
    if "--vain-sisaiset" in sys.argv:
        sys.exit(1 if missing else 0)
    data_links(external)
    urls = sorted(u for u in external if urllib.parse.urlparse(u).hostname not in IGNORE_HOSTS)
    with cf.ThreadPoolExecutor(8) as ex:
        results = dict(zip(urls, ex.map(check, urls)))
    rows = {"rikki": [], "estetty": [], "ok": []}
    for u in urls:
        code, final = results[u]
        rows[classify(code)].append((u, code, final, sorted(external[u])))
    print(f"Ulkoiset osoitteet: {len(urls)}; ok {len(rows['ok'])}, estetty {len(rows['estetty'])}, rikki {len(rows['rikki'])}")
    out = ["# Linkkitarkistus", "", "_Generoitu skriptillä `scripts/linkit.py` (GitHub Actions, työnkulku Linkkitarkistus)._", "",
           f"Sisäisiä rikkinäisiä linkkejä {len(missing)}. Ulkoisia osoitteita {len(urls)}: toimii {len(rows['ok'])}, "
           f"estää automaattisen haun {len(rows['estetty'])}, rikki {len(rows['rikki'])}.", ""]
    for page, url in missing:
        out.append(f"- sisäinen: `{page}` → `{url}`")
    for title, key in (("Rikki", "rikki"), ("Estää automaattisen haun (tarkista selaimella)", "estetty")):
        out += ["", f"## {title}", "", "| Tila | Osoite | Missä |", "|---|---|---|"]
        for u, code, final, where in rows[key]:
            out.append(f"| {code} | {u} | {', '.join(where[:4])}{' …' if len(where) > 4 else ''} |")
            print(f"  {key.upper()} {code} {u}  <- {', '.join(where[:3])}")
    (ROOT / "analysis" / "linkit.md").write_text("\n".join(out) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
