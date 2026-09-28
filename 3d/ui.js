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
  var links = {};
  document.querySelectorAll('.nav__links a').forEach(function (a) { links[a.getAttribute('href').slice(1)] = a; });
  if ('IntersectionObserver' in window) {
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
  if (frame && fine && !reduced) {
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

  /* ---------- Il piatto gira quando scegli una specialità ---------- */
  var plateImg = document.querySelector('.dishes__plate img');
  var turn = 0;
  document.querySelectorAll('.menu__item').forEach(function (d) {
    d.addEventListener('toggle', function () {
      if (!d.open) return;
      document.querySelectorAll('.menu__item[open]').forEach(function (o) { if (o !== d) o.open = false; });
      turn += 40;
      if (plateImg && !reduced) plateImg.style.transform = 'scale(1.1) rotate(' + turn + 'deg)';
    });
  });

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
    if (!box.showModal) return;
    boxImg.src = img.currentSrc || img.src;
    boxImg.alt = img.alt;
    box.showModal();
  }
  document.getElementById('lightbox-close').addEventListener('click', function () { box.close(); });
  box.addEventListener('click', function (e) { if (e.target === box) box.close(); });

  /* ---------- Giostra 3D della galleria ---------- */
  var carousel = document.getElementById('carousel');
  var ring = document.getElementById('ring');
  var items = Array.prototype.slice.call(ring.children);
  var N = items.length, step = 360 / N;
  var rot = 0, vel = 0, target = null, dragging = false, moved = 0, lastX = 0, inView = false, idle = 0;
  function radius() { return parseFloat(getComputedStyle(carousel).getPropertyValue('--r')) || 480; }
  function layout() {
    var r = radius();
    items.forEach(function (it, i) { it.style.transform = 'rotateY(' + (i * step) + 'deg) translateZ(' + r + 'px)'; });
  }
  function paint() {
    ring.style.transform = 'translateZ(' + (-radius()) + 'px) rotateY(' + rot + 'deg)';
    items.forEach(function (it, i) {
      var a = ((i * step + rot) % 360 + 540) % 360 - 180; // 0 = di fronte
      var f = Math.cos(a * Math.PI / 180);
      it.style.filter = 'brightness(' + (0.45 + 0.55 * Math.max(0, f)).toFixed(2) + ')';
      it.tabIndex = Math.abs(a) < step / 2 ? 0 : -1;
    });
  }
  function tick() {
    if (!dragging) {
      if (target !== null) {
        rot += (target - rot) * 0.12;
        if (Math.abs(target - rot) < 0.05) { rot = target; target = null; }
      } else if (Math.abs(vel) > 0.02) {
        rot += vel; vel *= 0.94;
      } else if (!reduced && inView && performance.now() - idle > 2500) {
        rot -= 0.06;
      }
    }
    paint();
    if (inView) requestAnimationFrame(tick);
  }
  function snapBy(dir) { target = Math.round((target !== null ? target : rot) / step) * step + dir * step; vel = 0; idle = performance.now(); }
  layout(); paint();
  addEventListener('resize', function () { layout(); paint(); });
  new IntersectionObserver(function (es) {
    var was = inView; inView = es[0].isIntersecting;
    if (inView && !was) requestAnimationFrame(tick);
  }).observe(carousel);
  carousel.addEventListener('pointerdown', function (e) {
    dragging = true; moved = 0; lastX = e.clientX; vel = 0; target = null;
    carousel.setPointerCapture(e.pointerId);
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

  /* ---------- Animazioni allo scroll ---------- */
  if (!hasGsap || reduced) return;
  var gsap = window.gsap;
  gsap.registerPlugin(window.ScrollTrigger);

  // Titolo: le parole entrano una dopo l'altra, finita l'intro
  var title = document.getElementById('hero-title');
  title.innerHTML = title.textContent.trim().split(/\s+/).map(function (w) { return '<span class="w">' + w + '</span>'; }).join(' ');
  gsap.from(title.querySelectorAll('.w'), { yPercent: 60, opacity: 0, duration: 1, ease: 'power3.out', stagger: 0.06, delay: 1.45 });
  gsap.from('.hero__kicker, .hero__lead, .hero__actions, .hero__facts', { y: 20, opacity: 0, duration: .9, ease: 'power3.out', stagger: .08, delay: 1.8 });
  gsap.from('.owner', { scale: .9, opacity: 0, duration: 1.3, ease: 'power3.out', delay: 1.5 });

  // La sala si apre dall'ovale del logo fino a tutto schermo
  var sala = document.getElementById('sala-media');
  gsap.timeline({
    scrollTrigger: { trigger: '.sala__pin', start: 'top top', end: '+=110%', scrub: 0.6, pin: true }
  })
    .fromTo(sala, { clipPath: 'ellipse(30% 34% at 50% 50%)' }, { clipPath: 'ellipse(85% 85% at 50% 50%)', ease: 'none' }, 0)
    .fromTo(sala.querySelector('img'), { scale: 1.18 }, { scale: 1, ease: 'none' }, 0)
    .fromTo('.sala__pin', { '--shade': 0 }, { '--shade': 1, ease: 'none', duration: .35 }, .65);

  // I quattro servizi scorrono in orizzontale (solo schermi larghi)
  var mm = gsap.matchMedia();
  mm.add('(min-width: 901px)', function () {
    var track = document.getElementById('services-track');
    var dist = function () { return Math.max(0, track.scrollWidth - innerWidth); };
    gsap.to(track, {
      x: function () { return -dist(); }, ease: 'none',
      scrollTrigger: { trigger: '.services__pin', start: 'top top', end: function () { return '+=' + dist(); }, scrub: 0.6, pin: true, invalidateOnRefresh: true }
    });
  });

  // Parallasse leggero sull'insegna
  gsap.fromTo('.family__photo img', { yPercent: -8 }, { yPercent: 4, ease: 'none', scrollTrigger: { trigger: '.family', start: 'top bottom', end: 'bottom top', scrub: true } });

  addEventListener('load', function () { window.ScrollTrigger.refresh(); });
})();
