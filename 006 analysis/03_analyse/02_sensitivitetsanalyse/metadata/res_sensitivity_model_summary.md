# Sensitivitetsanalyse for modellen

Sensitivitetsanalysen bruker samme beslutningslogikk som basiskjøringen: månedlig behov legges til billigste tilgjengelige havn i modellgrunnlaget. Scenarioene endrer priser og/eller etterspørsel, mens tilgjengelighet og historisk sammenligningsgrunnlag holdes fast.

## Referanse

- Antall måneder: 61
- Havnene i modellgrunnlaget: P001, P002, P003, P004
- Historisk kostnad: 498,813,531.26
- Basiskostnad modell: 473,953,291.65

## Største kostnadsøkninger mot basis

| Scenario | Endring mot basis | Endring i prosent |
| --- | ---: | ---: |
| stress_price_demand_+10pct | 99,530,191.25 | 21.00 % |
| price_all_+10pct | 47,395,329.17 | 10.00 % |
| demand_all_+10pct | 47,395,329.17 | 10.00 % |
| price_all_+5pct | 23,697,664.58 | 5.00 % |
| demand_all_+5pct | 23,697,664.58 | 5.00 % |

## Største kostnadsreduksjoner mot basis

| Scenario | Endring mot basis | Endring i prosent |
| --- | ---: | ---: |
| stress_price_demand_-10pct | -90,051,125.41 | -19.00 % |
| demand_all_-10pct | -47,395,329.17 | -10.00 % |
| price_all_-10pct | -47,395,329.17 | -10.00 % |
| price_P003_-10pct | -42,900,536.07 | -9.05 % |
| price_P002_-10pct | -30,826,133.17 | -6.50 % |

## Filer

- `006 analysis/03_analyse/02_sensitivitetsanalyse/output/res_sensitivity_model_scenarios.csv`
- `006 analysis/03_analyse/02_sensitivitetsanalyse/output/res_sensitivity_model_by_month.csv`
- `006 analysis/03_analyse/02_sensitivitetsanalyse/output/res_sensitivity_model_summary.json`
