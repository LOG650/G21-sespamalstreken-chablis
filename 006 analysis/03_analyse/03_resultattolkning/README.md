# 03 Resultattolkning

Denne aktiviteten samler tolkbare hovedfunn fra basiskjøring og sensitivitetsanalyse.

Etter review er aktiviteten utvidet med programmatisk validering av om kjøpsplanen er stabil i sensitivitetsanalysen, beregning av restandel fra startbeholdning og beholdningsflyt, skille mellom observasjoner og tolkning, og egne konsistenssjekker i tolkningsnotatet.

Aktiviteten er lukket etter review og oppdatering av rapport- og statuskoblinger.

Resultattolkningen kjøres med:

`uv run python "03_analyse/03_resultattolkning/src/interpret_route_inventory_results.py"`

Skriptet leser resultater fra:

- `03_analyse/01_basiskjoring/output`
- `03_analyse/02_sensitivitetsanalyse/output`

## Resultatfiler

- `src/interpret_route_inventory_results.py`: reproduserbart skript for resultattolkning.
- `output/res_route_inventory_interpretation.json`: maskinlesbar oppsummering av tolkbare funn.
- `metadata/res_route_inventory_interpretation.md`: norsk tolkningsnotat med hovedfunn, tolkning og konsistenssjekker.
