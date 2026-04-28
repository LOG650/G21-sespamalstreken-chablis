# Basiskjøring for modellen

Basiskjøringen bruker samme solver-uavhengige beslutningslogikk som modelltesten: for hver måned legges observert månedlig behov til billigste tilgjengelige havn i modellgrunnlaget.

## Resultat

- Antall måneder: 61
- Havnene i modellgrunnlaget: P001, P002, P003, P004
- Historisk kostnad i modellgrunnlaget: 498,813,531.26
- Beregnet kostnad i basiskjøring: 473,953,291.65
- Estimert differanse mot historisk praksis: 24,860,239.60
- Estimert differanse i prosent: 4.98 %

## Valgt havn per antall måneder

| Havn | Antall måneder valgt |
| --- | ---: |
| P001 | 2 |
| P002 | 14 |
| P003 | 44 |
| P004 | 1 |

## Filer

- `006 analysis/03_analyse/01_basiskjoring/output/res_baseline_model_v1_by_month.csv`
- `006 analysis/03_analyse/01_basiskjoring/output/res_baseline_model_v1_by_port.csv`
- `006 analysis/03_analyse/01_basiskjoring/output/res_baseline_model_v1_summary.json`

## Tolkning

Basiskjøringen er et kontrollert standardscenario for modellen. Resultatene skal brukes videre som sammenligningsgrunnlag i sensitivitetsanalysen og senere resultattolkning.
