"""research.fi-haku (lähde 7): Suomen tutkimusrahoituspäätökset (Suomen Akatemia, säätiöt, Business Finland ym.).

Käyttää research.fi-portaalin omaa hakuindeksiä (Elasticsearch, avoin, ei avainta). Haku kohdistuu hankkeen
nimeen, kuvaukseen ja avainsanoihin suomeksi, ruotsiksi ja englanniksi; osumat rajataan lisäksi yhteisellä
rajauksella (yhteinen.SCOPE). Mukaan rahoituksen alkuvuodet 2014–.
Henkilöiden nimiä ei kirjata: toteuttajaksi tulee organisaatio, jossa rahoitettu työ tehdään.
Tulos: hakulahteet/automaattihaku/7-research-fi-<pvm>.csv tarkistettavaksi. Ei muuta aineistoa.
"""
import datetime, json, sys, urllib.request
from yhteinen import SCOPE, EXCLUDE, fold, known, write, UA

ES = "https://researchfi-api-production.2.rahtiapp.fi/portalapi/funding/_search"
QUERY = ("turve* OR turvemai* OR suo OR soiden OR soilla OR suometsä* OR ojitet* OR ennallist* OR kosteikk* OR rahkasammal* OR "
         "peat* OR mire* OR fen OR fens OR bog OR bogs OR wetland* OR rewet* OR paludicult* OR sphagnum OR \"organic soil\" OR "
         "\"organic soils\" OR \"soil carbon\" OR \"carbon farming\" OR hiiliviljel* OR \"maaperän hiili\" OR hiilinielu* OR LULUCF OR "
         "maankäyttösektori* OR torv* OR myr OR myrar OR våtmark*")
FIELDS = ["projectNameFi", "projectNameEn", "projectNameSv", "projectDescriptionFi", "projectDescriptionEn", "projectDescriptionSv",
          "keywords.keyword"]


def post(body):
    req = urllib.request.Request(ES, data=json.dumps(body).encode(), headers={"User-Agent": UA, "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.loads(r.read())


def s(v):
    return str(v if v is not None else "").strip()


def main():
    today = datetime.date.today().isoformat()
    urls, names = known()
    hits, after = [], None
    while True:
        body = {"size": 500, "sort": [{"projectId": "asc"}],
                "query": {"bool": {"must": [{"query_string": {"query": QUERY, "fields": FIELDS, "default_operator": "OR"}}],
                                   "filter": [{"range": {"fundingStartYear": {"gte": 2014}}}]}}}
        if after:
            body["search_after"] = after
        d = post(body)
        batch = d["hits"]["hits"]
        if not batch:
            break
        hits += batch
        after = batch[-1]["sort"]
        if len(hits) >= 20000:
            break
    rows, seen = [], set()
    for h in hits:
        p = h["_source"]
        name = s(p.get("projectNameFi")) or s(p.get("projectNameEn")) or s(p.get("projectNameSv"))
        desc = s(p.get("projectDescriptionFi")) or s(p.get("projectDescriptionEn")) or s(p.get("projectDescriptionSv"))
        kw = " ".join(k.get("keyword", "") for k in p.get("keywords") or [] if isinstance(k, dict))
        blob = " ".join([name, s(p.get("projectNameEn")), desc, s(p.get("projectDescriptionEn")), kw])
        if not SCOPE.search(blob) or EXCLUDE.search(blob):
            continue
        pid = str(p.get("projectId"))
        url = f"https://research.fi/fi/results/funding/{pid}"
        if url in urls or fold(name) in names or pid in seen:
            continue
        seen.add(pid)
        orgs = []
        for g in p.get("fundingGroupPerson") or []:
            o = s(g.get("fundedPersonOrganizationNameFi")) or s(g.get("fundedPersonOrganizationNameEn"))
            if o and o not in orgs:
                orgs.append(o)
        for g in p.get("organizationConsortium") or []:
            o = s(g.get("consortiumOrganizationNameFi")) or s(g.get("consortiumOrganizationNameEn"))
            if o and o not in orgs:
                orgs.append(o)
        funder = s(p.get("funderNameFi")) or s(p.get("funderNameEn"))
        kind = s(p.get("typeOfFundingNameFi")) or s(p.get("typeOfFundingNameEn"))
        personal = not orgs or "apuraha" in kind.lower() or s(p.get("funderOrganizationType")) == "Säätiö" and not p.get("organizationConsortium")
        rows.append(dict(
            lahde="7", haettu=today, hakusana="automaattihaku: research.fi-hakuindeksi", hanke_nimi=name, lyhenne=s(p.get("funderProjectNumber")),
            maa="FI", alue="", rahasto="Kansallinen", ohjelmakausi=s(p.get("callProgrammeNameFi")) or s(p.get("callProgrammeNameEn")),
            alku=s(p.get("fundingStartYear")), loppu=s(p.get("fundingEndDate"))[:10] or s(p.get("fundingEndYear")),
            toteuttaja=orgs[0] if orgs else "", partnerit="; ".join(orgs[1:]), budjetti_eur=str(p.get("amount_in_EUR") or ""), eu_osuus_eur="",
            kuvaus=(desc[:1700] + f" Rahoittaja: {funder}; {kind}." + (" Henkilökohtainen apuraha." if personal and not orgs else ""))[:2000],
            tuotokset="", url=url))
    rows.sort(key=lambda r: (r["alku"], r["hanke_nimi"]))
    print(f"research.fi: {len(hits)} osumaa, {len(rows)} uutta rajaukseen osuvaa", file=sys.stderr)
    write(f"7-research-fi-{today}.csv", rows)


if __name__ == "__main__":
    main()
