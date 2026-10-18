# ---------- opties overgenomen van pa-wft.nl ----------
H2 = 'margin:0;font-size:clamp(28px,3.4vw,40px);line-height:1.05;letter-spacing:-0.02em'
LBLS = 'font-size:11px;letter-spacing:0.1em;text-transform:uppercase;font-weight:700;color:var(--color-accent-700)'
FLINK = 'color:var(--color-bg);text-decoration:none'

# 1. Gratis-blok met agenda-herinnering en zoeken, direct onder de hero
GRATIS = f'''<section id="gratis" style="border-bottom:2px solid var(--color-divider);background:var(--color-surface)">
  <div style="max-width:1200px;margin:0 auto;padding:48px var(--space-6);display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,340px),1fr));gap:var(--space-8);align-items:start">
    <div style="display:flex;flex-direction:column;gap:var(--space-3)">
      <span style="{LBLS}">Gratis voor alle adviseurs en medewerkers</span>
      <p style="margin:0;font-size:17px;line-height:1.6;text-wrap:pretty">AI Permanent Actueel helpt je je AI-kennis bij te houden. Oefen precies de modules die bij jouw rol en klantcontact horen, met uitleg bij elk antwoord. Zonder kosten, zonder abonnement en zonder account.</p>
      <p style="margin:0;font-size:15px;line-height:1.6;text-wrap:pretty">Doe de toets elk kwartaal, zo blijf je permanent actueel. Bewaar het certificaat in je personeelsdossier en lever het ook in bij je werkgever.</p>
      <div style="display:flex;flex-wrap:wrap;gap:var(--space-2);margin-top:var(--space-2)">
        <a class="btn btn-primary" href="kennistoets/" style="justify-content:flex-start;padding:12px 18px;font-size:15px">Start de kennistoets</a>
        <a class="btn btn-secondary" href="#modules" style="justify-content:flex-start;padding:12px 18px;font-size:15px;background:var(--color-bg)">Bekijk de 7 modules</a>
      </div>
    </div>
    <div style="display:flex;flex-direction:column;gap:var(--space-4)">
      <div style="background:var(--color-bg);border:2px solid var(--color-text);padding:var(--space-4) var(--space-6);display:flex;flex-direction:column;gap:var(--space-3)">
        <h3 style="margin:0;font-size:17px">Zet een herinnering in je agenda</h3>
        <p style="margin:0;font-size:14px;line-height:1.5">Elke eerste maandag van het kwartaal, de komende 5 jaar, met een link naar de toets.</p>
        <div style="display:flex;flex-wrap:wrap;gap:var(--space-2)">
          <button type="button" class="btn btn-primary" sc-camel-on-click="{{{{ agendaIcs }}}}" style="justify-content:flex-start">Zet in mijn agenda (Outlook, Apple)</button>
          <a class="btn btn-secondary" href="{{{{ agendaGoogle }}}}" target="_blank" rel="noopener" style="justify-content:flex-start">Google Agenda</a>
        </div>
      </div>
      <form role="search" action="./" method="get" sc-camel-on-submit="{{{{ heroZoek }}}}" style="background:var(--color-bg);border:2px solid var(--color-text);padding:var(--space-4) var(--space-6);display:flex;flex-direction:column;gap:var(--space-2)">
        <label for="zoek-hero" style="font-size:17px;font-weight:700">Zoek op de site</label>
        <div style="display:flex;gap:var(--space-2)">
          <input id="zoek-hero" name="q" type="search" class="input" value="{{{{ heroZoekTekst }}}}" sc-camel-on-change="{{{{ setHeroZoek }}}}" placeholder="Bijvoorbeeld: artikel 50, privacyverklaring, shadow AI" style="flex:1;min-width:0">
          <button type="submit" class="btn btn-primary" style="justify-content:flex-start">Zoeken</button>
        </div>
      </form>
    </div>
  </div>
</section>

'''
t = sub1('<section id="artikel4" ', GRATIS + '<section id="artikel4" ', t)

# 2. Tip je collega's
TIP = f'''<section id="tip" style="border-bottom:2px solid var(--color-divider);background:var(--color-surface)">
  <div style="max-width:1200px;margin:0 auto;padding:56px var(--space-6);display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,340px),1fr));gap:var(--space-8);align-items:start">
    <div style="display:flex;flex-direction:column;gap:var(--space-3)">
      <span style="{LBLS}">Delen</span>
      <h2 style="{H2}">Tip je collega’s</h2>
      <p style="margin:0;font-size:15px;line-height:1.6">Ken je collega’s die hun AI-kennis ook actueel willen houden? Vul hun e-mailadressen in. We zetten een mail met een korte uitnodiging klaar in je eigen mailprogramma; jij kijkt hem na en verstuurt hem zelf. De adressen gaan niet naar DFO en worden nergens bewaard.</p>
    </div>
    <div class="span2" style="background:var(--color-bg);border:2px solid var(--color-text);padding:var(--space-6);display:flex;flex-direction:column;gap:var(--space-4);grid-column:span 2;min-width:0">
      <div class="field" style="display:flex;flex-direction:column;gap:var(--space-1)">
        <label for="tip-adressen" style="font-weight:700">E-mailadressen van je collega’s</label>
        <span id="tip-hulp" style="font-size:12px;opacity:0.75">Eén of meer adressen, gescheiden door een komma, puntkomma of nieuwe regel.</span>
        <textarea id="tip-adressen" class="input" aria-describedby="tip-hulp" value="{{{{ tipAdressen }}}}" sc-camel-on-change="{{{{ setTipAdressen }}}}" rows="3" placeholder="naam@kantoor.nl, collega@kantoor.nl" style="width:100%"></textarea>
      </div>
      <div class="field" style="display:flex;flex-direction:column;gap:var(--space-1)">
        <label for="tip-naam" style="font-weight:700">Je naam (onder de mail, optioneel)</label>
        <input id="tip-naam" class="input" value="{{{{ tipNaam }}}}" sc-camel-on-change="{{{{ setTipNaam }}}}" placeholder="Voor- en achternaam" style="width:100%">
      </div>
      <label style="display:flex;gap:var(--space-2);align-items:center;font-size:14px;cursor:pointer"><input type="checkbox" checked="{{{{ tipBcc }}}}" sc-camel-on-change="{{{{ setTipBcc }}}}" style="width:18px;height:18px;accent-color:var(--color-accent)">Verstuur als bcc, zodat collega’s elkaars adres niet zien</label>
      <sc-if value="{{{{ tipFout }}}}" hint-placeholder-val="{{{{ false }}}}">
        <p role="alert" style="margin:0;font-size:14px;font-weight:700;color:var(--color-accent-700)">{{{{ tipFoutTekst }}}}</p>
      </sc-if>
      <div style="display:flex;flex-wrap:wrap;gap:var(--space-2)">
        <button type="button" class="btn btn-primary" sc-camel-on-click="{{{{ tipMail }}}}" style="justify-content:flex-start">Zet de mail klaar</button>
        <button type="button" class="btn btn-secondary" sc-camel-on-click="{{{{ tipKopieer }}}}" style="justify-content:flex-start">{{{{ tipKopieerLabel }}}}</button>
      </div>
      <details style="border-top:2px solid var(--color-divider);padding-top:var(--space-3)">
        <summary style="cursor:pointer;font-weight:700;font-size:14px">Bekijk de tekst van de mail</summary>
        <pre style="margin:var(--space-3) 0 0;white-space:pre-wrap;font:inherit;font-size:14px;line-height:1.55;background:var(--color-surface);padding:var(--space-3)">{{{{ tipVoorbeeld }}}}</pre>
      </details>
    </div>
  </div>
</section>

'''
nieuws_start = t.rindex('<section', 0, t.index('Blijf op de hoogte</h2>'))
t = t[:nieuws_start] + TIP + t[nieuws_start:]
# oude kopieer-link in de FAQ verwijst nu naar de tip-sectie
t = sub1('''<span style="font-size:14px;line-height:1.5">Eén link voor het hele team, zonder account.</span>
        <button type="button" class="btn btn-primary" sc-camel-on-click="{{ deelLink }}" style="justify-content:flex-start;align-self:flex-start">{{ deelLabel }}</button>''',
'''<span style="font-size:14px;line-height:1.5">Eén link voor het hele team, zonder account.</span>
        <a class="btn btn-primary" href="#tip" style="justify-content:flex-start;align-self:flex-start">Nodig je collega’s uit</a>''', t)

# 3. Blijf op de hoogte
ns = t.rindex('<section', 0, t.index('Blijf op de hoogte</h2>'))
ne = t.index('</section>', ns) + len('</section>\n')
NIEUWS = f'''<section id="nieuws" style="border-bottom:2px solid var(--color-divider)">
  <div style="max-width:1200px;margin:0 auto;padding:56px var(--space-6);display:flex;flex-direction:column;gap:var(--space-6)">
    <div style="display:flex;flex-direction:column;gap:var(--space-3)">
      <span style="{LBLS}">{re.search(r'>(\d\d) — Nieuws<', t[ns:ne]).group(1)} — Nieuws</span>
      <h2 style="{H2}">Blijf op de hoogte</h2>
      <p style="margin:0;font-size:16px;line-height:1.6">Zo blijf je op de hoogte van het actuele nieuws. Lees de <a href="nieuw/">updates en tijdlijn</a> op deze site en meld je aan voor de nieuwsbrieven van DFO.</p>
    </div>
    <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,320px),1fr));border-top:2px solid var(--color-text);border-left:2px solid var(--color-text)">
      <div style="padding:var(--space-6);border-right:2px solid var(--color-text);border-bottom:2px solid var(--color-text);display:flex;flex-direction:column;gap:var(--space-3)">
        <h3 style="margin:0;font-size:20px">DFO Signalen</h3>
        <p style="margin:0;font-size:14px;line-height:1.5;flex:1">Wekelijks signalen uit de markt, modelteksten en praktijkanalyses voor het advieskantoor, met een archief dat jaren teruggaat.</p>
        <a class="btn btn-secondary" href="https://www.dfosignalen.nl/" style="justify-content:flex-start;align-self:flex-start">Meld je aan voor DFO Signalen</a>
      </div>
      <div style="padding:var(--space-6);border-right:2px solid var(--color-text);border-bottom:2px solid var(--color-text);display:flex;flex-direction:column;gap:var(--space-3)">
        <h3 style="margin:0;font-size:20px">Nieuwsbrief Wft</h3>
        <p style="margin:0;font-size:14px;line-height:1.5;flex:1">Gemiddeld één keer per week de actuele ontwikkelingen in wet- en regelgeving en toezicht, kort en praktisch uitgelegd voor financieel dienstverleners.</p>
        <a class="btn btn-secondary" href="https://www.dfobv.nl/product/nieuwsbrief-wft/" style="justify-content:flex-start;align-self:flex-start">Meld je aan voor de Nieuwsbrief Wft</a>
      </div>
    </div>
    <p style="margin:0;font-size:12px;opacity:0.7">Aanmelden gaat via de website van DFO. AI Permanent Actueel slaat zelf geen gegevens op.</p>
  </div>
</section>
'''
t = t[:ns] + NIEUWS + t[ne:]

# 4. Afsluitende oproep
t = sub1('max-width:14ch;text-wrap:balance">Blijf dit jaar aantoonbaar AI-actueel.</h2>',
         'max-width:18ch;text-wrap:balance">Oefen alle modules die je nodig hebt. Gratis!</h2>', t)

# 5. Let op + 6. footer (NL en EN)
def letop(lang):
    if lang == 'en':
        return ('<p style="margin:0;max-width:110ch"><b>Please note.</b> The knowledge test is a practice test. It is not a recognised exam and not proof that an organisation complies with the EU AI Act. '
                'Have your own AI policy and records reviewed by compliance or a lawyer. DFO BV is not responsible for the accuracy and completeness of all questions and answers; rules change. '
                'Want to be sure? Contact <a href="https://www.dfobv.nl/">DFO BV</a> at <a href="tel:+31332580460">+31 33 258 04 60</a> or <a href="mailto:info@dfobv.nl">info@dfobv.nl</a>.</p>')
    return ('<p style="margin:0;max-width:110ch"><b>Let op.</b> De kennistoets is een oefentoets. Het certificaat is een deelnamebewijs, geen diploma, geen erkend examen en geen bewijs dat de organisatie aan de AI-verordening voldoet. '
            'Laat de eigen AI-policy en vastlegging toetsen door compliance of een jurist. DFO BV is niet verantwoordelijk voor de juistheid en volledigheid van alle vragen en antwoorden; regels wijzigen. '
            'Wil je het zeker weten? Neem contact op met <a href="https://www.dfobv.nl/">DFO BV</a> via <a href="tel:+31332580460">033 258 04 60</a> of <a href="mailto:info@dfobv.nl">info@dfobv.nl</a>.</p>')

OUD_LETOP = re.search(r'<p style="margin:0;max-width:110ch"><b>Let op.</b>.*?</p>', t).group(0)
t = sub1(OUD_LETOP, letop('nl'), t)

def footer(lang, home, toets):
    en = lang == 'en'
    T = (lambda nl, e: e if en else nl)
    kol = lambda titel, links: (f'''    <div style="display:flex;flex-direction:column;gap:var(--space-2);font-size:13px">
      <span style="font-size:11px;letter-spacing:0.1em;text-transform:uppercase;font-weight:700;color:var(--color-accent-400)">{titel}</span>
''' + ''.join(f'      <a href="{h}" style="{FLINK}">{n}</a>\n' for n, h in links) + '    </div>\n')
    nl_tag = ' (NL)' if en else ''
    return f'''<footer style="background:var(--color-accent-900);color:var(--color-bg);margin-top:auto">
  <div style="max-width:1200px;margin:0 auto;padding:56px var(--space-6) var(--space-6);display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,180px),1fr));gap:var(--space-8)">
    <div style="display:flex;flex-direction:column;gap:var(--space-3)">
      <span style="font-size:18px;font-weight:800">AI Permanent Actueel</span>
      <p style="margin:0;font-size:13px;line-height:1.5;opacity:0.8">{T("Gratis oefentoets AI-geletterdheid voor adviseurs en klantmedewerkers. Kennis actueel, elk kwartaal weer.", "Free AI literacy practice test for advisers and client-facing staff. Up to date, every quarter.")}</p>
      <a class="btn" href="{toets}" style="justify-content:flex-start;align-self:flex-start;background:var(--color-bg);color:var(--color-text);font-weight:700">{T("Start de kennistoets", "Start the knowledge test")}</a>
    </div>
{kol(T("Toets en kennis", "Test and knowledge"), [
    (T("Kennistoets", "Knowledge test"), toets), ("Modules" + nl_tag, home + "#modules"),
    (T("Klantcommunicatie bij AI", "Client communication on AI") + nl_tag, home + "#klantcommunicatie"),
    (T("Tip je collega’s", "Tell your colleagues") + nl_tag, home + "#tip"),
    (T("Welke modules heb ik nodig?", "Which modules do I need?") + nl_tag, home + "#pakket"),
    (T("Kantoorscan", "Firm scan") + nl_tag, home + "#scan"),
    (T("Dossier voor de werkgever", "Records for the employer") + nl_tag, home + "#dossier"),
    (T("Register AI-geletterdheid", "AI literacy register") + nl_tag, home + "register/"),
    (T("Veelgestelde vragen", "Frequently asked questions") + nl_tag, home + "#faq")])}{kol(T("Kennis", "Knowledge") + nl_tag, [
    (T("Wat is er nieuw", "What's new"), home + "nieuw/"), (T("Begrippenlijst", "Glossary"), home + "begrippen/"),
    (T("Wet- en regelgeving", "Laws and regulations"), home + "wetgeving/"),
    (T("Artikel 4: AI-geletterdheid", "Article 4: AI literacy"), home + "artikel-4-ai-geletterdheid/"),
    (T("AI in je privacyverklaring", "AI in your privacy statement"), home + "ai-in-de-privacyverklaring/"),
    (T("AI-chatbot melden aan de klant", "Disclosing an AI chatbot"), home + "ai-chatbot-melden-aan-klant/"),
    (T("AI voor volmachtbedrijven", "AI for underwriting agencies"), home + "ai-voor-volmachtbedrijven/"),
    (T("AI bij kredietadvies", "AI in credit advice"), home + "ai-kredietadvies-geautomatiseerde-beoordeling/"),
    (T("Over en verantwoording", "About"), home + "over/")])}{kol("DFO", [
    ("Wft Permanent Actueel", "https://pa-wft.nl/"), ("DFO Compliance", "https://www.dfobv.nl/"), (T("DFO Opleidingen", "DFO Training"), "https://www.dfobv.nl/"),
    (T("Ons team", "Our team"), "https://www.dfobv.nl/ons-team/"), ("DFO Signalen", "https://www.dfosignalen.nl/"),
    ("Nieuwsbrief Wft", "https://www.dfobv.nl/product/nieuwsbrief-wft/"), ("DFO Kennisbank", "https://kennisbank.dfobv.nl/")])}    <div style="display:flex;flex-direction:column;gap:var(--space-2);font-size:13px;line-height:1.5">
      <span style="font-size:11px;letter-spacing:0.1em;text-transform:uppercase;font-weight:700;color:var(--color-accent-400)">Contact</span>
      <span>DFO BV<br>De Wel 14–16<br>3871 MV Hoevelaken{T("", "<br>The Netherlands")}</span>
      <a href="tel:+31332580460" style="{FLINK}">{T("033 258 04 60", "+31 33 258 04 60")}</a>
      <a href="mailto:info@dfobv.nl" style="{FLINK}">info@dfobv.nl</a>
      <a href="https://www.dfobv.nl/contact/" style="{FLINK}">{T("Contactpagina", "Contact page")}</a>
      <span style="opacity:0.7;font-size:12px">KvK 32068727 · {T("btw", "VAT")} NL806480828B01</span>
    </div>
  </div>
  <div style="max-width:1200px;margin:0 auto;padding:var(--space-4) var(--space-6);border-top:2px solid var(--color-neutral-700);display:flex;justify-content:space-between;align-items:center;gap:var(--space-4);flex-wrap:wrap;font-size:12px">
    <a href="{home}privacy/" style="{FLINK};font-weight:700">{T("Privacy, voorwaarden en klachten", "Privacy, terms and complaints (NL)")}</a>
    <span style="opacity:0.7">{T("© 2026 DFO BV. AI Permanent Actueel is een activiteit van DFO BV. Oefentoets voor medewerkers van financieel dienstverleners; geen erkend examen en geen advies.", "© 2026 DFO BV. AI Permanent Actueel is an activity of DFO BV. Practice test for staff of financial service providers; not a recognised exam and not advice.")}</span>
    <span style="background:var(--color-bg);padding:6px 10px;display:flex"><img src="d846bd37-2ca1-4ae8-90ed-e35a3c300d49" alt="{T("DFO — dienstverlening voor financiële ondernemers", "DFO — services for financial businesses")}" style="height:28px;display:block"></span>
  </div>
</footer>
'''

fs_ = t.index('<footer'); fe_ = t.index('</footer>\n') + len('</footer>\n')
t = t[:fs_] + '__FOOTER__' + t[fe_:]

# JS: state + handlers
t = sub1("zoek:'', zoekOpen:false, zoekActief:0 };", "zoek:'', zoekOpen:false, zoekActief:0, heroZoekTekst:'', tipAdressen:'', tipNaam:'', tipBcc:true, tipFout:'', tipGekopieerd:false };", t)
EXTRA_M = r'''
  agendaStart(){
    const n=new Date(); let j=n.getFullYear(), m=Math.floor(n.getMonth()/3)*3+3; if(m>11){ m=0; j++; }
    const d=new Date(j,m,1); while(d.getDay()!==1) d.setDate(d.getDate()+1); return d;
  }
  agendaTekst(){ return {titel:'AI Permanent Actueel: kwartaaltoets AI-geletterdheid', url:'https://ai-permanent-actueel.nl/kennistoets/',
    oms:'Doe de kwartaaltoets AI-geletterdheid en bewaar het certificaat in je personeelsdossier: https://ai-permanent-actueel.nl/kennistoets/'}; }
  agendaIcs(){
    const d=this.agendaStart(), e=new Date(d), a=this.agendaTekst(); e.setDate(e.getDate()+1);
    const f=x=>x.getFullYear()+pad(x.getMonth()+1)+pad(x.getDate()), nu=new Date().toISOString().replace(/[-:]/g,'').slice(0,15)+'Z';
    const ics=['BEGIN:VCALENDAR','VERSION:2.0','PRODID:-//DFO BV//AI Permanent Actueel//NL','CALSCALE:GREGORIAN','METHOD:PUBLISH','BEGIN:VEVENT',
      'UID:aipa-kwartaal-'+f(d)+'@ai-permanent-actueel.nl','DTSTAMP:'+nu,'DTSTART;VALUE=DATE:'+f(d),'DTEND;VALUE=DATE:'+f(e),
      'RRULE:FREQ=MONTHLY;INTERVAL=3;BYDAY=1MO;COUNT=20','SUMMARY:'+a.titel,'DESCRIPTION:'+a.oms,'URL:'+a.url,'TRANSP:TRANSPARENT',
      'BEGIN:VALARM','ACTION:DISPLAY','DESCRIPTION:'+a.titel,'TRIGGER:PT9H','END:VALARM','END:VEVENT','END:VCALENDAR'].join('\r\n');
    const blob=new Blob([ics],{type:'text/calendar;charset=utf-8'}), u=URL.createObjectURL(blob), l=document.createElement('a');
    l.href=u; l.download='ai-permanent-actueel-kwartaaltoets.ics'; document.body.appendChild(l); l.click(); l.remove(); setTimeout(()=>URL.revokeObjectURL(u),1000);
  }
  agendaGoogle(){
    const d=this.agendaStart(), e=new Date(d), a=this.agendaTekst(); e.setDate(e.getDate()+1);
    const f=x=>x.getFullYear()+pad(x.getMonth()+1)+pad(x.getDate());
    return 'https://calendar.google.com/calendar/render?action=TEMPLATE&text='+encodeURIComponent(a.titel)+'&dates='+f(d)+'/'+f(e)+
      '&details='+encodeURIComponent(a.oms)+'&recur='+encodeURIComponent('RRULE:FREQ=MONTHLY;INTERVAL=3;BYDAY=1MO;COUNT=20')+'&ctz=Europe/Amsterdam';
  }
  tipTekst(){
    const naam=this.state.tipNaam.trim();
    return {onderwerp:'Tip: gratis kennistoets AI-geletterdheid (AI Permanent Actueel)',
      body:'Hoi,\n\nIk gebruik AI Permanent Actueel om mijn AI-kennis bij te houden: elk kwartaal een korte oefentoets met uitleg bij elk antwoord en een deelnamebewijs voor het personeelsdossier. Speciaal voor medewerkers van financieel dienstverleners, gratis en zonder account.\n\nHandig voor de AI-geletterdheid die artikel 4 van de AI-verordening vraagt.\n\nDoe de toets: https://ai-permanent-actueel.nl/kennistoets/\n\nGroet,\n'+(naam||'[je naam]')};
  }
  tipAdressenLijst(){ return this.state.tipAdressen.split(/[\s,;]+/).map(x=>x.trim()).filter(Boolean); }
  tipMail(){
    const lijst=this.tipAdressenLijst(), fout=lijst.filter(x=>!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(x));
    if(!lijst.length){ this.setState({tipFout:'Vul minstens één e-mailadres in.'}); return; }
    if(fout.length){ this.setState({tipFout:'Controleer dit adres: '+fout.join(', ')}); return; }
    this.setState({tipFout:''});
    const {onderwerp,body}=this.tipTekst(), adr=lijst.join(',');
    const q='subject='+encodeURIComponent(onderwerp)+'&body='+encodeURIComponent(body);
    window.location.href=this.state.tipBcc?'mailto:?bcc='+encodeURIComponent(adr)+'&'+q:'mailto:'+adr+'?'+q;
  }
'''
t = sub1("  kopieer(tekst,key){", EXTRA_M + "  kopieer(tekst,key){", t)
EXTRA_V = r'''
      agendaIcs:()=>this.agendaIcs(), agendaGoogle:this.agendaGoogle(),
      heroZoekTekst:s.heroZoekTekst, setHeroZoek:e=>this.setState({heroZoekTekst:e.target.value}),
      heroZoek:e=>{ e.preventDefault(); const q=s.heroZoekTekst.trim(); if(!q) return;
        this.setState({zoek:q,zoekOpen:true,zoekActief:0},()=>{ window.scrollTo({top:0,behavior:'smooth'}); const el=document.getElementById('zoek'); if(el) el.focus({preventScroll:true}); }); },
      tipAdressen:s.tipAdressen, setTipAdressen:e=>this.setState({tipAdressen:e.target.value,tipFout:''}),
      tipNaam:s.tipNaam, setTipNaam:e=>this.setState({tipNaam:e.target.value,tipGekopieerd:false}),
      tipBcc:s.tipBcc, setTipBcc:e=>this.setState({tipBcc:e.target.checked}),
      tipFout:!!s.tipFout, tipFoutTekst:s.tipFout,
      tipMail:()=>this.tipMail(),
      tipVoorbeeld:(()=>{ const x=this.tipTekst(); return 'Onderwerp: '+x.onderwerp+'\n\n'+x.body; })(),
      tipKopieerLabel:s.tipGekopieerd?'Gekopieerd':'Kopieer de tekst',
      tipKopieer:()=>{ const x=this.tipTekst(); this.kopieer(x.onderwerp+'\n\n'+x.body,'__tip'); this.setState({tipGekopieerd:true}); },'''
t = sub1("\n      deelLabel:s.gedeeld?", EXTRA_V + "\n      deelLabel:s.gedeeld?", t)
