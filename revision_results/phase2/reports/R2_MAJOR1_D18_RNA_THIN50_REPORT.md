# R2 Major 1 — D18 corrected full-data RNA 50% thinning

## Status and reviewer mapping

**PASS for seeds 0–2; mixed label metrics and poor assignment stability.** This count-level perturbation condition supports Reviewer 2 Major 1 and Reviewer 1 Major 2.

## Exact results

D18 full trimodal input, 25,517 cells; RNA counts thinned by independent Binomial(count, 0.5), ATAC/ADT unchanged; requested K=510; resolution approximately 0.02; 300 epochs; batch 256; kNN5.

| seed | K | empty | macro F1 | precision | recall | purity | median/max | ARI vs baseline | NMI | VI | wall | peak RSS |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0 | 500 | 10 | 0.714587 | 0.754933 | 0.694703 | 0.823564 | 47/742 | 0.116553 | 0.513069 | 5.875894 | 46:13.28 | 80,805,052 KiB |
| 1 | 496 | 14 | 0.685104 | 0.714723 | 0.669052 | 0.857667 | 47/1268 | 0.057747 | 0.513177 | 5.817540 | 46:45.02 | 80,831,172 KiB |
| 2 | 501 | 9 | 0.670653 | 0.712566 | 0.648184 | 0.855079 | 46/1617 | 0.073579 | 0.510348 | 5.762143 | 45:51.33 | 80,831,892 KiB |

Macro-F1 was favorable in seed 0 but declined across seeds, while maximum metacell size increased to 1,617. Same-seed assignment ARI was only 0.058–0.117. Thus label-level performance and assignment stability give materially different impressions.

## Evidence and limitations

- Results: `/data/zhangpeiru/GARQ_revision/revision_results/phase2/02_modality/noise_full_retry1/D18/RNA_thin_0.5/seed{0,1,2}`
- Configs: `revision_exp/configs/noise_full/p2_D18_noise_RNA_thin_0.5_seed{0,1,2}.yaml`
- Tests: 29 passed, 13 warnings

Safe wording: “With 50% RNA count retention, label-level macro-F1 was mixed across seeds and metacell membership was poorly preserved (ARI 0.058–0.117), with increasingly long size tails.”

Do not claim robustness based on seed 0 alone. The 25% and 75% retention levels and ATAC/ADT thinning remain in progress.
