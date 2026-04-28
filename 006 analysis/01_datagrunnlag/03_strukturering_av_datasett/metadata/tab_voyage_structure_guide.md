# Struktur for voyage-data 2025

Denne filen dokumenterer modellklare tabeller generert fra de anonymiserte voyage-filene i `004 data`.

## Genererte tabeller

| Fil | Nivå | Bruk |
| --- | --- | --- |
| `tab_voyage_events_2025.csv` | Rapporteringshendelse | Detaljert sporbarhet, kontroll og eventuell videre aggregering |
| `tab_voyage_legs_2025.csv` | Voyage-etappe | Hovedtabell for fartøy- og rutebasert optimeringsmodell |
| `tab_vessel_class_capacity.csv` | Fartøyklasse | Kapasitetsparameter $K_v$ |

## Kolonner i `tab_voyage_events_2025.csv`

| Kolonne | Forklaring |
| --- | --- |
| `vessel_class` | Anonymisert fartøyklasse, hentet fra filnavn |
| `vessel_file_id` | Anonym fil-ID, f.eks. `C001-1` |
| `event_datetime_utc` | Kombinert dato og tid i UTC |
| `event_type` | Rapportert hendelsestype |
| `voyage_number` | Voyage-identifikator |
| `from_port_P00X`, `to_port_P00X` | Anonymisert start- og slutthavn |
| `from_country`, `to_country` | Landprefiks fra opprinnelig UN/Locode når tabellen genereres fra ikke-pseudonymiserte rådata; tomt ved P-koder |
| `hours_since_previous_report` | Timer siden forrige rapport |
| `distance_nm` | Rapportert distanse, antatt nautiske mil |
| `me_consumption`, `ae_consumption`, `boiler_consumption`, `other_consumption` | Forbruk gruppert etter maskin-/forbrukstype |
| `total_consumption` | Sum modellrelevant forbruk for raden |
| `rob_fuel_total` | Total remaining on board etter rapportering |
| `contract_port_flag` | 1 dersom raden berører kontraktsrelevant havn basert på intern portmapping |
| `data_quality_flag` | Enkel kvalitetsmarkør for manglende voyage, port, ROB eller kapasitetsavvik |

## Kolonner i `tab_voyage_legs_2025.csv`

| Kolonne | Forklaring |
| --- | --- |
| `vessel_class`, `vessel_file_id`, `voyage_number` | Identifikasjon av anonymisert fartøy og voyage |
| `leg_sequence` | Kronologisk løpenummer innen fartøyfil |
| `from_port_P00X`, `to_port_P00X` | Etappens anonymiserte start- og slutthavn |
| `departure_datetime_utc`, `arrival_datetime_utc` | Første og siste tidspunkt i etappen |
| `period_month` | Måned brukt for kobling mot prisdata |
| `distance_nm_total`, `duration_hours_total` | Aggregert distanse og varighet |
| `fuel_consumption_total` | Aggregert forbruk, kandidat for $d_{v,t}$ |
| `rob_start`, `rob_end` | Første og siste observerte ROB i etappen |
| `bunkering_inferred` | 1 dersom ROB øker innen etappen |
| `available_ports_P00X` | Observerte anonymiserte havner i etappen, separert med `|` |
| `contract_port_flag` | 1 dersom en observert havn er kontraktsrelevant basert på intern portmapping |
| `data_quality_flag` | Oppsummerte kvalitetsflagg fra rapporteringsradene |

## Omfang og kontroller

- Rapporteringsrader strukturert: 3893
- Voyage-etapper aggregert: 486
- Fartøyklasser med kapasitet: 5

### Kvalitetsflagg på rapporteringsnivå

| Flagg | Antall |
| --- | ---: |
| `missing_rob` | 3 |
| `ok` | 3890 |

### Kvalitetsflagg på etappenivå

| Flagg | Antall |
| --- | ---: |
| `missing_rob` | 3 |
| `ok` | 483 |

## Modellkobling

- $K_v$ hentes fra `tab_vessel_class_capacity.csv`.
- $d_{v,t}$ kan hentes fra `fuel_consumption_total` i `tab_voyage_legs_2025.csv`.
- $I_{v,t}$ kan initialiseres eller kontrolleres med `rob_start` og `rob_end`.
- Reell havnetilgjengelighet kan avledes fra `from_port_P00X`, `to_port_P00X` og `available_ports_P00X`.
- Intern kobling mellom opprinnelige havnekoder og P-koder ligger i `data/tab_port_mapping_confidential.csv` og skal ikke publiseres som rapportvedlegg.
- `contract_port_flag` er et første teknisk flagg og må valideres mot faktisk kontraktsomfang før det brukes som hard restriksjon.
