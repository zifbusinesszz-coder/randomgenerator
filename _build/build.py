"""Builds every page of woodswastemn.com from _build/content.json + one design (site.css).
  python3 _build/build.py          → rewrites index.html, the 36 city pages and the 5 service pages
Home = the approved /preview/ design (paths made root-relative, SEO head + structured data from the old homepage).
City / service pages = one shared template; each keeps its own title, meta, canonical, structured data, local write-up and FAQ."""
import json, os, re, html, hashlib

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
C = json.load(open(os.path.join(ROOT, "_build", "content.json")))
CSS_V = "20261120e"
PHONE, TEL, SMS = "(507) 298-1179", "tel:5072981179", "sms:+15072981179"
GOOGLE = "https://share.google/2VDupAN3BZz3mM9Ml"
esc = lambda s: html.escape(str(s), quote=True)

CHECK = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6 9 17l-5-5"/></svg>'
ARROW = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'
BUBBLE = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12a8 8 0 0 1-11.6 7.1L4 20l1-4.6A8 8 0 1 1 21 12z"/></svg>'

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
ESTATE = ("/#quote", "Estate &amp; move-out cleanouts", "Whole-house, basement and rental turnovers. We donate what’s usable.",
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
PAIRS = {
    "garage": ("garage", "Garage cleanout", "Same day", "A garage piled high with boxes, a recliner and broken furniture", "The same garage floor, cleared"),
    "curb": ("curb", "Bedroom set &amp; furniture", "Curbside haul", "A bedroom set, loveseat and bed frame on a lawn", "The lawn after everything was hauled away"),
    "lot": ("lot", "Business back-lot cleanup", "Commercial", "Pallets, a cabinet and tabletops behind a business", "The same back lot, cleared"),
    "yard": ("yard", "Yard &amp; trampoline removal", "Residential", "Bookshelves, a play table and a trampoline on a lawn", "The same yard, cleared"),
}
REVIEWS = [
    ("BG", "Bob Gremel", "Big pile of junk in the back yard. They took care of it and cleaned up nicely. Extremely good customer service and honest answers."),
    ("KH", "Kjerstin Hedstrom", "Responsive and timely! All my junk was gone less than 24 hours after contacting them. Great job!"),
    ("MD", "Mary DeHate", "Responded quickly, showed up when they said and cheerfully hauled stuff away. Very positive experience."),
    ("BA", "Bryan Anders", "Helped tremendously and priced very fairly. Very pleasant to work with. I would recommend."),
    ("OL", "Olivia", "Easy to contact and the service was quick, easy and affordable. Definitely recommend!!"),
    ("SP", "Shayla P.", "Had them help clean out my garage. Incredibly fast and nice!"),
]
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


def head(p, slug):
    metas = "\n".join(p["metas"])
    lds = [d for d in p["ld"]]
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
    cards.append(f'<a class="svc reveal" href="{h}"><div class="ic"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{ic}</svg></div><h3>{t}</h3><p>{d}</p><span class="more">Get a quote →</span></a>')
    return f'''
<section class="sec" id="services">
  <div class="wrap">
    <div class="sec-head reveal"><span class="eyebrow">What we haul</span><h2>{title}</h2><p class="lede">{lede}</p></div>
    <div class="svc-grid">{"".join(cards)}</div>
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
    k = int(hashlib.md5(slug.encode()).hexdigest(), 16) % len(REVIEWS)
    pick = [REVIEWS[(k + i * 2) % len(REVIEWS)] for i in range(n)]
    cards = "".join(f'<div class="rev reveal"><span class="stars">★★★★★</span><q>{t}</q><div class="who"><span class="av">{i}</span><div>{nm}<small>Google review</small></div></div></div>' for i, nm, t in pick)
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


FOOT = f'''
<footer class="foot">
  <div class="wrap">
    <div class="foot-grid">
      <div><img class="foot-logo" src="/logo.PNG" alt="Wood's Waste"><p>Local, owner-operated junk removal out of Farmington, MN. Same-day pickup across the south metro.</p></div>
      <div><h4>Services</h4><a href="/furniture-removal">Furniture removal</a><a href="/appliance-removal">Appliance removal</a><a href="/garage-cleanout">Garage cleanouts</a><a href="/yard-waste-removal">Yard waste</a><a href="/construction-debris-removal">Construction debris</a></div>
      <div><h4>Top areas</h4><a href="/farmington">Farmington</a><a href="/lakeville">Lakeville</a><a href="/apple-valley">Apple Valley</a><a href="/burnsville">Burnsville</a><a href="/#areas">All areas</a></div>
      <div><h4>Contact</h4><a href="{TEL}">{PHONE}</a><a class="sms-link" href="{SMS}">Text us a photo</a><a href="#quote">Free quote form</a><a href="{GOOGLE}" target="_blank" rel="noopener">Google reviews</a></div>
    </div>
    <div class="foot-bottom"><span>© <span id="year">2026</span> Wood’s Waste · Farmington, MN</span><span><a href="/pro" style="color:inherit">For junk-removal operators</a></span></div>
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


def build_city(slug, p):
    city = p["place"] or slug.replace("-", " ").title()
    p["faq_final"] = fix_faq(slug, p, city)
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
            + services(f"What we haul in {esc(city)}", "From one couch to a full cleanout. We load, haul, and sweep up after.")
            + work(["garage", "curb"]) + pricing() + STEPS + reviews(slug)
            + faq(f"Junk removal in {esc(city)}: common questions", p["faq_final"]) + near_html + quote(f" in {esc(city)}")
            + band(f"Serving {esc(city)} and the south metro. Text a photo and get a price today.") + FOOT)


def build_service(slug, p):
    s = SVC[slug]
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
    src = open(os.path.join(ROOT, "preview", "index.html")).read()
    body = src[src.index("<body>") + len("<body>"):]
    body = body.replace('="../', '="/').replace("href=\"../", "href=\"/")
    body = re.sub(r'href="/([a-z-]+)\.html"', r'href="/\1"', body)
    body = body.replace('<span>Same-day junk removal · (507) 298-1179</span>', '<span><a href="/pro" style="color:inherit">For junk-removal operators</a></span>')
    faq_items = [(html.unescape(re.sub(r"<[^>]+>", "", q)), html.unescape(re.sub(r"<[^>]+>", "", a)))
                 for q, a in re.findall(r"<details><summary>(.*?)</summary><p>(.*?)</p></details>", body, re.S)]
    p["faq_final"] = faq_items
    return head(p, "index") + body


def main():
    n = 0
    for slug, p in C.items():
        if p["kind"] == "city":
            out = build_city(slug, p)
        elif p["kind"] == "service":
            out = build_service(slug, p)
        elif slug == "index":
            out = build_home(p)
        else:
            continue
        open(os.path.join(ROOT, slug + ".html"), "w").write(out)
        n += 1
    print("built", n, "pages")


if __name__ == "__main__":
    main()
