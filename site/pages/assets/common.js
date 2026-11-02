/* Turverkko – yhteiset apufunktiot kaikille sivuille. */
const TV = (() => {
  const REPO = "__REPO_URL__";
  const COUNTRY = {FI:"Suomi", SE:"Ruotsi", EE:"Viro", LV:"Latvia", IE:"Irlanti", "DE-NI":"Niedersachsen", "DE-SH":"Schleswig-Holstein"};
  const FUND = {JTF:"JTF – oikeudenmukainen siirtymä", EAKR:"EAKR / EFRE / ERDF", EIP:"EIP-AGRI", MSR:"Maaseuturahasto (EAFRD)",
                KF:"Koheesiorahasto", LIFE:"LIFE", Kansallinen:"Kansallinen", "?":"EU-osarahoitteinen, rahasto ei lähteessä", "—":"—"};
  const KIND = {hanke:"Hanke", osaamiskeskus:"Osaamiskeskus", vertailukohde:"Vertailukohde", organisaatio:"Organisaatio",
                julkaisu:"Julkaisu", ohjelma:"Ohjelma", teema:"Teema"};
  const EV = ["Ei tuotostietoa","Laadullinen kuvaus","Määrälliset tavoitteet","Raportoituja tuloksia","Avoin data / vertaisarvioitu"];

  let cache = null;
  async function load() {
    if (cache) return cache;
    const get = f => fetch("data/" + f).then(r => { if (!r.ok) throw new Error(f + " " + r.status); return r.json(); });
    const [ds, net, an] = await Promise.all([get("dataset.json"), get("network.json"), get("analysis.json")]);
    cache = {ds, net, an, byId: Object.fromEntries(net.nodes.map(n => [n.id, n]))};
    return cache;
  }
  const esc = s => String(s ?? "").replace(/[&<>"']/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
  const eur = v => v == null || v === "" ? "—" : v >= 1e6 ? (v/1e6).toLocaleString("fi-FI",{maximumFractionDigits:2}) + " M€" : Math.round(v).toLocaleString("fi-FI") + " €";
  const ccol = c => `var(--c-${COUNTRY[c] && c !== "DE-SH" ? c : "X"})`;
  const dot = c => `<span class="dot" style="background:${ccol(c)}" aria-hidden="true"></span>`;
  const evbar = n => `<span class="ev" role="img" aria-label="Näyttöaste ${n}/4: ${EV[n]}">${[1,2,3,4].map(i => `<i class="${i <= n ? "f" : ""}"></i>`).join("")}</span>`;

  function nav(current) {
    const items = [["index.html","Etusivu"],["kartta.html","Kartta ja verkosto"],["haku.html","Haku"],["ehdota.html","Ehdota lisäystä"]];
    const el = document.createElement("nav");
    el.className = "nav"; el.setAttribute("aria-label", "Päävalikko");
    el.innerHTML = `<div class="nav-in">
      <a class="brand" href="index.html"><svg width="22" height="22" viewBox="0 0 22 22" aria-hidden="true"><circle cx="5" cy="15" r="3" fill="var(--peat)"/><circle cx="16" cy="6" r="3" fill="var(--accent)"/><circle cx="17" cy="17" r="2.4" fill="var(--water)"/><path d="M5 15 16 6 17 17Z" fill="none" stroke="var(--muted)" stroke-width="1.2"/></svg>Turverkko</a>
      <ul>${items.map(([h,t]) => `<li><a href="${h}"${h === current ? ' aria-current="page"' : ""}>${t}</a></li>`).join("")}</ul>
      <a class="gh" href="${REPO}">GitHub ↗</a></div>`;
    document.body.prepend(el);
  }
  function footer() {
    const el = document.createElement("footer");
    el.className = "footer";
    el.innerHTML = `<div class="foot-in"><span>© 2026 Miiro Jääskeläinen</span><span>Koodi MIT · aineisto CC BY 4.0</span>
      <a href="${REPO}">Lähdekoodi ja aineisto</a><a href="${REPO}/blob/main/CONTRIBUTING.md">Osallistuminen</a>
      <a href="${REPO}/blob/main/SCHEMA.md">Aineistomalli</a></div>`;
    document.body.append(el);
  }
  function fail(el, err) {
    el.innerHTML = `<div class="panel"><h3>Aineistoa ei saatu ladattua</h3><p class="note">${esc(err.message)}. Sivu toimii vain verkkopalvelimelta (GitHub Pages). Paikallisesti: <code>python -m http.server -d docs</code>.</p></div>`;
  }
  return {REPO, COUNTRY, FUND, KIND, EV, load, esc, eur, ccol, dot, evbar, nav, footer, fail};
})();
