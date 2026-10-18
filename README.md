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

- Werkt: modules, pakket-check, kennistoets + certificaat, prompt-check, kantoorscan, dossier-checklist, veelgestelde vragen, tabblad *Klantcommunicatie* (per beroepsgroep), zoekfunctie (ook via `?q=zoekterm`) en Home-knop.
## Nog in te vullen

- Echte aanmeldlinks voor DFO Signalen en Nieuwsbrief Wft (nu `dfobv.nl`).
- Controle van de tekst bij "Wat kost het?" en de SLIM-subsidie.

## SEO en GEO

- `index.html` bevat in de `<head>` meta description, canonical, Open Graph/Twitter, favicon en JSON-LD (Organization, WebSite met SearchAction, WebPage, FAQPage).
- In de body staat een statische tekstversie van de pagina (`<main id="seo-static">`) voor zoekmachines, AI-crawlers en bezoekers zonder JavaScript. Die wordt vervangen zodra de interactieve pagina laadt. **Pas je teksten aan, werk dan ook dit blok en `llms.txt` bij.**
- `robots.txt` (ook AI-crawlers toegestaan), `sitemap.xml`, `llms.txt` (samenvatting voor AI-assistenten) en `og-image.png` (deelafbeelding 1200×630) staan in de root.
- Na livegang: dien de sitemap in bij Google Search Console en Bing Webmaster Tools.
