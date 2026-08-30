# P2-E7 D18 MOFA+ — SEACells seeds 0–2

## Status and reviewer mapping

**PASS for all three SEACells seeds.** This completes the last method arm of the cross-method D18 MOFA+ component for **R2 Major 4**. R2 Major 4 as a whole is not reply-ready because peak–gene, TF–gene, RNA–protein, and held-out/cross-fit evidence remains outstanding.

## Frozen experiment

- Corrected D18, 25,517 cells; matched-K SEACells assignments, realized K=510 for every seed.
- RNA top 2,000 dispersion features, ATAC top 5,000 prevalence features, and all ADT features.
- Metacell aggregation; RNA library/log1p, ATAC TF-IDF/log1p, ADT CLR, then feature z-scoring.
- mofapy2 0.7.2, 15 factors, MOFA seed 0, maximum 1,000 iterations, convergence `medium`, scale views on, scale groups off, spike-slab weights and ARD factors/weights on.
- KMeans evaluation on factors (`random_state=0`, `n_init=20`) against dominant metacell cell type.

## Exact results

| seed | K | status | ARI | NMI | AMI | ACC | balanced accuracy | wall time | peak RSS |
|---:|---:|---|---:|---:|---:|---:|---:|---:|---:|
| 0 | 510 | PASS | 0.6563694319 | 0.7753364014 | 0.7649388662 | 0.7470588235 | 0.7179772367 | 45.98 s | 2,591,692 KiB |
| 1 | 510 | PASS | 0.6398394764 | 0.7844228067 | 0.7741142385 | 0.7313725490 | 0.6331040673 | 35.55 s | 2,591,920 KiB |
| 2 | 510 | PASS | 0.6705293194 | 0.8067788439 | 0.7977444567 | 0.7568627451 | 0.6297856905 | 42.30 s | 2,590,648 KiB |

All fits exited successfully and produced complete factor, metric, settings, and summary files. There were no failed SEACells MOFA+ attempts.

## Evidence paths

- Workflow: `revision_exp/workflows/d18_mofa_benchmark.py`
- Server results: `/data/zhangpeiru/GARQ_revision/revision_results/phase2/07_trimodal/mofa/SEACells/seed{0,1,2}`
- Server logs: `/data/zhangpeiru/GARQ_revision/revision_results/phase2/logs/P2_E7_D18_MOFA_SEACells_seed{0,1,2}.driver.log`
- Small local artifacts: `phase2_reports/07_trimodal/mofa/SEACells/seed{0,1,2}/`

## Scientific limitations and safe wording

Safe interim wording: “All three matched-K SEACells D18 assignments yielded converged MOFA+ fits, with ARI 0.6398–0.6705 and balanced accuracy 0.6298–0.7180.”

SEACells has the highest mean metrics in this particular factor-space evaluation, but this does not establish global method superiority or answer the full R2 Major 4 comment. Dominant-label evaluation rewards cell-type separation and does not test modality-specific biological associations or held-out reproducibility.

