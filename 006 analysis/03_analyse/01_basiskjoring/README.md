# 01 Basiskjøring

Denne aktiviteten dokumenterer hovedscenarioet fra den operative rute- og beholdningsmodellen som basiskjøring for analysefasen.

Basiskjøringen er ikke en ny solver-kjøring. Den er en reproduserbar aggregering av allerede løst hovedscenario fra `02_modellutvikling/04_implementere_modell`, og arver derfor modellens antagelser om prisproxy, ekstern/ukjent bunkring, `ROB_Fuel_Total` og tankkapasitet.

Basiskjøringen kjøres med:

`uv run python "03_analyse/01_basiskjoring/src/run_baseline_route_inventory.py"`

Skriptet leser modellresultater fra:

`006 analysis/02_modellutvikling/04_implementere_modell/output`

Hovedscenarioet bruker `external_price_multiplier = 1,25`. Andre proxyfaktorer håndteres i egen sensitivitetsanalyse.

Ved kjøring overskrives tidligere baseline-artefakter i denne aktivitetsmappen. Skriptet skriver samtidig konsistenssjekker og kildefilenes `mtime`/`sha256` til `output/res_baseline_route_inventory_summary.json`, slik at en leser kan se hvilken modellkjøring baseline bygger på.

`weighted_avg_actual_purchase_price` i havnetabellen er vektet gjennomsnittspris for faktiske modellkjøp i basiskjøringen. Den er ikke det samme som historisk havnesnitt i modellens prisgrunnlag. Modellhavner uten kjøp, som `P002` i gjeldende basiskjøring, beholdes som rader med null kjøp for å vise at havnen var del av modellsettet, men ikke valgt i hovedscenarioet.

## Kontroller

- sum av kostnad i prisede havner per havn skal stemme med modellens sammendrag
- sum av total modellkostnad per fartøy skal stemme med modellens sammendrag
- sum av kjøpsmengde per måned skal stemme med modellens sammendrag
- kildefilene må ha forventede kolonner før aggregering gjennomføres
- hovedscenarioet må ha `external_price_multiplier = 1,25`
- alle outputfiler må være skrevet med ikke-null filstørrelse

## Resultatfiler

- `src/run_baseline_route_inventory.py`: reproduserbart skript for basiskjøring og aggregering.
- `output/res_baseline_route_inventory_summary.json`: maskinlesbar oppsummering av basiskjøringen.
- `output/res_baseline_route_inventory_by_vessel.csv`: resultater aggregert per fartøyfil.
- `output/res_baseline_route_inventory_by_port.csv`: kjøp aggregert per priset modellhavn.
- `output/res_baseline_route_inventory_by_month.csv`: forbruk, kjøp, ekstern/ukjent bunkring og kostnad aggregert per måned.
- `figures/fig_baseline_monthly_split.png`: figur som viser månedlig kjøp i prisede havner og ekstern/ukjent bunkring.
- `metadata/res_baseline_route_inventory_summary.md`: norsk oppsummering for rapport- og statusarbeid.
