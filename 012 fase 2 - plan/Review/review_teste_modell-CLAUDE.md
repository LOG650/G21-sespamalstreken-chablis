# Review: Teste modell (final)

Reviewen gjelder aktiviteten `006 analysis/02_modellutvikling/05_teste_modell` slik den foreligger pr. 2026-04-29, etter tre runder med review og utbedring. Reviewen er gjennomført uavhengig av forrige runde, basert på `README.md`, `src/test_route_inventory_model.py`, `metadata/res_route_inventory_test_summary.md`, `output/res_route_inventory_test_summary.json`, modellfilene i `04_implementere_modell` og kapittel 5.2 og 6 i `005 report/rapport.md`.

## 1. Sammendrag

Aktiviteten er ferdig. Testen kjører 35 av 35 kontroller grønt, dekker både intern konsistens i modelloutput og uavhengig kobling mot strukturerte inputtabeller, og produserer en JSON-logg med tidsstempel og sha256-sjekksummer for input- og resultatfiler. Tallene i kapittel 7 og 8 i rapporten lar seg verifisere direkte mot loggen. Den eneste reelle gjenstående svakheten — unit-test av selve LP-formuleringen (punkt F) — er bevisst parkert som dokumentert etterarbeid og er ikke en blokker.

## 2. Oppsummert status fra tidligere runder

| Punkt | Tema | Status |
| --- | --- | --- |
| A | Sirkulær lagerbalanse-validering | Løst funksjonelt — første ROB, forbruk og kapasitet krysses mot input, og første lagerbalanse per fartøy verifiseres direkte mot rådata (sjekk «Første lagerbalanse per fartøy stemmer direkte med inputdata»). |
| B | `available_priced_ports`-sjekken | Løst — eksakt mengdesammenligning mot input og oppslag av kjøpshavn mot prisede havner per etappe. |
| C | Solverstatus-substring | Løst — eksakt streng-likhet mot `OPTIMAL_SOLVER_STATUS` for alle 8 fartøyløsninger. |
| D | `priced_cost ≈ Σ qty × price` | Løst — to identitetssjekker (kostnad og pris) mot rå prisdata, både for `monthly_observation` og `historical_port_average`. |
| E | Sensitivitet 1,10/1,50 | Løst — alle tre rader får intern total- og eksternkostnadssjekk, og settet av multiplikatorer + antall rader valideres mot forventet sett {1.10, 1.25, 1.50}. |
| F | Unit-test av LP-formuleringen | **Parkert som dokumentert åpen etterarbeid** — ikke en åpen svakhet. |

## 3. Styrker i ferdigstilt versjon

- Direkte kobling til rådata: `tab_voyage_legs_2025.csv`, `tab_vessel_class_capacity.csv` og `tab_bunker_monthly_by_port.csv` leses og brukes til uavhengig validering, ikke bare til konsistenssjekk innad i output.
- 35 kontroller (opp fra 18 i runde 1 og 32 i runde 2) gir bred dekning på tvers av resultatfiler, solverstatus, etapperekkefølge, beholdning, kapasitet, kjøpslogikk og sensitivitet.
- Reproduserbarhet: JSON-loggen inneholder UTC-tidsstempel og sha256 for både input- og validerte filer, slik at det er sporbart hvilken modellkjøring som ble validert.
- README har en kontrollmatrise som mapper kategorier til konkret dekning, og toleransevalget (0,05) er begrunnet eksplisitt i README.
- Skriptet feiler hardt med `SystemExit(1)` ved feilet kontroll, slik at testen kan brukes i en pipeline.

## 4. Åpen etterarbeid (dokumentert)

- **F. Unit-test av selve LP-formuleringen.** Ingen direkte test av `solve_vessel`, `build_purchase_opportunities` eller `load_price_data` med konstruert mini-input der svaret er kjent på forhånd. Brukeren har bevisst valgt å parkere dette som etterarbeid.
  - **Observasjon:** Status på F er ikke nevnt eksplisitt i `README.md` eller `metadata/res_route_inventory_test_summary.md`. Anbefales lagt inn som en kort notis i README under «Kontroller» eller en egen «Åpne punkter»-seksjon, eller alternativt i `status.md`, slik at det ikke ser ut som om den er glemt.
- Mindre observasjon: Markdown-tabellen viser fortsatt `solver_status`-verdien som en dict-streng (`8 optimale løsninger`), men dette er ufarlig og kosmetisk.

## 5. Sjekk mot prosjektregler

- **Norsk språk:** Alle kontrollnavn, README, Markdown-rapport og kommentarer er på norsk.
- **UTF-8 uten BOM:** Filene leses inn og skrives tilbake med `encoding="utf-8"`, og innholdet rendres korrekt med `æ`, `ø` og `å` i tabellene (verifisert via lesing av `metadata/res_route_inventory_test_summary.md`).
- **Filnavn:** `res_`-prefiks for resultatfiler er fulgt. Skriptnavnet `test_route_inventory_model.py` har ikke `res_`-prefiks, hvilket er korrekt for kildekode.
- **Mappestruktur:** `src/`, `output/` og `metadata/` ligger alle under aktivitetsmappen, i tråd med prosjektreglene.
- **Konsistens med `04_implementere_modell`:** Testen leser fra `04_implementere_modell/output` og fra de samme strukturerte inputfilene som modellen selv bruker. Ingen avvik observert.

## 6. Konsistens med rapporten

Tallene i kapittel 7 og 8 stemmer mot output:

| Tall i rapport | Linje | Verdi i test/output |
| --- | --- | --- |
| 486 voyage-etapper | 478, 506, 511 | 486 (sjekk «Antall etapper stemmer med sammendrag») |
| 8 fartøyfiler | 510 | 8 (sjekk «Antall fartøyfiler stemmer med sammendrag») |
| 28 etapper med kjøp | 478, 513 | 28 (sjekk «Antall etapper med kjøp stemmer med sammendrag») |
| 18 857,45 kjøp i prisede havner | 480, 490 | 18857.451 |
| 21 260,62 ekstern bunkring | 480 | 21260.619 |
| 26 625 664,78 total modellkostnad | 490, 506 | 26625664.78 |
| 10 406 690,70 kostnad i prisede havner | 490 | 10406690.7 |

Sensitivitetstallene 24 679 387,90 (1,10) og 29 869 459,58 (1,50) i rapport linje 492 verifiseres internt i testen via konsistenssjekk på alle tre sensitivitetsrader, men det er ingen direkte sjekk av eksakt tallverdi mot rapporten — dette er akseptabelt fordi rapporten er sitert direkte fra `res_route_inventory_proxy_sensitivity.csv` som testen leser. Kapittel 5.2 omtaler de samme tre inputfilene som testen leser. Kapittel 6.5 beskriver testaktiviteten korrekt og uten overdrivelser.

## 7. Endelig konklusjon

**Aktiviteten kan lukkes nå.** Alle svakheter fra tidligere runder (A–E) er adressert, testen kjører 35/35 grønt, JSON-loggen har sha256 og tidsstempel, og rapportkapittel 6.5, 7 og 8 er konsistente med output. Punkt F (unit-test av LP-formuleringen) er parkert som dokumentert åpen post og er ikke en blokker for ferdigstillelse.

Eneste konkrete anbefaling før lukking er å nevne F kort i `README.md` (eller `status.md`) som «åpen etterarbeids-oppgave» slik at parkeringen er sporbar i selve aktivitetsdokumentasjonen, og ikke bare i samtalehistorikken.
