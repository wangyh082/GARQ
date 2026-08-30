# P2-E7 D18 MOFA+ — MetaQ seeds 0–2

## Status and reviewer mapping

**PASS for all three MetaQ seeds.** This completes the MetaQ arm of the D18 cross-method MOFA+ experiment requested for the trimodal reviewer comment. The comment remains incomplete until SEACells is evaluated under the same protocol.

## Frozen experiment

- Corrected D18, 25,517 cells; label-free calibrated, realized-K-matched MetaQ assignments.
- RNA top 2,000 dispersion features, ATAC top 5,000 prevalence features, and all ADT features.
- Metacell aggregation; RNA library/log1p, ATAC TF-IDF/log1p, ADT CLR, then feature z-scoring.
- mofapy2 0.7.2, 15 factors, MOFA seed 0, maximum 1,000 iterations, convergence `medium`, scale views on, scale groups off, spike-slab weights and ARD factors/weights on.
- Evaluation: KMeans on MOFA factors (`random_state=0`, `n_init=20`) against dominant metacell cell type.

## Exact results

| seed | K | status | ARI | NMI | AMI | ACC | balanced accuracy | wall time | peak RSS |
|---:|---:|---|---:|---:|---:|---:|---:|---:|---:|
| 0 | 511 | PASS | 0.6106568531 | 0.7089863459 | 0.6979644345 | 0.7181996086 | 0.4347188995 | 42.52 s | 2,590,544 KiB |
| 1 | 505 | PASS | 0.4245374831 | 0.5913628882 | 0.5753258216 | 0.5801980198 | 0.4898424755 | 43.88 s | 2,589,456 KiB |
| 2 | 517 | PASS | 0.5022003128 | 0.6546337108 | 0.6414891994 | 0.6479690522 | 0.4725328928 | 39.54 s | 2,592,040 KiB |

All fits exited successfully and produced complete factor, metric, settings, and summary files. There were no failed MetaQ MOFA+ attempts.

## Evidence paths

- Workflow: `revision_exp/workflows/d18_mofa_benchmark.py`
- Server results: `/data/zhangpeiru/GARQ_revision/revision_results/phase2/07_trimodal/mofa/MetaQ/seed{0,1,2}`
- Server logs: `/data/zhangpeiru/GARQ_revision/revision_results/phase2/logs/P2_E7_D18_MOFA_MetaQ_seed{0,1,2}.driver.log`
- Small local artifacts: `phase2_reports/07_trimodal/mofa/MetaQ/seed{0,1,2}/`

## Scientific limitations and safe wording

Safe interim wording: “All three realized-K-matched MetaQ D18 assignments yielded converged 15-factor MOFA+ fits; ARI ranged 0.4245–0.6107 and balanced accuracy 0.4347–0.4898.”

Do not hide the substantial seed variation, especially the seed-1 ARI decrease. Do not claim cross-method superiority or completion until SEACells is available. These factor-space cell-type metrics do not substitute for peak-gene, TF-gene, RNA-protein, or cross-fitting analyses.
