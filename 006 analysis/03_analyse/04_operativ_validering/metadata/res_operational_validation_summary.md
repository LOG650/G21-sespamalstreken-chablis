# Operativ validering mot observerte bunkringshendelser

Denne analysen sammenligner modellens bunkringsbeslutninger med observerte ROB-baserte bunkringshendelser i de strukturerte voyage-dataene for 2025.

Observert bunkringshendelse hentes fra `bunkering_inferred` i de strukturerte voyage-dataene. For slike hendelser estimeres observert bunkringsmengde som positiv økning i beholdning etter justering for forbruk på etappen: `max(0, ROB_slutt - ROB_start + forbruk)`. Dette gir en praktisk kontroll av modellens timing og volum, men ikke en full økonomisk backtest mot faktiske innkjøpspriser.

## Hovedtall

- Voyage-etapper: 486
- Observerte bunkringshendelser: 76
- Modellhendelser med bunkring: 89
- Overlappende hendelser: 16
- Event precision: 17,98 %
- Event recall: 21,05 %
- Estimert observert bunkringsmengde: 39 879,61
- Modellert total bunkringsmengde: 40 118,07
- Modellert mengde som andel av observert estimat: 100,60 %
- Gjennomsnittlig absolutt avvik mellom modellert sluttbeholdning og observert ROB-slutt: 476,06

## Tolkning

Modellen treffer ikke nødvendigvis de samme bunkringstidspunktene som observert praksis, fordi den er formulert som en kostnadsminimerende beslutningsmodell og ikke som en modell for å gjenskape historiske beslutninger. Avvik mellom observerte og modellerte hendelser er derfor forventet.

Valideringen er likevel nyttig fordi den viser om modellens samlede bunkringsmengde og beholdningsutvikling ligger i en operativt rimelig størrelsesorden. Dersom modellen hadde gitt svært få hendelser, ekstremt høye mengder eller systematiske brudd mot observert beholdningsnivå, ville det indikert svakere operativ relevans.

## Resultat per fartøyfil

| Fartøyfil | Observerte hendelser | Modellhendelser | Overlapp | Observert mengde | Modellert mengde | Modell/observert | Beholdningsavvik MAE |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| C001-1 | 8 | 14 | 2 | 5 468,62 | 5 645,65 | 103,24 % | 605,47 |
| C001-2 | 13 | 14 | 3 | 7 956,05 | 7 099,35 | 89,23 % | 651,21 |
| C002-1 | 10 | 7 | 1 | 5 195,94 | 6 710,84 | 129,16 % | 497,22 |
| C003-1 | 11 | 14 | 4 | 4 163,47 | 3 947,76 | 94,82 % | 370,40 |
| C004-1 | 12 | 9 | 1 | 6 782,63 | 4 963,38 | 73,18 % | 630,71 |
| C004-2 | 9 | 9 | 2 | 4 178,30 | 4 854,44 | 116,18 % | 484,45 |
| C004-3 | 9 | 10 | 3 | 5 476,80 | 4 974,15 | 90,82 % | 423,00 |
| C005-1 | 4 | 12 | 0 | 657,80 | 1 922,50 | 292,26 % | 256,66 |

<p align="center" style="font-size: 0.9em;"><small><i>Tabell V.1 Operativ validering av modellert bunkring mot observerte ROB-baserte bunkringshendelser.</i></small></p>
