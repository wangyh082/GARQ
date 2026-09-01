# R2 Major 1 — D18 corrected full-data ADT 50% thinning

## Status and reviewer mapping

**PASS for seeds 0–2; label metrics stable but assignments poorly preserved.** This supports Reviewer 2 Major 1 and Reviewer 1 Major 2.

## Exact results

D18 full trimodal, 25,517 cells; ADT counts independently thinned at retention probability 0.5; requested K=510; 300 epochs; batch 256; kNN5.

| seed | K | empty | macro F1 | purity | median/max | ARI vs baseline | NMI | VI | wall | peak RSS |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0 | 509 | 1 | 0.698714 | 0.864481 | 50/107 | 0.092026 | 0.558739 | 5.399149 | 46:00.25 | 80,549,056 KiB |
| 1 | 510 | 0 | 0.697177 | 0.875487 | 50/132 | 0.093579 | 0.562512 | 5.385162 | 45:02.52 | 80,548,296 KiB |
| 2 | 510 | 0 | 0.702970 | 0.869749 | 50/112 | 0.084861 | 0.556280 | 5.372639 | 49:12.49 | 80,551,172 KiB |

Macro-F1, purity, K and size tails were stable, but same-seed ARI remained only 0.085–0.094. Stable summaries therefore do not imply membership stability.

## Evidence and limitations

- Results: `/data/zhangpeiru/GARQ_revision/revision_results/phase2/02_modality/noise_full_retry1/D18/ADT_thin_0.5/seed{0,1,2}`
- Configs: `revision_exp/configs/noise_full/p2_D18_noise_ADT_thin_0.5_seed{0,1,2}.yaml`
- Tests: 29 passed, 13 warnings

Safe wording: “With 50% ADT retention, label-level and size summaries were stable across seeds, but metacell membership was not (ARI 0.085–0.094).”

Do not equate aggregate stability with assignment robustness. The 25% and 75% retention levels remain in progress.
