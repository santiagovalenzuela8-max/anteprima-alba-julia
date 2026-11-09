"""Le pagine della barra di navigazione (tranne /menu, che sta in build_site.py).

Ogni funzione restituisce (percorso del file, html). I testi riprendono solo informazioni
vere del locale: se qualcosa cambia (orari, servizi, storia) si corregge qui e si rilancia
python3 tools/build_site.py.
"""
from build_site import FOOT, SITE, WA, cta, e, head

RESTAURANT = {
    "@type": "Restaurant", "@id": SITE + "/#ristorante", "name": "Alba Iulia", "url": SITE + "/",
    "image": SITE + "/img/sala-hd.jpg", "telephone": "+39 045 862 6014",
    "servesCuisine": ["Romena", "Moldava", "Italiana"], "foundingDate": "2004",
    "address": {"@type": "PostalAddress", "streetAddress": "Via Luigi Prina, 21", "postalCode": "37136",
                "addressLocality": "Verona", "addressRegion": "VR", "addressCountry": "IT"},
    "openingHours": "Mo-Su 09:00-20:00",
}


def ld(path, name, extra=None):
    g = [{"@type": "WebPage", "name": name, "url": SITE + path, "about": {"@id": SITE + "/#ristorante"}},
         {"@type": "BreadcrumbList", "itemListElement": [
             {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
             {"@type": "ListItem", "position": 2, "name": name, "item": SITE + path}]},
         RESTAURANT]
    if extra:
        g.append(extra)
    return {"@context": "https://schema.org", "@graph": g}


def hero(name, kicker, title, intro, img, alt, meta=(), portrait=False, w=800, h=600):
    pills = "".join(f"<span>{e(m)}</span>" for m in meta)
    meta_html = f'\n        <p class="mp-hero__meta">{pills}</p>' if meta else ""
    cls = " pg-photo--portrait" if portrait else ""
    return f"""  <section class="mp-hero">
    <div class="wrap mp-hero__inner">
      <div class="mp-hero__copy">
        <nav class="crumbs" aria-label="Sei qui"><a href="/">Home</a><span aria-hidden="true">/</span><span aria-current="page">{e(name)}</span></nav>
        <p class="carta__kicker">{e(kicker)}</p>
        <h1>{e(title)}</h1>
        <p class="mp-hero__intro">{intro}</p>{meta_html}
      </div>
      <figure class="pg-photo{cls}">
        <img src="/img/{img}" alt="{e(alt)}" width="{w}" height="{h}" fetchpriority="high" decoding="async">
      </figure>
    </div>
  </section>
"""


def page(path, name, title, desc, image, body, extra_ld=None, msg="Ciao! Vorrei prenotare un tavolo da Alba Iulia."):
    html_ = head(title, desc, path, image, ld(path, name, extra_ld), path, "page-menu page-site")
    html_ += f'\n<main id="contenuto">\n{body}{cta(msg)}</main>\n'
    return html_ + FOOT


def more_pages(*items):
    """Riquadri finali verso altre pagine del sito."""
    cards = "\n".join(f"""      <a class="mp-next__card reveal" href="{href}">
        <img src="/img/{img}" alt="" width="800" height="600" loading="lazy" decoding="async">
        <span class="mp-next__label">{e(label)} →</span>
        <span class="mp-next__name">{e(title)}</span>
      </a>""" for href, img, label, title in items)
    return f"""
  <section class="mp-next pg-more" aria-label="Continua a scoprire Alba Iulia">
    <div class="wrap mp-next__row">
{cards}
    </div>
  </section>
"""


# ---------------------------------------------------------------- /il-titolare

def titolare():
    body = hero("Il titolare", "Dal 2004 · Famiglia Sbuciumelea", "Il titolare",
                "Ogni giorno in sala e al banco, per accogliervi di persona. Alba Iulia è un locale di famiglia: "
                "chi vi accoglie è chi l'ha costruito, un pezzo alla volta.",
                "titolare.webp", "Il titolare di Alba Iulia, sorridente, nel suo locale",
                ("Dal 2004", "Famiglia Sbuciumelea", "Via Luigi Prina 21"), portrait=True, w=764, h=954)
    body += """
  <section class="pg-section">
    <div class="wrap pg-split">
      <figure class="pg-split__media reveal"><img src="/img/insegna.webp" alt="L'insegna ovale sulla parete capitonné: Caffetteria Alba Iulia Gastronomia, dal 2004 famiglia Sbuciumelea" width="900" height="1200" loading="lazy" decoding="async"></figure>
      <div class="pg-split__copy reveal">
        <p class="pg-kicker">La nostra storia</p>
        <h2>Vent'anni fa abbiamo aperto la porta. Da allora non l'abbiamo più chiusa.</h2>
        <p>Nel 2004 Alba Iulia è stato il primo locale di Verona dedicato alla gastronomia tipica romena, e il secondo in tutta Italia. Porta il nome della città simbolo della nostra terra, e l'abbiamo costruito come si costruisce una casa: un pezzo alla volta.</p>
        <p>Oggi in sala e al banco c'è ancora la famiglia Sbuciumelea. Nel 2022 abbiamo inaugurato i nuovi spazi di caffetteria e gastronomia, con lo stesso spirito del primo giorno.</p>
      </div>
    </div>
  </section>

  <section class="pg-section pg-section--brand">
    <div class="wrap">
      <header class="pg-head reveal">
        <p class="pg-kicker">Le tappe</p>
        <h2>Da una porta aperta in Via Luigi Prina a quattro attività sotto lo stesso tetto</h2>
      </header>
      <ol class="pg-timeline">
        <li class="reveal"><b>2004</b><h3>Si apre la porta</h3><p>Nasce Alba Iulia in Via Luigi Prina: il primo locale di Verona dedicato alla gastronomia tipica romena.</p></li>
        <li class="reveal"><b>2022</b><h3>I nuovi spazi</h3><p>Inauguriamo la nuova caffetteria e la gastronomia, con il bancone e la parete capitonné che oggi ci rappresentano.</p></li>
        <li class="reveal"><b>Oggi</b><h3>Una casa per tutti</h3><p>Ristorante, caffetteria, gastronomia e macelleria, aperti sette giorni su sette dalle 9 alle 20.</p></li>
      </ol>
    </div>
  </section>

  <section class="pg-section">
    <div class="wrap">
      <header class="pg-head reveal">
        <p class="pg-kicker">Come lavoriamo</p>
        <h2>Quello che ci chiedete di non cambiare mai</h2>
      </header>
      <ul class="pg-cards">
        <li class="reveal"><span class="pg-cards__num">01</span><h3>Ricette di famiglia</h3><p>Sarmale, mici, ciorbe e tochitură come si preparano a casa in Romania, accanto ai piatti della cucina italiana.</p></li>
        <li class="reveal"><span class="pg-cards__num">02</span><h3>Fatto da noi</h3><p>I mici sono di nostra produzione e la carne arriva dal nostro banco di macelleria, la stessa che potete portare a casa.</p></li>
        <li class="reveal"><span class="pg-cards__num">03</span><h3>Accoglienza</h3><p>Porzioni generose e un'accoglienza che fa tornare: per tanti romeni a Verona è il sapore di casa, per tanti veronesi una cucina da scoprire.</p></li>
      </ul>
    </div>
  </section>

  <section class="pg-quote">
    <div class="wrap pg-quote__inner reveal">
      <p class="pg-quote__score"><strong>4,7</strong><span>su 5 · 232 recensioni su Google</span></p>
      <p class="pg-quote__text">“Cucina di famiglia, porzioni generose e un'accoglienza che fa tornare.”</p>
      <a class="link" href="https://www.google.com/maps/search/?api=1&amp;query=Alba+Iulia+Via+Luigi+Prina+21+Verona" target="_blank" rel="noopener">Leggi le recensioni su Google</a>
    </div>
  </section>
"""
    body += more_pages(("/il-locale", "sala.webp", "Scopri", "Il locale"), ("/menu", "piatto.webp", "Sfoglia", "Il menu"))
    return page("/il-titolare", "Il titolare", "Il titolare e la famiglia Sbuciumelea · Alba Iulia Verona",
                "La storia di Alba Iulia a Verona: dal 2004 la famiglia Sbuciumelea accoglie in sala e al banco, nel primo locale di gastronomia romena della città.",
                "/img/titolare-og.webp", body)


# ---------------------------------------------------------------- /il-locale

ANIME = [
    ("ristorante.webp", "Tavoli apparecchiati con tovaglie bianche nella sala del ristorante", "Ristorante",
     "Un menu tra le regioni romene e quelle italiane: ciorbe, sarmale, grigliate e contorni di nostra produzione, da gustare in sala o nel dehors.",
     ("Sala e dehors", "Cucina romena e italiana"), "/menu", "Sfoglia il menu"),
    ("caffe.webp", "Vassoio di dolci al cioccolato e sfogliatine della pasticceria", "Caffetteria",
     "Colazione con caffè e pasticceria fresca, poi il bancone si prepara per l'aperitivo. Dalle 9 del mattino, sette giorni su sette.",
     ("Colazione", "Pasticceria", "Aperitivo"), None, None),
    ("gastronomia.webp", "Il banco della gastronomia con orchidee e piante", "Gastronomia",
     "I nostri piatti pronti da portare via e un piccolo market di prodotti tipici romeni, moldavi e italiani: formaggi, conserve, dolci e bevande.",
     ("Piatti pronti", "Prodotti tipici", "Asporto"), None, None),
    ("macelleria.webp", "Taglio di carne bovina marezzata al banco", "Macelleria",
     "Carne fresca selezionata e salumi artigianali, tagliati al momento come li chiedete voi. La stessa carne che cuciniamo in sala.",
     ("Carne fresca", "Salumi artigianali", "Consegna a domicilio"), "/macelleria", "Scopri la macelleria"),
]


def locale():
    body = hero("Il locale", "Via Luigi Prina 21 · Verona", "Il locale",
                "La parete capitonné, i lampadari di cristallo, il bancone della caffetteria e la sala apparecchiata. "
                "Tutto sotto lo stesso tetto, dal mattino alla sera.",
                "sala-hd.webp", "La sala di Alba Iulia: parete capitonné bianca con il logo, tavoli apparecchiati e il bancone della caffetteria",
                ("Ristorante", "Caffetteria", "Gastronomia", "Macelleria"), w=2074, h=1508)
    rows = []
    for i, (img, alt, name, text, tags, href, cta_label) in enumerate(ANIME):
        tags_html = "".join(f"<li>{e(t)}</li>" for t in tags)
        link = f'\n        <a class="pg-arrow" href="{href}">{e(cta_label)} <span aria-hidden="true">→</span></a>' if href else ""
        rows.append(f"""    <article class="wrap pg-split{' pg-split--rev' if i % 2 else ''}">
      <figure class="pg-split__media reveal"><img src="/img/{img}" alt="{e(alt)}" width="1200" height="900" loading="lazy" decoding="async"></figure>
      <div class="pg-split__copy reveal">
        <p class="pg-kicker">{i + 1:02d} · Quattro modi di stare a tavola</p>
        <h2>{e(name)}</h2>
        <p>{e(text)}</p>
        <ul class="pg-tags">{tags_html}</ul>{link}
      </div>
    </article>""")
    body += f"""
  <section class="pg-section pg-stack" aria-label="Le quattro anime del locale">
{chr(10).join(rows)}
  </section>

  <section class="pg-section pg-section--cream">
    <div class="wrap">
      <header class="pg-head reveal">
        <p class="pg-kicker">Una giornata da Alba Iulia</p>
        <h2>Dalle 9 alle 20, tutti i giorni</h2>
      </header>
      <ol class="pg-day">
        <li class="reveal"><b>Mattina</b><p>Caffè e pasticceria fresca al bancone della caffetteria.</p></li>
        <li class="reveal"><b>Pranzo</b><p>In sala o nel dehors, con la cucina romena e italiana.</p></li>
        <li class="reveal"><b>Pomeriggio</b><p>La gastronomia e il market dei prodotti tipici, la carne fresca al banco.</p></li>
        <li class="reveal"><b>Sera</b><p>L'aperitivo al bancone, e i piatti pronti da portare a casa.</p></li>
      </ol>
      <ul class="pg-tags pg-tags--center reveal"><li>Sala</li><li>Dehors</li><li>Asporto</li><li>Consegna a domicilio</li></ul>
    </div>
  </section>
"""
    body += more_pages(("/galleria", "bar.webp", "Guarda", "La galleria"), ("/dove-siamo", "insegna.webp", "Vieni a trovarci", "Dove siamo"))
    return page("/il-locale", "Il locale", "Il locale · Ristorante, caffetteria, gastronomia e macelleria a Verona",
                "Alba Iulia in Via Luigi Prina 21 a Verona: ristorante con dehors, caffetteria, gastronomia con prodotti tipici e macelleria, aperti tutti i giorni dalle 9 alle 20.",
                "/img/sala-hd.jpg", body)


# ---------------------------------------------------------------- /macelleria

def macelleria():
    body = hero("Macelleria", "Macelleria e prodotti tipici", "La macelleria",
                "La stessa carne che cuciniamo in sala, pronta per la vostra cucina. Tagli freschi, macinato per i mici, "
                "salsicce e salumi artigianali, tagliati al momento come li chiedete.",
                "banco.webp", "Un taglio di manzo marezzato affettato a mano al banco della macelleria",
                ("Carne fresca ogni giorno", "Asporto e consegna"), w=1200, h=900)
    body += """
  <section class="pg-section">
    <div class="wrap">
      <header class="pg-head reveal">
        <p class="pg-kicker">Al banco</p>
        <h2>Cosa trovate da noi</h2>
      </header>
      <ul class="pg-products">
        <li class="reveal"><img src="/img/macelleria.webp" alt="Taglio di carne bovina marezzata" width="1200" height="900" loading="lazy" decoding="async"><h3>Carne fresca</h3><p>Tagli selezionati ogni giorno, preparati al momento come li chiedete.</p></li>
        <li class="reveal"><img src="/img/menu/mici.webp" alt="Mici alla griglia con senape" width="800" height="600" loading="lazy" decoding="async"><h3>Per i mici</h3><p>Il macinato speziato per i mici, come lo usiamo nella nostra cucina.</p></li>
        <li class="reveal"><img src="/img/menu/carnat.webp" alt="Salsiccia fresca alla griglia" width="800" height="600" loading="lazy" decoding="async"><h3>Salsicce e salumi</h3><p>Salsicce fresche e salumi artigianali, da cuocere o da affettare.</p></li>
        <li class="reveal"><img src="/img/gastronomia.webp" alt="Il banco della gastronomia" width="1200" height="900" loading="lazy" decoding="async"><h3>Prodotti tipici</h3><p>Formaggi, conserve, dolci e bevande per una tavola romena, moldava o italiana.</p></li>
      </ul>
    </div>
  </section>

  <section class="pg-section pg-section--cream">
    <div class="wrap">
      <header class="pg-head reveal">
        <p class="pg-kicker">Ordinare è semplice</p>
        <h2>Ditecelo su WhatsApp, al resto pensiamo noi</h2>
      </header>
      <ol class="pg-steps">
        <li class="reveal"><b>1</b><h3>Scrivete cosa vi serve</h3><p>Il taglio, il peso, quante persone: un messaggio su WhatsApp o una telefonata.</p></li>
        <li class="reveal"><b>2</b><h3>Prepariamo l'ordine</h3><p>La carne viene tagliata e confezionata al momento.</p></li>
        <li class="reveal"><b>3</b><h3>Ritiro o consegna</h3><p>Passate in Via Luigi Prina 21 oppure ve lo portiamo a domicilio.</p></li>
      </ol>
      <p class="pg-center reveal"><a class="btn btn--solid btn--lg js-wa" href="https://wa.me/393456967120" target="_blank" rel="noopener" data-msg="Ciao! Vorrei ordinare dalla macelleria di Alba Iulia."><svg aria-hidden="true"><use href="#wa"/></svg>Ordina su WhatsApp</a></p>
    </div>
  </section>
"""
    body += more_pages(("/menu/grigliate", "menu/platou-alba-iulia.webp", "Assaggiala in sala", "Le grigliate"), ("/dove-siamo", "insegna.webp", "Vieni a trovarci", "Dove siamo"))
    return page("/macelleria", "Macelleria", "Macelleria e prodotti tipici romeni · Alba Iulia Verona",
                "La macelleria di Alba Iulia a Verona: carne fresca selezionata, macinato per i mici, salsicce, salumi artigianali e prodotti tipici romeni e moldavi. Ordini su WhatsApp, asporto e consegna.",
                "/img/banco.webp", body, msg="Ciao! Vorrei ordinare dalla macelleria di Alba Iulia.")


# ---------------------------------------------------------------- /galleria

FOTO = [
    ("sala-hd.webp", "La sala con la parete capitonné, il logo e i tavoli apparecchiati", 2074, 1508),
    ("bancone.webp", "Il bancone con il titolare al lavoro", 0, 0),
    ("titolare.webp", "Il titolare nel suo locale", 764, 954),
    ("caffe.webp", "Dolci al cioccolato e sfogliatine della caffetteria", 0, 0),
    ("bar.webp", "Il bar con la macchina del caffè e le bottiglie", 0, 0),
    ("insegna.webp", "L'insegna: dal 2004 famiglia Sbuciumelea", 0, 0),
    ("ristorante.webp", "La sala con le vetrate verso il dehors", 0, 0),
    ("piatto.webp", "Pranzo in sala", 0, 0),
    ("gastronomia.webp", "Il banco della gastronomia", 0, 0),
    ("banco.webp", "Un taglio di manzo al banco della macelleria", 0, 0),
    ("macelleria.webp", "Carne bovina marezzata", 0, 0),
    ("sala.webp", "La sala e il logo sulla parete capitonné", 0, 0),
]


def galleria(sizes):
    items = []
    for img, alt, *_ in FOTO:
        w, h = sizes[img]
        items.append(f"""      <li class="reveal"><button type="button" class="pg-gallery__item" data-full="/img/{img}" aria-label="Ingrandisci: {e(alt)}">
        <img src="/img/{img}" alt="{e(alt)}" width="{w}" height="{h}" loading="lazy" decoding="async">
      </button></li>""")
    body = hero("Galleria", "Un giro nel locale", "Galleria",
                "La sala, il bancone, la caffetteria, la gastronomia e la macelleria: le foto del nostro locale in Via Luigi Prina. Toccate una foto per ingrandirla.",
                "bancone.webp", "Il bancone con il titolare al lavoro", (f"{len(FOTO)} foto",), w=sizes["bancone.webp"][0], h=sizes["bancone.webp"][1])
    body += f"""
  <section class="pg-section">
    <ul class="wrap pg-gallery">
{chr(10).join(items)}
    </ul>
  </section>

<dialog class="lightbox" id="lightbox" aria-label="Foto ingrandita">
  <button class="lightbox__close" type="button" id="lightbox-close" aria-label="Chiudi">×</button>
  <img id="lightbox-img" alt="">
</dialog>
"""
    body += more_pages(("/il-locale", "sala.webp", "Scopri", "Il locale"), ("/menu", "piatto.webp", "Sfoglia", "Il menu"))
    return page("/galleria", "Galleria", "Galleria fotografica · Alba Iulia Verona",
                "Le foto di Alba Iulia a Verona: la sala con la parete capitonné, il bancone della caffetteria, la gastronomia e la macelleria.",
                "/img/sala-hd.jpg", body)


# ---------------------------------------------------------------- /dove-siamo

GIORNI = ["Lunedì", "Martedì", "Mercoledì", "Giovedì", "Venerdì", "Sabato", "Domenica"]


def dove():
    rows = "\n".join(f'          <tr data-day="{i + 1}"><th scope="row">{g}</th><td>09:00 – 20:00</td></tr>' for i, g in enumerate(GIORNI))
    body = hero("Dove siamo", "Via Luigi Prina 21 · 37136 Verona", "Dove siamo",
                "Vi aspettiamo in Via Luigi Prina 21 a Verona, tutti i giorni dalle 9 alle 20. Per prenotare un tavolo, "
                "ordinare dalla macelleria o chiedere un'informazione, scriveteci su WhatsApp o chiamateci.",
                "insegna.webp", "L'insegna ovale di Alba Iulia sulla parete capitonné",
                ("Aperti 7 giorni su 7", "09:00 – 20:00"), portrait=True, w=900, h=1200)
    body += f"""
  <section class="pg-section">
    <div class="wrap pg-contacts">
      <a class="pg-contact reveal js-wa" href="{WA}" target="_blank" rel="noopener" data-msg="Ciao! Vorrei prenotare un tavolo da Alba Iulia.">
        <svg aria-hidden="true"><use href="#wa"/></svg><span class="pg-contact__k">WhatsApp</span><span class="pg-contact__v">345 696 7120</span><span class="pg-contact__go">Scrivici →</span>
      </a>
      <a class="pg-contact reveal" href="tel:+390458626014">
        <svg aria-hidden="true"><use href="#tel"/></svg><span class="pg-contact__k">Telefono</span><span class="pg-contact__v">045 862 6014</span><span class="pg-contact__go">Chiama →</span>
      </a>
      <a class="pg-contact reveal" href="https://www.google.com/maps/dir/?api=1&amp;destination=Via+Luigi+Prina+21+37136+Verona" target="_blank" rel="noopener">
        <svg aria-hidden="true" viewBox="0 0 24 24"><path fill="currentColor" d="M12 2a7 7 0 0 0-7 7c0 5.25 7 13 7 13s7-7.75 7-13a7 7 0 0 0-7-7Zm0 9.5A2.5 2.5 0 1 1 12 6.5a2.5 2.5 0 0 1 0 5Z"/></svg><span class="pg-contact__k">Indirizzo</span><span class="pg-contact__v">Via Luigi Prina 21, Verona</span><span class="pg-contact__go">Indicazioni →</span>
      </a>
    </div>
  </section>

  <section class="pg-section pg-section--cream">
    <div class="wrap pg-where">
      <div class="pg-where__info reveal">
        <p class="pg-kicker">Orari</p>
        <h2>Tutti i giorni, dalle 9 alle 20</h2>
        <p class="pg-open" id="open-status" aria-live="polite"></p>
        <table class="pg-hours">
          <caption class="sr-only">Orari di apertura</caption>
          <tbody>
{rows}
          </tbody>
        </table>
        <p class="pg-note">Sala, dehors, asporto e consegna a domicilio. Facebook: <a class="link" href="https://www.facebook.com/albajuliaverona/" target="_blank" rel="noopener">albajuliaverona</a></p>
      </div>
      <div class="pg-where__map reveal">
        <iframe title="Mappa: Alba Iulia, Via Luigi Prina 21, Verona" src="https://maps.google.com/maps?q=Via%20Luigi%20Prina%2021%2C%2037136%20Verona&amp;z=16&amp;output=embed" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>
      </div>
    </div>
  </section>
"""
    body += more_pages(("/menu", "piatto.webp", "Prima di venire", "Sfoglia il menu"), ("/il-locale", "sala.webp", "Scopri", "Il locale"))
    return page("/dove-siamo", "Dove siamo", "Dove siamo e orari · Alba Iulia, Via Luigi Prina 21 Verona",
                "Alba Iulia è in Via Luigi Prina 21, 37136 Verona. Aperti tutti i giorni dalle 9 alle 20. Telefono 045 862 6014, WhatsApp 345 696 7120.",
                "/img/insegna.webp", body)


def build_all(sizes):
    return [("il-titolare.html", titolare()), ("il-locale.html", locale()), ("macelleria.html", macelleria()),
            ("galleria.html", galleria(sizes)), ("dove-siamo.html", dove())]
