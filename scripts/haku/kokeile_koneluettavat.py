"""Kokeilu (vaihe 2): KIK:n XML-vienti, research.fi:n hakuindeksi, ETIS-rajapinnan parametrit, ESfondin taustahaku.
Ajetaan työnkulussa Automaattihaku (kokeilu = true, skripti = kokeile_koneluettavat.py); tulostaa otteet lokiin."""
import json, re, time, urllib.error, urllib.parse, urllib.request

UA = "Turverkko/1.0 (+https://github.com/joriim/Turverkko; avoin tutkimusaineisto)"


def fetch(url, body=None, n=3_000_000, ctype="application/json"):
    req = urllib.request.Request(url, data=body, headers={"User-Agent": UA, "Accept": "*/*", **({"Content-Type": ctype} if body else {})})
    t = time.time()
    try:
        with urllib.request.urlopen(req, timeout=90) as r:
            return r.status, r.headers.get("Content-Type", ""), r.read(n).decode("utf-8", "replace"), time.time() - t
    except urllib.error.HTTPError as e:
        return e.code, "", e.read(2000).decode("utf-8", "replace"), time.time() - t
    except Exception as e:
        return None, f"{type(e).__name__}: {e}", "", time.time() - t


def show(name, url, body=None, n=3_000_000, cut=2500):
    code, ct, b, s = fetch(url, body, n)
    print(f"\n===== {name}: {code} {ct.split(';')[0]} {len(b)} merkkiä {s:.1f} s\n{url}\n{b[:cut]}")
    time.sleep(1.5)
    return b


# KIK: koko XML ja hakukohtainen vienti
x = show("11 KIK projects.xml", "https://kik.ee/sites/default/files/projects-cron/projects.xml", n=200_000_000, cut=3000)
print("KIK XML: <project>-alkioita", len(re.findall(r"<project[ >]", x)), "| tagit:", sorted(set(re.findall(r"<([a-z_]+)>", x[:20000])))[:60])
show("11 KIK export", "https://kik.ee/et/projects/export?name=turba&items_per_page=100", cut=3000)
show("11 KIK hankesivu", "https://kik.ee/et/projektid/kuivendatud-ammendatud-ja-huljatud-turbaalade-korrastamine", cut=0)

# research.fi: kentät ja osumamäärä
b = show("7 research.fi kenttä", "https://researchfi-api-production.2.rahtiapp.fi/portalapi/funding/_search",
         json.dumps({"size": 1, "query": {"query_string": {"query": "turvemaa OR peatland OR suo"}}}).encode(), cut=0)
try:
    d = json.loads(b); h = d["hits"]["hits"][0]["_source"]
    print("OSUMIA:", d["hits"]["total"]); print(json.dumps({k: (str(v)[:120]) for k, v in h.items()}, ensure_ascii=False, indent=0)[:6000])
except Exception as e:
    print("virhe", e)

# ETIS: parametrit
for q in [{"Format": "json", "Take": 1, "SearchType": 1, "SearchValue": "turvas"}, {"Format": "json", "Take": 1, "Search": "turvas"},
          {"Format": "json", "Take": 1, "Title": "turvas"}, {"Format": "json", "Take": 1, "Keyword": "turvas"}]:
    b = show("33 ETIS " + json.dumps(q), "https://www.etis.ee:2346/api/project/getitems?" + urllib.parse.urlencode(q), n=400_000, cut=0)
    try:
        it = json.loads(b); print("RIVEJÄ", len(it), "| ensimmäinen:", (it[0].get("TitleEst") or it[0].get("Title") or "")[:100] if it else "")
        if q.get("SearchType") == 1 and it:
            print(json.dumps({k: str(v)[:100] for k, v in it[0].items()}, ensure_ascii=False)[:5000])
    except Exception as e:
        print("virhe", e)
show("33 ETIS api juuri", "https://www.etis.ee:2346/api", n=100_000, cut=3000)

# ESfondi: taustahaun osoitteet sivun skripteistä
b = show("14 ESfondi sivu", "https://www.esfondi.lv/istenotie-projekti/meklesanas-rezultati-2021-2027?projektanosaukums=k%C5%ABdr", cut=0)
for m in sorted(set(re.findall(r"""(?:fetch|axios\.get|axios\.post|url)\s*\(?\s*[`'"]([^`'"]+)""", b)))[:30]:
    print("KUTSU:", m)
for m in sorted(set(re.findall(r"""["'`](/[^"'`\s]*(?:api|search|projekt|meklesan|json)[^"'`\s]*)""", b, re.I)))[:40]:
    print("POLKU:", m)
i = b.find("istenotie-projekti/istenotie-projekti-2021-2027/")
print("HANKELINKKI:", b[max(0, i - 300):i + 300] if i >= 0 else "ei linkkejä HTML:ssä")
