# Test av operasjonell hovedmodell

Status: bestått
Antall kontroller: 35
Feilede kontroller: 0

| Kontroll | Status | Verdi | Forventet |
| --- | --- | ---: | ---: |
| Alle modellresultatfiler finnes | OK | `[]` | `[]` |
| Antall etapper stemmer med sammendrag | OK | `486` | `486` |
| Antall fartøyfiler stemmer med sammendrag | OK | `8` | `8` |
| Alle fartøyløsninger er optimale | OK | `8 optimale løsninger` | `Optimization terminated successfully. (HiGHS Status 7: Optimal)` |
| Antall etapper stemmer med inputdata | OK | `486` | `486` |
| Ingen dupliserte fartøy-etapper | OK | `0` | `0` |
| Alle output-etapper finnes i inputdata | OK | `0` | `0` |
| Etapperekkefølge er kronologisk per fartøy | OK | `0` | `0` |
| Forbruk per etappe stemmer med inputdata | OK | `0` | `0` |
| Første ROB per fartøy stemmer med inputdata | OK | `0` | `0` |
| Første lagerbalanse per fartøy stemmer direkte med inputdata | OK | `0` | `0` |
| Kapasitet per etappe stemmer med kapasitetstabell | OK | `0` | `0` |
| Tilgjengelige prisede havner stemmer med inputdata | OK | `0` | `0` |
| Ingen negativ sluttbeholdning | OK | `0` | `0` |
| Ingen sluttbeholdning over kapasitet | OK | `0` | `0` |
| Ingen beholdning før forbruk over kapasitet | OK | `0` | `0` |
| Lagerbalansen holder på etappenivå | OK | `0` | `0` |
| Ingen kjøp uten tilgjengelig priset modellhavn | OK | `0` | `0` |
| Antall etapper med kjøp stemmer med sammendrag | OK | `28` | `28` |
| Antall kjøpsrader stemmer med sammendrag | OK | `28` | `28` |
| Kjøpsmengde stemmer mellom etapper og kjøpsfil | OK | `0.0` | `0` |
| Kjøpsmengde stemmer med sammendrag | OK | `18857.451` | `18857.451` |
| Ekstern mengde stemmer med sammendrag | OK | `21260.619` | `21260.619` |
| Totalkostnad per fartøy stemmer med sammendrag | OK | `26625664.78` | `26625664.78` |
| Kostnad i prisede havner stemmer med sammendrag | OK | `10406690.7` | `10406690.7` |
| Kjøpshavn finnes blant prisede havner på samme etappe | OK | `0` | `0` |
| Alle kjøpspriser er positive | OK | `0` | `0` |
| Kjøpskostnad stemmer med mengde ganger pris | OK | `0` | `0` |
| Kjøpspriser stemmer med prisdata | OK | `0` | `0` |
| Prisgrunnlag for kjøp stemmer med sammendrag | OK | `{'historical_port_average': 25, 'monthly_observation': 3}` | `{'historical_port_average': 25, 'monthly_observation': 3}` |
| Sensitivitetsfil har forventede proxyfaktorer | OK | `[1.1, 1.25, 1.5]` | `[1.1, 1.25, 1.5]` |
| Sensitivitetsfil har forventet antall rader | OK | `3` | `3` |
| Sensitivitetsrader har konsistent totalkostnad | OK | `0` | `0` |
| Sensitivitetsrader har konsistent eksternkostnad | OK | `0` | `0` |
| Hovedscenario i sensitivitetsfil stemmer med sammendrag | OK | `26625664.78` | `26625664.78` |
