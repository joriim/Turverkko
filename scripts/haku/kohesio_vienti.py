"""Kohesion maakohtaisten vientitiedostojen suodatus (lähde 1).

Kohesio estää palvelinhaut, mutta sen kokonaisviennit saa ladattua selaimella (Kohesio → Data, tai
hakutulosten vienti CSV/XLSX, enintään 5 000 riviä). Tämä skripti lukee viennit, tunnistaa sarakkeet
nimen perusteella, rajaa rivit samoilla rajaustermeillä kuin automaattihaku (scope.py) ja kirjoittaa
uudet ehdokkaat tuontipohjan muotoon. Hakusanojen varaan ei jäädä: koko viennistä suodatetaan.

Aja:  python scripts/haku/kohesio_vienti.py hakulahteet/vienti/kohesio-FI.csv [...]
Tulos: hakulahteet/automaattihaku/1-kohesio-vienti-<pvm>.csv
"""
import csv, datetime, io, sys
from pathlib import Path
from yhteinen import SCOPE, EXCLUDE, fold, known, write

CANDIDATES = {
    "hanke_nimi": ["operation name", "project name", "project title", "name", "title"],
    "kuvaus": ["operation summary", "summary", "description", "objective"],
    "toteuttaja": ["beneficiary name", "beneficiary", "beneficiaries"],
    "budjetti_eur": ["total budget", "total eligible", "total cost", "budget"],
    "eu_osuus_eur": ["eu contribution", "union co-financing", "eu cofinancing", "eu co-financing"],
    "alku": ["start date", "start"], "loppu": ["end date", "end"],
    "rahasto": ["fund"], "ohjelmakausi": ["programme", "program"],
    "maa": ["country"], "alue": ["region", "nuts", "location"],
    "url": ["project url", "kohesio url", "url", "link"], "id": ["item", "id"],
}
FUND = {"erdf": "EAKR", "european regional development fund": "EAKR", "esf+": "ESR+", "esf": "ESR+", "jtf": "JTF",
        "just transition fund": "JTF", "cf": "KF", "cohesion fund": "KF"}


def read(path):
    p = Path(path)
    if p.suffix.lower() in (".xlsx", ".xlsm"):
        import openpyxl  # pip install openpyxl
        ws = openpyxl.load_workbook(p, read_only=True).active
        rows = list(ws.iter_rows(values_only=True))
        head = [str(h or "").strip() for h in rows[0]]
        return [dict(zip(head, ["" if v is None else str(v) for v in r])) for r in rows[1:]]
    text = p.read_text(encoding="utf-8-sig", errors="replace")
    delim = ";" if text[:5000].count(";") > text[:5000].count(",") else ","
    return list(csv.DictReader(io.StringIO(text), delimiter=delim))


def mapping(header):
    low = {h: h.lower().strip() for h in header}
    out = {}
    for field, cands in CANDIDATES.items():
        for c in cands:
            hit = next((h for h, l in low.items() if l == c), None) or next((h for h, l in low.items() if c in l), None)
            if hit and hit not in out.values():
                out[field] = hit
                break
    return out


def main(paths):
    today = datetime.date.today().isoformat()
    urls, names = known()
    rows = []
    for path in paths:
        data = read(path)
        if not data:
            continue
        m = mapping(list(data[0].keys()))
        print(f"{path}: {len(data)} riviä; sarakkeet {m}", file=sys.stderr)
        missing = [f for f in ("hanke_nimi", "kuvaus") if f not in m]
        if missing:
            sys.exit(f"{path}: sarakkeita ei tunnistettu: {missing}. Otsikot: {list(data[0].keys())}")
        n = 0
        for r in data:
            g = lambda f: (r.get(m[f]) or "").strip() if f in m else ""
            text = g("hanke_nimi") + " " + g("kuvaus")
            if not SCOPE.search(text) or EXCLUDE.search(text):
                continue
            url = g("url") or (f"https://kohesio.ec.europa.eu/en/projects/{g('id')}" if g("id").startswith("Q") else "")
            if url in urls or fold(g("hanke_nimi")) in names:
                continue
            fund = FUND.get(g("rahasto").lower(), g("rahasto"))
            rows.append(dict(lahde="1", haettu=today, hakusana="kohesio-vienti", hanke_nimi=g("hanke_nimi"), maa=g("maa"),
                             alue=g("alue"), rahasto=fund, ohjelmakausi=g("ohjelmakausi"), alku=g("alku")[:10], loppu=g("loppu")[:10],
                             toteuttaja=g("toteuttaja"), budjetti_eur=g("budjetti_eur"), eu_osuus_eur=g("eu_osuus_eur"),
                             kuvaus=g("kuvaus"), url=url))
            n += 1
        print(f"  rajaukseen osuu {n}", file=sys.stderr)
    write(f"1-kohesio-vienti-{today}.csv", rows)


if __name__ == "__main__":
    main(sys.argv[1:] or sys.exit(__doc__))
