/* La parete capitonné di Alba Iulia, in 3D.
   Versione leggera: geometria ridotta, materiali semplici, qualità adattiva
   e disegno solo quando serve (fermo quando la parete non è visibile o la pagina è nascosta). */
import * as THREE from 'three';

const canvas = document.getElementById('gl');
const hero = document.getElementById('hero');
const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
const coarse = matchMedia('(pointer: coarse)').matches;   // telefoni e tablet
const small = innerWidth < 768;
const lowPower = coarse || small || (navigator.hardwareConcurrency || 8) <= 4;

function webglOK() {
  try {
    const c = document.createElement('canvas');
    return !!(window.WebGLRenderingContext && (c.getContext('webgl2') || c.getContext('webgl')));
  } catch (e) { return false; }
}

if (canvas && webglOK()) init();

function init() {
  const renderer = new THREE.WebGLRenderer({ canvas, antialias: false, alpha: false, powerPreference: lowPower ? 'low-power' : 'high-performance', stencil: false });
  let dpr = Math.min(devicePixelRatio, lowPower ? 1 : 1.5);
  renderer.setPixelRatio(dpr);
  renderer.outputColorSpace = THREE.SRGBColorSpace;
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.setClearColor(0xf3ebe0, 1);

  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(32, 1, 0.1, 40);
  camera.position.set(0, 0, 11);

  /* ---------- La parete: rombi imbottiti ---------- */
  const S = small ? 1.1 : 0.9;
  const W = 20, H = 12;
  const seg = lowPower ? 6 : 10;
  const geo = new THREE.PlaneGeometry(W, H, Math.round(W / S * seg), Math.round(H / S * seg));
  const pos = geo.attributes.position;
  const fract = (v) => v - Math.floor(v);
  for (let i = 0; i < pos.count; i++) {
    const x = pos.getX(i), y = pos.getY(i);
    const fu = fract((x + y) / S) - 0.5, fv = fract((x - y) / S) - 0.5;
    const a = Math.max(0, 1 - 4 * fu * fu), b = Math.max(0, 1 - 4 * fv * fv);
    const du = 0.5 - Math.abs(fu), dv = 0.5 - Math.abs(fv);
    pos.setZ(i, 0.2 * Math.pow(a * b, 0.55) - 0.07 * Math.exp(-(du * du + dv * dv) / 0.006));
  }
  geo.computeVertexNormals();
  const group = new THREE.Group();
  group.add(new THREE.Mesh(geo, new THREE.MeshStandardMaterial({ color: 0xf6efe6, roughness: 0.5, metalness: 0 })));
  scene.add(group);

  /* Bottoni agli incroci delle cuciture */
  const pts = [];
  const n = Math.ceil((W + H) / S) + 2;
  for (let iu = -n; iu <= n; iu++) for (let iv = -n; iv <= n; iv++) {
    const x = (iu + iv) * S / 2, y = (iu - iv) * S / 2;
    if (Math.abs(x) < W / 2 - 0.1 && Math.abs(y) < H / 2 - 0.1) pts.push(x, y);
  }
  const btn = new THREE.InstancedMesh(
    new THREE.SphereGeometry(0.055, 10, 6),
    new THREE.MeshStandardMaterial({ color: 0xeee4d6, roughness: 0.25, metalness: 0.3 }),
    pts.length / 2
  );
  const m4 = new THREE.Matrix4();
  for (let i = 0; i < pts.length; i += 2) { m4.makeScale(1, 1, 0.6).setPosition(pts[i], pts[i + 1], -0.035); btn.setMatrixAt(i / 2, m4); }
  group.add(btn);

  /* Cristalli dei lampadari (pochi, e solo su computer) */
  const CR = lowPower ? 0 : 12;
  let crystals = null, cr = [];
  if (CR) {
    crystals = new THREE.InstancedMesh(
      new THREE.OctahedronGeometry(0.075, 0),
      new THREE.MeshStandardMaterial({ color: 0xfff4e4, roughness: 0.12, metalness: 0.4, emissive: 0x4a3620, emissiveIntensity: 0.45, flatShading: true }),
      CR
    );
    cr = Array.from({ length: CR }, () => ({ x: 0.5 + Math.random() * 6.5, y: (Math.random() - 0.5) * 7, z: 1.2 + Math.random() * 3, s: 0.7 + Math.random(), sp: 0.05 + Math.random() * 0.1, r: Math.random() * 6.3, rs: 0.3 + Math.random() * 0.8 }));
    scene.add(crystals);
  }

  /* ---------- Luci: poche e calde ---------- */
  scene.add(new THREE.HemisphereLight(0xffe7c4, 0x7a3a33, 0.55));
  // luce dall'alto al centro: illumina allo stesso modo entrambe le diagonali dei rombi
  const key = new THREE.DirectionalLight(0xfff4e6, 1.35);
  key.position.set(0, 9, 5);
  scene.add(key);
  const fill = new THREE.DirectionalLight(0xffe2c0, 0.35);
  fill.position.set(0, -6, 6);
  scene.add(fill);
  const warm = new THREE.PointLight(0xffc27a, 24, 10, 1.6);   // segue il cursore
  scene.add(warm);

  /* ---------- Interazione ---------- */
  const pointer = new THREE.Vector2(0.35, 0.1), smooth = pointer.clone();
  let lastMove = -1e9;
  if (!coarse) hero.addEventListener('pointermove', (e) => {
    const r = hero.getBoundingClientRect();
    pointer.set(((e.clientX - r.left) / r.width) * 2 - 1, -((e.clientY - r.top) / r.height) * 2 + 1);
    lastMove = performance.now();
  }, { passive: true });

  let scrollK = 0;
  addEventListener('scroll', () => { scrollK = Math.min(1, Math.max(0, -hero.getBoundingClientRect().top / Math.max(1, hero.offsetHeight))); }, { passive: true });

  let lastW = 0, lastH = 0;
  function resize() {
    const w = hero.clientWidth, h = hero.clientHeight;
    // sui telefoni la barra del browser cambia solo l'altezza: ignoriamo i piccoli scatti
    if (w === lastW && Math.abs(h - lastH) < 120) return;
    lastW = w; lastH = h;
    renderer.setSize(w, h, false);
    camera.aspect = w / h;
    camera.position.z = w / h < 0.8 ? 9 : 11;
    camera.updateProjectionMatrix();
  }
  resize();
  addEventListener('resize', resize);

  let visible = true, pageVisible = !document.hidden, running = false;
  new IntersectionObserver(([e]) => { visible = e.isIntersecting; wake(); }).observe(hero);
  document.addEventListener('visibilitychange', () => { pageVisible = !document.hidden; wake(); });

  const dir = new THREE.Vector3(), tmp = new THREE.Vector3(), q = new THREE.Quaternion(), eul = new THREE.Euler(), scl = new THREE.Vector3();
  let t = 0, prev = performance.now(), acc = 0;
  // Sui dispositivi leggeri si disegna a 30 fotogrammi al secondo: la luce si muove lenta, basta e avanza
  const minStep = lowPower ? 1000 / 30 - 2 : 0;

  /* Qualità adattiva: se i fotogrammi arrivano lenti, si abbassa la risoluzione */
  let samples = 0, slow = 0, tuned = false;
  function adapt(gap) {
    if (tuned) return;
    samples++;
    if (gap > (lowPower ? 45 : 24)) slow++;
    if (samples === 90) {
      if (slow > 30 && dpr > 0.75) { dpr = Math.max(0.75, dpr - 0.35); renderer.setPixelRatio(dpr); lastW = 0; resize(); }
      else tuned = true;
      samples = slow = 0;
    }
  }

  function draw(dt) {
    t += dt;
    if (coarse || performance.now() - lastMove > 2500) pointer.set(Math.cos(t * 0.3) * 0.6, Math.sin(t * 0.42) * 0.45);
    smooth.lerp(pointer, coarse ? 0.05 : 0.08);

    dir.set(smooth.x, smooth.y, 0.5).unproject(camera).sub(camera.position).normalize();
    warm.position.copy(camera.position).addScaledVector(dir, (2.4 - camera.position.z) / dir.z);

    group.rotation.y = smooth.x * 0.07;
    group.rotation.x = -smooth.y * 0.05 - scrollK * 0.35;
    group.position.y = scrollK * 1.6;

    if (crystals) {
      for (let i = 0; i < CR; i++) {
        const c = cr[i];
        c.y -= c.sp * dt; c.r += c.rs * dt;
        if (c.y < -4.5) { c.y = 4.5; c.x = 0.5 + Math.random() * 6.5; }
        eul.set(0.3, c.r, 0); q.setFromEuler(eul); scl.set(c.s, c.s * 1.9, c.s);
        m4.compose(tmp.set(c.x, c.y, c.z), q, scl);
        crystals.setMatrixAt(i, m4);
      }
      crystals.instanceMatrix.needsUpdate = true;
    }
    renderer.render(scene, camera);
  }

  function loop(now) {
    if (!visible || !pageVisible || reduced) { running = false; return; }
    acc += now - prev; prev = now;
    if (acc >= minStep) {
      adapt(acc);
      draw(Math.min(acc, 50) / 1000);
      acc = 0;
    }
    requestAnimationFrame(loop);
  }
  function wake() {
    if (running || !visible || !pageVisible || reduced) return;
    running = true; prev = performance.now(); acc = 0;
    requestAnimationFrame(loop);
  }

  draw(0);
  canvas.classList.add('is-ready');
  document.documentElement.classList.add('has-gl');
  wake();
}
