"""Le pagine interne del sito, costruite con gli stessi blocchi della home.

Stessa apertura della home (parete capitonné in 3D, ritratto nell'ovale che si inclina,
titolo che entra parola per parola, pulsanti magnetici), stesse sezioni (famiglia in rosso
con la linea del tempo, schede ad arco, macelleria, recensioni, giostra 3D, dove siamo)
e gli stessi script (ui.js, wall.js). I testi riprendono solo informazioni vere del locale:
se qualcosa cambia si corregge qui e si rilancia python3 tools/build_site.py.
"""
import json

from build_site import (CATS, DATA, SITE, SPRITE, WA, credits, e, euro, nav_links, plural,
                        price_range)

TEL = "tel:+390458626014"
MAPS_DIR = "https://www.google.com/maps/dir/?api=1&amp;destination=Via+Luigi+Prina+21+37136+Verona"
RESTAURANT = {
    "@type": "Restaurant", "@id": SITE + "/#ristorante", "name": "Alba Iulia", "url": SITE + "/",
    "image": SITE + "/img/sala-hd.jpg", "telephone": "+39 045 862 6014",
    "servesCuisine": ["Romena", "Moldava", "Italiana"], "foundingDate": "2004",
    "address": {"@type": "PostalAddress", "streetAddress": "Via Luigi Prina, 21", "postalCode": "37136",
                "addressLocality": "Verona", "addressRegion": "VR", "addressCountry": "IT"},
    "openingHours": "Mo-Su 09:00-20:00",
    "aggregateRating": {"@type": "AggregateRating", "ratingValue": "4.7", "reviewCount": "232"},
}


def wa_attr(msg):
    return f'href="{WA}" target="_blank" rel="noopener" data-msg="{e(msg)}"'


# ---------------------------------------------------------------- cornice comune

def head(title, desc, path, image, ld, active, preload):
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
<link rel="preconnect" href="https://cdn.jsdelivr.net" crossorigin>
<link rel="preconnect" href="https://cdnjs.cloudflare.com" crossorigin>
<link rel="preload" as="image" href="{preload}" fetchpriority="high">
<script type="importmap">
{{ "imports": {{
  "three": "https://cdn.jsdelivr.net/npm/three@0.169.0/build/three.module.min.js",
  "three/addons/": "https://cdn.jsdelivr.net/npm/three@0.169.0/examples/jsm/"
}} }}
</script>
<script type="application/ld+json">
{json.dumps(ld, ensure_ascii=False, indent=1)}
</script>
</head>
<body class="page-inner">

{SPRITE}

<a class="skip" href="#contenuto">Vai al contenuto</a>

<header class="nav" id="top">
  <div class="nav__inner">
    <a class="brand" href="/" aria-label="Alba Iulia, torna alla home">
      <svg class="brand__logo" aria-hidden="true"><use href="#logo"/></svg>
    </a>
    <nav class="nav__links" id="menu" aria-label="Sezioni">
{nav_links(active)}
    </nav>
    <a class="nav__wa js-wa" href="{WA}" target="_blank" rel="noopener" aria-label="Scrivici su WhatsApp">
      <svg aria-hidden="true"><use href="#wa"/></svg><span>WhatsApp</span>
    </a>
    <button class="nav__toggle" id="nav-toggle" type="button" aria-expanded="false" aria-controls="menu" aria-label="Apri il menu"><span></span><span></span></button>
  </div>
</header>

<main id="contenuto">
"""


FOOT = f"""</main>

<footer class="footer">
  <div class="wrap footer__inner">
    <svg class="footer__logo" role="img" aria-label="Alba Iulia"><use href="#logo"/></svg>
    <p class="footer__meta">Ristorante, caffetteria, gastronomia e macelleria<br>Via Luigi Prina 21, 37136 Verona<br><a href="{TEL}">045 862 6014</a> <span aria-hidden="true">/</span> <a href="https://www.facebook.com/albajuliaverona/" target="_blank" rel="noopener">Facebook</a></p>
    <p class="footer__bye">Poftă bună!<small>Buon appetito, in romeno</small></p>
  </div>
  <nav class="wrap footer__nav" aria-label="Pagine del sito">
{nav_links(None, "    ")}
  </nav>
  <div class="wrap made-by">
    <a class="made-by__link" href="https://andiamonline.eu/" target="_blank" rel="noopener">
      <span>Sito creato da</span>
      <img src="/img/andiamonline-logo.webp" alt="Andiamo Online" width="900" height="127" loading="lazy" decoding="async">
    </a>
  </div>
</footer>

<a class="wa-float js-wa" href="{WA}" target="_blank" rel="noopener" data-msg="Ciao Alba Iulia! Vorrei qualche informazione." aria-label="Scrivici su WhatsApp">
  <svg aria-hidden="true"><use href="#wa"/></svg>
  <span class="wa-float__label">Scrivici su WhatsApp</span>
</a>

<dialog class="lightbox" id="lightbox" aria-label="Foto ingrandita">
  <button class="lightbox__close" type="button" id="lightbox-close" aria-label="Chiudi">×</button>
  <img id="lightbox-img" alt="">
</dialog>

<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/ScrollTrigger.min.js"></script>
<script src="/ui.js"></script>
<script type="module" src="/wall.js"></script>
</body>
</html>
"""


def ld(path, crumbs, extra=None):
    items = [{"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"}]
    items += [{"@type": "ListItem", "position": i + 2, "name": n, "item": SITE + h} for i, (n, h) in enumerate(crumbs)]
    g = [{"@type": "WebPage", "name": crumbs[-1][0], "url": SITE + path, "about": {"@id": SITE + "/#ristorante"}},
         {"@type": "BreadcrumbList", "itemListElement": items}, RESTAURANT]
    if extra:
        g.append(extra)
    return {"@context": "https://schema.org", "@graph": g}


def page(path, crumbs, title, desc, og, body, hero_img, extra_ld=None, active=None):
    return head(title, desc, path, og, ld(path, crumbs, extra_ld), active or path, "/img/" + hero_img) + body + FOOT


# ---------------------------------------------------------------- blocchi della home

def hero(crumbs, kicker, title, lead, img, alt, tag, facts, wa_label, wa_msg, second=None, pos="50% 40%"):
    """Apertura come quella della home: parete 3D, testo a sinistra, foto nell'ovale a destra."""
    trail = ['<a href="/">Home</a>']
    for i, (n, h) in enumerate(crumbs):
        trail.append(f'<span aria-current="page">{e(n)}</span>' if i == len(crumbs) - 1 else f'<a href="{h}">{e(n)}</a>')
    sep = '<span aria-hidden="true">/</span>'
    if second is None:
        second = f'<a class="btn btn--ghost btn--lg magnetic" href="{TEL}"><svg aria-hidden="true"><use href="#tel"/></svg>045 862 6014</a>'
    dl = "\n".join(f"      <div><dt>{e(dt)}</dt><dd><strong>{e(st)}</strong> {e(dd)}</dd></div>" for dt, st, dd in facts)
    return f"""  <section class="hero hero--page" id="hero">
    <canvas class="hero__gl" id="gl" aria-hidden="true"></canvas>
    <div class="hero__inner">
      <div class="hero__copy">
        <nav class="crumbs" aria-label="Sei qui">{sep.join(trail)}</nav>
        <p class="hero__kicker">{e(kicker)}</p>
        <h1 class="hero__title" id="hero-title">{e(title)}</h1>
        <p class="hero__lead">{lead}</p>
        <div class="hero__actions">
          <a class="btn btn--solid btn--lg magnetic js-wa" {wa_attr(wa_msg)}>
            <svg aria-hidden="true"><use href="#wa"/></svg>{e(wa_label)}
          </a>
          {second}
        </div>
      </div>

      <figure class="owner">
        <div class="owner__frame" id="owner-frame">
          <div class="owner__ring" aria-hidden="true"></div>
          <div class="owner__photo">
            <img src="/img/{img}" alt="{e(alt)}" width="800" height="600" style="object-position:{pos}" fetchpriority="high" decoding="async">
            <span class="owner__glare" aria-hidden="true"></span>
          </div>
        </div>
        <figcaption class="owner__tag">
          <b>{e(tag[0])}</b>
          <span>{e(tag[1])}</span>
        </figcaption>
      </figure>
    </div>

    <dl class="hero__facts">
{dl}
    </dl>
  </section>
"""


def family(img, alt, h2, paras, steps, link=None, kicker=None):
    """Sezione rossa come "La famiglia" della home: foto con ombra dorata, testo e linea del tempo."""
    ps = "\n".join(f"        <p>{p}</p>" for p in paras)
    tl = "\n".join(f"          <li><b>{e(b)}</b><span>{e(t)}</span></li>" for b, t in steps)
    k = f'\n        <p class="sec-kicker sec-kicker--light">{e(kicker)}</p>' if kicker else ""
    more = f'\n        <a class="more-link more-link--light" href="{link[0]}">{e(link[1])} <span aria-hidden="true">→</span></a>' if link else ""
    n = f" timeline--{len(steps)}" if len(steps) != 3 else ""
    return f"""
  <section class="family">
    <div class="wrap family__inner">
      <figure class="family__photo reveal">
        <img src="/img/{img}" alt="{e(alt)}" width="800" height="600" loading="lazy" decoding="async">
      </figure>
      <div class="family__copy reveal">{k}
        <h2>{e(h2)}</h2>
{ps}
        <ol class="timeline{n}">
{tl}
        </ol>{more}
      </div>
    </div>
  </section>
"""


def services(h2, lead, cards, link=None):
    """Schede ad arco come "Quattro modi di stare a tavola" della home.
    cards: (img, alt, titolo, testo, href o None, etichetta o None)"""
    arts = []
    for img, alt, t, p, href, badge in cards:
        b = f'<span class="service__badge">{e(badge)}</span>' if badge else ""
        inner = f"""<div class="service__media"><img src="/img/{img}" alt="{e(alt)}" width="800" height="600" loading="lazy" decoding="async">{b}</div>
          <h3>{e(t)}</h3>
          <p>{e(p)}</p>"""
        if href:
            arts.append(f"""        <a class="service service--link" href="{href}">
          {inner}
          <span class="service__go">Scopri <span aria-hidden="true">→</span></span>
        </a>""")
        else:
            arts.append(f"""        <article class="service">
          {inner}
        </article>""")
    more = f'<br><a class="more-link" href="{link[0]}">{e(link[1])} <span aria-hidden="true">→</span></a>' if link else ""
    return f"""
  <section class="services">
    <div class="services__pin">
      <header class="services__head reveal">
        <h2>{e(h2)}</h2>
        <p>{e(lead)}{more}</p>
        <div class="services__ctrl">
          <button type="button" class="round round--dark" id="svc-prev" aria-label="Scheda precedente" disabled>‹</button>
          <button type="button" class="round round--dark" id="svc-next" aria-label="Scheda successiva">›</button>
        </div>
      </header>
      <div class="services__track services__track--{len(cards)}" id="services-track">
{chr(10).join(arts)}
      </div>
    </div>
  </section>
"""


def butcher(h2, text, checks, img, alt, msg, label, cream=True):
    li = "\n".join(f"          <li>{e(c)}</li>" for c in checks)
    return f"""
  <section class="butcher{'' if cream else ' butcher--paper'}">
    <div class="wrap butcher__inner">
      <div class="butcher__copy reveal">
        <h2>{e(h2)}</h2>
        <p>{e(text)}</p>
        <ul class="checks">
{li}
        </ul>
        <a class="btn btn--solid magnetic js-wa" {wa_attr(msg)}>
          <svg aria-hidden="true"><use href="#wa"/></svg>{e(label)}
        </a>
      </div>
      <figure class="butcher__photo reveal">
        <img src="/img/{img}" alt="{e(alt)}" width="800" height="600" loading="lazy" decoding="async">
      </figure>
    </div>
  </section>
"""


REVIEWS = """
  <section class="reviews">
    <div class="wrap reviews__inner reveal">
      <p class="reviews__score"><strong>4,7</strong><span class="reviews__stars" aria-label="4,7 su 5"><i style="--fill:94%"></i></span><small>232 recensioni su Google</small></p>
      <p class="reviews__big">Cucina di famiglia, porzioni generose e un'accoglienza che fa tornare. Per tanti romeni a Verona è il sapore di casa. Per tanti veronesi è la scoperta di una cucina nuova.</p>
      <a class="link" href="https://www.google.com/maps/search/?api=1&amp;query=Alba+Iulia+Via+Luigi+Prina+21+Verona" target="_blank" rel="noopener">Leggi le recensioni su Google</a>
    </div>
  </section>
"""


def visit(h2="Via Luigi Prina 21, Verona", msg="Ciao! Vorrei prenotare un tavolo da Alba Iulia.", week=False):
    rows = ""
    if week:
        giorni = ["Lunedì", "Martedì", "Mercoledì", "Giovedì", "Venerdì", "Sabato", "Domenica"]
        rows = "\n".join(f'            <tr><th scope="row">{g}</th><td>09:00 – 20:00</td></tr>' for g in giorni)
        rows = f"""
        <table class="hours">
          <caption class="sr-only">Orari di apertura</caption>
          <tbody>
{rows}
          </tbody>
        </table>"""
    return f"""
  <section class="visit" id="contatti">
    <div class="wrap visit__inner">
      <div class="visit__info reveal">
        <h2>{e(h2)}</h2>
        <dl class="visit__list">
          <div><dt>Orari</dt><dd>Tutti i giorni, 09:00 – 20:00<span class="visit__status" id="open-status" aria-live="polite"></span></dd></div>
          <div><dt>Telefono</dt><dd><a class="link" href="{TEL}">045 862 6014</a></dd></div>
          <div><dt>WhatsApp</dt><dd><a class="link js-wa" {wa_attr(msg)}>345 696 7120</a></dd></div>
          <div><dt>Indirizzo</dt><dd>Via Luigi Prina, 21, 37136 Verona</dd></div>
          <div><dt>Servizi</dt><dd>Sala, dehors, asporto e consegna a domicilio</dd></div>
        </dl>{rows}
        <div class="visit__actions">
          <a class="btn btn--wa btn--lg magnetic js-wa" {wa_attr(msg)}>
            <svg aria-hidden="true"><use href="#wa"/></svg>Scrivici su WhatsApp
          </a>
          <a class="btn btn--ghost btn--lg magnetic" href="{MAPS_DIR}" target="_blank" rel="noopener">Indicazioni stradali</a>
        </div>
      </div>
      <div class="visit__map reveal">
        <iframe title="Mappa: Alba Iulia, Via Luigi Prina 21, Verona" src="https://maps.google.com/maps?q=Via%20Luigi%20Prina%2021%2C%2037136%20Verona&amp;z=16&amp;output=embed" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>
      </div>
    </div>
  </section>
"""


SALA = """
  <section class="sala" id="sala">
    <div class="sala__pin">
      <div class="sala__stage">
        <figure class="sala__media" id="sala-media">
          <div class="sala__img" id="sala-img"><img src="/img/sala-hd.webp" alt="La sala di Alba Iulia: parete capitonné bianca con il logo, tavoli apparecchiati e il bancone della caffetteria" width="2074" height="1508" loading="lazy" decoding="async"></div>
        </figure>
        <div class="sala__shade" aria-hidden="true"></div>
        <div class="sala__text">
          <h2>Entrate pure.</h2>
          <p>La parete capitonné, i lampadari di cristallo, il bancone della caffetteria e la sala apparecchiata. Tutto sotto lo stesso tetto, dal mattino alla sera.</p>
        </div>
      </div>
    </div>
  </section>
"""

FOTO = [
    ("bancone.webp", "Il bancone con il titolare al lavoro"),
    ("sala.webp", "La sala con la parete capitonné e il logo"),
    ("caffe.webp", "Dolci al cioccolato e sfogliatine"),
    ("bar.webp", "Il bar con la macchina del caffè e le bottiglie"),
    ("piatto.webp", "Pranzo in sala"),
    ("ristorante.webp", "La sala con le vetrate verso il dehors"),
    ("gastronomia.webp", "Il banco della gastronomia"),
    ("insegna.webp", "L'insegna: dal 2004 famiglia Sbuciumelea"),
    ("banco.webp", "Un taglio di manzo al banco"),
    ("titolare.webp", "Il titolare"),
]


def carousel(h2="Un giro nel locale", lead="Trascina per girare, tocca una foto per ingrandirla."):
    items = "\n".join(f'        <button type="button" class="carousel__item"><img src="/img/{f}" alt="{e(a)}" width="800" height="600" loading="lazy" decoding="async"></button>' for f, a in FOTO)
    return f"""
  <section class="gallery" id="galleria-3d">
    <div class="wrap gallery__head">
      <h2>{e(h2)}</h2>
      <p>{e(lead)}</p>
    </div>
    <div class="carousel" id="carousel" tabindex="0" aria-roledescription="carosello" aria-label="Foto del locale. Usa le frecce per girare.">
      <div class="carousel__ring" id="ring">
{items}
      </div>
    </div>
    <div class="carousel__ctrl">
      <button type="button" class="round" id="prev" aria-label="Foto precedente">‹</button>
      <button type="button" class="round" id="next" aria-label="Foto successiva">›</button>
    </div>
  </section>
"""


def carta(c=None):
    """Il menu scuro della home. Con una sezione: solo quei piatti e le altre sezioni come link."""
    tabs = []
    for k in CATS:
        cur = ' aria-current="page"' if k is c else ""
        tabs.append(f'        <a class="carta__tab" href="/menu/{k["slug"]}"{cur}><span>{e(k["it"])}</span><small>{e(k["ro"])}</small></a>')
    shown = [c] if c else CATS
    panels = []
    for k in shown:
        dishes = []
        for d in k["dishes"]:
            q = f'<span class="dish__qty">{e(d["qty"])}</span>' if d["qty"] else ""
            dishes.append(f"""          <li class="dish reveal">
            <figure class="dish__media"><img src="/img/menu/{d["img"]}.webp" alt="{e(d["name"])}" width="800" height="600" loading="lazy" decoding="async"></figure>
            <div class="dish__body">
              <h3 class="dish__name">{e(d["name"])}{q}</h3>
              <p class="dish__desc">{e(d["desc"])}</p>
              <p class="dish__price">{euro(d["price"])}</p>
            </div>
          </li>""")
        head_ = "" if c else f'        <h2 class="carta__cat" id="{k["slug"]}">{e(k["it"])} <span>{e(k["ro"])}</span></h2>\n'
        more = "" if c else f'\n        <a class="carta__more" href="/menu/{k["slug"]}">Vai alla pagina {e(k["it"])} <span aria-hidden="true">→</span></a>'
        panels.append(f"""      <div class="carta__panel">
{head_}        <ul class="carta__grid">
{chr(10).join(dishes)}
        </ul>{more}
      </div>""")
    title = f'{e(c["it"])} <span class="carta__ro">{e(c["ro"])}</span>' if c else "Tutti i piatti"
    lead = e(c["intro"]) if c else "Cucina tradizionale romena, preparata ogni giorno dalla famiglia Sbuciumelea. Tocca una sezione per aprire la sua pagina."
    return f"""
  <section class="carta" id="piatti" aria-labelledby="carta-title">
    <div class="wrap">
      <header class="carta__head reveal">
        <div>
          <p class="carta__kicker">Meniu · Il menu</p>
          <h2 id="carta-title">{title}</h2>
        </div>
        <div class="carta__lead"><p>{lead}</p></div>
      </header>
      <nav class="carta__tabs" aria-label="Sezioni del menu">
{chr(10).join(tabs)}
      </nav>
{chr(10).join(panels)}
      <footer class="carta__foot">
        <p>Coperto {euro(DATA["coperto"])} a persona. Per allergie e intolleranze chiedi al personale.</p>
        <a class="btn btn--solid js-wa" {wa_attr("Ciao! Vorrei prenotare un tavolo da Alba Iulia.")}><svg aria-hidden="true"><use href="#wa"/></svg>Prenota un tavolo</a>
      </footer>
{credits([d for k in shown for d in k["dishes"]], "", "      ")}
    </div>
  </section>
"""


# ---------------------------------------------------------------- le pagine

def titolare():
    body = hero([("Il titolare", "/il-titolare")], "Dal 2004 · Famiglia Sbuciumelea", "Il titolare e la sua famiglia.",
                "Ogni giorno in sala e al banco, per accogliervi di persona. Alba Iulia è un locale di famiglia: chi vi accoglie è chi l'ha costruito, un pezzo alla volta.",
                "titolare.webp", "Il titolare di Alba Iulia, sorridente, nel suo locale",
                ("Il titolare", "Ogni giorno in sala e al banco, per accogliervi di persona."),
                [("Dal 2004", "Il primo", "locale romeno a Verona"), ("La famiglia", "Sbuciumelea", "in sala e al banco"), ("Su Google", "4,7", "su 5, 232 recensioni")],
                "Prenota su WhatsApp", "Ciao! Vorrei prenotare un tavolo da Alba Iulia.", pos="50% 30%")
    body += family("insegna.webp", "L'insegna ovale sulla parete capitonné: Caffetteria Alba Iulia Gastronomia, dal 2004 famiglia Sbuciumelea",
                   "Vent'anni fa abbiamo aperto la porta. Da allora non l'abbiamo più chiusa.",
                   ["Nel 2004 Alba Iulia è stato il primo locale di Verona dedicato alla gastronomia tipica romena, e il secondo in tutta Italia. Porta il nome della città simbolo della nostra terra, e l'abbiamo costruito come si costruisce una casa: un pezzo alla volta.",
                    "Oggi in sala e al banco c'è ancora la famiglia Sbuciumelea. Nel 2022 abbiamo inaugurato i nuovi spazi di caffetteria e gastronomia, con lo stesso spirito del primo giorno."],
                   [("2004", "Apre Alba Iulia in Via Luigi Prina"), ("2022", "Nuovi spazi di caffetteria e gastronomia"), ("Oggi", "Ristorante, caffè, gastronomia e macelleria")],
                   kicker="La nostra storia")
    body += services("Quello che ci chiedete di non cambiare mai", "Tre cose che la famiglia Sbuciumelea porta in tavola ogni giorno, dal 2004.", [
        ("menu/sarmale.webp", "Sarmale con mămăligă e smântână", "Ricette di famiglia", "Sarmale, mici, ciorbe e tochitură come si preparano a casa in Romania, accanto ai piatti della cucina italiana.", "/menu", None),
        ("banco.webp", "Un taglio di manzo al banco della macelleria", "Fatto da noi", "I mici sono di nostra produzione e la carne arriva dal nostro banco di macelleria, la stessa che potete portare a casa.", "/macelleria", None),
        ("bancone.webp", "Il bancone con il titolare al lavoro", "Accoglienza", "Porzioni generose e un'accoglienza che fa tornare: per tanti romeni a Verona è il sapore di casa.", None, None),
    ])
    body += REVIEWS + visit()
    return page("/il-titolare", [("Il titolare", "/il-titolare")], "Il titolare e la famiglia Sbuciumelea · Alba Iulia Verona",
                "La storia di Alba Iulia a Verona: dal 2004 la famiglia Sbuciumelea accoglie in sala e al banco, nel primo locale di gastronomia romena della città.",
                "/img/titolare-og.webp", body, "titolare.webp")


ANIME = [
    ("ristorante.webp", "Tavoli apparecchiati con tovaglie bianche nella sala del ristorante", "Ristorante",
     "Un menu tra le regioni romene e quelle italiane. Primi, secondi e contorni di nostra produzione, anche nel dehors.", "/menu", None),
    ("caffe.webp", "Vassoio di dolci al cioccolato e sfogliatine della pasticceria", "Caffetteria",
     "Colazione, pasticceria fresca e aperitivo. Dalle 9 del mattino, sette giorni su sette.", None, None),
    ("gastronomia.webp", "Il banco della gastronomia con orchidee e piante", "Gastronomia",
     "I nostri piatti pronti da portare via e un piccolo market di prodotti tipici romeni, moldavi e italiani.", None, None),
    ("macelleria.webp", "Taglio di carne bovina marezzata al banco", "Macelleria",
     "Carne fresca selezionata e salumi artigianali, tagliati al momento come li chiedi tu.", "/macelleria", None),
]


def locale():
    body = hero([("Il locale", "/il-locale")], "Via Luigi Prina 21 · Verona", "Un locale, quattro anime.",
                "La parete capitonné, i lampadari di cristallo, il bancone della caffetteria e la sala apparecchiata. Tutto sotto lo stesso tetto, dal mattino alla sera.",
                "sala-hd.webp", "La sala di Alba Iulia con la parete capitonné e il logo",
                ("Il locale", "Ristorante, caffetteria, gastronomia e macelleria."),
                [("Aperti", "7 giorni su 7", "dalle 9 alle 20"), ("Servizi", "Sala e dehors", "asporto e consegna"), ("Dal 2004", "Via Luigi Prina", "21, Verona")],
                "Prenota un tavolo", "Ciao! Vorrei prenotare un tavolo da Alba Iulia.", pos="40% 50%")
    body += SALA
    body += services("Quattro modi di stare a tavola con noi", "Un caffè con la brioche la mattina, il pranzo in sala, e prima di tornare a casa la carne per domani.", ANIME)
    body += family("bar.webp", "Il bar con la macchina del caffè e le bottiglie", "Una giornata da Alba Iulia",
                   ["Dalle 9 alle 20, tutti i giorni: il locale cambia con le ore, la famiglia resta la stessa."],
                   [("Mattina", "Caffè e pasticceria fresca al bancone"), ("Pranzo", "In sala o nel dehors, cucina romena e italiana"),
                    ("Pomeriggio", "Gastronomia, prodotti tipici e carne fresca al banco"), ("Sera", "L'aperitivo e i piatti pronti da portare a casa")],
                   link=("/galleria", "Guarda le foto del locale"), kicker="Dalle 9 alle 20")
    body += visit()
    return page("/il-locale", [("Il locale", "/il-locale")], "Il locale · Ristorante, caffetteria, gastronomia e macelleria a Verona",
                "Alba Iulia in Via Luigi Prina 21 a Verona: ristorante con dehors, caffetteria, gastronomia con prodotti tipici e macelleria, aperti tutti i giorni dalle 9 alle 20.",
                "/img/sala-hd.jpg", body, "sala-hd.webp")


def macelleria():
    msg = "Ciao! Vorrei ordinare dalla macelleria di Alba Iulia."
    body = hero([("Macelleria", "/macelleria")], "Macelleria e prodotti tipici", "Il banco della nostra macelleria.",
                "La stessa carne che cuciniamo in sala, pronta per la vostra cucina. Tagli freschi, macinato per i mici, salsicce e salumi artigianali, tagliati al momento come li chiedete.",
                "banco.webp", "Un taglio di manzo marezzato affettato a mano al banco della macelleria",
                ("La macelleria", "Tagliata al momento, come la chiedete voi."),
                [("Ogni giorno", "Carne fresca", "selezionata"), ("Da noi", "Salumi", "artigianali"), ("Ordini", "WhatsApp", "ritiro o consegna a domicilio")],
                "Ordina su WhatsApp", msg, pos="50% 50%")
    body += butcher("Macelleria e prodotti tipici",
                    "La stessa carne che cuciniamo in sala, pronta per la tua cucina. Tagli freschi, macinato per i mici, salsicce e salumi artigianali. E poi formaggi, conserve, dolci e bevande per una tavola romena o moldava.",
                    ["Carne fresca selezionata ogni giorno", "Salumi artigianali", "Prodotti tipici romeni, moldavi e italiani", "Asporto e consegna a domicilio"],
                    "macelleria.webp", "Taglio di carne bovina marezzata al banco", msg, "Ordina su WhatsApp")
    body += services("Cosa trovate al banco", "Dalla carne per la griglia ai prodotti per una tavola romena, moldava o italiana.", [
        ("menu/costata.webp", "Costata di manzo", "Carne fresca", "Tagli selezionati ogni giorno, preparati al momento come li chiedete.", None, None),
        ("menu/mici.webp", "Mici alla griglia con senape", "Per i mici", "Il macinato speziato per i mici, come lo usiamo nella nostra cucina.", None, None),
        ("menu/carnat.webp", "Salsiccia fresca alla griglia", "Salsicce e salumi", "Salsicce fresche e salumi artigianali, da cuocere o da affettare.", None, None),
        ("gastronomia.webp", "Il banco della gastronomia", "Prodotti tipici", "Formaggi, conserve, dolci e bevande romeni, moldavi e italiani.", None, None),
    ])
    body += family("insegna.webp", "L'insegna di Alba Iulia sulla parete capitonné", "Ditecelo su WhatsApp, al resto pensiamo noi.",
                   ["Ordinare è semplice: scrivete cosa vi serve, prepariamo l'ordine e lo ritirate in negozio oppure ve lo portiamo a casa."],
                   [("1", "Scrivete il taglio, il peso o quante persone siete"), ("2", "Tagliamo e confezioniamo la carne al momento"), ("3", "Ritiro in Via Luigi Prina 21 o consegna a domicilio")],
                   link=("/menu/grigliate", "Assaggiatela in sala: le grigliate"), kicker="Ordinare è semplice")
    body += visit(msg=msg)
    return page("/macelleria", [("Macelleria", "/macelleria")], "Macelleria e prodotti tipici romeni · Alba Iulia Verona",
                "La macelleria di Alba Iulia a Verona: carne fresca selezionata, macinato per i mici, salsicce, salumi artigianali e prodotti tipici romeni e moldavi. Ordini su WhatsApp, asporto e consegna.",
                "/img/banco.webp", body, "banco.webp")


GRIGLIA = ["sala-hd.webp", "bancone.webp", "titolare.webp", "caffe.webp", "bar.webp", "insegna.webp",
           "ristorante.webp", "piatto.webp", "gastronomia.webp", "banco.webp", "macelleria.webp", "sala.webp"]
ALT = dict(FOTO) | {"sala-hd.webp": "La sala con la parete capitonné, il logo e i tavoli apparecchiati", "macelleria.webp": "Carne bovina marezzata"}


def galleria():
    body = hero([("Galleria", "/galleria")], "Un giro nel locale", "Benvenuti da Alba Iulia.",
                "La sala, il bancone, la caffetteria, la gastronomia e la macelleria: le foto del nostro locale in Via Luigi Prina. Fate girare la giostra o toccate una foto per ingrandirla.",
                "bancone.webp", "Il bancone con il titolare al lavoro", ("La galleria", f"{len(GRIGLIA)} foto del nostro locale."),
                [("Sala", "Capitonné", "e lampadari di cristallo"), ("Bancone", "Caffetteria", "e aperitivo"), ("Banco", "Gastronomia", "e macelleria")],
                "Prenota un tavolo", "Ciao! Vorrei prenotare un tavolo da Alba Iulia.", pos="50% 35%")
    body += carousel()
    items = "\n".join(f"""      <li class="reveal"><button type="button" class="photo-grid__item" data-full="/img/{f}" aria-label="Ingrandisci: {e(ALT[f])}">
        <img src="/img/{f}" alt="{e(ALT[f])}" width="800" height="600" loading="lazy" decoding="async">
      </button></li>""" for f in GRIGLIA)
    body += f"""
  <section class="photo-grid-sec">
    <div class="wrap services__head reveal">
      <h2>Tutte le foto</h2>
      <p>Toccate una foto per vederla a schermo intero.</p>
    </div>
    <ul class="wrap photo-grid">
{items}
    </ul>
  </section>
"""
    body += visit()
    return page("/galleria", [("Galleria", "/galleria")], "Galleria fotografica · Alba Iulia Verona",
                "Le foto di Alba Iulia a Verona: la sala con la parete capitonné, il bancone della caffetteria, la gastronomia e la macelleria.",
                "/img/sala-hd.jpg", body, "bancone.webp")


def dove():
    body = hero([("Dove siamo", "/dove-siamo")], "Via Luigi Prina 21 · 37136 Verona", "Vi aspettiamo in Via Luigi Prina.",
                "Tutti i giorni dalle 9 alle 20. Per prenotare un tavolo, ordinare dalla macelleria o chiedere un'informazione, scriveteci su WhatsApp o chiamateci.",
                "insegna.webp", "L'insegna ovale di Alba Iulia sulla parete capitonné", ("Dove siamo", "Via Luigi Prina 21, Verona."),
                [("Aperti", "7 giorni su 7", "dalle 9 alle 20"), ("Telefono", "045 862 6014", "chiamateci"), ("WhatsApp", "345 696 7120", "per prenotare e ordinare")],
                "Scrivici su WhatsApp", "Ciao! Vorrei prenotare un tavolo da Alba Iulia.",
                second=f'<a class="btn btn--ghost btn--lg magnetic" href="{MAPS_DIR}" target="_blank" rel="noopener">Indicazioni stradali</a>', pos="50% 45%")
    body += visit("Orari e contatti", week=True)
    body += REVIEWS
    body += services("Prima di venire a trovarci", "Date un'occhiata al menu, al locale e alla macelleria.", [
        ("piatto.webp", "Pranzo in sala", "Il menu", "Antipasti, ciorbe, secondi, grigliate, contorni e dolci, con foto e prezzi.", "/menu", None),
        ("sala.webp", "La sala con la parete capitonné", "Il locale", "Ristorante, caffetteria, gastronomia e macelleria sotto lo stesso tetto.", "/il-locale", None),
        ("banco.webp", "Un taglio di manzo al banco", "La macelleria", "Carne fresca e prodotti tipici, con ordini su WhatsApp e consegna.", "/macelleria", None),
    ])
    return page("/dove-siamo", [("Dove siamo", "/dove-siamo")], "Dove siamo e orari · Alba Iulia, Via Luigi Prina 21 Verona",
                "Alba Iulia è in Via Luigi Prina 21, 37136 Verona. Aperti tutti i giorni dalle 9 alle 20. Telefono 045 862 6014, WhatsApp 345 696 7120.",
                "/img/insegna.webp", body, "insegna.webp")


def other_sections(current=None):
    cards = []
    for k in CATS:
        badge = "Sei qui" if k is current else plural(len(k["dishes"]))
        cards.append((f'menu/{k["dishes"][0]["img"]}.webp', k["dishes"][0]["name"], k["it"], f'{k["ro"]} · {price_range(k)}',
                      f'/menu/{k["slug"]}', badge))
    return cards


def menu_index():
    total = sum(len(k["dishes"]) for k in CATS)
    body = hero([("Menu", "/menu")], "Meniu · Il menu", "Il nostro menu.",
                f"Cucina tradizionale romena preparata ogni giorno dalla famiglia Sbuciumelea: {total} piatti tra antipasti, ciorbe, secondi, grigliate, contorni e dolci, con foto e prezzi.",
                "menu/tochitura.webp", "Tochitură con mămăligă, brânză e uovo", ("Il menu", "Ricette di famiglia, dal 2004."),
                [("Sezioni", str(len(CATS)), "dagli antipasti ai dolci"), ("Piatti", str(total), "con foto e prezzi"), ("Coperto", euro(DATA["coperto"]), "a persona")],
                "Prenota un tavolo", "Ciao! Vorrei prenotare un tavolo da Alba Iulia.", pos="50% 50%")
    body += services("Scegli una sezione", "Ogni sezione ha la sua pagina con tutti i piatti.", other_sections())
    body += carta()
    body += visit()
    ldm = {"@type": "Menu", "name": "Menu Alba Iulia", "url": SITE + "/menu", "inLanguage": "it",
           "hasMenuSection": [{"@type": "MenuSection", "name": f"{k['it']} / {k['ro']}", "url": f"{SITE}/menu/{k['slug']}",
                               "hasMenuItem": [{"@type": "MenuItem", "name": d["name"], "description": d["desc"],
                                                "offers": {"@type": "Offer", "price": d["price"], "priceCurrency": "EUR"}} for d in k["dishes"]]} for k in CATS]}
    return page("/menu", [("Menu", "/menu")], "Menu · Alba Iulia Verona, cucina tradizionale romena",
                f"Il menu di Alba Iulia a Verona: {total} piatti della tradizione romena tra antipasti, ciorbe, secondi, grigliate, contorni e dolci, con foto e prezzi.",
                "/img/menu/platou-alba-iulia.webp", body, "menu/tochitura.webp", ldm)


def category(c):
    path = f"/menu/{c['slug']}"
    n = len(c["dishes"])
    first = c["dishes"][0]
    body = hero([("Menu", "/menu"), (c["it"], path)], f"Meniu · {c['ro']}", c["it"] + ".",
                e(c["intro"]), f"menu/{first['img']}.webp", first["name"], (c["ro"], f"{plural(n)}, {price_range(c)}."),
                [("Piatti", str(n), "in questa sezione"), ("Prezzi", price_range(c), ""), ("Coperto", euro(DATA["coperto"]), "a persona")],
                "Prenota un tavolo", f"Ciao! Vorrei prenotare un tavolo da Alba Iulia. Ho visto il menu: {c['it']}.",
                second='<a class="btn btn--ghost btn--lg magnetic" href="#piatti">Vedi i piatti</a>', pos="50% 50%")
    body += carta(c)
    body += services("Le altre sezioni del menu", "Continuate a sfogliare: ogni sezione ha la sua pagina.", other_sections(c), link=("/menu", "Tutto il menu"))
    body += visit()
    ldc = {"@type": "MenuSection", "name": f"{c['it']} / {c['ro']}", "description": c["intro"], "url": SITE + path,
           "hasMenuItem": [{"@type": "MenuItem", "name": d["name"], "description": d["desc"], "image": f"{SITE}/img/menu/{d['img']}.webp",
                            "offers": {"@type": "Offer", "price": d["price"], "priceCurrency": "EUR"}} for d in c["dishes"]]}
    desc = f"{c['it']} del ristorante Alba Iulia a Verona: {', '.join(d['name'] for d in c['dishes'][:4])}{' e altri' if n > 4 else ''}. Cucina romena della famiglia Sbuciumelea, prezzi e foto."
    return page(path, [("Menu", "/menu"), (c["it"], path)], f"{c['it']} ({c['ro']}) · Menu Alba Iulia Verona", desc,
                f"/img/menu/{first['img']}.webp", body, f"menu/{first['img']}.webp", ldc, active="/menu")


def build_all():
    out = [("il-titolare.html", titolare()), ("il-locale.html", locale()), ("macelleria.html", macelleria()),
           ("galleria.html", galleria()), ("dove-siamo.html", dove()), ("menu/index.html", menu_index())]
    out += [(f"menu/{k['slug']}.html", category(k)) for k in CATS]
    return out
