# Turve – turvemaa-alueiden TKI-verkosto

Avoin aineisto ja visualisointi EU:n turvemaa-alueiden julkisesta TKI-rahoituksesta ja sen toimijaverkostosta. Mukana ovat Suomi, Ruotsi, Viro, Latvia, Irlanti ja Niedersachsen, rahastot JTF, EAKR, ESR+, maaseuturahasto ja EIP-AGRI sekä ohjelmakaudet 2014–20 ja 2021–27.

Aineistolla on kolme tehtävää:

1. **Visualisointi.** Mihin raha menee, mitkä teemat toistuvat ja paljonko hankkeista jää näytettävää.
2. **Yhteysverkoston dokumentointi.** Kuka osallistuu mihinkin, ja jokaiselle yhteydelle lähde.
3. **Yhteyksien analyysi.** Välittäjäorganisaatiot, erilliset yhteistyösaarekkeet ja puuttuvat yhteydet eli toimijat, jotka tekevät samaa mutta eivät tunne toisiaan.

**Sivusto:** `https://OMISTAJA.github.io/turve/` (GitHub Pages, kansio `docs/`)

## Keskeiset havainnot (31.10.2026)

Luvut on generoitu tiedostoon [`analysis/raportti.md`](analysis/raportti.md). Ne päivittyvät, kun aineisto kasvaa.

- 80 toimijaa jakautuu 14 erilliseen yhteistyösaarekkeeseen. Vain yksi saareke ylittää maarajan: suomalainen SuoLiike-hanke ja Latvian PeatTransform-verkosto.
- Maiden välisiä yhteistyösuhteita on lähteellä vahvistettuna yksi. Lisäksi on kolme vahvistamatonta, jotka liittyvät TUKKA-klusterin Irlanti-yhteistyöhön.
- 37 maiden välistä puuttuvaa yhteyttä. Selvimmät ovat Suomen ja Latvian JTF-ennallistamishankkeiden ja Viron jo toteutetun 2 000 ha:n ennallistamisen väliset. Myös Akatemian PeatResC-huippuyksiköllä ja Galwayn All-Ireland Peatlands CoE:lla on täsmälleen samat teemat, mutta ei yhteyttä.
- Vahvimmat välittäjät ovat SeAMK (6 hanketta), University of Galway ja Helsingin yliopisto.

## Rakenne

```
src/source.py          Ainoa käsin muokattava tiedosto: hankkeet, ohjelmat, keskukset,
                       julkaisut, organisaatiot, osallistumiset ja kytkökset lähteineen
scripts/build.py       → data/nodes.csv, edges.csv, network.graphml, network.json, dataset.json
scripts/analyze.py     → analysis/*.csv, analysis/raportti.md, data/analysis.json
scripts/site.py        → docs/index.html (+ docs/data/ ladattaviksi)
site/template.html     Sivun pohja
site/repo.txt          Repon osoite sivun linkkejä varten
```

## Käyttö

```bash
pip install -r requirements.txt
python scripts/build.py && python scripts/analyze.py && python scripts/site.py
```

Verkoston voi avata Gephissä tai Cytoscapessa tiedostosta `data/network.graphml`. Taulukkona se löytyy tiedostoista `data/nodes.csv` ja `data/edges.csv`.

## Aineistomalli lyhyesti

Solmutyypit ovat teema, ohjelma, hanke, osaamiskeskus, vertailukohde, organisaatio ja julkaisu. Särmätyypit ovat osallistuu, kuuluu_keskukseen, yhteistyo, ei_kytkosta, rahoittaa, tuotos, teema ja teemapaallekkaisyys. Jokaisella yhteistyösärmällä on näyttökenttä (`lähde`, `päätelty`, `vahvistamatta`) ja lähde-URL. Tarkemmin: [SCHEMA.md](SCHEMA.md).

## Menetelmä ja rajoitukset

- **Otos, ei populaatio.** Hanketaso on koottu kansallisista rekistereistä, EU CAP Networkin hankesivuilta, ohjelmatiedotteista ja tutkimusportaaleista. Kohesio-tietokantaa ei saatu haettua automaattisesti. Sen maakohtaiset CSV-viennit ([kohesio.ec.europa.eu/en/data](https://kohesio.ec.europa.eu/en/data)) ovat seuraava laajennus.
- **Teemaluokitus** (10 luokkaa) ja **näyttöaste** (0–4) ovat tämän katsauksen omia, ja niitä voi kritisoida. Päällekkäisyys lasketaan teematunnisteiden Jaccard-indeksinä.
- **Yhteistyöverkko** sisältää vain osallistumisen, keskukseen kuulumisen ja dokumentoidun yhteistyön. Rahoitus ja teemojen samankaltaisuus eivät ole yhteistyötä. Saarekkeet ja keskeisyys lasketaan vain lähteellä vahvistetuista yhteyksistä.
- **Puuttuva yhteys** tarkoittaa, että teemat ovat lähes samat (Jaccard ≥ 0,5) eikä vahvistettua polkua ole kolmen askeleen sisällä. Se kertoo, että yhteyttä ei löytynyt julkisista lähteistä. Se ei todista, ettei yhteyttä ole. Tämä on aineiston tärkein korjattava kohta: jos tiedät yhteyden, lisää se.

## Osallistuminen

Puuttuva hanke, organisaatio tai yhteys on tervetullut. Ohje: [CONTRIBUTING.md](CONTRIBUTING.md). Jokainen lisäys tarvitsee julkisen lähteen.

## Lisenssi

Koodi: MIT ([LICENSE](LICENSE)). Aineisto (`src/source.py`, `data/`, `analysis/`): CC BY 4.0 ([LICENSE-DATA](LICENSE-DATA)). Lähteinä käytettyjen sivujen sisältö kuuluu niiden julkaisijoille. Aineistossa on vain tosiasiatietoja ja linkit.
