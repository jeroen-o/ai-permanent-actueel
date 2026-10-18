"""Maakt antw.json (vraag -> juist antwoord) voor de tests, uit de gebouwde sjablonen."""
import json, os, re
D = os.path.dirname(os.path.abspath(__file__))
W = os.environ.get('AIPA_WERK', os.path.join(D, '.werk'))
m = {}
for f in ['template.toets.html', 'template.en.html']:
    t = open(os.path.join(W, f), encoding='utf-8').read()
    for v in re.finditer(r'  V\((\d+),\s*("(?:[^"\\]|\\.)*"),\s*("(?:[^"\\]|\\.)*")', t):
        m[json.loads(v.group(2))] = json.loads(v.group(3))
json.dump(m, open(os.path.join(W, 'antw.json'), 'w'), ensure_ascii=False)
print('antw.json:', len(m), 'vragen')
