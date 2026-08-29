# Scalability and complexity audit

## Status and scope

本报告严格区分 released implementation 与 diagnostic evidence。当前完成 E0 attention/shape 审计、D5/D11 2,000-cell 分阶段 smoke profiling，以及 E8.3 同一训练后模型的推理 batch-size/order 诊断。D13/D16 全量 profiling、训练 batch-size grid、global graph 和 sparse-safe prototype 尚未完成，因此当前结论为 **PARTIAL**。

## Released-code complexity

| Stage | Released behavior | Time complexity | Dominant memory |
|---|---|---:|---:|
| preprocessing | each sparse input is converted to a full dense matrix before feature selection; raw, normalized `AnnData`, selected arrays, and tensors coexist | at least O(n p) per modality | O(n p) dense, with multiple overlapping copies |
| encoder/decoder Transformer | each cell is reshaped to sequence length 1 | O(n d²) projection/FFN; attention term is O(n·1²·d), not O(n²d) inter-cell attention | O(Bd), no cross-cell attention matrix |
| batch-local cell graph | dense cosine `B×B`, top-k, dense adjacency, symmetrization | O(B²d + B² log k) approximately | O(B²) similarities plus adjacency |
| cell-anchor similarity | dense `B×K` cosine similarities | O(BKd) | O(BK) |
| graph smoothing | dense adjacency multiplied by `B×K` similarity | O(B²K) | O(B² + BK) |
| dynamic anchor update | usage EMA plus two continuous repositioning expressions; local branch after usage sum reaches threshold | O(BK + Kd) per quantized forward | O(BK + Kd) |
| inference | repeats quantization twice in released `engine.inference`, followed by all decoders and reconstruction losses | scales with number and composition of batches | inherits O(B² + BK) working memory |

The manuscript's theoretical description must not be used as a substitute for these released-code costs. In particular, the implemented Transformer has sequence length 1, while inter-cell dependence enters through the batch-local dense graph.

## Same-checkpoint inference stability (E8.3 smoke)

Design: one trained `instrumented_legacy` model per dataset, 2,000 uniformly selected cells, seed 0, requested K=40, 6 epochs. The reference is the released evaluation loader (batch size 1024, canonical order). The same post-training model was evaluated at batch sizes `{256,512,1024,2048,4096}` with canonical order plus 10 predeclared permutation seeds. Results are restored to canonical cell order before label-permutation-invariant comparison. No model parameter is retrained or selected using labels.

| Dataset | Inference batch size | ARI range vs reference | NMI range | VI range (nats) | realized K range |
|---|---:|---:|---:|---:|---:|
| D5 RNA+ADT | 256 | 0.845–0.877 | 0.814–0.835 | 0.850–0.964 | 34–37 |
| D5 RNA+ADT | 512 | 0.865–0.903 | 0.831–0.876 | 0.645–0.882 | 33–36 |
| D5 RNA+ADT | 1024 | 0.888–1.000 | 0.858–1.000 | 0.000–0.747 | 33–35 |
| D5 RNA+ADT | 2048/4096 | 0.912 (constant) | 0.882 (constant) | 0.622 (constant) | 34 |
| D11 RNA+ATAC | 256 | 0.765–0.796 | 0.783–0.806 | 1.062–1.187 | 40 |
| D11 RNA+ATAC | 512 | 0.781–0.832 | 0.801–0.846 | 0.843–1.096 | 40 |
| D11 RNA+ATAC | 1024 | 0.820–1.000 | 0.834–1.000 | 0.000–0.918 | 39–40 |
| D11 RNA+ATAC | 2048/4096 | 0.849 (constant) | 0.854 (constant) | 0.812 (constant) | 40 |

The canonical ordering is identical to the reference only at batch size 1024 (ARI=1). With one 2,000-cell batch, all permutations give the same partition because batch membership is unchanged, yet the result differs from the two-batch reference (D5 ARI=0.912; D11 ARI=0.849). At smaller batches, permutation changes batch membership and further changes assignments. D11 keeps realized K at 39–40 while ARI falls as low as 0.765, so the instability cannot be explained only by empty anchors.

Interpretation: this is direct evidence that released inference depends on batch partition/composition through the dense batch-local KNN smoothing term. It does not establish how large the effect is under full-data/long-training conditions; those runs remain required before a primary performance claim.

## Attention behavior

Forward hooks show encoder and decoder Transformer inputs shaped `[batch, 1, d]`. The E0 dependency test changes other cells while holding a target cell fixed and finds no target encoder change, confirming no inter-cell Transformer dependency. A separate batch-local graph test can change the target assignment when co-batch cells change. Evidence: `revision_results/00_audit/tensor_shapes.json`, `attention_dependency_test.csv`, and `batch_local_graph_dependency.json`.

## Evidence files

- `revision_results/08_scalability/batch_size_order_stability.csv`
- `revision_results/08_scalability/batch_size_order_per_type.csv`
- `revision_results/08_scalability/D5_inference_stability_smoke/`
- `revision_results/08_scalability/D11_inference_stability_smoke/`
- resolved configs `E8_D5_inference_stability_smoke_seed0_K002_v1` and `E8_D11_inference_stability_smoke_seed0_K002_v1`

## Remaining E8 work

- training batch-size `{256,512,1024,2048}` × 3 seeds;
- D13 and D16 stage profiling using confirmed registry paths;
- batch-local versus fixed-global graph diagnostic;
- sparse-safe preprocessing prototype and equivalence analysis;
- final figures and cross-seed confidence intervals.
