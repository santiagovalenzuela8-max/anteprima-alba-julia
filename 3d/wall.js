/* La parete capitonné di Alba Iulia, in 3D.
   Rombi imbottiti con bottoni perlati; una luce calda segue il cursore
   e qualche cristallo, come quelli dei lampadari del locale, fluttua davanti. */
import * as THREE from 'three';
import { RoomEnvironment } from 'three/addons/environments/RoomEnvironment.js';

const canvas = document.getElementById('gl');
const hero = document.getElementById('hero');
const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
const coarse = matchMedia('(pointer: coarse)').matches;
const small = innerWidth < 768;

function webglOK() {
  try {
    const c = document.createElement('canvas');
    return !!(window.WebGLRenderingContext && (c.getContext('webgl2') || c.getContext('webgl')));
  } catch (e) { return false; }
}

if (canvas && webglOK()) init();

function init() {
  const renderer = new THREE.WebGLRenderer({ canvas, antialias: !small, alpha: false, powerPreference: 'high-performance' });
  renderer.setPixelRatio(Math.min(devicePixelRatio, small ? 1.5 : 2));
  renderer.outputColorSpace = THREE.SRGBColorSpace;
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = 1.05;
  renderer.setClearColor(0xf3ebe0, 1);

  const scene = new THREE.Scene();
  const pmrem = new THREE.PMREMGenerator(renderer);
  scene.environment = pmrem.fromScene(new RoomEnvironment(), 0.04).texture;
  scene.environmentIntensity = 0.35;

  const camera = new THREE.PerspectiveCamera(32, 1, 0.1, 60);
  camera.position.set(0, 0, 11);

  /* ---------- La parete ---------- */
  const S = small ? 1.05 : 0.9;         // lato del rombo
  const W = 26, H = 16;                 // abbondante, per coprire anche con l'inclinazione
  const seg = small ? 7 : 10;           // suddivisioni per rombo
  const geo = new THREE.PlaneGeometry(W, H, Math.round(W / S * seg), Math.round(H / S * seg));
  const pos = geo.attributes.position;
  const AMP = 0.2;
  const fract = (v) => v - Math.floor(v);
  for (let i = 0; i < pos.count; i++) {
    const x = pos.getX(i), y = pos.getY(i);
    const u = (x + y) / S, v = (x - y) / S;          // coordinate ruotate di 45°: celle a rombo
    const fu = fract(u) - 0.5, fv = fract(v) - 0.5;
    const a = Math.max(0, 1 - 4 * fu * fu), b = Math.max(0, 1 - 4 * fv * fv);
    let z = AMP * Math.pow(a * b, 0.55);             // cuscino gonfio al centro, cucitura ai bordi
    const du = 0.5 - Math.abs(fu), dv = 0.5 - Math.abs(fv);
    const d2 = du * du + dv * dv;
    z -= 0.07 * Math.exp(-d2 / 0.006);               // l'affossamento sotto al bottone
    pos.setZ(i, z);
  }
  geo.computeVertexNormals();

  const wallMat = new THREE.MeshPhysicalMaterial({
    color: 0xf6f0e8, roughness: 0.46, metalness: 0,
    sheen: 1, sheenColor: new THREE.Color(0xfff1e2), sheenRoughness: 0.45,
    clearcoat: 0.35, clearcoatRoughness: 0.35,
  });
  const wall = new THREE.Mesh(geo, wallMat);
  const group = new THREE.Group();
  group.add(wall);
  scene.add(group);

  /* Bottoni perlati agli incroci delle cuciture */
  const buttons = [];
  const nU = Math.ceil((W + H) / S) + 2;
  for (let iu = -nU; iu <= nU; iu++) {
    for (let iv = -nU; iv <= nU; iv++) {
      const x = (iu + iv) * S / 2, y = (iu - iv) * S / 2;
      if (Math.abs(x) < W / 2 - 0.1 && Math.abs(y) < H / 2 - 0.1) buttons.push([x, y]);
    }
  }
  const btnGeo = new THREE.SphereGeometry(0.055, 16, 12);
  const btnMat = new THREE.MeshPhysicalMaterial({ color: 0xefe6da, roughness: 0.22, metalness: 0.15, clearcoat: 1, clearcoatRoughness: 0.1 });
  const btn = new THREE.InstancedMesh(btnGeo, btnMat, buttons.length);
  const m4 = new THREE.Matrix4();
  buttons.forEach(([x, y], i) => { m4.makeScale(1, 1, 0.6).setPosition(x, y, -0.035); btn.setMatrixAt(i, m4); });
  group.add(btn);

  /* Cristalli dei lampadari */
  const CR = small ? 14 : 26;
  const crGeo = new THREE.OctahedronGeometry(0.075, 0);
  const crMat = new THREE.MeshPhysicalMaterial({ color: 0xfff6ea, metalness: 0.35, roughness: 0.08, envMapIntensity: 3, clearcoat: 1, clearcoatRoughness: 0.05, emissive: 0x5a4328, emissiveIntensity: 0.35, flatShading: true });
  const crystals = new THREE.InstancedMesh(crGeo, crMat, CR);
  const cr = Array.from({ length: CR }, () => ({
    x: 0.5 + Math.random() * 6.5, y: (Math.random() - 0.5) * 7, z: 1.2 + Math.random() * 3.2,
    s: 0.6 + Math.random() * 1.1, sp: 0.05 + Math.random() * 0.12, r: Math.random() * Math.PI * 2, rs: 0.3 + Math.random() * 0.9,
  }));
  scene.add(crystals);

  /* ---------- Luci ---------- */
  scene.add(new THREE.HemisphereLight(0xffe7c4, 0x6e2a26, 0.55));
  const key = new THREE.DirectionalLight(0xfff4e6, 1.25);
  key.position.set(-6, 7, 8);
  scene.add(key);
  const warm = new THREE.PointLight(0xffc27a, 26, 11, 1.6);   // la luce che segue il cursore
  warm.position.set(2, 1, 2.4);
  scene.add(warm);
  const rim = new THREE.PointLight(0xb98246, 10, 14, 1.8);
  rim.position.set(6, -3, 3);
  scene.add(rim);

  /* ---------- Interazione ---------- */
  const pointer = new THREE.Vector2(0.35, 0.1), smooth = pointer.clone();
  let hasPointer = false;
  hero.addEventListener('pointermove', (e) => {
    const r = hero.getBoundingClientRect();
    pointer.set(((e.clientX - r.left) / r.width) * 2 - 1, -((e.clientY - r.top) / r.height) * 2 + 1);
    hasPointer = true;
  }, { passive: true });

  let scrollK = 0;
  addEventListener('scroll', () => { scrollK = Math.min(1, scrollY / Math.max(1, hero.offsetHeight)); }, { passive: true });

  function resize() {
    const w = hero.clientWidth, h = hero.clientHeight;
    renderer.setSize(w, h, false);
    camera.aspect = w / h;
    camera.updateProjectionMatrix();
    // su schermi stretti la parete si avvicina un po'
    camera.position.z = w / h < 0.8 ? 9 : 11;
  }
  resize();
  addEventListener('resize', resize);

  let visible = true;
  new IntersectionObserver(([e]) => { visible = e.isIntersecting; if (visible) loop(); }).observe(hero);

  const clock = new THREE.Clock();
  const tmp = new THREE.Vector3();
  const q = new THREE.Quaternion(), eul = new THREE.Euler(), scl = new THREE.Vector3();
  let running = false;

  function frame() {
    const dt = Math.min(clock.getDelta(), 0.05);
    const t = clock.elapsedTime;

    // Su touch o senza mouse, la luce disegna lentamente un ovale sulla parete
    if (!hasPointer || coarse) pointer.set(Math.cos(t * 0.35) * 0.6, Math.sin(t * 0.5) * 0.45);
    smooth.lerp(pointer, 0.06);

    tmp.set(smooth.x, smooth.y, 0.5).unproject(camera).sub(camera.position).normalize();
    const dist = (2.4 - camera.position.z) / tmp.z;
    warm.position.copy(camera.position).addScaledVector(tmp, dist);

    group.rotation.y = smooth.x * 0.07;
    group.rotation.x = -smooth.y * 0.05 - scrollK * 0.35;
    group.position.y = scrollK * 1.6;

    for (let i = 0; i < CR; i++) {
      const c = cr[i];
      if (!reduced) { c.y -= c.sp * dt; c.r += c.rs * dt; }
      if (c.y < -4.5) { c.y = 4.5; c.x = small ? (Math.random() - 0.5) * 4 : 0.5 + Math.random() * 6.5; }
      eul.set(0.3, c.r, 0);
      q.setFromEuler(eul);
      scl.set(c.s, c.s * 1.9, c.s);
      m4.compose(tmp.set(c.x + Math.sin(t * 0.4 + i) * 0.15, c.y, c.z), q, scl);
      crystals.setMatrixAt(i, m4);
    }
    crystals.instanceMatrix.needsUpdate = true;

    renderer.render(scene, camera);
  }

  function loop() {
    if (running) return;
    running = true;
    const step = () => {
      if (!visible) { running = false; return; }
      frame();
      if (reduced) { running = false; return; }
      requestAnimationFrame(step);
    };
    requestAnimationFrame(step);
  }

  frame();
  canvas.classList.add('is-ready');
  document.documentElement.classList.add('has-gl');
  loop();
}
