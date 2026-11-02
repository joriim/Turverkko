"""Lähteiden saavutettavuus ja näytevastaukset GitHub Actions -ajosta.

Kirjoittaa:
  hakulahteet/automaattihaku/saavutettavuus.md   taulukko: lähde, osoite, HTTP-tila, sisältötyyppi, koko
  (ympäristömuuttuja NAYTTEET=hakemisto)          raakavastaukset jäsentimien kehittämistä varten
"""
import json, os, sys, time, urllib.parse, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
UA = "Turverkko/1.0 (+https://github.com/joriim/Turverkko; tutkimusaineisto)"
SPARQL = "https://query.linkedopendata.eu/bigdata/namespace/wdq/sparql"

KYSELY = """SELECT ?item ?label WHERE { VALUES ?item { <https://linkedopendata.eu/entity/Q7735782> }
  ?item rdfs:label ?label . FILTER(LANG(?label) = "en") } LIMIT 5"""

CHECKS = [
    ("22", "OpenAIRE Graph v1 projects", "https://api.openaire.eu/graph/v1/projects?search=peatland&pageSize=3"),
    ("22", "OpenAIRE Search API projects", "https://api.openaire.eu/search/projects?keywords=peatland&format=json&size=3"),
    ("1", "Kohesio, hankesivu", "https://kohesio.ec.europa.eu/en/projects/Q7735782"),
    ("1", "Kohesio, API-arvaus", "https://kohesio.ec.europa.eu/api/facet/eu/search/project?language=en&keywords=peat&limit=3"),
    ("1", "Kohesio, entiteetti JSON", "https://linkedopendata.eu/wiki/Special:EntityData/Q7735782.json"),
    ("1", "Kohesio, SPARQL", SPARQL + "?" + urllib.parse.urlencode({"query": KYSELY, "format": "json"})),
    ("1", "Kohesio, data-sivu", "https://kohesio.ec.europa.eu/en/data"),
    ("10", "SweCRIS API", "https://swecris-api.vr.se/v1/projects/organisations?limit=1"),
    ("4", "keep.eu", "https://keep.eu/"),
    ("2", "EU CAP Network", "https://eu-cap-network.ec.europa.eu/projects_en"),
    ("3", "LIFE-haku", "https://webgate.ec.europa.eu/life/publicWebsite/search"),
    ("3", "EEA LIFE MapServer", "https://soer.discomap.eea.europa.eu/arcgis/rest/services/Life/LifeProjects_Dyna_WM/MapServer?f=json"),
    ("5", "EURA 2021", "https://eura2021.fi/"),
    ("7", "research.fi", "https://research.fi/fi/results/fundings"),
    ("8", "Tillväxtverket Projektbanken", "https://projektbank.tillvaxtverket.se/projektbanken2020"),
    ("9", "Landsbygdsnätverket EIP", "https://www.landsbygdsnatverket.se/gronanaringarakis/innovationsstodeteipagri.4.html"),
    ("18", "EPA SAFER", "https://erc.epa.ie/safer/"),
    ("19", "Europa für Niedersachsen", "https://www.europa-fuer-niedersachsen.niedersachsen.de/"),
    ("20", "DVS EIP-Agrar", "https://www.dvs-gap-netzwerk.de/"),
    ("21", "Förderkatalog", "https://foerderportal.bund.de/foekat/jsp/StartAction.do"),
]


def fetch(url, timeout=30):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json, text/html;q=0.8, */*;q=0.5"})
    t = time.time()
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            body = r.read(400_000)
            return r.status, r.headers.get("Content-Type", ""), body, round(time.time() - t, 1)
    except urllib.error.HTTPError as e:
        return e.code, e.headers.get("Content-Type", ""), e.read(4000), round(time.time() - t, 1)
    except Exception as e:  # verkkovirhe
        return None, type(e).__name__ + ": " + str(e)[:80], b"", round(time.time() - t, 1)


def main():
    out = os.environ.get("NAYTTEET")
    rows = []
    for i, (lahde, nimi, url) in enumerate(CHECKS):
        code, ctype, body, sec = fetch(url)
        rows.append((lahde, nimi, url, code, ctype, len(body), sec))
        print(f"{lahde:>3} {str(code):>4} {sec:>5}s {len(body):>7} t  {nimi}", flush=True)
        if out:
            Path(out).mkdir(parents=True, exist_ok=True)
            ext = "json" if "json" in ctype else "html"
            (Path(out) / f"{i:02d}-{lahde}.{ext}").write_bytes(body)
    md = ["# Lähteiden saavutettavuus GitHub Actionsista", "",
          f"_Ajettu {time.strftime('%Y-%m-%d %H:%M UTC', time.gmtime())} skriptillä `scripts/haku/probe.py`._", "",
          "| Lähde | Kohde | HTTP | Sisältö | Koko | Aika |", "|---|---|---|---|---|---|"]
    for lahde, nimi, url, code, ctype, size, sec in rows:
        md.append(f"| {lahde} | [{nimi}]({url}) | {code or 'virhe'} | {ctype.split(';')[0]} | {size} t | {sec} s |")
    (ROOT / "hakulahteet" / "automaattihaku").mkdir(parents=True, exist_ok=True)
    (ROOT / "hakulahteet" / "automaattihaku" / "saavutettavuus.md").write_text("\n".join(md) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
