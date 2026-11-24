# Automaattihaku

GitHub Actions -työnkulku [`automaattihaku.yml`](../../.github/workflows/automaattihaku.yml) hakee maanantaisin avoimista rajapinnoista uusia hankeehdokkaita ja avaa niistä pull requestin. Ajon voi käynnistää myös käsin (Actions → Automaattihaku → Run workflow).

Tämän kansion tiedostot eivät tule aineistoon automaattisesti. Tuonti (`src/tuonti.py`) lukee vain kansion [`../tulokset/`](../tulokset/).

## Pull requestin salliminen

Työnkulku tarvitsee luvan avata pull request. Ota se käyttöön kerran: repon **Settings → Actions → General → Workflow permissions** → valitse **Allow GitHub Actions to create and approve pull requests** → Save. Ilman lupaa tulokset jäävät haaraan [`automaattihaku`](https://github.com/joriim/Turverkko/tree/automaattihaku/hakulahteet/automaattihaku), josta PR:n voi avata käsin.

## Tarkistus

1. Avaa PR:n CSV-tiedosto. Rivit ovat samassa muodossa kuin [`../tuontipohja.csv`](../tuontipohja.csv).
2. Poista rivit, jotka eivät kuulu rajaukseen ([SCHEMA.md](../../SCHEMA.md#rajaus-rajaus)).
3. Horizon-hankkeet ovat usein monen maan konsortioita: maa on koordinaattorin maa, jos se on rajauksessa, muuten `EU`. Partnereista luetellaan vain rajauksen maiden osallistujat muodossa `Nimi (maa)`, ja aineistoon niistä tulee organisaatiosolmut.
4. OpenAIREn Saksan rivit tulevat maalla `DE`, koska rahoittajatiedosta ei näe osavaltiota. Muuta Niedersachsenin hankkeet muotoon `DE-NI`; muut jäävät tuonnissa pois.
5. Siirrä hyväksytyt rivit tiedostoon `../tulokset/<lähde>-<lähteen nimi>-<pvm>.csv` ja aja `python scripts/build.py && python scripts/analyze.py && python scripts/site.py`.
6. Yhdistä PR tai sulje se. Hylätyt rivit ehdotetaan uudelleen seuraavalla ajolla, ellei niitä lisätä `src/tuonti.py`:n `EXCLUDE`-listaan.

## Lähteet

| Lähde | Tapa | Tila |
|---|---|---|
| 22 OpenAIRE | [Graph API](https://graph.openaire.eu/docs/apis/graph-api/) ja Search API (osallistujat), ei avainta | käytössä: kansalliset rahoittajat FI, SE, EE, LV, IE, DE, hanke päättyy 2014 tai myöhemmin; Horizon (EC) haetaan CORDISista. Turvemaahankkeet ovat tiedoston alussa, muut maaperähankkeet sen jälkeen |
| 22 OpenAIRE, julkaisut | Graph API, haku hankkeen lyhenteellä | käytössä: ehdokkaat tiedostoon `julkaisut-<pvm>.csv`; hyväksytyt kansioon `../tulokset/julkaisut/` |
| ROR ja OpenAIRE, yhteisjulkaisut | ROR:n affiliaatiohaku, OpenAIRE-organisaation tuotokset | käytössä: `ror-<pvm>.csv` ja `yhteisjulkaisut-<pvm>.csv`; hyväksytyt tiedostoihin `../tulokset/verkosto/ror.csv` ja `../tulokset/verkosto/yhteisjulkaisut.csv` |
| 23 CORDIS | avoimet CSV-viennit (H2020, Horizon Europe), ei avainta | käytössä: hankkeet, joissa osallistuja rajauksen maista; Niedersachsen NUTS-koodista DE9 |
| 7 research.fi | portaalin hakuindeksi (Elasticsearch), ei avainta | käytössä: rahoituspäätökset 2014–, haku nimestä, kuvauksesta ja avainsanoista; `7-research-fi-<pvm>.csv`. Henkilöiden nimiä ei kirjata |
| 11 KIK | koko hankeluettelo XML-tiedostona (`projects.xml`) | käytössä: rahoitusvuodet 2014–, seulonta nimestä ja kuvauksesta (myös virolainen suo- ja turvesanasto); `11-kik-<pvm>.csv`. Url on KIK:n haku hankkeen nimellä |
| 30 Valtioneuvoston julkaisut | DSpace 7 -hakurajapinta | käytössä: julkaisut 2014–; `30-vn-julkaisut-<pvm>.csv`. Kirjataan selvityshankkeina tai julkaisuina |
| 33 ETIS | avoin rajapinta `www.etis.ee:2346/api/project/getitems` | käytössä: kaikki hankkeet sivuittain, rajaus paikallisesti; `33-etis-<pvm>.csv` |
| 1 Kohesio | estää GitHubin palvelimet (HTTP 403) | selainagentti omalla koneella |
| 10 SweCRIS | REST-rajapinta, vaatii avaimen | odottaa avainta (repon salaisuus `SWECRIS_TOKEN`) |
| 4 keep.eu | avoimen datan rajapinta, vaatii avaimen | odottaa avainta (keep.support@interact.eu, salaisuus `KEEP_KEY`) |
| 3 LIFE | EEA:n LIFE-MapServer (ArcGIS REST, JSON) ja hakusivun sisäinen JSON-rajapinta | MapServer ei vastaa GitHubista (aikakatkaisu 24.11.2026); sisäinen rajapinta tarkistamatta |
| 20 DVS | EIP-projektihaku on POST-lomake | GET-osoite ei hae EIP-tietokannasta; selainagentti |
| 2 EU CAP Network | toimintaryhmähaku estää palvelimen (403) | selvityksessä |
| 14 ESfondi | tulokset ladataan JavaScriptillä | selainagentti |
| 24 EURA 2014, 26 Hiilestä kiinni, 28 MAKERA | eivät vastaa GitHubista (aikakatkaisu tai 403) | selainagentti |
| muut | ei rajapintaa | selainagentti |

Kaikkien lähteiden haku- ja automaatiotila: [`../lahteet.csv`](../lahteet.csv) ja taulukko [../README.md](../README.md#lähteet-yhdellä-silmäyksellä).

Ajantasainen saavutettavuus: [`saavutettavuus.md`](https://github.com/joriim/Turverkko/blob/automaattihaku/hakulahteet/automaattihaku/saavutettavuus.md) (haarassa `automaattihaku`, päivittyy jokaisella ajolla).
