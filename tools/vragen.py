"""Alle toetsvragen (NL en EN), 45 per module. Bron: vragen_nl.py + vragen_nl2.py en vragen_en.py + vragen_en2.py."""
from vragen_nl import NL as _NL1
from vragen_nl2 import NL2
from vragen_en import EN as _EN1
from vragen_en2 import EN2

NL = _NL1 + NL2
EN = _EN1 + EN2
