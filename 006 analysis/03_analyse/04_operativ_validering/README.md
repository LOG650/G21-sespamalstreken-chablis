# 04 Operativ validering

Denne aktiviteten sammenligner modellens bunkringsbeslutninger med observerte ROB-baserte bunkringshendelser i de strukturerte voyage-dataene for 2025.

Valideringen bruker eksisterende data og er ikke en full økonomisk backtest mot faktiske innkjøpskostnader. Formålet er å kontrollere om modellens bunkringsmengder, hendelser og beholdningsutvikling ligger i en operativt rimelig størrelsesorden sammenlignet med observert praksis.

Analysen kjøres med:

`uv run python "03_analyse/04_operativ_validering/src/validate_against_observed_bunkering.py"`

## Datagrunnlag

- `01_datagrunnlag/03_strukturering_av_datasett/data/tab_voyage_legs_2025.csv`
- `02_modellutvikling/04_implementere_modell/output/res_route_inventory_by_leg.csv`

Observerte bunkringshendelser hentes fra feltet `bunkering_inferred`. For disse hendelsene estimeres observert bunkringsmengde fra ROB-endring og forbruk per etappe:

`max(0, ROB_slutt - ROB_start + forbruk)`

## Resultatfiler

- `output/res_operational_validation_summary.json`: maskinlesbar oppsummering.
- `output/res_operational_validation_by_vessel.csv`: valideringsmål per fartøyfil.
- `output/res_operational_validation_by_leg.csv`: valideringsmål per etappe.
- `metadata/res_operational_validation_summary.md`: norsk tolkningsnotat.
