(function () {
  'use strict';

  /* Numero WhatsApp del locale (formato internazionale, senza + e spazi) */
  var WA_NUMBER = '393456967120';

  var root = document.documentElement;
  var reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
  var fine = matchMedia('(pointer: fine)').matches;
  var hasGsap = !!(window.gsap && window.ScrollTrigger);
  if (reduced) root.classList.add('no-motion');
  if (!hasGsap) root.classList.add('no-gsap');

  /* ---------- WhatsApp: link con messaggio già scritto ---------- */
  document.querySelectorAll('.js-wa').forEach(function (a) {
    var msg = a.getAttribute('data-msg') || 'Ciao Alba Iulia! Vorrei qualche informazione.';
    a.href = 'https://wa.me/' + WA_NUMBER + '?text=' + encodeURIComponent(msg);
  });
  var waFloat = document.querySelector('.wa-float');
  if (waFloat && !reduced) {
    setTimeout(function () { waFloat.classList.add('is-peek'); }, 4200);
    setTimeout(function () { waFloat.classList.remove('is-peek'); }, 8800);
  }

  /* ---------- Navigazione ---------- */
  var nav = document.querySelector('.nav');
  var toggle = document.getElementById('nav-toggle');
  function onScroll() { nav.classList.toggle('is-scrolled', window.scrollY > 10); }
  onScroll();
  addEventListener('scroll', onScroll, { passive: true });
  toggle.addEventListener('click', function () {
    var open = nav.classList.toggle('is-open');
    toggle.setAttribute('aria-expanded', open);
    toggle.setAttribute('aria-label', open ? 'Chiudi il menu' : 'Apri il menu');
  });
  // Con <base> i link #ancora ricaricherebbero la pagina: li gestiamo qui
  document.querySelectorAll('a[href^="#"]').forEach(function (a) {
    a.addEventListener('click', function (e) {
      var id = a.getAttribute('href').slice(1);
      var el = id ? document.getElementById(id) : document.body;
      if (!el) return;
      e.preventDefault();
      nav.classList.remove('is-open');
      toggle.setAttribute('aria-expanded', 'false');
      var y = id === 'top' ? 0 : el.getBoundingClientRect().top + scrollY - nav.offsetHeight + 1;
      scrollTo({ top: y, behavior: reduced ? 'auto' : 'smooth' });
      if (id) history.replaceState(null, '', location.pathname + '#' + id);
    });
  });
  // Le voci della barra aprono le pagine; nella home si evidenzia la voce della sezione che si sta guardando
  var SECTION = { titolare: '/il-titolare', famiglia: '/il-titolare', locale: '/il-locale', carta: '/menu',
                  macelleria: '/macelleria', galleria: '/galleria', dove: '/dove-siamo' };
  var links = {};
  document.querySelectorAll('.nav__links a').forEach(function (a) {
    Object.keys(SECTION).forEach(function (id) { if (SECTION[id] === a.getAttribute('href')) links[id] = a; });
  });
  if ('IntersectionObserver' in window && !document.body.classList.contains('page-inner')) {
    var spy = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting && links[e.target.id]) {
          Object.keys(links).forEach(function (k) { links[k].classList.remove('is-active'); });
          links[e.target.id].classList.add('is-active');
        }
      });
    }, { rootMargin: '-45% 0px -50% 0px' });
    Object.keys(links).forEach(function (id) { var el = document.getElementById(id); if (el) spy.observe(el); });
  }

  /* ---------- Il titolare: l'ovale si inclina verso il cursore ---------- */
  var hero = document.getElementById('hero');
  var frame = document.getElementById('owner-frame');
  var photo = frame && frame.querySelector('.owner__photo');
  if (hero && frame && fine && !reduced) {
    hero.addEventListener('pointermove', function (e) {
      var r = frame.getBoundingClientRect();
      var dx = (e.clientX - (r.left + r.width / 2)) / innerWidth;
      var dy = (e.clientY - (r.top + r.height / 2)) / innerHeight;
      frame.style.transform = 'rotateY(' + (dx * 16).toFixed(2) + 'deg) rotateX(' + (-dy * 12).toFixed(2) + 'deg)';
      photo.style.setProperty('--gx', (50 + dx * 90).toFixed(1) + '%');
      photo.style.setProperty('--gy', (40 + dy * 90).toFixed(1) + '%');
    });
    hero.addEventListener('pointerleave', function () { frame.style.transform = ''; });
  }

  /* ---------- Bottoni magnetici ---------- */
  if (fine && !reduced) {
    document.querySelectorAll('.magnetic').forEach(function (b) {
      b.addEventListener('pointermove', function (e) {
        var r = b.getBoundingClientRect();
        var x = (e.clientX - r.left - r.width / 2) * 0.22;
        var y = (e.clientY - r.top - r.height / 2) * 0.3;
        b.style.transform = 'translate(' + x.toFixed(1) + 'px,' + y.toFixed(1) + 'px)';
      });
      b.addEventListener('pointerleave', function () { b.style.transform = ''; });
    });
  }

  /* ---------- Servizi: fila da scorrere col mouse (trascinando o con le frecce) ---------- */
  (function () {
    var track = document.getElementById('services-track');
    if (!track) return;
    var prev = document.getElementById('svc-prev'), next = document.getElementById('svc-next');
    function step() { var c = track.children[0]; return c ? c.getBoundingClientRect().width + parseFloat(getComputedStyle(track).columnGap || 24) : 300; }
    function update() {
      var max = track.scrollWidth - track.clientWidth - 40;   // a pochi pixel dalla fine la fila è già "finita"
      if (prev) prev.disabled = track.scrollLeft <= 2;
      if (next) next.disabled = track.scrollLeft >= max;
    }
    if (prev) prev.addEventListener('click', function () { track.scrollBy({ left: -step(), behavior: reduced ? 'auto' : 'smooth' }); });
    if (next) next.addEventListener('click', function () { track.scrollBy({ left: step(), behavior: reduced ? 'auto' : 'smooth' }); });
    track.addEventListener('scroll', update, { passive: true });
    addEventListener('resize', update);
    update();
    // trascinamento col mouse (sul touch ci pensa lo scorrimento nativo)
    var down = false, startX = 0, startLeft = 0, moved = 0;
    track.addEventListener('pointerdown', function (e) {
      if (e.pointerType !== 'mouse' || e.button !== 0) return;
      down = true; moved = 0; startX = e.clientX; startLeft = track.scrollLeft;
      track.classList.add('is-dragging'); track.setPointerCapture(e.pointerId);
    });
    track.addEventListener('pointermove', function (e) {
      if (!down) return;
      var dx = e.clientX - startX; moved = Math.max(moved, Math.abs(dx));
      track.scrollLeft = startLeft - dx;
    });
    function end() {
      if (!down) return;
      down = false; track.classList.remove('is-dragging');
      // riaggancia alla scheda più vicina
      var s = step(), target = Math.round(track.scrollLeft / s) * s;
      track.scrollTo({ left: target, behavior: reduced ? 'auto' : 'smooth' });
    }
    track.addEventListener('pointerup', end);
    track.addEventListener('pointercancel', end);
    track.addEventListener('click', function (e) { if (moved > 6) { e.preventDefault(); e.stopPropagation(); } }, true);
  })();

  /* ---------- Aperto adesso? (ora di Verona, tutti i giorni 9–20) ---------- */
  var status = document.getElementById('open-status');
  try {
    var parts = new Intl.DateTimeFormat('it-IT', { timeZone: 'Europe/Rome', hour: '2-digit', minute: '2-digit', hour12: false }).formatToParts(new Date());
    var h = +parts.find(function (p) { return p.type === 'hour'; }).value;
    var m = +parts.find(function (p) { return p.type === 'minute'; }).value;
    var open = h * 60 + m >= 540 && h * 60 + m < 1200;
    status.textContent = open ? 'Aperto adesso, chiude alle 20:00' : 'Chiuso adesso, riapre alle 09:00';
    status.classList.add(open ? 'is-open' : 'is-closed');
  } catch (e) {}

  /* ---------- Lightbox ---------- */
  var box = document.getElementById('lightbox');
  var boxImg = document.getElementById('lightbox-img');
  function openBox(img) {
    if (!box || !box.showModal) return;
    boxImg.src = img.currentSrc || img.src;
    boxImg.alt = img.alt;
    box.showModal();
  }
  if (box) {
    document.getElementById('lightbox-close').addEventListener('click', function () { box.close(); });
    box.addEventListener('click', function (e) { if (e.target === box) box.close(); });
    document.querySelectorAll('[data-full]').forEach(function (b) {
      b.addEventListener('click', function () { openBox(b.querySelector('img')); });
    });
  }

  /* ---------- Giostra 3D della galleria ---------- */
  var carousel = document.getElementById('carousel');
  if (carousel) (function () {
  var ring = document.getElementById('ring');
  var items = Array.prototype.slice.call(ring.children);
  var shades = items.map(function (it) { var sh = document.createElement('span'); sh.className = 'carousel__shade'; it.appendChild(sh); return sh; });
  var lastOp = items.map(function () { return -1; });
  var front = -1, running = false;
  var autoSpin = !reduced && !matchMedia('(pointer: coarse)').matches;
  var N = items.length, step = 360 / N;
  var rot = 0, vel = 0, target = null, dragging = false, moved = 0, lastX = 0, inView = false, idle = 0;
  function radius() { return parseFloat(getComputedStyle(carousel).getPropertyValue('--r')) || 480; }
  function layout() {
    var r = radius();
    items.forEach(function (it, i) { it.style.transform = 'rotateY(' + (i * step) + 'deg) translateZ(' + r + 'px)'; });
  }
  function paint() {
    ring.style.transform = 'translateZ(' + (-radius()) + 'px) rotateY(' + rot + 'deg)';
    var nf = -1;
    items.forEach(function (it, i) {
      var a = ((i * step + rot) % 360 + 540) % 360 - 180; // 0 = di fronte
      var op = Math.round((1 - Math.max(0, Math.cos(a * Math.PI / 180))) * 55) / 100;
      if (op !== lastOp[i]) { shades[i].style.opacity = op; lastOp[i] = op; }
      if (Math.abs(a) < step / 2) nf = i;
    });
    if (nf !== front) { items.forEach(function (it, i) { it.tabIndex = i === nf ? 0 : -1; }); front = nf; }
  }
  function tick() {
    var busy = dragging;
    if (!dragging) {
      if (target !== null) {
        rot += (target - rot) * 0.14; busy = true;
        if (Math.abs(target - rot) < 0.05) { rot = target; target = null; }
      } else if (Math.abs(vel) > 0.02) {
        rot += vel; vel *= 0.93; busy = true;
      } else if (autoSpin && performance.now() - idle > 2500) {
        rot -= 0.05; busy = true;
      } else if (autoSpin) busy = true; // in attesa di ripartire
    }
    paint();
    if (inView && busy) requestAnimationFrame(tick); else running = false;
  }
  function kick() { if (!running && inView) { running = true; requestAnimationFrame(tick); } }
  function snapBy(dir) { target = Math.round((target !== null ? target : rot) / step) * step + dir * step; vel = 0; idle = performance.now(); kick(); }
  layout(); paint();
  addEventListener('resize', function () { layout(); paint(); });
  new IntersectionObserver(function (es) {
    inView = es[0].isIntersecting;
    kick();
  }).observe(carousel);
  carousel.addEventListener('pointerdown', function (e) {
    dragging = true; moved = 0; lastX = e.clientX; vel = 0; target = null;
    carousel.setPointerCapture(e.pointerId);
    kick();
  });
  carousel.addEventListener('pointermove', function (e) {
    if (!dragging) return;
    var dx = e.clientX - lastX; lastX = e.clientX; moved += Math.abs(dx);
    rot += dx * 0.25; vel = dx * 0.25;
  });
  function endDrag(e) {
    if (!dragging) return;
    dragging = false; idle = performance.now();
    if (moved < 6) {
      var el = document.elementFromPoint(e.clientX, e.clientY);
      var it = el && el.closest('.carousel__item');
      if (it) openBox(it.querySelector('img'));
    } else {
      target = Math.round((rot + vel * 12) / step) * step; vel = 0;
    }
    kick();
  }
  carousel.addEventListener('pointerup', endDrag);
  carousel.addEventListener('pointercancel', function () { dragging = false; });
  carousel.addEventListener('keydown', function (e) {
    if (e.key === 'ArrowLeft') { snapBy(1); e.preventDefault(); }
    if (e.key === 'ArrowRight') { snapBy(-1); e.preventDefault(); }
    if (e.key === 'Enter') {
      var front = items.find(function (it) { return it.tabIndex === 0; });
      if (front) openBox(front.querySelector('img'));
    }
  });
  document.getElementById('prev').addEventListener('click', function () { snapBy(1); });
  document.getElementById('next').addEventListener('click', function () { snapBy(-1); });
  })();

  /* ---------- Animazioni allo scroll ---------- */
  if (!hasGsap || reduced) return;
  var gsap = window.gsap;
  gsap.registerPlugin(window.ScrollTrigger);
  window.ScrollTrigger.config({ ignoreMobileResize: true });

  // Titolo: le parole entrano una dopo l'altra, finita l'intro
  // (nella home dopo l'animazione del logo, nelle altre pagine subito)
  var d0 = document.getElementById('intro') ? 0.95 : 0.1;
  var title = document.getElementById('hero-title');
  if (title) {
    title.innerHTML = title.textContent.trim().split(/\s+/).map(function (w) { return '<span class="w">' + w + '</span>'; }).join(' ');
    gsap.from(title.querySelectorAll('.w'), { yPercent: 60, opacity: 0, duration: 1, ease: 'power3.out', stagger: 0.05, delay: d0 });
    gsap.from('.crumbs, .hero__kicker, .hero__lead, .hero__actions, .hero__facts', { y: 20, opacity: 0, duration: .9, ease: 'power3.out', stagger: .07, delay: d0 + 0.25 });
    gsap.from('.owner', { scale: .9, opacity: 0, duration: 1.1, ease: 'power3.out', delay: d0 + 0.05 });
  }
  // Nelle pagine interne i blocchi entrano dal basso quando arrivano sullo schermo
  gsap.utils.toArray('.reveal').forEach(function (el) {
    gsap.from(el, { y: 36, opacity: 0, duration: 1, ease: 'power3.out', scrollTrigger: { trigger: el, start: 'top 90%', once: true } });
  });

  // La sala si apre dall'ovale del logo fino a tutto schermo (solo transform e opacità)
  var salaBox = document.getElementById('sala-media');
  if (salaBox) (function () {
  var salaImg = document.getElementById('sala-img');
  var salaShade = document.querySelector('.sala__shade');
  var salaText = document.querySelector('.sala__text');
  // L'ovale di partenza ha le proporzioni del logo (largo, non alto) anche sui telefoni in verticale.
  // Il riquadro animato è il 142% della scena, quindi l'ovale visibile misura K0 × 1,42 × scena.
  var K0x, K0y, Z0 = 1.06;   // zoom iniziale leggero: la foto non va ingrandita troppo
  var salaStage = document.querySelector('.sala__stage');
  function salaSize() {
    var W = salaStage.clientWidth, H = salaStage.clientHeight;
    var ovalH = Math.min(H * 0.62, (W * 0.88) / 1.7), ovalW = ovalH * 1.7;
    K0x = ovalW / (1.42 * W); K0y = ovalH / (1.42 * H);
  }
  salaSize();
  function salaAt(p) {
    var kx = K0x + (1 - K0x) * p, ky = K0y + (1 - K0y) * p, z = Z0 + (1 - Z0) * p;
    salaBox.style.transform = 'scale(' + kx.toFixed(4) + ',' + ky.toFixed(4) + ')';
    salaImg.style.transform = 'scale(' + (z / kx).toFixed(4) + ',' + (z / ky).toFixed(4) + ')';
    var o = Math.max(0, (p - 0.65) / 0.35).toFixed(3);
    salaShade.style.opacity = o; salaText.style.opacity = o;
  }
  salaAt(0);
  window.ScrollTrigger.create({
    trigger: '.sala__pin', start: 'top top', end: '+=110%', pin: true, anticipatePin: 1,
    onUpdate: function (st) { salaAt(st.progress); },
    onRefresh: function (st) { salaSize(); salaAt(st.progress); }
  });
  })();


  // Parallasse leggero sull'insegna
  if (document.querySelector('.family__photo img')) gsap.fromTo('.family__photo img', { yPercent: -8 }, { yPercent: 4, ease: 'none', scrollTrigger: { trigger: '.family', start: 'top bottom', end: 'bottom top', scrub: true } });

  addEventListener('load', function () { window.ScrollTrigger.refresh(); });
})();

// Il menu: una sezione alla volta (Antipasti, Ciorbe, ...), con frecce da tastiera
(function () {
  var tabs = [].slice.call(document.querySelectorAll('button.carta__tab'));
  if (!tabs.length) return;
  var bar = tabs[0].parentNode;
  function show(tab, focus) {
    tabs.forEach(function (t) {
      var on = t === tab;
      t.setAttribute('aria-selected', on ? 'true' : 'false');
      t.tabIndex = on ? 0 : -1;
      document.getElementById(t.getAttribute('aria-controls')).hidden = !on;
    });
    if (focus) tab.focus();
    // la scheda scelta resta visibile nella fila che scorre
    bar.scrollTo({ left: tab.offsetLeft - bar.offsetLeft - 16, behavior: 'smooth' });
    // se si è già scesi nel menu, si torna all'inizio della sezione scelta
    var top = bar.getBoundingClientRect().top;
    if (top < 0) window.scrollBy({ top: top - 90, behavior: 'smooth' });
    if (window.ScrollTrigger) window.ScrollTrigger.refresh();
  }
  tabs.forEach(function (t, i) {
    t.addEventListener('click', function () { show(t); });
    t.addEventListener('keydown', function (e) {
      var j = e.key === 'ArrowRight' ? i + 1 : e.key === 'ArrowLeft' ? i - 1 : e.key === 'Home' ? 0 : e.key === 'End' ? tabs.length - 1 : null;
      if (j === null) return;
      e.preventDefault();
      show(tabs[(j + tabs.length) % tabs.length], true);
    });
  });
})();
