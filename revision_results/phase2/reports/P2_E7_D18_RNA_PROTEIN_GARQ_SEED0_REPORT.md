# P2-E7 D18 RNA–protein — GARQ seed 0

## Status and reviewer mapping

**PASS after one compatibility-equivalent retry.** This is one descriptive full-feature run for R2 Major 4. It is not confirmatory and does not complete the RNA–protein component because the other seeds/methods and feature-exclusion reruns remain outstanding.

## Experiment and exact findings

Corrected D18 GARQ seed 0, 25,517 cells, realized K=497. Fifteen RNA–ADT pairs were mapped. Metacell RNA was library-normalized/log1p; ADT was log1p/CLR. Pearson, Spearman, and Pearson correlation after residualizing dominant cell type were computed; partial-correlation intervals used 1,000 metacell bootstrap resamples with seed 0.

| pair | Pearson r | Spearman rho | cell-type partial r | bootstrap 95% CI |
|---|---:|---:|---:|---:|
| NCAM1–CD56 | 0.523144 | 0.299748 | 0.143487 | [0.044024, 0.243592] |
| CD8A–CD8a | 0.646730 | 0.599277 | 0.287028 | [0.191806, 0.377769] |

All 15 rows and all requested statistics were finite. Both prespecified pairs had positive partial correlations with bootstrap intervals above zero.

## Preserved failure and retry

The initial run failed before correlation calculation because SciPy 1.11 removed string support from `stats.mode`. The original stderr is preserved at `/data/zhangpeiru/GARQ_revision/revision_results/phase2/logs/P2_E7_D18_RNAPROTEIN_GARQ_seed0.driver.log`. The retry used the equivalent unique-value count to choose the dominant label and changed no scientific setting. Accepted retry evidence: exit code 0, 15 complete pairs, both prespecified pairs present, and zero missing values.

## Evidence paths

- Workflow: `revision_exp/workflows/d18_rna_protein_benchmark.py`
- Exact rows: `revision_results/phase2/07_trimodal/rna_protein/GARQ_seed0_retry1.csv`
- PASS log: `/data/zhangpeiru/GARQ_revision/revision_results/phase2/logs/P2_E7_D18_RNAPROTEIN_GARQ_seed0_retry1.driver.log`

## Safe wording and prohibited claims

Safe interim wording: “In a descriptive GARQ seed-0 aggregation, NCAM1–CD56 and CD8A–CD8a remained positively associated after controlling dominant cell type.”

Do not call this held-out, causal, feature-excluded, or de-circularized evidence. The assignments used the full feature set; feature-exclusion reruns are required before a confirmatory reply.
