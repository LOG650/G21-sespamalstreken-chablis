
# Prosjektspesifikke arbeidsregler

## Språk og tegnsett

- Bruk norsk i rapporttekst, statusfiler og planfiler.
- Behold norske bokstaver `æ`, `ø` og `å` i både kode, Markdown og genererte tabeller når filene skal leses av mennesker.
- Lagre tekstfiler som ren `UTF-8` uten BOM hvis ikke noe annet er nødvendig.
- Hvis PowerShell viser feil tegn, anta ikke at filen er ødelagt før filinnholdet er kontrollert direkte.
- Vær ekstra oppmerksom på `status.md`, `rapport.md` og genererte `.md`-tabeller, siden disse lett blir stygge ved feil encoding.

## Rapportskriving

- Skriv innhold fortløpende i rapporten underveis i prosjektet, ikke vent til alt analysearbeid er ferdig.
- I `rapport.md` skal inline matematikk skrives med `$...$`, ikke `\(...\)`, siden prosjektets Markdown-visning støtter dollar-notasjon best.
- Skill tydelig mellom:
  - `Casebeskrivelse`: beskriver bedriften, situasjonen og historiske fakta.
  - `Metode og data`: beskriver metodevalg, datagrunnlag, datakvalitet og datasplitt.
  - `Analyse/Resultat`: brukes først når faktisk prognoseanalyse og modellvurdering er gjort.
- Beskrivende figurer for historisk salg skal inn i casekapitlet, ikke i analysekapitlet.
- Datatabeller som dokumenterer datasettet skal inn i datakapitlet.
- Beskrivende historiske figurer for bunkringsdata skal ligge i kapittel 4, mens dokumentasjon av datasett, datakvalitet og train/test-splitt skal ligge i kapittel 5.
- Modellnære forklaringer, parametere, restriksjoner og kobling til modellfiler skal ligge i kapittel 6, ikke i casekapitlet.
- Når train/test-splitt omtales i rapporten, skal det beskrives eksplisitt at splitten er kronologisk etter `Delivery Date`, med de tidligste 80 % som trening og de siste 20 % som test.

## Rapportstruktur

- `Tittel/forside`: tittel, forfatter(e), sidetall og innleveringsdato.
- `Sammendrag`: kort norsk oppsummering av problem, metode, hovedfunn og konklusjon.
- `Abstract`: kort engelsk oppsummering av det samme som sammendraget.
- `Innhold`: oppdatert innholdsfortegnelse når rapporten begynner å sette seg.
- `1 Innledning`: tema, relevans, kort caseforankring, motivasjon og overgang til problemstilling.
- `1.1 Problemstilling`: presist hovedspørsmål som rapporten faktisk skal svare på.
- `1.2 Delproblemer`: bare hvis hovedproblemstillingen trenger en tydelig oppdeling.
- `1.3 Avgrensinger`: hva som er holdt utenfor og hvorfor.
- `1.4 Antagelser`: eksplisitte antagelser som analysen bygger på og hvilke konsekvenser de har.
- `2 Litteratur`: relevante kilder og tidligere arbeid som knyttes direkte til problemstillingen.
- `3 Teori`: teoretisk rammeverk og begreper som brukes senere i metode, analyse og diskusjon.
- `4 Casebeskrivelse`: bedriften, beslutningssituasjonen og historiske fakta fra datasettet.
- `4.1 PowerHorse og beslutningssituasjonen`: hva bedriften trenger beslutningsstøtte til.
- `4.2 Historisk salgsutvikling`: beskrivende figurer og tekst om utvikling over tid.
- `4.3 Sesongmønster i salget`: sesongbeskrivelse med figur og eventuell tabell i tallform.
- `4.4 Utfordringer dårlige prognoser medfører i bedriften`: konsekvenser for produksjon, lager og planlegging.
- `5 Metode og data`: valgt tilnærming, datagrunnlag, datakvalitet og datasplitt.
- `5.1 Metode`: analyseopplegg, modellstrategi og hvordan arbeidet gjennomføres.
- `5.2 Data`: periode, variabler, observasjoner, datakvalitet og trening/test-oppsett.
- `6 Modellering`: konkret modellvalg, spesifikasjon og estimeringsopplegg.
- `7 Analyse`: analyse av modelloppførsel, residualer, prognoseegenskaper og tolkning.
- `8 Resultat`: resultater som presenteres ryddig med figurer, tabeller og kort forklaring.
- `9 Diskusjon`: vurdering av funnene opp mot problemstilling, teori, metode og begrensninger.
- `10 Konklusjon`: kort svar på problemstillingen og viktigste implikasjoner for caset.
- `11 Bibliografi`: fullstendig og konsistent referanseliste.
- `12 Vedlegg`: supplerende tabeller, figurer, utvidede resultater eller annet støttemateriale.

Les også filen @000 templates\Mal prosjekt LOG650 v2.docx for mer detaljert tips og krav.

## Rapportsjekkliste

- Innledningen skal være kort og presis, normalt rundt 1-2 sider.
- Innledningen skal aktualisere temaet og forklare hvorfor oppgaven er relevant.
- Innledningen kan kort nevne casebedriften, men detaljene skal ligge i kapittel 4.
- Problemstillingen bør formuleres som et `hvordan`- eller `hvorfor`-spørsmål når det passer faglig.
- Problemstillingen må være så presis at rapporten verken svarer på mer eller mindre enn det som er formulert.
- Delproblemer brukes bare når de gir en klarere struktur på analysen.
- Avgrensinger skal begrunnes faglig, ikke med tidsmangel.
- Antagelser skal forklares og knyttes til konsekvenser for analysens aktualitet og gyldighet.
- Litteraturkapitlet skal knytte kilder til problemstillingen, ikke bare oppsummere løsrevne referanser.
- Teorikapitlet skal gi et faktisk grunnlag for metodevalg og tolkning senere i rapporten.
- Resultatkapitlet skal presentere funn nøkternt; diskusjon og vurderinger hører hjemme i diskusjonskapitlet.
- Diskusjonskapitlet skal knytte funn til problemstilling, litteratur, usikkerhet og praktiske implikasjoner.
- Konklusjonen skal svare direkte på problemstillingen og løfte fram de viktigste funnene.

## Figurer i rapporten

- Bruk HTML for bilder i `rapport.md`, ikke vanlig Markdown-bildeformat, når bredde og sentrering skal styres.
- Standard for rapportfigurer i dette prosjektet:
  - sentrert figur
  - `width=\"80%\"`
  - kort figurtekst under figuren
- Figurtekst skal være:
  - sentrert
  - liten skrift
  - kursiv
- Foretrukket mønster:

```html
<div align="center">
  <img src="..." alt="..." width="80%">
  <p align="center"><small><i>Figur X Kort figurtekst.</i></small></p>
</div>
```

- Figurteksten skal være kort og nøktern, ikke en hel forklaring.
- I dette repoet brukes nå også `style="font-size: 0.9em;"` på figurteksten for å gjøre den litt mindre enn brødteksten når Markdown-visningen støtter det.
- Figurtekstene skal tydelig si om figuren viser en tidsserie for hver enkelt måned eller et gjennomsnitt aggregert på tvers av flere år.

## Tabeller i rapporten

- Tabeller kan limes inn direkte som Markdown-tabeller når de er små og lesbare.
- Tabeller skal ha en kort introduksjonssetning i brødteksten før de settes inn.
- Bruk tabellnummer i teksten, for eksempel `Tabell 4.1`.
- Tabeller som trenger tabelltekst kan få samme stil som figurtekster: sentrert, liten skrift og kursiv under tabellen.

## Kode og analyse

- Analysearbeid i `006 analysis` organiseres etter aktiviteter i prosjektplanen.
- Ett felles `uv`-prosjekt brukes for hele `006 analysis`.
- Skript, figurer og resultatfiler skal ligge i samme aktivitetsmappe.
- Filnavn i analyseartefakter skal være korte, ryddige og prefikset med `fig_` og `tab_`.
- `006 analysis` er nå organisert i hovedmappene `01_datagrunnlag`, `02_modellutvikling` og `03_analyse`, med undermapper per aktivitet i planen.
- Innen hver aktivitetsmappe skal man så langt som mulig skille mellom `src`, `input`/`data`, `output`, `figures` og `metadata`.
- Behold versjonsmerking som `v1` i filnavn og metadata når relevant, men la mappestrukturen følge aktivitetene i prosjektplanen heller enn modellversjoner.
- Når datasett splittes i trening og test, skal originalfilen beholdes urørt, og nye filer opprettes som egne filer med tydelige navn.

## Review av aktiviteter

- Når en aktivitet skal reviewes med `review-act`-skillen, start alltid en egen subagent (Agent-verktøyet) for å gjennomføre reviewen. Dette sikrer uavhengighet og unngår bias fra konteksten i hovedsamtalen.

## Praktiske preferanser i dette repoet

- Når noe er fullført i prosjektet, oppdater både planfiler og `status.md`.
- Nye arbeidssteg bør legges inn i planen før aktiviteten lukkes.
- Når noe bare er en antagelse, skriv det eksplisitt som antagelse og ikke som verifisert fakta.
- `status.md` skal fungere som et levende styringsdokument med innholdsfortegnelse, neste steg, Gantt/milepæler og sjekklister, ikke bare som en statisk logg.
- Når et nytt mellomsteg oppstår i arbeidet, som datasplitt eller dokumentasjon i rapporten før neste aktivitet, skal det legges inn som egen task i planfilene før hovedaktiviteten lukkes.
