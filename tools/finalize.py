import re, json, sys, os
D = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, D)
from kc_data import *
REPO = os.environ.get('AIPA_REPO', os.path.dirname(D)); W = os.environ.get('AIPA_WERK', os.path.join(D, '.werk')); SITE = 'https://ai-permanent-actueel.nl/'
TITLE = 'AI Permanent Actueel | AI-geletterdheid voor financieel dienstverleners'
NOSCRIPT = '''  <noscript>
    <style>#__bundler_loading, #__bundler_thumbnail { display: none !important; } body { display: block !important; }</style>
  </noscript>
  <style>
    #seo-static { display: block; max-width: 900px; margin: 0 auto; padding: 24px 16px; color: #16202b; font: 16px/1.6 Arial, Helvetica, sans-serif; background: #fff; }
    #seo-static nav a { margin-right: 12px; }
    #seo-static h1, #seo-static h2, #seo-static h3, #seo-static h4 { line-height: 1.2; }
  </style>'''
PAGINAS = [('index.html','seo_head.html','static.html','AI Permanent Actueel | AI-geletterdheid voor financieel dienstverleners','nl'),
           ('kennistoets/index.html','seo_head_toets.html','static_toets.html','Kennistoets AI-geletterdheid | AI Permanent Actueel','nl'),
           ('en/knowledge-test/index.html','seo_head_en.html','static_en.html','AI Literacy Knowledge Test | AI Permanent Actueel','en')]
for PAD, HEADF, STATF, TITEL, LANG in PAGINAS:
  head = open(f'{W}/'+HEADF).read()
  static = open(f'{W}/'+STATF).read()
  static = re.sub(r'\s*<span>\d{1,2} \w+ 20\d\d</span>', '', static)
  static = static.replace('<div id="dc-root">', '<div>', 1)
  s = open(f'{REPO}/'+PAD, encoding='utf-8').read()
  def sub1(old, new):
      global s
      assert s.count(old) == 1, old[:60]; s = s.replace(old, new)
  sub1('<!DOCTYPE html>\n<html>\n<head>\n  <meta charset="utf-8">\n  <title>AI Permanent Actueel — ai-permanent-actueel.nl</title>\n',
       f'<!DOCTYPE html>\n<html lang="{LANG}">\n<head>\n  <meta charset="utf-8">\n  <meta name="viewport" content="width=device-width, initial-scale=1">\n  <title>{TITEL}</title>\n' + head)
  s, n = re.subn(r'  <noscript>.*?</noscript>', lambda m: NOSCRIPT, s, count=1, flags=re.S); assert n == 1
  sub1('  <div id="__bundler_loading">Unpacking...</div>\n',
       '  <div id="__bundler_loading">Laden…</div>\n  <!-- Statische versie van de inhoud voor zoekmachines, AI-crawlers en bezoekers zonder JavaScript. Wordt vervangen zodra de pagina geladen is. -->\n'
       '  <main id="seo-static">\n' + static + '\n  <p>' + ('This page works best with JavaScript enabled.' if LANG=='en' else 'Deze pagina werkt het best met JavaScript ingeschakeld (kennistoets, kantoorscan, zoeken).') + '</p>\n  </main>\n')
  open(f'{REPO}/'+PAD, 'w', encoding='utf-8').write(s)

open(f'{REPO}/robots.txt', 'w').write(f'''User-agent: *
Allow: /

# AI-zoekmachines en -assistenten expliciet welkom
User-agent: GPTBot
Allow: /
User-agent: OAI-SearchBot
Allow: /
User-agent: ChatGPT-User
Allow: /
User-agent: ClaudeBot
Allow: /
User-agent: Claude-SearchBot
Allow: /
User-agent: Claude-User
Allow: /
User-agent: PerplexityBot
Allow: /
User-agent: Google-Extended
Allow: /
User-agent: Applebot-Extended
Allow: /

Sitemap: {SITE}sitemap.xml
''')
def u(loc, prio, alt=False):
    x = f'  <url>\n    <loc>{loc}</loc>\n    <lastmod>2026-10-18</lastmod>\n    <changefreq>monthly</changefreq>\n    <priority>{prio}</priority>\n'
    if alt:
        x += f'    <xhtml:link rel="alternate" hreflang="nl" href="{SITE}kennistoets/"/>\n    <xhtml:link rel="alternate" hreflang="en" href="{SITE}en/knowledge-test/"/>\n'
    return x + '  </url>\n'
open(f'{REPO}/sitemap.xml', 'w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
    + u(SITE, '1.0') + u(SITE + 'kennistoets/', '0.9', True) + u(SITE + 'en/knowledge-test/', '0.6', True) + ''.join(u(SITE + pad.lstrip('/'), pr) for pad, tt, om, pr in json.load(open(f'{W}/paginas.json'))) + '</urlset>\n')

dc = json.load(open(f'{W}/dc.json')); faq = json.load(open(f'{W}/faq_all.json'))
md = [f'# AI Permanent Actueel', '',
      '> AI-geletterdheid (artikel 4 AI-verordening) voor medewerkers van Nederlandse financieel dienstverleners: hypotheek-, assurantie- en kredietadviseurs en volmachtbedrijven. Maandelijkse AI-update, kwartaaltoets met deelnamebewijs, en praktische hulp bij klantcommunicatie over AI-gebruik. Een activiteit van DFO BV (Hoevelaken).', '',
      'Gratis, zonder account. Het certificaat is een deelnamebewijs, geen diploma en geen bewijs van naleving.', '',
      f'- Website: {SITE}', f'- Kennistoets: {SITE}kennistoets/ (Engels: {SITE}en/knowledge-test/)', '- Uitgever: DFO BV, De Wel 14-16, 3871 MV Hoevelaken, 033 258 04 60, info@dfobv.nl', '- Stand: oktober 2026', '',
      '## Modules', '']
md += [f'{m["id"]}. **{m["naam"]}**: {m["omschr"]}' for m in dc['MODULES']]
md += ['', '## Pagina\'s', ''] + [f'- [{tt.split("|")[0].strip()}]({SITE}{pad.lstrip("/")}): {om}' for pad, tt, om, pr in json.load(open(f'{W}/paginas.json'))]
md += ['', '## Klantcommunicatie bij AI-gebruik', '', f'Bron: {SITE}#klantcommunicatie. Geldt voor hypotheek-, assurantie- en kredietadvies en volmachtbedrijven.', '']
for key, titel, lijst in BLOKKEN:
    md += [f'### {titel}', '']
    for k in lijst:
        sec = '' if 'alle' in k['s'] else ' (' + ', '.join(SECTORNAAM[x] for x in k['s']) + ')'
        bron = f' Grondslag: {k["bron"]}.' if k.get('bron') else ''
        md.append(f'- **{k["titel"]}**{sec}: {k["tekst"]}{bron}')
    md.append('')
md += ['## Dossier voor de werkgever (artikel 4)', '']
md += [f'- **{c["b"]}**: {c["s"]}' for c in dc['CHECKLIST']]
md += ['', '## Veelgestelde vragen', '']
for f in faq: md += [f'### {f["v"]}', '', f['a'], '']
md += ['## Disclaimer', '', 'Oefen- en bewustwordingsinstrument, geen juridisch advies. Laat AI-beleid en klantteksten toetsen door compliance of een jurist.', '']
open(f'{REPO}/llms.txt', 'w').write('\n'.join(md))
print('klaar')
