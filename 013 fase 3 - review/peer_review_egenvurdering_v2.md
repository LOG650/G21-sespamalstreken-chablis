# Peer-review av rapporten "Optimalisering av bunkringsbeslutninger i Odfjell Tankers basert på historiske data" — versjon 2

**Vurderende gruppe:** *(fyll inn)*
**Vurdert gruppe:** G21 - Sespamalstreken Chablis (Orlien & Floden)
**Dato:** 2026-04-30

---

## 1. Helhetsinntrykk

Rapporten har en tydelig rød tråd fra problemstilling, via teori og metode, til en operasjonell lineær optimaliseringsmodell som faktisk kjøres på reelle data fra Odfjell Tankers. Metodekapitlet er løftet betydelig sammenlignet med forrige versjon: den nye Tabell 5.1 (l. 320-329) mapper hvert arbeidssteg eksplisitt til en metode og et formål, og det nye avsnittet (l. 331) om hvilke metoder som *ikke* er valgt (ML, tidsserieprognoser, EOQ, køteori, simulering, multikriterier) med faglig begrunnelse svarer direkte på veiledningens krav om begrunnelse for valgte metoder. De viktigste gjenværende utfordringene er: (i) litteraturkapitlet identifiserer fortsatt ikke faglige hull, (ii) innholdsfortegnelsen er ikke oppdatert til ny tabellnummerering eller utvidet metodestruktur, (iii) "ekstern/ukjent bunkring" introduseres fortsatt uforklart i sammendraget, (iv) konklusjonen mangler eksplisitte avsnitt om begrensninger og videre forskning, og (v) APA 7-konsistens i bibliografien er fortsatt mangelfull.

---

## 2. Områdevis vurdering

### 2.1 Innledning

**Styrker:** Innledningen aktualiserer temaet kort og knytter det til både volatilitet (Stopford, 2008) og regulatoriske rammer (FuelEU, 2025). Problemstillingen (l. 166) er presis og formulert som et "hvordan"-spørsmål. Delproblemene (1.2) er logisk avledet, og avgrensingene (1.3) er faglig begrunnet.

**Forbedringspunkter:**
- Begrepet "ekstern/ukjent bunkring" brukes i sammendraget (l. 92) og abstract (l. 102) før det forklares. Tallene 21 260,62 og 46,89 % er vanskelige å tolke for en førstegangsleser. Forslag: én forklarende setning i sammendraget ("ekstern/ukjent bunkring representerer behov som ikke kan dekkes gjennom de prisede modellhavnene").
- Studiens betydning ("hvorfor er dette verdt å undersøke?") står implisitt i casebeskrivelsen, men bør gjøres eksplisitt i innledningen — gjerne med henvisning til volumet på 400 000 tonn / 250 mUSD som først kommer i 4.1.
- Antagelse 2 i 1.4 om at datasettet er "grunnleggende kvalitetssjekket av dataleverandøren" er sterk uten dokumentasjon. Konsekvensen for analysens gyldighet bør antydes allerede her, ikke bare i 5.2.

### 2.2 Litteraturgjennomgang og teoretisk forankring

**Styrker:** Teorikapittelet (3.0) skiller tydelig mellom beslutningsvariabler og parametere (3.2), og knytter teori om modellforenkling til den maritime konteksten. Begrunnelsen for kronologisk train/test-splitt (3.4) er ryddig.

**Forbedringspunkter:**
- Litteraturkapitlet (2.0) hviler fortsatt nesten utelukkende på fire-fem lærebøker. Veiledningen krever "gjennomgang av relevant forskning" og "identifikasjon av teoretiske eller begrepsmessige hull" — det siste mangler. Forslag: utvid med 4-6 peer-reviewed artikler om *bunker management*, *fuel inventory routing* eller *ship refueling problem* (f.eks. Besbes & Savin, Sheng et al., Wang et al.), og avslutt med ett avsnitt der dere eksplisitt formulerer hvilket hull rapporten plasserer seg i.
- Grammenos (2026) er datert ett år frem i tid (l. 705) — verifiser eller korriger.
- Litteratur- og teorikapitlet refererer i stor grad til de samme kildene. Skill tydeligere: kapittel 2 plasserer rapporten i forskningsfeltet, kapittel 3 etablerer det operative begrepsapparatet.

### 2.3 Metode

**Styrker (vesentlig løft i denne versjonen):**
- **Tabell 5.1** (l. 320-329) er nå et godt metodisk oversiktskart som binder problemstilling, metoder og formål sammen i én ryddig oversikt. Dette gjør metodekapitlet vesentlig sterkere mot veiledningskriteriet "Detaljer i analytisk rammeverk og framgangsmåte".
- Det nye avsnittet (l. 331) som eksplisitt navngir hvilke metoder som *ikke* er brukt (ML, tidsserieprognoser, EOQ, køteori, simulering, multikriterier) med faglig begrunnelse er en stor styrke. Dette demonstrerer at alternativene er vurdert, og styrker svaret på kriteriet "begrunnelse for valgte metoder".
- Renseprosessen (l. 333-335) er reproduserbar, fallback-regler er dokumentert (Tabell 5.3), og train/test-splitt er begrunnet selv om hovedmodellen er deterministisk (l. 381). Tabell 5.6 dokumenterer omfang, kvalitet og bruk i samme tabell — forbilledlig.

**Forbedringspunkter:**
- **Validitet og reliabilitet** er fortsatt ikke eksplisitt diskutert som egne begreper. Intern konsistensvalidering nevnes (6.5), men ekstern validitet (overføringsverdi til andre fartøy/havner/perioder) og reliabilitet (kjørestabilitet, sensitivitet for inputvariasjoner) bør skilles og navngis. Forslag: ett kort avsnitt sist i 5.1 med tre underpunkter "validitet", "reliabilitet", "etikk".
- **Etiske hensyn** er ikke omtalt. Pseudonymisering av havner og fartøy (l. 337) berører nettopp etiske/konfidensielle hensyn og burde løftes til metodekapitlet. Veiledningen tillater å utelate kriteriet, men ber da om en kort begrunnelse.
- Valg av **proxyfaktor 1,25** (l. 470) presenteres uten faglig begrunnelse. Hvorfor 1,25 som basis? Anbefal: enten begrunn (f.eks. erfaringstall, midtpunkt mellom typiske spotpåslag) eller marker eksplisitt som "nøytral midtverdi i sensitivitetsspennet 1,10-1,50".
- Funksjonen **$t(l)$** i målfunksjonen (l. 484) er ikke eksplisitt definert. Tilføy: "der $t(l)$ betegner kalendermåneden etappe $l$ tilhører".
- Implementeringsdetaljen `available_ports_P00X` (l. 451, l. 500) lekker fra koden inn i rapporten. Erstatt med en ren tekstlig formulering ("modellhavner observert tilgjengelige i etappens rute").

### 2.4 Analyse og resultater

**Styrker:** Analysen (kap. 7) og resultatene (kap. 8) er internt konsistente; tallene i Tabell 8.1 stemmer overens med tekst i 7.1 og sammendraget. Anvendbarhetsklassifiseringen (8.3, Tabell 8.3) er en god analytisk tilleggsstørrelse som gjør resultatene operative. Sensitivitetsanalysen er rapportert med både tabell og figur, og dekker både ekstern proxypris (Tabell 8.5) og ±10 % prisnivå (Tabell 8.6).

**Forbedringspunkter:**
- Det er fortsatt betydelig overlapp mellom kapittel 7 og 8 — flere tall (18 857,45, 21 260,62, 41,59 %, 46,89 %) gjentas. Veiledningen og prosjektets egen rapportsjekkliste skiller eksplisitt: kapittel 7 vurderer modelloppførsel, kapittel 8 presenterer funnene nøkternt. Forslag: la 7 fokusere på *hvordan* modellen oppfører seg (etappevalg, kapasitetsbinding, beholdningsforløp) og la 8 være ren tabell- og figurpresentasjon.
- Avsnitt **7.4 "Modellens bidrag"** (l. 552) leser fortsatt som diskusjon. Flytt eller omformuler.
- For klasse C-fartøyene (`C004-3`, `C005-1`) er ekstern/ukjent prosent rapportert (81,89 % og 80,26 %), men summen av priset + ekstern/ukjent gir ikke 100 %. Differansen kommer trolig fra startbeholdning — dette bør forklares kort der det først vises (under Tabell 8.2 eller 8.3).

### 2.5 Diskusjon

**Styrker:** Diskusjonen (kap. 9) knytter funnene tilbake til problemstillingen og teorigrunnlaget om LP under restriksjoner (l. 675). Den skiller tydelig mellom hva modellen *kan* og *ikke kan* basert på datadekning, og foreslår en konkret bruksprosess (l. 679).

**Forbedringspunkter:**
- Diskusjonen drøfter ikke uventede funn. At **`P002` ikke får noen kjøp** på tross av å være i modellhavnsettet (Tabell 8.4) er et slikt funn som fortjener egen kommentar — er det fordi havnen er dyrest, ikke i ruten, eller begge?
- Implikasjoner for *teori* og *policy* (jf. veiledning) mangler. I dag drøftes hovedsakelig praktiske implikasjoner.
- Diskusjonen kobler ikke funnene tilbake til litteraturkapitlet. Når litteraturen utvides (jf. 2.2), bør diskusjonen sammenligne resultatene med tidligere funn.

### 2.6 Konklusjon

**Styrker:** Konklusjonen (kap. 10) svarer direkte på problemstillingen og oppsummerer hovedtallene presist. Klassifiseringen i klasse A/B/C løftes som et sentralt funn.

**Forbedringspunkter:**
- Veiledningen krever eksplisitt: "refleksjon over begrensninger" og "forslag til videre forskning". Begge mangler som egne avsnitt. Forslag: legg inn to korte avsnitt nederst i kapittel 10.
- Studiens bidrag til *teori* er ikke nevnt, kun praktisk bidrag. Kan rammes inn som metodisk bidrag (kobling av historiske transaksjonsdata til operasjonell rute-/lager-LP under datadekningsbegrensninger, med eksplisitt anvendbarhetsklassifisering).

### 2.7 Skriveflyt, formelle aspekter og helhetsvurdering

**Språk og struktur:** Språket er klart, fagtermer er jevnt over godt forklart. Norske bokstaver er gjennomført.

**Forbedringspunkter:**

- **Forsiden** (l. 1-86) mangler utfylte verdier for `Totalt antall sider`, `Studiepoeng`, `Veileder`, `Dato`, `Antall ord`, samt avkrysning på egenerklæring og publiseringsavtale.
- **Innholdsfortegnelsen** (l. 110-147) er ikke synkronisert med den oppdaterte rapporten. Den viser kun 5.1 Metode og 5.2 Data, og reflekterer ikke at metodekapitlet nå har en metode-tabell og en eksplisitt diskusjon av valgte/ikke-valgte metoder. Den må også oppdateres dersom 7.4 omklassifiseres eller flyttes.
- **Tabellnummerering:** den nye Tabell 5.1 har skjøvet de øvrige tabellene i kapittel 5 ned ett hakk (5.2-5.6). Sjekk at alle teksthenvisninger til disse tabellene (f.eks. l. 345, l. 362, l. 387, l. 400, l. 412) er oppdatert konsistent — det ser riktig ut nå, men dette er et typisk sted feil snur seg etter omnummerering.
- **4.4 og 4.5** har nesten identiske titler ("Konsekvenser av begrenset beslutningsgrunnlag" / "Utfordringer ved begrenset beslutningsgrunnlag"). Slå sammen eller skill skarpere.
- **Drivstoffbenevnelse:** Casebeskrivelsen sier hovedtypen er VLSFO (l. 246), mens analysegrunnlaget er LSF. Forholdet mellom de to bør klargjøres tidligere — er LSF en samlebetegnelse eller en spesifikk variant?
- **APA 7:** Bibliografien er ikke fullt konsistent: blanding av "&" og "og" mellom tekst og liste, "1st ed."/"3rd ed." på engelsk i en norsk rapport, manglende DOI/ISBN, "u.å." på et dokument med datostempel (Vedlegg A), Grammenos datert 2026 (fremtidig). Veiledningen nevner APA 7 eksplisitt.
- **Kryssreferanser:** Tabeller og figurer refereres jevnt med "Tabell 4.1", "Figur 7.2" — bra. Men noen ganger med backticks (`Tabell 4.1`), andre ganger uten. Vær konsistent.
- **Akronymer:** LSF, VLSFO, LSGO, ROB, LP introduseres ujevnt. Lag akronymliste i innledningen eller som vedlegg.
- **Figurtekst-stil:** CLAUDE.md spesifiserer `<small><i>` for figurtekst, men flere figurer (4.1, 4.2, 4.3, 7.1, 7.2, 8.1) bruker `style="font-size: 0.9em;"` uten `<small>`. Tabellteksten bruker `<small><i>`. Vær konsistent.
- **Vedlegg:** Vedlegg A og B er bare henvisninger til PDF-er, og Vedlegg C dupliserer Tabell 8.5. Forslag: legg inn fartøyspesifikke detaljer (per-etappe-resultater, beholdningsforløp for klasse A-fartøy) som ekte vedlegg.
- **Originalitet:** Anvendelsen av rute- og lagerbasert LP på et konkret rederi-case med eksplisitt klassifisering av modellens anvendbarhet (klasse A/B/C) er originalt og praktisk verdifullt. Dette bidraget bør løftes tydeligere i konklusjonen.

---

## 3. Hovedendring siden forrige versjon

Metodekapitlet er klart styrket. Tabell 5.1 og avsnittet om ikke-valgte metoder svarer direkte på forrige punkt om manglende begrunnelse for metodevalget, og gir et tydeligere svar på veiledningens kriterier "Metodevalgene er plausible og sammenhengende" og "begrunnelse for valgte metoder".

## 4. Oppsummering av prioriterte tiltak

1. **Innholdsfortegnelse:** synkroniser med oppdatert kapittelstruktur.
2. **Forside:** fyll inn manglende felt før innlevering.
3. **Sammendrag/abstract:** forklar "ekstern/ukjent bunkring" ved første nevning.
4. **Litteraturkapittel:** utvid med 4-6 peer-reviewed referanser om bunker management/fuel routing og formuler eksplisitt hvilket hull rapporten adresserer.
5. **Konklusjon:** legg inn egne avsnitt om begrensninger og videre forskning.
6. **Validitet/reliabilitet/etikk:** legg inn som korte navngitte avsnitt sist i 5.1.
7. **Bibliografi:** rens for APA 7-konsistens; verifiser Grammenos-året.
8. **Kapittel 7 vs 8:** reduser overlapp; flytt avsnitt 7.4 til diskusjon.
9. **Begrunn proxyfaktor 1,25**, definer $t(l)$, og fjern `available_ports_P00X` fra rapportteksten.
