# R2 Major 1 — D18 corrected full-data ATAC 50% thinning

## Status and reviewer mapping

**PASS for seeds 0–2; poor assignment stability and unstable size tails.** This count-level condition supports Reviewer 2 Major 1 and Reviewer 1 Major 2.

## Exact results

D18 full trimodal, 25,517 cells; ATAC counts independently thinned with retention probability 0.5; requested K=510; 300 epochs; batch 256; kNN5.

| seed | K | empty | macro F1 | purity | median/max | ARI vs baseline | NMI | VI | wall | peak RSS |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0 | 500 | 10 | 0.682047 | 0.856562 | 48/582 | 0.118059 | 0.545188 | 5.492813 | 46:21.85 | 81,042,812 KiB |
| 1 | 492 | 18 | 0.670930 | 0.851854 | 47/882 | 0.080183 | 0.548686 | 5.453141 | 46:11.55 | 81,041,636 KiB |
| 2 | 490 | 20 | 0.689499 | 0.846111 | 46/1584 | 0.066664 | 0.541698 | 5.426007 | 46:32.47 | 81,035,056 KiB |

Assignment ARI declined from 0.118 to 0.067 across seeds, empty anchors increased from 10 to 20, and maximum size increased from 582 to 1,584.

## Evidence and limitations

- Results: `/data/zhangpeiru/GARQ_revision/revision_results/phase2/02_modality/noise_full_retry1/D18/ATAC_thin_0.5/seed{0,1,2}`
- Configs: `revision_exp/configs/noise_full/p2_D18_noise_ATAC_thin_0.5_seed{0,1,2}.yaml`
- Tests: 29 passed, 13 warnings

Safe wording: “At 50% ATAC count retention, macro-F1 remained moderate, but assignment ARI was only 0.067–0.118 and size-tail behavior was strongly seed-dependent.”

Do not claim ATAC thinning robustness. The 25% and 75% levels remain in progress.
