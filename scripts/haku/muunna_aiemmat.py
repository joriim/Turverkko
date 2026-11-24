"""Muuntaa 3.–4.11.2026 tehdyt KIK-, ESfondi- ja EURA-haut (hakulahteet/vienti/2026-11-03/, 2026-11-04/) tuontimuotoon.

- KIK (11): rahasto KP (Keskkonnaprogramm) ja HKS (päästökauppatulot) ovat Viron kansallista rahoitusta → "Kansallinen".
  KIK:n sivuilla ei ole alku- ja loppupäivää, joten alku = kuvauksen rahoitusvuosi (likiarvo) ja kausi sen mukaan.
- ESfondi (14): TPF (JTF) → JTF, ERAF → EAKR.
- EURA (5): sellaisenaan.

Aja:  python scripts/haku/muunna_aiemmat.py
"""
import csv, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
V, OUT = ROOT / "hakulahteet" / "vienti", ROOT / "hakulahteet" / "tulokset"


def rw(src, dst, fix):
    with open(src, encoding="utf-8-sig") as f:
        r = csv.DictReader(f)
        fields, rows = r.fieldnames, [fix(dict(x)) for x in r]
    with open(dst, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields, quoting=csv.QUOTE_ALL)
        w.writeheader()
        w.writerows(rows)
    print(f"{dst.name}: {len(rows)} riviä")


def kik(x):
    if x["rahasto"].startswith(("KP", "HKS")):
        x["kuvaus"] = f"Viron kansallinen rahoitus: {x['rahasto']}. " + x["kuvaus"]
        x["rahasto"] = "Kansallinen"
    m = re.search(r"rahoitusvuosi (20\d\d)", x["kuvaus"])
    if m and not x["alku"]:
        x["alku"] = m.group(1)
    if not x["ohjelmakausi"]:
        y = int(x["alku"][:4]) if x["alku"][:4].isdigit() else None
        x["ohjelmakausi"] = ("2014-2020" if y and y < 2021 else "2021-2027") if y else ""
    if x["alue"].startswith("Üleriiklikud"):
        x["alue"] = "koko maa"
    return x


def esfondi(x):
    x["rahasto"] = {"TPF (JTF)": "JTF", "ERAF": "EAKR"}.get(x["rahasto"], x["rahasto"])
    return x


if __name__ == "__main__":
    rw(V / "2026-11-03" / "kik_turverkko_lahde11.csv", OUT / "11-kik-2026-11-03.csv", kik)
    rw(V / "2026-11-04" / "esfondi_turverkko_lahde14.csv", OUT / "14-esfondi-2026-11-04.csv", esfondi)
    rw(V / "2026-11-03" / "eura2021_lisarivit.csv", OUT / "5-eura2021-2026-11-03.csv", lambda x: x)
