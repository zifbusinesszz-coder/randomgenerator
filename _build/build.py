"""Builds every page of woodswastemn.com from _build/content.json + one design (site.css).
  python3 _build/build.py          → rewrites index.html, the 36 city pages and the 5 service pages
Home = the approved /preview/ design (paths made root-relative, SEO head + structured data from the old homepage).
City / service pages = one shared template; each keeps its own title, meta, canonical, structured data, local write-up and FAQ."""
import json, os, re, html, hashlib

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
C = json.load(open(os.path.join(ROOT, "_build", "content.json")))
CSS_V = hashlib.md5(open(os.path.join(ROOT, "site.css"), "rb").read()).hexdigest()[:10]   # changes whenever site.css does → no stale styles
PHONE, TEL, SMS = "(507) 298-1179", "tel:5072981179", "sms:+15072981179"
GOOGLE = "https://share.google/2VDupAN3BZz3mM9Ml"
esc = lambda s: html.escape(str(s), quote=True)

CHECK = '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6 9 17l-5-5"/></svg>'
ARROW = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'
BUBBLE = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12a8 8 0 0 1-11.6 7.1L4 20l1-4.6A8 8 0 1 1 21 12z"/></svg>'

SERVICES = [  # slug, card title, card text, icon path
    ("furniture-removal", "Furniture removal", "Couches, sectionals, mattresses, dressers, desks and recliners.",
     '<path d="M4 11V8a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v3M3 13a2 2 0 0 1 4 0v2h10v-2a2 2 0 0 1 4 0v5H3zM6 18v2M18 18v2"/>'),
    ("appliance-removal", "Appliance removal", "Fridges, washers, dryers, freezers and water heaters, removed the right way.",
     '<rect x="5" y="2" width="14" height="20" rx="2"/><path d="M5 9h14M9 5v1M9 12v3"/>'),
    ("garage-cleanout", "Garage cleanouts", "Years of stuff gone in an afternoon. Floor swept when we leave.",
     '<path d="M3 21V9l9-6 9 6v12M7 21v-8h10v8M7 17h10"/>'),
    ("yard-waste-removal", "Yard waste", "Branches, brush, old landscaping, playsets and trampolines.",
     '<path d="M11 20A7 7 0 0 1 4 13c0-6 7-10 16-10-1 9-5 16-9 17zM4 21c4-4 7-7 10-11"/>'),
    ("construction-debris-removal", "Construction debris", "Drywall, lumber, flooring, tile and remodel leftovers.",
     '<path d="M2 20h20M5 20V10l7-6 7 6v10M9 20v-5h6v5"/>'),
]
ESTATE = ("/estate-cleanout", "Estate &amp; move-out cleanouts", "Whole-house, basement and rental turnovers. We donate what’s usable.",
          '<path d="M3 10l9-7 9 7v10a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1zM9 21v-6h6v6"/>')

# per service: name, what we take (* = extra disposal fee), photo pair, heavy-load note
SVC = {
    "furniture-removal": dict(name="Furniture removal", pair="curb", items=[
        "Couches, sofas &amp; sectionals", "Recliners &amp; armchairs", "Mattresses &amp; box springs*", "Bed frames &amp; headboards",
        "Dressers &amp; nightstands", "Tables &amp; chairs", "Desks &amp; office furniture", "Bookshelves &amp; entertainment centers",
        "Patio furniture", "Cribs &amp; kids’ furniture"]),
    "appliance-removal": dict(name="Appliance removal", pair="curb", items=[
        "Refrigerators &amp; freezers*", "Washers &amp; dryers", "Dishwashers", "Stoves &amp; ovens", "Microwaves",
        "Water heaters", "Window AC units*", "Dehumidifiers*", "Grills", "Small appliances"]),
    "garage-cleanout": dict(name="Garage cleanouts", pair="garage", items=[
        "Old furniture", "Tools &amp; workbenches", "Lawn mowers &amp; snowblowers", "Bikes &amp; sporting goods",
        "Boxes &amp; storage bins", "Shelving &amp; cabinets", "Old appliances*", "Scrap wood &amp; metal",
        "Tires*", "Holiday decor &amp; toys"]),
    "yard-waste-removal": dict(name="Yard waste removal", pair="yard", heavy="Heavy loads like dirt, rock and concrete can carry a weight surcharge.", items=[
        "Branches &amp; brush", "Leaves &amp; yard bags", "Shrubs &amp; old landscaping", "Fencing &amp; lumber",
        "Playsets &amp; swing sets", "Trampolines", "Firewood &amp; logs", "Landscape timbers &amp; edging"]),
    "construction-debris-removal": dict(name="Construction debris removal", pair="lot", heavy="Heavy loads like concrete, brick and tile can carry a weight surcharge.", items=[
        "Drywall", "Lumber &amp; scrap wood", "Flooring &amp; carpet", "Tile", "Cabinets &amp; countertops",
        "Doors &amp; windows", "Toilets, sinks &amp; tubs", "Trim &amp; molding", "Pallets", "Job-site trash &amp; packaging"]),
}
NEW = json.load(open(os.path.join(ROOT, "_build", "new_services.json")))
NEW_ICONS = {
    "estate-cleanout": '<path d="M3 10l9-7 9 7v10a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1zM9 21v-6h6v6"/>',
    "basement-cleanout": '<path d="M3 9l9-6 9 6M5 9v12h14V9M9 21v-4h6v4M8 13h8"/>',
    "move-out-cleanout": '<path d="M3 7h11v10H3zM14 10h4l3 3v4h-7M7 20a2 2 0 1 0 0-4 2 2 0 0 0 0 4zM17 20a2 2 0 1 0 0-4 2 2 0 0 0 0 4z"/>',
    "mattress-removal": '<path d="M3 9h18v8H3zM3 13h18M5 17v2M19 17v2M6 9V6h12v3"/>',
    "hot-tub-removal": '<path d="M3 11h18v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2zM7 8c0-2 2-2 2-4M12 8c0-2 2-2 2-4M17 8c0-2 2-2 2-4"/>',
    "commercial-junk-removal": '<path d="M4 21V5a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v16M16 9h3a1 1 0 0 1 1 1v11M8 7h4M8 11h4M8 15h4M2 21h20"/>',
}
for _slug, _n in NEW.items():
    SVC[_slug] = dict(name=_n["name"], pair=_n["pair"], items=_n["items"])
MORE_SERVICES = [(k, v["name"], v["card"], NEW_ICONS[k]) for k, v in NEW.items()]
ALL_SVC_NAMES = {**{k: v["name"] for k, v in SVC.items()}}

PAIRS = {
    "garage": ("garage", "Garage cleanout", "Same day", "A garage piled high with boxes, a recliner and broken furniture", "The same garage floor, cleared"),
    "curb": ("curb", "Bedroom set &amp; furniture", "Curbside haul", "A bedroom set, loveseat and bed frame on a lawn", "The lawn after everything was hauled away"),
    "lot": ("lot", "Business back-lot cleanup", "Commercial", "Pallets, a cabinet and tabletops behind a business", "The same back lot, cleared"),
    "yard": ("yard", "Yard &amp; trampoline removal", "Residential", "Bookshelves, a play table and a trampoline on a lawn", "The same yard, cleared"),
}
RATING, NREV = "4.8", "17"          # Google, 2026-11-20 (Places API). Update both when the profile changes.
OLD_REVIEWS = [
    ("KH", "Kjerstin Hedstrom", "Responsive and timely! All my junk was gone less than 24 hours after contacting them. Great job!"),
    ("MD", "Mary DeHate", "Responded quickly, showed up when they said and cheerfully hauled stuff away. Very positive experience."),
    ("BA", "Bryan Anders", "Helped tremendously and priced very fairly. Very pleasant to work with. I would recommend."),
    ("OL", "Olivia", "Easy to contact and the service was quick, easy and affordable. Definitely recommend!!"),
    ("SP", "Shayla P.", "Had them help clean out my garage. Incredibly fast and nice!"),
]


def _trim(t, n=230):
    t = re.sub(r"\s+", " ", t).strip()
    if len(t) <= n:
        return t
    cut = max(t.rfind(". ", 0, n), t.rfind("! ", 0, n))
    return t[:cut + 1] if cut > 80 else t[:n].rsplit(" ", 1)[0] + "…"


def _load_reviews():
    out = []
    try:
        g = json.load(open(os.path.join(ROOT, "_build", "google_reviews.json")))
        for r in g.get("reviews", []):
            if r.get("rating") == 5 and r.get("text"):
                nm = r["name"].title() if r["name"].islower() else r["name"]
                out.append({"name": nm, "text": _trim(r["text"]), "photo": r.get("photo") or "",
                            "init": "".join(w[0] for w in nm.split()[:2]).upper()})
    except Exception:
        pass
    order = ["Cunto House", "Bob Gremel", "Dan Hornseth", "Melissa Colbert"]
    out.sort(key=lambda r: order.index(r["name"]) if r["name"] in order else 9)
    have = {r["name"] for r in out}
    out += [{"name": n, "text": t, "photo": "", "init": i} for i, n, t in OLD_REVIEWS if n not in have]
    return out


REVIEWS = _load_reviews()


def rev_card(r):
    av = (f'<img class="av" src="{esc(r["photo"])}" alt="" width="38" height="38" loading="lazy" referrerpolicy="no-referrer" '
          f'onerror="this.outerHTML=\'<span class=&quot;av&quot;>{r["init"]}</span>\'">' if r["photo"] else f'<span class="av">{r["init"]}</span>')
    return (f'<div class="rev reveal"><span class="stars">★★★★★</span><q>{esc(r["text"])}</q>'
            f'<div class="who">{av}<div>{esc(r["name"])}<small>Google review</small></div></div></div>')


TIERS = [(0.12, "Minimum", "up to ~2 cu yd", "1–2 items: a couch, a mattress set, an appliance", "$199"),
         (0.25, "1/4 load", "~4 cu yd", "A few pieces of furniture or a small pile", "$329"),
         (0.5, "1/2 load", "~7.5 cu yd", "A room’s worth or a small garage", "$479"),
         (0.75, "3/4 load", "~11 cu yd", "A big garage or basement", "$629"),
         (1.0, "Full load", "~15 cu yd", "Whole-house or estate cleanouts", "$779")]
TIER_GUIDE = "As a guide: about $329 for a quarter load, $479 for a half, $629 for three-quarters and $779 for a full 15-yard load."
FEE_NOTE = "Items with extra dump fees (mattresses, Freon appliances, tires, TVs) add to the total, and you always get the full price before we start."
NO_HAZ = "We don’t take paint, chemicals or other hazardous waste."


def truck(frac):
    w = 70 * frac; x0 = 80 - w
    lines = "".join(f'<line x1="{x}" y1="9" x2="{x}" y2="45" stroke="#fff" stroke-opacity=".35" stroke-width="1.5"/>' for x in (24, 42, 60) if x > x0)
    return ('<svg class="truck" viewBox="0 0 124 66" aria-hidden="true"><rect x="4" y="6" width="78" height="42" rx="4" fill="#fff" stroke="#121212" stroke-width="3"/>'
            f'<rect x="{x0:.1f}" y="9" width="{w:.1f}" height="36" rx="2" fill="#178a63"/>{lines}'
            '<path d="M84 18h18l12 14v16H84z" fill="#121212"/><path d="M89 22h11l8 9H89z" fill="#cfe9dd"/><rect x="2" y="47" width="114" height="5" rx="2" fill="#121212"/>'
            '<circle cx="24" cy="55" r="8" fill="#121212"/><circle cx="24" cy="55" r="3" fill="#fff"/><circle cx="98" cy="55" r="8" fill="#121212"/><circle cx="98" cy="55" r="3" fill="#fff"/></svg>')


def _fit(cands, n):
    for c in cands:
        if len(c) <= n:
            return c
    return cands[-1][:n]


def seo(slug, p):
    """→ (title ≤ 60, description ≤ 155) written to win the click: price, same-day, stars, one action."""
    if p["kind"] == "partner":
        return ("Junk Removal for Realtors & Property Managers | Wood’s Waste"[:60] if len("Junk Removal for Realtors & Property Managers | Wood’s Waste") <= 60
                else "Realtor & Property Manager Junk Removal | Wood’s Waste",
                "Junk removal partner for south metro realtors & property managers. 10% off whole-house cleanouts, priority scheduling, before/after photos.")
    if p["kind"] == "home":
        t = _fit(["Same-Day Junk Removal, South Metro MN | Wood’s Waste", "Junk Removal South Metro MN | Wood’s Waste"], 60)
        d = f"Local junk removal in Farmington, Lakeville, Apple Valley & the south metro. Same-day pickup from $199, we do all the lifting. {RATING}★ on Google."
    elif p["kind"] == "city":
        c = p["place"]
        t = _fit([f"Junk Removal {c}, MN | Same-Day from $199 | Wood’s Waste", f"Junk Removal {c}, MN | From $199 | Wood’s Waste",
                  f"Junk Removal {c}, MN | Same-Day from $199", f"Junk Removal {c}, MN | From $199"], 60)
        d = _fit([f"Same-day junk removal in {c}, MN from $199. Furniture, appliances, garage & estate cleanouts. We do all the lifting. {RATING}★ on Google. Text a photo.",
                  f"Same-day junk removal in {c}, MN from $199. Furniture, appliances & cleanouts. We do all the lifting. {RATING}★ on Google. Text a photo.",
                  f"Same-day junk removal in {c}, MN from $199. We do all the lifting. {RATING}★ on Google. Text a photo for a price."], 155)
    else:
        short = html.unescape(p.get("short") or OLD_SHORT.get(slug) or SVC[slug]["name"])
        sent = html.unescape(SVC[slug]["name"])
        t = _fit([f"{short} Twin Cities, MN | From $199 | Wood’s Waste", f"{short} Twin Cities | From $199 | Wood’s Waste",
                  f"{short} MN | From $199 | Wood’s Waste", f"{short} MN | Wood’s Waste"], 60)
        what = SVC_DESC.get(slug, "")
        d = _fit([f"{sent} across the south metro from $199. {what} Same-day pickup, we do all the lifting. {RATING}★ on Google.",
                  f"{sent} across the south metro from $199. {what} Same-day, we do the lifting.",
                  f"{sent} across the south metro from $199. Same-day pickup, we do all the lifting. {RATING}★ on Google."], 155)
    return t, d


OLD_SHORT = {"furniture-removal": "Furniture Removal", "appliance-removal": "Appliance Removal", "garage-cleanout": "Garage Cleanout",
             "yard-waste-removal": "Yard Waste Removal", "construction-debris-removal": "Construction Debris Removal"}
SVC_DESC = {"furniture-removal": "Couches, mattresses, dressers & more.", "appliance-removal": "Fridges, washers, dryers & more.",
            "garage-cleanout": "Whole garages cleared, floor swept.", "yard-waste-removal": "Brush, branches, playsets & trampolines.",
            "construction-debris-removal": "Drywall, lumber, flooring & tile.", "estate-cleanout": "Whole homes cleared, usable items donated.",
            "basement-cleanout": "We carry it all up the stairs.", "move-out-cleanout": "Rental turnovers & leftover stuff.",
            "mattress-removal": "Mattresses, box springs & frames.", "hot-tub-removal": "Cut up, hauled off, cleaned up.",
            "commercial-junk-removal": "Office furniture, fixtures & pallets."}


def apply_seo(slug, p):
    t, d = seo(slug, p)
    p["title"] = t
    og = t.replace(" | Wood’s Waste", "") + " | Wood’s Waste" if "Wood’s Waste" not in t else t
    keep = [m for m in p["metas"] if not re.search(r'name="description"|property="og:(title|description)"|name="twitter:(title|description)"', m)]
    p["metas"] = [f'<meta name="description" content="{esc(d)}">'] + keep + [
        f'<meta property="og:title" content="{esc(og)}">', f'<meta property="og:description" content="{esc(d)}">',
        f'<meta name="twitter:title" content="{esc(og)}">', f'<meta name="twitter:description" content="{esc(d)}">']
    p["metas"] = [m for m in p["metas"] if 'name="theme-color"' not in m] + ['<meta name="theme-color" content="#ffffff">']


def head(p, slug):
    metas = "\n".join(p["metas"])
    lds = [d for d in p["ld"]]
    for d in lds:
        if isinstance(d, dict) and isinstance(d.get("aggregateRating"), dict):
            d["aggregateRating"].update(ratingValue=RATING, reviewCount=NREV)
    lds.append({"@context": "https://schema.org", "@type": "FAQPage",
                "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in p["faq_final"]]})
    ld = "\n".join(f'<script type="application/ld+json">{json.dumps(d, ensure_ascii=False)}</script>' for d in lds)
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(p["title"])}</title>
{metas}
<link rel="icon" href="/favicon.ico">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@700;800&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/site.css?v={CSS_V}">
{ld}
</head>
<body>'''


def topbar(local=True):
    a = "" if local else "/"
    return f'''
<header class="top" id="nav">
  <div class="wrap">
    <a href="/" class="brand" aria-label="Wood's Waste home"><img src="/logo.PNG" alt="Wood's Waste" width="141" height="30"></a>
    <nav class="nav-links" id="navLinks">
      <a href="/#services">Services</a><a href="/#work">Our work</a><a href="#pricing">Pricing</a><a href="#reviews">Reviews</a><a href="#areas">Areas</a><a href="#faq">FAQ</a>
    </nav>
    <div class="top-cta"><a class="top-phone" href="{TEL}">{PHONE}</a><a class="btn btn-green" href="#quote">Free quote</a></div>
    <button class="ham" id="hamburger" aria-label="Menu"><span></span><span></span><span></span></button>
  </div>
</header>
<main id="top">'''


def hero(eyebrow, h1_html, lede, pair="yard"):
    k = PAIRS[pair][0]
    return f'''
<section class="hero">
  <div class="wrap">
    <div>
      <span class="eyebrow">{eyebrow}</span>
      <h1>{h1_html}</h1>
      <p class="lede">{lede}</p>
      <div class="hero-ctas"><a class="btn btn-green" href="#quote">Get a free quote {ARROW}</a><a class="btn btn-line sms-link" href="{SMS}">{BUBBLE}Text a photo</a></div>
      <div class="trust"><span><span class="stars">★★★★★</span> 5.0 on Google</span><span>{CHECK.replace('2.6','2.4')}Same-day available</span><span>{CHECK.replace('2.6','2.4')}Owner-operated</span></div>
    </div>
    <div class="hero-photos" aria-label="A real job: before and after">
      <figure class="ph-a"><img src="/img/jobs/{k}-before.jpg" alt="{PAIRS[pair][3]}" fetchpriority="high"><span class="tag">Before</span></figure>
      <figure class="ph-b"><img src="/img/jobs/{k}-after.jpg" alt="{PAIRS[pair][4]}"><span class="tag after">After</span></figure>
      <div class="price-badge"><small>Starting at</small><b>$199</b><small>no hidden fees</small></div>
    </div>
  </div>
</section>'''


STRIP = '''
<section class="strip"><div class="wrap">
  <div><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg><p><b>Same-day</b><span>pickup available</span></p></div>
  <div><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3l2.7 5.6 6.1.9-4.4 4.3 1 6.1L12 17l-5.4 2.9 1-6.1L3.2 9.5l6.1-.9z"/></svg><p><b>5.0 stars</b><span>13 Google reviews</span></p></div>
  <div><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M7 19h10M12 5v14M5 9l7-6 7 6"/></svg><p><b>We do the lifting</b><span>any room, any floor</span></p></div>
  <div><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 12a8 8 0 0 1 13.7-5.6L20 9M20 4v5h-5M20 12a8 8 0 0 1-13.7 5.6L4 15M4 20v-5h5"/></svg><p><b>Donate &amp; recycle</b><span>whatever we can</span></p></div>
</div></section>'''


def services(title, lede, skip=None):
    cards = []
    for slug, t, d, ic in SERVICES:
        if slug == skip:
            continue
        cards.append(f'<a class="svc reveal" href="/{slug}"><div class="ic"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{ic}</svg></div><h3>{t}</h3><p>{d}</p><span class="more">Learn more →</span></a>')
    h, t, d, ic = ESTATE
    cards.append(f'<a class="svc reveal" href="{h}"><div class="ic"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{ic}</svg></div><h3>{t}</h3><p>{d}</p><span class="more">Learn more →</span></a>')
    more = "".join(f'<a href="/{k}">{n}</a>' for k, n, _, _ in MORE_SERVICES if k not in (skip, "estate-cleanout"))
    return f'''
<section class="sec" id="services">
  <div class="wrap">
    <div class="sec-head reveal"><span class="eyebrow">What we haul</span><h2>{title}</h2><p class="lede">{lede}</p></div>
    <div class="svc-grid">{"".join(cards)}</div>
    <div class="areas svc-more reveal"><span>Also:</span>{more}</div>
  </div>
</section>'''


def work(pairs):
    cards = []
    for p in pairs:
        k, cap, sub, ab, aa = PAIRS[p]
        cards.append(f'''<div class="ba reveal"><div class="ba-pair">
        <figure><img loading="lazy" src="/img/jobs/{k}-before.jpg" alt="{ab}"><span class="tag">Before</span></figure>
        <figure><img loading="lazy" src="/img/jobs/{k}-after.jpg" alt="{aa}"><span class="tag after">After</span></figure>
      </div><div class="ba-cap">{cap} <span>{sub}</span></div></div>''')
    return f'''
<section class="sec sec-sand" id="work">
  <div class="wrap">
    <div class="sec-head reveal"><span class="eyebrow">Real jobs</span><h2>Before &amp; after</h2><p class="lede">No stock photos. These are jobs we did, start to finish.</p></div>
    <div class="ba-grid">{"".join(cards)}</div>
  </div>
</section>'''


def pricing(extra=""):
    cards = "".join(f'<div class="tier reveal">{truck(f)}<div class="tier-name">{n}</div><div class="tier-yd">{yd}</div><p>{ex}</p><div class="tier-price"><small>from*</small>{pr}</div></div>'
                    for f, n, yd, ex, pr in TIERS)
    extra_html = f" {extra}" if extra else ""
    return f'''
<section class="sec sec-sand" id="pricing">
  <div class="wrap">
    <div class="sec-head center reveal"><span class="eyebrow">Simple pricing</span><h2>Pay only for the space your stuff takes</h2>
      <p class="lede center">Loading, haul-away and disposal are all included. Text a photo and we’ll tell you exactly where you land before we come out.</p></div>
    <div class="tiers">{cards}</div>
    <p class="tier-note reveal"><b>Prices are starting points.</b> Your total can be higher if your load includes items the dump charges extra for: mattresses and box springs, appliances with Freon (fridges, freezers, AC units), tires, and TVs and electronics.{extra_html} We’ll always give you the full price before we start. {NO_HAZ}</p>
    <div class="tier-foot reveal">
      <ul><li>{CHECK}Price set before we start, no surprises</li><li>{CHECK}Bigger than a full load? Quoted by volume</li></ul>
      <div class="hero-ctas"><a class="btn btn-green" href="#quote">Get my exact price</a><a class="btn btn-line sms-link" href="{SMS}">Text a photo</a></div>
    </div>
  </div>
</section>'''


STEPS = '''
<section class="sec" id="how">
  <div class="wrap">
    <div class="sec-head center reveal"><span class="eyebrow">How it works</span><h2>Three steps to a clean space</h2></div>
    <div class="steps">
      <div class="step reveal"><div class="n">1</div><h3>Text us a photo</h3><p>Or fill out the quick form. Tell us what’s going and where you are.</p></div>
      <div class="step reveal"><div class="n">2</div><h3>Get a price</h3><p>We text you an upfront price, usually the same day. No obligation.</p></div>
      <div class="step reveal"><div class="n">3</div><h3>We haul it all</h3><p>We show up on time, do all the lifting, and sweep up before we leave.</p></div>
    </div>
  </div>
</section>'''


def reviews(slug, n=3):
    photo = [r for r in REVIEWS if r["photo"]]
    k = int(hashlib.md5(slug.encode()).hexdigest(), 16)
    pick = [photo[(k + i) % len(photo)] for i in range(min(n, len(photo)))] if photo else []
    rest = [r for r in REVIEWS if r not in pick]
    pick += rest[k % max(1, len(rest)):][: n - len(pick)] or rest[: n - len(pick)]
    cards = "".join(rev_card(r) for r in pick[:n])
    return f'''
<section class="sec" id="reviews">
  <div class="wrap">
    <div class="rev-top reveal"><div><span class="eyebrow">Reviews</span><h2 style="margin-top:12px">Neighbors love the results</h2></div>
      <div class="rev-score"><b>5.0</b><div><span class="stars">★★★★★</span><small>13 reviews on Google</small></div></div></div>
    <div class="rev-grid">{cards}</div>
    <p style="margin-top:26px" class="reveal"><a class="btn btn-line" href="{GOOGLE}" target="_blank" rel="noopener">Read all reviews on Google →</a></p>
  </div>
</section>'''


def faq(title, items):
    det = "".join(f"<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>" for q, a in items)
    return f'''
<section class="sec" id="faq">
  <div class="wrap">
    <div class="sec-head center reveal"><span class="eyebrow">FAQ</span><h2>{title}</h2></div>
    <div class="faq">{det}</div>
  </div>
</section>'''


ALL_AREAS = [("farmington", "Farmington", 1), ("lakeville", "Lakeville", 1), ("apple-valley", "Apple Valley", 1), ("burnsville", "Burnsville", 1),
             ("rosemount", "Rosemount", 1), ("eagan", "Eagan", 1), ("hastings", "Hastings", 0), ("prior-lake", "Prior Lake", 0), ("savage", "Savage", 0),
             ("inver-grove-heights", "Inver Grove Heights", 0), ("northfield", "Northfield", 0), ("cottage-grove", "Cottage Grove", 0), ("woodbury", "Woodbury", 0),
             ("bloomington", "Bloomington", 0), ("richfield", "Richfield", 0), ("edina", "Edina", 0), ("eden-prairie", "Eden Prairie", 0), ("shakopee", "Shakopee", 0),
             ("south-st-paul", "South St. Paul", 0), ("west-st-paul", "West St. Paul", 0), ("mendota-heights", "Mendota Heights", 0), ("newport", "Newport", 0),
             ("st-paul", "St. Paul", 0), ("minneapolis", "Minneapolis", 0), ("minnetonka", "Minnetonka", 0), ("chanhassen", "Chanhassen", 0), ("chaska", "Chaska", 0),
             ("victoria", "Victoria", 0), ("waconia", "Waconia", 0), ("plymouth", "Plymouth", 0), ("maple-grove", "Maple Grove", 0), ("brooklyn-park", "Brooklyn Park", 0),
             ("coon-rapids", "Coon Rapids", 0), ("blaine", "Blaine", 0), ("fridley", "Fridley", 0), ("maplewood", "Maplewood", 0)]


def areas(title, lede, chips):
    a = "".join('<a%s href="/%s">%s</a>' % (' class="core"' if core else "", s, n) for s, n, core in chips)
    return f'''
<section class="sec" id="areas">
  <div class="wrap">
    <div class="sec-head reveal"><span class="eyebrow">Service area</span><h2>{title}</h2><p class="lede">{lede}</p></div>
    <div class="areas reveal">{a}</div>
  </div>
</section>'''


def quote(where=""):
    return f'''
<section class="sec sec-sand" id="quote">
  <div class="wrap quote">
    <div class="quote-side reveal">
      <span class="eyebrow">Free quote</span>
      <h2 style="margin-top:12px">Get your price today</h2>
      <p class="lede" style="margin-top:14px">Tell us what needs to go{where} and add a photo if you can. We’ll text you a price, usually the same day.</p>
      <ul><li>{CHECK}No obligation, no pressure</li><li>{CHECK}Starting at $199, price set before we start</li><li>{CHECK}Same-day pickup often available</li></ul>
      <div class="alt"><b>Faster by text?</b><p>Snap a few photos and send them straight to Griffin.</p>
        <div class="row"><a class="btn btn-green sms-link" href="{SMS}">Text {PHONE}</a><a class="btn btn-line" href="{TEL}">Call</a></div></div>
    </div>
    <div class="form-card reveal">
      <form id="bookingForm" class="quote-form">
        <div class="row2">
          <div class="field"><label for="bName">Full name</label><input class="input" type="text" id="bName" required autocomplete="name" placeholder="Jane Smith"></div>
          <div class="field"><label for="bPhone">Phone number</label><input class="input" type="tel" id="bPhone" required autocomplete="tel" placeholder="(507) 555-0100"></div>
        </div>
        <div class="field"><label for="bAddress">Address</label><input class="input" type="text" id="bAddress" required autocomplete="street-address" placeholder="123 Main St, Farmington, MN"></div>
        <div class="field"><label for="bItems">What needs to be removed?</label><textarea class="input" id="bItems" required rows="3" placeholder="e.g. couch, 2 mattresses, garage cleanout..."></textarea></div>
        <div class="field"><label for="bWhen">When are you looking to get this done?</label><select class="input" id="bWhen" required><option value="">Choose one...</option><option>As soon as possible</option><option>This week</option><option>Next week</option><option>In the next month</option><option>Not sure yet, just want a price</option></select></div>
        <div class="field">
          <div class="field-head"><label>Photos</label><span class="opt">Optional, but gets you a faster price</span></div>
          <div class="drop" id="dropZone" onclick="document.getElementById('fileInput').click()" ondragover="event.preventDefault();this.classList.add('over')" ondragleave="this.classList.remove('over')" ondrop="event.preventDefault();this.classList.remove('over');handleFiles(event.dataTransfer.files)">
            <div class="drop-ic">＋</div><p>Tap to add photos</p><p class="drop-sub">JPG, PNG or HEIC · up to 10</p>
          </div>
          <input type="file" id="fileInput" multiple accept="image/*,.pdf,.heic,.heif" hidden onchange="handleFiles(this.files)">
          <div class="file-list" id="fileList"></div>
        </div>
        <button type="submit" class="btn btn-green btn-block" id="submitBtn">Get my free quote →</button>
        <div class="form-status" id="formStatus"></div>
        <p class="fine">We’ll only use your number to text you about this quote.</p>
      </form>
    </div>
  </div>
</section>'''


def band(sub="Text a photo now and get a price today."):
    return f'''
<section class="sec" style="padding-top:0">
  <div class="wrap"><div class="band reveal">
    <div><h2>Ready to get your space back?</h2><p>{sub}</p></div>
    <div class="hero-ctas"><a class="btn btn-ink sms-link" href="{SMS}">Text a photo</a><a class="btn btn-line" href="{TEL}">Call {PHONE}</a></div>
  </div></div>
</section>
</main>'''


FOOT_SVC = ('<div><h4>Services</h4><a href="/garage-cleanout">Garage cleanouts</a><a href="/estate-cleanout">Estate cleanouts</a>'
            '<a href="/basement-cleanout">Basement cleanouts</a><a href="/furniture-removal">Furniture removal</a><a href="/appliance-removal">Appliance removal</a>'
            '<a href="/mattress-removal">Mattress removal</a><a href="/hot-tub-removal">Hot tub removal</a><a href="/move-out-cleanout">Move-out cleanouts</a>'
            '<a href="/commercial-junk-removal">Office &amp; commercial</a><a href="/yard-waste-removal">Yard waste</a><a href="/construction-debris-removal">Construction debris</a></div>')
FOOT = f'''
<footer class="foot">
  <div class="wrap">
    <div class="foot-grid">
      <div><img class="foot-logo" src="/logo.PNG" alt="Wood's Waste"><p>Local, owner-operated junk removal out of Farmington, MN. Same-day pickup across the south metro.</p></div>
      FOOT_SVC_SLOT
      <div><h4>Top areas</h4><a href="/farmington">Farmington</a><a href="/lakeville">Lakeville</a><a href="/apple-valley">Apple Valley</a><a href="/burnsville">Burnsville</a><a href="/#areas">All areas</a></div>
      <div><h4>Contact</h4><a href="{TEL}">{PHONE}</a><a class="sms-link" href="{SMS}">Text us a photo</a><a href="#quote">Free quote form</a><a href="{GOOGLE}" target="_blank" rel="noopener">Google reviews</a></div>
    </div>
    <div class="foot-bottom"><span>© <span id="year">2026</span> Wood’s Waste · Farmington, MN</span><span><a href="/realtors" style="color:inherit">For realtors &amp; property managers</a> · <a href="/pro" style="color:inherit">For junk-removal operators</a></span></div>
  </div>
</footer>
<script src="/script.js"></script>
<script>
  (function () {{
    var ios = /iPad|iPhone|iPod/.test(navigator.userAgent);
    var href = 'sms:+15072981179' + (ios ? '&' : '?') + 'body=' + encodeURIComponent('Hi! Junk removal quote, photos attached:');
    document.querySelectorAll('.sms-link').forEach(function (a) {{ a.href = href; }});
  }})();
</script>
</body>
</html>
'''


def fix_faq(slug, p, city=None):
    out = []
    for q, a in p["faq"]:
        ql = q.lower()
        if ("cost" in ql or "price" in ql) and p["kind"] == "city":
            a = f"Our minimum pickup in {city} is $199 for a single item or small load. Bigger jobs are priced by how much truck space your load takes. {TIER_GUIDE} {FEE_NOTE}"
        elif ("cost" in ql or "price" in ql) and p["kind"] == "service":
            a = re.sub(r"\s*Call or text( us)?( \(507\) 298-1179)? for a (fast|quick) estimate\.?", "", a).strip()
            a = f"{a} {TIER_GUIDE} {FEE_NOTE}"
        elif q.startswith("What items do you take"):
            a = f"Almost everything: furniture, appliances, mattresses, electronics, construction debris, yard waste, garage contents and general clutter. {NO_HAZ}"
        a = a.replace("appliances, paint cans, scrap wood", "appliances, scrap wood")
        out.append((q, a))
    return out


COUNTY = {**{c: "Dakota" for c in ("farmington", "lakeville", "apple-valley", "burnsville", "rosemount", "eagan", "hastings", "inver-grove-heights",
                                     "south-st-paul", "west-st-paul", "mendota-heights")},
          **{c: "Scott" for c in ("prior-lake", "savage", "shakopee")},
          **{c: "Hennepin" for c in ("bloomington", "richfield", "edina", "eden-prairie", "minneapolis", "minnetonka", "plymouth", "maple-grove", "brooklyn-park")},
          **{c: "Carver" for c in ("chanhassen", "chaska", "victoria", "waconia")},
          **{c: "Washington" for c in ("woodbury", "cottage-grove", "newport")},
          **{c: "Ramsey" for c in ("st-paul", "maplewood")},
          **{c: "Anoka" for c in ("coon-rapids", "blaine", "fridley")}, "northfield": "Rice"}
HOME_LL = (44.6403, -93.1438)


def miles_from_home(p):
    import math
    m = next((re.search(r'content="([-\d.]+);([-\d.]+)"', x) for x in p["metas"] if "geo.position" in x), None)
    if not m:
        return None
    la, lo = float(m.group(1)), float(m.group(2))
    r = 3958.8; f1, f2 = math.radians(HOME_LL[0]), math.radians(la)
    dl, dn = math.radians(la - HOME_LL[0]), math.radians(lo - HOME_LL[1])
    a = math.sin(dl / 2) ** 2 + math.cos(f1) * math.cos(f2) * math.sin(dn / 2) ** 2
    return round(2 * r * math.asin(math.sqrt(a)))


POPULAR = [("garage-cleanout", "Garage cleanouts", "Clear the garage in an afternoon"), ("furniture-removal", "Furniture removal", "Couches, beds, dressers and more"),
           ("estate-cleanout", "Estate cleanouts", "Whole homes, handled with care"), ("basement-cleanout", "Basement cleanouts", "We carry it up the stairs"),
           ("appliance-removal", "Appliance removal", "Fridges, washers and dryers"), ("move-out-cleanout", "Move-out cleanouts", "Rentals ready to turn over"),
           ("mattress-removal", "Mattress removal", "From any room, any floor"), ("hot-tub-removal", "Hot tub removal", "Cut up and hauled off"),
           ("yard-waste-removal", "Yard waste removal", "Brush, playsets, trampolines"), ("construction-debris-removal", "Construction debris", "Remodel leftovers gone"),
           ("commercial-junk-removal", "Office &amp; commercial", "Offices, retail and back lots")]


def city_extras(slug, p, city):
    county = COUNTY.get(slug)
    mi = miles_from_home(p)
    dist = ("Farmington is our home base, so we’re usually minutes away." if slug == "farmington"
            else f"{city} is about {mi} miles from our home base in Farmington, so we’re in the area most weeks." if mi else "")
    cards = "".join(f'<a class="pop reveal" href="/{k}"><b>{n} in {esc(city)}</b><span>{d}</span></a>' for k, n, d in POPULAR)
    facts = [dist,
             f"{city} is in {county} County. We don’t take paint, chemicals or other hazardous waste; {county} County’s household hazardous waste program takes those." if county else "",
             "Same-day and next-day pickups are often available. Text a photo in the morning for the fastest price."]
    facts_html = "".join(f"<li>{CHECK}{esc(x)}</li>" for x in facts if x)
    sec = f'''
<section class="sec sec-sand" id="popular">
  <div class="wrap">
    <div class="sec-head reveal"><span class="eyebrow">Popular in {esc(city)}</span><h2>Junk removal services in {esc(city)}</h2>
      <p class="lede">Every job is priced by truck space, with the full price before we start.</p></div>
    <div class="pop-grid">{cards}</div>
    <div class="local-card reveal" style="margin-top:22px"><h3>Good to know in {esc(city)}</h3><ul>{facts_html}</ul></div>
  </div>
</section>'''
    extra_faq = []
    if mi and slug != "farmington":
        extra_faq.append((f"How far is {city} from Wood’s Waste?", f"About {mi} miles from our home base in Farmington. We serve {city} most weeks, and same-day pickup is often available."))
    extra_faq.append((f"Do you do estate, basement and move-out cleanouts in {city}?",
                      f"Yes. We handle whole-house estate cleanouts, basement cleanouts and rental move-outs in {city}, priced by volume with the full price up front."))
    return sec, extra_faq


def build_city(slug, p):
    city = p["place"] or slug.replace("-", " ").title()
    pop_sec, extra_faq = city_extras(slug, p, city)
    p["faq_final"] = fix_faq(slug, p, city) + extra_faq
    intro, why = p["intro"], p["why"]
    paras = "".join(f"<p>{esc(x)}</p>" for x in intro["paras"])
    why_p = "".join(f"<p>{esc(x)}</p>" for x in (why or {}).get("paras", []))
    local = f'''
<section class="sec" id="local">
  <div class="wrap about">
    <div class="reveal"><span class="eyebrow">{esc(city)}, MN</span><h2 style="margin-top:12px">{esc(intro["h2"])}</h2>{paras}</div>
    <div class="local-card reveal"><h3>Why {esc(city)} chooses us</h3>{why_p}
      <ul><li>{CHECK}Owner-operated out of Farmington</li><li>{CHECK}Upfront price before we start</li><li>{CHECK}We donate &amp; recycle what we can</li></ul>
      <a class="btn btn-green" href="#quote">Get a free quote</a></div>
  </div>
</section>'''
    near = [(h.strip("/").replace(".html", ""), n, 0) for n, h in p["nearby"]]
    near.append(("#areas-all", "", 0))
    near = [x for x in near if x[1]]
    chips = "".join(f'<a href="/{s}">{n}</a>' for s, n, _ in near) + '<a class="core" href="/#areas">All service areas →</a>'
    near_html = f'''
<section class="sec" id="areas">
  <div class="wrap">
    <div class="sec-head reveal"><span class="eyebrow">Service area</span><h2>Also serving towns near {esc(city)}</h2><p class="lede">Based in Farmington and out across the south metro every week.</p></div>
    <div class="areas reveal">{chips}</div>
  </div>
</section>'''
    h1 = f"Junk removal in {esc(city)}, MN.<br><em>Gone today.</em>"
    lede = f"Local, owner-run junk removal for {esc(city)}. Furniture, appliances, garages and full cleanouts, usually the same day. We do all the lifting. Text a photo, get a price."
    return (head(p, slug) + topbar() + hero(f"Serving {esc(city)} · Same-day", h1, lede, "yard") + STRIP + local
            + pop_sec
            + work(["garage", "curb"]) + pricing() + STEPS + reviews(slug)
            + faq(f"Junk removal in {esc(city)}: common questions", p["faq_final"]) + near_html + quote(f" in {esc(city)}")
            + band(f"Serving {esc(city)} and the south metro. Text a photo and get a price today.") + FOOT)


AREA_NAMES = [n for _, n, _ in ALL_AREAS] if "ALL_AREAS" in globals() else []


def service_ld(slug, p):
    s = SVC[slug]
    nm = html.unescape(p.get("short") or s["name"])
    areas_ = [{"@type": "City", "name": n} for _, n, _ in ALL_AREAS]
    return {"@context": "https://schema.org", "@type": "Service", "name": nm, "serviceType": nm,
            "provider": {"@type": "LocalBusiness", "@id": "https://woodswastemn.com/#business", "name": "Wood’s Waste", "telephone": "+1-507-298-1179"},
            "areaServed": areas_, "url": f"https://woodswastemn.com/{slug}",
            "description": seo(slug, p)[1],
            "offers": {"@type": "AggregateOffer", "priceCurrency": "USD", "lowPrice": "199", "highPrice": "779", "offerCount": "5"}}


def new_service_content(slug):
    n = NEW[slug]
    base = C["garage-cleanout"]
    lb = json.loads(json.dumps(base["ld"][0])); lb["url"] = f"https://woodswastemn.com/{slug}"
    lb["description"] = f"{html.unescape(n['short'])} across the Twin Cities south metro. Same-day, owner-operated by Griffin and Gavin out of Farmington, MN."
    crumbs = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://woodswastemn.com/"},
        {"@type": "ListItem", "position": 2, "name": html.unescape(n["short"]), "item": f"https://woodswastemn.com/{slug}"}]}
    metas = [m.replace("garage-cleanout", slug) for m in base["metas"] if 'name="keywords"' not in m]
    kw = html.unescape(n["short"]).lower()
    metas.insert(0, f'<meta name="keywords" content="{kw} MN, {kw} Twin Cities, {kw} Lakeville, {kw} Apple Valley, {kw} Farmington, same day {kw}">')
    return {"kind": "service", "title": "", "metas": metas, "ld": [lb, {"@type": "Service"}, crumbs], "h1": html.unescape(n["h1"]),
            "faq": [tuple(x) for x in n["faq"]], "intro": {"h2": n["intro_h2"], "eyebrow": "", "paras": n["intro"]}, "why": None,
            "nearby": [], "place": "Farmington", "short": n["short"]}


def build_service(slug, p):
    s = SVC[slug]
    p["ld"] = [service_ld(slug, p) if (isinstance(d, dict) and d.get("@type") == "Service") else d for d in p["ld"]]
    p["faq_final"] = fix_faq(slug, p)
    intro = p["intro"]
    paras = "".join(f"<p>{esc(x)}</p>" for x in intro["paras"])
    items = "".join(f'<li>{CHECK}{i.replace("*", "")}{"<sup>*</sup>" if i.endswith("*") else ""}</li>' for i in s["items"])
    has_fee = any(i.endswith("*") for i in s["items"])
    take = f'''
<section class="sec" id="local">
  <div class="wrap about">
    <div class="reveal"><span class="eyebrow">{s["name"]}</span><h2 style="margin-top:12px">{esc(intro["h2"])}</h2>{paras}</div>
    <div class="local-card reveal"><h3>What we take</h3>
      <ul class="take">{items}</ul>
      <p class="take-note">{"<sup>*</sup>Extra disposal fee, included in your quote. " if has_fee else ""}{NO_HAZ}</p>
      <a class="btn btn-green" href="#quote">Get a free quote</a></div>
  </div>
</section>'''
    h1 = esc(p["h1"].rstrip(".")) + ".<br><em>Gone today.</em>"
    lede = f"{s['name']} across Farmington, Lakeville, Apple Valley and the south metro. We do all the lifting, usually the same day. Text a photo, get a price."
    return (head(p, slug) + topbar() + hero(f"{s['name']} · South Metro MN", h1, lede, s["pair"]) + STRIP + take
            + work([s["pair"]] + [x for x in ("garage", "curb", "lot", "yard") if x != s["pair"]][:1]) + pricing(s.get("heavy", ""))
            + STEPS + reviews(slug)
            + faq(f"{s['name']}: common questions", p["faq_final"])
            + services("We haul everything else too", "One call covers the whole job.", skip=slug)
            + areas("Serving the south metro &amp; beyond", "Home base is Farmington. We’re in these towns every week.", ALL_AREAS)
            + quote() + band() + FOOT)


def build_home(p):
    src = open(os.path.join(ROOT, "_build", "home.html")).read()
    lb = p["ld"][0]
    lb["hasOfferCatalog"] = {"@type": "OfferCatalog", "name": "Junk removal by load size", "itemListElement": [
        {"@type": "Offer", "name": f"{n} ({yd})", "price": pr.strip("$"), "priceCurrency": "USD",
         "itemOffered": {"@type": "Service", "name": f"Junk removal, {n.lower()}"}} for _, n, yd, _, pr in TIERS]}
    body = src[src.index("<body>") + len("<body>"):]
    body = body.replace('="../', '="/').replace("href=\"../", "href=\"/")
    body = re.sub(r'href="/([a-z-]+)\.html"', r'href="/\1"', body)
    body = body.replace('<span>Same-day junk removal · (507) 298-1179</span>', '<span><a href="/realtors" style="color:inherit">For realtors &amp; property managers</a> · <a href="/pro" style="color:inherit">For junk-removal operators</a></span>')
    body = body.replace('<a class="svc reveal" href="#quote">', '<a class="svc reveal" href="/estate-cleanout">').replace('<span class="more">Get a quote →</span>', '<span class="more">Learn more →</span>')
    more = "".join(f'<a href="/{k}">{n}</a>' for k, n, _, _ in MORE_SERVICES if k != "estate-cleanout")
    body = body.replace('</div>\n  </div>\n</section>\n\n<section class="sec sec-sand" id="work">',
                        f'</div>\n    <div class="areas svc-more reveal"><span>Also:</span>{more}</div>\n  </div>\n</section>\n\n<section class="sec sec-sand" id="work">', 1)
    body = re.sub(r'<div><h4>Services</h4>.*?</div>', FOOT_SVC, body, count=1, flags=re.S)
    body = re.sub(r'<div class="rev-grid">.*?</div>\s*<p style="margin-top:26px"', '<div class="rev-grid">' + "".join(rev_card(r) for r in REVIEWS[:6]) + '</div>\n    <p style="margin-top:26px"', body, count=1, flags=re.S)
    faq_items = [(html.unescape(re.sub(r"<[^>]+>", "", q)), html.unescape(re.sub(r"<[^>]+>", "", a)))
                 for q, a in re.findall(r"<details><summary>(.*?)</summary><p>(.*?)</p></details>", body, re.S)]
    p["faq_final"] = faq_items
    return head(p, "index") + body


PARTNER_FAQ = [
    ("How does the 10% agent discount work?", "When you or your client texts us photos, mention you’re an agent (or have them mention your name). 10% comes off any whole-house cleanout for your clients."),
    ("Who pays, me or my client?", "Whoever you prefer. Tell us who’s paying and we’ll send the receipt there."),
    ("Does someone need to be at the property?", "No. A lockbox or door code works. We text you before and after photos when the job is done."),
    ("How fast can you get there?", "Listings and turnovers jump our schedule. We’re usually out within 2 days, often sooner."),
    ("Do you offer a rate for regular turnovers?", "Yes. Property managers with regular turnovers get a flat per-unit rate, so you’re not getting a new quote every time."),
    ("Is there anything you can’t take?", "We don’t take paint, chemicals or other hazardous waste. Everything else in a typical house or unit, we haul."),
]


def partner_content():
    base = C["garage-cleanout"]
    lb = json.loads(json.dumps(base["ld"][0])); lb["url"] = "https://woodswastemn.com/realtors"
    lb["description"] = "Junk removal partner for south metro realtors and property managers: whole-house cleanouts, rental turnovers, priority scheduling and before/after photos."
    crumbs = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://woodswastemn.com/"},
        {"@type": "ListItem", "position": 2, "name": "Realtors & property managers", "item": "https://woodswastemn.com/realtors"}]}
    svc = {"@context": "https://schema.org", "@type": "Service", "name": "Junk removal for realtors and property managers", "serviceType": "Junk removal",
           "provider": {"@type": "LocalBusiness", "@id": "https://woodswastemn.com/#business", "name": "Wood’s Waste", "telephone": "+1-507-298-1179"},
           "areaServed": [{"@type": "City", "name": n} for _, n, _ in ALL_AREAS], "url": "https://woodswastemn.com/realtors",
           "audience": {"@type": "BusinessAudience", "audienceType": "Real estate agents and property managers"},
           "offers": {"@type": "AggregateOffer", "priceCurrency": "USD", "lowPrice": "199", "highPrice": "779", "offerCount": "5"}}
    metas = [m.replace("garage-cleanout", "realtors") for m in base["metas"] if 'name="keywords"' not in m]
    metas.insert(0, '<meta name="keywords" content="junk removal for realtors, estate cleanout realtor MN, rental turnover junk removal, property manager junk removal Twin Cities, pre-listing cleanout Lakeville">')
    return {"kind": "partner", "title": "", "metas": metas, "ld": [lb, svc, crumbs], "h1": "", "faq": PARTNER_FAQ,
            "intro": None, "why": None, "nearby": [], "place": "Farmington"}


def build_partner(slug, p):
    p["faq_final"] = list(PARTNER_FAQ)
    agent = ["Listings jump our schedule, usually out within 2 days", "Before &amp; after photos texted to you", "Lockbox is fine, no need to be there",
             "Pre-listing, estate and move-out cleanouts"]
    pm = ["Flat per-unit rate for regular turnovers", "Turnovers get priority, usually within 2 days", "Before &amp; after photos for your records",
          "Evictions, abandoned furniture, dumped items", "A receipt for every job"]
    li = lambda xs: "".join(f"<li>{CHECK}{x}</li>" for x in xs)
    offers = f'''
<section class="sec" id="offers">
  <div class="wrap">
    <div class="sec-head center reveal"><span class="eyebrow">Partner program</span><h2>Built for listings and turnovers</h2>
      <p class="lede center">We’re Griffin and Gavin, brothers who run Wood’s Waste out of Farmington. We get houses and units empty, hauled off and swept, so they’re ready for photos or the next tenant.</p></div>
    <div class="offer-grid">
      <div class="offer reveal" id="agents"><span class="offer-who">For real estate agents</span><div class="offer-big">10% off</div>
        <p class="offer-what">any whole-house cleanout for your clients</p><p class="offer-sub">On a typical house that’s $300 to $500 back in your seller’s pocket.</p>
        <ul>{li(agent)}</ul><a class="btn btn-green sms-link" href="{SMS}">Text Griffin photos</a></div>
      <div class="offer reveal" id="pm"><span class="offer-who">For property managers</span><div class="offer-big">10% off</div>
        <p class="offer-what">your first unit cleanout</p><p class="offer-sub">Got regular turnovers? We’ll set a flat per-unit rate so you’re not getting a new quote every time.</p>
        <ul>{li(pm)}</ul><a class="btn btn-green sms-link" href="{SMS}">Text Griffin photos</a></div>
    </div>
  </div>
</section>'''
    steps = '''
<section class="sec" id="how">
  <div class="wrap">
    <div class="sec-head center reveal"><span class="eyebrow">How it works</span><h2>Three texts and the house is empty</h2></div>
    <div class="steps">
      <div class="step reveal"><div class="n">1</div><h3>Text photos + address</h3><p>Add the lockbox or door code and your deadline.</p></div>
      <div class="step reveal"><div class="n">2</div><h3>Get a firm price</h3><p>Usually the same day, so you can pass it to your client or owner.</p></div>
      <div class="step reveal"><div class="n">3</div><h3>We clear it, you get photos</h3><p>Hauled, swept and photographed. Receipt goes to whoever’s paying.</p></div>
    </div>
  </div>
</section>'''
    h1 = "Your listings and turnovers,<br><em>cleared fast.</em>"
    lede = "Junk removal partner for south metro realtors and property managers. Whole-house cleanouts, move-out leftovers and rental turnovers, with priority scheduling and before/after photos."
    return (head(p, slug) + topbar() + hero("For realtors &amp; property managers", h1, lede, "curb") + STRIP + offers
            + work(["curb", "lot"]) + steps + pricing() + reviews(slug)
            + faq("Questions from agents and property managers", p["faq_final"]) + quote() + band("Text a few photos of the listing or unit and get a price today.") + FOOT)


def sitemap(slugs):
    import datetime
    today = datetime.date.today().isoformat()
    def pri(s):
        return "1.0" if s == "index" else ("0.9" if C[s]["kind"] in ("service", "partner") else "0.8")
    urls = "".join(f"  <url>\n    <loc>https://woodswastemn.com/{'' if s == 'index' else s}</loc>\n    <lastmod>{today}</lastmod>\n    <priority>{pri(s)}</priority>\n  </url>\n" for s in slugs)
    open(os.path.join(ROOT, "sitemap.xml"), "w").write(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n')


def main():
    n = 0
    for slug in NEW:
        C[slug] = new_service_content(slug)
    C["realtors"] = partner_content()
    for slug, p in C.items():
        if p["kind"] in ("city", "service", "home", "partner"):
            apply_seo(slug, p)
    built = []
    for slug, p in C.items():
        if p["kind"] == "city":
            out = build_city(slug, p)
        elif p["kind"] == "service":
            out = build_service(slug, p)
        elif p["kind"] == "partner":
            out = build_partner(slug, p)
        elif slug == "index":
            out = build_home(p)
        else:
            continue
        out = out.replace("FOOT_SVC_SLOT", FOOT_SVC)
        for a, b in (("5.0 on Google", f"{RATING} on Google"), ("<b>5.0 stars</b>", f"<b>{RATING} stars</b>"), ("13 Google reviews", f"{NREV} Google reviews"),
                     ("13 reviews on Google", f"{NREV} reviews on Google"), ('<div class="rev-score"><b>5.0</b>', f'<div class="rev-score"><b>{RATING}</b>')):
            out = out.replace(a, b)
        out = out.replace('<svg viewBox="0 0 24 24"', '<svg width="24" height="24" viewBox="0 0 24 24"')        # intrinsic size: never huge, even without CSS
        out = out.replace('<svg class="truck" viewBox="0 0 124 66"', '<svg class="truck" width="150" height="80" viewBox="0 0 124 66"')
        open(os.path.join(ROOT, slug + ".html"), "w").write(out)
        n += 1; built.append(slug)
    sitemap(["index"] + [s for s in built if C[s]["kind"] in ("service", "partner")] + [s for s in built if C[s]["kind"] == "city"])
    print("built", n, "pages + sitemap")


if __name__ == "__main__":
    main()
