# 03 Definere restriksjoner

Denne aktiviteten dokumenterer restriksjonene for prosjektets operative hovedmodell. Restriksjonene gjør modellen operasjonell ved å koble bunkringsbeslutninger til faktisk rutesekvens, forbruk, beholdning og tankkapasitet.

## Beholdningsbalanse

Beholdningen etter hver etappe beregnes som beholdning før etappen, pluss eventuell bunkring, minus forbruk:

$I_{v,l} = I_{v,l-1} + \sum_{h \in H} x_{v,l,h} + u_{v,l} - c_{v,l}$

For første etappe brukes observert startbeholdning fra `rob_start`:

$I_{v,0}^{start} = \text{første observerte } rob\_start \text{ for fartøyfil } v$

Denne restriksjonen er sentral fordi den gjør at en bunkringsbeslutning på én etappe påvirker senere etapper.

## Ikke-negativ beholdning

Modellen tillater ikke at fartøyet går tomt for drivstoff:

$I_{v,l} \geq 0 \quad \forall v,l$

Dette betyr at forbruket på alle etapper må dekkes av startbeholdning, kjøp i prisede modellhavner eller ekstern/ukjent bunkring.

## Kapasitetsgrense

Beholdningen kan ikke overstige oppgitt bunkerskapasitet:

$I_{v,l} \leq K_v \quad \forall v,l$

I implementasjonen kontrolleres også beholdning rett etter bunkring og før forbruk, slik at modellen ikke kan fylle mer enn tankkapasiteten tillater:

$I_{v,l-1} + \sum_{h \in H} x_{v,l,h} + u_{v,l} \leq K_v$

For første etappe brukes observert startbeholdning i stedet for $I_{v,l-1}$.

## Rute- og havnetilgjengelighet

Modellen kan bare bunkre i en priset modellhavn dersom havnen finnes i etappens observerte tilgjengelige havner:

$x_{v,l,h} = 0 \quad \text{hvis } a_{v,l,h}=0$

Teknisk håndheves dette ved at modellen bare oppretter kjøpsvariabler for havner i `P001`-`P004` som også finnes i `available_ports_P00X` på etappen. Dette hindrer at modellen velger en billig havn som ikke inngår i den observerte ruten.

## Ekstern/ukjent bunkring

Variabelen $u_{v,l}$ gjør modellen løsbar når fartøyet trenger drivstoff, men ruten ikke har tilstrekkelig tilgang til prisede modellhavner:

$u_{v,l} \geq 0 \quad \forall v,l$

Denne variabelen skal tolkes som kjøp utenfor modellens prisede havnenettverk. Den er ikke en anbefaling om en bestemt havn. Den viser hvor prisgrunnlaget er for svakt til å gi en full operasjonell kjøpsanbefaling.

## Restriksjoner som ikke er inkludert

Følgende forhold er ikke lagt inn som harde restriksjoner i hovedmodellen:

| Forhold | Begrunnelse |
| --- | --- |
| Minimumsbuffer | Det finnes ikke validert bufferkrav i datagrunnlaget |
| Kontraktskrav | Kontraktsflagg er ikke faglig validert som pris- eller tilgjengelighetsrestriksjon |
| Drivstofftypekobling per ROB-/forbruksfelt | Ikke tilstrekkelig avklart til å brukes som hard restriksjon |
| Havner utenfor `P001`-`P004` | Mangler prisgrunnlag og håndteres derfor som ekstern/ukjent bunkring |

## Valideringskontroller

Etter kjøring kontrolleres følgende:

- alle 486 voyage-etapper er behandlet
- ingen modellert beholdning er negativ
- ingen beholdning overstiger kapasitet etter forbruk
- ingen beholdning overstiger kapasitet rett etter bunkring og før forbruk
- kjøp i priset havn skjer bare når havnen finnes i etappens tilgjengelige havner

Disse kontrollene er kjørt mot output fra hovedmodellen og ga ingen brudd.
