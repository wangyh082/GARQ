# D5/D11 full-data training batch-size stability

## Status and reviewer mapping

**PASS: complete four-batch-size × three-seed grid on corrected D5 and D11.** The existing batch-256 runs were reused and 18 new batch-512/1024/2048 runs all passed. This addresses Reviewer 1 Major 3 and Reviewer 2 Major 5. The scientific finding is negative for batch-size invariance, particularly on D11.

## Experiment

Corrected full D5 and D11 datasets, requested K=242 and 193, 300 epochs, seeds 0–2, training batch sizes 256/512/1024/2048, identical preprocessing and common evaluator. Same-seed assignments at batch 512/1024/2048 were compared against batch 256 using ARI, NMI, VI, and random-pair coassignment agreement.

## Exact mean results

| dataset | batch | mean realized K | mean macro F1 | mean wall (s) | mean peak CPU RSS | mean peak GPU reserved |
|---|---:|---:|---:|---:|---:|---:|
| D5 | 256 | 237.3 | 0.7672 | 1,078.6 | 5.43 GB | 0.285 GB |
| D5 | 512 | 238.7 | 0.8307 | 1,778.9 | 5.43 GB | 0.432 GB |
| D5 | 1024 | 241.3 | 0.8337 | 1,446.9 | 5.43 GB | 1.135 GB |
| D5 | 2048 | 240.0 | 0.7865 | 1,296.5 | 5.43 GB | 2.106 GB |
| D11 | 256 | 193.0 | 0.8880 | 978.4 | 22.86 GB | 2.571 GB |
| D11 | 512 | 188.7 | 0.8483 | 918.5 | 22.86 GB | 4.662 GB |
| D11 | 1024 | 189.3 | 0.5934 | 908.7 | 22.86 GB | 8.774 GB |
| D11 | 2048 | 181.0 | 0.4882 | 1,013.1 | 22.86 GB | 17.895 GB |

GPU reserved memory increased strongly with batch size, especially on D11. CPU RSS was nearly constant within dataset because legacy full-data preprocessing dominated it. Runtime did not improve monotonically.

## Assignment stability versus batch 256

| dataset | batch | mean ARI (range) | mean NMI | mean VI |
|---|---:|---:|---:|---:|
| D5 | 512 | 0.1301 (0.1136–0.1497) | 0.5876 | 4.4063 |
| D5 | 1024 | 0.1340 (0.1073–0.1521) | 0.5769 | 4.5373 |
| D5 | 2048 | 0.1302 (0.1116–0.1429) | 0.5649 | 4.6272 |
| D11 | 512 | 0.1819 (0.0458–0.2563) | 0.6377 | 3.6091 |
| D11 | 1024 | 0.0936 (0.0229–0.2200) | 0.5526 | 4.0880 |
| D11 | 2048 | 0.0412 (0.0339–0.0552) | 0.5115 | 4.2929 |

Membership was not invariant even when aggregate D5 macro F1 improved at batch 512/1024. D11 showed both declining macro F1 and very low same-seed membership ARI as batch size increased. The released batch-local graph therefore materially affects results.

## Safe reply wording

> We added full-data batch-size experiments at 256, 512, 1024, and 2048 with three seeds on corrected D5 and D11. GPU reserved memory increased with batch size, reaching approximately 17.9 GB on D11 at batch 2048, whereas CPU RSS remained dominated by preprocessing. Assignments were not batch-size invariant: mean ARI relative to batch 256 was approximately 0.13 on D5 and declined from 0.18 to 0.04 on D11 as batch size increased. We therefore explicitly identify the released batch-local graph as a source of sensitivity and avoid claiming batch-size-independent results.

## Limitations and prohibited claims

- Do not claim batch-size invariance or monotonic speedup.
- Do not use aggregate macro F1 to conceal low membership ARI.
- The comparison changes both training minibatch composition and the batch-local graph; it does not isolate their effects.
- Strict bitwise determinism is not guaranteed because the logs retain CUDA nondeterminism warnings.
- Inference batch-size/order testing from a common checkpoint remains separate and incomplete.
- Other-user GPU workloads coexisted during part of the queue; no jobs were interrupted, and wall time should not be treated as isolated-system throughput.

## Evidence

- Run-level table (24 rows): `revision_results/phase2/08_scalability/training_batch_size.csv`
- Same-seed stability table (18 rows): `revision_results/phase2/08_scalability/training_batch_size_assignment_stability.csv`
- Configs: `revision_exp/configs/batch_size_full/`
- Workflow: `revision_exp/workflows/summarize_batch_size_full.py`
- Server logs: `/data/zhangpeiru/GARQ_revision/revision_results/phase2/logs/P2_E8_D{5,11}_batch*`
- All 18 new run statuses are 0; existing six batch-256 runs were previously verified PASS.
