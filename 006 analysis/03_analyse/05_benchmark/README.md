# Naiv benchmark

Denne aktiviteten legger inn et enkelt sammenligningsgrunnlag for hovedmodellen etter peer review.

Benchmarken bruker en deterministisk referanseregel: På hver etappe fylles det til kapasitet i billigste tilgjengelige prisede modellhavn dersom `P001`-`P004` er tilgjengelig. Dersom beholdningen likevel ikke dekker etappeforbruket, brukes ekstern/ukjent bunkring med samme proxypris som i hovedmodellen.

Regelen er ikke en rekonstruksjon av faktisk Odfjell-praksis. Den brukes bare for å vise om LP-modellen gir lavere modellkostnad enn en enkel, naiv kjøpsregel innenfor samme datagrunnlag.

## Filer

- `src/run_naive_benchmark.py`: beregner benchmarken.
- `output/res_naive_benchmark_summary.json`: hovedtall og sammenligning mot LP-modellen.
- `output/res_naive_benchmark_by_vessel.csv`: benchmarkresultat per fartøyfil.
- `output/res_naive_benchmark_by_leg.csv`: benchmarkresultat per etappe.
- `metadata/res_naive_benchmark_summary.md`: kort lesbart sammendrag.
