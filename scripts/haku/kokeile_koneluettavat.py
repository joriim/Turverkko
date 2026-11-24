"""Kokeilu: aja uudet koneluettavat haut (KIK, research.fi, ETIS, VN-julkaisut) ja tulosta tulosten alku lokiin.
Ajetaan työnkulussa Automaattihaku (kokeilu = true, skripti = kokeile_koneluettavat.py)."""
import csv, json, subprocess, sys, urllib.request
from pathlib import Path
HERE = Path(__file__).parent
OUT = HERE.parents[1] / "hakulahteet" / "automaattihaku"
r = urllib.request.urlopen(urllib.request.Request("https://www.etis.ee:2346/api/project/getitems?Format=json&Take=1",
                                                   headers={"User-Agent": "Turverkko/1.0"}), timeout=60)
it = json.loads(r.read())[0]
print("ETIS-kentät:", sorted(it.keys()))
for k in ("Guid", "Title", "TitleEng", "Institutions", "FinancingInstitutions"):
    print(" ", k, "=", json.dumps(it.get(k), ensure_ascii=False)[:300])
for s in ["kik.py", "researchfi.py", "vn_julkaisut.py", "etis.py"]:
    print(f"\n===== {s}", flush=True)
    subprocess.run([sys.executable, str(HERE / s)], check=False)
    for f in sorted(OUT.glob(f"{ {'kik.py': '11', 'researchfi.py': '7', 'vn_julkaisut.py': '30', 'etis.py': '33'}[s]}-*.csv")):
        rows = list(csv.DictReader(open(f, encoding="utf-8")))
        print(f.name, len(rows), "riviä")
        for row in rows:
            print(" |", row["alku"], "|", row["rahasto"], "|", row["toteuttaja"][:40], "|", row["hanke_nimi"][:110])
