# ai-permanent-actueel.nl

AI Permanent Actueel — maandelijkse AI-updates en een kwartaaltoets voor medewerkers van financieel dienstverleners. Een activiteit van DFO BV.

## Publiceren met GitHub Pages

1. Maak een repository aan, bijv. `ai-permanent-actueel`.
2. Upload `index.html` (en deze README) naar de root van de `main`-branch.
3. Ga naar **Settings → Pages**, kies *Deploy from a branch*, branch `main`, map `/ (root)`.
4. Eigen domein: vul bij **Custom domain** `ai-permanent-actueel.nl` in en zet bij je DNS-provider:
   - 4 A-records naar `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`
   - een CNAME `www` naar `<gebruikersnaam>.github.io`
5. Vink **Enforce HTTPS** aan.

`index.html` is volledig zelfstandig: stijlen, scripts en het DFO-logo zitten erin.

## Wat werkt er op GitHub Pages

- Werkt: modules, pakket-check, kennistoets + certificaat, prompt-check, kantoorscan, dossier-checklist, veelgestelde vragen.
- Werkt niet zonder koppeling: de **AI-assistent** (en de knop "Leg verder uit met AI"). Die gebruikt nu de ingebouwde AI van de ontwerpomgeving. Voor livegang is een eigen backend nodig (bijv. een serverless functie die de Claude API aanroept met een API-sleutel die niet in de browser staat).

## Nog in te vullen

- Echte aanmeldlinks voor DFO Signalen en Nieuwsbrief Wft (nu `dfobv.nl`).
- Controle van de tekst bij "Wat kost het?" en de SLIM-subsidie.
