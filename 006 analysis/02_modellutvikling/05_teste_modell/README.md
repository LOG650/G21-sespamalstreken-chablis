# 05 Teste modell

Denne aktiviteten brukes til validering av prosjektets operative hovedmodell.

Gjeldende validering kjøres med:

`uv run python "02_modellutvikling/05_teste_modell/src/test_route_inventory_model.py"`

Testen leser modellresultatene fra:

`006 analysis/02_modellutvikling/04_implementere_modell/output`

Testen leser også strukturerte inputdata fra:

`006 analysis/01_datagrunnlag/03_strukturering_av_datasett/data`

## Kontroller

| Kontrollkategori | Konkret dekning |
| --- | --- |
| Resultatfiler | alle modellresultatfiler finnes |
| Sammendrag | antall etapper, fartøyfiler, kjøpsrader, mengder og totalkostnader stemmer mellom detaljfiler og sammendrag |
| Solverstatus | alle fartøyløsninger har eksakt optimal HiGHS-status |
| Inputkobling | output-etapper, forbruk, første ROB, kapasitet og tilgjengelige prisede havner stemmer med strukturerte inputdata |
| Etapperekkefølge | fartøy-etapper er unike og kronologisk ordnet uten hull |
| Beholdning og kapasitet | sluttbeholdning blir ikke negativ, og beholdning før og etter forbruk overstiger ikke kapasitet |
| Lagerbalanse | lagerbalansen stemmer rad for rad på etappenivå, og første lagerbalanse per fartøy kontrolleres direkte mot inputdata |
| Kjøpslogikk | kjøp skjer bare i prisede havner som finnes på samme etappe, prisene er positive, kostnad stemmer med mengde og prisgrunnlag, og prisgrunnlaget stemmer med sammendraget |
| Sensitivitet | sensitivitetsfilen har forventede proxyfaktorer, alle rader har konsistent total- og eksternkostnad, og hovedscenarioet stemmer med samlet modellresultat |

Toleransen i kostnads- og prissjekker er 0,05 fordi modelloutput avrundes til 2 desimaler for kostnader/priser og 6 desimaler for mengder i CSV-filene.

Siste kjøring bestod 35 av 35 kontroller.

Åpent etterarbeid er parkert: en eventuell unit-test av selve LP-formuleringen kan vurderes ved senere refaktorering av modellfilen.

## Resultatfiler

- `src/test_route_inventory_model.py`: reproduserbart testskript
- `output/res_route_inventory_test_summary.json`: maskinlesbar testoppsummering
- `metadata/res_route_inventory_test_summary.md`: norsk testoppsummering

Resultatet av siste kontroll dokumenteres også i `012 fase 2 - plan/status.md`.
