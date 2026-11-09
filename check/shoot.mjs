// Controllo del sito pubblicato: stato HTTP, errori JS, scorrimento laterale e screenshot
import { chromium, devices } from 'playwright';
import fs from 'fs';
const BASE = 'https://albaiulia.it';
const PAGES = ['/', '/il-titolare', '/il-locale', '/menu', '/menu/grigliate', '/macelleria', '/galleria', '/dove-siamo'];
const out = []; fs.mkdirSync('shots', { recursive: true });
const b = await chromium.launch();
for (const [dev, opts] of [['iphone', devices['iPhone 13']], ['desktop', { viewport: { width: 1440, height: 900 } }]]) {
  const ctx = await b.newContext(opts);
  for (const path of PAGES) {
    const p = await ctx.newPage(); const errs = [];
    p.on('pageerror', e => errs.push('JS: ' + e.message));
    p.on('console', m => m.type() === 'error' && errs.push('console: ' + m.text().slice(0, 200)));
    p.on('response', r => r.status() >= 400 && errs.push(r.status() + ' ' + r.url()));
    const res = await p.goto(BASE + path, { waitUntil: 'load', timeout: 60000 }).catch(e => (errs.push('goto ' + e.message), null));
    await p.waitForTimeout(2500);
    const H = await p.evaluate(() => document.documentElement.scrollHeight);
    const vh = p.viewportSize().height; let k = 0;
    for (let y = 0; y < H && k < (path === '/' ? 26 : 10); y += Math.round(vh * 0.85), k++) {
      await p.evaluate(y => scrollTo(0, y), y); await p.waitForTimeout(500);
      const ow = await p.evaluate(() => document.documentElement.scrollWidth - innerWidth);
      if (ow > 0) errs.push(`overflow ${ow}px y=${y}`);
      await p.screenshot({ path: `shots/${dev}${path.replace(/\//g, '_') || '_home'}-${String(k).padStart(2, '0')}.jpg`, quality: 60 });
    }
    out.push({ dev, path, status: res && res.status(), url: p.url(), errs: [...new Set(errs)] });
    await p.close();
  }
  await ctx.close();
}
await b.close();
fs.writeFileSync('shots/report.json', JSON.stringify(out, null, 1));
console.log(JSON.stringify(out, null, 1));
