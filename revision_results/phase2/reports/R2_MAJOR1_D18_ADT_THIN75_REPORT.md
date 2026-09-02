# R2 Major 1 — D18 corrected full-data ADT 75% retention

## Status and reviewer mapping

**PASS for seeds 0–2; assignment preservation was highly seed-dependent.** This experiment contributes to Reviewer 2 Major 1 and Reviewer 1 Major 2.

## Exact results

D18 full trimodal, 25,517 cells; ADT counts independently thinned at retention probability 0.75; requested K=510; 300 epochs; batch 256; kNN5.

| seed | K | empty | macro F1 | purity | median/max | ARI vs baseline | NMI | VI | wall | peak RSS |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0 | 501 | 9 | 0.696721 | 0.859307 | 48/1328 | 0.202611 | 0.561576 | 5.275554 | 47:36.04 | 80,550,828 KiB |
| 1 | 504 | 6 | 0.697306 | 0.871382 | 50/190 | 0.109298 | 0.579128 | 5.149456 | 46:57.04 | 80,550,472 KiB |
| 2 | 497 | 13 | 0.738161 | 0.833322 | 48/1260 | 0.334512 | 0.561152 | 5.210223 | 49:53.76 | 80,551,420 KiB |

ARI ranged from 0.109 to 0.335. Seeds 0 and 2 produced unusually long metacell-size tails (maximum 1,328 and 1,260), and seed 2 combined the highest ARI and macro F1 with the lowest purity. Thus the favorable seed-2 values do not establish consistent robustness.

## Evidence and limitations

- Results: `/data/zhangpeiru/GARQ_revision/revision_results/phase2/02_modality/noise_full_retry1/D18/ADT_thin_0.75/seed{0,1,2}`
- Configs: `revision_exp/configs/noise_full/p2_D18_noise_ADT_thin_0.75_seed{0,1,2}.yaml`
- Exact combined table: `revision_results/phase2/02_modality/d18_noise_full_summary.csv`
- Tests: 29 passed, 13 warnings

Safe wording: “With 75% ADT retention, assignment preservation varied substantially across seeds (ARI 0.109–0.335), and two seeds developed metacells exceeding 1,200 cells.”

Do not claim consistent ADT-noise robustness or select seed 2 as representative.
