# R2 Major 1 — D18 corrected full-data RNA 75% retention

## Status and reviewer mapping

**PASS for seeds 0–2; poor and seed-dependent assignment preservation.** This supports Reviewer 2 Major 1 and Reviewer 1 Major 2.

## Exact results

D18 full trimodal, 25,517 cells; RNA counts independently thinned at retention probability 0.75; requested K=510; 300 epochs; batch 256; kNN5.

| seed | K | empty | macro F1 | purity | median/max | ARI vs baseline | NMI | VI | wall | peak RSS |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0 | 493 | 17 | 0.683746 | 0.867021 | 47/761 | 0.124886 | 0.522222 | 5.747158 | 48:32.81 | 80,763,200 KiB |
| 1 | 491 | 19 | 0.720599 | 0.791360 | 46/1413 | 0.061200 | 0.532129 | 5.600911 | 45:45.19 | 80,767,492 KiB |
| 2 | 488 | 22 | 0.683935 | 0.870435 | 47/1216 | 0.078055 | 0.523696 | 5.626052 | 48:34.84 | 80,755,396 KiB |

Even mild thinning produced ARI only 0.061–0.125. Seed 1 had the highest macro-F1 but lowest purity, lowest ARI, and largest size tail, again showing that label F1 alone is misleading.

## Evidence and limitations

- Results: `/data/zhangpeiru/GARQ_revision/revision_results/phase2/02_modality/noise_full_retry1/D18/RNA_thin_0.75/seed{0,1,2}`
- Configs: `revision_exp/configs/noise_full/p2_D18_noise_RNA_thin_0.75_seed{0,1,2}.yaml`
- Tests: 29 passed, 13 warnings

Safe wording: “With 75% RNA retention, metacell membership remained poorly preserved and seed-dependent (ARI 0.061–0.125), despite moderate label-level macro-F1.”

Do not claim robustness to mild RNA thinning or select seed 1 based on macro-F1.
