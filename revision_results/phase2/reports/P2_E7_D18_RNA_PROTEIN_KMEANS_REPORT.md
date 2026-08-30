# P2-E7 D18 RNA–protein — KMeans seeds 0–2

## Status and reviewer mapping

**PASS for all three seeds.** These descriptive full-feature runs contribute to R2 Major 4 but are not confirmatory; feature-excluded reruns and the remaining methods are outstanding.

## Experiment

Corrected D18 matched-K KMeans assignments, 25,517 cells, realized K=510. Fifteen mapped RNA–ADT pairs per seed; RNA library/log1p and ADT log1p/CLR metacell profiles. Reported Pearson, Spearman, dominant-cell-type partial Pearson, and 1,000-resample bootstrap intervals.

| seed | pair | Pearson r | partial r | bootstrap 95% CI |
|---:|---|---:|---:|---:|
| 0 | NCAM1–CD56 | 0.595180 | 0.234655 | [0.124415, 0.321510] |
| 0 | CD8A–CD8a | 0.656592 | 0.295225 | [0.221726, 0.360907] |
| 1 | NCAM1–CD56 | 0.612556 | 0.254639 | [0.154633, 0.340120] |
| 1 | CD8A–CD8a | 0.640139 | 0.262443 | [0.171046, 0.337062] |
| 2 | NCAM1–CD56 | 0.621170 | 0.294849 | [0.204813, 0.372211] |
| 2 | CD8A–CD8a | 0.626398 | 0.245415 | [0.156530, 0.317952] |

All 45 rows were complete and finite; no KMeans run failed.

## Evidence

- Exact rows: `revision_results/phase2/07_trimodal/rna_protein/KMeans_seed{0,1,2}.csv`
- Server logs: `/data/zhangpeiru/GARQ_revision/revision_results/phase2/logs/P2_E7_D18_RNAPROTEIN_KMeans_seed{0,1,2}.driver.log`
- Workflow: `revision_exp/workflows/d18_rna_protein_benchmark.py`

## Safe wording and limitations

Safe interim wording: “In three descriptive matched-K KMeans aggregations, both prespecified RNA–protein pairs retained positive within-cell-type associations.”

Do not call these associations causal, held-out, or de-circularized. The narrow intervals reflect metacell bootstrapping within each fixed assignment and do not capture method-selection uncertainty. Full-feature assignments used the evaluated markers, so feature exclusion remains required.
