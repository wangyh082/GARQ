# R2 Major 1 — D18 corrected full-data RNA-only combination

## Status and reviewer mapping

**PASS for seeds 0–2.** This completes the RNA-only arm of the seven-combination D18 full-data grid for R2 Major 1 (also supports R1 Major 2). The reviewer comment remains incomplete while the other modality combinations and neighborhood/perturbation analyses are running.

## Frozen experiment

Corrected D18 RNA, 25,517 cells; requested K=510 (resolution approximately 0.02); GARQ instrumented legacy implementation; 300 epochs; batch size 256; kNN k=5; seeds 0–2; deterministic warning mode; one job per GPU.

| seed | realized K | empty anchors | macro F1 | macro precision | macro recall | mean weighted purity | size median | size max | wall time | peak RSS |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0 | 510 | 0 | 0.639872 | 0.645508 | 0.643378 | 0.774610 | 49 | 385 | 35:42.56 | 11,390,368 KiB |
| 1 | 509 | 1 | 0.641290 | 0.668300 | 0.627721 | 0.801960 | 48 | 573 | 38:05.47 | 11,390,204 KiB |
| 2 | 510 | 0 | 0.630941 | 0.635119 | 0.664161 | 0.762143 | 47 | 440 | 30:20.64 | 11,387,940 KiB |

All runs completed 300 epochs with exit status 0. Seed 1 emitted the preserved legacy empty-slice warning because one requested anchor was unused; its 25,517 assignments and 509 realized metacells remained complete.

## Evidence

- Configs: `revision_exp/configs/modality_full/p2_D18_RNA_seed{0,1,2}.yaml`
- Server results: `/data/zhangpeiru/GARQ_revision/revision_results/phase2/02_modality/full/D18/RNA/seed{0,1,2}`
- Logs: `/data/zhangpeiru/GARQ_revision/revision_results/phase2/logs/P2_E7_D18_MODALITY_RNA_seed{0,1,2}.driver.log`

## Safe wording and limitations

Safe interim wording: “The corrected full-data RNA-only arm completed across three seeds with realized K 509–510 and macro-F1 0.6309–0.6413.”

Do not claim RNA-only is optimal or that full trimodal input is necessary/unnecessary until all seven combinations are complete. The maximum metacell size varied from 385 to 573, and the seed-1 empty-anchor warning must remain disclosed.
