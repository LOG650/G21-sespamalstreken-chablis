# Review: Basiskjøring (final)

Reviewer: Claude (uavhengig subagent)
Dato: 2026-04-29
Aktivitet: `006 analysis/03_analyse/01_basiskjoring`
Omfang: kun basiskjøring som standalone aktivitet.

## 1. Sammendrag

Aktiviteten er nå ferdigstilt. Det siste blokkerende punktet fra forrige runde — å koble figuren `fig_baseline_monthly_split.png` til rapporten med prosjektets HTML-mønster — er løst. Figuren er referert i kapittel 7.1 (linje 484-487) med riktig sentrering, `width="80%"` og kursiv figurtekst. Nøkkeltallene i rapporten stemmer fortsatt eksakt mot baseline-artefaktene, og README dokumenterer eksplisitt at aktiviteten er en aggregering, ikke en ny solver-kjøring. Aktiviteten er klar til å lukkes.

## 2. Oppsummert status fra tidligere runder

- A. Navngiving — **akseptert designvalg** (aggregeringsaktivitet). README linje 5 dokumenterer eksplisitt at "Basiskjøringen er ikke en ny solver-kjøring", og brukeren har bevisst latt navnet stå.
- B. Intern konsistenssjekk — **løst**. Tre numeriske sjekker pluss skjema-/proxyfaktor- og outputfilkontroll, alle med status `OK` i nåværende kjøring.
- C. Tolkning i metadata — **løst**. `res_baseline_route_inventory_summary.md` slutter med konsistenssjekk-tabellen, ingen tolkende formuleringer.
- D. Figur i rapporten — **løst**. Referert i `005 report/rapport.md` linje 484-487 i kapittel 7.1 med korrekt HTML-mønster og figurnummer 7.1.
- E. Antagelser i README — **løst**. README linje 5 lister prisproxy, ekstern/ukjent bunkring, `ROB_Fuel_Total` og tankkapasitet som arvede antagelser.

## 3. Styrker i ferdigstilt versjon

- Figuren er plassert direkte etter avsnittet om dekning fra prisede modellhavner (rapport linje 478-482), som er det faglig riktige stedet — figuren visualiserer nettopp den månedlige kontrasten mellom kjøp i prisede havner og ekstern/ukjent bunkring som diskuteres i avsnittet.
- HTML-mønsteret følger CLAUDE.md eksakt: `<div align="center">`, `width="80%"`, `<p align="center">` med `<small><i>` for figurtekst, og kort kursiv figurtekst med figurnummer.
- Konsistenssjekkene er nå tiendelt: fire numeriske/proxyfaktor-sjekker pluss seks outputfil-sjekker (`output/...` og `figures/...`), alle synliggjort i både JSON og metadata-md.
- Skriptet (`run_baseline_route_inventory.py`) kaster `RuntimeError` hvis `external_price_multiplier != 1.25`, slik at baseline-filene ikke kan endres taust ved en annen modellkjøring (linje 396-405).
- README linje 19 forklarer eksplisitt at `weighted_avg_actual_purchase_price` er vektet snittpris for faktiske modellkjøp, og at `P002` beholdes som rad med null kjøp — to av de tidligere "kommunikasjonsrisikoene" er adressert.
- Alle outputfiler er kontrollert med `path.exists() and path.stat().st_size > 0` (skript linje 354-368), og eksistenssjekken er en del av konsistenssjekk-tabellen.

## 4. Åpen etterarbeid (dokumentert)

- Aktiviteten er en aggregeringsaktivitet, ikke en ny solver-kjøring. Dette er en akseptert designvalg, dokumentert i README linje 5 og i metadata-md linje 3.
- `generated_at` settes ved hver kjøring (idempotensutfordring fra tidligere review). Ikke blokkerende; kildefil-`sha256` gir reell sporbarhet uavhengig av tidsstempel.

## 5. Sjekk mot prosjektregler

- **Norsk språk**: README, metadata-md, skript-output og figurakser/legend er på norsk. Bestått.
- **UTF-8 uten BOM**: alle skriveoperasjoner bruker eksplisitt `encoding="utf-8"` og `ensure_ascii=False` for JSON. Bestått.
- **Æ/ø/å**: korrekt brukt i `Basiskjøring`, `kjøp`, `prisede havner`, `månedlig`, `fartøyfiler`. Bestått.
- **Filnavn**: alle resultatfiler har `res_baseline_*`-prefiks, figuren har `fig_baseline_*`-prefiks. Bestått.
- **HTML-figurmønster i rapporten**: rapport linje 484-487 følger mønsteret eksakt (`<div align="center">`, `width="80%"`, kursiv figurtekst i `<small><i>`, kort figurtekst). Bestått.

## 6. Konsistens med rapporten

Alle sentrale tall i rapport kapittel 7 og 8 stemmer fortsatt eksakt mot baseline-filene (verifisert direkte mot `res_baseline_route_inventory_summary.json`):

- Linje 480: 486 etapper, 42 etapper, 28 etapper — matcher `leg_count`, `priced_leg_count`, `purchased_leg_count`.
- Linje 482: forbruk 45 345,04, kjøp 18 857,45 (41,59 %), ekstern 21 260,62 (46,89 %) — matcher.
- Linje 497: proxypris 762,86, total kostnad 26 625 664,78, priset 10 406 690,70, ekstern 16 218 974,08 — matcher.

Figuren er korrekt referert: `../006%20analysis/03_analyse/01_basiskjoring/figures/fig_baseline_monthly_split.png` med `Figur 7.1` og kort kursiv figurtekst.

## 7. Endelig konklusjon

**Aktiviteten kan lukkes nå.** Alle blokkerende punkter fra tidligere runder er løst. Figuren er korrekt integrert i rapporten med prosjektets HTML-mønster og riktig figurnummer, konsistenssjekkene kjører grønt, README dokumenterer arvede antagelser, og rapporttall matcher baseline-artefaktene eksakt. Det aksepterte designvalget om at aktiviteten er en aggregering (ikke ny solver-kjøring) er tydelig dokumentert og skal ikke telle som svakhet. Ingen gjenstående blokkere.
