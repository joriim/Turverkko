"""Organisaatioiden ROR-tunnisteet ja yhteisjulkaisut turvemaa- ja maaperäaiheista (OpenAIRE, ROR).

1. ROR: kullekin tutkimusorganisaatiolle haetaan ROR-tunniste ROR:n affiliaatiohaulla
   (https://api.ror.org/v2/organizations?affiliation=...). Vain ROR:n itse "chosen"-merkitsemät,
   samassa maassa olevat osumat hyväksytään ehdokkaiksi.
2. OpenAIRE: ROR-tunnisteella haetaan OpenAIRE-organisaatio ja sen rajausaiheiset tutkimustuotokset.
   Kahden organisaation yhteisjulkaisu = sama tuotos molempien listalla.
Tulos: hakulahteet/automaattihaku/ror-<pvm>.csv ja yhteisjulkaisut-<pvm>.csv tarkistettavaksi.
Hyväksytyt: hakulahteet/tulokset/verkosto/ror.csv ja hakulahteet/tulokset/verkosto/yhteisjulkaisut.csv.

Aja:  python scripts/haku/yhteisjulkaisut.py [--nayte] [--max-sivut 5]
"""
import argparse, csv, datetime, itertools, json, os, sys, time
from yhteinen import ROOT, OUT, SCOPE, fold, get

ROR = "https://api.ror.org/v2/organizations"
OA = "https://api.openaire.eu/graph/v1"
RESEARCH_TYPES = {"yliopisto", "amk", "tutkimuslaitos"}
# OpenAIRE sallii enintään neljä loogista operaattoria hakua kohden, joten aiheet haetaan viiden sanan ryhminä
TOPICS = ["peat OR peatland OR peatlands OR bog OR mire", "fen OR rewetting OR paludiculture OR sphagnum OR histosol",
          "turvemaa OR torvmark OR Moorboden OR Wiedervernässung OR kūdra"]
COUNTRY = {"FI": "FI", "SE": "SE", "EE": "EE", "LV": "LV", "IE": "IE", "DE-NI": "DE", "DE-SH": "DE", "DE": "DE"}


def say(*a):
    print(*a, file=sys.stderr, flush=True)


def variants(o):
    """Nimimuodot ROR-hakuun: koko nimi, ilman sulkeita, sulkeiden sisältö ja tuonnin tuntemat viralliset nimet."""
    import re
    sys.path.insert(0, str(ROOT / "src"))
    import tuonti
    name = o["name"]
    out = [name, re.sub(r"\s*\([^)]*\)", "", name).strip()]
    out += re.findall(r"\(([^)]{4,})\)", name)
    out += [sub for sub, oid in tuonti.ORG_CONTAINS if oid == o["id"] and len(sub) > 8]
    return list(dict.fromkeys(v for v in out if v))


def ror_match(o, cc):
    best = None
    for q in variants(o):
        d = get(ROR, {"affiliation": q})
        for it in d.get("items") or []:
            org = it.get("organization") or {}
            loc = ((org.get("locations") or [{}])[0].get("geonames_details") or {}).get("country_code")
            if cc and loc != cc:
                continue
            disp = next((n["value"] for n in org.get("names", []) if "ror_display" in n.get("types", [])), "")
            if it.get("chosen"):
                return org.get("id"), disp, it.get("score"), q
            if (it.get("score") or 0) >= 0.9 and not best:
                best = (org.get("id"), disp, it.get("score"), q + " (ei chosen)")
    return best


def oa_org(ror_id):
    d = get(f"{OA}/organizations", {"pid": ror_id, "pageSize": 5})
    res = d.get("results") or []
    return res[0]["id"] if res else None


def products(oa_id, max_pages):
    out = {}
    for topic in TOPICS:
        out.update(_products(oa_id, topic, max_pages))
    return out


def _products(oa_id, topic, max_pages):
    out = {}
    cursor = "*"
    for _ in range(max_pages):
        d = get(f"{OA}/researchProducts", {"relOrganizationId": oa_id, "search": topic, "pageSize": 50, "cursor": cursor})
        for r in d.get("results") or []:
            t = (r.get("mainTitle") or "") + " " + " ".join(x if isinstance(x, str) else "" for x in r.get("descriptions") or [])
            y = (r.get("publicationDate") or "")[:4]
            if SCOPE.search(t) and (not y.isdigit() or int(y) >= 2014):
                doi = next((p.get("value") for p in r.get("pids") or [] if (p.get("scheme") or "").lower() == "doi"), "")
                out[r["id"]] = (y, doi, (r.get("mainTitle") or "")[:120])
        cursor = (d.get("header") or {}).get("nextCursor")
        if not cursor or not d.get("results"):
            break
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--nayte", action="store_true")
    ap.add_argument("--max-sivut", type=int, default=10)
    a = ap.parse_args()
    today = datetime.date.today().isoformat()
    ds = json.loads((ROOT / "data" / "dataset.json").read_text(encoding="utf-8"))
    known_ror = {}
    f = ROOT / "hakulahteet" / "tulokset" / "verkosto" / "ror.csv"
    if f.exists():
        known_ror = {r["org_id"]: r["ror"] for r in csv.DictReader(open(f, encoding="utf-8-sig")) if r.get("ror")}
    orgs = [o for o in ds["orgs"] if o.get("type") in RESEARCH_TYPES]
    say(f"tutkimusorganisaatioita {len(orgs)}")
    ror_rows, prods = [], {}
    for o in orgs:
        cc = COUNTRY.get(o.get("country") or "", "")
        rid = known_ror.get(o["id"])
        if not rid:
            try:
                m = ror_match(o, cc)
            except Exception as e:  # noqa: BLE001
                say(f"ROR {o['id']}: {e}"); m = None
            if a.nayte and not ror_rows:
                say("ROR-näyte:", json.dumps(get(ROR, {"affiliation": o["name"]}), ensure_ascii=False)[:1500])
            if not m:
                say(f"ROR {o['id']} ({o['name']}): ei varmaa osumaa")
                continue
            rid = m[0]
            ror_rows.append(dict(org_id=o["id"], nimi=o["name"], maa=o.get("country", ""), ror=rid, ror_nimi=m[1], pisteet=m[2], haku=m[3]))
        try:
            oid = oa_org(rid)
            if a.nayte and oid and not prods:
                say("OpenAIRE-organisaatio:", oid)
            p = products(oid, a.max_sivut) if oid else {}
        except Exception as e:  # noqa: BLE001
            body = e.read()[:300] if hasattr(e, "read") else b""
            say(f"OpenAIRE {o['id']}: {type(e).__name__} {e} {body}"); p = {}
        prods[o["id"]] = p
        say(f"{o['id']}: ROR {rid}, OpenAIRE {oid}, rajausaiheisia tuotoksia {len(p)}")
        time.sleep(0.5)
    pairs = []
    for x, y in itertools.combinations(sorted(prods), 2):
        common = prods[x].keys() & prods[y].keys()
        if common:
            items = sorted((prods[x][k] for k in common), reverse=True)
            pairs.append(dict(org_a=x, org_b=y, yhteisjulkaisuja=len(common),
                              vuodet=f"{min(i[0] for i in items if i[0]) if any(i[0] for i in items) else ''}–{max(i[0] for i in items)}",
                              esimerkit="; ".join(f"{i[2]} (doi:{i[1]})" if i[1] else i[2] for i in items[:3])))
    pairs.sort(key=lambda r: -r["yhteisjulkaisuja"])
    OUT.mkdir(parents=True, exist_ok=True)
    for name, rows in ((f"ror-{today}.csv", ror_rows), (f"yhteisjulkaisut-{today}.csv", pairs)):
        with open(OUT / name, "w", encoding="utf-8", newline="") as fh:
            if rows:
                w = csv.DictWriter(fh, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
        say(f"{name}: {len(rows)} riviä")
        if os.environ.get("TULOSTA_CSV"):
            print(f"===== {name}", file=sys.stderr)
            print((OUT / name).read_text(encoding="utf-8"), file=sys.stderr)


if __name__ == "__main__":
    main()
