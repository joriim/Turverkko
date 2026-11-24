"""Muuntaa 24.11.2026 tehdyt haut (hakulahteet/vienti/2026-11-24/) tuontipohjan muotoon (hakulahteet/tulokset/).

Lähteet ja rajaus (kaikki päätökset näkyvät tässä tiedostossa):
- 3 LIFE: life_turvemaahankkeet_v3.xlsx. Mukana LIFE14 ja uudemmat (kaudet 2014–20 ja 2021–27), joissa
  turvemaiden rooli on pääteema tai osatoimenpide. Pelkät maininnat ja vanhemmat kaudet jäävät pois.
- 4 keep.eu: keep_eu_turvehankkeet.csv (käsin käyty läpi). Päivämäärät ja budjetit raakaviennistä
  (keep_eu_raakavienti_bog.xlsx), kun hanke löytyy sieltä. Kumppanin Niedersachsen-sijainti NUTS1-koodista DE9.
- 5 EURA 2021: eura2021_tulokset.json (ryhmähankkeen osat yhdistetään yhdeksi hankkeeksi).
- 6 Maaseutu.fi: maaseuturahasto_msr_leader.xlsx, kuvaukset hankerekisteri_suometsa.csv:stä.
- 7 research.fi: research_fi_rahoitukset.csv. Henkilökohtaisissa apurahoissa saajan nimi korvataan
  merkinnällä "henkilökohtainen apuraha", jotta yksityishenkilöiden nimiä ei julkaista sivustolla.

Aja:  python scripts/haku/muunna_2026_11_24.py
"""
import csv, json, re
from pathlib import Path

import openpyxl

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "hakulahteet" / "vienti" / "2026-11-24"
OUT = ROOT / "hakulahteet" / "tulokset"
DATE = "2026-11-24"
FIELDS = ["lahde", "haettu", "hakusana", "hanke_nimi", "lyhenne", "maa", "alue", "rahasto", "ohjelmakausi", "alku", "loppu",
          "toteuttaja", "partnerit", "budjetti_eur", "eu_osuus_eur", "kuvaus", "tuotokset", "url"]
EXCLUDED = []  # (lähde, nimi, peruste) → hakulahteet/tulokset/poissuljetut-2026-11-24.csv


def write(name, rows):
    with open(OUT / name, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS, quoting=csv.QUOTE_NONNUMERIC)
        w.writeheader()
        for r in rows:
            w.writerow({k: ("" if r.get(k) is None else r.get(k, "")) for k in FIELDS})
    print(f"{name}: {len(rows)} riviä")


def num(v):
    try:
        return round(float(str(v).replace(" ", "").replace(",", "."))) if v not in (None, "") else ""
    except ValueError:
        return ""


def sheet(path, name=None):
    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    rows = list((wb[name] if name else wb.worksheets[0]).iter_rows(values_only=True))
    return [dict(zip(rows[0], r)) for r in rows[1:] if any(c not in (None, "") for c in r)]


SCOPE_CC = {"Finland": "FI", "Sweden": "SE", "Estonia": "EE", "Latvia": "LV", "Ireland": "IE"}


HOME_WORDS = {
    "FI": r"\boy\b|\bry\b|\bsr\b|yliopisto|keskus|suomen|saatio|säätiö|kaupunki|kunta|metsa|metsä|mtk|finland|\boyj\b|ammattikorkeakoulu|tapio",
    "SE": r"lansstyrelsen|länsstyrelsen|kommun\b|universitet\b|\bab\b|sveriges|skogs|sweden|svenska|region\b|naturskydds",
    "LV": r"latvijas|\bsia\b|biedriba|biedrība|nodibinajums|universitate|valsts|parvalde|pārvalde|dome\b|novada|latvia|fonds\b",
    "EE": r"sihtasutus|\bmtu\b|\bmtü\b|\bou\b|\bas\b|eesti|ulikool|ülikool|estonia|keskkonna|ministeerium",
    "IE": r"department|council|coillte|teoranta|ireland|irish|university college|agency|trust|\bltd\b|\bclg\b|bord na|galway|teagasc",
    "DE-NI": r"niedersachs|hannover|landkreis|stiftung|nlwkn|landesbetrieb|naturschutz",
}


def split_partners(items, home=None):
    """Erottaa kumppanit: rajausalueen kumppanit merkitään maakoodilla "(FI)", muut siirretään kuvaukseen,
    koska tuonti antaisi merkitsemättömälle kumppanille hankkeen maan."""
    keep_, other = [], []
    for p in items:
        p = p.strip()
        if not p:
            continue
        m = re.match(r"^(.*?)(?:,\s*|\s+\(|\s+\[)(Finland|Sweden|Estonia|Latvia|Ireland|DE-NI|FI|SE|EE|LV|IE|[A-Z][a-z]+(?: [A-Z][a-z]+)*)[)\]]?\s*$", p)
        if m and m.group(2) in SCOPE_CC.values() or (m and m.group(2) == "DE-NI"):
            keep_.append(f"{m.group(1).strip()} ({m.group(2)})")
        elif m and m.group(2) in SCOPE_CC:
            keep_.append(f"{m.group(1).strip()} ({SCOPE_CC[m.group(2)]})")
        elif m:
            other.append(f"{m.group(1).strip()} ({m.group(2)})")
        elif home and home in HOME_WORDS and re.search(HOME_WORDS[home], p, re.I):
            keep_.append(p)  # maa ei tiedossa, nimi viittaa hankkeen maahan
        elif home:
            other.append(p)  # maa ei tiedossa eikä nimi viittaa hankkeen maahan: ei kirjata kumppaniksi
        else:
            keep_.append(p)
    return "; ".join(keep_), ("Muut kumppanit: " + "; ".join(other) + ".") if other else ""


def period(year):
    return "2014-2020" if year and int(year) < 2021 else "2021-2027"


# ---------------------------------------------------------------------------
# 3 LIFE
LIFE_COUNTRY = {"Suomi": "FI", "Ruotsi": "SE", "Viro": "EE", "Latvia": "LV", "Irlanti": "IE",
                "Saksa (Niedersachsen)": "DE-NI", "Saksa (koordinaattori, toteutus kohdemaissa)": "EU"}


LIFE_NAME_FIX = {"Metshallitus": "Metsähallitus", "Metshallitus, Parks & Wildlife Finland": "Metsähallitus, Parks & Wildlife Finland",
                 "County administrative board of Skne": "County Administrative Board of Skåne"}


def life():
    out = []
    for d in sheet(SRC / "life_turvemaahankkeet_v3.xlsx", "LIFE-hankkeet"):
        start = str(d["alku"] or "")[:10]
        name = (d["nimi"] or "").strip()
        if d["turvemaiden_rooli"] == "Maininta":
            EXCLUDED.append(("3", name, "turvemaat vain mainintana (LIFE-taulukon luokitus)"))
            continue
        if not start or start[:4] < "2014":
            EXCLUDED.append(("3", name, f"ohjelmakausi rajauksen ulkopuolella (alku {start[:4]})"))
            continue
        c = LIFE_COUNTRY.get(d["maa"])
        if not c:
            EXCLUDED.append(("3", name, f"maa rajauksen ulkopuolella ({d['maa']})"))
            continue
        ref = d["ohjelmakausi"]
        parts, others = split_partners(re.split(r"\s*;\s*", d["partnerit"] or ""), LIFE_COUNTRY.get(d["maa"]))
        note = f" Huom: {d['huomio']}" if d["huomio"] else ""
        out.append(dict(lahde=3, haettu=DATE, hakusana=d["osumasanat"] or "", hanke_nimi=name, lyhenne=d["lyhenne"] or ref,
                        maa=c, alue="", rahasto="LIFE", ohjelmakausi=f"LIFE {period(start[:4])}", alku=start, loppu=str(d["loppu"] or "")[:10],
                        toteuttaja=LIFE_NAME_FIX.get(d["toteuttaja"] or "", d["toteuttaja"] or ""), partnerit=parts,
                        budjetti_eur=num(d["budjetti_eur"]), eu_osuus_eur=num(d["eu_osuus_eur"]),
                        kuvaus=f"LIFE {ref}, alaohjelma {d['alaohjelma']}. Turvemaiden rooli: {d['turvemaiden_rooli']}. "
                               f"{(d['kuvausote'] or '').strip()}{note} {others}".strip(),
                        tuotokset="", url=f"https://webgate.ec.europa.eu/life/publicWebsite/search?reference={ref.replace(' ', '%20')}"))
    return out


# ---------------------------------------------------------------------------
# 4 keep.eu
# Rajaus: kumppani jollakin Turverkon kuudesta alueesta ja ohjelmakausi 2014–20 tai 2021–27.
KEEP_EXCLUDE = {
    "20099": "ei kumppania Turverkon alueilta (Mecklenburg, Puola, Liettua, Venäjä)",
    "21673": "ei kumppania Turverkon alueilta; DESIRE-hankkeen valmisteluraha",
    "26723": "vesistöhanke, turve mainittu vain sivulauseessa",
    "31432": "pelastuspalveluhanke, turve mainittu kerran",
    "2812": "ohjelmakausi 2000–2006 rajauksen ulkopuolella",
    "2989": "ohjelmakausi 2000–2006 ja alue rajauksen ulkopuolella",
    "2990": "ohjelmakausi 2000–2006 ja alue rajauksen ulkopuolella",
    "13309": "ohjelmakausi 2000–2006; turpeen nosto ja vienti (energia/teollisuus)",
    "35162": "ei kumppania Turverkon alueilta (Alppien alue)",
    "34599": "ei kumppania Turverkon alueilta (Itävalta–Baijeri)",
    "32420": "ei kumppania Turverkon alueilta (Itävalta–Baijeri)",
    "20832": "ei kumppania Turverkon alueilta (Saksi–Tšekki)",
    "20858": "ei kumppania Turverkon alueilta (Saksi–Tšekki)",
}
KEEP_COUNTRY = {"31625": "FI", "27513": "FI", "23241": "FI", "29062": "LV", "34965": "DE-NI", "29076": "DE-NI",
                "20746": "IE", "20733": "IE"}
NAME_EN = {"Finland": "FI", "Sweden": "SE", "Estonia": "EE", "Latvia": "LV", "Ireland": "IE"}


def keep():
    raw_p = sheet(SRC / "keep_eu_raakavienti_bog.xlsx", "Search results, projects")
    raw_o = sheet(SRC / "keep_eu_raakavienti_bog.xlsx", "Search results, partners")
    ni = {(o["Organisation in English"] or "").strip().lower() for o in raw_o if (o["NUTS1 code (or equivalent)"] or "") == "DE9"}
    ni |= {(o["Organisation in language 2"] or "").strip().lower() for o in raw_o if (o["NUTS1 code (or equivalent)"] or "") == "DE9"}
    # Niedersachsenin kumppanit, joita raakaviennissä ei ole (tarkistettu osoitteesta: kaikki Niedersachsenissa)
    ni |= {s.lower() for s in ["Landkreis Diepholz", "Hoch Schule Emden Leer", "Stiftung Ökowerk Emden", "Universität Vechta",
                               "Landwirtschaftskammer Niedersachsen", "Oldenburgisch-Ostfriesischer Wasserverband",
                               "Landesamt für Bergbau, Energie und Geologie", "Bundesanstalt für Geowissenschaften und Rohstoffe",
                               "Leibniz-Institut für Angewandte Geophysik", "Dachverband Feldberegnung Uelzen",
                               "Office for Regional Development, Weser and Ems Region", "Energiewert Cloppenburg GmbH",
                               "3N-Kompetenzzentrum Niedersachsen Netzwerk Nachwachsende Rohstoffe und Bioökonomie e.V.",
                               "Hochschule Osnabrück", "Jade Hochschule Oldenburg",
                               "Niedersachsen Netzwerk Nachwachsende Rohstoffe und Bioökonomie e.V."]}

    def raw_for(name):
        key = name.split("–")[0].split("(")[0].strip().lower()
        for p in raw_p:
            t = f"{p['Project acronym']} {p['Project name in English']} {p['Project name in language 2']}".lower()
            if key and (key in t or (p["Project acronym"] or "").lower() == key):
                return p
        return None

    def tag(partner):
        m = re.match(r"^(.*)\s+\(([^)]+)\)\s*$", partner.strip())
        if not m:
            return partner.strip()
        org, ctry = m.group(1).strip(), m.group(2)
        if ctry in NAME_EN:
            return f"{org} ({NAME_EN[ctry]})"
        if ctry == "Germany" and org.lower() in ni:
            return f"{org} (DE-NI)"
        return f"{org} [{ctry}]"

    out = []
    with open(SRC / "keep_eu_turvehankkeet.csv", encoding="utf-8-sig") as f:
        for d in csv.DictReader(f):
            kid, name = d["keep.eu ID"].strip(), d["Hanke"].strip()
            if kid in KEEP_EXCLUDE:
                EXCLUDED.append(("4", name, KEEP_EXCLUDE[kid]))
                continue
            partners, others = split_partners([tag(p) for p in re.split(r";\s*", d["Partnerit"]) if p.strip()])
            lead_c = NAME_EN.get(d["Maa"])
            lead_ni = d["Maa"] == "Germany" and d["Toteuttaja"].strip().lower() in ni
            c = KEEP_COUNTRY.get(kid) or lead_c or ("DE-NI" if lead_ni else "EU")
            lead = d["Toteuttaja"].strip() + (f" ({lead_c})" if c == "EU" and lead_c else " (DE-NI)" if c == "EU" and lead_ni else "")
            r = raw_for(name)
            prog = d["Ohjelmakausi"].replace("2014-2020", "2014-2020").strip()
            desc = f"{prog}. {d['Huomio']}. Epävarmuudet: {d['Epävarmuudet']}. {others}".strip()
            if "ENI CBC" in prog:
                desc = "ENI CBC -ulkorajaohjelma (kirjattu Interreg-ryhmään). " + desc
            out.append(dict(lahde=4, haettu=DATE, hakusana="peat; mire; bog", hanke_nimi=name, lyhenne="",
                            maa=c, alue="useita maita" if c == "EU" else "", rahasto="Interreg",
                            ohjelmakausi=prog if "Interreg" in prog else f"Interreg {prog}",
                            alku=str(r["Project start"])[:10] if r and r["Project start"] else "",
                            loppu=str(r["Project end"])[:10] if r and r["Project end"] else "",
                            toteuttaja=lead, partnerit=partners,
                            budjetti_eur=num(r["Project's total budget / expenditure"]) if r else "",
                            eu_osuus_eur=num(r["Project's EU funding"]) if r else "",
                            kuvaus=desc, tuotokset="", url=f"https://keep.eu/projects/{kid}/"))
    return out


# ---------------------------------------------------------------------------
# 5 EURA 2021
EURA_EXCLUDE = {"J11290": "yleinen yrittäjyyskoulutus turpeesta luopuvalla alueella, ei maankäyttöä (rajaus: ei yleisiä yritystukia)"}
EURA_NOT_VERIFIED = {"J10970", "J11106"}  # toteuttaja päätelty tai lukematta: ei kirjata organisaatioksi


def eura():
    data = json.loads((SRC / "eura2021_tulokset.json").read_text(encoding="utf-8"))
    groups = {}
    for d in data:
        if d["hankekoodi"] in EURA_EXCLUDE:
            EXCLUDED.append(("5", d["hankkeen_nimi"], EURA_EXCLUDE[d["hankekoodi"]]))
            continue
        groups.setdefault(d["hankkeen_nimi"], []).append(d)
    out = []
    for name, ds in groups.items():
        main = ds[0]
        a, _, b = (main["aika"] or "").partition("-")
        iso = lambda s: "-".join(f"{int(v):02d}" if len(v) < 3 else v for v in reversed(s.strip().split("."))) if s.strip() else ""
        others = [d["toteuttaja"] for d in ds[1:] if d["toteuttaja"] and d["hankekoodi"] not in EURA_NOT_VERIFIED]
        if "KEMMO" in name:
            others.append("Koulutuskeskus Sedu")  # nimetty päähankkeen kuvauksessa
        toteuttaja = re.sub(r"\s*\((nimi|päätelty)[^)]*\)", "", main["toteuttaja"] or "").split(",")[0].strip()
        out.append(dict(lahde=5, haettu=DATE, hakusana=main["hakusana"], hanke_nimi=name,
                        lyhenne="KEMMO" if "KEMMO" in name else "", maa="FI", alue=main["alue"] or "", rahasto="JTF",
                        ohjelmakausi="2021-2027", alku=iso(a), loppu=iso(b), toteuttaja=toteuttaja,
                        partnerit="; ".join(re.sub(r"\s*\((nimi|päätelty)[^)]*\)", "", o).split(",")[0].strip() for o in others),
                        budjetti_eur=sum(d["budjetti_eur"] or 0 for d in ds) or "", eu_osuus_eur=sum(d["eu_osuus_eur"] or 0 for d in ds) or "",
                        kuvaus=" ".join(f"[{d['hankekoodi']}] {d['kuvaus']}" for d in ds),
                        tuotokset=main["tuotokset"] or "", url=f"https://eura2021.fi/hanketietopalvelu?koodi={main['hankekoodi']}"))
    return out


# ---------------------------------------------------------------------------
# 6 Maaseutu.fi (maaseuturahasto ja Leader)
MSR_EXCLUDE = {
    "Kosteikko-osaaminen kasvuun": "vesiensuojelukosteikkojen rakentaminen, turvemaayhteyttä ei löytynyt",
    "Järvi-Suomen kosteikko- ja valuma-aluesuunnittelun koulutushanke": "vesiensuojelukosteikot ja valuma-aluesuunnittelu, turvemaayhteyttä ei löytynyt",
    "Metsäopisto 1 – Wirtavesitiimi vahvistaa osaamistaan": "virtavesikunnostus; suot vain sivumaininta",
}


def msr():
    reg = {}
    with open(SRC / "hankerekisteri_suometsa.csv", encoding="utf-8-sig") as f:
        for d in csv.DictReader(f):
            reg[d["Otsikko"].strip()[:40].lower()] = d
    out = []
    for d in sheet(SRC / "maaseuturahasto_msr_leader.xlsx"):
        name = d["Hanke"].strip()
        if name in MSR_EXCLUDE:
            EXCLUDED.append(("6", name, MSR_EXCLUDE[name]))
            continue
        r = next((v for k, v in reg.items() if name.lower().startswith(k[:35])), None)
        aika = str(d["Hankeaika"] or "")
        yrs = re.findall(r"(20\d\d)", aika)
        def iso(s):
            m = re.match(r"(\d+)\.(\d+)\.(\d{4})", s.strip())
            return f"{m.group(3)}-{int(m.group(2)):02d}-{int(m.group(1)):02d}" if m else (s.strip()[:4] if s.strip()[:4].isdigit() else "")
        a, _, b = aika.partition("–")
        if r:
            a, b = r["Aloituspvm"], r["Lopetuspvm"]
        fund = "JTF" if "JTF" in str(d["Rahasto"]) else "MSR"
        kausi = "2021-2027" if fund == "JTF" else ("2014-2020" if "2014" in str(d["Ohjelmakausi"]) else "2021-2027")
        desc = (r["Kuvaus"].strip() if r else "") or ""
        desc = re.sub(r"\s+", " ", desc)[:1500]
        extra = f"Rahasto: {d['Rahasto']}. Alue: {d['Alue / Leader-ryhmä']}." + (f" Huom: {d['Huomio']}." if d["Huomio"] else "")
        out.append(dict(lahde=6, haettu=DATE, hakusana="turvemaa; suo; suometsä", hanke_nimi=name, lyhenne="", maa="FI",
                        alue=("-".join(w.capitalize() for w in r["Maakunta"].split("-")) if r else str(d["Alue / Leader-ryhmä"]).split(";")[0].replace(" elinvoimakeskus", "")),
                        rahasto=fund, ohjelmakausi=f"Maaseuturahasto {kausi}" if fund == "MSR" else kausi,
                        alku=iso(a) if a else (yrs[0] if yrs else ""), loppu=iso(b) if b else (yrs[-1] if yrs else ""),
                        toteuttaja=str(d["Toteuttaja"]).strip(), partnerit="",
                        budjetti_eur=num(d["Kokonaisbudjetti (€)"]), eu_osuus_eur="",
                        kuvaus=(desc + " " + extra).strip(), tuotokset="",
                        url="https://www.maaseutu.fi/hankkeet" + (f"#hankenumero-{r['Hankenumero']}" if r else "")))
    return out


# ---------------------------------------------------------------------------
# 7 research.fi
RFI_EXCLUDE = {
    "79702": "peruutettu kokonaan", "79890": "peruutettu kokonaan",
    "32888": "energiajärjestelmä (rajaus: ei energiaa)", "85272": "turve-energia, tutkijavierailu (rajaus: ei energiaa)",
    "34123": "yleinen ekosysteemimallinnus, turvemaa vain sovelluksena",
    "34096": "kasvillisuuden N2O-aineenvaihdunta, ei maaperää",
}
RFI_MAAPERA = {"78074", "27163"}  # maaperän päästöjen mittaus ja maan orgaaninen aines yleisesti
HORIZON = {"88531", "88304", "88297", "78911", "78914", "78915", "78921", "44892"}


def research_fi():
    out = []
    lines = (SRC / "research_fi_rahoitukset.csv").read_text(encoding="utf-8-sig").splitlines()[1:]
    for line in lines:
        if not line.strip():
            continue
        # Kumppanit on erotettu samalla puolipisteellä kuin sarakkeet: kiinteät sarakkeet luetaan alusta ja lopusta
        x = line.split(";")
        mid = [m.strip() for m in x[3:-4]]
        d = dict(id=x[0], rahasto=x[1], nimi=x[2], alku=x[-4].strip(), loppu=x[-3].strip(), budjetti_eur=x[-2], kuvaus=x[-1],
                 toteuttaja="; ".join(m for m in mid if m) if x[1] == "EU" else (mid[0] if mid else ""),
                 partnerit="" if x[1] == "EU" else "; ".join(m for m in mid[1:] if m))
        assert not d["alku"] or d["alku"].isdigit(), line
        if True:
            rid, name = d["id"].strip(), d["nimi"].strip()
            if rid in RFI_EXCLUDE:
                EXCLUDED.append(("7", name, RFI_EXCLUDE[rid]))
                continue
            note, who = d["kuvaus"].strip(), d["toteuttaja"].strip()
            funder = note.split(".")[0].split(",")[0].strip()
            org_words = re.search(r"yliopisto|keskus|laitos|universit|vtt|tapio|oy\b|metsäkeskus|syke|akademi|gtk|ymparisto|ympäristö", who, re.I)
            if not org_words and d["rahasto"] != "EU":
                who = "henkilökohtainen apuraha"
            if d["rahasto"] == "EU":
                fund = "Horizon" if rid in HORIZON else ("EAKR" if "ERDF" in note else "EU-muu")
                kausi = "2014-2020" if "ERDF" in note and int(d["alku"]) <= 2022 else period(d["alku"])
                finns = [p.strip() for p in re.split(r";", who) if p.strip() and "ei nimetty" not in p]
                if fund == "EAKR":
                    c, lead, partners = "FI", finns[0] if finns else "", "; ".join(finns[1:])
                else:
                    c, lead, partners = "EU", "Kansainvälinen konsortio", "; ".join(f"{p} (FI)" for p in finns)
            else:
                fund, kausi, c = "Kansallinen", period(d["alku"]), "FI"
                lead, partners = who, "; ".join(p.strip() for p in d["partnerit"].split(";") if p.strip())
            if rid in RFI_MAAPERA:
                note += " (rajaus: maaperä)"
            out.append(dict(lahde=7, haettu=DATE, hakusana="turvemaa; peatland; suo", hanke_nimi=name, lyhenne="", maa=c, alue="",
                            rahasto=fund, ohjelmakausi=f"{'Horizon' if fund == 'Horizon' else fund} {kausi}",
                            alku=d["alku"], loppu=d["loppu"], toteuttaja=lead, partnerit=partners,
                            budjetti_eur=num(d["budjetti_eur"]), eu_osuus_eur="" if fund == "Kansallinen" else "",
                            kuvaus=f"Rahoittaja: {funder}. {note}", tuotokset="",
                            url=f"https://research.fi/fi/results/funding/{rid}"))
    return out


if __name__ == "__main__":
    write("3-life-2026-11-24.csv", life())
    write("4-keep-eu-2026-11-24.csv", keep())
    write("5-eura2021-2026-11-24.csv", eura())
    write("6-maaseutu-2026-11-24.csv", msr())
    write("7-research-fi-2026-11-24.csv", research_fi())
    with open(OUT / "poissuljetut" / "2026-11-24.csv", "w", newline="", encoding="utf-8") if (OUT / "poissuljetut").is_dir() else open(ROOT / "hakulahteet" / "vienti" / "2026-11-24" / "poissuljetut.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["lahde", "hanke_nimi", "peruste"])
        w.writerows(EXCLUDED)
    print(f"poissuljettu {len(EXCLUDED)}")
