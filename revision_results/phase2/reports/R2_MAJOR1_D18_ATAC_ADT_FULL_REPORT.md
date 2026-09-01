# R2 Major 1 — D18 corrected full-data ATAC+ADT combination

## Status and reviewer mapping

**PASS for seeds 0–2, with negative size-stability findings.** This completes the ATAC+ADT arm of the D18 seven-combination modality grid for Reviewer 2 Major 1. The full trimodal arm is still running, and the reviewer comment is not yet reply-ready because neighborhood/homogeneity and thinning/permutation evidence also remains incomplete.

## Frozen experiment and exact results

Corrected D18 ATAC+ADT, 25,517 cells; requested K=510; resolution approximately 0.02; 300 epochs; batch size 256; kNN k=5; seeds 0–2.

| seed | realized K | empty anchors | macro F1 | macro precision | macro recall | mean weighted purity | size median | size max | wall time | peak RSS |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0 | 489 | 21 | 0.649518 | 0.685509 | 0.639659 | 0.822611 | 44 | 1581 | 45:56.08 | 77,784,580 KiB |
| 1 | 491 | 19 | 0.673490 | 0.703229 | 0.658229 | 0.843875 | 44 | 1968 | 44:53.61 | 77,784,812 KiB |
| 2 | 494 | 16 | 0.663896 | 0.687180 | 0.653496 | 0.824617 | 42 | 2383 | 46:50.95 | 77,785,384 KiB |

All three runs completed with exit status 0 and realized K remained within 5% of requested K. However, 16–21 anchors were unused, maximum metacell size increased from 1,581 to 2,383 across seeds, and peak CPU RSS was approximately 74.2 GiB.

## Evidence

- Configs: `revision_exp/configs/modality_full/p2_D18_ATAC_ADT_seed{0,1,2}.yaml`
- Server results: `/data/zhangpeiru/GARQ_revision/revision_results/phase2/02_modality/full/D18/ATAC_ADT/seed{0,1,2}`
- Logs: `/data/zhangpeiru/GARQ_revision/revision_results/phase2/logs/P2_E7_D18_MODALITY_ATAC_ADT_seed{0,1,2}.driver.log`
- Status files: `/data/zhangpeiru/GARQ_revision/revision_results/phase2/logs/P2_E7_D18_MODALITY_ATAC_ADT_seed{0,1,2}.status`

## Safe wording and limitations

Safe wording: “ATAC+ADT completed reproducibly at approximately matched realized K and produced macro-F1 of 0.650–0.673, but retained 16–21 empty anchors and pronounced, seed-dependent long metacell-size tails.”

Do not claim that ATAC+ADT is optimal, uniformly stable, memory-efficient, or sufficient to answer Reviewer 2 Major 1. This arm is a label-based aggregation comparison; it does not replace the planned modality-specific neighborhood retention, homogeneity, thinning/permutation, or downstream held-out analyses.
