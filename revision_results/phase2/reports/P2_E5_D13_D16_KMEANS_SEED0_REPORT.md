# P2-E5 D13/D16 fixed-representation KMeans seed 0

## Status and reviewer mapping

**PASS for both datasets.** This is the KMeans seed-0 assignment prerequisite for the unified D13/D16 multi-batch MOFA+ comparison requested by Reviewer 1 Major 5. It does not complete the reviewer comment: GARQ, SEACells and MetaQ must be evaluated under the same batch workflow, and unified MOFA+ plus the global-versus-batch-stratified diagnostic remain pending.

## Frozen configuration

The preregistered fixed equal-weight representation was used: RNA PCA plus ADT CLR for D13, and RNA PCA plus ATAC LSI for D16. KMeans used seed 0 and the full corrected paired cell sets. Requested K was fixed from resolution K/n≈0.02, without label tuning: D13 K=3,235; D16 K=645. Labels were used only by the common post-assignment evaluator.

## Exact results

| dataset | cells | requested/realized K | empty clusters | median/mean/max size | size Gini | macro cell-type F1 |
|---|---:|---:|---:|---:|---:|---:|
| D13 GSE164378 RNA+ADT | 161,764 | 3,235/3,235 | 0 | 48/50.004/328 | 0.169624 | 0.865386 |
| D16 GSE140203 RNA+ATAC | 32,231 | 645/645 | 0 | 48/49.971/203 | 0.210309 | 0.793058 |

D16 Schwann Cell abundance was 0.005057 (163 cells). Its precision/recall/F1 was 0.7600/0.349693/0.478992. It occupied two dominant metacells; majority retention was 0.349693 and high-purity recovery was 0.011765. This is unfavorable for a strong rare-state preservation claim and must be retained in the comparison.

## Commands and evidence

Command pattern:

```text
conda run -n MetqQ2 python -m revision_exp.workflows.matched_baseline_fixed --dataset <D16|D13> --seed 0 --phase2-root revision_results/phase2
```

- Queue log: `/data/zhangpeiru/GARQ_revision/revision_results/phase2/logs/P2_E5_D16_D13_KMeans_seed0_queue.driver.log`
- D13 results: `/data/zhangpeiru/GARQ_revision/revision_results/phase2/01_size_resolution/D13/KMeans/full_seed0_K002/`
- D16 results: `/data/zhangpeiru/GARQ_revision/revision_results/phase2/01_size_resolution/D16/KMeans/full_seed0_K002/`
- Workflow: `revision_exp/workflows/matched_baseline_fixed.py`

Both runs produced complete 1:1 cell assignments, fixed-representation provenance, size summaries, per-type metrics and stage profiles. The queue exited after both commands completed; only deprecation/future warnings occurred, with no traceback.

## Scientific limitations and safe wording

These are seed-0 KMeans assignments, not MOFA+ integration results. D13 cell-type labels are numeric in the frozen input, so biological names must not be inferred. The current outputs also do not isolate global construction from batch-stratified construction.

Safe interim wording: “On the corrected full D13 and D16 inputs, the fixed-representation KMeans seed-0 controls completed at exactly the requested K. D16 Schwann-cell recall was 0.350 (F1 0.479), so the control does not support uniformly strong rare-state retention. Unified cross-method MOFA+ and batch-workflow sensitivity remain in progress.”

