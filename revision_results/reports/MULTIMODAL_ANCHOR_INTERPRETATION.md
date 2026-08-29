# Multimodal anchor interpretation

## Status

当前证据包括 D5/D11/D17/D18 的 2,000-cell、seed-0 modality combination smoke，learned-block contribution 与 kNN-to-anchor mapping，以及 D5/D11 count-level thinning/permutation grids。尚未完成 5 seeds、全量 cells、D17/D18 noise grids、显式 modality-weight grid 和其他 baseline，因此结论为 **PARTIAL diagnostic evidence**，不得写成最终 biological superiority claim。

## What a released shared anchor represents

Released GARQ encodes each modality independently into a 32-dimensional block, concatenates raw blocks without per-block L2 normalization or variance equalization, and computes shared cell-anchor cosine similarity on the concatenation. A shared anchor is therefore an algorithmic centroid/quantization target in a joint learned space, not a directly identifiable biological regulatory unit. The assignment is also modified by a batch-local graph, so anchor membership is conditional on co-batch composition.

Block L2 means are all near 5.67–5.71 because upstream encoders contain LayerNorm, but equal norms do not imply equal similarity contribution. Sampled absolute-dot contribution is D5 RNA/ADT 51.8%/48.2%, D11 RNA/ATAC 36.8%/63.2%, D17 RNA/ATAC 48.8%/51.2%, and D18 RNA/ATAC/ADT 27.6%/38.3%/34.2%. Thus modality dominance is dataset-dependent and cannot be inferred from block dimension alone.

## Modality-specific neighborhoods versus shared anchors

At k=15, cross-modality learned-neighborhood Jaccard is low in every core smoke: D5 RNA–ADT 0.0318; D11 RNA–ATAC 0.0227; D17 RNA–ATAC 0.0077; D18 RNA–ATAC 0.0132, RNA–ADT 0.0201, ATAC–ADT 0.0110. This is evidence that paired modalities encode substantially different local neighborhoods. Shared anchors pool those discordant structures; they do not prove that a single common local manifold exists.

The within-shared-anchor edge fraction still varies by modality (for example D11 RNA 0.462 versus ATAC 0.337; D18 RNA 0.315, ATAC 0.265, ADT 0.342). Consequently, an anchor can be compact in one modality and diffuse in another. Conflict-anchor diagnostics are retained in `conflict_anchor_metrics.csv`; no visually favorable region was hand-selected.

## D5 count-level modality perturbation

Design: same 2,000 cells, seed 0, requested K=40, 6 epochs. Source `.X` matrices are verified non-negative integer counts. One shared p=1 count baseline is compared with per-modality binomial thinning p∈{0.75,0.5,0.25} and cell-wise permutation negative controls. Every condition retrains from scratch. These runs are tagged `diagnostic_variant_modality_noise`, not legacy reproduction.

| Condition | realized K | ARI vs p=1 | perturbed-block kNN15 Jaccard | unperturbed-block kNN15 Jaccard |
|---|---:|---:|---:|---:|
| RNA thin 0.75 | 37 | 0.190 | 0.089 | 0.070 |
| RNA thin 0.50 | 38 | 0.258 | 0.069 | 0.067 |
| RNA thin 0.25 | 40 | 0.202 | 0.045 | 0.065 |
| RNA permutation | 40 | 0.087 | 0.004 | 1.000 |
| ADT thin 0.75 | 39 | 0.377 | 0.270 | 1.000 |
| ADT thin 0.50 | 40 | 0.358 | 0.137 | 1.000 |
| ADT thin 0.25 | 39 | 0.280 | 0.068 | 1.000 |
| ADT permutation | 39 | 0.175 | 0.004 | 1.000 |

The grid shows strong assignment sensitivity and asymmetric coupling. ADT perturbation leaves the learned RNA block numerically neighborhood-identical in these runs, while RNA thinning changes the learned ADT block even though ADT counts are unchanged. RNA permutation is a special case: because the ADT encoder receives the same inputs and the deterministic training path happens to preserve its block, its Jaccard is 1.0, yet shared assignments still collapse to ARI 0.087. These patterns require multi-seed confirmation and mechanistic gradient/update tracing before stronger interpretation.

The relative absolute-dot contribution does not automatically suppress a degraded modality: across RNA thinning, RNA contribution remains 37.9%–48.8%; across ADT thinning/permutation, ADT remains 48.7%–51.9%. Thus raw concatenation does not provide an evident quality-aware gating mechanism.

## D11 count-level modality perturbation

Design matches the D5 smoke (same 2,000-cell subset, seed 0, requested K=40, 6 epochs), but uses `layers['counts']` for RNA because D11 RNA `.X` is log-normalized, and uses ATAC `.X` after verifying non-negative integer values. The shared p=1 baseline therefore is a count-source diagnostic baseline, not a silent replacement for the legacy log-`.X` reproduction.

| Condition | realized K | ARI vs p=1 | perturbed-block kNN15 Jaccard | unperturbed-block kNN15 Jaccard |
|---|---:|---:|---:|---:|
| RNA thin 0.75 | 40 | 0.307 | 0.082 | 0.036 |
| RNA thin 0.50 | 40 | 0.227 | 0.057 | 0.036 |
| RNA thin 0.25 | 40 | 0.153 | 0.038 | 0.035 |
| RNA permutation | 40 | 0.132 | 0.004 | 1.000 |
| ATAC thin 0.75 | 40 | 0.303 | 0.050 | 1.000 |
| ATAC thin 0.50 | 40 | 0.245 | 0.033 | 1.000 |
| ATAC thin 0.25 | 40 | 0.263 | 0.013 | 1.000 |
| ATAC permutation | 37 | 0.190 | 0.005 | 1.000 |

The D11 count baseline realizes 39 anchors. Its sampled absolute-dot contribution is RNA 37.4% and ATAC 62.6%. The contribution does not track input quality monotonically: at ATAC p=0.25 the ATAC share rises to 70.3%, while at RNA p=0.25 the RNA share remains 30.2%. As in D5, thinning one modality can substantially change the separately encoded block for the unchanged modality, whereas the permutation controls happen to preserve the unchanged block exactly under this deterministic single-seed path. This supports sensitivity and training-coupling, not automatic quality-aware weighting.

## Rare-state evidence

In the D5 subset, Regulatory T cells and conventional DC each have 15 cells. Treg recall/F1 is 0 in the p=1 baseline and every perturbation condition. cDC recall/F1 is also 0 except RNA thinning p=0.75 (recall 0.467, F1 0.438). In the D11 subset, Plasma cell has 8 cells and recall/F1 is 0 in the count baseline and all eight perturbations; the reviewer-requested gdT label is absent from the current D11 labels. These results do not support rare-state robustness. The isolated non-monotonic D5 cDC result must not be selected as evidence that noise improves rare-state preservation.

## Interpretation boundary

- Current results support “shared anchors combine modality-dependent learned signals and may be sensitive to modality quality.”
- They do not support “all modalities contribute equally,” “adding a modality is always beneficial,” or a causal biological interpretation of anchor membership.
- Full claims require D5/D11/D17/D18 full-data, 5 seeds, explicit block-normalization/variance/weight variants, matched realized K, gradient/update norm tracing, and baseline comparisons.

Primary evidence: `revision_results/02_modality/modality_block_contribution.csv`, `neighborhood_anchor_mapping.csv`, `modality_noise_perturbation.csv`, `modality_noise_per_type.csv`, and all resolved `E2_D5_noise_*` / `E2_D11_noise_*` configs/manifests.
