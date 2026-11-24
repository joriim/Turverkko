"""ETIS-haku (lähde 33): Viron tutkimushankkeet Eesti Teadusinfosüsteemin avoimesta rajapinnasta.

Rajapinta (www.etis.ee:2346/api/project/getitems) ei suodata hakusanalla, joten skripti käy hankkeet läpi
sivuittain (Take/Skip) ja rajaa ne paikallisesti nimestä ja tiivistelmästä (viro ja englanti) yhteisellä
rajauksella sekä virolaisilla suo- ja turvesanoilla. Mukaan hankkeet, jotka päättyvät 2014 tai myöhemmin.
Henkilöiden nimiä ei kirjata. Tulos: hakulahteet/automaattihaku/33-etis-<pvm>.csv. Ei muuta aineistoa.
"""
import datetime, json, re, sys, time, urllib.parse, urllib.request
from yhteinen import SCOPE, EXCLUDE, fold, known, write, UA
from kik import ET_SCOPE

API = "https://www.etis.ee:2346/api/project/getitems"
PAGE, BUDGET_S = 200, 25 * 60


def page(skip):
    url = API + "?" + urllib.parse.urlencode({"Format": "json", "Take": PAGE, "Skip": skip})
    for i in range(3):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=180) as r:
                return json.loads(r.read())
        except Exception as e:  # noqa: BLE001
            print(f"ETIS skip={skip}: {type(e).__name__} {e}", file=sys.stderr)
            time.sleep(10 * (i + 1))
    return None


def year(d):
    m = re.search(r"(\d{4})", d or "")
    return int(m.group(1)) if m else None


def main():
    today = datetime.date.today().isoformat()
    urls, names = known()
    rows, n, skip, t0 = [], 0, 0, time.time()
    while time.time() - t0 < BUDGET_S:
        items = page(skip)
        if not items:
            break
        n += len(items)
        for p in items:
            end, start = year(p.get("ProjectEndDate")), year(p.get("ProjectStartDate"))
            if (end or start or 0) < 2014:
                continue
            name = (p.get("Title") or p.get("TitleEst") or "").strip() or re.sub(r'^\S+ "|"$', "", (p.get("DisplayInfo") or "").strip())
            name_en = (p.get("TitleEng") or "").strip() or re.sub(r'^\S+ "|"$', "", (p.get("DisplayInfoEng") or "").strip())
            ann, ann_en = (p.get("Annotation") or "").strip(), (p.get("AnnotationEng") or "").strip()
            blob = " ".join([name, name_en, ann, ann_en])
            if not (SCOPE.search(blob) or ET_SCOPE.search(blob)) or EXCLUDE.search(blob):
                continue
            nr = (p.get("FinancierProjectNr") or "").strip()
            guid = p.get("Guid") or ""
            url = f"https://www.etis.ee/Portal/Projects/Display/{guid}" if guid else "https://www.etis.ee/Portal/Projects/Index"
            if url in urls or fold(name) in names or fold(name_en) in names:
                continue
            inst = [i.get("Name", "").strip() for i in p.get("Institutions") or [] if i.get("Name")]
            fin = [f.get("Name", "").strip() for f in p.get("FinancingInstitutions") or [] if f.get("Name")]
            prog = (p.get("ProgrammeName") or p.get("OtherProgrammeName") or "").strip()
            horizon = re.search(r"horisont|horizon|h2020", prog, re.I)
            rows.append(dict(
                lahde="33", haettu=today, hakusana="automaattihaku: ETIS-rajapinta, nimi ja tiivistelmä", hanke_nimi=name or name_en,
                lyhenne=(p.get("Acronym") or nr).strip(), maa="EE", alue="", rahasto="Horizon" if horizon else "Kansallinen",
                ohjelmakausi=prog, alku=str(year(p.get("ProjectStartDate")) or ""), loppu=str(end or ""),
                toteuttaja=inst[0] if inst else "", partnerit="; ".join(inst[1:]), budjetti_eur=str(p.get("FinancingInPeriodsTotal") or ""),
                eu_osuus_eur="", kuvaus=((ann or ann_en)[:1700] + (f" Rahoittaja: {', '.join(fin)}." if fin else "") + (f" Hankenumero {nr}." if nr else ""))[:2000],
                tuotokset="", url=url))
        if len(items) < PAGE:
            break
        skip += PAGE
        time.sleep(1)
    rows.sort(key=lambda r: (r["alku"], r["hanke_nimi"]))
    print(f"ETIS: {n} hanketta läpikäyty, {len(rows)} uutta rajaukseen osuvaa" + (" (aikaraja, ei kaikkia)" if time.time() - t0 >= BUDGET_S else ""), file=sys.stderr)
    write(f"33-etis-{today}.csv", rows)


if __name__ == "__main__":
    main()
