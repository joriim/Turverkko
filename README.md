# Turverkko – turvemaa-alueiden TKI-verkosto

Avoin aineisto ja visualisointi turvemaihin ja maaperään liittyvästä julkisesta TKI-rahoituksesta ja sen toimijaverkostosta. Alueina ovat Suomi, Ruotsi, Viro, Latvia, Irlanti ja Niedersachsen, rahastoina JTF, EAKR, ESR+, maaseuturahasto, EIP-AGRI sekä Horizon 2020 ja Horizon Europe (lisätty 2.11.2026) ja ohjelmakausina 2014–20 ja 2021–27.

**Rajaus:** turvemaat, turvepellot, suometsät, kosteikkoviljely, turvetuotantoalueiden ja soiden ennallistaminen, maaperän ja maankäyttösektorin päästöt, hiilensidonta ja MRV sekä niihin liittyvä osaaminen ja maankäytön suunnittelu. Vety, energiaratkaisut, yleinen yritystuki ja matkailu on rajattu pois. Rajatut hankkeet on lueteltu `src/source.py`:n `REMOVED`-listassa.

Aineistolla on kolme tehtävää:

1. **Visualisointi.** Mihin raha menee, mitkä teemat toistuvat ja paljonko hankkeista jää näytettävää.
2. **Yhteysverkoston dokumentointi.** Kuka osallistuu mihinkin, ja jokaiselle yhteydelle lähde.
3. **Yhteyksien analyysi.** Välittäjäorganisaatiot, erilliset yhteistyösaarekkeet ja puuttuvat yhteydet eli toimijat, jotka tekevät samaa mutta eivät tunne toisiaan.

**Sivusto:** [joriim.github.io/Turverkko](https://joriim.github.io/Turverkko/): etusivu, kartta ja verkosto, haku hankekortteineen, [esitystyökalu](https://joriim.github.io/Turverkko/esitys.html) (rahoitus, aloitetut hankkeet ja ennallistetut hehtaarit vuosittain valitulle alueelle ja ajanjaksolle; toisto, esitystila ja jaettava osoite) sekä ehdotuslomake. Julkaistaan automaattisesti GitHub Actionsilla.

**In English:** [joriim.github.io/Turverkko/en/](https://joriim.github.io/Turverkko/en/). Englanninkieliset sivut kootaan suomenkielisistä: `site/i18n/en.tsv` sisältää sivujen tekstit (tiedosto, suomi, englanti) ja `site/i18n/vocab_en.json` aineiston sanaston (teemat, yhteystyypit, näyttöluokat). Jos sivun tekstiä muutetaan eikä katkelmaa löydy, `scripts/site.py` pysähtyy ja kertoo puuttuvat rivit; `python scripts/i18n_extract.py` listaa kääntämättömät katkelmat. Hankkeiden nimet ja kuvaukset ovat lähteen kielellä.

## Keskeiset havainnot (24.11.2026)

Luvut on generoitu tiedostoihin [`analysis/raportti.md`](analysis/raportti.md), [`analysis/paallekkaisyydet.csv`](analysis/paallekkaisyydet.csv) ja [`analysis/herkkyys.csv`](analysis/herkkyys.csv). Ne päivittyvät, kun aineisto kasvaa. Menetelmät on kuvattu tiedostossa [SCHEMA.md](SCHEMA.md).

Aineistossa on 370 hanketta: Kohesiosta 100, research.fi:stä 77 (Suomen Akatemia, säätiöt, Horizon ja EAKR), KIK:stä (Viro) 62, LIFE-tietokannasta 31, EURA 2021:stä 28, maaseuturahaston hankerekisteristä 19, käsin kirjattuja 17, EU CAP Networkin EIP-hankkeista 13, keep.eu:sta 8, Ruotsin EIP-tietokannasta 6, ESfondista (Latvia) 5 ja Tillväxtverketin projektbankenista 4. Lisäksi useat eri lähteiden rivit täydensivät jo mukana olleita hankkeita (`src/tuonti.py`, `MATCH_EXISTING`). Hankkeista 36 on muita maaperähankkeita (maaperän päästöt, hiilensidonta, MRV). Mukana on 6 osaamiskeskusta ja 369 organisaatiota. Tunnistetuista 31 hanketietokannasta 11 on mukana aineistossa ([lähdeluettelo](hakulahteet/README.md#lähteet-yhdellä-silmäyksellä)).

- **Hankkeet eivät yhdistä toimijoita, tutkimus yhdistää.** Hankkeiden kautta 750 toimijaa jakautuu 144 erilliseen saarekkeeseen. Niistä 114 on yksittäisiä hankkeita toteuttajineen, joten usean hankkeen yhteistyöryppäitä on 30, ja niistä 6 ylittää maarajan. Maiden välisiä vahvistettuja yhteistyösärmiä on 44. Organisaatioiden yhteiset turvemaa- ja maaperäjulkaisut vuodesta 2014 (OpenAIRE) yhdistävät 97 organisaatioparia, joista 54 on maiden välisiä. Vahvimmat maiden väliset parit ovat Luke–SLU (38 yhteisjulkaisua), Helsingin yliopisto–SLU (37) ja Ilmatieteen laitos–SLU (24). Yhteistyö on siis olemassa tutkijoiden välillä, mutta se näkyy heikosti rakennerahasto- ja EIP-hankkeiden kumppanuuksissa.
- **Rinnakkaista työtä samassa maassa.** Tekstiltään samankaltaisia hankepareja on 1474 (kynnys 0,20; tulokset kynnyksillä 0,15–0,40 herkkyystaulukossa). Niistä 233 on samassa maassa samaan aikaan ilman yhteistä toimijaa tai yhteistyöpolkua: 177 Suomessa, 30 Virossa ja 20 Niedersachsenissa. Suomessa ne ovat enimmäkseen JTF:n turvetuotantoalueiden kosteikko- ja ennallistamishankkeita eri kohteissa sekä maaseuturahaston suometsähankkeita. Lisäksi 273 parissa toiselta hankkeelta puuttuu organisaatio (pääosin henkilökohtaisia apurahoja), joten yhteyttä ei voi arvioida; ne on erotettu omaksi luokakseen.
- **Maiden välillä samankaltaisia hankkeita ilman yhteyttä on vähän: 18.** Esimerkiksi Viron ja Irlannin LIFE-keidassuohankkeet. Menetelmä aliarvioi maiden välisiä pareja, koska eri kielillä kuvatut hankkeet saavat matalampia arvoja.
- **Tuotokset näkyvät huonosti julkisissa lähteissä.** 272 hanketta 370:stä saa näyttöasteen 1 (pelkkä kuvaus toimenpiteistä), 56 asteen 2 (määrälliset tavoitteet), 41 asteen 3 (raportoitu toteuma tai tarkistettu tuotos) ja 1 asteen 4. Perusteet näkyvät hankekortissa. Matala taso tarkoittaa, että tuloksia ei löydy lähteestä, ei sitä, että niitä ei ole.
- **Niedersachsen ennallistaa, Suomi suunnittelee ja tutkii.** Niedersachsenin EFRE-hankkeet 2014–20 ovat pääosin toteutettuja vettämisiä ja suojelualueiden vesitalouden korjauksia. Suomen JTF- ja EAKR-hankkeet ovat pääosin jälkikäytön suunnittelua ja esiselvityksiä, ja suomalaisista 161 hankkeesta 64 on kansallista tutkimusrahoitusta.
- **LIFE hallitsee euromääriä, mutta luku on harhaanjohtava.** 31 LIFE-hanketta kattaa 388 M€ aineiston 657 M€:sta. Kuusi suurinta ovat 20–50 M€:n integroituja luonto- ja vesihankkeita, joissa turvemaat ovat vain yksi osatoimenpide. Summat ovat hankkeiden kokonaisbudjetteja, eivät turvemaille kohdistettua rahaa, joten rahastojen välinen euromäärävertailu ei kerro turvemaarahoituksen jakautumisesta.
- **Suomen turvepainotteinen JTF-rahoitus Kohesiossa on pieni.** Kohesiosta löytyi 24 suomalaista JTF-turvemaahanketta, yhteensä 7,7 M€, kun Suomen koko JTF-allokaatio on 465 M€. Luku kattaa vain hakusanoilla löytyneet hankkeet; Kohesion kokonaisviennin suodatus ([hakulähteet](hakulahteet/README.md#1-kohesio-eakr-esr-jtf-koheesiorahasto-interreg)) tarkentaa sen.
- **Ennallistetut hehtaarit ovat lähes kokonaan tavoitteita.** 24 hankkeen teksteistä löytyi hehtaaritieto, ja ne on kirjattu käsin lainauksineen ([`hakulahteet/tulokset/hehtaarit/hehtaarit.csv`](hakulahteet/tulokset/hehtaarit/hehtaarit.csv)). Ennallistavien toimenpiteiden tavoitteita on 6 177 ha, mutta raportoitua toteumaa vain 96 ha. 24.11. tuotujen hankkeiden (LIFE, maaseuturahasto, KIK, ESfondi ja EURA:n lisärivit) hehtaareja ei ole vielä käyty läpi; tarkistamattomia hehtaarimainintoja on 40. Hinta hehtaaria kohden on ennallistamisessa mediaanina 2 289 €/ha (11 hanketta), kosteikoissa 3 631 €/ha (2) ja vettämisessä 22 160 €/ha (2). Suurin ero on maiden välillä: Suomen kohteet ovat laajoja entisiä turvetuotantoalueita, Niedersachsenin pieniä Natura-soita. Luku on hankkeen hinta hehtaaria kohden, ei ennallistamistyön yksikköhinta. Vertailu on esitystyökalussa ja tiedostossa [`analysis/hehtaarihinta.csv`](analysis/hehtaarihinta.csv).
- **Viro:** KIK:n 67 hankkeesta (Viron ympäristöinvestointikeskus) 62 on uusia: suoinventoinnit, jääksoo- ja rabaennallistamiset, kõdusoo-metsien hiilitase ja LULUCF-inventaarion tutkimus. Ne ovat enimmäkseen pieniä kansallisen ympäristöohjelman hankkeita, joista 21 on muita maaperähankkeita.
- **Ruotsi:** 16 hanketta (EIP 6, LIFE 5, Interreg 3, EAKR 2). Seitsemän on muita maaperähankkeita. Ruotsin EU-ohjelmien koko hankelista (1 633 hanketta) ei tuonut uusia turvemaahankkeita. Kruunumäärät on muunnettu euroiksi EKP:n vuosikeskikursseilla.

**Rajoitukset.** Hakukattavuutta ei vielä tunneta: tunnettujen hankkeiden lista ([`hakulahteet/tunnetut.csv`](hakulahteet/tunnetut.csv)) on alussa. Kaksoiskappaleet on tarkistettu käsin 5.11. ja 24.11.2026: eri lähteistä tulleet samat hankkeet on yhdistetty yhdeksi riviksi (`src/tuonti.py`, `MATCH_EXISTING`), ja kaksi automaattista ehdokasparia todettiin erillisiksi hankkeiksi (perustelut `scripts/analyze.py`, `NOT_DUPLICATE`). Uudet ehdokkaat näkyvät tiedostossa [`analysis/kaksoisehdokkaat.csv`](analysis/kaksoisehdokkaat.csv). Alueina ovat kuusi turvemaa-aluetta. EU:n suurimpia turvemaa-alueita (Mecklenburg-Vorpommern, Brandenburg, Alankomaat, Tanska, Puola) ei ole mukana, joten maiden väliset tulokset koskevat vain näitä alueita.

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

## Aineistomalli lyhyesti

Teemat T1–T8 on kuvattu [SCHEMA.md](SCHEMA.md):ssa. Solmutyypit ovat teema, ohjelma, hanke, osaamiskeskus, vertailukohde, organisaatio ja julkaisu. Särmätyypit ovat osallistuu, kuuluu_keskukseen, yhteistyo, ei_kytkosta, rahoittaa, tuotos, teema ja teemapaallekkaisyys. Jokaisella yhteistyösärmällä on näyttökenttä (`lähde`, `päätelty`, `vahvistamatta`) ja lähde-URL. Tarkemmin: [SCHEMA.md](SCHEMA.md).

## Menetelmä ja rajoitukset

- **Otos, ei populaatio.** Hanketaso on koottu kansallisista rekistereistä, EU CAP Networkin hankesivuilta, ohjelmatiedotteista ja tutkimusportaaleista. Kohesio-tietokantaa ei saatu haettua automaattisesti. Sen maakohtaiset CSV-viennit ([kohesio.ec.europa.eu/en/data](https://kohesio.ec.europa.eu/en/data)) ovat seuraava laajennus.
- **Teemaluokitus** (8 turvemaa- ja maaperäluokkaa) ja **näyttöaste** (0–4) ovat tämän katsauksen omia, ja niitä voi kritisoida. Päällekkäisyys lasketaan teematunnisteiden Jaccard-indeksinä.
- **Yhteistyöverkko** sisältää vain osallistumisen, keskukseen kuulumisen ja dokumentoidun yhteistyön. Rahoitus ja teemojen samankaltaisuus eivät ole yhteistyötä. Saarekkeet ja keskeisyys lasketaan vain lähteellä vahvistetuista yhteyksistä.
- **Puuttuva yhteys** tarkoittaa, että teemat ovat lähes samat (Jaccard ≥ 0,5) eikä vahvistettua polkua ole kolmen askeleen sisällä. Se kertoo, että yhteyttä ei löytynyt julkisista lähteistä. Se ei todista, ettei yhteyttä ole. Tämä on aineiston tärkein korjattava kohta: jos tiedät yhteyden, lisää se.

## Osallistuminen

Aineiston laajentamiseen on valmis hakuopas: [hakulahteet/](hakulahteet/README.md) listaa 31 hanketietokantaa ja antaa jokaiselle hakuohjeen Claude in Chromelle. Tiedosto [`hakulahteet/lahteet.csv`](hakulahteet/lahteet.csv) kertoo, mistä on haettu, mistä ei ja missä automaattihaku on käytössä tai mahdollinen. Lähteistä 24–31 on tunnistettu TUKKA-hankkeen hankeselvityksestä (HY Ruralia 2026). Sivustolla on myös [ehdotuslomake](https://joriim.github.io/Turverkko/ehdota.html).


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
