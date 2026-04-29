# Sensitivitetsanalyse for operasjonell hovedmodell

Analysen viser hvordan total modellkostnad endres når proxykostnaden for ekstern/ukjent bunkring varierer. Basisscenarioet er proxyfaktor 1,25 og skal stemme med basiskjøringen.

Dette er en smal én-veis proxysensitivitet. Kjøps- og eksternmengdene er stabile i alle tre scenarioer, slik at analysen primært dokumenterer kostnadseffekten av ekstern/ukjent proxypris, ikke endringer i anbefalt kjøpsplan.

## Nøkkeltall

- Scenarioer: 3
- Laveste total modellkostnad: 24,679,387.90
- Høyeste total modellkostnad: 29,869,459.58
- Kostnadsspenn: 5,190,071.68
- Basisscenario total modellkostnad: 26,625,664.78

## Scenarioer

| external_price_multiplier | external_price | total_model_cost | cost_change_vs_baseline | cost_change_pct_vs_baseline | priced_cost | external_cost | model_purchase_qty | model_external_qty | external_share_of_consumption |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1.1 | 671.32 | 24679387.9 | -1946276.88 | -0.073098 | 10406690.7 | 14272697.2 | 18857.451 | 21260.619 | 0.468863 |
| 1.25 | 762.86 | 26625664.78 | 0.0 | 0.0 | 10406690.7 | 16218974.08 | 18857.451 | 21260.619 | 0.468863 |
| 1.5 | 915.44 | 29869459.58 | 3243794.8 | 0.12183 | 10406690.7 | 19462768.88 | 18857.451 | 21260.619 | 0.468863 |

## Kontroller

| check | status | value | expected |
| --- | --- | --- | --- |
| Forventede proxyfaktorer finnes | OK | [1.1, 1.25, 1.5] | [1.1, 1.25, 1.5] |
| Basisscenario stemmer med basiskjøring | OK | 26625664.78 | 26625664.78 |
| Alle scenarioer har konsistent totalkostnad | OK | 0 | 0 |
| Alle scenarioer har konsistent eksternkostnad | OK | 0 | 0 |
| Kjøps- og eksternmengde er stabil på tvers av scenarioer | OK | 0 | 0 |
| Outputfil er skrevet: 006 analysis/03_analyse/02_sensitivitetsanalyse/output/res_sensitivity_route_inventory_summary.json | OK | skrevet | skrevet |
| Outputfil er skrevet: 006 analysis/03_analyse/02_sensitivitetsanalyse/output/res_sensitivity_route_inventory_scenarios.csv | OK | skrevet | skrevet |
| Outputfil er skrevet: 006 analysis/03_analyse/02_sensitivitetsanalyse/metadata/res_sensitivity_route_inventory_summary.md | OK | skrevet | skrevet |
| Outputfil er skrevet: 006 analysis/03_analyse/02_sensitivitetsanalyse/figures/fig_sensitivity_total_cost.png | OK | skrevet | skrevet |
| Outputfil er skrevet: 006 analysis/03_analyse/02_sensitivitetsanalyse/figures/fig_sensitivity_cost_components.png | OK | skrevet | skrevet |
