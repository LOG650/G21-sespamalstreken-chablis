# Operasjonell hovedmodell

Modellen bruker voyage-etapper, forbruk, ROB og fartøykapasitet som operative restriksjoner. Prisdata brukes for modellhavnene P001-P004. Dersom en rutehavn har prisgrunnlag, men ikke eksakt prisobservasjon i 2025-måneden, brukes historisk havnesnitt som prisproxy. Havner utenfor P001-P004 får ikke egen estimert pris; nødvendig bunkring utenfor prisgrunnlaget vises som ekstern/ukjent bunkring med konservativ proxykostnad.

## Resultat

- Fartøyfiler: 8
- Etapper: 486
- Etapper med priset havn tilgjengelig: 42
- Etapper med modellert kjøp i priset havn: 28
- Samlet forbruk: 45,345.04
- Modellert kjøp i prisede havner: 18,857.45
- Ekstern/ukjent bunkring: 21,260.62
- Andel ekstern/ukjent av forbruk: 46.89%
- Pris per ekstern/ukjent enhet: 762.86
- Kostnad i prisede havner: 10,406,690.70
- Kostnad for ekstern/ukjent bunkring: 16,218,974.08
- Total modellkostnad: 26,625,664.78

## Per fartøyfil

| Fartøyfil | Klasse | Etapper | Prisede etapper | Kjøp-etapper | Forbruk | Kjøp i prisede havner | Ekstern/ukjent | Total kostnad |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| C001-1 | C001 | 63 | 3 | 3 | 6,354.45 | 316.20 | 5,329.45 | 4,248,109.53 |
| C001-2 | C001 | 57 | 16 | 11 | 7,173.35 | 6,961.16 | 138.19 | 3,966,878.77 |
| C002-1 | C002 | 53 | 12 | 6 | 7,256.64 | 5,754.57 | 956.27 | 3,856,017.66 |
| C003-1 | C003 | 44 | 3 | 2 | 4,537.68 | 1,896.12 | 2,051.64 | 2,659,264.59 |
| C004-1 | C004 | 55 | 3 | 3 | 5,809.90 | 1,945.63 | 3,017.75 | 3,354,416.95 |
| C004-2 | C004 | 55 | 5 | 3 | 5,743.17 | 1,983.77 | 2,870.67 | 3,279,766.98 |
| C004-3 | C004 | 68 | 0 | 0 | 6,074.55 | 0.00 | 4,974.15 | 3,794,603.06 |
| C005-1 | C005 | 91 | 0 | 0 | 2,395.30 | 0.00 | 1,922.50 | 1,466,607.24 |

## Tolkning

Modellen er et faktisk lineært optimeringsproblem fordi den må balansere kjøp, forbruk, beholdning og tankkapasitet gjennom fartøyenes etapperekkefølge. Den gir Odfjell en konkret, kvantitativ plan for når det lønner seg å fylle i prisede modellhavner, og hvor mye som fortsatt må dekkes utenfor prisgrunnlaget. Ekstern/ukjent bunkring er ikke en anbefalt havn, men en kostnadsatt markør for datagapet modellen ikke kan løse uten bedre prisdekning.
