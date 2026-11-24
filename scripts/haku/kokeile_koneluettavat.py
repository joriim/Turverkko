"""Kokeilu: vastaavatko koneluettavat hakuosoitteet GitHubin palvelimelta, ja miltä vastaus näyttää.
Ajetaan työnkulussa Automaattihaku (kokeilu = true, skripti = kokeile_koneluettavat.py); tulostaa otteet lokiin."""
import re, time, urllib.error, urllib.parse, urllib.request

UA = "Turverkko/1.0 (+https://github.com/joriim/Turverkko; avoin tutkimusaineisto)"
LIFE_MS = "https://soer.discomap.eea.europa.eu/arcgis/rest/services/Life/LifeProjects_Dyna_WM/MapServer"
Q = urllib.parse.quote
CHECKS = [
    ("3 LIFE MapServer, tasot", LIFE_MS + "?f=json", None),
    ("3 LIFE MapServer, taso 0 kenttiä", LIFE_MS + "/0?f=json", None),
    ("3 LIFE MapServer, kysely", LIFE_MS + "/0/query?" + urllib.parse.urlencode({"where": "1=1", "outFields": "*", "resultRecordCount": 2, "f": "json"}), None),
    ("7 research.fi ES funding", "https://researchfi-api-production.2.rahtiapp.fi/portalapi/funding/_search",
     b'{"size":1,"query":{"query_string":{"query":"peatland"}}}'),
    ("7 research.fi avoin API", "https://researchfi-api-production.2.rahtiapp.fi/v1/fundingdecisions?" + urllib.parse.urlencode({"Keyword": "suo", "PageSize": 2}), None),
    ("11 KIK nimihaku", "https://kik.ee/et/projektid?" + urllib.parse.urlencode({"name": "turba", "items_per_page": 100}), None),
    ("14 ESfondi 2021-27", "https://www.esfondi.lv/istenotie-projekti/meklesanas-rezultati-2021-2027?projektanosaukums=" + Q("kūdr"), None),
    ("14 ESfondi 2014-20", "https://www.esfondi.lv/istenotie-projekti/meklesanas-rezultati?projektanosaukums=" + Q("kūdr"), None),
    ("20 DVS projektisuche", "https://www.dvs-gap-netzwerk.de/agrar-umwelt/eip-agri/eip-projekt-datenbank/projektsuche/?tx_solr%5Bq%5D=Moor", None),
    ("24 EURA 2014 etusivu", "https://www.eura2014.fi/rrtiepa/", None),
    ("30 VN julkaisut OAI", "https://julkaisut.valtioneuvosto.fi/oai/request?verb=Identify", None),
    ("30 VN julkaisut DSpace 7 haku", "https://julkaisut.valtioneuvosto.fi/server/api/discover/search/objects?query=turvemaa&size=2", None),
    ("30 VN julkaisut DSpace 6 REST", "https://julkaisut.valtioneuvosto.fi/rest/items?limit=1", None),
    ("33 ETIS API projektit", "https://www.etis.ee:2346/api/project/getitems?" + urllib.parse.urlencode({"Format": "json", "Take": 2, "SearchType": 3, "SearchValue": "turvas"}), None),
    ("33 ETIS portaali", "https://www.etis.ee/Portal/Projects/Index", None),
    ("26 Hiilestä kiinni", "https://mmm.fi/maankayttosektorin-ilmastosuunnitelma/hankkeet", None),
    ("28 MAKERA", "https://mmm.fi/mato/rahoitetut-hankkeet", None),
]


def fetch(url, body):
    req = urllib.request.Request(url, data=body, headers={"User-Agent": UA, "Accept": "application/json, text/html;q=0.8, */*;q=0.5",
                                                         **({"Content-Type": "application/json"} if body else {})})
    t = time.time()
    try:
        with urllib.request.urlopen(req, timeout=40) as r:
            return r.status, r.headers.get("Content-Type", ""), r.read(600_000).decode("utf-8", "replace"), time.time() - t
    except urllib.error.HTTPError as e:
        return e.code, e.headers.get("Content-Type", ""), e.read(3000).decode("utf-8", "replace"), time.time() - t
    except Exception as e:
        return None, f"{type(e).__name__}: {str(e)[:120]}", "", time.time() - t


for name, url, body in CHECKS:
    code, ctype, b, sec = fetch(url, body)
    print(f"\n===== {name}: {code} {ctype.split(';')[0]} {len(b)} merkkiä {sec:.1f} s\n{url}")
    if "json" in ctype or b.lstrip()[:1] in ("{", "["):
        print(b[:2500])
    else:
        t = re.search(r"<title[^>]*>(.*?)</title>", b, re.S)
        print("TITLE:", (t.group(1).strip() if t else "")[:120])
        print("LOMAKKEET:", re.findall(r"<form[^>]*>", b, re.I)[:5])
        print("KENTÄT:", sorted(set(re.findall(r"<(?:input|select)[^>]*name=[\"']([^\"']+)", b, re.I)))[:40])
        links = re.findall(r'href="([^"]+)"[^>]*>([^<]{8,140})<', b)
        keep = [l for l in links if re.search(r"projekt|project|hanke|detail|istenotie|item|handle|eip", l[0], re.I)]
        for h, txt in keep[:25]:
            print("LINKKI:", h[:140], "|", txt.strip()[:100])
        m = re.search(r"(\d[\d\s]*)\s*(tulemus|rezult|Treffer|Ergebnis|results|hakutulos)", b, re.I)
        print("OSUMIA:", m.group(0) if m else "")
        txt = re.sub(r"\s+", " ", re.sub(r"<script.*?</script>|<style.*?</style>|<[^>]+>", " ", b, flags=re.S))
        print("TEKSTI:", txt[:1500])
    time.sleep(1.5)
