/* Il fuoco: il video avanza con lo scroll.
   Il video è stato diviso in fotogrammi WebP (fuoco/d = computer, fuoco/m = telefono, uno ogni due).
   I fotogrammi si scaricano solo quando la sezione si avvicina e si disegnano su canvas
   solo quando cambia il fotogramma: fluido anche su iPhone, dove "sfogliare" un <video> scatta. */
(function () {
  'use strict';
  var section = document.getElementById('fuoco');
  var canvas = document.getElementById('fire-canvas');
  if (!section || !canvas) return;

  var reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
  var mobile = matchMedia('(max-width: 900px), (pointer: coarse)').matches;
  var TOTAL = 105;                          // fotogrammi del video originale (4,2 s a 25 fps)
  var STEP = mobile ? 2 : 1;                // sul telefono uno ogni due
  var DIR = mobile ? 'fuoco/m/' : 'fuoco/d/';
  var list = [];
  for (var n = 1; n <= TOTAL; n += STEP) list.push(DIR + String(n).padStart(3, '0') + '.webp');
  var N = list.length;

  var ctx = canvas.getContext('2d', { alpha: false });
  var frames = new Array(N), loaded = 0, started = false;
  var current = -1, wanted = 0, ticking = false;
  var lines = section.querySelectorAll('.fire__line');
  var bar = document.getElementById('fire-progress');
  var stick = section.querySelector('.fire__stick');
  var hint = section.querySelector('.fire__hint');

  // Primo fotogramma subito come sfondo, così la sezione non è mai vuota
  canvas.style.backgroundImage = 'url(' + list[0] + ')';

  function size() {
    var dpr = Math.min(devicePixelRatio || 1, mobile ? 1.5 : 1.75);
    var w = Math.round(canvas.clientWidth * dpr), h = Math.round(canvas.clientHeight * dpr);
    if (canvas.width !== w || canvas.height !== h) { canvas.width = w; canvas.height = h; current = -1; }
  }

  function draw(i) {
    // se il fotogramma non è ancora arrivato, usa il più vicino già caricato
    var img = frames[i], exact = true;
    if (!img || !img.complete || !img.naturalWidth) {
      exact = false;
      for (var d = 1; d < N; d++) {
        var a = frames[i - d], b = frames[i + d];
        if (a && a.naturalWidth) { img = a; break; }
        if (b && b.naturalWidth) { img = b; break; }
      }
      if (!img || !img.naturalWidth) return;
    }
    var cw = canvas.width, ch = canvas.height, iw = img.naturalWidth, ih = img.naturalHeight;
    var s = Math.max(cw / iw, ch / ih);                     // effetto "cover"
    var w = iw * s, h = ih * s;
    // su schermi verticali inquadriamo la fiamma (un po' a sinistra del centro)
    var fx = cw / ch < 1 ? 0.42 : 0.5;
    ctx.drawImage(img, (cw - w) * fx, (ch - h) / 2, w, h);
    // se abbiamo disegnato un fotogramma vicino, quello giusto verrà ridisegnato appena arriva
    current = exact ? i : -2;
  }

  function load() {
    if (started) return;
    started = true;
    // prima un fotogramma ogni 8 (per avere subito tutto il movimento), poi gli altri
    var order = [];
    for (var k = 0; k < N; k += 8) order.push(k);
    for (var j = 0; j < N; j++) if (j % 8) order.push(j);
    var i = 0, inflight = 0, MAX = 6;
    function next() {
      while (inflight < MAX && i < order.length) {
        (function (idx) {
          var img = new Image();
          img.decoding = 'async';
          inflight++;
          img.onload = img.onerror = function () {
            inflight--; loaded++;
            if (idx === wanted || current < 0) request();
            next();
          };
          img.src = list[idx];
          frames[idx] = img;
        })(order[i++]);
      }
    }
    next();
  }

  function progress() {
    var r = section.getBoundingClientRect();
    var total = section.offsetHeight - stick.offsetHeight;
    return total > 0 ? Math.min(1, Math.max(0, -r.top / total)) : 0;
  }

  function update() {
    ticking = false;
    var p = reduced ? 0.55 : progress();
    wanted = Math.min(N - 1, Math.round(p * (N - 1)));
    if (wanted !== current) draw(wanted);
    // la fiamma "scalda" la scena, e i testi entrano a metà percorso
    section.style.setProperty('--heat', (0.12 + 0.28 * Math.sin(p * Math.PI)).toFixed(3));
    if (bar) bar.style.transform = 'scaleX(' + p.toFixed(3) + ')';
    // è la prima sezione: il titolo è visibile da subito, il resto entra scorrendo
    lines[0] && lines[0].classList.add('is-on');
    lines[1] && lines[1].classList.toggle('is-on', p > 0.22 || reduced);
    lines[2] && lines[2].classList.toggle('is-on', p > 0.4 || reduced);
    if (hint) hint.classList.toggle('is-off', p > 0.04);
  }
  function request() { if (!ticking) { ticking = true; requestAnimationFrame(update); } }

  // Scarica quando la sezione è a circa due schermi di distanza
  if ('IntersectionObserver' in window) {
    new IntersectionObserver(function (es) { if (es[0].isIntersecting) load(); }, { rootMargin: '200% 0px' }).observe(section);
    var near = false;
    new IntersectionObserver(function (es) { near = es[0].isIntersecting; if (near) { size(); request(); } }).observe(section);
    addEventListener('scroll', function () { if (near) request(); }, { passive: true });
  } else {
    load();
    addEventListener('scroll', request, { passive: true });
  }
  addEventListener('resize', function () { size(); request(); });
  size();
  request();
})();
