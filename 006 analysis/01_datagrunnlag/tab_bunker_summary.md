# Oppsummering av renset bunkringsdata

- Rå observasjoner lest inn: 1389
- Rensede observasjoner beholdt: 1381
- Månedlige aggregater opprettet: 229
- Antall havner: 4 (P001, P002, P003, P004)
- Antall måneder i aggregatet: 61

## Rensevalg

- `Invoiced Qty` brukes som hovedvolum, med fallback til `Ordered Qty`: 10 observasjoner
- `Invoice Price` brukes som hovedpris, med fallback til `Order Price`: 10 observasjoner
- Forkastet på grunn av manglende pris eller volum etter fallback: 0 observasjoner
- Forkastet på grunn av ikke-positivt volum: 8 observasjoner
- Forkastet på grunn av ikke-positiv pris: 0 observasjoner

## Aggregert oversikt per havn

| Havn | Observasjoner | Total mengde | Vektet snittpris |
| --- | --- | --- | --- |
| P001 | 209 | 113606.88 | 578.75 |
| P002 | 286 | 181419.36 | 610.29 |
| P003 | 369 | 253591.20 | 540.84 |
| P004 | 517 | 320932.69 | 577.04 |

## Filer

- `tab_bunker_cleaned.csv`: renset transaksjonsnivå
- `tab_bunker_monthly_by_port.csv`: aggregert per havn og måned
