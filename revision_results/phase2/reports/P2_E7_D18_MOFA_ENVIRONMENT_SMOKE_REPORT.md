# P2-E7 D18 MOFA+ environment smoke

Status: **PASS (environment smoke only; D18 biological fit not yet run)**  
Reviewer mapping: **R2 Major 4** and, for unified downstream settings, **R1 Major 5**.

## Exact environment

- Python 3.9.18
- mofapy2 0.7.2
- Environment: `/home/zhangpeiru/.conda/envs/mofa`
- `mofapy2.run.entry_point.entry_point` import: PASS

## Synthetic fit smoke

A deterministic two-view synthetic matrix (20 samples; 10 and 8 features; seed 0) was fitted for 10 iterations with two factors. Training completed and printed `SYNTHETIC_MOFA_SMOKE_PASS`; exit status was 0.

Evidence:

- `/data/zhangpeiru/GARQ_revision/revision_results/phase2/logs/P2_E7_D18_MOFA_environment_smoke.driver.log`
- `/data/zhangpeiru/GARQ_revision/revision_results/phase2/logs/P2_E7_D18_MOFA_environment_smoke.status`

## Scientific limitation

This result proves only that the frozen official MOFA+ environment can construct and train a multi-view model. It does not provide D18 factors, cross-method ARI/NMI/AMI/ACC, Balanced Accuracy, per-type metrics, held-out reproducibility, or GARQ-specific evidence.

Before the full D18 comparison, the following must be frozen identically for every assignment method: feature universe and filters per view, aggregation/normalization, factor count, view scaling, seed, convergence mode, maximum iterations, missing-data policy and downstream clustering/evaluation. These settings must not be chosen using method performance.

## What must not be claimed

- Do not report MOFA+ downstream results as complete.
- Do not use this synthetic smoke as biological evidence.
- Do not choose factor count or feature filters separately for GARQ and baselines.
