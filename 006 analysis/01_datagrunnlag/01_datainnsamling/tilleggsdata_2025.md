# Tilleggsdata 2025

Denne filen dokumenterer supplerende operative data mottatt etter den første datavasken av pris- og volumdatasettet.

## Kilder

Tilleggsdataene ligger i `004 data`:

- `C001 - 1.csv`
- `C001 - 2.csv`
- `C002 - 1.csv`
- `C003 - 1.csv`
- `C004 - 1.csv`
- `C004 - 2.csv`
- `C004 - 3.csv`
- `C005 - 1.csv`

Filene er anonymisert. IMO-nummer og fartøynavn er fjernet, og fartøyene er kategorisert etter fartøyklasse. Voyage-kodene er UN/Locode, der de to første bokstavene representerer landet havnen ligger i.

## Foreløpig omfang

| Fil | Rader | Periode | Antall voyage | ROB min | ROB maks |
| --- | ---: | --- | ---: | ---: | ---: |
| C001 - 1.csv | 492 | 2025-01-01 til 2025-12-30 | 32 | 146,5 | 1385,69 |
| C001 - 2.csv | 479 | 2025-01-01 til 2025-12-30 | 30 | 58,5 | 1581,5 |
| C002 - 1.csv | 471 | 2025-01-01 til 2025-12-30 | 27 | 267,7 | 1466,77 |
| C003 - 1.csv | 456 | 2025-01-01 til 2025-12-30 | 22 | 137,3 | 1089,39 |
| C004 - 1.csv | 476 | 2025-01-01 til 2025-12-30 | 28 | 208,77 | 1402,26 |
| C004 - 2.csv | 474 | 2025-01-01 til 2025-12-30 | 28 | 327,33 | 1632,34 |
| C004 - 3.csv | 497 | 2025-01-01 til 2025-12-30 | 35 | 104,3 | 1195,4 |
| C005 - 1.csv | 548 | 2025-01-01 til 2025-12-30 | 46 | 88,4 | 787,1 |

<p align="center" style="font-size: 0.9em;"><small><i>Tabell: Foreløpig teknisk oversikt over de åtte supplerende 2025-filene.</i></small></p>

Samlet inneholder tilleggsdataene 3893 rapporteringsrader, 69 unike UN/Locode-havnekoder og 26 landprefiks. Filene inneholder blant annet dato, rapporttype, seilt distanse, tidsbruk, voyage fra/til, voyage-nummer, forbruksfelt og `ROB_Fuel_Total`.

## Oppgitt bunkerskapasitet

| Fartøyklasse | Bunkerskapasitet |
| --- | --- |
| C001 | 2,087.006 m3 |
| C002 | 2,061.430 m3 |
| C003 | 1,533.719 m3 |
| C004 | 1,907.080 m3 |
| C005 | 1,024.531 m3 |

Tallene er oppgitt som verifiserte 2025-tall fra dataleverandøren.

## Kontraktsinformasjon

Dataleverandøren har oppgitt at selskapet har bunkerskontrakt i Singapore og Sør-Korea, samt kontrakt på VLSFO i Rotterdam.

I modellarbeidet bør dette foreløpig behandles som supplerende operativ kontekst. Før kontraktene brukes som restriksjoner eller prisparametere, må det avklares hvilke havnekoder, drivstofftyper, tidsperioder og prisvilkår kontraktene gjelder for.

## Foreløpig vurdering

Tilleggsdataene svarer på flere av databehovene som tidligere ble identifisert i rapportutkastet:

- tankkapasitet per anonymisert fartøyklasse
- historisk forbruk per fartøyfil og voyage
- beholdningsfelt gjennom `ROB_Fuel_Total`
- havnesekvens gjennom `Voyage_From`, `Voyage_To` og `Voyage_Number`
- kontraktskontekst for Singapore, Sør-Korea og Rotterdam

## Strukturert modellgrunnlag

Tilleggsdataene er strukturert videre i `006 analysis/01_datagrunnlag/03_strukturering_av_datasett` med skriptet `src/structure_voyage_data_2025.py`.

Følgende modellklare tabeller er generert:

- `data/tab_voyage_events_2025.csv`: 3893 rapporteringsrader med klasse, fil-ID, dato/tid, voyage, havn, forbruk, ROB og kontraktsflagg.
- `data/tab_voyage_legs_2025.csv`: 486 aggregerte voyage-etapper med samlet distanse, varighet, forbruk, start-/slutt-ROB og tilgjengelige havner.
- `data/tab_vessel_class_capacity.csv`: oppgitt bunkerskapasitet per anonymisert fartøyklasse.

Kolonneforklaring og kvalitetskontroller ligger i `metadata/tab_voyage_structure_guide.md`. Foreløpig kontroll viser 3 etapper med manglende ROB og ingen flaggede kapasitetsbrudd mot oppgitt bunkerskapasitet.
