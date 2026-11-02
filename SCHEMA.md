# Aineistomalli

## Solmut (`data/nodes.csv`)

| kind | Mitä se on | Tunnisteen muoto | Keskeiset kentät |
|---|---|---|---|
| `teema` | Teemaluokka T1–T8 | `T1` | label |
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
| T2 | Turvepellot: vettäminen, vedenpinnan säätö, tulosperusteiset maksut |
| T3 | Kosteikkoviljely (paludikulttuuri) ja turpeen korvaajat |
| T4 | Suometsät: metsitys, ojitettujen suometsien hoito ja ennallistaminen |
| T5 | Luonnontilaisten soiden suojelu ja ennallistaminen |
| T6 | Maankäyttösektorin päästöt: KHK-mittaus, päästökertoimet, inventaario, MRV |
| T7 | Osaamiskeskittymät, klusterit ja tiedonvälitys |
| T8 | Maanomistajat, maankäytön suunnittelu ja turpeesta luopumisen sosioekonomia |

Rajauksen ulkopuolella: vety, energiaratkaisut, yleinen yritystuki, matkailu.

### Näyttöaste (`evidence_level`)

| Taso | Merkitys |
|---|---|
| 0 | Ei tuotostietoa |
| 1 | Laadullinen kuvaus toimenpiteistä |
| 2 | Määrälliset tavoitteet |
| 3 | Raportoituja mitattuja tuloksia |
| 4 | Avoin data tai vertaisarvioitu julkaisu |

### Rajaus (`rajaus`)

Aineiston rajaus on turvemaat ja muu maaperä. Hankkeen kenttä `rajaus` on joko

- `turvemaa`: hanke koskee nimetysti turvemaita, soita, turvepeltoja, suometsiä, turvetuotantoalueita tai turpeen korvaajia
- `maaperä`: hanke koskee maaperän tai maankäyttösektorin päästöjä, hiilensidontaa, päästöjen mittausta ja todentamista (MRV), hiiliviljelyä tai maaperän vesitaloutta, mutta ei nimetysti turvemaata.

Kentässä `rajaus_peruste` on lyhyt peruste maaperähankkeille. Päätökset ovat listassa `MAAPERA` tiedostossa `src/tuonti.py`. Hakusivulla rajauksen voi valita suodattimella.

Rajauksen ulkopuolelle jäävät vety, energia, matkailu, yleinen yritystuki, jätehuolto ilman maaperäyhteyttä sekä ravinteiden kierrätys ja maan kasvukunto ilman päästö- tai hiilinäkökulmaa.

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
