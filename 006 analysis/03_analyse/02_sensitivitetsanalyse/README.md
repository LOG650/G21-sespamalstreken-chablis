# 02 Sensitivitetsanalyse

Denne aktiviteten dokumenterer sensitivitetsanalyse for modellen. Analysen bruker samme solver-uavhengige beslutningslogikk som basiskjøringen: for hver måned legges observert månedlig behov til billigste tilgjengelige havn i modellgrunnlaget.

## Formål

Formålet er å undersøke hvor følsom modellens beregnede kostnad er for endringer i pris og etterspørsel. Basiskjøringen brukes som referanse, mens historisk kostnad holdes fast som sammenligningsgrunnlag.

## Input

- `006 analysis/02_modellutvikling/04_implementere_modell/input/tab_model_v1_price_by_port_month.csv`
- `006 analysis/02_modellutvikling/04_implementere_modell/input/tab_model_v1_demand_by_month.csv`
- `006 analysis/02_modellutvikling/04_implementere_modell/input/tab_model_v1_availability_by_port_month.csv`
- `006 analysis/02_modellutvikling/04_implementere_modell/input/data_model_v1_parameters.json`
- `006 analysis/01_datagrunnlag/03_strukturering_av_datasett/data/tab_bunker_monthly_by_port.csv`

## Scenarioer

Analysen dekker 19 scenarioer:

- basis med opprinnelige priser og opprinnelig etterspørsel
- alle havnepriser endret med `-10 %`, `-5 %`, `+5 %` og `+10 %`
- hver enkelt havn endret med `-10 %` og `+10 %`
- samlet etterspørsel endret med `-10 %`, `-5 %`, `+5 %` og `+10 %`
- kombinerte stresscenarioer med pris og etterspørsel `+10 %` og `-10 %`

## Output

- `output/res_sensitivity_model_scenarios.csv`
- `output/res_sensitivity_model_by_month.csv`
- `output/res_sensitivity_model_summary.json`
- `output/tab_result_baseline_vs_historical.md`
- `output/tab_result_baseline_by_port.md`
- `output/tab_result_sensitivity_top_effects.md`
- `metadata/res_sensitivity_model_summary.md`
- `figures/fig_result_baseline_cost_comparison.png`
- `figures/fig_result_baseline_selected_ports.png`
- `figures/fig_result_sensitivity_tornado.png`

## Kjøring

Kjør fra repo-roten:

```powershell
python "006 analysis/03_analyse/02_sensitivitetsanalyse/src/run_sensitivity_model.py"
```

For å generere tabeller og figurer som brukes i rapporten:

```powershell
python "006 analysis/03_analyse/02_sensitivitetsanalyse/src/generate_result_tables_figures.py"
```

## Resultat

Basisscenarioet i sensitivitetsanalysen gir samme beregnede modellkostnad som basiskjøringen: `473 953 291,65`. Den største kostnadsøkningen oppstår i stresscenarioet der både pris og etterspørsel øker med 10 %, mens den største kostnadsreduksjonen oppstår når både pris og etterspørsel reduseres med 10 %.
