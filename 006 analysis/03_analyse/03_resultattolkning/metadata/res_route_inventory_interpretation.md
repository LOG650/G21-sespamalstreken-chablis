# Resultattolkning for operasjonell hovedmodell

Dette notatet samler hovedfunn fra basiskjøring og sensitivitetsanalyse. Det er et støtteartefakt for rapportens analyse-, resultat- og diskusjonskapitler.

Generert: 2026-04-29T21:56:21.762434+00:00

## Hovedfunn

- Prisede modellhavner finnes på 42 av 486 etapper (8,64 %).
- Kjøp i prisede havner dekker 41,59 % av modellert forbruk.
- Ekstern/ukjent bunkring utgjør 46,89 % av modellert forbruk.
- Startbeholdning og beholdningsflyt dekker den resterende andelen på 11,53 %.
- Fartøy uten prisede modellhavner i ruten: C004-3, C005-1.
- Fartøy med minst 80 % ekstern/ukjent andel: C001-1, C004-3, C005-1.

## Fartøy og havner

- Størst modellert kjøp i prisede havner ligger på C001-2 med 6 961,16.
- Størst ekstern/ukjent mengde ligger på C001-1 med 5 329,45.
- Høyest ekstern/ukjent andel ligger på C001-1 med 83,87 %.
- Størst kjøpsvolum i priset modellhavn ligger på P003 med 13 441,28.
- Modellhavner uten kjøp i basiskjøringen: P002.

## Sensitivitet

- Total modellkostnad i basisscenarioet er 26 625 664,78.
- Kostnadsspennet i proxyanalysen er 5 190 071,68.
- Ekstern/ukjent kostnad utgjør 60,91 % av total modellkostnad i basisscenarioet.
- Laveste scenario er proxyfaktor 1,1; høyeste scenario er proxyfaktor 1,5.
- Kjøpsplanen er stabil i de testede proxy-scenarioene; analysen viser derfor kostnadseffekt, ikke endret anbefalt plan.

## Tolkning

Resultatet viser at modellen gir en konkret bunkringsplan først og fremst der fartøyenes ruter overlapper med de prisede modellhavnene. Når prisede modellhavner bare finnes på en liten andel av etappene, blir modellens operative anbefalinger sterkest for fartøy som faktisk passerer `P001`-`P004`, og svakere for fartøy som ikke gjør det.

Ekstern/ukjent bunkring på 46,89 % bør tolkes som en kvantitativ diagnose av datagapet i prisgrunnlaget, ikke som et eget operativt havnevalg. Andelen viser hvor stor del av forbruket modellen ikke kan knytte til prisede modellhavner med dagens datadekning.

Den resterende dekningsandelen på 11,53 % kommer fra startbeholdning og beholdningsflyt gjennom ruten. Dette forklarer hvorfor priset andel og ekstern/ukjent andel ikke summerer til 100 %, og gjør tolkningen av dekningsandelene mer komplett.

Proxyfaktor 1,25 er en arbeidsantagelse for ekstern/ukjent bunkring. Sensitivitetsanalysen er en smal én-veis analyse av denne antagelsen, og terskelen på 80 % brukes bare som en arbeidsdefinisjon for å identifisere fartøy der ekstern/ukjent bunkring dominerer kraftig.

## Konsistenssjekker

- OK: Kjøpsmengde er lik i alle proxy-scenarioer (verdi: [18857.451], forventet: én unik verdi).
- OK: Ekstern/ukjent mengde er lik i alle proxy-scenarioer (verdi: [21260.619], forventet: én unik verdi).
- OK: Kostnadsspenn stemmer med laveste og høyeste scenario (verdi: 5190071.68, forventet: 5190071.68).
- OK: Dekningsandeler overstiger ikke totalforbruk (verdi: 0.884729, forventet: <= 1).
- OK: Minst ett fartøy har høy ekstern/ukjent andel (verdi: 3, forventet: > 0).
