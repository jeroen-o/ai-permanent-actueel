#!/usr/bin/env bash
# Bouwt de hele site opnieuw uit tools/basis/index.html + de scripts in tools/.
# Gebruik: bash tools/bouw.sh      (vanuit de root van de repo)
set -euo pipefail
cd "$(dirname "$0")/.."
export AIPA_REPO="$PWD" AIPA_WERK="$PWD/tools/.werk"
mkdir -p "$AIPA_WERK"
python3 tools/build.py                      # homepage, /kennistoets/, /en/knowledge-test/
node tools/snap.js                          # statische tekst + og-image (homepage)
node tools/snap.js kennistoets/index.html static_toets.html
node tools/snap.js en/knowledge-test/index.html static_en.html
python3 tools/paginas.py                    # losse pagina's: nieuw, begrippen, wetgeving, register, ...
python3 tools/finalize.py                   # SEO-head, statische tekst, robots, sitemap, llms.txt
python3 tools/maak_antw.py                  # antwoordsleutel voor de tests
