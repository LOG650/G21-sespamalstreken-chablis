# Analysearbeid i `006 analysis`

Denne mappen er organisert etter hovedfasene og aktivitetene i prosjektplanen.

## Hovedstruktur

- `01_datagrunnlag`: aktiviteter knyttet til datainnsamling, datavask, strukturering og deskriptiv analyse
- `02_modellutvikling`: aktiviteter knyttet til variabler, målfunksjon, restriksjoner, implementering og testing av modell
- `03_analyse`: aktiviteter for basiskjøring, sensitivitetsanalyse og resultattolkning
- `_shared`: valgfritt område for delte hjelpemoduler eller maler

## Felles analysemiljø

Hele `006 analysis` bruker ett felles `uv`-prosjekt:

- `pyproject.toml`
- `uv.lock`

## Prinsipp

Hver aktivitetsmappe skal så langt som mulig skille mellom:

- `src`: skript og kode
- `input` eller `data`: inputfiler og strukturerte data
- `output`, `figures`, `tables` eller `metadata`: resultater, figurer, tabeller og dokumentasjon
