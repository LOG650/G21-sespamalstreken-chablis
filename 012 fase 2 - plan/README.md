# Planartefakter i JSON

Denne mappen inneholder maskinlesbare planartefakter for prosjektet `Minimering av drivstoffkostnader hos Odfjell Tankers`.

JSON-filene er strukturert med utgangspunkt i:

- `Prosjektstyringsplan, Odfjell Tankers.md`
- `MS_Project.mpp`
- `status.md`

Formålet er å gjøre planinformasjonen enklere å gjenbruke i videre analyse, automatisering, visualisering eller integrasjon mot andre verktøy.

## Filer

### `core.json`

Inneholder prosjektets overordnede styringsinformasjon:

- prosjektidentitet
- bakgrunn og behov
- mål og leveranser
- roller og interessenter
- omfang, forutsetninger og begrensninger
- verifikasjonsprinsipper

Bruk denne filen når du trenger et samlet bilde av prosjektets rammer og styringsgrunnlag.

### `requirements.json`

Inneholder kravregisteret fra prosjektstyringsplanen i strukturert form.

Hvert krav har blant annet:

- `id`
- `type`
- `krav`
- `gantt_aktivitet`
- `eier`
- `leveranse`
- `testtilfelle`
- `teststatus`

Bruk denne filen når du vil spore sammenhengen mellom krav, aktiviteter, leveranser og testtilfeller.

### `risk.json`

Inneholder prosjektets risikoregister og overordnet risikostyringsoppsett.

Filen dekker blant annet:

- tilnærming til risikostyring
- fokusområder
- risikobuffer
- samlet estimert tidskonsekvens
- detaljer for hver identifiserte risiko

Bruk denne filen når du vil analysere usikkerhet, oppfølgingstiltak og risikoeierskap.

### `schedule.json`

Inneholder fremdriftsbaselinen i strukturert form.

Filen omfatter:

- prosjektets baseline-datoer
- milepæler
- aktiviteter med start og slutt
- status per referansedato
- avhengigheter
- kritisk linje

Bruk denne filen når du vil jobbe videre med fremdriftsanalyse, dashboards eller enkel maskinell planoppfølging.

### `wbs.json`

Inneholder arbeidsnedbrytningsstrukturen i hierarkisk form.

Filen beskriver:

- prosjekt på toppnivå
- hovedfaser
- arbeidspakker
- aktiviteter
- milepæler

Bruk denne filen når du vil visualisere prosjektstrukturen eller knytte leveranser og aktiviteter til en WBS.

## Viktige antagelser

- `MS_Project.mpp` er brukt som styrende kilde for fremdriftsdatoer der den avviker fra tekstplanen.
- `wbs.json` er delvis avledet, fordi vedlegg B i den konverterte prosjektstyringsplanen ikke inneholder en utfylt maskinlesbar WBS.
- `Datasplit trening/test` ligger nå som egen aktivitet i gjeldende `MS_Project.mpp` og er dokumentert i JSON- og statusfilene.
- Flere felt er skrevet på norsk for å være konsistente med prosjektets arbeidsregler i repoet.

## Vedlikehold

Hvis prosjektstyringsplanen, statusfilen eller `MS_Project.mpp` oppdateres, bør også JSON-filene oppdateres slik at de fortsatt representerer gjeldende baseline.
