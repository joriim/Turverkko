"""Lähdeaineisto: hankkeet, ohjelmat, osaamiskeskukset, julkaisut ja dokumentoidut kytkökset.

Tämä tiedosto on ainoa käsin muokattava aineisto. Kaikki luvut ovat lähteistä (url-kenttä).
None = lähde ei kerro. Ks. CONTRIBUTING.md."""

THEMES = {
    "T1": "Turvetuotantoalueiden ennallistaminen ja jälkikäyttö",
    "T2": "Turvepellot: vettäminen, vedenpinnan säätö, tulosperusteiset maksut",
    "T3": "Kosteikkoviljely (paludikulttuuri) ja turpeen korvaajat",
    "T4": "Suometsät: metsitys, ojitettujen suometsien hoito ja ennallistaminen",
    "T5": "Luonnontilaisten soiden suojelu ja ennallistaminen",
    "T6": "Maankäyttösektorin päästöt: KHK-mittaus, päästökertoimet, inventaario, MRV",
    "T7": "Osaamiskeskittymät, klusterit ja tiedonvälitys",
    "T8": "Maanomistajat, maankäytön suunnittelu ja turpeesta luopumisen sosioekonomia",
}

COUNTRIES = {
    "FI": "Suomi", "SE": "Ruotsi", "EE": "Viro", "LV": "Latvia",
    "IE": "Irlanti", "DE-NI": "Niedersachsen", "EU": "Ylikansallinen (Interreg)",
}

# Ohjelmataso (allokaatiot ja tavoitteet)
PROGRAMMES = [
    dict(id="P-FI-JTF", country="FI", fund="JTF", period="2021–27", eur=465_000_000,
         scope="14 maakuntaa (mm. Etelä-, Keski- ja Pohjois-Pohjanmaa, Keski-Suomi)",
         focus=["T1","T3","T8"],
         targets="1 900 pk-yritystä; 4 000 yritystä TKI-yhteistyöhön; 1 800 innovaatiota; 3 700 työpaikkaa",
         realised=None,
         url="https://finland.representation.ec.europa.eu/uutiset/eun-koheesiopolitiikka-suomi-saa-yli-465-miljoonaa-euroa-oikeudenmukaisen-ilmastosiirtyman-2022-12-21_fi"),
    dict(id="P-FI-PP-JTF", country="FI", fund="JTF", period="2021–27", eur=119_000_000,
         scope="Pohjois-Pohjanmaa", focus=["T7","T1","T8"],
         targets="Jako: TKI ~37 %, pk-yritykset ~44 %, osaaminen ~14 %, turvealueiden ennallistaminen ~5 %",
         realised=None, url="https://www.pohjois-pohjanmaa.fi/wp-content/uploads/2023/04/JTF-tiedote2-1.pdf"),
    dict(id="P-EE-JTF", country="EE", fund="JTF", period="2021–27", eur=354_000_000,
         scope="Ida-Virumaa", focus=[],
         targets="Öljyliuskeesta luopuminen 2040 – ei turvepainotusta, mukana vertailuna",
         realised="Matkailuhankkeita lähes 100 M€; kritiikkiä kiireisistä päätöksistä ja paperille jääneistä suurhankkeista",
         url="https://news.err.ee/1608745423/ida-viru-county-to-receive-354-million-for-green-transition-eu-confirms"),
    dict(id="P-LV-JTF", country="LV", fund="JTF", period="2021–27", eur=192_000_000,
         scope="Vidzeme, Latgale, Kurzeme, Zemgale", focus=["T1","T3","T6","T8"],
         targets="Turvesektorin siirtymä; historiallisten turvealueiden inventointi",
         realised=None, url="https://ec.europa.eu/regional_policy/whats-new/newsroom/12-01-2022-eu-cohesion-policy-eur192-million-for-latvia-s-just-climate-transition_en"),
    dict(id="P-IE-JTF", country="IE", fund="JTF", period="2021–27", eur=169_000_000,
         scope="Midlands (turveteollisuuden alue)", focus=["T1","T2","T7","T8"],
         targets="500 pk-yritystä; 12 500 ha ennallistettu; organogeenisten maiden Centre of Excellence",
         realised="Maksettu edunsaajille 51 M€, EU-nostot 7 M€ (8/2026); 2 toimea à 15 M€ poistettu 3/2026 → 10 000 ha ja 60 latauspistettä pois tavoitteista",
         url="https://www.travelextra.ie/auditor-general-finds-repeated-failures-to-utilise-just-transition-fund/"),
    dict(id="P-SE-JTF", country="SE", fund="JTF", period="2021–27", eur=156_000_000,
         scope="Norrbotten, Västerbotten, Gotland", focus=[],
         targets="Teräs- ja metalliteollisuuden fossiilivapaus – ei turvepainotusta, mukana vertailuna",
         realised=None, url="https://ec.europa.eu/regional_policy/whats-new/panorama/2023/11/15-11-2023-just-transition-fund-helps-sweden-move-towards-climate-neutrality_en"),
    dict(id="P-DE-NI", country="DE-NI", fund="—", period="2021–27", eur=0,
         scope="Niedersachsen ei kuulu Saksan JTF-alueisiin (NRW, Brandenburg, Saksi, Saksi-Anhalt)",
         focus=[], targets="Turvemaat rahoitetaan EAKR/EFRE:n (KliMo) ja ELER/MSR:n kautta",
         realised=None, url="https://ec.europa.eu/regional_policy/whats-new/newsroom/21-10-2022-eu-cohesion-policy-eur2-5-billion-for-a-just-climate-transition-in-germany_en"),
    dict(id="P-EE-KF", country="EE", fund="KF", period="2014–20", eur=81_000_000,
         scope="Koko Viro: jääkturvealueiden korjaaminen", focus=["T1"],
         targets="≥2 000 ha ennallistettu (n. 10 000 ha:sta) vuoteen 2023",
         realised="2021: suunnitelmat ja rahoitus 2 000 ha:lle; Laiuse saavuttanut tavoitevedenpinnan",
         url="https://www.err.ee/1608302574/eesti-peab-paari-aastaga-taastama-paar-tuhat-hektarit-jaaksoid"),
    dict(id="P-FI-MSR", country="FI", fund="MSR", period="2014–20", eur=None,
         scope="Manner-Suomi", focus=["T2","T5"],
         targets="Kehittämishankkeita ~7 700 (76 % Leaderin kautta)",
         realised="Kosteikkosopimuksia 1 474 ha (tavoite 1 100 ha); yritystuki 7 900 yritykselle, 15 500 työpaikkaa",
         url="https://arkisto.maaseutu.fi/uploads/Tiivistelma_Manner-Suomen-maaseudun-kehittamisohjelman-2014-2020-raportti-vuodelta-2024.pdf"),
]

# Hanketaso. evidence: 0 ei tietoa, 1 laadullinen kuvaus, 2 määrälliset tavoitteet,
# 3 raportoituja mitattuja tuloksia, 4 avoin data / vertaisarvioitu
PROJECTS = [
    dict(id="FI-01", country="FI", region="Etelä- ja Keski-Pohjanmaa", fund="JTF", period="2021–27",
         name="TUKKA – Turvemaiden kestävän käytön osaamisklusteri", lead="HY Ruralia (SeAMK, Metsäkeskus, Chydenius)",
         start=2023, end=2027, eur_total=83758, eur_eu=None, themes=["T7","T8","T1","T2","T4"],
         outputs="Klusteri, 21 jäsenorganisaatiota; testialueet EP ja KP", evidence=1,
         url="https://researchportal.helsinki.fi/fi/projects/turvemaiden-kest%C3%A4v%C3%A4n-k%C3%A4yt%C3%B6n-osaamisklusterin-aktivointi-ja-koordi/"),
    dict(id="FI-02", country="FI", region="Etelä-Pohjanmaa", fund="JTF", period="2021–27",
         name="PohjaNeva – Myllynevan ennallistaminen (Alavus)", lead="Etelä-Pohjanmaan ELY",
         start=2024, end=None, eur_total=12722, eur_eu=None, themes=["T1"],
         outputs="10 ha kosteikko; ravinnekuorman ja päästöjen vähentäminen", evidence=2,
         url="https://www.sttinfo.fi/tiedote/70637574/entisen-turvetuotantoalueen-ennallistamishanke-kaynnistyy-alavudella-etela-pohjanmaapublisherId=69817874&lang=fi"),
    dict(id="FI-03", country="FI", region="Pohjois-Pohjanmaa, Kainuu, Lappi", fund="JTF", period="2021–27",
         name="PUHTI – Turvetuotantoalueiden ennallistamisten vauhdittaminen", lead="Pohjois-Pohjanmaan ELY",
         start=2025, end=None, eur_total=None, eur_eu=None, themes=["T1"],
         outputs="Kohteiden tunnistus, esiselvitykset, toteuttajien haku, vesistökunnostussuunnitelmat", evidence=1,
         url="https://www.sttinfo.fi/tiedote/70848438/turvetuotantoalueiden-ennallistamista-vauhdittava-puhti-hanke-on-kaynnistynyt-kainuu-lappi-pohjois-pohjanmaapublisherId=69817869&lang=fi"),
    dict(id="EE-02", country="EE", region="Koko Viro", fund="KF", period="2014–20",
         name="Jääkturvealueiden korjaaminen (mm. Laiuse)", lead="(toteuttaja ei lähteessä)",
         start=2016, end=2023, eur_total=None, eur_eu=81_000_000, themes=["T1"],
         outputs="≥2 000 ha; Laiuse tavoitevedenpinnassa", evidence=3,
         url="https://www.err.ee/1608302574/eesti-peab-paari-aastaga-taastama-paar-tuhat-hektarit-jaaksoid"),
    dict(id="LV-01", country="LV", region="Koko Latvia", fund="JTF", period="2021–27",
         name="PeatTransform – turvesektorin TKI-pohjainen siirtymä", lead="LSFRI Silava + 6 tutkimuslaitosta",
         start=2025, end=2029, eur_total=5_588_265, eur_eu=4_750_025, themes=["T6","T3","T1","T7","T8"],
         outputs="≥50 artikkelia (≥5 Q1); >30 KHK-seurantakohdetta; ≥10 kasvualustareseptiä; ≥4 kemiallista prototyyppiä; ≥1 patentti; Centre of Excellence",
         evidence=2, url="https://www.silava.lv/en/research/projects/PeatTransform"),
    dict(id="LV-02", country="LV", region="Vidzeme, Latgale, Kurzeme, Zemgale", fund="JTF", period="2021–27",
         name="Historiallisten turvealueiden elvyttäminen", lead="Suunnittelualueet / CFLA",
         start=2024, end=2026, eur_total=2_250_000, eur_eu=1_920_000, themes=["T1","T8"],
         outputs="≥9 000 ha inventointi; turvepolttolaitosten korvausselvitys", evidence=2,
         url="https://www.esfondi.lv/en/about-eu-funds/news/planning-regions-to-receive-eur1-92-million-from-eu-funds-to-boost-investments-in-the-just-transition-fund"),
    dict(id="LV-03", country="LV", region="Koko Latvia", fund="EAKR", period="2014–20",
         name="Ilmastopolitiikkaan sovitetut ratkaisut nostetuille turvemaille ja paludikulttuuri", lead="LSFRI Silava (postdoc)",
         start=2021, end=2023, eur_total=None, eur_eu=None, themes=["T1","T3"],
         outputs="Jälkikäyttöskenaariot 4 turvealueelle; paludikulttuuriratkaisut", evidence=2,
         url="https://silava.lv/en/projects/climate-policy-adapted-solutions-for-extracted-peatlands-and-paludiculture-implementation"),
    dict(id="IE-01", country="IE", region="Midlands", fund="EIP", period="2014–20",
         name="Farm Carbon – tulosperusteiset maksut turvemaiden hiiliviljelyyn", lead="Green Restoration Ireland",
         start=2021, end=2023, eur_total=1_147_000, eur_eu=None, themes=["T2","T6"],
         outputs="23 tilaa; vettäminen ~95 ha + 40 ha suo; arvio 320–690 tCO2e vältetty; KHK-perustaso mitattu; Irish Peatland Code -luonnos",
         evidence=3, url="https://eu-cap-network.ec.europa.eu/sites/default/files/2023-10/EUCAP-GoodPracticeReport-EIP-AGRI-OperationalGroupFarmCarbon.pdf"),
    dict(id="IE-02", country="IE", region="Midlands", fund="EIP", period="2014–20",
         name="FarmPEAT – tulosperusteinen ympäristöohjelma kohosoiden ympärille", lead="Wetland Surveys Ireland / Nature Based Agri Solutions",
         start=2021, end=2023, eur_total=1_213_800, eur_eu=None, themes=["T2","T5"],
         outputs="8 aluetta; elinympäristöjen pisteytys 0–10; koulutus", evidence=2,
         url="https://eu-cap-network.ec.europa.eu/projects/farmpeat-farm-payments-ecological-and-agricultural-transitions-project_de"),
    dict(id="NI-01", country="DE-NI", region="Niedersachsen", fund="EAKR", period="2014–20",
         name="KliMo – Klimaschutz durch Moorentwicklung (ohjelma, 33 hanketta)", lead="NMU / NLWKN",
         start=2016, end=2023, eur_total=None, eur_eu=None, themes=["T5","T2","T1"],
         outputs="12 vettämis-, 12 valmistelu- ja 9 kestävän käytön hanketta", evidence=1,
         url="https://www.lbeg.niedersachsen.de/download/140086/Uebersicht_zu_den_Projekten_Klimaschutz_durch_Moorentwicklung_Ulrich_Sippel_NMU.pdf"),
    dict(id="NI-02", country="DE-NI", region="Niedersachsen", fund="EAKR", period="2014–20",
         name="Produktketten aus Niedermoorbiomasse (paludikulttuuri)", lead="NLWKN-verbundprojekt",
         start=None, end=None, eur_total=None, eur_eu=None, themes=["T3"],
         outputs="Lähde ei raportoi", evidence=0,
         url="https://www.nlwkn.niedersachsen.de/startseite/naturschutz/fach_und_forderprogramme/klimaschutz_durch_moorentwicklung/produktketten_aus_niedermoorbiomasse/efre-verbundprojekt-produktketten-aus-niedermoorbiomasse-206903.html"),
    dict(id="NI-03", country="DE-NI", region="Niedersachsen", fund="MSR", period="2014–20",
         name="FKU – maanhankinnat suokohteille (ELER)", lead="ML / MU",
         start=2017, end=2020, eur_total=None, eur_eu=15_000_000, themes=["T5"],
         outputs="Sitoumukset 4,78 M€ (2017) ja 4,03 M€ (2018), pääosin maanostoihin", evidence=2,
         url="https://www.lbeg.niedersachsen.de/download/140086/Uebersicht_zu_den_Projekten_Klimaschutz_durch_Moorentwicklung_Ulrich_Sippel_NMU.pdf"),
    # --- Osaamiskeskusten verkostojen hankkeet (lisätty 31.10.2026) ---
    dict(id="FI-06", country="FI", region="Etelä-Pohjanmaa", fund="JTF", period="2021–27",
         name="Suopaikka – suonpohjien paikkatietopohjainen jälkikäytön suunnittelu", lead="SeAMK (rahoitus Keski-Suomen ELY)",
         start=2023, end=2026, eur_total=245000, eur_eu=None, themes=["T1","T3","T8"], hub="H-FI",
         outputs="Jälkikäyttösuunnitelmat maanomistajille, kosteikko- ja soistamiskohteet, sopimusmallit", evidence=1,
         url="https://lehti.seamk.fi/kestavat-ruokaratkaisut/suopaikka-alkanut-seamkin-ensimmaisena-jtf-hankkeena/?print=pdf"),
    dict(id="FI-07", country="FI", region="Etelä-Pohjanmaa, Pirkanmaa", fund="?", period="2021–27",
         name="TUPSU – Turvetuotantoalueiden palauttaminen suometsäksi", lead="HY INAR (HY metsätieteet, IL, Oulun yliopisto, SeAMK)",
         start=2024, end=2026, eur_total=None, eur_eu=None, themes=["T1","T4","T6"], hub="H-FI",
         outputs="Naarasnevan jatkuva CO2/N2O/CH4-asema + >80 kammiopistettä; vertaisarvioitu kannattavuustutkimus (Suo 2025)", evidence=4,
         url="https://lehti.seamk.fi/verkkolehti/tupsun-maastokausi-alkoi/?print=pdf"),
    dict(id="FI-08", country="FI", region="Etelä-Pohjanmaa", fund="?", period="2021–27",
         name="Turvevapaa ruokaketju – kosteikkoviljelypilotti Santanevalla", lead="SeAMK",
         start=None, end=None, eur_total=None, eur_eu=None, themes=["T3"], hub="H-FI",
         outputs="Rahkasammal- ja osmankäämipilotti entisellä turvetuotantoalueella; turpeen korvaajien kokeet", evidence=1,
         url="https://lehti.seamk.fi/verkkolehti/yhteista-kehittamista-ja-kokeiluja-katsaus-luonnonvara-ala-ja-biotalous-tiimin-vuoteen-2025/?print=pdf"),
    dict(id="FI-09", country="FI", region="Kymenlaakso", fund="JTF", period="2021–27",
         name="SuoLiike – suonpohjien uusi viljelyliiketoiminta", lead="Luke, Kinno, SYKLI",
         start=None, end=None, eur_total=None, eur_eu=None, themes=["T3","T1","T8"],
         outputs="Kaupallisesti kannattavat suonpohjien viljelymallit; tutustuminen Silavaan 8/2025", evidence=1,
         url="https://silava.lv/en/news/the-visit-of-finnish-peatland-management-specialists-at-lsfri-silava-for-knowledge-exchange"),
]

PROJECTS.append(dict(id="FI-10", country="FI", region="Pohjois-Karjala", fund="JTF", period="2021–27",
     name="Kasvua sammalesta Pohjois-Karjala – rahkasammalen viljely", lead="(toteuttaja ei lähteessä)",
     start=None, end=None, eur_total=None, eur_eu=None, themes=["T3"],
     outputs="Lähde mainitsee vain hankkeen nimen ja aiheen", evidence=0,
     url="https://www.uef.fi/fi/artikkeli/soiden-ennallistaminen-voi-tuottaa-ilmastoa-viilentavaa-vaikutusta-jo-muutaman-vuosikymmenen-aikana"))

# Osaamiskeskukset (CoE / klusterit)
HUBS = [
    dict(id="H-FI-AKA", country="FI", name="PeatResC – Suot, ilmastonmuutos ja ennallistaminen (Akatemian huippuyksikkö)", fund="Kansallinen",
         budget="5 M€ Suomen Akatemia", years="2026–2033", status="käynnistynyt 1/2026",
         members="Yli 70 tutkijaa: UEF (johtaja Tuittila), IL (Lohila, Aalto), HY (Väliranta), Aalto (Rautiainen)", projects=["X-FI-PEATRESC"],
         target="Päätöstukea siihen, miten, missä ja kuinka laajasti soita ennallistetaan; ilmasto- ja monimuotoisuusvaikutusten ristiriidat",
         url="https://uefconnect.uef.fi/en/peatresc/"),
    dict(id="H-FI", country="FI", name="Turvemaaklusteri (TUKKA)", fund="JTF",
         budget="83 758 € koordinaatio", years="2023–2027", status="käynnissä",
         members="21 jäsentä (2023) → 25 toimijaa (2025)", projects=["FI-01","FI-06","FI-07","FI-08"],
         target="Tutkimus ja käytäntö yhteen; maanomistajafoorumit EP ja KP",
         url="https://jyx.jyu.fi/jyx/Record/jyx_123456789_107454/Description"),
    dict(id="H-LV", country="LV", name="PeatTransform Centre of Excellence", fund="JTF",
         budget="4,75 M€ JTF / 5,59 M€", years="2025–2029", status="käynnistynyt",
         members="7 tutkimuslaitosta (Silava, LU, RTU, LBTU, IES, LatHort, AREI)", projects=["LV-01"],
         target="≥50 artikkelia (≥5 Q1), >30 KHK-seurantakohdetta, ≥1 patentti",
         url="https://www.silava.lv/en/research/projects/PeatTransform"),
    dict(id="H-IE-JTF", country="IE", name="JTF Centre of Excellence (kestävä maankäyttö)", fund="JTF",
         budget="ei julkista", years="2021–27", status="toteutusta ei löytynyt",
         members="Eastern and Midland Regional Assembly (hallinnoija)", projects=[],
         target="Organogeenisten maiden päästövähennykset, viljelykokeet turvemailla",
         url="https://pact-for-skills.ec.europa.eu/stakeholders-and-business/funding-opportunities/just-transition-fund-jtf-ireland-eastern-and-midland-region_en"),
    dict(id="H-IE-LIFE", country="IE", name="Peatlands and People – Centre of Excellence -osio", fund="LIFE",
         budget="9,89 M€ EU / 27,4 M€", years="2020–2027", status="käynnissä",
         members="Bord na Móna, EPA, University of Galway, DHLGH, Intrigo", projects=["X-IE-LIFE"],
         target="2 900 ha Natura-kohosuota ennallistettu, 7 000 ha BnM-alueita kunnostettu, demonstraatiokohteet",
         url="https://webgate.ec.europa.eu/life/publicWebsite/project/details/5435"),
    dict(id="H-IE-GAL", country="IE", name="All-Ireland Peatlands Centre of Excellence (Galway)", fund="Kansallinen",
         budget="ei julkista", years="2025–", status="avattu 12/2025",
         members="University of Galway Ryan Institute; RePEAT: Trinity College Dublin", projects=["X-IE-GAL"],
         target="Turvemaiden suojelu, tieto, koulutus ja politiikkatuki",
         url="https://www.universityofgalway.ie/about-us/news-and-events/news-archive/2025/december/all-ireland-peatlands-centre-of-excellence-launched-.html"),
]

# Julkaisut ja muut tuotokset. verified=False: otsikko löytyi hakemistosta, metatiedot avaamatta
PUBS = [
    dict(id="J1", hub="H-FI", project="FI-01", year=2025, type="ammattijulkaisu", verified=True,
         authors="Teixeira, Iivari, Liinamaa, Pihlaja, Kurki, Matilainen, Kaipainen",
         title="Etelä-Pohjanmaan turvemailla on käynnissä haastava kestävyyskoe",
         venue="AMK-kestävyysvuosikirja 2025, HUMAK Julkaisuja 192, s. 87–91", themes=["T7","T8"],
         url="https://jyx.jyu.fi/jyx/Record/jyx_123456789_107454/Description"),
    dict(id="J2", hub="H-FI", project="FI-07", year=2025, type="vertaisarvioitu", verified=True,
         authors="Lauhanen, Laasasenaho, Aro, Ojanen, Minkkinen, Jokelainen, Liutu, Lohila",
         title="Metsityksen taloudellinen kannattavuus paksuturpeisilla suonpohjilla",
         venue="Suo – Mires and Peat 76(1): 23–36", themes=["T4","T1"],
         url="https://lehti.seamk.fi/verkkolehti/metsitys-voi-olla-kannattavaa-paksuturpeisilla-suonpohjilla/?print=pdf"),
    dict(id="J3", hub="H-FI", project="FI-07", year=2024, type="tiedote / mittausasema", verified=True,
         authors="SeAMK, HY, IL, Oulun yliopisto",
         title="Naarasnevalla alkaa suonpohjien metsityksen monimuotoisuus- ja N2O-seuranta",
         venue="SeAMK-verkkolehti 11.4.2024", themes=["T6","T4"],
         url="https://lehti.seamk.fi/verkkolehti/naarasnevan-mittausasemalla-alkaa-suonpohjien-metsityksen-monimuotoisuusvaikutusten-ja-n2o-paastojen-seuranta/?print=pdf"),
    dict(id="J4", hub="H-FI", project="FI-01", year=None, type="ammattijulkaisu", verified=False,
         authors="(ei avattu)", title="Irlantilaiset asiantuntijat vierailulla Suomessa: yhteisiä haasteita, erilaisia ratkaisuja",
         venue="JYX-julkaisuarkisto", themes=["T7"], link_to="IE",
         url="https://jyx.jyu.fi/handle/123456789/105416"),
    dict(id="J5", hub="H-FI", project="FI-01", year=None, type="ammattijulkaisu", verified=False,
         authors="(ei avattu)", title="Yhteistyö Irlannin kanssa auttaa laajentamaan ymmärrystä eurooppalaisista turvemaista",
         venue="JYX-julkaisuarkisto", themes=["T7"], link_to="IE",
         url="https://jyx.jyu.fi/jyx/Record/jyx_123456789_109406"),
    dict(id="J6", hub="H-FI", project="FI-01", year=None, type="ammattijulkaisu", verified=False,
         authors="(ei avattu)", title="Suolla soi moniääninen muutos: turvemaiden kestävä käyttö rakentuu alhaalta ylöspäin",
         venue="JYX-julkaisuarkisto", themes=["T8","T7"],
         url="https://jyx.jyu.fi/handle/123456789/109405"),
    dict(id="J7", hub="H-LV", project="LV-01", year=2026, type="konferenssiabstrakti", verified=True,
         authors="Retike, Stivrins, Lazdins, Zakenfelde, Kasparinskis, Turks, Rubauskis, Zute, Jakovels",
         title="PeatTransform: Supporting the Transition of the Peat Sector towards Climate Neutrality in Latvia",
         venue="EGU General Assembly 2026, EGU26-10980", themes=["T6","T3","T1"],
         url="https://meetingorganizer.copernicus.org/EGU26/EGU26-10980.html"),
    dict(id="J8", hub="H-LV", project="LV-01", year=2026, type="tapahtuma", verified=True,
         authors="LSFRI Silava", title="PeatTransform-seminaari: viisi tutkimussuuntaa, ~100 osallistujaa",
         venue="Silava 8.1.2026", themes=["T7"],
         url="https://silava.lv/en/news/seminar-peattransform-towards-climate-neutrality-in-the-peat-sector-held-at-lsfri-silava"),
    dict(id="J9", hub="H-LV", project="FI-09", year=2025, type="tapahtuma", verified=True,
         authors="Luke, Kinno, SYKLI, Silava", title="Suomalainen SuoLiike-hanke Silavassa: paludikulttuurin päästöt, kuitupohjaiset kasvualustat",
         venue="Silava 20.8.2025", themes=["T3","T6"], link_to="FI",
         url="https://silava.lv/en/news/the-visit-of-finnish-peatland-management-specialists-at-lsfri-silava-for-knowledge-exchange"),
    dict(id="J10", hub="H-IE-LIFE", project="X-IE-LIFE", year=2022, type="raportti", verified=True,
         authors="Mc Hugh, P.", title="Stakeholder Engagement and Partnership Report for Phase 1, EU LIFE Peatlands and People",
         venue="University of Galway, tekninen julkaisu", themes=["T7"],
         url="https://research.universityofgalway.ie/en/publications/stakeholder-engagement-and-partnership-report-for-phase-1-eu-life-4/"),
    dict(id="J11", hub="H-IE-GAL", project="X-IE-GAL", year=2025, type="aineisto", verified=True,
         authors="University of Galway, Trinity College Dublin (RePEAT)", title="Bog Commissioner -karttojen digitointi (1810–1814): >200 000 ha entistä turvemaata tunnistettu",
         venue="RePEAT, DAFM + EPA", themes=["T6"],
         url="https://www.universityofgalway.ie/about-us/news-and-events/news-archive/2025/december/all-ireland-peatlands-centre-of-excellence-launched-.html"),
]

PUBS += [
    dict(id="J12", hub="H-FI-AKA", project="X-FI-PEATRESC", year=2026, type="vertaisarvioitu", verified=True,
         authors="Tahvanainen, T. (UEF)", title="Restoration of forestry-drained oligotrophic peatlands can bring climate change mitigation within a few decades",
         venue="Restoration Ecology 2026 – UEF:n turveyhteisö, ei merkitty huippuyksikön tuotokseksi", themes=["T4","T6"],
         url="https://www.uef.fi/fi/artikkeli/soiden-ennallistaminen-voi-tuottaa-ilmastoa-viilentavaa-vaikutusta-jo-muutaman-vuosikymmenen-aikana"),
    dict(id="J13", hub="H-FI-AKA", project="X-FI-PEATRESC", year=2026, type="kenttäkohde", verified=True,
         authors="UEF / Hiilipörssi Oy", title="Piitsonsuo: kolmen ennallistamismenetelmän vertailu, lampareiden vertailu Siikanevaan",
         venue="Hiilipörssi, tiedeartikkeli", themes=["T5","T6"],
         url="https://hiiliporssi.fi/tiede/ainutlaatuisia-tutkimuksia-hiiliporssin-ennallistamalla-piitsonsuolla/"),
    dict(id="J14", hub="H-FI-AKA", project="X-FI-PEATRESC", year=2026, type="kenttäkohde", verified=True,
         authors="UEF", title="Kyyrönsuo (Kontiolahti): rahkasammalviljelyn tutkimus entisellä turvetuotantoalueella",
         venue="Yle 24.1.2026", themes=["T3"],
         url="https://yle.fi/a/74-20204573"),
]

# Dokumentoidut kytkökset keskusten välillä
LINKS = [
    dict(a="H-FI-AKA", b="H-FI", kind="dokumentoitu", note="Annalea Lohila on PeatResC:n johtajistossa ja johtaa TUKKA-verkoston TUPSU-hanketta"),
    dict(a="H-FI-AKA", b="H-LV", kind="ei kytköstä", note="Molemmat rakentavat KHK-mittauksia ja ennallistamistietoa, ei löydettyä yhteyttä"),
    dict(a="H-FI", b="IE", kind="dokumentoitu", note="TUKKA: irlantilaisten vierailu Suomessa ja yhteistyöartikkelit (JYX); irlantilainen kumppani ei vahvistettu"),
    dict(a="FI-09", b="H-LV", kind="dokumentoitu", note="SuoLiike (JTF, Kymenlaakso) Silavassa 20.8.2025; ei TUKKA-verkoston hanke"),
    dict(a="H-IE-LIFE", b="H-IE-GAL", kind="dokumentoitu", note="University of Galway on LIFE IP:n partneri ja Galwayn keskuksen isäntä"),
    dict(a="H-IE-JTF", b="H-IE-LIFE", kind="ei kytköstä", note="Sama alue ja tavoite, ei löydettyä yhteyttä"),
    dict(a="H-FI", b="H-LV", kind="ei kytköstä", note="Teemat lähes samat (T1, T3, T7, T8), ei suoraa TUKKA–PeatTransform-yhteyttä"),
]

# Vertailukohteet rajauksen ulkopuolelta: näyttävät päällekkäisyydet, eivät summiin
CONTEXT = [
    dict(id="X-FI-PEATRESC", country="FI", fund="Kansallinen", name="PeatResC – Akatemian turvemaiden huippuyksikkö (5 M€, 2026–33)",
         themes=["T5","T1","T6","T7"], note="UEF:n johtama huippuyksikkö (IL, HY, Aalto). Sama tietotarve kuin PeatTransformissa ja Irlannin keskuksissa",
         url="https://uefconnect.uef.fi/en/peatresc/"),
    dict(id="X-IE-LIFE", country="IE", fund="LIFE", name="LIFE IP Peatlands and People (EU 9,9 M€ / 27,4 M€)",
         themes=["T1","T5","T7"], note="2020–2027, Bord na Móna koordinoi. Sisältää Peatlands Centre of Excellence -osion → päällekkäinen JTF:n CoE-tavoitteen kanssa",
         url="https://webgate.ec.europa.eu/life/publicWebsite/project/details/5435"),
    dict(id="X-IE-GAL", country="IE", fund="Kansallinen", name="All-Ireland Peatlands CoE ja RePEAT (Galway)",
         themes=["T7","T6","T5"], note="Avattu 12/2025; RePEAT rahoittajina DAFM ja EPA. Kolmas irlantilainen turvemaiden osaamiskeskus",
         url="https://www.universityofgalway.ie/about-us/news-and-events/news-archive/2025/december/all-ireland-peatlands-centre-of-excellence-launched-.html"),
    dict(id="X-IE-NAT", country="IE", fund="Kansallinen", name="Midlands Just Transition -ohjelma (135,8 M€, 47 hanketta, 2020)",
         themes=["T1","T8"], note="Kansallinen rinnakkaisohjelma; ennallistaminen 108 M€ + Bord na Móna",
         url="https://www.shannonside.ie/news/e135-8m-350-jobs-announced-just-transition-programme-173604"),
    dict(id="X-DE-SH", country="DE-SH", fund="EIP", name="Our Moor Future Oldenburger Graben (Schleswig-Holstein, 0,5 M€)",
         themes=["T2","T8","T7"], note="Naapurialue; suoyhteisön vyöhykejako ≈ TUKKA-klusterin tavoite",
         url="https://eu-cap-network.ec.europa.eu/projects/our-moor-future-oldenburger-graben-cooperative-moorland-oldenburger-graben-schleswig_de"),
]

# Tunnistetut kaksoiskirjaukset (sama hanke eri nimellä/summalla)
DUPLICATES = [
    dict(a="IE-01", alias="Green Restoration Ireland, 1 050 646 € (ministeriön tiedote 2/2021)",
         note="Tiedotteen summa ≠ CAP Network -rekisterin 1 147 000 €"),
    dict(a="IE-02", alias="Wetland Surveys Ireland, 1 113 800 € (ministeriön tiedote 2/2021)",
         note="Tiedotteen summa ≠ rekisterin 1 213 800 €"),
]


# ---------------------------------------------------------------------------
# Organisaatiot. type: yliopisto | amk | tutkimuslaitos | viranomainen | yritys | jarjesto | muu
ORGS = [
    dict(id="seamk", name="Seinäjoen ammattikorkeakoulu (SeAMK)", country="FI", type="amk"),
    dict(id="hy", name="Helsingin yliopisto", country="FI", type="yliopisto"),
    dict(id="il", name="Ilmatieteen laitos", country="FI", type="tutkimuslaitos"),
    dict(id="uef", name="Itä-Suomen yliopisto", country="FI", type="yliopisto"),
    dict(id="aalto", name="Aalto-yliopisto", country="FI", type="yliopisto"),
    dict(id="oy", name="Oulun yliopisto", country="FI", type="yliopisto"),
    dict(id="luke", name="Luonnonvarakeskus (Luke)", country="FI", type="tutkimuslaitos"),
    dict(id="metsakeskus", name="Suomen metsäkeskus", country="FI", type="viranomainen"),
    dict(id="chydenius", name="Kokkolan yliopistokeskus Chydenius", country="FI", type="yliopisto"),
    dict(id="ep-ely", name="Etelä-Pohjanmaan ELY-keskus", country="FI", type="viranomainen"),
    dict(id="pp-ely", name="Pohjois-Pohjanmaan ELY-keskus", country="FI", type="viranomainen"),
    dict(id="ks-ely", name="Keski-Suomen ELY-keskus", country="FI", type="viranomainen"),
    dict(id="kinno", name="Kouvola Innovation Oy (Kinno)", country="FI", type="yritys"),
    dict(id="sykli", name="SYKLI Environmental School of Finland", country="FI", type="jarjesto"),
    dict(id="hiiliporssi", name="Hiilipörssi Oy", country="FI", type="yritys"),
    dict(id="silava", name="LSFRI Silava", country="LV", type="tutkimuslaitos"),
    dict(id="lu", name="Latvian yliopisto", country="LV", type="yliopisto"),
    dict(id="rtu", name="Riga Technical University", country="LV", type="yliopisto"),
    dict(id="lbtu", name="Latvia University of Life Sciences and Technologies", country="LV", type="yliopisto"),
    dict(id="ies", name="Institute for Environmental Solutions", country="LV", type="tutkimuslaitos"),
    dict(id="lathort", name="Institute of Horticulture (LatHort)", country="LV", type="tutkimuslaitos"),
    dict(id="arei", name="Institute of Agricultural Resources and Economics", country="LV", type="tutkimuslaitos"),
    dict(id="cfla", name="Central Finance and Contracting Agency", country="LV", type="viranomainen"),
    dict(id="lv-regions", name="Latvian suunnittelualueet", country="LV", type="viranomainen"),
    dict(id="gri", name="Green Restoration Ireland", country="IE", type="jarjesto"),
    dict(id="nbas", name="Nature Based Agri Solutions (FarmPEAT)", country="IE", type="yritys"),
    dict(id="wsi", name="Wetland Surveys Ireland", country="IE", type="yritys"),
    dict(id="irl", name="Irish Rural Link", country="IE", type="jarjesto"),
    dict(id="umeras", name="Umeras Community Development Group", country="IE", type="jarjesto"),
    dict(id="galway", name="University of Galway", country="IE", type="yliopisto"),
    dict(id="teagasc", name="Teagasc", country="IE", type="tutkimuslaitos"),
    dict(id="tcd", name="Trinity College Dublin", country="IE", type="yliopisto"),
    dict(id="bnm", name="Bord na Móna", country="IE", type="yritys"),
    dict(id="epa-ie", name="Environmental Protection Agency (IE)", country="IE", type="viranomainen"),
    dict(id="dhlgh", name="Department of Housing, Local Government and Heritage", country="IE", type="viranomainen"),
    dict(id="intrigo", name="Intrigo Ltd", country="IE", type="yritys"),
    dict(id="emra", name="Eastern and Midland Regional Assembly", country="IE", type="viranomainen"),
    dict(id="nmu", name="Niedersächsisches Umweltministerium", country="DE-NI", type="viranomainen"),
    dict(id="ml-ni", name="Niedersächsisches Landwirtschaftsministerium", country="DE-NI", type="viranomainen"),
    dict(id="nlwkn", name="NLWKN", country="DE-NI", type="viranomainen"),
]

# Osallistuminen: (organisaatio, hanke tai keskus, rooli, lähde). rooli: koordinaattori | partneri | rahoituksen välittäjä | kenttäkumppani
PARTICIPATION = [
    ("hy", "FI-01", "koordinaattori", "https://researchportal.helsinki.fi/fi/projects/turvemaiden-kest%C3%A4v%C3%A4n-k%C3%A4yt%C3%B6n-osaamisklusterin-aktivointi-ja-koordi/"),
    ("seamk", "FI-01", "partneri", "https://researchportal.helsinki.fi/fi/projects/turvemaiden-kest%C3%A4v%C3%A4n-k%C3%A4yt%C3%B6n-osaamisklusterin-aktivointi-ja-koordi/"),
    ("metsakeskus", "FI-01", "partneri", "https://researchportal.helsinki.fi/fi/projects/turvemaiden-kest%C3%A4v%C3%A4n-k%C3%A4yt%C3%B6n-osaamisklusterin-aktivointi-ja-koordi/"),
    ("chydenius", "FI-01", "partneri", "https://researchportal.helsinki.fi/fi/projects/turvemaiden-kest%C3%A4v%C3%A4n-k%C3%A4yt%C3%B6n-osaamisklusterin-aktivointi-ja-koordi/"),
    ("ep-ely", "FI-02", "koordinaattori", "https://www.sttinfo.fi/tiedote/70637574/entisen-turvetuotantoalueen-ennallistamishanke-kaynnistyy-alavudella-etela-pohjanmaapublisherId=69817874&lang=fi"),
    ("pp-ely", "FI-03", "koordinaattori", "https://www.sttinfo.fi/tiedote/70848438/turvetuotantoalueiden-ennallistamista-vauhdittava-puhti-hanke-on-kaynnistynyt-kainuu-lappi-pohjois-pohjanmaapublisherId=69817869&lang=fi"),
    ("seamk", "FI-06", "koordinaattori", "https://lehti.seamk.fi/kestavat-ruokaratkaisut/suopaikka-alkanut-seamkin-ensimmaisena-jtf-hankkeena/?print=pdf"),
    ("ks-ely", "FI-06", "rahoituksen välittäjä", "https://lehti.seamk.fi/kestavat-ruokaratkaisut/suopaikka-alkanut-seamkin-ensimmaisena-jtf-hankkeena/?print=pdf"),
    ("hy", "FI-07", "koordinaattori", "https://lehti.seamk.fi/verkkolehti/tupsun-maastokausi-alkoi/?print=pdf"),
    ("il", "FI-07", "partneri", "https://lehti.seamk.fi/verkkolehti/tupsun-maastokausi-alkoi/?print=pdf"),
    ("oy", "FI-07", "partneri", "https://lehti.seamk.fi/verkkolehti/tupsun-maastokausi-alkoi/?print=pdf"),
    ("seamk", "FI-07", "partneri", "https://lehti.seamk.fi/verkkolehti/tupsun-maastokausi-alkoi/?print=pdf"),
    ("seamk", "FI-08", "koordinaattori", "https://lehti.seamk.fi/verkkolehti/yhteista-kehittamista-ja-kokeiluja-katsaus-luonnonvara-ala-ja-biotalous-tiimin-vuoteen-2025/?print=pdf"),
    ("luke", "FI-09", "partneri", "https://silava.lv/en/news/the-visit-of-finnish-peatland-management-specialists-at-lsfri-silava-for-knowledge-exchange"),
    ("kinno", "FI-09", "partneri", "https://silava.lv/en/news/the-visit-of-finnish-peatland-management-specialists-at-lsfri-silava-for-knowledge-exchange"),
    ("sykli", "FI-09", "partneri", "https://silava.lv/en/news/the-visit-of-finnish-peatland-management-specialists-at-lsfri-silava-for-knowledge-exchange"),
    ("uef", "X-FI-PEATRESC", "koordinaattori", "https://uefconnect.uef.fi/en/peatresc/"),
    ("il", "X-FI-PEATRESC", "partneri", "https://uefconnect.uef.fi/en/peatresc/"),
    ("hy", "X-FI-PEATRESC", "partneri", "https://uefconnect.uef.fi/en/peatresc/"),
    ("aalto", "X-FI-PEATRESC", "partneri", "https://uefconnect.uef.fi/en/peatresc/"),
    ("hiiliporssi", "X-FI-PEATRESC", "kenttäkumppani", "https://hiiliporssi.fi/tiede/ainutlaatuisia-tutkimuksia-hiiliporssin-ennallistamalla-piitsonsuolla/"),
    ("silava", "LV-01", "koordinaattori", "https://www.silava.lv/en/research/projects/PeatTransform"),
    ("lu", "LV-01", "partneri", "https://www.silava.lv/en/research/projects/PeatTransform"),
    ("rtu", "LV-01", "partneri", "https://www.silava.lv/en/research/projects/PeatTransform"),
    ("lbtu", "LV-01", "partneri", "https://www.silava.lv/en/research/projects/PeatTransform"),
    ("ies", "LV-01", "partneri", "https://www.silava.lv/en/research/projects/PeatTransform"),
    ("lathort", "LV-01", "partneri", "https://www.silava.lv/en/research/projects/PeatTransform"),
    ("arei", "LV-01", "partneri", "https://www.silava.lv/en/research/projects/PeatTransform"),
    ("lv-regions", "LV-02", "koordinaattori", "https://www.esfondi.lv/en/about-eu-funds/news/planning-regions-to-receive-eur1-92-million-from-eu-funds-to-boost-investments-in-the-just-transition-fund"),
    ("cfla", "LV-02", "rahoituksen välittäjä", "https://www.esfondi.lv/en/about-eu-funds/news/planning-regions-to-receive-eur1-92-million-from-eu-funds-to-boost-investments-in-the-just-transition-fund"),
    ("silava", "LV-03", "koordinaattori", "https://silava.lv/en/projects/climate-policy-adapted-solutions-for-extracted-peatlands-and-paludiculture-implementation"),
    ("gri", "IE-01", "koordinaattori (päätelty)", "https://www.gov.ie/en/department-of-agriculture-food-and-the-marine/press-releases/minister-hackett-announces-22-million-funding-for-peatlands-projects/"),
    ("galway", "IE-01", "partneri", "https://eu-cap-network.ec.europa.eu/sites/default/files/2023-10/EUCAP-GoodPracticeReport-EIP-AGRI-OperationalGroupFarmCarbon.pdf"),
    ("teagasc", "IE-01", "partneri", "https://eu-cap-network.ec.europa.eu/sites/default/files/2023-10/EUCAP-GoodPracticeReport-EIP-AGRI-OperationalGroupFarmCarbon.pdf"),
    ("wsi", "IE-02", "koordinaattori (päätelty)", "https://www.gov.ie/en/department-of-agriculture-food-and-the-marine/press-releases/minister-hackett-announces-22-million-funding-for-peatlands-projects/"),
    ("nbas", "IE-02", "partneri", "https://eu-cap-network.ec.europa.eu/projects/farmpeat-farm-payments-ecological-and-agricultural-transitions-project_de"),
    ("irl", "IE-02", "partneri", "https://eu-cap-network.ec.europa.eu/projects/farmpeat-farm-payments-ecological-and-agricultural-transitions-project_de"),
    ("umeras", "IE-02", "partneri", "https://eu-cap-network.ec.europa.eu/projects/farmpeat-farm-payments-ecological-and-agricultural-transitions-project_de"),
    ("bnm", "X-IE-LIFE", "koordinaattori", "https://webgate.ec.europa.eu/life/publicWebsite/project/details/5435"),
    ("epa-ie", "X-IE-LIFE", "partneri", "https://webgate.ec.europa.eu/life/publicWebsite/project/details/5435"),
    ("galway", "X-IE-LIFE", "partneri", "https://webgate.ec.europa.eu/life/publicWebsite/project/details/5435"),
    ("dhlgh", "X-IE-LIFE", "partneri", "https://webgate.ec.europa.eu/life/publicWebsite/project/details/5435"),
    ("intrigo", "X-IE-LIFE", "partneri", "https://webgate.ec.europa.eu/life/publicWebsite/project/details/5435"),
    ("galway", "X-IE-GAL", "koordinaattori", "https://www.universityofgalway.ie/about-us/news-and-events/news-archive/2025/december/all-ireland-peatlands-centre-of-excellence-launched-.html"),
    ("tcd", "X-IE-GAL", "partneri", "https://www.universityofgalway.ie/about-us/news-and-events/news-archive/2025/december/all-ireland-peatlands-centre-of-excellence-launched-.html"),
    ("bnm", "X-IE-NAT", "partneri", "https://www.shannonside.ie/news/e135-8m-350-jobs-announced-just-transition-programme-173604"),
    ("emra", "H-IE-JTF", "rahoituksen välittäjä", "https://pact-for-skills.ec.europa.eu/stakeholders-and-business/funding-opportunities/just-transition-fund-jtf-ireland-eastern-and-midland-region_en"),
    ("nmu", "NI-01", "koordinaattori", "https://www.lbeg.niedersachsen.de/download/140086/Uebersicht_zu_den_Projekten_Klimaschutz_durch_Moorentwicklung_Ulrich_Sippel_NMU.pdf"),
    ("nlwkn", "NI-01", "partneri", "https://www.lbeg.niedersachsen.de/download/140086/Uebersicht_zu_den_Projekten_Klimaschutz_durch_Moorentwicklung_Ulrich_Sippel_NMU.pdf"),
    ("nlwkn", "NI-02", "koordinaattori", "https://www.nlwkn.niedersachsen.de/startseite/naturschutz/fach_und_forderprogramme/klimaschutz_durch_moorentwicklung/produktketten_aus_niedermoorbiomasse/efre-verbundprojekt-produktketten-aus-niedermoorbiomasse-206903.html"),
    ("ml-ni", "NI-03", "koordinaattori", "https://www.lbeg.niedersachsen.de/download/140086/Uebersicht_zu_den_Projekten_Klimaschutz_durch_Moorentwicklung_Ulrich_Sippel_NMU.pdf"),
    ("nmu", "NI-03", "partneri", "https://www.lbeg.niedersachsen.de/download/140086/Uebersicht_zu_den_Projekten_Klimaschutz_durch_Moorentwicklung_Ulrich_Sippel_NMU.pdf"),
]

# Ohjelma → hanke -rahoitussuhteet (vain varmistetut)
FUNDED_BY = [
    ("P-FI-JTF", "FI-01"), ("P-FI-JTF", "FI-02"), ("P-FI-JTF", "FI-06"), ("P-FI-JTF", "FI-09"), ("P-FI-JTF", "FI-10"),
    ("P-FI-PP-JTF", "FI-03"), ("P-FI-JTF", "P-FI-PP-JTF"),
    ("P-EE-KF", "EE-02"),
    ("P-LV-JTF", "LV-01"), ("P-LV-JTF", "LV-02"),
    ("P-IE-JTF", "H-IE-JTF"),
]

# Rajattu pois 31.10.2026, kun tarkastelu rajattiin turvemaihin ja maaperään
REMOVED = [
    dict(id="FI-04", name="VEP – Vetytalouden mahdollisuudet ruokaketjussa", reason="vety"),
    dict(id="FI-05", name="EIP Energiaälykäs eteläpohjalainen maatila", reason="tilan energiaratkaisu, ei turvemaata"),
    dict(id="EE-01", name="Harvinaisten maametallien magneettitehdas, Narva", reason="teollisuusinvestointi"),
    dict(id="SE-01", name="H2-Labs – vedyn testilaitos, Piteå", reason="vety"),
]

# ---------------------------------------------------------------------------
# Hakulähteiden tulokset (hakulahteet/tulokset/*.csv), ks. src/tuonti.py
import tuonti as _tuonti  # noqa: E402

_ORG_EXTRA = [
    dict(id="syke", name="Suomen ympäristökeskus (Syke)", country="FI", type="tutkimuslaitos"),
    dict(id="keha", name="ELY-keskusten kehittämis- ja hallintokeskus (KEHA)", country="FI", type="viranomainen"),
    dict(id="rmk", name="Riigimetsa Majandamise Keskus (RMK)", country="EE", type="viranomainen"),
]
_known = {o["id"] for o in ORGS}
ORGS += [o for o in _ORG_EXTRA if o["id"] not in _known]

_new, _orgs, _part, _enrich, _removed = _tuonti.load()
_known = {o["id"] for o in ORGS}
ORGS += [o for o in _orgs if o["id"] not in _known]
PROJECTS += _new
PARTICIPATION += _part
REMOVED += _removed

# Hakulähteiden rivit, jotka täydentävät olemassa olevia hankkeita tai vertailukohteita
_byid = {p["id"]: p for p in PROJECTS + CONTEXT}
for _pid, _rows in _enrich.items():
    _p = _byid[_pid]
    _b = sum(_tuonti._num(r["budjetti_eur"]) or 0 for r in _rows) or None
    _e = sum(_tuonti._num(r["eu_osuus_eur"]) or 0 for r in _rows) or None
    if "eur_total" in _p:
        _p["eur_total"] = _p["eur_total"] or _b
        _p["eur_eu"] = _p["eur_eu"] or _e
    _p.setdefault("urls", [_p["url"]])
    _p["urls"] += [r["url"] for r in _rows if r["url"] not in _p["urls"]]
    for r in _rows:
        _who = [(r["toteuttaja"], "edunsaaja")] + [(x, "partneri") for x in r["partnerit"].split(";") if x.strip()]
        for _w, _role in _who:
            _o = _tuonti.org_of(_w)
            if not _o:
                continue
            _oid, _oname = _o
            if _oid not in {o["id"] for o in ORGS}:
                ORGS.append(dict(id=_oid, name=_oname, country=_p["country"], type=_tuonti.org_type(_oname)))
            if (_oid, _pid) not in {(x[0], x[1]) for x in PARTICIPATION}:
                PARTICIPATION.append((_oid, _pid, _role, r["url"]))

# Viro: aiempi EE-02-rivi käytti ohjelmatason summaa (KF 81 M€ koko maalle); Kohesio antaa hankkeen omat luvut
_ee = next(r for r in _enrich.get("EE-02", []))
_byid["EE-02"].update(lead="Riigimetsa Majandamise Keskus (RMK)", start=2016, end=2023,
    eur_total=_tuonti._num(_ee["budjetti_eur"]), eur_eu=_tuonti._num(_ee["eu_osuus_eur"]),
    outputs="2 000 ha hylättyjä turvetuotantoalueita ennallistettu (Kohesio); Laiuse saavutti tavoitevedenpinnan (ERR 2021). Koko KF-ohjelman jääksoiden korjaamiseen varattiin 81 M€.")

# PohjaNeva: Kohesio kertoo koko hankkeen, aiempi rivi vain Myllynevan osakohteen
_byid["FI-02"].update(
    name="PohjaNeva – Vauhtia pohjalaismaakuntien JTF-ennallistamisiin",
    start=2024, end=2027,
    outputs="Pohjalaismaakuntien turvetuotantoalueiden ennallistamisen vauhdittaminen; esimerkkinä Myllynevan 10 ha:n kosteikko (Alavus, 12 722 €)")
