"""One-time: pull every page's unique content out of the CURRENT pages into _build/content.json (the source for build.py)."""
import re, html, json, glob, os
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(HERE)
def txt(x): return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", x))).strip()
SERVICES = ["furniture-removal", "appliance-removal", "garage-cleanout", "yard-waste-removal", "construction-debris-removal"]
out = {}
for f in sorted(glob.glob("*.html")):
    slug = f[:-5]
    if slug in ("pro",) or slug.startswith("_"): continue
    s = open(f).read()
    s = s[:s.index("</html>") + 7] if "</html>" in s else s
    head = s[:s.find("</head>")]
    metas = [m for m in re.findall(r'<(?:meta|link)[^>]*>', head)
             if re.search(r'name="(description|keywords|geo\.[a-z]+|twitter:[a-z]+|theme-color)"|property="og:|rel="canonical"', m)]
    title = txt(re.search(r"<title>(.*?)</title>", head, re.S).group(1))
    lds = []
    for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', s, re.S):
        d = json.loads(m.group(1))
        if d.get("@type") != "FAQPage": lds.append(d)
    body = s[s.find("<body"):]
    faq = [(txt(q), txt(a)) for q, a in re.findall(r'class="faq-q"[^>]*>(.*?)<span.*?class="faq-a"><p>(.*?)</p>', body, re.S)]
    sections = re.findall(r'<section[^>]*>.*?</section>', body, re.S)
    intro = None
    for sec in sections:
        if 'section-tight' in sec[:120] and 'id=' not in sec[:60] and '<p' in sec:
            h2 = re.search(r'<h2[^>]*>(.*?)</h2>', sec, re.S)
            eb = re.search(r'class="(?:eyebrow|sec-eyebrow|kicker)[^"]*"[^>]*>(.*?)<', sec, re.S)
            paras = [txt(p) for p in re.findall(r'<p[^>]*>(.*?)</p>', sec, re.S) if len(txt(p)) > 60]
            if h2 and paras and "common questions" not in txt(h2.group(1)):
                intro = {"h2": txt(h2.group(1)), "eyebrow": txt(eb.group(1)) if eb else "", "paras": paras}
                break
    why = None
    m = re.search(r'<section id="about".*?</section>', body, re.S)
    if m:
        paras = [txt(p) for p in re.findall(r'<p[^>]*>(.*?)</p>', m.group(0), re.S) if len(txt(p)) > 60]
        h2 = re.search(r'<h2[^>]*>(.*?)</h2>', m.group(0), re.S)
        why = {"h2": txt(h2.group(1)) if h2 else "", "paras": paras}
    nearby = []
    m = re.search(r'<section id="areas".*?</section>', body, re.S)
    if m:
        nearby = [(txt(t), h) for h, t in re.findall(r'<a[^>]*href="([^"]+)"[^>]*>(.*?)</a>', m.group(0), re.S) if "View" not in txt(t) and "All" not in txt(t)]
    h1 = txt(re.search(r'<h1[^>]*>(.*?)</h1>', body, re.S).group(1)) if re.search(r'<h1', body) else ""
    place = re.search(r'name="geo.placename" content="([^,"]+)', head)
    kind = "home" if slug == "index" else ("service" if slug in SERVICES else "city")
    out[slug] = {"kind": kind, "title": title, "metas": metas, "ld": lds, "h1": h1, "faq": faq, "intro": intro,
                 "why": why, "nearby": nearby, "place": place.group(1) if place else ""}
json.dump(out, open("_build/content.json", "w"), indent=1, ensure_ascii=False)
for k, v in out.items():
    print(f"{k:28s} {v['kind']:8s} faq={len(v['faq'])} intro={'Y' if v['intro'] else '-'} why={'Y' if v['why'] else '-'} near={len(v['nearby'])} ld={[d.get('@type') if isinstance(d.get('@type'), str) else 'LB' for d in v['ld']]} place={v['place']}")
