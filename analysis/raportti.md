# Yhteysanalyysi

_Generoitu skriptillä `scripts/analyze.py`. Älä muokkaa käsin._

## Yhteenveto

- Toimijoita yhteistyöverkossa: **750**, vahvistettuja yhteistyösärmiä **686** (lisäksi 3 vahvistamatonta, jotka eivät ole mukana saarekkeissa eikä keskeisyydessä).
- Erillisiä yhteistyösaarekkeita: **144**, joista **30** sisältää vähintään kaksi hanketta tai keskusta (loput ovat yksittäisiä hankkeita toteuttajineen). Suurin kattaa 327 toimijaa.
- Usean maan saarekkeita: **6**. Maiden välisiä vahvistettuja yhteistyösärmiä: **44**.
- Yhteisjulkaisut mukaan lukien (organisaatioiden yhteiset turvemaa- ja maaperäjulkaisut, OpenAIRE): yhteisjulkaisusärmiä **97**, joista maiden välisiä **54**; saarekkeita **137**, joista usean maan **3**. Päällekkäisyysparien yhteys lasketaan tässä verkossa.
- Sisällöltään samankaltaisia hankepareja (tekstin samankaltaisuus ≥ 0.2, 375 vertailtavaa hanketta): **1474**. Niistä
  - rinnakkaisia ilman yhteyttä (sama maa, samaan aikaan, ei yhteistä toimijaa eikä polkua ≤ 3); kohdekohtaisissa toteutushankkeissa tämä on usein tarkoituksellista, menetelmä- ja suunnitteluhankkeissa se viittaa päällekkäiseen työhön: **233**
  - peräkkäisiä samassa maassa ilman yhteyttä: **379**
  - puuttuvia maiden välisiä yhteyksiä: **18**
  - yhteydessä olevia (yhteinen toimija tai lyhyt polku): **568**
  - saman hankekokonaisuuden osia: **3**
  - pareja, joissa toisen hankkeen toimija ei ole tiedossa (esim. henkilökohtainen apuraha), joten yhteyttä ei voi arvioida: **273**
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
| Luonnonvarakeskus (Luke) | FI | 41 | 2 | 0.1224 |
| LSFRI Silava | LV | 14 | 1 | 0.0477 |
| Latvia University of Life Sciences and Technologies | LV | 4 | 1 | 0.0323 |
| Latvian yliopisto | LV | 10 | 1 | 0.0322 |
| Helsingin yliopisto | FI | 24 | 2 | 0.0184 |
| Itä-Suomen yliopisto | FI | 21 | 1 | 0.0181 |
| University of Tartu | EE | 10 | 0 | 0.0165 |
| Suomen metsäkeskus | FI | 16 | 1 | 0.0164 |
| Suomen ympäristökeskus (Syke) | FI | 12 | 0 | 0.0128 |
| Oulun yliopisto | FI | 13 | 1 | 0.0108 |

## Osaamiskeskusten yhteiset organisaatiot

- H-FI ↔ H-FI-AKA: hy, il
- H-IE-GAL ↔ H-IE-LIFE: galway

## Päällekkäisyyden menetelmä

Hankkeiden nimi, kuvaus ja tuotokset verrataan TF-IDF-painotettuina. Monikielinen käsitesanasto yhdistää saman asian eri kielillä (esim. turve, peat, torv, kūdra, Torf). Samankaltaisuus on kosini väliltä 0–1. Kynnys on valittu tarkastelemalla pareja käsin, joten alla on tulokset usealla kynnyksellä. Eri kielillä kuvatut ja eri maiden hankkeet saavat järjestelmällisesti matalampia arvoja, koska paikannimet ja kielikohtaiset sanat eivät osu yhteen.

Lähdeaineiston kuvaukset ovat lyhyitä (keskimäärin noin 200 merkkiä), mikä heikentää erottelukykyä. Tulokset ovat ehdokkaita tarkistettavaksi, eivät todettuja päällekkäisyyksiä.

| Kynnys | Pareja | saman kokonaisuuden osat | rinnakkainen ilman yhteyttä | peräkkäiset samassa maassa | puuttuva yhteys | yhteydessä | toimija ei tiedossa |
|---|---|---|---|---|---|---|---|
| 0.15 | 2326 | 3 | 489 | 608 | 86 | 741 | 399 |
| 0.2 | 1474 | 3 | 233 | 379 | 18 | 568 | 273 |
| 0.25 | 917 | 3 | 110 | 213 | 3 | 390 | 198 |
| 0.3 | 559 | 3 | 61 | 79 | 1 | 254 | 161 |
| 0.35 | 410 | 3 | 32 | 51 | 0 | 171 | 153 |
| 0.4 | 349 | 2 | 23 | 47 | 0 | 132 | 145 |

## Rinnakkainen ilman yhteyttä (15 samankaltaisinta)

_sama maa, samaan aikaan, ei yhteistä toimijaa eikä yhteistyöpolkua. Voi olla tarkoituksellista (eri kohteet) tai päällekkäistä työtä (sama menetelmä tai suunnittelu kahteen kertaan)._

| A | B | Samankaltaisuus | Yhteiset käsitteet ja sanat | Samaan aikaan |
|---|---|---|---|---|
| A-FI-1fc3 ECO-WADE - carbon and groundwater dynamics in Euro | A-FI-2fd2 MiDiPeat - peat microbial diversity and carbon dyn | 0.818 | yhteish, euroopp, akatemi, suomen, dynamic, hiili | kyllä |
| M-FI-361d Ilmastokestävää metsänhoitoa Kainuuseen | M-FI-82f3 Kaliumilla turvemaat tuottamaan (KaTu) | 0.622 | msr, rahasto, pohjois, elinvoi, suomen, suo | ? |
| M-FI-9d56 Turvemaiden Ilmastoviisas Käyttö | M-FI-f232 Suunnitteluhanke TURPO – turvekasvualustojen hiile | 0.603 | kaakkoi, msr, rahasto, elinvoi, suomen, suo | kyllä |
| M-FI-361d Ilmastokestävää metsänhoitoa Kainuuseen | M-FI-9d56 Turvemaiden Ilmastoviisas Käyttö | 0.582 | msr, rahasto, elinvoi, suomen, ilmasto, suo | kyllä |
| M-FI-361d Ilmastokestävää metsänhoitoa Kainuuseen | M-FI-ebaa Turvemaiden viljanviljelyssä syntyvä ilmasto- ja v | 0.578 | msr, rahasto, pohjois, elinvoi, suomen, ilmasto | kyllä |
| M-FI-0c06 Suometsien puunkorjuun uudet tuulet | M-FI-82f3 Kaliumilla turvemaat tuottamaan (KaTu) | 0.542 | msr, rahasto, pohjois, elinvoi, suomen, suo | ? |
| A-FI-c64f Sphagnum mosses as ecosystem engineers in transiti | A-FI-d1fe Suomen soiden karhukaiset bioindikaattorina soiden | 0.53 | koneen, saatio, vaitost, rahoitt, suo | kyllä |
| M-FI-82f3 Kaliumilla turvemaat tuottamaan (KaTu) | M-FI-9d56 Turvemaiden Ilmastoviisas Käyttö | 0.528 | msr, rahasto, elinvoi, suomen, suo, turvema | ? |
| M-FI-82f3 Kaliumilla turvemaat tuottamaan (KaTu) | M-FI-ebaa Turvemaiden viljanviljelyssä syntyvä ilmasto- ja v | 0.526 | msr, rahasto, pohjois, elinvoi, suomen, suo | ? |
| M-FI-0c06 Suometsien puunkorjuun uudet tuulet | M-FI-ebaa Turvemaiden viljanviljelyssä syntyvä ilmasto- ja v | 0.462 | msr, rahasto, pohjois, elinvoi, suomen, suo | kyllä |
| V-EE-5816 Süsinikubilanss kuuse-kase segametsade vanusereas | V-EE-df6e Soode ökoloogilise funktsionaalsuse tagamiseks vaj | 0.458 | kik, rahoitu, viron, keskkon, lopetat, kansall | kyllä |
| M-FI-0c06 Suometsien puunkorjuun uudet tuulet | M-FI-9d56 Turvemaiden Ilmastoviisas Käyttö | 0.456 | msr, rahasto, elinvoi, suomen, suo | kyllä |
| R-FI-a987 Pengerjoen valuma-alueselvitys | R-FI-aa38 Keuruun Suojoen valuma-alueselvitys | 0.456 | valuma, aluesel, kalatal, vesistot, laadita, toimenp | kyllä |
| K-DE-NI-6f11 Rewetting of the slope moor Friedrichshäuser Bruch | K-DE-NI-c57b Rewetting of the hill moor at the forest town of W | 0.447 | hill, trenche, removin, moor, drainag, vettaminen | kyllä |
| M-FI-5dac Suometsiin liittyvän tiedon lisääminen ja osaamise | M-FI-9d56 Turvemaiden Ilmastoviisas Käyttö | 0.438 | msr, rahasto, elinvoi, suomen, suo | ? |

## Puuttuva yhteys (15 samankaltaisinta)

_eri maat, ei yhteistyöpolkua._

| A | B | Samankaltaisuus | Yhteiset käsitteet ja sanat | Samaan aikaan |
|---|---|---|---|---|
| L-EU-9184 Multi-stakeholder Landscape and Technical Innovati | L-EU-9ecc Scaling Up PEatland Restoration in EUrope | 0.315 | eurosit, ghg, emissio, verenig, ochrony, beheer | kyllä |
| I-DE-NI-1d0c Blue Transition – How to make my region climate re | I-EU-598e Care-Peat – Carbon loss reduction from peatlands:  | 0.289 | france, univers, netherl, recherc, rennes, nationa | ? |
| L-LV-6382 Restoring EU priority grasslands and promoting the | L-SE-0893 Restoration of habitats rich in trees and shrubs | 0.25 | grassla, rich, urgent, habitat, fragmen, require | kyllä |
| K-EU-0882 BUFFER carbon + water in peatlands: landscape-base | K-EU-48f5 Carbon Connects | 0.246 | netherl, belgium, chambre, agricul, france, univers | kyllä |
| LV-03 Ilmastopolitiikkaan sovitetut ratkaisut nostetuill | NI-02 Produktketten aus Niedermoorbiomasse (paludikulttu | 0.24 | paludik, paludikulttuuri, turve | kyllä |
| K-DE-NI-9d56 Planning for the renaturation of the Steinmoor | K-FI-6c73 Konttisuo restoration plan | 0.239 | plan, norther, restora, suunnittelu, luonto, ennallistaminen | ei |
| I-EU-598e Care-Peat – Carbon loss reduction from peatlands:  | K-EU-48f5 Carbon Connects | 0.237 | united, kingdom, netherl, trust, univers, france | ? |
| L-FI-ea10 Restoring the hydrological integrity of wetland ha | L-SE-350f Restoration of EU Redlisted Annex I habitats, depe | 0.237 | most, origina, remains, last, habitat, serious | kyllä |
| L-EU-d0c3 Reduction of CO2 emissions by restoring degraded p | L-LV-8d1e Sustainable and responsible management and re-use  | 0.231 | stored, accordi, carbon, least, degrada, ccm | kyllä |
| L-IE-f155 Restoring Active Raised Bog in Ireland's SAC Netwo | L-LV-2005 Conservation and Management of Priority Wetland Ha | 0.227 | raised, bogs, active, now, these, nat | kyllä |
| L-EU-9ecc Scaling Up PEatland Restoration in EUrope | L-EU-d0c3 Reduction of CO2 emissions by restoring degraded p | 0.226 | estimat, degrade, saksan, co2, nabu, koordin | ei |
| NI-01 KliMo – Klimaschutz durch Moorentwicklung (ohjelma | X-IE-NAT Midlands Just Transition -ohjelma (135,8 M€, 47 ha | 0.223 | hankett, ohjelma | ? |
| L-LV-2005 Conservation and Management of Priority Wetland Ha | L-SE-0893 Restoration of habitats rich in trees and shrubs | 0.217 | now, life13, particu, negativ, highly, biodive | kyllä |
| I-EU-598e Care-Peat – Carbon loss reduction from peatlands:  | K-EU-0882 BUFFER carbon + water in peatlands: landscape-base | 0.214 | france, netherl, univers, west, north, partner | ? |
| A-FI-f0c7 Microbes cycling arsenic and antimony in Northern  | K-DE-NI-f3b0 WetWeb Organic Soils – Networked Research for Moor | 0.212 | researc, soils, turve | kyllä |

## Peräkkäiset samassa maassa (15 samankaltaisinta)

_sama maa, eri aikaan, ei yhteistä toimijaa eikä polkua (toisto tai jatko ilman yhteyttä)._

| A | B | Samankaltaisuus | Yhteiset käsitteet ja sanat | Samaan aikaan |
|---|---|---|---|---|
| A-FI-1fc3 ECO-WADE - carbon and groundwater dynamics in Euro | A-FI-5ced PRENIC - peatland rewetting in nitrogen-contaminat | 0.727 | yhteish, euroopp, akatemi, suomen, rahoitt, suo | ei |
| V-EE-4e98 Eesti põllumajandusmuldade orgaanilise süsiniku si | V-EE-4eb4 Süsinikubilanss palumännikute vanusereas | 0.674 | kik, rahoitu, viron, keskkon, lopetat, kansall | ei |
| V-EE-4e98 Eesti põllumajandusmuldade orgaanilise süsiniku si | V-EE-b287 Hall-lepikud Eesti metsade süsinikubilansis | 0.671 | kik, rahoitu, viron, keskkon, lopetat, kansall | ei |
| V-EE-2d14 Süsinikubilanss viljakate kuusikute vanusereas | V-EE-4e98 Eesti põllumajandusmuldade orgaanilise süsiniku si | 0.646 | kik, rahoitu, viron, keskkon, lopetat, kansall | ei |
| V-EE-4e98 Eesti põllumajandusmuldade orgaanilise süsiniku si | V-EE-a38b Kuivendamise mõju viljakate soometsade süsinikubil | 0.637 | kik, rahoitu, viron, keskkon, lopetat, kansall | ei |
| V-EE-4e98 Eesti põllumajandusmuldade orgaanilise süsiniku si | V-EE-d59e Kasvukoha süsinikubilansi dünaamika lageraie järgs | 0.62 | kik, rahoitu, viron, keskkon, lopetat, kansall | ei |
| V-EE-4eb4 Süsinikubilanss palumännikute vanusereas | V-EE-f93f Reduction of CO2 emissions by restoring degraded p | 0.618 | kik, rahoitu, viron, keskkon, lopetat, kansall | ei |
| V-EE-4e98 Eesti põllumajandusmuldade orgaanilise süsiniku si | V-EE-5816 Süsinikubilanss kuuse-kase segametsade vanusereas | 0.613 | kik, rahoitu, viron, keskkon, lopetat, kansall | ei |
| V-EE-2d74 Metsakuivenduse elustikumõjude leevendusmeetmete v | V-EE-4eb4 Süsinikubilanss palumännikute vanusereas | 0.604 | kik, rahoitu, viron, keskkon, lopetat, kansall | ei |
| V-EE-2d14 Süsinikubilanss viljakate kuusikute vanusereas | V-EE-f93f Reduction of CO2 emissions by restoring degraded p | 0.593 | kik, rahoitu, viron, keskkon, lopetat, kansall | ei |
| A-FI-6568 Liukoisen orgaanisen aineksen ominaisuudet luonnon | A-FI-d1fe Suomen soiden karhukaiset bioindikaattorina soiden | 0.591 | koneen, saatio, vaitost, ennallistaminen, rahoitt, ennalli | ei |
| V-EE-a38b Kuivendamise mõju viljakate soometsade süsinikubil | V-EE-f93f Reduction of CO2 emissions by restoring degraded p | 0.584 | kik, rahoitu, viron, keskkon, lopetat, kansall | ei |
| V-EE-b287 Hall-lepikud Eesti metsade süsinikubilansis | V-EE-f93f Reduction of CO2 emissions by restoring degraded p | 0.583 | kik, rahoitu, viron, keskkon, lopetat, kansall | ei |
| A-FI-1243 Restoring Peatlands: predicting biodiversity, GHG  | A-FI-d1fe Suomen soiden karhukaiset bioindikaattorina soiden | 0.579 | koneen, saatio, vaitost, ennallistaminen, rahoitt | ei |
| V-EE-2d14 Süsinikubilanss viljakate kuusikute vanusereas | V-EE-2d74 Metsakuivenduse elustikumõjude leevendusmeetmete v | 0.579 | kik, rahoitu, viron, keskkon, lopetat, kansall | ei |

## Teema × maapari

Maaparit, joilla on hankkeita samassa teemassa: **91**, joista ilman yhtään vahvistettua yhteistyöpolkua **44**.

| Teema | Maat | Hankkeita | Yhteys |
|---|---|---|---|
| T5 | EE–FI | 28 + 88 | ei |
| T1 | EE–FI | 20 + 54 | ei |
| T5 | DE-NI–EE | 35 + 28 | ei |
| T6 | EE–FI | 20 + 41 | ei |
| T5 | EE–IE | 28 + 15 | ei |
| T6 | DE-NI–EE | 15 + 20 | ei |
| T1 | DE-NI–FI | 5 + 54 | ei |
| T5 | EE–SE | 28 + 6 | ei |
| T6 | EE–SE | 20 + 8 | ei |
| T4 | EE–FI | 4 + 38 | ei |
| T4 | FI–SE | 38 + 3 | ei |
| T1 | DE-NI–EE | 5 + 20 | ei |
| T5 | IE–SE | 15 + 6 | ei |
| T5 | LV–SE | 13 + 6 | ei |
| T3 | DE-NI–IE | 12 + 6 | ei |
| T1 | EE–IE | 20 + 3 | ei |
| T1 | DE-NI–LV | 5 + 11 | ei |
| T8 | DE-NI–FI | 3 + 17 | ei |
| T8 | FI–SE | 17 + 3 | ei |
| T7 | DE-NI–FI | 7 + 7 | ei |
| T6 | EE–IE | 20 + 2 | ei |
| T4 | DE-NI–FI | 1 + 38 | ei |
| T7 | DE-NI–IE | 7 + 5 | ei |
| T1 | IE–LV | 3 + 11 | ei |
| T7 | DE-NI–LV | 7 + 4 | ei |

## Saarekkeet

| # | Solmuja | Maat | Hankkeet ja keskukset |
|---|---|---|---|
| 1 | 327 | EE EU FI IE LV SE | A-EU-10ff A-EU-1892 A-EU-18f8 A-EU-1958 A-EU-88ad A-EU-e163 A-EU-fcae A-FI-0222 A-FI-0ebc A-FI-0f15 A-FI-1123 A-FI-1243 A-FI-1da3 A-FI-1f5c A-FI-1fc3 A-FI-2ee2 A-FI-2f32 A-FI-2fd2 A-FI-3a41 A-FI-50e3 A-FI-5129 A-FI-5277 A-FI-5770 A-FI-57a1 A-FI-593f A-FI-5bc3 A-FI-5cd8 A-FI-5ced A-FI-6420 A-FI-64c3 A-FI-6568 A-FI-663f A-FI-66ca A-FI-68d7 A-FI-71e2 A-FI-72e3 A-FI-8120 A-FI-8915 A-FI-8afc A-FI-99f9 A-FI-9d06 A-FI-b9fb A-FI-c3c5 A-FI-c61b A-FI-c64f A-FI-cc7b A-FI-d1fe A-FI-d390 A-FI-d4c5 A-FI-e29b A-FI-ed8e A-FI-f0c7 A-FI-f1c6 E-LV-6430 E-LV-8eeb E-LV-9406 E-LV-b130 E-LV-c39d E-LV-d12c E-LV-e70c F-LV-594d F-LV-7d15 F-LV-cadf F-LV-dfd5 F-LV-f837 FI-01 FI-06 FI-07 FI-08 FI-09 FI-10 H-FI H-FI-AKA H-LV I-EU-414b I-FI-b431 J-SE-0e6e K-EU-2e51 K-FI-006d K-FI-0ac6 K-FI-1d92 K-FI-519c K-FI-561d K-FI-6894 K-FI-6978 K-FI-6c73 K-FI-6f20 K-FI-7c34 K-FI-879d K-FI-9061 K-FI-9511 K-FI-a45d K-FI-ceda K-FI-e8b3 K-LV-4390 K-LV-74bd K-LV-cbb2 K-SE-dbb8 L-EE-89f5 L-EU-9184 L-EU-d0c3 L-FI-a176 L-FI-ba2f L-FI-dfbb L-FI-e958 L-FI-ea10 L-LV-05ed L-LV-1f9f L-LV-2005 L-LV-2b35 L-LV-42ff L-LV-50b4 L-LV-5d8c L-LV-6382 L-LV-8d1e L-LV-ec74 L-SE-5a2c LV-01 LV-03 M-FI-0c06 M-FI-0ce4 M-FI-17f1 M-FI-1bc7 M-FI-361d M-FI-5dac M-FI-658f M-FI-9dbb M-FI-c9a7 M-FI-d55d M-FI-e41c M-FI-ebaa M-FI-f232 M-FI-f3b2 R-FI-1dd0 R-FI-4496 R-FI-5c35 R-FI-6df1 R-FI-70e5 R-FI-7dd3 R-FI-ba80 R-FI-e3a3 T-SE-bda3 V-EE-0b09 V-EE-1653 V-EE-1e63 V-EE-23f0 V-EE-2d74 V-EE-bb80 V-EE-bff8 V-EE-c03a V-EE-cf0a V-EE-db4f V-EE-df6e V-EE-fd78 V-EE-fdb3 X-FI-PEATRESC |
| 2 | 55 | DE-NI EU IE | E-IE-e6ef H-IE-GAL H-IE-LIFE I-DE-NI-c078 I-EU-598e I-EU-f185 I-EU-f393 IE-01 K-DE-NI-d14f K-IE-7fa4 L-IE-4ec5 L-IE-b2a4 L-IE-d4a5 L-IE-ed33 X-IE-GAL X-IE-LIFE X-IE-NAT |
| 3 | 21 | DE-NI SE | I-DE-NI-1d0c L-SE-1410 |
| 4 | 17 | EE | V-EE-2d14 V-EE-41f4 V-EE-4eb4 V-EE-5816 V-EE-657c V-EE-68d6 V-EE-7b2b V-EE-7f94 V-EE-869e V-EE-8898 V-EE-95f8 V-EE-a38b V-EE-b287 V-EE-d59e V-EE-ed09 V-EE-f333 |
| 5 | 12 | DE-NI | K-DE-NI-36d2 K-DE-NI-9d56 K-DE-NI-a456 K-DE-NI-b8d9 K-DE-NI-e715 K-DE-NI-f68e NI-01 NI-02 NI-03 |
| 6 | 11 | SE | L-SE-350f |
| 7 | 9 | EE | EE-02 V-EE-0a98 V-EE-3a13 V-EE-4177 V-EE-8c2f V-EE-9bf8 V-EE-fac4 V-EE-ff23 |
| 8 | 8 | FI | FI-02 FI-03 K-FI-56cf K-FI-e290 |
| 9 | 7 | DE-NI | K-DE-NI-1c15 K-DE-NI-209b K-DE-NI-9595 K-DE-NI-af02 K-DE-NI-cf1c K-DE-NI-f620 |
| 10 | 6 | EE | V-EE-3d47 V-EE-7917 V-EE-afa9 V-EE-c24e V-EE-d0de |
| 11 | 5 | IE | IE-02 |
| 12 | 5 | DE-NI | E-DE-NI-3e4b |
| 13 | 5 | EU | K-EU-0882 |
| 14 | 5 | SE | L-SE-53b2 |
| 15 | 4 | DE-NI | E-DE-NI-b06d |
| 16 | 4 | DE-NI | K-DE-NI-0e2b K-DE-NI-61e6 K-DE-NI-c1d3 |
| 17 | 4 | EE | V-EE-5807 V-EE-efdf V-EE-f93f |
| 18 | 4 | EU | K-EU-48f5 |
| 19 | 4 | FI | K-FI-06b9 K-FI-b095 |
| 20 | 4 | IE | K-IE-0b63 |
| 21 | 3 | LV | LV-02 |
| 22 | 3 | DE-NI | K-DE-NI-1746 K-DE-NI-dab1 |
| 23 | 3 | DE-NI | K-DE-NI-a450 K-DE-NI-accd |
| 24 | 3 | DE DE-NI | K-DE-NI-0499 K-DE-NI-77b2 |
| 25 | 3 | DE-NI | K-DE-NI-1847 K-DE-NI-34e3 |
| 26 | 3 | DE-NI | K-DE-NI-3eb1 K-DE-NI-ee94 |
| 27 | 3 | DE-NI | K-DE-NI-bf71 K-DE-NI-d8d1 |
| 28 | 3 | DE-NI | K-DE-NI-03c5 K-DE-NI-6c80 |
| 29 | 3 | DE-NI | L-DE-NI-aaba |
| 30 | 3 | EE | V-EE-13e8 V-EE-181a |
| 31 | 3 | EE | V-EE-61dd V-EE-daf4 |
| 32 | 3 | EE | V-EE-097f V-EE-ff69 |
| 33 | 3 | EU | K-EU-5a7e |
| 34 | 3 | EU | K-EU-f426 |
| 35 | 3 | EU | T-EU-73cb T-EU-88fc |
| 36 | 3 | EU FI | A-EU-e4f8 |
| 37 | 3 | FI | K-FI-050e K-FI-b38f |
| 38 | 3 | FI | K-FI-2fcc R-FI-fc0e |
| 39 | 3 | FI | R-FI-34b2 R-FI-b490 |
| 40 | 3 | FI | K-FI-665a K-FI-9cd5 |
| 41 | 3 | FI | M-FI-0705 R-FI-7ce4 |
| 42 | 3 | FI | I-FI-a184 |
| 43 | 3 | FI | K-FI-3bb2 R-FI-87f3 |
| 44 | 3 | SE | K-SE-8b1e K-SE-be89 |
| 45 | 2 | DE-NI | K-DE-NI-e147 |
| 46 | 2 | DE DE-NI | K-DE-NI-44a1 |
| 47 | 2 | DE-NI | K-DE-NI-bd6b |
| 48 | 2 | DE-NI | K-DE-NI-410f |
| 49 | 2 | DE-NI | K-DE-NI-9163 |
| 50 | 2 | DE-NI | K-DE-NI-ca87 |
| 51 | 2 | DE-NI | K-DE-NI-d3d6 |
| 52 | 2 | DE-NI | K-DE-NI-8755 |
| 53 | 2 | DE-NI | K-DE-NI-04a5 |
| 54 | 2 | DE-NI | K-DE-NI-c57b |
| 55 | 2 | DE-NI | K-DE-NI-3ac3 |
| 56 | 2 | DE-NI | K-DE-NI-6f11 |
| 57 | 2 | DE-NI | K-DE-NI-cad6 |
| 58 | 2 | DE-NI | L-DE-NI-83ea |
| 59 | 2 | DE-NI | K-DE-NI-f3b0 |
| 60 | 2 | EE | V-EE-282f |
| 61 | 2 | EE | V-EE-4e98 |
| 62 | 2 | EE | V-EE-2de5 |
| 63 | 2 | EE | V-EE-e77d |
| 64 | 2 | EE | V-EE-4532 |
| 65 | 2 | EE | V-EE-7fa3 |
| 66 | 2 | EE | V-EE-5ba7 |
| 67 | 2 | EU | L-EU-9ecc |
| 68 | 2 | FI | R-FI-3f2a |
| 69 | 2 | FI | R-FI-d4ba |
| 70 | 2 | FI | R-FI-d7e0 |
| 71 | 2 | FI | R-FI-f466 |
| 72 | 2 | FI | K-FI-1fcb |
| 73 | 2 | FI | M-FI-3104 |
| 74 | 2 | FI | M-FI-82f3 |
| 75 | 2 | FI | R-FI-aa38 |
| 76 | 2 | FI | R-FI-f1ce |
| 77 | 2 | FI | R-FI-a987 |
| 78 | 2 | FI | R-FI-e499 |
| 79 | 2 | FI | K-FI-8d28 |
| 80 | 2 | FI | K-FI-cb20 |
| 81 | 2 | FI | K-FI-16d2 |
| 82 | 2 | FI | M-FI-f0a8 |
| 83 | 2 | FI | R-FI-437d |
| 84 | 2 | FI | K-FI-c4ea |
| 85 | 2 | FI | R-FI-b914 |
| 86 | 2 | FI | M-FI-9d56 |
| 87 | 2 | FI | R-FI-295f |
| 88 | 2 | FI | R-FI-7f1e |
| 89 | 2 | FI | R-FI-17e2 |
| 90 | 2 | IE | K-IE-06fb |
| 91 | 2 | IE | K-IE-cee8 |
| 92 | 2 | IE | K-IE-0814 |
| 93 | 2 | IE | L-IE-f155 |
| 94 | 2 | IE | K-IE-d7ff |
| 95 | 2 | IE | K-IE-8525 |
| 96 | 2 | LV | K-LV-2fac |
| 97 | 2 | LV | K-LV-37ba |
| 98 | 2 | SE | J-SE-5a7e |
| 99 | 2 | SE | J-SE-b073 |
| 100 | 2 | SE | T-SE-5e29 |
| 101 | 2 | SE | J-SE-2f3b |
| 102 | 2 | SE | L-SE-0893 |
| 103 | 2 | SE | J-SE-50cf |
| 104 | 2 | SE | J-SE-a3d4 |
| 105 | 2 | IE | H-IE-JTF |
| 106 | 1 | DE-NI | K-DE-NI-7a94 |
| 107 | 1 | DE-NI | K-DE-NI-c05c |
| 108 | 1 | DE-NI | K-DE-NI-d90f |
| 109 | 1 | DE-NI | K-DE-NI-cc25 |
| 110 | 1 | DE-NI | K-DE-NI-e128 |
| 111 | 1 | EE | V-EE-8de1 |
| 112 | 1 | EE | V-EE-0545 |
| 113 | 1 | EE | V-EE-5af6 |
| 114 | 1 | EE | V-EE-7bce |
| 115 | 1 | EE | V-EE-c306 |
| 116 | 1 | EU | A-EU-b538 |
| 117 | 1 | FI | R-FI-609b |
| 118 | 1 | FI | A-FI-4a0c |
| 119 | 1 | FI | A-FI-db3f |
| 120 | 1 | FI | A-FI-9293 |
| 121 | 1 | FI | A-FI-9f42 |
| 122 | 1 | FI | A-FI-4676 |
| 123 | 1 | FI | A-FI-7c97 |
| 124 | 1 | FI | A-FI-4690 |
| 125 | 1 | FI | A-FI-3609 |
| 126 | 1 | FI | A-FI-5eb8 |
| 127 | 1 | FI | A-FI-822d |
| 128 | 1 | FI | R-FI-dba7 |
| 129 | 1 | FI | A-FI-7b9e |
| 130 | 1 | FI | A-FI-ace0 |
| 131 | 1 | FI | A-FI-4167 |
| 132 | 1 | FI | A-FI-9ed2 |
| 133 | 1 | FI | A-FI-e8bb |
| 134 | 1 | FI | A-FI-5a0a |
| 135 | 1 | FI | A-FI-5a0a5772 |
| 136 | 1 | FI | A-FI-d1f1 |
| 137 | 1 | FI | A-FI-cf8d |
| 138 | 1 | FI | A-FI-6f78 |
| 139 | 1 | FI | A-FI-fce4 |
| 140 | 1 | FI | A-FI-a2a9 |
| 141 | 1 | IE | E-IE-9275 |
| 142 | 1 | IE | E-IE-2cb2 |
| 143 | 1 | IE | E-IE-9676 |
| 144 | 1 | DE-SH | X-DE-SH |
