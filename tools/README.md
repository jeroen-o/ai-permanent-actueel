# Bouwscripts

De pagina's `index.html`, `kennistoets/index.html` en `en/knowledge-test/index.html` zijn gebundelde bestanden
(sjabloon in een JSON-string). Ze zijn **niet bedoeld om met de hand te bewerken**: pas de scripts hier aan en bouw opnieuw.
De losse pagina's (nieuw, begrippen, wetgeving, over, register, privacy, onderwerppagina's, 404) worden door `paginas.py` gegenereerd.

## Bouwen

```bash
bash tools/bouw.sh        # vanuit de root van de repo
```

Nodig: Python 3, Node.js, `playwright` (met Chromium) en `Pillow` (alleen voor het maken van `favicon.ico` met `fav.js`).
Tussenbestanden komen in `tools/.werk/` (niet in git).

## Waar pas je wat aan?

| Wat | Waar |
|---|---|
| Klantcommunicatie (verplicht, aanbevolen, intern, modelteksten, aandachtspunten) | `kc_data.py` |
| Toetsvragen (NL en EN, 20 per module) | `vragen_nl.py`, `vragen_en.py` (via `vragen.py`) |
| Gratis-blok, tip je collega's, nieuwsbrieven, footer, Let op-tekst | `extras.py` |
| HOERA-banner en confetti | `feest.py` |
| Zoeken, scroll-offset, header | `ronde3.py` |
| Bronlinks in de toetsuitleg, doorzoekbare pagina's en begrippen | `ronde4.py` |
| Kennistoets-pagina en Engelse versie | `variants.py` |
| Updates, begrippen, wetgeving, over, register, onderwerppagina's, 404, privacy | `paginas.py` (privacytekst in `basis/privacy_body.html`) |
| SEO-head, statische tekst voor crawlers, robots.txt, sitemap.xml, llms.txt | `finalize.py` |
| Favicons | `fav.js` (bron: `favicon.svg`) |

`basis/index.html` is de oorspronkelijke gebundelde homepage waarop alle aanpassingen worden toegepast.

## Testen

```bash
python3 tools/tests/links.py                        # alle interne links en ankers
python3 tools/tests/vragen_kwaliteit.py             # vragenbank: aantallen en geen lengte-cue
python3 -m http.server 8765 &                       # vanuit de repo-root
cd tools/tests && node e2e.js && node mob.js && node scroll.js && node paginas.js
node err.js kennistoets/index.html                  # console-fouten per pagina
```

## Let op bij onderhoud

- Pas je een tekst aan, bouw dan opnieuw: de statische tekst voor zoekmachines, `llms.txt` en de sitemap worden daaruit afgeleid.
- Regelgeving rond de AI-verordening is in beweging (Digital Omnibus). Controleer de teksten in `paginas.py` (`pagina_nieuw`) en `kc_data.py` regelmatig.
