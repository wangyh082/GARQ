# P2-E7 D18 RNA–protein — GARQ seeds 0–2

## Status and reviewer mapping

**PASS for all three GARQ seeds after one seed-0 compatibility-equivalent retry.** These are descriptive full-feature runs for R2 Major 4. They are not confirmatory and do not complete the RNA–protein component because the other methods and feature-exclusion reruns remain outstanding.

## Experiment and exact findings

Corrected D18 GARQ seeds 0–2, 25,517 cells, realized K=497/493/486. Fifteen RNA–ADT pairs were mapped per seed. Metacell RNA was library-normalized/log1p; ADT was log1p/CLR. Pearson, Spearman, and Pearson correlation after residualizing dominant cell type were computed; partial-correlation intervals used 1,000 metacell bootstrap resamples with the assignment seed.

| seed | pair | Pearson r | Spearman rho | cell-type partial r | bootstrap 95% CI |
|---:|---|---:|---:|---:|---:|
| 0 | NCAM1–CD56 | 0.523144 | 0.299748 | 0.143487 | [0.044024, 0.243592] |
| 0 | CD8A–CD8a | 0.646730 | 0.599277 | 0.287028 | [0.191806, 0.377769] |
| 1 | NCAM1–CD56 | 0.637895 | 0.388807 | 0.324649 | [0.229866, 0.412468] |
| 1 | CD8A–CD8a | 0.627274 | 0.577749 | 0.249567 | [0.149509, 0.341562] |
| 2 | NCAM1–CD56 | 0.376471 | 0.199059 | 0.209477 | [0.105718, 0.315182] |
| 2 | CD8A–CD8a | 0.642266 | 0.533909 | 0.392820 | [0.305994, 0.469009] |

All 45 rows and all requested statistics were finite. Both prespecified pairs had positive partial correlations with bootstrap intervals above zero in all three seeds, although effect sizes varied materially.

## Preserved failure and retry

The initial run failed before correlation calculation because SciPy 1.11 removed string support from `stats.mode`. The original stderr is preserved at `/data/zhangpeiru/GARQ_revision/revision_results/phase2/logs/P2_E7_D18_RNAPROTEIN_GARQ_seed0.driver.log`. The retry used the equivalent unique-value count to choose the dominant label and changed no scientific setting. Accepted retry evidence: exit code 0, 15 complete pairs, both prespecified pairs present, and zero missing values.

## Evidence paths

- Workflow: `revision_exp/workflows/d18_rna_protein_benchmark.py`
- Exact rows: `revision_results/phase2/07_trimodal/rna_protein/GARQ_seed0_retry1.csv`, `GARQ_seed1.csv`, and `GARQ_seed2.csv`
- PASS log: `/data/zhangpeiru/GARQ_revision/revision_results/phase2/logs/P2_E7_D18_RNAPROTEIN_GARQ_seed0_retry1.driver.log`

## Safe wording and prohibited claims

Safe interim wording: “Across three descriptive GARQ aggregations, NCAM1–CD56 and CD8A–CD8a remained positively associated after controlling dominant cell type, with material seed-dependent effect-size variation.”

Do not call this held-out, causal, feature-excluded, or de-circularized evidence. The assignments used the full feature set; feature-exclusion reruns are required before a confirmatory reply.
