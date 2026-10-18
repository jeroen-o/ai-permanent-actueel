# ---------- ronde 3: vragenbank, scroll-offset, header, privacy, geen Google Fonts ----------
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import vragen as VX

def vjs(v):
    return '  V(' + json.dumps(list(v), ensure_ascii=False)[1:-1] + ')'

# 1. vragenbank: 10 per module, toets kiest er willekeurig 2 per module
a = t.index('const VRAGEN = ['); b = t.index('\n];', a)
t = t[:a] + 'const VRAGEN = [\n' + ',\n'.join(vjs(v) for v in VX.NL) + t[b:]
t = sub1("const reeks = VRAGEN.filter(v=>mods.includes(v.m)).sort((a,b)=>a.m-b.m).map(v=>({...v,o:shuffle(v.o)}));",
         "const reeks = [...mods].sort((a,b)=>a-b).flatMap(m=>shuffle(VRAGEN.filter(v=>v.m===m)).slice(0,2)).map(v=>({...v,o:shuffle(v.o)}));", t)
t = sub1("const aantal=VRAGEN.filter(v=>s.mods.includes(v.m)).length;",
         "const aantal=s.mods.reduce((n,m)=>n+Math.min(2,VRAGEN.filter(v=>v.m===m).length),0);", t)
t = sub1('line-height:1.55">Twee vragen per gekozen module, met uitleg bij elk antwoord. Vanaf 70% goed krijg je een deelnamebewijs voor je dossier.</p>',
         'line-height:1.55">Twee vragen per gekozen module, elke keer willekeurig gekozen uit een vragenbank van twintig per module, met uitleg bij elk antwoord. Vanaf 70% goed krijg je een deelnamebewijs voor je dossier.</p>', t)

# 2. scroll-offset op basis van de werkelijke headerhoogte
t = sub1("html{scroll-behavior:smooth}", "html{scroll-behavior:smooth}\n[id]{scroll-margin-top:calc(var(--kop,0px) + 16px)}", t)
t = sub1("    window.scrollTo({top:el.getBoundingClientRect().top+window.scrollY-90,behavior:'smooth'});",
         "    window.scrollTo({top:el.getBoundingClientRect().top+window.scrollY-this.kopHoogte()-16,behavior:'smooth'});", t)
t = t.replace("window.scrollTo({top:el.getBoundingClientRect().top+window.scrollY-80,behavior:'smooth'})",
              "window.scrollTo({top:el.getBoundingClientRect().top+window.scrollY-this.kopHoogte()-16,behavior:'smooth'})")
t = t.replace("window.scrollTo({top:el.getBoundingClientRect().top+window.scrollY-70,behavior:'smooth'})",
              "window.scrollTo({top:el.getBoundingClientRect().top+window.scrollY-this.kopHoogte()-16,behavior:'smooth'})")
assert 'scrollY-70' not in t and 'scrollY-80' not in t and 'scrollY-90' not in t
t = sub1("  componentDidMount(){\n",
         """  kopHoogte(){ const h=document.querySelector('header'); return h&&getComputedStyle(h).position==='sticky'?h.offsetHeight:0; }
  zetKop(){ document.documentElement.style.setProperty('--kop',this.kopHoogte()+'px'); }
  componentDidMount(){
    this.zetKop(); window.addEventListener('resize',()=>this.zetKop());
    if(window.ResizeObserver){ const h=document.querySelector('header'); if(h) new ResizeObserver(()=>this.zetKop()).observe(h); }
""", t)

# 3. DFO BV uit de header
t = sub1('      <a href="https://www.dfobv.nl" style="color:var(--color-text);text-decoration:none">DFO BV</a>\n    </nav>', '    </nav>', t)

# 4. geen verbindingen met Google Fonts
t = sub1('<link rel="preconnect" href="https://fonts.googleapis.com">\n', '', t)
t, n = re.subn(r'<link rel="stylesheet" href="https://fonts\.googleapis\.com/css2\?family=Archivo[^"]*">', '', t); assert n == 1
t = sub1('body{font-family:Archivo,sans-serif;', 'body{font-family:Archivo,Arial,Helvetica,sans-serif;', t)
assert 'googleapis' not in t

# 5. zoeken achter een vergrootglas in de header; zoekveld in het gratis-blok weg
zs = t.index('\n    <div role="search"')
ze = t.index('\n    </div>\n', t.index('id="zoek-resultaten"', zs)) + len('\n    </div>')
ZOEK_NIEUW = '''
    <div class="zoek-wrap" role="search" style="position:relative;flex:none">
      <button type="button" id="zoek-knop" class="btn" aria-label="Zoeken op de site" title="Zoeken" aria-expanded="{{ zoekVeldAttr }}" aria-controls="zoek-paneel" sc-camel-on-click="{{ zoekToggle }}" style="width:44px;height:44px;justify-content:center;padding:0;border:2px solid var(--color-text);background:{{ zoekKnopBg }};color:{{ zoekKnopFg }}"><svg width="20" height="20" sc-camel-view-box="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" aria-hidden="true"><circle cx="10.5" cy="10.5" r="6.5"></circle><path d="M15.5 15.5 21 21"></path></svg></button>
      <sc-if value="{{ zoekVeldOpen }}" hint-placeholder-val="{{ false }}">
        <div id="zoek-paneel" style="position:absolute;top:calc(100% + 8px);right:0;width:min(440px,calc(100vw - 32px));background:var(--color-bg);border:2px solid var(--color-text);z-index:40;padding:12px;display:flex;flex-direction:column;gap:8px;box-shadow:0 8px 24px color-mix(in srgb,var(--color-text) 18%,transparent)">
          <label for="zoek" style="font-size:12px;font-weight:700;letter-spacing:0.08em;text-transform:uppercase;color:var(--color-accent-700)">Zoek op deze site</label>
          <input id="zoek" type="search" class="input" value="{{ zoek }}" sc-camel-on-change="{{ setZoek }}" sc-camel-on-key-down="{{ zoekKey }}" sc-camel-on-focus="{{ zoekFocus }}" placeholder="Bijv. privacyverklaring, artikel 50, shadow AI" autocomplete="off" role="combobox" aria-autocomplete="list" aria-controls="zoek-resultaten" aria-expanded="{{ zoekToonAttr }}" style="width:100%">
          <sc-if value="{{ zoekToon }}" hint-placeholder-val="{{ false }}">
            <div id="zoek-resultaten" role="listbox" aria-label="Zoekresultaten" style="max-height:60vh;overflow-y:auto;border-top:2px solid var(--color-divider)">
              <sc-for list="{{ zoekResultaten }}" as="z" hint-placeholder-count="0">
                <button type="button" role="option" aria-selected="{{ z.actiefAttr }}" sc-camel-on-click="{{ z.ga }}" style="display:flex;flex-direction:column;gap:2px;width:100%;text-align:left;padding:10px 8px;border:0;border-bottom:1px solid var(--color-divider);background:{{ z.bg }};font:inherit;color:var(--color-text);cursor:pointer">
                  <span style="font-size:10px;letter-spacing:0.1em;text-transform:uppercase;font-weight:700;color:var(--color-accent-700)">{{ z.sectie }}</span>
                  <span style="font-size:14px;font-weight:700;line-height:1.3">{{ z.titel }}</span>
                  <span style="font-size:12px;line-height:1.45;opacity:0.85">{{ z.voor }}<mark style="background:var(--color-accent-200);color:inherit;padding:0 1px">{{ z.treffer }}</mark>{{ z.na }}</span>
                </button>
              </sc-for>
              <sc-if value="{{ zoekGeen }}" hint-placeholder-val="{{ false }}">
                <div style="padding:12px 8px;font-size:13px">Geen resultaten. Probeer een ander of korter woord.</div>
              </sc-if>
            </div>
          </sc-if>
        </div>
      </sc-if>
    </div>'''
t = t[:zs] + ZOEK_NIEUW + t[ze:]
t, n = re.subn(r'\n      <form role="search".*?</form>', '', t, flags=re.S); assert n == 1
t = sub1("@media (max-width:720px){ header{position:static!important} .span2{grid-column:auto!important} }",
         "header > div{position:relative;padding-right:calc(var(--space-6) + 56px)!important}\n.zoek-wrap{position:absolute!important;top:50%;right:var(--space-6);transform:translateY(-50%)}\n@media (max-width:720px){ header{position:static!important} .span2{grid-column:auto!important} .zoek-wrap{top:14px;right:16px;transform:none} }", t)
t = sub1("zoekActief:0, heroZoekTekst:''", "zoekActief:0, zoekVeldOpen:false, heroZoekTekst:''", t)
t = sub1("if(q) this.setState({zoek:q,zoekOpen:true},", "if(q) this.setState({zoek:q,zoekOpen:true,zoekVeldOpen:true},", t)
t = sub1("    this.zetKop(); window.addEventListener('resize',()=>this.zetKop());",
         "    this.zetKop(); window.addEventListener('resize',()=>this.zetKop());\n"
         "    document.addEventListener('click',e=>{ if(this.state.zoekVeldOpen&&!e.target.closest('.zoek-wrap')) this.setState({zoekVeldOpen:false,zoekOpen:false}); });", t)
t = sub1("zoekGa(r){ this.setState({zoekOpen:false});", "zoekGa(r){ this.setState({zoekOpen:false,zoekVeldOpen:false});", t)
t = sub1("else if(e.key==='Escape'){ this.setState({zoek:'',zoekOpen:false}); }",
         "else if(e.key==='Escape'){ this.setState({zoek:'',zoekOpen:false,zoekVeldOpen:false},()=>{ const k=document.getElementById('zoek-knop'); if(k) k.focus(); }); }", t)
t = sub1("          zoek:s.zoek, zoekToon:toon,",
         "          zoekVeldOpen:s.zoekVeldOpen, zoekVeldAttr:s.zoekVeldOpen?'true':'false',\n"
         "          zoekKnopBg:s.zoekVeldOpen?'var(--color-text)':'var(--color-bg)', zoekKnopFg:s.zoekVeldOpen?'var(--color-bg)':'var(--color-text)',\n"
         "          zoekToggle:()=>{ if(s.zoekVeldOpen) this.setState({zoekVeldOpen:false,zoekOpen:false}); else this.setState({zoekVeldOpen:true,zoekOpen:true},()=>setTimeout(()=>{ const el=document.getElementById('zoek'); if(el) el.focus(); },0)); },\n"
         "          zoek:s.zoek, zoekToon:toon,", t)
