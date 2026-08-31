# R2 Major 1 — D18 corrected full-data RNA+ADT combination

## Status and reviewer mapping

**PASS for seeds 0–2, with mixed stability findings.** This completes the RNA+ADT arm of the D18 seven-combination grid for R2 Major 1. ATAC+ADT and full trimodal arms remain outstanding.

## Frozen experiment and exact results

Corrected D18 RNA+ADT, 25,517 cells; requested K=510; resolution approximately 0.02; 300 epochs; batch size 256; kNN k=5; seeds 0–2.

| seed | realized K | empty anchors | macro F1 | macro precision | macro recall | mean weighted purity | size median | size max | wall time | peak RSS |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0 | 503 | 7 | 0.666923 | 0.791661 | 0.640809 | 0.863630 | 46 | 1107 | 36:09.83 | 11,391,040 KiB |
| 1 | 504 | 6 | 0.677586 | 0.715190 | 0.656870 | 0.858228 | 45 | 1830 | 40:56.90 | 11,390,972 KiB |
| 2 | 503 | 7 | 0.624396 | 0.642228 | 0.617528 | 0.856303 | 46 | 1822 | 43:39.00 | 11,390,648 KiB |

All runs completed with exit status 0. Weighted purity was stable, but macro-F1 varied by more than 0.05 and maximum metacell size ranged from 1,107 to 1,830. Six to seven requested anchors were unused in every seed.

## Evidence

- Configs: `revision_exp/configs/modality_full/p2_D18_RNA_ADT_seed{0,1,2}.yaml`
- Server results: `/data/zhangpeiru/GARQ_revision/revision_results/phase2/02_modality/full/D18/RNA_ADT/seed{0,1,2}`
- Logs: `/data/zhangpeiru/GARQ_revision/revision_results/phase2/logs/P2_E7_D18_MODALITY_RNA_ADT_seed{0,1,2}.driver.log`

## Safe wording and limitations

Safe wording: “RNA+ADT improved label-based aggregation metrics over either single-modality RNA or ADT on average, but showed seed-dependent macro-F1 and long size tails.”

Do not claim RNA+ADT stability or optimality. In particular, the high seed-0 macro precision did not reproduce at seed 2, and all seeds retained empty anchors and metacells exceeding 1,000 cells.
