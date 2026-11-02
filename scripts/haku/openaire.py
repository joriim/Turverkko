"""OpenAIRE Graph API -haku (lähde 22): kansallisten rahoittajien turvemaa- ja maaperähankkeet.

Hakee https://api.openaire.eu/graph/v1/projects -rajapinnasta hakusanoilla, rajaa rahoittajan maan
Turverkon maihin ja jättää EU:n tutkimuksen puiteohjelmat (Horizon, rahoittaja EC) pois.
Tulos: hakulahteet/automaattihaku/22-openaire-<pvm>.csv tarkistettavaksi. Ei muuta aineistoa.

Aja:  python scripts/haku/openaire.py [--max-sivut 5]
"""
import argparse, datetime, sys
from yhteinen import SCOPE, EXCLUDE, fold, get, known, write

API = "https://api.openaire.eu/graph/v1"
COUNTRIES = {"FI": "FI", "SE": "SE", "EE": "EE", "LV": "LV", "IE": "IE", "DE": "DE"}
SKIP_FUNDERS = {"EC"}  # Horizon ja edeltäjät eivät kuulu rajaukseen
TERMS = ["peatland", "peat", "bog", "mire", "fen", "rewetting", "paludiculture", "sphagnum", "organic soil",
         "histosol", "drained peatland", "peatland forest", "soil organic carbon", "soil carbon", "carbon farming",
         "soil greenhouse gas", "nitrous oxide soil", "methane wetland", "LULUCF", "emission factor soil",
         "wetland restoration", "turve", "suo", "torv", "myr", "Moor"]


def project_rows(term, max_pages, today):
    for page in range(1, max_pages + 1):
        d = get(f"{API}/projects", {"search": term, "pageSize": 100, "page": page})
        res = d.get("results") or []
        for p in res:
            yield p
        if len(res) < 100:
            break


def to_row(p, term, today):
    f = next((x for x in p.get("fundings") or [] if x.get("jurisdiction") in COUNTRIES and x.get("shortName") not in SKIP_FUNDERS), None)
    if not f:
        return None
    text = " ".join(str(p.get(k) or "") for k in ("title", "summary", "keywords", "acronym"))
    if not SCOPE.search(text) or EXCLUDE.search(text):
        return None
    g = p.get("granted") or {}
    amount = g.get("fundedAmount") or g.get("totalCost") or 0
    stream = (f.get("fundingStream") or {}).get("description") or ""
    pid = p["id"]
    orgs = []
    try:  # osallistujat, jos rajapinta antaa ne
        o = get(f"{API}/organizations", {"relProjectId": pid, "pageSize": 20})
        orgs = [x.get("legalName") or x.get("legalShortName") for x in o.get("results") or []]
    except Exception as e:  # noqa: BLE001 – osallistujat ovat lisätieto
        print(f"  organisaatiot {pid}: {e}", file=sys.stderr)
    outputs = ""
    try:
        r = get(f"{API}/researchProducts", {"relProjectId": pid, "pageSize": 1})
        n = (r.get("header") or {}).get("numFound")
        if n:
            outputs = f"OpenAIRE: {n} tutkimustuotosta (julkaisut, aineistot)"
    except Exception as e:  # noqa: BLE001
        print(f"  tuotokset {pid}: {e}", file=sys.stderr)
    return dict(
        lahde="22", haettu=today, hakusana=term, hanke_nimi=(p.get("title") or "").strip(), lyhenne=p.get("acronym") or p.get("code") or "",
        maa=COUNTRIES[f["jurisdiction"]], rahasto="Kansallinen",
        ohjelmakausi=" – ".join(x for x in [f.get("name"), stream] if x),
        alku=p.get("startDate") or "", loppu=p.get("endDate") or "",
        toteuttaja=orgs[0] if orgs else "", partnerit=";".join(orgs[1:]),
        budjetti_eur=round(amount) if amount and (g.get("currency") or "EUR") == "EUR" else "",
        kuvaus=((p.get("summary") or "")[:280] + f" Rahoittaja: {f.get('name')}.").strip(),
        tuotokset=outputs,
        url=p.get("websiteUrl") or f"https://explore.openaire.eu/search/project?projectId={pid}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--max-sivut", type=int, default=5)
    a = ap.parse_args()
    today = datetime.date.today().isoformat()
    urls, names = known()
    seen, rows = set(), []
    for term in TERMS:
        n = 0
        try:
            for p in project_rows(term, a.max_sivut, today):
                if p["id"] in seen:
                    continue
                seen.add(p["id"])
                if fold(p.get("title")) in names:
                    continue
                r = to_row(p, term, today)
                if r and r["url"] not in urls:
                    rows.append(r); n += 1
        except Exception as e:  # noqa: BLE001 – yksi hakusana ei kaada ajoa
            print(f"{term}: virhe {e}", file=sys.stderr)
        print(f"{term}: {n} uutta", file=sys.stderr)
    rows.sort(key=lambda r: (r["maa"], r["hanke_nimi"]))
    write(f"22-openaire-{today}.csv", rows)


if __name__ == "__main__":
    main()
