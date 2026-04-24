# Modellinput for modellversjon 1

Denne mappen inneholder modellparametere som hører til den forenklede modellversjon 1 beskrevet i `005 report/Kaylee_rapport.md`.

## Filer

- `tab_model_v1_price_by_port_month.csv`: prisparameter `p[h,t]`
- `tab_model_v1_demand_by_month.csv`: behovsparameter `D[t]`
- `tab_model_v1_availability_by_port_month.csv`: tilgjengelighetsparameter `f[h,t]`
- `data_model_v1_parameters.json`: samlet metadata og parameterbeskrivelse

## Definisjon

- Havner: P001, P002, P003, P004
- Perioder: 2020-01 til 2025-01
- Prisregel ved manglende observasjon: Hvis en havn mangler observasjon i en måned, brukes havnens vektede gjennomsnittspris over hele analyseperioden.
- Behovsregel: Månedlig behov settes lik samlet observert bunkret mengde på tvers av de fire havnene i perioden.
- Tilgjengelighetsregel: available_flag = 1 hvis havnen har observert transaksjon i måneden, ellers 0.

Filnavnene starter med `tab_model_v1_` eller `data_model_v1_` for å gjøre det enkelt å se at de tilhører modellversjon 1.
