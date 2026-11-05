// Kerää kaikki renderöityjen sivujen linkit (myös JS:n luomat) ja kirjoittaa ne JSON-listaksi.
const {chromium} = require('playwright');
const fs = require('fs');
(async () => {
  const ROOT = 'http://localhost:8765/';
  const out = process.argv[2];
  const ids = JSON.parse(fs.readFileSync(process.argv[3], 'utf8'));
  const b = await chromium.launch();
  const p = await b.newPage({viewport: {width: 1400, height: 1000}});
  const errs = [], links = [], missingCards = [];
  p.on('pageerror', e => errs.push(p.url() + ' ' + e.message));
  let LANG = '';
  const grab = async (where) => {
    const hs = await p.$$eval('a', as => as.map(a => ({href: a.getAttribute('href') ?? a.getAttribute('xlink:href'), abs: a.href && a.href.baseVal !== undefined ? a.href.baseVal : a.href, text: (a.textContent || '').trim().slice(0, 60)})));
    hs.forEach(h => links.push({...h, where: LANG + where}));
  };
  // suomenkieliset sivut juuressa, englanninkieliset en/-kansiossa
  for (LANG of ['', 'en/']) {
  const BASE = ROOT + LANG;
  // 1. jokainen sivu
  for (const pg of ['index.html', 'kartta.html', 'haku.html', 'esitys.html', 'ehdota.html']) {
    await p.goto(BASE + pg); await p.waitForTimeout(900); await grab(pg);
  }
  // 2. kartan kaikki näkymät ja kytkimet
  await p.goto(BASE + 'kartta.html'); await p.waitForTimeout(900);
  for (const v of ['map', 'net', 'hubs', 'matrix', 'overlap', 'output', 'prog']) {
    const t = await p.$(`[data-view="${v}"]`); if (!t) continue; await t.click(); await p.waitForTimeout(300);
    if (v === 'net') { for (const c of ['#net-miss', '#net-pubs', '#net-copub']) { const e = await p.$(c); if (e) await e.click(); } await p.waitForTimeout(300);
      for (const d of await p.$$('details')) await d.evaluate(x => x.open = true); }
    await grab('kartta.html:' + v);
  }
  // kartan solmupaneelit: napautetaan jokaista solmua verkossa
  await p.click('[data-view="net"]'); await p.waitForTimeout(300);
  const nodes = await p.$$('#net [data-id]');
  for (const n of nodes.slice(0, 400)) { try { await n.click({force: true, timeout: 500}); await grab('kartta.html:net-panel'); } catch (e) {} }
  // 3. haun jokainen hankekortti
  await p.goto(BASE + 'haku.html'); await p.waitForTimeout(900);
  for (const id of ids) {
    await p.evaluate(h => { location.hash = h; }, encodeURIComponent(id)); await p.waitForTimeout(40);
    const ok = await p.evaluate(id => { const c = document.querySelector('#card'); return !!c && c.textContent.includes(id); }, id);
    if (!ok) missingCards.push(LANG + id);
    await grab('haku.html#' + id);
  }
  // 4. esitys: kaikki maat ja vuodet 2014–2030
  await p.goto(BASE + 'esitys.html#alku=2014&loppu=2030'); await p.waitForTimeout(800);
  for (let y = 2014; y <= 2030; y++) { await p.evaluate(y => { const s = document.getElementById('slider'); s.value = y; s.dispatchEvent(new Event('input')); }, y); await p.waitForTimeout(60); await grab('esitys.html:' + y); }
  }
  fs.writeFileSync(out, JSON.stringify({links, errs, missingCards}, null, 0));
  console.log('linkkejä', links.length, 'virheitä', errs.length, 'puuttuvia kortteja', missingCards.length);
  await b.close();
})();
