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
| 1 Kohesio | estää GitHubin palvelimet (HTTP 403) | selainagentti omalla koneella |
| 10 SweCRIS | REST-rajapinta, vaatii avaimen | odottaa avainta (repon salaisuus `SWECRIS_TOKEN`) |
| 4 keep.eu | avoimen datan rajapinta, vaatii avaimen | odottaa avainta (keep.support@interact.eu, salaisuus `KEEP_KEY`) |
| 3 LIFE | hakusivun sisäinen JSON-rajapinta | selvityksessä |
| 2 EU CAP Network, 20 DVS | palvelimella muodostetut hakusivut | selvityksessä |
| muut | ei rajapintaa | selainagentti, ks. [../README.md](../README.md) |

Ajantasainen saavutettavuus: [`saavutettavuus.md`](saavutettavuus.md).
