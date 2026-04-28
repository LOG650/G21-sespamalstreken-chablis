# Review: Basiskjøring og sensitivitetsanalyse

**Dato:** 2026-04-28  
**Reviewer:** Claude (uavhengig review)  
**Aktivitet:** 03_analyse/01_basiskjoring og 03_analyse/02_sensitivitetsanalyse

---

## Kort oppsummering

Aktiviteten består av to deler:

1. **Basiskjøring** (`01_basiskjoring`): En solver-uavhengig simulering der månedlig bunkerbehov allokeres til billigste tilgjengelige havn. Kjøringen dekker 61 måneder (januar 2020 – januar 2025) med fire havner (P001–P004). Resultatet viser en estimert besparelse på 4,98 % (ca. 24,9 mill.) mot historisk praksis.

2. **Sensitivitetsanalyse** (`02_sensitivitetsanalyse`): 19 scenarioer som varierer priser og etterspørsel systematisk. Scenarioene inkluderer globale prisendringer (±5 % og ±10 %), havnespesifikke prisendringer (±10 % per havn), etterspørselsendringer (±5 % og ±10 %) og kombinerte stresscenarioer (pris og etterspørsel ±10 %). I tillegg genereres rapportklare tabeller og figurer (tornadodiagram, søylediagram).

---

## Styrker

1. **Ryddig mappestruktur og sporbarhet.** Hver aktivitet har README, src, output og metadata adskilt. Input-filer er dokumentert med fulle stier i JSON-oppsummeringen, noe som gjør det mulig å gjenskape resultatene.

2. **Reproduserbar kode.** Skriptene er selvstendige, bruker kun standardbibliotek (pluss matplotlib for figurer), og trenger ingen manuell input. Alle stier er relative til repoet.

3. **Konsistent beslutningslogikk.** Basiskjøring og sensitivitetsanalyse bruker identisk allokeringslogikk (billigste tilgjengelig havn per måned), og basisscenarioet i sensitivitetsanalysen gir nøyaktig samme totalkostnad som basiskjøringen. Dette bekrefter intern konsistens.

4. **Systematiske scenarioer.** Sensitivitetsanalysen dekker både uniforme og havnespesifikke endringer, samt kombinerte stresscenarioer. Dette gir et godt bilde av modellens følsomhet langs flere dimensjoner.

5. **Rapportklare artefakter.** Tabeller og figurer genereres automatisk med norsk tallformat og figurtekster som kan brukes direkte i rapporten.

6. **God dokumentasjon.** Metadata-filene gir lett lesbare norske oppsummeringer av resultatene.

---

## Svakheter og mangler

### Metodiske

1. **Lineær og triviell beslutningsmodell.** Modellen velger alltid billigste havn uten begrensninger på kapasitet, leveringskontinuitet, transportkostnad eller kontraktsforpliktelser. Dette er en ren «perfekt informasjon»-strategi som aldri vil kunne realiseres i praksis fullt ut. Diskusjonen av realiserbarhet mangler i metadata/dokumentasjonen.

2. **Historisk kostnad som benchmark kan være misvisende.** Den historiske kostnaden beregnes som `total_qty * weighted_avg_price` per havn per måned. Hvis den historiske fordelingen på havner reflekterer logistikkhensyn (avstand, skipsstørrelse, kontrakter), overvurderer sammenligningen modellens potensial.

3. **Etterspørsel og pris endres symmetrisk.** Sensitivitetsanalysen gir nøyaktig samme resultat for «alle priser +10 %» og «etterspørsel +10 %» (begge gir 47 395 329 i endring). Dette er matematisk korrekt for en lineær modell uten kapasitetsbegrensninger, men det betyr at de to dimensjonene egentlig ikke gir uavhengig informasjon. Analysen kunne påpekt dette eksplisitt.

4. **Ingen usikkerhet i prisprognoser.** Modellen bruker observert historisk pris og sammenligner med observert historisk kostnad. Ingen fremoverskuende prognosefeil er simulert, så man vet ikke om besparelsen ville holde i en realistisk beslutningssituasjon der priser er ukjente ex ante.

5. **Havnestabilitet er ikke adressert.** P003 velges i 44 av 61 måneder, noe som betyr at modellen i praksis anbefaler å konsentrere nesten alt volum i én havn. Konsekvensen for leveringssikkerhet er ikke diskutert.

### Tekniske

6. **Duplisert kode.** Basiskjøringen og sensitivitetsanalysen dupliserer mye av datainnlastings- og beslutningslogikken. Felles hjelpefunksjoner i en delt modul ville redusert vedlikeholdsbyrden og feilrisiko.

7. **Ingen automatisert test.** Det finnes ingen unittest eller integrasjonstest som verifiserer at basiskjøring og sensitivitetsanalysens baseline faktisk gir identisk resultat. Dette hviler i dag på manuell kontroll.

8. **Manglende feilhåndtering for manglende havner.** Skriptene kaster `RuntimeError` ved manglende tilgjengelighet, men gir ingen diagnostikk som hjelper med feilsøking (f.eks. hvilke havner som faktisk var tilgjengelige den måneden).

9. **Alle priser har `price_source = "observed"`.** Det betyr at ingen priser er imputert eller estimert for den aktuelle perioden. Dette er godt for datakvaliteten, men det er ikke kommentert i metadata.

---

## Mulige forbedringer

1. **Introduser kapasitetsbegrensninger eller splittmulighet** slik at modellen kan fordele volum på flere havner i samme måned. Dette gir mer realistiske scenarier.

2. **Simuler prisprognosefeil** (f.eks. rolling window der beslutningen baseres på forrige måneds pris eller et glidende gjennomsnitt) for å kvantifisere hvor mye besparelsen avhenger av perfekt informasjon.

3. **Legg til en sensitivitetsanalyse der tilgjengelighet endres** – hva skjer om én havn faller ut i visse måneder? Dette er relevant for risikovurdering.

4. **Refaktorer felles kode** til en hjelpemodul som deles mellom basiskjøring og sensitivitetsanalyse.

5. **Legg inn en automatisk regresjonstest** som verifiserer at basisscenarioet i sensitivitetsanalysen gir nøyaktig samme totalkostnad som basiskjøringen.

6. **Kommenter den høye konsentrasjonen i P003** i oppsummeringsfilen, og vurder om dette er ønskelig fra et operasjonelt synspunkt.

7. **Vis prosentvis besparelse per måned grafisk** for å vise volatiliteten i modellens merverdi over tid (høy i 2022, lav i rolige perioder).

---

## Konklusjon og anbefaling

Arbeidet er gjennomført på en teknisk ryddig og reproduserbar måte. Kodestruktur, dokumentasjon og output-format holder god standard. Sensitivitetsanalysen gir nyttig innsikt i modellens følsomhet, særlig at havnespesifikke prisendringer (P003 og P002) dominerer utslagene.

De viktigste forbedringspunktene handler om **metodisk dybde**: modellen bør diskutere konsekvensene av perfekt informasjon og konsentrert havnevalg eksplisitt i rapporten. Uten dette risikerer man å overselge modellens potensial.

**Anbefaling:** Aktiviteten kan godkjennes som gjennomført, men resultatene bør ledsages av et avsnitt i rapportens diskusjonskapittel som adresserer begrensningene nevnt over – særlig punktene om perfekt informasjon, konsentrasjonsrisiko og lineæritet mellom pris- og etterspørselssensitivitet.
