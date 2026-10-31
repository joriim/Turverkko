# Aineistomalli

## Solmut (`data/nodes.csv`)

| kind | Mitä se on | Tunnisteen muoto | Keskeiset kentät |
|---|---|---|---|
| `teema` | Teemaluokka T1–T10 | `T1` | label |
| `ohjelma` | Rahasto-ohjelma tai alueellinen allokaatio | `P-FI-JTF` | country, fund, eur |
| `hanke` | Rajauksen sisällä oleva hanke | `FI-07` | country, fund, period, eur_total, eur_eu, evidence_level, start, end |
| `osaamiskeskus` | CoE, klusteri tai huippuyksikkö | `H-FI`, `H-LV` | country, fund, status, years |
| `vertailukohde` | Rajauksen ulkopuolinen hanke (LIFE, kansallinen, naapurialue) | `X-IE-LIFE` | country, fund |
| `organisaatio` | Toteuttaja tai partneri | lyhyt slug, esim. `seamk` | country, org_type |
| `julkaisu` | Julkaisu, aineisto, kenttäkohde tai tapahtuma | `J1` | year, pub_type, verified, venue |

Maakoodit: `FI`, `SE`, `EE`, `LV`, `IE`, `DE-NI` (Niedersachsen), `DE-SH` (vain vertailu).

### Teemat

| Koodi | Teema |
|---|---|
| T1 | Turvetuotantoalueiden ennallistaminen ja jälkikäyttö |
| T2 | Turvemaat maatilalla: vettäminen, tulosperusteiset maksut |
| T3 | Turpeen korvaajat ja turvebiotalouden tuotteet |
| T4 | Osaamiskeskittymä / Centre of Excellence / klusteri |
| T5 | Vety ja Power-to-X |
| T6 | Uusiutuva energia ja bioenergia |
| T7 | Osaaminen, uudelleenkoulutus, työllisyys |
| T8 | Yritystuki ja elinkeinojen monipuolistaminen |
| T9 | Kasvihuonekaasumittaus, päästökertoimet, MRV |
| T10 | Luontomatkailu ja virkistys |

### Näyttöaste (`evidence_level`)

| Taso | Merkitys |
|---|---|
| 0 | Ei tuotostietoa |
| 1 | Laadullinen kuvaus toimenpiteistä |
| 2 | Määrälliset tavoitteet |
| 3 | Raportoituja mitattuja tuloksia |
| 4 | Avoin data tai vertaisarvioitu julkaisu |

Asteikko mittaa julkaistun tuotostiedon todennettavuutta, ei hankkeen laatua.

## Särmät (`data/edges.csv`)

| kind | Suunta | Yhteistyötä? | Merkitys |
|---|---|---|---|
| `osallistuu` | organisaatio → hanke/keskus | kyllä | `note` = rooli (koordinaattori, partneri, rahoituksen välittäjä, kenttäkumppani) |
| `kuuluu_keskukseen` | hanke → keskus | kyllä | Hanke on osa keskuksen verkostoa |
| `yhteistyo` | keskus/hanke ↔ keskus | kyllä | Dokumentoitu vierailu, yhteinen tutkija, yhteishanke |
| `ei_kytkosta` | keskus ↔ keskus | ei | Haettu, ei löytynyt; kirjataan, jotta haku on toistettavissa |
| `rahoittaa` | ohjelma → hanke | ei | Varmistettu rahoitussuhde |
| `tuotos` | hanke → julkaisu | ei | |
| `teema` | hanke/julkaisu → teema | ei | |
| `teemapaallekkaisyys` | hanke ↔ hanke | ei | Laskettu, `weight` = Jaccard ≥ 0,4, `note` = yhteiset teemat |

### Näyttö (`evidence`)

| Arvo | Merkitys |
|---|---|
| `lähde` | Suora maininta `url`-kentän lähteessä |
| `päätelty` | Yhdistetty kahdesta lähteestä tai nimen perusteella; tarkistettava |
| `vahvistamatta` | Viite löytyi (esim. otsikko arkistosta), mutta sisältöä ei voitu avata |
| `laskettu` | Skriptin tuottama |
| `haku` | Kirjattu hakutulos (ei_kytkosta) |

Analyysi (`scripts/analyze.py`) käyttää saarekkeissa ja keskeisyydessä vain `lähde`- ja `päätelty`-särmiä.

## Analyysin tuotokset (`analysis/`)

| Tiedosto | Sisältö |
|---|---|
| `organisaatiot.csv` | Hankkeiden ja keskusten määrä, tavoitetut maat, välityskeskeisyys, saareke |
| `komponentit.csv` | Erilliset yhteistyösaarekkeet ja niiden maat |
| `puuttuvat_yhteydet.csv` | Teemallisesti päällekkäiset parit ilman polkua ≤ 3 askelta |
| `raportti.md` | Luettava yhteenveto |
