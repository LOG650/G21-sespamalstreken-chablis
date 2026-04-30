# G21 - Sespamalstreken Chablis

**Tittel: Optimalisering av bunkringsbeslutninger i Odfjell Tankers basert på historiske data**

**Forfattere : Elisabeth Kirkeland Orlien og Kaylee Floden**

**Totalt antall sider inkludert forsiden:**

**Molde, Innleveringsdato: 31.05.2026**

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

Forfatter(ne) har opphavsrett til oppgaven. Det betyr blant annet enerett til å gjøre verket tilgjengelig for allmennheten (åndsverkloven § 2).

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

Denne rapporten undersøker hvordan en lineær optimaliseringsmodell kan brukes som beslutningsstøtte for å minimere drivstoffkostnader hos Odfjell Tankers. Analysen bygger på historiske bunkringsdata for LSF i fire prisede modellhavner, kombinert med operative voyage-, forbruks- og beholdningsdata. Datagrunnlaget brukes først til å beskrive historisk pris- og volumutvikling, og deretter til å formulere en kostnadsminimerende bunkringsmodell med restriksjoner for rutesekvens, tankkapasitet og ikke-negativ beholdning.

Hovedmodellen behandler 486 voyage-etapper for åtte anonymiserte fartøyfiler. I basisscenarioet kjøper modellen 18 857,45 enheter i prisede modellhavner og fører 21 260,62 enheter som ekstern/ukjent bunkring. Ekstern/ukjent bunkring betyr her drivstoffbehov som ikke kan dekkes gjennom de prisede modellhavnene i rapportens datagrunnlag, og som derfor kostnadssettes med en proxypris. Dette tilsvarer at 41,59 % av modellert forbruk dekkes gjennom prisede modellhavner, mens 46,89 % faller utenfor dagens prisgrunnlag. Total modellkostnad i basisscenarioet er 26 625 664,78. Sensitivitetsanalysen viser at total modellkostnad varierer med 5 190 071,68 når proxykostnaden for ekstern/ukjent bunkring endres fra faktor 1,10 til 1,50, men kjøpsplanen er stabil i de testede scenarioene.

Resultatene viser at modellen gir mest operativ verdi der fartøyenes ruter overlapper med de prisede modellhavnene. Samtidig viser den eksterne/ukjente andelen et tydelig datagap: modellen er egnet som transparent analyse- og beslutningsstøtte, men bredere prisdekning og videre validering er nødvendig før den kan brukes som full operativ planleggingsmodell.

---

## Abstract

This report examines how a linear optimization model can support fuel cost minimization for Odfjell Tankers. The analysis is based on historical LSF bunkering data from four priced model ports, combined with operational voyage, consumption and inventory data. The data are first used to describe historical price and volume patterns, and then to formulate a cost-minimizing bunkering model with constraints for route sequence, tank capacity and non-negative inventory.

The main model covers 486 voyage legs across eight anonymized vessel files. In the baseline scenario, the model purchases 18,857.45 units in priced model ports and assigns 21,260.62 units to external/unknown bunkering. External/unknown bunkering means fuel demand that cannot be covered through the priced model ports in the report's data basis and is therefore priced with a proxy cost. This means that 41.59% of modeled consumption is covered through priced model ports, while 46.89% falls outside the current price coverage. The total model cost in the baseline scenario is 26,625,664.78. The sensitivity analysis shows that total model cost varies by 5,190,071.68 when the proxy cost for external/unknown bunkering changes from factor 1.10 to 1.50, while the purchase plan remains stable in the tested scenarios.

The results show that the model is most operationally useful when vessel routes overlap with the priced model ports. At the same time, the external/unknown share provides a clear diagnosis of the data gap. The model is therefore suitable as transparent analytical decision support, but broader price coverage and further validation are needed before it can be used as a full operational planning model.

---

## Innholdsfortegnelse

- 1.0 Innledning
- 1.1 Problemstilling
- 1.2 Delproblemer
- 1.3 Avgrensinger
- 1.4 Antagelser
- 2.0 Litteratur
- 3.0 Teori
- 4.0 Casebeskrivelse
- 4.1 Odfjell Tankers og beslutningssituasjonen
- 4.2 Historisk utvikling i volum og pris
- 4.3 Sesongmønster i bunkringsdataene
- 4.4 Konsekvenser for planlegging og kostnadsstyring
- 5.0 Metode og data
- 5.1 Metode
- 5.2 Data
- 6.0 Modellering
- 6.1 Datagrunnlag og beslutningsnivå
- 6.2 Sett, parametere og beslutningsvariabler
- 6.3 Målfunksjon
- 6.4 Restriksjoner
- 6.5 Modellfiler og validering
- 6.6 Avgrensninger
- 7.0 Analyse
- 7.1 Dekning fra prisede modellhavner
- 7.2 Fartøyforskjeller
- 7.3 Kostnadsdriver og proxypris
- 8.0 Resultat
- 8.1 Hovedresultat
- 8.2 Resultat per fartøyfil
- 8.3 Anvendbarhet per fartøyfil
- 8.4 Resultat per modellhavn
- 8.5 Sensitivitet for ekstern proxypris
- 9.0 Diskusjon
- 9.1 Praktiske og faglige implikasjoner
- 9.2 Begrensninger og videre bruk
- 10.0 Konklusjon
- 11.0 Bibliografi
- 12.0 Vedlegg

---

## 1.0 Innledning 


Drivstoffkostnader er en av de største og mest variable kostnadskomponentene i maritim drift. Shippingnæringen er generelt preget av betydelig volatilitet, både i fraktrater og innsatsfaktorer som drivstoff, noe som gjør kostnadsstyring særlig krevende (Stopford, 2008). For et rederi som Odfjell Tankers, der bunkring skjer løpende for en stor global flåte, kan selv moderate prisforskjeller per enhet gi store utslag i totale kostnader over tid. Casebedriften oppgir at innkjøpene gjelder rundt 70 tankskip og om lag 400 000 metriske tonn marint drivstoff i 2025, med en samlet verdi på rundt 250 millioner USD. Dette gjør bunkringsbeslutninger til et beslutningsområde der bedre datastøtte kan ha betydelig økonomisk relevans.

Beslutningene tas samtidig i en operativ virkelighet preget av prisvariasjon mellom havner, ulike innkjøpsformer og behov for å balansere kostnad, tilgjengelighet, kvalitet og regulatoriske rammer (FuelEU Guidance Document for Shipping Companies, 2025). Dette gjør bunkringsbeslutninger til et relevant område for beslutningsstøtte basert på data og optimering. Temaet er aktuelt fordi historiske transaksjonsdata gir mulighet til å undersøke om det finnes systematiske mønstre i pris og volum som kan utnyttes bedre enn i en mer erfaringsbasert beslutningsprosess. Dersom slike mønstre kan dokumenteres og knyttes til en enkel og transparent modell, kan analysen gi Odfjell Tankers et bedre grunnlag for å vurdere hvor bunkring bør skje under gitte forutsetninger.

Rapporten er forankret i et konkret case der prosjektgruppen har fått tilgang til historiske bunkringstransaksjoner for drivstofftypen LSF i de fire mest brukte havnene i datasettet. Dette er den drivstoffkategorien rapporten faktisk analyserer, selv om den operative bunkringsvirkeligheten i selskapet er bredere. Prisgrunnlaget dekker 61 måneder fra januar 2020 til januar 2025. I tillegg brukes supplerende operative voyage-data fra 2025 for å modellere rutesekvens, forbruk, beholdning og tankkapasitet. Formålet er ikke å utvikle en fullstendig operativ planleggingsmodell, men å etablere et analysemessig beslutningsgrunnlag som kan vise hvordan historiske prisdata kan kobles med operative data i en kostnadsminimerende modell.

Tidligere forskning og praksis innen operasjonsanalyse viser at lineær programmering er godt egnet til å analysere ressursallokering og kostnadsminimering under restriksjoner. I en maritim sammenheng er dette relevant fordi bunkringsbeslutninger kan forstås som et valg mellom alternative havner, priser og tidspunkter. Denne rapporten knytter derfor historiske bunkringsdata til en lineær kostnadsminimeringsmodell og vurderer hvordan pris- og volumdatasettet kan brukes til dette formålet.

Rapporten er strukturert slik at case og historiske data presenteres før den matematiske modellen formuleres. Dette gjør det mulig å bygge en tydelig sammenheng mellom den faktiske beslutningssituasjonen, datagrunnlaget, modellforenklingene og den videre analysen.

### 1.1 Problemstilling

Hvordan kan en lineær optimaliseringsmodell bidra til å minimere drivstoffkostnader for Odfjell Tankers ved bruk av historiske prisdata og operative voyage-, forbruks- og beholdningsdata?

Gitt den høye volatiliteten i drivstoffkostnader i shippingmarkedet (Stopford, 2008), er det relevant å undersøke hvordan bunkringsbeslutninger kan struktureres og støttes gjennom en optimaliseringsmodell.

### 1.2 Delproblemer

Hovedproblemstillingen kan presiseres gjennom tre delspørsmål:

- Hvordan kan historiske bunkringsdata renses, struktureres og beskrives slik at de gir et konsistent grunnlag for modellering?
- Hvordan kan historiske prisdata kobles med voyage-data, forbruk, ROB og tankkapasitet i en operasjonell kostnadsmodell?
- Hvilke deler av rute- og forbruksbehovet kan modellen kostnadsminimere med dagens prisdekning, og hvor oppstår datagap?

### 1.3 Avgrensinger

Rapporten er avgrenset til de fire mest brukte havnene i pris- og volumdatasettet, `P001`, `P002`, `P003` og `P004`, fordi det er disse havnene som har den tydeligste historiske datadekningen. Videre er modellgrunnlaget avgrenset til drivstofftypen `LSF`, slik den er registrert i pris- og volumdatasettet, slik at modell og datagrunnlag bygger på én konsistent produktkategori. Tidsmessig er arbeidet avgrenset til perioden januar 2020 til januar 2025, som gir 61 måneder med historiske observasjoner.

Hovedmodellen er en operasjonell rute- og lagerbasert modell på fartøy- og etappenivå. Prisgrunnlaget er avgrenset til modellhavnene `P001`, `P002`, `P003` og `P004`, mens voyage-dataene dekker åtte anonymiserte fartøyfiler fra 2025. Havner utenfor modellhavnene får ikke egne estimerte priser, men behov som ikke kan dekkes gjennom prisede modellhavner kostnadssettes som ekstern/ukjent bunkring.

Selv om den operative bunkringsvirkeligheten omfatter flere drivstofftyper, kontraktsforhold, spotkjøp og regulatoriske hensyn, er analysen i denne rapporten avgrenset til det historiske datagrunnlaget som faktisk er tilgjengelig for prosjektgruppen. `LSGO` og biodrivstoff omtales derfor kun som bakgrunnsinformasjon om casebedriften og inngår ikke i modellgrunnlaget.

### 1.4 Antagelser

Rapporten bygger på flere eksplisitte antagelser. For det første antas det at historiske prisobservasjoner gir et rimelig grunnlag for å beskrive relative prisforskjeller mellom modellhavnene. For det andre antas det at pris- og volumdatasettet som er mottatt fra Odfjell Tankers allerede er grunnleggende kvalitetssjekket av dataleverandøren, selv om prosjektgruppen ikke har mottatt en separat datakvalitetsrapport for dette datasettet. For det tredje antas det at `ROB_Fuel_Total`, rapportert forbruk og oppgitt bunkerskapasitet kan brukes som operative modellparametere for de anonymiserte 2025-fartøyfilene.

Disse antagelsene er nødvendige for å kunne arbeide videre med pris- og volumdatasettet, men de innebærer også begrensninger. Historiske prisforskjeller mellom havnene kan ikke uten videre tolkes som sikre framtidige prisforskjeller. Manglende uavhengig datakvalitetsrapport gjør også at eventuelle feil, mangler eller registreringsforskjeller i datasettet kan bli videreført inn i analysen. I tillegg innebærer bruken av `ROB_Fuel_Total`, rapportert forbruk og bunkerskapasitet som modellparametere at modellen forenkler den operative virkeligheten. Analysen må derfor tolkes som et beslutningsstøttende modellforsøk og ikke som en full operativ anbefaling uten videre validering.

---

## 2.0 Litteratur

Litteraturgrunnlaget for denne rapporten ligger i skjæringspunktet mellom operasjonsanalyse, lineær programmering, bunkringsbeslutninger og maritim beslutningsstøtte. Kapittelet brukes til å plassere rapporten i forskningsfeltet, mens kapittel 3 avgrenser de teoretiske begrepene som brukes i modelleringen.

Innen operasjonsanalyse er lineær programmering et etablert rammeverk for å formulere problemer der en aktør ønsker å minimere kostnader eller maksimere nytte under et sett av begrensninger (Fox & Burks, 2024). Denne litteraturen er relevant fordi bunkringsproblemet kan forstås som et valgproblem: et gitt drivstoffbehov skal dekkes ved å fordele innkjøp mellom alternative havner og perioder med ulike priser.

Forskningslitteraturen om bunkring viser at problemet ofte behandles som en kombinasjon av rute-, beholdnings- og innkjøpsbeslutninger. Besbes og Savin (2009) formulerer bunkringsbeslutninger som et problem der refueling-kostnader må minimeres under tilfeldig prisutvikling og begrenset tankkapasitet. Zhen et al. (2017) studerer optimal skipsbunkring med stokastisk drivstofforbruk og stokastiske havnepriser, og viser hvordan beslutningen om hvor og hvor mye som skal bunkres kan behandles som en dynamisk beslutningsregel. Wang og Meng (2015) utvider dette perspektivet til robuste bunkringsbeslutninger i liner-nettverk, der både hastighet, bunkring og usikkert forbruk påvirker totalkostnaden.

Andre bidrag viser at bunkring sjelden kan isoleres fra øvrige operative beslutninger. Sheng et al. (2015) kobler refueling-policy og hastighetsvalg i linerfart, mens Du et al. (2015) bruker robust optimering for å håndtere usikkerhet i drivstofforbruk over en rundreise. Nyere arbeid på trampfart viser også at bunkringsbeslutninger kan integreres med rute- og planleggingsproblemer, slik at modellen må håndtere både hvor drivstoff kjøpes og hvordan ruten gjennomføres (Omholt-Jensen et al., 2025).

Denne litteraturen har to konsekvenser for rapporten. For det første støtter den at bunkringsbeslutninger kan analyseres som et optimeringsproblem med pris, kapasitet, rute og forbruk som sentrale parametere. For det andre viser den at mer avanserte modeller ofte inkluderer usikkerhet, hastighet, rutevalg, kontrakter og flere drivstofftyper. Rapportens modell er enklere: rutesekvensen tas som gitt, prisgrunnlaget er avgrenset til fire modellhavner, og ekstern/ukjent bunkring brukes for å synliggjøre datagap.

Det faglige hullet rapporten adresserer er derfor ikke mangel på optimeringsmodeller for bunkring generelt. Hullet ligger i den praktiske overgangen fra et begrenset historisk transaksjonsdatasett til en transparent og etterprøvbar beslutningsstøttemodell for et konkret redericase. Rapportens bidrag er å vise hvordan historiske prisdata, voyage-data, forbruk, beholdning og kapasitet kan kobles i en lineær rute- og lagerbasert modell, samtidig som modellen klassifiserer hvor resultatene er direkte anvendbare og hvor datadekningen fortsatt er for svak.

Litteratur om logistikk og maritim planlegging peker samtidig på at modeller bør vurderes i lys av operativ kontekst (Song & Panayides, 2021; Venkataraman & Pinto, 2018). I praksis vil forhold som tilgjengelighet, kapasitet, forbruk, ruter, kontrakter og regelverk påvirke hvilke løsninger som faktisk er gjennomførbare. Dette er relevant for denne rapporten fordi pris- og volumdatasettet ikke inneholder alle slike variabler. Dermed må modellens rolle avgrenses til å være et analytisk beslutningsstøtteverktøy, ikke en fullstendig operativ sannhetsmodell.

Denne rapporten plasserer seg dermed i en anvendt tradisjon, der etablerte prinsipper fra lineær programmering og modellbasert analyse benyttes for å støtte praktiske beslutninger i en operativ maritim kontekst. Metoden anvendes på et konkret case med et begrenset, men reelt datagrunnlag fra Odfjell Tankers. Dette er i tråd med hvordan analyseverktøy ofte brukes i praksis innen maritim økonomi og drift, hvor modellbaserte tilnærminger inngår som beslutningsstøtte heller enn som fullstendige operasjonelle løsninger (Grammenos, 2026).

---

## 3.0 Teori

### Lineær programmering som teoretisk rammeverk

Lineær programmering er en matematisk metode for å finne den beste løsningen på et problem der både målfunksjonen og restriksjonene kan uttrykkes lineært (Fox & Burks, 2024). Et standard lineært programmeringsproblem består av beslutningsvariabler, en målfunksjon og et sett av begrensninger. I denne oppgaven er teorien relevant fordi bunkringsbeslutninger kan forstås som et kostnadsminimeringsproblem, der drivstoff kjøpes i ulike havner til varierende priser under gitte kapasitets- og etterspørselsbetingelser.

Det teoretiske poenget med lineær programmering i denne sammenhengen er at metoden gjør det mulig å gå fra en intuitiv problemforståelse til en eksplisitt og etterprøvbar beslutningsmodell. Når modellens antagelser og restriksjoner er tydelige, kan både styrker og begrensninger diskuteres på en faglig ryddig måte. Dette gjør lineær programmering særlig egnet som grunnlag for beslutningsstøtte i situasjoner med flere alternative handlingsvalg og tydelige kostnadsforskjeller.

### Beslutningsvariabler, parametere og restriksjoner

Et sentralt teoretisk skille i optimeringslitteraturen går mellom beslutningsvariabler og parametere (Fox & Burks, 2024). Beslutningsvariablene beskriver hva modellen skal velge, mens parametrene beskriver størrelser som antas gitt. I denne rapporten brukes dette skillet for å definere bunkret volum som beslutningsvariabel, mens pris, behov og tilgjengelighet behandles som parametere i modellen.

Restriksjoner er like viktige som målfunksjonen, fordi de avgjør hvilke løsninger som er gyldige. Teoretisk sett er dette nødvendig for at en modell ikke bare skal finne den billigste løsningen, men den billigste løsningen innenfor de rammene som er definert. I praksis betyr det at modellens verdi avhenger av hvor godt restriksjonene representerer den faktiske beslutningssituasjonen.

### Modellforenkling og operativ relevans

All anvendt modellering innebærer forenklinger (Song & Panayides, 2021; Venkataraman & Pinto, 2018). En modell er derfor ikke en kopi av virkeligheten, men en analytisk representasjon av utvalgte forhold som anses viktigst for beslutningen. I denne oppgaven er dette særlig relevant fordi datagrunnlaget ikke inneholder alle operative variabler som i prinsippet burde inngå i en full bunkringsmodell. Dette er særlig relevant i maritime beslutningssituasjoner, hvor operasjonelle forhold ofte begrenser hvilke løsninger som faktisk er gjennomførbare (Song & Panayides, 2021; Venkataraman & Pinto, 2018).

Teoretisk innebærer dette at modellen må forstås som en deterministisk og operasjonell lager-/rutemodell. Den arbeider på fartøy- og etappenivå, men bruker historiske prisobservasjoner som grunnlag for kostnadsparameterne. Dette gjør modellen mer beslutningsnær enn en ren månedsaggregert modell, men stiller samtidig krav om at prisproxyer og manglende havnedekning dokumenteres tydelig.

### Datagrunnlag og modellkontroll

Når historiske data brukes til modellering, oppstår det en risiko for at modellen tolkes for sterkt dersom datagrunnlag, forutsetninger og kontroller ikke skilles tydelig. Et vanlig prinsipp i analyse og modellutvikling er derfor å dokumentere hvilke data som brukes til utvikling, hvilke data som holdes tilbake for senere kontroll, og hvilke kontroller som faktisk er gjennomført (Fox & Burks, 2024). I denne rapporten er dette prinsippet relevant fordi både prisdata og voyage-data er dokumentert med kronologisk train/test-splitt, samtidig som hovedmodellen kontrolleres gjennom interne konsistenssjekker og sensitivitetsanalyse.

Den teoretiske begrunnelsen for kronologisk splitt er at senere observasjoner ikke skal blandes inn i tidligere analysegrunnlag. I denne rapporten brukes splitten primært som datadokumentasjon og for å gjøre videre validering mulig. Selve vurderingen av hovedmodellen skjer gjennom kontroll av at rutesekvens, forbruk, beholdning, kapasitet og kjøpsmuligheter behandles konsistent i modellresultatene. Samlet sett gir dette et teoretisk grunnlag for å formulere bunkringsproblemet som et optimeringsproblem, der kostnadsminimering skjer under gitte operative og datamessige begrensninger. Dette danner utgangspunktet for modellformuleringen som presenteres i neste kapittel.

---

## 4.0 Casebeskrivelse

Dette prosjektet tar utgangspunkt i Odfjell Tankers sitt behov for bedre beslutningsstøtte i bunkringsarbeidet. Drivstoff er en stor kostnadspost i maritim drift, og prisforskjeller mellom havner og over tid kan få betydning når kjøpene gjentas mange ganger gjennom året. Casebeskrivelsen i dette kapittelet bygger derfor på historiske bunkringstransaksjoner og brukes til å forklare hvorfor datasettet er relevant som grunnlag for videre modellering.

### 4.1 Odfjell Tankers og beslutningssituasjonen

Odfjell Tankers opererer i en maritim kontekst der bunkringsbeslutninger må tas med begrenset og spredt informasjon om priser, tilgjengelighet og framtidig behov. I denne oppgaven er målet ikke å beskrive alle operative detaljer i selskapets drift, men å undersøke om historiske pris- og volumdata kan brukes til å etablere et første datadrevet beslutningsgrunnlag for hvor bunkring bør skje.

Den operative beslutningssituasjonen er bredere enn det datasettet i denne rapporten direkte dekker. Ifølge kontaktpersonen med ansvar for innkjøp av marint drivstoff kjøper Odfjell Tankers drivstoff til rundt 70 tankskip som opererer globalt. I 2025 utgjorde dette om lag 400 000 metriske tonn, med en samlet verdi på rundt 250 millioner USD. Dette illustrerer at selv små forbedringer i innkjøpsbeslutningene kan få betydelige økonomiske konsekvenser over tid.

I den daglige driften brukes flere drivstofftyper. Hovedtyngden består av `VLSFO` (`Very Low Sulphur Fuel Oil`), mens flåten også bruker `LSGO` (`Low Sulphur Gasoil`) og noe biodrivstoff (*Everything You Need to Know About Marine Fuels*, u.å.). I denne rapporten fungerer `LSGO` og biodrivstoff likevel bare som bakgrunnsinformasjon. Det mottatte analysegrunnlaget dekker kun transaksjoner for drivstofftypen `LSF`, og det er denne kategorien som ligger til grunn for videre analyse og modellering. I rapporten behandles derfor `LSF` som datasettets registrerte produktkategori, mens `VLSFO` omtales som den bredere operative drivstoffkategorien i casebeskrivelsen.

Bruken av biodrivstoff er heller ikke bare et kommersielt valg, men må sees i lys av regulatoriske krav knyttet til utslipp og etterlevelse av europeisk regelverk (*FuelEU Guidance Document for Shipping Companies*, 2025). Drivstoffvalget påvirkes dermed i praksis både av pris, tilgjengelighet, kvalitet og regulatoriske rammer. Den faktiske beslutningssituasjonen er derfor mer sammensatt enn den avgrensede analysen i denne rapporten.

Innkjøpene skjer også under ulike markedsbetingelser. I noen havner har selskapet kontrakt med en leverandør for å sikre tilgjengelighet og/eller kvalitet, mens drivstoff i andre havner kjøpes i spotmarkedet. Dette betyr at bunkringsbeslutninger i praksis ikke bare handler om å velge lavest mulig pris, men også om å håndtere leveringssikkerhet, kvalitet og markedsforhold.

Odfjell Tankers bruker dessuten `imarex` som beslutningsstøtte i det operative arbeidet. Systemet brukes til å predikere framtidige priser i ulike havner og støtter særlig vurderinger av når innkjøp bør gjennomføres. Samtidig er denne støtten avgrenset til ordinært fossilt drivstoff, det vil si `VLSFO` og `LSGO`, og omfatter ikke biodrivstoff. Dette understreker at dagens beslutningsstøtte er nyttig, men ikke nødvendigvis dekkende for hele bredden i bunkringsarbeidet.

Det opprinnelige analysegrunnlaget dekker drivstofftypen `LSF` og de fire mest brukte havnene i datasettet: `P001`, `P002`, `P003` og `P004`. Dette er en relevant avgrensing fordi disse havnene representerer de observerte beslutningsalternativene som er best dokumentert i pris- og volumdatasettet. Prosjektgruppen har i tillegg mottatt og strukturert supplerende 2025-data med anonymiserte fartøyklasser, forbruk, voyage-koder, `ROB_Fuel_Total`, tankkapasitet og kontraktskontekst. Disse dataene brukes direkte i den operative hovedmodellen, men de erstatter ikke pris- og volumdatasettet som kilde til dokumenterte prisparametere.

### 4.2 Historisk utvikling i volum og pris

Et sentralt spørsmål i casebeskrivelsen er om datasettet faktisk viser variasjon som kan begrunne videre analyse og modellering. Hvis volum og pris er helt stabile, vil verdien av et beslutningsstøtteverktøy være mer begrenset. Hvis det derimot finnes tydelige svingninger, styrker det begrunnelsen for å bruke modellering.

Figur 4.1 viser samlet bunkret volum måned for måned gjennom hele analyseperioden fra januar 2020 til januar 2025. Hvert punkt på kurven representerer altså én faktisk måned i tidsserien, ikke et gjennomsnitt på tvers av flere år. Volumet varierer betydelig mellom månedene, med en topp i januar 2023 på 22 316,23 og et bunnpunkt i februar 2020 på 4 726,55. Dette tyder på at aktivitetsnivået ikke er konstant, og at modellen må bygge på et datagrunnlag som håndterer variasjon over tid.

<div align="center">
  <img src="../006%20analysis/01_datagrunnlag/04_deskriptiv_analyse/figures/fig_bunker_total_qty_by_month.png" alt="Historisk bunkret volum per måned" width="80%">
  <p align="center" style="font-size: 0.9em;"><small><i>Figur 4.1 Samlet bunkret volum for hver enkelt måned i perioden 2020-01 til 2025-01.</i></small></p>
</div>

Prisnivået varierer også tydelig mellom havnene. Figur 4.2 viser vektet gjennomsnittspris per havn for hver enkelt måned i perioden. Også her er figuren en tidsserie, der hver observasjon er knyttet til en konkret måned mellom januar 2020 og januar 2025. Figuren viser at havnene ikke bare har ulike gjennomsnittspriser, men også ulike prisbaner over tid. Dette er et sentralt premiss for videre modellering, fordi det innebærer at havnevalg kan påvirke totale bunkringskostnader.

<div align="center">
  <img src="../006%20analysis/01_datagrunnlag/04_deskriptiv_analyse/figures/fig_bunker_weighted_price_by_port_month.png" alt="Pris per havn og måned" width="80%">
  <p align="center" style="font-size: 0.9em;"><small><i>Figur 4.2 Vektet gjennomsnittspris per havn for hver enkelt måned i perioden 2020-01 til 2025-01.</i></small></p>
</div>

Tabell 4.1 oppsummerer forskjellene mellom havnene og dokumenterer både aktivitetsnivå og prisnivå i analyseperioden.

| Havn | Antall observasjoner | Total mengde | Vektet gjennomsnittspris | Antall måneder med observasjon |
| --- | --- | --- | --- | --- |
| P001 | 209 | 113606.88 | 578.75 | 61 |
| P002 | 286 | 181419.36 | 610.29 | 46 |
| P003 | 369 | 253591.20 | 540.84 | 61 |
| P004 | 517 | 320932.69 | 577.04 | 61 |

<p align="center" style="font-size: 0.9em;"><small><i>Tabell 4.1 Oversikt over aktivitetsnivå og prisnivå for de fire mest brukte havnene i analyseperioden.</i></small></p>

Tabell 4.1 viser at `P004` er den mest brukte havnen målt i antall observasjoner, mens `P003` har lavest vektet gjennomsnittspris. `P002` fremstår som den dyreste havnen i utvalget og har dessuten færre måneder med observasjoner enn de øvrige havnene. Dette understøtter at både prisnivå og datadekning varierer mellom havnene.

### 4.3 Sesongmønster i bunkringsdataene

For å vurdere om det finnes et mønster som gjentar seg gjennom kalenderåret, er volum og pris også aggregert per kalendermåned. Figur 4.3 er derfor ikke en tidsserie for ett bestemt år. I stedet viser den et gjennomsnitt på tvers av analyseperioden, der alle januar-måneder er slått sammen, alle februar-måneder er slått sammen, og så videre. Stolpene representerer gjennomsnittlig volum per kalendermåned, mens linjen viser vektet gjennomsnittspris for samme kalendermåned når hele perioden ses under ett.

<div align="center">
  <img src="../006%20analysis/01_datagrunnlag/04_deskriptiv_analyse/figures/fig_bunker_season_profile.png" alt="Sesongprofil for volum og pris" width="80%">
  <p align="center" style="font-size: 0.9em;"><small><i>Figur 4.3 Gjennomsnittlig volum og pris per kalendermåned, aggregert på tvers av perioden 2020-01 til 2025-01.</i></small></p>
</div>

Figuren viser at aktivitetsnivået i gjennomsnitt er høyest rundt mars og juli, mens prisnivået i gjennomsnitt er relativt høyt i februar, mars og juni og lavere i mai og desember. Mønsteret er ikke så sterkt at det alene kan forklare alle beslutninger, men det viser at både volum og pris varierer systematisk nok til at sesong bør beskrives eksplisitt i caset.

### 4.4 Konsekvenser for planlegging og kostnadsstyring

Når prisene varierer mellom havner og over tid, mens volumet samtidig svinger gjennom analyseperioden, øker behovet for et mer strukturert beslutningsgrunnlag. Uten en systematisk sammenstilling av slike mønstre risikerer virksomheten å basere bunkringsbeslutninger på enkelthendelser eller lokal erfaring alene. Det betyr ikke at historiske data kan erstatte operativ vurdering, men det betyr at historiske transaksjoner kan brukes til å synliggjøre hvor det finnes et potensial for kostnadsreduksjon og bedre prioritering mellom havner.

Selv om selskapet allerede bruker beslutningsstøtte for deler av bunkringsarbeidet, er beslutningssituasjonen fortsatt kompleks fordi ulike drivstofftyper, kontraktsforhold, spotkjøp og regulatoriske krav gjør at ikke alle valg kan støttes på samme måte. Den underliggende utfordringen i bedriften er derfor bredere enn bare historiske prisforskjeller. Når beslutningsgrunnlaget ikke kobler pris, rute, forbruk, beholdning og kapasitet systematisk, blir beslutninger lettere preget av kortsiktige vurderinger og mindre av etterprøvbar analyse. Dette kan føre til at bunkring skjer i havner som i ettertid viser seg å være relativt dyre, eller at volum fordeles på en måte som ikke utnytter prisvariasjonene godt nok.

For bedriften kan et begrenset beslutningsgrunnlag skape flere praktiske problemer. For det første øker risikoen for høyere drivstoffkostnader fordi valg av havn og tidspunkt i større grad blir reaktive enn planlagte. For det andre blir det vanskeligere å vurdere hvilke kostnadsforskjeller som faktisk skyldes markedet, og hvilke som skyldes beslutningsmønsteret i virksomheten. For det tredje svekkes grunnlaget for læring over tid, fordi historiske beslutninger ikke blir vurdert systematisk opp mot alternative løsninger.

I en virksomhet som Odfjell Tankers får dette betydning utover enkeltkjøp. Når bunkerrelaterte valg gjentas mange ganger gjennom året, kan selv små avvik mellom faktisk praksis og en mer kostnadseffektiv løsning gi betydelige samlede utslag. En analysemodell som synliggjør historiske mønstre, estimerer kostnadskonsekvenser og peker på mulige forbedringer, er derfor relevant ikke bare som et teknisk verktøy, men som støtte for bedre planlegging og mer konsistente beslutninger i bedriften.

---

## 5.0 Metode og data

### 5.1 Metode

Studien er gjennomført som en kvantitativ caseanalyse av Odfjell Tankers, der historiske bunkringstransaksjoner og operative voyage-data brukes som grunnlag for å utvikle en optimeringsmodell for beslutningsstøtte. Arbeidet er lagt opp i seks steg: innlesing og kvalitetssikring av rådata, rensing og strukturering av pris- og volumdatasettet, deskriptiv analyse av historiske mønstre, strukturering av operative voyage-, forbruks-, ROB- og kapasitetsdata, formulering og implementering av en lineær rute- og lagerbasert hovedmodell, og til slutt basiskjøring, sensitivitetsanalyse og resultattolkning.

Metodisk kombinerer rapporten datavask og strukturering, deskriptiv grafisk analyse, lineær programmering, intern konsistenskontroll, sensitivitetsanalyse og anvendbarhetsklassifisering. Tabell 5.1 viser hvordan disse metodene brukes i de ulike delene av arbeidet.

| Del av arbeidet | Metode brukt | Formål |
| --- | --- | --- |
| Datagrunnlag | Innlesing, rensing og strukturering av historiske bunkringsdata og operative voyage-data | Etablere konsistente inputdata for analyse og modellering |
| Beskrivende analyse | Tidsseriefigurer, sesongprofil og aggregerte tabeller | Dokumentere historisk utvikling, variasjon og mønstre i volum og pris |
| Modellering | Lineær kostnadsminimeringsmodell med rute-, beholdnings- og kapasitetsrestriksjoner | Oversette bunkringsbeslutningen til et matematisk optimeringsproblem |
| Løsning | Numerisk lineær programmering med `scipy.optimize.linprog` | Beregne kostnadsminimerende bunkringsmengder gitt modellens restriksjoner |
| Kontroll | Datakvalitetskontroll, interne konsistenssjekker og sensitivitetsanalyse | Vurdere om datagrunnlag, modellresultater og sentrale antagelser er rimelige |
| Anvendelse | Anvendbarhetsklassifisering per fartøyfil | Vise hvor modellen kan gi direkte beslutningsstøtte, og hvor mer data trengs |

<p align="center" style="font-size: 0.9em;"><small><i>Tabell 5.1 Oversikt over metoder brukt i analyse- og modellarbeidet.</i></small></p>

Metoder som maskinlæring, tidsserieprognoser, EOQ-modeller, køteori, simulering og multikriteriemetoder er ikke brukt i denne rapporten. Årsaken er at problemstillingen er formulert som et deterministisk kostnadsminimeringsproblem med gitt rutesekvens, ikke som et prognoseproblem, et rutevalgsproblem, en klassisk lagerpolitikk eller en flermålsbeslutning. Valget av lineær programmering gir derfor en mer direkte kobling mellom problemstillingen, tilgjengelige data og modellens beslutningsvariabler.

Rådataene er behandlet i en reproduserbar renseprosess. Her standardiseres datoer og numeriske felt, samtidig som volum- og prisvariabler harmoniseres ved å bruke `Invoiced Qty` og `Invoice Price` som hovedkilder, med fallback til `Ordered Qty` og `Order Price` når fakturerte verdier mangler. Observasjoner med ikke-positivt volum eller ikke-positiv pris forkastes for å unngå at ugyldige transaksjoner påvirker analysen og de estimerte modellparametrene.

Etter rensing ble dataene strukturert i to nivåer. Først ble et renset transaksjonsdatasett etablert. Deretter ble transaksjonene aggregert per havn og måned for å skape et enklere og mer robust analysegrunnlag for modellen. Dette aggregatet gir blant annet total mengde, antall transaksjoner, vektet gjennomsnittspris, minimums- og maksimumspris, samt antall unike fartøy og leverandører per kombinasjon av havn og måned. Metodevalget innebærer en bevisst forenkling av den operative virkeligheten, men gir et transparent og reproduserbart grunnlag for kostnadsminimeringsmodellen.

Prosjektgruppen har i tillegg mottatt supplerende operative 2025-data for åtte anonymiserte fartøyfiler fordelt på klassene `C001` til `C005`. Råfilene inneholder blant annet dato, rapporttype, seilt distanse, tidsbruk, voyage fra/til, voyage-nummer, forbruksfelt og `ROB_Fuel_Total`. Voyage-havnene var opprinnelig oppgitt som UN/Locode, men er pseudonymisert i analysearbeidet slik at havner vises som `Pxxx` og voyage-numre som `VGxxx`. Det er også oppgitt tankkapasitet per fartøyklasse og informasjon om at selskapet har bunkerskontrakt i Singapore og Sør-Korea, samt VLSFO-kontrakt i Rotterdam. Tilleggsdataene brukes direkte i den operative hovedmodellen til å modellere forbruk, ROB, tankkapasitet og havnetilgjengelighet, mens pris- og volumdatasettet fortsatt er kilden til dokumenterte prisparametere.

Validitet, reliabilitet og etikk er vurdert som del av metodeopplegget. Intern validitet styrkes ved at modellen bygger direkte på observerte voyage-data, dokumenterte rensevalg og eksplisitte konsistenssjekker, men ekstern validitet er begrenset fordi modellen bare dekker én drivstoffkategori, fire prisede modellhavner og åtte anonymiserte fartøyfiler. Reliabiliteten styrkes gjennom reproduserbare skript, faste inputregler og sensitivitetsanalyse av proxykostnaden, men resultatene vil fortsatt være følsomme for endringer i prisdekning, rutegrunnlag og antagelser om ekstern/ukjent bunkring. Etisk er databehandlingen avgrenset til operasjonelle bedriftsdata uten personanalyse. Havner, fartøy og voyage-numre er pseudonymisert for å redusere risikoen for å eksponere kommersielt eller operasjonelt sensitiv informasjon. Siden prosjektet ikke behandler personopplysninger som forskningsdata, vurderes personvernet som lite berørt, men konfidensialitet rundt bedriftsdata er likevel et viktig hensyn.

### 5.2 Data

Datagrunnlaget består av historiske bunkringstransaksjoner fra råfilen mottatt fra Odfjell Tankers. Datasettet dekker de siste 61 månedene i perioden fra januar 2020 til januar 2025 og er avgrenset til de fire mest brukte havnene i materialet: `P001`, `P002`, `P003` og `P004`. Hver observasjon representerer en bunkringshendelse og inneholder blant annet informasjon om fartøy, voyage, havn, leveringsdato, bestilt mengde, fakturert mengde, ordrepris, fakturapris, leverandør og supplier.

Selve analysegrunnlaget omfatter kun transaksjoner for drivstofftypen `LSF`, slik denne er registrert i rådataene. Andre drivstofftyper som `LSGO` og biodrivstoff er relevante for å forstå den bredere operative beslutningssituasjonen i Odfjell Tankers, men de inngår ikke i datasettet som brukes i denne oppgaven og påvirker derfor heller ikke modellgrunnlaget direkte.

Tabell 5.2 oppsummerer pris- og volumdatasettet som brukes som modellens primære datagrunnlag.

| Element | Verdi |
| --- | --- |
| Periode | 2020-01-04 til 2025-01-30 |
| Antall rå observasjoner | 1389 |
| Antall rensede observasjoner | 1381 |
| Antall forkastede observasjoner | 8 |
| Drivstofftype | LSF |
| Antall havner | 4 |
| Havner inkludert | P001, P002, P003, P004 |
| Antall måneder | 61 |

<p align="center" style="font-size: 0.9em;"><small><i>Tabell 5.2 Oppsummering av pris- og volumdatasettet som brukes som modellgrunnlag.</i></small></p>

Det opprinnelige datasettet inneholder 1389 observasjoner. Gjennomgangen viser at de sentrale identifikasjonsfeltene er komplette, men at enkelte verdi- og prisfelt har mangler eller ugyldige verdier. Det finnes 10 observasjoner uten `Invoice Price`, 10 observasjoner uten `Invoiced Qty`, 2 observasjoner uten `Supplier`, samt 8 observasjoner med ikke-positivt volum. Etter rensing ble 1381 observasjoner beholdt, mens 8 observasjoner ble forkastet på grunn av ikke-positivt volum. Rensingen er en del av prosjektgruppens metodearbeid og endrer ikke hvilken fil som er rapportens opprinnelige datakilde.

Tabell 5.3 dokumenterer rensevalg og datakvalitet i materialet.

| Kontrollpunkt | Antall / regel | Konsekvens |
| --- | --- | --- |
| Manglende `Invoice Price` | 10 observasjoner | Håndteres med fallback til `Order Price` |
| Manglende `Invoiced Qty` | 10 observasjoner | Håndteres med fallback til `Ordered Qty` |
| Fallback-regel for pris | `Invoice Price` først | Bevarer observasjoner med manglende fakturapris |
| Fallback-regel for volum | `Invoiced Qty` først | Bevarer observasjoner med manglende fakturert volum |
| Forkastet pga. ikke-positivt volum | 8 observasjoner | Tas ut av analysegrunnlaget |
| Forkastet pga. ikke-positiv pris | 0 observasjoner | Ingen observasjoner fjernet av denne grunnen |
| Manglende `Supplier` | 2 observasjoner | Har liten betydning for modellen |
| Endelig antall beholdte observasjoner | 1381 | Brukes videre i renset og aggregert datasett |

<p align="center" style="font-size: 0.9em;"><small><i>Tabell 5.3 Oversikt over rensevalg, fallback-regler og vurdert datakvalitet i materialet.</i></small></p>

For analyse- og modelleringsformål er rådataene strukturert på to nivåer: rensede transaksjoner på detaljnivå og et månedlig aggregat per havn. Aggregatet består av 229 havn-måned-kombinasjoner fordelt over 61 måneder. For hver kombinasjon beregnes blant annet antall transaksjoner, total mengde, vektet gjennomsnittspris, enkel gjennomsnittspris, minimums- og maksimumspris, samt antall unike fartøy og leverandører. Dette er beregninger gjort fra rådataene, ikke egne eksterne datakilder.

For å skille mellom data brukt til utvikling og data brukt til senere vurdering, er rådatasettet også splittet i en treningsdel og en testdel. Splittingen er gjort kronologisk etter `Delivery Date`, slik at de tidligste 80 % av observasjonene brukes til trening og de siste 20 % brukes til testing. Splitten er gjort på rådatasettet før videre rensing, og gir en treningsdel med 1111 observasjoner og en testdel med 278 observasjoner. Modellarbeidet bygger på rådataene etter de beskrevne rense- og aggregeringsreglene, mens splitten dokumenterer et kronologisk skille mellom utviklingsgrunnlag og senere kontrollgrunnlag.

Train/test-splitten brukes ikke som klassisk evaluering av en prediktiv modell, fordi hovedmodellen ikke trenes statistisk. Den er en deterministisk optimeringsmodell som beregner kostnadsminimerende beslutninger gitt rute, forbruk, beholdning, kapasitet og prisparametere. Splitten brukes derfor først og fremst til datadisiplin: utviklingsvalg kan gjøres uten å blande inn de siste observasjonene, og testdelen kan senere brukes til robusthetskontroll av prisnivåer, datadekning og modelloppførsel.

De supplerende voyage-råfilene fra 2025 er også splittet kronologisk 80/20 før videre rensing. For disse filene er splitten gjort separat per råfil etter kombinert `Date_UTC` og `Time_UTC`, med originalfilene beholdt urørt.

En oppsummering av materialet viser tydelige forskjeller mellom havnene. `P004` er den mest brukte havnen målt i antall observasjoner, mens `P003` har lavest vektet gjennomsnittspris i utvalget. `P002` fremstår som den dyreste havnen. Dette indikerer at havnevalg har potensial til å påvirke totale drivstoffkostnader og støtter relevansen av å utvikle en optimeringsmodell basert på datasettet.

Tabell 5.4 oppsummerer den strukturerte havneinformasjonen som videreføres til modellgrunnlaget.

| Havn | Antall observasjoner | Total mengde | Vektet gjennomsnittspris | Antall måneder med observasjon |
| --- | --- | --- | --- | --- |
| P001 | 209 | 113606.88 | 578.75 | 61 |
| P002 | 286 | 181419.36 | 610.29 | 46 |
| P003 | 369 | 253591.20 | 540.84 | 61 |
| P004 | 517 | 320932.69 | 577.04 | 61 |

<p align="center" style="font-size: 0.9em;"><small><i>Tabell 5.4 Strukturert havneoversikt brukt videre i modellgrunnlaget.</i></small></p>

Etter den første datavasken er det mottatt et supplerende datasett med åtte anonymiserte fartøyfiler fra 2025. Filene ligger i `004 data` og er navngitt etter fartøyklasse og løpenummer, for eksempel `C001 - 1.csv`. Det samlede tilleggsdatasettet har 3893 rapporteringsrader fra 2025-01-01 til 2025-12-30. De opprinnelige havnekodene er erstattet med 70 interne P-koder, og voyage-numrene er erstattet med 244 interne VG-koder. Siden filene inneholder forbruk, seilt distanse, rapporterte voyage-koder og `ROB_Fuel_Total`, brukes de direkte til å etablere rutesekvens, forbruksbehov, startbeholdning og havnetilgjengelighet i hovedmodellen.

Tabell 5.5 oppsummerer de oppgitte tankkapasitetene for de anonymiserte fartøyklassene. Tallene er oppgitt som verifiserte 2025-tall fra dataleverandøren og brukes som kapasitetsrestriksjoner i hovedmodellen.

| Fartøyklasse | Bunkerskapasitet |
| --- | --- |
| C001 | 2,087.006 m3 |
| C002 | 2,061.430 m3 |
| C003 | 1,533.719 m3 |
| C004 | 1,907.080 m3 |
| C005 | 1,024.531 m3 |

<p align="center" style="font-size: 0.9em;"><small><i>Tabell 5.5 Verifisert bunkerskapasitet per anonymisert fartøyklasse brukt som kapasitetsparameter i hovedmodellen.</i></small></p>

Tabell 5.6 oppsummerer de supplerende voyage-dataene. Tabellen dokumenterer omfang, kvalitet og hvordan dataene brukes i den operative hovedmodellen. Voyage-dataene gir ikke prisparametere, men de inngår direkte i modellens rutesekvens, forbruksbehov, startbeholdning, havnetilgjengelighet og kapasitetsrestriksjoner.

| Element | Verdi | Bruk i rapporten |
| --- | --- | --- |
| Periode | 2025-01-01 til 2025-12-30 | Operasjonell støtte |
| Antall rapporteringsrader | 3893 | Omfang av voyage-data |
| Antall voyage-etapper | 486 | Grunnlag for rute- og forbruksvurdering |
| Antall fartøyklasser | 5 | Kapasitetsrestriksjoner |
| Antall interne havnekoder | 70 | Havnetilgjengelighet og rutespredning |
| Antall interne voyage-koder | 244 | Voyage-struktur |
| Train-rader | 3110 | Dokumentert kronologisk utviklingsgrunnlag |
| Test-rader | 783 | Dokumentert kronologisk kontrollgrunnlag |
| Datakvalitetsavvik | 43 | Kvalitetsvurdering |
| Manglende ROB | 3 | Begrensning |
| Nullforbruk | 40 | Begrensning |
| Modellrolle | Direkte operasjonell modellinput | Rute, forbruk, ROB, kapasitet og havnetilgjengelighet |

<p align="center" style="font-size: 0.9em;"><small><i>Tabell 5.6 Oppsummering av supplerende voyage-data brukt i operasjonell hovedmodell.</i></small></p>

Datakvaliteten i det opprinnelige pris- og volumdatasettet vurderes som tilstrekkelig for modellen, men datasettet har klare begrensninger. Det omfatter bare fire havner og én drivstofftype, og inneholder ikke eksplisitte variabler for minimumsbeholdning, faktisk drivstofforbruk mellom havner, havnesekvens eller kontraktsmessige bindinger. Tilleggsdataene reduserer noen av disse manglene, særlig for tankkapasitet, forbruk og voyage-sekvens.

Tilleggsdataene er strukturert til rapporteringshendelser, aggregerte voyage-etapper og kapasitetsparametere per anonymisert fartøyklasse. Struktureringen ga 3893 rapporteringsrader og 486 voyage-etapper. En egen datakvalitetskontroll av voyage-dataene identifiserer 43 avvik: 3 tilfeller med manglende ROB og 40 rapporteringsrader med nullforbruk. Det er ikke identifisert negativt forbruk, negativ varighet eller ROB over oppgitt tankkapasitet. Dette gjør det mulig å etablere en operasjonell hovedmodell som bruker voyage-dataene direkte til beholdning, forbruk, kapasitet og rutesekvens, samtidig som manglende prisdekning synliggjøres eksplisitt i resultatene.

Train/test-splitt av de åtte supplerende voyage-råfilene ga samlet 3110 train-rader og 783 test-rader. I denne rapporten brukes splitten som dokumentasjon av et kronologisk skille og som grunnlag for eventuell senere kontroll. Den operative hovedmodellen kjøres som en deterministisk kostnadsminimering på det strukturerte 2025-grunnlaget, og vurderes primært gjennom interne konsistenssjekker, basiskjøring og sensitivitetsanalyse. Dersom modellen senere skal videreutvikles, kan train- og testdelene brukes til å undersøke om kjøpsmønster, ekstern/ukjent andel og kostnadsnivå er stabile mellom tidligere og senere deler av datagrunnlaget.

Det finnes samtidig ingen separat datakvalitetsrapport eller annen direkte dokumentasjon fra Odfjell Tankers som beskriver kvalitetssikringsprosessen for det opprinnelige pris- og volumdatasettet. I denne oppgaven legges det derfor inn en eksplisitt antagelse om at dette datasettet allerede er kvalitetssjekket av aktøren som leverte det, det vil si Odfjell Tankers, før det ble delt med prosjektgruppen. Denne antagelsen betyr ikke at datasettet anses som feilfritt, men at vi legger til grunn at grunnleggende kontroller av innhold, format og relevans allerede er utført hos dataleverandøren. Vår egen datavask må derfor forstås som en sekundær kontroll tilpasset analyse- og modellformål, ikke som en full revisjon av hele datagrunnlaget. For de supplerende voyage-dataene er det i tillegg gjennomført en egen teknisk datakvalitetskontroll i prosjektet.

---

## 6.0 Modellering

Prosjektets hovedmodell er en kvantitativ og operasjonell lineær kostnadsminimeringsmodell. Modellen arbeider på fartøy- og etappenivå og bruker 2025-voyage-dataene direkte til å beskrive rutesekvens, forbruk, startbeholdning og tankkapasitet. Prisdata fra de fire modellhavnene brukes som kostnadsparametere. Dermed svarer modellen på et operasjonelt beslutningsspørsmål:

Hvor mye bør hvert fartøy bunkre i prisede modellhavner gjennom den observerte ruten, og hvor mye må dekkes utenfor prisgrunnlaget, slik at samlet modellert drivstoffkostnad blir lavest mulig?

### 6.1 Datagrunnlag og beslutningsnivå

Hovedinput til modellen er avledet fra rådataene for voyage, kapasitet og historiske bunkringstransaksjoner. Voyage-grunnlaget gir 486 etapper for åtte anonymiserte fartøyfiler, med forbruk, observert ROB, rutehavner og måned. Kapasitetsgrunnlaget gir øvre grense for bunkersbeholdning per fartøyklasse. Prisgrunnlaget gir historiske priser for `P001`, `P002`, `P003` og `P004`.

Modellen bruker bare prisede modellhavner når de er observert tilgjengelige i den aktuelle etappens rute. Havner utenfor `P001`-`P004` får ikke egne estimerte priser. Når fartøyets behov ikke kan dekkes gjennom prisede modellhavner innenfor rute- og kapasitetsbegrensningene, brukes en egen variabel for ekstern eller ukjent bunkring. Denne variabelen gjør modellen løsbar, men synliggjør samtidig hvor datagrunnlaget ikke er tilstrekkelig for full kostnadsoptimering.

### 6.2 Sett, parametere og beslutningsvariabler

La:

- $V$ være mengden fartøyfiler
- $L_v$ være kronologisk ordnede etapper for fartøyfil $v$
- $H = \{P001, P002, P003, P004\}$ være modellhavnene med prisgrunnlag

De viktigste parameterne er:

- $c_{v,l}$ = forbruk på etappe $l$ for fartøyfil $v$
- $K_v$ = oppgitt bunkerskapasitet for fartøyklasse til fartøyfil $v$
- $I_{v,0}$ = observert startbeholdning før første etappe
- $a_{v,l,h}$ = 1 dersom modellhavn $h$ er observert tilgjengelig på etappe $l$, ellers 0
- $p_{h,t}$ = pris for modellhavn $h$ i måned $t$
- $p^U$ = proxykostnad for ekstern/ukjent bunkring

Prisparameteren bruker faktisk månedlig pris der den finnes. Dersom ruten har en modellhavn i en 2025-måned uten eksakt prisobservasjon, brukes historisk vektet snittpris for havnen. Disse snittprisene er P001: 578,75, P002: 610,29, P003: 540,84 og P004: 577,04. Ekstern/ukjent bunkring kostnadssettes til 1,25 ganger høyeste historiske havnesnitt, altså 762,86 per enhet i hovedkjøringen. Faktoren 1,25 er ikke estimert fra et eget marked for eksterne havner, men valgt som en nøytral basisverdi midt i sensitivitetsspennet 1,10-1,50. Dermed fungerer hovedscenarioet som et referansepunkt, mens sensitivitetsanalysen viser hvor mye kostnadsnivået påvirkes av denne antagelsen.

Beslutningsvariablene er:

- $x_{v,l,h}$ = bunkret mengde i modellhavn $h$ på etappe $l$ for fartøyfil $v$
- $I_{v,l}$ = modellert beholdning etter etappe $l$
- $u_{v,l}$ = ekstern/ukjent bunkring på etappe $l$

Alle beslutningsvariabler er ikke-negative.

### 6.3 Målfunksjon

Målet er å minimere samlet modellert drivstoffkostnad:

$\min Z = \sum_{v \in V}\sum_{l \in L_v}\sum_{h \in H} p_{h,t(l)}x_{v,l,h} + \sum_{v \in V}\sum_{l \in L_v} p^U u_{v,l}$

Her betegner $t(l)$ kalendermåneden etappe $l$ tilhører. Målfunksjonen gjør at modellen prioriterer prisede modellhavner når de er tilgjengelige og økonomisk gunstige, men fortsatt kan dekke behovet når ruten mangler priset havn. Siden ekstern/ukjent bunkring har høyere proxypris enn modellhavnene, blir den brukt som et kostnadsatt alternativ når prisgrunnlaget ikke dekker den operative ruten.

### 6.4 Restriksjoner

Beholdningsbalansen kobler beslutningene sammen over tid:

$I_{v,l} = I_{v,l-1} + \sum_{h \in H} x_{v,l,h} + u_{v,l} - c_{v,l}$

For første etappe brukes observert startbeholdning $I_{v,0}$ som inngang til balansen. Beholdningen må være ikke-negativ etter hver etappe, og både beholdning etter bunkring og beholdning etter forbruk kan ikke overstige fartøyets kapasitet $K_v$.

Modellen kan bare bunkre i priset modellhavn når havnen er observert i ruten:

$x_{v,l,h} = 0 \quad \text{hvis } a_{v,l,h}=0$

Dette håndheves i implementeringen ved at det bare opprettes kjøpsvariabler for modellhavner som er observert tilgjengelige på den aktuelle etappen. Dermed kan modellen ikke flytte et fartøy til en billig havn som ikke er del av den observerte ruten.

### 6.5 Modellimplementering og validering

Hovedmodellen er implementert som en lineær optimeringsmodell med `scipy.optimize.linprog`. Modellkjøringen gir resultat per fartøy, per etappe, per kjøp og en samlet oppsummering. Det genereres også en sensitivitetsanalyse for proxykostnaden på ekstern/ukjent bunkring med faktorene 1,10, 1,25 og 1,50.

Valideringen kontrollerer både intern konsistens i modellresultatene og kobling mot datagrunnlaget modellen bygger på. Den verifiserer blant annet at alle 486 etapper behandles, at forbruk, første ROB og kapasitet stemmer med rådatagrunnlaget, at beholdningen aldri blir negativ, at beholdningen ikke overstiger kapasitet før eller etter forbruk, og at kjøp i priset havn bare skjer når havnen er observert tilgjengelig i ruten. Dette gjør modellen mer etterprøvbar innenfor datagrunnlaget.

### 6.6 Avgrensninger

Modellen er operasjonell, men ikke en full produksjonsmodell. Havner utenfor `P001`-`P004` får ikke egne prisestimater, og ekstern/ukjent bunkring representerer derfor kjøp utenfor modellens prisede havnenettverk. Kontraktsflagg og drivstofftypekoblinger brukes ikke som harde restriksjoner, fordi de ikke er faglig validert på et nivå som gjør dem egnet som modellparametere. Minimumsbeholdning er heller ikke lagt inn som egen buffer utover kravet om ikke-negativ beholdning.

Sensitivitetsanalysen er avgrenset til en én-veis variasjon av proxykostnaden for ekstern/ukjent bunkring. Den tester ikke separate endringer i tankkapasitet, første ROB, modellhavnpriser eller havnetilgjengelighet.

---

## 7.0 Analyse

Analysen vurderer hvordan den operative hovedmodellen oppfører seg når den må balansere forbruk, beholdning, tankkapasitet og tilgang til prisede modellhavner gjennom fartøyenes ruter. Modellen er ikke en enkel rangering av billigste havn. Den må avgjøre om det lønner seg å fylle når en priset havn er tilgjengelig, hvor mye fartøyet har kapasitet til å ta om bord, og hvor mye som uansett må dekkes utenfor prisgrunnlaget.

Basiskjøringen bruker hovedscenarioet fra den operative modellen med ekstern proxyfaktor 1,25. Aktiviteten aggregerer resultatene per fartøyfil, modellhavn og måned som grunnlag for analysen under.

### 7.1 Dekning fra prisede modellhavner

Voyage-dataene inneholder 486 etapper. Av disse har 42 etapper minst én av modellhavnene `P001`, `P002`, `P003` eller `P004` tilgjengelig i ruten. Modellen gjennomfører faktisk kjøp i priset havn på 28 etapper. Dette viser at modellen ikke automatisk kjøper hver gang en priset havn er tilgjengelig, men vurderer kjøpet mot beholdning, kapasitet og senere forbruk.

Den månedlige fordelingen i Figur 7.1 viser hvordan modellen veksler mellom prisede modellhavner og ekstern/ukjent bunkring gjennom året. Perioder med høy ekstern/ukjent mengde tolkes som perioder der ruten i liten grad overlapper med de fire prisede modellhavnene, ikke som feil i optimeringen. Startbeholdningen forklarer også at summen av kjøp i prisede havner og ekstern/ukjent bunkring ikke nødvendigvis er lik samlet forbruk på fartøy- eller totalsnivå.

<div align="center">
  <img src="../006%20analysis/03_analyse/01_basiskjoring/figures/fig_baseline_monthly_split.png" alt="Månedlig fordeling mellom kjøp i prisede havner og ekstern ukjent bunkring" width="80%">
  <p align="center" style="font-size: 0.9em;"><small><i>Figur 7.1 Månedlig mengde kjøpt i prisede havner og ekstern/ukjent bunkring i basiskjøringen.</i></small></p>
</div>

### 7.2 Fartøyforskjeller

Modellen gir mest konkret beslutningsstøtte for fartøyfiler som faktisk møter prisede modellhavner i ruten. Fartøyfiler med mange prisede etapper får en mer konkret kjøpsplan, mens fartøyfiler uten slike etapper i praksis bare får synliggjort datagapet. For `C004-3` og `C005-1` finnes ingen etapper med priset modellhavn tilgjengelig, og modellen kan derfor ikke anbefale konkret kjøp i `P001`-`P004` for disse rutene.

Dette er et viktig operasjonelt funn. Modellen kan brukes direkte der ruten overlapper med prisgrunnlaget, men den viser også hvilke fartøy og ruter som krever bedre prisdata før Odfjell kan få full automatisert innkjøpsstøtte.

### 7.3 Kostnadsdriver og proxypris

Hovedkjøringen bruker en ekstern proxypris på 762,86 per enhet, beregnet som 1,25 ganger høyeste historiske havnesnitt blant modellhavnene. Fordi proxyprisen er høyere enn prisene i modellhavnene, fungerer ekstern/ukjent bunkring som en kostbar reservekategori. Modellen bruker den derfor primært når den ikke kan dekke forbruket gjennom prisede modellhavner innenfor rute- og kapasitetsbegrensningene.

Sensitivitetsanalysen viser at kostnadsnivået er følsomt for proxyprisen, men at selve kjøpsplanen er stabil i de testede scenarioene. Mengden kjøp i prisede havner og ekstern/ukjent mengde er uendret i disse scenarioene, fordi proxyprisen fortsatt er høyere enn prisene i modellhavnene.

<div align="center">
  <img src="../006%20analysis/03_analyse/02_sensitivitetsanalyse/figures/fig_sensitivity_total_cost.png" alt="Total modellkostnad per proxyfaktor" width="80%">
  <p align="center" style="font-size: 0.9em;"><small><i>Figur 7.2 Total modellkostnad ved ulike proxyfaktorer for ekstern/ukjent bunkring.</i></small></p>
</div>

---

## 8.0 Resultat

Dette kapittelet presenterer resultatene fra den operative hovedmodellen, basiskjøringen og sensitivitetsanalysen. Alle beløp er oppgitt i datasettets kostnadsenheter. Kapittelet presenterer funnene nøkternt; vurdering av implikasjoner og begrensninger gjøres i diskusjonskapitlet.

### 8.1 Hovedresultat

Tabell 8.1 viser hovedresultatet fra modellen. Modellen behandler alle 486 voyage-etapper og gir en samlet modellkostnad på 26 625 664,78. Prisede modellhavner finnes på 42 av etappene, og modellen gjennomfører kjøp i priset havn på 28 etapper. Kjøp i prisede modellhavner dekker 18 857,45 av samlet forbruk, mens 21 260,62 føres som ekstern/ukjent bunkring.

| Mål | Verdi |
| --- | ---: |
| Fartøyfiler | 8 |
| Voyage-etapper | 486 |
| Etapper med priset havn tilgjengelig | 42 |
| Etapper med modellert kjøp i priset havn | 28 |
| Samlet forbruk | 45 345,04 |
| Modellert kjøp i prisede havner | 18 857,45 |
| Ekstern/ukjent bunkring | 21 260,62 |
| Andel forbruk dekket av prisede havner | 41,59 % |
| Andel ekstern/ukjent av forbruk | 46,89 % |
| Kostnad i prisede havner | 10 406 690,70 |
| Kostnad for ekstern/ukjent bunkring | 16 218 974,08 |
| Total modellkostnad | 26 625 664,78 |

<p align="center" style="font-size: 0.9em;"><small><i>Tabell 8.1 Hovedresultat fra operasjonell kostnadsmodell.</i></small></p>

Resultatet viser at 41,59 % av forbruket dekkes gjennom prisede modellhavner i hovedscenarioet. Ekstern/ukjent bunkring utgjør 46,89 % av forbruket. Resterende forbruksdekning kommer fra startbeholdning og beholdningsflyt gjennom ruten.

### 8.2 Resultat per fartøyfil

Tabell 8.2 viser resultatene per fartøyfil. Fartøyfilene har ulik tilgang til prisede modellhavner, og dette gir store forskjeller i hvor mye modellen kjøper i `P001`-`P004`. `C001-2` har størst modellert kjøp i prisede havner med 6 961,16, mens `C004-3` og `C005-1` ikke har prisede modellhavner tilgjengelig i ruten og derfor ikke får modellert kjøp i disse havnene.

| Fartøyfil | Prisede etapper | Kjøp-etapper | Forbruk | Kjøp i prisede havner | Ekstern/ukjent | Total kostnad |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| C001-1 | 3 | 3 | 6 354,45 | 316,20 | 5 329,45 | 4 248 109,53 |
| C001-2 | 16 | 11 | 7 173,35 | 6 961,16 | 138,19 | 3 966 878,77 |
| C002-1 | 12 | 6 | 7 256,64 | 5 754,57 | 956,27 | 3 856 017,66 |
| C003-1 | 3 | 2 | 4 537,68 | 1 896,12 | 2 051,64 | 2 659 264,59 |
| C004-1 | 3 | 3 | 5 809,90 | 1 945,63 | 3 017,75 | 3 354 416,95 |
| C004-2 | 5 | 3 | 5 743,17 | 1 983,77 | 2 870,67 | 3 279 766,98 |
| C004-3 | 0 | 0 | 6 074,55 | 0,00 | 4 974,15 | 3 794 603,06 |
| C005-1 | 0 | 0 | 2 395,30 | 0,00 | 1 922,50 | 1 466 607,24 |

<p align="center" style="font-size: 0.9em;"><small><i>Tabell 8.2 Resultat fra operasjonell modell per fartøyfil.</i></small></p>

Fartøyfilene `C001-1`, `C004-3` og `C005-1` har minst 80 % ekstern/ukjent andel av forbruket. `C001-2` skiller seg motsatt ut med 97,04 % av forbruket dekket gjennom kjøp i prisede modellhavner og bare 1,93 % ekstern/ukjent andel.

Summen av kjøp i prisede havner og ekstern/ukjent bunkring blir ikke alltid 100 % av forbruket for hver fartøyfil. Differansen kommer fra startbeholdning og beholdningsflyt gjennom ruten, som også dekker deler av forbruket i modellen.

### 8.3 Anvendbarhet per fartøyfil

For å gjøre resultatene mer praktisk anvendbare er fartøyfilene klassifisert etter hvor direkte modellen kan brukes som beslutningsstøtte med dagens prisgrunnlag. Klasse A betyr at modellen har lav ekstern/ukjent andel og minst én priset etappe. Klasse B betyr at modellen gir delvis beslutningsstøtte, men at datagapet fortsatt er vesentlig. Klasse C betyr at modellen først og fremst viser behov for bedre prisdekning før konkrete anbefalinger kan brukes operativt.

| Fartøyfil | Prisede etapper | Kjøp i prisede havner | Ekstern/ukjent andel | Klasse | Operativ tolkning |
| --- | ---: | ---: | ---: | --- | --- |
| C001-1 | 3 | 316,20 | 83,87 % | C | Krever mer prisdata |
| C001-2 | 16 | 6 961,16 | 1,93 % | A | Direkte anvendbar innenfor dagens prisgrunnlag |
| C002-1 | 12 | 5 754,57 | 13,18 % | A | Direkte anvendbar innenfor dagens prisgrunnlag |
| C003-1 | 3 | 1 896,12 | 45,21 % | B | Delvis anvendbar |
| C004-1 | 3 | 1 945,63 | 51,94 % | B | Delvis anvendbar |
| C004-2 | 5 | 1 983,77 | 49,98 % | B | Delvis anvendbar |
| C004-3 | 0 | 0,00 | 81,89 % | C | Krever mer prisdata |
| C005-1 | 0 | 0,00 | 80,26 % | C | Krever mer prisdata |

<p align="center" style="font-size: 0.9em;"><small><i>Tabell 8.3 Anvendbarhetsklassifisering per fartøyfil basert på datadekning og ekstern/ukjent andel.</i></small></p>

Klassifiseringen gir to fartøyfiler i klasse A, tre i klasse B og tre i klasse C. Dette betyr at modellen allerede gir mest direkte beslutningsstøtte for `C001-2` og `C002-1`, mens `C001-1`, `C004-3` og `C005-1` først og fremst viser hvor Odfjell bør prioritere bedre prisdekning før modellen kan brukes operativt for tilsvarende ruter.

### 8.4 Resultat per modellhavn

Tabell 8.4 viser hvordan modellert kjøp i prisede havner fordeler seg mellom modellhavnene. `P003` står for størst kjøpsmengde i hovedscenarioet, mens `P002` er en del av modellhavnsettet, men får ingen modellert kjøp i basiskjøringen.

| Modellhavn | Kjøpsrader | Kjøpsmengde | Kostnad i priset havn | Vektet faktisk kjøpspris |
| --- | ---: | ---: | ---: | ---: |
| P001 | 1 | 565,60 | 320 090,01 | 565,93 |
| P002 | 0 | 0,00 | 0,00 | 0,00 |
| P003 | 15 | 13 441,28 | 7 287 615,34 | 542,18 |
| P004 | 12 | 4 850,57 | 2 798 985,35 | 577,04 |

<p align="center" style="font-size: 0.9em;"><small><i>Tabell 8.4 Modellert kjøp fordelt på prisede modellhavner.</i></small></p>

At `P002` ikke får modellert kjøp er et resultat av modellens kostnadsminimering innenfor observerte ruter. Havnens historiske vektede gjennomsnittspris er høyest i modellhavnsettet, og når andre prisede alternativer eller beholdning kan dekke behovet, velger modellen derfor ikke kjøp i `P002` i basisscenarioet.

### 8.5 Sensitivitet for ekstern proxypris

Tabell 8.5 viser sensitivitetsanalysen for proxykostnaden på ekstern/ukjent bunkring. Kjøpsmengdene er stabile i de tre scenarioene, men total modellkostnad endres med proxyprisen. Kostnadsspennet mellom laveste og høyeste scenario er 5 190 071,68.

| Proxyfaktor | Ekstern pris | Total modellkostnad | Kostnad i prisede havner | Ekstern kostnad |
| ---: | ---: | ---: | ---: | ---: |
| 1,10 | 671,32 | 24 679 387,90 | 10 406 690,70 | 14 272 697,20 |
| 1,25 | 762,86 | 26 625 664,78 | 10 406 690,70 | 16 218 974,08 |
| 1,50 | 915,44 | 29 869 459,58 | 10 406 690,70 | 19 462 768,88 |

<p align="center" style="font-size: 0.9em;"><small><i>Tabell 8.5 Sensitivitetsanalyse for ekstern/ukjent bunkringskostnad.</i></small></p>

<div align="center">
  <img src="../006%20analysis/03_analyse/02_sensitivitetsanalyse/figures/fig_sensitivity_cost_components.png" alt="Kostnadskomponenter per proxyfaktor" width="80%">
  <p align="center" style="font-size: 0.9em;"><small><i>Figur 8.1 Kostnadskomponenter ved ulike proxyfaktorer for ekstern/ukjent bunkring.</i></small></p>
</div>

Sensitivitetsresultatet viser at kostnad i prisede havner er 10 406 690,70 i alle de tre scenarioene, mens ekstern kostnad varierer fra 14 272 697,20 til 19 462 768,88. I basisscenarioet utgjør ekstern/ukjent kostnad 60,91 % av total modellkostnad. Dette følger av at mengdene er uendret i scenarioene, mens prisen på ekstern/ukjent bunkring endres.

Som en ekstra robusthetskontroll er det også beregnet en enkel prisnivå-sensitivitet for modellhavnene, der kjøpsplanen holdes uendret og kostnaden i `P001`-`P004` justeres med $\pm 10$ %. Denne analysen tester ikke en ny optimal kjøpsplan, men viser hvor følsomt kostnadsnivået er for generelle prisendringer i de prisede modellhavnene.

| Scenario | Endring i modellhavnpris | Kostnad i prisede havner | Ekstern kostnad | Total modellkostnad | Endring mot basis |
| --- | ---: | ---: | ---: | ---: | ---: |
| Modellhavnpris -10 % | -10 % | 9 366 021,63 | 16 218 974,08 | 25 584 995,71 | -1 040 669,07 |
| Basis | 0 % | 10 406 690,70 | 16 218 974,08 | 26 625 664,78 | 0,00 |
| Modellhavnpris +10 % | 10 % | 11 447 359,77 | 16 218 974,08 | 27 666 333,85 | 1 040 669,07 |

<p align="center" style="font-size: 0.9em;"><small><i>Tabell 8.6 Kostnadssensitivitet ved lik prosentvis endring i modellhavnprisene, med uendret kjøpsplan.</i></small></p>

---

## 9.0 Diskusjon

Hovedmodellen svarer på problemstillingen ved å formulere bunkringsbeslutningen som et operasjonelt kostnadsminimeringsproblem. Den bruker faktisk rutesekvens, forbruk, ROB og tankkapasitet, og gir dermed beslutningsstøtte for hvor mye som bør bunkres i prisede modellhavner og hvor stor del av behovet som fortsatt faller utenfor prisgrunnlaget. Sammenlignet med en ren historisk prisanalyse gir modellen derfor et mer operasjonelt beslutningsgrunnlag: den kobler prisdata til hvor fartøyene faktisk seiler, hvor mye de forbruker, og hvilke beholdningsgrenser de har.

Modellen bidrar med en konkret bunkringsplan under operative restriksjoner. Den viser hvor mye som bør fylles i prisede havner, hvordan beholdningen utvikler seg gjennom ruten, og hvor modellen må bruke ekstern/ukjent bunkring fordi prisgrunnlaget ikke dekker ruten. Dermed gir modellen både en kostnadsminimerende beslutning og en kvantitativ diagnose av datagapet.

### 9.1 Praktiske og faglige implikasjoner

Det viktigste bidraget er at modellen viser hvor Odfjell kan bruke prisede modellhavner i en konkret ruteplan. For fartøyfiler som `C001-2` og `C002-1` gir modellen betydelige kjøp i prisede havner og dermed en direkte bunkringsplan. For `C004-3` og `C005-1` finnes ingen prisede modellhavner i ruten, og modellen kan derfor ikke anbefale konkret kjøp i `P001`-`P004` for disse fartøyfilene. Dette viser at modellens verdi varierer med overlappet mellom rutedata og prisgrunnlag.

Anvendbarhetsklassifiseringen gjør denne forskjellen mer operativ. `C001-2` og `C002-1` klassifiseres som klasse A fordi de har lav ekstern/ukjent andel og flere kjøp i prisede modellhavner. Disse resultatene er de mest direkte anvendbare innenfor dagens datagrunnlag, men bør fortsatt fagvalideres før de brukes i faktisk beslutningstaking. `C003-1`, `C004-1` og `C004-2` klassifiseres som klasse B, der modellen gir delvis beslutningsstøtte, mens `C001-1`, `C004-3` og `C005-1` klassifiseres som klasse C fordi datagapet er for stort til at modellen alene kan gi konkrete operative anbefalinger.

Ekstern/ukjent bunkring må tolkes som et datagap, ikke som et nytt havnevalg. Når 46,89 % av forbruket faller i denne kategorien, betyr det at modellen er operasjonell, men at verdien for Odfjell øker betydelig dersom prisdata utvides til flere rutehavner og perioder. Dette er også tydelig på fartøynivå: `C001-1`, `C004-3` og `C005-1` har minst 80 % ekstern/ukjent andel. Modellen gir dermed både en kostnadsminimerende plan innenfor tilgjengelige data og et konkret beslutningsgrunnlag for hvilke data som bør samles inn videre.

At `P002` ikke får modellert kjøp, selv om havnen inngår i modellhavnsettet, er et interessant funn. Den mest nærliggende forklaringen er at `P002` både har høyest historisk vektet gjennomsnittspris i utvalget og begrenset nytte i de observerte rute- og beholdningssituasjonene. Modellen velger derfor heller `P003`, `P004` eller `P001` når disse er tilgjengelige, eller bruker eksisterende beholdning der det er mulig. Dette illustrerer at modellhavnstatus alene ikke er nok; havnen må også være gunstig i kombinasjonen av pris, rute, timing og tankkapasitet.

Resultatene støtter teorigrunnlaget om lineær programmering som et egnet verktøy for kostnadsminimering under restriksjoner. Modellen finner ikke bare billigste historiske havn, men må balansere kostnad mot beholdning, kapasitet og etapperekkefølge. Dette er viktig fordi lav pris alene ikke gir en gjennomførbar beslutning dersom fartøyet ikke er i nærheten av den aktuelle havnen, eller dersom tankkapasiteten ikke tillater kjøpet. Funnene samsvarer også med bunkringslitteraturen, der refueling-beslutninger typisk forstås som en kombinasjon av pris, rute, kapasitet og usikkerhet (Besbes & Savin, 2009; Wang & Meng, 2015; Zhen et al., 2017). Rapporten skiller seg fra flere av disse bidragene ved å holde rute og hastighet faste, og heller bruke modellen til å dokumentere hva som faktisk kan optimeres med begrenset prisdekning.

Teoretisk bidrar rapporten derfor ikke med en ny generell optimeringsmetode, men med en anvendt modellkobling mellom historiske transaksjonsdata og operasjonelle voyage-data. Anvendbarhetsklassifiseringen i klasse A, B og C fungerer som et metodisk tillegg fordi den gjør modellens gyldighetsområde eksplisitt. Policy-messig peker resultatene på at intern datastyring, prisdekning og standardisert registrering av bunkringsalternativer kan være like viktige som selve optimeringsalgoritmen dersom modellen skal brukes som beslutningsstøtte i større skala.

### 9.2 Begrensninger og videre bruk

Samtidig har modellen flere begrensninger som påvirker hvor langt resultatene kan tolkes. Prisgrunnlaget er avgrenset til `P001`-`P004`, og havner utenfor dette settet får ikke egne prisestimater. Ekstern/ukjent bunkring er derfor kostnadsatt med en proxy, ikke observert som et faktisk innkjøpsalternativ. Sensitivitetsanalysen viser at total modellkostnad varierer med 5 190 071,68 mellom proxyfaktor 1,10 og 1,50, mens kjøpsplanen er stabil i de testede scenarioene. En lik prisendring på $\pm 10$ % i modellhavnene gir et kostnadsspenn på 2 081 338,14 når kjøpsplanen holdes uendret. Dette betyr at kostnadsnivået er følsomt både for proxyantagelsen og prisnivået i modellhavnene, men at anbefalt kjøpsmønster i prisede havner ikke endres i de scenarioene som er testet.

For praktisk bruk hos Odfjell Tankers bør modellen derfor forstås som et beslutningsstøttende analyseverktøy, ikke som en full produksjonsmodell. En enkel bruksprosess kan være å oppdatere pris- og voyage-data, kjøre modellen, kontrollere ekstern/ukjent andel per fartøyfil, vurdere anbefalte kjøp i prisede havner og deretter bruke resultatet som støtte i innkjøpsbeslutningen. Dersom en rute havner i klasse A kan modellen gi et konkret beslutningsgrunnlag innenfor dagens prisdekning. Dersom ruten havner i klasse B eller C bør resultatet først og fremst brukes til å identifisere datagap og behov for faglig avklaring.

Før modellen kan brukes operativt i større skala, bør den utvides med flere havner, mer presise drivstoff- og kontraktskoblinger, minimumsbeholdning og eventuelt flere sensitiviteter på kapasitet, ROB og havnepriser. Det viktigste neste steget er å validere anbefalingene mot faktiske historiske bunkringsbeslutninger og mot fagpersoner hos Odfjell Tankers. Slik kan selskapet vurdere om modellens forslag er praktisk gjennomførbare, og om modellen bør inngå som fast beslutningsstøtte i bunkringsarbeidet.

---

## 10.0 Konklusjon

Problemstillingen var hvordan en lineær optimaliseringsmodell kan bidra til å minimere drivstoffkostnader for Odfjell Tankers ved bruk av historiske prisdata og operative voyage-, forbruks- og beholdningsdata. Analysen viser at en slik modell kan gi konkret beslutningsstøtte når historiske prisdata kobles med rutesekvens, forbruk, startbeholdning og tankkapasitet.

Hovedmodellen behandler 486 voyage-etapper for åtte anonymiserte fartøyfiler. I hovedscenarioet kjøper modellen 18 857,45 enheter i prisede modellhavner og fører 21 260,62 enheter som ekstern/ukjent bunkring. Total modellkostnad blir 26 625 664,78. Kjøp i prisede modellhavner dekker 41,59 % av modellert forbruk, mens ekstern/ukjent bunkring utgjør 46,89 %.

Det viktigste funnet er at modellen gir mest operativ verdi der fartøyenes ruter overlapper med prisgrunnlaget. Anvendbarhetsklassifiseringen viser at `C001-2` og `C002-1` er direkte anvendbare innenfor dagens prisgrunnlag, mens `C003-1`, `C004-1` og `C004-2` er delvis anvendbare. `C001-1`, `C004-3` og `C005-1` krever mer prisdata før modellen kan gi konkrete operative kjøpsforslag. Dette viser både modellens beslutningsverdi og begrensningen i dagens datadekning.

Sensitivitetsanalysen viser at total modellkostnad er følsom for proxykostnaden på ekstern/ukjent bunkring og for prisnivået i modellhavnene, men at kjøpsplanen er stabil i de testede scenarioene. Modellen kan derfor brukes som et transparent beslutningsgrunnlag på ruter med tilstrekkelig prisdekning, og som støtte for videre datainnsamling der ekstern/ukjent andel er høy. Full operativ anvendelse krever fortsatt bredere prisdekning, validering mot faktiske historiske bunkringsbeslutninger og faglig vurdering fra Odfjell Tankers.

Rapportens metodiske bidrag er å vise hvordan historiske transaksjonsdata kan kobles til en operasjonell rute- og lagerbasert lineær modell under tydelige databegrensninger. Anvendbarhetsklassifiseringen gjør modellens gyldighetsområde eksplisitt ved å skille mellom ruter der modellen kan gi direkte beslutningsstøtte, og ruter der resultatet først og fremst dokumenterer et datagap.

Begrensningene ligger særlig i at modellen bare dekker fire prisede modellhavner, én registrert drivstoffkategori og et avgrenset sett anonymiserte voyage-data. Ekstern/ukjent bunkring er kostnadsatt med en proxy, og modellen inkluderer ikke kontraktsvilkår, minimumsbeholdning, kvalitet, leverandørrisiko, hastighetsvalg eller regulatoriske drivstoffkrav som harde restriksjoner. Resultatene bør derfor tolkes som beslutningsstøtte og modellert potensial, ikke som en full operativ kjøpsinstruks.

Videre arbeid bør utvide prisgrunnlaget til flere havner og drivstofftyper, validere modellens forslag mot faktiske historiske beslutninger og la fagpersoner hos Odfjell Tankers vurdere om anbefalingene er praktisk gjennomførbare. Det vil også være relevant å teste minimumsbeholdning, kontraktsbindinger, alternative proxypriser og mer dynamiske prisprognoser dersom modellen skal utvikles videre mot operativ bruk.

---

## 11.0 Bibliografi

Besbes, O., & Savin, S. (2009). Going bunkers: The joint route selection and refueling problem. *Manufacturing & Service Operations Management, 11*(4), 694-711. https://doi.org/10.1287/msom.1080.0249

Du, Y., Meng, Q., & Wang, Y. (2015). Budgeting fuel consumption of container ship over round-trip voyage through robust optimization. *Transportation Research Record, 2477*(1), 68-75. https://doi.org/10.3141/2477-08

*Everything You Need to Know About Marine Fuels*. (u.å.). PDF-dokument i `003 references/Everything You Need To Know About Marine Fuels.pdf`.

*FuelEU Guidance Document for Shipping Companies*. (2025, 8. oktober). PDF-dokument i `003 references/fueleu_guidance_document_for_shipping_companies_2025-10-08.pdf`.

Fox, W. P., & Burks, R. E. (2024). *Modeling operations research and business analytics* (1. utg.). CRC Press.

Grammenos, C. T. (Red.). (2026). *The handbook of maritime economics and business* (3. utg.). Informa Law from Routledge.

Lov om opphavsrett til åndsverk mv. (åndsverkloven). (2018). LOV-2018-06-15-40. Lovdata. https://lovdata.no/LTI/lov/2018-06-15-40

Omholt-Jensen, S., Fagerholt, K., & Meisel, F. (2025). Fleet repositioning in the tramp ship routing and scheduling problem with bunker optimization: A matheuristic solution approach. *European Journal of Operational Research, 321*(1), 88-106. https://doi.org/10.1016/j.ejor.2024.09.029

Sheng, X., Chew, E. P., & Lee, L. H. (2015). (s, S) policy model for liner shipping refueling and sailing speed optimization problem. *Transportation Research Part E: Logistics and Transportation Review, 76*, 76-92. https://doi.org/10.1016/j.tre.2014.12.001

Song, D.-W., & Panayides, P. (2021). *Maritime logistics: A guide to contemporary shipping and port management* (3. utg.). Kogan Page.

Stopford, M. (2008). *Maritime economics* (3. utg.). Routledge.

Venkataraman, R. R., & Pinto, J. K. (2018). *Operations management: Managing global supply chains* (2. utg.). SAGE Publications.

Wang, S., & Meng, Q. (2015). Robust bunker management for liner shipping networks. *European Journal of Operational Research, 243*(3), 789-797. https://doi.org/10.1016/j.ejor.2014.12.049

Zhen, L., Wang, S., & Zhuge, D. (2017). Dynamic programming for optimal ship refueling decision. *Transportation Research Part E: Logistics and Transportation Review, 100*, 63-74. https://doi.org/10.1016/j.tre.2016.12.013

---

## 12.0 Vedlegg

**Vedlegg A.** `Everything You Need To Know About Marine Fuels.pdf` brukes som støttedokument for korte forklaringer av drivstofftypene `VLSFO`, `LSGO` og biodrivstoff i casebeskrivelsen.

**Vedlegg B.** `fueleu_guidance_document_for_shipping_companies_2025-10-08.pdf` brukes som støttedokument for omtalen av regulatoriske rammer og hvorfor biodrivstoff også må forstås i lys av utslippskrav.

**Vedlegg C.** Akronymer og sentrale forkortelser brukt i rapporten.

| Akronym | Forklaring | Bruk i rapporten |
| --- | --- | --- |
| LSF | Low Sulphur Fuel | Drivstofftypen i analysegrunnlaget |
| VLSFO | Very Low Sulphur Fuel Oil | Operativ hovedtype hos Odfjell, omtalt som casebakgrunn |
| LSGO | Low Sulphur Gasoil | Drivstofftype omtalt som casebakgrunn |
| ROB | Remaining On Board | Rapportert beholdning brukt som modellparameter |
| LP | Lineær programmering | Matematisk metode for kostnadsminimering |
| UN/Locode | United Nations Code for Trade and Transport Locations | Opprinnelig havnekodeformat før pseudonymisering |

<p align="center" style="font-size: 0.9em;"><small><i>Tabell C.1 Akronymer og forkortelser brukt i rapporten.</i></small></p>
