# Basiskjøring av operasjonell hovedmodell

Basiskjøringen dokumenterer hovedscenarioet fra den operative rute- og beholdningsmodellen. Scenarioet bruker ekstern proxyfaktor 1,25 og resultatfilene fra `04_implementere_modell` som kilde.

## Nøkkeltall

- Fartøyfiler: 8
- Etapper: 486
- Etapper med priset modellhavn tilgjengelig: 42
- Etapper med modellert kjøp i priset modellhavn: 28
- Samlet forbruk: 45,345.04
- Modellert kjøp i prisede havner: 18,857.45
- Ekstern/ukjent bunkring: 21,260.62
- Kostnad i prisede havner: 10,406,690.70
- Kostnad for ekstern/ukjent bunkring: 16,218,974.08
- Total modellkostnad: 26,625,664.78

## Per fartøyfil

| vessel_file_id | vessel_class | leg_count | priced_leg_count | purchased_leg_count | total_consumption | model_purchase_qty | model_external_qty | priced_share_of_consumption | external_share_of_consumption | total_model_cost |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| C001-1 | C001 | 63 | 3 | 3 | 6354.45 | 316.2 | 5329.45 | 0.0498 | 0.8387 | 4248109.53 |
| C001-2 | C001 | 57 | 16 | 11 | 7173.35 | 6961.16 | 138.19 | 0.9704 | 0.0193 | 3966878.77 |
| C002-1 | C002 | 53 | 12 | 6 | 7256.64 | 5754.57 | 956.27 | 0.793 | 0.1318 | 3856017.66 |
| C003-1 | C003 | 44 | 3 | 2 | 4537.68 | 1896.12 | 2051.64 | 0.4179 | 0.4521 | 2659264.59 |
| C004-1 | C004 | 55 | 3 | 3 | 5809.9 | 1945.63 | 3017.75 | 0.3349 | 0.5194 | 3354416.95 |
| C004-2 | C004 | 55 | 5 | 3 | 5743.17 | 1983.77 | 2870.67 | 0.3454 | 0.4998 | 3279766.98 |
| C004-3 | C004 | 68 | 0 | 0 | 6074.55 | 0.0 | 4974.15 | 0.0 | 0.8189 | 3794603.06 |
| C005-1 | C005 | 91 | 0 | 0 | 2395.3 | 0.0 | 1922.5 | 0.0 | 0.8026 | 1466607.24 |

## Per modellhavn

| port | purchase_count | purchase_qty | priced_cost | weighted_avg_actual_purchase_price |
| --- | --- | --- | --- | --- |
| P001 | 1 | 565.6 | 320090.01 | 565.93 |
| P002 | 0 | 0.0 | 0.0 | 0.0 |
| P003 | 15 | 13441.28 | 7287615.34 | 542.18 |
| P004 | 12 | 4850.57 | 2798985.35 | 577.04 |

## Per måned

| period_month | leg_count | priced_leg_count | purchased_leg_count | model_purchase_qty | model_external_qty | total_model_cost |
| --- | --- | --- | --- | --- | --- | --- |
| 2025-01 | 49 | 9 | 3 | 1868.1 | 234.43 | 1221359.98 |
| 2025-02 | 29 | 3 | 3 | 3447.25 | 1334.88 | 2882757.07 |
| 2025-03 | 39 | 7 | 5 | 4055.14 | 1983.06 | 3706002.14 |
| 2025-04 | 47 | 0 | 0 | 0.0 | 3253.06 | 2481644.39 |
| 2025-05 | 43 | 6 | 4 | 3457.18 | 2589.93 | 3845561.66 |
| 2025-06 | 45 | 3 | 2 | 1896.12 | 130.53 | 1193720.02 |
| 2025-07 | 34 | 2 | 0 | 0.0 | 3096.7 | 2362363.64 |
| 2025-08 | 40 | 1 | 1 | 1179.21 | 5175.48 | 4585958.44 |
| 2025-09 | 34 | 0 | 0 | 0.0 | 1005.07 | 766732.34 |
| 2025-10 | 52 | 6 | 5 | 2170.71 | 975.59 | 1996834.61 |
| 2025-11 | 30 | 0 | 0 | 0.0 | 1162.16 | 886570.76 |
| 2025-12 | 44 | 5 | 5 | 783.75 | 319.72 | 696159.72 |

## Konsistenssjekker

| check | status | value | expected |
| --- | --- | --- | --- |
| Basiskjøring bruker hovedscenarioets proxyfaktor | OK | 1.25 | 1.25 |
| Kostnad i prisede havner per havn stemmer med sammendrag | OK | 10406690.7 | 10406690.7 |
| Total modellkostnad per fartøy stemmer med sammendrag | OK | 26625664.78 | 26625664.78 |
| Kjøpsmengde per måned stemmer med sammendrag | OK | 18857.46 | 18857.45 |
| Outputfil er skrevet: 006 analysis/03_analyse/01_basiskjoring/output/res_baseline_route_inventory_summary.json | OK | skrevet | skrevet |
| Outputfil er skrevet: 006 analysis/03_analyse/01_basiskjoring/output/res_baseline_route_inventory_by_vessel.csv | OK | skrevet | skrevet |
| Outputfil er skrevet: 006 analysis/03_analyse/01_basiskjoring/output/res_baseline_route_inventory_by_port.csv | OK | skrevet | skrevet |
| Outputfil er skrevet: 006 analysis/03_analyse/01_basiskjoring/output/res_baseline_route_inventory_by_month.csv | OK | skrevet | skrevet |
| Outputfil er skrevet: 006 analysis/03_analyse/01_basiskjoring/figures/fig_baseline_monthly_split.png | OK | skrevet | skrevet |
| Outputfil er skrevet: 006 analysis/03_analyse/01_basiskjoring/metadata/res_baseline_route_inventory_summary.md | OK | skrevet | skrevet |
