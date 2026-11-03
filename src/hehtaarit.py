"""Ennallistamisen ja muun maankäytön muutoksen hehtaarit.

Hehtaarit kirjataan käsin tarkistettuun taulukkoon hakulahteet/tulokset/hehtaarit/hehtaarit.csv
lainauksineen, koska automaattinen poiminta sekoittaa kohteen pinta-alan, inventoinnin ja aiemman
tuotantoalan. Tämä moduuli
  - liittää rivit hankkeisiin, ohjelmiin ja keskuksiin (kenttä hectares),
  - laskee hankekohtaiset summat: tavoite ja raportoitu toteuma ennallistavista toimenpiteistä,
  - listaa tarkistamattomat hehtaarimaininnat (candidates), jotta uudet tuonnit tulevat tarkistetuiksi.

Laji:       tavoite | toteuma | ohitettu (maininta tarkistettu, ei koske hankkeen omaa pinta-alaa)
Toimenpide: ennallistaminen | vettäminen | kosteikko  (= ennallistava, lasketaan summiin)
            metsitys | suunnittelu | inventointi | muu (näytetään, ei lasketa ennallistettuihin)
"""
import csv, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FILE = ROOT / "hakulahteet" / "tulokset" / "hehtaarit" / "hehtaarit.csv"
RESTORING = {"ennallistaminen", "vettäminen", "kosteikko"}
KINDS = {"tavoite", "toteuma", "ohitettu"}  # ohitettu = maininta tarkistettu, ei hankkeen pinta-ala
ACTIONS = RESTORING | {"metsitys", "suunnittelu", "inventointi", "muu"}
HA = re.compile(r"(\d[\d  .,]*\d|\d)\s*(ha\b|hectares?|hehtaari\w*|hektar\w*|ha:n)", re.I)


def load():
    if not FILE.exists():
        return []
    rows = []
    for r in csv.DictReader(open(FILE, encoding="utf-8-sig")):
        if r["laji"] not in KINDS or r["toimenpide"] not in ACTIONS:
            raise SystemExit(f"hehtaarit.csv: tuntematon laji tai toimenpide: {r}")
        rows.append(dict(id=r["kohde_id"], level=r["taso"], ha=float(r["ha"]), kind=r["laji"], action=r["toimenpide"],
                         year=int(r["vuosi"]) if r["vuosi"].strip().isdigit() else None, quote=r["lainaus"], note=r["huom"]))
    return rows


def apply(projects, programmes, hubs, context):
    rows = load()
    targets = {x["id"]: x for x in projects + programmes + hubs + context}
    unknown = sorted({r["id"] for r in rows} - set(targets))
    if unknown:
        raise SystemExit(f"hehtaarit.csv: tuntemattomat tunnisteet {unknown}")
    for r in rows:
        t = targets[r["id"]]
        t.setdefault("hectares", []).append({k: r[k] for k in ("ha", "kind", "action", "year", "quote", "note")})
    for p in projects:
        hs = p.get("hectares", [])
        tgt = sum(h["ha"] for h in hs if h["kind"] == "tavoite" and h["action"] in RESTORING)
        real = sum(h["ha"] for h in hs if h["kind"] == "toteuma" and h["action"] in RESTORING)
        p["ha_target"] = tgt or None
        p["ha_realised"] = real or None
        p["ha_other"] = sum(h["ha"] for h in hs if h["action"] not in RESTORING and h["kind"] != "ohitettu") or None
    return rows


def candidates(projects):
    """Hehtaarimaininnat hankkeista, joita ei ole tarkistettu taulukkoon."""
    out = []
    for p in projects:
        if p.get("hectares"):
            continue
        t = " ".join(str(p.get(k) or "") for k in ("name", "outputs", "description", "description_extra"))
        for m in HA.finditer(t):
            out.append(dict(hanke_id=p["id"], nimi=p["name"], maininta=" ".join(t[max(0, m.start() - 90):m.end() + 40].split())))
    return out
