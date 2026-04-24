# Figurguide for datagrunnlag

Disse figurene er laget fra renset og aggregert bunkringsdata og kan brukes direkte i rapportens casekapittel og datakapittel.

## Figurer

- `fig_bunker_total_qty_by_month.png`: viser total historisk bunkringsmengde per måned og egner seg i kapittel 4.2 om historisk utvikling.
- `fig_bunker_weighted_price_by_port_month.png`: viser prisutvikling per havn over tid og egner seg til å forklare geografiske prisforskjeller i casekapitlet.
- `fig_bunker_season_profile.png`: viser sesongprofil for både volum og pris og egner seg i kapittel 4.3 om sesongmønster.

## Kjøring

Bruk denne kommandoen fra repo-roten:

```powershell
uv run --project "006 analysis" python "006 analysis\01_datagrunnlag\generate_bunker_figures.py"
```

Figurene skrives til `006 analysis/01_datagrunnlag/figures`.
