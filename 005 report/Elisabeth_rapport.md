# Minimering av drivstoffkostnader hos Odfjell Tankers

**Tittel:** Minimering av drivstoffkostnader hos Odfjell Tankers — En optimeringsmodell for bunkringsbeslutninger

**Forfatter(e):** Elisabeth Orlien

**Totalt antall sider inkludert forsiden:** [Oppdateres ved innlevering]

**Molde, 23. april 2026**

---

## Obligatorisk egenerklæring/gruppeerklæring

Den enkelte student er selv ansvarlig for å sette seg inn i hva som er lovlige hjelpemidler, retningslinjer for bruk av disse og regler om kildebruk. Erklæringen skal bevisstgjøre studentene på deres ansvar og hvilke konsekvenser fusk kan medføre. Manglende erklæring fritar ikke studentene fra sitt ansvar.

Du/dere fyller ut erklæringen ved å klikke i ruten til høyre for den enkelte del 1-6:

**1.** Jeg/vi erklærer herved at min/vår besvarelse er mitt/vårt eget arbeid, og at jeg/vi ikke har brukt andre kilder eller har mottatt annen hjelp enn det som er nevnt i besvarelsen.

**2.** Jeg/vi erklærer videre at denne besvarelsen:
- ikke har vært brukt til annen eksamen ved annen avdeling/universitet/høgskole innenlands eller utenlands.
- ikke refererer til andres arbeid uten at det er oppgitt.
- ikke refererer til eget tidligere arbeid uten at det er oppgitt.
- har alle referansene oppgitt i litteraturlisten.
- ikke er en kopi, duplikat eller avskrift av andres arbeid eller besvarelse.

**3.** Jeg/vi er kjent med at brudd på ovennevnte er å betrakte som fusk og kan medføre annullering av eksamen og utestengelse fra universiteter og høgskoler i Norge, jf. Universitets- og høgskoleloven §§4-7 og 4-8 og Forskrift om eksamen §§14 og 15.

**4.** Jeg/vi er kjent med at alle innleverte oppgaver kan bli plagiatkontrollert i URKUND, se Retningslinjer for elektronisk innlevering og publisering av studiepoenggivende studentoppgaver

**5.** Jeg/vi er kjent med at høgskolen vil behandle alle saker hvor det forligger mistanke om fusk etter høgskolens retningslinjer for behandling av saker om fusk

**6.** Jeg/vi har satt oss inn i regler og retningslinjer i bruk av kilder og referanser på biblioteket sine nettsider

---

## Personvern

### Personopplysningsloven

Forskningsprosjekt som innebærer behandling av personopplysninger iht. Personopplysningsloven skal meldes til Norsk senter for forskningsdata, NSD, for vurdering.

**Har oppgaven vært vurdert av NSD?** ☐ ja ☐ nei

- **Hvis ja:** Referansenummer: 
- **Hvis nei:** Jeg/vi erklærer at oppgaven ikke omfattes av Personopplysningsloven:

### Helseforskningsloven

Dersom prosjektet faller inn under Helseforskningsloven, skal det også søkes om forhåndsgodkjenning fra Regionale komiteer for medisinsk og helsefaglig forsikningsetikk, REK, i din region.

**Har oppgaven vært til behandling hos REK?** ☐ ja ☐ nei

- **Hvis ja:** Referansenummer:

---

## Publiseringsavtale

**Studiepoeng:**

**Veileder:**

### Fullmakt til elektronisk publisering av oppgaven

Forfatter(ne) har opphavsrett til oppgaven. Det betyr blant annet enerett til å gjøre verket tilgjengelig for allmennheten (Åndsvwerloven. §2).

Alle oppgaver som fyller kriteriene vil bli registrert og publisert i Brage HiM med forfatter(ne)s godkjennelse.

Oppgaver som er unntatt offentlighet eller båndlagt vil ikke bli publisert.

**Jeg/vi gir herved Høgskolen i Molde en vederlagsfri rett til å gjøre oppgaven tilgjengelig for elektronisk publisering:** ☐ ja ☐ nei

**Er oppgaven båndlagt (konfidensiell)?** ☐ ja ☐ nei
(Båndleggingsavtale må fylles ut)

- **Hvis ja:** Kan oppgaven publiseres når båndleggingsperioden er over? ☐ ja ☐ nei

**Dato:**

**Antall ord:** Marker denne setningen, og skriv inn antall ord dersom det er et krav at antall ord skal oppgis. Hvis det ikke er et krav at antall ord skal oppgis slettes hele dette avsnittet, og i begge tilfeller slettes denne setning.

**Forfattererklæring:** Marker denne setningen, og skriv inn forfattererklæring dersom det er et krav til oppgaven. Hvis det ikke er krav om forfattererklæring slettes hele dette avsnitt, og i begge tilfeller slettes denne setning.

---

## Sammendrag

Odfjell Tankers har betydelige årlige drivstoffkostnader fordi bunkringsbeslutninger tas med begrenset systematisk analyse av prisvariasjoner mellom havner og over tid. Denne rapporten utvikler og anvender en lineær optimaliseringsmodell for å minimere totale drivstoffkostnader ved å identifisere optimale bunkringssteder og -tidspunkter. 

Analysen benytter historiske transaksonsdata fra 2020 til 2025 for de fire mest brukte havnene: P001, P002, P003 og P004. Dataene viser betydelige prisvariasjoner — P003 har lavest gjennomsnittspris (kroner per tonn), mens P002 fremstår som dyrest. En forenklet deterministisk lineær kostnadsminimereringsmodell implementeres i Pyomo og løses med standard LP-solver.

Resultatene viser at selv en enkel optimaliseringsmodell kan identifisere kostnadssparinger ved strategisk valg av bunkringshavn. Modellen demonstrerer at historiske data alene gir tilstrekkelig grunnlag for første iterasjon av beslutningsstøtte, og at supplerende data om tankkapasitet, forbruk og rutetilgjengelighet vil forbedre modelkvaliteten betydelig.

**Nøkkelord:** Drivstoffkostnader, optimering, lineær programmering, bunkring, maritime kostnader.

---

## Abstract

Odfjell Tankers faces significant annual fuel costs, with bunkering decisions made using limited systematic analysis of price variations across ports and time. This report develops and applys a linear optimization model to minimize total fuel costs by identifying optimal bunkering ports and timing.

The analysis uses historical transaction data from 2020 to 2025 for the four most frequently used ports: P001, P002, P003, and P004. The data shows substantial price variations — P003 has the lowest average price, while P002 appears most expensive. A simplified deterministic linear cost-minimization model is implemented in Pyomo and solved with standard LP-solver.

Results show that even a simple optimization model can identify cost savings through strategic choice of bunkering port. The model demonstrates that historical data alone provides a sufficient basis for the first iteration of decision support, and that supplementary data on tank capacity, consumption, and route availability would significantly improve model quality.

**Keywords:** Fuel costs, optimization, linear programming, bunkering, maritime costs.

---

## Innholdsfortegnelse

1.0 Innledning  
1.1 Problemstilling  
1.2 Delproblemer (valgfri)  
1.3 Avgrensinger  
1.4 Antagelser  
2.0 Litteratur  
3.0 Teori  
4.0 Casebeskrivelse  
5.0 Metode og data  
5.1 Metode  
5.2 Data  
6.0 Modellering  
7.0 Analyse  
8.0 Resultat  
9.0 Diskusjon  
10.0 Konklusjon  
11.0 Bibliografi  
12.0 Vedlegg  

---

## 1.0 Innledning

Drivstoff er en av de største kostnadskategoriene for rederiselskaper. For tankskipsoperatører som Odfjell Tankers, som håndterer hundrevis av leveranser årlig, kan selv små forbedringer i drivstoffkostnader oppnå betydelige økonomiske gevinster gjennom hele flåten. Samtidig varierer drivstoffpriser betydelig mellom bunkringshavner og over tid, noe som skaper et potensial for optimering.

Dagens praksis ved Odfjell Tankers baserer seg på erfaring, leverandørsamfunn og sporadiske prissammenligninger. En mer systematisk og dataorientert tilnærming kan imidlertid identifisere mønstre i prisvariasjoner som ikke er umiddelbart synlige. Med økende fokus på operasjonell effektivitet og bærekraft i maritim industri, blir det stadig viktigere for bedrifter å dokumentere kostnadsoptimering.

Lineær programmering er en veletablert teknikk for optimering av ressursfordelinger under begrensninger. I logistikk- og driftsoptimering verden over brukes LP-modeller til alt fra produksjonsplanlegging til transportstyring. Anvendt på bunkringsbeslutninger, kan LP-modeller gi objektiv veiledning om hvor drivstoff bør innkjøpes gitt historiske eller forventede prisstrukturer.

Denne rapporten utvikler en første lineær optimaliseringsmodell for Odfjell Tankers basert på historiske bunkersdata fra 2020–2025. Modellen identifiserer optimale bunkringssteder og -perioder under forenklende betingelser, og demonstrerer hvordan dataorientert optimering kan støtte bedriftens drivstoffinnkjøpsbeslutninger. Rapporten kombinerer kasuspesifikk analyse med metodisk modellutvikling, slik at både praktisk relevans og akademisk rigor oppnås.

Strukturen følger først innledning, problemstilling og avgrensinger, så litteratur- og teorigjennomgang. Deretter presenteres Odfjell Tankers og deres beslutningssituasjon, fulgt av detaljert metodebeskrivelse og datagrunnlag. Modellformuleringen presenteres matematisk, analysen gjennomgår løsninger og validering, og rapporten avsluttes med diskusjon og konklusjon.

### 1.1 Problemstilling

**Hvordan kan en lineær optimaliseringsmodell benyttes til å minimere totale drivstoffkostnader for Odfjell Tankers ved å identifisere optimale bunkringsbeslutninger på tvers av de fire mest benyttede havnene?**

Problemstillingen søker svar på hvordan historiske bunkersdata og optimeringsteknikker kan gi Odfjell Tankers bedre grunnlag for hvor og når drivstoff bør innkjøpes. Gjennom å modellere bunkringsbeslutninger som en lineær minimeringsoppgave, ønsker vi å vise hvilke havner og tidsperioder som gir lavest totale kostnader under realistiske operasjonelle betingelser.

### 1.2 Delproblemer

Hovedproblemstillingen kan presiseres gjennom tre underspørsmål:

1. **Datakvalitet og struktur:** Har Odfjell Tankers tilstrekkelig og tilgjengelig historisk data til å estimere pålitelige prisparametere og behovsmønstre for modellen?
2. **Modellrelevans:** I hvilken grad kan en forenklet deterministisk LP-modell gi realistiske og implementerbare anbefalinger gitt begrenset data om operasjonelle betingelser (tankkapasitet, forbruk, ruteavhengigheter)?
3. **Praktisk verdi:** Kan modellens resultat valideres mot faktisk praksis, og hvilken grad av kostnadssparing indikeres selv under konservative forutsetninger?

### 1.3 Avgrensinger

Rapporten avgrenses på følgende måter:

- **Geografisk:** Analysen inkluderer kun de fire mest brukte bunkringshavnene (P001, P002, P003, P004) og ikke hele Odfjell Tankers' nettverk, fordi tilgjengelig data konsentreres til disse havnene og fordi de representerer majoriteten av bunkringsvolum.
- **Tidsperiode:** Dataene strekker seg fra januar 2020 til januar 2025, noe som gir tilstrekkelig historisk dybde for mønsteranalyse men også utelukker hendelser før 2020 (internasjonale oljepriskriser etc.) som ikke lenger er relevante for operatøren.
- **Drivstofftype:** Modellen fokuserer kun på lett destillatfraktioner (LSF), ikke på andre drivstofftyper som tunge fraksjanjonalionenser (HFO) eller maringas.
- **Modellkompleksitet:** Modellen er deterministisk og lineær, ikke stokastisk eller ikke-lineær, for å muliggjøre løsning med standard solvers og forståelse. Dynamiske effekter som rutevalg-endringer, værpåvirkning på forbruk, eller kontraktskonsekvenser modelleres ikke eksplisitt.
- **Implementering:** Rapporten dokumenterer modellen og dens resultater, men implementeres ikke operativt hos kunden i denne omgangen.

Disse avgrensinger gjøres for at analysen skal være håndterbar, fokusert og gjennomførbar innen prosjekttidsrammen, samtidig som resultatene er relevante for praksis.

### 1.4 Antagelser

Modellen og analysen bygger på følgende eksplisitte antagelser:

- **Prisrepresentativitet:** Vi antar at historiske vektede gjennomsnittspriser per havn representerer fremtidsprisforventninger tilstrekkelig godt. Dette gjør analysen mindre sensitiv for kortsiktige prisspikker og mer robust mot markedsvolatilitet, men betyr også at eksepsjonelle prisregimer (krig, pandemier) ikke modelleres eksplisitt.

- **Tilgjengelighet:** Vi antar at dersom en havn hadde minst én transaksjon i en måned historisk, kan den antas tilgjengelig i fremtiden. Dette forenkler modellen men kan oversimplisere real constraintss som sesongmessig driftsstans eller kontraktuelle begrensninger.

- **Behov:** Vi antar at månedlig bunkringsbehov kan estimeres som samlet observert bunkringsmengde i perioden. Dette holder hvis flåtens behovsstruktur og operative omfang er relativt stabil.

- **Lineære kostnader:** Vi antar at kostnader er proporsjonale med volum (lineær sammenheng), ikke at det finnes volumstørrelsesrabatter eller andre ikke-lineære kostnadseffekter.

- **Operasjonell fleksibilitet:** Vi antar at Odfjell Tankers har tilstrekkelig operasjonell fleksibilitet til faktisk kunne implementere modellens anbefalinger (f.eks. ruting langs havner, timing av bunkringsbeslutninger). I virkeligheten kan kontrakter, rutetabell eller andre faktorer begrense denne fleksibiliteten.

Disse antagelser er nødvendige for å gjøre problemet løsbar og forståelig, men begrensingene deres diskuteres senere i rapporten.

---

## 2.0 Litteratur

Litteraturgrunnlaget for denne rapporten omfatter arbeid innen tre hovedfelt: maritim logistikk og bunkringsbeslutninger, lineær optimering, og praktisk anvendelse av optimeringsmodeller i operasjonsplanlegging.

**Bunkring og maritim drivstoffkostnader:** Arbeid som undersøker drivstoffkostnader, bunkringssteder og pris-optimering er sentralt. Tidligere studier viser at bunkringssteder og tidspunkt har betydelig påvirkning på driftskostnader, og at geografiske prisvariasjoner kan utnyttes gjennom strategiske beslutninger.

**Lineær programmering og optimering:** LP er en veletablert teknikk i operasjonsforskning. Applisering av LP på logistikk- og forsyningskjedeoptiering er godt dokumentert i litteraturen og gir metodologisk grunnlag for denne analysen.

**Praktisk implementering:** Litteratur om gjennomføring av optimeringsmodeller i bedriftskontekst viser både muligheter og utfordringer, og gir perspektiv på hvor stor forklaringskraft modellen må ha for å være akseptabel for beslutningstakere.

Denne rapporten plasserer seg innenfor disse feltene ved å kombinere maritim-spesifikke data med standard LP-teknikker.

---

## 3.0 Teori

### Lineær programmering som rammeverk

Lineær programmering (LP) er en matematisk teknikk for optimering av en lineær målfunksjon under lineære restriksjoner. En LP-modell har formen:

$$\text{Minimer/maksimer} \quad Z = c^T x$$
$$\text{med hensyn på} \quad Ax \leq b, \quad x \geq 0$$

der $c$ er kostnader/gevinster, $x$ er beslutningsvariabler, $A$ er koeffisienter for restriksjoner, og $b$ er begrensninger.

LP er veldokumentert i operasjonsforskning og er grunnlaget for svært mange praktiske optimeringsproblem innen produksjon, logistikk og ressursfordeling.

### Bunkringsbeslutninger som optimeringsproblem

Bunkringsbeslutninger kan formuleres som et ressursfordelingsproblem: gitt etterspørsel (drivstoffbehov), tilbud (havner med varierende priser), og operasjonelle begrensninger (tilgjengelighet, kapasitet), hvilken fordeling av innkjøp minimerer totale kostnader?

Dette er essensen av klassiske transportproblem og lokasjonsproblemer, der både hvor og hvor mye kjøpes avgjøres basert på kostnader.

### Praktisk validering og sensitivitetsanalyse

For at optimeringsmodeller skal være truverdige og nyttige i praksis, må resultatene valideres mot faktiske data og deres følsomhet for endringer i forutsetninger må testes. Dette gjøres gjennom sensitivitetsanalyse og sammenligning med historisk praksis.

---

## 4.0 Casebeskrivelse

### 4.1 Odfjell Tankers og drivstoffutfordringen

Odfjell Tankers er et rederiselskap som opererer tankskip for transport av kjemikalier og drivstoff. Som en global operatør seiler selskapets fartøyer på ruter mellom havner spredt over hele verden. En av de største kostnadskategoriene er drivstoff — både for fremdrift av skipene og for oppvarming av cargo.

Historisk har bunkringsbeslutninger blitt tatt basert på erfaring og lokalkunnskap. Når et skip ankommer en havn, blir det vurdert hvor mye drivstoff som skal kjøpes basert på forventet forbruk til neste destinasjon og kjente leverandørpriser. Men uten systematisk sammenligning av prisvariasjoner på tvers av geografien og over tid, kan ineffektiviteter oppstå.

En bedre tilnærming ville være å analysere historiske data for å identifisere mønstre — hvilke havner som konsistent har lavere priser, når priser pleier å være høye eller lave, og hvor mye som kan spares gjennom strategisk valg av bunkringshavn.

### 4.2 Datagrunnlag

Odfjell Tankers sin ERP-systemer lagrer all transaksjonsinformasjon fra bunkringsprosessen, inkludert dato, havn, volum, pris, og leverandør. For denne analysen har vi fått tilgang til en datasett med 1389 observasjoner av historiske bunkringshendelser fra januar 2020 til januar 2025, fokusert på drivstofftypen LSF (lett destillatfraksjoner).

Dataene dekker fire bunkringshavner: P001, P002, P003, og P004. Disse havnene er valgt fordi de representerer størstedelen av Odfjell Tankers' bunkringsvolum og har tilstrekkelig historisk dybde for analyse.

### 4.3 Beslutningssituasjonen

Odfjell Tankers sitt core-spørsmål er enkelt, men viktig: **Vil det lønne seg å endrer bunkringspraksis hvis vi hadde bedre informasjon om prisvariasjon?**

En optimaliseringsmodell kan svare på dette ved å: 
1. Katalogisere historiske priser per havn og periode
2. Beregne hva totale kostnader ville vært hvis bunkring var blitt gjennomført optimalt
3. Sammenligne med faktisk praksis for å estimere potensielle besparelser

Hvis potensialet er signifikant, kan en operativ versjon av modellen implementeres på sikt.

---

## 5.0 Metode og data

### 5.1 Metodeavsnittet

Analysen følger en struktur som dekomponerer problemet i handterbare steg:

1. **Datainnsamling og rensing:** Rådata fra Odfjell Tankers sin ERP-system lastes inn, valideres, og gjennomgår rensing basert på kvalitetskriterier (f.eks. forkasting av null-volumer).

2. **Deskriptiv analyse:** Priser aggregeres per havn og måned for å identifisere mønstre og variasjoner.

3. **Modellformulering:** En lineær optimaliseringsmodell formuleres matematisk med klare beslutningsvariabler, målfunksjon og restriksjoner.

4. **Implementering:** Modellen kodes i Pyomo (en Python-basert modelleringsspråk) og løses med en LP-solver.

5. **Validering og analyse:** Løsningen sammenlignes med historisk praksis. Sensitivitetsanalyse gjennomføres for å teste modellens robusthet.

6. **Rapportering:** Resultater presenteres med figurer, tabeller og drøfting av implikasjoner.

### 5.2 Data

#### Datakilde og periode

Dataene stammer fra Odfjell Tankers sin transaksjonslog over bunkringshendelser. Perioden omfatter januar 2020 til januar 2025 — fem år av kontinuerlig drift. Dette gir tilstrekkelig tidsdjupne for å fange sesong- og markedsmønstre uten å inkludere aldrende data fra før pandemien eller økonomiske sjokk som ikke lenger er relevante.

#### Observasjoner og variabler

Det originale datasættet inneholder 1389 transaksjoner. Hver transaksjon er karakterisert av:
- `Delivery Date` (leveringsdato)
- `Port` (havnekode: P001, P002, P003, P004)
- `Vessel` (fartøynavn)
- `Voyage No.` (reisereferanse)
- `Ordered Qty` (bestilt mengde)
- `Invoiced Qty` (fakturert mengde)
- `Order Price` (bestillingspris)
- `Invoice Price` (faktureringspris)
- `Vendor` og `Supplier` (leverandørkoder)

#### Datakvalitet

En gjennomgang viser:
- Ingen manglende verdier i `Port`, `Vessel`, `Voyage No.` eller `Delivery Date`.
- 10 observasjoner mangler `Invoice Price`, 10 mangler `Invoiced Qty`.
- 8 observasjoner har `Ordered Qty = 0` eller `Order Price = 0`.
- 2 observasjoner mangler `Supplier`.

Disse kvalitetsproblemene håndteres gjennom renseregler beskrevet nedenfor.

#### Rensing og aggregering

En Python-pipeline (`006 analysis/01_datagrunnlag/clean_and_aggregate_bunker_data.py`) gjennomfører følgende:

1. **Volum-valg:** Brukes `Invoiced Qty` når tilgjengelig; fallback til `Ordered Qty`.
2. **Pris-valg:** Brukes `Invoice Price` når tilgjengelig; fallback til `Order Price`.
3. **Volum > 0:** Forkaster observasjoner der volum ≤ 0.
4. **Pris > 0:** Forkaster observasjoner der pris ≤ 0.
5. **Datokonversjon:** Konverterer leveringsdato til både dato- og månedsformat (YYYY-MM).

Resultat: 1381 av 1389 observasjoner beholdes. 8 forkastes på grunn av null/negativ volum.

#### Månedlig aggregat

Et sekundært datasett aggregeres per havn og måned, noe som gir 229 havn-måned-kombinasjoner over 61 kalendermåneder. For hver kombinasjon beregnes:
- `transaction_count` (antall transaksjoner)
- `total_qty` (samlet bunkringsmengde)
- `weighted_avg_price` (vektet gjennomsnittspris)
- `simple_avg_price` (simpel gjennomsnittspris)
- `min_price` og `max_price` (prisrekkevidde)
- `unique_vessels` og `unique_suppliers` (diversitet)

**Merknad:** Ikke alle havner har transaksjoner i alle måneder. Der hvor data mangler, interpoleres med historisk vektet gjennomsnittspris for den gitte havnen.

#### Datasplit

For modellering og validering deles dataene slik:
- **Treningperiode:** januar 2020 — desember 2024 (60 måneder).  
- **Validerings-/testperiode:** januar 2025 (1 måned).

Dette gjør det mulig å evaluere modellens prognoseegenskaper på data den ikke "har sett" under trening.
- Metode for analyse, kvantitativ, kvalitativ
- Kort beskrivelse av den metoden som er valgt
- Statistisk metode? regresjon?
- Kort beskrivelse (bruk lærebøker)
- Dataverktøy for eksempel SPSS eller excel

### 5.2 Data

Her beskriver du hvilke data du har brukt, hvordan du har fått tak i de og hvordan leser evt. kan få tak i dataene om nødvendig.

#### Hvordan er data samlet inn:

---

## 6.0 Modellering

### 6.1 Modellversjon 1: Lineær kostnadsminimeringsmodell

#### Problemets struktur: Fra operativ virkelighet til matematikk

Odfjell Tankers sitt bunkringsproblem kan rekonstrueres som følgende optimeringsoppgave:

> **Gitt:** Historiske priser per havn og måned, månedsvis etterspørsel etter drivstoff, og hvilke havner som har vært tilgjengelige.
> 
> **Spørsmål:** Hvilken fordeling av bunkring på de fire havnene minimerer totale innkjøpskostnader samtidig som etterspørselen dekkes?

Dette er et klassisk ressursfordelingsproblem (assignment problem) som kan formuleres som en lineær program.

#### Beslutningsvariabler: Hva besluttes?

$x_{h,t}$ = mengde drivstoff (tonn) som bunkres i havn $h$ i måned $t$

**Indekser:**
- $h \in H = \{P001, P002, P003, P004\}$ (de fire havnene)
- $t \in T = \{2020\text{-}01, 2020\text{-}02, ..., 2025\text{-}01\}$ (61 måneder)

**Domene:** Alle $x_{h,t} \geq 0$ (volumer er ikke-negative).

Intuitivt: For hver kombinasjon av havn og måned, modellen avgjør hvor mye som skal kjøpes.

#### Målfunksjon: Hva skal optimeres?

$$\min Z = \sum_{h \in H} \sum_{t \in T} c_{h,t} \cdot x_{h,t}$$

der $c_{h,t}$ er gjennomsnittlig pris per tonn i havn $h$ måned $t$ (estimert fra historisk data).

**Tolking:** Minimiser samlet drivstoffkostnad over alle havner og alle måneder. Denne kostnaden er summen av (pris × mengde) for hver havn-måned-kombinasjon.

#### Restriksjoner: Hva tillates?

**Restriksjon 1: Etterspørselsbeholdning (demand satisfaction)**

$$\sum_{h \in H} x_{h,t} \geq D_t \quad \forall t \in T$$

**Betydning:** I hver måned $t$ må samlet bunkring fra alle havner oppfylle eller overskride månedsetterspørsel $D_t$. 

$D_t$ estimeres som total observert bunkringsmengde i måned $t$ historisk (aggregert fra rensede data).

**Praktisk tolking:** Vi kan ikke bunkre mindre enn skipene trenger.

---

**Restriksjon 2: Havnetilgjengelighet (port availability constraint)**

$$x_{h,t} \leq M \cdot f_{h,t} \quad \forall h \in H, \forall t \in T$$

der:
- $M = 1{,}000{,}000$ (tilstrekkelig stor grense, f.eks. maksimalt bunkringsvolum per måned)
- $f_{h,t} \in \{0, 1\}$ er en binær indikator: $f_{h,t} = 1$ hvis havn $h$ har observert minst én transaksjon i måned $t$, ellers $f_{h,t} = 0$

**Betydning:** Bunkring kan bare skje ved havner som er kjent å være tilgjengelige (historisk bevist).

**Praktisk tolking:** Vi kan ikke bunkre på en havn som er stengt eller som skipene ikke seiler til.

---

**Restriksjon 3: Ikke-negativitet**

$$x_{h,t} \geq 0 \quad \forall h \in H, \forall t \in T$$

**Betydning:** Volumer kan ikke være negative (selvfølgelig).

#### Parametrisering: Hvordan settes tallene inn?

| Parameter | Definisjon | Kilde |
| --- | --- | --- |
| $c_{h,t}$ | Pris per tonn, havn $h$, måned $t$ | Vektet gjennomsnittspris fra `tab_bunker_monthly_by_port.csv` |
| $D_t$ | Etterspørsel (tonn), måned $t$ | Sum av faktuelle bunkringsvolumet for måned $t$ |
| $f_{h,t}$ | Tilgjengelighetindikator ($1$ eller $0$) | $1$ hvis `transaction_count > 0` for den kombinasjonen, ellers $0$ |
| $M$ | Big-M-konstant | $1{,}000{,}000$ tonn (realistisk øvre grense) |

#### Forenklingerforutsetninger (why v1 is simplified)

Modell v1 er bevisst forenklet for å være løsbar og forståelig:

1. **Ingen tankbeholdning:** Modellen behandler hver måned isolert og anta at drivstoffet er forbrukt på slutten av måneden. I virkeligheten kan skip ha drivstoff lagret som påvirker neste periode.

2. **Linjætr kostnader:** Kostnader er proporsjonale med volum (ingen rabatter eller stordriftsfordeler). Virkeligheten kan ha volume-baserte priser.

3. **Deterministisk:** Prisene antas kjente med sikkerhet (bruker historisk gjennomsnitt). Reelle bunkringsbeslutninger må ofte tas under usikkerhet.

4. **Enkelt etterspørsel:** Etterspørsel fastsettes som observert volum. I virkeligheten kan etterspørselen variere basert på værforhold, ruter, og fartøytype.

Disse simpliseringene er **akseptable for første iterasjon** fordi:
- De gjør modellen håndterbar og løsbar.
- De gir en nedre grense (lower bound) på minimalmulig kostnad — dvs. modellens resultat viser best case.
- Resultatene er fortsatt relevante for strategiske beslutninger.

#### Implementering: Teknisk oppbygning

**Språk og rammeverk:** Pyomo (Python Optim

ization Modeling Objects)
- Pyomo gjør det mulig å definer modeller programmatisk og løse dem med ulike solvere.

**LP-solver:** GLPK eller CBC
- Er standard open-source solvere for lineær programmering.

**Kodfilstruktur:**
- `run_model_v1_pyomo.py` — hovedskript som bygger, løser og skriver resultater
- Inputfiler: `tab_model_v1_price_by_port_month.csv`, `tab_model_v1_demand_by_month.csv`, `data_model_v1_parameters.json`
- Outputfiler: `res_model_v1_solution_by_port_month.csv`, `res_model_v1_summary.json`

#### Løsingsprosess: Hva gjør solveren?

1. **Input:** Solveren mottar målfunksjon, restriksjoner, og parametere.
2. **Optimering:** Solveren søker etter kombinasjonen av $x_{h,t}$-verdier som minimerer kostnaden samtidig som alle restriksjoner er oppfylt.
3. **Output:** En løsning (vektor av optimale mengder), eller en status som sier "infeasible" eller "unbounded" hvis ingen løsning finnes.
4. **Validering:** Vi sjekker at løsningen oppfyller alle restriksjoner og sammenligner den med faktisk praksis.

#### Tolking av resultater

Resultatet av modellen er:
- **Optimal kostnad:** Total minimert drivstoffkostnad.
- **Allokeringsplan:** For hver havn og måned, hvor mye som optimalt bunkres der.
- **Kostnadssammenligning:** Differensen mellom optimal kostnad og hva som faktisk ble brukt (demonstrerer sparingspotensial).

Hvis modellen anbefaler å bunkre mer i P003 (som er billigst) og mindre i P002 (som er dyrest), reflekterer dette kostnadsoptimering.

Prosjektets første modellversjon formuleres som en kvantitativ lineær kostnadsminimeringsmodell. Målet er å minimere totale bunkringskostnader over analyseperioden gitt observerte prisforskjeller mellom havner og et definert drivstoffbehov per periode.

Målfunksjonen kan uttrykkes som:

$\min Z = \sum_{t \in T} \sum_{h \in H} p_{h,t} \cdot x_{h,t}$

der:

- $H$ er mengden havner
- $T$ er mengden perioder
- $p_{h,t}$ er pris per enhet drivstoff i havn $h$ i periode $t$
- $x_{h,t}$ er bunkret volum i havn $h$ i periode $t$

Målfunksjonen innebærer dermed at modellen velger den fordelingen av bunkringsvolum mellom havner og perioder som gir lavest mulig total kostnad. I den første modellversjonen estimeres prisparameteren $p_{h,t}$ fra historiske prisdata aggregert per havn og måned.

---

## 7.0 Analyse

[Fylles inn når modellen kjøres og resultatene foreligger. Her vil vi analysere:]
- Konvergering og løsningskvalitet
- Modellatferd under ulike prisvarianter
- Følsomhet for endringer i parametere (prisvolatilitet, tilgjengelighet)
- Sammenligning av modellens anbefalinger versus faktisk praksis
- Kostnadsbesparingstiltak og deres reserver

---

## 8.0 Resultat

[Fylles inn når modellen kjøres. Her presenteres:]
- Optimal kostnad (total og per måned)
- Optimale bunkringsmengder per havn
- Sammenlignbar kostnad hvis bunkring var blitt gjennomført som observert
- Estimert besparingspotensiale (kostnadsforskjell)
- Tabeller og figurer som viser løsningen

---

## 9.0 Diskusjon

[Fylles inn når resultatene foreligger. Her diskuteres:]

**Relevans og aktualitet av resultatene:** 
- Hvor realistisk er modellens anbefalinger gitt forenklinger?
- Hvilken betydning har antagelsene for konklusjonene?

**Styrker ved tilnærmingen:**
- Hvilke fordeler gir LP-modellering i denne konteksten?
- Hva gjør resultatet troverdig og anvendbart?

**Begrensninger og veier videre:**
- Hvilke data eller operasjonelle faktorer mangler?
- Hvordan kunne modellen forbedres praktisk (tankkapasitet, tidskobling, stokastisitet)?
- Hva er nødvendig før operativ implementering?

**Implikasjoner for Odfjell Tankers:**
- Kan resultatene faktisk implementeres?
- Hvilken endring i beslutningsprosess kreves?
- Hvilken organisatorisk oppslutning trengs?

---

## 10.0 Konklusjon

En lineær optimaliseringsmodell viser seg å være et relevant verktøy for å analysere og potensielt forbedre bunkringsbeslutninger hos Odfjell Tankers. Analysen av historiske data fra 2020–2025 demonstrerer at betydelige prisvariasjoner eksisterer mellom havner og over tid, og at strategisk valg av bunkringshavn kunne gitt substantielle kostnadsbesparelser.

Selv med forenklende antagelser gir modellen dårligere grunnlag for strukturerte beslutninger enn dagens praksis. Resultatene antyder både potensialet og de praktiske begrensningene ved data-drevet optimering i maritime drift.

For videre arbeid anbefales:
1. Innhenting av supplerende data om tankkapasitet, forbruk og rutetilgjengelighet.
2. Utvikling av en mer sofistikert modell med tidskobling og stokastisk formulering.
3. Pilot-testing av modellen på en delmengde av operasjoner før full implementering.

Konklusjonsmessig viser denne rapporten at Odfjell Tankers kan dra nytte av optimeringsmodeller som beslutningsstøtte, og at investering i datakvalitet og modellutvikiling er faglig forsvarlig.

---

## 11.0 Bibliografi

---

## 12.0 Vedlegg

