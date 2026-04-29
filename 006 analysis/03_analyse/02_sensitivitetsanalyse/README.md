# 02 Sensitivitetsanalyse

Denne aktiviteten analyserer hvordan total modellkostnad endres når proxykostnaden for ekstern/ukjent bunkring varieres.

Analysen er en smal én-veis proxysensitivitet. Den varierer ikke tankkapasitet, første ROB, modellhavnpriser eller havnetilgjengelighet. Slike flerveis- eller parameterutvidelser er parkert som mulig etterarbeid.

Sensitivitetsanalysen kjøres med:

`uv run python "03_analyse/02_sensitivitetsanalyse/src/run_route_inventory_sensitivity.py"`

Skriptet leser sensitivitetsfilen fra den operative hovedmodellen:

`006 analysis/02_modellutvikling/04_implementere_modell/output/res_route_inventory_proxy_sensitivity.csv`

Basisscenarioet er proxyfaktor `1,25`, som skal matche basiskjøringen i `03_analyse/01_basiskjoring`.

Hovedfunnet er at kjøpsplanen er stabil i de tre scenarioene. Proxyprisen ligger over prisene i modellhavnene, slik at analysen primært viser kostnadssensitivitet for ekstern/ukjent bunkring, ikke endringer i anbefalt kjøpsplan.

Sensitivitetsfilen genereres av hovedmodellskriptet i `02_modellutvikling/04_implementere_modell`. Endring av proxyfaktorene må derfor gjøres der før denne analyseaktiviteten kjøres på nytt.

## Kontroller

- sensitivitetsfilen skal inneholde proxyfaktorene `1,10`, `1,25` og `1,50`
- basisscenarioet `1,25` skal stemme med basiskjøringens totale modellkostnad
- hver rad skal ha konsistent total- og eksternkostnad
- alle outputfiler og figurer skal være skrevet med ikke-null filstørrelse

## Resultatfiler

- `src/run_route_inventory_sensitivity.py`: reproduserbart skript for sensitivitetsanalyse.
- `output/res_sensitivity_route_inventory_summary.json`: maskinlesbar oppsummering.
- `output/res_sensitivity_route_inventory_scenarios.csv`: scenarioer med endring mot basiskjøring.
- `metadata/res_sensitivity_route_inventory_summary.md`: norsk oppsummering.
- `figures/fig_sensitivity_total_cost.png`: total modellkostnad per proxyfaktor.
- `figures/fig_sensitivity_cost_components.png`: kostnad i prisede havner og ekstern/ukjent kostnad per proxyfaktor.
