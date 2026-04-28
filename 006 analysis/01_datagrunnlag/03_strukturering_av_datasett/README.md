# 03 Strukturering av datasett

Denne aktiviteten inneholder det strukturerte datasettet som brukes videre i modellutviklingen.

- `data`: aggregert datasett per havn og måned
- `metadata`: oppsummering av rensing og struktur

Mappen er koblingen mellom datavask og videre modellinput.

Supplerende voyage-data fra 2025 struktureres med `src/structure_voyage_data_2025.py`.
Skriptet lager tre modellklare tabeller:

- `data/tab_voyage_events_2025.csv`
- `data/tab_voyage_legs_2025.csv`
- `data/tab_vessel_class_capacity.csv`

Kolonneforklaring og kontroller dokumenteres i `metadata/tab_voyage_structure_guide.md`.

Råfilene for voyage-data splittes kronologisk 80/20 før videre rensing med `src/split_voyage_raw_train_test_2025.py`.
Skriptet beholder originalfilene i `004 data` urørt og lager `_train_80.csv` og `_test_20.csv` for hver av de åtte `C*.csv`-filene.

Splitten er dokumentert i `metadata/tab_voyage_raw_train_test_split_2025.md`.

Voyage-havner og voyage-numre er pseudonymisert på plass med `src/anonymize_voyage_ports_2025.py`. Skriptet oppdaterer eksisterende `C*.csv`-filer i `004 data` og de strukturerte voyage-tabellene, slik at havner vises som `Pxxx` og voyage-numre som `VGxxx`. De strukturerte tabellene bruker kolonnenavnene `from_port_P00X`, `to_port_P00X` og `available_ports_P00X`.

Intern kobling mellom opprinnelig havnekode og P-kode ligger i `data/tab_port_mapping_confidential.csv`. Denne filen er et internt arbeidsgrunnlag og skal ikke legges som publisert rapportvedlegg.
