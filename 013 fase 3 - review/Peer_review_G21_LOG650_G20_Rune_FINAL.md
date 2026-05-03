Side 1 av 4Peer review-rapport — LOG650, Våren 2026
Gruppe som vurderer G20 — Rune Grødem (individuell)
Gruppe som blir vurdert G21 — Elisabeth Kirkeland Orlien og Kaylee Floden
Tittel på rapporten Optimalisering av bunkringsbeslutninger i Odfjell Tankers basert på
historiske data
Sider i rapporten 47 (inkl. forside)
Dato for vurdering 2. mai 2026

Helhetsinntrykk
Rapporten  er  en  konkret  og  selvkritisk  casestudie  som  anvender  lineær  programmering  på  et  reelt
bunkringsdatasett fra Odfjell Tankers. Strukturen følger emnemalen tett, datavasken er reproduserbar og
dokumentert  (Tabell  5.3),  den  matematiske  modellformuleringen  er  klar  (kap.  6.2–6.4),  og  rapporten
håndterer  datagap  eksplisitt  gjennom  anvendbarhetsklassifiseringen  A/B/C  (kap.  8.3).  De  viktigste
forbedringspunktene gjelder dokumentasjonen av hvor langt resultatene kan tolkes: rapporten mangler en
eksplisitt benchmark mot faktisk praksis eller en naiv kjøpsregel, slik at modellens beslutningsverdi ikke er
kvantifisert; proxyprisen for ekstern/ukjent bunkring er internt definert fra samme prisgrunnlag og mangler
uavhengig forankring, samtidig som den gjelder 46,89 % av forbruket og 60,91 % av modellkostnaden; og
enheter, valuta og datavalidering bør harmoniseres på tvers av case, modell og resultater. Samlet sett fremstår
rapporten som ærlig, godt strukturert og praktisk relevant, men med behov for en sterkere kobling fra litteratur
til metodevalg og en skarpere tolkningsramme rundt modellens dominerende kostnadsdriver.
Områdevis vurdering
1. Innledning
Styrker. Innledningen aktualiserer temaet konkret med skala og økonomisk relevans (~70 tankskip, ~400 000
tonn drivstoff, ~250 mill. USD per år, s. 7), og strukturen 1.1–1.4 er ren. Avgrensningene knyttes faglig til
datadekning  (P001–P004  og  LSF,  s.  8),  ikke  til  tidsmangel.  Antagelsene  i  1.4  er  eksplisitte  og  kobles  til
konsekvenser — særlig at manglende uavhengig datakvalitetsrapport kan videreføres i analysen (s. 9).
Forbedringspunkter. Problemstillingen er kvantitativ og avgrenset i datatype og verktøy, og fyller mal-kravet
om en regnemessig formulering. Det som likevel kan strammes inn er svaromfanget: «bidra til å minimere»
åpner for tolkninger fra «hvordan modellen formuleres» til «hvor mye Odfjell sparer», og det er først i
diskusjonen at det blir klart at rapporten primært svarer på det første. En spissere variant — f.eks. «I hvilken
grad kan en deterministisk lineær kostnadsmodell, avgrenset til fire prisede modellhavner og åtte fartøyfiler,
gi etterprøvbar beslutningsstøtte for fordelingen av bunkring i Odfjell Tankers' rutestruktur?» — vil binde
problemstillingen tettere til det modellen faktisk klarer å gjøre. Delproblemene i 1.2 er nyttige som rammeverk,
men gjenfinnes ikke som eksplisitte røde tråder i resultat- eller diskusjonskapittelet — vurder å besvare dem
direkte i 9.0 eller 10.0.

Side 2 av 42. Litteraturgjennomgang og teoretisk forankring
Styrker. Kapittel 2 plasserer rapporten i krysningen mellom operasjonsanalyse, lineær programmering og
maritim bunkring, med relevante kjernekilder (Besbes & Savin, 2009; Wang & Meng, 2015; Zhen et al., 2017;
Sheng et al., 2015; Du et al., 2015; Omholt-Jensen et al., 2025). Kapittel 3 er ryddig oppbygd rundt LP-
rammeverket (Fox & Burks, 2024) og henter inn modellforenkling/operativ relevans (Song & Panayides, 2021;
Venkataraman & Pinto, 2018).
Forbedringspunkter. Det faglige hullet, slik det formuleres på s. 11 («praktisk overgang fra et begrenset
historisk transaksjonsdatasett til en transparent og etterprøvbar beslutningsstøttemodell»), framstår mer som
en operativ anvendelse enn et teoretisk eller begrepsmessig hull. Litteraturen som er omtalt — særlig Zhen et
al. (2017) og Wang & Meng (2015) — handler nettopp om stokastiske og robuste utvidelser av problemet, men
rapporten begrunner ikke aktivt hvorfor en deterministisk LP velges fremfor disse rammeverkene. Anbefaling:
utvid med en kort metodisk avveining («LP er valgt foran stokastisk programmering fordi …») og knytt valget
tydeligere til datagrunnlagets karakter. Klassisk lager- og refueling-litteratur ((s, S)-modeller, EOQ-tankegang)
kunne også vært nevnt eksplisitt, siden modellen i praksis er en rute- og lagerbalansert kjøpsmodell.
3. Metode
Styrker. Metodeoppsettet er transparent og reproduserbart. Tabell 5.1 (s. 20) gir en ren oversikt over seks
arbeidssteg, og rensestrategien i 5.2 dokumenterer kontrollpunkter, fallback-regler og forkastinger på en måte
som gjør analysen etterprøvbar (Tabell 5.3, s. 23). Pseudonymisering av havner og voyage-koder er forklart, og
bruk av scipy.optimize.linprog gjør modellen åpen og verifiserbar. Valget om å holde rute og hastighet faste er
konsistent begrunnet og avgrenser modellens omfang tydelig.
Forbedringspunkter. Validitet, reliabilitet og etikk er presset inn i ett avsnitt (s. 21–22) og kunne vært utvidet
—  særlig  ekstern  validitet  bør  drøftes  mot  at  modellen  kun  dekker  fire  havner,  åtte  fartøyfiler  og  én
drivstoffkategori. Train/test-splitten beskrives som «datadisplin», men brukes verken som evaluering eller
robusthetstest i selve analysen (s. 24); det er en ærlig framstilling, men reiser spørsmål om hva splittens
praktiske rolle egentlig er i denne rapporten. Anbefaling: enten utnytt testdelen i 7.0 eller 8.0 (f.eks. ved å
sammenligne kjøpsmønster eller ekstern andel mellom train og test), eller forklar tydeligere hvorfor splitten
beholdes som ren dokumentasjon. Et annet forbedringspunkt er enheter og valuta: casebeskrivelsen omtaler
«metriske tonn» (s. 14), Tabell 5.5 oppgir bunkerskapasitet i m³ (s. 25), mens analyse- og resultatkapitlene
konsekvent bruker «enheter» og kostnader uten valutaangivelse. En liten samletabell som forklarer hvilken
enhet som brukes for mengde, hvilken kostnadsenhet/valuta som ligger bak modellkostnaden, og om kapasitet
og  forbruk  er  direkte  sammenlignbare,  vil  styrke  etterprøvbarheten  betydelig.  Antagelsen  om  at
dataleverandøren har kvalitetssikret datasettet (s. 27) er dessuten en kritisk premiss — vurder å markere den
enda tydeligere som risiko for funnenes generaliserbarhet.
4. Analyse og resultater
Styrker. Analysen er internt konsistent: kostnadsbalansen i hovedscenarioet (10 406 690,70 + 16 218 974,08 =
26 625 664,78) stemmer (Tabell 8.1, s. 35), forbruk per fartøyfil summerer korrekt til 45 345,04, og prosentvise
andeler  i  klasseinndelingen  (Tabell  8.3,  s.  37–38)  reproduserer  korrekt  fra  rådata-tabellen.
Anvendbarhetsklassifiseringen  A/B/C  er  et  metodisk  nyttig  tillegg  som  gjør  modellens  gyldighetsområde
eksplisitt på fartøynivå. Sensitivitetsanalysen er tydelig presentert med to akser (proxyfaktor 1,10–1,50 og
prisnivå ±10 %, Tabell 8.5–8.6).
Forbedringspunkter. Den viktigste mangelen er at rapporten ikke har en eksplisitt benchmark mot faktisk
innkjøpspraksis eller en naiv referanseregel (f.eks. «kjøp i den billigste tilgjengelige modellhavnen i ruten»).
Modellen rapporterer hva den selv velger gitt sine restriksjoner, men ikke hvor mye bedre den er enn

Side 3 av 4alternativene. Uten et slikt sammenligningsgrunnlag er beslutningsverdien ikke kvantifisert. Anbefaling: legg
inn minst én avgrenset referansemodell, eller forklar eksplisitt hvorfor en kostnads-benchmark ikke er mulig
(konfidensialitet,  manglende  faktiske  kjøpspriser).  Det  andre  store  problemet  er  at  proxyprisen  for
ekstern/ukjent bunkring (1,25 × høyeste historiske havnesnitt = 762,86, s. 29) er internt definert fra samme
prisgrunnlag som modellen optimerer på, og mangler uavhengig forankring. Siden ekstern/ukjent bunkring
gjelder  46,89  %  av  forbruket  og  60,91  %  av  modellkostnaden  i  basisscenarioet,  blir  proxyprisen  den
dominerende  kostnadsdriveren.  Knytt  proxyfaktor-valget  til  en  uavhengig  referanse  (spotmarkedsdata,
Imarex-prisbane,  observert  premium  for  off-network  bunkring),  eller  diskuter  eksplisitt  at  modellens
kostnadsnivå kun fungerer som intern sammenligning. Den operative valideringen (Tabell 7.1, s. 34) viser 16 av
76  overlappende  hendelser  og  «gjennomsnittlig  absolutt  avvik  mot  observert  slutt-ROB»  på  476,06  —
sistnevnte bør oppgis som prosent av kapasitet eller typisk forbruk, ellers er det vanskelig å vurdere om avviket
er stort eller lite. Til slutt er Tabell 4.1 (s. 17) og Tabell 5.4 (s. 25) identisk innhold; én bør sløyfes eller eksplisitt
re-refereres som «se Tabell 4.1».
5. Diskusjon
Styrker. Diskusjonen knytter funn tilbake til problemstillingen og deler implikasjonene tydelig i praksis, teori og
policy  (s.  41–42).  Erkjennelsen  av  at  modellen  ikke  er  en  historisk  rekonstruksjon  av  faktiske
bunkringsbeslutninger, men en kostnadsminimerende plan på aggregert nivå, er en presis og ærlig formulering.
Behandlingen av P002 — som inngår i modellhavnesettet, men ikke får noen modellert kjøp i basisscenarioet
— er et godt eksempel på at forfatterne reflekterer over uventede funn.
Forbedringspunkter. Diskusjonen kunne vært skarpere på den grunnleggende konsekvensen av at 46,89 % av
forbruket havner i ekstern/ukjent: gitt at denne andelen i praksis må kostnadssettes med en valgt parameter,
er det rimelig å si at modellen minimerer kostnaden ved den dekningen prisgrunnlaget tillater — ikke det totale
drivstoffinnkjøpet.  Dette  nyanseres  delvis  i  avsnitt  9.2,  men  bør  gjøres  til  et  eksplisitt  diskusjonspunkt.
Forventede vs. uventede funn er navngitt i ett avsnitt om P002, men ikke systematisk på tvers av resultatene;
vurder en kort underseksjon der dere lister hva dere forventet og hva som overrasket (lav timing-overlapp,
stabile kjøpsplaner i sensitivitetsanalysen, ulik klassetilhørighet per fartøy). Koblingen til litteraturen i 9.1
(«Funnene samsvarer også med bunkringslitteraturen», s. 42) er kort — hvilke konkrete bidrag understøttes,
og hvor avviker dere?
6. Konklusjon
Styrker. Konklusjonen  er  konsis,  gjentar  problemstillingen,  oppsummerer  hovedfunn  (kostnadsfordeling,
anvendbarhetsklasser, sensitivitet) og lister konkret videre arbeid (utvide prisgrunnlag, validere mot historiske
beslutninger, faglig vurdering hos Odfjell). Begrensninger er ærlig anerkjent.
Forbedringspunkter. Konklusjonen kan skille tydeligere mellom tre typer bidrag: (i) det praktiske bidraget for
Odfjell, (ii) det metodiske bidraget i LOG650-sammenheng, og (iii) de viktigste begrensningene. Innholdet er
allerede der, men en litt skarpere tredeling vil gjøre avslutningen mer slagkraftig. Bidraget til teori er dessuten
formulert litt forsiktig («ikke en ny generell optimeringsmetode, men en anvendt modellkobling», s. 42);
anvendbarhetsklassifiseringen er det mest interessante metodiske grepet og kan løftes fram som det teoretiske
bidraget, ikke bare som et tillegg, fordi den gir et generaliserbart språk for modellgyldighet på objektnivå.
Forslag  til  videre  forskning  kan  også  knyttes  tettere  til  problemstillingen  —  f.eks.  om
anvendbarhetsklassifiseringen kan formaliseres som metodisk verktøy også utenfor bunkringskonteksten.
7. Skriveflyt, formelle aspekter og helhetsvurdering
Styrker. Norsken er ryddig og presis, kapittelhierarkiet følger mal-strukturen, og kryssreferanser til figur og
tabell brukes systematisk. Akronymtabellen i Vedlegg C er nyttig. Den matematiske notasjonen er gjennomført

Side 4 av 4og henger sammen med tekstforklaringene. Ekstern/ukjent-variabelen og anvendbarhetsklassifiseringen er
originale grep som tydelig markerer modellens rolle som beslutningsstøtte heller enn full produksjonsmodell.
Forbedringspunkter (formalia).  Forsiden oppgir «Totalt antall sider inkludert forsiden: 46» (s. 1), men selve
PDF-en har 47 sider — sidetallet bør oppdateres. Studiepoeng og veileder mangler (s. 3), og placeholder-
tekstene  «Marker  denne  setningen  …»  for  antall  ord  og  forfattererklæring  bør  fjernes.  Det  står
«forsikningsetikk» i omtalen av REK på s. 2 — skal være «forskningsetikk». Tabell 4.1 (s. 17) og Tabell 5.4 (s. 25)
er innholdsmessig identiske; én bør sløyfes. I bibliografien bør «Everything You Need to Know About Marine
Fuels (u.å.)» og «FuelEU Guidance Document for Shipping Companies (2025, 8. oktober)» oppgraderes til full
APA-referanse med utgiver/forfatter og URL der det er aktuelt. Sjekk at Grammenos-referansen er korrekt ført
etter APA, særlig årstall/utgave. Lov om opphavsrett til åndsverk er listet i bibliografien, men brukes kun i
forsidetekstens publiseringsavtale; bibliografi-listing er ikke nødvendig hvis loven kun siteres der. Tabell C.1 i
vedlegg har ingen henvisning fra hovedteksten — en kort «se Vedlegg C» gjør den lettere å finne.
Avsluttende kommentar
Rapporten er, særlig på data- og modellsiden, et grundig og ærlig stykke arbeid. De viktigste anbefalingene er,
i  prioritert  rekkefølge:  (i)  legg  inn  en  benchmark  mot  faktisk  praksis  eller  en  naiv  referanseregel  for  å
kvantifisere  modellens  beslutningsverdi;  (ii)  gi  proxyprisen  for  ekstern/ukjent  bunkring  en  uavhengig
forankring, siden den gjelder 46,89 % av forbruket og 60,91 % av modellkostnaden i basisscenarioet; (iii)
harmoniser enheter (tonn, m³, «enheter») og valuta i en samletabell; (iv) bruk train/test-splitten til en konkret
robusthetskontroll eller ton den ned; (v) styrk metodisk begrunnelse av deterministisk LP framfor stokastiske
alternativer  i  kap.  2;  og  (vi)  rydd  de  formelle  uregelmessighetene  (sidetall,  placeholder-tekster,  typo,
tabellduplikat, APA-detaljer) før innlevering. De øvrige forbedringspunktene er nyanseringer som kan styrke et
allerede godt utkast.
