"""Automaattihakujen yhteiset apufunktiot: HTTP, CSV-muoto ja jo aineistossa olevien hankkeiden tunnistus."""
import csv, json, re, sys, time, unicodedata, urllib.error, urllib.parse, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "hakulahteet" / "automaattihaku"
UA = "Turverkko/1.0 (+https://github.com/joriim/Turverkko; avoin tutkimusaineisto)"
FIELDS = ["lahde", "haettu", "hakusana", "hanke_nimi", "lyhenne", "maa", "alue", "rahasto", "ohjelmakausi", "alku", "loppu",
          "toteuttaja", "partnerit", "budjetti_eur", "eu_osuus_eur", "kuvaus", "tuotokset", "url"]

# Rajaus (SCHEMA.md): hankkeen nimen, tiivistelmän tai avainsanojen on osuttava johonkin näistä
SCOPE = re.compile(
    r"peat|bog\b|bogs\b|mire|fen\b|fens\b|wetland|paludicult|sphagnum|organic soil|histosol|rewet|drain|"
    r"soil (organic )?carbon|soil c\b|carbon farming|carbon sequestration|soil (greenhouse|ghg|emission|respiration)|"
    r"nitrous oxide|n2o|methane|lulucf|land.use (sector|emission|change)|emission factor|eddy covariance|"
    r"turve|suo\b|soiden|torv|myr\b|våtmark|kūdr|purv|turba|raba\b|moor", re.I)
EXCLUDE = re.compile(r"hydrogen|vety|marine sediment|ocean|lake sediment only|permafrost thaw on mars", re.I)


def get(url, params=None, accept="application/json", tries=3, timeout=60):
    if params:
        url += ("&" if "?" in url else "?") + urllib.parse.urlencode(params, doseq=True)
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": accept})
            with urllib.request.urlopen(req, timeout=timeout) as r:
                body = r.read()
                return json.loads(body) if "json" in accept else body.decode("utf-8", "replace")
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503, 504) and i < tries - 1:
                time.sleep(5 * (i + 1)); continue
            raise
        except (urllib.error.URLError, TimeoutError):
            if i < tries - 1:
                time.sleep(5 * (i + 1)); continue
            raise


def fold(s):
    s = unicodedata.normalize("NFKD", (s or "").lower())
    return re.sub(r"[^a-z0-9]+", " ", "".join(c for c in s if not unicodedata.combining(c))).strip()


def known():
    """Jo aineistossa tai tuloskansiossa olevat osoitteet ja nimet (jotta niitä ei ehdoteta uudelleen)."""
    urls, names = set(), set()
    ds = ROOT / "data" / "dataset.json"
    if ds.exists():
        d = json.loads(ds.read_text(encoding="utf-8"))
        for p in d.get("projects", []) + d.get("context", []):
            names.add(fold(p.get("name")))
            urls.update(u for u in [p.get("url")] + p.get("urls", []) if u)
        for r in d.get("removed", []):
            names.add(fold(r.get("name")))
    for f in list((ROOT / "hakulahteet" / "tulokset").glob("*.csv")) + list(OUT.glob("*.csv")):
        with open(f, encoding="utf-8-sig") as fh:
            for r in csv.DictReader(fh):
                names.add(fold(r.get("hanke_nimi"))); urls.add(r.get("url", ""))
    return urls, names


def write(name, rows):
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / name
    with open(path, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=FIELDS, quoting=csv.QUOTE_MINIMAL)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in FIELDS})
    print(f"{path.relative_to(ROOT)}: {len(rows)} riviä", file=sys.stderr)
    return path
