# R2 Major 1 — D18 corrected full-data ADT-only combination

## Status and reviewer mapping

**PASS for seeds 0–2, with negative stability/size findings.** This completes the ADT-only arm of the seven-combination D18 grid for R2 Major 1. The full reviewer comment remains incomplete.

## Frozen experiment and exact results

Corrected D18 ADT, 25,517 cells; requested K=510; resolution approximately 0.02; 300 epochs; batch size 256; kNN k=5; seeds 0–2.

| seed | realized K | empty anchors | macro F1 | macro precision | macro recall | mean weighted purity | size median | size max | wall time | peak RSS |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0 | 498 | 12 | 0.565895 | 0.611146 | 0.549617 | 0.733375 | 45 | 930 | 29:28.77 | 1,443,408 KiB |
| 1 | 499 | 11 | 0.583902 | 0.607007 | 0.571868 | 0.809342 | 45 | 2899 | 33:51.40 | 1,462,860 KiB |
| 2 | 488 | 22 | 0.580291 | 0.648331 | 0.562520 | 0.777997 | 44 | 3096 | 33:17.62 | 1,446,892 KiB |

All runs completed with exit status 0. Empty anchors were frequent (11–22), and maximum metacell size varied sharply from 930 to more than 3,000 cells despite similar medians.

## Evidence

- Configs: `revision_exp/configs/modality_full/p2_D18_ADT_seed{0,1,2}.yaml`
- Server results: `/data/zhangpeiru/GARQ_revision/revision_results/phase2/02_modality/full/D18/ADT/seed{0,1,2}`
- Logs: `/data/zhangpeiru/GARQ_revision/revision_results/phase2/logs/P2_E7_D18_MODALITY_ADT_seed{0,1,2}.driver.log`

## Safe wording and prohibited claims

Safe wording: “ADT-only full-data aggregation completed across three seeds, but realized K and size tails were unstable, with 11–22 empty anchors and maxima of 930–3,096 cells.”

Do not claim ADT-only stability or uniformly bounded metacell size. Do not interpret the lower memory footprint as superior scientific performance. Cross-combination conclusions require the remaining paired and trimodal arms.
