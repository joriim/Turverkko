"""Hankkeiden sisällöllinen päällekkäisyys tekstin perusteella.

Teemaluokat (T1–T8) ovat liian karkeita päällekkäisyyden mittaamiseen: kaksi hanketta, joilla on sama
yksi teema, saisivat täyden osuman. Tämä moduuli vertaa hankkeiden omia tekstejä (nimi, kuvaus,
tuotokset ja muiden lähteiden kuvaukset).

Menetelmä
- Tekstit pilkotaan sanoiksi, taivutus tasoitetaan katkaisemalla sanat seitsemään merkkiin, ja
  yleiset sanat poistetaan (STOP).
- Monikielisyys: sama asia eri kielillä (turve, peat, torv, kūdra, Torf, turvas) tunnistetaan
  käsitesanastolla (CONCEPTS), joka lisää tekstiin kieliriippumattoman käsitesanan.
- Sanoista ja käsitteistä lasketaan TF-IDF-painot ja hankeparien kosinisamankaltaisuus.
- Samankaltaisuuden lisäksi parille kirjataan ajallinen päällekkäisyys, yhteiset toimijat ja
  lyhin yhteistyöpolku, ja pari luokitellaan (TYPES).

Kynnysarvo ei ole luonnonvakio, joten raportti näyttää tulokset usealla kynnyksellä (SENSITIVITY).
"""
import math, re, unicodedata
from collections import Counter

MIN_TOKENS = 6          # liian lyhyt teksti ei kelpaa vertailuun
STEM = 7                # katkaisupituus
CONCEPT_WEIGHT = 2      # käsitesana painaa kuin kaksi esiintymää
DEFAULT_THRESHOLD = 0.20  # valittu tarkastelemalla pareja käsin; ks. herkkyystaulukko
SENSITIVITY = [0.15, 0.20, 0.25, 0.30, 0.35, 0.40]

# Käsitteet: kieliriippumaton tunnus → säännöllinen lauseke (taivutetut ja yhdyssanat mukaan)
CONCEPTS = {
    "turve": r"peat|turve|turpee|turvem|torv|kudr|turba|turvas|torf|moor",
    "suo": r"\bbogs?\b|\bmires?\b|\bfens?\b|\bsuo|soiden|\bsoo\b|\braba\b|myr\b|myrar|mosse|purv|hochmoor|niedermoor",
    "ennallistaminen": r"restor|ennallist|restaurer|taastam|atjauno|renatur|rehabilit|revitali",
    "vettaminen": r"rewet|vettam|atervatn|wiedervern|water ?table|vedenpin|grundvatten|wasserstand|ditch block|plug",
    "kosteikko": r"wetland|kosteik|vatmark|margala|mitraj|feuchtgebiet|lavbund",
    "paludikulttuuri": r"paludi|kosteikkoviljel|cattail|typha|reed|ruoko|rohrkolben|wet farming|wet agricult",
    "rahkasammal": r"sphagnum|rahkasammal|vitmoss|torfmoos|sfagn",
    "kasvualusta": r"growing media|substrat|kasvualust|odlingssubstrat|peat.?free|peat substitut|turpeeton|turvevapaa|torvfri|torffrei|torfersatz",
    "jalkikaytto": r"after.?use|cutaway|cutover|jalkikayt|suonpohj|extraction site|turvetuotanto|torvtakt|efterbehandl|jaaksoo|abtorf|production area",
    "suometsa": r"peatland forest|suomets|drained forest|forest drain|kunnostusoj|skogsdik|moorwald|metsaoj|forestry",
    "turvepelto": r"agricultur|farm|grassland|pelto|maatalou|jordbruk|lantbruk|landwirt|lauksaimn|pollumaj|grunland|cultivat|crop",
    "paastot": r"emission|greenhouse|\bghg\b|kasvihuone|vaxthusgas|kasvuhoone|siltumnic|treibhaus|co2|carbon dioxide|hiilidioksid",
    "metaani": r"methan|metaan|\bch4\b",
    "typpioksiduuli": r"nitrous|\bn2o\b|typpioksid|lustgas|lachgas",
    "hiili": r"carbon|hiili|hiilen|\bkol\b|kolsank|kolinlagr|susinik|oglek|kohlenstoff|sequestr|\bsinks?\b|nielu",
    "mittaus": r"monitor|measur|mittau|seuran|matning|uppfoljn|eddy|flux|kaasuvuo|inventor|mrv|verific|todent",
    "kaukokartoitus": r"remote sens|satellit|kaukokart|drone|lidar|mapping|kartoit|kartlagg",
    "mallinnus": r"model|mallin|simul|digital twin",
    "luonto": r"biodivers|luonnon monimuot|habitat|natura|species|lajist|naturvard|naturschutz|bird|lintu",
    "vesistot": r"water quality|vesiens|vesisto|nutrient|ravinne|leach|huumus|humus|runoff|valuma",
    "maanomistaja": r"landowner|maanomist|markagar|forest owner|metsanomist|stakeholder|farmer|viljelij",
    "suunnittelu": r"plan(ning)?\b|suunnit|planer|konzept|concept|strateg|roadmap|tiekartt",
    "liiketoiminta": r"business|liiketoim|yritys|company|enterpris|market|markkin|value chain|arvoketj",
    "koulutus": r"educat|training|koulut|opetus|learning|oppim|curricul",
    "aurinko": r"solar|aurinko|photovolt|agrivolt",
    "marjat": r"berr|marja|cranberr|blueberr|cloudberr|lakka|karpalo|mustik|jõhvik|dzerven",
    "palo": r"\bfires?\b|turvepalo|\bpalo|torvbrand|ugunsgr",
}
_CONCEPT_RX = {k: re.compile(v) for k, v in CONCEPTS.items()}

STOP = set("""
the and for with from that this will are was were has have been into their its our also which other such more than
project projects aim aims objective objectives activities activity main new well use used using based within between
through about area areas region regional development developing develop support results result work part
hanke hankkeen hankkeessa hankkeessa tavoite tavoitteena tavoitteet tarkoitus kehit kehitt kehittaa alue alueen alueella
seka myos ovat joka jotka jonka sekä kanssa kautta osalta lisaksi avulla mukaan ollut olla
projektet projekt syfte mal och att med som for till den det har kan inom samt
das die der und fur mit von zur zum ein eine wird werden auf des den dem
ja ka ning on et
can could may located approxi approximately subproj subproject teilprojekt osahanke osaprojekti
okad vill genom ett eller under efter
""".split())


def fold(s):
    s = unicodedata.normalize("NFKD", (s or "").lower())
    return "".join(c for c in s if not unicodedata.combining(c))


def tokens(text):
    t = fold(text)
    words = [w[:STEM] for w in re.findall(r"[a-z][a-z0-9]{2,}", t) if w not in STOP and w[:STEM] not in STOP]
    concepts = [f"#{k}" for k, rx in _CONCEPT_RX.items() if rx.search(t)]
    return words + concepts * CONCEPT_WEIGHT


def text_of(p):
    return " ".join(str(p.get(k) or "") for k in ("name", "description", "outputs", "description_extra", "note"))


def vectors(items):
    docs = {i: Counter(tokens(t)) for i, t in items.items()}
    docs = {i: c for i, c in docs.items() if sum(c.values()) >= MIN_TOKENS}
    n = len(docs)
    df = Counter(w for c in docs.values() for w in c)
    vec = {}
    for i, c in docs.items():
        v = {w: (1 + math.log(k)) * (math.log((n + 1) / (df[w] + 1)) + 1) for w, k in c.items()}
        norm = math.sqrt(sum(x * x for x in v.values())) or 1.0
        vec[i] = {w: x / norm for w, x in v.items()}
    return vec


def cosine(a, b):
    if len(a) > len(b):
        a, b = b, a
    return sum(x * b.get(w, 0.0) for w, x in a.items())


def shared_terms(a, b, k=6):
    common = sorted(((a[w] * b[w], w) for w in a.keys() & b.keys()), reverse=True)[:k]
    return [w.lstrip("#") for _, w in common]


def years(p):
    s, e = p.get("start"), p.get("end")
    s = s or e
    e = e or s
    return (s, e) if s else None


def time_overlap(p, q):
    a, b = years(p), years(q)
    if not a or not b:
        return None
    return max(a[0], b[0]) <= min(a[1], b[1])


# Parin luokat. Järjestys = tulkinnan tärkeys.
TYPES = {
    "saman kokonaisuuden osat": "nimet alkavat samalla hanke- tai ohjelmanimellä (osahankkeet tai -toteutukset)",
    "rinnakkainen ilman yhteyttä": "sama maa, samaan aikaan, ei yhteistä toimijaa eikä yhteistyöpolkua. Voi olla tarkoituksellista (eri kohteet) tai päällekkäistä työtä (sama menetelmä tai suunnittelu kahteen kertaan)",
    "peräkkäiset samassa maassa": "sama maa, eri aikaan, ei yhteistä toimijaa eikä polkua (toisto tai jatko ilman yhteyttä)",
    "puuttuva yhteys": "eri maat, ei yhteistyöpolkua",
    "yhteydessä": "yhteinen toimija tai yhteistyöpolku enintään kolme askelta",
}


def family(name):
    """Hankekokonaisuuden tunnus: nimen ensimmäinen sana, jos se on lyhenne (vähintään 4 merkkiä ja 2 isoa kirjainta),
    esim. MOOSWEIT, OptiMOOS, PohjaNeva."""
    m = re.match(r"\s*([^\s,:–-]{4,})", name or "")
    return fold(m.group(1)) if m and sum(ch.isupper() for ch in m.group(1)) >= 2 else None


def classify(same_country, overlap_t, connected, same_family=False):
    if same_family:
        return "saman kokonaisuuden osat"
    if connected:
        return "yhteydessä"
    if same_country:
        return "rinnakkainen ilman yhteyttä" if overlap_t is not False else "peräkkäiset samassa maassa"
    return "puuttuva yhteys"


def compute(projects, distance, actors_of, threshold=DEFAULT_THRESHOLD, max_hops=3):
    """projects: {id: dict}; distance(a, b) -> int|None; actors_of(id) -> set of org ids.
    Palauttaa (parit kynnyksen ylittäviltä, herkkyystaulukko, vertailuun kelvanneiden määrä)."""
    vec = vectors({i: text_of(p) for i, p in projects.items()})
    ids = sorted(vec)
    pairs, all_scores = [], []
    for x, a in enumerate(ids):
        for b in ids[x + 1:]:
            s = cosine(vec[a], vec[b])
            if s < min(SENSITIVITY):
                continue
            pa, pb = projects[a], projects[b]
            shared = sorted(actors_of(a) & actors_of(b))
            d = distance(a, b)
            connected = bool(shared) or (d is not None and d <= max_hops)
            same = pa.get("country") == pb.get("country") and pa.get("country") not in ("EU", "", None)
            t = time_overlap(pa, pb)
            rec = dict(a=a, b=b, a_nimi=pa["name"], b_nimi=pb["name"], a_maa=pa.get("country"), b_maa=pb.get("country"),
                       score=round(s, 3), yhteiset=", ".join(shared_terms(vec[a], vec[b])),
                       samaan_aikaan={True: "kyllä", False: "ei", None: "?"}[t],
                       yhteiset_toimijat=" ".join(shared), etaisyys="ei polkua" if d is None else d,
                       tyyppi=classify(same, t, connected, family(pa["name"]) is not None and family(pa["name"]) == family(pb["name"])))
            all_scores.append(rec)
    sens = []
    for th in SENSITIVITY:
        c = Counter(r["tyyppi"] for r in all_scores if r["score"] >= th)
        sens.append(dict(kynnys=th, pareja=sum(c.values()), **{k: c.get(k, 0) for k in TYPES}))
    pairs = sorted((r for r in all_scores if r["score"] >= threshold), key=lambda r: (-r["score"], r["a"], r["b"]))
    return pairs, sens, len(ids)
