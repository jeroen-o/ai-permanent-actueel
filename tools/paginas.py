"""Losse (statische) pagina's: nieuw, begrippen, wetgeving, over, register, onderwerppagina's en 404.

Elke pagina is een zelfstandig HTML-bestand zonder externe verbindingen.
Gebruik: python3 tools/paginas.py  (wordt aangeroepen door tools/bouw.sh)
"""
import html
import json
import os
import re

TOOLS = os.path.dirname(os.path.abspath(__file__))
REPO = os.environ.get('AIPA_REPO', os.path.dirname(TOOLS))
SITE = 'https://ai-permanent-actueel.nl'
DATUM = '2026-10-18'
DATUM_NL = '18 oktober 2026'


def md(t):
    """Mini-opmaak: [tekst](url) en **vet**, de rest wordt ge-escaped."""
    t = html.escape(t, quote=False)
    t = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', lambda m: f'<a href="{m.group(2)}">{m.group(1)}</a>', t)
    return re.sub(r'\*\*([^*]+)\*\*', r'<b>\1</b>', t)


def P(t): return f'<p>{md(t)}</p>'
def UL(items): return '<ul>' + ''.join(f'<li>{md(i)}</li>' for i in items) + '</ul>'
def H2(t, id=None): return f'<h2{f" id={chr(34)}{id}{chr(34)}" if id else ""}>{html.escape(t)}</h2>'
def H3(t): return f'<h3>{html.escape(t)}</h3>'
def MODEL(t): return f'<blockquote>{md(t)}</blockquote>'


# ---------------------------------------------------------------- gedeelde bronnen
BRON = {
    'ai': ('AI-verordening (Verordening (EU) 2024/1689)', 'https://eur-lex.europa.eu/eli/reg/2024/1689/oj'),
    'avg': ('Algemene verordening gegevensbescherming (Verordening (EU) 2016/679)', 'https://eur-lex.europa.eu/eli/reg/2016/679/oj'),
    'ccd2': ('Richtlijn (EU) 2023/2225 (Consumentenkredietrichtlijn)', 'https://eur-lex.europa.eu/eli/dir/2023/2225/oj'),
    'wft': ('Wet op het financieel toezicht', 'https://wetten.overheid.nl/BWBR0020368'),
    'uavg': ('Uitvoeringswet AVG', 'https://wetten.overheid.nl/BWBR0040940'),
    'bw6': ('Burgerlijk Wetboek Boek 6 (art. 6:170)', 'https://wetten.overheid.nl/BWBR0005289'),
    'ap': ('Autoriteit Persoonsgegevens', 'https://www.autoriteitpersoonsgegevens.nl/'),
    'afm': ('Autoriteit Financiële Markten (AFM)', 'https://www.afm.nl/'),
    'dnb': ('De Nederlandsche Bank (DNB)', 'https://www.dnb.nl/'),
    'rdi': ('Rijksinspectie Digitale Infrastructuur (RDI)', 'https://www.rdi.nl/'),
    'kifid': ('Klachteninstituut Financiële Dienstverlening (Kifid)', 'https://www.kifid.nl/'),
    'eu-ai': ('Europese Commissie: regelgevend kader voor AI', 'https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai'),
}

NAV = [('Home', '/'), ('Kennistoets', '/kennistoets/'), ('Klantcommunicatie', '/#klantcommunicatie'),
       ('Nieuw', '/nieuw/'), ('Begrippen', '/begrippen/'), ('Wetgeving', '/wetgeving/'), ('Register', '/register/')]

FOOT_LINKS = [('Wat is er nieuw', '/nieuw/'), ('Begrippenlijst', '/begrippen/'), ('Wet- en regelgeving', '/wetgeving/'),
              ('Register AI-geletterdheid', '/register/'), ('Over en verantwoording', '/over/'),
              ('Privacy, voorwaarden en klachten', '/privacy/')]

CSS = '''
  :root { --bg:#ffffff; --surface:#f1f6fb; --text:#16202b; --accent:#1462ad; --accent-100:#e8f1fa; --accent-700:#0e4a84; --accent-900:#082a4b; --divider:color-mix(in srgb,#16202b 30%,transparent); }
  * { box-sizing: border-box; }
  html { scroll-behavior: smooth; }
  body { margin: 0; background: var(--bg); color: var(--text); font: 16px/1.65 Arial, Helvetica, sans-serif; }
  a { color: var(--accent-700); }
  a:hover { color: var(--accent-900); }
  header { border-bottom: 2px solid var(--divider); background: var(--bg); }
  .wrap { max-width: 880px; margin: 0 auto; padding: 0 16px; }
  .kop { display: flex; align-items: center; justify-content: space-between; gap: 12px 20px; flex-wrap: wrap; padding: 14px 0; }
  .merk { font-weight: 800; font-size: 17px; color: var(--text); text-decoration: none; }
  nav { display: flex; gap: 8px 16px; flex-wrap: wrap; font-size: 14px; font-weight: 600; }
  nav a { color: var(--text); text-decoration: none; }
  nav a[aria-current] { color: var(--accent); text-decoration: underline; text-underline-offset: 4px; }
  main { padding: 36px 0 56px; }
  .lbl { font-size: 11px; letter-spacing: .1em; text-transform: uppercase; font-weight: 700; color: var(--accent-700); }
  h1 { font-size: clamp(30px, 5vw, 44px); line-height: 1.08; letter-spacing: -.02em; margin: 8px 0 14px; text-wrap: balance; }
  h2 { font-size: 24px; line-height: 1.2; margin: 40px 0 8px; padding-top: 16px; border-top: 2px solid var(--text); }
  h3 { font-size: 17px; margin: 22px 0 4px; }
  p, li { max-width: 72ch; }
  .lead { font-size: 19px; line-height: 1.55; max-width: 62ch; }
  ul { padding-left: 20px; }
  blockquote { margin: 12px 0; padding: 12px 16px; background: var(--surface); border-left: 4px solid var(--accent); max-width: 72ch; }
  .crumbs { font-size: 13px; opacity: .8; margin-bottom: 8px; }
  .toc { background: var(--surface); padding: 14px 18px; display: flex; gap: 6px 18px; flex-wrap: wrap; font-weight: 700; font-size: 14px; margin: 18px 0; }
  .klein { font-size: 13px; opacity: .75; }
  .kaart { border: 2px solid var(--text); padding: 14px 18px; margin: 14px 0; max-width: 72ch; }
  .kaart h3 { margin-top: 0; }
  .btn { display: inline-block; padding: 10px 16px; border: 2px solid var(--text); background: var(--text); color: #fff; font-weight: 700; font-size: 14px; text-decoration: none; cursor: pointer; font-family: inherit; }
  .btn.sec { background: var(--bg); color: var(--text); }
  .btn.prim { background: var(--accent); border-color: var(--accent); }
  .waarschuwing { border: 2px solid var(--accent); padding: 12px 16px; background: var(--bg); max-width: 72ch; margin: 18px 0; }
  .tijdlijn { list-style: none; padding: 0; margin: 12px 0; border-left: 3px solid var(--accent); }
  .tijdlijn li { padding: 0 0 18px 18px; position: relative; max-width: 72ch; }
  .tijdlijn li::before { content: ""; position: absolute; left: -9px; top: 6px; width: 15px; height: 15px; background: var(--bg); border: 3px solid var(--accent); border-radius: 50%; }
  .tijdlijn time { font-weight: 800; display: block; }
  dt { font-weight: 800; margin-top: 18px; scroll-margin-top: 16px; }
  dd { margin: 2px 0 0; max-width: 72ch; }
  footer { background: var(--accent-900); color: #fff; padding: 28px 0; font-size: 13px; }
  footer a { color: #fff; }
  footer ul { list-style: none; padding: 0; display: flex; flex-wrap: wrap; gap: 6px 18px; margin: 0 0 14px; }
  table { border-collapse: collapse; width: 100%; font-size: 14px; }
  th, td { text-align: left; padding: 8px 10px; border-bottom: 1px solid var(--divider); vertical-align: top; }
  th { border-bottom: 2px solid var(--text); font-size: 12px; text-transform: uppercase; letter-spacing: .06em; }
  label { font-weight: 700; font-size: 14px; display: block; margin-bottom: 2px; }
  input, select, textarea { font: inherit; padding: 8px 10px; border: 2px solid var(--divider); background: var(--bg); color: var(--text); width: 100%; }
  input:focus-visible, select:focus-visible, textarea:focus-visible, .btn:focus-visible, a:focus-visible { outline: 3px solid var(--accent); outline-offset: 2px; }
  .rij { display: grid; grid-template-columns: repeat(auto-fit, minmax(190px, 1fr)); gap: 12px; margin: 12px 0; }
  @media print { header, footer, .nodruk { display: none !important; } main { padding: 0; } }
'''


def favicons():
    return ('<link rel="icon" href="/favicon.ico" sizes="32x32">\n<link rel="icon" href="/favicon.svg" type="image/svg+xml">\n'
            '<link rel="apple-touch-icon" href="/apple-touch-icon.png">\n<link rel="manifest" href="/site.webmanifest">\n')


def layout(pad, titel, beschrijving, h1, label, body, extra_ld=None, crumb=None, robots='index, follow', sitemap=True):
    url = f'{SITE}{pad}'
    org = {"@type": "Organization", "@id": SITE + "/#dfo", "name": "DFO BV", "url": "https://www.dfobv.nl"}
    graph = [org, {"@type": "WebPage", "@id": url + '#webpage', "url": url, "name": titel, "description": beschrijving,
                   "inLanguage": "nl-NL", "isPartOf": {"@id": SITE + "/#website"}, "publisher": {"@id": SITE + "/#dfo"},
                   "dateModified": DATUM, "breadcrumb": {"@id": url + '#breadcrumb'}}]
    graph.append({"@type": "BreadcrumbList", "@id": url + '#breadcrumb', "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "AI Permanent Actueel", "item": SITE + '/'},
        {"@type": "ListItem", "position": 2, "name": crumb or h1, "item": url}]})
    graph += extra_ld or []
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False)
    nav = ''.join('<a href="%s"%s>%s</a>' % (h, ' aria-current="page"' if h == pad else '', n) for n, h in NAV)
    foot = ''.join(f'<li><a href="{h}">{n}</a></li>' for n, h in FOOT_LINKS)
    return f'''<!DOCTYPE html>
<html lang="nl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(titel)}</title>
<meta name="description" content="{html.escape(beschrijving)}">
<meta name="robots" content="{robots}, max-snippet:-1, max-image-preview:large">
<link rel="canonical" href="{url}">
{favicons()}<meta name="theme-color" content="#1462ad">
<meta property="og:type" content="article">
<meta property="og:locale" content="nl_NL">
<meta property="og:site_name" content="AI Permanent Actueel">
<meta property="og:title" content="{html.escape(titel)}">
<meta property="og:description" content="{html.escape(beschrijving)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/og-image.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{html.escape(titel)}">
<meta name="twitter:description" content="{html.escape(beschrijving)}">
<meta name="twitter:image" content="{SITE}/og-image.png">
<script type="application/ld+json">{ld}</script>
<style>{CSS}</style>
</head>
<body>
<header>
  <div class="wrap kop">
    <a class="merk" href="/">AI Permanent Actueel</a>
    <nav aria-label="Hoofdnavigatie">{nav}</nav>
  </div>
</header>
<main class="wrap">
  <div class="crumbs"><a href="/">AI Permanent Actueel</a> › {html.escape(crumb or h1)}</div>
  <span class="lbl">{html.escape(label)}</span>
  <h1>{html.escape(h1)}</h1>
{body}
  <p class="klein">Laatst bijgewerkt: {DATUM_NL}. Hulpmiddel voor het gesprek met compliance, geen juridisch advies.</p>
</main>
<footer>
  <div class="wrap">
    <ul>{foot}</ul>
    <div>© 2026 DFO BV. AI Permanent Actueel is een activiteit van DFO BV. · De Wel 14–16, 3871 MV Hoevelaken · <a href="tel:+31332580460">033 258 04 60</a> · <a href="mailto:info@dfobv.nl">info@dfobv.nl</a></div>
  </div>
</footer>
</body>
</html>
'''


def faq_ld(url, vragen):
    return [{"@type": "FAQPage", "@id": url + '#faq', "inLanguage": "nl-NL", "mainEntity": [
        {"@type": "Question", "name": v, "acceptedAnswer": {"@type": "Answer", "text": a}} for v, a in vragen]}]


def faq_html(vragen):
    return H2('Veelgestelde vragen') + ''.join(H3(v) + P(a) for v, a in vragen)


def zie_ook(links):
    return H2('Zie ook') + UL([f'[{n}]({h})' for n, h in links])


DISCLAIMER = ('Deze pagina is een hulpmiddel voor het gesprek met compliance of een jurist en geen juridisch advies. '
              'Regels wijzigen: controleer de actuele stand in de bronnen op [Wet- en regelgeving](/wetgeving/).')

PAGINAS = []   # (pad, titel, omschrijving, prioriteit) voor sitemap en llms.txt


def schrijf(pad, *args, prio='0.6', **kw):
    inhoud = layout(pad, *args, **kw)
    bestand = os.path.join(REPO, pad.strip('/'), 'index.html') if pad != '/404.html' else os.path.join(REPO, '404.html')
    os.makedirs(os.path.dirname(bestand), exist_ok=True)
    open(bestand, 'w', encoding='utf-8').write(inhoud)
    if kw.get('sitemap', True) and pad != '/404.html':
        PAGINAS.append((pad, args[0], args[1], prio))


# ================================================================ NIEUW
def pagina_nieuw():
    items = [
        ('2026-11-20', '20 november 2026', 'Herziene Consumentenkredietrichtlijn van toepassing',
         'Richtlijn (EU) 2023/2225 wordt van toepassing. Bij een geautomatiseerde kredietwaardigheidsbeoordeling heeft de consument recht op menselijke tussenkomst, een uitleg van de beoordeling en op het geven van zijn standpunt. **Controleer de stand van de Nederlandse implementatie.** Zie [AI bij kredietadvies](/ai-kredietadvies-geautomatiseerde-beoordeling/).'),
        ('2026-10-18', 'Oktober 2026', 'Controleer de actuele stand van de AI-verordening',
         'De Europese Commissie heeft met het Digital Omnibus-voorstel (november 2025) voorgesteld om onder meer termijnen voor hoog-risico-AI uit te stellen. Ook aanpassingen aan de invulling van artikel 4 zijn onderdeel van die discussie. Wij hebben niet kunnen vaststellen wat er op dit moment definitief is besloten. **Controleer de actuele stand voordat je beleid of klantteksten aanpast**, en zie [Wet- en regelgeving](/wetgeving/).'),
        ('2026-08-02', '2 augustus 2026', 'Transparantieverplichtingen (artikel 50) en groot deel van de verordening van toepassing',
         'Volgens de oorspronkelijke planning geldt vanaf deze datum het grootste deel van de AI-verordening, waaronder de transparantieverplichtingen van artikel 50 (chatbots, deepfakes, AI-gegenereerde tekst over zaken van algemeen belang). Voor hoog-risicosystemen uit bijlage III, zoals kredietwaardigheidsbeoordeling van particulieren, kan uitstel gelden. Zie [AI-chatbot melden aan de klant](/ai-chatbot-melden-aan-klant/).'),
        ('2025-08-02', '2 augustus 2025', 'Regels voor AI-modellen voor algemene doeleinden',
         'De verplichtingen voor aanbieders van AI-modellen voor algemene doeleinden (de grote taalmodellen) en het bestuursmodel van de verordening gaan in. Voor een advieskantoor als gebruiker is dit vooral relevant bij de keuze van een leverancier: vraag naar de afspraken over gegevensgebruik en transparantie.'),
        ('2025-02-27', '27 februari 2025', 'Hof van Justitie: uitleg over de logica van geautomatiseerde besluiten',
         'In de zaak Dun & Bradstreet Austria (C-203/22) oordeelde het Hof dat een betrokkene bij een geautomatiseerd besluit recht heeft op een begrijpelijke uitleg van de gevolgde procedure en beginselen, en dat bedrijfsgeheim dat niet zonder meer kan tegenhouden. Relevant voor acceptatie- en kredietbeslissingen.'),
        ('2025-02-02', '2 februari 2025', 'AI-geletterdheid (artikel 4) en verboden AI-praktijken van toepassing',
         'Organisaties die AI inzetten moeten maatregelen nemen voor AI-geletterdheid van hun medewerkers. Tegelijk gelden de verboden praktijken uit artikel 5. Zie [Artikel 4: AI-geletterdheid](/artikel-4-ai-geletterdheid/).'),
        ('2023-12-07', '7 december 2023', 'Hof van Justitie: kredietscore kan zelf een geautomatiseerd besluit zijn',
         'In de SCHUFA-zaak (C-634/21) oordeelde het Hof dat het opstellen van een kredietscore al een geautomatiseerd besluit in de zin van artikel 22 AVG kan zijn, als de uitkomst bepalend is voor het besluit van de kredietverstrekker. Relevant voor kantoren en volmachtbedrijven die scores of AI-beoordelingen gebruiken.'),
    ]
    tijd = '<ol class="tijdlijn">' + ''.join(
        f'<li><time datetime="{d}">{n}</time><b>{html.escape(t)}</b><br>{md(x)}</li>' for d, n, t, x in items) + '</ol>'
    body = (P('Wat verandert er in regels en rechtspraak rond AI, en wat betekent dat voor een advieskantoor of volmachtbedrijf? Op deze pagina staan de updates en de tijdlijn. De nieuwste staat bovenaan.') +
            '<div class="waarschuwing"><b>Let op.</b> Dit overzicht geeft de stand van oktober 2026 voor zover ons bekend. Termijnen en inhoud van Europese regels kunnen nog wijzigen. Controleer altijd de bron.</div>' +
            H2('Update oktober 2026: wat betekent dit voor je kantoor?') +
            UL(['**Beleid:** leg vast dat je de actuele stand van de AI-verordening controleert, bijvoorbeeld bij elke jaarlijkse evaluatie van je AI-beleid.',
                '**Klantteksten:** meld AI-gebruik in privacyverklaring en dienstverleningsdocument; de modelteksten staan bij [Klantcommunicatie](/#klantcommunicatie).',
                '**Krediet:** bereid je voor op de herziene Consumentenkredietrichtlijn per 20 november 2026 en leg vast hoe de klant menselijke tussenkomst kan vragen.',
                '**Volmacht:** controleer in de volmachtovereenkomst welk AI-gebruik bij acceptatie, premie en schade is toegestaan.']) +
            H2('Tijdlijn') + tijd +
            H2('Meer weten?') + UL(['Doe de [kennistoets](/kennistoets/) en bewaar het deelnamebewijs in je personeelsdossier.',
                                    'Bekijk de [begrippenlijst](/begrippen/) en de bronnen onder [Wet- en regelgeving](/wetgeving/).']))
    ld = [{"@type": "ItemList", "@id": SITE + '/nieuw/#lijst', "name": "Tijdlijn AI-regelgeving en rechtspraak", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": f'{n}: {t}'} for i, (d, n, t, x) in enumerate(items)]}]
    schrijf('/nieuw/', 'Wat is er nieuw in AI-regelgeving voor financieel dienstverleners | AI Permanent Actueel',
            'Tijdlijn en updates over de AI-verordening, AVG en rechtspraak voor hypotheek-, assurantie- en kredietadviseurs en volmachtbedrijven.',
            'Wat is er nieuw?', 'Updates', body, ld, crumb='Wat is er nieuw', prio='0.8')


# ================================================================ BEGRIPPEN
TERMEN = [
    ('AI-agent', 'Een AI-systeem dat zelfstandig stappen uitvoert, zoals mails versturen of systemen raadplegen. Hoe meer een systeem zelf doet, hoe belangrijker menselijk toezicht en duidelijke grenzen zijn.'),
    ('AI-geletterdheid', 'De kennis, vaardigheden en het begrip waarmee mensen AI-systemen verantwoord kunnen gebruiken en de kansen en risico’s ervan kunnen beoordelen. Artikel 4 van de AI-verordening vraagt organisaties maatregelen te nemen om dit voor hun medewerkers te waarborgen. Zie [Artikel 4](/artikel-4-ai-geletterdheid/).'),
    ('AI-systeem', 'Een machinegebaseerd systeem dat uit de ontvangen invoer afleidt hoe het uitvoer, zoals voorspellingen, teksten, aanbevelingen of beslissingen, genereert. Zo is de term gedefinieerd in de AI-verordening.'),
    ('Aanbieder', 'In de AI-verordening: wie een AI-systeem ontwikkelt of laat ontwikkelen en het onder eigen naam of merk op de markt brengt of in gebruik stelt. Een kantoor dat een chatbot onder eigen naam aanbiedt, kan zelf aanbieder zijn.'),
    ('Anonimiseren', 'Gegevens zo bewerken dat een persoon niet meer te identificeren is. Geanonimiseerde gegevens vallen buiten de AVG. Zie ook pseudonimiseren.'),
    ('Automation bias', 'De neiging om de uitkomst van een systeem te vertrouwen zonder die kritisch te controleren. Menselijk toezicht werkt alleen als de controleur ook echt durft af te wijken.'),
    ('AVG', 'De Algemene verordening gegevensbescherming (Verordening (EU) 2016/679). Regelt de verwerking van persoonsgegevens, ook als een AI-tool die verwerkt.'),
    ('Bias', 'Systematische scheefheid in de uitkomsten van een systeem, bijvoorbeeld doordat trainingsdata bestaande vooroordelen bevatten. Kan leiden tot ongelijke behandeling van groepen klanten.'),
    ('Dataminimalisatie', 'Alleen de persoonsgegevens verwerken die nodig zijn voor het doel. Bij AI-tools: voer niet meer in dan nodig en anonimiseer of pseudonimiseer waar dat kan.'),
    ('Datalek', 'Een inbreuk op de beveiliging waarbij persoonsgegevens per ongeluk of onrechtmatig worden vernietigd, verloren, gewijzigd of verstrekt. Een datalek met risico voor betrokkenen meld je binnen 72 uur bij de Autoriteit Persoonsgegevens (AVG art. 33).'),
    ('Deepfake', 'Door AI gemaakte of bewerkte beelden, geluid of video die echt lijken. Voor gebruikers geldt een transparantieplicht (AI-verordening art. 50). Ook een risico bij fraude, zoals een nagemaakte stem van een directeur.'),
    ('Dienstverleningsdocument (DVD)', 'Het document waarmee een adviseur de klant informeert over zijn dienstverlening, werkwijze en beloning. Een goede plek om kort te melden dat AI-hulpmiddelen worden gebruikt en dat de adviseur zelf adviseert.'),
    ('DPIA', 'Gegevensbeschermingseffectbeoordeling: een beoordeling vooraf van de privacyrisico’s van een verwerking, verplicht bij waarschijnlijk hoog risico, bijvoorbeeld bij nieuwe technologie en grootschalige verwerking van financiële gegevens (AVG art. 35).'),
    ('EER', 'Europese Economische Ruimte: de EU-landen plus IJsland, Liechtenstein en Noorwegen. Voor doorgifte van persoonsgegevens buiten de EER is een geldige basis nodig.'),
    ('Generatieve AI', 'AI die nieuwe inhoud maakt, zoals tekst, beeld of geluid, op basis van patronen in trainingsdata.'),
    ('Geautomatiseerd besluit', 'Een besluit dat uitsluitend door geautomatiseerde verwerking tot stand komt en rechtsgevolgen of een vergelijkbaar aanmerkelijk effect heeft voor de klant. De klant heeft dan onder meer recht op menselijke tussenkomst en uitleg (AVG art. 22).'),
    ('Gebruiksverantwoordelijke', 'In de AI-verordening: wie een AI-systeem onder eigen verantwoordelijkheid gebruikt. Een advieskantoor dat een AI-tool inzet, is meestal gebruiksverantwoordelijke en heeft eigen verplichtingen, zoals AI-geletterdheid.'),
    ('Hallucinatie', 'Een vloeiend geformuleerd maar feitelijk onjuist of verzonnen antwoord van een AI-model, zoals verzonnen bronnen, bedragen of wetsartikelen.'),
    ('Hoog-risico-AI', 'AI-systemen die de AI-verordening om hun risico voor gezondheid, veiligheid of grondrechten zwaarder reguleert. In de financiële sector onder meer AI die de kredietwaardigheid van particulieren beoordeelt en AI voor risicobeoordeling en prijsstelling bij levens- en ziektekostenverzekeringen (bijlage III). De ingangsdatum is mogelijk uitgesteld: controleer de actuele stand.'),
    ('Kifid', 'Klachteninstituut Financiële Dienstverlening: het geschilleninstituut waar consumenten terechtkunnen met klachten over financiële dienstverleners.'),
    ('Menselijk toezicht', 'Een bekwame medewerker beoordeelt de uitkomst van een AI-systeem en kan die corrigeren of terzijde schuiven. Het toezicht moet echt zijn: met kennis, tijd en de bevoegdheid om af te wijken.'),
    ('Prompt', 'De instructie of vraag die je aan een AI-model geeft. Hoe preciezer, hoe bruikbaarder de output, maar ook een goede prompt garandeert geen juistheid.'),
    ('Pseudonimiseren', 'Persoonsgegevens zo bewerken dat ze zonder aanvullende informatie niet aan een persoon zijn te koppelen. Pseudonieme gegevens blijven persoonsgegevens.'),
    ('Shadow AI', 'AI-tools die medewerkers gebruiken buiten het goedgekeurde aanbod, zonder zicht van de organisatie. Een van de grootste praktische risico’s, omdat er geen afspraken, geen zicht en geen vastlegging zijn.'),
    ('Taalmodel (LLM)', 'Een AI-model dat getraind is op grote hoeveelheden tekst en op basis van waarschijnlijkheid het meest passende vervolg op een tekst voorspelt. Daardoor klinkt de uitvoer overtuigend, ook als die niet klopt.'),
    ('Trainingsdata', 'De grote hoeveelheid tekst en gegevens waarmee een AI-model is ontwikkeld. Afhankelijk van de voorwaarden kunnen door jou ingevoerde gegevens gebruikt worden om modellen verder te trainen.'),
    ('Transparantieplicht', 'De plicht om mensen te informeren dat zij met AI te maken hebben of dat inhoud door AI is gegenereerd (AI-verordening art. 50).'),
    ('Verwerker', 'Een partij die in opdracht van jou persoonsgegevens verwerkt, zoals een AI-leverancier. Voor een verwerker is een verwerkersovereenkomst nodig (AVG art. 28).'),
    ('Verwerkersovereenkomst', 'Een overeenkomst met een verwerker over wat die met persoonsgegevens mag doen, hoe ze worden beveiligd en wanneer ze worden verwijderd. Zonder deze overeenkomst laat je geen klantgegevens verwerken door een AI-dienst.'),
    ('Volmachtbedrijf', 'Een tussenpersoon die namens een verzekeraar bevoegd is besluiten te nemen over acceptatie, premie of schade. Daardoor raakt AI hier snel aan geautomatiseerde besluitvorming. Zie [AI voor volmachtbedrijven](/ai-voor-volmachtbedrijven/).'),
    ('Zorgplicht', 'De verplichting van een financieel dienstverlener om in het belang van de klant te handelen (Wft art. 4:24a en volgende). De adviseur blijft verantwoordelijk voor het advies, ook als AI heeft geholpen.'),
]


def slug(t):
    return re.sub(r'[^a-z0-9]+', '-', t.lower().replace('é', 'e')).strip('-')


def pagina_begrippen():
    termen = sorted(TERMEN, key=lambda x: x[0].lower())
    letters = sorted({t[0][0].upper() for t in termen})
    toc = '<div class="toc" aria-label="Snel naar letter">' + ''.join(
        f'<a href="#letter-{l.lower()}">{l}</a>' for l in letters) + '</div>'
    body = P('Wat betekenen begrippen als hallucinatie, gebruiksverantwoordelijke en DPIA? Hieronder staan de belangrijkste begrippen uit de AI-verordening, de AVG en het dagelijks werk met AI, kort en praktisch uitgelegd voor financieel dienstverleners.') + toc
    huidige = None
    delen = []
    for n, d in termen:
        l = n[0].upper()
        if l != huidige:
            if huidige: delen.append('</dl>')
            delen.append(f'<h2 id="letter-{l.lower()}">{l}</h2><dl>')
            huidige = l
        delen.append(f'<dt id="{slug(n)}">{html.escape(n)}</dt><dd>{md(d)}</dd>')
    delen.append('</dl>')
    body += ''.join(delen) + zie_ook([('Wet- en regelgeving', '/wetgeving/'), ('Kennistoets', '/kennistoets/')])
    ld = [{"@type": "DefinedTermSet", "@id": SITE + '/begrippen/#set', "name": "Begrippenlijst AI voor financieel dienstverleners", "inLanguage": "nl-NL",
           "hasDefinedTerm": [{"@type": "DefinedTerm", "name": n, "description": re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', d), "url": f'{SITE}/begrippen/#{slug(n)}'} for n, d in termen]}]
    schrijf('/begrippen/', 'Begrippenlijst AI voor financieel dienstverleners | AI Permanent Actueel',
            'Wat is een hallucinatie, gebruiksverantwoordelijke, DPIA of shadow AI? Begrippen uit de AI-verordening en AVG uitgelegd voor adviseurs en volmachtbedrijven.',
            'Begrippenlijst AI', 'Kennis', body, ld, crumb='Begrippenlijst', prio='0.7')


# ================================================================ WETGEVING
def pagina_wetgeving():
    def l(k, toelichting=''):
        n, u = BRON[k]
        return f'[{n}]({u})' + (f': {toelichting}' if toelichting else '')
    body = (P('Waar staat het precies? Hieronder staan de officiële bronnen achter de uitleg op deze site. Controleer bij twijfel altijd de actuele wettekst.') +
            '<div class="toc"><a href="#ai-verordening">AI-verordening</a><a href="#avg">AVG</a><a href="#wft">Wft en zorgplicht</a><a href="#krediet">Krediet</a><a href="#aansprakelijkheid">Aansprakelijkheid</a><a href="#toezicht">Toezichthouders</a></div>' +
            H2('AI-verordening', 'ai-verordening') +
            UL([l('ai', 'artikel 4 (AI-geletterdheid), artikel 5 (verboden praktijken), artikel 26 (verplichtingen van gebruiksverantwoordelijken), artikel 50 (transparantie) en bijlage III (hoog-risico)'),
                l('eu-ai', 'achtergrond, richtsnoeren en actuele ontwikkelingen')]) +
            P('Let op: met het Digital Omnibus-voorstel zijn wijzigingen voorgesteld, onder meer aan termijnen. Controleer de actuele stand. Zie [Wat is er nieuw](/nieuw/).') +
            H2('Privacy en AVG', 'avg') +
            UL([l('avg', 'artikel 13 en 14 (informatieplicht), 22 (geautomatiseerde besluiten), 28 (verwerker), 33 (datalek), 35 (DPIA) en hoofdstuk V (doorgifte)'),
                l('uavg'), l('ap', 'toezichthouder en richtsnoeren')]) +
            H2('Wft en zorgplicht', 'wft') +
            UL([l('wft', 'onder meer artikel 4:19 (informatie aan de klant) en 4:24a (zorgplicht)'), l('afm', 'toezicht op gedrag en klantbelang'), l('dnb', 'toezicht op soliditeit en beheerste bedrijfsvoering')]) +
            H2('Krediet', 'krediet') +
            UL([l('ccd2', 'artikel 18: beoordeling van de kredietwaardigheid, ook bij geautomatiseerde verwerking; van toepassing vanaf 20 november 2026'),
                '**Hof van Justitie, SCHUFA (C-634/21, 7 december 2023):** een kredietscore kan zelf een geautomatiseerd besluit zijn.',
                '**Hof van Justitie, Dun & Bradstreet Austria (C-203/22, 27 februari 2025):** recht op uitleg van de logica van een geautomatiseerd besluit.']) +
            P('Zoek uitspraken van het Hof van Justitie op [curia.europa.eu](https://curia.europa.eu/) via het zaaknummer.') +
            H2('Aansprakelijkheid', 'aansprakelijkheid') +
            UL([l('bw6', 'artikel 6:170: aansprakelijkheid van de werkgever voor fouten van ondergeschikten'), l('kifid', 'geschillen tussen consumenten en financiële dienstverleners')]) +
            H2('Toezichthouders', 'toezicht') +
            UL([l('ap'), l('rdi'), l('afm'), l('dnb'), l('kifid')]) +
            P('Voor financiële ondernemingen gelden naast de AI-verordening de Wft-regels voor zorgplicht en beheerste bedrijfsvoering. In Nederland houden onder meer de Autoriteit Persoonsgegevens en de RDI toezicht op de AI-verordening; AFM en DNB kijken mee via hun eigen toezicht.') +
            zie_ook([('Begrippenlijst', '/begrippen/'), ('Wat is er nieuw', '/nieuw/'), ('Kennistoets', '/kennistoets/')]))
    schrijf('/wetgeving/', 'Wet- en regelgeving AI voor financieel dienstverleners | AI Permanent Actueel',
            'Links naar de AI-verordening, AVG, Wft, de Consumentenkredietrichtlijn en de toezichthouders, met de artikelen die voor adviseurs en volmachtbedrijven relevant zijn.',
            'Wet- en regelgeving', 'Bronnen', body, crumb='Wet- en regelgeving', prio='0.7')


# ================================================================ OVER
def pagina_over():
    body = (P('AI Permanent Actueel helpt medewerkers van financieel dienstverleners hun kennis over AI actueel te houden en aantoonbaar te maken. De site is een activiteit van DFO BV in Hoevelaken, het bedrijf achter onder meer Wft Permanent Actueel.') +
            H2('Voor wie') +
            P('Voor medewerkers van hypotheek-, assurantie- en kredietadvieskantoren en volmachtbedrijven: adviseurs, binnendienst, management, marketing, HR en IT, inclusief ingehuurd personeel dat namens het kantoor AI gebruikt.') +
            H2('Wat je hier vindt') +
            UL(['Een gratis [kennistoets](/kennistoets/) met uitleg bij elk antwoord en een deelnamebewijs.', 'Praktische hulp bij [klantcommunicatie](/#klantcommunicatie) als je AI gebruikt, met modelteksten.',
                'Een [register](/register/) om per medewerker vast te leggen dat de AI-geletterdheid is bijgehouden.', 'Een [begrippenlijst](/begrippen/), [updates](/nieuw/) en de bronnen onder [Wet- en regelgeving](/wetgeving/).']) +
            H2('Zo is de inhoud tot stand gekomen') +
            P('De teksten, vragen en modelteksten zijn samengesteld met hulp van AI-hulpmiddelen, op basis van de AI-verordening, de AVG, de Wft en openbare rechtspraak. De bronnen staan op de pagina [Wet- en regelgeving](/wetgeving/). Controleer bij twijfel altijd de wettekst en laat eigen beleid en klantteksten toetsen door compliance of een jurist.') +
            H2('Grenzen') +
            UL(['De kennistoets is een oefentoets. Het certificaat is een deelnamebewijs: geen diploma, geen erkend examen en geen bewijs dat een organisatie aan de AI-verordening voldoet.',
                'De site geeft geen juridisch advies. Regels wijzigen en sommige termijnen zijn nog niet definitief; zie [Wat is er nieuw](/nieuw/).']) +
            H2('Fouten melden') +
            P('Zie je een fout in een vraag of tekst, of mis je een onderwerp? Mail naar [info@dfobv.nl](mailto:info@dfobv.nl). Hoe we met gegevens omgaan staat bij [Privacy, voorwaarden en klachten](/privacy/).') +
            H2('Contact') +
            P('DFO BV, De Wel 14–16, 3871 MV Hoevelaken · [033 258 04 60](tel:+31332580460) · [info@dfobv.nl](mailto:info@dfobv.nl) · KvK 32068727 · btw NL806480828B01'))
    schrijf('/over/', 'Over en verantwoording | AI Permanent Actueel',
            'Wie achter AI Permanent Actueel zit, voor wie het is, hoe de inhoud tot stand kwam en wat de grenzen zijn. Een activiteit van DFO BV.',
            'Over en verantwoording', 'Over deze site', body, crumb='Over en verantwoording', prio='0.4')


# ================================================================ REGISTER
REGISTER_BODY = '''
  <p class="lead">Leg per medewerker vast dat de AI-geletterdheid is bijgehouden: wie, welke modules, wanneer de toets is gedaan en wat de uitkomst was. Handig als onderdeel van het dossier waarmee je de inspanning voor artikel 4 aantoont.</p>
  <div class="waarschuwing"><b>Er wordt niets opgeslagen.</b> De gegevens blijven in dit browservenster en verdwijnen als je de pagina sluit. Download daarom het bestand (CSV) of print het register, en bewaar het in je personeelsdossier. Het is jouw register: DFO ontvangt geen gegevens.</div>
  <form id="regform" class="nodruk" autocomplete="off">
    <div class="rij">
      <div><label for="r-naam">Naam medewerker</label><input id="r-naam" required></div>
      <div><label for="r-rol">Functie of rol</label><input id="r-rol" placeholder="Bijv. adviseur, binnendienst"></div>
      <div><label for="r-mods">Modules</label><input id="r-mods" placeholder="Bijv. 1, 2, 3, 4, 5, 6, 7"></div>
    </div>
    <div class="rij">
      <div><label for="r-datum">Datum toets</label><input id="r-datum" type="date"></div>
      <div><label for="r-score">Score (%)</label><input id="r-score" type="number" min="0" max="100" inputmode="numeric"></div>
      <div><label for="r-cert">Certificaatnummer</label><input id="r-cert" placeholder="AIPA-…"></div>
    </div>
    <div class="rij"><div><label for="r-opm">Opmerking</label><input id="r-opm" placeholder="Bijv. ingehuurd, vervolgtraining gepland"></div></div>
    <button class="btn prim" type="submit">Toevoegen aan het register</button>
  </form>
  <h2>Register</h2>
  <p class="klein" id="r-leeg">Nog geen medewerkers toegevoegd.</p>
  <div style="overflow-x:auto"><table id="r-tabel" hidden>
    <thead><tr><th>Naam</th><th>Rol</th><th>Modules</th><th>Datum</th><th>Score</th><th>Certificaat</th><th>Opmerking</th><th class="nodruk"><span class="sr">Verwijderen</span></th></tr></thead>
    <tbody></tbody>
  </table></div>
  <p class="nodruk" style="margin-top:16px;display:flex;gap:10px;flex-wrap:wrap">
    <button class="btn" type="button" id="r-csv">Download als CSV</button>
    <button class="btn sec" type="button" id="r-print">Printen</button>
    <button class="btn sec" type="button" id="r-wis">Alles wissen</button>
  </p>
  <p class="klein">Tip: houd per kwartaal een nieuwe regel bij per medewerker, zodat het ritme zichtbaar blijft. Bewaar het register volgens je eigen bewaarbeleid; het bevat persoonsgegevens van medewerkers.</p>
  <style>.sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)} td button{font:inherit;cursor:pointer;border:0;background:none;color:var(--accent-700);text-decoration:underline}</style>
  <script>
  (function(){
    var rijen=[], tb=document.querySelector('#r-tabel tbody'), tabel=document.getElementById('r-tabel'), leeg=document.getElementById('r-leeg');
    var veld=['naam','rol','mods','datum','score','cert','opm'];
    function esc(t){ return String(t).replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c];}); }
    function datumNL(d){ if(!d) return ''; var p=d.split('-'); return p.length===3?p[2]+'-'+p[1]+'-'+p[0]:d; }
    function teken(){
      tb.innerHTML=rijen.map(function(r,i){ return '<tr><td>'+esc(r.naam)+'</td><td>'+esc(r.rol)+'</td><td>'+esc(r.mods)+'</td><td>'+esc(datumNL(r.datum))+'</td><td>'+esc(r.score?r.score+'%':'')+'</td><td>'+esc(r.cert)+'</td><td>'+esc(r.opm)+'</td><td class="nodruk"><button type="button" data-i="'+i+'" aria-label="Verwijder '+esc(r.naam)+'">Verwijder</button></td></tr>'; }).join('');
      tabel.hidden=!rijen.length; leeg.hidden=!!rijen.length;
    }
    document.getElementById('regform').addEventListener('submit',function(e){ e.preventDefault(); var r={}; veld.forEach(function(v){ r[v]=document.getElementById('r-'+v).value.trim(); });
      if(!r.naam) return; rijen.push(r); teken(); e.target.reset(); document.getElementById('r-naam').focus(); });
    tb.addEventListener('click',function(e){ var i=e.target.getAttribute('data-i'); if(i===null) return; rijen.splice(+i,1); teken(); });
    document.getElementById('r-wis').addEventListener('click',function(){ if(rijen.length&&confirm('Alle regels uit het register wissen?')){ rijen=[]; teken(); } });
    document.getElementById('r-csv').addEventListener('click',function(){
      if(!rijen.length){ alert('Het register is leeg.'); return; }
      var kop=['Naam','Rol','Modules','Datum toets','Score (%)','Certificaatnummer','Opmerking'];
      function cel(t){ t=String(t||''); if(/^[=+\\-@\\t\\r]/.test(t)) t="'"+t; return '"'+t.replace(/"/g,'""')+'"'; }
      var csv='\\ufeff'+kop.map(cel).join(';')+'\\r\\n'+rijen.map(function(r){ return [r.naam,r.rol,r.mods,datumNL(r.datum),r.score,r.cert,r.opm].map(cel).join(';'); }).join('\\r\\n');
      var u=URL.createObjectURL(new Blob([csv],{type:'text/csv;charset=utf-8'})), a=document.createElement('a');
      a.href=u; a.download='register-ai-geletterdheid.csv'; document.body.appendChild(a); a.click(); a.remove(); setTimeout(function(){URL.revokeObjectURL(u);},1000);
    });
    document.getElementById('r-print').addEventListener('click',function(){
      if(!rijen.length){ alert('Het register is leeg.'); return; }
      var w=window.open('','_blank'); if(!w){ alert('Sta pop-ups toe om het register te printen.'); return; }
      var d=new Date().toLocaleDateString('nl-NL',{day:'numeric',month:'long',year:'numeric'});
      w.document.write('<!DOCTYPE html><html lang="nl"><head><meta charset="utf-8"><title>Register AI-geletterdheid</title><style>@page{size:A4 landscape;margin:12mm}body{font:13px/1.45 Arial,Helvetica,sans-serif;color:#16202b}h1{font-size:20px;margin:0 0 4px}table{border-collapse:collapse;width:100%;margin-top:12px}th,td{text-align:left;padding:6px 8px;border-bottom:1px solid #999;vertical-align:top}th{border-bottom:2px solid #16202b;font-size:11px;text-transform:uppercase}.p{margin-bottom:12px}@media print{.p{display:none}}</style></head><body><div class="p"><button onclick="print()">Printen of opslaan als pdf</button></div><h1>Register AI-geletterdheid</h1><div>Afgedrukt op '+esc(d)+' · AI Permanent Actueel (ai-permanent-actueel.nl) · artikel 4 Verordening (EU) 2024/1689</div><table><thead><tr><th>Naam</th><th>Rol</th><th>Modules</th><th>Datum</th><th>Score</th><th>Certificaat</th><th>Opmerking</th></tr></thead><tbody>'+
        rijen.map(function(r){ return '<tr><td>'+esc(r.naam)+'</td><td>'+esc(r.rol)+'</td><td>'+esc(r.mods)+'</td><td>'+esc(datumNL(r.datum))+'</td><td>'+esc(r.score?r.score+'%':'')+'</td><td>'+esc(r.cert)+'</td><td>'+esc(r.opm)+'</td></tr>'; }).join('')+'</tbody></table></body></html>');
      w.document.close();
    });
    window.addEventListener('beforeunload',function(e){ if(rijen.length){ e.preventDefault(); e.returnValue=''; } });
  })();
  </script>
'''


def pagina_register():
    body = REGISTER_BODY + zie_ook([('Kennistoets', '/kennistoets/'), ('Artikel 4: AI-geletterdheid aantoonbaar maken', '/artikel-4-ai-geletterdheid/#aantonen')])
    schrijf('/register/', 'Register AI-geletterdheid per medewerker | AI Permanent Actueel',
            'Hulpmiddel om per medewerker vast te leggen dat de AI-geletterdheid is bijgehouden: modules, toetsdatum, score en certificaatnummer. Er wordt niets opgeslagen.',
            'Register AI-geletterdheid', 'Voor de werkgever', body, crumb='Register', prio='0.6')


# ================================================================ ONDERWERPPAGINA'S
CHECKLIST = [
    ('AI-policy vastgesteld', 'Toegestane tools, welke gegevens er niet in gaan, wie controleert, hoe je vastlegt.'),
    ('AI-gebruik per rol in kaart', 'Per functiegroep beschreven welk AI-gebruik er is en welk risico daarbij hoort.'),
    ('Modulepakket toegewezen', 'Elke medewerker heeft een pakket dat past bij rol en risico.'),
    ('Instructie aantoonbaar aangeboden', 'Verzendlijst of intranetarchief met datum per update.'),
    ('Kwartaaltoets afgenomen', 'Deelname en resultaat per medewerker geregistreerd, bijvoorbeeld in het [register](/register/).'),
    ('Certificaten in het personeelsdossier', 'Per medewerker bewaard, met datum en getoetste modules.'),
    ('Ingehuurd personeel meegenomen', 'Ook wie namens de organisatie AI gebruikt valt eronder.'),
    ('Verwerkersovereenkomsten op orde', 'Voor elke AI-leverancier die in opdracht persoonsgegevens verwerkt.'),
]


def onderwerp(pad, titel, desc, h1, label, lead, secties, faq, links, prio='0.8'):
    body = f'<p class="lead">{md(lead)}</p>' + ''.join(secties) + faq_html(faq) + zie_ook(links) + f'<p class="klein">{md(DISCLAIMER)}</p>'
    schrijf(pad, titel, desc, h1, label, body, faq_ld(f'{SITE}{pad}', faq), crumb=h1, prio=prio)


def pagina_onderwerpen():
    # --- artikel 4
    onderwerp('/artikel-4-ai-geletterdheid/', 'Artikel 4 AI-verordening: AI-geletterdheid voor financieel dienstverleners | AI Permanent Actueel',
              'Wat artikel 4 van de AI-verordening vraagt, voor wie het geldt en hoe een advieskantoor of volmachtbedrijf de AI-geletterdheid van medewerkers aantoonbaar maakt.',
              'Artikel 4 AI-verordening: AI-geletterdheid', 'Onderwerp',
              'Artikel 4 van de AI-verordening verplicht organisaties die AI inzetten om, naar beste vermogen, te zorgen voor een toereikend niveau van AI-geletterdheid van hun medewerkers en andere personen die namens hen met AI werken. De verplichting geldt sinds 2 februari 2025 en is een inspanningsverplichting: je moet kunnen laten zien wat je hebt gedaan.',
              [H2('Wat zegt artikel 4?') + P('Aanbieders en gebruiksverantwoordelijken nemen maatregelen om de AI-geletterdheid van hun personeel te waarborgen, rekening houdend met kennis, ervaring, opleiding en training van de betrokkenen, de context waarin AI wordt gebruikt en de mensen op wie het wordt toegepast. De verordening noemt **geen verplicht certificaat of examen** en geen vaste inhoud.'),
               H2('Voor wie geldt het?') + UL(['Elke organisatie die AI inzet, ook een advieskantoor met een paar medewerkers.', 'Alle medewerkers die met AI werken: adviseurs, binnendienst, management, marketing, HR en IT.', 'Ingehuurd personeel, uitzendkrachten en anderen die namens het kantoor AI gebruiken.']),
               H2('Hoe diep moet het gaan?') + P('Afgestemd op rol, risico en intensiteit van het AI-gebruik. Een adviseur die AI gebruikt voor gespreksverslagen heeft andere kennis nodig dan een medewerker die alleen mails laat samenvatten. De [pakket-check](/#pakket) helpt bij die keuze.'),
               H2('Zo toon je het aan', 'aantonen') + P('Een vast ritme met vastlegging werkt beter dan één training per jaar. Denk aan:') + '<ul>' + ''.join(f'<li><b>{html.escape(a)}.</b> {md(b)}</li>' for a, b in CHECKLIST) + '</ul>',
               H2('Toezicht') + P('In Nederland houden onder meer de [Autoriteit Persoonsgegevens](https://www.autoriteitpersoonsgegevens.nl/) en de [RDI](https://www.rdi.nl/) toezicht op de AI-verordening. AFM en DNB kijken mee via de zorgplicht en de beheerste bedrijfsvoering van financiële ondernemingen.'),
               '<div class="waarschuwing"><b>Controleer de actuele stand.</b> Met het Digital Omnibus-voorstel kunnen onderdelen van de AI-verordening, mogelijk ook de invulling van artikel 4, wijzigen. Zie [Wat is er nieuw](/nieuw/).</div>'],
              [('Moet ik een certificaat hebben voor artikel 4?', 'Nee. De AI-verordening schrijft geen certificaat of examen voor. Wel moet je kunnen laten zien welke maatregelen je hebt genomen. Een deelnamebewijs van een kwartaaltoets is daar één bouwsteen van, naast je AI-beleid en de vastlegging per medewerker.'),
               ('Geldt artikel 4 ook voor een klein kantoor?', 'Ja, elke organisatie die AI inzet moet zorgen voor voldoende AI-geletterdheid. De invulling mag in verhouding staan tot de omvang en het risico van het AI-gebruik.'),
               ('Sinds wanneer geldt de verplichting?', 'Sinds 2 februari 2025.'),
               ('Valt ingehuurd personeel eronder?', 'Ja, ook wie namens het kantoor AI gebruikt valt eronder. Neem hen mee in instructie, toetsing en vastlegging.')],
              [('Kennistoets AI-geletterdheid', '/kennistoets/'), ('Register AI-geletterdheid per medewerker', '/register/'), ('Begrippenlijst', '/begrippen/'), ('Wet- en regelgeving', '/wetgeving/')], prio='0.9')

    # --- privacyverklaring
    onderwerp('/ai-in-de-privacyverklaring/', 'AI in je privacyverklaring: wat vermeld je als adviseur? | AI Permanent Actueel',
              'Wat een hypotheek-, assurantie- of kredietadviseur in de privacyverklaring moet melden als AI-tools klantgegevens verwerken, met modelteksten en de bijbehorende AVG-artikelen.',
              'AI in je privacyverklaring', 'Onderwerp',
              'Gebruik je AI-tools bij klantgegevens, bijvoorbeeld voor het uitschrijven van gesprekken of het verwerken van documenten? Dan moet je dat in je privacyverklaring melden: dat je AI gebruikt, met welk doel, welke categorie ontvangers erbij betrokken is en of gegevens buiten de EER gaan (AVG art. 13 en 14).',
              [H2('Wat neem je op?') + UL(['Dat AI-hulpmiddelen worden gebruikt en waarvoor (bijvoorbeeld transcriptie en tekstverwerking).', 'De categorie ontvangers: de AI-dienstverlener als verwerker.', 'Doorgifte buiten de EER en de waarborg, zoals het EU-VS-dataprivacykader of modelcontractbepalingen.', 'De bewaartermijn bij de leverancier en of gegevens worden gebruikt om modellen te trainen.', 'Dat de adviseur het advies zelf opstelt, controleert en ondertekent.']),
               H2('Modeltekst privacyverklaring') + MODEL('Wij gebruiken AI-diensten van zorgvuldig geselecteerde leveranciers, bijvoorbeeld voor het uitschrijven van gesprekken en het verwerken van documenten. Met deze leveranciers hebben wij een verwerkersovereenkomst. [Alleen opnemen als contractueel vastgelegd: Zij gebruiken uw gegevens niet om hun AI-modellen te trainen.] [Vermeld of gegevens buiten de EER worden verwerkt en op basis van welke waarborg.]'),
               H2('Gesprekken opnemen of laten uitschrijven') + P('Meld aan het begin van het gesprek dat het wordt opgenomen of door AI wordt uitgeschreven, waarvoor en hoe lang het wordt bewaard. Leg de melding of toestemming vast in het dossier.') + MODEL('Voor een goed verslag laten we dit gesprek uitschrijven met een AI-hulpmiddel. De opname bewaren we niet langer dan nodig. Het verslag komt in uw dossier en u krijgt het ter controle. Heeft u bezwaar? Dan maken we zelf aantekeningen.'),
               H2('Wat leg je intern vast?') + UL(['Een **verwerkersovereenkomst** per AI-leverancier (AVG art. 28), met een zakelijke licentie en geen consumentenaccount.', 'Een **DPIA** als de verwerking waarschijnlijk een hoog risico oplevert, bijvoorbeeld bij nieuwe technologie en grootschalige verwerking van financiële gegevens (AVG art. 35).', 'Een **register van AI-toepassingen** per rol, als basis voor privacyverklaring en DPIA.', 'Een **meldroute** voor datalekken: binnen 72 uur melden bij de Autoriteit Persoonsgegevens als er risico is voor betrokkenen (AVG art. 33).'])],
              [('Moet ik in mijn privacyverklaring vermelden dat ik AI gebruik?', 'Ja, als AI-tools persoonsgegevens van klanten verwerken. Vermeld doel, categorie ontvangers en eventuele doorgifte buiten de EER (AVG art. 13 en 14).'),
               ('Heb ik een verwerkersovereenkomst nodig met een AI-leverancier?', 'Ja, als de leverancier in jouw opdracht persoonsgegevens verwerkt (AVG art. 28). Zonder die overeenkomst laat je geen klantgegevens verwerken door een AI-dienst.'),
               ('Mag ik een klantgesprek door AI laten uitschrijven?', 'Ja, mits je de klant vooraf informeert over de opname of transcriptie, het doel en de bewaartermijn, en dat vastlegt.'),
               ('Wanneer is een DPIA nodig?', 'Als een verwerking waarschijnlijk een hoog privacyrisico oplevert. Bij klantdossiers met financiële gegevens en nieuwe technologie is dat snel het geval.')],
              [('Klantcommunicatie bij AI: alle modelteksten', '/#klantcommunicatie'), ('AI-chatbot melden aan de klant', '/ai-chatbot-melden-aan-klant/'), ('Begrippenlijst', '/begrippen/'), ('Wet- en regelgeving', '/wetgeving/#avg')])

    # --- chatbot
    onderwerp('/ai-chatbot-melden-aan-klant/', 'AI-chatbot melden aan de klant: wat vraagt artikel 50? | AI Permanent Actueel',
              'Moet een advieskantoor klanten vertellen dat een chatbot of AI-mailassistent AI is? Wat artikel 50 van de AI-verordening vraagt, met een modeltekst.',
              'AI-chatbot melden aan de klant', 'Onderwerp',
              'Ja: mensen die met een chatbot of andere AI communiceren, moeten weten dat ze met AI te maken hebben, tenzij dat uit de omstandigheden duidelijk is (AI-verordening art. 50). Formeel ligt die plicht bij de aanbieder van het systeem. Bouw je de chatbot zelf of bied je hem onder eigen naam aan, dan ben jij die aanbieder. Meld het in elk geval altijd.',
              [H2('Wat vraagt artikel 50?') + UL(['**Chatbots en andere systemen die rechtstreeks met mensen communiceren** (art. 50 lid 1): de gebruiker moet weten dat het AI is.', '**Deepfakes** (art. 50 lid 4): de gebruiker maakt bekend dat beeld, geluid of video kunstmatig is gegenereerd of bewerkt.', '**AI-gegenereerde tekst** die wordt gepubliceerd om het publiek te informeren over zaken van algemeen belang: label het als AI-gegenereerd, tenzij een mens de tekst redactioneel heeft gecontroleerd en een persoon de verantwoordelijkheid draagt.']),
               H2('Wat mag de chatbot wel en niet?') + P('Een chatbot mag algemene informatie geven, maar geen persoonlijk advies. Persoonlijk advies vraagt een klantprofiel en valt onder de zorgplicht van de adviseur. Laat de chatbot daarom doorverwijzen naar een adviseur.'),
               H2('Modeltekst chatbot of AI-mailassistent') + MODEL('U communiceert met een digitale assistent die werkt met AI. De antwoorden zijn algemene informatie en geen advies. Wilt u een medewerker spreken? Typ ‘medewerker’ of bel [telefoonnummer].'),
               H2('Marketing met AI-beelden en AI-stemmen') + P('Gebruik je AI-gegenereerde beelden of stemmen die echt lijken, zoals een nagemaakt persoon? Maak dan bekend dat de inhoud kunstmatig is. Gebruik ook geen garantieclaims zoals ‘gegarandeerd de laagste maandlasten’: informatie aan klanten moet correct, duidelijk en niet misleidend zijn (Wft art. 4:19).'),
               '<div class="waarschuwing"><b>Controleer de actuele stand.</b> Termijnen voor onderdelen van artikel 50 kunnen via het Digital Omnibus-voorstel wijzigen. Zie [Wat is er nieuw](/nieuw/).</div>'],
              [('Moet ik klanten vertellen dat onze chatbot AI is?', 'Ja. Mensen moeten weten dat ze met een AI-systeem communiceren, tenzij dat duidelijk is. Meld het uiterlijk bij het eerste contact.'),
               ('Wie is verantwoordelijk voor die melding, ik of de leverancier?', 'Formeel de aanbieder van het systeem (art. 50 lid 1). Bouw of lever je de chatbot onder eigen naam, dan ben jij aanbieder. Meld het daarnaast zelf altijd, ook om misleiding te voorkomen.'),
               ('Mag een chatbot een leenbedrag noemen?', 'Alleen als algemene informatie. Een persoonlijk, bindend bedrag of advies vraagt een adviseur en een klantprofiel.')],
              [('AI in je privacyverklaring', '/ai-in-de-privacyverklaring/'), ('Klantcommunicatie: modelteksten', '/#klantcommunicatie'), ('Begrippenlijst', '/begrippen/'), ('Wet- en regelgeving', '/wetgeving/#ai-verordening')])

    # --- volmacht
    onderwerp('/ai-voor-volmachtbedrijven/', 'AI voor volmachtbedrijven: geautomatiseerde besluiten en afspraken | AI Permanent Actueel',
              'Wat een volmachtbedrijf moet regelen als AI wordt ingezet bij acceptatie, premie en schade: AVG artikel 22, afspraken met de volmachtgever en klantcommunicatie.',
              'AI voor volmachtbedrijven', 'Onderwerp',
              'Een volmachtbedrijf neemt namens de verzekeraar besluiten over acceptatie, premie en schade. Daardoor raakt AI hier snel aan geautomatiseerde besluitvorming: bij volledig geautomatiseerde besluiten met aanmerkelijk effect heeft de klant recht op uitleg, menselijke tussenkomst en bezwaar (AVG art. 22).',
              [H2('Wat leg je vast met de volmachtgever?') + UL(['Welk AI-gebruik binnen de volmacht valt bij acceptatie, premie en schade.', 'Wie verantwoordelijk is voor het systeem en voor de uitkomsten.', 'Hoe je rapporteert en hoe fouten worden hersteld.', 'Of de verzekeraar eigen kaders doorlegt, zoals het Ethisch Kader datagedreven toepassingen van het Verbond van Verzekeraars. Controleer of dat voor jouw volmacht geldt.']),
               H2('Geautomatiseerde besluiten') + P('Automatische acceptatie, premievaststelling of schade-afwijzing zonder menselijke beoordeling valt snel onder AVG art. 22. Neem in de brief op wie het besluit nam, en bied bij volledig geautomatiseerde besluiten uitleg, menselijke tussenkomst en de weg naar bezwaar en klacht.'),
               H2('Modeltekst acceptatie- of schadebesluit') + MODEL('Over uw [aanvraag/schade] is besloten door een medewerker van [naam volmachtbedrijf], namens [naam verzekeraar]. Daarbij gebruiken wij digitale hulpmiddelen. Bent u het niet eens met dit besluit? Neem dan contact met ons op. Komen we er samen niet uit, dan kunt u uw klacht voorleggen aan het Kifid.'),
               H2('Hoog-risico-AI bij leven en zorg') + P('AI voor risicobeoordeling en premiebepaling bij levens- en ziektekostenverzekeringen van particulieren is hoog-risico (AI-verordening bijlage III, punt 5c). Dat raakt vooral de verzekeraar, maar vraag een leverancier naar de conformiteit als je zo’n tool zelf inzet. De ingangsdatum is mogelijk uitgesteld: controleer de actuele stand.'),
               H2('Privacyverklaring') + P('Beschrijf welke gegevens AI of datamodellen gebruiken bij acceptatie, premievaststelling, schadebehandeling en fraudesignalering, en of daar een mens naar kijkt.')],
              [('Is automatische schade-afwijzing toegestaan?', 'Alleen onder de voorwaarden van AVG art. 22 en de afspraken met de volmachtgever. Bij volledig geautomatiseerde besluiten met aanmerkelijk effect heeft de klant recht op uitleg, menselijke tussenkomst en bezwaar.'),
               ('Wie is verantwoordelijk voor AI-gebruik binnen een volmacht?', 'Dat leg je vast in de volmachtovereenkomst. Het volmachtbedrijf blijft zelf verantwoordelijk voor zorgvuldigheid, controle en klantcommunicatie.'),
               ('Waar kan een klant terecht met een klacht?', 'Eerst bij het volmachtbedrijf zelf. Komen partijen er niet uit, dan kan de consument de klacht voorleggen aan het Kifid.')],
              [('Klantcommunicatie: modelteksten voor volmachtbedrijven', '/#klantcommunicatie'), ('AI in je privacyverklaring', '/ai-in-de-privacyverklaring/'), ('Begrippenlijst', '/begrippen/'), ('Wat is er nieuw', '/nieuw/')])

    # --- krediet
    onderwerp('/ai-kredietadvies-geautomatiseerde-beoordeling/', 'AI bij kredietadvies: geautomatiseerde beoordeling en de nieuwe richtlijn | AI Permanent Actueel',
              'Wat kredietadviseurs moeten weten over AI en geautomatiseerde kredietwaardigheidsbeoordeling: AVG artikel 22, hoog-risico-AI en de herziene Consumentenkredietrichtlijn per 20 november 2026.',
              'AI bij kredietadvies', 'Onderwerp',
              'Bij een geautomatiseerde kredietwaardigheidsbeoordeling heeft de consument volgens de herziene Consumentenkredietrichtlijn (EU) 2023/2225, van toepassing vanaf 20 november 2026, recht op menselijke tussenkomst, een uitleg van de beoordeling en het geven van zijn standpunt. Daarnaast is AI die de kredietwaardigheid van particulieren beoordeelt hoog-risico onder de AI-verordening.',
              [H2('Wat verandert er?') + UL(['**Consumentenkredietrichtlijn (EU) 2023/2225** (art. 18): rechten bij geautomatiseerde verwerking in de kredietwaardigheidsbeoordeling. Controleer de stand van de Nederlandse implementatie.', '**AVG art. 22:** recht om niet te worden onderworpen aan een uitsluitend geautomatiseerd besluit met aanmerkelijk effect.', '**AI-verordening bijlage III, punt 5b:** AI voor het beoordelen van de kredietwaardigheid van particulieren is hoog-risico. De ingangsdatum is mogelijk uitgesteld: controleer de actuele stand.']),
               H2('Wat zegt het Hof van Justitie?') + UL(['**SCHUFA (C-634/21, 7 december 2023):** het opstellen van een kredietscore kan zelf een geautomatiseerd besluit zijn, als de uitkomst bepalend is voor het besluit van de kredietverstrekker.', '**Dun & Bradstreet Austria (C-203/22, 27 februari 2025):** recht op een begrijpelijke uitleg van de logica van een geautomatiseerd besluit.']),
               H2('Wat doe je in de praktijk?') + UL(['Leg vast welke tools een rol spelen bij de beoordeling, en of het besluit uitsluitend geautomatiseerd is.', 'Zorg dat de klant een medewerker kan vragen de beoordeling opnieuw te bekijken.', 'Kan je een afwijzing uitleggen? Test dat voordat een klant het vraagt.', 'Neem het AI-gebruik op in privacyverklaring en dienstverleningsdocument.']),
               H2('Modeltekst kredietaanvraag') + MODEL('Bij de beoordeling van uw kredietaanvraag gebruiken wij geautomatiseerde hulpmiddelen. U heeft recht op een toelichting op de uitkomst, op een nieuwe beoordeling door een medewerker en op het geven van uw standpunt.')],
              [('Wanneer geldt de herziene Consumentenkredietrichtlijn?', 'Vanaf 20 november 2026. Controleer hoe de richtlijn in Nederlandse wetgeving is geïmplementeerd.'),
               ('Is AI voor kredietbeoordeling verboden?', 'Nee, maar het is hoog-risico-AI met zwaardere eisen, en bij geautomatiseerde besluiten gelden de rechten uit AVG art. 22 en de richtlijn.'),
               ('Wat betekent de SCHUFA-uitspraak voor mijn kantoor?', 'Dat ook een kredietscore van een derde partij zelf een geautomatiseerd besluit kan zijn als het besluit er in hoge mate van afhangt. Controleer welke scores je gebruikt en hoe ze het besluit bepalen.')],
              [('Klantcommunicatie voor kredietadvies', '/#klantcommunicatie'), ('AI in je privacyverklaring', '/ai-in-de-privacyverklaring/'), ('Wat is er nieuw', '/nieuw/'), ('Wet- en regelgeving', '/wetgeving/#krediet')])


# ================================================================ 404
def pagina_404():
    body = (P('Deze pagina bestaat niet (meer). Misschien helpt een van deze pagina’s:') +
            UL(['[Home](/)', '[Kennistoets AI-geletterdheid](/kennistoets/)', '[Klantcommunicatie bij AI](/#klantcommunicatie)', '[Wat is er nieuw](/nieuw/)', '[Begrippenlijst](/begrippen/)', '[Wet- en regelgeving](/wetgeving/)']))
    schrijf('/404.html', 'Pagina niet gevonden | AI Permanent Actueel', 'Deze pagina bestaat niet. Ga naar de homepage of de kennistoets van AI Permanent Actueel.',
            'Pagina niet gevonden', '404', body, crumb='Niet gevonden', robots='noindex, follow', sitemap=False)


def pagina_privacy():
    body = open(os.path.join(TOOLS, 'basis', 'privacy_body.html'), encoding='utf-8').read()
    schrijf('/privacy/', 'Privacy, voorwaarden en klachten | AI Permanent Actueel',
            'Hoe AI Permanent Actueel met je gegevens omgaat, de gebruiksvoorwaarden van de oefentoets en hoe je een klacht indient. Een activiteit van DFO BV.',
            'Privacy, voorwaarden en klachten', 'Over deze site', body, crumb='Privacy, voorwaarden en klachten', prio='0.3')


def genereer():
    pagina_privacy(); pagina_nieuw(); pagina_begrippen(); pagina_wetgeving(); pagina_over(); pagina_register(); pagina_onderwerpen(); pagina_404()
    json.dump(PAGINAS, open(os.path.join(os.environ.get('AIPA_WERK', os.path.join(TOOLS, '.werk')), 'paginas.json'), 'w'), ensure_ascii=False)
    print(f'{len(PAGINAS)} losse pagina\'s + 404 geschreven')


if __name__ == '__main__':
    os.makedirs(os.environ.get('AIPA_WERK', os.path.join(TOOLS, '.werk')), exist_ok=True)
    genereer()
