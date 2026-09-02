# D18 matched-method MOFA+ and RNA–protein evidence

## Status and reviewer mapping

**PASS:** MOFA+ 12/12 runs and RNA–protein 12/12 runs. This is a completed evidence unit for the D18 downstream portions of Reviewer 2 and the GARQ-specific downstream claim. It is not the complete D18 reviewer response because peak–gene, TF–gene, and feature-exclusion/cross-fitting analyses remain missing.

## Common design

The same corrected D18 cells and matched-realized-K assignments were used for GARQ, KMeans, MetaQ, and SEACells at seeds 0–2. MOFA+ used 2,000 RNA features, 5,000 ATAC features, all ADT features, 15 factors, fixed MOFA seed 0, at most 1,000 iterations, medium convergence, view scaling on, group scaling off, spike-and-slab weights on, and ARD for factors and weights. Assignment seed varies; the MOFA seed is intentionally fixed to isolate assignment variation.

## MOFA+ exact results

| method | mean ARI (range) | mean NMI | mean AMI | mean ACC | mean balanced accuracy |
|---|---:|---:|---:|---:|---:|
| GARQ | 0.6232 (0.5886–0.6534) | 0.7377 | 0.7281 | 0.7383 | 0.4969 |
| KMeans | 0.5627 (0.5043–0.6137) | 0.7195 | 0.7081 | 0.6438 | 0.5768 |
| MetaQ | 0.5125 (0.4245–0.6107) | 0.6517 | 0.6383 | 0.6488 | 0.4657 |
| SEACells | 0.6556 (0.6398–0.6705) | 0.7888 | 0.7789 | 0.7451 | 0.6603 |

SEACells exceeded GARQ on the mean of all five reported MOFA-derived label metrics. GARQ exceeded KMeans and MetaQ in mean ARI/NMI/AMI/ACC, but not KMeans in balanced accuracy. These descriptive three-seed results do not justify a GARQ-superiority claim.

## RNA–protein exact findings

Fifteen mapped RNA–ADT pairs were evaluated per method and seed using Pearson, Spearman, and cell-type-adjusted partial Pearson correlation with bootstrap intervals. For the two prespecified pairs, the mean partial correlations were:

| pair | GARQ | KMeans | MetaQ | SEACells |
|---|---:|---:|---:|---:|
| CD8A–CD8a | 0.3098 | 0.2677 | 0.3308 | 0.2973 |
| NCAM1–CD56 | 0.2259 | 0.2614 | 0.3452 | 0.3470 |

All seed-level bootstrap intervals for these two pairs were above zero. Across the full panel, performance was pair-dependent: for example, mean partial correlation for FCGR3A–CD16 was 0.1881/0.2345/0.2710/0.3993 for GARQ/KMeans/MetaQ/SEACells. The tested features were not excluded during metacell construction, so these are descriptive, potentially circular association results rather than held-out validation.

## Safe reply wording

> Using identical corrected D18 inputs, matched-realized-K assignments, and a fixed 15-factor MOFA+ configuration, we compared GARQ with KMeans, MetaQ, and SEACells across three assignment seeds. GARQ produced useful integrated factors but was not uniformly best; SEACells had the highest mean MOFA label metrics. RNA–protein correlations were reproducible for the prespecified CD8A–CD8a and NCAM1–CD56 pairs, but relative performance was method- and pair-dependent. We therefore avoid claiming a GARQ-specific downstream advantage from these analyses alone.

## Failures, limitations, and prohibited claims

- GARQ MOFA seed0 attempts 0 and retry1 failed; stderr/logs and partial `model.hdf5` are preserved. Retry2 passed after compatibility-equivalent output handling; the successful metrics are used.
- Do not claim GARQ is superior to all matched methods: SEACells had higher mean MOFA metrics.
- Do not call the RNA–protein results held-out or non-circular; feature-exclusion remains required.
- Do not treat this unit as completing peak–gene, TF–gene, odd/even cross-fitting, or the full Reviewer 2 downstream request.
- Three assignment seeds quantify seed variation, while the fixed MOFA seed deliberately does not quantify MOFA initialization variance.

## Evidence and commands

- Combined MOFA table: `revision_results/phase2/07_trimodal/d18_mofa_metrics.csv`
- RNA–protein run tables: `revision_results/phase2/07_trimodal/rna_protein/*.csv`
- Workflows: `revision_exp/workflows/d18_mofa_benchmark.py`, `revision_exp/workflows/d18_rna_protein_benchmark.py`
- Server outputs: `/data/zhangpeiru/GARQ_revision/revision_results/phase2/07_trimodal`
- Logs: `/data/zhangpeiru/GARQ_revision/revision_results/phase2/logs/P2_E7_D18_MOFA_*`
- MOFA command pattern: `/home/zhangpeiru/.conda/envs/MetqQ2/bin/python -m revision_exp.workflows.d18_mofa_benchmark --method <METHOD> --seed <SEED>`
- Test requirement before delivery: `/home/zhangpeiru/.conda/envs/MetqQ2/bin/python -m pytest -q revision_exp/tests`.
