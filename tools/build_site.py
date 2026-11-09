#!/usr/bin/env python3
"""Genera le pagine interne del sito (stessa intestazione, footer e stile per tutte).

    python3 tools/build_site.py

- una pagina per ogni voce della barra: /la-famiglia, /il-locale, /menu, /macelleria,
  /galleria, /dove-siamo, e le pagine del menu dei piatti /menu/antipasti, /menu/ciorbe, ...
  (modelli e testi in tools/site_pages.py, piatti e prezzi in tools/menu.json)
- in index.html la parte tra <!-- IL MENU COMPLETO --> e <!-- MACELLERIA -->, e sitemap.xml
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


def img_size(rel):
    """Larghezza e altezza di un'immagine WebP in /img (letta dall'intestazione del file)."""
    with open(os.path.join(ROOT, "img", rel), "rb") as f:
        b = f.read(30)
    kind = b[12:16]
    if kind == b"VP8X":
        return 1 + int.from_bytes(b[24:27], "little"), 1 + int.from_bytes(b[27:30], "little")
    if kind == b"VP8L":
        n = int.from_bytes(b[21:25], "little")
        return 1 + (n & 0x3FFF), 1 + ((n >> 14) & 0x3FFF)
    return int.from_bytes(b[26:28], "little") & 0x3FFF, int.from_bytes(b[28:30], "little") & 0x3FFF


def dims(rel):
    w, h = img_size(rel)
    return f'width="{w}" height="{h}"'


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


NAV = [("La famiglia", "/la-famiglia"), ("Il locale", "/il-locale"), ("Menu", "/menu"),
       ("Macelleria", "/macelleria"), ("Galleria", "/galleria"), ("Dove siamo", "/dove-siamo")]


def nav_links(active, ind="      "):
    out = []
    for label, href in NAV:
        on = ' class="is-active" aria-current="page"' if href == active else ""
        out.append(f'{ind}<a href="{href}"{on}>{label}</a>')
    return "\n".join(out)


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


# ---------------------------------------------------------------- sezione della home

def home_section():
    o = ['''  <!-- IL MENU COMPLETO (generato da tools/build_menu.py) -->
  <section class="carta" id="carta" aria-labelledby="carta-title">
    <div class="wrap">
      <header class="carta__head">
        <div>
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


IMG_TAG = re.compile(r'(<img src="/img/([^"]+\.webp)"[^>]*?)width="\d+" height="\d+"')


def fix_dims(text):
    """Mette a ogni <img> di /img la larghezza e l'altezza vere (niente salti durante il caricamento)."""
    return IMG_TAG.sub(lambda m: m.group(1) + dims(m.group(2)), text)


def write(rel, text):
    p = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        f.write(fix_dims(text))
    print("scritto", rel)


ASSETS = ("style.css", "ui.js", "fire.js", "wall.js")


def stamp_versions():
    """Aggiunge a style.css, ui.js, ... un numero di versione (?v=...) legato al contenuto del file.
    Così, dopo ogni modifica, i browser scaricano subito i file nuovi invece di usare quelli vecchi in memoria."""
    import hashlib
    import glob
    ver = {a: hashlib.md5(open(os.path.join(ROOT, a), "rb").read()).hexdigest()[:8] for a in ASSETS}
    pat = re.compile(r'((?:href|src)=")(/?)(' + "|".join(re.escape(a) for a in ASSETS) + r')(?:\?v=[0-9a-f]+)?"')
    for f in glob.glob(os.path.join(ROOT, "*.html")) + glob.glob(os.path.join(ROOT, "menu", "*.html")):
        t = open(f, encoding="utf-8").read()
        n = pat.sub(lambda m: f'{m.group(1)}{m.group(2)}{m.group(3)}?v={ver[m.group(3)]}"', t)
        if n != t:
            open(f, "w", encoding="utf-8").write(n)
    print("versioni", ver)


if __name__ == "__main__":
    import sys
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import site_pages

    for rel, text in site_pages.build_all():
        write(rel, text)
    idx = open(os.path.join(ROOT, "index.html"), encoding="utf-8").read()
    a = idx.index("  <!-- IL MENU COMPLETO")
    b = idx.index("  <!-- MACELLERIA -->")
    idx = idx[:a] + home_section() + idx[b:]
    # nella home la barra porta alle pagine
    n0 = idx.index('<nav class="nav__links" id="menu" aria-label="Sezioni">')
    n1 = idx.index("</nav>", n0)
    idx = idx[:n0] + '<nav class="nav__links" id="menu" aria-label="Sezioni">\n' + nav_links(None) + "\n    " + idx[n1:]
    write("index.html", idx)
    stamp_versions()
    url = lambda path, pr: f"  <url><loc>{SITE}{path}</loc><changefreq>monthly</changefreq><priority>{pr}</priority></url>"
    sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">', url("/", "1.0")]
    sm += [url(href, "0.9") for _, href in NAV]
    sm += [url(f"/menu/{c['slug']}", "0.8") for c in CATS]
    write("sitemap.xml", "\n".join(sm + ["</urlset>", ""]))
