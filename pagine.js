/* Pagine del menu (/menu, /menu/antipasti, ...): niente 3D né GSAP, solo l'essenziale */
(function () {
  'use strict';
  var WA_NUMBER = '393456967120';
  var reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
  document.documentElement.classList.add('js');

  // WhatsApp con messaggio già scritto
  document.querySelectorAll('.js-wa').forEach(function (a) {
    var msg = a.getAttribute('data-msg') || 'Ciao Alba Iulia! Vorrei qualche informazione.';
    a.href = 'https://wa.me/' + WA_NUMBER + '?text=' + encodeURIComponent(msg);
  });
  var waFloat = document.querySelector('.wa-float');
  if (waFloat && !reduced) {
    setTimeout(function () { waFloat.classList.add('is-peek'); }, 3500);
    setTimeout(function () { waFloat.classList.remove('is-peek'); }, 8000);
  }

  // Menu a tendina su mobile
  var nav = document.querySelector('.nav');
  var toggle = document.getElementById('nav-toggle');
  if (nav && toggle) toggle.addEventListener('click', function () {
    var open = nav.classList.toggle('is-open');
    toggle.setAttribute('aria-expanded', open);
    toggle.setAttribute('aria-label', open ? 'Chiudi il menu' : 'Apri il menu');
  });

  // La sezione aperta resta visibile nella fila delle sezioni (su mobile scorre)
  var row = document.querySelector('.mp-cats__row');
  var cur = row && row.querySelector('[aria-current]');
  if (cur) row.scrollLeft = cur.offsetLeft - row.offsetLeft - 16;

  // Galleria: tocca una foto per ingrandirla
  var box = document.getElementById('lightbox');
  if (box && box.showModal) {
    var big = document.getElementById('lightbox-img');
    document.querySelectorAll('[data-full]').forEach(function (b) {
      b.addEventListener('click', function () {
        var img = b.querySelector('img');
        big.src = b.getAttribute('data-full'); big.alt = img ? img.alt : '';
        box.showModal();
      });
    });
    document.getElementById('lightbox-close').addEventListener('click', function () { box.close(); });
    box.addEventListener('click', function (e) { if (e.target === box) box.close(); });
  }

  // Dove siamo: aperto adesso? (ora di Verona, tutti i giorni 9–20) e giorno di oggi in tabella
  var status = document.getElementById('open-status');
  if (status) {
    try {
      var parts = new Intl.DateTimeFormat('it-IT', { timeZone: 'Europe/Rome', weekday: 'short', hour: '2-digit', minute: '2-digit', hour12: false }).formatToParts(new Date());
      var get = function (t) { return (parts.filter(function (x) { return x.type === t; })[0] || {}).value; };
      var mins = (+get('hour') % 24) * 60 + +get('minute');
      var open = mins >= 540 && mins < 1200;
      status.textContent = open ? 'Aperto adesso · chiude alle 20:00' : 'Chiuso adesso · apre alle 9:00';
      status.classList.toggle('is-closed', !open);
      var days = ['lun', 'mar', 'mer', 'gio', 'ven', 'sab', 'dom'];
      var today = days.indexOf((get('weekday') || '').slice(0, 3).toLowerCase()) + 1;
      var row = document.querySelector('.pg-hours tr[data-day="' + today + '"]');
      if (row) row.classList.add('is-today');
    } catch (err) { /* browser senza fusi orari: niente stato */ }
  }

  // I piatti entrano con una leggera dissolvenza
  var items = document.querySelectorAll('.reveal');
  if (reduced || !('IntersectionObserver' in window)) {
    items.forEach(function (el) { el.classList.add('is-in'); });
    return;
  }
  var io = new IntersectionObserver(function (es) {
    es.forEach(function (en) {
      if (!en.isIntersecting) return;
      en.target.classList.add('is-in');
      io.unobserve(en.target);
    });
  }, { rootMargin: '0px 0px -8% 0px' });
  items.forEach(function (el) { io.observe(el); });
})();
