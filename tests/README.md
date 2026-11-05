# Linkkitarkistus

Tarkistaa sivuston kaikki sisäiset linkit renderöidyiltä sivuilta, myös JavaScriptin luomat (hankekortit, taulukot, kaaviot, paneelit).

```sh
python scripts/build.py && python scripts/analyze.py && python scripts/site.py
python -m http.server 8765 -d docs &
python -c "import json;n=json.load(open('docs/data/network.json'));json.dump([x['id'] for x in n['nodes']],open('/tmp/ids.json','w'))"
node tests/linkit_keraa.js /tmp/links.json /tmp/ids.json      # vaatii playwrightin
python tests/linkit_tarkista.py /tmp .                          # lukee /tmp/links.json
```

Keräin käy läpi sekä suomenkieliset sivut että englanninkieliset `docs/en/`-sivut. Tarkistettavat kohteet: sivut ja datatiedostot `docs/`-kansiossa, hakukorttien tunnisteet (`haku.html#ID`), sivujen ankkurit, repoon osoittavat linkit (tiedosto tai kansio `git ls-files`:ssä ja Markdown-otsikkoankkuri). Ulkoiset osoitteet listataan mutta niitä ei avata.
