# Turverkko – turvemaa-alueiden TKI-verkosto

Avoin aineisto ja visualisointi turvemaihin ja maaperään liittyvästä julkisesta TKI-rahoituksesta ja sen toimijaverkostosta. Alueina ovat Suomi, Ruotsi, Viro, Latvia, Irlanti ja Niedersachsen, rahastoina JTF, EAKR, ESR+, maaseuturahasto ja EIP-AGRI ja ohjelmakausina 2014–20 ja 2021–27.

**Rajaus:** turvemaat, turvepellot, suometsät, kosteikkoviljely, turvetuotantoalueiden ja soiden ennallistaminen, maankäyttösektorin päästöt sekä niihin liittyvä osaaminen ja maankäytön suunnittelu. Vety, energiaratkaisut, yleinen yritystuki ja matkailu on rajattu pois. Rajatut hankkeet on lueteltu `src/source.py`:n `REMOVED`-listassa.

Aineistolla on kolme tehtävää:

1. **Visualisointi.** Mihin raha menee, mitkä teemat toistuvat ja paljonko hankkeista jää näytettävää.
2. **Yhteysverkoston dokumentointi.** Kuka osallistuu mihinkin, ja jokaiselle yhteydelle lähde.
3. **Yhteyksien analyysi.** Välittäjäorganisaatiot, erilliset yhteistyösaarekkeet ja puuttuvat yhteydet eli toimijat, jotka tekevät samaa mutta eivät tunne toisiaan.

**Sivusto:** [joriim.github.io/Turverkko](https://joriim.github.io/Turverkko/): etusivu, kartta ja verkosto, haku hankekortteineen sekä ehdotuslomake. Julkaistaan automaattisesti GitHub Actionsilla.

## Keskeiset havainnot (31.10.2026)

Luvut on generoitu tiedostoon [`analysis/raportti.md`](analysis/raportti.md). Ne päivittyvät, kun aineisto kasvaa.

- 68 toimijaa jakautuu 12 erilliseen yhteistyösaarekkeeseen. Vain yksi saareke ylittää maarajan: suomalainen SuoLiike-hanke ja Latvian PeatTransform-verkosto.
- Maiden välisiä yhteistyösuhteita on lähteellä vahvistettuna yksi. Lisäksi on kolme vahvistamatonta, jotka liittyvät TUKKA-klusterin Irlanti-yhteistyöhön.
- 31 maiden välistä puuttuvaa yhteyttä. Selvimmät ovat Suomen JTF-ennallistamishankkeiden ja Viron jo toteutetun 2 000 ha:n ennallistamisen väliset, Suomen ja Niedersachsenin kosteikkoviljelyhankkeiden väliset sekä Akatemian PeatResC-huippuyksikön ja Irlannin kahden turvemaakeskuksen väliset.
- Ennallistaminen (T1) on tihein teema: 11 hanketta neljässä maassa. Suometsiä (T4) tutkitaan otoksessa vain Suomessa.
- Turvepainotteiset JTF-allokaatiot ovat 826 M€ (Suomi, Latvia, Irlanti). Viron ja Ruotsin JTF:t eivät painota turvetta, ja Niedersachsen ei ole JTF-alue.
- **Aukko:** Ruotsista ei ole otoksessa yhtään turvemaahanketta. Ruotsin turvemaiden vettäminen rahoitetaan pitkälti kansallisesti, ja se on seuraava täydennettävä kohta.

## Rakenne

```
src/source.py          Ainoa käsin muokattava tiedosto: hankkeet, ohjelmat, keskukset,
                       julkaisut, organisaatiot, osallistumiset ja kytkökset lähteineen
scripts/build.py       → data/nodes.csv, edges.csv, network.graphml, network.json, dataset.json
scripts/analyze.py     → analysis/*.csv, analysis/raportti.md, data/analysis.json
scripts/site.py        → docs/: etusivu, kartta, haku, ehdotuslomake (+ docs/data/)
site/pages/            Etusivun, haun ja lomakkeen lähdetiedostot
hakulahteet/           Hakuopas aineiston laajentamiseen (Claude in Chrome)
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

Teemat T1–T8 on kuvattu [SCHEMA.md](SCHEMA.md):ssa. Solmutyypit ovat teema, ohjelma, hanke, osaamiskeskus, vertailukohde, organisaatio ja julkaisu. Särmätyypit ovat osallistuu, kuuluu_keskukseen, yhteistyo, ei_kytkosta, rahoittaa, tuotos, teema ja teemapaallekkaisyys. Jokaisella yhteistyösärmällä on näyttökenttä (`lähde`, `päätelty`, `vahvistamatta`) ja lähde-URL. Tarkemmin: [SCHEMA.md](SCHEMA.md).

## Menetelmä ja rajoitukset

- **Otos, ei populaatio.** Hanketaso on koottu kansallisista rekistereistä, EU CAP Networkin hankesivuilta, ohjelmatiedotteista ja tutkimusportaaleista. Kohesio-tietokantaa ei saatu haettua automaattisesti. Sen maakohtaiset CSV-viennit ([kohesio.ec.europa.eu/en/data](https://kohesio.ec.europa.eu/en/data)) ovat seuraava laajennus.
- **Teemaluokitus** (8 turvemaa- ja maaperäluokkaa) ja **näyttöaste** (0–4) ovat tämän katsauksen omia, ja niitä voi kritisoida. Päällekkäisyys lasketaan teematunnisteiden Jaccard-indeksinä.
- **Yhteistyöverkko** sisältää vain osallistumisen, keskukseen kuulumisen ja dokumentoidun yhteistyön. Rahoitus ja teemojen samankaltaisuus eivät ole yhteistyötä. Saarekkeet ja keskeisyys lasketaan vain lähteellä vahvistetuista yhteyksistä.
- **Puuttuva yhteys** tarkoittaa, että teemat ovat lähes samat (Jaccard ≥ 0,5) eikä vahvistettua polkua ole kolmen askeleen sisällä. Se kertoo, että yhteyttä ei löytynyt julkisista lähteistä. Se ei todista, ettei yhteyttä ole. Tämä on aineiston tärkein korjattava kohta: jos tiedät yhteyden, lisää se.

## Osallistuminen

Aineiston laajentamiseen on valmis hakuopas: [hakulahteet/](hakulahteet/README.md) listaa 22 avointa hanketietokantaa ja antaa jokaiselle hakuohjeen Claude in Chromelle. Sivustolla on myös [ehdotuslomake](https://joriim.github.io/Turverkko/ehdota.html).


Puuttuva hanke, organisaatio tai yhteys on tervetullut. Ohje: [CONTRIBUTING.md](CONTRIBUTING.md). Jokainen lisäys tarvitsee julkisen lähteen.

## Tekijä ja tekijän panos

Turverkko on Miiro Jääskeläisen ([ORCID 0000-0002-0683-8352](https://orcid.org/0000-0002-0683-8352)) asiantuntijatyötä Seinäjoen ammattikorkeakoulussa.

Työ on tehty tekoälyavusteisesti: lähdehaku, koodi, analyysiskriptit ja visualisointi tuotettiin Clauden (Anthropic) avulla tekijän ohjauksessa. Tekijän oma panos:

- **Tutkimuskysymys ja rajaus.** Tavoite vertailla hankkeiden päällekkäisyyttä sekä tuotosten määrää ja laatua, alueiden valinta (EU:n turvemaa-alueet), ohjelmakaudet ja rajaus turvemaihin, turvepeltoihin, suometsiin, kosteikkoviljelyyn, ennallistamiseen ja maankäyttösektorin päästöihin.
- **Asiantuntijatarkistus.** Teemaluokituksen ja hankkeiden välisten kytkösten oikeellisuuden arviointi maaperä- ja ympäristötieteen asiantuntemuksella.
- **Julkaisupäätökset.** Nimi, avoin julkaisu, lisenssit ja jatkokehitysmalli.

Kaikki aineiston luvut ja kytkökset ovat lähteistä, ja lähde-URL on tallennettu jokaiselle riville.

## Lisenssi ja viittaaminen

Tekijänoikeus © 2026 Miiro Jääskeläinen. Repoa saa vapaasti forkata, muokata ja kehittää alla olevien lisenssien ehdoin.

| Osa | Lisenssi | Ehto |
|---|---|---|
| Koodi (`scripts/`, `site/`) | [MIT](LICENSE) | Tekijänoikeusilmoitus ja lisenssiteksti säilytetään kopioissa |
| Aineisto (`src/source.py`, `data/`, `analysis/`) | [CC BY 4.0](LICENSE-DATA) | Tekijä mainitaan ja muutokset kerrotaan |

Viittaustiedot ovat tiedostossa [CITATION.cff](CITATION.cff), ja GitHub näyttää ne "Cite this repository" -painikkeessa. Jokainen GitHub-release arkistoidaan Zenodoon ja saa DOI:n (metatiedot: [.zenodo.json](.zenodo.json)). Lähteinä käytettyjen sivujen sisältö kuuluu niiden julkaisijoille. Aineistossa on vain tosiasiatietoja ja linkit.
