/* Turverkko – yhteiset apufunktiot kaikille sivuille. */
const TV = (() => {
  const REPO = "__REPO_URL__";
  // SEAMK-tunnus: site.py täyttää originaalitiedostojen nimet, jos ne on lisätty kansioon site/pages/assets/
  const LOGO = "__SEAMK_LOGO__", LOGO_DARK = "__SEAMK_LOGO_DARK__";
  const COUNTRY = {FI:"Suomi", SE:"Ruotsi", EE:"Viro", LV:"Latvia", IE:"Irlanti", "DE-NI":"Niedersachsen", "DE-SH":"Schleswig-Holstein", EU:"Ylikansallinen (Interreg)"};
  const FUND = {JTF:"JTF – oikeudenmukainen siirtymä", EAKR:"EAKR / EFRE / ERDF", EIP:"EIP-AGRI", MSR:"Maaseuturahasto (EAFRD)",
                KF:"Koheesiorahasto", Interreg:"Interreg (EAKR)", "ESR+":"ESR+", LIFE:"LIFE", Horizon:"Horizon 2020 / Horizon Europe", Kansallinen:"Kansallinen", "?":"EU-osarahoitteinen, rahasto ei lähteessä", "—":"—"};
  const KIND = {hanke:"Hanke", osaamiskeskus:"Osaamiskeskus", vertailukohde:"Vertailukohde", organisaatio:"Organisaatio",
                julkaisu:"Julkaisu", ohjelma:"Ohjelma", teema:"Teema"};
  const EV = ["Ei tuotostietoa","Laadullinen kuvaus","Määrälliset tavoitteet","Raportoituja tuloksia","Avoin data / vertaisarvioitu"];

  // Kieli: englanninkieliset sivut ovat kansiossa en/ (scripts/site.py)
  const LANG = document.documentElement.lang === "en" ? "en" : "fi";
  const DATA = LANG === "en" ? "../data/" : "data/";
  // Aineiston sanasto (teemat, tyypit, luokat) näytetään englanniksi; logiikka käyttää suomenkielisiä arvoja.
  // V_PREFIX_EN: [säännöllinen lauseke, korvaus] -parit vakiomuotoisille teksteille (näyttöasteen perusteet, valuuttamuunnos).
  const V_EN = __V_EN__;
  const V_PREFIX_EN = __V_PREFIX_EN__;
  const v = s => {
    if (LANG !== "en" || s == null) return s;
    const k = String(s);
    if (k in V_EN) return V_EN[k];
    for (const [re, en] of V_PREFIX_EN) { const r = new RegExp(re); if (r.test(k)) return k.replace(r, en); }
    return k;
  };

  let cache = null;
  async function load() {
    if (cache) return cache;
    const get = f => fetch(DATA + f).then(r => { if (!r.ok) throw new Error(f + " " + r.status); return r.json(); });
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
    const items = [["index.html","Etusivu"],["kartta.html","Kartta ja verkosto"],["haku.html","Haku"],["esitys.html","Esitys"],["ehdota.html","Ehdota lisäystä"]];
    const el = document.createElement("nav");
    el.className = "nav"; el.setAttribute("aria-label", "Päävalikko");
    el.innerHTML = `<div class="nav-in">
      <a class="brand" href="index.html"><svg width="22" height="22" viewBox="0 0 22 22" aria-hidden="true"><path d="M5 15 16 6 17 17Z" fill="none" stroke="var(--muted)" stroke-width="1.2"/><circle cx="5" cy="15" r="3" fill="var(--accent)"/><circle cx="16" cy="6" r="3.2" fill="#FFF023" stroke="#542583" stroke-width="1.2"/><circle cx="17" cy="17" r="2.4" fill="#AA92C1"/></svg>Turverkko</a>
      <ul>${items.map(([h,t]) => `<li><a href="${h}"${h === current ? ' aria-current="page"' : ""}>${t}</a></li>`).join("")}</ul>
      <a class="lang" id="lang-switch" hreflang="${LANG === "en" ? "fi" : "en"}" lang="${LANG === "en" ? "fi" : "en"}" href="${LANG === "en" ? "../" : "en/"}${current}">${LANG === "en" ? "Suomeksi" : "English"}</a>
      <a class="gh" href="${REPO}">GitHub ↗</a></div>`;
    document.body.prepend(el);
    const sw = el.querySelector("#lang-switch");
    sw.addEventListener("click", () => { sw.href = sw.href.split("#")[0] + location.hash; });
  }
  function footer() {
    const el = document.createElement("footer");
    el.className = "footer";
    const logo = LOGO ? `<a class="seamk${LOGO_DARK ? " has-dark" : ""}" href="https://www.seamk.fi/" aria-label="Seinäjoen ammattikorkeakoulu – SEAMK"><picture>${LOGO_DARK ? `<source srcset="${LANG === "en" ? "../" : ""}assets/${LOGO_DARK}" media="(prefers-color-scheme: dark)">` : ""}<img src="${LANG === "en" ? "../" : ""}assets/${LOGO}" alt="Seinäjoen ammattikorkeakoulu – SEAMK"></picture></a>` : "";
    el.innerHTML = `<div class="foot-in publisher">${logo}<span>Julkaisija: Seinäjoen ammattikorkeakoulu (SEAMK)</span></div><div class="foot-in"><span>© 2026 Miiro Jääskeläinen</span><span>Koodi MIT · aineisto CC BY 4.0</span>
      <a href="${REPO}">Lähdekoodi ja aineisto</a><a href="${REPO}/blob/main/CONTRIBUTING.md">Osallistuminen</a>
      <a href="${REPO}/blob/main/SCHEMA.md">Aineistomalli</a></div>`;
    document.body.append(el);
  }
  function fail(el, err) {
    el.innerHTML = `<div class="panel"><h3>Aineistoa ei saatu ladattua</h3><p class="note">${esc(err.message)}. Sivu toimii vain verkkopalvelimelta (GitHub Pages). Paikallisesti: <code>python -m http.server -d docs</code>.</p></div>`;
  }
  return {LANG, v, REPO, COUNTRY, FUND, KIND, EV, load, esc, eur, ccol, dot, evbar, nav, footer, fail};
})();
