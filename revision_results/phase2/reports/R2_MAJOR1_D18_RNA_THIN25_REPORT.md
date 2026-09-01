# R2 Major 1 — D18 corrected full-data RNA 25% retention

## Status and reviewer mapping

**PASS for seeds 0–2; highly seed-dependent assignment and size stability.** This count-level condition supports Reviewer 2 Major 1 and Reviewer 1 Major 2.

## Exact results

D18 full trimodal, 25,517 cells; RNA counts independently thinned at retention probability 0.25; requested K=510; 300 epochs; batch 256; kNN5.

| seed | K | empty | macro F1 | purity | median/max | ARI vs baseline | NMI | VI | wall | peak RSS |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0 | 487 | 23 | 0.731705 | 0.822556 | 46/3126 | 0.039989 | 0.500892 | 5.733828 | 46:10.49 | 80,915,996 KiB |
| 1 | 494 | 16 | 0.670937 | 0.816336 | 48/1044 | 0.066167 | 0.515097 | 5.815587 | 48:06.73 | 80,918,720 KiB |
| 2 | 489 | 21 | 0.694906 | 0.874080 | 47/1232 | 0.302428 | 0.507770 | 5.799854 | 45:23.01 | 80,869,200 KiB |

Seed 0 had the highest macro-F1 but the lowest ARI and an extreme 3,126-cell metacell. Seed 2 had substantially higher ARI, demonstrating that assignment sensitivity is not reproducible across seeds.

## Evidence and limitations

- Results: `/data/zhangpeiru/GARQ_revision/revision_results/phase2/02_modality/noise_full_retry1/D18/RNA_thin_0.25/seed{0,1,2}`
- Configs: `revision_exp/configs/noise_full/p2_D18_noise_RNA_thin_0.25_seed{0,1,2}.yaml`
- Tests: 29 passed, 13 warnings

Safe wording: “At 25% RNA retention, label-level metrics, assignment ARI, and size tails varied strongly across seeds; the most favorable macro-F1 coincided with the least stable assignment and an extreme size outlier.”

Do not report the seed-0 F1 as robustness evidence or average away the large seed heterogeneity.
