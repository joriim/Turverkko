"""Turverkon rajaus yhdessä paikassa.

Tätä tiedostoa käyttävät
  - hakuohjeen yhteinen ohje (hakulahteet/README.md: RAJAUS- ja YDINSANAT-kohdat generoidaan tästä, build.py),
  - automaattihaut ja Kohesion viennin suodatus (scripts/haku/yhteinen.py: SCOPE ja EXCLUDE),
  - tarkistus, että jokainen ydinsana osuu koneelliseen rajaukseen (check()).
Muuta rajausta vain täällä ja aja build.py.
"""
import re

# Sanallinen rajaus hakuohjeeseen
SCOPE_TEXT = """RAJAUS: Kerää hankkeita, jotka liittyvät turvemaihin tai maaperään:
- turvemaat: turvetuotantoalueiden ennallistaminen ja jälkikäyttö, turvepellot ja
  vettäminen, kosteikkoviljely (paludikulttuuri) ja turpeen korvaajat, suometsät, soiden
  suojelu, turvemaiden osaamiskeskukset ja maanomistajien maankäytön suunnittelu
- muu maaperä: maaperän ja maankäyttösektorin päästöt (CO2, CH4, N2O), maaperän
  hiilensidonta ja hiiliviljely, päästöjen mittaus, mallinnus ja todentaminen (MRV,
  päästökertoimet, kasvihuonekaasuinventaario, kaukokartoitus), hiilimarkkinat ja
  -sertifiointi, maaperän vesitalous (säätösalaojitus, kuivatus) ilmastonäkökulmasta
  sekä metsien ja peltojen hiilinielut.
Rahastot: JTF, EAKR, ESR+, maaseuturahasto, EIP-AGRI, Interreg, Horizon 2020 ja
Horizon Europe sekä kansallinen tutkimusrahoitus. Ohjelmakaudet 2014–20 ja 2021–27.
ÄLÄ kerää vety-, energia-, matkailu- tai yleisiä yritystukihankkeita, äläkä
ravinteiden kierrätystä tai maan kasvukuntoa, jos niissä ei ole päästö- tai hiilinäkökulmaa."""

# Ydinsanat kielittäin (hakuohjeeseen ja tarkistukseen)
CORE_TERMS = {
    "en": ["peat", "peatland", "bog", "mire", "fen", "organic soil", "histosol", "drained organic soils", "rewetting",
           "paludiculture", "sphagnum farming", "peat-free", "peat substitute", "growing media", "cutaway", "cutover",
           "after-use", "water table", "controlled drainage", "LULUCF", "carbon farming", "soil carbon",
           "soil organic carbon", "carbon sequestration", "emission factor", "MRV", "greenhouse gas inventory",
           "nitrous oxide", "methane", "eddy covariance", "carbon credit", "raised bog", "blanket bog"],
    "fi": ["turve", "turvemaa", "turvepelto", "eloperäinen maa", "multamaa", "suo", "suometsä", "suonpohja",
           "turvetuotantoalue", "jälkikäyttö", "ennallistaminen", "vettäminen", "kosteikkoviljely", "rahkasammal",
           "säätösalaojitus", "pohjavedenpinnan säätö", "kunnostusojitus", "jatkuvapeitteinen kasvatus", "valumavesi",
           "humus", "maankäyttösektori", "hiilinielu", "maaperän hiili", "hiiliviljely", "hiilensidonta",
           "kasvihuonekaasu", "typpioksiduuli", "päästökerroin", "todentaminen"],
    "sv": ["torv", "torvmark", "myr", "mosse", "kärr", "organogen jord", "mulljord", "dikad", "återvätning", "våtmark",
           "torvtäkt", "efterbehandling", "vitmossa", "torvfri", "odlingssubstrat", "grundvattennivå",
           "reglerbar dränering", "kolsänka", "kolinlagring", "markkol", "växthusgas", "lustgas", "markanvändning",
           "klimatkompensation"],
    "et": ["turvas", "turbaala", "turvasmuld", "jääksoo", "soo", "raba", "madalsoo", "märgala", "ammendatud turbaväli",
           "taastamine", "korrastamine", "maaparandus", "veerežiim", "süsinik", "mulla süsinik", "süsiniku sidumine",
           "kasvuhoonegaas", "heitkogused"],
    "lv": ["kūdra", "kūdrājs", "kūdras ieguve", "purvs", "augstais purvs", "zāļu purvs", "mitrājs", "organiskās augsnes",
           "rekultivācija", "renaturalizācija", "meliorācija", "paludikultūra", "ZIZIMM", "augsnes ogleklis",
           "oglekļa piesaiste", "siltumnīcefekta gāzes", "emisijas"],
    "de": ["Moor", "Moorboden", "Hochmoor", "Niedermoor", "Anmoor", "organische Böden", "kohlenstoffreiche Böden",
           "Wiedervernässung", "Renaturierung", "Paludikultur", "Torfmoos", "Torfersatz", "torffrei", "Moorgrünland",
           "Moorwald", "Wasserstandsanhebung", "Moorschutz", "Bodenkohlenstoff", "Humusaufbau",
           "Kohlenstoffspeicherung", "Treibhausgas", "Lachgas", "Carbon Farming"],
}
NATURA = ("7110 keidassuot / active raised bogs, 7120 degraded raised bogs, 7130 blanket bogs, "
          "7140 transition mires, 7160 lähteiköt, 7230 alkaline fens, 91D0 bog woodland / puustoiset suot")

# Ydinsanat, joita koneellinen rajaus ei tarkoituksella yksinään hyväksy, koska ne tuovat liikaa vääriä osumia
# (esim. metaani biokaasuhankkeissa). Ne kelpaavat hakusanoiksi, mutta osuman on täytettävä muu rajaus.
BROAD = {"jälkikäyttö", "methane", "nitrous oxide", "carbon sequestration", "water table", "MRV", "greenhouse gas inventory",
         "carbon credit", "eddy covariance", "after-use", "humus", "valumavesi", "todentaminen", "kasvihuonekaasu",
         "typpioksiduuli", "jatkuvapeitteinen kasvatus", "kunnostusojitus", "taastamine", "korrastamine", "maaparandus",
         "veerežiim", "süsinik", "kasvuhoonegaas", "heitkogused", "rekultivācija", "renaturalizācija", "meliorācija",
         "siltumnīcefekta gāzes", "emisijas", "Renaturierung", "Treibhausgas", "Lachgas", "efterbehandling",
         "växthusgas", "lustgas", "markanvändning", "klimatkompensation", "dikad", "grundvattennivå", "kärr", "soo",
         "pohjavedenpinnan säätö", "päästökerroin", "Humusaufbau", "Kohlenstoffspeicherung", "Wasserstandsanhebung"}

# Koneellinen rajaus (automaattihaut, Kohesion vienti). Sanarajat estävät osumat kuten repeat, turbine, Moore.
SCOPE = re.compile(
    r"\bpeat(s|land|lands|y)?\b|\bbogs?\b|\bmires?\b|\bfens?\b|\bwetlands?\b|\bpaludicult|\bsphagnum|"
    r"\borganic soils?\b|\bhistosols?\b|\brewet|\bdrain(ed|age)\b.{0,40}\b(soil|land|forest|peat)|"
    r"\bsoil (organic )?carbon\b|\bsoil c\b|\bcarbon farming\b|\bsoil carbon sequestration|carbon sequestration in (agricultural )?soils?|"
    r"\bsoil (greenhouse|ghg|emissions?|respiration|methane|n2o)\b|\b(nitrous oxide|n2o|methane|ch4) (emissions?|fluxes?) from (agricultural )?(soils?|wetlands?|peat)|"
    r"\blulucf\b|\bland[- ]use (sector|emissions)\b|\bemission factors?\b.{0,40}\b(soil|land|peat)|"
    r"\bcutaway|\bcutover|\bgrowing media\b|\bpeat[- ](free|substitut)|\bcontrolled drainage|"
    r"\bturve|\bturvemaa|\bturpee|\bsuo\b|\bsoiden\b|\bsuometsä|\bsuonpohj|\beloperäi|\bmultamaa|\bkosteikko|\bvettäm|\bennallist|"
    r"\brahkasammal|\bsäätösalaoj|\bhiilinielu|\bmaaperän hiil|\bhiiliviljel|\bhiilensidon|\bmaankäyttösektor|"
    r"\btorv(mark|myr|täkt|fri)?\b|\bmyr(ar|mark)?\b|\bmosse\b|\bvåtmark|\borganogen|\bmulljord|\båterväta|\båtervätning|\bvitmoss|"
    r"\bodlingssubstrat|\breglerbar dränering|\bkolsänk|\bkolinlagr|\bmarkkol|"
    r"\bkūdr|\bpurv(s|ā|i|u)\b|\bmitrāj|\borganiskās augsnes|\bpaludikultūr|\bzizimm\b|\baugsnes oglek|\boglekļa piesaist|"
    r"\bturba(s|ala|väl)|\bturvas|\bjääksoo|\braba\b|\bmadalsoo|\bmärgala|\bmulla süsinik|\bsüsiniku sidumi|"
    r"\bmoor(land|lands|boden|schutz|grünland|wald|es)?\b|\bhochmoor|\bniedermoor|\banmoor|\borganische böden|\bkohlenstoffreiche böden|"
    r"\bwiedervernäss|\bpaludikultur|\btorf(moos|ersatz|frei)|\btorffrei|\bbodenkohlenstoff|\bcarbon farming", re.I)
EXCLUDE = re.compile(r"\bhydrogen\b|\bvety\b|marine sediment|\bocean\b", re.I)

_MARK_SCOPE = ("RAJAUS:", "\nSÄÄNNÖT:")
_MARK_TERMS = ("YDINSANAT (rajaa tarvittaessa lähteen kieleen):", "\nTOIMIJAHAKU")


def _wrap(prefix, words, width=88):
    lines, cur = [], prefix
    for w in words:
        add = w + ", "
        if len(cur) + len(add) > width:
            lines.append(cur.rstrip())
            cur = "  "
        cur += add
    lines.append(cur.rstrip(", "))
    return lines


def terms_block():
    L = ["YDINSANAT (rajaa tarvittaessa lähteen kieleen):"]
    for lang, words in CORE_TERMS.items():
        L += _wrap(f"- {lang}: ", words)
    L += _wrap("- Natura 2000 -luontotyypit (hae koodilla ja nimellä): ", NATURA.split(", "))
    return "\n".join(L)


def render_guide(text):
    """Korvaa hakuohjeen RAJAUS- ja YDINSANAT-kohdat tämän tiedoston sisällöllä."""
    for (start, end), new in ((_MARK_SCOPE, SCOPE_TEXT), (_MARK_TERMS, terms_block())):
        i = text.index(start)
        j = text.index(end, i)
        text = text[:i] + new + "\n" + text[j:]
    return text


def check():
    """Ydinsanat, joita SCOPE ei tunnista eikä niitä ole merkitty laajoiksi (BROAD)."""
    return [(lang, w) for lang, ws in CORE_TERMS.items() for w in ws
            if w not in BROAD and not SCOPE.search(w) and not SCOPE.search(f"{w} soil")]
