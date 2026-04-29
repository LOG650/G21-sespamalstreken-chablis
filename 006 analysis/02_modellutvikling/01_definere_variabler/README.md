# 01 Definere variabler

Denne aktiviteten dokumenterer sett, parametere og beslutningsvariabler for prosjektets operative hovedmodell. Modellen arbeider på fartøy- og etappenivå.

## Modellnivå

Hovedmodellen er en rute- og lagerbasert lineær optimeringsmodell. Den bruker voyage-etapper fra 2025 til å beskrive faktisk rutesekvens, forbruk, startbeholdning og tilgjengelige havner. Prisgrunnlaget er begrenset til modellhavnene `P001`, `P002`, `P003` og `P004`.

Modellen svarer på spørsmålet:

Hvor mye bør hvert fartøy bunkre i prisede modellhavner gjennom den observerte ruten, og hvor mye må dekkes utenfor prisgrunnlaget, slik at samlet modellert drivstoffkostnad blir lavest mulig?

## Sett og indekser

| Symbol | Betydning | Datakilde |
| --- | --- | --- |
| $V$ | Mengde fartøyfiler | `tab_voyage_legs_2025.csv` |
| $L_v$ | Kronologisk ordnede etapper for fartøyfil $v$ | `tab_voyage_legs_2025.csv` |
| $H$ | Prisede modellhavner, $H = \{P001, P002, P003, P004\}$ | `tab_bunker_monthly_by_port.csv` |
| $t(l)$ | Måned for etappe $l$ | `period_month` |

## Parametere

| Symbol | Betydning | Datakilde / regel |
| --- | --- | --- |
| $c_{v,l}$ | Forbruk på etappe $l$ for fartøyfil $v$ | `fuel_consumption_total` |
| $K_v$ | Bunkerskapasitet for fartøyfilens klasse | `tab_vessel_class_capacity.csv` |
| $I_{v,0}$ | Observert startbeholdning før første etappe | første `rob_start` per fartøyfil |
| $a_{v,l,h}$ | 1 dersom modellhavn $h$ finnes i etappens tilgjengelige havner, ellers 0 | `available_ports_P00X` |
| $p_{h,t}$ | Pris i modellhavn $h$ i måned $t$ | månedlig pris, ellers historisk havnesnitt |
| $p^U$ | Proxykostnad for ekstern/ukjent bunkring | 1,25 ganger høyeste historiske havnesnitt |

## Beslutningsvariabler

| Variabel | Type | Betydning |
| --- | --- | --- |
| $x_{v,l,h}$ | Kontinuerlig, ikke-negativ | Mengde bunkret i modellhavn $h$ på etappe $l$ for fartøyfil $v$ |
| $I_{v,l}$ | Kontinuerlig, ikke-negativ | Modellert beholdning etter etappe $l$ for fartøyfil $v$ |
| $u_{v,l}$ | Kontinuerlig, ikke-negativ | Ekstern/ukjent bunkring på etappe $l$ når behovet ikke kan dekkes gjennom prisede modellhavner |

## Tolkning

Variabelen $x_{v,l,h}$ er modellens direkte beslutning om bunkring i havner med dokumentert prisgrunnlag. Variabelen $I_{v,l}$ binder beslutningene sammen over tid, slik at modellen ikke kan vurdere hver etappe isolert. Variabelen $u_{v,l}$ er ikke en anbefalt havn, men en kostnadsatt markør for kjøp utenfor modellens prisede havnenettverk.

## Kobling til kode

Variablene implementeres i:

`006 analysis/02_modellutvikling/04_implementere_modell/src/run_route_inventory_model.py`

I koden opprettes $x_{v,l,h}$ bare for modellhavner som faktisk finnes i `available_ports_P00X` på etappen. Dette gjør at modellen ikke kan velge en billig havn som ikke ligger i den observerte ruten.
