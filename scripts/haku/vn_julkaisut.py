"""Valtioneuvoston julkaisuarkisto (lähde 30): VN TEAS -selvitykset ja ministeriöiden raportit (DSpace 7 -rajapinta).

Hakee julkaisut.valtioneuvosto.fi:n avoimesta hakurajapinnasta (server/api/discover/search/objects) hakusanoilla
ja rajaa osumat yhteisellä rajauksella. Selvitykset ovat usein hankkeiden tuotoksia: rivit tarkistetaan ja
kirjataan joko hankkeina (selvityshanke) tai julkaisuina julkaisupohjaan.
Tulos: hakulahteet/automaattihaku/30-vn-julkaisut-<pvm>.csv tarkistettavaksi. Ei muuta aineistoa.
"""
import datetime, json, sys, time, urllib.parse, urllib.request
from yhteinen import SCOPE, EXCLUDE, fold, known, write, UA

API = "https://julkaisut.valtioneuvosto.fi/server/api/discover/search/objects"
TERMS = ["turvemaa", "turvemaiden", "turve", "suometsä", "suo", "ennallistaminen", "turvepelto", "kosteikkoviljely",
         "maankäyttösektori", "LULUCF", "hiilinielu", "maaperän hiili", "peatland", "torvmark"]


def get(params):
    url = API + "?" + urllib.parse.urlencode(params)
    with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"}), timeout=90) as r:
        return json.loads(r.read())


def meta(item, key):
    return [v.get("value", "") for v in (item.get("metadata") or {}).get(key, [])]


def main():
    today = datetime.date.today().isoformat()
    urls, names = known()
    found = {}
    for term in TERMS:
        pg = 0
        while pg < 20:
            d = get({"query": term, "dsoType": "ITEM", "size": 100, "page": pg})
            sr = d["_embedded"]["searchResult"]
            for o in sr["_embedded"].get("objects", []):
                it = o["_embedded"]["indexableObject"]
                found.setdefault(it["uuid"], (it, set()))[1].add(term)
            info = sr.get("page", {})
            pg += 1
            if pg >= info.get("totalPages", 0):
                break
            time.sleep(1)
        time.sleep(1)
    rows = []
    for uuid, (it, terms) in found.items():
        title = (meta(it, "dc.title") or [it.get("name", "")])[0]
        abstract = " ".join(meta(it, "dc.description.abstract"))
        date = (meta(it, "dc.date.issued") or [""])[0]
        if not date[:4].isdigit() or int(date[:4]) < 2014:
            continue
        if not SCOPE.search(title + " " + abstract + " " + " ".join(meta(it, "dc.subject"))) or EXCLUDE.search(title + " " + abstract):
            continue
        handle = it.get("handle")
        url = f"https://julkaisut.valtioneuvosto.fi/handle/{handle}" if handle else f"https://julkaisut.valtioneuvosto.fi/items/{uuid}"
        if url in urls or fold(title) in names:
            continue
        pub = "; ".join(meta(it, "dc.publisher"))
        series = "; ".join(meta(it, "dc.relation.ispartofseries"))
        orgs = [a for a in meta(it, "dc.contributor.organization") + meta(it, "dc.contributor") if a]
        rows.append(dict(
            lahde="30", haettu=today, hakusana="; ".join(sorted(terms)), hanke_nimi=title, lyhenne="", maa="FI", alue="",
            rahasto="Kansallinen", ohjelmakausi=series, alku=date[:4], loppu="", toteuttaja=orgs[0] if orgs else "",
            partnerit="; ".join(orgs[1:]), budjetti_eur="", eu_osuus_eur="",
            kuvaus=(abstract[:1700] + (f" Julkaisija: {pub}." if pub else ""))[:2000],
            tuotokset="julkaisu " + date[:10], url=url))
    rows.sort(key=lambda r: (r["alku"], r["hanke_nimi"]))
    print(f"VN-julkaisut: {len(found)} osumaa, {len(rows)} uutta rajaukseen osuvaa", file=sys.stderr)
    write(f"30-vn-julkaisut-{today}.csv", rows)


if __name__ == "__main__":
    main()
