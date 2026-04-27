# 05 Teste modell

Denne aktiviteten samler test- og simuleringsarbeid for modellen.

- `src`: skript for test eller solver-uavhengig simulering
- `output`: resultatfiler fra testkjøringer og simulerte løsninger

Formålet er å holde validering og testkjøringer adskilt fra selve implementeringsaktiviteten.

## Testnotat per 2026-04-27

Det er kjørt en solver-uavhengig simulering av modellversjon 1 med `src/simulate_model_v1_results.py`. Simuleringen bruker samme hovedlogikk som den forenklede lineære modellen: for hver måned dekkes observert månedlig behov ved å velge billigste tilgjengelige havn i datagrunnlaget.

Resultatene ligger i:

- `output/res_model_v1_summary.json`
- `output/res_model_v1_solution_by_port_month.csv`

Oppsummeringsfilen viser modellversjon `v1`, fire inkluderte havner, måneder fra `2020-01` til `2025-01` og total beregnet kostnad på 76 358 151,85. CSV-filen viser valgt volum, pris og beregnet kostnad per måned og havn.

Testen er foreløpig en simulert kontroll, ikke en dokumentert LP-solver-kjøring. Den viser at datagrunnlag, parameterfiler og forenklet beslutningslogikk henger sammen, og at modellen kan tas videre til `Basiskjøring`. Før endelig modellvalidering bør det fortsatt dokumenteres om Pyomo-modellen kjøres med faktisk solver eller om simuleringen brukes som prosjektets kontrollerbare testgrunnlag.
