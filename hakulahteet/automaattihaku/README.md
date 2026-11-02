# Automaattihaku

GitHub Actions -työnkulku [`automaattihaku.yml`](../../.github/workflows/automaattihaku.yml) hakee maanantaisin avoimista rajapinnoista uusia hankeehdokkaita ja avaa niistä pull requestin. Ajon voi käynnistää myös käsin (Actions → Automaattihaku → Run workflow).

Tämän kansion tiedostot eivät tule aineistoon automaattisesti. Tuonti (`src/tuonti.py`) lukee vain kansion [`../tulokset/`](../tulokset/).

## Tarkistus

1. Avaa PR:n CSV-tiedosto. Rivit ovat samassa muodossa kuin [`../tuontipohja.csv`](../tuontipohja.csv).
2. Poista rivit, jotka eivät kuulu rajaukseen ([SCHEMA.md](../../SCHEMA.md#rajaus-rajaus)).
3. Saksan rivit tulevat maalla `DE`, koska rahoittajatiedosta ei näe osavaltiota. Muuta Niedersachsenin hankkeet muotoon `DE-NI`; muut jäävät tuonnissa pois.
4. Siirrä hyväksytyt rivit tiedostoon `../tulokset/<lähde>-<lähteen nimi>-<pvm>.csv` ja aja `python scripts/build.py && python scripts/analyze.py && python scripts/site.py`.
5. Yhdistä PR tai sulje se. Hylätyt rivit ehdotetaan uudelleen seuraavalla ajolla, ellei niitä lisätä `src/tuonti.py`:n `EXCLUDE`-listaan.

## Lähteet

| Lähde | Tapa | Tila |
|---|---|---|
| 22 OpenAIRE | [Graph API](https://graph.openaire.eu/docs/apis/graph-api/), ei avainta | käytössä: kansalliset rahoittajat FI, SE, EE, LV, IE, DE; Horizon (EC) rajattu pois |
| 1 Kohesio | estää GitHubin palvelimet (HTTP 403) | selainagentti omalla koneella |
| 10 SweCRIS | REST-rajapinta, vaatii avaimen | odottaa avainta (repon salaisuus `SWECRIS_TOKEN`) |
| 4 keep.eu | avoimen datan rajapinta, vaatii avaimen | odottaa avainta (keep.support@interact.eu, salaisuus `KEEP_KEY`) |
| 3 LIFE | hakusivun sisäinen JSON-rajapinta | selvityksessä |
| 2 EU CAP Network, 20 DVS | palvelimella muodostetut hakusivut | selvityksessä |
| muut | ei rajapintaa | selainagentti, ks. [../README.md](../README.md) |

Ajantasainen saavutettavuus: [`saavutettavuus.md`](saavutettavuus.md).
