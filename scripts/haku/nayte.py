"""Tulostaa näytevastauksista jäsentimien kehitykseen tarvittavat otteet lokiin."""
import re, sys
from pathlib import Path

d = Path(sys.argv[1])
for f in sorted(d.iterdir()):
    b = f.read_text(encoding="utf-8", errors="replace")
    print(f"\n===== {f.name} ({len(b)} merkkiä) =====")
    if f.suffix == ".json":
        print(b[:3500])
        continue
    title = re.search(r"<title[^>]*>(.*?)</title>", b, re.S)
    print("TITLE:", (title.group(1).strip() if title else "")[:120])
    urls = sorted(set(re.findall(r"""["'](/[^"'\s<>]*(?:api|search|json|export|csv|xlsx|download|sok|projekt)[^"'\s<>]*)["']""", b, re.I)))
    print("POLUT:", urls[:40])
    abs_ = sorted(set(re.findall(r"https?://[^\"'\s<>]*(?:api|json|graphql|search)[^\"'\s<>]*", b, re.I)))
    print("OSOITTEET:", abs_[:30])
    forms = re.findall(r"<form[^>]*>", b, re.I)
    print("LOMAKKEET:", forms[:6])
    inputs = re.findall(r"<input[^>]*name=[\"']([^\"']+)", b, re.I)
    print("KENTÄT:", sorted(set(inputs))[:30])
    print("SCRIPTIT:", re.findall(r"<script[^>]*src=[\"']([^\"']+)", b, re.I)[:15])
