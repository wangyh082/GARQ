# D13 full-length scaling series

## Status and reviewer mapping

**PASS for all five planned sizes:** 10k, 25k, 50k, 100k, and full 161,764 cells, each with seed 0 and 300 epochs. This directly addresses Reviewer 1 Major 3 and Reviewer 2 Major 5 on implementation-level scaling and CPU/GPU memory. It does not establish broad scalability across datasets or batch-size/order stability.

## Exact results

| cells | requested/realized K | empty anchors | median/max size | Gini | wall | peak CPU RSS | peak GPU allocated/reserved |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 10,000 | 200/200 | 0 | 54/77 | 0.149 | 18.1 min | 13.3 GiB | 0.23/0.30 GiB |
| 25,000 | 500/472 | 28 | 48/821 | 0.261 | 42.0 min | 32.0 GiB | 0.22/0.30 GiB |
| 50,000 | 1,000/762 | 238 | 29/1,782 | 0.670 | 85.1 min | 63.2 GiB | 0.21/0.30 GiB |
| 100,000 | 2,000/1,999 | 1 | 54/76 | 0.146 | 70.5 min | 125.7 GiB | 5.19/7.07 GiB |
| 161,764 | 3,235/3,234 | 1 | 52/74 | 0.107 | 119.0 min | 202.9 GiB | 5.25/7.13 GiB |

Peak CPU RSS rose from 14,239,342,592 to 217,792,278,528 bytes and was dominated by legacy loading/preprocessing. GPU reserved memory remained below 0.33 GiB through 50k, then rose to about 7.1 GiB at 100k/full. Wall time and memory do not form a perfectly monotonic series because subset materialization, paging/cache state, initialization size, and downstream aggregation differ.

The 25k and especially 50k conditions showed severe seed-specific size-tail degradation, while 100k/full returned to nearly complete realized K and balanced sizes. Thus neither a monotonic-quality claim nor a monotonic-degradation claim is supported. This non-monotonicity is itself an important stability limitation and requires more seeds before mechanistic interpretation.

## Failures and compatibility disclosure

The first full configuration exited in 3.33 seconds because the scientific classification string `diagnostic_large_sample_initialization` was supplied as `implementation_tag`, which the runtime whitelist rejects. The independent failure log and status are preserved. Retry1 used the legal runtime tag `instrumented_legacy` while retaining the large-K scientific classification in comments/reporting; data, K, seed, epochs, and evaluator were unchanged.

The released initializer used only two batches and could not initialize K greater than the available initialization points. The preregistered compatibility fix preserves two batches when sufficient and adds batches until at least K points are present. FAISS still warned that 8,192 points were fewer than its recommended 126,165 points for 3,235 centroids; the full run nevertheless completed at realized K=3,234. This warning prohibits presenting the full result as an optimized large-K initialization study.

## Safe reply wording

> We added a five-point, 300-epoch D13 scaling series through the complete 161,764-cell dataset. The full run completed in approximately 119 minutes with peak CPU RSS of 203 GiB and peak GPU allocated/reserved memory of 5.25/7.13 GiB. CPU-side loading and legacy preprocessing dominated memory. Although the 100k and full runs realized nearly all requested anchors, intermediate 25k/50k runs showed substantial empty-anchor and size-tail instability, so we report implementation feasibility but do not claim uniformly stable quality across scale.

## Prohibited claims and limitations

- Do not describe GPU-only memory as total memory.
- Do not claim linear empirical runtime scaling or uniform size stability.
- Do not hide the 50k empty-anchor rate (23.8%) or max size 1,782.
- This is one seed and one RNA+ADT dataset; uncertainty across seeds is unmeasured.
- Training batch-size/order stability, D16 scaling points, sparse-safe preprocessing equivalence, and unified D13–D16 batch integration remain missing.
- CUDA deterministic warnings mean strict bitwise determinism is not guaranteed.

## Evidence

- Exact combined table: `revision_results/phase2/08_scalability/d13_scaling_series.csv`
- Per-run outputs: `revision_results/phase2/08_scalability/D13/GARQ/{n10000_seed0_K002,n25000_seed0_K002,n50000_seed0_K002,n100000_seed0_K002,full_seed0_K002_retry1}`
- Configs: `revision_exp/configs/methods_phase2/p2_D13_scaling_*_seed0*.yaml`
- Logs: `/data/zhangpeiru/GARQ_revision/revision_results/phase2/logs/P2_E8_D13_scaling_*`
- Command pattern: `CUDA_VISIBLE_DEVICES=0 /usr/bin/time -v /home/zhangpeiru/.conda/envs/MetqQ2/bin/python -m revision_exp.run --config <CONFIG>`
