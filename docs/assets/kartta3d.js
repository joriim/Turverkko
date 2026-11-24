// Turverkko 3D: hankkeet kartalla, korkeus = aloitusvuosi (vanhin alimpana).
// Ei ulkoisia kirjastoja: oma perspektiiviprojektio canvasille. Rajat: assets/rajat.js (window.RAJAT).
// Sijainnit ovat likimääräisiä: maakunnan, läänin tai maan keskipiste (ALUEET alla). Saman paikan
// ja vuoden hankkeet levitetään spiraaliksi, jotta ne eivät peitä toisiaan.
window.Kartta3D = (() => {
  const EN = TV.LANG === "en";
  const T = EN ? {
    year: "Start year", org: "Organisation", hub: "Competence centre", proj: "Project", noYear: "projects without a start year are not shown",
    open: "Open project card", partners: "participants", none: "No organisations linked in the data", multi: "multi-country", projects: "projects"
  } : {
    year: "Aloitusvuosi", org: "Organisaatio", hub: "Osaamiskeskus", proj: "Hanke", noYear: "hanketta ilman aloitusvuotta ei näy",
    open: "Avaa hankekortti", partners: "osallistujaa", none: "Aineistossa ei ole toimijoita", multi: "useita maita", projects: "hanketta"
  };

  // Likimääräiset keskipisteet [pituus, leveys]. Avain on alueen nimen alku pienillä kirjaimilla.
  const ALUEET = {
    FI: {"etelä-pohjanma": [23.0, 62.8], "etela-pohjanma": [23.0, 62.8], "keski-pohjanma": [24.0, 63.7], "pohjanmaa": [21.9, 63.0], "kainuu": [28.4, 64.4],
      "keski-suom": [25.5, 62.4], "kymenlaakso": [26.8, 60.7], "lappi": [26.0, 67.5], "lapin": [26.0, 67.5], "pirkanmaa": [23.7, 61.7], "pohjois-karjala": [30.0, 62.8],
      "pohjois-pohjanmaa": [26.0, 65.0], "pohjois-savo": [27.6, 63.0], "satakunta": [22.0, 61.5], "uusimaa": [24.9, 60.4], "uudenmaa": [24.9, 60.4],
      "etelä-savo": [27.5, 61.7], "varsinais-suomi": [22.5, 60.6], "päijät-häme": [25.7, 61.2], "kanta-häme": [24.4, 60.9], "etelä-karjala": [28.2, 61.1],
      "itä-suome": [28.5, 62.5], "kaakkois-suome": [27.5, 60.8], "pohjois-suome": [26.5, 66.0], "alavus": [23.6, 62.6], "kannus": [23.9, 63.9],
      "kokkola": [23.1, 63.8], "kotka": [26.9, 60.5], "kouvola": [26.7, 60.9], "lapua": [23.0, 62.97], "miehikkälä": [27.7, 60.67], "pyhtää": [26.55, 60.5],
      "virolahti": [27.7, 60.58], "ähtäri": [24.07, 62.55], "hamina": [27.2, 60.57], "seinäjoki": [22.84, 62.79]},
    EE: {"harju": [24.9, 59.3], "ida-viru": [27.4, 59.2], "jõgeva": [26.4, 58.75], "lääne-viru": [26.3, 59.2], "lääne": [23.6, 58.95], "pärnu": [24.5, 58.4],
      "tartu": [26.7, 58.4], "viljandi": [25.6, 58.35], "valga": [26.1, 57.9], "võru": [27.0, 57.75], "põlva": [27.1, 58.05], "rapla": [24.8, 58.95],
      "järva": [25.6, 58.9], "saare": [22.5, 58.4], "hiiu": [22.6, 58.9]},
    LV: {"alūksnes": [27.05, 57.42], "augšdaugavas": [26.5, 55.9], "balvu": [27.25, 57.13], "cēsu": [25.27, 57.3], "dienvidkurzemes": [21.3, 56.6],
      "gulbenes": [26.75, 57.18], "jelgavas": [23.7, 56.6], "jēkabpils": [25.9, 56.5], "līvānu": [26.18, 56.35], "talsu": [22.6, 57.25], "valkas": [25.95, 57.75],
      "valmieras": [25.4, 57.55], "ventspils": [21.6, 57.3], "kurzeme": [21.8, 56.9], "latgale": [27.3, 56.4], "pierīga": [24.4, 57.05], "rīga": [24.1, 56.95],
      "vidzeme": [25.8, 57.3], "zemgale": [24.0, 56.5]},
    IE: {"border": [-7.6, 54.3], "mid-east": [-6.6, 53.2], "midlands": [-7.6, 53.3], "south-east": [-7.0, 52.5], "south-west": [-9.0, 51.9],
      "west": [-9.0, 53.5], "dublin": [-6.26, 53.35], "mid-west": [-8.8, 52.6]},
    SE: {"blekinge": [15.3, 56.2], "halland": [12.8, 56.9], "norrbotten": [21.0, 66.8], "skåne": [13.5, 55.9], "stockholm": [18.1, 59.4],
      "södermanland": [16.6, 59.1], "västmanland": [16.2, 59.7], "västra götaland": [12.5, 58.3], "örebro": [15.0, 59.3], "östergötland": [15.6, 58.4],
      "aurora": [20.5, 65.5], "jämtland": [14.5, 63.2], "västerbotten": [18.5, 64.8], "västernorrland": [17.5, 63.0], "dalarna": [14.5, 61.0],
      "värmland": [13.2, 59.8], "uppsala": [17.6, 60.0], "gävleborg": [16.4, 61.4], "jönköping": [14.4, 57.6], "kronoberg": [14.6, 56.8], "kalmar": [16.2, 57.2], "gotland": [18.5, 57.5]},
    DK: {"köpenhamns omnejd": [12.3, 55.7], "köpenhamns stad": [12.57, 55.68], "vest- och sydsjälland": [11.6, 55.35], "östsjälland": [12.1, 55.45]},
    "DE-NI": {"ammerland": [7.95, 53.2], "braunschweig": [10.52, 52.27], "cloppenburg": [7.95, 52.85], "cuxhaven": [8.7, 53.7], "diepholz": [8.6, 52.65],
      "emsland": [7.35, 52.75], "friesland": [7.95, 53.5], "gifhorn": [10.55, 52.55], "grafschaft bentheim": [7.05, 52.45], "göttingen": [10.0, 51.55],
      "holzminden": [9.6, 51.85], "lüneburg": [10.6, 53.2], "northeim": [9.95, 51.75], "oldenburg": [8.3, 52.95], "osterholz": [8.85, 53.25],
      "rotenburg": [9.3, 53.15], "stade": [9.35, 53.55], "vechta": [8.3, 52.7], "verden": [9.25, 52.95]}
  };
  const MAA = {FI: [25.2, 62.6], SE: [15.5, 59.8], EE: [25.6, 58.7], LV: [24.9, 56.9], IE: [-7.8, 53.2], "DE-NI": [9.2, 52.75], "DE-SH": [9.8, 54.2], EU: [19.0, 58.0]};
  const LON0 = 13.5, LAT0 = 59, KX = Math.cos(LAT0 * Math.PI / 180);
  const geo = ([lon, lat]) => [(lon - LON0) * KX, lat - LAT0];

  function locate(p) {
    const regs = (p.regions && p.regions.length ? p.regions : [p.region || ""]).map(r => String(r).toLowerCase().replace(/^[(\s]+|[)\s]+$/g, ""));
    const hits = [];
    for (const r of regs) {
      for (const tab of [ALUEET[p.country], ALUEET.DK, ALUEET.SE].filter(Boolean)) {
        const k = Object.keys(tab).sort((a, b) => b.length - a.length).find(k => r.startsWith(k) || r.includes(k));
        if (k) { hits.push(tab[k]); break; }
      }
    }
    if (!hits.length) return {ll: MAA[p.country] || MAA.EU, exact: false};
    return {ll: [hits.reduce((a, h) => a + h[0], 0) / hits.length, hits.reduce((a, h) => a + h[1], 0) / hits.length], exact: true};
  }

  const css = n => getComputedStyle(document.documentElement).getPropertyValue(n).trim();
  const FUNDVAR = {JTF: "--c-FI", EAKR: "--c-DE-NI", Interreg: "--c-EE", EIP: "--c-SE", MSR: "--c-LV", LIFE: "--c-IE", Horizon: "--c-EU", Kansallinen: "--c-8"};
  const THEMEVAR = {T1: "--c-FI", T2: "--c-SE", T3: "--c-EE", T4: "--c-LV", T5: "--c-IE", T6: "--c-DE-NI", T7: "--c-EU", T8: "--c-8"};
  const hash = s => { let h = 2166136261; for (const c of s) h = Math.imul(h ^ c.charCodeAt(0), 16777619); return (h >>> 0) / 4294967296; };

  function build(ds, net) {
    const years = ds.projects.map(p => parseInt(p.start)).filter(Number.isFinite);
    const y0 = Math.min(...years), y1 = Math.max(...years);
    const ZS = 13 / Math.max(8, y1 - y0 + 1);           // koko aikajana noin 13 yksikköä (kartta noin 23 leveä)
    const zOf = y => (y - y0 + 0.5) * ZS;
    const groups = {}, nodes = {}, P = [];
    let noYear = 0;
    for (const p of ds.projects) {
      const y = parseInt(p.start);
      if (!Number.isFinite(y)) { noYear++; continue; }
      const {ll, exact} = locate(p);
      const key = ll.join() + "|" + y, i = (groups[key] = (groups[key] || 0) + 1) - 1;
      let [gx, gy] = geo(ll);
      if (!exact) { const rr = 1.6 * Math.sqrt(hash(p.id)), aa = hash(p.id + "a") * 6.283; gx += rr * Math.cos(aa); gy += rr * Math.sin(aa) * 0.8; }
      const r = exact && i ? 0.16 * Math.sqrt(i) : 0, a = i * 2.4 + hash(p.id) * 0.5;
      const eur = +p.eur_total || 0;
      const n = {id: p.id, kind: "hanke", p, x: gx + r * Math.cos(a), y: gy + r * Math.sin(a), z: zOf(y), gx, gy, year: y,
                 size: 2.2 + Math.min(7, Math.sqrt(eur / 1e5) * 0.9), links: []};
      nodes[p.id] = n; P.push(n);
    }
    // Organisaatiot maan pinnalle kotimaansa hankkeiden keskipisteeseen; osaamiskeskukset aloitusvuotensa korkeudelle
    const byId = Object.fromEntries(net.nodes.map(n => [n.id, n]));
    const E = [], other = {};
    for (const e of net.edges) {
      if (!["osallistuu", "kuuluu_keskukseen"].includes(e.kind)) continue;
      const pr = nodes[e.target] || nodes[e.source], oid = nodes[e.target] ? e.source : e.target, on = byId[oid];
      if (!pr || !on || nodes[oid] || !["organisaatio", "osaamiskeskus"].includes(on.kind)) continue;
      const o = other[oid] = other[oid] || {id: oid, kind: on.kind, n: on, members: [], links: []};
      o.members.push(pr);
      E.push({a: o, b: pr, weak: e.evidence === "vahvistamatta"});
    }
    const O = Object.values(other);
    for (const o of O) {
      const home = o.members.filter(m => m.p.country === o.n.country);
      const ms = home.length ? home : o.members;
      o.x = ms.reduce((a, m) => a + m.gx, 0) / ms.length + (hash(o.id) - 0.5) * 0.35;
      o.y = ms.reduce((a, m) => a + m.gy, 0) / ms.length + (hash(o.id + "y") - 0.5) * 0.35;
      const hy = o.kind === "osaamiskeskus" && parseInt(o.n.years);
      o.z = hy ? zOf(Math.min(Math.max(hy, y0), y1)) : 0;
      o.size = o.kind === "osaamiskeskus" ? 7 : 1.6 + Math.min(4, Math.sqrt(o.members.length) * 0.9);
    }
    for (const e of E) { e.a.links.push(e); e.b.links.push(e); }
    return {P, O, E, y0, y1, zOf, noYear, zMid: zOf(y1) / 2};
  }

  function open(host, data, ui) {
    const M = build(data.ds, data.net);
    const cv = host.querySelector("canvas"), ctx = cv.getContext("2d"), tip = host.querySelector(".t3-tip");
    const info = host.querySelector(".t3-info");
    const reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;
    const S = {yaw: -0.35, pitch: 1.0, zoom: 1, panX: 0, panY: 0, mode: ui.mode.value, orgs: ui.orgs.checked, par: ui.par.checked,
               upTo: M.y1, hover: null, sel: null, spin: !reduce, dpr: 1, W: 0, H: 0};
    ui.year.min = M.y0; ui.year.max = M.y1; ui.year.value = M.y1; ui.yearOut.textContent = M.y1;
    ui.note.textContent = M.noYear ? `${M.noYear} ${T.noYear}.` : "";
    const missing = data.an.missing_links.filter(m => m.tyyppi === "rinnakkainen ilman yhteyttä" || m.tyyppi === "puuttuva yhteys");
    const PN = Object.fromEntries(M.P.map(n => [n.id, n]));
    let C = {};
    const colors = () => {
      C = {bg: css("--bg"), fg: css("--fg"), muted: css("--muted"), line: css("--line"), sunk: css("--sunk"), hot: css("--hot"), x: css("--c-X"), surf: css("--surface")};
      for (const k of ["FI", "SE", "EE", "LV", "IE", "DE-NI", "EU", "8"]) C["c" + k] = css("--c-" + k);
    };
    const ccol = c => C["c" + c] || C.x;
    const col = n => {
      if (n.kind !== "hanke") return ccol(n.n.country);
      if (S.mode === "fund") return FUNDVAR[n.p.fund] ? css(FUNDVAR[n.p.fund]) : C.x;
      if (S.mode === "theme") return n.p.themes && n.p.themes[0] ? css(THEMEVAR[n.p.themes[0]]) : C.x;
      return ccol(n.p.country);
    };
    const legend = () => {
      const items = S.mode === "fund" ? Object.keys(FUNDVAR).map(k => [TV.FUND[k] || k, css(FUNDVAR[k])]).concat([[TV.FUND["?"], C.x]])
        : S.mode === "theme" ? Object.keys(THEMEVAR).map(k => [k + " " + TV.v(data.ds.themes[k] || ""), css(THEMEVAR[k])])
        : ["FI", "SE", "EE", "LV", "IE", "DE-NI", "EU"].map(k => [TV.COUNTRY[k], ccol(k)]);
      ui.legend.innerHTML = items.map(([t, c]) => `<span><i style="background:${c}"></i>${TV.esc(t)}</span>`).join("");
    };

    function resize() {
      const r = cv.getBoundingClientRect();
      S.dpr = Math.min(2, devicePixelRatio || 1); S.W = r.width; S.H = r.height;
      cv.width = Math.round(r.width * S.dpr); cv.height = Math.round(r.height * S.dpr);
    }
    // Projektio: kierto z-akselin ympäri (yaw), kallistus (pitch: 0 = suoraan ylhäältä, π/2 = sivulta), perspektiivi
    function proj(x, y, z) {
      const zc = z - M.zMid * 0.8, yc = y + 1.5;
      const cy = Math.cos(S.yaw), sy = Math.sin(S.yaw), cp = Math.cos(S.pitch), sp = Math.sin(S.pitch);
      const x1 = x * cy - yc * sy, y1 = x * sy + yc * cy;
      const up = y1 * cp + zc * sp, toward = zc * cp - y1 * sp;
      const s = Math.min(S.W, S.H) * 0.04 * S.zoom * 110 / Math.max(20, 110 - toward);   // lievä perspektiivi
      return [S.W / 2 + S.panX + x1 * s, S.H / 2 + S.panY - up * s, 110 - toward, s];
    }
    function draw() {
      const W = S.W, H = S.H;
      ctx.setTransform(S.dpr, 0, 0, S.dpr, 0, 0);
      ctx.fillStyle = C.bg; ctx.fillRect(0, 0, W, H);
      // Kartta maan pinnalla (z = 0)
      const edge = (lon, lat) => lon <= -11.5 || lon >= 33 || lat <= 47.5 || lat >= 71.5;
      for (const [code, rings] of Object.entries(window.RAJAT || {})) {
        const inScope = ["FI", "SE", "EE", "LV", "IE", "DE"].includes(code);
        const Q = rings.map(r => { const out = []; for (let i = 0; i < r.length; i += 2) { const [x, y] = geo([r[i], r[i + 1]]); out.push([...proj(x, y, 0), edge(r[i], r[i + 1])]); } return out; });
        ctx.beginPath();
        for (const r of Q) { r.forEach((q, i) => i ? ctx.lineTo(q[0], q[1]) : ctx.moveTo(q[0], q[1])); ctx.closePath(); }
        if (code !== "RU" && code !== "BY") { ctx.fillStyle = inScope ? C.sunk : C.surf; ctx.globalAlpha = inScope ? 0.9 : 0.6; ctx.fill(); ctx.globalAlpha = 1; }
        ctx.beginPath();
        for (const r of Q) r.forEach((q, i) => { const pv = r[(i || r.length) - 1]; if (q[4] && pv[4]) ctx.moveTo(q[0], q[1]); else { ctx.moveTo(pv[0], pv[1]); ctx.lineTo(q[0], q[1]); } });
        ctx.strokeStyle = C.line; ctx.lineWidth = 1; ctx.stroke();
      }
      // Vuosiasteikko: pystytolppa kartan lounaiskulmassa
      const base = geo([-11, 50.5]);
      const b0 = proj(base[0], base[1], 0), b1 = proj(base[0], base[1], M.zOf(M.y1) + 0.6);
      ctx.strokeStyle = C.muted; ctx.lineWidth = 1.5; ctx.beginPath(); ctx.moveTo(b0[0], b0[1]); ctx.lineTo(b1[0], b1[1]); ctx.stroke();
      ctx.font = "11px ui-monospace, Menlo, monospace"; ctx.fillStyle = C.muted; ctx.textAlign = "right"; ctx.textBaseline = "middle";
      for (let y = M.y0; y <= M.y1; y++) {
        if ((y - M.y0) % 2 && y !== M.y1) continue;
        const q = proj(base[0], base[1], M.zOf(y));
        ctx.fillRect(q[0] - 3, q[1] - 0.5, 6, 1); ctx.fillText(y, q[0] - 6, q[1]);
      }
      ctx.textAlign = "left"; ctx.fillText(T.year, b1[0] + 6, b1[1]);
      const vis = n => n.kind !== "hanke" || n.year <= S.upTo;
      const sel = S.sel, focus = sel && new Set([sel.id, ...sel.links.map(e => e.a === sel ? e.b.id : e.a.id)]);
      // Varret: hanke -> maan pinta
      ctx.lineWidth = 1;
      for (const n of M.P) {
        if (!vis(n)) continue;
        const a = proj(n.x, n.y, 0), b = proj(n.x, n.y, n.z);
        ctx.strokeStyle = C.muted; ctx.globalAlpha = focus ? (focus.has(n.id) ? 0.5 : 0.04) : 0.12;
        ctx.beginPath(); ctx.moveTo(a[0], a[1]); ctx.lineTo(b[0], b[1]); ctx.stroke();
      }
      // Yhteydet: toimija -> hanke
      if (S.orgs || sel) for (const e of M.E) {
        if (!vis(e.b)) continue;
        const on = focus && (e.a === sel || e.b === sel);
        if (focus && !on) continue;
        const a = proj(e.a.x, e.a.y, e.a.z), b = proj(e.b.x, e.b.y, e.b.z);
        ctx.strokeStyle = ccol(e.a.n.country); ctx.globalAlpha = on ? 0.85 : 0.14; ctx.lineWidth = on ? 1.8 : 0.8;
        ctx.setLineDash(e.weak ? [3, 3] : []);
        ctx.beginPath(); ctx.moveTo(a[0], a[1]); ctx.lineTo(b[0], b[1]); ctx.stroke();
      }
      ctx.setLineDash([]);
      // Samankaltaiset hankkeet ilman yhteyttä
      if (S.par) {
        ctx.strokeStyle = C.hot; ctx.setLineDash([5, 4]); ctx.lineWidth = 1.3;
        for (const m of missing) {
          const a = PN[m.a], b = PN[m.b];
          if (!a || !b || !vis(a) || !vis(b)) continue;
          if (focus && !(focus.has(a.id) && focus.has(b.id)) && sel.id !== a.id && sel.id !== b.id) continue;
          const p = proj(a.x, a.y, a.z), q = proj(b.x, b.y, b.z);
          ctx.globalAlpha = 0.55; ctx.beginPath(); ctx.moveTo(p[0], p[1]); ctx.lineTo(q[0], q[1]); ctx.stroke();
        }
        ctx.setLineDash([]);
      }
      // Solmut syvyysjärjestyksessä (kaukaisin ensin)
      const all = M.P.filter(vis).concat(S.orgs || sel ? M.O : M.O.filter(o => o.kind === "osaamiskeskus"));
      const pr = all.map(n => [n, proj(n.x, n.y, n.z)]).sort((a, b) => b[1][2] - a[1][2]);
      S.screen = pr;
      for (const [n, q] of pr) {
        const s = Math.max(0.6, Math.min(2, Math.sqrt(q[3] / (Math.min(S.W, S.H) * 0.04))));
        const r = n.size * s;
        ctx.globalAlpha = focus ? (focus.has(n.id) ? 1 : 0.12) : (n.kind === "organisaatio" ? 0.75 : 0.95);
        ctx.fillStyle = col(n); ctx.strokeStyle = C.bg; ctx.lineWidth = 1.2;
        ctx.beginPath();
        if (n.kind === "hanke") { ctx.rect(q[0] - r, q[1] - r, 2 * r, 2 * r); ctx.fill(); ctx.stroke(); }
        else if (n.kind === "osaamiskeskus") { ctx.arc(q[0], q[1], r, 0, 7); ctx.strokeStyle = col(n); ctx.lineWidth = 3; ctx.fillStyle = C.bg; ctx.fill(); ctx.stroke(); }
        else { ctx.arc(q[0], q[1], r, 0, 7); ctx.fill(); }
        if (n === S.hover || n === sel) { ctx.globalAlpha = 1; ctx.strokeStyle = C.fg; ctx.lineWidth = 2; ctx.beginPath(); ctx.arc(q[0], q[1], r + 4, 0, 7); ctx.stroke(); }
      }
      ctx.globalAlpha = 1;
    }
    let raf = 0;
    const frame = () => { raf = 0; if (S.spin) { S.yaw += 0.0025; schedule(); } draw(); };
    const schedule = () => { if (!raf) raf = requestAnimationFrame(frame); };

    function pick(x, y) {
      let best = null, bd = 1e9;
      for (const [n, q] of (S.screen || [])) {
        const d = Math.hypot(q[0] - x, q[1] - y);
        if (d < Math.max(10, n.size * 1.6) && d - q[2] * 0.01 < bd) { best = n; bd = d - q[2] * 0.01; }
      }
      return best;
    }
    const label = n => n.kind === "hanke" ? n.p.name : n.n.label;
    function showTip(n, x, y) {
      if (!n) { tip.hidden = true; return; }
      tip.hidden = false;
      tip.innerHTML = n.kind === "hanke"
        ? `<b>${TV.esc(n.p.name)}</b><span>${n.year}${n.p.end ? "–" + TV.esc(n.p.end) : ""} · ${TV.esc(TV.COUNTRY[n.p.country] || n.p.country)} · ${TV.esc(n.p.fund)} · ${TV.eur(+n.p.eur_total || null)}</span>`
        : `<b>${TV.esc(n.n.label)}</b><span>${n.kind === "osaamiskeskus" ? T.hub : T.org} · ${n.members.length} ${T.projects}</span>`;
      const r = host.getBoundingClientRect();
      tip.style.left = Math.min(x + 14, r.width - tip.offsetWidth - 8) + "px";
      tip.style.top = Math.min(y + 14, r.height - tip.offsetHeight - 8) + "px";
    }
    function showInfo(n) {
      if (!n) { info.hidden = true; return; }
      info.hidden = false;
      const others = n.links.map(e => e.a === n ? e.b : e.a);
      const list = others.slice(0, 12).map(o => `<li>${TV.dot(o.kind === "hanke" ? o.p.country : o.n.country)}${TV.esc(label(o))}${o.kind === "hanke" ? ` <span class="note mono">${o.year}</span>` : ""}</li>`).join("");
      info.innerHTML = `<button class="t3-x" type="button" aria-label="×">×</button><span class="eyebrow">${n.kind === "hanke" ? T.proj + " · " + n.year : n.kind === "osaamiskeskus" ? T.hub : T.org}</span><h3>${TV.esc(label(n))}</h3>`
        + (others.length ? `<p class="note">${others.length} ${n.kind === "hanke" ? T.partners : T.projects}</p><ul>${list}${others.length > 12 ? "<li>…</li>" : ""}</ul>` : `<p class="note">${T.none}</p>`)
        + (n.kind === "hanke" ? `<a href="haku.html#${encodeURIComponent(n.id)}">${T.open} →</a>` : "");
      info.querySelector(".t3-x").onclick = () => { S.sel = null; showInfo(null); schedule(); };
    }

    // Ohjaus: veto kääntää, kaksi sormea tai rulla zoomaa, shift-veto tai oikea painike siirtää
    const pts = new Map(); let last = null, moved = 0, pinch = 0;
    cv.onpointerdown = e => { cv.setPointerCapture(e.pointerId); pts.set(e.pointerId, [e.offsetX, e.offsetY]); last = [e.offsetX, e.offsetY]; moved = 0; S.spin = false;
      if (pts.size === 2) { const [a, b] = [...pts.values()]; pinch = Math.hypot(a[0] - b[0], a[1] - b[1]); } };
    cv.onpointermove = e => {
      if (!pts.size) { const n = pick(e.offsetX, e.offsetY); if (n !== S.hover) { S.hover = n; schedule(); } showTip(n, e.offsetX, e.offsetY); cv.style.cursor = n ? "pointer" : "grab"; return; }
      pts.set(e.pointerId, [e.offsetX, e.offsetY]);
      if (pts.size === 2) {
        const [a, b] = [...pts.values()], d = Math.hypot(a[0] - b[0], a[1] - b[1]);
        if (pinch) S.zoom = Math.max(0.5, Math.min(6, S.zoom * d / pinch)); pinch = d; moved = 99; schedule(); return;
      }
      const dx = e.offsetX - last[0], dy = e.offsetY - last[1]; last = [e.offsetX, e.offsetY]; moved += Math.abs(dx) + Math.abs(dy);
      if (e.shiftKey || e.buttons === 2) { S.panX += dx; S.panY += dy; }
      else { S.yaw -= dx * 0.008; S.pitch = Math.max(0.15, Math.min(1.45, S.pitch - dy * 0.006)); }
      tip.hidden = true; schedule();
    };
    cv.onpointerup = cv.onpointercancel = e => {
      pts.delete(e.pointerId); pinch = 0;
      if (moved < 6 && e.type === "pointerup") { const n = pick(e.offsetX, e.offsetY); S.sel = n === S.sel ? null : n; showInfo(S.sel); schedule(); }
    };
    cv.oncontextmenu = e => e.preventDefault();
    cv.onwheel = e => { e.preventDefault(); S.zoom = Math.max(0.5, Math.min(6, S.zoom * Math.exp(-e.deltaY * 0.001))); S.spin = false; schedule(); };
    cv.onpointerleave = () => { S.hover = null; tip.hidden = true; schedule(); };

    ui.mode.onchange = () => { S.mode = ui.mode.value; legend(); schedule(); };
    ui.orgs.onchange = () => { S.orgs = ui.orgs.checked; schedule(); };
    ui.par.onchange = () => { S.par = ui.par.checked; schedule(); };
    ui.year.oninput = () => { S.upTo = +ui.year.value; ui.yearOut.textContent = S.upTo; schedule(); };
    let play = 0;
    ui.play.onclick = () => {
      if (play) { clearInterval(play); play = 0; ui.play.textContent = "▶"; return; }
      S.upTo = M.y0; ui.play.textContent = "❚❚";
      play = setInterval(() => { ui.year.value = S.upTo; ui.yearOut.textContent = S.upTo; schedule();
        if (S.upTo >= M.y1) { clearInterval(play); play = 0; ui.play.textContent = "▶"; } else S.upTo++; }, 700);
    };
    ui.reset.onclick = () => { Object.assign(S, {yaw: -0.35, pitch: 1.0, zoom: 1, panX: 0, panY: 0}); schedule(); };
    const ro = new ResizeObserver(() => { resize(); schedule(); }); ro.observe(cv);
    const mq = matchMedia("(prefers-color-scheme: dark)"); const recolor = () => { colors(); legend(); schedule(); };
    mq.addEventListener("change", recolor);
    colors(); legend(); resize(); schedule();
    return () => { ro.disconnect(); mq.removeEventListener("change", recolor); if (play) clearInterval(play); cancelAnimationFrame(raf); S.spin = false; };
  }
  return {open, build, locate};
})();
