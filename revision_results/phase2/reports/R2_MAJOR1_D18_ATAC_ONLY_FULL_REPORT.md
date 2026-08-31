# R2 Major 1 — D18 corrected full-data ATAC-only combination

## Status and reviewer mapping

**PASS for seeds 0–2, with materially negative findings.** This completes the ATAC-only arm of the D18 seven-combination grid for R2 Major 1. The full comment remains incomplete.

## Frozen experiment and exact results

Corrected D18 ATAC, 25,517 cells; requested K=510; resolution approximately 0.02; 300 epochs; batch size 256; kNN k=5; seeds 0–2.

| seed | realized K | empty anchors | macro F1 | macro precision | macro recall | mean weighted purity | size median | size max | wall time | peak RSS |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0 | 509 | 1 | 0.474450 | 0.508461 | 0.467123 | 0.762691 | 31 | 3260 | 40:26.78 | 77,782,724 KiB |
| 1 | 507 | 3 | 0.468828 | 0.491491 | 0.462799 | 0.737237 | 33 | 3080 | 41:41.12 | 77,785,028 KiB |
| 2 | 506 | 4 | 0.512340 | 0.586124 | 0.516639 | 0.703348 | 31.5 | 2741 | 43:23.13 | 77,785,472 KiB |

All runs completed with exit status 0. Realized K decreased from 509 to 506 as empty anchors increased. Every seed produced an extreme size tail (maximum 2,741–3,260 cells), while macro-F1 remained 0.469–0.512.

## Evidence

- Configs: `revision_exp/configs/modality_full/p2_D18_ATAC_seed{0,1,2}.yaml`
- Server results: `/data/zhangpeiru/GARQ_revision/revision_results/phase2/02_modality/full/D18/ATAC/seed{0,1,2}`
- Logs: `/data/zhangpeiru/GARQ_revision/revision_results/phase2/logs/P2_E7_D18_MODALITY_ATAC_seed{0,1,2}.driver.log`

## Safe wording and prohibited claims

Safe wording: “ATAC-only full-data aggregation completed across three seeds but showed lower macro-F1 and severe metacell-size tails, arguing against ATAC-only sufficiency under this configuration.”

Do not hide the empty anchors or size maxima. Do not infer that ATAC is biologically uninformative: these results concern this method/configuration and evaluator, and the remaining modality combinations are needed for attribution.
