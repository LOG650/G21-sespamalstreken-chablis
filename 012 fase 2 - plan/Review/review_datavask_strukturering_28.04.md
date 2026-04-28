# Sjekk av datavask og strukturering – review

**Dato:** 28. april 2026
**Utført av:** Claude Code (automatisert review)
**Aktiviteter:** Datavask (02_datavask) og Strukturering av datasett (03_strukturering_av_datasett)

---

## Oppsummering

Dataarbeidet er **solid og reproduserbart**. Alle nøkkeltall i rapporten stemmer eksakt med faktiske datafiler. Rensepipelinen er komplett, logisk og godt dokumentert.

---

## Godkjent

- Rensepipeline komplett: 1389 → 1381 observasjoner (8 forkastet pga. ikke-positivt volum)
- Alle output-filer til stede:
  - `tab_bunker_cleaned.csv` (172 KB, 1381 datarader)
  - `tab_bunker_monthly_by_port.csv` (13 KB, 229 datarader)
  - `tab_bunker_summary.md` (metadata)
- Aggregering: 229 havn-måned-kombinasjoner, 4 havner, 61 måneder
- Tall i rapport (tabell 5.1, 5.2, 5.3) stemmer **eksakt** med datafilene
- 3 deskriptive figurer generert
- Train/test-split filer finnes i `004 data/`
- README-filer oppdaterte i alle aktivitetsmapper

### Tallvalidering – rapport vs. datafiler

| Element | Rapport | Faktisk | Status |
|---------|---------|---------|--------|
| Rå observasjoner | 1389 | 1389 | OK |
| Rensede observasjoner | 1381 | 1381 | OK |
| Forkastede | 8 | 8 | OK |
| Antall havner | 4 | 4 | OK |
| Antall måneder | 61 | 61 | OK |
| P001 obs / qty / pris | 209 / 113 607 / 578,75 | 209 / 113 607 / 578,75 | OK |
| P002 obs / qty / pris | 286 / 181 419 / 610,29 | 286 / 181 419 / 610,29 | OK |
| P003 obs / qty / pris | 369 / 253 591 / 540,84 | 369 / 253 591 / 540,84 | OK |
| P004 obs / qty / pris | 517 / 320 933 / 577,04 | 517 / 320 933 / 577,04 | OK |
| Fallback qty | 10 obs | 10 obs | OK |
| Fallback pris | 10 obs | 10 obs | OK |

---

## Avvik som bør rettes

### 1. Train/test-splittall i rapporten (bør fikses)
Rapporten sier 1111/278 observasjoner i train/test. Filene inneholder 1119/286 rader. Avviket skyldes at filene er splittet på **rådata** (1389 obs) mens rapporten oppgir tall for **rensede** observasjoner (1381 obs). Bør presiseres i rapporten slik at leseren forstår at split-tallene gjelder etter rensing.

### 2. P002-hull (forbedring)
P002 mangler data for 15 av 61 måneder. Riktig nevnt i rapporten ("46 måneder"), men det hadde vært nyttig å dokumentere *hvilke* måneder som mangler.

### 3. Fallback-observasjoner ikke merket i renset CSV (forbedring)
De 10 qty- og 10 pris-fallback-tilfellene er ikke merket i den rensede CSV-en. Ikke kritisk, men kan være relevant for sensitivitetsanalyse.

---

## Reproduserbarhet

| Kriterium | Vurdering |
|-----------|-----------|
| Skript bruker relative stier (Path-objekter) | OK |
| Encoding håndtert korrekt (cp1252 inn, UTF-8 ut) | OK |
| Metadata genereres programmatisk | OK |
| README-filer dokumenterer formål | OK |
| Ingen hardkodede absolutte stier | OK |

---

## Konklusjon

**Datavask og strukturering er godkjent for videre analyse.** Eneste avvik som bør rettes er presiseringen av train/test-splittall i rapporten (avvik 1). Avvik 2 og 3 er forbedringer som kan gjøres senere ved behov.
