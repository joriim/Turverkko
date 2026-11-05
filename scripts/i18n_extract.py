"""Poimii käännettävät tekstikatkelmat sivuista (apuväline en.tsv:n ylläpitoon).

Aja:  python scripts/i18n_extract.py > /tmp/segments.tsv
Tulostaa katkelmat, joita ei vielä ole tiedostossa site/i18n/en.tsv.
"""
import re, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
FILES = ["site/pages/index.html", "site/pages/haku.html", "site/pages/esitys.html", "site/pages/ehdota.html",
         "site/pages/assets/common.js", "site/template.html"]
FI = re.compile(r"[äöÄÖ]|\b(ja|on|tai|ei|ole|kun|joka|jotka|hanke\w*|maa\w*|vuo\w*|kaikki|näytä|valitse|avaa|tuotos\w*|julkais\w*|teema\w*|toimija\w*|yhteis\w*|lähde\w*|rahoitus\w*|aineisto\w*|sivu\w*|haku|hae|kartta|verkosto|esitys|kohde|tulos\w*)\b", re.I)


def known():
    f = ROOT / "site" / "i18n" / "en.tsv"
    if not f.exists():
        return set()
    return {l.split("\t")[0] for l in f.read_text(encoding="utf-8").splitlines() if "\t" in l and not l.startswith("#")}


def segments(text):
    text = re.sub(r"<style>.*?</style>", "", text, flags=re.S)
    out = []
    cands = re.findall(r">([^<>]+)<", text)
    cands += re.findall(r'(?:placeholder|aria-label|title|alt|content|label)="([^"]+)"', text)
    cands += re.findall(r'"((?:[^"\\\n]|\\.){2,})"', text) + re.findall(r"`([^`]{2,})`", text)
    for c in cands:
        for part in re.split(r"\$\{(?:[^{}]|\{[^{}]*\})*\}|<[^>]*>", c):
            p = part.strip(" \n·:–—,.(")
            if len(p) >= 2 and FI.search(p) and not re.search(r"^[\w.]+\(|=>|\bconst\b|\bfunction\b|querySelector", p):
                out.append(p)
    return out


have = known()
seen = set()
for f in FILES:
    for seg in segments((ROOT / f).read_text(encoding="utf-8")):
        if seg not in seen and seg not in have:
            seen.add(seg)
            print(f"{seg}\t\t{f}")
