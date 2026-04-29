# Status fase 2

Oppdatert: 2026-04-29

## Innhold

- [Kort status](#kort-status)
- [Modellutvikling](#modellutvikling)
- [Implementering](#implementering)
- [Validering](#validering)
- [Analyse](#analyse)
- [Neste steg](#neste-steg)

## Kort status

Prosjektet har nå én operasjonell hovedmodell for minimering av drivstoffkostnader. Modellen bruker voyage-etapper, forbruk, ROB, tankkapasitet og tilgjengelige prisede modellhavner direkte. Modellarbeidet er samlet i `006 analysis/02_modellutvikling`, med implementeringen i `04_implementere_modell`.

## Modellutvikling

| Aktivitet | Status | Fil |
| --- | --- | --- |
| Definere variabler | Fullført | `006 analysis/02_modellutvikling/01_definere_variabler/README.md` |
| Formulere målfunksjon | Fullført | `006 analysis/02_modellutvikling/02_formulere_malfunksjon/README.md` |
| Definere restriksjoner | Fullført | `006 analysis/02_modellutvikling/03_definere_restriksjoner/README.md` |
| Implementere modell | Fullført | `006 analysis/02_modellutvikling/04_implementere_modell` |
| Teste modell | Fullført | `006 analysis/02_modellutvikling/05_teste_modell/README.md` |

## Implementering

Hovedmodellen er implementert i:

`006 analysis/02_modellutvikling/04_implementere_modell/src/run_route_inventory_model.py`

Modellen løses med `scipy.optimize.linprog` og genererer disse resultatfilene:

- `output/res_route_inventory_summary.json`
- `output/res_route_inventory_by_vessel.csv`
- `output/res_route_inventory_by_leg.csv`
- `output/res_route_inventory_purchases.csv`
- `output/res_route_inventory_proxy_sensitivity.csv`
- `metadata/res_route_inventory_summary.md`

Implementeringen beregner bunkringsmengde i prisede modellhavner, beholdning etter hver etappe og ekstern/ukjent bunkring når ruten ikke kan dekkes fullt ut av prisgrunnlaget.

## Validering

Siste modellkjøring: 2026-04-29.

| Kontrollpunkt | Resultat |
| --- | ---: |
| Rader i etapperesultat | 486 |
| Negativ modellert sluttbeholdning | 0 |
| Modellert sluttbeholdning over tankkapasitet | 0 |
| Beholdning før etappeforbruk over tankkapasitet | 0 |
| Kjøp i prisede modellhavner uten tilgjengelig priset modellhavn | 0 |

Hovedresultatet fra kjøringen er samlet modellkostnad 26 625 664,78, med 18 857,451 enheter bunkret i prisede modellhavner og 21 260,619 enheter ekstern/ukjent bunkring.

Modelltesten er kjørt med `006 analysis/02_modellutvikling/05_teste_modell/src/test_route_inventory_model.py`. Testen bestod 35 av 35 kontroller. Den validerer både intern konsistens i modellresultatene og kobling mot inputdata for etapper, forbruk, første ROB, første lagerbalanse per fartøy, kapasitet, tilgjengelige prisede havner, prisgrunnlag og forventede sensitivitetsfaktorer. Oppsummeringen er lagret i:

- `006 analysis/02_modellutvikling/05_teste_modell/output/res_route_inventory_test_summary.json`
- `006 analysis/02_modellutvikling/05_teste_modell/metadata/res_route_inventory_test_summary.md`

## Analyse

| Aktivitet | Status | Fil |
| --- | --- | --- |
| Basiskjøring | Fullført | `006 analysis/03_analyse/01_basiskjoring/README.md` |
| Sensitivitetsanalyse | Neste steg | `006 analysis/03_analyse/02_sensitivitetsanalyse` |

Ny basiskjøring er gjennomført med `006 analysis/03_analyse/01_basiskjoring/src/run_baseline_route_inventory.py`. Aktiviteten bruker hovedscenarioet fra den operative rute- og beholdningsmodellen med ekstern proxyfaktor 1,25, og skriver rapportvennlige aggregater per fartøyfil, modellhavn og måned.

Basiskjøringen er oppdatert etter review med interne konsistenssjekker mot modellens sammendrag, eksplisitt sjekk av hovedscenarioets proxyfaktor, kildefil-hash i JSON-oppsummeringen, nøytral metadata uten hardkodet tolkning, synlig nullrad for modellhavner uten kjøp og en rapportkoblet figur for månedlig fordeling mellom kjøp i prisede havner og ekstern/ukjent bunkring.

Resultatene er lagret i:

- `006 analysis/03_analyse/01_basiskjoring/output/res_baseline_route_inventory_summary.json`
- `006 analysis/03_analyse/01_basiskjoring/output/res_baseline_route_inventory_by_vessel.csv`
- `006 analysis/03_analyse/01_basiskjoring/output/res_baseline_route_inventory_by_port.csv`
- `006 analysis/03_analyse/01_basiskjoring/output/res_baseline_route_inventory_by_month.csv`
- `006 analysis/03_analyse/01_basiskjoring/figures/fig_baseline_monthly_split.png`
- `006 analysis/03_analyse/01_basiskjoring/metadata/res_baseline_route_inventory_summary.md`

## Neste steg

- Viderefør analysefasen med sensitivitetsanalyse og resultattolkning basert på den operative hovedmodellen og ny basiskjøring.
- Oppdater rapporten dersom senere modellkjøringer endrer hovedresultatene.
