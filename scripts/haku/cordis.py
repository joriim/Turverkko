"""CORDIS-haku (lähde 23): Horizon 2020- ja Horizon Europe -hankkeet, joissa on osallistuja Turverkon maista.

Lataa CORDISin avoimet CSV-viennit (projektit ja osallistujaorganisaatiot), rajaa hankkeet
turvemaa- ja maaperätermeillä (yhteinen.SCOPE) ja pitää ne, joissa on osallistuja Suomesta, Ruotsista,
Virosta, Latviasta, Irlannista tai Niedersachsenista (NUTS DE9). Muut Saksan osallistujat merkitään DE.
Tulos: hakulahteet/automaattihaku/23-cordis-<pvm>.csv tarkistettavaksi. Ei muuta aineistoa.

Partnerit kirjataan muodossa "Nimi (maa)", ja vain rajauksen maiden osallistujat luetellaan.
"""
import csv, datetime, io, sys, zipfile
from yhteinen import SCOPE, EXCLUDE, fold, known, write, UA
import urllib.request

csv.field_size_limit(10_000_000)
PROGRAMMES = [
    ("Horizon 2020 (2014-2020)", "https://cordis.europa.eu/data/cordis-h2020projects-csv.zip"),
    ("Horizon Europe (2021-2027)", "https://cordis.europa.eu/data/cordis-HORIZONprojects-csv.zip"),
]
IN_SCOPE = {"FI", "SE", "EE", "LV", "IE"}
ROLE_ORDER = {"coordinator": 0, "participant": 1, "partner": 2, "associatedPartner": 3, "thirdParty": 4}


def download(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=300) as r:
        return r.read()


def read_csv(z, stem):
    name = next((n for n in z.namelist() if n.lower().endswith(stem + ".csv")), None)
    if not name:
        raise FileNotFoundError(f"{stem}.csv puuttuu: {z.namelist()}")
    text = z.read(name).decode("utf-8-sig", "replace")
    delim = ";" if text[:2000].count(";") > text[:2000].count(",") else ","
    return list(csv.DictReader(io.StringIO(text), delimiter=delim))


def country_of(o):
    c = (o.get("country") or "").upper()
    if c == "DE":
        return "DE-NI" if (o.get("nutsCode") or "").upper().startswith("DE9") else "DE"
    return c


def money(v):
    v = (v or "").strip().replace(" ", "")
    if not v:
        return ""
    if "," in v and "." not in v:
        v = v.replace(",", ".")
    try:
        return round(float(v))
    except ValueError:
        return ""


def rows_for(label, url, today, urls, names):
    z = zipfile.ZipFile(io.BytesIO(download(url)))
    projects = read_csv(z, "project")
    orgs = read_csv(z, "organization")
    by_proj = {}
    for o in orgs:
        by_proj.setdefault(o.get("projectID"), []).append(o)
    out = []
    for p in projects:
        text = " ".join(p.get(k) or "" for k in ("title", "acronym", "objective", "topics", "keywords"))
        if not SCOPE.search(text) or EXCLUDE.search(text):
            continue
        parts = sorted(by_proj.get(p.get("id"), []), key=lambda o: (ROLE_ORDER.get(o.get("role"), 9), int(o.get("order") or 999)))
        ours = [o for o in parts if country_of(o) in IN_SCOPE | {"DE-NI"}]
        if not ours:
            continue
        link = f"https://cordis.europa.eu/project/id/{p.get('id')}"
        if link in urls or fold(p.get("title")) in names:
            continue
        coord = next((o for o in parts if o.get("role") == "coordinator"), None)
        cc = country_of(coord) if coord else ""
        maa = cc if cc in IN_SCOPE | {"DE-NI"} else ("EU" if len({country_of(o) for o in ours}) > 1 or cc else country_of(ours[0]))
        named = [f"{o.get('name', '').strip()} ({country_of(o)})" for o in ours]
        lead = f"{coord.get('name', '').strip()} ({cc})" if coord else named[0]
        partners = [n for n in named if n != lead]
        others = len(parts) - len(ours)
        objective = " ".join((p.get("objective") or "").split())
        ours_eu = sum(money(o.get("ecContribution")) or 0 for o in ours)
        out.append(dict(
            lahde="23", haettu=today, hakusana="cordis", hanke_nimi=(p.get("title") or "").strip(), lyhenne=p.get("acronym") or "",
            maa=maa, alue="; ".join(sorted({o.get("nutsCode") or "" for o in ours} - {""}))[:120], rahasto="Horizon",
            ohjelmakausi=f"{label} – {p.get('fundingScheme') or ''}".strip(" –"),
            alku=(p.get("startDate") or "")[:10], loppu=(p.get("endDate") or "")[:10],
            toteuttaja=lead, partnerit=";".join(partners),
            budjetti_eur=money(p.get("totalCost")), eu_osuus_eur=money(p.get("ecMaxContribution")),
            kuvaus=(objective[:2000] + f" Aihe: {p.get('topics') or ''}. Osallistujia {len(parts)}, joista {len(ours)} rajauksen maista"
                    + (f" (EU-osuus {ours_eu} €)" if ours_eu else "") + (f"; {others} muista maista." if others > 0 else ".")),
            tuotokset="", url=link))
    return out


def main():
    today = datetime.date.today().isoformat()
    urls, names = known()
    rows, failed = [], []
    for label, url in PROGRAMMES:
        try:
            r = rows_for(label, url, today, urls, names)
            print(f"{label}: {len(r)} uutta", file=sys.stderr)
            rows += r
        except Exception as e:  # noqa: BLE001
            print(f"{label}: virhe {type(e).__name__}: {e}", file=sys.stderr)
            failed.append(label)
    rows.sort(key=lambda r: (r["maa"], r["hanke_nimi"]))
    write(f"23-cordis-{today}.csv", rows)
    if len(failed) == len(PROGRAMMES):
        sys.exit("CORDIS-viennit eivät latautuneet")


if __name__ == "__main__":
    main()
