# Yhteysanalyysi

_Generoitu skriptillä `scripts/analyze.py`. Älä muokkaa käsin._

## Yhteenveto

- Toimijoita yhteistyöverkossa: **628**, vahvistettuja yhteistyösärmiä **587** (lisäksi 3 vahvistamatonta, jotka eivät ole mukana saarekkeissa eikä keskeisyydessä).
- Erillisiä yhteistyösaarekkeita: **115**, joista **19** sisältää vähintään kaksi hanketta tai keskusta (loput ovat yksittäisiä hankkeita toteuttajineen). Suurin kattaa 295 toimijaa.
- Usean maan saarekkeita: **6**. Maiden välisiä vahvistettuja yhteistyösärmiä: **44**.
- Yhteisjulkaisut mukaan lukien (organisaatioiden yhteiset turvemaa- ja maaperäjulkaisut, OpenAIRE): yhteisjulkaisusärmiä **97**, joista maiden välisiä **54**; saarekkeita **108**, joista usean maan **3**. Päällekkäisyysparien yhteys lasketaan tässä verkossa.
- Sisällöltään samankaltaisia hankepareja (tekstin samankaltaisuus ≥ 0.2, 284 vertailtavaa hanketta): **834**. Niistä
  - rinnakkaisia ilman yhteyttä (sama maa, samaan aikaan, ei yhteistä toimijaa eikä polkua ≤ 3); kohdekohtaisissa toteutushankkeissa tämä on usein tarkoituksellista, menetelmä- ja suunnitteluhankkeissa se viittaa päällekkäiseen työhön: **138**
  - peräkkäisiä samassa maassa ilman yhteyttä: **20**
  - puuttuvia maiden välisiä yhteyksiä: **20**
  - yhteydessä olevia (yhteinen toimija tai lyhyt polku): **440**
  - saman hankekokonaisuuden osia: **3**
  - pareja, joissa toisen hankkeen toimija ei ole tiedossa (esim. henkilökohtainen apuraha), joten yhteyttä ei voi arvioida: **213**
- Todennäköisiä kaksoiskappaleita eri lähteistä (sama maa ja vuodet, yhteinen toimija tai samankaltainen teksti): **0**. Ne tarkistetaan: todelliset kaksoiskappaleet yhdistetään `src/tuonti.py`:n `MATCH_EXISTING`-listalla, ja erillisiksi todetut parit kirjataan perusteluineen `scripts/analyze.py`:n `NOT_DUPLICATE`-listaan (`analysis/kaksoisehdokkaat.csv`).

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

- DE-NI–EU: 4 (lähteellä vahvistettu)
- DE-NI–IE: 2 (lähteellä vahvistettu)
- DE-NI–SE: 2 (lähteellä vahvistettu)
- DE–DE-NI: 3 (lähteellä vahvistettu)
- EE–EU: 1 (lähteellä vahvistettu)
- EE–LV: 2 (lähteellä vahvistettu)
- EU–FI: 17 (lähteellä vahvistettu)
- EU–IE: 2 (lähteellä vahvistettu)
- EU–LV: 5 (lähteellä vahvistettu)
- EU–SE: 1 (lähteellä vahvistettu)
- FI–LV: 2 (lähteellä vahvistettu)
- FI–SE: 3 (lähteellä vahvistettu)
- FI–IE: 3 (kumppani vahvistamatta)

## Välittäjäorganisaatiot (välityskeskeisyys)

| Organisaatio | Maa | Hankkeita | Keskuksia | Välityskeskeisyys |
|---|---|---|---|---|
| Luonnonvarakeskus (Luke) | FI | 38 | 2 | 0.1419 |
| LSFRI Silava | LV | 12 | 1 | 0.059 |
| Latvian yliopisto | LV | 10 | 1 | 0.0399 |
| Latvia University of Life Sciences and Technologies | LV | 4 | 1 | 0.0367 |
| Helsingin yliopisto | FI | 24 | 2 | 0.0242 |
| Itä-Suomen yliopisto | FI | 20 | 1 | 0.0227 |
| Suomen metsäkeskus | FI | 16 | 1 | 0.0209 |
| Suomen ympäristökeskus (Syke) | FI | 10 | 0 | 0.0146 |
| Oulun yliopisto | FI | 12 | 1 | 0.0135 |
| Latvian Fund for Nature | LV | 4 | 0 | 0.0128 |

## Osaamiskeskusten yhteiset organisaatiot

- H-FI ↔ H-FI-AKA: hy, il
- H-IE-GAL ↔ H-IE-LIFE: galway

## Päällekkäisyyden menetelmä

Hankkeiden nimi, kuvaus ja tuotokset verrataan TF-IDF-painotettuina. Monikielinen käsitesanasto yhdistää saman asian eri kielillä (esim. turve, peat, torv, kūdra, Torf). Samankaltaisuus on kosini väliltä 0–1. Kynnys on valittu tarkastelemalla pareja käsin, joten alla on tulokset usealla kynnyksellä. Eri kielillä kuvatut ja eri maiden hankkeet saavat järjestelmällisesti matalampia arvoja, koska paikannimet ja kielikohtaiset sanat eivät osu yhteen.

Lähdeaineiston kuvaukset ovat lyhyitä (keskimäärin noin 200 merkkiä), mikä heikentää erottelukykyä. Tulokset ovat ehdokkaita tarkistettavaksi, eivät todettuja päällekkäisyyksiä.

| Kynnys | Pareja | saman kokonaisuuden osat | rinnakkainen ilman yhteyttä | peräkkäiset samassa maassa | puuttuva yhteys | yhteydessä | toimija ei tiedossa |
|---|---|---|---|---|---|---|---|
| 0.15 | 1299 | 3 | 248 | 52 | 92 | 576 | 328 |
| 0.2 | 834 | 3 | 138 | 20 | 20 | 440 | 213 |
| 0.25 | 565 | 3 | 76 | 11 | 3 | 305 | 167 |
| 0.3 | 417 | 3 | 52 | 9 | 1 | 201 | 151 |
| 0.35 | 325 | 3 | 29 | 8 | 0 | 138 | 147 |
| 0.4 | 274 | 2 | 18 | 7 | 0 | 101 | 146 |

## Rinnakkainen ilman yhteyttä (15 samankaltaisinta)

_sama maa, samaan aikaan, ei yhteistä toimijaa eikä yhteistyöpolkua. Voi olla tarkoituksellista (eri kohteet) tai päällekkäistä työtä (sama menetelmä tai suunnittelu kahteen kertaan)._

| A | B | Samankaltaisuus | Yhteiset käsitteet ja sanat | Samaan aikaan |
|---|---|---|---|---|
| A-FI-1fc3 ECO-WADE - carbon and groundwater dynamics in Euro | A-FI-2fd2 MiDiPeat - peat microbial diversity and carbon dyn | 0.82 | yhteish, euroopp, akatemi, suomen, dynamic, hiili | kyllä |
| M-FI-361d Ilmastokestävää metsänhoitoa Kainuuseen | M-FI-82f3 Kaliumilla turvemaat tuottamaan (KaTu) | 0.657 | pohjois, msr, rahasto, elinvoi, suomen, suo | ? |
| M-FI-9d56 Turvemaiden Ilmastoviisas Käyttö | M-FI-f232 Suunnitteluhanke TURPO – turvekasvualustojen hiile | 0.616 | kaakkoi, msr, rahasto, elinvoi, suomen, suo | kyllä |
| M-FI-361d Ilmastokestävää metsänhoitoa Kainuuseen | M-FI-ebaa Turvemaiden viljanviljelyssä syntyvä ilmasto- ja v | 0.603 | pohjois, msr, rahasto, elinvoi, suomen, ilmasto | kyllä |
| M-FI-0c06 Suometsien puunkorjuun uudet tuulet | M-FI-82f3 Kaliumilla turvemaat tuottamaan (KaTu) | 0.581 | pohjois, msr, rahasto, elinvoi, suomen, suo | ? |
| M-FI-361d Ilmastokestävää metsänhoitoa Kainuuseen | M-FI-9d56 Turvemaiden Ilmastoviisas Käyttö | 0.581 | msr, rahasto, elinvoi, suomen, ilmasto, suo | kyllä |
| M-FI-82f3 Kaliumilla turvemaat tuottamaan (KaTu) | M-FI-ebaa Turvemaiden viljanviljelyssä syntyvä ilmasto- ja v | 0.551 | pohjois, msr, rahasto, elinvoi, suomen, suo | ? |
| M-FI-82f3 Kaliumilla turvemaat tuottamaan (KaTu) | M-FI-9d56 Turvemaiden Ilmastoviisas Käyttö | 0.529 | msr, rahasto, elinvoi, suomen, suo, turvema | ? |
| A-FI-c64f Sphagnum mosses as ecosystem engineers in transiti | A-FI-d1fe Suomen soiden karhukaiset bioindikaattorina soiden | 0.503 | koneen, saatio, vaitost, rahoitt, suo | kyllä |
| M-FI-0c06 Suometsien puunkorjuun uudet tuulet | M-FI-ebaa Turvemaiden viljanviljelyssä syntyvä ilmasto- ja v | 0.493 | pohjois, msr, rahasto, elinvoi, suomen, suo | kyllä |
| M-FI-0c06 Suometsien puunkorjuun uudet tuulet | M-FI-9d56 Turvemaiden Ilmastoviisas Käyttö | 0.465 | msr, rahasto, elinvoi, suomen, suo | kyllä |
| K-DE-NI-6f11 Rewetting of the slope moor Friedrichshäuser Bruch | K-DE-NI-c57b Rewetting of the hill moor at the forest town of W | 0.442 | hill, trenche, removin, drainag, moor, vettaminen | kyllä |
| M-FI-5dac Suometsiin liittyvän tiedon lisääminen ja osaamise | M-FI-9d56 Turvemaiden Ilmastoviisas Käyttö | 0.435 | msr, rahasto, elinvoi, suomen, suo | ? |
| M-FI-9d56 Turvemaiden Ilmastoviisas Käyttö | M-FI-f3b2 Metsien vedet | 0.416 | msr, rahasto, elinvoi | kyllä |
| M-FI-5dac Suometsiin liittyvän tiedon lisääminen ja osaamise | M-FI-82f3 Kaliumilla turvemaat tuottamaan (KaTu) | 0.414 | msr, rahasto, elinvoi, suomen, suo | ? |

## Puuttuva yhteys (15 samankaltaisinta)

_eri maat, ei yhteistyöpolkua._

| A | B | Samankaltaisuus | Yhteiset käsitteet ja sanat | Samaan aikaan |
|---|---|---|---|---|
| L-EU-9184 Multi-stakeholder Landscape and Technical Innovati | L-EU-9ecc Scaling Up PEatland Restoration in EUrope | 0.311 | eurosit, ghg, emissio, verenig, ochrony, beheer | kyllä |
| I-DE-NI-1d0c Blue Transition – How to make my region climate re | I-EU-598e Care-Peat – Carbon loss reduction from peatlands:  | 0.284 | france, univers, netherl, recherc, rennes, nationa | ? |
| L-EE-89f5 Conservation and restoration of Mire Habitats | L-IE-f155 Restoring Active Raised Bog in Ireland's SAC Netwo | 0.263 | raised, active, bogs, life14, status, due | kyllä |
| L-LV-6382 Restoring EU priority grasslands and promoting the | L-SE-0893 Restoration of habitats rich in trees and shrubs | 0.245 | grassla, urgent, rich, habitat, fragmen, require | kyllä |
| K-EU-0882 BUFFER carbon + water in peatlands: landscape-base | K-EU-48f5 Carbon Connects | 0.241 | netherl, belgium, chambre, agricul, france, univers | kyllä |
| K-DE-NI-9d56 Planning for the renaturation of the Steinmoor | K-FI-6c73 Konttisuo restoration plan | 0.239 | plan, norther, suunnittelu, restora, luonto, ennallistaminen | ei |
| L-FI-ea10 Restoring the hydrological integrity of wetland ha | L-SE-350f Restoration of EU Redlisted Annex I habitats, depe | 0.236 | most, origina, remains, last, habitat, serious | kyllä |
| I-EU-598e Care-Peat – Carbon loss reduction from peatlands:  | K-EU-48f5 Carbon Connects | 0.233 | united, kingdom, netherl, trust, univers, france | ? |
| LV-03 Ilmastopolitiikkaan sovitetut ratkaisut nostetuill | NI-02 Produktketten aus Niedermoorbiomasse (paludikulttu | 0.233 | paludik, paludikulttuuri, turve | kyllä |
| L-EU-d0c3 Reduction of CO2 emissions by restoring degraded p | L-LV-8d1e Sustainable and responsible management and re-use  | 0.227 | stored, accordi, carbon, least, degrada, ccm | kyllä |
| L-EU-9ecc Scaling Up PEatland Restoration in EUrope | L-EU-d0c3 Reduction of CO2 emissions by restoring degraded p | 0.224 | degrade, co2, estimat, saksan, nabu, koordin | ei |
| L-IE-f155 Restoring Active Raised Bog in Ireland's SAC Netwo | L-LV-2005 Conservation and Management of Priority Wetland Ha | 0.224 | raised, bogs, active, now, these, nat | kyllä |
| K-DE-NI-0e2b Rewetting Sauerbach | K-FI-e290 Restoration and water protection project of South- | 0.217 | south, mittaus, former, measure, peat, turve | ei |
| L-LV-2005 Conservation and Management of Priority Wetland Ha | L-SE-0893 Restoration of habitats rich in trees and shrubs | 0.214 | now, life13, negativ, particu, highly, biodive | kyllä |
| L-EE-89f5 Conservation and restoration of Mire Habitats | L-LV-6382 Restoring EU priority grasslands and promoting the | 0.211 | fennosc, habitat, rich, types, priorit, followi | kyllä |

## Peräkkäiset samassa maassa (15 samankaltaisinta)

_sama maa, eri aikaan, ei yhteistä toimijaa eikä polkua (toisto tai jatko ilman yhteyttä)._

| A | B | Samankaltaisuus | Yhteiset käsitteet ja sanat | Samaan aikaan |
|---|---|---|---|---|
| A-FI-1fc3 ECO-WADE - carbon and groundwater dynamics in Euro | A-FI-5ced PRENIC - peatland rewetting in nitrogen-contaminat | 0.728 | yhteish, euroopp, akatemi, suomen, rahoitt, suo | ei |
| A-FI-6568 Liukoisen orgaanisen aineksen ominaisuudet luonnon | A-FI-d1fe Suomen soiden karhukaiset bioindikaattorina soiden | 0.572 | koneen, saatio, vaitost, ennallistaminen, rahoitt, ennalli | ei |
| A-FI-1243 Restoring Peatlands: predicting biodiversity, GHG  | A-FI-d1fe Suomen soiden karhukaiset bioindikaattorina soiden | 0.566 | koneen, saatio, vaitost, ennallistaminen, rahoitt | ei |
| A-FI-3a41 Peittynyt perintö - arkeologinen näkökulma turvema | A-FI-d1fe Suomen soiden karhukaiset bioindikaattorina soiden | 0.538 | koneen, saatio, ennallistaminen, rahoitt, ennalli | ei |
| A-FI-6420 Alastomuutta, allikoita ja kannanottoa: suotrendi  | A-FI-d1fe Suomen soiden karhukaiset bioindikaattorina soiden | 0.507 | koneen, saatio, rahoitt, suo | ei |
| M-FI-9d56 Turvemaiden Ilmastoviisas Käyttö | M-FI-ebaa Turvemaiden viljanviljelyssä syntyvä ilmasto- ja v | 0.493 | msr, rahasto, elinvoi, suomen, ilmasto, suo | ei |
| A-FI-50e3 Lettojen ennallistaminen - aktiiviset ennallistami | A-FI-d1fe Suomen soiden karhukaiset bioindikaattorina soiden | 0.431 | koneen, saatio, ennalli, ennallistaminen, rahoitt | ei |
| M-FI-ebaa Turvemaiden viljanviljelyssä syntyvä ilmasto- ja v | M-FI-f0a8 Salmiojan–Jokilammen valuma-alueen soiden osittain | 0.359 | msr, rahasto, elinvoi, vesistot, suo | ei |
| M-FI-ebaa Turvemaiden viljanviljelyssä syntyvä ilmasto- ja v | M-FI-f232 Suunnitteluhanke TURPO – turvekasvualustojen hiile | 0.322 | msr, rahasto, elinvoi, suomen, suo, turve | ei |
| M-FI-1bc7 Luonnonhoidon laatuharppaus ja ennallistamisen enn | M-FI-ebaa Turvemaiden viljanviljelyssä syntyvä ilmasto- ja v | 0.268 | msr, rahasto, elinvoi, pohjois, suomen, suo | ei |
| A-FI-1fc3 ECO-WADE - carbon and groundwater dynamics in Euro | A-FI-8afc ReindeerPaths - reindeer impacts on wetland carbon | 0.252 | akatemi, suomen, hiili, rahoitt, suo, carbon | ei |
| L-LV-2b35 Peatland restoration for greenhouse gas emission r | L-LV-8d1e Sustainable and responsible management and re-use  | 0.247 | sinks, exploit, mitigat, extract, change, carbon | ei |
| K-DE-NI-04a5 Wiedervernässung des Weißen Moores | K-DE-NI-d8d1 Regeneration of a moorland in the Günnemoor | 0.242 | extract, drainag, high, bog, peat, suo | ei |
| E-DE-NI-b06d Industrial raw material using bog sites – I-ROBI | K-DE-NI-44a1 MOOSWEIT TV3 – GHG balance of cultivation and harv | 0.239 | crop, cultiva, raw, balance, materia, ghg | ei |
| A-FI-1fc3 ECO-WADE - carbon and groundwater dynamics in Euro | A-FI-ed8e MIso - belowground methane turnover at a boreal pe | 0.234 | akatemi, suomen, rahoitt, suo, peatlan, turve | ei |

## Teema × maapari

Maaparit, joilla on hankkeita samassa teemassa: **77**, joista ilman yhtään vahvistettua yhteistyöpolkua **33**.

| Teema | Maat | Hankkeita | Yhteys |
|---|---|---|---|
| T1 | DE-NI–FI | 5 + 33 | ei |
| T4 | FI–SE | 34 + 3 | ei |
| T5 | IE–SE | 15 + 6 | ei |
| T5 | EE–FI | 1 + 75 | ei |
| T3 | DE-NI–IE | 12 + 6 | ei |
| T5 | LV–SE | 11 + 6 | ei |
| T1 | DE-NI–LV | 5 + 10 | ei |
| T7 | DE-NI–FI | 7 + 6 | ei |
| T8 | DE-NI–FI | 3 + 13 | ei |
| T8 | FI–SE | 13 + 3 | ei |
| T5 | DE-NI–EE | 35 + 1 | ei |
| T7 | DE-NI–IE | 7 + 5 | ei |
| T4 | DE-NI–FI | 1 + 34 | ei |
| T1 | EE–FI | 1 + 33 | ei |
| T1 | IE–LV | 3 + 10 | ei |
| T7 | DE-NI–LV | 7 + 4 | ei |
| T8 | DE-NI–LV | 3 + 6 | ei |
| T8 | LV–SE | 6 + 3 | ei |
| T1 | DE-NI–IE | 5 + 3 | ei |
| T4 | LV–SE | 5 + 3 | ei |
| T5 | EE–IE | 1 + 15 | ei |
| T8 | FI–IE | 13 + 1 | ei |
| T5 | EE–LV | 1 + 11 | ei |
| T1 | EE–LV | 1 + 10 | ei |
| T8 | DE-NI–SE | 3 + 3 | ei |

## Saarekkeet

| # | Solmuja | Maat | Hankkeet ja keskukset |
|---|---|---|---|
| 1 | 295 | EE EU FI IE LV SE | A-EU-10ff A-EU-1892 A-EU-18f8 A-EU-1958 A-EU-88ad A-EU-e163 A-EU-fcae A-FI-0222 A-FI-0ebc A-FI-0f15 A-FI-1123 A-FI-1243 A-FI-1da3 A-FI-1f5c A-FI-1fc3 A-FI-2ee2 A-FI-2f32 A-FI-2fd2 A-FI-3a41 A-FI-50e3 A-FI-5129 A-FI-5277 A-FI-5770 A-FI-57a1 A-FI-593f A-FI-5bc3 A-FI-5cd8 A-FI-5ced A-FI-6420 A-FI-64c3 A-FI-6568 A-FI-663f A-FI-66ca A-FI-68d7 A-FI-71e2 A-FI-72e3 A-FI-8120 A-FI-8915 A-FI-8afc A-FI-99f9 A-FI-9d06 A-FI-b9fb A-FI-c3c5 A-FI-c61b A-FI-c64f A-FI-cc7b A-FI-d1fe A-FI-d390 A-FI-d4c5 A-FI-e29b A-FI-ed8e A-FI-f0c7 A-FI-f1c6 E-LV-6430 E-LV-8eeb E-LV-9406 E-LV-b130 E-LV-c39d E-LV-d12c E-LV-e70c FI-01 FI-06 FI-07 FI-08 FI-09 H-FI H-FI-AKA H-LV I-EU-414b I-FI-b431 J-SE-0e6e K-EU-2e51 K-FI-006d K-FI-0ac6 K-FI-1d92 K-FI-519c K-FI-561d K-FI-6894 K-FI-6978 K-FI-6c73 K-FI-6f20 K-FI-7c34 K-FI-879d K-FI-9061 K-FI-9511 K-FI-a45d K-FI-ceda K-FI-e8b3 K-LV-4390 K-LV-74bd K-SE-dbb8 L-EE-89f5 L-EU-9184 L-EU-d0c3 L-FI-a176 L-FI-ba2f L-FI-dfbb L-FI-e958 L-FI-ea10 L-LV-05ed L-LV-1f9f L-LV-2005 L-LV-2b35 L-LV-42ff L-LV-50b4 L-LV-5d8c L-LV-6382 L-LV-8d1e L-LV-ec74 L-SE-5a2c LV-01 LV-03 M-FI-0c06 M-FI-17f1 M-FI-1bc7 M-FI-361d M-FI-5dac M-FI-658f M-FI-8c1d M-FI-9b2e M-FI-afed M-FI-b2cb M-FI-cc8a M-FI-ebaa M-FI-f232 M-FI-f3b2 R-FI-5c35 R-FI-70e5 T-SE-bda3 X-FI-PEATRESC |
| 2 | 55 | DE-NI EU IE | E-IE-e6ef H-IE-GAL H-IE-LIFE I-DE-NI-c078 I-EU-598e I-EU-f185 I-EU-f393 IE-01 K-DE-NI-d14f K-IE-7fa4 L-IE-4ec5 L-IE-b2a4 L-IE-d4a5 L-IE-ed33 X-IE-GAL X-IE-LIFE X-IE-NAT |
| 3 | 21 | DE-NI SE | I-DE-NI-1d0c L-SE-1410 |
| 4 | 12 | DE-NI | K-DE-NI-36d2 K-DE-NI-9d56 K-DE-NI-a456 K-DE-NI-b8d9 K-DE-NI-e715 K-DE-NI-f68e NI-01 NI-02 NI-03 |
| 5 | 11 | SE | L-SE-350f |
| 6 | 7 | DE-NI | K-DE-NI-1c15 K-DE-NI-209b K-DE-NI-9595 K-DE-NI-af02 K-DE-NI-cf1c K-DE-NI-f620 |
| 7 | 5 | FI | FI-02 K-FI-56cf K-FI-e290 |
| 8 | 5 | IE | IE-02 |
| 9 | 5 | DE-NI | E-DE-NI-3e4b |
| 10 | 5 | EU | K-EU-0882 |
| 11 | 5 | SE | L-SE-53b2 |
| 12 | 4 | DE-NI | E-DE-NI-b06d |
| 13 | 4 | DE-NI | K-DE-NI-0e2b K-DE-NI-61e6 K-DE-NI-c1d3 |
| 14 | 4 | EU | K-EU-48f5 |
| 15 | 4 | FI | K-FI-06b9 K-FI-b095 |
| 16 | 4 | IE | K-IE-0b63 |
| 17 | 3 | LV | LV-02 |
| 18 | 3 | DE-NI | K-DE-NI-1746 K-DE-NI-dab1 |
| 19 | 3 | DE-NI | K-DE-NI-a450 K-DE-NI-accd |
| 20 | 3 | DE DE-NI | K-DE-NI-0499 K-DE-NI-77b2 |
| 21 | 3 | DE-NI | K-DE-NI-1847 K-DE-NI-34e3 |
| 22 | 3 | DE-NI | K-DE-NI-3eb1 K-DE-NI-ee94 |
| 23 | 3 | DE-NI | K-DE-NI-bf71 K-DE-NI-d8d1 |
| 24 | 3 | DE-NI | K-DE-NI-03c5 K-DE-NI-6c80 |
| 25 | 3 | DE-NI | L-DE-NI-aaba |
| 26 | 3 | EU | K-EU-5a7e |
| 27 | 3 | EU | K-EU-f426 |
| 28 | 3 | EU | T-EU-73cb T-EU-88fc |
| 29 | 3 | EU FI | A-EU-e4f8 |
| 30 | 3 | FI | K-FI-050e K-FI-b38f |
| 31 | 3 | FI | K-FI-665a K-FI-9cd5 |
| 32 | 3 | FI | I-FI-a184 |
| 33 | 3 | SE | K-SE-8b1e K-SE-be89 |
| 34 | 2 | FI | FI-03 |
| 35 | 2 | EE | EE-02 |
| 36 | 2 | DE-NI | K-DE-NI-e147 |
| 37 | 2 | DE DE-NI | K-DE-NI-44a1 |
| 38 | 2 | DE-NI | K-DE-NI-bd6b |
| 39 | 2 | DE-NI | K-DE-NI-410f |
| 40 | 2 | DE-NI | K-DE-NI-9163 |
| 41 | 2 | DE-NI | K-DE-NI-ca87 |
| 42 | 2 | DE-NI | K-DE-NI-d3d6 |
| 43 | 2 | DE-NI | K-DE-NI-8755 |
| 44 | 2 | DE-NI | K-DE-NI-04a5 |
| 45 | 2 | DE-NI | K-DE-NI-c57b |
| 46 | 2 | DE-NI | K-DE-NI-3ac3 |
| 47 | 2 | DE-NI | K-DE-NI-6f11 |
| 48 | 2 | DE-NI | K-DE-NI-cad6 |
| 49 | 2 | DE-NI | L-DE-NI-83ea |
| 50 | 2 | DE-NI | K-DE-NI-f3b0 |
| 51 | 2 | EU | L-EU-9ecc |
| 52 | 2 | FI | R-FI-d4ba |
| 53 | 2 | FI | K-FI-1fcb |
| 54 | 2 | FI | K-FI-2fcc |
| 55 | 2 | FI | M-FI-4fba |
| 56 | 2 | FI | M-FI-82f3 |
| 57 | 2 | FI | K-FI-8d28 |
| 58 | 2 | FI | K-FI-cb20 |
| 59 | 2 | FI | K-FI-16d2 |
| 60 | 2 | FI | M-FI-f0a8 |
| 61 | 2 | FI | M-FI-d8c9 |
| 62 | 2 | FI | K-FI-3bb2 |
| 63 | 2 | FI | K-FI-c4ea |
| 64 | 2 | FI | R-FI-b914 |
| 65 | 2 | FI | M-FI-9d56 |
| 66 | 2 | IE | K-IE-06fb |
| 67 | 2 | IE | K-IE-cee8 |
| 68 | 2 | IE | K-IE-0814 |
| 69 | 2 | IE | L-IE-f155 |
| 70 | 2 | IE | K-IE-d7ff |
| 71 | 2 | IE | K-IE-8525 |
| 72 | 2 | LV | K-LV-2fac |
| 73 | 2 | LV | K-LV-37ba |
| 74 | 2 | LV | K-LV-cbb2 |
| 75 | 2 | SE | J-SE-5a7e |
| 76 | 2 | SE | J-SE-b073 |
| 77 | 2 | SE | T-SE-5e29 |
| 78 | 2 | SE | J-SE-2f3b |
| 79 | 2 | SE | L-SE-0893 |
| 80 | 2 | SE | J-SE-50cf |
| 81 | 2 | SE | J-SE-a3d4 |
| 82 | 2 | IE | H-IE-JTF |
| 83 | 1 | FI | FI-10 |
| 84 | 1 | DE-NI | K-DE-NI-7a94 |
| 85 | 1 | DE-NI | K-DE-NI-c05c |
| 86 | 1 | DE-NI | K-DE-NI-d90f |
| 87 | 1 | DE-NI | K-DE-NI-cc25 |
| 88 | 1 | DE-NI | K-DE-NI-e128 |
| 89 | 1 | EU | A-EU-b538 |
| 90 | 1 | FI | A-FI-4a0c |
| 91 | 1 | FI | A-FI-db3f |
| 92 | 1 | FI | A-FI-9293 |
| 93 | 1 | FI | A-FI-9f42 |
| 94 | 1 | FI | A-FI-4676 |
| 95 | 1 | FI | A-FI-7c97 |
| 96 | 1 | FI | A-FI-4690 |
| 97 | 1 | FI | A-FI-3609 |
| 98 | 1 | FI | A-FI-5eb8 |
| 99 | 1 | FI | A-FI-822d |
| 100 | 1 | FI | A-FI-7b9e |
| 101 | 1 | FI | A-FI-ace0 |
| 102 | 1 | FI | A-FI-4167 |
| 103 | 1 | FI | A-FI-9ed2 |
| 104 | 1 | FI | A-FI-e8bb |
| 105 | 1 | FI | A-FI-5a0a |
| 106 | 1 | FI | A-FI-5a0a5772 |
| 107 | 1 | FI | A-FI-d1f1 |
| 108 | 1 | FI | A-FI-cf8d |
| 109 | 1 | FI | A-FI-6f78 |
| 110 | 1 | FI | A-FI-fce4 |
| 111 | 1 | FI | A-FI-a2a9 |
| 112 | 1 | IE | E-IE-9275 |
| 113 | 1 | IE | E-IE-2cb2 |
| 114 | 1 | IE | E-IE-9676 |
| 115 | 1 | DE-SH | X-DE-SH |
