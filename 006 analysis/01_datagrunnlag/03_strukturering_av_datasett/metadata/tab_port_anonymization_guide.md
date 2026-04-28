# Port- og voyage-anonymisering 2025

Eksisterende voyage-filer i repoet er anonymisert på plass. Rådata med opprinnelige koder forutsettes oppbevart utenfor repoet.

## Regler

- `Voyage_From` og `Voyage_To` i `004 data/C*.csv` er erstattet med anonymiserte `Pxxx`-koder.
- `Voyage_Number` i `004 data/C*.csv` er erstattet med anonymiserte `VGxxx`-koder.
- `from_port_unlocode` er erstattet av `from_port_P00X` i strukturerte voyage-tabeller.
- `to_port_unlocode` er erstattet av `to_port_P00X` i strukturerte voyage-tabeller.
- `available_ports` er erstattet av `available_ports_P00X` i strukturerte voyage-etapper.
- `P001` til `P004` følger eksisterende modellhavner, mens `P005+` er øvrige voyage-havner.

## Omfang

- Rå-/splitfiler anonymisert i `004 data`: 24
- Portkoder i konfidensiell mapping: 70
- Voyage-koder anonymisert: 244

## Konfidensiell mapping

`data/tab_port_mapping_confidential.csv` inneholder kobling mellom opprinnelig havnekode og anonym portkode. Filen skal brukes internt og ikke legges som publisert rapportvedlegg.
