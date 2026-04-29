# 02 Formulere målfunksjon

Denne aktiviteten dokumenterer målfunksjonen for prosjektets operative hovedmodell. Målet er å minimere modellert drivstoffkostnad for observerte fartøyruter, gitt beholdning, forbruk, kapasitet og tilgjengelige prisede modellhavner.

## Kostnadselementer

Modellen har to kostnadselementer:

| Kostnad | Beskrivelse |
| --- | --- |
| Priset bunkring | Kjøp i modellhavnene `P001`, `P002`, `P003` og `P004` når havnen er tilgjengelig i ruten |
| Ekstern/ukjent bunkring | Kjøp utenfor modellens prisede havnenettverk, kostnadsatt med konservativ proxypris |

Ekstern/ukjent bunkring gjør modellen løsbar også når ruten ikke har tilstrekkelig tilgang til prisede modellhavner. Dette er samtidig en eksplisitt synliggjøring av datagapet i prisgrunnlaget.

## Prisregel

For modellhavnene `P001`-`P004` brukes følgende prioritet:

1. Eksakt månedlig pris dersom `tab_bunker_monthly_by_port.csv` har observasjon for havn og måned.
2. Historisk vektet havnesnitt dersom ruten har modellhavnen, men måneden mangler eksakt pris.

Historiske havnesnitt brukt i hovedmodellen:

| Havn | Historisk vektet snittpris |
| --- | ---: |
| P001 | 578,75 |
| P002 | 610,29 |
| P003 | 540,84 |
| P004 | 577,04 |

Ekstern/ukjent bunkring kostnadssettes i hovedkjøringen til 1,25 ganger høyeste historiske havnesnitt, altså 762,86 per enhet.

## Matematisk formulering

Målfunksjonen er:

$\min Z = \sum_{v \in V}\sum_{l \in L_v}\sum_{h \in H} p_{h,t(l)}x_{v,l,h} + \sum_{v \in V}\sum_{l \in L_v} p^U u_{v,l}$

der:

- $x_{v,l,h}$ er mengde bunkret i priset modellhavn
- $p_{h,t(l)}$ er pris for modellhavn $h$ i etappens måned
- $u_{v,l}$ er ekstern/ukjent bunkring
- $p^U$ er proxykostnaden for ekstern/ukjent bunkring

## Tolkning

Målfunksjonen prioriterer kjøp i prisede modellhavner når dette er mulig og økonomisk gunstig innenfor rute-, beholdnings- og kapasitetsrestriksjonene. Samtidig straffer den ekstern/ukjent bunkring med en høyere proxykostnad, slik at modellen ikke bruker denne variabelen med mindre prisgrunnlaget og ruten gjør det nødvendig.

## Sensitivitetsanalyse

Siden $p^U$ er en antagelse, kjøres det en enkel sensitivitetsanalyse med tre proxyfaktorer:

| Proxyfaktor | Formål |
| --- | --- |
| 1,10 | Lavere straff for kjøp utenfor prisgrunnlaget |
| 1,25 | Hovedscenario |
| 1,50 | Høyere straff for kjøp utenfor prisgrunnlaget |

Resultatfil:

`006 analysis/02_modellutvikling/04_implementere_modell/output/res_route_inventory_proxy_sensitivity.csv`
