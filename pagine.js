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
