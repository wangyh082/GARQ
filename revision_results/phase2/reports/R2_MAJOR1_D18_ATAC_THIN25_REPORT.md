# R2 Major 1 — D18 corrected full-data ATAC 25% retention

## Status and reviewer mapping

**PASS for seeds 0–2; reproducibly poor assignment preservation.** This supports Reviewer 2 Major 1 and Reviewer 1 Major 2.

## Exact results

D18 full trimodal, 25,517 cells; ATAC counts independently thinned at retention probability 0.25; requested K=510; 300 epochs; batch 256; kNN5.

| seed | K | empty | macro F1 | purity | median/max | ARI vs baseline | NMI | VI | wall | peak RSS |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0 | 497 | 13 | 0.669625 | 0.840287 | 49/635 | 0.071492 | 0.526501 | 5.710532 | 45:52.83 | 81,043,964 KiB |
| 1 | 501 | 9 | 0.671740 | 0.866823 | 47/850 | 0.072930 | 0.537761 | 5.601612 | 45:25.84 | 81,043,252 KiB |
| 2 | 500 | 10 | 0.673483 | 0.847807 | 46/859 | 0.073519 | 0.526332 | 5.625572 | 45:55.14 | 81,042,168 KiB |

Macro-F1 and ARI were numerically stable across seeds, but ARI was consistently only about 0.072. Maximum metacell size increased from 635 to about 850.

## Evidence and limitations

- Results: `/data/zhangpeiru/GARQ_revision/revision_results/phase2/02_modality/noise_full_retry1/D18/ATAC_thin_0.25/seed{0,1,2}`
- Configs: `revision_exp/configs/noise_full/p2_D18_noise_ATAC_thin_0.25_seed{0,1,2}.yaml`
- Tests: 29 passed, 13 warnings

Safe wording: “At 25% ATAC count retention, macro-F1 was stable across seeds, but metacell membership was consistently poorly preserved (ARI approximately 0.072).”

Do not equate reproducibility of a low ARI with perturbation robustness.
