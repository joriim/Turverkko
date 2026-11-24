"""KIK-haku (lähde 11): Viron ympäristöinvestointikeskuksen kaikki rahoitetut hankkeet XML-viennistä.

KIK julkaisee koko hankeluettelon kuvauksineen tiedostona projects.xml (päivittyy kerran vuorokaudessa).
Selaimen haku etsii vain hankkeen nimestä; tämä skripti seuloo myös kuvaukset (Projekti_tutvustus) samoilla
rajaustermeillä kuin muut automaattihaut sekä virolaisilla suo- ja turvesanoilla. Mukaan rahoitusvuodet 2014–.
Tulos: hakulahteet/automaattihaku/11-kik-<pvm>.csv tarkistettavaksi. Ei muuta aineistoa.

Hankesivun osoite ei ole XML:ssä, joten url-kenttään tulee KIK:n haku hankkeen nimellä.
"""
import datetime, re, sys, urllib.parse, urllib.request
import xml.etree.ElementTree as ET
from yhteinen import SCOPE, EXCLUDE, fold, known, write, UA

XML = "https://kik.ee/sites/default/files/projects-cron/projects.xml"
# Viron suo- ja turvesanat, joita yhteinen SCOPE ei kata (soo on siellä liian laaja yksinään)
ET_SCOPE = re.compile(
    r"\bsoo(d|de|dest|desse|del|dele|dega|s|st|ga|alad|alade|aladel|aladele|mets\w*|taast\w*|kooslus\w*|elupaig\w*|ökosüsteem\w*)\b|"
    r"kõdusoo\w*|siirdesoo\w*|madalsoo\w*|\braba(de|des|dest|del|s|st|le|ga|mets\w*)?\b|turba(ala\w*|väl\w*|kiht\w*|tootmis\w*|maard\w*|sammal\w*|muld\w*)|"
    r"turvasmul\w*|jääksoo\w*|ammendatud turba|märgala\w*|\blulucf\b|maakasutussektor\w*|kasvuhoonegaaside (heite|heitkogus|inventu)\w*|"
    r"mulla (orgaanilise )?süsiniku?\w*|süsiniku (sidumi|varu)\w*", re.I)
# Väärät osumat: turpeen energiakäyttö, jätevesi, paikannimet (Turba alevik, Tootsi Turvas), opastus ja retket
KIK_EXCLUDE = re.compile(r"katlamaja|turbakütt|kaugkütte|soojus(varustus|trass)|reovee|ühisveevär|veevärg|kanalisatsiooni|"
                         r"turba alevik|tootsi turvas|\bloodusmaja|õppepäev|õppekäik|matk(ad|arada)|laager|konkurss|näitus|"
                         r"festival|trükis|infotahvl|teavitus|lasteaed|lasteaia|\bkool\b|\bkooli\b|õpilas|keskkonnahariduslik|aktiivõpe|õppeprogramm|"
                         r"loodusõpe|keskkonnaõpe|soojus|kompost|biojäätme|jäätmejaam|kütusekvaliteed", re.I)
FUND = {"KP": "Kansallinen", "ÜF": "KF", "UF": "KF", "ERF": "EAKR", "ERDF": "EAKR", "ÕÜF": "JTF", "OÜF": "JTF", "JTF": "JTF"}


def text(x, tag):
    e = x.find(tag)
    return (e.text or "").strip() if e is not None and e.text else ""


def main():
    today = datetime.date.today().isoformat()
    urls, names = known()
    req = urllib.request.Request(XML, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=300) as r:
        root = ET.fromstring(r.read())
    items = root.findall("x")
    rows, seen = [], set()
    for x in items:
        name, desc = text(x, "Projekti_nimi"), text(x, "Projekti_tutvustus")
        year = text(x, "Rahastamise_aasta")
        if not year.isdigit() or int(year) < 2014:
            continue
        blob = name + " " + desc
        if not (SCOPE.search(blob) or ET_SCOPE.search(blob)) or EXCLUDE.search(blob) or KIK_EXCLUDE.search(blob + " " + text(x, "Toetuse_saaja")):
            continue
        key = fold(name)
        if key in names or key in seen:
            continue
        seen.add(key)
        src = text(x, "Rahastusallikas")
        rows.append(dict(
            lahde="11", haettu=today, hakusana="automaattihaku: XML-vienti, nimi ja kuvaus", hanke_nimi=name,
            lyhenne=text(x, "Projekti_number"), maa="EE", alue=text(x, "Maakond"), rahasto=FUND.get(src, ""),
            ohjelmakausi=text(x, "Taotlusvoor"), alku=year, loppu="", toteuttaja=text(x, "Toetuse_saaja"), partnerit="",
            budjetti_eur=text(x, "Projekti_maksumus"), eu_osuus_eur=text(x, "Toetuse_summa") if FUND.get(src) not in ("Kansallinen", "") else "",
            kuvaus=(desc + f" Rahoitus: {text(x, 'RahastusallikasKodulehele')}; tuki {text(x, 'Toetuse_summa')} €; tila {text(x, 'Staatus')}; "
                    f"valdkond {text(x, 'ValdkondKodulehele')}.")[:2000],
            tuotokset="", url="https://kik.ee/et/projektid?" + urllib.parse.urlencode({"name": name, "items_per_page": 100})))
    rows.sort(key=lambda r: (r["alku"], r["hanke_nimi"]))
    print(f"KIK: {len(items)} hanketta XML:ssä, {len(rows)} uutta rajaukseen osuvaa", file=sys.stderr)
    write(f"11-kik-{today}.csv", rows)


if __name__ == "__main__":
    main()
