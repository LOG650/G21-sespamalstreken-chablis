# Review: Sensitivitetsanalyse (final)

Reviewer: Claude (uavhengig subagent)
Dato: 2026-04-29
Aktivitet: `006 analysis/03_analyse/02_sensitivitetsanalyse`
Forrige review: samme fil, overskrevet.

## 1. Sammendrag

Aktiviteten er nå klar for lukking. Begge hovedpunktene fra forrige runde er løst, og den ene gjenstående mindre observasjonen om manglende én-veis-merknad i rapporten er også adressert. Det eneste som *ikke* er fjernet er den kosmetiske dobbeltskrivingen av `summary` til JSON i skriptet, men dette er funksjonelt korrekt og ikke blokkerende. Tall, figurer og dokumentasjon er konsistente på tvers av kode, metadata og rapport.

## 2. Oppsummert status fra tidligere runder

- **A. Smal scenariodekning** — *akseptert/dokumentert avgrensning*. Tre proxyfaktorer (1,10, 1,25, 1,50). Eksplisitt parkert i README linje 5, metadata-md linje 5 og rapport linje 470 som mulig etterarbeid. Ikke utvidet teknisk.
- **B. Figurreferanse i rapporten** — *løst*. `fig_sensitivity_cost_components.png` er referert som Figur 8.1 i kapittel 8.3 (rapport linje 568-571) med korrekt HTML-mønster. Begge sensitivitetsfigurene (7.2 og 8.1) er nå koblet inn.
- **Mindre: dobbeltskriving av summary** — *ikke løst*. Skriptet skriver fortsatt `SENSITIVITY_SUMMARY_JSON` på linje 411-414 og igjen på linje 426-429. Funksjonelt riktig (andre skriving inkluderer outputfilkontrollene), men stilistisk overflødig. Ikke blokkerende.
- **Mindre: én-veis-merknad i rapport kapittel 6.6** — *løst*. Rapport linje 470 sier nå: «Sensitivitetsanalysen er avgrenset til en én-veis variasjon av proxykostnaden for ekstern/ukjent bunkring. Den tester ikke separate endringer i tankkapasitet, første ROB, modellhavnpriser eller havnetilgjengelighet.» Plasseringen i kapittel 6.6 «Avgrensninger» er korrekt.

## 3. Styrker i ferdigstilt versjon

- **Komplett dokumentasjonskjede.** Kjernebegrensningen (én-veis proxysensitivitet, kjøpsplan stabil per design) er nå beskrevet med samme ordlyd i README, metadata-md og rapport (kapittel 6.6, 7.3 og 8.3). En leser av rapporten alene får nå avgrensningen tydelig allerede i metodekapitlet.
- **Robust skript.** Alle ti kontroller er grønne i siste kjøring (summary.json linje 34-103). Skjemavalidering på baseline-summarien (linje 92-101 + 108-112) gir presise feilmeldinger. sha256 og mtime spores for både modellsensitivitet og baseline-summary.
- **Annoterte figurer.** `write_figures` skriver nå totalkostnad i mill. på hvert datapunkt (linje 266-274 og 293-301), noe som gjør figurene mer leservennlige i rapporten.
- **Konsistente tall.** Scenariotabellene i metadata-md, scenarios.csv og rapport (Tabell 8.3, Tabell C.1, kapittel 7.3) viser identiske verdier ned til siste desimal.

## 4. Åpen etterarbeid (dokumentert)

Følgende er parkert som mulig etterarbeid og er nevnt i README/metadata:

- Utvidelse til flerveis-sensitivitet (tankkapasitet `K_v`, første ROB `I_{v,0}`, modellhavnpriser, havnetilgjengelighet) — README linje 5, metadata-md linje 5, rapport linje 470.
- Finere proxyfaktor-rutenett (f.eks. 0,8–2,0 i steg på 0,1) for å finne en eventuell terskel — implisitt åpent gjennom samme avgrensning.

Ingen av punktene blokkerer lukking.

## 5. Sjekk mot prosjektregler

- **Norsk:** Bestått. README, metadata, rapportkapitler og kontrollnavn er konsekvent på norsk.
- **UTF-8 uten BOM, korrekte æ/ø/å:** Bestått. «kjøpsplanen», «én-veis», «proxyfaktor», «første ROB» gjengis korrekt.
- **Filnavn-prefiks:** Bestått. `res_sensitivity_*` og `fig_sensitivity_*` følger prosjektmønsteret.
- **HTML-figurmønster:** Bestått. Begge figurer bruker sentrert `<div>`, `width="80%"`, `<small><i>` figurtekst og figurnummer.
- **Aktivitetsmappestruktur:** Bestått. `src/`, `output/`, `metadata/` og `figures/` er alle under aktiviteten.

## 6. Konsistens med rapporten

- **Tall stemmer:** Verifisert. 1,10 → 24 679 387,90; 1,25 → 26 625 664,78; 1,50 → 29 869 459,58. Ekstern pris 762,86 ved 1,25; kostnad i prisede havner 10 406 690,70 i alle scenarioer; kjøp 18 857,45 og ekstern 21 260,62 stabilt. Identisk i scenarios.csv, summary.json, metadata-md, Tabell 8.3 og Tabell C.1.
- **Figurer korrekt referert:** Bestått. Figur 7.2 (`fig_sensitivity_total_cost.png`, rapport linje 503-506) og Figur 8.1 (`fig_sensitivity_cost_components.png`, rapport linje 568-571).
- **Metodekapittel beskriver én-veis-naturen:** Bestått. Kapittel 6.6 (linje 470) gjør avgrensningen eksplisitt.

## 7. Endelig konklusjon

**Aktiviteten kan lukkes.** Alle hoved- og småpunkter fra tidligere runder er enten løst eller dokumentert som parkert. Den eneste reelle gjenstående observasjonen er den kosmetiske dobbeltskrivingen av summary i `run_route_inventory_sensitivity.py` (linje 411-414 og 426-429), som er stilistisk og ikke påvirker resultater eller kontroller. Anbefalt opprydding ved senere anledning, men ikke nødvendig for å markere aktiviteten som ferdig.
