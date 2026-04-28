# Kaylee - arbeidsutkast til rapport

Denne filen er et separat arbeidsutkast for samarbeid i gruppen. Innhold herfra kan flyttes inn i `rapport.md` når gruppen er enig om formuleringene.

---

## Arbeidslogg 2026-04-12

### Ferdigstilt i dag

- Gjennomgang av tilgjengelig bunkringsdata i `004 data`.
- Dokumentasjon av datagrunnlag og datakvalitet.
- Rensing av rådata og etablering av aggregert datasett per havn og måned.
- Første utkast til beslutningsvariabler for modellen.
- Første utkast til målfunksjon.
- Første modellinput for modellversjon 1.
- Første Pyomo-struktur for modellversjon 1.

### Under arbeid

- Videre presisering av restriksjoner.
- Avklaring av hvilke ekstra data som trengs for en mer realistisk modell.
- Forberedelse til implementering og testing av modellen når supplerende data eller solver-oppsett er tilgjengelig.

---

## 5.0 Metode og data

### 5.2 Data

#### Hvordan er data samlet inn:

Det foreliggende datasettet er hentet fra filen `004 data/Bunker Lifting List(Worksheet1) (1).csv`. Filen inneholder historiske bunkringshendelser for drivstofftypen `LSF` og er filtrert til de fire mest brukte havnene i materialet: `P001`, `P002`, `P003` og `P004`. Tidsperioden i datasettet strekker seg fra 4. januar 2020 til 30. januar 2025.

Etter at tittel- og filterlinjene i CSV-filen er hoppet over, består observasjonstabellen av 1389 rader. Hver rad representerer en bunkringshendelse og inneholder blant annet informasjon om fartøy, voyage, havn, bestilt mengde, fakturert mengde, pris, leveringsdato, leverandør og supplier.

De viktigste variablene for videre modellering er `Port`, `Vessel`, `Voyage No.`, `Ordered Qty`, `Invoiced Qty`, `Invoice Price`, `Order Price`, `Delivery Date`, `Vendor` og `Supplier`. Datasettet er relativt komplett for de sentrale feltene. Det er ingen manglende verdier i `Port`, `Vessel`, `Voyage No.` eller `Delivery Date`. Samtidig finnes det 10 observasjoner uten `Invoice Price`, 10 observasjoner uten `Invoiced Qty`, 2 observasjoner uten `Supplier`, samt 8 observasjoner med `Ordered Qty = 0` og 8 observasjoner med `Order Price = 0`. Disse observasjonene må håndteres i datavasken før modellen implementeres.

En første oppsummering av materialet er vist i tabellen nedenfor.

| Havn | Antall observasjoner | Total fakturert mengde | Vektet gjennomsnittspris |
| --- | --- | --- | --- |
| P001 | 209 | 113606.88 | 578.75 |
| P002 | 286 | 181419.36 | 610.29 |
| P003 | 368 | 252848.64 | 540.86 |
| P004 | 516 | 320732.69 | 577.06 |

Tabellen viser at `P004` er den mest brukte havnen målt i antall bunkringshendelser, mens `P003` har lavest vektet gjennomsnittspris i utvalget. `P002` fremstår som den dyreste av de fire havnene. Dette indikerer at havnevalg har potensial til å påvirke totale drivstoffkostnader og at datasettet derfor er relevant som grunnlag for en første optimaliseringsmodell.

Datagrunnlaget har samtidig klare begrensninger. Per nå omfatter materialet bare fire havner og én drivstofftype. Datasettet inneholder heller ikke eksplisitte variabler for tankkapasitet, minimumsbeholdning, forbruk mellom havner eller tilgjengelige rutealternativer. Disse størrelsene må derfor estimeres eller formuleres som eksplisitte antagelser i modelleringen.

### 5.2.1 Rensing og aggregering av pris- og volumdata

For videre analyse er det laget en egen rense- og aggregeringsprosess i `006 analysis/01_datagrunnlag/clean_and_aggregate_bunker_data.py`. Prosessen leser råfilen, hopper over tittel- og filterlinjene i toppen av CSV-filen, og standardiserer deretter de sentrale numeriske feltene.

Følgende rensevalg er brukt:

1. `Invoiced Qty` brukes som hovedvariabel for volum. Dersom denne mangler, brukes `Ordered Qty`.
2. `Invoice Price` brukes som hovedvariabel for pris. Dersom denne mangler, brukes `Order Price`.
3. Observasjoner med ikke-positivt volum forkastes.
4. Observasjoner med ikke-positiv pris forkastes.
5. Leveringsdato transformeres til både datoformat og månedsnivå (`YYYY-MM`) for videre tidsaggregering.

Etter rensing beholdes 1381 av 1389 observasjoner. Åtte observasjoner forkastes fordi volumet er null eller ikke-positivt. Ingen observasjoner faller ut på grunn av manglende pris eller manglende volum etter at fallback-reglene er brukt.

Det er også laget et aggregert datasett per havn og måned i `006 analysis/01_datagrunnlag/tab_bunker_monthly_by_port.csv`. Aggregatet inneholder 229 havn-måned-observasjoner fordelt på 61 måneder fra januar 2020 til januar 2025.

De viktigste feltene i månedsaggregatet er:

- `delivery_month`
- `port`
- `transaction_count`
- `total_qty`
- `weighted_avg_price`
- `simple_avg_price`
- `min_price`
- `max_price`
- `unique_vessels`
- `unique_suppliers`

Dette aggregerte datasettet er et bedre utgangspunkt for modellering enn rå transaksjonsdata, fordi prisparameterne blir mer stabile og volumene kan knyttes til en tydelig tidsperiode.

En viktig observasjon er at ikke alle havner har transaksjoner i alle måneder. Det finnes 61 måneder i analyseperioden, men bare 229 havn-måned-kombinasjoner av maksimalt 244 mulige. Særlig mangler `P002` observasjoner gjennom hele 2020. Dette betyr at prisparametere for enkelte havn-måned-kombinasjoner må estimeres eller interpoleres dersom modellen skal bruke et komplett månedsrutenett.

De månedlige prisene varierer også betydelig mellom perioder. For eksempel har `P003` en observert laveste vektede månedspris på 189.34 i april 2020 og en høyeste på 913.00 i juni 2022. Tilsvarende varierer `P004` fra 220.33 i mai 2020 til 1087.85 i juli 2022. Dette understøtter at både havnevalg og tidspunkt kan ha stor betydning for totale bunkringskostnader.

---

## 6.0 Modellering

Med utgangspunkt i tilgjengelige data anbefales det å starte med en deterministisk lineær kostnadsminimeringsmodell for bunkring. Siden datasettet foreløpig dekker fire havner og én drivstofftype, bør første modellversjon avgrenses til disse havnene og `LSF`. Dette gir en modell som er enkel nok til å implementere, men samtidig direkte knyttet til casebedriftens beslutningsproblem.

### 6.1 Klargjøring av beslutningsvariabler

En naturlig beslutningsvariabel er mengden drivstoff som bunkres for et fartøy ved et gitt beslutningstidspunkt i en gitt havn:

$x_{v,t,p}$ = mengde drivstoff bunkret for fartøy $v$ ved tidspunkt eller voyage $t$ i havn $p$

der $v \in V$ er fartøy, $t \in T_v$ er beslutningstidspunkter eller reiser for fartøy $v$, og $p \in P$ er havnene `P001`, `P002`, `P003` og `P004`.

Dersom modellen også skal uttrykke et eksplisitt valg av bunkringshavn, kan vi innføre en binær variabel:

$y_{v,t,p} = 1$ dersom fartøy $v$ bunkrer i havn $p$ på tidspunkt $t$, ellers 0

For å følge drivstoffet gjennom planhorisonten må modellen i tillegg ha en tilstandsvariabel:

$I_{v,t}$ = drivstoffbeholdning for fartøy $v$ etter tidspunkt $t$

Denne beholdningsvariabelen er nødvendig fordi bunkringsbeslutningen i én havn påvirker hvilke valg som er mulige senere i ruten.

### 6.2 Definering av målfunksjon

Målet er å minimere totale drivstoffkostnader:

$\min Z = \sum_{v \in V} \sum_{t \in T_v} \sum_{p \in P} c_{v,t,p} \cdot x_{v,t,p}$

der $c_{v,t,p}$ er pris per enhet drivstoff i havn $p$ for fartøy $v$ ved tidspunkt $t$.

I første modellversjon kan denne prisparameteren estimeres fra `Invoice Price` i datasettet, for eksempel som historisk vektet gjennomsnittspris per havn eller som gjennomsnittspris per havn og måned. En aggregert prisparameter vil være mer robust enn å bruke hver enkelt observasjon direkte, fordi dette reduserer støy og gjør modellen lettere å validere.

### 6.3 Definering av restriksjoner

For at modellen skal gi realistiske løsninger, bør den minst inneholde følgende restriksjoner:

**Beholdningsbalanse**

$I_{v,t} = I_{v,t-1} + \sum_{p \in P} x_{v,t,p} - d_{v,t}$

der $d_{v,t}$ er drivstofforbruk for fartøy $v$ i periode eller voyage $t$.

**Kapasitetsrestriksjon**

$I_{v,t} \leq K_v$

der $K_v$ er tankkapasiteten til fartøy $v$.

**Minimumsbeholdning**

$I_{v,t} \geq I_v^{min}$

der $I_v^{min}$ er en sikkerhetsbuffer for fartøy $v$.

**Kobling mellom havnevalg og bunkringsmengde**

Hvis den binære variabelen $y_{v,t,p}$ brukes, må bunkret volum bare kunne være positivt når havnen faktisk velges:

$x_{v,t,p} \leq M \cdot y_{v,t,p}$

der $M$ er en stor øvre grense for mulig bunkringsmengde.

**Maksimalt ett bunkringsvalg per beslutningstidspunkt**

$\sum_{p \in P} y_{v,t,p} \leq 1$

**Tilgjengelige havner**

$x_{v,t,p} = 0$ dersom havn $p$ ikke er relevant eller tilgjengelig for fartøy $v$ ved tidspunkt $t$.

### 6.4 Hva datasettet støtter direkte

Det opprinnelige pris- og volumdatasettet støtter spesielt godt estimering av prisparametere, historiske volum og sammenligning mot faktisk praksis. Datasettet støtter derimot ikke alene en full operativ modell, fordi sentrale størrelser som faktisk drivstoffbeholdning, minimumsbuffer og forbruk mellom to beslutningspunkter ikke er direkte observert.

Etter den første gjennomgangen er det mottatt supplerende 2025-data for åtte anonymiserte fartøyfiler fordelt på klassene `C001` til `C005`. Filene inneholder blant annet forbruk, `ROB_Fuel_Total`, voyage fra/til og voyage-nummer. Voyage-havnene var opprinnelig UN/Locode, men analysefilene i repoet er pseudonymisert videre slik at havner vises som `Pxxx` og voyage-numre som `VGxxx`. I tillegg er det mottatt verifiserte bunkerskapasiteter per klasse og informasjon om bunkerskontrakt i Singapore og Sør-Korea, samt VLSFO-kontrakt i Rotterdam.

Tilleggsdataene er nå strukturert til hendelses-, etappe- og kapasitetstabeller. De styrker grunnlaget for en senere fartøy- og rutebasert modell, men må valideres mot kontraktsomfang og drivstofftypekobling før de kan erstatte den aggregerte modellversjonen.

Neste steg i analysearbeidet bør derfor være:

1. Rense og aggregere pris- og volumdata per havn og periode.
2. Etablere eksplisitte antagelser eller supplerende parametere for forbruk, kapasitet og havnetilgjengelighet.
3. Implementere en første lineær modell med de fire havnene som beslutningsalternativer.

### 6.5 Supplerende data og gjenværende avklaringer

Følgende supplerende data er nå mottatt fra Odfjell Tankers eller intern dataleverandør:

| Fartøyklasse | Bunkerskapasitet |
| --- | --- |
| C001 | 2,087.006 m3 |
| C002 | 2,061.430 m3 |
| C003 | 1,533.719 m3 |
| C004 | 1,907.080 m3 |
| C005 | 1,024.531 m3 |

<p align="center" style="font-size: 0.9em;"><small><i>Tabell 6.1 Verifisert bunkerskapasitet per anonymisert fartøyklasse.</i></small></p>

De åtte filene `C001 - 1.csv`, `C001 - 2.csv`, `C002 - 1.csv`, `C003 - 1.csv`, `C004 - 1.csv`, `C004 - 2.csv`, `C004 - 3.csv` og `C005 - 1.csv` dekker 2025 og inneholder samlet 3893 rapporteringsrader. De opprinnelige havnekodene er erstattet med 70 interne P-koder, og voyage-numrene er erstattet med 244 interne VG-koder.

Dette svarer på flere av punktene som tidligere manglet:

**Må ha for en god operativ modell**

1. **Tankkapasitet per fartøyklasse**
   Dette kan brukes til å definere $K_v$ i kapasitetsrestriksjonen når klassene kobles til modellens fartøysindeks.

2. **Forbruk mellom beslutningspunkter**
   De nye filene inneholder forbruksfelt som kan brukes til å estimere $d_{v,t}$ etter rensing og harmonisering.

3. **Beholdning ved start eller ROB-data**
   Feltet `ROB_Fuel_Total` gir et bedre grunnlag for å initialisere eller kontrollere $I_{v,t}$ enn det opprinnelige pris- og volumdatasettet.

4. **Rute- eller havnetilgjengelighet per voyage**
   Feltene `Voyage_From`, `Voyage_To` og `Voyage_Number` gir havnesekvens på voyage-nivå. Dette må fortsatt struktureres før det kan brukes som tilgjengelighetsrestriksjon.

**Gjenværende avklaringer**

5. **Kobling mellom anonymiserte fartøyklasser og opprinnelig prisdata**
   Det må avklares om klassene `C001` til `C005` kan kobles direkte eller indirekte til fartøyfeltet i transaksjonsdatasettet.

6. **Kontraktsinformasjon eller innkjøpsregime**
   Kontrakter i Singapore, Sør-Korea og Rotterdam må oversettes til konkrete havnekoder, drivstofftyper, perioder og eventuelle pris- eller tilgjengelighetsregler.

7. **Prisdefinisjon og kostnadskomponenter**
   Det bør avklares om `Invoice Price` er direkte sammenlignbar mellom havner og over tid, eller om den inkluderer ulike tillegg som bargekostnader, avgifter eller andre påslag.

8. **Leveringsledetid og bunkringsbegrensninger**
   For eksempel minimumsordre, maksvolum per leveranse eller begrensninger knyttet til supplier eller barge.

9. **Flere havner enn de fire mest brukte**
    Hvis problemstillingen skal speile reell beslutningsstøtte bredere, vil det være nyttig å få med flere alternative bunkerhavner.
### 6.6 Modellversjon 1 basert på dagens data

Selv om datasettet ikke er tilstrekkelig til å utvikle en full operativ bunkringsmodell, er det godt nok til å etablere en første kvantitativ modellversjon. Denne modellen bør forstås som en forenklet kostnadsminimeringsmodell basert på historiske pris- og volumdata per havn og periode.

Formålet med modellversjon 1 er ikke å gjenskape hele den operative beslutningssituasjonen for hvert fartøy, men å analysere hvordan valg av havn og tidspunkt påvirker bunkringskostnadene når analysen begrenses til de fire observerte havnene og de historiske prisene i datasettet.

#### Sett

La:

- $H$ være mengden havner, der $H = \{P001, P002, P003, P004\}$
- $T$ være mengden perioder

I denne første modellen er det naturlig å la periodene være måneder, slik at $T$ dekker månedene fra januar 2020 til januar 2025.

#### Parametere

Følgende parametere kan defineres med utgangspunkt i dagens datagrunnlag:

- $p_{h,t}$ = historisk pris i havn $h$ i periode $t$
- $D_t$ = samlet drivstoffbehov i periode $t$
- $f_{h,t}$ = 1 dersom havn $h$ er tilgjengelig i periode $t$, ellers 0

Prisparameteren $p_{h,t}$ kan hentes fra `weighted_avg_price` i det månedlige aggregatet i `tab_bunker_monthly_by_port.csv`.

Behovsparameteren $D_t$ kan i første omgang settes lik samlet observert bunkret volum i periode $t$ på tvers av de fire havnene. Dette er en forenkling, men det gir modellen et definert behov per periode som kan brukes til å analysere kostnadsminimerende fordeling.

Tilgjengelighetsparameteren $f_{h,t}$ kan i modellversjon 1 settes til 1 dersom havnen har observasjoner i perioden, og 0 ellers. Dette er ikke det samme som reell operativ havnetilgjengelighet, men det sikrer at modellen bare bruker havn-periode-kombinasjoner hvor dere faktisk har prisdata.

#### Beslutningsvariabel

Beslutningsvariabelen defineres som:

$x_{h,t}$ = mengde drivstoff som skal bunkres i havn $h$ i periode $t$

Her gjelder $x_{h,t} \geq 0$.

Denne formuleringen arbeider på aggregert nivå og er derfor bedre tilpasset dagens datagrunnlag enn en fartøybasert modell.

#### Målfunksjon

Målet er å minimere totale bunkringskostnader over hele planperioden:

$\min Z = \sum_{t \in T} \sum_{h \in H} p_{h,t} \cdot x_{h,t}$

Denne målfunksjonen er lineær og direkte koblet til de observerte historiske prisforskjellene mellom havnene.

#### Restriksjoner

Den enkleste og mest naturlige restriksjonsstrukturen i modellversjon 1 er:

**1. Dekke behov i hver periode**

$\sum_{h \in H} x_{h,t} \geq D_t \quad \forall t \in T$

Denne restriksjonen sikrer at samlet bunkret volum i perioden er tilstrekkelig til å dekke det definerte behovet.

**2. Kun bunkre i tilgjengelige havner**

$x_{h,t} \leq M \cdot f_{h,t} \quad \forall h \in H, t \in T$

der $M$ er en stor konstant.

Denne restriksjonen gjør at modellen bare kan velge bunkring i havner og perioder der vi faktisk har prisgrunnlag eller har valgt å definere havnen som tilgjengelig.

**3. Ikke-negativitet**

$x_{h,t} \geq 0 \quad \forall h \in H, t \in T$

Dette er tilstrekkelig for en første lineær modellversjon.

#### Tolkning av modellversjon 1

Denne modellen svarer på følgende spørsmål:

Hvordan kan et gitt bunkringsbehov i hver periode fordeles mellom de fire observerte havnene slik at totale kostnader blir lavest mulig, gitt historiske prisforskjeller og begrensninger i tilgjengelighet?

Modellen er derfor godt egnet som en første kvantitativ analyse av kostnadsbesparelsespotensial. Den kan brukes til å sammenligne historisk observert bunkerfordeling med en kostnadsminimerende fordeling under forenklede forutsetninger.

#### Fordeler med modellversjon 1

- Den kan implementeres direkte med dagens data.
- Den er lineær og enkel å løse i Pyomo.
- Den gir et tydelig kvantitativt svar på hvordan prisforskjeller mellom havner påvirker kostnader.
- Den er godt egnet som første steg før en mer avansert modellutvidelse.

#### Begrensninger ved modellversjon 1

- Modellen arbeider på aggregert nivå og skiller ikke mellom fartøy.
- Den modellerer ikke beholdning om bord.
- Den bruker periodebehov som en proxy for forbruk, ikke faktisk forbruk.
- Den tar ikke eksplisitt hensyn til ruter, tankkapasitet eller sikkerhetsbuffer.
- Tilgjengelighet er definert ut fra observerte data, ikke fra faktisk operativ havnetilgang.

#### Faglig vurdering

Modellversjon 1 er likevel metodisk forsvarlig som første analysemodell i prosjektet. Den er kvantitativ, transparent og direkte koblet til det datagrunnlaget dere faktisk har. I rapporten vil det derfor være naturlig å presentere denne modellen som et første beslutningsstøtteverktøy og samtidig være tydelig på at en mer realistisk operativ modell krever supplerende data om fartøy, forbruk, beholdning og ruter.

#### Kobling til Pyomo-modellen

Denne modellstrukturen samsvarer godt med den generelle Pyomo-modellen dere tidligere har sett på:

```python
# Sets
H = range(4)        # Havner
T = range(N)        # Perioder

# Parameters
p = {(h, t): ... for h in H for t in T}
D = {t: ... for t in T}
f = {(h, t): ... for h in H for t in T}
M = 1e6

# Decision variable
x[h, t] >= 0

# Objective
min sum(p[h, t] * x[h, t] for h in H for t in T)

# Constraints
sum(x[h, t] for h in H) >= D[t]                for all t
x[h, t] <= M * f[h, t]                         for all h, t
```

Det betyr at den modellen dere allerede har diskutert, er et godt og naturlig utgangspunkt for første implementering med dagens datagrunnlag.

#### Modellfiler for versjon 1

For å gjøre det enkelt å se hvilke filer som tilhører denne modellen, er alle modellinputfiler lagt i `006 analysis/02_modell_v1` og navngitt med prefikset `tab_model_v1_` eller `data_model_v1_`.

Følgende filer hører til modellversjon 1:

- `tab_model_v1_price_by_port_month.csv`
  Prisparameter `p[h,t]` for hver havn og måned.

- `tab_model_v1_demand_by_month.csv`
  Behovsparameter `D[t]` per måned.

- `tab_model_v1_availability_by_port_month.csv`
  Tilgjengelighetsparameter `f[h,t]`, der `available_flag = 1` betyr at havnen er observert i perioden.

- `data_model_v1_parameters.json`
  Samlet metadata for modellversjon 1, inkludert sett, filkoblinger og reglene som er brukt for pris, behov og tilgjengelighet.

Navnekonvensjonen er dermed:

- `tab_bunker_...` = datagrunnlag og rensede/aggregert data
- `tab_model_v1_...` = modellinput for første modellversjon
- `data_model_v1_...` = strukturert metadata for første modellversjon

Det er også laget en første kjørbar modellfil i `006 analysis/02_modell_v1/run_model_v1_pyomo.py`, som leser disse modellfilene direkte når `pyomo` og en solver er tilgjengelig.
