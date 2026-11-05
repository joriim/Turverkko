# Turverkko – turvemaa-alueiden TKI-verkosto

Avoin aineisto ja visualisointi turvemaihin ja maaperään liittyvästä julkisesta TKI-rahoituksesta ja sen toimijaverkostosta. Alueina ovat Suomi, Ruotsi, Viro, Latvia, Irlanti ja Niedersachsen, rahastoina JTF, EAKR, ESR+, maaseuturahasto, EIP-AGRI sekä Horizon 2020 ja Horizon Europe (lisätty 2.11.2026) ja ohjelmakausina 2014–20 ja 2021–27.

**Rajaus:** turvemaat, turvepellot, suometsät, kosteikkoviljely, turvetuotantoalueiden ja soiden ennallistaminen, maaperän ja maankäyttösektorin päästöt, hiilensidonta ja MRV sekä niihin liittyvä osaaminen ja maankäytön suunnittelu. Vety, energiaratkaisut, yleinen yritystuki ja matkailu on rajattu pois. Rajatut hankkeet on lueteltu `src/source.py`:n `REMOVED`-listassa.

Aineistolla on kolme tehtävää:

1. **Visualisointi.** Mihin raha menee, mitkä teemat toistuvat ja paljonko hankkeista jää näytettävää.
2. **Yhteysverkoston dokumentointi.** Kuka osallistuu mihinkin, ja jokaiselle yhteydelle lähde.
3. **Yhteyksien analyysi.** Välittäjäorganisaatiot, erilliset yhteistyösaarekkeet ja puuttuvat yhteydet eli toimijat, jotka tekevät samaa mutta eivät tunne toisiaan.

**Sivusto:** [joriim.github.io/Turverkko](https://joriim.github.io/Turverkko/): etusivu, kartta ja verkosto, haku hankekortteineen, [esitystyökalu](https://joriim.github.io/Turverkko/esitys.html) (rahoitus, aloitetut hankkeet ja ennallistetut hehtaarit vuosittain valitulle alueelle ja ajanjaksolle; toisto, esitystila ja jaettava osoite) sekä ehdotuslomake. Julkaistaan automaattisesti GitHub Actionsilla.

## Keskeiset havainnot (2.11.2026)

Luvut on generoitu tiedostoihin [`analysis/raportti.md`](analysis/raportti.md), [`analysis/paallekkaisyydet.csv`](analysis/paallekkaisyydet.csv) ja [`analysis/herkkyys.csv`](analysis/herkkyys.csv). Ne päivittyvät, kun aineisto kasvaa. Menetelmät on kuvattu tiedostossa [SCHEMA.md](SCHEMA.md).

Aineistossa on 143 hanketta: Kohesiosta 100, EU CAP Networkin EIP-hankkeista 13, EURA 2021:stä 3 (lisäksi 3 täydensi Kohesion hankkeita), Tillväxtverketin projektbankenista 4 ja Ruotsin EIP-tietokannasta 6. Hankkeista 13 on muita maaperähankkeita (maaperän päästöt, hiilensidonta, MRV). Lisäksi mukana on 6 osaamiskeskusta ja 152 organisaatiota, joista 32:lla on ROR-tunniste. Automaattihaun ehdokkaina odottaa tarkistusta noin 140 kansallista tutkimushanketta (OpenAIRE), noin 75 Horizon-hanketta (CORDIS) ja 8 julkaisua.

- **Hankkeet eivät yhdistä toimijoita, tutkimus yhdistää.** Hankkeiden kautta 306 toimijaa jakautuu 81 erilliseen saarekkeeseen. Niistä 63 on yksittäisiä hankkeita toteuttajineen, joten varsinaisia usean hankkeen yhteistyöryppäitä on 18, ja niistä neljä ylittää maarajan. Kun mukaan otetaan organisaatioiden yhteiset turvemaa- ja maaperäjulkaisut vuodesta 2014 (OpenAIRE, 97 organisaatioparia, joista 54 maiden välisiä), 40 tutkimusorganisaatiosta 34 kuuluu samaan usean maan verkkoon (129 toimijaa, kaikki kuusi aluetta). Vahvimmat maiden väliset parit ovat Luke–SLU (38 yhteisjulkaisua), Helsingin yliopisto–SLU (37) ja Ilmatieteen laitos–SLU (24). Yhteistyö siis on olemassa tutkijoiden välillä, mutta se ei näy rakennerahasto- ja EIP-hankkeiden kumppanuuksissa.
- **Rinnakkaista työtä samassa maassa.** Tekstiltään samankaltaisia hankepareja on 102 (kynnys 0,20; tulokset kynnyksillä 0,15–0,40 herkkyystaulukossa). Niistä 75 on samassa maassa samaan aikaan ilman yhteistä toimijaa tai yhteistyöpolkua: 44 Suomessa ja 27 Niedersachsenissa. Suomessa ne ovat enimmäkseen JTF:n turvetuotantoalueiden kosteikko- ja ennallistamishankkeita eri kohteissa (esim. Peat Bogs to Wetlands, Linttirämeen ennallistaminen, Aarreaitta/Kanasuo, Suokeidas). Kohteet ovat eri, mutta menetelmä ja suunnittelu toistuvat ilman yhteistä toimijaa. Toinen esimerkki on kaksi JTF-hanketta turpeettomista kasvualustoista (SEAMKin Turvevapaa ruokaketju ja Xamkin BioKas) ilman yhteyttä.
- **Maiden välillä samankaltaisia hankkeita ilman yhteyttä on vähän: 5.** Esimerkiksi Steinmoorin ennallistamissuunnittelu (Niedersachsen) ja Konttisuon ennallistamissuunnitelma (Suomi). Menetelmä aliarvioi maiden välisiä pareja, koska eri kielillä kuvatut hankkeet saavat matalampia arvoja.
- **Tuotokset näkyvät huonosti julkisissa lähteissä.** 105 hanketta 143:sta saa näyttöasteen 1 (pelkkä kuvaus toimenpiteistä), 31 asteen 2 (määrälliset tavoitteet), 6 asteen 3 (raportoitu toteuma tai tarkistettu tuotos) ja 1 asteen 4. Perusteet näkyvät hankekortissa. Lähteiden lyhyet kuvaukset kertovat yleensä suunnitelmista, joten matala taso tarkoittaa, että tuloksia ei löydy lähteestä, ei sitä, että niitä ei ole.
- **Niedersachsen ennallistaa, Suomi suunnittelee.** Niedersachsenin EFRE-hankkeet 2014–20 ovat pääosin toteutettuja vettämisiä ja suojelualueiden vesitalouden korjauksia. Suomen JTF- ja EAKR-hankkeet ovat pääosin jälkikäytön suunnittelua ja esiselvityksiä.
- **Suomen turvepainotteinen JTF-rahoitus Kohesiossa on pieni.** Kohesiosta löytyi 23 suomalaista JTF-turvemaahanketta, yhteensä 7,6 M€, kun Suomen koko JTF-allokaatio on 465 M€. Luku kattaa vain hakusanoilla löytyneet hankkeet; Kohesion kokonaisviennin suodatus ([hakulähteet](hakulahteet/README.md#1-kohesio-eakr-esr-jtf-koheesiorahasto-interreg)) tarkentaa sen.
- **Ennallistetut hehtaarit ovat lähes kokonaan tavoitteita.** 24 hankkeen teksteistä löytyi hehtaaritieto, ja ne on kirjattu käsin lainauksineen ([`hakulahteet/tulokset/hehtaarit/hehtaarit.csv`](hakulahteet/tulokset/hehtaarit/hehtaarit.csv)). Ennallistavien toimenpiteiden (ennallistaminen, vettäminen, kosteikot) tavoitteita on 6 177 ha, mutta raportoitua toteumaa vain 96 ha (Farm Carbon 95 ha ja yksi EURA-toteuma). Jo päättyneiden hankkeiden tavoitteita, joiden toteumaa lähde ei kerro, on 2 260 ha (Viron jääkturvealueet 2 000 ha, Niedersachsenin vettämiset 255 ha). Hinta hehtaaria kohden (budjetti jaettuna tavoitteella, vain hankkeet, joissa hehtaarit ovat päätuotos) on ennallistamisessa mediaanina 2 289 €/ha (11 hanketta, kvartiiliväli 1 766–4 304), kosteikoissa 3 631 €/ha (2) ja vettämisessä 22 160 €/ha (2). Suurin ero on maiden välillä, ei toimenpiteiden: Suomen ennallistamishankkeet maksavat mediaanina 1 986 €/ha ja Niedersachsenin 28 216 €/ha. Toimenpideluokat noudattavat lähteiden sanamuotoa ja ovat käytännössä pääosin samaa ojien tukkimista; Suomen kohteet ovat laajoja entisiä turvetuotantoalueita, Niedersachsenin pieniä Natura-soita, joiden budjettiin sisältyy maanhankintaa ja rakentamista. Luku on hankkeen hinta hehtaaria kohden, ei ennallistamistyön yksikköhinta. Vertailu on esitystyökalussa ja tiedostossa [`analysis/hehtaarihinta.csv`](analysis/hehtaarihinta.csv). PohjaNevan 4 580 ha:n maakunnallista tavoitetta ei lasketa mukaan, koska se toteutuu muissa JTF-hankkeissa.
- **Ruotsi:** 11 hanketta ja kaksi Tanskan–Ruotsin Interreg-hanketta. Seitsemän on muita maaperähankkeita, ja soiden ennallistamista koskee vain MyreN. Kruunumäärät on muunnettu euroiksi EKP:n vuosikeskikursseilla, ja alkuperäinen summa näkyy hankekortissa.

**Rajoitukset.** Hakukattavuutta ei vielä tunneta: tunnettujen hankkeiden lista ([`hakulahteet/tunnetut.csv`](hakulahteet/tunnetut.csv)) on alussa. Aineistossa on kaksi todennäköistä kaksoiskappaletta tarkistettavaksi ([`analysis/kaksoisehdokkaat.csv`](analysis/kaksoisehdokkaat.csv)). Alueina ovat kuusi turvemaa-aluetta. EU:n suurimpia turvemaa-alueita (Mecklenburg-Vorpommern, Brandenburg, Alankomaat, Tanska, Puola) ei ole mukana, joten maiden väliset tulokset koskevat vain näitä alueita.

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

Verkoston voi avata suoraan selaimessa:

- **Gephi Lite:** [avaa Turverkko](https://gephi.org/gephi-lite/?file=https%3A%2F%2Fjoriim.github.io%2FTurverkko%2Fdata%2Fturverkko.gexf)
- **Cytoscape Web:** [avaa Turverkko](https://web.cytoscape.org/?import=https%3A%2F%2Fjoriim.github.io%2FTurverkko%2Fdata%2Fturverkko.cx2)

Linkit lataavat sivuston tiedostot `turverkko.gexf` ja `turverkko.cx2`, jotka `scripts/site.py` tuottaa jokaisella julkaisulla. Gephi- ja Cytoscape-työpöytäversioihin ne voi ladata samoista osoitteista. Koko verkosto teemoineen on tiedostossa `data/network.graphml`. Taulukkona se löytyy tiedostoista `data/nodes.csv` ja `data/edges.csv`.

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

- **Tutkimuskysymys ja rajaus.** Tavoite vertailla hankkeiden päällekkäisyyttä sekä tuotosten määrää ja laatua, alueiden valinta (EU:n turvemaa-alueet), ohjelmakaudet ja rajaus turvemaihin, turvepeltoihin, suometsiin, kosteikkoviljelyyn, ennallistamiseen sekä maaperän ja maankäyttösektorin päästöihin, hiilensidontaan ja MRV:hen (rajausta laajennettu 2.11.2026, ks. [SCHEMA.md](SCHEMA.md#rajaus-rajaus)).
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
