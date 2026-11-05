# Yhteysanalyysi

_Generoitu skriptillä `scripts/analyze.py`. Älä muokkaa käsin._

## Yhteenveto

- Toimijoita yhteistyöverkossa: **306**, vahvistettuja yhteistyösärmiä **247** (lisäksi 3 vahvistamatonta, jotka eivät ole mukana saarekkeissa eikä keskeisyydessä).
- Erillisiä yhteistyösaarekkeita: **81**, joista **18** sisältää vähintään kaksi hanketta tai keskusta (loput ovat yksittäisiä hankkeita toteuttajineen). Suurin kattaa 92 toimijaa.
- Usean maan saarekkeita: **4**. Maiden välisiä vahvistettuja yhteistyösärmiä: **11**.
- Yhteisjulkaisut mukaan lukien (organisaatioiden yhteiset turvemaa- ja maaperäjulkaisut, OpenAIRE): yhteisjulkaisusärmiä **97**, joista maiden välisiä **54**; saarekkeita **74**, joista usean maan **1**. Päällekkäisyysparien yhteys lasketaan tässä verkossa.
- Sisällöltään samankaltaisia hankepareja (tekstin samankaltaisuus ≥ 0.2, 148 vertailtavaa hanketta): **102**. Niistä
  - rinnakkaisia ilman yhteyttä (sama maa, samaan aikaan, ei yhteistä toimijaa eikä polkua ≤ 3); kohdekohtaisissa toteutushankkeissa tämä on usein tarkoituksellista, menetelmä- ja suunnitteluhankkeissa se viittaa päällekkäiseen työhön: **75**
  - peräkkäisiä samassa maassa ilman yhteyttä: **5**
  - puuttuvia maiden välisiä yhteyksiä: **5**
  - yhteydessä olevia (yhteinen toimija tai lyhyt polku): **14**
  - saman hankekokonaisuuden osia: **3**
- Todennäköisiä kaksoiskappaleita eri lähteistä (sama maa ja vuodet, yhteinen toimija tai samankaltainen teksti): **2**. Ne tarkistetaan ja yhdistetään `src/tuonti.py`:n `MATCH_EXISTING`-listalla (`analysis/kaksoisehdokkaat.csv`).

## Ennallistetut hehtaarit

Hehtaaritieto on **24** hankkeella. Ennallistavien toimenpiteiden (ennallistaminen, vettäminen, kosteikko) tavoitteita on yhteensä **6 177 ha** ja raportoitua toteumaa **96 ha**. Jo päättyneiden hankkeiden tavoitteita, joiden toteumaa lähde ei raportoi, on 2 260 ha.

Hehtaarit on kirjattu käsin lainauksineen tiedostoon `hakulahteet/tulokset/hehtaarit/hehtaarit.csv`. Inventoinnit, suunnitelmat, metsitys ja muu pinta-ala näytetään erikseen, eikä niitä lasketa ennallistettuihin.

| Maa | Hankkeita | Tavoite ha | Toteuma ha | Päättyneiden tavoite ha |
|---|---|---|---|---|
| DE-NI | 4 | 255 | 0 | 255 |
| EE | 1 | 2000 | 0 | 2000 |
| FI | 14 | 1422 | 1 | 5 |
| IE | 2 | 0 | 95 | 0 |
| LV | 2 | 1500 | 0 | 0 |
| SE | 1 | 1000 | 0 | 0 |

### Hinta hehtaaria kohden toimenpiteittäin

Budjetti jaettuna hankkeen ennallistavalla hehtaaritavoitteella (tai toteumalla, jos tavoitetta ei ole). Mukana vain hankkeet, joissa hehtaarit ovat päätuotos; pilotit ja kehityshankkeet näkyvät hanketaulukossa mutta eivät mediaaneissa. Budjetti sisältää usein myös suunnittelun, maanhankinnan, seurannan ja viestinnän, joten luku on hankkeen hinta hehtaaria kohden, ei ennallistamistyön yksikköhinta. Summat ovat nimellisiä euroja.

| Toimenpide | Hankkeita | Mediaani €/ha | Kvartiiliväli €/ha | Vaihteluväli €/ha | Painotettu €/ha (Σ€ / Σha) |
|---|---|---|---|---|---|
| ennallistaminen | 11 | 2 289 | 1 766–4 304 | 1 040–38 877 | 2 984 |
| kosteikko | 2 | 3 631 | 3 284–3 978 | 2 936–4 326 | 3 738 |
| vettäminen | 2 | 22 160 | 11 425–32 896 | 689–43 632 | 1 531 |

| Toimenpide · maa | Hankkeita | Mediaani €/ha | Painotettu €/ha |
|---|---|---|---|
| ennallistaminen · DE-NI | 2 | 28 216 | 23 826 |
| ennallistaminen · EE | 1 | 1 631 | 1 631 |
| ennallistaminen · FI | 6 | 1 986 | 1 645 |
| ennallistaminen · LV | 1 | 4 706 | 4 706 |
| ennallistaminen · SE | 1 | 2 696 | 2 696 |
| kosteikko · FI | 2 | 3 631 | 3 738 |
| vettäminen · DE-NI | 2 | 22 160 | 1 531 |

| Hanke | Maa | Toimenpide | € | ha | €/ha | Vertailukelpoinen |
|---|---|---|---|---|---|---|
| K-FI-cb20 Restoration of the Western Valkeasuo Mire | FI | ennallistaminen | 72 800 | 70 (tavoite) | 1 040 | kyllä |
| K-FI-e290 Restoration and water protection project of S | FI | ennallistaminen | 923 512 | 750 (tavoite) | 1 231 | kyllä |
| EE-02 Jääkturvealueiden korjaaminen (mm. Laiuse) | EE | ennallistaminen | 3 262 985 | 2 000 (tavoite) | 1 631 | kyllä |
| K-FI-06b9 Suokeidas - From peat production to diverse w | FI | ennallistaminen | 380 145 | 200 (tavoite) | 1 901 | kyllä |
| K-FI-b095 Aarreaitta - Restoring the Kanasuo peat extra | FI | ennallistaminen | 287 815 | 139 (tavoite) | 2 071 | kyllä |
| K-FI-2fcc Heinäpuro restoration project | FI | ennallistaminen | 41 210 | 18 (tavoite) | 2 289 | kyllä |
| K-SE-dbb8 Myrrestaurering i Norrbottens län (MyreN) – s | SE | ennallistaminen | 2 696 225 | 1 000 (tavoite) | 2 696 | kyllä |
| K-FI-6978 Peat Bogs to Wetlands | FI | ennallistaminen | 397 904 | 102 (tavoite) | 3 901 | kyllä |
| K-LV-cbb2 Restoration of bog ecosystems in SACs | LV | ennallistaminen | 7 058 824 | 1 500 (tavoite) | 4 706 | kyllä |
| K-DE-NI-3ac3 Rewetting of the hill moor in the forest town | DE-NI | ennallistaminen | 1 263 983 | 72 (tavoite) | 17 555 | kyllä |
| K-DE-NI-6f11 Rewetting of the slope moor Friedrichshäuser  | DE-NI | ennallistaminen | 1 166 300 | 30 (tavoite) | 38 877 | kyllä |
| K-FI-0ac6 Value from the carbon market for the next lan | FI | ennallistaminen | 788 547 | 8 (tavoite) | 98 568 | ei: Kehityshanke (hiilimarkkina); hehtaarit ovat pieni osa tuotoksista |
| K-FI-665a Transforming peat production areas in North O | FI | kosteikko | 161 484 | 55 (tavoite) | 2 936 | kyllä |
| K-FI-9cd5 Restoration of peat production areas in North | FI | kosteikko | 324 432 | 75 (tavoite) | 4 326 | kyllä |
| K-DE-NI-0e2b Rewetting Sauerbach | DE-NI | vettäminen | 103 403 | 150 (tavoite) | 689 | kyllä |
| IE-01 Farm Carbon – tulosperusteiset maksut turvema | IE | vettäminen | 1 147 000 | 95 (toteuma) | 12 074 | ei: EIP-kehityshanke; budjetti kattaa tulosperusteiset maksut, neuvonnan ja seurannan 23 tilalla |
| K-DE-NI-61e6 Wetting area at Westerbeck | DE-NI | vettäminen | 130 895 | 3 (tavoite) | 43 632 | kyllä |
| K-FI-3bb2 The restoration and sustainable further use o | FI | vettäminen | 220 269 | 5 (tavoite) | 44 054 | ei: Tutkimus- ja kehityspilotti; 5 ha koealue |


## Maiden väliset yhteydet

- DE-NI–IE: 2 (lähteellä vahvistettu)
- DE–DE-NI: 3 (lähteellä vahvistettu)
- EU–FI: 2 (lähteellä vahvistettu)
- EU–SE: 1 (lähteellä vahvistettu)
- FI–LV: 1 (lähteellä vahvistettu)
- FI–SE: 2 (lähteellä vahvistettu)
- FI–IE: 3 (kumppani vahvistamatta)

## Välittäjäorganisaatiot (välityskeskeisyys)

| Organisaatio | Maa | Hankkeita | Keskuksia | Välityskeskeisyys |
|---|---|---|---|---|
| Luonnonvarakeskus (Luke) | FI | 9 | 1 | 0.05 |
| LSFRI Silava | LV | 9 | 1 | 0.0275 |
| Seinäjoen ammattikorkeakoulu (SeAMK) | FI | 7 | 1 | 0.0173 |
| Oulun yliopisto | FI | 5 | 1 | 0.0119 |
| Latvian yliopisto | LV | 4 | 1 | 0.0117 |
| Institute of Horticulture (LatHort) | LV | 2 | 1 | 0.011 |
| Itä-Suomen yliopisto | FI | 4 | 1 | 0.01 |
| Suomen ympäristökeskus (Syke) | FI | 4 | 0 | 0.0068 |
| Helsingin yliopisto | FI | 5 | 2 | 0.0057 |
| Institute of Agricultural Resources and Economics | LV | 2 | 1 | 0.0034 |

## Osaamiskeskusten yhteiset organisaatiot

- H-FI ↔ H-FI-AKA: hy, il
- H-IE-GAL ↔ H-IE-LIFE: galway

## Päällekkäisyyden menetelmä

Hankkeiden nimi, kuvaus ja tuotokset verrataan TF-IDF-painotettuina. Monikielinen käsitesanasto yhdistää saman asian eri kielillä (esim. turve, peat, torv, kūdra, Torf). Samankaltaisuus on kosini väliltä 0–1. Kynnys on valittu tarkastelemalla pareja käsin, joten alla on tulokset usealla kynnyksellä. Eri kielillä kuvatut ja eri maiden hankkeet saavat järjestelmällisesti matalampia arvoja, koska paikannimet ja kielikohtaiset sanat eivät osu yhteen.

Lähdeaineiston kuvaukset ovat lyhyitä (keskimäärin noin 200 merkkiä), mikä heikentää erottelukykyä. Tulokset ovat ehdokkaita tarkistettavaksi, eivät todettuja päällekkäisyyksiä.

| Kynnys | Pareja | saman kokonaisuuden osat | rinnakkainen ilman yhteyttä | peräkkäiset samassa maassa | puuttuva yhteys | yhteydessä |
|---|---|---|---|---|---|---|
| 0.15 | 251 | 3 | 152 | 25 | 37 | 34 |
| 0.2 | 102 | 3 | 75 | 5 | 5 | 14 |
| 0.25 | 43 | 3 | 29 | 1 | 1 | 9 |
| 0.3 | 22 | 3 | 12 | 0 | 0 | 7 |
| 0.35 | 13 | 3 | 4 | 0 | 0 | 6 |
| 0.4 | 6 | 1 | 1 | 0 | 0 | 4 |

## Rinnakkainen ilman yhteyttä (15 samankaltaisinta)

_sama maa, samaan aikaan, ei yhteistä toimijaa eikä yhteistyöpolkua. Voi olla tarkoituksellista (eri kohteet) tai päällekkäistä työtä (sama menetelmä tai suunnittelu kahteen kertaan)._

| A | B | Samankaltaisuus | Yhteiset käsitteet ja sanat | Samaan aikaan |
|---|---|---|---|---|
| K-DE-NI-6f11 Rewetting of the slope moor Friedrichshäuser Bruch | K-DE-NI-c57b Rewetting of the hill moor at the forest town of W | 0.434 | trenche, hill, removin, drainag, moor, vettaminen | kyllä |
| K-DE-NI-3ac3 Rewetting of the hill moor in the forest town of W | K-DE-NI-6f11 Rewetting of the slope moor Friedrichshäuser Bruch | 0.397 | spring, hill, complex, moor, vettaminen, ennallistaminen | kyllä |
| K-FI-6978 Peat Bogs to Wetlands | K-FI-8d28 Restoration of Linttiräme after Peat Production | 0.382 | state, wetland, natural, peat, restora, constru | kyllä |
| K-DE-NI-0499 OptiMOOS – Subproject vegetation development and w | K-DE-NI-34e3 Monitoring of the peat moss field in the Ahlenmoor | 0.381 | moss, regard, cultiva, peat, turvepelto, turve | kyllä |
| K-DE-NI-c05c Gnarrenburger Moor – Area concept and water manage | K-DE-NI-dab1 Development of priorities in moor and climate prot | 0.327 | concept, protect, moor, climate, suunnittelu, turve | kyllä |
| K-DE-NI-0499 OptiMOOS – Subproject vegetation development and w | K-DE-NI-bd6b MOOSWEIT, Subproject 5 | 0.325 | moss, cultiva, peat, turvepelto, turve | kyllä |
| K-DE-NI-34e3 Monitoring of the peat moss field in the Ahlenmoor | K-DE-NI-bd6b MOOSWEIT, Subproject 5 | 0.318 | moss, cultiva, peat, turvepelto, turve | kyllä |
| K-FI-6978 Peat Bogs to Wetlands | K-FI-b095 Aarreaitta - Restoring the Kanasuo peat extraction | 0.31 | wetland, peat, kosteikko, restora, multifu, decommi | kyllä |
| K-DE-NI-0e2b Rewetting Sauerbach | K-DE-NI-b8d9 Optimisation of water balance in selected bogs of  | 0.305 | gifhorn, rewetti, measure, mittaus, vettaminen, moor | kyllä |
| K-DE-NI-9595 Management of moorland areas | K-DE-NI-b8d9 Optimisation of water balance in selected bogs of  | 0.305 | measure, rewetti, mittaus, bogs, vettaminen, suo | kyllä |
| K-DE-NI-03c5 Moorhausen moor area, test and demonstration areas | K-DE-NI-cc25 Model project Gnarrenburger Moor – Underfloor irri | 0.301 | test, demonst, reducti, paastot, moor, turve | kyllä |
| K-DE-NI-bd6b MOOSWEIT, Subproject 5 | K-DE-NI-cad6 Succession of the dragonfly fauna of a peat moss c | 0.301 | moss, harvest, peat, turve | kyllä |
| K-DE-NI-3ac3 Rewetting of the hill moor in the forest town of W | K-DE-NI-c57b Rewetting of the hill moor at the forest town of W | 0.292 | hill, moor, town, vettaminen, rewetti, forest | kyllä |
| K-FI-8d28 Restoration of Linttiräme after Peat Production | K-FI-b095 Aarreaitta - Restoring the Kanasuo peat extraction | 0.292 | product, wetland, peat, former, kosteikko, restora | kyllä |
| K-DE-NI-c05c Gnarrenburger Moor – Area concept and water manage | K-DE-NI-f68e Establishment of a “Paludiculture Competence Centr | 0.286 | concept, managem, suunnittelu, climate | kyllä |

## Puuttuva yhteys (15 samankaltaisinta)

_eri maat, ei yhteistyöpolkua._

| A | B | Samankaltaisuus | Yhteiset käsitteet ja sanat | Samaan aikaan |
|---|---|---|---|---|
| K-DE-NI-9d56 Planning for the renaturation of the Steinmoor | K-FI-6c73 Konttisuo restoration plan | 0.271 | plan, norther, suunnittelu, restora, luonto, ennallistaminen | ei |
| LV-03 Ilmastopolitiikkaan sovitetut ratkaisut nostetuill | NI-02 Produktketten aus Niedermoorbiomasse (paludikulttu | 0.246 | paludik, paludikulttuuri, turve | ? |
| NI-01 KliMo – Klimaschutz durch Moorentwicklung (ohjelma | X-IE-NAT Midlands Just Transition -ohjelma (135,8 M€, 47 ha | 0.222 | hankett, ohjelma | ? |
| K-DE-NI-0e2b Rewetting Sauerbach | K-FI-e290 Restoration and water protection project of South- | 0.214 | south, mittaus, measure, former, peat, turve | ei |
| FI-01 TUKKA – Turvemaiden kestävän käytön osaamiskluster | NI-01 KliMo – Klimaschutz durch Moorentwicklung (ohjelma | 0.2 | kayton, kestava, turve | kyllä |

## Peräkkäiset samassa maassa (15 samankaltaisinta)

_sama maa, eri aikaan, ei yhteistä toimijaa eikä polkua (toisto tai jatko ilman yhteyttä)._

| A | B | Samankaltaisuus | Yhteiset käsitteet ja sanat | Samaan aikaan |
|---|---|---|---|---|
| K-DE-NI-04a5 Wiedervernässung des Weißen Moores | K-DE-NI-d8d1 Regeneration of a moorland in the Günnemoor | 0.251 | drainag, high, extract, bog, peat, suo | ei |
| E-DE-NI-b06d Industrial raw material using bog sites – I-ROBI | K-DE-NI-44a1 MOOSWEIT TV3 – GHG balance of cultivation and harv | 0.239 | crop, cultiva, raw, balance, ghg, materia | ei |
| K-DE-NI-1847 Network Moor Care and Moor Management Elbe-Weser ( | K-DE-NI-f3b0 WetWeb Organic Soils – Networked Research for Moor | 0.225 | network, managem, moor, turve | ei |
| K-DE-NI-1746 Care and development concept Meckelmoor Landkreis  | K-DE-NI-bf71 Moor wetting Ahrensfelder Moor | 0.212 | partial, moor, turve | ei |
| K-FI-9cd5 Restoration of peat production areas in North Ostr | K-FI-ceda Tools and methods for combating the effects of pea | 0.2 | suometsa, ostrobo, north, finland, peatlan, peat | ei |

## Teema × maapari

Maaparit, joilla on hankkeita samassa teemassa: **72**, joista ilman yhtään vahvistettua yhteistyöpolkua **42**.

| Teema | Maat | Hankkeita | Yhteys |
|---|---|---|---|
| T1 | DE-NI–FI | 5 + 29 | ei |
| T5 | DE-NI–LV | 31 + 4 | ei |
| T5 | FI–LV | 18 + 4 | ei |
| T3 | DE-NI–IE | 11 + 5 | ei |
| T3 | FI–IE | 8 + 5 | ei |
| T5 | IE–LV | 10 + 4 | ei |
| T1 | DE-NI–LV | 5 + 7 | ei |
| T2 | DE-NI–FI | 8 + 4 | ei |
| T5 | DE-NI–SE | 31 + 1 | ei |
| T1 | EE–FI | 1 + 29 | ei |
| T3 | IE–LV | 5 + 5 | ei |
| T2 | DE-NI–LV | 8 + 3 | ei |
| T8 | DE-NI–FI | 3 + 8 | ei |
| T8 | FI–SE | 8 + 3 | ei |
| T1 | IE–LV | 3 + 7 | ei |
| T2 | IE–LV | 7 + 3 | ei |
| T5 | FI–SE | 18 + 1 | ei |
| T7 | DE-NI–FI | 6 + 3 | ei |
| T7 | DE-NI–IE | 6 + 3 | ei |
| T4 | FI–LV | 8 + 2 | ei |
| T4 | FI–SE | 8 + 2 | ei |
| T1 | DE-NI–IE | 5 + 3 | ei |
| T2 | FI–LV | 4 + 3 | ei |
| T2 | LV–SE | 3 + 4 | ei |
| T7 | DE-NI–LV | 6 + 2 | ei |

## Saarekkeet

| # | Solmuja | Maat | Hankkeet ja keskukset |
|---|---|---|---|
| 1 | 92 | EU FI LV SE | E-LV-6430 E-LV-8eeb E-LV-9406 E-LV-b130 E-LV-c39d E-LV-d12c E-LV-e70c FI-01 FI-06 FI-07 FI-08 FI-09 H-FI H-FI-AKA H-LV J-SE-0e6e K-EU-2e51 K-FI-006d K-FI-0ac6 K-FI-1d92 K-FI-519c K-FI-561d K-FI-6894 K-FI-7c34 K-FI-879d K-FI-9061 K-FI-9511 K-FI-a45d K-FI-e8b3 K-LV-4390 K-LV-74bd LV-01 LV-03 R-FI-70e5 R-FI-b45a T-SE-bda3 X-FI-PEATRESC |
| 2 | 23 | DE-NI IE | E-IE-e6ef H-IE-GAL H-IE-LIFE IE-01 K-DE-NI-d14f K-IE-7fa4 X-IE-GAL X-IE-LIFE X-IE-NAT |
| 3 | 12 | DE-NI | K-DE-NI-36d2 K-DE-NI-9d56 K-DE-NI-a456 K-DE-NI-b8d9 K-DE-NI-e715 K-DE-NI-f68e NI-01 NI-02 NI-03 |
| 4 | 7 | DE-NI | K-DE-NI-1c15 K-DE-NI-209b K-DE-NI-9595 K-DE-NI-af02 K-DE-NI-cf1c K-DE-NI-f620 |
| 5 | 5 | FI | FI-02 K-FI-56cf K-FI-e290 |
| 6 | 5 | IE | IE-02 |
| 7 | 5 | DE-NI | E-DE-NI-3e4b |
| 8 | 4 | DE-NI | E-DE-NI-b06d |
| 9 | 4 | DE-NI | K-DE-NI-0e2b K-DE-NI-61e6 K-DE-NI-c1d3 |
| 10 | 4 | FI | K-FI-06b9 K-FI-b095 |
| 11 | 3 | LV | LV-02 |
| 12 | 3 | DE-NI | K-DE-NI-1746 K-DE-NI-dab1 |
| 13 | 3 | DE-NI | K-DE-NI-a450 K-DE-NI-accd |
| 14 | 3 | DE DE-NI | K-DE-NI-0499 K-DE-NI-77b2 |
| 15 | 3 | DE-NI | K-DE-NI-1847 K-DE-NI-34e3 |
| 16 | 3 | DE-NI | K-DE-NI-3eb1 K-DE-NI-ee94 |
| 17 | 3 | DE-NI | K-DE-NI-bf71 K-DE-NI-d8d1 |
| 18 | 3 | DE-NI | K-DE-NI-03c5 K-DE-NI-6c80 |
| 19 | 3 | EU | T-EU-73cb T-EU-88fc |
| 20 | 3 | FI | K-FI-050e K-FI-b38f |
| 21 | 3 | FI | K-FI-665a K-FI-9cd5 |
| 22 | 3 | FI | K-FI-6f20 |
| 23 | 3 | SE | K-SE-8b1e K-SE-be89 |
| 24 | 2 | FI | FI-03 |
| 25 | 2 | EE | EE-02 |
| 26 | 2 | DE-NI | K-DE-NI-e147 |
| 27 | 2 | DE DE-NI | K-DE-NI-44a1 |
| 28 | 2 | DE-NI | K-DE-NI-bd6b |
| 29 | 2 | DE-NI | K-DE-NI-410f |
| 30 | 2 | DE-NI | K-DE-NI-9163 |
| 31 | 2 | DE-NI | K-DE-NI-ca87 |
| 32 | 2 | DE-NI | K-DE-NI-d3d6 |
| 33 | 2 | DE-NI | K-DE-NI-8755 |
| 34 | 2 | DE-NI | K-DE-NI-04a5 |
| 35 | 2 | DE-NI | K-DE-NI-c57b |
| 36 | 2 | DE-NI | K-DE-NI-3ac3 |
| 37 | 2 | DE-NI | K-DE-NI-6f11 |
| 38 | 2 | DE-NI | K-DE-NI-cad6 |
| 39 | 2 | DE-NI | K-DE-NI-f3b0 |
| 40 | 2 | EU | K-EU-5a7e |
| 41 | 2 | EU | K-EU-0882 |
| 42 | 2 | EU | K-EU-48f5 |
| 43 | 2 | EU | K-EU-f426 |
| 44 | 2 | FI | R-FI-d4ba |
| 45 | 2 | FI | K-FI-1fcb |
| 46 | 2 | FI | K-FI-2fcc |
| 47 | 2 | FI | K-FI-6c73 |
| 48 | 2 | FI | K-FI-6978 |
| 49 | 2 | FI | K-FI-8d28 |
| 50 | 2 | FI | K-FI-cb20 |
| 51 | 2 | FI | K-FI-16d2 |
| 52 | 2 | FI | K-FI-3bb2 |
| 53 | 2 | FI | K-FI-c4ea |
| 54 | 2 | FI | K-FI-ceda |
| 55 | 2 | IE | K-IE-06fb |
| 56 | 2 | IE | K-IE-0b63 |
| 57 | 2 | IE | K-IE-cee8 |
| 58 | 2 | IE | K-IE-0814 |
| 59 | 2 | IE | K-IE-d7ff |
| 60 | 2 | IE | K-IE-8525 |
| 61 | 2 | LV | K-LV-2fac |
| 62 | 2 | LV | K-LV-37ba |
| 63 | 2 | LV | K-LV-cbb2 |
| 64 | 2 | SE | K-SE-dbb8 |
| 65 | 2 | SE | J-SE-5a7e |
| 66 | 2 | SE | J-SE-b073 |
| 67 | 2 | SE | T-SE-5e29 |
| 68 | 2 | SE | J-SE-2f3b |
| 69 | 2 | SE | J-SE-50cf |
| 70 | 2 | SE | J-SE-a3d4 |
| 71 | 2 | IE | H-IE-JTF |
| 72 | 1 | FI | FI-10 |
| 73 | 1 | DE-NI | K-DE-NI-7a94 |
| 74 | 1 | DE-NI | K-DE-NI-c05c |
| 75 | 1 | DE-NI | K-DE-NI-d90f |
| 76 | 1 | DE-NI | K-DE-NI-cc25 |
| 77 | 1 | DE-NI | K-DE-NI-e128 |
| 78 | 1 | IE | E-IE-9275 |
| 79 | 1 | IE | E-IE-2cb2 |
| 80 | 1 | IE | E-IE-9676 |
| 81 | 1 | DE-SH | X-DE-SH |
