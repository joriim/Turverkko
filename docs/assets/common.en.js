/* Turverkko – yhteiset apufunktiot kaikille sivuille. */
const TV = (() => {
  const REPO = "https://github.com/joriim/Turverkko";
  // SEAMK-tunnus: site.py täyttää originaalitiedostojen nimet, jos ne on lisätty kansioon site/pages/assets/
  const LOGO = "", LOGO_DARK = "";
  const COUNTRY = {FI:"Finland", SE:"Sweden", EE:"Estonia", LV:"Latvia", IE:"Ireland", "DE-NI":"Lower Saxony", "DE-SH":"Schleswig-Holstein", EU:"Multi-country (Interreg)"};
  const FUND = {JTF:"JTF – Just Transition Fund", EAKR:"ERDF / EFRE / EAKR", EIP:"EIP-AGRI", MSR:"Rural development fund (EAFRD)",
                KF:"Cohesion Fund", Interreg:"Interreg (ERDF)", "ESR+":"ESR+", LIFE:"LIFE", Horizon:"Horizon 2020 / Horizon Europe", Kansallinen:"National", "?":"EU co-funded, fund not stated in source", "—":"—"};
  const KIND = {hanke:"Project", osaamiskeskus:"Competence centre", vertailukohde:"Reference case", organisaatio:"Organisation",
                julkaisu:"Publication", ohjelma:"Programme", teema:"Theme"};
  const EV = ["No output information","Qualitative description","Quantitative targets","Reported results","Open data / peer-reviewed"];

  // Kieli: englanninkieliset sivut ovat kansiossa en/ (scripts/site.py)
  const LANG = document.documentElement.lang === "en" ? "en" : "fi";
  const DATA = LANG === "en" ? "../data/" : "data/";
  // Aineiston sanasto (teemat, tyypit, luokat) näytetään englanniksi; logiikka käyttää suomenkielisiä arvoja.
  // V_PREFIX_EN: [säännöllinen lauseke, korvaus] -parit vakiomuotoisille teksteille (näyttöasteen perusteet, valuuttamuunnos).
  const V_EN = {"Turvetuotantoalueiden ennallistaminen ja jälkikäyttö": "Restoration and after-use of peat extraction sites", "Turvepellot: vettäminen, vedenpinnan säätö, tulosperusteiset maksut": "Peat fields: rewetting, water-table control, results-based payments", "Kosteikkoviljely (paludikulttuuri) ja turpeen korvaajat": "Paludiculture and peat substitutes", "Suometsät: metsitys, ojitettujen suometsien hoito ja ennallistaminen": "Peatland forests: afforestation, management and restoration of drained peatland forests", "Luonnontilaisten soiden suojelu ja ennallistaminen": "Protection and restoration of natural mires", "Maaperän ja maankäyttösektorin päästöt ja hiilensidonta: KHK-mittaus, päästökertoimet, inventaario, MRV, hiiliviljely": "Soil and land-use sector emissions and carbon sequestration: GHG measurement, emission factors, inventory, MRV, carbon farming", "Osaamiskeskittymät, klusterit ja tiedonvälitys": "Competence centres, clusters and knowledge transfer", "Maanomistajat, maankäytön suunnittelu ja turpeesta luopumisen sosioekonomia": "Landowners, land-use planning and the socio-economics of the peat phase-out", "saman kokonaisuuden osat": "parts of the same programme", "rinnakkainen ilman yhteyttä": "parallel, unconnected", "peräkkäiset samassa maassa": "sequential in the same country", "puuttuva yhteys": "missing link", "yhteydessä": "connected", "nimet alkavat samalla hanke- tai ohjelmanimellä (osahankkeet tai -toteutukset)": "names start with the same project or programme name (sub-projects or implementations)", "sama maa, samaan aikaan, ei yhteistä toimijaa eikä yhteistyöpolkua. Voi olla tarkoituksellista (eri kohteet) tai päällekkäistä työtä (sama menetelmä tai suunnittelu kahteen kertaan)": "same country, same time, no shared actor and no collaboration path. May be intentional (different sites) or duplicated work (the same method or planning done twice)", "sama maa, eri aikaan, ei yhteistä toimijaa eikä polkua (toisto tai jatko ilman yhteyttä)": "same country, different time, no shared actor or path (repetition or continuation without a link)", "eri maat, ei yhteistyöpolkua": "different countries, no collaboration path", "yhteinen toimija tai yhteistyöpolku enintään kolme askelta": "shared actor or a collaboration path of at most three steps", "lähde": "source", "päätelty": "inferred", "vahvistamatta": "unverified", "laskettu": "calculated", "haku": "search", "osallistuu": "participates", "kuuluu_keskukseen": "member of centre", "yhteistyo": "collaboration", "ei_kytkosta": "no link found", "rahoittaa": "funds", "tuotos": "output", "yhteisjulkaisu": "co-publication", "turvemaa": "peatland", "maaperä": "other soil", "tavoite": "target", "toteuma": "reported", "ohitettu": "skipped", "ennallistaminen": "restoration", "vettäminen": "rewetting", "kosteikko": "wetland", "metsitys": "afforestation", "suunnittelu": "planning", "inventointi": "inventory", "muu": "other", "useita": "several", "viranomainen": "public authority", "yliopisto": "university", "jarjesto": "association", "tutkimuslaitos": "research institute", "yritys": "company", "amk": "university of applied sciences", "ammattijulkaisu": "professional publication", "vertaisarvioitu": "peer-reviewed", "tapahtuma": "event", "kenttäkohde": "field site", "tiedote / mittausasema": "press release / monitoring station", "konferenssiabstrakti": "conference abstract", "raportti": "report", "aineisto": "dataset", "opinnäyte": "thesis", "kyllä": "yes", "ei": "no", "?": "?", "kuvaus toimenpiteistä": "description of activities", "(toteuttaja ei lähteessä)": "(lead not stated in source)"};
  const V_PREFIX_EN = [["^määrällinen tavoite tai tuotos: ", "quantitative target or output: "], ["^raportoitu toteuma: ", "reported result: "], ["^käsin arvioitu taso (\\d)", "manually assessed level $1"], ["^OpenAIRE linkittää hankkeeseen (\\d+) tutkimustuotosta \\(tarkistamatta\\)", "OpenAIRE links $1 research outputs to the project (unverified)"], ["^avoin aineisto tai DOI mainittu: ", "open data or DOI mentioned: "], ["^linkitetty vertaisarvioitu julkaisu ", "linked peer-reviewed publication "], ["^linkitetty avoin aineisto ", "linked open dataset "], ["^linkitetty tuotos ", "linked output "], ["^linkitetty ", "linked "], ["^Muunnettu euroiksi: kokonaisbudjetti ([\\d ]+) SEK, EU-osuus ([\\d ]+) SEK; EKP:n vuoden (\\d{4}) keskikurssi ([\\d.]+) SEK/EUR\\.", "Converted to euros: total budget $1 SEK, EU share $2 SEK; ECB $3 annual average rate $4 SEK/EUR."], ["^Muunnettu euroiksi: kokonaisbudjetti ([\\d ]+) SEK; EKP:n vuoden (\\d{4}) keskikurssi ([\\d.]+) SEK/EUR\\.", "Converted to euros: total budget $1 SEK; ECB $2 annual average rate $3 SEK/EUR."], ["^(.*) \\+ (\\d+) muuta edunsaajaa$", "$1 (+$2 beneficiaries)"], ["^(\\d+) yhteisjulkaisua (.*)$", "$1 co-publications $2"]];
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
  const evbar = n => `<span class="ev" role="img" aria-label="Evidence level ${n}/4: ${EV[n]}">${[1,2,3,4].map(i => `<i class="${i <= n ? "f" : ""}"></i>`).join("")}</span>`;

  function nav(current) {
    const items = [["index.html","Home"],["kartta.html","Map and network"],["haku.html","Search"],["esitys.html","Presentation"],["ehdota.html","Suggest an addition"]];
    const el = document.createElement("nav");
    el.className = "nav"; el.setAttribute("aria-label", "Main menu");
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
    const logo = LOGO ? `<a class="seamk${LOGO_DARK ? " has-dark" : ""}" href="https://www.seamk.fi/" aria-label="Seinäjoki University of Applied Sciences – SEAMK"><picture>${LOGO_DARK ? `<source srcset="${LANG === "en" ? "../" : ""}assets/${LOGO_DARK}" media="(prefers-color-scheme: dark)">` : ""}<img src="${LANG === "en" ? "../" : ""}assets/${LOGO}" alt="Seinäjoki University of Applied Sciences – SEAMK"></picture></a>` : "";
    el.innerHTML = `<div class="foot-in publisher">${logo}<span>Publisher: Seinäjoki University of Applied Sciences (SEAMK)</span></div><div class="foot-in"><span>© 2026 Miiro Jääskeläinen</span><span>Code MIT · data CC BY 4.0</span>
      <a href="${REPO}">Source code and data</a><a href="${REPO}/blob/main/CONTRIBUTING.md">Contributing</a>
      <a href="${REPO}/blob/main/SCHEMA.md">Data model</a></div>`;
    document.body.append(el);
  }
  function fail(el, err) {
    el.innerHTML = `<div class="panel"><h3>Could not load the data</h3><p class="note">${esc(err.message)}. The page only works from a web server (GitHub Pages). Locally: <code>python -m http.server -d docs</code>.</p></div>`;
  }
  return {LANG, v, REPO, COUNTRY, FUND, KIND, EV, load, esc, eur, ccol, dot, evbar, nav, footer, fail};
})();
