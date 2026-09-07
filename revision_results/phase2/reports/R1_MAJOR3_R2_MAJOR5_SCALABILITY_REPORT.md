# R1 Major 3 / R2 Major 5 — implementation-scale and batch/order delivery unit

## Status and reviewer mapping

This delivery unit is **PASS / reply-ready with a qualified implementation-level
claim** for Reviewer 1 Major 3 and Reviewer 2 Major 5.  Every experiment listed
below has an explicit status.  The results characterize the released
batch-local-graph implementation; they do not establish a uniformly scalable,
batch-invariant or graph-invariant method.

| experiment | status | scope |
|---|---|---|
| D13 full-length scaling series | **PASS** | 10,000, 25,000, 50,000, 100,000 and 161,764 cells; seed 0; 300 epochs; 5/5 completed |
| D16 corrected full-data stage profile | **PASS (retry2)** | 32,231 cells; seed 0; requested/realized K=645/645; 300 epochs |
| D5/D11 training batch-size grid | **PASS** | batch sizes 256/512/1024/2048 × seeds 0–2; 24/24 rows evaluated (18 new plus six existing batch-256 runs) |
| D5/D11 frozen-checkpoint inference batch/order diagnostic | **PASS** | five batch sizes × canonical order and ten pre-specified permutations; 55/55 evaluations per dataset, 110/110 total |
| 12-run GARQ stage-profile aggregation | **PASS** | D5/D11/D17/D18 × seeds 0–2; stage wall, CPU RSS and GPU allocation/reservation recorded |

## D13 five-point scaling — exact results

| cells | requested/realized K | empty anchors | median/max size | Gini | wall | peak CPU RSS | peak GPU allocated/reserved |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 10,000 | 200/200 | 0 | 54/77 | 0.149 | 18.1 min | 13.3 GiB | 0.23/0.30 GiB |
| 25,000 | 500/472 | 28 | 48/821 | 0.261 | 42.0 min | 32.0 GiB | 0.22/0.30 GiB |
| 50,000 | 1,000/762 | 238 | 29/1,782 | 0.670 | 85.1 min | 63.2 GiB | 0.21/0.30 GiB |
| 100,000 | 2,000/1,999 | 1 | 54/76 | 0.146 | 70.5 min | 125.7 GiB | 5.19/7.07 GiB |
| 161,764 | 3,235/3,234 | 1 | 52/74 | 0.107 | 119.0 min | 202.9 GiB | 5.25/7.13 GiB |

The observed series is non-monotonic: the 25k and 50k conditions have severe
empty-anchor and size-tail degradation, whereas 100k and full data return to
near-complete realized K.  The exact CSV reports peak CPU RSS from
14,239,342,592 to 217,792,278,528 bytes; CPU-side loading/legacy preprocessing
dominates the full-data memory footprint.  These are one-seed measurements on
one RNA+ADT dataset.

## D16 full profile — exact results

The corrected D16 paired RNA+ATAC run used 32,231 cells, requested/realized
K=645/645, resolution 0.0200118, batch size 256, kNN=5, seed 0 and 300 epochs.
Wall time was 3,636.998 s (the external timer reported 1:00:41), peak CPU RSS
was 217,934,420 KiB (internal sampler 223,164,846,080 bytes, 207.84 GiB), and
peak GPU allocated/reserved memory was 1,580,255,232/2,287,992,832 bytes.
Median/mean/max metacell size was 52/49.97/115 and Gini was 0.1958.

| stage | wall seconds | peak CPU RSS bytes | peak GPU allocated bytes | peak GPU reserved bytes |
|---|---:|---:|---:|---:|
| loading + legacy preprocessing | 497.660 | 223,164,846,080 | 0 | 0 |
| anchor initialization | 1.232 | 56,620,203,520 | 148,508,160 | 176,160,768 |
| warmup + full training | 3,102.671 | 57,200,467,968 | 999,972,249.6 | 1,050,673,152 |
| inference | 13.893 | 57,434,030,080 | 1,580,255,232 | 2,287,992,832 |
| common evaluation + aggregation | 19.321 | 58,884,747,264 | 269,969,920 | 2,287,992,832 |

## Training batch-size grid — exact findings

Mean over three seeds:

| dataset | batch | mean realized K | mean macro F1 | mean wall (s) | mean peak GPU reserved |
|---|---:|---:|---:|---:|---:|
| D5 | 256 | 237.3 | 0.7672 | 1,078.6 | 0.285 GB |
| D5 | 512 | 238.7 | 0.8307 | 1,778.9 | 0.432 GB |
| D5 | 1024 | 241.3 | 0.8337 | 1,446.9 | 1.135 GB |
| D5 | 2048 | 240.0 | 0.7865 | 1,296.5 | 2.106 GB |
| D11 | 256 | 193.0 | 0.8880 | 978.4 | 2.571 GB |
| D11 | 512 | 188.7 | 0.8483 | 918.5 | 4.662 GB |
| D11 | 1024 | 189.3 | 0.5934 | 908.7 | 8.774 GB |
| D11 | 2048 | 181.0 | 0.4882 | 1,013.1 | 17.895 GB |

Membership was not batch-size invariant.  Relative to batch 256, mean ARI
was 0.1301/0.1340/0.1302 on D5 and 0.1819/0.0936/0.0412 on D11 for batch
512/1024/2048, respectively.  GPU reserved memory increased strongly while
CPU RSS remained dominated by preprocessing.  This comparison changes both
minibatch composition and the released batch-local graph, so it does not
isolate those effects.

## Frozen-checkpoint inference order/batch diagnostic

At the reference inference batch 1,024, ten cell-order permutations produced
mean ARI 0.5746 (range 0.5704–0.5833) on D5 and 0.6942 (0.6876–0.7031) on
D11 relative to canonical order.  Across batch sizes 256/512/1024/2048/4096,
the mean permuted ARI was 0.5264/0.5532/0.5746/0.5864/0.5945 on D5 and
0.6590/0.6783/0.6942/0.7082/0.7152 on D11.  Larger batches improved
agreement but did not eliminate order dependence and increased GPU memory.
All 55 evaluations per dataset passed and assignments were restored to
canonical cell order before comparison; canonical batch 1,024 ARI=1 is only
an internal correctness check.

## Preserved failures and compatibility-equivalent retries

- D13's first full configuration **FAIL**ed in 3.33 s because a descriptive
  `implementation_tag` was not in the runner whitelist.  Retry1 changed only
  that tag to the legal `instrumented_legacy`; the scientific K, data, seed,
  epochs and evaluator were unchanged and the independent failure log remains
  preserved.
- D16 original full profile **FAIL**ed at `nx >= k` because the released
  initializer used two 256-cell batches (512 points) for K=645.  Retry1
  **FAIL**ed after the same whitelist validation.  Retry2 **PASS**ed after the
  compatibility-equivalent initializer read additional batches only until at
  least K initialization points were available.  Original and retry1 output
  directories and driver logs remain intact.
- FAISS's warning that 8,192 initialization points are below its recommended
  126,165 points for 3,235 centroids is retained; the D13 full result is not
  presented as an optimized large-K initialization study.

## Reply-safe wording

> We added a five-point, 300-epoch D13 scaling series through the complete
> 161,764-cell dataset and a corrected full-data D16 profile.  The D13 full run
> completed in approximately 119 minutes with peak CPU RSS of 203 GiB and
> peak GPU allocated/reserved memory of 5.25/7.13 GiB; D16 reached 208 GiB
> peak CPU RSS during loading/preprocessing.  We also evaluated full-data
> training batch sizes and frozen-checkpoint inference order.  These diagnostics
> show that CPU preprocessing is the principal memory bottleneck and that the
> released batch-local graph is sensitive to scale, batch size and cell order.
> We therefore report implementation feasibility and its limitations rather
> than claim uniform scalability or batch/order invariance.

## Prohibited claims and scientific limitations

- Do not claim linear runtime, uniformly stable metacell sizes, or
  batch/order-invariant assignments.
- Do not describe GPU-only memory as total memory; CPU RSS and GPU allocated/
  reserved values are separate quantities.
- Do not generalize the one-seed D13 or D16 results to all datasets or seeds.
- The inference diagnostic compares assignments with a canonical reference,
  not ground truth, and does not test a global sparse-kNN redesign.
- The D16 profile is a scalability component for R1 Major 5, not the missing
  unified D13–D16 batch-integration/MOFA+ benchmark.
- CUDA warnings mean strict bitwise determinism is not established.

## Evidence, commands and verification

Local summary tables:

- `revision_results/phase2/08_scalability/d13_scaling_series.csv`
- `revision_results/phase2/08_scalability/stage_profile.csv`
- `revision_results/phase2/08_scalability/training_batch_size.csv`
- `revision_results/phase2/08_scalability/training_batch_size_assignment_stability.csv`
- `revision_results/phase2/08_scalability/inference_stability/D5/seed0_K002/batch_size_order_stability.csv`
- `revision_results/phase2/08_scalability/inference_stability/D11/seed0_K002/batch_size_order_stability.csv`
- `revision_results/phase2/08_scalability/D16/GARQ/full_seed0_profile_K002_retry2/metacell_size_summary.csv`

Server raw outputs are under
`/data/zhangpeiru/GARQ_revision/revision_results/phase2/08_scalability/`; D13
driver/status logs are `P2_E8_D13_scaling_*`, D16 logs are
`P2_E8_D16_full_profile_seed0*`, and the batch/inference status files are under
`/data/zhangpeiru/GARQ_revision/revision_results/phase2/logs/`.  The run
command was `CUDA_VISIBLE_DEVICES=<gpu> /usr/bin/time -v
/home/zhangpeiru/.conda/envs/MetqQ2/bin/python -m revision_exp.run --config
<CONFIG>`.  The final server verification was `43 passed, 13 warnings` with
`python -m pytest -q revision_exp/tests`; all 18 batch-size and both inference
status files were zero, and all five D13 plus D16 retry2 status files were
zero.  This report is the dedicated reviewer delivery unit for R1 Major 3 and
R2 Major 5; R1 Major 5 remains partial until unified batch integration is run.
