# 01 Basiskjøring

Denne aktiviteten inneholder standardkjøring av modellversjon 1 med pris-/volumdatasettet som primær modellinput.

Basiskjøringen bruker solver-uavhengig simulering: månedlig behov legges til billigste tilgjengelige havn i modellgrunnlaget. Dette er samme beslutningslogikk som ble validert i `006 analysis/02_modellutvikling/05_teste_modell`, men resultatene lagres her som analysegrunnlag.

## Struktur

- `src/run_baseline_model_v1.py`: kjører basiskjøringen
- `output/res_baseline_model_v1_by_month.csv`: månedlig resultat med historisk kostnad, modellkostnad og estimert differanse
- `output/res_baseline_model_v1_by_port.csv`: aggregert valgt mengde og kostnad per havn
- `output/res_baseline_model_v1_summary.json`: maskinlesbar oppsummering
- `metadata/res_baseline_model_v1_summary.md`: kort norsk oppsummering av basiskjøringen

## Kjøring

```powershell
python "006 analysis\03_analyse\01_basiskjoring\src\run_baseline_model_v1.py"
```
