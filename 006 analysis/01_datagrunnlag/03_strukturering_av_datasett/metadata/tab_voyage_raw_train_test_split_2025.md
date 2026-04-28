# Train/test-splitt av voyage-rådata 2025

Denne filen dokumenterer kronologisk 80/20-splitt av de åtte anonymiserte voyage-råfilene i `004 data`.

Splitten er laget på råfilnivå som grunnlag for eventuell separat train/test-rensing og -strukturering. Originalfilene er beholdt urørt, og nye filer er skrevet med suffiksene `_train_80.csv` og `_test_20.csv`.

## Metode

- Hver råfil er splittet separat.
- Radene er sortert etter kombinert `Date_UTC` og `Time_UTC`.
- De tidligste 80 % av radene er lagt i train.
- De siste 20 % av radene er lagt i test.
- Split-indeks er beregnet som `int(antall_rader * 0.8)`.

## Oppsummering

- Råfiler splittet: 8
- Totalt antall rå rader: 3893
- Totalt antall train-rader: 3110
- Totalt antall test-rader: 783

## Splitt per fil

| Kilde | Rå rader | Train-fil | Train-rader | Train-periode | Test-fil | Test-rader | Test-periode | Original urørt |
| --- | ---: | --- | ---: | --- | --- | ---: | --- | --- |
| `C001 - 1.csv` | 492 | `C001 - 1_train_80.csv` | 393 | 2025-01-01T16:00 til 2025-10-21T06:30 | `C001 - 1_test_20.csv` | 99 | 2025-10-22T06:30 til 2025-12-30T05:00 | ja |
| `C001 - 2.csv` | 479 | `C001 - 2_train_80.csv` | 383 | 2025-01-01T11:00 til 2025-10-17T05:50 | `C001 - 2_test_20.csv` | 96 | 2025-10-17T08:35 til 2025-12-30T18:00 | ja |
| `C002 - 1.csv` | 471 | `C002 - 1_train_80.csv` | 376 | 2025-01-01T08:00 til 2025-10-17T16:00 | `C002 - 1_test_20.csv` | 95 | 2025-10-17T23:06 til 2025-12-30T17:00 | ja |
| `C003 - 1.csv` | 456 | `C003 - 1_train_80.csv` | 364 | 2025-01-01T17:00 til 2025-10-12T12:00 | `C003 - 1_test_20.csv` | 92 | 2025-10-13T12:00 til 2025-12-30T18:00 | ja |
| `C004 - 1.csv` | 476 | `C004 - 1_train_80.csv` | 380 | 2025-01-01T17:00 til 2025-10-18T19:00 | `C004 - 1_test_20.csv` | 96 | 2025-10-18T22:15 til 2025-12-30T16:00 | ja |
| `C004 - 2.csv` | 474 | `C004 - 2_train_80.csv` | 379 | 2025-01-01T17:00 til 2025-10-18T16:00 | `C004 - 2_test_20.csv` | 95 | 2025-10-19T16:00 til 2025-12-30T04:00 | ja |
| `C004 - 3.csv` | 497 | `C004 - 3_train_80.csv` | 397 | 2025-01-01T18:00 til 2025-10-25T17:00 | `C004 - 3_test_20.csv` | 100 | 2025-10-26T17:00 til 2025-12-30T16:00 | ja |
| `C005 - 1.csv` | 548 | `C005 - 1_train_80.csv` | 438 | 2025-01-01T15:00 til 2025-10-20T05:06 | `C005 - 1_test_20.csv` | 110 | 2025-10-20T05:30 til 2025-12-30T15:00 | ja |
