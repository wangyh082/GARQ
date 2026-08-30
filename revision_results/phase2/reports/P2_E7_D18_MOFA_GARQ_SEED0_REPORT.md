# P2-E7 D18 MOFA+ — GARQ seed 0

## Status and reviewer mapping

**PASS after two compatibility-equivalent retries.** This is one completed run within the D18 cross-method MOFA+ evidence requested for the trimodal reviewer comment. The reviewer comment is not reply-ready until the remaining methods and seeds are run under the same frozen settings.

## Frozen experiment

- Dataset: corrected D18, 25,517 cells.
- Assignment: GARQ seed 0, realized K = 497.
- Views: RNA top 2,000 dispersion features; ATAC top 5,000 prevalence features; all ADT features.
- Preprocessing: metacell aggregation; RNA library-size normalization plus log1p; ATAC TF-IDF plus log1p; ADT CLR; feature z-scoring.
- MOFA+: mofapy2 0.7.2; 15 factors; MOFA seed 0; maximum 1,000 iterations; convergence mode `medium`; `scale_views=true`; `scale_groups=false`; spike-slab weights, ARD factors, and ARD weights enabled.
- Common evaluation: KMeans (`random_state=0`, `n_init=20`) on MOFA factors against dominant metacell cell type.

## Exact result

| status | ARI | NMI | AMI | ACC | balanced accuracy | wall time | peak RSS |
|---|---:|---:|---:|---:|---:|---:|---:|
| PASS | 0.6534031714 | 0.7470417197 | 0.7379512035 | 0.7464788732 | 0.4765117726 | 44.08 s | 2,589,492 KiB |

MOFA converged at iteration 91. There were 10 dominant cell-type classes.

## Preserved failures and resolution

1. Initial attempt failed while aggregating dense ADT because the workflow assumed sparse output (`numpy.ndarray` has no `toarray`). This was an engineering compatibility error; the retry accepted sparse or dense matrix products without changing values or scientific settings.
2. Retry 1 fitted and saved the MOFA model, then failed during evaluation because the returned factor matrix was already sample-by-factor and was transposed to 15-by-497. This was an engineering orientation error; retry 2 selected orientation by the independently known realized K and added a hard dimension check. No model or benchmark setting changed.

Acceptance evidence for retry 2: exit status 0, 497 factor rows matching 497 metacells, complete metric/settings/summary files, and a converged MOFA fit. Earlier stderr and partial outputs remain in their original independent directories and logs.

## Evidence paths

- Workflow: `revision_exp/workflows/d18_mofa_benchmark.py`
- PASS directory: `/data/zhangpeiru/GARQ_revision/revision_results/phase2/07_trimodal/mofa/GARQ/seed0_retry2`
- PASS log: `/data/zhangpeiru/GARQ_revision/revision_results/phase2/logs/P2_E7_D18_MOFA_GARQ_seed0_retry2.driver.log`
- Initial failure log: `/data/zhangpeiru/GARQ_revision/revision_results/phase2/logs/P2_E7_D18_MOFA_GARQ_seed0.driver.log`
- Retry-1 failure log: `/data/zhangpeiru/GARQ_revision/revision_results/phase2/logs/P2_E7_D18_MOFA_GARQ_seed0_retry1.driver.log`
- Small local artifacts: `phase2_reports/07_trimodal/mofa/GARQ/seed0_retry2/`

## Scientific limitations and safe wording

Safe interim wording: “For corrected D18 GARQ seed 0, the frozen 15-factor MOFA+ analysis converged and produced ARI 0.6534 and balanced accuracy 0.4765 against dominant metacell cell type.”

Do not claim cross-method superiority, robustness across seeds, or completion of the D18 MOFA+ reviewer response. This is one of twelve planned method/seed runs and uses dominant metacell labels only for evaluation and downstream factor clustering, not for MOFA training.
