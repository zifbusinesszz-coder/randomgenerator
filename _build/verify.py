import re, json, glob, subprocess, html, os, collections
def old(f): return subprocess.run(["git", "show", "HEAD:" + f], capture_output=True, text=True).stdout
def grab(s, rx):
    m = re.search(rx, s, re.S); return m.group(1).strip() if m else None
IDS = ["nav", "navLinks", "hamburger", "bookingForm", "bName", "bPhone", "bAddress", "bItems", "bWhen", "submitBtn", "formStatus", "fileInput", "dropZone", "fileList"]
files = {f[:-5] for f in glob.glob("*.html")}
bad = collections.defaultdict(list); n = 0
for f in sorted(glob.glob("*.html")):
    if f == "pro.html": continue
    n += 1; s = open(f).read(); o = old(f)
    t = html.unescape(grab(s, r"<title>(.*?)</title>") or ""); d = html.unescape(grab(s, r'name="description" content="([^"]*)"') or "")
    if not (20 <= len(t) <= 60): bad[f].append(f"title length {len(t)}: {t}")
    if not (90 <= len(d) <= 160): bad[f].append(f"description length {len(d)}: {d}")
    can = grab(s, r'rel="canonical" href="([^"]+)"')
    want = "https://woodswastemn.com/" + ("" if f == "index.html" else f[:-5])
    if o and grab(o, r'rel="canonical" href="([^"]+)"') != can: bad[f].append(f"canonical changed {can}")
    if not o and can != want: bad[f].append(f"new page canonical {can} != {want}")
    sm = open("sitemap.xml").read()
    if f"<loc>{want}</loc>" not in sm: bad[f].append("not in sitemap")
    lds = []
    for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', s, re.S):
        try: lds.append(json.loads(m.group(1)))
        except Exception as e: bad[f].append(f"bad LD {e}")
    oldtypes = sorted(str(json.loads(m.group(1)).get("@type")) for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', o, re.S))
    if o and sorted(str(d.get("@type")) for d in lds) != oldtypes: bad[f].append(f"LD types {oldtypes} → {sorted(str(d.get('@type')) for d in lds)}")
    fq = next((d for d in lds if d.get("@type") == "FAQPage"), None)
    vis = re.findall(r"<details><summary>(.*?)</summary><p>(.*?)</p></details>", s, re.S)
    if not fq or len(fq["mainEntity"]) != len(vis) or len(vis) < 5: bad[f].append(f"FAQ mismatch LD {len(fq['mainEntity']) if fq else 0} vs visible {len(vis)}")
    else:
        for e, (q, a) in zip(fq["mainEntity"], vis):
            if e["name"] != html.unescape(q) or e["acceptedAnswer"]["text"] != html.unescape(a): bad[f].append("FAQ text differs: " + e["name"][:40])
    for i in IDS:
        if s.count(f'id="{i}"') != 1: bad[f].append(f"id {i} x{s.count(f'id=\"{i}\"')}")
    ids = re.findall(r'\sid="([^"]+)"', s); d = [k for k, v in collections.Counter(ids).items() if v > 1]
    if d: bad[f].append(f"dup ids {d}")
    if s.count("<h1") != 1: bad[f].append(f"h1 x{s.count('<h1')}")
    for junk in ("$150", "handle hazardous", "FOOT_SVC_SLOT", "Removal Removal", '="../', "noindex", "Book my free quote", "Preferred date"):
        if junk in s: bad[f].append(f"contains {junk!r}")
    for h in re.findall(r'href="(/[^"#?]*)', s):
        if "'" in h: continue                      # a link built in JavaScript (zone map popups)
        t = h.strip("/")
        if t and not (t in files or os.path.exists(t) or os.path.exists(t + ".html") or os.path.isdir(t)): bad[f].append(f"broken link {h}")
    for src in re.findall(r'src="(/[^"?]+)', s):
        if not os.path.exists(src.lstrip("/")): bad[f].append(f"missing file {src}")
print(f"checked {n} pages · problems on {len(bad)}")
for f, b in bad.items(): print(" ", f, sorted(set(b))[:6])
