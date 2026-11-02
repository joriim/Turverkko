"""Julkaisuehdokkaat aineiston hankkeille OpenAIRE Graph API:sta (lähde 22).

Kullekin hankkeelle, jolla on lyhenne (esim. TUPSU, FarmPEAT), haetaan tutkimustuotokset, joissa
lyhenne mainitaan otsikossa, tiivistelmässä tai rahoitustiedoissa. Ehdokas hyväksytään, jos
  - lyhenne esiintyy kokonaisena sanana,
  - tuotos osuu rajaustermeihin (yhteinen.SCOPE) ja
  - julkaisuvuosi on hankkeen alkuvuoden ja loppuvuoden + 3 välillä.
Tulos: hakulahteet/automaattihaku/julkaisut-<pvm>.csv (muoto hakulahteet/julkaisupohja.csv) tarkistettavaksi.
Hyväksytyt rivit siirretään kansioon hakulahteet/tulokset/julkaisut/.

Aja:  python scripts/haku/julkaisut.py [--nayte]
"""
import argparse, csv, datetime, json, re, sys
from yhteinen import ROOT, OUT, SCOPE, get

API = "https://api.openaire.eu/graph/v1/researchProducts"
FIELDS = ["hanke_id", "otsikko", "tekijat", "vuosi", "tyyppi", "julkaisija", "doi", "url", "avoin", "lahde", "haettu"]
FUNDS = {"ELER", "EFRE", "EAKR", "ERDF", "EAFRD", "LIFE", "INTERREG", "HORIZON", "EIP-AGRI", "JTF", "ESR"}
COMMON = {"peat", "moor", "bogs", "farm", "carbon", "climate", "wetland", "water", "soil", "life", "green", "smart", "future",
          "restore", "moss", "network", "nature", "wise", "land", "forest", "turve", "suo", "projekt", "project", "landscape"}


def acronyms(p):
    out = []
    first = re.match(r"\s*([A-ZÄÖÅ][A-Za-zÄÖÅäöå0-9-]{3,})", p.get("name") or "")
    for a in [p.get("acronym") or "", first.group(1) if first else ""]:
        a = a.strip(" –-:,")
        if re.search(r"-[a-zäöå]|-[A-ZÄÖÅ][a-zäöå]", a):  # TKI-pohjainen, Pohjois-Karjala
            continue
        if len(a) >= 4 and sum(c.isupper() for c in a) >= 2 and a.lower() not in COMMON and a.upper() not in FUNDS and a not in out:
            out.append(a)
    return out


def text(r):
    parts = [r.get("mainTitle") or ""] + [d if isinstance(d, str) else json.dumps(d) for d in r.get("descriptions") or []]
    parts.append(json.dumps(r.get("projects") or r.get("fundings") or [], ensure_ascii=False))
    parts.append(json.dumps(r.get("subjects") or [], ensure_ascii=False))
    return " ".join(parts)


def year(r):
    d = r.get("publicationDate") or ""
    return int(d[:4]) if d[:4].isdigit() else None


def doi(r):
    for pid in r.get("pids") or []:
        if (pid.get("scheme") or "").lower() == "doi":
            return pid.get("value", "")
    return ""


def kind(r):
    t = (r.get("type") or "").lower()
    inst = " ".join(json.dumps(i.get("type", "")) for i in r.get("instances") or []).lower()
    if t == "dataset":
        return "aineisto"
    if doi(r).lower().startswith("10.5194/egusphere") or "abstract" in inst:
        return "konferenssiabstrakti"
    if "article" in inst and (r.get("container") or {}).get("name"):
        return "vertaisarvioitu"
    if "report" in inst:
        return "raportti"
    if "thesis" in inst or "master" in inst or "doctoral" in inst:
        return "opinnäyte"
    if "conference" in inst:
        return "konferenssiabstrakti"
    return "muu"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--nayte", action="store_true", help="tulosta ensimmäinen vastaus lokiin")
    a = ap.parse_args()
    today = datetime.date.today().isoformat()
    ds = json.loads((ROOT / "data" / "dataset.json").read_text(encoding="utf-8"))
    have = {(p.get("project"), (p.get("url") or "").lower()) for p in ds["pubs"]}
    rows, printed = [], False
    for p in ds["projects"] + ds["context"]:
        start, end = p.get("start"), p.get("end")
        for acr in acronyms(p):
            try:
                d = get(API, {"search": f'"{acr}"', "pageSize": 50})
            except Exception as e:  # noqa: BLE001
                print(f"{p['id']} {acr}: {e}", file=sys.stderr)
                continue
            res = d.get("results") or []
            if a.nayte and res and not printed:
                print(json.dumps(res[0], ensure_ascii=False)[:4000], file=sys.stderr)
                printed = True
            n = 0
            for r in res:
                t = text(r)
                y = year(r)
                if not re.search(rf"(?<![\w-]){re.escape(acr)}(?![\w-])", t):
                    continue
                if not SCOPE.search(t):
                    continue
                if start and y and not (start - 1 <= y <= (end or start) + 3):
                    continue
                dd = doi(r)
                url = f"https://doi.org/{dd}" if dd else f"https://explore.openaire.eu/search/result?id={r.get('id')}"
                if (p["id"], url.lower()) in have:
                    continue
                have.add((p["id"], url.lower()))
                authors = "; ".join((x.get("fullName") or "") for x in (r.get("authors") or [])[:8])
                rows.append(dict(hanke_id=p["id"], otsikko=(r.get("mainTitle") or "").strip(), tekijat=authors, vuosi=y or "",
                                 tyyppi=kind(r), julkaisija=(r.get("container") or {}).get("name") or r.get("publisher") or "",
                                 doi=dd, url=url,
                                 avoin="kyllä" if "open" in json.dumps(r.get("bestAccessRight") or "").lower() else "ei",
                                 lahde=f"OpenAIRE, lyhenne {acr}", haettu=today))
                n += 1
            print(f"{p['id']} {acr}: {len(res)} osumaa, {n} ehdokasta", file=sys.stderr)
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / f"julkaisut-{today}.csv"
    with open(path, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(rows)
    print(f"{path.relative_to(ROOT)}: {len(rows)} riviä", file=sys.stderr)


if __name__ == "__main__":
    main()
