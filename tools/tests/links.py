"""Controleert alle interne links en ankers in de gebouwde site (zonder netwerk)."""
import os, re, sys
from html.parser import HTMLParser
from urllib.parse import urlparse, urldefrag, unquote

REPO = os.environ.get('AIPA_REPO', os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
SITE = 'https://ai-permanent-actueel.nl'

def bestanden():
    for r, d, f in os.walk(REPO):
        d[:] = [x for x in d if x not in ('.git', 'tools', 'node_modules')]
        for n in f:
            if n.endswith('.html'): yield os.path.join(r, n)

class P(HTMLParser):
    def __init__(s): super().__init__(); s.hrefs = []
    def handle_starttag(s, tag, attrs):
        a = dict(attrs)
        if tag in ('a', 'link') and a.get('href'): s.hrefs.append(a['href'])
        if tag in ('img', 'script') and a.get('src'): s.hrefs.append(a['src'])

def doel(van, href):
    if href.startswith(('mailto:', 'tel:', 'data:', 'javascript:', 'blob:')) or re.match(r'^[0-9a-f-]{36}$', href): return None
    if href.startswith(SITE): href = href[len(SITE):] or '/'
    if re.match(r'^[a-z]+://', href): return None
    pad, frag = urldefrag(href); pad = unquote(pad)
    if not pad: p = van
    elif pad.startswith('/'): p = os.path.join(REPO, pad.lstrip('/'))
    else: p = os.path.normpath(os.path.join(os.path.dirname(van), pad))
    if os.path.isdir(p): p = os.path.join(p, 'index.html')
    return p, frag

fouten = 0; n = 0; cache = {}
def tekst(p):
    if p not in cache: cache[p] = open(p, encoding='utf-8').read()
    return cache[p]
for b in bestanden():
    p = P(); p.feed(tekst(b))
    for h in p.hrefs:
        n += 1
        d = doel(b, h)
        if not d: continue
        pad, frag = d
        if not os.path.exists(pad):
            print('ONTBREEKT', os.path.relpath(b, REPO), '->', h); fouten += 1; continue
        if frag and pad.endswith('.html'):
            t = tekst(pad)
            if not re.search(r'id=\\?"%s\\?"' % re.escape(frag), t) and not re.search(r'name=\\?"%s\\?"' % re.escape(frag), t):
                print('ANKER ONTBREEKT', os.path.relpath(b, REPO), '->', h); fouten += 1
print(f'{n} links gecontroleerd, {fouten} fout(en)')
sys.exit(1 if fouten else 0)
