"""Kwaliteitscontrole toetsvragen: aantal per module, unieke opties, en geen 'kies het langste antwoord'-patroon."""
import os, sys, collections
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from vragen import NL, EN

def check(naam, lijst, per_module=20):
    fouten = []
    c = collections.Counter(v[0] for v in lijst)
    for m in range(1, 8):
        if c[m] != per_module: fouten.append(f'{naam}: module {m} heeft {c[m]} vragen (verwacht {per_module})')
    vragen = set()
    langste = 0; ratios = []
    for v in lijst:
        m, vraag, goed, fout, uitleg = v
        opts = [goed] + fout
        if len(set(opts)) != 4: fouten.append(f'{naam}: dubbele opties bij "{vraag[:50]}"')
        if vraag in vragen: fouten.append(f'{naam}: dubbele vraag "{vraag[:50]}"')
        vragen.add(vraag)
        if not uitleg.strip(): fouten.append(f'{naam}: geen uitleg bij "{vraag[:50]}"')
        if len(goed) >= max(len(x) for x in fout): langste += 1
        ratios.append(len(goed) / (sum(len(x) for x in fout) / 3))
    n = len(lijst)
    gem = sum(ratios) / n
    print(f'{naam}: {n} vragen | juiste antwoord is langste bij {langste} ({round(100*langste/n)}%) | gem. verhouding juist/fout {gem:.2f} | max {max(ratios):.2f}')
    if langste / n > 0.40: fouten.append(f'{naam}: juiste antwoord is te vaak het langste ({langste}/{n})')
    if gem > 1.25: fouten.append(f'{naam}: juiste antwoorden zijn gemiddeld te lang t.o.v. de foute ({gem:.2f})')
    return fouten

f = check('NL', NL) + check('EN', EN)
if len(NL) != len(EN): f.append('NL en EN hebben een verschillend aantal vragen')
for a, b in zip(NL, EN):
    if a[0] != b[0]: f.append(f'Module-volgorde wijkt af bij "{a[1][:40]}"')
print('\n'.join(f) if f else 'OK')
sys.exit(1 if f else 0)
