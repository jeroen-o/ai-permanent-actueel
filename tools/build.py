import json, re, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kc_data import *

import os as _os
TOOLS=_os.path.dirname(_os.path.abspath(__file__))
REPO=_os.environ.get('AIPA_REPO',_os.path.dirname(TOOLS))
WERK=_os.environ.get('AIPA_WERK',_os.path.join(TOOLS,'.werk'))
_os.makedirs(WERK,exist_ok=True)
SITE = 'https://ai-permanent-actueel.nl/'
TITLE = 'AI Permanent Actueel | AI-geletterdheid voor financieel dienstverleners'
DESC = ('AI-geletterdheid (art. 4 AI-verordening) voor hypotheek-, assurantie- en kredietadviseurs en volmachtbedrijven: '
        'maandupdates, kwartaaltoets met certificaat en wat je de klant vertelt als je AI gebruikt.')

src = open(f'{TOOLS}/basis/index.html', encoding='utf-8').read()
L = src.split('\n')
assert L[380].strip() == '<script type="__bundler/template">'
t = json.loads(L[381])
assert 'id="klantcommunicatie"' not in t, 'al toegepast'

def sub1(old, new, s):
    assert s.count(old) == 1, (s.count(old), old[:80])
    return s.replace(old, new)

# ---------- head / SEO ----------
FAVICON = ("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Crect width='100' height='100' fill='%231462ad'/%3E"
           "%3Ctext x='50' y='66' text-anchor='middle' font-family='Arial,sans-serif' font-weight='900' font-size='46' fill='%23fff'%3EAI%3C/text%3E%3C/svg%3E")

faq_static = None  # gevuld via node (FAQ uit het dc-script)

def jsonld(faq):
    g = [
        {"@type": "Organization", "@id": SITE + "#dfo", "name": "DFO BV", "url": "https://www.dfobv.nl",
         "email": "info@dfobv.nl", "telephone": "+31332580460",
         "address": {"@type": "PostalAddress", "streetAddress": "De Wel 14-16", "postalCode": "3871 MV",
                     "addressLocality": "Hoevelaken", "addressCountry": "NL"}},
        {"@type": "WebSite", "@id": SITE + "#website", "url": SITE, "name": "AI Permanent Actueel",
         "inLanguage": "nl-NL", "publisher": {"@id": SITE + "#dfo"},
         "potentialAction": {"@type": "SearchAction", "target": {"@type": "EntryPoint", "urlTemplate": SITE + "?q={search_term_string}"},
                             "query-input": "required name=search_term_string"}},
        {"@type": "WebPage", "@id": SITE + "#webpage", "url": SITE, "name": TITLE, "description": DESC,
         "inLanguage": "nl-NL", "isPartOf": {"@id": SITE + "#website"}, "publisher": {"@id": SITE + "#dfo"},
         "dateModified": "2026-10-18",
         "about": [{"@type": "Thing", "name": n} for n in ["AI-geletterdheid", "AI-verordening artikel 4", "AI-verordening artikel 50", "AVG", "Wft-zorgplicht", "Klantcommunicatie bij AI"]],
         "audience": {"@type": "BusinessAudience", "audienceType": "Hypotheekadviseurs, assurantieadviseurs, kredietadviseurs en volmachtbedrijven"}},
        {"@type": "FAQPage", "@id": SITE + "#faq", "inLanguage": "nl-NL",
         "mainEntity": [{"@type": "Question", "name": f["v"], "acceptedAnswer": {"@type": "Answer", "text": f["a"]}} for f in faq]},
    ]
    return json.dumps({"@context": "https://schema.org", "@graph": g}, ensure_ascii=False)

def seo_head(faq):
    return head_html(TITLE, DESC, SITE, jsonld(faq))

def head_html(TITLE, DESC, URL, LD):
    return f'''<meta name="description" content="{DESC}">
<meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large">
<link rel="canonical" href="{URL}">
<link rel="icon" href="/favicon.ico" sizes="32x32">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<meta name="theme-color" content="#1462ad">
<meta property="og:type" content="website">
<meta property="og:locale" content="nl_NL">
<meta property="og:site_name" content="AI Permanent Actueel">
<meta property="og:title" content="{TITLE}">
<meta property="og:description" content="{DESC}">
<meta property="og:url" content="{URL}">
<meta property="og:image" content="{SITE}og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{TITLE}">
<meta name="twitter:description" content="{DESC}">
<meta name="twitter:image" content="{SITE}og-image.png">
<link rel="alternate" type="text/plain" title="LLM-samenvatting" href="{SITE}llms.txt">
<script type="application/ld+json">{LD}</script>
'''

# FAQ-data uit het dc-script halen (via node)
import subprocess
dcjs = t[t.index('<script type="text/x-dc" data-dc-script="">') + len('<script type="text/x-dc" data-dc-script="">'):t.index('class Component extends DCLogic')]
out = subprocess.run(['node', '-e', 'const vm=require("vm");const c=require("fs").readFileSync(0,"utf8");'
                      'process.stdout.write(vm.runInNewContext(c+";JSON.stringify({MODULES,FAQ,CHECKLIST})"))'],
                     input=dcjs, capture_output=True, text=True, check=True).stdout
DC = json.loads(out)
FAQ_ALL = DC['FAQ'] + KC_FAQ

t = sub1('<html><head>', '<html lang="nl"><head>', t)
t = sub1('<meta name="viewport" content="width=device-width, initial-scale=1">\n<script src=',
         '<meta name="viewport" content="width=device-width, initial-scale=1">\n' + seo_head(FAQ_ALL) + '<script src=', t)
t = sub1('<title>AI Permanent Actueel — ai-permanent-actueel.nl</title>', f'<title>{TITLE}</title>', t)

# ---------- nummering secties 02..10 -> 03..11 ----------
for n in range(10, 1, -1):
    t = sub1(f'>{n:02d} — ', f'>{n+1:02d} — ', t)

# ---------- navigatie + zoeker ----------
LBL = 'font-size:11px;letter-spacing:0.1em;text-transform:uppercase;font-weight:700;color:var(--color-accent-700)'
t = sub1('<a href="#artikel4" style="color:var(--color-text);text-decoration:none">Artikel 4</a>',
         '<a href="#artikel4" style="color:var(--color-text);text-decoration:none">Artikel 4</a>\n'
         '      <a href="#klantcommunicatie" style="color:var(--color-text);text-decoration:none">Klantcommunicatie</a>', t)

ZOEKER = f'''
    <div role="search" style="position:relative;flex:1 1 220px;max-width:340px;min-width:0">
      <label for="zoek" style="position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap">Zoek op deze site</label>
      <input id="zoek" type="search" class="input" value="{{{{ zoek }}}}" sc-camel-on-change="{{{{ setZoek }}}}" sc-camel-on-key-down="{{{{ zoekKey }}}}" sc-camel-on-focus="{{{{ zoekFocus }}}}" sc-camel-on-blur="{{{{ zoekBlur }}}}" placeholder="Zoek, bijv. privacyverklaring" autocomplete="off" role="combobox" aria-autocomplete="list" aria-controls="zoek-resultaten" aria-expanded="{{{{ zoekToonAttr }}}}" style="width:100%">
      <sc-if value="{{{{ zoekToon }}}}" hint-placeholder-val="{{{{ false }}}}">
        <div id="zoek-resultaten" role="listbox" aria-label="Zoekresultaten" style="position:absolute;top:calc(100% + 4px);left:0;right:0;background:var(--color-bg);border:2px solid var(--color-text);z-index:40;max-height:70vh;overflow-y:auto;box-shadow:0 8px 24px color-mix(in srgb,var(--color-text) 18%,transparent)">
          <sc-for list="{{{{ zoekResultaten }}}}" as="z" hint-placeholder-count="0">
            <button type="button" role="option" aria-selected="{{{{ z.actiefAttr }}}}" sc-camel-on-click="{{{{ z.ga }}}}" style="display:flex;flex-direction:column;gap:2px;width:100%;text-align:left;padding:10px 12px;border:0;border-bottom:1px solid var(--color-divider);background:{{{{ z.bg }}}};font:inherit;color:var(--color-text);cursor:pointer">
              <span style="font-size:10px;letter-spacing:0.1em;text-transform:uppercase;font-weight:700;color:var(--color-accent-700)">{{{{ z.sectie }}}}</span>
              <span style="font-size:14px;font-weight:700;line-height:1.3">{{{{ z.titel }}}}</span>
              <span style="font-size:12px;line-height:1.45;opacity:0.85">{{{{ z.voor }}}}<mark style="background:var(--color-accent-200);color:inherit;padding:0 1px">{{{{ z.treffer }}}}</mark>{{{{ z.na }}}}</span>
            </button>
          </sc-for>
          <sc-if value="{{{{ zoekGeen }}}}" hint-placeholder-val="{{{{ false }}}}">
            <div style="padding:12px;font-size:13px">Geen resultaten. Probeer een ander of korter woord.</div>
          </sc-if>
        </div>
      </sc-if>
    </div>
'''
t = sub1('      <a href="https://www.dfobv.nl" style="color:var(--color-text);text-decoration:none">DFO BV</a>\n    </nav>\n',
         '      <a href="https://www.dfobv.nl" style="color:var(--color-text);text-decoration:none">DFO BV</a>\n    </nav>\n' + ZOEKER, t)


# ---------- home-knop ----------
t = sub1('<nav style="display:flex;flex-wrap:wrap;gap:var(--space-4);font-size:13px;font-weight:600">\n',
         '<nav aria-label="Hoofdnavigatie" style="display:flex;flex-wrap:wrap;gap:var(--space-4);font-size:13px;font-weight:600">\n'
         '      <a href="#top" style="color:var(--color-text);text-decoration:none">Home</a>\n', t)
t = sub1('</footer>\n', '''</footer>
<a href="#top" aria-label="Terug naar home" title="Terug naar home" style="position:fixed;right:16px;bottom:16px;z-index:30;display:flex;align-items:center;gap:6px;padding:10px 14px;background:var(--color-accent);color:var(--color-bg);text-decoration:none;font-weight:700;font-size:13px;border:2px solid var(--color-bg);box-shadow:0 4px 14px color-mix(in srgb,var(--color-text) 25%,transparent)"><svg width="16" height="16" sc-camel-view-box="0 0 24 24" aria-hidden="true"><path d="M3 11.5 12 4l9 7.5V20a1 1 0 0 1-1 1h-5v-6H9v6H4a1 1 0 0 1-1-1z" fill="currentColor"></path></svg>Home</a>
''', t)

# ---------- footer-link ----------
t = sub1('<a href="#dossier" style="color:var(--color-bg);text-decoration:none">Dossier voor de werkgever</a>',
         '<a href="#dossier" style="color:var(--color-bg);text-decoration:none">Dossier voor de werkgever</a>\n'
         '      <a href="#klantcommunicatie" style="color:var(--color-bg);text-decoration:none">Klantcommunicatie bij AI</a>', t)

# ---------- sectie klantcommunicatie ----------
def rij(lijst, model=False, letop=False):
    rand = 'var(--color-accent)' if letop else 'var(--color-text)'
    kop = f'''<div style="flex:1 1 220px;display:flex;flex-direction:column;gap:var(--space-2);min-width:0">
                <h4 style="margin:0;font-size:16px;line-height:1.3">{{{{ k.titel }}}}</h4>
                <sc-if value="{{{{ k.heeftTag }}}}" hint-placeholder-val="{{{{ false }}}}"><span class="tag tag-accent" style="align-self:flex-start">{{{{ k.tag }}}}</span></sc-if>
              </div>'''
    if model:
        body = f'''<div style="flex:2 1 320px;display:flex;flex-direction:column;gap:var(--space-2);min-width:0">
                <p style="margin:0;font-size:14px;line-height:1.6;padding:var(--space-3);background:var(--color-bg);border-left:4px solid var(--color-accent)">{{{{ k.tekst }}}}</p>
                <button type="button" class="btn btn-secondary" sc-camel-on-click="{{{{ k.kopieer }}}}" style="justify-content:flex-start;align-self:flex-start">{{{{ k.kopieerLabel }}}}</button>
              </div>'''
    else:
        body = f'''<div style="flex:2 1 320px;display:flex;flex-direction:column;gap:var(--space-1);min-width:0">
                <p style="margin:0;font-size:14px;line-height:1.6">{{{{ k.tekst }}}}</p>
                <sc-if value="{{{{ k.heeftBron }}}}" hint-placeholder-val="{{{{ true }}}}"><span style="font-size:12px;font-weight:700;color:var(--color-accent-700)">{{{{ k.bron }}}}</span></sc-if>
              </div>'''
    return f'''<sc-for list="{{{{ {lijst} }}}}" as="k" hint-placeholder-count="4">
            <div id="{{{{ k.anker }}}}" style="display:flex;flex-wrap:wrap;gap:var(--space-3) var(--space-6);padding:var(--space-4) 0;border-bottom:1px solid var(--color-divider);scroll-margin-top:90px">
              {kop}
              {body}
            </div>
          </sc-for>'''

def blok(key, titel, model=False, letop=False):
    stijl = 'border:2px solid var(--color-accent);padding:var(--space-4) var(--space-6);background:var(--color-bg)' if letop else ''
    icoon = '⚠ ' if letop else ''
    return f'''<div style="display:flex;flex-direction:column;{stijl}">
          <h3 style="margin:0;font-size:20px;padding-bottom:var(--space-2);border-bottom:2px solid {'var(--color-accent)' if letop else 'var(--color-text)'}">{icoon}{titel}</h3>
          {rij('kc.' + key, model, letop)}
        </div>'''

KC = f'''<section id="klantcommunicatie" style="border-bottom:2px solid var(--color-divider);background:var(--color-surface)">
  <div style="max-width:1200px;margin:0 auto;padding:56px var(--space-6);display:flex;flex-direction:column;gap:var(--space-6)">
    <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,340px),1fr));gap:var(--space-8);align-items:end">
      <div style="display:flex;flex-direction:column;gap:var(--space-3)">
        <span style="{LBL}">02 — Voor de werkgever: klantcommunicatie</span>
        <h2 style="margin:0;font-size:clamp(28px,3.4vw,40px);line-height:1.05;letter-spacing:-0.02em">Wat vertel je de klant als je AI gebruikt?</h2>
      </div>
      <p style="margin:0;font-size:16px;line-height:1.6;text-wrap:pretty">Voor hypotheek-, assurantie- en kredietadviseurs en volmachtbedrijven: welke documenten en teksten je aanpast zodra medewerkers AI gebruiken in hun dagelijkse werk, en wat je intern vastlegt.</p>
    </div>
    <div role="tablist" aria-label="Beroepsgroep" style="display:flex;flex-wrap:wrap;gap:var(--space-2)">
      <sc-for list="{{{{ kcTabs }}}}" as="b" hint-placeholder-count="5">
        <button type="button" role="tab" id="{{{{ b.tabId }}}}" aria-selected="{{{{ b.selected }}}}" aria-controls="kc-paneel" tabindex="{{{{ b.tabindex }}}}" sc-camel-on-click="{{{{ b.kies }}}}" sc-camel-on-key-down="{{{{ b.toets }}}}" class="btn" style="justify-content:flex-start;border:2px solid var(--color-text);background:{{{{ b.bg }}}};color:{{{{ b.fg }}}};font-weight:600">{{{{ b.naam }}}}</button>
      </sc-for>
    </div>
    <div id="kc-paneel" role="tabpanel" aria-labelledby="{{{{ kc.tabId }}}}" style="display:flex;flex-direction:column;gap:var(--space-8)">
      <p style="margin:0;font-size:15px;line-height:1.6;max-width:80ch;font-weight:600">{{{{ kc.intro }}}}</p>
      {blok('verplicht', '1 · Verplicht naar de klant')}
      {blok('aanbevolen', '2 · Aanbevolen in je klantdocumenten')}
      {blok('intern', '3 · Intern vastleggen (niet naar de klant)')}
      {blok('modellen', '4 · Modelteksten', model=True)}
      {blok('letop', 'Compliance-aandachtspunten', letop=True)}
    </div>
    <p style="margin:0;font-size:12px;opacity:0.7">Stand: oktober 2026. Hulpmiddel voor het gesprek met compliance, geen juridisch advies.</p>
  </div>
</section>

'''
t = sub1('<section id="modules" ', KC + '<section id="modules" ', t)


t = sub1("componentDidUpdate(pp,ps){ if(ps.berichten.length!==this.state.berichten.length||ps.laden!==this.state.laden){",
         "componentDidUpdate(){ const n=this.state.berichten.length*2+(this.state.laden?1:0); if(n!==this._chatN){ this._chatN=n;", t)


t = sub1("*{box-sizing:border-box}\n", "*{box-sizing:border-box}\n@media (max-width:720px){ header{position:static!important} .span2{grid-column:auto!important} }\n", t)


# ---------- AI-assistent verwijderen ----------
n0 = len(t)
t, n = re.subn(r'\n\n      <div id="assistent".*?\n      </div>\n(?=\n    </div>\n  </div>\n</section>\n\n<section id="scan")', '', t, flags=re.S); assert n == 1
t, n = re.subn(r'\n            <button type="button" class="btn btn-secondary" sc-camel-on-click="\{\{ legUit \}\}"[^\n]*', '', t); assert n == 1
t = sub1('controleer een prompt op klantgegevens voordat je hem ergens invoert, en stel je vragen over AI in de praktijk.',
         'controleer een prompt op klantgegevens voordat je hem ergens invoert.', t)
assert 'AI-assistent</h3>' not in t and 'legUit }}' not in t

# ---------- JS: data, state, methodes, renderVals ----------
KCDATA = {"sectoren": SECTOREN, "intro": INTRO,
          "blokken": {k: lijst for k, _, lijst in BLOKKEN}, "titels": {k: titel for k, titel, _ in BLOKKEN}}
t = sub1('const V = (m,v,goed,fout,u)', "const PAGINA='__PAGINA__';\nconst HOME=PAGINA==='toets'?'../':'./';\nconst TOETSURL=PAGINA==='toets'?'./':'kennistoets/';\nconst KC = " + json.dumps(KCDATA, ensure_ascii=False) + ';\nconst V = (m,v,goed,fout,u)', t)

t = sub1("laden:false };\n  chatRef", "laden:false, kcSector:'alle', kcGekopieerd:null, zoek:'', zoekOpen:false, zoekActief:0 };\n  chatRef", t)

METHODS = r'''
  componentDidMount(){
    const q=new URLSearchParams(window.location.search).get('q');
    if(q) this.setState({zoek:q,zoekOpen:true},()=>{ const el=document.getElementById('zoek'); if(el){ el.focus(); window.scrollTo(0,0); } });
    else if(window.location.hash.length>1){ const id=decodeURIComponent(window.location.hash.slice(1)); setTimeout(()=>this.scrollNaar(id,id.startsWith('kc-')),300); }
    if(PAGINA==='toets'){
      const p=new URLSearchParams(window.location.search);
      const mods=(p.get('mods')||'').split(',').map(Number).filter(n=>MODULES.some(m=>m.id===n));
      if(mods.length){ if(p.get('start')==='1') this.start(mods); else this.setState({mods}); }
    }
  }
  kopieer(tekst,key){
    const klaar=()=>this.setState({kcGekopieerd:key});
    if(navigator.clipboard&&window.isSecureContext){ navigator.clipboard.writeText(tekst).then(klaar,()=>this.kopieerOud(tekst,klaar)); }
    else this.kopieerOud(tekst,klaar);
  }
  kopieerOud(tekst,klaar){
    const ta=document.createElement('textarea'); ta.value=tekst; ta.setAttribute('readonly',''); ta.style.position='fixed'; ta.style.opacity='0';
    document.body.appendChild(ta); ta.select(); try{ document.execCommand('copy'); klaar(); }catch(e){} document.body.removeChild(ta);
  }
  zoekNorm(t){ return String(t||'').normalize('NFD').replace(/[̀-ͯ]/g,'').toLowerCase(); }
  zoekBronnen(){
    const items=[], gezien=new Set();
    const voeg=(sectie,titel,tekst,ga)=>{ const sleutel=(titel+'|'+tekst).slice(0,200); if(gezien.has(sleutel)) return; gezien.add(sleutel); items.push({sectie,titel,tekst,ga}); };
    if(PAGINA==='home') voeg('Kwartaaltoets','Kennistoets AI-geletterdheid','Twee vragen per gekozen module, met uitleg bij elk antwoord. Vanaf 70% goed krijg je een deelnamebewijs voor je dossier.',()=>{ window.location.href=TOETSURL; });
    FAQ.forEach((f,i)=>voeg('Veelgestelde vragen',f.v,f.a,()=>this.setState({faqOpen:i},()=>this.scrollNaar('faq'))));
    Object.keys(KC.blokken).forEach(b=>KC.blokken[b].forEach(k=>{
      const sector=k.s.includes('alle')?'alle':k.s[0];
      voeg('Klantcommunicatie · '+KC.titels[b].replace(/^\d · /,''),k.titel,k.tekst+(k.bron?' ('+k.bron+')':''),()=>{
        const zicht=this.state.kcSector==='alle'||this.state.kcSector===sector||sector==='alle';
        this.setState(zicht?{}:{kcSector:sector},()=>this.scrollNaar('kc-'+k.k,true));
      });
    }));
    document.querySelectorAll('section[id]').forEach(sec=>{
      if(sec.id==='klantcommunicatie') return;
      const h2=sec.querySelector('h2'); const sectie=h2?h2.textContent.trim():sec.id;
      sec.querySelectorAll('h2,h3,h4,p,li,label').forEach(el=>{
        const tekst=el.textContent.replace(/\s+/g,' ').trim(); if(tekst.length<4) return;
        let titel=sectie;
        if(/^H[34]$/.test(el.tagName)) titel=tekst;
        else { let p=el.parentElement; while(p&&p!==sec){ const h=p.querySelector('h3,h4'); if(h&&h!==el){ titel=h.textContent.trim(); break; } p=p.parentElement; } }
        voeg(sectie,titel,tekst,()=>this.scrollNaarEl(el));
      });
    });
    return items;
  }
  zoekResultaten(){
    const q=this.zoekNorm(this.state.zoek).trim(); if(q.length<2) return [];
    const woorden=q.split(/\s+/).filter(Boolean);
    return this.zoekBronnen().map(it=>{
      const nt=this.zoekNorm(it.titel), nx=this.zoekNorm(it.tekst), alles=nt+' '+nx;
      if(!woorden.every(w=>alles.includes(w))) return null;
      let score=0; woorden.forEach(w=>{ if(nt.includes(w)) score+=3; if(nx.includes(w)) score+=1; if(nt.startsWith(w)) score+=2; });
      return {...it,score};
    }).filter(Boolean).sort((a,b)=>b.score-a.score).slice(0,8).map(it=>{
      const nx=this.zoekNorm(it.tekst), w=woorden.find(w=>nx.includes(w));
      let voor='',treffer='',na=it.tekst;
      if(w){ const i=nx.indexOf(w), s=Math.max(0,i-50);
        voor=(s>0?'…':'')+it.tekst.slice(s,i); treffer=it.tekst.slice(i,i+w.length);
        const rest=it.tekst.slice(i+w.length); na=rest.length>110?rest.slice(0,110)+'…':rest; }
      else if(na.length>140) na=na.slice(0,140)+'…';
      return {...it,voor,treffer,na};
    });
  }
  zoekGa(r){ this.setState({zoekOpen:false}); const el=document.getElementById('zoek'); if(el) el.blur(); r.ga(); }
  scrollNaarEl(el,flits=true){
    window.scrollTo({top:el.getBoundingClientRect().top+window.scrollY-90,behavior:'smooth'});
    if(flits){ el.style.outline='3px solid var(--color-accent)'; el.style.outlineOffset='4px'; setTimeout(()=>{ el.style.outline=''; el.style.outlineOffset=''; },1800); }
  }
'''
t = sub1("  scrollNaar(id){ const el=document.getElementById(id); if(el) window.scrollTo({top:el.getBoundingClientRect().top+window.scrollY-80,behavior:'smooth'}); }",
         METHODS + "  scrollNaar(id,flits){ const el=document.getElementById(id); if(!el){ if(PAGINA!=='home') window.location.href=HOME+'#'+id; return; } if(flits) this.scrollNaarEl(el); else window.scrollTo({top:el.getBoundingClientRect().top+window.scrollY-80,behavior:'smooth'}); }", t)

VALS = r'''
      ...(()=>{
        const sec=s.kcSector, ids=KC.sectoren.map(x=>x.id);
        const naam=Object.fromEntries(KC.sectoren.map(x=>[x.id,x.naam]));
        const kiesTab=id=>{ this.setState({kcSector:id}); setTimeout(()=>{ const b=document.getElementById('kc-tab-'+id); if(b) b.focus(); },0); };
        const zichtbaar=k=>sec==='alle'||k.s.includes('alle')||k.s.includes(sec);
        const map=(lijst,model)=>lijst.filter(zichtbaar).map(k=>({...k,anker:'kc-'+k.k,
          heeftTag:sec==='alle'&&!k.s.includes('alle'),tag:k.s.map(x=>naam[x]).join(', '),
          heeftBron:!!k.bron,
          kopieer:()=>this.kopieer(k.tekst,k.k),kopieerLabel:s.kcGekopieerd===k.k?'Gekopieerd':'Kopieer tekst'}));
        const kc={tabId:'kc-tab-'+sec,intro:KC.intro[sec]};
        Object.keys(KC.blokken).forEach(b=>{ kc[b]=map(KC.blokken[b]); });
        return {
          kc,
          kcTabs:KC.sectoren.map((x,i)=>{ const a=x.id===sec; return {naam:x.naam,tabId:'kc-tab-'+x.id,selected:a?'true':'false',tabindex:a?'0':'-1',
            bg:a?'var(--color-text)':'var(--color-bg)',fg:a?'var(--color-bg)':'var(--color-text)',kies:()=>kiesTab(x.id),
            toets:e=>{ let j=null; if(e.key==='ArrowRight') j=(i+1)%ids.length; else if(e.key==='ArrowLeft') j=(i-1+ids.length)%ids.length; else if(e.key==='Home') j=0; else if(e.key==='End') j=ids.length-1;
              if(j!==null){ e.preventDefault(); kiesTab(ids[j]); } }}; })
        };
      })(),
      ...(()=>{
        const res=s.zoekOpen?this.zoekResultaten():[];
        const actief=Math.min(s.zoekActief,Math.max(res.length-1,0));
        const toon=s.zoekOpen&&s.zoek.trim().length>=2;
        return {
          zoek:s.zoek, zoekToon:toon, zoekToonAttr:toon?'true':'false', zoekGeen:toon&&res.length===0,
          zoekResultaten:res.map((r,i)=>({...r,actiefAttr:i===actief?'true':'false',bg:i===actief?'var(--color-accent-100)':'var(--color-bg)',ga:()=>this.zoekGa(r)})),
          setZoek:e=>this.setState({zoek:e.target.value,zoekOpen:true,zoekActief:0}),
          zoekFocus:()=>this.setState({zoekOpen:true}),
          zoekBlur:()=>setTimeout(()=>this.setState({zoekOpen:false}),200),
          zoekKey:e=>{
            if(e.key==='ArrowDown'){ e.preventDefault(); this.setState({zoekActief:Math.min(actief+1,res.length-1)}); }
            else if(e.key==='ArrowUp'){ e.preventDefault(); this.setState({zoekActief:Math.max(actief-1,0)}); }
            else if(e.key==='Enter'){ e.preventDefault(); if(res[actief]) this.zoekGa(res[actief]); }
            else if(e.key==='Escape'){ this.setState({zoek:'',zoekOpen:false}); }
          }
        };
      })(),'''
t = sub1("      deelLabel:s.gedeeld?", VALS + "\n      deelLabel:s.gedeeld?", t)

exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'feest.py')).read())
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'extras.py')).read())
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'ronde3.py')).read())
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'ronde4.py')).read())
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'variants.py')).read())
