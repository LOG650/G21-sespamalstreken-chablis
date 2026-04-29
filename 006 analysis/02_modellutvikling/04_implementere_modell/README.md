# Operasjonell hovedmodell

Denne aktiviteten etablerer prosjektets operative hovedmodell for minimering av drivstoffkostnader med dataene som faktisk finnes i repoet.

Modellen bruker voyage-etapper, forbruk, startbeholdning, tankkapasitet og havner observert i ruten. Prisdata brukes for modellhavnene `P001`-`P004`. Dersom en modellhavn mangler eksakt månedlig pris for en 2025-etappe, brukes historisk havnesnitt som prisproxy. Havner utenfor `P001`-`P004` får ikke egne estimerte priser; nødvendig bunkring utenfor prisgrunnlaget føres som ekstern/ukjent bunkring med konservativ proxykostnad.

## Filer

- `src/run_route_inventory_model.py`: lineær kostnadsmodell for rute, beholdning og bunkring.
- `output/res_route_inventory_summary.json`: samlet modellresultat.
- `output/res_route_inventory_by_vessel.csv`: resultat aggregert per fartøyfil.
- `output/res_route_inventory_by_leg.csv`: beholdning, forbruk, kjøp og ekstern mengde per etappe.
- `output/res_route_inventory_purchases.csv`: positive kjøp i prisede havner.
- `output/res_route_inventory_proxy_sensitivity.csv`: sensitivitetsanalyse for proxykostnad på ekstern/ukjent bunkring.
- `metadata/res_route_inventory_summary.md`: norsk tolkningsnotat.

## Modellidé

Modellen minimerer samlet modellkostnad for rute- og beholdningsplanen. Kostnaden består av kjøp i prisede modellhavner og ekstern/ukjent bunkring. Ekstern/ukjent bunkring brukes når ruten ikke kan dekkes gjennom prisede modellhavner innenfor beholdnings- og kapasitetsbegrensningene.

Resultatet er en kvantitativ, operasjonell bunkringsplan for de åtte anonymiserte fartøyfilene. Det viser hvor modellen anbefaler å fylle i prisede havner, hvor mye som må dekkes utenfor prisgrunnlaget, og hvilken kostnad dette gir under de valgte prisantagelsene.
