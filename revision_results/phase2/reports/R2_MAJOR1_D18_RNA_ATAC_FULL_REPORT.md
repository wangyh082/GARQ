# R2 Major 1 — D18 corrected full-data RNA+ATAC combination

## Status and reviewer mapping

**PASS for seeds 0–2.** This completes the RNA+ATAC arm of the D18 seven-combination grid for R2 Major 1. The remaining RNA+ADT, ATAC+ADT, and full trimodal arms are still required.

## Frozen experiment and exact results

Corrected D18 RNA+ATAC, 25,517 cells; requested K=510; resolution approximately 0.02; 300 epochs; batch size 256; kNN k=5; seeds 0–2.

| seed | realized K | empty anchors | macro F1 | macro precision | macro recall | mean weighted purity | size median | size max | wall time | peak RSS |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0 | 510 | 0 | 0.697015 | 0.720854 | 0.687114 | 0.865025 | 51 | 108 | 46:42.43 | 80,523,936 KiB |
| 1 | 509 | 1 | 0.695761 | 0.716143 | 0.688000 | 0.859371 | 52 | 121 | 49:05.19 | 80,523,716 KiB |
| 2 | 510 | 0 | 0.699044 | 0.725379 | 0.685729 | 0.870455 | 52 | 91 | 46:56.35 | 80,524,152 KiB |

All runs completed with exit status 0. Macro-F1 and weighted purity were stable, and maximum metacell size stayed between 91 and 121—substantially more controlled than the ATAC-only and ADT-only arms.

## Evidence

- Configs: `revision_exp/configs/modality_full/p2_D18_RNA_ATAC_seed{0,1,2}.yaml`
- Server results: `/data/zhangpeiru/GARQ_revision/revision_results/phase2/02_modality/full/D18/RNA_ATAC/seed{0,1,2}`
- Logs: `/data/zhangpeiru/GARQ_revision/revision_results/phase2/logs/P2_E7_D18_MODALITY_RNA_ATAC_seed{0,1,2}.driver.log`

## Safe wording and limitations

Safe wording: “The RNA+ATAC arm was stable across seeds and improved macro-F1 and size-tail control relative to either single-modality RNA or ATAC under the same requested K.”

Do not claim it is the optimal modality combination until all seven arms are complete. These label-based aggregation metrics also do not establish downstream peak–gene, TF–gene, RNA–protein, or held-out performance.
