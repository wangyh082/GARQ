# D5/D11 same-checkpoint inference batch/order stability

## Status and reviewer mapping

**PASS:** corrected full D5 and D11 each completed one frozen-checkpoint diagnostic comprising five inference batch sizes, canonical order, and ten preregistered permutations (55 evaluations per dataset). This addresses Reviewer 1 Major 3 and Reviewer 2 Major 5. The result strongly rejects inference batch/order invariance in the released batch-local graph path.

## Design clarification

Each model was trained once at training batch 256, seed 0, K=242 (D5) or K=193 (D11), for 300 epochs. The reference assignment is the released evaluation loader, whose batch size is four times the training batch, i.e. 1,024. All 55 diagnostic evaluations reuse the in-memory model/anchors without retraining. Permuted results are restored to canonical cell order before comparison. Therefore ARI=1 for canonical inference batch 1,024 is an internal correctness check, not a favorable result selected after inspection.

## Exact primary results

Mean over ten permuted orders relative to the canonical reference:

| dataset | inference batch | mean ARI (range) | mean NMI | mean VI | mean realized K | peak GPU allocated |
|---|---:|---:|---:|---:|---:|---:|
| D5 | 256 | 0.5264 (0.5189–0.5333) | 0.7854 | 2.3149 | 237.1 | 83 MB |
| D5 | 512 | 0.5532 (0.5453–0.5602) | 0.7977 | 2.1835 | 237.1 | 88 MB |
| D5 | 1024 | 0.5746 (0.5704–0.5833) | 0.8071 | 2.0823 | 237.1 | 106 MB |
| D5 | 2048 | 0.5864 (0.5819–0.5950) | 0.8126 | 2.0224 | 237.1 | 165 MB |
| D5 | 4096 | 0.5945 (0.5879–0.5993) | 0.8169 | 1.9770 | 237.0 | 382 MB |
| D11 | 256 | 0.6590 (0.6544–0.6660) | 0.8464 | 1.6001 | 193.0 | 419 MB |
| D11 | 512 | 0.6783 (0.6705–0.6872) | 0.8547 | 1.5138 | 193.0 | 488 MB |
| D11 | 1024 | 0.6942 (0.6876–0.7031) | 0.8615 | 1.4428 | 193.0 | 630 MB |
| D11 | 2048 | 0.7082 (0.7036–0.7145) | 0.8679 | 1.3767 | 193.0 | 910 MB |
| D11 | 4096 | 0.7152 (0.7088–0.7195) | 0.8713 | 1.3411 | 193.0 | 1,471 MB |

Even without permutation, changing the canonical inference batch away from 1,024 changed assignments: D5 canonical ARI was 0.572/0.669/1.000/0.692/0.620 and D11 was 0.701/0.779/1.000/0.789/0.751 for batch 256/512/1024/2048/4096. At the same reference batch 1,024, merely permuting cell order reduced mean ARI to 0.575 on D5 and 0.694 on D11. Larger batches reduced but did not remove order dependence, while GPU memory increased.

## Safe reply wording

> Using one frozen full-data checkpoint per corrected dataset, we evaluated five inference batch sizes and ten preregistered cell-order permutations. The released batch-local graph path was not invariant: at the reference batch size of 1,024, cell-order permutation yielded mean ARI 0.575 on D5 and 0.694 on D11 relative to canonical order. Larger inference batches improved agreement but did not eliminate order dependence and increased GPU memory. We now report this as an implementation limitation rather than claiming order-independent inference.

## Scientific limitations and prohibited claims

- Do not claim inference order or batch-size invariance.
- The diagnostic uses one trained seed per dataset; it measures 10 order permutations but not checkpoint-to-checkpoint uncertainty.
- ARI is against the canonical batch-1,024 assignment, not ground truth.
- Larger batches change the batch-local neighbor graph; improved agreement does not prove improved biological quality.
- This experiment does not test the planned global sparse-kNN candidate. A global-graph method would change the diagnostic method definition and requires separate author evaluation.
- Strict bitwise determinism is not guaranteed due to retained CUDA warnings.

## Evidence

- D5 exact 55 rows: `revision_results/phase2/08_scalability/inference_stability/D5/seed0_K002/batch_size_order_stability.csv`
- D11 exact 55 rows: `revision_results/phase2/08_scalability/inference_stability/D11/seed0_K002/batch_size_order_stability.csv`
- Configs: `revision_exp/configs/inference_stability_full/`
- Implementation: `revision_exp/workflows/stability.py`
- Server logs: `/data/zhangpeiru/GARQ_revision/revision_results/phase2/logs/P2_E8_D{5,11}_inference_stability_seed0*`
- Both top-level statuses are 0; full tests must pass before delivery.
