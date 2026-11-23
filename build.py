import os, json, datetime
import shutil
BASE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(BASE, "dist")
shutil.rmtree(OUT, ignore_errors=True)
for c in ("p", "boys", "girls", "ladies"): os.makedirs(f"{OUT}/{c}")
for d in ("images", "admin"):
    if os.path.isdir(f"{BASE}/{d}"): shutil.copytree(f"{BASE}/{d}", f"{OUT}/{d}")
DOM = os.environ.get("URL", "https://qadmora.pages.dev").rstrip("/")
BP = os.environ.get("BASEPATH", "").rstrip("/")
SET = json.load(open(f"{BASE}/data/settings.json"))
YEAR = datetime.date.today().year

CATS = {
 "boys":  dict(n="Boys",   c="#1d5fc4", l="#d6e4fb", note="Tough, comfy pairs for play and school.", seo="Boys shoes for school, play and every day: sneakers, boots and sandals with cushioned insoles and strong, flexible soles."),
 "girls": dict(n="Girls",  c="#c7246b", l="#fbd5e5", note="Pretty, soft pairs for every day.", seo="Girls shoes that look lovely and feel soft: flats, sneakers and winter boots made for growing feet."),
 "ladies":dict(n="Ladies", c="#8a2b7c", l="#f1d6ec", note="Elegant comfort from morning to night.", seo="Ladies shoes for work, family and everyday walking: sandals, slip-ons and walkers with soft cushioning."),
}
SIZES = {"boys": list(range(28, 36)), "girls": list(range(28, 36)), "ladies": list(range(36, 42))}
PR = []
for p in json.load(open(f"{BASE}/data/products.json"))["products"]:
    p["slug"] = p["sku"].lower(); p["cols"] = p.get("colours") or ["Standard"]; p["season"] = p.get("season") or "All"; PR.append(p)
    assert p["cat"] in CATS, p["sku"]

def shoe(col, lab=""):
    t = f'<text x="50" y="12" text-anchor="middle" font-size="5" fill="{col}" opacity=".8">{lab}</text>' if lab else ""
    return f'<svg viewBox="0 0 100 70" aria-hidden="true">{t}<path d="M6 54c0-12 6-17 15-20l9-9c4-4 10-4 14 0l8 9c12 3 32 7 39 15l1 6c0 3-2 5-5 5H11c-3 0-5-2-5-6z" fill="{col}"/><path d="M6 56h88v6c0 3-2 5-5 5H11c-3 0-5-2-5-5z" fill="#fff" opacity=".95"/><path d="M34 29l8 9M44 26l8 9" stroke="#fff" stroke-width="2.4" stroke-linecap="round" opacity=".8"/></svg>'

def img(p, i, alt, root="../"):
    ims = p.get("images") or []
    if i - 1 < len(ims) and ims[i - 1]:
        return f'<img src="{root}{ims[i - 1].lstrip("/")}" alt="{alt}" loading="lazy" width="800" height="600">'
    return shoe(CATS[p["cat"]]["c"], f"Photo {i} coming soon")

def card(p, root):
    c = CATS[p["cat"]]
    tag = f'<span class="tag">{p["season"]}</span>' if p["season"] != "All" else ""
    return (f'<article class="card" data-season="{p["season"]}"><a class="img" href="{root}p/{p["slug"]}.html" style="background:{c["l"]}" aria-label="{p["name"]}">{tag}{shoe(c["c"])}</a>'
            f'<div class="body"><h3><a href="{root}p/{p["slug"]}.html">{p["name"]}</a></h3><div class="meta">{c["n"]} · {p["sku"]}</div>'
            f'<div class="row"><span class="price">Rs. {p["price"]:,}</span><a class="buy" href="{root}p/{p["slug"]}.html">View</a></div></div></article>')

def chips():
    return ('<div class="chips" id="seasonChips" aria-label="Season"><button class="chip" data-s="all" aria-pressed="true">All seasons</button>'
            '<button class="chip" data-s="Summer" aria-pressed="false">Summer</button><button class="chip" data-s="Winter" aria-pressed="false">Winter</button></div>')

def page(title, desc, body, root="", path="", ld=""):
    ldt = f'<script type="application/ld+json">{json.dumps(ld)}</script>' if ld else ""
    cats = "".join(f'<a href="{root}{k}/">{v["n"]}</a>' for k, v in CATS.items())
    return f'''<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title><meta name="description" content="{desc}">
<meta name="theme-color" content="#1d5fc4"><link rel="icon" href="{root}favicon.svg" type="image/svg+xml">
<meta property="og:type" content="website"><meta property="og:title" content="{title}"><meta property="og:description" content="{desc}"><meta property="og:image" content="{DOM}/og-image.svg"><meta name="twitter:card" content="summary_large_image">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:wght@600;800&family=DM+Sans:wght@400;500;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{root}styles.css">{ldt}</head>
<body><div class="adbar" id="adTop" hidden></div>
<header><div class="wrap nav"><div class="left"><button class="burger" id="burger" aria-label="Open menu" aria-expanded="false" aria-controls="drawer">☰</button><a class="logo" href="{root or './'}">Qadm<i>ora</i></a></div><a class="wa" data-wa="Assalam o Alaikum, I want to order from Qadmora." href="#" rel="noopener" target="_blank">Order on WhatsApp</a></div></header>
<div class="overlay" id="overlay" hidden></div>
<aside class="drawer" id="drawer" aria-label="Menu"><a class="logo" href="{root or './'}">Qadm<i>ora</i></a>{cats}<a href="{root}#shop">All shoes</a><a href="{root}#seasons" id="navSeason">Seasons</a><a href="{root}#about">About</a><a href="{root}#contact">Contact</a><a href="{root}returns.html">Returns</a><a href="{root}delivery.html">Delivery</a></aside>
<main id="top">{body}</main>
<footer><div class="wrap"><div><b>Qadmora</b><br>Comfortable shoes for kids and ladies.<div id="soc"></div></div><div class="fl"><a href="{root}returns.html">Returns and exchange</a><a href="{root}delivery.html">Delivery</a><a href="{root}privacy.html">Privacy</a></div><div class="cp">© {YEAR} Qadmora. All rights reserved.</div></div></footer>
<script src="{root}config.js"></script><script src="{root}app.js"></script></body></html>'''

def write(path, s):
    with open(f"{OUT}/{path}", "w", encoding="utf-8") as f: f.write(s)

# ---------- home ----------
panels = "".join(f'<a class="panel" href="{k}/" style="background:{v["c"]}" aria-label="Shop {v["n"]} shoes"><div><h2>{v["n"]}</h2><small>{v["note"]}</small></div>{shoe(v["l"])}<span class="go">Shop {v["n"].lower()}</span></a>' for k, v in CATS.items())
home = f'''<div class="wrap hero"><h1>Soft steps for every little and big walker.</h1><p class="sub">Comfortable, good-looking shoes for boys, girls and ladies. Pick a side and start looking.</p><div class="panels">{panels}</div></div>
<section id="shop"><div class="wrap"><div class="head"><h2>Shop all shoes</h2>{chips()}</div><div class="grid">{"".join(card(p, "") for p in PR)}</div></div></section>
<section id="seasons"><div class="wrap"><div class="head"><h2>Shop by season</h2></div><div class="seasons"><button class="season s-summer" data-s="Summer"><span class="h">Summer</span><p>Light, breathable pairs for hot days.</p></button><button class="season s-winter" data-s="Winter"><span class="h">Winter</span><p>Warm, cushioned pairs for cold mornings.</p></button></div></div></section>
<section id="adMid" hidden><div class="wrap"><div class="banner" id="bannerBox"></div></div></section>
<section id="about"><div class="wrap two"><div><h2 class="big">Made around the foot, not the trend.</h2><p class="lead">Qadmora, from “qadam” (step), is built on one idea: shoes should feel good from the first wear. We choose soft insoles, light soles and clean designs that suit school, family time and everyday life.</p></div><div class="feat"><div><b>Soft, cushioned insoles</b><span>Comfort for long days on your feet.</span></div><div><b>Light, flexible soles</b><span>Easy movement for running kids and busy ladies.</span></div><div><b>Easy ordering</b><span>Message us on WhatsApp with the shoe, size and colour.</span></div></div></div></section>
<section id="contact"><div class="wrap two"><div><h2 class="big">Contact us</h2><p class="lead">Tell us what you need and we will reply on WhatsApp with sizes, colours and delivery details.</p></div><form id="form"><input name="n" placeholder="Your name" required autocomplete="name" aria-label="Your name"><input name="p" type="tel" inputmode="tel" placeholder="Phone number" required autocomplete="tel" aria-label="Phone number"><textarea name="m" rows="4" placeholder="Which shoe and size do you need?" required aria-label="Message"></textarea><button class="send" type="submit">Send on WhatsApp</button></form></div></section>'''
write("index.html", page("Qadmora – Comfortable shoes for boys, girls and ladies", "Qadmora makes soft, comfortable, good-looking shoes for boys, girls and ladies. Shop by category and season.", home,
      ld={"@context": "https://schema.org", "@type": "Store", "name": "Qadmora", "url": DOM, "description": "Comfortable shoes for boys, girls and ladies.", "areaServed": "PK", "currenciesAccepted": "PKR"}))

# ---------- category pages ----------
for k, v in CATS.items():
    items = [p for p in PR if p["cat"] == k]
    others = " ".join(f'<a class="chip" href="../{o}/">{ov["n"]}</a>' for o, ov in CATS.items() if o != k)
    body = f'''<div class="wrap"><nav class="crumb" aria-label="Breadcrumb"><a href="../">Home</a> / {v["n"]}</nav><h1 class="ph" style="color:{v["c"]}">{v["n"]} shoes</h1><p class="lead">{v["seo"]}</p>
<div class="head">{chips()}<div class="chips">{others}</div></div><div class="grid">{"".join(card(p, "../") for p in items)}</div></div><div style="height:50px"></div>'''
    write(f"{k}/index.html", page(f"{v['n']} Shoes – Qadmora", v["seo"], body, "../",
          ld={"@context": "https://schema.org", "@type": "CollectionPage", "name": f"{v['n']} shoes", "description": v["seo"]}))

# ---------- product pages ----------
for p in PR:
    c = CATS[p["cat"]]
    th = "".join(f'<button class="th" style="background:{c["l"]}" data-i="{i}" aria-label="View photo {i}">{img(p, i, p["name"] + " view " + str(i))}</button>' for i in (1, 2, 3))
    cols = "".join(f'<button class="opt" aria-pressed="{str(j == 0).lower()}">{x}</button>' for j, x in enumerate(p["cols"]))
    szs = "".join(f'<button class="opt" aria-pressed="false">{s}</button>' for s in (p.get("sizes") or SIZES[p["cat"]]))
    rel = "".join(card(r, "../") for r in PR if r["cat"] == p["cat"] and r["sku"] != p["sku"])
    body = f'''<div class="wrap"><nav class="crumb" aria-label="Breadcrumb"><a href="../">Home</a> / <a href="../{p["cat"]}/">{c["n"]}</a> / {p["name"]}</nav>
<div class="prod"><div><div class="main" id="main" style="background:{c["l"]}">{img(p, 1, p["name"] + " " + c["n"].lower() + " shoes")}</div><div class="thumbs" id="thumbs">{th}</div></div>
<div><h1 class="ph">{p["name"]}</h1><div class="meta">{c["n"]} shoes · SKU {p["sku"]}{" · " + p["season"] if p["season"] != "All" else ""}</div><div class="price big2">Rs. {p["price"]:,}</div><p class="lead">{p["desc"]}</p>
<div class="og" data-opt="colour"><b>Colour</b><div>{cols}</div></div><div class="og" data-opt="size"><b>Size (EU)</b><div>{szs}</div></div>
<a class="buy lg" href="#" data-order data-name="{p["name"]}" data-sku="{p["sku"]}">Order on WhatsApp</a><p id="pmsg" class="err" role="status"></p>
<p class="note">Not sure about the size? Message us the foot length in cm and we will help. Delivery and exchange details are on the <a href="../delivery.html">delivery</a> and <a href="../returns.html">returns</a> pages.</p></div></div>
<h2 class="rel">More {c["n"].lower()} shoes</h2><div class="grid">{rel}</div></div><div style="height:50px"></div>'''
    ld = {"@context": "https://schema.org", "@type": "Product", "name": p["name"], "sku": p["sku"], "description": p["desc"], "brand": {"@type": "Brand", "name": "Qadmora"}, "category": c["n"] + " shoes", "color": ", ".join(p["cols"]),
          "offers": {"@type": "Offer", "priceCurrency": "PKR", "price": str(p["price"]), "availability": "https://schema.org/InStock", "url": f"{DOM}/p/{p['slug']}"}}
    write(f"p/{p['slug']}.html", page(f"{p['name']} – {c['n']} shoes | Qadmora", f"{p['name']} ({c['n']} shoes). {p['desc']} Rs. {p['price']:,}.", body, "../", ld=ld))

# ---------- policy pages and 404 ----------
POL = {
 "returns": ("Returns and exchange", ["We want you to be happy with your shoes. If the size does not fit or the shoes arrive damaged, message us on WhatsApp within 7 days of delivery and we will arrange an exchange.", "Shoes must be unworn, clean and in their original box. Please send us a photo of the shoes and your order details.", "(Sample text: edit the days and conditions to match your real policy.)"]),
 "delivery": ("Delivery", ["We deliver across Pakistan. Delivery time and charges are confirmed with you on WhatsApp when you place your order.", "Cash on delivery can be offered on request. Tell us your city and address when you order.", "(Sample text: edit to match your real delivery areas, time and charges.)"]),
 "privacy": ("Privacy", ["Qadmora does not store your personal details on this website. When you order or contact us, your name, phone number and message are sent to us on WhatsApp and used only to serve your order.", "This site uses Google Fonts, which may share your IP address with Google when the page loads."]),
}
for k, (t, ps) in POL.items():
    write(f"{k}.html", page(f"{t} – Qadmora", f"{t} information for Qadmora shoes.", f'<div class="wrap narrow"><h1 class="ph">{t}</h1>{"".join(f"<p class=lead>{x}</p>" for x in ps)}<p><a class="buy" href="./">Back to shop</a></p></div><div style="height:50px"></div>'))
write("404.html", page("Page not found – Qadmora", "This page could not be found.", '<div class="wrap narrow"><h1 class="ph">Page not found</h1><p class="lead">That page does not exist. Try our shoes instead.</p><p><a class="buy" href="' + BP + '/">Go to Qadmora home</a></p></div><div style="height:80px"></div>', BP + "/"))

# ---------- SEO + security files ----------
urls = ["/"] + [f"/{k}/" for k in CATS] + [f"/p/{p['slug']}" for p in PR] + ["/returns", "/delivery", "/privacy"]
write("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + "".join(f"<url><loc>{DOM}{u}</loc></url>" for u in urls) + "</urlset>")
write("robots.txt", f"User-agent: *\nAllow: /\nDisallow: /admin/\nSitemap: {DOM}/sitemap.xml\n")
write("_headers", "/*\n  X-Frame-Options: DENY\n  X-Content-Type-Options: nosniff\n  Referrer-Policy: strict-origin-when-cross-origin\n  Permissions-Policy: camera=(), microphone=(), geolocation=()\n/admin/*\n  X-Robots-Tag: noindex\n/\n  Content-Security-Policy: default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src https://fonts.gstatic.com; img-src 'self' data:; connect-src 'self'; frame-ancestors 'none'; base-uri 'self'; form-action 'self'\n/boys/*\n  Content-Security-Policy: default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src https://fonts.gstatic.com; img-src 'self' data:; connect-src 'self'; frame-ancestors 'none'; base-uri 'self'; form-action 'self'\n/girls/*\n  Content-Security-Policy: default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src https://fonts.gstatic.com; img-src 'self' data:; connect-src 'self'; frame-ancestors 'none'; base-uri 'self'; form-action 'self'\n/ladies/*\n  Content-Security-Policy: default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src https://fonts.gstatic.com; img-src 'self' data:; connect-src 'self'; frame-ancestors 'none'; base-uri 'self'; form-action 'self'\n/p/*\n  Content-Security-Policy: default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src https://fonts.gstatic.com; img-src 'self' data:; connect-src 'self'; frame-ancestors 'none'; base-uri 'self'; form-action 'self'\n/returns*\n  Content-Security-Policy: default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src https://fonts.gstatic.com; img-src 'self' data:; connect-src 'self'; frame-ancestors 'none'; base-uri 'self'; form-action 'self'\n/delivery*\n  Content-Security-Policy: default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src https://fonts.gstatic.com; img-src 'self' data:; connect-src 'self'; frame-ancestors 'none'; base-uri 'self'; form-action 'self'\n/privacy*\n  Content-Security-Policy: default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src https://fonts.gstatic.com; img-src 'self' data:; connect-src 'self'; frame-ancestors 'none'; base-uri 'self'; form-action 'self'\n/404*\n  Content-Security-Policy: default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src https://fonts.gstatic.com; img-src 'self' data:; connect-src 'self'; frame-ancestors 'none'; base-uri 'self'; form-action 'self'\n")
fav = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><defs><linearGradient id="g"><stop offset="0" stop-color="#1d5fc4"/><stop offset="1" stop-color="#c7246b"/></linearGradient></defs><rect width="64" height="64" rx="16" fill="url(#g)"/><text x="32" y="44" text-anchor="middle" font-size="36" font-weight="800" font-family="Arial" fill="#fff">Q</text></svg>'
write("favicon.svg", fav)
write("og-image.svg", '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 630"><defs><linearGradient id="g"><stop offset="0" stop-color="#1d5fc4"/><stop offset="1" stop-color="#c7246b"/></linearGradient></defs><rect width="1200" height="630" fill="url(#g)"/><text x="600" y="330" text-anchor="middle" font-size="120" font-weight="800" font-family="Arial" fill="#fff">Qadmora</text><text x="600" y="410" text-anchor="middle" font-size="40" font-family="Arial" fill="#fff">Comfortable shoes for kids and ladies</text></svg>')

# ---------- css, config, js ----------
write("styles.css", """:root{--ink:#14213d;--bg:#fbfaff;--mut:#4d5670;--line:#e1e4ef;--blue:#1d5fc4;--pink:#c7246b;--r:18px}
*{box-sizing:border-box;margin:0}html{scroll-behavior:smooth}
body{font-family:'DM Sans',system-ui,sans-serif;color:var(--ink);background:var(--bg);line-height:1.55}
h1,h2,h3,.logo,.h{font-family:'Bricolage Grotesque','DM Sans',sans-serif;line-height:1.08}a{color:inherit;text-decoration:none}
:focus-visible{outline:3px solid var(--ink);outline-offset:3px;border-radius:6px}.wrap{max-width:1180px;margin:0 auto;padding:0 20px}.narrow{max-width:760px}
.adbar{background:var(--ink);color:#fff;text-align:center;font-size:.9rem;padding:9px 16px}.adbar a{text-decoration:underline;text-underline-offset:3px}
header{position:sticky;top:0;z-index:20;background:rgba(251,250,255,.94);backdrop-filter:blur(8px);border-bottom:1px solid var(--line)}
.nav{display:flex;align-items:center;justify-content:space-between;height:66px}.left{display:flex;align-items:center;gap:12px}
.logo{font-size:1.7rem;font-weight:800;letter-spacing:-.02em}.logo i{font-style:normal;background:linear-gradient(90deg,var(--blue),var(--pink));-webkit-background-clip:text;background-clip:text;color:transparent}
.burger{font-size:1.5rem;line-height:1;background:none;border:1.5px solid var(--line);border-radius:12px;width:44px;height:44px;cursor:pointer;color:var(--ink)}
.wa{background:var(--ink);color:#fff;padding:10px 18px;border-radius:99px;font-weight:700;font-size:.92rem}
.drawer{position:fixed;top:0;left:0;bottom:0;width:min(300px,82vw);overflow:auto;background:#fff;z-index:40;padding:24px 18px;transform:translateX(-100%);visibility:hidden;transition:transform .3s ease,visibility .3s;display:flex;flex-direction:column;gap:2px;box-shadow:10px 0 40px rgba(20,33,61,.15)}
.drawer.open{transform:none;visibility:visible}.drawer a{padding:12px;border-radius:12px;font-weight:500;font-size:1.05rem}.drawer a:hover{background:#f1f2fa}.drawer a.logo{padding:0 12px 16px}
.overlay{position:fixed;inset:0;background:rgba(20,33,61,.45);z-index:30}
.hero h1{font-size:clamp(2.2rem,5.4vw,4.2rem);font-weight:800;letter-spacing:-.03em;max-width:15ch;padding:48px 0 12px}.sub{color:var(--mut);max-width:48ch;font-size:1.08rem;margin-bottom:28px}
.panels{display:flex;gap:14px;height:440px;margin-bottom:30px}
.panel{flex:1;border-radius:26px;padding:26px;display:flex;flex-direction:column;justify-content:space-between;position:relative;overflow:hidden;color:#fff;transition:flex .45s ease}
.panel:hover,.panel:focus-visible{flex:1.6}.panel h2{font-size:clamp(2rem,4vw,3.2rem);font-weight:800}.panel small{display:block;font-size:1rem;margin-top:6px;max-width:22ch}
.panel svg{position:absolute;right:-10px;bottom:34px;width:72%;max-width:340px;filter:drop-shadow(0 18px 18px rgba(0,0,0,.18));transition:transform .45s ease}.panel:hover svg{transform:rotate(-6deg) scale(1.06)}
.go{align-self:flex-start;background:#fff;color:var(--ink);padding:10px 18px;border-radius:99px;font-weight:700;font-size:.92rem;position:relative;z-index:1}
section{padding:54px 0}.head{display:flex;justify-content:space-between;align-items:end;flex-wrap:wrap;gap:16px;margin-bottom:24px}
.head h2,.big{font-size:clamp(1.8rem,3.6vw,2.6rem);font-weight:800;letter-spacing:-.02em}
.chips{display:flex;gap:8px;flex-wrap:wrap}.chip{border:1.5px solid var(--line);background:#fff;padding:8px 16px;border-radius:99px;font:inherit;font-weight:500;cursor:pointer;display:inline-block}
.chip[aria-pressed=true]{background:var(--ink);color:#fff;border-color:var(--ink)}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:20px}
.card{background:#fff;border:1px solid var(--line);border-radius:var(--r);overflow:hidden;display:flex;flex-direction:column}.card[hidden]{display:none}
.card .img{aspect-ratio:4/3;display:grid;place-items:center;position:relative}.card .img svg{width:70%}
.tag{position:absolute;left:12px;top:12px;background:#fff;border-radius:99px;font-size:.78rem;padding:4px 11px;font-weight:700}
.body{padding:16px 18px 18px;display:flex;flex-direction:column;gap:6px;flex:1}.card h3{font-size:1.15rem;font-weight:600}.meta{color:var(--mut);font-size:.9rem}
.row{display:flex;justify-content:space-between;align-items:center;margin-top:auto;padding-top:10px}.price{font-weight:700;font-size:1.1rem}
.buy{display:inline-block;background:var(--ink);color:#fff;padding:8px 14px;border-radius:99px;font-size:.88rem;font-weight:700}.buy.lg{padding:14px 26px;font-size:1rem;margin-top:8px}
.seasons{display:grid;grid-template-columns:1fr 1fr;gap:16px}.season{border-radius:24px;padding:34px;min-height:230px;display:flex;flex-direction:column;justify-content:flex-end;cursor:pointer;border:0;font:inherit;text-align:left}
.season .h{font-size:2rem;font-weight:800}.season p{max-width:30ch;margin-top:6px}.s-summer{background:#ffe9a8;color:#5a3d00}.s-winter{background:#d7e6fb;color:#12325c}
.banner{border-radius:26px;background:linear-gradient(100deg,var(--blue),var(--pink));color:#fff;padding:38px;display:flex;justify-content:space-between;align-items:center;gap:20px;flex-wrap:wrap}
.banner h3{font-size:clamp(1.5rem,3vw,2.2rem);font-weight:800;max-width:24ch}.banner img{max-height:120px;border-radius:14px}.banner .btn{background:#fff;color:var(--ink);padding:12px 22px;border-radius:99px;font-weight:700}
.two{display:grid;grid-template-columns:1fr 1fr;gap:40px}.feat{display:grid;gap:14px}.feat div{background:#fff;border:1px solid var(--line);border-radius:var(--r);padding:18px 20px}.feat b{display:block}.feat span{color:var(--mut);font-size:.95rem}
.lead{color:var(--mut);margin:12px 0 18px;max-width:58ch}form{display:grid;gap:12px}
input,textarea{font:inherit;padding:13px 15px;border:1.5px solid var(--line);border-radius:12px;background:#fff;width:100%}
.send{font:inherit;font-weight:700;background:var(--pink);color:#fff;border:0;padding:14px;border-radius:99px;cursor:pointer}
.ph{font-size:clamp(2rem,4.4vw,3.2rem);font-weight:800;letter-spacing:-.02em;padding-top:28px}.crumb{padding-top:22px;color:var(--mut);font-size:.92rem}.crumb a{text-decoration:underline}
.prod{display:grid;grid-template-columns:1.1fr 1fr;gap:40px;align-items:start;margin-bottom:20px}.main{border-radius:24px;aspect-ratio:4/3;display:grid;place-items:center;overflow:hidden}.main svg,.main img{width:80%}
.thumbs{display:flex;gap:10px;margin-top:10px}.th{flex:1;border:2px solid transparent;border-radius:14px;aspect-ratio:4/3;display:grid;place-items:center;cursor:pointer;overflow:hidden;padding:0}.th[aria-current=true]{border-color:var(--ink)}.th svg,.th img{width:80%}
.big2{font-size:1.8rem;margin:8px 0}.og{margin:16px 0}.og b{display:block;margin-bottom:8px}.og div{display:flex;gap:8px;flex-wrap:wrap}
.opt{border:1.5px solid var(--line);background:#fff;padding:9px 16px;border-radius:12px;font:inherit;font-weight:500;cursor:pointer}.opt[aria-pressed=true]{background:var(--ink);color:#fff;border-color:var(--ink)}
.err{color:#b3261e;font-weight:500;min-height:1.4em;margin-top:8px}.note{color:var(--mut);font-size:.92rem;margin-top:14px}.note a{text-decoration:underline}.rel{font-size:1.6rem;margin:36px 0 18px}
footer{border-top:1px solid var(--line);padding:30px 0;color:var(--mut);font-size:.93rem}footer .wrap{display:flex;justify-content:space-between;flex-wrap:wrap;gap:18px}
.fl{display:flex;flex-direction:column;gap:6px}.fl a,#soc a{text-decoration:underline}#soc{display:flex;gap:12px;margin-top:8px}.cp{width:100%}
@media(max-width:820px){.panels{flex-direction:column;height:auto}.panel{min-height:240px}.panel:hover{flex:1}.panel svg{width:58%}.two,.seasons,.prod{grid-template-columns:1fr}section{padding:38px 0}.hero h1{padding-top:32px}}
@media(max-width:480px){.wa{padding:9px 13px;font-size:.82rem}.logo{font-size:1.45rem}.banner,.season{padding:24px}.wrap{padding:0 16px}.grid{grid-template-columns:1fr 1fr;gap:12px}.body{padding:12px}.card h3{font-size:1rem}}
@media(prefers-reduced-motion:reduce){*{transition:none!important;scroll-behavior:auto!important}}""")
write("config.js", "window.QADMORA = " + json.dumps(SET, indent=2) + ";")
write("app.js", """(function(){
const C=window.QADMORA||{},$=s=>document.querySelector(s),$$=s=>[...document.querySelectorAll(s)];
const B=new URL('.',document.currentScript.src).href,L=u=>u&&u[0]==='/'?B+u.slice(1):u;\nconst wa=t=>`https://wa.me/${C.whatsapp}?text=${encodeURIComponent(t)}`;
$$('[data-wa]').forEach(a=>a.href=wa(a.dataset.wa));
const A=C.ads||{};
if(A.top&&A.top.text&&$('#adTop')){const e=$('#adTop');e.hidden=false;e.textContent=A.top.text+' ';const a=document.createElement('a');a.href=L(A.top.link);a.textContent=A.top.label;e.append(a)}
if(A.middle&&A.middle.title&&$('#adMid')){const m=A.middle;$('#adMid').hidden=false;const b=$('#bannerBox'),h=document.createElement('h3');h.textContent=m.title;b.append(h);
 if(m.image){const i=document.createElement('img');i.src=m.image;i.alt='';b.append(i)}const a=document.createElement('a');a.className='btn';a.href=L(m.link);a.textContent=m.label;b.append(a)}
const S=C.social||{},so=$('#soc');if(so)for(const k in S)if(S[k]){const a=document.createElement('a');a.href=S[k];a.rel='noopener';a.target='_blank';a.textContent=k[0].toUpperCase()+k.slice(1);so.append(a)}
function season(v){$$('.card[data-season]').forEach(c=>c.hidden=!(v==='all'||c.dataset.season===v||c.dataset.season==='All'));
 $$('#seasonChips .chip').forEach(b=>b.setAttribute('aria-pressed',b.dataset.s===v))}
if(C.useSeasons===false){$$('#seasonChips,#seasons,#navSeason').forEach(e=>e.remove())}
else{const sc=$('#seasonChips');if(sc)sc.addEventListener('click',e=>{const b=e.target.closest('.chip');if(b)season(b.dataset.s)});
 $$('.season').forEach(b=>b.addEventListener('click',()=>{season(b.dataset.s);$('#shop').scrollIntoView({behavior:'smooth'})}))}
const dr=$('#drawer'),ov=$('#overlay'),bg=$('#burger');
function menu(o){dr.classList.toggle('open',o);ov.hidden=!o;bg.setAttribute('aria-expanded',o);(o?dr.querySelector('a'):bg).focus({preventScroll:true})}
bg.onclick=()=>menu(true);ov.onclick=()=>menu(false);dr.addEventListener('click',e=>{if(e.target.closest('a'))menu(false)});
document.addEventListener('keydown',e=>{if(e.key==='Escape'&&dr.classList.contains('open'))menu(false)});
const th=$('#thumbs');if(th){const m=$('#main');const set=b=>{m.innerHTML=b.innerHTML;$$('.th').forEach(x=>x.setAttribute('aria-current',x===b))};
 th.addEventListener('click',e=>{const b=e.target.closest('.th');if(b)set(b)});set($('.th'))}
const o=$('[data-order]');if(o){const sel={};$$('[data-opt]').forEach(g=>{const on=g.querySelector('[aria-pressed=true]');if(on)sel[g.dataset.opt]=on.textContent;
 g.addEventListener('click',e=>{const b=e.target.closest('.opt');if(!b)return;g.querySelectorAll('.opt').forEach(x=>x.setAttribute('aria-pressed',x===b));sel[g.dataset.opt]=b.textContent})});
 o.addEventListener('click',e=>{e.preventDefault();const m=$('#pmsg');if(!sel.size){m.textContent='Please choose a size first.';return}m.textContent='';
 window.open(wa(`Assalam o Alaikum, I want to order ${o.dataset.name} (SKU ${o.dataset.sku}). Size: EU ${sel.size}. Colour: ${sel.colour||'any'}.`),'_blank','noopener')})}
const f=$('#form');if(f)f.addEventListener('submit',e=>{e.preventDefault();const d=new FormData(f);window.open(wa(`Name: ${d.get('n')}\\nPhone: ${d.get('p')}\\n${d.get('m')}`),'_blank','noopener')});
})();""")
print("done", len(os.listdir(OUT)))
