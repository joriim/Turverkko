import json, re, os, subprocess, sys, unicodedata, urllib.parse
from collections import defaultdict
S, ROOT = sys.argv[1], sys.argv[2]
d = json.load(open(f"{S}/links.json"))
print("puuttuvat kortit:", d["missingCards"])
docs = os.path.join(ROOT, "docs")
net = json.load(open(os.path.join(docs, "data/network.json")))
ids = {n["id"]: n for n in net["nodes"]}
tracked = set(subprocess.run(["git", "-C", ROOT, "ls-files"], capture_output=True, text=True).stdout.split("\n"))
dirs = {os.path.dirname(f) for f in tracked} | {"/".join(f.split("/")[:i]) for f in tracked for i in range(1, f.count("/") + 1)}
REPO = "https://github.com/joriim/Turverkko"

def slug(h):  # GitHubin otsikkoankkuri
    h = h.strip().lower()
    h = re.sub(r"[^\w\- ]", "", h, flags=re.UNICODE)
    return h.replace(" ", "-")

def anchors_md(path):
    t = open(os.path.join(ROOT, path), encoding="utf-8").read()
    out, seen = set(), defaultdict(int)
    for m in re.finditer(r"^#{1,6}\s+(.+?)\s*#*$", t, re.M):
        s = slug(re.sub(r"[`*_\[\]()]", "", m.group(1)))
        out.add(s if not seen[s] else f"{s}-{seen[s]}"); seen[s] += 1
    return out

def html_ids(page):
    t = open(os.path.join(docs, page), encoding="utf-8").read()
    return set(re.findall(r'id="([^"$]+)"', t))

uniq = defaultdict(set)
LOCAL = "http://localhost:8765/"
for l in d["links"]:
    h = l["href"]
    # sisäinen linkki: polku sivuston juuresta selaimen ratkaisemasta osoitteesta (en/-sivut viittaavat ../)
    if h and not re.match(r"[a-z]+:", h) and h != "#" and (l.get("abs") or "").startswith(LOCAL):
        h = l["abs"][len(LOCAL):] or "index.html"
    uniq[h or "(tyhjä)"].add(l["where"].split(":")[0].split("#")[0])
bad, ext, ok = [], defaultdict(set), 0
for href, where in sorted(uniq.items()):
    w = ", ".join(sorted(where))[:80]
    if href in ("(tyhjä)",):
        bad.append((href, w, "tyhjä href")); continue
    if href.startswith(("mailto:", "tel:")):
        ok += 1; continue
    if href.startswith(REPO):
        rest = href[len(REPO):]
        if rest in ("", "/"):
            ok += 1; continue
        m = re.match(r"/(blob|tree)/main/([^#?]*)(#.*)?$", rest)
        if m:
            path = urllib.parse.unquote(m.group(2)).rstrip("/")
            exists = path in tracked if m.group(1) == "blob" else (path in dirs or path in tracked)
            if not exists:
                bad.append((href, w, "repossa ei ole tiedostoa/kansiota")); continue
            if m.group(3) and path.endswith(".md"):
                a = urllib.parse.unquote(m.group(3)[1:])
                if a not in anchors_md(path):
                    bad.append((href, w, f"otsikkoankkuria #{a} ei ole tiedostossa {path}")); continue
            ok += 1; continue
        m = re.match(r"#(.+)$", rest)
        if m:
            a = urllib.parse.unquote(m.group(1))
            if a not in anchors_md("README.md"):
                bad.append((href, w, f"README:ssä ei ole otsikkoa #{a}")); continue
            ok += 1; continue
        if rest.startswith(("/issues", "/actions", "/releases")):
            ok += 1; continue
        bad.append((href, w, "tuntematon repolinkki")); continue
    if re.match(r"https?://", href):
        ext[re.match(r"https?://([^/]+)", href).group(1)].add(href); continue
    # sivuston sisäinen
    u = urllib.parse.urlparse(href)
    page = u.path or None
    frag = urllib.parse.unquote(u.fragment)
    if href == "#":
        bad.append((href, w, "tyhjä ankkuri #")); continue
    if page:
        if not os.path.exists(os.path.join(docs, page)):
            bad.append((href, w, "tiedostoa ei ole sivustolla")); continue
    tp = page or None
    if frag:
        if (tp or "").endswith("haku.html") or (tp is None and any("haku" in x for x in where)):
            if frag not in ids:
                bad.append((href, w, f"hakukorttia {frag} ei ole aineistossa")); continue
        elif tp and tp.endswith(".html"):
            if frag not in html_ids(tp) and not re.match(r"(maa|alku|alue|rahasto|rajaus|loppu)=", frag):
                bad.append((href, w, f"ankkuria #{frag} ei ole sivulla {tp}")); continue
    ok += 1
print(f"\nyksilöllisiä linkkejä {len(uniq)}, kunnossa {ok}, ongelmia {len(bad)}, ulkoisia osoitteita {sum(len(v) for v in ext.values())} ({len(ext)} palvelinta)\n")
for h, w, why in bad:
    print(f"- {h[:110]}\n    {why} · sivut: {w}")
json.dump({"bad": bad, "ext": {k: sorted(v) for k, v in ext.items()}}, open(f"{S}/linkcheck.json", "w"), ensure_ascii=False, indent=1)
print("\nulkoiset palvelimet:", ", ".join(f"{k} ({len(v)})" for k, v in sorted(ext.items(), key=lambda x: -len(x[1]))))
