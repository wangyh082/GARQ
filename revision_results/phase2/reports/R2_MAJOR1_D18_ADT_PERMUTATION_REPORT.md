# R2 Major 1 — D18 corrected full-data ADT cell permutation

## Status and reviewer mapping

**PASS for corrected retry1 seeds 0–2; negative for strong perturbation robustness.** This condition supports Reviewer 2 Major 1 and Reviewer 1 Major 2.

## Exact results

D18 RNA+ATAC+ADT, 25,517 cells; ADT rows permuted while RNA/ATAC and identifiers remain fixed; requested K=510; resolution approximately 0.02; 300 epochs; batch 256; kNN5.

| seed | K | empty | macro F1 | purity | median/max size | ARI vs baseline | NMI | VI (nats) | wall | peak RSS |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0 | 510 | 0 | 0.683527 | 0.843299 | 49/97 | 0.064103 | 0.520059 | 5.874379 | 45:49.82 | 80,535,136 KiB |
| 1 | 509 | 1 | 0.684101 | 0.847537 | 50/111 | 0.060845 | 0.519838 | 5.908180 | 50:06.01 | 80,535,072 KiB |
| 2 | 505 | 5 | 0.660503 | 0.812739 | 50/203 | 0.062671 | 0.517594 | 5.826662 | 46:06.94 | 80,534,172 KiB |

All provenance records confirm full-data ADT permutation. Assignment sensitivity was slightly weaker than for RNA/ATAC permutation, but ARI remained only 0.061–0.064; seed 2 also had lower purity and a longer size tail.

## Evidence and limitations

- Results: `/data/zhangpeiru/GARQ_revision/revision_results/phase2/02_modality/noise_full_retry1/D18/ADT_cell_permutation/seed{0,1,2}`
- Configs: `revision_exp/configs/noise_full/p2_D18_noise_ADT_cell_permutation_seed{0,1,2}.yaml`
- Tests: 29 passed, 13 warnings

Safe wording: “ADT permutation produced a nearly complete metacell-membership reorganization (ARI 0.061–0.064) despite moderate label-level macro-F1.”

Do not claim robustness to ADT corruption. Permutation is a destructive negative control; count-thinning conditions remain in progress.
