# Lähteiden saavutettavuus GitHub Actionsista

_Ajettu 2026-11-09 11:47 UTC skriptillä `scripts/haku/probe.py`._

| Lähde | Kohde | HTTP | Sisältö | Koko | Aika |
|---|---|---|---|---|---|
| 22 | [OpenAIRE Graph v1 projects](https://api.openaire.eu/graph/v1/projects?search=peatland&pageSize=3) | 200 | application/json | 5539 t | 0.9 s |
| 22 | [OpenAIRE Search API projects](https://api.openaire.eu/search/projects?keywords=peatland&format=json&size=3) | virhe | TimeoutError: The read operation timed out | 0 t | 30.5 s |
| 1 | [Kohesio, hankesivu](https://kohesio.ec.europa.eu/en/projects/Q7735782) | 403 | text/html | 118 t | 0.6 s |
| 1 | [Kohesio, API-arvaus](https://kohesio.ec.europa.eu/api/facet/eu/search/project?language=en&keywords=peat&limit=3) | 403 | text/html | 118 t | 0.6 s |
| 1 | [Kohesio, entiteetti JSON](https://linkedopendata.eu/wiki/Special:EntityData/Q7735782.json) | 403 | text/html | 118 t | 0.6 s |
| 1 | [Kohesio, SPARQL](https://query.linkedopendata.eu/bigdata/namespace/wdq/sparql?query=SELECT+%3Fitem+%3Flabel+WHERE+%7B+VALUES+%3Fitem+%7B+%3Chttps%3A%2F%2Flinkedopendata.eu%2Fentity%2FQ7735782%3E+%7D%0A++%3Fitem+rdfs%3Alabel+%3Flabel+.+FILTER%28LANG%28%3Flabel%29+%3D+%22en%22%29+%7D+LIMIT+5&format=json) | 403 | text/html | 118 t | 0.5 s |
| 1 | [Kohesio, data-sivu](https://kohesio.ec.europa.eu/en/data) | 403 | text/html | 118 t | 0.6 s |
| 10 | [SweCRIS API](https://swecris-api.vr.se/v1/projects/organisations?limit=1) | 401 |  | 0 t | 0.8 s |
| 4 | [keep.eu](https://keep.eu/) | 200 | text/html | 94712 t | 1.2 s |
| 2 | [EU CAP Network](https://eu-cap-network.ec.europa.eu/projects_en) | 200 | text/html | 94794 t | 0.4 s |
| 3 | [LIFE-haku](https://webgate.ec.europa.eu/life/publicWebsite/search) | 200 | text/html | 20488 t | 0.9 s |
| 3 | [EEA LIFE MapServer](https://soer.discomap.eea.europa.eu/arcgis/rest/services/Life/LifeProjects_Dyna_WM/MapServer?f=json) | 200 | application/json | 5011 t | 0.9 s |
| 5 | [EURA 2021](https://eura2021.fi/) | 200 | text/html | 1945 t | 0.4 s |
| 7 | [research.fi](https://research.fi/fi/results/fundings) | 200 | text/html | 135514 t | 1.3 s |
| 8 | [Tillväxtverket Projektbanken](https://projektbank.tillvaxtverket.se/projektbanken2020) | 200 | text/html | 66699 t | 1.0 s |
| 9 | [Landsbygdsnätverket EIP](https://www.landsbygdsnatverket.se/gronanaringarakis/innovationsstodeteipagri.4.html) | 404 | text/html | 4000 t | 0.8 s |
| 18 | [EPA SAFER](https://erc.epa.ie/safer/) | virhe | URLError: <urlopen error [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: Hostn | 0 t | 0.6 s |
| 19 | [Europa für Niedersachsen](https://www.europa-fuer-niedersachsen.niedersachsen.de/) | 200 | text/html | 40659 t | 1.7 s |
| 20 | [DVS EIP-Agrar](https://www.dvs-gap-netzwerk.de/) | 200 | text/html | 132598 t | 1.6 s |
| 21 | [Förderkatalog](https://foerderportal.bund.de/foekat/jsp/StartAction.do) | 200 | text/html | 8689 t | 1.8 s |
| 3 | [LIFE, hakuohjain JS](https://webgate.ec.europa.eu/life/publicWebsite/assets/kendoJs/module/lifePublicWebsite/controller/BasicSearchLifeController.js) | 200 | text/javascript | 25446 t | 0.6 s |
| 3 | [LIFE, RemoteCall JS](https://webgate.ec.europa.eu/life/publicWebsite/assets/kendoJs/commons/support/ajax/RemoteCall.js) | 200 | text/javascript | 4872 t | 0.4 s |
| 2 | [EU CAP Network, OG-haku](https://eu-cap-network.ec.europa.eu/projects/search_en?fulltext=peatland&f%5B0%5D=project_type%3Aoperational_group_project) | 200 | text/html | 181308 t | 0.3 s |
| 20 | [DVS, EIP-projektisuche](https://www.dvs-gap-netzwerk.de/agrar-umwelt/eip-agri/eip-projekt-datenbank/projektsuche/?tx_solr%5Bq%5D=Moor) | 200 | text/html | 171605 t | 1.2 s |
