# ---------- ronde 4: bronlinks bij toetsuitleg, losse pagina's doorzoekbaar ----------
import paginas as _pg
_pg.PAGINAS.clear(); _pg.genereer()
ZOEKPAGINAS = [[tt.split('|')[0].strip(), om, pad] for pad, tt, om, pr in _pg.PAGINAS]

ZOEKTERMEN = [[n, re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', d), _pg.slug(n)] for n, d in _pg.TERMEN]
BRONNEN = {1: ['begrippen/#taalmodel-llm', 'Begrippenlijst'], 2: ['wetgeving/#ai-verordening', 'AI-verordening'],
           3: ['wetgeving/#avg', 'AVG en privacy'], 4: ['begrippen/#automation-bias', 'Begrippenlijst'],
           5: ['wetgeving/#wft', 'Wft en zorgplicht'], 6: ['begrippen/#shadow-ai', 'Begrippenlijst'],
           7: ['wetgeving/#aansprakelijkheid', 'Aansprakelijkheid']}

t = sub1("const PAGINA='__PAGINA__';",
         "const PAGINA='__PAGINA__';\nconst BRONNEN=" + json.dumps(BRONNEN, ensure_ascii=False) + ";\nconst ZOEKTERMEN=" + json.dumps(ZOEKTERMEN, ensure_ascii=False) + ";\nconst ZOEKPAGINAS=" + json.dumps(ZOEKPAGINAS, ensure_ascii=False) + ";", t)
t = sub1('<span>{{ uitleg }}</span>',
         '<span>{{ uitleg }}</span>\n            <a href="{{ bronHref }}" style="font-size:13px;font-weight:700">{{ bronLabel }}</a>', t)
t = sub1("      uitleg:vraag.u,",
         "      uitleg:vraag.u, bronHref:HOME+BRONNEN[vraag.m||1][0], bronLabel:(document.documentElement.lang==='en'?'Read more (Dutch): ':'Meer lezen: ')+BRONNEN[vraag.m||1][1],", t)
t = sub1("    if(PAGINA==='home') voeg('Kwartaaltoets'",
         "    ZOEKTERMEN.forEach(z=>voeg('Begrippenlijst',z[0],z[1],()=>{ window.location.href=HOME+'begrippen/#'+z[2]; }));\n    ZOEKPAGINAS.forEach(z=>voeg('Pagina',z[0],z[1],()=>{ window.location.href=HOME+z[2].slice(1); }));\n    if(PAGINA==='home') voeg('Kwartaaltoets'", t)
t = sub1('<p style="margin:0;font-size:14px;line-height:1.5">Eén thema, drie minuten, met een voorbeeld uit de kantoorpraktijk.</p>',
         '<p style="margin:0;font-size:14px;line-height:1.5">Eén thema, drie minuten, met een voorbeeld uit de kantoorpraktijk. Lees de <a href="nieuw/">updates</a>.</p>', t)
