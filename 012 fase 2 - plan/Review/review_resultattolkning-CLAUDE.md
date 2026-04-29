# Review: Resultattolkning (oppdatert)

Reviewer: Claude (uavhengig subagent)
Dato: 2026-04-29
Aktivitet: `006 analysis/03_analyse/03_resultattolkning`
Omfang: ny gjennomgang etter at brukeren har forsøkt å rette opp svakhetene fra forrige review.

## 1. Sammendrag

Aktiviteten er klart løftet siden forrige runde. Skriptet er utvidet med faktisk programmatisk verifisering av plan-stabilitet, en eksplisitt beregning av dekning fra startbeholdning, en konsistenssjekk-blokk på linje med basiskjøring og sensitivitetsanalyse, samt en tydelig "Tolkning"-seksjon i Markdown-notatet som kobler tallene til datagapsdiagnose, beholdningsflyt og proxyantagelser. Tallene matcher fortsatt kildefilene eksakt og er konsistente med rapporten. De tre hovedsvakhetene som forrige review pekte på (A: manglende reell tolkning, B: hardkodet `plan_stable_in_tested_scenarios`, C: manglende eksplisitt datagapskobling) er alle reelt adressert. Aktiviteten kan etter min vurdering lukkes.

## 2. Status på tidligere svakheter

### A. Manglende reell tolkning — **løst**

Notatet `res_route_inventory_interpretation.md` har nå en egen `## Tolkning`-seksjon (linje 32-40) som leverer faktiske tolkninger og ikke bare tabellpunkter. De fire forventede elementene er dekket:

- **Ekstern/ukjent som kvantitativ datagapsdiagnose:** Notat linje 36 — "Ekstern/ukjent bunkring på 46,89 % bør tolkes som en kvantitativ diagnose av datagapet i prisgrunnlaget, ikke som et eget operativt havnevalg". Dette er direkte forankret i tallet og bruker ordet "datagap" eksplisitt.
- **Dekning fra startbeholdning (~11,5 %):** Notat linje 12 ("Startbeholdning og beholdningsflyt dekker den resterende andelen på 11,53 %") og linje 38 ("Den resterende dekningsandelen på 11,53 % kommer fra startbeholdning og beholdningsflyt gjennom ruten"). Beregnet i koden linje 98-103 som `1 - priced_share - external_share`, som gir 1 - 0,415866 - 0,468863 = 0,115271.
- **Kostnadsdriver-analyse:** Notat linje 28 — "Ekstern/ukjent kostnad utgjør 60,91 % av total modellkostnad i basisscenarioet". Dette tallet beregnes i kode linje 104 (`external_cost / baseline_cost` = 16 218 974,08 / 26 625 664,78 = 0,6091). Forrige review etterlyste nettopp at "ekstern proxy er den dominerende kostnadskomponenten" skulle verbaliseres — det er nå gjort både som tallrapport og som tolkningssetning.
- **Usikkerhetshåndtering:** Notat linje 40 — "Proxyfaktor 1,25 er en arbeidsantagelse for ekstern/ukjent bunkring. Sensitivitetsanalysen er en smal én-veis analyse av denne antagelsen, og terskelen på 80 % brukes bare som en arbeidsdefinisjon for å identifisere fartøy der ekstern/ukjent bunkring dominerer kraftig." Dette dekker både proxyantakelsen, énveis-karakteren og 80 %-terskelvalget som forrige review etterlyste.

### B. Hardkodet `plan_stable_in_tested_scenarios = True` — **løst**

Skriptet beregner nå flagget faktisk fra scenariodataene. `interpret_route_inventory_results.py` linje 92-94:

```python
purchase_qty_values = unique_rounded(scenarios, "model_purchase_qty")
external_qty_values = unique_rounded(scenarios, "model_external_qty")
plan_stable = len(purchase_qty_values) == 1 and len(external_qty_values) == 1
```

`unique_rounded` (linje 52-53) avrunder til 6 desimaler og samler unike verdier i et sett. Flagget settes deretter på linje 203 i JSON-strukturen, og legges samtidig inn som to separate konsistenssjekker (linje 107-118). I `res_sensitivity_route_inventory_scenarios.csv` har alle tre rader `model_purchase_qty=18857.451` og `model_external_qty=21260.619`, så flagget evalueres korrekt til `True`. Dersom kjøpsplanen i fremtiden endres mellom scenarier, vil flagget automatisk bli `False` og notatets stabilitetssetning byttes ut via `stable_text` (linje 222-226).

### C. Datagapskoblingen mangler i tolkningsartefaktet — **løst**

Forrige review pekte på at rapport linje 510 ("kvantitativ diagnose av datagapet") ble forankret i tallene fra notatet, men ikke i selve notatets formuleringer. Dette er nå rettet. Notat linje 36 sier eksplisitt at "Ekstern/ukjent bunkring på 46,89 % bør tolkes som en kvantitativ diagnose av datagapet i prisgrunnlaget, ikke som et eget operativt havnevalg." Formuleringen speiler rapport linje 600 ("Ekstern/ukjent bunkring må tolkes som et datagap, ikke som et nytt havnevalg") nesten ord for ord, og rapport linje 510 har dermed nå direkte støtte i tolkningsartefaktet.

## 3. Nye styrker

- **Konsistenssjekker på linje med basis og sensitivitet.** Kode linje 106-141 og JSON linje 72-107 leverer fem eksplisitte sjekker (kjøpsmengde unik, ekstern mengde unik, kostnadsspenn, dekningsandeler ikke over 1, minst ett fartøy med høy ekstern andel). Dette løfter aktiviteten opp på samme dokumentasjonsnivå som `01_basiskjoring` og `02_sensitivitetsanalyse`, og var ett av forbedringspunktene i forrige review.
- **Kostnadsandel for ekstern bunkring eksponert.** `external_cost_share_of_total = 0,6091` (JSON linje 63) er en helt ny tolkbar nøkkelfigur som ikke fantes i forrige iterasjon. Den knytter tolkningen til kostnadsdrivervurderingen.
- **Dekningsregnskapet er fullført.** `inventory_share_of_consumption` (JSON linje 17) lukker de manglende ~11,5 % og gjør at de tre dekningsandelene nå summerer til 100 % av forbruket. Dette gjør dekningsbildet komplett i selve artefaktet.
- **Egen "Hovedfunn"/"Fartøy og havner"/"Sensitivitet"/"Tolkning"/"Konsistenssjekker"-struktur.** Notatet er nå klart strukturert i seksjoner som speiler skillet mellom observasjon og tolkning som CLAUDE.md ber om.
- **Modul-docstring og funksjonsdocstrings.** Skriptet (linje 1, 66, 212) har nå korte docstrings for modulen og de to hovedfunksjonene. Konsistent med forrige reviews lavprioriterte forslag.
- **Tre fartøy-vinkler i stedet for én.** Forrige review påpekte at top eksternfartøy bare ble valgt på absolutt mengde. Skriptet rapporterer nå både `top_external_vessel` (på mengde) og `top_external_share_vessel` (på andel) — i dette datasettet er det samme fartøy (C001-1), men strukturen tåler fremtidige datasett der disse ikke faller sammen.
- **Generated_at i notatet.** Notat linje 5 ("Generert: 2026-04-29T21:56:21.762434+00:00") matcher metadatafilene i de andre aktivitetene og dekker forbedringspunkt 9 i forrige review.

## 4. Gjenstående svakheter

Ingen av de tre hovedsvakhetene står åpne lenger. Det jeg ser av reststøy er små:

- **Avrundingsterskel for "stabil plan" er fast.** `unique_rounded` bruker `digits=6` (linje 52). I dette datasettet er dette nok (kjøps- og eksternmengde er identiske ned til siste desimal i CSV-en), men dersom solveren senere skulle gi marginale numeriske forskjeller på 7. desimalplass ville sjekken kunne sl ut feilaktig som "ikke stabil". Dette er ikke en feil her og nå, men det kunne vært dokumentert at det er en avrundingsterskel.
- **README ble oppdatert, men listingen av filer dekker ikke `consistency_checks` eksplisitt.** README linje 5 nevner endringene generelt, og linje 18-20 viser de tre artefaktene. Det er greit, men en eksplisitt setning om at notatet og JSON-en inneholder eksplisitte konsistenssjekker hadde vært helt på linje med dokumentasjonsstilen i de andre aktivitetene. Lavt prioritert.
- **80 %-terskelen er fortsatt hardkodet i kode (linje 79) og forklart kun i notat-tolkningsdelen.** Det er greit — terskelen er nå begrunnet i tolkningsteksten — men en kort kommentar i koden ("# arbeidsdefinisjon: ekstern/ukjent dominans, jf. tolkningsnotat") ville gitt full sporbarhet.

Ingen av disse er blokkere for å lukke aktiviteten.

## 5. Eventuelle nye observasjoner

- **`top_external_vessel` og `top_external_share_vessel` peker på samme fartøy i dette datasettet.** Begge gir C001-1 (5 329,45 / 83,87 %). Strukturen i koden (linje 82-85) tåler at de er ulike, og det at de faller sammen her kommenteres ikke i notatet — det er heller ikke nødvendig.
- **Konsistenssjekken "Dekningsandeler overstiger ikke totalforbruk" rapporteres med summen 0,884729** (JSON linje 98). Dette er priset + ekstern, og restandelen på 11,53 % er korrekt komplementært. Sjekken er teknisk en "≤ 1"-sjekk, ikke en "= 1"-sjekk; det er rett valg fordi startbeholdning kan dekke positivt restbeløp, men aldri mer enn 1.
- **Sensitivitetstabellen i CSV (`res_sensitivity_route_inventory_scenarios.csv`) bekrefter strukturlikhet.** Alle tre rader har identisk `priced_cost = 10 406 690,70`, identisk `model_purchase_qty = 18857,451` og identisk `model_external_qty = 21260,619`. Plan-stabiliteten er dermed reelt verifisert i data, ikke bare i kode.
- **Top_purchase_port-rapportering tar med priset_cost.** JSON linje 50 (`"priced_cost": 7287615.34`) er ny informasjon i forhold til forrige iterasjon. Det binder havn-funn til kostnadssiden og gjør artefaktet noe rikere.

## 6. Sjekk mot prosjektregler (CLAUDE.md)

- **Norsk språk:** Bestått. Notat, README og JSON-feltinnhold er på norsk; engelske identifikatorer er kun maskinnavn.
- **UTF-8 uten BOM, æ/ø/å:** Bestått. "Kjøpsmengde", "Modellhavner", "håndteres", "fartøy", "også" leses korrekt i begge MD-artefakter og i JSON.
- **Filnavn-prefiks:** Bestått. JSON og MD bruker `res_`-prefiks; skriptet bruker verbformet `interpret_`-prefiks som er i tråd med søsteraktivitetenes `run_`-prefiks.
- **Aktivitetsmappestruktur:** Bestått. `src/`, `output/`, `metadata/` og README under aktiviteten.
- **Skille mellom resultat og tolkning:** Bestått nå. Notatet har egne seksjoner "Hovedfunn", "Fartøy og havner", "Sensitivitet" (rene observasjoner) og "Tolkning" (faktisk tolkning) — dette er i tråd med CLAUDE.md-regelen om at resultatpresentasjon og diskusjon skal skilles.
- **Konsistenssjekker:** Bestått nå. Skriptet leverer egen `consistency_checks`-blokk på linje med `01_basiskjoring` og `02_sensitivitetsanalyse`.

## 7. Konsistens med rapporten

- **Numerisk:** Alle tall i notat og JSON matcher rapporten linje for linje:
  - 42 av 486 etapper, 8,64 % (rapport linje 484, 532; baseline-summary linje 6-8).
  - 41,59 % priset andel og 46,89 % ekstern/ukjent andel (rapport linje 484, 539; baseline linje 13-14).
  - Kjøp 18 857,45, ekstern 21 260,62 (rapport linje 484, 614; baseline linje 11-12).
  - Total kostnad 26 625 664,78, priset kostnad 10 406 690,70, ekstern kostnad 16 218 974,08 (rapport linje 590, 614; baseline linje 15-17).
  - Kostnadsspenn 5 190 071,68, proxyfaktorer 1,1 og 1,5 (rapport linje 604; sensitivity linje 13-14, scenarios-CSV linje 2-4).
  - Ekstern kostnadsandel 60,91 % (rapport linje 590; tolkningsnotat linje 28; beregnet i kode linje 104).
  - Top kjøpsfartøy C001-2 og fartøy med ≥80 % ekstern andel C001-1, C004-3, C005-1 (rapport linje 600; notat linje 14; JSON linje 22-26).
  - Restdekning fra startbeholdning 11,53 % (rapport linje 484, 539 omtaler kvalitativt; tolkningsnotat linje 12, 38 har kvantitativ verdi).
- **Tekstlig forankring:** Bestått nå. Rapport linje 510 ("kvantitativ diagnose av datagapet") og linje 600 ("må tolkes som et datagap, ikke som et nytt havnevalg") har nå direkte motsvarighet i notat linje 36 ("kvantitativ diagnose av datagapet i prisgrunnlaget, ikke som et eget operativt havnevalg"). Rapport linje 604 ("kjøpsplanen er stabil i de testede scenarioene") matcher notat linje 30 og er nå reelt verifisert mot scenariodataene.

## 8. Konklusjon

**Forbedringene er tilstrekkelige til å lukke aktiviteten.** Alle tre hovedsvakhetene fra forrige runde (A: manglende reell tolkning, B: hardkodet plan-stabilitet, C: manglende eksplisitt datagapskobling) er reelt og verifiserbart løst. I tillegg er det flere sekundære forbedringer: konsistenssjekker, kostnadsandel for ekstern bunkring, fullført dekningsregnskap (priset + ekstern + startbeholdning = 100 %), seksjonsstruktur i notatet, docstrings i koden og dobbel fartøy-vinkel (mengde og andel). Tallene er fortsatt eksakt sporbare til kildene, og rapporten er konsistent med tolkningsartefaktet både numerisk og tekstlig. Anbefaling: marker aktiviteten som ferdig.
