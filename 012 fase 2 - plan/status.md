# Status fase 2

Oppdatert: 2026-04-30

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
| Sensitivitetsanalyse | Fullført | `006 analysis/03_analyse/02_sensitivitetsanalyse/README.md` |
| Resultattolkning | Lukket | `006 analysis/03_analyse/03_resultattolkning/README.md` |
| Operativ validering | Fullført | `006 analysis/03_analyse/04_operativ_validering/README.md` |

Ny basiskjøring er gjennomført med `006 analysis/03_analyse/01_basiskjoring/src/run_baseline_route_inventory.py`. Aktiviteten bruker hovedscenarioet fra den operative rute- og beholdningsmodellen med ekstern proxyfaktor 1,25, og skriver rapportvennlige aggregater per fartøyfil, modellhavn og måned.

Basiskjøringen er oppdatert etter review med interne konsistenssjekker mot modellens sammendrag, eksplisitt sjekk av hovedscenarioets proxyfaktor, kildefil-hash i JSON-oppsummeringen, nøytral metadata uten hardkodet tolkning, synlig nullrad for modellhavner uten kjøp og en rapportkoblet figur for månedlig fordeling mellom kjøp i prisede havner og ekstern/ukjent bunkring.

Resultatene er lagret i:

- `006 analysis/03_analyse/01_basiskjoring/output/res_baseline_route_inventory_summary.json`
- `006 analysis/03_analyse/01_basiskjoring/output/res_baseline_route_inventory_by_vessel.csv`
- `006 analysis/03_analyse/01_basiskjoring/output/res_baseline_route_inventory_by_port.csv`
- `006 analysis/03_analyse/01_basiskjoring/output/res_baseline_route_inventory_by_month.csv`
- `006 analysis/03_analyse/01_basiskjoring/figures/fig_baseline_monthly_split.png`
- `006 analysis/03_analyse/01_basiskjoring/metadata/res_baseline_route_inventory_summary.md`

Sensitivitetsanalyse er gjennomført med `006 analysis/03_analyse/02_sensitivitetsanalyse/src/run_route_inventory_sensitivity.py`. Analysen bruker proxyfaktorene 1,10, 1,25 og 1,50 for ekstern/ukjent bunkring, og bekrefter at basisscenarioet 1,25 stemmer med basiskjøringen. Total modellkostnad varierer fra 24 679 387,90 til 29 869 459,58, med et kostnadsspenn på 5 190 071,68.

Sensitivitetsanalysen er lukket etter review. Aktiviteten dokumenterer eksplisitt at analysen er en smal én-veis proxysensitivitet, og begge figurene er koblet inn i rapporten.

Resultatene er lagret i:

- `006 analysis/03_analyse/02_sensitivitetsanalyse/output/res_sensitivity_route_inventory_summary.json`
- `006 analysis/03_analyse/02_sensitivitetsanalyse/output/res_sensitivity_route_inventory_scenarios.csv`
- `006 analysis/03_analyse/02_sensitivitetsanalyse/figures/fig_sensitivity_total_cost.png`
- `006 analysis/03_analyse/02_sensitivitetsanalyse/figures/fig_sensitivity_cost_components.png`
- `006 analysis/03_analyse/02_sensitivitetsanalyse/metadata/res_sensitivity_route_inventory_summary.md`

Resultattolkning er gjennomført med `006 analysis/03_analyse/03_resultattolkning/src/interpret_route_inventory_results.py`. Tolkningsnotatet samler hovedfunn om datadekning, fartøyforskjeller, havnefordeling og proxyfølsomhet.

Resultattolkningen er oppdatert etter review og senere anvendbarhetsarbeid. Skriptet validerer nå programmatisk at kjøpsmengde og ekstern/ukjent mengde er stabile i proxy-scenarioene, beregner restandel fra startbeholdning og beholdningsflyt, rapporterer ekstern kostnadsandel, skiller tydeligere mellom observasjon og tolkning, skriver egne konsistenssjekker i tolkningsnotatet, klassifiserer fartøyfiler etter operativ anvendbarhet og beregner en enkel prisnivå-sensitivitet for modellhavnene.

Aktiviteten er lukket etter review og oppdatering av rapport- og statuskoblinger.

Kapittel 8 i `005 report/rapport.md` er fylt ut med hovedresultat, resultat per fartøyfil, anvendbarhetsklassifisering, resultat per modellhavn og sensitivitetsresultat. Tabellnummereringen er oppdatert slik at anvendbarhetsklassifiseringen er Tabell 8.3, havnefordelingen er Tabell 8.4 og proxy-sensitivitetsanalysen er Tabell 8.5.

Kapittel 8 i `005 report/rapport.md` er videre utvidet med anvendbarhetsklassifisering per fartøyfil og prisnivå-sensitivitet for modellhavnene. Kapittel 9 Diskusjon og kapittel 10 Konklusjon er oppdatert med vurdering av funnene opp mot problemstilling, modellbegrensninger, datadekning og praktisk bruk for Odfjell Tankers.

Resultatene er lagret i:

- `006 analysis/03_analyse/03_resultattolkning/output/res_route_inventory_interpretation.json`
- `006 analysis/03_analyse/03_resultattolkning/output/res_route_inventory_applicability_by_vessel.csv`
- `006 analysis/03_analyse/03_resultattolkning/output/res_route_inventory_price_level_sensitivity.csv`
- `006 analysis/03_analyse/03_resultattolkning/metadata/res_route_inventory_interpretation.md`

Operativ validering er gjennomført med `006 analysis/03_analyse/04_operativ_validering/src/validate_against_observed_bunkering.py`. Analysen sammenligner modellens bunkringshendelser og totale bunkringsmengder med observerte ROB-baserte bunkringshendelser i voyage-dataene. Valideringen viser 76 observerte bunkringshendelser, 89 modellhendelser og 16 overlappende hendelser. Samlet modellert bunkringsmengde er 40 118,07 mot et observert ROB-basert estimat på 39 879,61, altså 100,60 % av observert estimat. Dette er lagt inn i kapittel 7.4 i rapporten.

Resultatene er lagret i:

- `006 analysis/03_analyse/04_operativ_validering/output/res_operational_validation_summary.json`
- `006 analysis/03_analyse/04_operativ_validering/output/res_operational_validation_by_vessel.csv`
- `006 analysis/03_analyse/04_operativ_validering/output/res_operational_validation_by_leg.csv`
- `006 analysis/03_analyse/04_operativ_validering/metadata/res_operational_validation_summary.md`

## Neste steg

- Sammendrag, abstract og innholdsfortegnelse er oppdatert slik at de samsvarer med ferdig analyse, diskusjon og konklusjon.
- Kapittel 1-5 er kontrollert mot den operative hovedmodellen og justert slik at metode, teori, case og data omtaler voyage-data, ROB, forbruk, tankkapasitet, modellhavner og ekstern/ukjent bunkring konsistent med valgt modellvei.
- Kapittel 5 presiserer nå at train/test-splitten brukes som datadisiplin og mulig senere robusthetskontroll, ikke som klassisk evaluering av en prediktiv modell.
- Kapittel 5.1 er oppdatert med en eksplisitt metodeoversikt som navngir datavask, deskriptiv analyse, lineær programmering, konsistenskontroll, sensitivitetsanalyse og anvendbarhetsklassifisering som metodene brukt i rapporten.
- Rapportteksten er ryddet slik at datagrunnlaget omtales med utgangspunkt i rådata; konkrete henvisninger til prosesserte datafiler og interne analyseartefakter er fjernet fra brødteksten.
- Publiseringsavtalen er rettet med korrekt henvisning til åndsverkloven, og `003 references/Åndsverkloven.md` er lagt til som kildenotat.
- Egenerklæringen er oppdatert med en presisering av at studentene har ansvar for faglige valg og kvalitetssikring, mens KI er brukt som verktøy for analyse, koding og dokumentasjon.
- Personvern-, helseforsknings- og publiseringsfeltene i rapportens innledende skjema er fylt ut: NSD/Sikt nei, REK nei, elektronisk publisering nei, og oppgaven er markert som båndlagt/konfidensiell i henhold til avtale med Odfjell Tankers.
- Helhetlig rapportrevisjon etter egenvurdering v2 er gjennomført i `005 report/rapport.md`. Revisjonen forklarer ekstern/ukjent bunkring ved første nevning, utvider litteraturkapitlet med peer-reviewed bunkrings- og refueling-litteratur, legger inn validitet/reliabilitet/etikk i metodekapitlet, rydder kapittel 7/8, flytter modellbidrag til diskusjonen, presiserer proxyfaktor 1,25 og $t(l)$, fjerner interne implementeringsfeltnavn fra rapporttekst, og utvider konklusjonen med begrensninger og videre arbeid.
- Nye peer-reviewed kilder fra rapportrevisjonen er lagt inn som egne Markdown-filer i `003 references`, én fil per referanse, med kort relevansvurdering, DOI og bibliografioppføring.
- Neste arbeidssteg er en siste formell innleveringskontroll av forsidefelter, ordtelling, egenerklæring, publiseringsavtale og endelig PDF/Word-format.
- Dersom gruppen ønsker enda mer operativ anvendelse, bør neste analyseaktivitet være faglig vurdering fra Odfjell Tankers av om modellens anbefalte kjøp er praktisk gjennomførbare.
- Oppdater rapporten dersom senere modellkjøringer endrer hovedresultatene.
