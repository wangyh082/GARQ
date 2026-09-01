# R2 Major 1 — D18 corrected full-data ATAC cell permutation

## Status and reviewer mapping

**PASS for corrected retry1 seeds 0–2; negative for strong perturbation robustness.** This condition supports Reviewer 2 Major 1 and Reviewer 1 Major 2. It uses the verified full-data perturbation materialization fix documented in the RNA-permutation report.

## Frozen experiment and exact results

D18 RNA+ATAC+ADT, 25,517 cells; ATAC rows permuted while RNA/ADT and cell identifiers remain fixed; requested K=510; resolution approximately 0.02; 300 epochs; batch 256; kNN5.

| seed | K | empty | macro F1 | precision | recall | purity | median/max size | ARI vs baseline | NMI | VI (nats) | wall | peak RSS |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0 | 509 | 1 | 0.667947 | 0.704867 | 0.652197 | 0.845840 | 52/101 | 0.041378 | 0.480182 | 6.347042 | 46:52.96 | 80,992,676 KiB |
| 1 | 509 | 1 | 0.668203 | 0.699043 | 0.653949 | 0.838852 | 51/161 | 0.037323 | 0.484469 | 6.335612 | 45:50.15 | 80,991,464 KiB |
| 2 | 510 | 0 | 0.643566 | 0.660239 | 0.638005 | 0.792287 | 51/115 | 0.040595 | 0.476310 | 6.335458 | 45:25.08 | 80,992,988 KiB |

All provenance records confirm full-data ATAC permutation and assignments differ from their same-seed baselines. Label-level macro-F1 remained 0.644–0.668, but assignment ARI was only 0.037–0.041. Seed 2 also showed lower purity than seeds 0/1.

## Evidence and limitations

- Results: `/data/zhangpeiru/GARQ_revision/revision_results/phase2/02_modality/noise_full_retry1/D18/ATAC_cell_permutation/seed{0,1,2}`
- Configs: `revision_exp/configs/noise_full/p2_D18_noise_ATAC_cell_permutation_seed{0,1,2}.yaml`
- Logs: `/data/zhangpeiru/GARQ_revision/revision_results/phase2/logs/p2_D18_noise_ATAC_cell_permutation_seed{0,1,2}.driver.log`
- Tests: 29 passed, 13 warnings

Safe wording: “ATAC permutation preserved moderate label-level macro-F1 but reorganized metacell membership almost completely (ARI 0.037–0.041), with additional purity loss in one seed.”

Do not claim robustness to ATAC corruption. Cell permutation is a destructive negative control, not a realistic measurement-noise model. ADT permutation and count-thinning levels remain in progress.
