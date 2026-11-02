# Osallistuminen

Aineisto kasvaa lisäyksillä. Tärkeimpiä ovat yhteydet, joita analyysi pitää puuttuvina, mutta joista sinulla on tietoa.

## Periaatteet

- **Jokaisella lisäyksellä on julkinen lähde.** Lisää URL. Sisäinen tieto ei riitä.
- **Kirjaa vain se, mitä lähde sanoo.** Jos yhdistät kaksi lähdettä tai päättelet, merkitse rooliin `(päätelty)`.
- **Henkilöt eivät ole solmuja.** Jos yhteys perustuu yhteiseen tutkijaan, mainitse se kytköksen `note`-kentässä ammatillisessa roolissa.
- **Summat lähteen mukaan.** Erottele kokonaisbudjetti (`eur_total`) ja EU-osuus (`eur_eu`). Tuntematon arvo on `None`.

## Mistä etsiä

[hakulahteet/README.md](hakulahteet/README.md) listaa hanketietokannat maittain ja rahastoittain valmiine hakuohjeineen. Yksittäisen ehdotuksen voi tehdä myös sivuston lomakkeella, joka luo valmiin issuen.

## Näin lisäät

Kaikki muutokset tehdään tiedostoon `src/source.py`.

**Hanke:** lisää `dict` listaan `PROJECTS`. Lisää vain turvemaihin tai maaperään liittyviä hankkeita. Anna tunniste muodossa `MAA-nn`, teemat T1–T8 ja näyttöaste 0–4 ([SCHEMA.md](SCHEMA.md)).

**Organisaatio:** lisää `ORGS`-listaan. Käytä lyhyttä tunnistetta pienillä kirjaimilla.

**Osallistuminen:** lisää rivi `PARTICIPATION`-listaan:

```python
("seamk", "FI-06", "koordinaattori", "https://lähde"),
```

**Yhteistyö keskusten välillä:** lisää `LINKS`-listaan `kind="dokumentoitu"` ja kuvaus `note`-kenttään. Jos etsit yhteyttä etkä löytänyt sitä, kirjaa `kind="ei kytköstä"`, jotta haku on toistettavissa.

**Julkaisu:** lisää `PUBS`-listaan ja liitä se hankkeeseen (`project`) ja keskukseen (`hub`). Jos et voinut avata julkaisun sivua, merkitse `verified=False`.

Aja sitten:

```bash
python scripts/build.py && python scripts/analyze.py && python scripts/site.py
```

`build.py` pysähtyy, jos särmä viittaa puuttuvaan solmuun tai tunniste toistuu. Committaa myös `data/`, `analysis/` ja `docs/`. GitHub Actions tarkistaa, että ne vastaavat lähdetiedostoa.

## Pull requestin kuvaus

Kerro mitä lisäsit ja mistä lähteestä. Kerro myös, muuttiko lisäys analyysiä: syntyikö uusi yhteys tai yhdistyikö kaksi saareketta. `analysis/raportti.md`:n diff näyttää tämän suoraan.
