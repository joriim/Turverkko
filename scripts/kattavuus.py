"""Kattavuustesti: kuinka suuri osa tunnetuista hankkeista löytyy aineistosta tai automaattihaun ehdokkaista.

Tunnetut hankkeet listataan tiedostoon hakulahteet/tunnetut.csv (nimi, lyhenne, maa, rahasto, tunniste, lisaaja,
huom). Lista kootaan hakumenetelmästä riippumatta, esimerkiksi omasta tiedosta, rahoittajien tiedotteista tai
kirjallisuudesta. Hakukattavuus = löydetyt / tunnetut.

Tulos: analysis/kattavuus.md ja analysis/kattavuus.csv.  Aja:  python scripts/kattavuus.py
"""
import csv, json, re, unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def fold(s):
    s = unicodedata.normalize("NFKD", (s or "").lower())
    return re.sub(r"[^a-z0-9]+", " ", "".join(c for c in s if not unicodedata.combining(c))).strip()


def main():
    src = ROOT / "hakulahteet" / "tunnetut.csv"
    if not src.exists():
        return
    known = list(csv.DictReader(open(src, encoding="utf-8-sig")))
    ds = json.loads((ROOT / "data" / "dataset.json").read_text(encoding="utf-8"))
    pool = [("aineisto", p["id"], p["name"], p.get("acronym", ""), " ".join([p.get("url", "")] + p.get("urls", [])))
            for p in ds["projects"] + ds["context"]]
    for f in sorted((ROOT / "hakulahteet" / "automaattihaku").glob("*.csv")):
        if f.name.startswith("julkaisut"):
            continue
        for r in csv.DictReader(open(f, encoding="utf-8-sig")):
            pool.append((f"ehdokas ({f.name})", "", r.get("hanke_nimi", ""), r.get("lyhenne", ""), r.get("url", "")))
    rows = []
    for k in known:
        name, acr, ident = fold(k["nimi"]), fold(k.get("lyhenne")), (k.get("tunniste") or "").strip()
        hit = None
        for where, pid, pname, pacr, purls in pool:
            fp = fold(pname)
            if (ident and ident in purls) or (name and (name == fp or (len(name) > 15 and (name in fp or fp in name)))) \
                    or (acr and len(acr) >= 4 and (acr == fold(pacr) or re.search(rf"\b{re.escape(acr)}\b", fp))):
                hit = (where, pid)
                if where == "aineisto":
                    break
        rows.append(dict(nimi=k["nimi"], maa=k.get("maa", ""), rahasto=k.get("rahasto", ""),
                         loytyi=hit[0] if hit else "ei", tunniste=hit[1] if hit else ""))
    with open(ROOT / "analysis" / "kattavuus.csv", "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()) if rows else ["nimi"])
        w.writeheader(); w.writerows(rows)
    n = len(rows)
    a = sum(1 for r in rows if r["loytyi"] == "aineisto")
    c = sum(1 for r in rows if r["loytyi"].startswith("ehdokas"))
    L = ["# Hakukattavuus", "", "_Generoitu skriptillä `scripts/kattavuus.py`._", "",
         f"Tunnettuja hankkeita **{n}**: aineistossa **{a}** ({round(100 * a / n) if n else 0} %), automaattihaun ehdokkaissa **{c}**, "
         f"löytymättä **{n - a - c}**.", "",
         "Lista on vielä lyhyt, joten luku on suuntaa antava. Lisää tunnettuja hankkeita tiedostoon `hakulahteet/tunnetut.csv`.", "",
         "| Hanke | Maa | Rahasto | Löytyi |", "|---|---|---|---|"]
    L += [f"| {r['nimi']} | {r['maa']} | {r['rahasto']} | {r['loytyi']} {r['tunniste']} |" for r in rows]
    (ROOT / "analysis" / "kattavuus.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"kattavuus: {a}/{n} aineistossa, {c} ehdokkaissa")


if __name__ == "__main__":
    main()
