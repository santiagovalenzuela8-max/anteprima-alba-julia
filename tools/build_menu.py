#!/usr/bin/env python3
"""Genera le pagine del menu e la sezione "Il nostro menu" della home da tools/menu.json.

    python3 tools/build_menu.py

Scrive menu/index.html (/menu), una pagina per sezione (/menu/antipasti, /menu/ciorbe, ...)
e aggiorna in index.html la parte tra <!-- IL MENU COMPLETO --> e <!-- MACELLERIA -->.
Per cambiare un piatto o un prezzo basta modificare menu.json e rilanciare lo script.
"""
import html
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://albaiulia.it"
WA = "https://wa.me/393456967120"
DATA = json.load(open(os.path.join(ROOT, "tools", "menu.json"), encoding="utf-8"))
CATS = DATA["categories"]
e = html.escape


def euro(p):
    return "€ " + p.replace(".", ",")


def price_range(c):
    ps = sorted(float(d["price"]) for d in c["dishes"])
    lo, hi = ps[0], ps[-1]
    f = lambda v: f"{v:.2f}".replace(".", ",")
    return f"€ {f(lo)}" if lo == hi else f"da € {f(lo)} a € {f(hi)}"


def plural(n):
    return f"{n} piatto" if n == 1 else f"{n} piatti"


def license_name(l):
    return l if l.startswith(("CC", "Public")) else "CC " + l


# ---------------------------------------------------------------- parti comuni

SPRITE = open(os.path.join(ROOT, "index.html"), encoding="utf-8").read()
SPRITE = SPRITE[SPRITE.index('<svg width="0" height="0"'):]
SPRITE = SPRITE[:SPRITE.index("</svg>") + 6]


FP = ' fetchpriority="high"'


def head(title, desc, path, image, ld):
    return f"""<!doctype html>
<html lang="it">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta name="theme-color" content="#6e2a26">
<meta property="og:type" content="website">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:image" content="{SITE}{image}">
<meta property="og:url" content="{SITE}{path}">
<meta property="og:locale" content="it_IT">
<link rel="canonical" href="{SITE}{path}">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Sorts+Mill+Goudy:ital@0;1&family=Figtree:wght@400;500;600;700&display=swap">
<link rel="stylesheet" href="/style.css">
<script type="application/ld+json">
{json.dumps(ld, ensure_ascii=False, indent=1)}
</script>
</head>
<body class="page-menu">

{SPRITE}

<a class="skip" href="#contenuto">Vai al contenuto</a>

<header class="nav is-scrolled" id="top">
  <div class="nav__inner">
    <a class="brand" href="/" aria-label="Alba Iulia, torna alla home">
      <svg class="brand__logo" aria-hidden="true"><use href="#logo"/></svg>
    </a>
    <nav class="nav__links" id="menu" aria-label="Sezioni">
      <a href="/#titolare">Il titolare</a>
      <a href="/#locale">Il locale</a>
      <a href="/menu" class="is-active">Menu</a>
      <a href="/#macelleria">Macelleria</a>
      <a href="/#galleria">Galleria</a>
      <a href="/#dove">Dove siamo</a>
    </nav>
    <a class="nav__wa js-wa" href="{WA}" target="_blank" rel="noopener" aria-label="Scrivici su WhatsApp">
      <svg aria-hidden="true"><use href="#wa"/></svg><span>WhatsApp</span>
    </a>
    <button class="nav__toggle" id="nav-toggle" type="button" aria-expanded="false" aria-controls="menu" aria-label="Apri il menu"><span></span><span></span></button>
  </div>
</header>
"""


FOOT = f"""
<footer class="footer">
  <div class="wrap footer__inner">
    <svg class="footer__logo" role="img" aria-label="Alba Iulia"><use href="#logo"/></svg>
    <p class="footer__meta">Ristorante, caffetteria, gastronomia e macelleria<br>Via Luigi Prina 21, 37136 Verona<br><a href="tel:+390458626014">045 862 6014</a> <span aria-hidden="true">/</span> <a href="https://www.facebook.com/albajuliaverona/" target="_blank" rel="noopener">Facebook</a></p>
    <p class="footer__bye">Poftă bună!<small>Buon appetito, in romeno</small></p>
  </div>
  <div class="wrap made-by">
    <a class="made-by__link" href="https://andiamonline.eu/" target="_blank" rel="noopener">
      <span>Sito creato da</span>
      <img src="/img/andiamonline-logo.webp" alt="Andiamo Online" width="900" height="127" loading="lazy" decoding="async">
    </a>
  </div>
</footer>

<a class="wa-float js-wa" href="{WA}" target="_blank" rel="noopener" data-msg="Ciao Alba Iulia! Vorrei qualche informazione sul menu." aria-label="Scrivici su WhatsApp">
  <svg aria-hidden="true"><use href="#wa"/></svg>
  <span class="wa-float__label">Scrivici su WhatsApp</span>
</a>

<script src="/pagine.js" defer></script>
</body>
</html>
"""


def cta(msg):
    return f"""
  <section class="mp-cta">
    <div class="wrap mp-cta__inner reveal">
      <div>
        <h2>Ti aspettiamo a tavola</h2>
        <p>Via Luigi Prina 21, Verona. Aperti tutti i giorni. Prenota un tavolo o chiedici il piatto del giorno su WhatsApp.</p>
      </div>
      <div class="mp-cta__actions">
        <a class="btn btn--solid btn--lg js-wa" href="{WA}" target="_blank" rel="noopener" data-msg="{e(msg)}"><svg aria-hidden="true"><use href="#wa"/></svg>Prenota su WhatsApp</a>
        <a class="btn btn--ghost btn--lg" href="tel:+390458626014"><svg aria-hidden="true"><use href="#tel"/></svg>045 862 6014</a>
      </div>
    </div>
    <p class="wrap mp-cta__note">Coperto {euro(DATA["coperto"])} a persona. Per allergie e intolleranze chiedi al personale: ti indichiamo gli ingredienti di ogni piatto.</p>
  </section>
"""


def credits(dishes, extra=" mp-credits", ind="    "):
    def author(d):
        return e(re.sub(r"\s+", " ", d["credit"]["author"]).strip() or "autore sconosciuto")
    li = "\n".join(
        f'{ind}    <li>{e(d["name"])}: <a href="{e(d["credit"]["page"])}" target="_blank" rel="noopener nofollow">'
        f'{author(d)}</a>, {e(license_name(d["credit"]["license"]))}</li>'
        for d in dishes)
    return (f'{ind}<details class="carta__credits{extra}">\n'
            f'{ind}  <summary>Le foto sono indicative del piatto servito · Crediti fotografici</summary>\n'
            f'{ind}  <ul>\n{li}\n{ind}  </ul>\n{ind}</details>')


def cats_nav(current=None):
    links = []
    for c in CATS:
        cur = ' aria-current="page"' if c is current else ""
        links.append(f'      <a href="/menu/{c["slug"]}"{cur}><span>{e(c["it"])}</span><small>{e(c["ro"])}</small></a>')
    return f"""  <nav class="mp-cats" aria-label="Sezioni del menu">
    <div class="wrap mp-cats__row">
{chr(10).join(links)}
    </div>
  </nav>
"""


# ---------------------------------------------------------------- pagina di una sezione

def dish_card(d):
    qty = f'<span class="dish__qty">{e(d["qty"])}</span>' if d["qty"] else ""
    return f"""      <li class="mp-dish reveal">
        <figure class="mp-dish__media"><img src="/img/menu/{d["img"]}.webp" alt="{e(d["name"])}" width="800" height="600" loading="lazy" decoding="async"></figure>
        <div class="mp-dish__body">
          <div class="mp-dish__head">
            <h2 class="mp-dish__name">{e(d["name"])}</h2>
            <span class="mp-dish__dots" aria-hidden="true"></span>
            <p class="mp-dish__price">{euro(d["price"])}</p>
          </div>
          {qty}
          <p class="mp-dish__desc">{e(d["desc"])}</p>
        </div>
      </li>"""


def category_page(i, c):
    n = len(c["dishes"])
    prev_c, next_c = CATS[i - 1], CATS[(i + 1) % len(CATS)]
    path = f"/menu/{c['slug']}"
    title = f"{c['it']} ({c['ro']}) · Menu Alba Iulia Verona"
    desc = f"{c['it']} del ristorante Alba Iulia a Verona: {', '.join(d['name'] for d in c['dishes'][:4])}{' e altri' if n > 4 else ''}. Cucina romena della famiglia Sbuciumelea, prezzi e foto."
    ld = {
        "@context": "https://schema.org",
        "@graph": [
            {"@type": "MenuSection", "name": f"{c['it']} / {c['ro']}", "description": c["intro"], "url": SITE + path,
             "hasMenuItem": [{"@type": "MenuItem", "name": d["name"], "description": d["desc"],
                              "image": f"{SITE}/img/menu/{d['img']}.webp",
                              "offers": {"@type": "Offer", "price": d["price"], "priceCurrency": "EUR"}} for d in c["dishes"]]},
            {"@type": "BreadcrumbList", "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
                {"@type": "ListItem", "position": 2, "name": "Menu", "item": SITE + "/menu"},
                {"@type": "ListItem", "position": 3, "name": c["it"], "item": SITE + path}]},
        ],
    }
    pics = c["dishes"][:3]
    stack = "\n".join(
        f'        <img class="mp-hero__pic mp-hero__pic--{k + 1}" src="/img/menu/{d["img"]}.webp" alt="{e(d["name"])}" width="800" height="600"{FP if k == 0 else ""} decoding="async">'
        for k, d in enumerate(pics))
    nxt = lambda c2, label, cls: f"""      <a class="mp-next__card mp-next__card--{cls} reveal" href="/menu/{c2["slug"]}">
        <img src="/img/menu/{c2["dishes"][0]["img"]}.webp" alt="" width="800" height="600" loading="lazy" decoding="async">
        <span class="mp-next__label">{label}</span>
        <span class="mp-next__name">{e(c2["it"])} <em>{e(c2["ro"])}</em></span>
      </a>"""
    body = f"""
<main id="contenuto">
  <section class="mp-hero">
    <div class="wrap mp-hero__inner">
      <div class="mp-hero__copy">
        <nav class="crumbs" aria-label="Sei qui"><a href="/">Home</a><span aria-hidden="true">/</span><a href="/menu">Menu</a><span aria-hidden="true">/</span><span aria-current="page">{e(c["it"])}</span></nav>
        <p class="carta__kicker">Meniu · {e(c["ro"])}</p>
        <h1>{e(c["it"])}</h1>
        <p class="mp-hero__intro">{e(c["intro"])}</p>
        <p class="mp-hero__meta"><span>{plural(n)}</span><span>{price_range(c)}</span></p>
      </div>
      <div class="mp-hero__stack mp-hero__stack--{len(pics)}" aria-hidden="true">
{stack}
      </div>
    </div>
  </section>

{cats_nav(c)}
  <section class="mp-list" aria-label="{e(c["it"])}: i piatti">
    <ul class="wrap mp-grid">
{chr(10).join(dish_card(d) for d in c["dishes"])}
    </ul>
  </section>

  <section class="mp-next" aria-label="Continua a sfogliare il menu">
    <div class="wrap mp-next__row">
{nxt(prev_c, "← Sezione precedente", "prev")}
{nxt(next_c, "Sezione successiva →", "next")}
    </div>
    <p class="wrap mp-next__all"><a class="link" href="/menu">Tutte le sezioni del menu</a></p>
  </section>
{cta(f"Ciao! Vorrei prenotare un tavolo da Alba Iulia. Ho visto il menu: {c['it']}.")}
  <div class="wrap">
{credits(c["dishes"])}
  </div>
</main>
"""
    return head(title, desc, path, f"/img/menu/{c['dishes'][0]['img']}.webp", ld) + body + FOOT


# ---------------------------------------------------------------- /menu

def menu_index():
    path = "/menu"
    total = sum(len(c["dishes"]) for c in CATS)
    title = "Menu · Alba Iulia Verona, cucina tradizionale romena"
    desc = f"Il menu di Alba Iulia a Verona: {total} piatti della tradizione romena tra antipasti, ciorbe, secondi, grigliate, contorni e dolci, con foto e prezzi."
    ld = {
        "@context": "https://schema.org", "@type": "Menu", "name": "Menu Alba Iulia", "url": SITE + path,
        "inLanguage": "it",
        "hasMenuSection": [{"@type": "MenuSection", "name": f"{c['it']} / {c['ro']}", "url": f"{SITE}/menu/{c['slug']}",
                            "hasMenuItem": [{"@type": "MenuItem", "name": d["name"], "description": d["desc"],
                                             "offers": {"@type": "Offer", "price": d["price"], "priceCurrency": "EUR"}}
                                            for d in c["dishes"]]} for c in CATS],
    }
    cards = []
    for k, c in enumerate(CATS):
        cards.append(f"""      <li class="reveal">
        <a class="mp-cat" href="/menu/{c["slug"]}">
          <figure class="mp-cat__media"><img src="/img/menu/{c["dishes"][0]["img"]}.webp" alt="{e(c["dishes"][0]["name"])}" width="800" height="600"{' loading="lazy"' if k > 2 else ''} decoding="async"></figure>
          <div class="mp-cat__body">
            <p class="mp-cat__num">{k + 1:02d}</p>
            <h2>{e(c["it"])} <em>{e(c["ro"])}</em></h2>
            <p class="mp-cat__intro">{e(c["intro"].split(": ")[0].split(". ")[0].rstrip("."))}.</p>
            <p class="mp-cat__meta"><span>{plural(len(c["dishes"]))}</span><span>{price_range(c)}</span></p>
            <span class="mp-cat__go">Scopri la sezione <span aria-hidden="true">→</span></span>
          </div>
        </a>
      </li>""")
    body = f"""
<main id="contenuto">
  <section class="mp-hero mp-hero--index">
    <div class="wrap mp-hero__inner">
      <div class="mp-hero__copy">
        <nav class="crumbs" aria-label="Sei qui"><a href="/">Home</a><span aria-hidden="true">/</span><span aria-current="page">Menu</span></nav>
        <p class="carta__kicker">Meniu · Il menu</p>
        <h1>Il nostro menu</h1>
        <p class="mp-hero__intro">Cucina tradizionale romena preparata ogni giorno dalla famiglia Sbuciumelea, dal 2004 in Via Luigi Prina a Verona. Scegli una sezione: per ogni piatto trovi foto, descrizione e prezzo.</p>
        <p class="mp-hero__meta"><span>{len(CATS)} sezioni</span><span>{plural(total)}</span><span>Coperto {euro(DATA["coperto"])}</span></p>
      </div>
      <div class="mp-hero__stack mp-hero__stack--3" aria-hidden="true">
        <img class="mp-hero__pic mp-hero__pic--1" src="/img/menu/tochitura.webp" alt="" width="800" height="600" fetchpriority="high" decoding="async">
        <img class="mp-hero__pic mp-hero__pic--2" src="/img/menu/platou-alba-iulia.webp" alt="" width="800" height="600" decoding="async">
        <img class="mp-hero__pic mp-hero__pic--3" src="/img/menu/salata-vinete.webp" alt="" width="800" height="600" decoding="async">
      </div>
    </div>
  </section>

  <section class="mp-index" aria-label="Le sezioni del menu">
    <ul class="wrap mp-index__grid">
{chr(10).join(cards)}
    </ul>
  </section>
{cta("Ciao! Vorrei prenotare un tavolo da Alba Iulia.")}
</main>
"""
    return head(title, desc, path, "/img/menu/platou-alba-iulia.webp", ld) + body + FOOT


# ---------------------------------------------------------------- sezione della home

def home_section():
    o = ['''  <!-- IL MENU COMPLETO (generato da tools/build_menu.py) -->
  <section class="carta" id="carta" aria-labelledby="carta-title">
    <div class="wrap">
      <header class="carta__head">
        <div>
          <p class="carta__kicker">Meniu · Il menu</p>
          <h2 id="carta-title">Il nostro menu</h2>
        </div>
        <div class="carta__lead">
          <p>Cucina tradizionale romena, preparata ogni giorno dalla famiglia Sbuciumelea. Scegli una sezione e sfoglia i piatti.</p>
          <a class="carta__all" href="menu">Apri il menu completo <span aria-hidden="true">→</span></a>
        </div>
      </header>
      <div class="carta__tabs" role="tablist" aria-label="Sezioni del menu">''']
    for i, c in enumerate(CATS):
        sel = "true" if i == 0 else "false"
        ti = "" if i == 0 else ' tabindex="-1"'
        o.append(f'        <button type="button" role="tab" class="carta__tab" id="tab-{c["id"]}" aria-controls="cat-{c["id"]}" aria-selected="{sel}"{ti}><span>{e(c["it"])}</span><small>{e(c["ro"])}</small></button>')
    o.append("      </div>")
    for i, c in enumerate(CATS):
        hid = "" if i == 0 else " hidden"
        o.append(f'      <div class="carta__panel" role="tabpanel" id="cat-{c["id"]}" aria-labelledby="tab-{c["id"]}"{hid}>')
        o.append(f'        <h3 class="carta__cat">{e(c["it"])} <span>{e(c["ro"])}</span></h3>')
        o.append('        <ul class="carta__grid">')
        for d in c["dishes"]:
            q = f'<span class="dish__qty">{e(d["qty"])}</span>' if d["qty"] else ""
            o.append(f'''          <li class="dish">
            <figure class="dish__media"><img src="img/menu/{d["img"]}.webp" alt="{e(d["name"])}" width="800" height="600" loading="lazy" decoding="async"></figure>
            <div class="dish__body">
              <h4 class="dish__name">{e(d["name"])}{q}</h4>
              <p class="dish__desc">{e(d["desc"])}</p>
              <p class="dish__price">{euro(d["price"])}</p>
            </div>
          </li>''')
        o.append("        </ul>")
        o.append(f'        <a class="carta__more" href="menu/{c["slug"]}">Vai alla pagina {e(c["it"])} <span aria-hidden="true">→</span></a>')
        o.append("      </div>")
    o.append(f'''      <footer class="carta__foot">
        <p>Coperto {euro(DATA["coperto"])} a persona. Per allergie e intolleranze chiedi al personale.</p>
        <a class="btn btn--solid js-wa" href="{WA}" target="_blank" rel="noopener" data-msg="Ciao! Vorrei prenotare un tavolo da Alba Iulia."><svg aria-hidden="true"><use href="#wa"/></svg>Prenota un tavolo</a>
      </footer>
{credits([d for c in CATS for d in c["dishes"]], "", "      ")}
    </div>
  </section>

''')
    return "\n".join(o)


def write(rel, text):
    p = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        f.write(text)
    print("scritto", rel)


if __name__ == "__main__":
    write("menu/index.html", menu_index())
    for i, c in enumerate(CATS):
        write(f"menu/{c['slug']}.html", category_page(i, c))
    idx = open(os.path.join(ROOT, "index.html"), encoding="utf-8").read()
    a = idx.index("  <!-- IL MENU COMPLETO")
    b = idx.index("  <!-- MACELLERIA -->")
    write("index.html", idx[:a] + home_section() + idx[b:])
    sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
          f'  <url><loc>{SITE}/</loc><changefreq>monthly</changefreq><priority>1.0</priority></url>',
          f'  <url><loc>{SITE}/menu</loc><changefreq>monthly</changefreq><priority>0.9</priority></url>']
    sm += [f'  <url><loc>{SITE}/menu/{c["slug"]}</loc><changefreq>monthly</changefreq><priority>0.8</priority></url>' for c in CATS]
    write("sitemap.xml", "\n".join(sm + ["</urlset>", ""]))
