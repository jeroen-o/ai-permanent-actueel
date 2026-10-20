# ---------- twee pagina's: home en kennistoets ----------
D = WERK
TOETS_URL = SITE + 'kennistoets/'
TOETS_TITLE = 'Kennistoets AI-geletterdheid | AI Permanent Actueel'
TOETS_DESC = ('Gratis oefentoets AI-geletterdheid (art. 4 AI-verordening) voor financieel dienstverleners: '
              'zeven vragen per module, uitleg bij elk antwoord en een deelnamebewijs vanaf 70% goed.')
ORG = jsonld([])  # bevat Organization + WebSite
ORG_G = [x for x in json.loads(ORG)['@graph'] if x['@type'] in ('Organization', 'WebSite')]
TOETS_LD = json.dumps({"@context": "https://schema.org", "@graph": ORG_G + [
    {"@type": "WebPage", "@id": TOETS_URL + "#webpage", "url": TOETS_URL, "name": TOETS_TITLE, "description": TOETS_DESC,
     "inLanguage": "nl-NL", "isPartOf": {"@id": SITE + "#website"}, "publisher": {"@id": SITE + "#dfo"}, "dateModified": "2026-10-18",
     "breadcrumb": {"@id": TOETS_URL + "#breadcrumb"},
     "mainEntity": {"@type": "Quiz", "name": "Kennistoets AI-geletterdheid", "inLanguage": "nl-NL", "isAccessibleForFree": True,
                    "about": [{"@type": "Thing", "name": m["naam"]} for m in DC["MODULES"]],
                    "educationalUse": "Oefentoets AI-geletterdheid (artikel 4 AI-verordening)", "provider": {"@id": SITE + "#dfo"}}},
    {"@type": "BreadcrumbList", "@id": TOETS_URL + "#breadcrumb", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "AI Permanent Actueel", "item": SITE},
        {"@type": "ListItem", "position": 2, "name": "Kennistoets", "item": TOETS_URL}]},
]}, ensure_ascii=False)

HEAD_HOME = seo_head(FAQ_ALL)
HEAD_TOETS = head_html(TOETS_TITLE, TOETS_DESC, TOETS_URL, TOETS_LD)

ts = t.index('<section id="toets" ')
te = t.index('</section>', ts) + len('</section>\n')
TOETS_SECTIE = t[ts:te]

# --- home: toets vervangen door verwijzing ---
LBL = 'font-size:11px;letter-spacing:0.1em;text-transform:uppercase;font-weight:700;color:var(--color-accent-700)'
lbl = re.search(r'>(\d\d) — Kwartaaltoets<', TOETS_SECTIE).group(1)
TEASER = f'''<section id="toets" style="border-bottom:2px solid var(--color-divider);background:var(--color-surface)">
  <div style="max-width:1200px;margin:0 auto;padding:56px var(--space-6);display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,320px),1fr));gap:var(--space-8);align-items:start">
    <div style="display:flex;flex-direction:column;gap:var(--space-3)">
      <span style="{LBL}">{lbl} — Kwartaaltoets</span>
      <h2 style="margin:0;font-size:clamp(28px,3.4vw,40px);line-height:1.05;letter-spacing:-0.02em">Kennistoets AI-geletterdheid</h2>
      <p style="margin:0;font-size:15px;line-height:1.55">Zeven vragen per gekozen module, met uitleg bij elk antwoord. Vanaf 70% goed krijg je een deelnamebewijs voor je dossier.</p>
      <p style="margin:0;font-size:12px;opacity:0.7">Oefentoets — geen erkend examen en geen bewijs van naleving.</p>
    </div>
    <div style="background:var(--color-bg);border:2px solid var(--color-text);padding:var(--space-6);display:flex;flex-direction:column;gap:var(--space-4);grid-column:span 2;min-width:0">
      <h3 style="margin:0;font-size:20px">7 modules · 7 vragen per module · deelnamebewijs vanaf 70%</h3>
      <p style="margin:0;font-size:15px;line-height:1.55">De toets staat op een eigen pagina. Kies daar zelf de modules, of start vanuit de pakket-check met precies de modules die bij jouw rol horen.</p>
      <div style="display:flex;flex-wrap:wrap;gap:var(--space-2)">
        <a class="btn btn-primary" href="kennistoets/" style="justify-content:flex-start;padding:12px 18px;font-size:15px">Naar de kennistoets</a>
        <a class="btn btn-secondary" href="#pakket" style="justify-content:flex-start;padding:12px 18px;font-size:15px">Eerst mijn pakket bepalen</a>
      </div>
    </div>
  </div>
</section>
'''
home = t[:ts] + TEASER + t[te:]
home = home.replace('href="#toets"', 'href="kennistoets/"')
home = sub1("startUitPakket:()=>pakket.length&&this.start(pakket),",
            "startUitPakket:()=>{ if(pakket.length) window.location.href=TOETSURL+'?mods='+pakket.join(',')+'&start=1'; },", home)
home = home.replace("const PAGINA='__PAGINA__';", "const PAGINA='home';")

# --- kennistoets: header + toets + let op + footer ---
bs = t.index('<section id="top"')
lo = t.rindex('<section', 0, t.index('<b>Let op.</b>'))
le = t.index('</section>', lo) + len('</section>\n')
fs = t.index('__FOOTER__')
sectie = TOETS_SECTIE
sectie = re.sub(r'>\d\d — Kwartaaltoets<', '>Kwartaaltoets · AI Permanent Actueel<', sectie)
sectie = sub1('<h2 style="margin:0;font-size:clamp(28px,3.4vw,40px);line-height:1.05;letter-spacing:-0.02em">Kennistoets AI-geletterdheid</h2>',
              '<h1 style="margin:0;font-size:clamp(32px,4.4vw,52px);line-height:1.05;letter-spacing:-0.02em">Kennistoets AI-geletterdheid</h1>', sectie)
sectie = sub1('<p style="margin:0;font-size:12px;opacity:0.7">Oefentoets — geen erkend examen en geen bewijs van naleving.</p>',
              '<p style="margin:0;font-size:12px;opacity:0.7">Oefentoets — geen erkend examen en geen bewijs van naleving.</p>\n'
              '      <p style="margin:0;font-size:14px"><a href="../#pakket">Welke modules horen bij mijn rol?</a></p>', sectie)
kop, staart = t[:bs], t[fs:]
kop = kop.replace('href="#toets"', 'href="./"').replace('href="#', 'href="../#')
staart = staart.replace('href="#toets"', 'href="./"').replace('href="#', 'href="../#')
toets = kop + '<main>\n' + sectie + '</main>\n\n' + t[lo:le] + '\n' + staart
toets = toets.replace(f'<title>{TITLE}</title>', f'<title>{TOETS_TITLE}</title>')
toets = toets.replace("const PAGINA='__PAGINA__';", "const PAGINA='toets';")
assert 'id="klantcommunicatie"' not in toets and 'href="#' not in toets
# ---------- Engelse kennistoets ----------
EN_URL = SITE + 'en/knowledge-test/'
EN_TITLE = 'AI Literacy Knowledge Test | AI Permanent Actueel'
EN_DESC = ('Free AI literacy practice test (Article 4 EU AI Act) for staff of Dutch financial service providers: '
           'seven questions per module, an explanation for every answer and a certificate of participation from 70%.')

MODULES_EN = [
  (1, "AI basics", "What AI is, how a language model works and what you can and cannot expect from it."),
  (2, "EU AI Act", "Article 4, transparency for chatbots and generated content, risk categories and supervision."),
  (3, "Privacy and GDPR", "Client data in AI tools, legal basis, data processing agreements and data breaches."),
  (4, "Risk and quality", "Hallucinations, bias, source checking and human oversight."),
  (5, "AI in the client process", "Duty of care, record keeping and client communication for AI-assisted work."),
  (6, "Safe use and policy", "AI policy, approved tools, shadow AI and record keeping."),
  (7, "Case law and liability", "What courts do with unchecked AI output, and who pays the bill."),
]


EN_LD = json.dumps({"@context": "https://schema.org", "@graph": ORG_G + [
    {"@type": "WebPage", "@id": EN_URL + "#webpage", "url": EN_URL, "name": EN_TITLE, "description": EN_DESC,
     "inLanguage": "en", "isPartOf": {"@id": SITE + "#website"}, "publisher": {"@id": SITE + "#dfo"}, "dateModified": "2026-10-18",
     "mainEntity": {"@type": "Quiz", "name": "AI Literacy Knowledge Test", "inLanguage": "en", "isAccessibleForFree": True,
                    "about": [{"@type": "Thing", "name": m[1]} for m in MODULES_EN], "provider": {"@id": SITE + "#dfo"}}},
]}, ensure_ascii=False)
HREFLANG = (f'<link rel="alternate" hreflang="nl" href="{TOETS_URL}">\n<link rel="alternate" hreflang="en" href="{EN_URL}">\n'
            f'<link rel="alternate" hreflang="x-default" href="{TOETS_URL}">\n')
HEAD_EN = HREFLANG + head_html(EN_TITLE, EN_DESC, EN_URL, EN_LD).replace('content="nl_NL"', 'content="en_GB"')
HEAD_TOETS = HREFLANG + HEAD_TOETS

def to_en(x):
    def r(old, new, n=1):
        nonlocal x
        assert x.count(old) == n, (x.count(old), old[:90]); x = x.replace(old, new)
    r('<html lang="nl"><head>\n', '<html lang="en"><head>\n')
    r(HEAD_TOETS_BASE, HEAD_EN)
    r(f'<title>{TOETS_TITLE}</title>', f'<title>{EN_TITLE}</title>')
    x = x.replace('href="../', 'href="../../')
    # navigatie
    a = x.index('<nav aria-label="Hoofdnavigatie"'); b = x.index('</nav>', a) + len('</nav>')
    x = x[:a] + '''<nav aria-label="Main navigation" style="display:flex;flex-wrap:wrap;gap:var(--space-4);font-size:13px;font-weight:600">
      <a href="../../" style="color:var(--color-text);text-decoration:none">Home (NL)</a>
      <a href="./" style="color:var(--color-text);text-decoration:none">Knowledge test</a>
      <a href="../../kennistoets/" hreflang="nl" lang="nl" style="color:var(--color-text);text-decoration:none">Nederlands</a>
    </nav>''' + x[b:]
    a = x.index('\n    <div class="zoek-wrap" role="search"'); b = x.index('\n    </div>\n', x.index('id="zoek-resultaten"')) + len('\n    </div>')
    x = x[:a] + x[b:]
    # toetssectie
    r('>Kwartaaltoets · AI Permanent Actueel<', '>Quarterly test · AI Permanent Actueel<')
    r('>Kennistoets AI-geletterdheid</h1>', '>AI Literacy Knowledge Test</h1>')
    r('line-height:1.55">Zeven vragen per gekozen module, elke keer willekeurig gekozen uit een vragenbank van vijfenveertig per module, met uitleg bij elk antwoord. Vanaf 70% goed krijg je een deelnamebewijs voor je dossier.',
      'line-height:1.55">Seven questions per selected module, randomly drawn each time from a bank of forty-five per module, with an explanation for every answer. Score 70% or more to get a certificate of participation for your records. Questions refer to Dutch and EU rules for financial service providers.')
    r('Oefentoets — geen erkend examen en geen bewijs van naleving.', 'Practice test — not a recognised exam and no proof of compliance.')
    r('\n      <p style="margin:0;font-size:14px"><a href="../../#pakket">Welke modules horen bij mijn rol?</a></p>', '')
    r('>Kies de modules voor deze toets<', '>Choose the modules for this test<')
    r('>Start de toets ({{ aantalVragen }} vragen)<', '>Start the test ({{ aantalVragen }} questions)<')
    r('>Alle modules<', '>All modules<')
    r('>HOERA! GESLAAGD 🎉<', '>HOORAY! YOU PASSED 🎉<')
    r('font-weight:700">Resultaat</span>', 'font-weight:700">Result</span>')
    r('<label for="naam">Naam voor op het certificaat</label>', '<label for="naam">Name on the certificate</label>')
    r('placeholder="Voor- en achternaam"', 'placeholder="First and last name"')
    r('<label for="org">Organisatie</label>', '<label for="org">Organisation</label>')
    r('placeholder="Naam van het kantoor"', 'placeholder="Name of the firm"')
    r('>Certificaat openen en printen<', '>Open and print certificate<')
    r('>Opnieuw<', '>Try again<')
    r(letop('nl'), letop('en'))
    r('aria-label="Terug naar home" title="Terug naar home"', 'aria-label="Back to home" title="Back to home"')
    # JS
    r("const HOME=PAGINA==='toets'?'../':'./';", "const HOME='../../';")
    a = x.index('const MODULES = ['); b = x.index('];', a) + 2
    x = x[:a] + 'const MODULES = ' + json.dumps([{"id": i, "naam": n, "omschr": o} for i, n, o in MODULES_EN], ensure_ascii=False) + ';' + x[b:]
    a = x.index('const VRAGEN = ['); b = x.index('\n];', a) + 3
    x = x[:a] + 'const VRAGEN = [\n' + ',\n'.join('  V(' + json.dumps(list(v), ensure_ascii=False)[1:-1] + ')' for v in VX.EN) + '\n];' + x[b:]
    r("alert('Vul een naam in voor op het certificaat.')", "alert('Please enter a name for the certificate.')")
    r("alert('Sta pop-ups toe om het certificaat te openen.')", "alert('Please allow pop-ups to open the certificate.')")
    r("datum=d.toLocaleDateString('nl-NL'", "datum=d.toLocaleDateString('en-GB'")
    r('<html lang="nl"><head><meta charset="utf-8"><title>Certificaat — ', '<html lang="en"><head><meta charset="utf-8"><title>Certificate — ')
    r('>Printen of opslaan als pdf<', '>Print or save as PDF<')
    r('>Deelnamebewijs oefentoets · ${kw}<', '>Certificate of participation · practice test · ${kw}<')
    r('<td>Datum</td>', '<td>Date</td>')
    r('<td>Resultaat</td>', '<td>Result</td>')
    r('(${s.goed} van ${s.reeks.length} goed)', '(${s.goed} of ${s.reeks.length} correct)')
    r('<td>Getoetste modules</td>', '<td>Modules tested</td>')
    r('<td>Certificaatnummer</td>', '<td>Certificate number</td>')
    r('<b>Verantwoording.</b> Deelnamebewijs van een oefentoets in het kader van AI-geletterdheid (art. 4 Verordening (EU) 2024/1689). Geen diploma, geen erkend examen en geen bewijs van naleving. Bewaar dit in het personeels- of vakbekwaamheidsdossier. AI Permanent Actueel is een activiteit van DFO BV.',
      '<b>Statement.</b> Certificate of participation in a practice test on AI literacy (Article 4 Regulation (EU) 2024/1689). Not a diploma, not a recognised exam and not proof of compliance. Keep this in your personnel or professional competence file. AI Permanent Actueel is an activity of DFO BV.')
    r("vraagMeta:`Vraag ${s.idx+1} van ${s.reeks.length} · ", "vraagMeta:`Question ${s.idx+1} of ${s.reeks.length} · ")
    r("oordeel:juist?'Goed.':'Niet juist. Het juiste antwoord is gemarkeerd.',", "oordeel:juist?'Correct.':'Incorrect. The correct answer is highlighted.',")
    r("volgLabel:s.idx+1<s.reeks.length?'Volgende vraag':'Naar het resultaat',", "volgLabel:s.idx+1<s.reeks.length?'Next question':'See result',")
    r("eindTekst:`${s.goed} van de ${s.reeks.length} vragen goed. `+(pct>=70?'Voldoende voor een deelnamebewijs.':'Minimaal 70% nodig; lees de uitleg terug en probeer het opnieuw.'),",
      "eindTekst:`${s.goed} of ${s.reeks.length} questions correct. `+(pct>=70?'Enough for a certificate of participation.':'You need at least 70%; review the explanations and try again.'),")
    r("vandaag:new Date().toLocaleDateString('nl-NL'", "vandaag:new Date().toLocaleDateString('en-GB'")
    return x

HEAD_TOETS_BASE = HEAD_TOETS
toets = sub1(HEAD_HOME, HEAD_TOETS, toets)
en_tpl = to_en(toets).replace('__FOOTER__', footer('en', '../../', './'))
toets = sub1('Vragen</a>\n    </nav>',
             'Vragen</a>\n      <a href="../en/knowledge-test/" hreflang="en" lang="en" style="color:var(--color-text);text-decoration:none">English</a>\n    </nav>', toets)
toets = toets.replace('__FOOTER__', footer('nl', '../', './'))
home = home.replace('__FOOTER__', footer('nl', '', 'kennistoets/'))
for x in (home, toets, en_tpl): assert '__FOOTER__' not in x and '__PAGINA__' not in x
# ---------- terugschrijven in de bundel ----------
def schrijf(pad, tpl):
    enc = json.dumps(tpl, ensure_ascii=False).replace('</', '<\\u002F')
    assert json.loads(enc) == tpl
    L2 = list(L); L2[381] = enc
    os.makedirs(os.path.dirname(pad), exist_ok=True)
    open(pad, 'w', encoding='utf-8').write('\n'.join(L2))
schrijf(f'{REPO}/index.html', home)
schrijf(f'{REPO}/kennistoets/index.html', toets)
schrijf(f'{REPO}/en/knowledge-test/index.html', en_tpl)
open(f'{D}/template.en.html', 'w').write(en_tpl)
open(f'{D}/seo_head_en.html', 'w').write(HEAD_EN)
open(f'{D}/template.new.html', 'w').write(home)
open(f'{D}/template.toets.html', 'w').write(toets)
json.dump(FAQ_ALL, open(f'{D}/faq_all.json', 'w'), ensure_ascii=False)
json.dump(DC, open(f'{D}/dc.json', 'w'), ensure_ascii=False)
open(f'{D}/seo_head.html', 'w').write(HEAD_HOME)
open(f'{D}/seo_head_toets.html', 'w').write(HEAD_TOETS)
print('ok', len(home), len(toets))
