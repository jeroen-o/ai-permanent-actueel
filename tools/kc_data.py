# Inhoud tabblad "Klantcommunicatie bij AI" — gedeeld door template, statische SEO-tekst en llms.txt
ALLE = ['alle']

SECTOREN = [
    {"id": "alle", "naam": "Alle beroepsgroepen"},
    {"id": "hypotheek", "naam": "Hypotheekadvies"},
    {"id": "assurantie", "naam": "Assurantieadvies"},
    {"id": "krediet", "naam": "Kredietadvies"},
    {"id": "volmacht", "naam": "Volmachtbedrijf"},
]

INTRO = {
    "alle": "Wat voor iedereen geldt, plus de punten per beroepsgroep. Kies hierboven een beroepsgroep om alleen die te zien.",
    "hypotheek": "Hypotheekadvies: AI ondersteunt bij gespreksverslagen, het lezen van loonstroken, werkgeversverklaringen en taxatierapporten, en bij conceptteksten voor het adviesrapport.",
    "assurantie": "Assurantieadvies (schade, leven, inkomen): AI ondersteunt bij inventarisaties, polisvergelijkingen, schademeldingen en klantcorrespondentie.",
    "krediet": "Kredietadvies en -bemiddeling (consumptief krediet): AI ondersteunt bij het verwerken van inkomens- en lastengegevens en bij het beoordelen van aanvragen.",
    "volmacht": "Volmachtbedrijven nemen namens de verzekeraar besluiten over acceptatie, premie en schade. Daar raakt AI het snelst aan geautomatiseerde besluitvorming en strengere regels.",
}

VERPLICHT = [
    {"k": "privacyverklaring", "s": ALLE, "titel": "Privacyverklaring",
     "tekst": "Meld dat je AI-tools gebruikt en welke klantgegevens erin gaan. Noem de categorie verwerker (bijv. 'AI-dienstverlener voor transcriptie en tekstverwerking'), doorgifte buiten de EER met de waarborg (EU-VS-dataprivacykader of modelcontractbepalingen), de bewaartermijn bij de leverancier en of gegevens voor training worden gebruikt.",
     "bron": "AVG art. 13 en 14"},
    {"k": "opname", "s": ALLE, "titel": "Melding bij opnemen of transcriberen van gesprekken",
     "tekst": "Meld aan het begin van het gesprek dat het wordt opgenomen of door AI wordt uitgeschreven, waarvoor en hoe lang het wordt bewaard. Leg de melding of toestemming vast in het dossier.",
     "bron": "AVG art. 5, 6 en 13"},
    {"k": "chatbot", "s": ALLE, "titel": "Melding bij chatbot of AI-gegenereerde content",
     "tekst": "Klanten moeten weten dat ze met een AI-systeem communiceren, uiterlijk bij het eerste contact (chatbot op de site, AI-mailassistent, voicebot). De plicht ligt formeel bij de aanbieder van de chatbot (art. 50 lid 1): bouw je hem zelf of bied je hem onder eigen naam aan, dan ben jij dat. Meld het in elk geval altijd. AI-gegenereerde teksten die je publiceert om het publiek te informeren over zaken van algemeen belang, label je als AI-gegenereerd, tenzij een mens ze redactioneel heeft gecontroleerd.",
     "bron": "AI-verordening art. 50, sinds 2 augustus 2026"},
    {"k": "art22", "s": ALLE, "titel": "Informatie bij geautomatiseerde besluiten",
     "tekst": "Alleen als een systeem zonder menselijke beoordeling een besluit neemt met rechtsgevolg of aanmerkelijk effect, zoals automatische acceptatie, afwijzing of premievaststelling. Dan: vooraf melden, de onderliggende logica uitleggen en recht geven op menselijke tussenkomst en bezwaar.",
     "bron": "AVG art. 22"},
]

AANBEVOLEN = [
    # hypotheek
    {"k": "hyp-dvd", "s": ["hypotheek"], "titel": "Dienstverleningsdocument",
     "tekst": "Korte paragraaf over je werkwijze: AI ondersteunt, de adviseur adviseert. Verwijs naar de privacyverklaring.", "bron": "Wft-informatieplicht"},
    {"k": "hyp-rapport", "s": ["hypotheek"], "titel": "Adviesrapport",
     "tekst": "Eén zin dat de adviseur de inhoud heeft beoordeeld en verantwoordelijk is voor het advies. Geen disclaimer die verantwoordelijkheid naar de AI verschuift.", "bron": "Wft zorgplicht (art. 4:24a)"},
    {"k": "hyp-opdracht", "s": ["hypotheek"], "titel": "Opdracht tot dienstverlening en algemene voorwaarden",
     "tekst": "Verwijzing naar het AI-gebruik en de privacyverklaring, zodat de klant het bij de start van de opdracht weet.", "bron": "AVG art. 13"},
    # assurantie
    {"k": "ass-dvd", "s": ["assurantie"], "titel": "Dienstverleningsdocument",
     "tekst": "Paragraaf over de werkwijze met AI bij inventarisatie, polisvergelijking en schadebehandeling. AI ondersteunt, de adviseur adviseert.", "bron": "Wft-informatieplicht"},
    {"k": "ass-advies", "s": ["assurantie"], "titel": "Adviesrapport of adviesverslag (leven, inkomen, schade)",
     "tekst": "Vermeld dat de adviseur de uitkomst van een AI-ondersteunde inventarisatie of vergelijking heeft gecontroleerd. Een vergelijking door AI is geen advies.", "bron": "Wft zorgplicht (art. 4:24a)"},
    {"k": "ass-schade", "s": ["assurantie"], "titel": "Schademelding via chatbot of formulier",
     "tekst": "Laat bij een AI-chatbot of slimme schadeformulier vooraf zien dat de klant met AI communiceert en hoe hij een medewerker bereikt.", "bron": "AI-verordening art. 50"},
    # krediet
    {"k": "kre-dvd", "s": ["krediet"], "titel": "Dienstverleningsdocument",
     "tekst": "Paragraaf over de werkwijze met AI bij het verwerken van inkomens- en lastengegevens. De adviseur beoordeelt de uitkomst.", "bron": "Wft-informatieplicht"},
    {"k": "kre-advies", "s": ["krediet"], "titel": "Kredietadvies en uitleg bij afwijzing",
     "tekst": "Leg uit hoe de beoordeling tot stand kwam als AI of geautomatiseerde verwerking een rol speelde, en dat de klant beoordeling door een medewerker kan vragen.", "bron": "AVG art. 22 · Consumentenkredietrichtlijn (EU) 2023/2225"},
    # volmacht
    {"k": "vol-privacy", "s": ["volmacht"], "titel": "Privacyverklaring: acceptatie, premie, schade en fraude",
     "tekst": "Beschrijf welke gegevens AI of datamodellen gebruiken bij acceptatie, premievaststelling, schadebehandeling en fraudesignalering, en of daar een mens naar kijkt.", "bron": "AVG art. 13, 14 en 22"},
    {"k": "vol-besluit", "s": ["volmacht"], "titel": "Acceptatie- en schadebesluiten",
     "tekst": "Vermeld in de brief wie het besluit nam. Bij volledig geautomatiseerde besluiten: uitleg, recht op menselijke tussenkomst en de weg naar bezwaar, klachtenprocedure en Kifid.", "bron": "AVG art. 22"},
    {"k": "vol-voorwaarden", "s": ["volmacht"], "titel": "Polisvoorwaarden en klantinformatie",
     "tekst": "Neem op dat digitale hulpmiddelen worden gebruikt bij acceptatie en schadebehandeling, in lijn met wat de volmachtgever voorschrijft.", "bron": "Volmachtovereenkomst"},
]

INTERN = [
    {"k": "verwerker", "s": ALLE, "titel": "Verwerkersovereenkomst per AI-leverancier",
     "tekst": "Voor elke tool die in opdracht persoonsgegevens verwerkt. Gebruik een zakelijke licentie, geen consumentenaccount.", "bron": "AVG art. 28"},
    {"k": "dpia", "s": ALLE, "titel": "DPIA",
     "tekst": "Bij grootschalige verwerking van financiële gegevens of inzet van nieuwe technologie. Bij klantdossiers is dat snel het geval.", "bron": "AVG art. 35"},
    {"k": "beleid", "s": ALLE, "titel": "AI-beleid",
     "tekst": "Welke tools mogen, voor welke taken, welke gegevens er niet in gaan en hoe de output wordt gecontroleerd.", "bron": "Beheerste bedrijfsvoering (Wft)"},
    {"k": "register", "s": ALLE, "titel": "Register van AI-toepassingen",
     "tekst": "Per rol welk AI-gebruik er is, met risico en verantwoordelijke. Basis voor de privacyverklaring en de DPIA.", "bron": "AVG art. 30 · AI-verordening"},
    {"k": "geletterdheid", "s": ALLE, "titel": "AI-geletterdheid aantoonbaar",
     "tekst": "Instructie en toetsing per medewerker vastgelegd, ook voor ingehuurd personeel. Zie de kennistoets en het dossier op deze site.", "bron": "AI-verordening art. 4, sinds 2 februari 2025"},
    {"k": "volmachtgever", "s": ["volmacht"], "titel": "Afspraken met de volmachtgever",
     "tekst": "Leg vast welk AI-gebruik binnen de volmacht valt bij acceptatie, premie en schade, wie verantwoordelijk is en hoe je rapporteert. Controleer of de verzekeraar eigen kaders doorlegt, zoals het Ethisch Kader datagedreven toepassingen van het Verbond van Verzekeraars.", "bron": "Volmachtovereenkomst"},
]

MODELLEN = [
    {"k": "m-dvd", "s": ALLE, "titel": "Dienstverleningsdocument",
     "tekst": "Wij gebruiken AI-hulpmiddelen ter ondersteuning van ons werk, bijvoorbeeld voor gespreksverslagen en het verwerken van documenten. Het advies stelt uw adviseur zelf op, controleert en ondertekent het. Hoe wij met uw gegevens omgaan, leest u in onze privacyverklaring."},
    {"k": "m-rapport", "s": ALLE, "titel": "Adviesrapport",
     "tekst": "Bij de voorbereiding van dit rapport zijn digitale hulpmiddelen gebruikt, waaronder AI. De inhoud is beoordeeld en vastgesteld door [naam adviseur], die verantwoordelijk is voor dit advies."},
    {"k": "m-gesprek", "s": ALLE, "titel": "Gespreksopening bij AI-transcriptie",
     "tekst": "Voor een goed verslag laten we dit gesprek uitschrijven met een AI-hulpmiddel. De opname bewaren we niet langer dan nodig. Het verslag komt in uw dossier en u krijgt het ter controle. Heeft u bezwaar? Dan maken we zelf aantekeningen."},
    {"k": "m-chatbot", "s": ALLE, "titel": "Chatbot of AI-mailassistent",
     "tekst": "U communiceert met een digitale assistent die werkt met AI. De antwoorden zijn algemene informatie en geen advies. Wilt u een medewerker spreken? Typ 'medewerker' of bel [telefoonnummer]."},
    {"k": "m-privacy", "s": ALLE, "titel": "Passage privacyverklaring",
     "tekst": "Wij gebruiken AI-diensten van zorgvuldig geselecteerde leveranciers, bijvoorbeeld voor het uitschrijven van gesprekken en het verwerken van documenten. Met deze leveranciers hebben wij een verwerkersovereenkomst. [Alleen opnemen als contractueel vastgelegd: Zij gebruiken uw gegevens niet om hun AI-modellen te trainen.] [Vermeld of gegevens buiten de EER worden verwerkt en op basis van welke waarborg.]"},
    {"k": "m-krediet", "s": ["krediet"], "titel": "Kredietaanvraag met geautomatiseerde beoordeling",
     "tekst": "Bij de beoordeling van uw kredietaanvraag gebruiken wij geautomatiseerde hulpmiddelen. U heeft recht op een toelichting op de uitkomst, op een nieuwe beoordeling door een medewerker en op het geven van uw standpunt."},
    {"k": "m-volmacht", "s": ["volmacht"], "titel": "Acceptatie- of schadebesluit",
     "tekst": "Over uw [aanvraag/schade] is besloten door een medewerker van [naam volmachtbedrijf], namens [naam verzekeraar]. Daarbij gebruiken wij digitale hulpmiddelen. Bent u het niet eens met dit besluit? Neem dan contact met ons op. Komen we er samen niet uit, dan kunt u uw klacht voorleggen aan het Kifid."},
]

LETOP = [
    {"k": "lo-zorgplicht", "s": ALLE, "titel": "Zorgplicht: de adviseur blijft verantwoordelijk",
     "tekst": "Teksten als 'AI-gestuurd advies' of 'AI berekent uw maximale hypotheek' kunnen misleiden over wie adviseert. Risico: AFM-toezicht op misleidende informatie en een zwakkere positie bij een Kifid-klacht.",
     "bron": "Wft art. 4:19 en 4:24a"},
    {"k": "lo-claims", "s": ALLE, "titel": "Geen garantieclaims",
     "tekst": "Gebruik geen termen als 'AVG-proof' of 'AI-gecertificeerd' in klantcommunicatie. Dat zijn claims die je niet kunt waarmaken.",
     "bron": "Wft art. 4:19"},
    {"k": "lo-hoogrisico-hyp", "s": ["hypotheek"], "titel": "Kredietwaardigheid is hoog-risico-AI",
     "tekst": "AI die de kredietwaardigheid van particulieren beoordeelt, is hoog-risico (bijlage III, punt 5b). Een rekentool met vaste rekenregels valt daar doorgaans niet onder, een zelflerend model wel. Als gebruiker moet je de klant dan informeren (art. 26). De ingangsdatum is via het Digital Omnibus-voorstel mogelijk uitgesteld: controleer de actuele stand.",
     "bron": "AI-verordening bijlage III, art. 26"},
    {"k": "lo-hoogrisico-ass", "s": ["assurantie"], "titel": "Leven en zorg: hoog-risico-AI",
     "tekst": "AI voor risicobeoordeling en premiebepaling bij levens- en ziektekostenverzekeringen van particulieren is hoog-risico (bijlage III, punt 5c). Dat raakt vooral de verzekeraar. Gebruik je zelf zo'n tool richting de klant, vraag de leverancier dan naar de conformiteit. De ingangsdatum is mogelijk uitgesteld: controleer de actuele stand.",
     "bron": "AI-verordening bijlage III"},
    {"k": "lo-ccd2", "s": ["krediet"], "titel": "Nieuwe Consumentenkredietrichtlijn",
     "tekst": "De herziene richtlijn (EU) 2023/2225 geldt vanaf 20 november 2026. Bij een geautomatiseerde kredietwaardigheidsbeoordeling krijgt de consument recht op menselijke tussenkomst, een uitleg en het geven van zijn standpunt. Controleer de stand van de Nederlandse implementatie. Daarnaast is AI voor kredietwaardigheid hoog-risico (bijlage III, punt 5b).",
     "bron": "Richtlijn (EU) 2023/2225 · AI-verordening"},
    {"k": "lo-volmacht", "s": ["volmacht"], "titel": "Besluiten namens de verzekeraar",
     "tekst": "Automatische acceptatie, premie of schadeafwijzing valt snel onder AVG art. 22. Bij leven- en ziektekostenverzekeringen kan ook hoog-risico-AI aan de orde zijn (bijlage III, punt 5c). Leg in de volmachtovereenkomst vast wat mag en wie verantwoordelijk is.",
     "bron": "AVG art. 22 · AI-verordening"},
    {"k": "lo-omnibus", "s": ALLE, "titel": "Controleer de actuele stand van de AI-verordening",
     "tekst": "Het Digital Omnibus-voorstel kan termijnen (onder meer voor hoog-risico-AI) en onderdelen van de verordening wijzigen, mogelijk ook de invulling van artikel 4. Dit overzicht geeft de stand van oktober 2026 voor zover bekend. Zie Wat is er nieuw.",
     "bron": "AI-verordening · Digital Omnibus"},
    {"k": "lo-toets", "s": ALLE, "titel": "Modelteksten zijn voorbeelden",
     "tekst": "Pas de teksten aan op je eigen tools en processen en laat ze toetsen door compliance of een jurist. Dit overzicht is geen juridisch advies.",
     "bron": ""},
]

BLOKKEN = [
    ("verplicht", "1 · Verplicht naar de klant", VERPLICHT),
    ("aanbevolen", "2 · Aanbevolen in je klantdocumenten", AANBEVOLEN),
    ("intern", "3 · Intern vastleggen (niet naar de klant)", INTERN),
    ("modellen", "4 · Modelteksten", MODELLEN),
    ("letop", "Compliance-aandachtspunten", LETOP),
]

SECTORNAAM = {s["id"]: s["naam"] for s in SECTOREN}

# Extra vragen voor FAQPage / llms.txt
KC_FAQ = [
    {"v": "Welke documenten moet ik aanpassen als ik AI gebruik in mijn werk als financieel adviseur?",
     "a": "Verplicht: de privacyverklaring (AVG art. 13 en 14), een melding vooraf bij het opnemen of AI-transcriberen van gesprekken, een AI-melding bij een chatbot of AI-mailassistent (AI-verordening art. 50) en, bij volledig geautomatiseerde besluiten, informatie over AVG art. 22. Aanbevolen: een paragraaf in het dienstverleningsdocument, één zin in het adviesrapport en een verwijzing in de opdracht tot dienstverlening."},
    {"v": "Moet ik klanten vertellen dat onze chatbot AI is?",
     "a": "Ja. Op grond van artikel 50 van de AI-verordening (van toepassing sinds 2 augustus 2026; controleer de actuele stand) moeten mensen weten dat ze met een AI-systeem communiceren, uiterlijk bij het eerste contact. Formeel ligt die plicht bij de aanbieder van de chatbot; bouw of lever je hem onder eigen naam, dan ben jij dat zelf."},
    {"v": "Wat moet een volmachtbedrijf extra regelen bij AI?",
     "a": "Een volmachtbedrijf neemt besluiten over acceptatie, premie en schade. Bij geautomatiseerde besluiten gelden de rechten uit AVG art. 22 (uitleg, menselijke tussenkomst, bezwaar). Leg in de volmachtovereenkomst vast welk AI-gebruik is toegestaan en wie verantwoordelijk is."},
    {"v": "Wat verandert er voor kredietadviseurs door de nieuwe Consumentenkredietrichtlijn?",
     "a": "Richtlijn (EU) 2023/2225 geldt vanaf 20 november 2026. Bij een geautomatiseerde kredietwaardigheidsbeoordeling heeft de consument recht op menselijke tussenkomst, een uitleg en het geven van zijn standpunt. Controleer de stand van de Nederlandse implementatie."},
]
