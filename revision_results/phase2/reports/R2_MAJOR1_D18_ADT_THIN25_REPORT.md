# R2 Major 1 — D18 corrected full-data ADT 25% retention

## Status and reviewer mapping

**PASS for seeds 0–2; stable aggregate metrics but low assignment preservation.** This supports Reviewer 2 Major 1 and Reviewer 1 Major 2.

## Exact results

D18 full trimodal, 25,517 cells; ADT counts independently thinned at retention probability 0.25; requested K=510; 300 epochs; batch 256; kNN5.

| seed | K | empty | macro F1 | purity | median/max | ARI vs baseline | NMI | VI | wall | peak RSS |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0 | 510 | 0 | 0.695955 | 0.859148 | 51/123 | 0.091174 | 0.552600 | 5.470609 | 45:27.96 | 80,549,108 KiB |
| 1 | 510 | 0 | 0.702029 | 0.870197 | 52/101 | 0.087346 | 0.553927 | 5.479794 | 48:51.83 | 80,550,436 KiB |
| 2 | 507 | 3 | 0.701299 | 0.868369 | 52/106 | 0.077607 | 0.553587 | 5.396163 | 45:42.54 | 80,549,228 KiB |

Label metrics and size summaries were stable, but same-seed assignment ARI was only 0.078–0.091.

## Evidence and limitations

- Results: `/data/zhangpeiru/GARQ_revision/revision_results/phase2/02_modality/noise_full_retry1/D18/ADT_thin_0.25/seed{0,1,2}`
- Configs: `revision_exp/configs/noise_full/p2_D18_noise_ADT_thin_0.25_seed{0,1,2}.yaml`
- Tests: 29 passed, 13 warnings

Safe wording: “At 25% ADT count retention, aggregate label and size metrics remained stable, while metacell membership was poorly preserved (ARI 0.078–0.091).”

Do not equate aggregate stability with assignment robustness.
