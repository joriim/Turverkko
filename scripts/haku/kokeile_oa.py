"""Kertakokeilu: OpenAIRE researchProducts -parametrit organisaatiolle (kehitysapu, ei tuota tiedostoja)."""
import json, sys, urllib.error
from yhteinen import get
OA = "https://api.openaire.eu/graph/v1/researchProducts"
org = "openorgs____::6e16c0bf9dd63d3d0c21cce4295d3dba"  # Oulun yliopisto
tries = [
    {"relOrganizationId": org, "pageSize": 2},
    {"relOrganizationId": org, "search": "peatland", "pageSize": 2},
    {"relOrganizationId": org, "search": "peat OR peatland", "pageSize": 2},
    {"relOrganizationId": org, "search": "peatland", "pageSize": 2, "cursor": "*"},
    {"relOrganizationId": org, "search": "peatland", "pageSize": 2, "page": 1},
    {"relOrganizationId": org, "title": "peatland", "pageSize": 2},
]
for t in tries:
    try:
        d = get(OA, t, tries=1)
        h = d.get("header") or {}
        print("OK ", json.dumps(t, ensure_ascii=False), "numFound", h.get("numFound"), "nextCursor" in h, [r.get("mainTitle", "")[:60] for r in d.get("results") or []])
    except urllib.error.HTTPError as e:
        print("ERR", json.dumps(t, ensure_ascii=False), e.code, e.read()[:300])
