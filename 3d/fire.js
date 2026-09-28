/* Video guidati dallo scroll (il fuoco, il dolce, ...).
   Ogni video è diviso in fotogrammi WebP numerati 001, 002, ... in due cartelle:
   <dir>/d = computer, <dir>/m = telefono (meno fotogrammi e più piccoli).
   Nell'HTML ogni sezione dichiara: data-dir, data-count-d, data-count-m e, se serve,
   data-first (titolo visibile da subito) e data-focus (dove inquadrare sugli schermi verticali, 0–1).
   I fotogrammi si scaricano solo quando la sezione si avvicina e si disegnano su canvas
   solo quando cambia il fotogramma: fluido anche su iPhone, dove "sfogliare" un <video> scatta. */
(function () {
  'use strict';
  var reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
  var mobile = matchMedia('(max-width: 900px), (pointer: coarse)').matches;

  document.querySelectorAll('.scrollvid[data-dir]').forEach(setup);

  function setup(section) {
    var canvas = section.querySelector('.fire__canvas');
    var stick = section.querySelector('.fire__stick');
    if (!canvas || !stick) return;

    var dir = section.getAttribute('data-dir') + (mobile ? '/m/' : '/d/');
    var count = +section.getAttribute(mobile ? 'data-count-m' : 'data-count-d');
    var focus = parseFloat(section.getAttribute('data-focus') || '0.5');
    var first = section.hasAttribute('data-first');
    var list = [];
    for (var n = 1; n <= count; n++) list.push(dir + String(n).padStart(3, '0') + '.webp');
    var N = list.length;
    if (!N) return;

    var ctx = canvas.getContext('2d', { alpha: false });
    var frames = new Array(N), started = false;
    var current = -1, wanted = 0, ticking = false, near = false;
    var lines = section.querySelectorAll('.fire__line');
    var bar = section.querySelector('.fire__bar i');
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
      var fx = cw / ch < 1 ? focus : 0.5;                     // inquadratura sugli schermi verticali
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
              inflight--;
              if (near && (idx === wanted || current < 0)) request();
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
      section.style.setProperty('--heat', (0.12 + 0.28 * Math.sin(p * Math.PI)).toFixed(3));
      if (bar) bar.style.transform = 'scaleX(' + p.toFixed(3) + ')';
      // il titolo entra subito (o è già visibile se è la prima sezione), il resto scorrendo
      lines[0] && lines[0].classList.toggle('is-on', first || p > 0.08 || reduced);
      lines[1] && lines[1].classList.toggle('is-on', p > 0.22 || reduced);
      lines[2] && lines[2].classList.toggle('is-on', p > 0.4 || reduced);
      if (hint) hint.classList.toggle('is-off', p > 0.04);
    }
    function request() { if (!ticking) { ticking = true; requestAnimationFrame(update); } }

    // Scarica quando la sezione è a circa due schermi di distanza
    if ('IntersectionObserver' in window) {
      new IntersectionObserver(function (es) { if (es[0].isIntersecting) load(); }, { rootMargin: '200% 0px' }).observe(section);
      new IntersectionObserver(function (es) { near = es[0].isIntersecting; if (near) { size(); request(); } }).observe(section);
      addEventListener('scroll', function () { if (near) request(); }, { passive: true });
    } else {
      near = true;
      load();
      addEventListener('scroll', request, { passive: true });
    }
    addEventListener('resize', function () { if (near) { size(); request(); } });
    size();
    request();
  }
})();
