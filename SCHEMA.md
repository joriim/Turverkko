# Aineistomalli

## Solmut (`data/nodes.csv`)

| kind | Mitä se on | Tunnisteen muoto | Keskeiset kentät |
|---|---|---|---|
| `teema` | Teemaluokka T1–T8 | `T1` | label |
| `ohjelma` | Rahasto-ohjelma tai alueellinen allokaatio | `P-FI-JTF` | country, fund, eur |
| `hanke` | Rajauksen sisällä oleva hanke | `FI-07` | country, fund, period, eur_total, eur_eu, evidence_level, start, end |
| `osaamiskeskus` | CoE, klusteri tai huippuyksikkö | `H-FI`, `H-LV` | country, fund, status, years |
| `vertailukohde` | Rajauksen ulkopuolinen hanke (LIFE, kansallinen, naapurialue) | `X-IE-LIFE` | country, fund |
| `organisaatio` | Toteuttaja tai partneri | lyhyt slug, esim. `seamk` | country, org_type, ror (ROR-tunniste) |
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
Näyttöaste kuvaa, kuinka todennettavaa tietoa hankkeen tuotoksista on julkisesti saatavilla. Se ei mittaa hankkeen laatua. Taso lasketaan skriptissä [`src/naytto.py`](src/naytto.py) vahvimman löydetyn perusteen mukaan, ja perusteet tallennetaan kenttään `evidence_basis` (näkyy hankekortissa).

| Taso | Merkitys | Peruste |
|---|---|---|
| 0 | Ei tuotostietoa | ei kuvausta |
| 1 | Laadullinen kuvaus toimenpiteistä | kuvaus on, ei lukuja |
| 2 | Määrälliset tavoitteet | luku ja yksikkö (ha, km, mittauspisteet, kohteet, innovaatiot, tilat, julkaisut …) tai tarkistamaton linkitetty tuotos |
| 3 | Raportoitu toteuma tai tarkistettu tuotos | toteumailmaisu (toteuma, ennallistettiin, were restored, återvätts, wiedervernässt …), linkitetty raportti, tapahtuma tai ammattijulkaisu, tai OpenAIREn hankkeeseen linkittämät tuotokset |
| 4 | Vertaisarvioitu julkaisu tai avoin aineisto | linkitetty ja tarkistettu vertaisarvioitu julkaisu tai aineisto |

Käsin arvioitu taso säilyy, jos se on laskettua korkeampi. Lähteiden lyhyet kuvaukset kertovat yleensä suunnitelmista, joten matala taso tarkoittaa usein sitä, että tuloksia ei ole julkaistu lähteessä, ei sitä, että niitä ei ole.

### Hehtaarit (`hakulahteet/tulokset/hehtaarit/hehtaarit.csv`)

Ennallistamisen ja muun maankäytön muutoksen pinta-alat kirjataan käsin, lainauksineen, koska tekstistä poimittu luku voi olla kohteen koko, inventoitu ala tai aiempi tuotantoala. Sarakkeet: `kohde_id` (hanke, ohjelma tai keskus), `taso`, `ha`, `laji` (tavoite, toteuma, ohitettu), `toimenpide`, `vuosi` (tavoitteen tai toteuman vuosi, yleensä hankkeen loppuvuosi), `lainaus`, `huom`.

- Ennallistaviksi lasketaan toimenpiteet *ennallistaminen*, *vettäminen* ja *kosteikko*. Hankkeen kentät `ha_target` ja `ha_realised` ovat niiden summia.
- *Metsitys*, *suunnittelu*, *inventointi* ja *muu* näytetään, mutta niitä ei lasketa ennallistettuihin. Muuhun kirjataan myös alueelliset tavoitteet, jotka toteutuvat muissa hankkeissa (kaksoislaskennan välttämiseksi).
- *Ohitettu* tarkoittaa, että maininta on tarkistettu eikä koske hankkeen omaa pinta-alaa.
- Ohjelma- ja keskustason hehtaarit ovat vertailutietoa, eikä niitä lasketa yhteen hankkeiden kanssa.
- `analysis/hehtaari_ehdokkaat.csv` listaa tarkistamattomat hehtaarimaininnat uusista tuonneista.

### Julkaisut (`hakulahteet/tulokset/julkaisut/`)

Tarkistetut julkaisut tuodaan CSV-tiedostoista muodossa [`hakulahteet/julkaisupohja.csv`](hakulahteet/julkaisupohja.csv): `hanke_id` (aineiston hanketunniste), `otsikko`, `tekijat`, `vuosi`, `tyyppi` (vertaisarvioitu, raportti, aineisto, ammattijulkaisu, opinnäyte, konferenssiabstrakti, muu), `julkaisija`, `doi`, `url`, `avoin` (kyllä/ei), `lahde`, `haettu`. Automaattihaku tuottaa ehdokkaat tiedostoon `hakulahteet/automaattihaku/julkaisut-<pvm>.csv`.

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
| `yhteisjulkaisu` | organisaatio ↔ organisaatio | erillinen näyttö | Organisaatioilla on yhteisiä turvemaa- tai maaperäjulkaisuja vuodesta 2014 (OpenAIRE, organisaatiot ROR-tunnisteella). `weight` = julkaisujen määrä. Analyysi raportoi saarekkeet ilman ja kanssa yhteisjulkaisujen; päällekkäisyysparien yhteys lasketaan niiden kanssa. |
| `ei_kytkosta` | keskus ↔ keskus | ei | Haettu, ei löytynyt; kirjataan, jotta haku on toistettavissa |
| `rahoittaa` | ohjelma → hanke | ei | Varmistettu rahoitussuhde |
| `tuotos` | hanke → julkaisu | ei | |
| `teema` | hanke/julkaisu → teema | ei | |

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

## Sisällöllinen päällekkäisyys (`analysis/paallekkaisyydet.csv`)

Päällekkäisyys lasketaan hankkeiden teksteistä skriptissä [`scripts/overlap.py`](scripts/overlap.py), ei teemaluokista. Sarakkeet:

| Sarake | Merkitys |
|---|---|
| `score` | tekstin samankaltaisuus 0–1 (TF-IDF, monikielinen käsitesanasto, kosini) |
| `yhteiset` | eniten samankaltaisuutta tuottavat yhteiset käsitteet ja sanat |
| `samaan_aikaan` | hankkeiden toteutusvuodet menevät päällekkäin (kyllä/ei/?) |
| `yhteiset_toimijat` | organisaatiot, jotka osallistuvat molempiin |
| `etaisyys` | lyhin vahvistettu yhteistyöpolku (askelta) tai "ei polkua" |
| `tyyppi` | saman kokonaisuuden osat · rinnakkainen ilman yhteyttä · peräkkäiset samassa maassa · puuttuva yhteys · yhteydessä |

Kynnyksen herkkyys on tiedostossa `analysis/herkkyys.csv`.

