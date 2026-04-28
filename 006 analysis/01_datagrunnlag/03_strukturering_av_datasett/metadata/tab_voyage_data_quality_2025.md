# Datakvalitet for voyage-data 2025

Denne kontrollen vurderer om de strukturerte voyage-dataene er klare for direkte modellbruk.

## Omfang

- Rapporteringsrader kontrollert: 3893
- Voyage-etapper kontrollert: 486
- Etapper med positivt forbruk og havnekobling: 486
- Etapper med inferert bunkring: 76
- Etapper med kontraktsflagg: 64

## Avvik

| Avvikstype | Antall |
| --- | ---: |
| `missing_rob` | 3 |
| `zero_consumption` | 40 |

## Alvorlighetsgrad

| Grad | Antall |
| --- | ---: |
| `low` | 40 |
| `medium` | 3 |

## Modellvurdering

- Pris- og volumdatasettet fra bunkringslisten bør fortsatt være primærkilde for modellversjon 1.
- Voyage-dataene er egnet som operasjonell støtte for forbruk, ROB, tankkapasitet og havnetilgjengelighet.
- Direkte bruk i en fartøybasert modell krever at kontraktsflagg og drivstofftypekobling valideres faglig før de brukes som harde restriksjoner.
- Avvikene er begrenset i omfang, men bør dokumenteres eksplisitt dersom voyage-dataene brukes i analyse eller resultatdrøfting.

Detaljerte avvik er lagret i `006 analysis/01_datagrunnlag/03_strukturering_av_datasett/data/tab_voyage_data_quality_issues_2025.csv`.
