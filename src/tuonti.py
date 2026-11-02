"""Hakulähteiden CSV-tulosten tuonti aineistoon.

Lukee hakulahteet/tulokset/*.csv (muoto: hakulahteet/tuontipohja.csv) ja muuntaa rivit
hankkeiksi, organisaatioiksi ja osallistumisiksi. Kaikki päätökset (pois rajaus, yhdistäminen
olemassa olevaan hankkeeseen, organisaatioiden tunnistus) ovat tässä tiedostossa näkyvinä
listoina, jotta ne voi tarkistaa ja korjata.

Teemat luokitellaan avainsanasäännöillä (THEME_RULES). Automaattisesti luokitellut hankkeet
merkitään kentällä auto_themes=True, ja ne kannattaa tarkistaa käsin.
"""
import csv, hashlib, re, unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "hakulahteet" / "tulokset"

COUNTRY_MAP = {"Finland": "FI", "Sweden": "SE", "Estonia": "EE", "Latvia": "LV", "Ireland": "IE", "Germany": "DE-NI"}

# Rivit, jotka jäävät rajauksen ulkopuolelle (hankkeen nimi → peruste)
EXCLUDE = {
    "BioKas — Recycling-based growing media solutions": "yleinen ravinteiden kierrätys, ei turvemaa- tai turpeenkorvaajapainotusta",
    "Towards a carbon-neutral research farm — Investment project (hitu-I)": "tutkimustilan infrastruktuuri, ei turvemaapainotusta",
    "Towards a carbon-neutral research farm — Development project (hitu-D)": "tutkimustilan kehittäminen, ei turvemaapainotusta",
    "Use of bio-ash-based materials as fertilisers on forest soils": "tuhkalannoitus metsämaille yleisesti, ei turvemaapainotusta",
    "Investment project/Utilisation of biomass-based materials as fertilisers on forest land": "tuhkalannoitus metsämaille yleisesti, ei turvemaapainotusta",
    "Forest plan for responsible forest owners": "yleinen metsäsuunnittelu, ei turvemaapainotusta",
    "MEQAL-Methane Quantization and Localization": "jätehuollon metaanipäästöt, ei maankäyttöä",
    # EU CAP Network (lähde 2)
    "Utilization of by-product of grain drying as material and energy": "viljankuivauksen sivuvirta, ei turvemaata",
    "Adapting composting technologies for the utilisation of plant biomass to meet the conditions of the European Green Deal in the areas of GHG reduction, environmental protection, and enhancement of soil fertility": "yleinen maan kasvukunto ja kompostointi, ei turvemaata",
}

# Saksan hankkeet muista osavaltioista kuin Niedersachsen jäävät aluerajauksen ulkopuolelle
EXCLUDE_COUNTRY = {"DE": "Saksa, muu osavaltio kuin Niedersachsen (aluerajauksen ulkopuolella)"}

# Lähteen numero → tunnisteen etuliite (K = Kohesio, E = EU CAP Network / EIP)
SOURCE_PREFIX = {"1": "K", "2": "E"}

# Rivit, jotka ovat jo aineistossa olevia hankkeita (nimi → olemassa oleva tunniste).
# Rivin tiedot täydentävät olemassa olevaa hanketta eivätkä luo uutta.
MATCH_EXISTING = {
    "Accelerating the JTF Restoration of Ostrobothnian Provinces": "FI-02",
    "Product chains of low bog biomass": "NI-02",
    "Aid for the revitalisation of historical peat extraction sites": "LV-02",
    "Restoration of drained, exhausted and abandoned peatlands": "EE-02",
    "Farm Carbon EIP": "IE-01",
    "FarmPEAT (Farm Payments for Ecological and Agricultural Transitions) Project": "IE-02",
    "Our Moor Future Oldenburger Graben - Cooperative moorland in the Oldenburger Graben in Schleswig-Holstein for climate protection and agricultural added value": "X-DE-SH",
}

# Käsin tarkistetut teemat (ohittavat avainsanasäännöt)
THEME_OVERRIDE = {
    "Development of cloudberry propagation and cultivation technologies for recultivation of peat bogs by establishing commercial plantations": ["T1", "T3"],
    "Innovative Agrivoltaic System in a Blackberry Plantation on Peat Soil: Integration of Renewable Energy and Reduction of GHG Emissions": ["T1", "T6"],
    "Innovative organic fertilizer, containing microorganisms": ["T3"],
    "Waste-free recycling of coniferous green biomass in a biodegradable planter container system": ["T3"],
    "Agricultural land management planning for use in agriculture, forestry or agroforestry, based on agro-technological, economic, environmental and climate risk data": ["T2", "T6", "T8"],
    "Sustainable management of degraded organic soils: impact of legume and digestate use on carbon cycling and ecosystem in a long term tree plantating": ["T2", "T4", "T6"],
    "The Conservation of Breeding Curlew in Ireland": ["T5"],
    "Blackstairs farming Futures (BFF) Sustainable farming project in the Blackstairs Mountains": ["T2", "T5"],
    "A Sustainable Agricultural Plan for the MacGillycuddy Reeks - Conservation and restoration of Upland Habitat in the MacGillycuddy Reeks": ["T2", "T5"],
    "Inishowen Upland Farmers Project": ["T2", "T5"],
    "FloraGPT: Artificial intelligence- and sensor-controlled irrigation with a user-friendly interface for cultivation methods optimized for peat replacement": ["T3"],
    "Industrial raw material using bog sites – I-ROBI": ["T2", "T3"],
}

# Organisaation tunnistus nimen osasta (taivutettu, pienet kirjaimet) → olemassa oleva tunniste
ORG_CONTAINS = [("silava", "silava"), ("latvijas universit", "lu"), ("lauksaimniecibas universit", "lbtu"),
                ("darzkopibas instit", "lathort"), ("agroresursu un ekonomikas", "arei"), ("teagasc", "teagasc"),
                ("green restoration ireland", "gri"), ("nature based agri", "nbas"), ("irish rural link", "irl"),
                ("umeras", "umeras"), ("helsingin yliopisto", "hy"), ("ita-suomen yliopisto", "uef"),
                ("luonnonvarakeskus", "luke"), ("seinajoen ammattikorkeakoulu", "seamk"), ("oulun yliopisto", "oy"),
                ("offis", "offis"), ("hochschule hannover", "hochschule-hannover"), ("biokunststoffe", "hochschule-hannover")]

# Organisaatioksi tunnistettavat sanat; muut nimet tulkitaan henkilöiksi eikä niistä tehdä solmuja
ORG_WORDS = (r"universit|instit|silava|lvmi|\bsia\b|z/s|\bzs\b|biedrib|asociacij|fonds|centrs|saimnieciba|komercsabiedr|apvieniba|"
             r"\bmpks\b|\bapp\b|gmbh|e\.\s?v\.|\bug\b|\bgbr\b|\bltd\b|limited|\boy\b|oyj|cooperative|society|group|teagasc|"
             r"technology|hochschule|offis|\bkg\b|\bry\b|project|rural link|community|baumschul|beratungsring|dammtechnik|"
             r"biolat|gourmet|kolkanrinne|epira|\btmi\b|council|authority|agency|ministry|association|foundation|stiftung|landkreis|"
             r"forst|verband|nabu|bund |nlwkn|yliopisto|ammattikorkeakoulu|keskus|saatio|kaupunki|metsahallitus|\bab\b|\bas\b|"
             r"lansstyrelsen|skogsstyrelsen|riigimetsa|regions|pasvaldiba|departamentas|chambres|larenstein|kompetenzzentrum|peat ltd|"
             r"rspb|broads|zid|archehof|schmedt|torfwerk|forstamt|landesforsten|moorverwaltung|fachzentrum|naturschutz")

# Konekäännösvirheiden korjaus (Kohesion englanninkielinen nimi → oikea nimi)
NAME_FIX = {
    "Ant restoration in Norrbotten County": "Myrrestaurering i Norrbottens län (MyreN) – soiden ennallistaminen",
    "Rewetting of the White Moore": "Wiedervernässung des Weißen Moores",
    "Rewetting “Dead Moor”": "Wiedervernässung des Toten Moores",
    "Optimisation of water balance in high bogs of the Dieph. Moor dropping": "Optimisation of water balance in high bogs of the Diepholzer Moorniederung",
    "Climate Tools – Climate Protection and Biodiversity of Diepholz Moor Lowing": "Climate Tools – Climate Protection and Biodiversity of the Diepholzer Moorniederung",
    "Planning for the renaturation of the rock moor": "Planning for the renaturation of the Steinmoor",
}

# Edunsaajan nimi → olemassa oleva organisaatiotunniste
ORG_ALIAS = {
    "helsingin yliopisto": "hy", "itä-suomen yliopisto": "uef", "luonnonvarakeskus": "luke", "luke luonnonvarakeskus": "luke",
    "seinäjoen ammattikorkeakoulu oy": "seamk", "oulun yliopisto": "oy", "university of oulu": "oy",
    "suomen metsäkeskus - finlands skogscentral": "metsakeskus", "suomen metsäkeskus": "metsakeskus",
    "nlwkn - niedersächsischer landesbetrieb für wasserwirtschaft, küsten- und naturschutz": "nlwkn",
    "nlwkn betriebsstelle süd, gb iv": "nlwkn", "nlwkn betriebsstelle brake-oldenburg": "nlwkn",
    'atvasināta publiska persona "latvijas valsts mežzinātnes institūts "silava""': "silava",
    "vidzemes plānošanas reģions": "lv-regions",
    "green restoration ireland cooperative society limited": "gri", "green restoration ireland cooperative society ltd": "gri",
    "suomen ympäristökeskus": "syke", "elinkeino-, liikenne- ja ympäristökeskusten kehittämis- ja hallintokeskus": "keha",
    "riigimetsa majandamise keskus": "rmk",
}

# Teemasäännöt: (teema, säännöllinen lauseke). Haetaan nimestä, kuvauksesta, tuotoksista ja hakusanasta.
THEME_RULES = [
    ("T1", r"peat (production|extraction)|extraction site|cutaway|cutover|after.?use|next land use|reuse of peat|historical peat|turvetuotan|leaving peat production|exhausted and abandoned"),
    ("T2", r"agricultur|farm(?!ing ?of sphagnum)|grassland|grazing|suckler|cattle|sheep|underfloor irrigation|wet grassland|landscape management company"),
    ("T3", r"paludicult|sphagnum|peat moss|growing media|peat.?(free|replace|substitut|alternative)|substrate|biochar|cattail|biomass|compost|straw|bark|horticultur|new cultivated plants|moos"),
    ("T4", r"peatland forest|forest management|logging|forestry|forest soil|baltic forests|drained forest|ditch.{0,20}forest|soft lands|storm damage"),
    ("T5", r"natura|nature reserve|nature management|sacs?\b|raised bog|blanket bog|high (moor|bog)|hill moor|slope moor|mire restoration|bog ecosystem|biodiversity|habitat|rewetting|renaturation|wetting|area protection|land protection|bird protection|peat fire|restor"),
    ("T6", r"greenhouse|\bghg\b|emission|carbon|methane|climate (protection|donation|tools)|co2|water levels?|monitoring"),
    ("T7", r"network|competence cent|knowledge|information system|cooperation|collaborative|research for moor|policies"),
    ("T8", r"landowner|land.?use plan|livelihood|stakeholder|business|carbon market|decision|area concept|meanings|priorities|care and development concept|just transition|vitality"),
]


def _slug(s):
    s = unicodedata.normalize("NFKD", s.lower())
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")[:40]


def _num(v):
    try:
        return round(float(str(v).replace(" ", "").replace(",", "."))) if str(v).strip() else None
    except ValueError:
        return None


def _fold(s):
    s = unicodedata.normalize("NFKD", s.lower())
    return "".join(c for c in s if not unicodedata.combining(c))


def org_of(who):
    """Palauttaa (tunniste, nimi) organisaatiolle tai None, jos merkintä on pelkkä henkilö.
    Käsittelee muodot "Henkilö, Organisaatio", "Organisaatio (Henkilö)" ja "Organisaatio, Henkilö"."""
    who = re.sub(r"\s*\([^)]*\)", lambda m: "" if not re.search(ORG_WORDS, _fold(m.group(0))) else m.group(0), who.strip())
    parts = [p.strip(" ;") for p in re.split(r",(?![^(]*\))", who) if p.strip(" ;")]
    cands = [p for p in parts if re.search(ORG_WORDS, _fold(p))]
    if not cands:
        return None
    name = cands[0].strip().strip('"').strip()
    m = re.match(r"^(.*?)\s*\((.+)\)$", name)
    if m and re.search(ORG_WORDS, _fold(m.group(2))) and not re.search(ORG_WORDS, _fold(m.group(1))):
        name = m.group(2)
    f = _fold(name)
    for sub, oid in ORG_CONTAINS:
        if sub in f:
            return oid, name
    oid = ORG_ALIAS.get(name.lower()) or ORG_ALIAS.get(who.strip().lower())
    return (oid or _slug(_org_name(name))), _org_name(name)


def _period(s):
    m = re.search(r"(20\d\d)-(20\d\d)", s or "")
    return f"{m.group(1)}–{m.group(2)[2:]}" if m else (s or "")


def _fund(row):
    if "Interreg" in row["ohjelmakausi"]:
        return "Interreg"
    return {"EAKR": "EAKR", "JTF": "JTF", "KF": "KF", "ESR+": "ESR+"}.get(row["rahasto"], row["rahasto"])


# Monen maan Interreg-hankkeet: maa = johtavan edunsaajan maa, jos se on rajauksessa; muuten "EU"
COUNTRY_OVERRIDE = {
    "MEQAL-Methane Quantization and Localization": "FI",
    "PRESERVE: Protection and REStoration of peatland biodiversity, and Ecosystem seRVicEs in Natura 2000 areas": "FI",
    "Smart Carbon Farming": "DE-NI",
    "Improving cross border cooperation in the field of peat fire prevention and response": "LV",
    "Collaborative Action for the Natural Network": "IE",
    "Co-operation Across Borders for Biodiversity": "IE",
}


def _country(row):
    name = row["hanke_nimi"].strip()
    if row["maa"].strip() in ("FI", "SE", "EE", "LV", "IE", "DE-NI", "DE-SH", "EU", "DE"):
        return row["maa"].strip()
    for k, v in COUNTRY_OVERRIDE.items():
        if name.startswith(k):
            return v
    cs = [x.strip() for x in row["maa"].split(";") if x.strip()]
    if len(cs) == 1 and cs[0] in COUNTRY_MAP:
        return COUNTRY_MAP[cs[0]]
    return "EU"


def org_type(n):
    """Organisaatiotyyppi nimen perusteella (tarkistettava)."""
    f = unicodedata.normalize("NFKD", n.lower())
    f = "".join(c for c in f if not unicodedata.combining(c))
    if re.search(r"ammattikorkeakoulu|university of applied|hochschule", f): return "amk"
    if re.search(r"yliopisto|universit|teknillinen", f): return "yliopisto"
    if re.search(r"ymparistokeskus|tutkimuskeskus|institut|fachzentrum|kompetenzzentrum|\btapio\b", f): return "tutkimuslaitos"
    if re.search(r"saatio|stiftung|\bry\b|e\.\s?v\.|nabu|bund fur|rspb|association|yhdistys|luontokollektiivi|luonnonsuojelupiiri", f): return "jarjesto"
    if re.search(r"\boy\b|oyj|\bltd\b|gmbh|\bas\b|archehof|schmedt|nursery|latvijas valsts mezi|power", f): return "yritys"
    return "viranomainen"


def _org_name(n):
    n = n.strip()
    return n.title() if n.isupper() else n


def _themes(text):
    t = text.lower()
    found = [k for k, rx in THEME_RULES if re.search(rx, t)]
    if not found:
        found = ["T5"] if re.search(r"bog|moor|mire|suo|purv", t) else ["T1"]
    return found


def _evidence(row):
    out = row["tuotokset"]
    if re.search(r"\d[\d ,.]*\s*(ha\b|hectare|hehtaari|%|conservation action plans)", out, re.I):
        return 2
    return 1 if (out.strip() or row["kuvaus"].strip()) else 0


def load():
    """Palauttaa (uudet hankkeet, uudet organisaatiot, osallistumiset, täydennykset, poistetut)."""
    rows = []
    for f in sorted(RESULTS.glob("*.csv")):
        with open(f, encoding="utf-8-sig") as fh:
            for r in csv.DictReader(fh):
                r["_file"] = f.name
                rows.append(r)

    removed, enrich, groups = [], {}, {}
    for r in rows:
        name = r["hanke_nimi"].strip()
        if name in EXCLUDE:
            removed.append(dict(id=f"kohesio:{_slug(name)}", name=name, reason=EXCLUDE[name]))
            continue
        if _country(r) in EXCLUDE_COUNTRY and name not in MATCH_EXISTING:
            removed.append(dict(id=f"rajattu:{_slug(name)}", name=name, reason=EXCLUDE_COUNTRY[_country(r)]))
            continue
        if name in MATCH_EXISTING:
            enrich.setdefault(MATCH_EXISTING[name], []).append(r)
            continue
        key = (name, r["ohjelmakausi"])
        groups.setdefault(key, []).append(r)

    projects, orgs, part = [], {}, []
    for (name, _), rs in sorted(groups.items(), key=lambda kv: (_country(kv[1][0]), kv[0][0])):
        r0 = rs[0]
        c = _country(r0)
        # Pysyvä tunniste: lähde + maa + tiiviste hankesivun osoitteesta (ei muutu, kun aineistoa lisätään)
        pid = f"{SOURCE_PREFIX.get(r0['lahde'].strip(), 'H')}-{c}-{hashlib.sha1(r0['url'].encode()).hexdigest()[:4]}"
        text = " ".join([name, r0["kuvaus"], r0["tuotokset"], r0["hakusana"]])
        budgets = [_num(r["budjetti_eur"]) for r in rs]
        eus = [_num(r["eu_osuus_eur"]) for r in rs]
        _lo = org_of(r0["toteuttaja"])
        lead = _lo[1] if _lo else _org_name(r0["toteuttaja"])
        others = sorted({(org_of(r["toteuttaja"]) or (None, _org_name(r["toteuttaja"])))[1] for r in rs[1:]} - {lead})
        partners_listed = [p.strip() for p in r0["partnerit"].split(";") if p.strip()] if c != "EU" else []
        projects.append(dict(
            id=pid, country=c, region=r0["alue"] or ("useita maita" if c == "EU" else ""), fund=_fund(r0),
            period=_period(r0["ohjelmakausi"]), name=NAME_FIX.get(name, name),
            lead=lead + (f" + {len(others)} muuta edunsaajaa" if others else ""),
            start=int(r0["alku"][:4]) if r0["alku"][:4].isdigit() else None,
            end=int(r0["loppu"][:4]) if r0["loppu"][:4].isdigit() else None,
            eur_total=sum(b for b in budgets if b) or None, eur_eu=sum(e for e in eus if e) or None,
            themes=THEME_OVERRIDE.get(name) or _themes(text), auto_themes=name not in THEME_OVERRIDE, outputs=(r0["tuotokset"] or r0["kuvaus"])[:400],
            evidence=_evidence(r0), url=r0["url"], urls=[r["url"] for r in rs],
            programme=r0["ohjelmakausi"], imported_from=r0["_file"],
            partners_note="; ".join(p for p in [r0["partnerit"]] if p) if c == "EU" else ""))
        for i, who in enumerate([r["toteuttaja"] for r in rs] + partners_listed):
            if not who.strip():
                continue
            o = org_of(who)
            if not o:
                continue  # henkilö: ei solmua
            oid, oname = o
            orgs.setdefault(oid, dict(id=oid, name=oname, country=c if c != "EU" else "", type=org_type(oname)))
            role = "edunsaaja" if i < len(rs) else "partneri"
            url = rs[i]["url"] if i < len(rs) else r0["url"]
            if (oid, pid) not in {(p[0], p[1]) for p in part}:
                part.append((oid, pid, role, url))
    return projects, list(orgs.values()), part, enrich, removed
