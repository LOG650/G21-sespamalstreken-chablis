# Status - Minimering av drivstoffkostnader hos Odfjell Tankers

_Sist oppdatert automatisk: 2026-04-02_

Denne filen er generert fra:
- `012 fase 2 - plan/Prosjektstyringsplan, Odfjell Tankers.md`
- `012 fase 2 - plan/MS_Project.mpp`
- faktiske filer og siste aktivitet i repoet

## Overordnet status

- Prosjektet er i fasen **Modellutvikling** per 2026-04-02.
- Aktiviteten som er planlagt akkurat nå er **Formulere målfunksjon** (2026-04-02–2026-04-03).
- Planunderlaget er dokumentert i både prosjektstyringsplanen og `MS_Project.mpp`.
- Repoet inneholder rådata i `004 data`, så datainnsamling ser ut til å være startet eller gjennomført.
- Repoet inneholder nå tydelige filer for renset og strukturert datasett i `006 analysis/01_datagrunnlag`.
- Repoet inneholder nå modellinput og en første modellimplementasjon i `006 analysis/02_modell_v1`.
- Rapportarbeidet er startet i `005 report`, inkludert første utkast til modell- og databeskrivelse.

## Hva vi må gjøre nå

- Formulere målfunksjon: pågår innen perioden 2026-04-02–2026-04-03.
- Opprett første modellutkast før `Implementere modell` starter 2026-04-09.

## Fremdrift mot milepæler

| Milepæl | Dato | Status |
| --- | --- | --- |
| Proposal godkjent | 2026-02-08 | Passert |
| Planleggingsfase ferdig | 2026-03-09 | Passert |
| Datagrunnlag ferdig | 2026-03-29 | Passert |
| Modelltesting ferdig | 2026-04-28 | Kommende |
| Innlevering | 2026-06-02 | Kommende |

## Aktivitetsstatus

| Fase | Aktivitet | Start | Slutt | Status 2026-04-02 | Grunnlag |
| --- | --- | --- | --- | --- | --- |
| Datagrunnlag | Datainnsamling | 2026-03-10 | 2026-03-17 | Fullført | Dokumentert i repo |
| Datagrunnlag | Datavask | 2026-03-18 | 2026-03-23 | Fullført | Dokumentert i `006 analysis/01_datagrunnlag` med rensepipeline, renset fil og oppsummeringsfil |
| Datagrunnlag | Strukturering av datasett | 2026-03-24 | 2026-03-26 | Fullført | Dokumentert i `006 analysis/01_datagrunnlag` med aggregert datasett og videre kobling til modellinput |
| Datagrunnlag | Deskriptiv analyse | 2026-03-27 | 2026-03-29 | Bør være ferdig | Ingen tydelig dokumentasjon funnet i repo |
| Modellutvikling | Definere variabler | 2026-03-30 | 2026-04-01 | Bør være ferdig | Ingen tydelig dokumentasjon funnet i repo |
| Modellutvikling | Formulere målfunksjon | 2026-04-02 | 2026-04-03 | Pågår | Planlagt aktivitet nå (2026-04-02–2026-04-03) |
| Modellutvikling | Definere restriksjoner | 2026-04-04 | 2026-04-08 | Kommende | Starter 2026-04-04 |
| Modellutvikling | Implementere modell | 2026-04-09 | 2026-04-20 | Kommende | Starter 2026-04-09 |
| Modellutvikling | Teste modell | 2026-04-21 | 2026-04-28 | Kommende | Starter 2026-04-21 |
| Analyse | Basiskjøring | 2026-04-29 | 2026-05-01 | Kommende | Starter 2026-04-29 |
| Analyse | Sensitivitetsanalyse | 2026-05-02 | 2026-05-06 | Kommende | Starter 2026-05-02 |
| Analyse | Resultattolkning | 2026-05-07 | 2026-05-11 | Kommende | Starter 2026-05-07 |
| Rapportering | Skrive resultater | 2026-05-09 | 2026-05-14 | Kommende | Starter 2026-05-09 |
| Rapportering | Diskusjon | 2026-05-12 | 2026-05-17 | Kommende | Starter 2026-05-12 |
| Rapportering | Ferdigstille rapport | 2026-05-18 | 2026-05-23 | Kommende | Starter 2026-05-18 |
| Rapportering | Revisjon | 2026-05-24 | 2026-05-29 | Kommende | Starter 2026-05-24 |
| Rapportering | Språkvask / referanser | 2026-05-26 | 2026-05-30 | Kommende | Starter 2026-05-26 |
| Avslutning | Prosjektbuffer | 2026-05-31 | 2026-06-02 | Kommende | Starter 2026-05-31 |
| Avslutning | Innlevering | 2026-06-02 | 2026-06-02 | Kommende | Starter 2026-06-02 |

## Sjekkliste for å lukke aktiviteten `Rense og strukturere data`

Denne sjekklisten konkretiserer hva som må være på plass for å kunne markere `Datavask` og `Strukturering av datasett` som fullført i planen. Listen inkluderer både aktiviteter som er ferdigstilt, kontrollpunkter som er oppfylt, og gjenstående opprydding før aktiviteten kan lukkes formelt.

### Fullførte aktiviteter

- [x] Rådatafilen er identifisert og brukes konsekvent som kilde: `004 data/Bunker Lifting List(Worksheet1) (1).csv`
- [x] Rensepipeline er etablert i `006 analysis/01_datagrunnlag/clean_and_aggregate_bunker_data.py`
- [x] Renselogikken leser inn transaksjonsrader og filtrerer bort tomme eller ugyldige rader
- [x] Datoer og tallfelt parses eksplisitt i rensepipen
- [x] `Invoiced Qty` brukes som hovedvolum med fallback til `Ordered Qty`
- [x] `Invoice Price` brukes som hovedpris med fallback til `Order Price`
- [x] Observasjoner med manglende pris eller volum etter fallback håndteres eksplisitt i rensepipen
- [x] Observasjoner med ikke-positivt volum forkastes eksplisitt i rensepipen
- [x] Observasjoner med ikke-positiv pris forkastes eksplisitt i rensepipen
- [x] Rensede variabler som `delivery_month`, `delivery_year`, `effective_qty`, `effective_price` og `cost_value` opprettes
- [x] Renset transaksjonsfil er generert: `006 analysis/01_datagrunnlag/tab_bunker_cleaned.csv`
- [x] Aggregert datasett per `måned × havn` er generert: `006 analysis/01_datagrunnlag/tab_bunker_monthly_by_port.csv`
- [x] Aggregatet inneholder sentrale strukturvariabler som transaksjonsantall, total mengde, vektet snittpris, enkelt snitt, minimum, maksimum og antall unike fartøy og leverandører
- [x] Oppsummeringsfil med nøkkeltall og renseutfall er generert: `006 analysis/01_datagrunnlag/tab_bunker_summary.md`
- [x] Det aggregerte datasettet brukes videre som kilde til modellinput i `006 analysis/02_modell_v1/generate_model_v1_inputs.py`
- [x] Modellinput er generert videre til pris-, behovs- og tilgjengelighetsfiler i `006 analysis/02_modell_v1`

### Kontrollpunkter som er oppfylt

- [x] Filene i `006 analysis/01_datagrunnlag` finnes og samsvarer med rense- og aggregeringsløpet
- [x] Kolonnenavnene i renset fil og aggregert fil er konsistente med videre bruk i modellinput
- [x] Antall observasjoner etter rensing er dokumentert i oppsummeringsfilen
- [x] Antall forkastede observasjoner er dokumentert i oppsummeringsfilen
- [x] Tidsperioden i aggregatet er dokumentert og brukt videre i modellinput
- [x] Havnene i aggregatet stemmer med havnene som brukes i modellversjon 1
- [x] Datastrukturen er tilstrekkelig moden til å støtte arbeidet med `Definere variabler`, `Formulere målfunksjon` og `Implementere modell`

### Verifisert opprydding før lukking av aktiviteten

- [x] `006 analysis/01_datagrunnlag/tab_bunker_summary.md` er kontrollert direkte som UTF-8 og viser korrekt norsk tekst
- [x] `006 analysis/02_modell_v1/README.md` er kontrollert direkte som UTF-8 og viser korrekt norsk tekst
- [x] Statusgrunnlaget i denne filen er oppdatert slik at `Datavask` og `Strukturering av datasett` står som fullført
- [x] Det er lagt inn en kort metodebeskrivelse i rapportens kapittel `5 Metode og data` som forklarer rense- og aggregeringsløpet

### Vurdering

- Datavask er gjennomført og dokumentert.
- Strukturering av datasett er gjennomført og dokumentert.
- Aktiviteten `Rense og strukturere data` kan nå lukkes faglig i prosjektplanen.

## Spor i repoet

- Siste datafil: `004 data/Bunker Lifting List(Worksheet1) (1).csv` sist endret 2026-03-31 15:32
- Siste analysefil: `006 analysis/01_datagrunnlag/tab_bunker_summary.md`
- Siste modellfil: `006 analysis/02_modell_v1/simulate_model_v1_results.py`
- Siste rapportfil: `005 report/rapport.md`

### Siste git-aktivitet

- `2026-04-02 6a8fea5 commit	modified:   011 fase 1 - proposal/proposal.md`
- `2026-03-31 ba953f1 Add files via upload`
- `2026-03-19 50d401f commit	renamed:    012 fase 2 - plan/LOG650 (1).mpp -> 012 fase 2 - plan/MS_Project.mpp commit	deleted:    012 fase 2 - plan/Prosjektstyringsplan, Odfjell Tankers.docx commit	new file:   012 fase 2 - plan/Prosjektstyringsplan, Odfjell Tankers.md commit	new file:   012 fase 2 - plan/conversion_report.md commit	new file:   TargetMDDirectory/Prosjektstyringsplan, Odfjell Tankers/images/image_001_spd2m_image6.jpg commit	new file:   TargetMDDirectory/Prosjektstyringsplan, Odfjell Tankers/images/image_002_spd2m_image5.jpg commit	new file:   TargetMDDirectory/Prosjektstyringsplan, Odfjell Tankers/images/image_003_spd2m_image2.jpg commit	new file:   TargetMDDirectory/Prosjektstyringsplan, Odfjell Tankers/images/image_004_spd2m_image1.jpg`
- `2026-03-19 418f3e6 Add files via upload`
- `2026-03-19 87d9ad7 Add files via upload`

## Merknad om datoer

Tekstplanen nevner endelig innlevering **2026-05-31**, mens `MS_Project.mpp` viser **2026-06-02** inkludert prosjektbuffer. Statusen under følger datoene i `MS_Project.mpp`.

## Oppdatering

Bruk en av disse kommandoene for å oppdatere statusfilen manuelt:

```powershell
python "012 fase 2 - plan\generate_status.py"
```

```powershell
.\012 fase 2 - plan\oppdater_status.ps1
```

Hvis du vil oppdatere for en bestemt dato, bruk:

```powershell
python "012 fase 2 - plan\generate_status.py" 2026-04-02
```

## Manuell merknad 2026-04-12

- Følgende planartefakter er opprettet i `012 fase 2 - plan`: `core.json`, `requirements.json`, `risk.json`, `schedule.json` og `wbs.json`.
- JSON-filene er strukturert fra prosjektstyringsplanen, `MS_Project.mpp` og denne statusfilen.
- WBS-strukturen er delvis avledet, fordi vedlegg B i den konverterte Markdown-filen ikke inneholder en utfylt maskinlesbar WBS.
- Det er også opprettet `README.md` som forklarer innholdet og bruken av planartefaktene.
- Datagrunnlaget i `004 data/Bunker Lifting List(Worksheet1) (1).csv` er gjennomgått som grunnlag for modellering.
- Et separat arbeidsutkast er opprettet i `005 report/Kaylee_rapport.md` med første databeskrivelse og et første modellutkast for beslutningsvariabler, målfunksjon og restriksjoner.
- Målfunksjonen for første modellversjon er nå også formulert eksplisitt i `005 report/rapport.md`.
- Det er laget en rense- og aggregeringspipeline i `006 analysis/01_datagrunnlag/clean_and_aggregate_bunker_data.py`.
- Rensede og aggregerte datafiler er opprettet i `006 analysis/01_datagrunnlag`, inkludert månedlig aggregat per havn.
- Modellinput for modellversjon 1 er opprettet i `006 analysis/02_modell_v1` med tydelige filnavn for pris, behov, tilgjengelighet og parameter-metadata.
- En første Pyomo-implementasjon for modellversjon 1 er opprettet i `006 analysis/02_modell_v1/run_model_v1_pyomo.py`.

## Arbeid i dag 2026-04-12

### Ferdigstilt

- Datavask er dokumentert og gjennomført for tilgjengelig bunkringsdata.
- Strukturering av datasett er gjennomført med egne rensede og aggregerte filer.
- Beslutningsvariabler for første modellversjon er formulert i `005 report/Kaylee_rapport.md`.
- Målfunksjonen er formulert i både `005 report/Kaylee_rapport.md` og `005 report/rapport.md`.
- Modellinput for versjon 1 er etablert i `006 analysis/02_modell_v1`.

### Under arbeid

- Restriksjonene for første modellversjon videreutvikles i `005 report/Kaylee_rapport.md`.
- Implementering av modellversjon 1 pågår i `006 analysis/02_modell_v1`.
- Avklaring av hvilke supplerende data som trengs for en mer realistisk operativ modell pågår.

### Anbefalt oppdatering i MS Project

- Marker som fullført: `Datavask`
- Marker som fullført: `Strukturering av datasett`
- Marker som fullført: `Definere variabler`
- Marker som fullført: `Formulere målfunksjon`
- Marker som under arbeid: `Definere restriksjoner`
- Marker som under arbeid: `Implementere modell`
