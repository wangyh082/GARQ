# Multimodal anchor interpretation

## Status

当前证据包括 D5/D11/D17/D18 的 2,000-cell、seed-0 modality combination smoke，learned-block contribution、kNN-to-anchor mapping，以及四个核心数据集的 count-level thinning/permutation 与显式 modality-weight grids。尚未完成 5 seeds、全量 cells 和其他 baseline，因此结论为 **PARTIAL diagnostic evidence**，不得写成最终 biological superiority claim。

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

## D17 and D18 count-level modality perturbation

D17 uses integer RNA/ATAC `.X`; D18 uses integer RNA/ATAC/ADT `.X` plus the preregistered ADT cell-ID canonicalization. Both use the same 2,000-cell, seed-0, requested-K=40, 6-epoch diagnostic design. All 9 D17 and 13 D18 manifests are `PASS`. To respect the shared-server storage budget, condition-specific thinning/permutation H5AD caches were removed after output validation; p=1 subset caches, resolved configs, seeds, provenance, manifests, and all small result tables remain, so the transient caches can be regenerated exactly.

| Dataset / perturbation | thinning ARI vs p=1 | permutation ARI vs p=1 | baseline absolute-dot contribution |
|---|---:|---:|---|
| D17 RNA | 0.199–0.241 | 0.102 | RNA 48.8% |
| D17 ATAC | 0.172–0.287 | 0.089 | ATAC 51.2% |
| D18 RNA | 0.194–0.261 | 0.114 | RNA 27.6% |
| D18 ATAC | 0.200–0.276 | 0.195 | ATAC 38.3% |
| D18 ADT | 0.221–0.310 | 0.228 | ADT 34.2% |

D17 realizes 39–40 anchors across conditions and D18 realizes 38–40, so the low ARIs are not explained by a gross collapse in realized K. D17 reproduces the directional pattern seen in D5/D11: ATAC perturbation leaves the RNA block's kNN15 neighborhoods identical, while RNA thinning changes the unchanged ATAC learned block. D18 is more informative because there are two unperturbed blocks. ATAC or ADT perturbation leaves both unperturbed learned blocks identical in this deterministic path; RNA thinning changes both unchanged ATAC (mean Jaccard 0.014–0.019) and ADT (0.076–0.085) blocks. This asymmetry is evidence of optimizer/training-path coupling and requires multi-seed gradient/update tracing before mechanistic claims.

The contribution shares again do not behave as quality gates. D18 ATAC contribution rises from 38.3% at p=1 to 49.2% at p=0.25, and ADT remains 36.3% at p=0.25. D18 first-epoch reconstruction loss is also on a very different scale for ADT (roughly 11–24 across its perturbations) than RNA/ATAC (roughly 0.1–0.5). Reconstruction scale and cosine contribution are distinct diagnostics, but together they show that raw concatenation/reconstruction has no explicit cross-modality quality calibration.

## Core-dataset explicit modality-weight diagnostics

The diagnostic implementation accepts one non-negative scalar per modality block and multiplies each encoded block before concatenation, anchor initialization, quantization, and inference export. `modality_weights: null` preserves the released `torch.cat` path exactly and is the equal-weight baseline. The grid uses λ∈{0,0.25,0.5,1,2}, where λ=1 is represented by that baseline; every non-baseline run is tagged `diagnostic_variant_modality_weight`. These are 2,000-cell, seed-0, requested-K=40, 6-epoch smoke runs on D5, D11, D17, and D18 and are not a proposed replacement for released GARQ.

All 40 manifests pass: 9 each for D5/D11/D17 and 13 for tri-modal D18. Equal-weight absolute-dot contributions are D5 RNA/ADT 51.8%/48.2%, D11 RNA/ATAC 36.8%/63.2%, D17 RNA/ATAC 48.8%/51.2%, and D18 RNA/ATAC/ADT 27.6%/38.3%/34.2%. Scaling strongly changes assignment despite similar realized K. Non-baseline ARI versus equal weights is 0.247–0.398 for D5 (realized K 34–40), 0.166–0.254 for D11 (K 38–40), 0.117–0.242 for D17 (K always 40), and 0.217–0.325 for D18 (K 39–40). Thus the diagnostic supports broad sensitivity to block weighting, not a uniquely optimal weight.

Contribution changes are large and nonlinear because the reported absolute-dot shares depend approximately on squared block scale. For example, D5 ADT contribution moves from 0% at λ=0 to 5.5%, 18.9%, 48.2%, and 78.8% at λ=0.25, 0.5, 1, and 2. D11 ATAC moves from 0% to 9.7%, 30.1%, 63.2%, and 87.3%. A positive scalar leaves that block's own cosine-neighbor ordering unchanged, so its kNN15 Jaccard versus equal weights is 1.0 by construction; at λ=0 the block is all zeros and the resulting arbitrary tie-based neighborhood Jaccard must not be biologically interpreted.

Rare-state outcomes do not justify selecting a favorable λ. D5 Regulatory T cells and conventional DC each have 15 sampled cells and recall/F1=0 in every weight condition. D11 Plasma cell has 8 cells and recall/F1=0 throughout. D11 cDC2 (42 cells) is non-monotonic (F1 0–0.471), while the equal-weight F1 is 0.125; this single-seed fluctuation is exploratory and cannot be used for label-guided weight choice. The reviewer-requested D11 gdT label remains absent. D17 Mast Cells (8 cells) have recall/F1=0 throughout. In D18, DC.Myeloid and T.DoubleNegative (2 each) plus Mono.CD16 (8) are never recovered; Platelets (4) has recall/F1=0 except at ATAC λ=0.5 (recall 0.25, F1 0.40), an isolated result that cannot support weight selection. Multi-seed, full-data and preregistered label-free model-selection evidence is required before recommending any explicit weighting.

Primary weight evidence: `revision_results/02_modality/modality_weight_grid.csv`, `modality_weight_per_type.csv`, `weights/D5`, `weights/D11`, `weights/D17`, `weights/D18`, and all resolved `E2_D*_weight_*` configs and manifests.

## Rare-state evidence

In the D5 subset, Regulatory T cells and conventional DC each have 15 cells. Treg recall/F1 is 0 in the p=1 baseline and every perturbation condition. cDC recall/F1 is also 0 except RNA thinning p=0.75 (recall 0.467, F1 0.438). In D11, Plasma cell has 8 cells and recall/F1 is 0 in all conditions; the reviewer-requested gdT label is absent. In D17, Endothelial Cells (4), Mast Cells (8), and T Cells (14) have recall/F1=0 in every condition. In D18, DC.Myeloid (2), T.DoubleNegative (2), and Mono.CD16 (8) are never recovered; Platelets (4) has baseline recall/F1=0 and reaches recall 0.5 only in an isolated perturbation condition. These results do not support rare-state robustness. Non-monotonic isolated improvements must not be selected as evidence that noise is beneficial.

## Interpretation boundary

- Current results support “shared anchors combine modality-dependent learned signals and may be sensitive to modality quality.”
- They do not support “all modalities contribute equally,” “adding a modality is always beneficial,” or a causal biological interpretation of anchor membership.
- Full claims require D5/D11/D17/D18 full-data, 5 seeds, explicit block-normalization/variance/weight variants, matched realized K, gradient/update norm tracing, and baseline comparisons.

Primary evidence: `revision_results/02_modality/modality_block_contribution.csv`, `neighborhood_anchor_mapping.csv`, `modality_noise_perturbation.csv`, `modality_noise_per_type.csv`, and all resolved `E2_D5_noise_*`, `E2_D11_noise_*`, `E2_D17_noise_*`, and `E2_D18_noise_*` configs/manifests.
