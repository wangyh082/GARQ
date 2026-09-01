# R2 Major 1 — D18 corrected full-data ATAC 75% retention

## Status and reviewer mapping

**PASS for seeds 0–2; seed-dependent assignment preservation.** This supports Reviewer 2 Major 1 and Reviewer 1 Major 2.

## Exact results

D18 full trimodal, 25,517 cells; ATAC counts independently thinned at retention probability 0.75; requested K=510; 300 epochs; batch 256; kNN5.

| seed | K | empty | macro F1 | purity | median/max | ARI vs baseline | NMI | VI | wall | peak RSS |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0 | 495 | 15 | 0.696658 | 0.861437 | 49/429 | 0.089069 | 0.548319 | 5.479583 | 45:34.08 | 81,041,244 KiB |
| 1 | 498 | 12 | 0.675692 | 0.873388 | 49/691 | 0.090865 | 0.555363 | 5.410802 | 47:42.69 | 81,041,328 KiB |
| 2 | 489 | 21 | 0.688545 | 0.834815 | 47/911 | 0.250239 | 0.549159 | 5.368350 | 45:36.05 | 81,042,224 KiB |

Seeds 0/1 had ARI about 0.09, whereas seed 2 reached 0.25 but had more empty anchors, lower purity, and the longest size tail. Mild ATAC thinning therefore did not yield a uniform stability response.

## Evidence and limitations

- Results: `/data/zhangpeiru/GARQ_revision/revision_results/phase2/02_modality/noise_full_retry1/D18/ATAC_thin_0.75/seed{0,1,2}`
- Configs: `revision_exp/configs/noise_full/p2_D18_noise_ATAC_thin_0.75_seed{0,1,2}.yaml`
- Tests: 29 passed, 13 warnings

Safe wording: “With 75% ATAC retention, assignment preservation was strongly seed-dependent (ARI 0.089–0.250) and the seed with higher ARI had worse purity and size-tail behavior.”

Do not claim consistent robustness from the seed-2 ARI.
