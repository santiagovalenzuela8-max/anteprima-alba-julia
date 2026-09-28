(function () {
  var root = document.documentElement;
  root.classList.add('js');

  /* Foto mancanti: al posto dell'immagine un tessuto a punto croce con etichetta */
  function placeholder(img) {
    if (img.dataset.ph) return;
    img.dataset.ph = '1';
    var ph = document.createElement('div');
    ph.className = 'ph is-missing';
    ph.setAttribute('data-label', img.getAttribute('data-label') || 'Foto');
    ph.setAttribute('role', 'img');
    ph.setAttribute('aria-label', img.alt || '');
    img.replaceWith(ph);
  }
  document.querySelectorAll('img[data-label]').forEach(function (img) {
    if (img.complete && img.naturalWidth === 0) placeholder(img);
    else img.addEventListener('error', function () { placeholder(img); });
  });

  /* Link interni: con <base> servono a scorrere nella pagina, non a ricaricarla */
  document.querySelectorAll('a[href^="#"]').forEach(function (a) {
    a.addEventListener('click', function (e) {
      var id = a.getAttribute('href').slice(1);
      var el = id ? document.getElementById(id) : document.body;
      if (!el) return;
      e.preventDefault();
      el.scrollIntoView({ behavior: window.matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth' });
      if (id) history.replaceState(null, '', location.pathname + location.search + '#' + id);
    });
  });

  /* Navigazione */
  var nav = document.querySelector('.nav');
  var toggle = document.getElementById('nav-toggle');
  function onScroll() { nav.classList.toggle('is-scrolled', window.scrollY > 8); }
  onScroll();
  window.addEventListener('scroll', onScroll, { passive: true });
  toggle.addEventListener('click', function () {
    var open = nav.classList.toggle('is-open');
    toggle.setAttribute('aria-expanded', open);
    toggle.setAttribute('aria-label', open ? 'Chiudi il menu' : 'Apri il menu');
  });
  document.querySelectorAll('.nav__links a').forEach(function (a) {
    a.addEventListener('click', function () {
      nav.classList.remove('is-open');
      toggle.setAttribute('aria-expanded', 'false');
    });
  });

  /* Voce di menu attiva */
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

    /* Rivelazione leggera delle sezioni sotto la piega */
    if (!window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
      var rev = new IntersectionObserver(function (entries) {
        entries.forEach(function (e) {
          if (e.isIntersecting) { e.target.classList.remove('is-pending'); rev.unobserve(e.target); }
        });
      }, { rootMargin: '0px 0px -8% 0px' });
      document.querySelectorAll('.service, .family__inner, .menu__item, .butcher__inner, .reviews__inner, .gallery__item, .visit__inner').forEach(function (el) {
        var r = el.getBoundingClientRect();
        if (r.top > window.innerHeight) { el.classList.add('reveal', 'is-pending'); rev.observe(el); }
      });
    }
  }

  /* Aperto adesso? (orario di Verona, tutti i giorni 09:00–20:00) */
  var status = document.getElementById('open-status');
  try {
    var parts = new Intl.DateTimeFormat('it-IT', { timeZone: 'Europe/Rome', hour: '2-digit', minute: '2-digit', hour12: false }).formatToParts(new Date());
    var h = +parts.find(function (p) { return p.type === 'hour'; }).value;
    var m = +parts.find(function (p) { return p.type === 'minute'; }).value;
    var mins = h * 60 + m, open = mins >= 540 && mins < 1200;
    status.textContent = open ? 'Aperto adesso · chiude alle 20:00' : 'Chiuso adesso · riapre alle 09:00';
    status.classList.add(open ? 'is-open' : 'is-closed');
  } catch (e) { /* senza Intl l'orario resta comunque visibile */ }

  /* Galleria a schermo intero */
  var box = document.getElementById('lightbox');
  var boxImg = document.getElementById('lightbox-img');
  if (box && box.showModal) {
    document.querySelectorAll('.gallery__item').forEach(function (btn) {
      btn.addEventListener('click', function () {
        var img = btn.querySelector('img');
        if (!img) return;
        boxImg.src = img.currentSrc || img.src;
        boxImg.alt = img.alt;
        box.showModal();
      });
    });
    document.getElementById('lightbox-close').addEventListener('click', function () { box.close(); });
    box.addEventListener('click', function (e) { if (e.target === box) box.close(); });
  }
})();
