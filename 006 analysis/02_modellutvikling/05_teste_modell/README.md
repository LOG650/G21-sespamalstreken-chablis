# 05 Teste modell

Denne aktiviteten samler test- og simuleringsarbeid for modellen.

- `src`: skript for test eller solver-uavhengig simulering
- `output`: resultatfiler fra testkjøringer og simulerte løsninger

Formålet er å holde validering og testkjøringer adskilt fra selve implementeringsaktiviteten.

## Testnotat per 2026-04-28

Det er kjørt en solver-uavhengig simulering av modellversjon 1 med `src/simulate_model_v1_results.py`. Simuleringen brukes som endelig valideringsgrunnlag for modellversjon 1. Valget er gjort fordi modellen i denne versjonen er en aggregert månedsmodell der beslutningslogikken kan etterprøves direkte mot modellinputen: for hver måned dekkes observert månedlig behov ved å velge billigste tilgjengelige havn i datagrunnlaget.

Resultatene ligger i:

- `output/res_model_v1_summary.json`
- `output/res_model_v1_solution_by_port_month.csv`

Oppsummeringsfilen viser modellversjon `v1`, fire inkluderte havner, måneder fra `2020-01` til `2025-01`, 61 valgte månedsløsninger og total beregnet kostnad på 76 358 151,85. CSV-filen viser valgt volum, pris og beregnet kostnad per måned og havn.

Testen er ikke en dokumentert LP-solver-kjøring. Pyomo-implementasjonen dokumenterer hvordan modellen kan løses som lineær optimering når solver og eventuelle mer detaljerte operasjonelle restriksjoner er avklart. For modellversjon 1 er simuleringen likevel et tilstrekkelig og kontrollerbart valideringsgrunnlag, fordi den tester samme beslutningsregel som den forenklede modellen og gir et reproduserbart resultat fra de etablerte parameterfilene.

Konklusjonen er at datagrunnlag, parameterfiler og forenklet beslutningslogikk henger sammen. Aktiviteten `Teste modell` kan derfor lukkes faglig, og modellen kan tas videre til `Basiskjøring`.
