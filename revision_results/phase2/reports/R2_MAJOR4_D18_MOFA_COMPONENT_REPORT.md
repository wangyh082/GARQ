# R2 Major 4 — D18 cross-method MOFA+ component

## Delivery status

**MOFA+ component PASS (12/12); full reviewer comment PARTIAL.** Corrected D18 assignments for GARQ, KMeans, MetaQ, and SEACells were evaluated for seeds 0–2 using one frozen MOFA+ and factor-space evaluator. Peak–gene, TF–gene, RNA–protein, and held-out/cross-fit analyses are still required before R2 Major 4 is reply-ready.

## Exact frozen settings

RNA top 2,000 dispersion features; ATAC top 5,000 prevalence features; all ADT features; aggregation by each method's metacells; RNA library-size normalization/log1p; ATAC TF-IDF/log1p; ADT CLR; per-feature z-scoring; mofapy2 0.7.2; 15 factors; MOFA seed 0; at most 1,000 iterations; `medium` convergence; `scale_views=true`; `scale_groups=false`; spike-slab weights, ARD factors, and ARD weights enabled. Factor evaluation used KMeans with `random_state=0`, `n_init=20` and dominant metacell cell type.

## Cross-method results

| method | passes | realized K | mean ARI | mean NMI | mean AMI | mean ACC | mean balanced accuracy |
|---|---:|---|---:|---:|---:|---:|---:|
| GARQ | 3/3 | 486–497 | 0.6232460651 | 0.7376680766 | 0.7281171685 | 0.7383351072 | 0.4969307766 |
| KMeans | 3/3 | 510 | 0.5626561491 | 0.7195122376 | 0.7081311948 | 0.6437908497 | 0.5768182210 |
| MetaQ | 3/3 | 505–517 | 0.5124648830 | 0.6516609816 | 0.6382598185 | 0.6487888935 | 0.4656980893 |
| SEACells | 3/3 | 510 | 0.6555794092 | 0.7888460173 | 0.7789325205 | 0.7450980392 | 0.6602889982 |

Favorable finding: GARQ exceeded KMeans and MetaQ in mean ARI/NMI/AMI/ACC. Negative finding: SEACells exceeded GARQ on every reported mean metric, and GARQ balanced accuracy was below KMeans. GARQ balanced accuracy was also unstable (0.3748–0.6394). Therefore these results do not support a broad GARQ-superiority claim.

## Failures and verification

The GARQ seed-0 workflow had two preserved compatibility failures: dense ADT aggregation and MOFA factor orientation. Both were corrected without changing data, features, model options, seed, or evaluator; the accepted retry had exit status 0 and a 497-by-15 factor matrix. All later runs passed directly. Server tests: `python -m pytest -q revision_exp/tests` = 28 passed, 13 warnings.

## Evidence

- Combined exact rows: `revision_results/phase2/07_trimodal/mofa_metrics.csv`
- Per-method reports: `P2_E7_D18_MOFA_GARQ_SEED0_REPORT.md`, `P2_E7_D18_MOFA_KMEANS_REPORT.md`, `P2_E7_D18_MOFA_METAQ_REPORT.md`, and `P2_E7_D18_MOFA_SEACELLS_REPORT.md`
- Server results: `/data/zhangpeiru/GARQ_revision/revision_results/phase2/07_trimodal/mofa/`
- Server logs: `/data/zhangpeiru/GARQ_revision/revision_results/phase2/logs/P2_E7_D18_MOFA_*.driver.log`

## Safe reply wording and prohibited claims

Safe partial wording: “Using identical frozen MOFA+ settings on matched-resolution corrected-D18 metacells, all 12 method/seed fits converged. GARQ improved mean factor-space ARI over KMeans and MetaQ, but SEACells achieved the highest mean scores; GARQ balanced accuracy was variable. We therefore do not claim universal downstream superiority.”

Do not present R2 Major 4 as fully answered. Do not claim that MOFA+ clustering proves regulatory coupling, trimodal necessity, peak–gene or TF–gene fidelity, RNA–protein concordance, or held-out reproducibility. Those planned experiments remain outstanding.
