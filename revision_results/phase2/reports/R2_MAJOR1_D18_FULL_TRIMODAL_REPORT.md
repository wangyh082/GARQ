# R2 Major 1 — D18 corrected full-data RNA+ATAC+ADT combination

## Status and reviewer mapping

**PASS for seeds 0–2, with mixed size-tail stability.** This completes the full trimodal arm and therefore all 21 runs in the seven-combination D18 modality grid for Reviewer 2 Major 1. The reviewer comment is not yet fully reply-ready because modality-specific neighborhood/homogeneity and thinning/permutation evidence remains incomplete.

## Frozen experiment and exact results

Corrected D18 RNA+ATAC+ADT, 25,517 cells; requested K=510; resolution approximately 0.02; 300 epochs; batch size 256; kNN k=5; seeds 0–2.

| seed | realized K | empty anchors | macro F1 | macro precision | macro recall | mean weighted purity | size median | size max | wall time | peak RSS |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0 | 497 | 13 | 0.683585 | 0.708952 | 0.670394 | 0.850743 | 49 | 572 | 50:42.49 | 80,523,536 KiB |
| 1 | 493 | 17 | 0.693848 | 0.711756 | 0.689063 | 0.854107 | 49 | 147 | 47:25.31 | 80,524,464 KiB |
| 2 | 486 | 24 | 0.681357 | 0.721383 | 0.661537 | 0.865660 | 47 | 988 | 45:00.78 | 80,524,224 KiB |

All runs completed with exit status 0. Realized K was 486–497, within 5% of requested K. Macro-F1 was comparatively stable (0.681–0.694), while empty anchors increased from 13 to 24 and maximum metacell size varied substantially from 147 to 988.

## Evidence and verification

- Configs: `revision_exp/configs/modality_full/p2_D18_RNA_ATAC_ADT_seed{0,1,2}.yaml`
- Server results: `/data/zhangpeiru/GARQ_revision/revision_results/phase2/02_modality/full/D18/RNA_ATAC_ADT/seed{0,1,2}`
- Logs: `/data/zhangpeiru/GARQ_revision/revision_results/phase2/logs/P2_E7_D18_MODALITY_RNA_ATAC_ADT_seed{0,1,2}.driver.log`
- Status files: `/data/zhangpeiru/GARQ_revision/revision_results/phase2/logs/P2_E7_D18_MODALITY_RNA_ATAC_ADT_seed{0,1,2}.status`, each exit status 0
- Standard test command: `/home/zhangpeiru/.conda/envs/MetqQ2/bin/python -m pytest -q revision_exp/tests`

## Safe wording and limitations

Safe wording: “The full trimodal configuration completed across three seeds at approximately matched realized K, with macro-F1 of 0.681–0.694 and weighted purity of 0.851–0.866; however, empty-anchor counts and the upper size tail remained seed-dependent.”

Do not claim that full trimodal input is necessary, uniformly stable, or superior for all outcomes. These are label-based aggregation metrics and do not substitute for the planned neighborhood retention, homogeneity, perturbation, and held-out downstream comparisons. In particular, RNA+ATAC produced slightly higher macro-F1 in the already completed arm, so the present evidence does not support automatic full-trimodal optimality.
