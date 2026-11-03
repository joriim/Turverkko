"""Hankkeiden alueiden yhtenäistäminen (esitystyökalun aluesuodatin).

Lähteiden aluenimet ovat eri kielillä ja muodoissa (North Savo / Pohjois-Savo, Cuxhaven district).
normalize() palauttaa listan yhtenäisiä aluenimiä. Koko maata tai useaa maata koskevat merkinnät
palauttavat tyhjän listan: hanke näkyy silloin vain, kun aluetta ei ole rajattu.
"""
import re

WHOLE = {"useita maita", "koko viro", "koko latvia", "niedersachsen", "aurora", "öresund-kattegat-skagerrak",
         "östra mellansverige", "manner-suomi", "koko suomi"}
ALIAS = {
    "central ostrobothnia": "Keski-Pohjanmaa", "south ostrobothnia": "Etelä-Pohjanmaa", "north ostrobothnia": "Pohjois-Pohjanmaa",
    "north savo": "Pohjois-Savo", "north karelia": "Pohjois-Karjala", "lapland": "Lappi", "south savo": "Etelä-Savo",
    "south karelia": "Etelä-Karjala", "central finland": "Keski-Suomi",
    "etelä- ja keski-pohjanmaa": ["Etelä-Pohjanmaa", "Keski-Pohjanmaa"],
    "brunswick": "Braunschweig", "county of bentheim": "Grafschaft Bentheim", "emsland (niedersachsen)": "Emsland",
    "oldenburg (niedersachsen)": "Oldenburg",
    "riga": "Rīga",
    "blekinge county": "Blekinge", "hallands län": "Halland", "norrbotten county": "Norrbotten", "skåne län": "Skåne",
    "stockholms län": "Stockholm", "västra götaland county": "Västra Götaland", "västra götalands län": "Västra Götaland",
    "south-east (ie)": "South-East", "south-west (ie)": "South-West", "mid-east region": "Mid-East",
}


def normalize(region):
    out = []
    for t in re.split(r"[;,]", region or ""):
        t = t.strip()
        if not t or t.lower() in WHOLE:
            continue
        a = ALIAS.get(t.lower())
        if a is None:
            a = re.sub(r"\s*\((district)\)|\s+(district|County|län)$", "", t).strip()
        for x in (a if isinstance(a, list) else [a]):
            if x not in out:
                out.append(x)
    return out
