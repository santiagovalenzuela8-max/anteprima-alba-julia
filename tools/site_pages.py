"""Le pagine interne del sito, con un impianto editoriale (come la rivista di un ristorante).

Stesso linguaggio della home (bordeaux e oro, capitonné, l'ovale del logo, Sorts Mill Goudy),
ma ogni pagina ha una composizione sua:
- /la-famiglia  titolo grande, ritratto ad arco con sigillo rotante, la storia con gli anni giganti
- /il-locale    sala in panoramica, quattro capitoli sfalsati, la giornata, nastro di foto
- /menu         indice delle sezioni con la foto che segue il mouse, e la carta "stampata"
- /menu/...     i piatti di una sezione con il prezzo nel sigillo
- /macelleria   apertura scura, il banco ad archi sfalsati, tre passi con i numeri giganti
- /galleria     mosaico di foto da ingrandire
- /dove-siamo   indirizzo in grande, orari con il giorno di oggi, mappa ad arco
In fondo a ogni pagina: l'invito a tavola e il link grande alla pagina successiva.
I testi riprendono solo informazioni vere del locale; si rigenera con python3 tools/build_site.py.
"""
import json

from build_site import CATS, DATA, SITE, SPRITE, WA, credits, e, euro, nav_links, plural, price_range

TEL = "tel:+390458626014"
MAPS_DIR = "https://www.google.com/maps/dir/?api=1&amp;destination=Via+Luigi+Prina+21+37136+Verona"
MAP_SRC = "https://maps.google.com/maps?q=Via%20Luigi%20Prina%2021%2C%2037136%20Verona&amp;z=16&amp;output=embed"
BOOK = "Ciao! Vorrei prenotare un tavolo da Alba Iulia."
RESTAURANT = {
    "@type": "Restaurant", "@id": SITE + "/#ristorante", "name": "Alba Iulia", "url": SITE + "/",
    "image": SITE + "/img/sala-hd.jpg", "telephone": "+39 045 862 6014",
    "servesCuisine": ["Romena", "Moldava", "Italiana"], "foundingDate": "2004",
    "address": {"@type": "PostalAddress", "streetAddress": "Via Luigi Prina, 21", "postalCode": "37136",
                "addressLocality": "Verona", "addressRegion": "VR", "addressCountry": "IT"},
    "openingHours": "Mo-Su 09:00-20:00",
    "aggregateRating": {"@type": "AggregateRating", "ratingValue": "4.7", "reviewCount": "232"},
}
# ordine delle pagine: numero nell'etichetta e "pagina successiva"
ORDER = [("/la-famiglia", "La famiglia", "titolare.webp"), ("/il-locale", "Il locale", "sala.webp"),
         ("/menu", "Il menu", "menu/tochitura.webp"), ("/macelleria", "La macelleria", "banco.webp"),
         ("/galleria", "La galleria", "bancone.webp"), ("/dove-siamo", "Dove siamo", "insegna.webp")]



def wa(msg):
    return f'href="{WA}" target="_blank" rel="noopener" data-msg="{e(msg)}"'


def img(src, alt="", cls="", lazy=True, extra=""):
    c = f' class="{cls}"' if cls else ""
    load = ' loading="lazy"' if lazy else ' fetchpriority="high"'
    return f'<img{c} src="/img/{src}" alt="{e(alt)}" width="800" height="600"{load} decoding="async"{extra}>'


def btn_wa(label, msg, cls="btn--solid"):
    return f'<a class="btn {cls} btn--lg magnetic js-wa" {wa(msg)}><svg aria-hidden="true"><use href="#wa"/></svg>{e(label)}</a>'


def btn_tel(cls="btn--ghost"):
    return f'<a class="btn {cls} btn--lg magnetic" href="{TEL}"><svg aria-hidden="true"><use href="#tel"/></svg>045 862 6014</a>'


# ---------------------------------------------------------------- cornice

def head(title, desc, path, og, ld, active, preload, dark=False):
    return f"""<!doctype html>
<html lang="it">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta name="theme-color" content="{'#1d0b0a' if dark else '#6e2a26'}">
<meta property="og:type" content="website">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:image" content="{SITE}{og}">
<meta property="og:url" content="{SITE}{path}">
<meta property="og:locale" content="it_IT">
<link rel="canonical" href="{SITE}{path}">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Sorts+Mill+Goudy:ital@0;1&family=Figtree:wght@400;500;600;700&display=swap">
<link rel="stylesheet" href="/style.css">
<link rel="preconnect" href="https://cdnjs.cloudflare.com" crossorigin>
<link rel="preload" as="image" href="{preload}" fetchpriority="high">
<script type="application/ld+json">
{json.dumps(ld, ensure_ascii=False, indent=1)}
</script>
</head>
<body class="page-inner{' page-dark' if dark else ''}">

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


def page(path, crumbs, title, desc, og, preload, body, extra_ld=None, active=None, dark=False):
    return head(title, desc, path, og, ld(path, crumbs, extra_ld), active or path, "/img/" + preload, dark) + body + FOOT


def crumbs_html(crumbs):
    out = ['<a href="/">Home</a>']
    for i, (n, h) in enumerate(crumbs):
        out.append(f'<span aria-current="page">{e(n)}</span>' if i == len(crumbs) - 1 else f'<a href="{h}">{e(n)}</a>')
    return '<nav class="crumbs" aria-label="Sei qui">' + '<span aria-hidden="true">/</span>'.join(out) + "</nav>"


def facts(items):
    return '<dl class="ed-facts">' + "".join(f"<div><dt>{e(a)}</dt><dd>{e(b)}</dd></div>" for a, b in items) + "</dl>"


def badge(text, uid):
    return f"""<svg class="ed-badge" viewBox="0 0 200 200" aria-hidden="true">
          <defs><path id="badge-{uid}" d="M100,100 m-74,0 a74,74 0 1,1 148,0 a74,74 0 1,1 -148,0"/></defs>
          <circle cx="100" cy="100" r="98"/>
          <text><textPath href="#badge-{uid}">{e(text)}</textPath></text>
          <ellipse cx="100" cy="100" rx="34" ry="20"/>
        </svg>"""


# ---------------------------------------------------------------- aperture (tre composizioni)

def hero_arch(crumbs, label, title, lead, pic, alt, actions, fx, ghost, badge_text, oval=False, dark=False, pos="50% 40%"):
    """Testo a sinistra, foto ad arco (o ovale) a destra con il filetto dorato e il sigillo rotante."""
    return f"""  <section class="ed-hero ed-hero--arch{' ed-hero--dark' if dark else ''}">
    <span class="ed-ghost" aria-hidden="true">{e(ghost)}</span>
    <div class="wrap ed-hero__grid">
      <div class="ed-hero__copy">
        {crumbs_html(crumbs)}
        <p class="ed-label">{e(label[1])}</p>
        <h1 class="ed-title ed-split">{title}</h1>
        <p class="ed-lead">{lead}</p>
        <div class="ed-actions">{actions}</div>
      </div>
      <figure class="ed-arch{' ed-arch--oval' if oval else ''}">
        <div class="ed-arch__img ed-img">{img(pic, alt, lazy=False, extra=f' style="object-position:{pos}"')}</div>
        {badge(badge_text, "a")}
      </figure>
    </div>
    <div class="wrap ed-hero__foot">{facts(fx)}</div>
  </section>
"""


def hero_wide(crumbs, label, title, lead, pic, alt, actions, ghost):
    """Titolo su tutta la larghezza, poi la foto in panoramica che scorre più lenta."""
    return f"""  <section class="ed-hero ed-hero--wide">
    <span class="ed-ghost" aria-hidden="true">{e(ghost)}</span>
    <div class="wrap">
      {crumbs_html(crumbs)}
      <p class="ed-label">{e(label[1])}</p>
      <h1 class="ed-title ed-title--xl ed-split">{title}</h1>
      <div class="ed-hero__row">
        <p class="ed-lead">{lead}</p>
        <div class="ed-actions">{actions}</div>
      </div>
      <figure class="ed-pano ed-img"><img src="/img/{pic}" alt="{e(alt)}" width="800" height="600" fetchpriority="high" decoding="async" data-speed="-12"></figure>
    </div>
  </section>
"""


def hero_center(crumbs, label, title, lead, actions, pics, ghost):
    """Titolo al centro, tre foto sospese intorno che si muovono a velocità diverse."""
    fl = "\n".join(f'      <figure class="ed-float ed-float--{i + 1}" data-speed="{s}">{img(p, a, lazy=False)}</figure>'
                   for i, ((p, a), s) in enumerate(zip(pics, (-18, -30, -10))))
    return f"""  <section class="ed-hero ed-hero--center">
    <span class="ed-ghost" aria-hidden="true">{e(ghost)}</span>
{fl}
    <div class="wrap ed-hero__center">
      {crumbs_html(crumbs)}
      <p class="ed-label ed-label--center">{e(label[1])}</p>
      <h1 class="ed-title ed-split">{title}</h1>
      <p class="ed-lead">{lead}</p>
      <div class="ed-actions">{actions}</div>
    </div>
  </section>
"""


# ---------------------------------------------------------------- blocchi

def sec_head(label, h2, intro=None, center=False):
    i = f'\n        <p class="ed-intro">{intro}</p>' if intro else ""
    return f"""      <header class="ed-head{' ed-head--center' if center else ''}">
        <p class="ed-label"><span>—</span>{e(label)}</p>
        <h2 class="ed-h2 ed-split">{h2}</h2>{i}
      </header>"""


def quote(text, meta=None, link=None):
    m = f'\n      <p class="ed-quote__meta">{meta}</p>' if meta else ""
    a = ""
    if link:
        ext = ' target="_blank" rel="noopener"' if link[0].startswith("http") else ""
        a = f'\n      <a class="ed-quote__link" href="{link[0]}"{ext}>{e(link[1])} <span aria-hidden="true">→</span></a>'
    return f"""
  <section class="ed-quote">
    <svg class="ed-quote__logo" viewBox="0 0 240 140" aria-hidden="true"><ellipse cx="120" cy="70" rx="116" ry="66" fill="none" stroke="currentColor" stroke-width=".7"/><ellipse cx="120" cy="70" rx="108" ry="59" fill="none" stroke="currentColor" stroke-width=".35"/></svg>
    <div class="wrap">
      <p class="ed-quote__text ed-split">{text}</p>{m}{a}
    </div>
  </section>
"""


def cta(msg=BOOK, title="Vi aspettiamo a <em>tavola.</em>", lead="Via Luigi Prina 21, Verona · tutti i giorni dalle 9 alle 20"):
    return f"""
  <section class="ed-cta">
    <svg class="ed-cta__logo" viewBox="0 0 240 140" aria-hidden="true"><ellipse cx="120" cy="70" rx="116" ry="66" fill="none" stroke="currentColor" stroke-width=".7"/><ellipse cx="120" cy="70" rx="108" ry="59" fill="none" stroke="currentColor" stroke-width=".35"/></svg>
    <div class="wrap ed-cta__inner">
      <p class="ed-label ed-label--light ed-label--center"><span>—</span>Prenotazioni e ordini</p>
      <h2 class="ed-split">{title}</h2>
      <p>{lead}</p>
      <div class="ed-actions ed-actions--center">
        {btn_wa("Scrivici su WhatsApp", msg, "btn--gold")}
        {btn_tel("btn--line")}
      </div>
    </div>
  </section>
"""


def next_link(href, title, pic, label="Pagina successiva"):
    return f"""
  <section class="ed-next-sec">
    <a class="wrap ed-next" href="{href}">
      <span class="ed-next__label">{e(label)}</span>
      <span class="ed-next__title">{e(title)} <i aria-hidden="true">→</i></span>
      <span class="ed-next__img">{img(pic)}</span>
    </a>
  </section>
"""


def next_page(path):
    paths = [p for p, *_ in ORDER]
    p, t, pic = ORDER[(paths.index(path) + 1) % len(ORDER)]
    return next_link(p, t, pic)


def marquee(pics):
    """Nastro di foto che scorre da solo; si ferma sotto il mouse o il dito e si può trascinare."""
    nodrag = ' draggable="false"'
    row = "".join(f"<li>{img(p, a, extra=nodrag)}</li>" for p, a in pics)
    return f"""
  <section class="ed-marquee" aria-label="Foto del locale">
    <div class="ed-marquee__view" tabindex="0" aria-label="Foto del locale: trascina o scorri per sfogliarle">
      <ul class="ed-marquee__track">{row}{row.replace('alt="', 'aria-hidden="true" alt="')}</ul>
    </div>
    <div class="wrap ed-marquee__ctrl">
      <p>Trascinate le foto o usate le frecce</p>
      <button type="button" class="round round--dark" data-dir="-1" aria-label="Foto precedenti">‹</button>
      <button type="button" class="round round--dark" data-dir="1" aria-label="Foto successive">›</button>
    </div>
  </section>
"""


# ---------------------------------------------------------------- /la-famiglia

def titolare():
    path = "/la-famiglia"
    body = hero_arch([("La famiglia", path)], ("", "La famiglia"), "La famiglia dietro il <em>bancone.</em>",
                     "Ogni giorno in sala e al banco, per accogliervi di persona. Alba Iulia è un locale di famiglia: chi vi accoglie è chi l'ha costruito, un pezzo alla volta.",
                     "titolare.webp", "Il titolare di Alba Iulia, sorridente, nel suo locale",
                     btn_wa("Prenota un tavolo", BOOK) + btn_tel(),
                     [("Dal", "2004"), ("Famiglia", "Sbuciumelea"), ("Su Google", "4,7 / 5")], "Familia",
                     "FAMIGLIA SBUCIUMELEA · DAL 2004 · VERONA · ", pos="50% 28%")
    story = [
        ("2004", "Si apre la porta", "Alba Iulia nasce in Via Luigi Prina: il primo locale di Verona dedicato alla gastronomia tipica romena, e il secondo in tutta Italia. Porta il nome della città simbolo della nostra terra.", "insegna.webp", "L'insegna di Alba Iulia sulla parete capitonné"),
        ("2022", "I nuovi spazi", "Inauguriamo la nuova caffetteria e la gastronomia: il bancone, la parete capitonné, i lampadari di cristallo. Con lo stesso spirito del primo giorno.", "bancone.webp", "Il bancone della caffetteria"),
        ("Oggi", "Una casa per tutti", "Ristorante, caffetteria, gastronomia e macelleria sotto lo stesso tetto, aperti sette giorni su sette. In sala e al banco c'è ancora la famiglia Sbuciumelea.", "sala.webp", "La sala con la parete capitonné"),
    ]
    items = "\n".join(f"""        <li class="ed-story__item">
          <span class="ed-story__year" data-speed="-8">{y}</span>
          <div class="ed-story__text reveal"><h3>{e(h)}</h3><p>{e(t)}</p></div>
          <figure class="ed-story__img ed-img">{img(p, a)}</figure>
        </li>""" for y, h, t, p, a in story)
    body += f"""
  <section class="ed-sec">
    <div class="wrap">
{sec_head("La nostra storia", "Vent'anni fa abbiamo aperto la porta. Da allora non l'abbiamo più <em>chiusa.</em>", "L'abbiamo costruito come si costruisce una casa: un pezzo alla volta.")}
      <ol class="ed-story">
{items}
      </ol>
    </div>
  </section>
"""
    body += quote("Per tanti romeni a Verona è il sapore di casa. Per tanti veronesi, la scoperta di una cucina <em>nuova.</em>",
                  "4,7 su 5 · 232 recensioni su Google",
                  ("https://www.google.com/maps/search/?api=1&amp;query=Alba+Iulia+Via+Luigi+Prina+21+Verona", "Leggi le recensioni"))
    vals = [("Ricette di famiglia", "Sarmale, mici, ciorbe e tochitură come si preparano a casa in Romania, accanto ai piatti della cucina italiana."),
            ("Fatto da noi", "I mici sono di nostra produzione e la carne arriva dal nostro banco di macelleria: la stessa che potete portare a casa."),
            ("Accoglienza", "Porzioni generose e un'accoglienza che fa tornare. Chi vi serve al tavolo è chi il locale l'ha costruito.")]
    li = "\n".join(f'        <li class="reveal"><h3>{e(h)}</h3><p>{e(t)}</p></li>' for i, (h, t) in enumerate(vals))
    body += f"""
  <section class="ed-sec ed-sec--cream">
    <div class="wrap">
{sec_head("Come lavoriamo", "Quello che ci chiedete di non cambiare <em>mai.</em>")}
      <ol class="ed-values">
{li}
      </ol>
    </div>
  </section>
"""
    body += cta() + next_page(path)
    return page(path, [("La famiglia", path)], "La famiglia Sbuciumelea · Alba Iulia Verona",
                "La storia di Alba Iulia a Verona: dal 2004 la famiglia Sbuciumelea accoglie in sala e al banco, nel primo locale di gastronomia romena della città.",
                "/img/titolare-og.webp", "titolare.webp", body)


# ---------------------------------------------------------------- /il-locale

ANIME = [
    ("ristorante.webp", "La sala del ristorante con le tovaglie bianche e le vetrate", "Ristorante",
     "Un menu tra le regioni romene e quelle italiane: ciorbe, sarmale, grigliate e contorni di nostra produzione, in sala o nel dehors.",
     ("Sala", "Dehors", "Cucina romena e italiana"), ("/menu", "Sfoglia il menu")),
    ("caffe.webp", "Dolci al cioccolato e sfogliatine della pasticceria", "Caffetteria",
     "Colazione con caffè e pasticceria fresca, poi il bancone si prepara per l'aperitivo. Dalle 9 del mattino, sette giorni su sette.",
     ("Colazione", "Pasticceria", "Aperitivo"), None),
    ("gastronomia.webp", "Il banco della gastronomia con orchidee e piante", "Gastronomia",
     "I nostri piatti pronti da portare via e un piccolo market di prodotti tipici romeni, moldavi e italiani.",
     ("Piatti pronti", "Prodotti tipici", "Asporto"), None),
    ("macelleria.webp", "Taglio di carne bovina marezzata al banco", "Macelleria",
     "Carne fresca selezionata e salumi artigianali, tagliati al momento come li chiedete. La stessa carne che cuciniamo in sala.",
     ("Carne fresca", "Salumi", "Consegna a domicilio"), ("/macelleria", "Scopri la macelleria")),
]


def locale():
    path = "/il-locale"
    body = hero_wide([("Il locale", path)], ("", "Il locale"), "Un locale, quattro <em>anime.</em>",
                     "La parete capitonné, i lampadari di cristallo, il bancone della caffetteria e la sala apparecchiata. Tutto sotto lo stesso tetto, dal mattino alla sera.",
                     "sala-hd.webp", "La sala di Alba Iulia: parete capitonné bianca con il logo, tavoli apparecchiati e il bancone della caffetteria",
                     btn_wa("Prenota un tavolo", BOOK) + btn_tel(), "Acasă")
    ch = []
    for i, (p, a, t, txt, tags, link) in enumerate(ANIME):
        tg = "".join(f"<li>{e(x)}</li>" for x in tags)
        lk = f'\n          <a class="ed-arrow" href="{link[0]}">{e(link[1])} <span aria-hidden="true">→</span></a>' if link else ""
        ch.append(f"""      <article class="ed-chapter{' ed-chapter--rev' if i % 2 else ''}">
        <figure class="ed-chapter__img ed-img">{img(p, a, extra=' data-speed="-6"')}</figure>
        <div class="ed-chapter__copy reveal">
          <h3 class="ed-h3">{e(t)}</h3>
          <p>{e(txt)}</p>
          <ul class="ed-tags">{tg}</ul>{lk}
        </div>
      </article>""")
    body += f"""
  <section class="ed-sec">
    <div class="wrap">
{sec_head("Quattro anime", "Quattro modi di stare a tavola con <em>noi.</em>", "Un caffè con la brioche la mattina, il pranzo in sala, e prima di tornare a casa la carne per domani.")}
      <div class="ed-chapters">
{chr(10).join(ch)}
      </div>
    </div>
  </section>
"""
    day = [("Mattina", "Il caffè e la pasticceria fresca al bancone della caffetteria."),
           ("Pranzo", "In sala o nel dehors, con la cucina romena e quella italiana."),
           ("Pomeriggio", "La gastronomia, i prodotti tipici e la carne fresca al banco."),
           ("Sera", "L'aperitivo al bancone e i piatti pronti da portare a casa.")]
    li = "\n".join(f'        <li class="reveal"><b>{e(h)}</b><p>{e(t)}</p></li>' for h, t in day)
    body += f"""
  <section class="ed-day">
    <div class="wrap">
{sec_head("Una giornata da Alba Iulia", "Dalle 9 alle 20, tutti i <em>giorni.</em>", "Il locale cambia con le ore, la famiglia resta la stessa.")}
      <ol class="ed-day__line">
{li}
      </ol>
    </div>
  </section>
"""
    body += marquee([("bancone.webp", "Il bancone"), ("caffe.webp", "La pasticceria"), ("insegna.webp", "L'insegna"),
                     ("ristorante.webp", "La sala"), ("bar.webp", "Il bar"), ("gastronomia.webp", "La gastronomia"),
                     ("piatto.webp", "Pranzo in sala"), ("sala.webp", "La parete capitonné")])
    body += cta() + next_page(path)
    return page(path, [("Il locale", path)], "Il locale · Ristorante, caffetteria, gastronomia e macelleria a Verona",
                "Alba Iulia in Via Luigi Prina 21 a Verona: ristorante con dehors, caffetteria, gastronomia con prodotti tipici e macelleria, aperti tutti i giorni dalle 9 alle 20.",
                "/img/sala-hd.jpg", "sala-hd.webp", body)


# ---------------------------------------------------------------- menu

def index_rows(current=None):
    rows = []
    for i, k in enumerate(CATS):
        cur = ' aria-current="page"' if k is current else ""
        pic = f'menu/{k["dishes"][0]["img"]}.webp'
        rows.append(f"""        <li><a class="ed-index__row" href="/menu/{k["slug"]}" data-img="/img/{pic}"{cur}>
          <span class="ed-index__thumb">{img(pic, k["dishes"][0]["name"])}</span>
          <span class="ed-index__name">{e(k["it"])} <em>{e(k["ro"])}</em></span>
          <span class="ed-index__meta">{plural(len(k["dishes"]))}<br>{price_range(k)}</span>
          <span class="ed-index__arrow" aria-hidden="true">→</span>
        </a></li>""")
    return f"""      <ul class="ed-index">
{chr(10).join(rows)}
      </ul>
      <div class="ed-follow" aria-hidden="true"><img alt=""></div>"""


def card(cats, title, sub):
    secs = []
    for k in cats:
        items = []
        for d in k["dishes"]:
            q = f' <i>· {e(d["qty"])}</i>' if d["qty"] else ""
            items.append(f"""            <li class="ed-item">
              {img("menu/" + d["img"] + ".webp", d["name"])}
              <div>
                <p class="ed-item__line"><span class="ed-item__name">{e(d["name"])}</span><span class="ed-item__dots" aria-hidden="true"></span><span class="ed-item__price">{euro(d["price"])}</span></p>
                <p class="ed-item__desc">{e(d["desc"])}{q}</p>
              </div>
            </li>""")
        more = "" if len(cats) == 1 else f'\n          <a class="ed-card__more" href="/menu/{k["slug"]}">Vedi le foto dei piatti <span aria-hidden="true">→</span></a>'
        secs.append(f"""        <section class="ed-card__sec">
          <h3>{e(k["it"])} <em>{e(k["ro"])}</em></h3>
          <ul>
{chr(10).join(items)}
          </ul>{more}
        </section>""")
    return f"""      <div class="ed-card reveal">
        <header class="ed-card__head">
          <svg class="ed-card__logo" aria-hidden="true"><use href="#logo"/></svg>
          <p class="ed-label ed-label--center"><span>—</span>{e(sub)}</p>
          <h2>{title}</h2>
        </header>
        <div class="ed-card__cols{' ed-card__cols--one' if len(cats) == 1 else ''}">
{chr(10).join(secs)}
        </div>
        <p class="ed-card__foot">Coperto {euro(DATA["coperto"])} a persona · Per allergie e intolleranze chiedete al personale</p>
      </div>"""


def menu_index():
    path = "/menu"
    total = sum(len(k["dishes"]) for k in CATS)
    body = hero_center([("Menu", path)], ("", "Il menu"), "Il nostro <em>menu.</em>",
                       f"Cucina tradizionale romena preparata ogni giorno dalla famiglia Sbuciumelea: {total} piatti tra antipasti, ciorbe, secondi, grigliate, contorni e dolci.",
                       btn_wa("Prenota un tavolo", BOOK) + '<a class="btn btn--ghost btn--lg magnetic" href="#carta">Leggi la carta</a>',
                       [("menu/sarmale.webp", "Sarmale con mămăligă"), ("menu/mici.webp", "Mici alla griglia"), ("menu/papanasi.webp", "Papanași")], "Meniu")
    body += f"""
  <section class="ed-sec ed-sec--cream" id="carta">
    <div class="wrap">
{card(CATS, "La <em>carta</em>", "Alba Iulia · dal 2004")}
{credits([d for k in CATS for d in k["dishes"]], " ed-credits", "      ")}
    </div>
  </section>
"""
    body += cta() + next_page(path)
    ldm = {"@type": "Menu", "name": "Menu Alba Iulia", "url": SITE + path, "inLanguage": "it",
           "hasMenuSection": [{"@type": "MenuSection", "name": f"{k['it']} / {k['ro']}", "url": f"{SITE}/menu/{k['slug']}",
                               "hasMenuItem": [{"@type": "MenuItem", "name": d["name"], "description": d["desc"],
                                                "offers": {"@type": "Offer", "price": d["price"], "priceCurrency": "EUR"}} for d in k["dishes"]]} for k in CATS]}
    return page(path, [("Menu", path)], "Menu · Alba Iulia Verona, cucina tradizionale romena",
                f"Il menu di Alba Iulia a Verona: {total} piatti della tradizione romena tra antipasti, ciorbe, secondi, grigliate, contorni e dolci, con foto e prezzi.",
                "/img/menu/platou-alba-iulia.webp", "menu/sarmale.webp", body, ldm)


def category(i, c):
    path = f"/menu/{c['slug']}"
    n = len(c["dishes"])
    first = c["dishes"][0]
    body = hero_arch([("Menu", "/menu"), (c["it"], path)], ("", "Il menu"), e(c["it"]) + ".",
                     e(c["intro"]), f"menu/{first['img']}.webp", first["name"],
                     btn_wa("Prenota un tavolo", f"Ciao! Vorrei prenotare un tavolo da Alba Iulia. Ho visto il menu: {c['it']}.") +
                     '<a class="btn btn--ghost btn--lg magnetic" href="#piatti">Vedi i piatti</a>',
                     [("Piatti", str(n)), ("Prezzi", price_range(c)), ("Coperto", euro(DATA["coperto"]))], c["ro"],
                     f"{c['ro'].upper()} · ALBA IULIA · VERONA · ", oval=True, pos="50% 50%")
    tiles = []
    for d in c["dishes"]:
        q = f'<p class="ed-dish__qty">{e(d["qty"])}</p>' if d["qty"] else ""
        tiles.append(f"""        <li class="ed-dish reveal">
          <figure class="ed-dish__img"><span class="ed-dish__frame">{img("menu/" + d["img"] + ".webp", d["name"])}</span><span class="ed-seal">{euro(d["price"])}</span></figure>
          <h3>{e(d["name"])}</h3>
          {q}<p class="ed-dish__desc">{e(d["desc"])}</p>
        </li>""")
    body += f"""
  <section class="ed-sec" id="piatti">
    <div class="wrap">
{sec_head(c["ro"], f"{plural(n).capitalize()}, da gustare in sala o da portare <em>via.</em>")}
      <ul class="ed-dishes ed-dishes--{min(n, 3)}">
{chr(10).join(tiles)}
      </ul>
{credits(c["dishes"], " ed-credits", "      ")}
    </div>
  </section>

  <section class="ed-sec ed-sec--cream">
    <div class="wrap">
{sec_head("Il menu", "Le altre <em>sezioni.</em>")}
{index_rows(c)}
    </div>
  </section>
"""
    nxt = CATS[(i + 1) % len(CATS)]
    body += cta(f"Ciao! Vorrei prenotare un tavolo da Alba Iulia. Ho visto il menu: {c['it']}.")
    body += next_link(f"/menu/{nxt['slug']}", nxt["it"], f"menu/{nxt['dishes'][0]['img']}.webp", "Sezione successiva")
    ldc = {"@type": "MenuSection", "name": f"{c['it']} / {c['ro']}", "description": c["intro"], "url": SITE + path,
           "hasMenuItem": [{"@type": "MenuItem", "name": d["name"], "description": d["desc"], "image": f"{SITE}/img/menu/{d['img']}.webp",
                            "offers": {"@type": "Offer", "price": d["price"], "priceCurrency": "EUR"}} for d in c["dishes"]]}
    desc = f"{c['it']} del ristorante Alba Iulia a Verona: {', '.join(d['name'] for d in c['dishes'][:4])}{' e altri' if n > 4 else ''}. Cucina romena della famiglia Sbuciumelea, prezzi e foto."
    return page(path, [("Menu", "/menu"), (c["it"], path)], f"{c['it']} ({c['ro']}) · Menu Alba Iulia Verona", desc,
                f"/img/menu/{first['img']}.webp", f"menu/{first['img']}.webp", body, ldc, active="/menu")


# ---------------------------------------------------------------- /macelleria

def macelleria():
    path = "/macelleria"
    msg = "Ciao! Vorrei ordinare dalla macelleria di Alba Iulia."
    body = hero_arch([("Macelleria", path)], ("", "La macelleria"), "Tagliata al momento, come la <em>chiedete voi.</em>",
                     "La stessa carne che cuciniamo in sala, pronta per la vostra cucina. Tagli freschi, macinato per i mici, salsicce e salumi artigianali.",
                     "banco.webp", "Un taglio di manzo marezzato affettato a mano al banco della macelleria",
                     btn_wa("Ordina su WhatsApp", msg, "btn--gold") + btn_tel("btn--line"),
                     [("Ogni giorno", "Carne fresca"), ("Da noi", "Salumi artigianali"), ("Ordini", "Ritiro o consegna")], "Măcelărie",
                     "MACELLERIA · PRODOTTI TIPICI · ALBA IULIA · ", dark=True, pos="50% 50%")
    prods = [("menu/costata.webp", "Costata di manzo", "Carne fresca", "Tagli selezionati ogni giorno, preparati al momento come li chiedete."),
             ("menu/mici.webp", "Mici alla griglia con senape", "Per i mici", "Il macinato speziato per i mici, come lo usiamo nella nostra cucina."),
             ("menu/carnat.webp", "Salsiccia fresca alla griglia", "Salsicce e salumi", "Salsicce fresche e salumi artigianali, da cuocere o da affettare."),
             ("gastronomia.webp", "Il banco della gastronomia", "Prodotti tipici", "Formaggi, conserve, dolci e bevande romeni, moldavi e italiani.")]
    li = "\n".join(f"""        <li>
          <figure class="ed-img">{img(p, a)}</figure>
          <div class="reveal"><h3>{e(h)}</h3><p>{e(t)}</p></div>
        </li>""" for i, (p, a, h, t) in enumerate(prods))
    body += f"""
  <section class="ed-sec">
    <div class="wrap">
{sec_head("Al banco", "Dalla griglia alla tavola di <em>casa.</em>", "La carne per la griglia, il macinato per i mici e i prodotti per una tavola romena, moldava o italiana.")}
      <ul class="ed-products">
{li}
      </ul>
    </div>
  </section>
"""
    body += quote("La stessa carne che cuciniamo in sala, pronta per la vostra <em>cucina.</em>", "Carne fresca selezionata ogni giorno · Salumi artigianali")
    steps = [("Scrivete cosa vi serve", "Il taglio, il peso, quante persone siete: un messaggio su WhatsApp o una telefonata."),
             ("Prepariamo l'ordine", "La carne viene tagliata e confezionata al momento, come la chiedete."),
             ("Ritiro o consegna", "Passate in Via Luigi Prina 21 oppure ve la portiamo a domicilio.")]
    li = "\n".join(f'        <li class="reveal"><b>{i + 1}</b><h3>{e(h)}</h3><p>{e(t)}</p></li>' for i, (h, t) in enumerate(steps))
    body += f"""
  <section class="ed-sec ed-sec--cream">
    <div class="wrap">
{sec_head("Ordinare è semplice", "Ditecelo su WhatsApp, al resto pensiamo <em>noi.</em>")}
      <ol class="ed-steps">
{li}
      </ol>
      <p class="ed-center reveal">{btn_wa("Ordina su WhatsApp", msg)}</p>
    </div>
  </section>
"""
    body += cta(msg, "La carne per domani, <em>oggi.</em>", "Ordini su WhatsApp · ritiro in Via Luigi Prina 21 o consegna a domicilio") + next_page(path)
    return page(path, [("Macelleria", path)], "Macelleria e prodotti tipici romeni · Alba Iulia Verona",
                "La macelleria di Alba Iulia a Verona: carne fresca selezionata, macinato per i mici, salsicce, salumi artigianali e prodotti tipici romeni e moldavi. Ordini su WhatsApp, asporto e consegna.",
                "/img/banco.webp", "banco.webp", body, dark=True)


# ---------------------------------------------------------------- /galleria

FOTO = [("sala-hd.webp", "La sala con la parete capitonné, il logo e i tavoli apparecchiati"),
        ("bancone.webp", "Il bancone con il titolare al lavoro"), ("titolare.webp", "Il titolare nel suo locale"),
        ("caffe.webp", "Dolci al cioccolato e sfogliatine della caffetteria"), ("bar.webp", "Il bar con la macchina del caffè e le bottiglie"),
        ("insegna.webp", "L'insegna: dal 2004 famiglia Sbuciumelea"), ("ristorante.webp", "La sala con le vetrate verso il dehors"),
        ("piatto.webp", "Pranzo in sala"), ("gastronomia.webp", "Il banco della gastronomia"),
        ("banco.webp", "Un taglio di manzo al banco della macelleria"), ("macelleria.webp", "Carne bovina marezzata"),
        ("sala.webp", "La sala e il logo sulla parete capitonné")]


def galleria():
    path = "/galleria"
    body = hero_center([("Galleria", path)], ("", "La galleria"), "Un giro nel <em>locale.</em>",
                       "La sala, il bancone, la caffetteria, la gastronomia e la macelleria. Toccate una foto per vederla a schermo intero.",
                       btn_wa("Prenota un tavolo", BOOK),
                       [("caffe.webp", "La pasticceria"), ("bancone.webp", "Il bancone"), ("insegna.webp", "L'insegna")], "Galerie")
    tiles = "\n".join(f"""        <li class="ed-bento__item"><button type="button" class="ed-bento__btn ed-img" data-full="/img/{p}" aria-label="Ingrandisci: {e(a)}">{img(p, a)}</button></li>""" for p, a in FOTO)
    body += f"""
  <section class="ed-sec ed-sec--tight">
    <div class="wrap">
      <ul class="ed-bento">
{tiles}
      </ul>
    </div>
  </section>
"""
    body += cta() + next_page(path)
    return page(path, [("Galleria", path)], "Galleria fotografica · Alba Iulia Verona",
                "Le foto di Alba Iulia a Verona: la sala con la parete capitonné, il bancone della caffetteria, la gastronomia e la macelleria.",
                "/img/sala-hd.jpg", "caffe.webp", body)


# ---------------------------------------------------------------- /dove-siamo

def dove():
    path = "/dove-siamo"
    giorni = ["Lunedì", "Martedì", "Mercoledì", "Giovedì", "Venerdì", "Sabato", "Domenica"]
    hours = "\n".join(f'            <li data-day="{i + 1}"><span>{g}</span><span>09:00 – 20:00</span></li>' for i, g in enumerate(giorni))
    body = hero_arch([("Dove siamo", path)], ("", "Dove siamo"), "Vi aspettiamo in Via <em>Luigi Prina.</em>",
                     "Tutti i giorni dalle 9 alle 20. Per prenotare un tavolo, ordinare dalla macelleria o chiedere un'informazione, scriveteci o chiamateci.",
                     "insegna.webp", "L'insegna ovale di Alba Iulia sulla parete capitonné",
                     btn_wa("Scrivici su WhatsApp", BOOK) + f'<a class="btn btn--ghost btn--lg magnetic" href="{MAPS_DIR}" target="_blank" rel="noopener">Indicazioni stradali</a>',
                     [("Aperti", "7 giorni su 7"), ("Orario", "09:00 – 20:00"), ("Servizi", "Sala, dehors, asporto")], "Verona",
                     "VIA LUIGI PRINA 21 · 37136 VERONA · ", pos="50% 45%")
    body += f"""
  <section class="ed-sec">
    <div class="wrap ed-where">
      <div class="ed-where__info">
        <p class="ed-label"><span>—</span>Indirizzo</p>
        <p class="ed-where__addr ed-split">Via Luigi Prina, <em>21</em></p>
        <p class="ed-where__city">37136 Verona</p>
        <p class="ed-open" id="open-status" aria-live="polite"></p>
        <div class="ed-where__block reveal">
          <h2 class="ed-where__h">Orari</h2>
          <ul class="ed-hours">
{hours}
          </ul>
        </div>
        <div class="ed-where__block reveal">
          <h2 class="ed-where__h">Contatti</h2>
          <a class="ed-contact js-wa" {wa(BOOK)}><span>WhatsApp</span><b>345 696 7120</b><i aria-hidden="true">→</i></a>
          <a class="ed-contact" href="{TEL}"><span>Telefono</span><b>045 862 6014</b><i aria-hidden="true">→</i></a>
          <a class="ed-contact" href="https://www.facebook.com/albajuliaverona/" target="_blank" rel="noopener"><span>Facebook</span><b>albajuliaverona</b><i aria-hidden="true">→</i></a>
          <a class="ed-contact" href="{MAPS_DIR}" target="_blank" rel="noopener"><span>Indicazioni</span><b>Apri in Google Maps</b><i aria-hidden="true">→</i></a>
        </div>
      </div>
      <div class="ed-where__map ed-img">
        <iframe title="Mappa: Alba Iulia, Via Luigi Prina 21, Verona" src="{MAP_SRC}" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>
      </div>
    </div>
  </section>
"""
    body += quote("Sala, dehors, asporto e consegna a <em>domicilio.</em>", "Ristorante · Caffetteria · Gastronomia · Macelleria", ("/il-locale", "Scopri il locale"))
    body += next_page(path)
    return page(path, [("Dove siamo", path)], "Dove siamo e orari · Alba Iulia, Via Luigi Prina 21 Verona",
                "Alba Iulia è in Via Luigi Prina 21, 37136 Verona. Aperti tutti i giorni dalle 9 alle 20. Telefono 045 862 6014, WhatsApp 345 696 7120.",
                "/img/insegna.webp", "insegna.webp", body)


def build_all():
    out = [("la-famiglia.html", titolare()), ("il-locale.html", locale()), ("macelleria.html", macelleria()),
           ("galleria.html", galleria()), ("dove-siamo.html", dove()), ("menu/index.html", menu_index())]
    out += [(f"menu/{k['slug']}.html", category(i, k)) for i, k in enumerate(CATS)]
    return out
