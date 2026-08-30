# P2-E7 D18 MOFA+ — KMeans seeds 0–2

## Status and reviewer mapping

**PASS for all three KMeans seeds.** This completes the KMeans arm of the D18 cross-method MOFA+ experiment requested for the trimodal reviewer comment. The full reviewer comment remains incomplete until MetaQ and SEACells are evaluated identically.

## Frozen experiment

- Corrected D18, 25,517 cells; matched-K KMeans assignments, realized K=510 for every seed.
- RNA top 2,000 dispersion features, ATAC top 5,000 prevalence features, and all ADT features.
- Metacell aggregation; RNA library/log1p, ATAC TF-IDF/log1p, ADT CLR, then feature z-scoring.
- mofapy2 0.7.2, 15 factors, MOFA seed 0, maximum 1,000 iterations, convergence `medium`, scale views on, scale groups off, spike-slab weights and ARD factors/weights on.
- Evaluation: KMeans on MOFA factors with `random_state=0`, `n_init=20`; dominant metacell cell type used only after unsupervised fitting.

## Exact results

| seed | K | dominant types | status | ARI | NMI | AMI | ACC | balanced accuracy | wall time | peak RSS |
|---:|---:|---:|---|---:|---:|---:|---:|---:|---:|---:|
| 0 | 510 | 10 | PASS | 0.6136955388 | 0.7509833522 | 0.7411188528 | 0.6882352941 | 0.5744719840 | 48.36 s | 2,591,008 KiB |
| 1 | 510 | 10 | PASS | 0.5042821478 | 0.6870389112 | 0.6753762943 | 0.6196078431 | 0.5909937261 | 41.65 s | 2,589,020 KiB |
| 2 | 510 | 11 | PASS | 0.5699907606 | 0.7205144495 | 0.7078984374 | 0.6235294118 | 0.5649889528 | 57.14 s | 2,590,356 KiB |

All fits exited successfully and produced factor, metric, settings, and summary files. There were no failed KMeans MOFA+ attempts.

## Evidence paths

- Workflow: `revision_exp/workflows/d18_mofa_benchmark.py`
- Server results: `/data/zhangpeiru/GARQ_revision/revision_results/phase2/07_trimodal/mofa/KMeans/seed{0,1,2}`
- Server logs: `/data/zhangpeiru/GARQ_revision/revision_results/phase2/logs/P2_E7_D18_MOFA_KMeans_seed{0,1,2}.driver.log`
- Small local artifacts: `phase2_reports/07_trimodal/mofa/KMeans/seed{0,1,2}/`

## Scientific limitations and safe wording

Safe interim wording: “All three matched-K KMeans D18 assignments yielded converged 15-factor MOFA+ fits; ARI ranged 0.5043–0.6137 and balanced accuracy 0.5650–0.5910.”

Do not claim KMeans or GARQ superiority before the remaining methods are complete. Seed-to-seed variation is material, and seed 2 produced 11 rather than 10 dominant metacell label classes, so balanced-accuracy comparisons must retain per-seed class context. These metrics assess factor-space recovery of dominant cell type; they do not by themselves establish peak-gene, TF-gene, RNA-protein, or cross-fitting validity.
