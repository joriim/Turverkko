"""Tuotosten näyttöaste 0–4 ja sen perusteet.

Näyttöaste kuvaa, kuinka todennettavaa tietoa hankkeen tuotoksista on julkisesti saatavilla. Se ei
mittaa hankkeen laatua. Taso määräytyy vahvimman löydetyn perusteen mukaan:

  0  ei tuotostietoa
  1  laadullinen kuvaus toimenpiteistä
  2  määrälliset tavoitteet (esim. hehtaarit, mittauspisteet, kohteet, innovaatiot)
  3  raportoitu toteuma tekstissä, linkitetty raportti tai muu tarkistettu tuotos
  4  linkitetty vertaisarvioitu julkaisu tai avoin aineisto

Jokaiselle hankkeelle tallennetaan kenttä evidence_basis: lista perusteista, jotka näkyvät
hankekortissa. Käsin kuratoitu taso (evidence) säilyy, jos se on korkeampi kuin laskettu.
"""
import re, unicodedata

UNITS = (r"ha\b|hehtaari\w*|hectares?|km\b(?! (from|away|south|north|east|west|etel|pohjo|ita|lant))|kilomet\w*|kpl\b|%(?! of (the )?(world|global|eu|europe|finland|total))|prosent\w*|tonn\w*|t ?co2|mittauspist\w*|measurement (points|sites)|"
         r"monitoring (points|sites)|sites?\b|kohde\w*|kohtee\w*|pilot\w*|demonstr\w*|innovaat\w*|innovations?|yritys\w*|companies|"
         r"farms?\b|tilaa?\b|tiloj\w*|plans?\b|suunnitelm\w*|reports?\b|julkaisu\w*|articles?|artikkel\w*|workshops?|tyopaja\w*|"
         r"seminaar\w*|webinaar\w*|guides?|opas\w*|mallia?\b|models?\b|hektar\w*")
TARGET = re.compile(r"(?<![\w.])\d[\d  .,]*\s*(?:" + UNITS + r")", re.I)
RESULT = re.compile(
    r"toteuma|toteutu\w*|saavutt\w*|saavutett\w*|ennallistettiin|kunnostettiin|vettiin|valmistui|valmistuneet|"
    r"loppuraportissa|final report (shows|showed)|\bwere (restored|rewetted|built|established|completed)|"
    r"\bwas (restored|rewetted|completed|achieved)|\bhas been (restored|rewetted|completed|achieved)|"
    r"\bhave been (restored|rewetted|completed|achieved)|\b(was|were) achieved\b|\bresulted in\b|results (show|showed)|"
    r"\brestored \d|\brewetted \d|genomf[oö]rts|uppn[aå]tts|[aå]terv[aä]tts|uzlabot|atjaunot|taastati|"
    r"wurden? (wiedervern[aä]sst|renaturiert|umgesetzt)|wiedervern[aä]sst\b|reached (its|the) target", re.I)
OPENDATA = re.compile(r"open (access )?data|avoin(ta)? (data|aineisto)|avoimesti saatavilla|zenodo|dataset|data portal|"
                      r"\bdoi\b|10\.\d{4,}/", re.I)
OPENAIRE_N = re.compile(r"OpenAIRE: (\d+) tutkimustuotosta")
PEER = {"vertaisarvioitu"}
DATA = {"aineisto"}
REPORT = {"raportti", "ammattijulkaisu", "konferenssiabstrakti", "opinnäyte", "tiedote / mittausasema"}


def _snip(m, text, n=60):
    a = max(0, m.start() - 20)
    return " ".join(text[a:m.end() + n // 2].split())[:n]


def assess(p, pubs):
    """p: hanke (dict); pubs: hankkeeseen linkitetyt julkaisut. Palauttaa (taso, perusteet)."""
    text = " ".join(str(p.get(k) or "") for k in ("outputs", "description", "description_extra"))
    basis, level = [], 0
    if text.strip() or p.get("name"):
        level = 1
        basis.append("kuvaus toimenpiteistä")
    t = TARGET.search(text)
    if t:
        level = 2
        basis.append(f"määrällinen tavoite tai tuotos: “{_snip(t, text)}”")
    r = RESULT.search(text)
    if r:
        level = max(level, 3)
        basis.append(f"raportoitu toteuma: “{_snip(r, text)}”")
    m = OPENAIRE_N.search(text)
    if m and int(m.group(1)) > 0:
        level = max(level, 3)
        basis.append(f"OpenAIRE linkittää hankkeeseen {m.group(1)} tutkimustuotosta (tarkistamatta)")
    od = OPENDATA.search(text)
    if od:
        basis.append(f"avoin aineisto tai DOI mainittu: “{_snip(od, text)}”")
    for pub in pubs:
        kind = pub.get("type", "")
        tag = f"{pub['id']} ({kind}{', tarkistamatta' if not pub.get('verified') else ''})"
        if not pub.get("verified"):
            basis.append(f"linkitetty tuotos {tag}")
            level = max(level, 2)
        elif kind in PEER or kind in DATA:
            basis.append(f"linkitetty {'vertaisarvioitu julkaisu' if kind in PEER else 'avoin aineisto'} {tag}")
            level = 4
        else:
            basis.append(f"linkitetty {kind or 'tuotos'} {tag}")
            level = max(level, 3)
    return level, basis


def apply(projects, pubs):
    by_project = {}
    for pub in pubs:
        by_project.setdefault(pub.get("project"), []).append(pub)
    for p in projects:
        level, basis = assess(p, by_project.get(p["id"], []))
        manual = p.get("evidence") if not p.get("imported_from") else None
        if manual is not None and manual > level:
            basis.append(f"käsin arvioitu taso {manual}")
            level = manual
        p["evidence"] = level
        p["evidence_basis"] = basis
        p["pubs_n"] = len(by_project.get(p["id"], []))
