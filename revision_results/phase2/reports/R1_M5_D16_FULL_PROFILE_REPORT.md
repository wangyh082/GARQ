# D16 full-data GARQ stage profile

## Status and reviewer mapping

**PASS for corrected retry2 (seed 0).** This is the required D16 full-data profile component for Reviewer 1 Major 5 and the scalability/memory concern. It does not complete the requested D13–D16 unified batch-integration benchmark.

## Experiment and exact result

D16 corrected paired RNA+ATAC data, 32,231 cells, requested/realized K=645/645, resolution 0.0200118, 300 epochs, training batch size 256, kNN5, seed 0. The run produced all assignments with no empty anchors. Median/mean/max metacell size was 52/49.97/115; Gini was 0.1958; compression ratio was 49.97.

Total monitored wall time was 3,636.998 seconds (1:00:37). `/usr/bin/time -v` reported 1:00:41 wall and peak RSS 217,934,420 KiB. The internal sampler recorded peak CPU RSS 223,164,846,080 bytes (207.84 GiB). Peak GPU allocated/reserved during inference was 1,580,255,232/2,287,992,832 bytes; GPU memory must not be described as total memory.

| stage | wall seconds | peak CPU RSS bytes | peak GPU allocated bytes | peak GPU reserved bytes |
|---|---:|---:|---:|---:|
| resource preflight | 0.068 | 677,302,272 | 0 | 0 |
| load + legacy preprocessing | 497.660 | 223,164,846,080 | 0 | 0 |
| anchor initialization | 1.232 | 56,620,203,520 | 148,508,160 | 176,160,768 |
| warmup + full training | 3,102.671 | 57,200,467,968 | 999,972,249.6 | 1,050,673,152 |
| inference | 13.893 | 57,434,030,080 | 1,580,255,232 | 2,287,992,832 |
| common evaluation | 0.205 | 57,171,169,280 | 269,969,920 | 2,287,992,832 |
| metacell aggregation | 19.116 | 58,884,747,264 | 269,969,920 | 2,287,992,832 |

The main memory bottleneck was CPU-side loading/preprocessing, not GPU training. This supports the implementation-level concern that preprocessing densification can dominate memory.

## Preserved failures and compatibility-equivalent retry

1. Original run: **FAIL** after preprocessing. The released initializer always used two 256-cell batches (512 points), fewer than requested K=645, and FAISS raised `nx >= k`. Peak RSS before failure was 212,123,112 KiB. Evidence remains in the original output directory and `P2_E8_D16_full_profile_seed0.driver.log`.
2. Retry1: **FAIL** after 3.23 seconds because a descriptive `implementation_tag` was not accepted by the runner whitelist. Evidence remains in the retry1 directory/log.
3. Retry2: **PASS**. The compatibility fix preserves exactly two initialization batches when sufficient and reads extra batches only until training points are at least K. It does not change K, data, seed, training schedule, or downstream evaluator. Two regression tests cover both large-K and legacy two-batch behavior.

## Safe reply wording and limitations

> On the corrected full D16 dataset (32,231 cells), GARQ completed 300 epochs at K=645 in approximately 61 minutes. Peak CPU RSS was about 208 GiB during legacy loading/preprocessing, whereas peak GPU allocated/reserved memory was about 1.58/2.29 GB during inference. We therefore report CPU and GPU memory separately and identify dense preprocessing, rather than GPU model execution, as the principal memory bottleneck in this run.

Do not claim broad scalability from one seed/dataset. D13, batch-size/order stability, scaling-series points, sparse-safe equivalence, and the common D13–D16 MOFA+ integration benchmark remain incomplete. The deterministic-mode warnings document CUDA operations without deterministic implementations; this seed is reproducible by configuration but strict bitwise determinism is not established.

## Evidence

- Config: `revision_exp/configs/methods_phase2/p2_D16_full_profile_seed0_retry2.yaml`
- Successful outputs: `revision_results/phase2/08_scalability/D16/GARQ/full_seed0_profile_K002_retry2/`
- Exact stage table: `stage_profile.csv`
- Exact size table: `metacell_size_summary.csv`
- Server logs: `/data/zhangpeiru/GARQ_revision/revision_results/phase2/logs/P2_E8_D16_full_profile_seed0*.driver.log`
- Server command: `CUDA_VISIBLE_DEVICES=0 /usr/bin/time -v /home/zhangpeiru/.conda/envs/MetqQ2/bin/python -m revision_exp.run --config revision_exp/configs/methods_phase2/p2_D16_full_profile_seed0_retry2.yaml`
- Tests after compatibility fix: 31 passed, 13 warnings.
