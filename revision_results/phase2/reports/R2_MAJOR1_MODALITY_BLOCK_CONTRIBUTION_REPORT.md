# R2 Major 1 — corrected full-data modality block contribution

## Status

**PASS for the block-contribution component; R2 Major 1 remains PARTIAL.** Corrected full-data GARQ embeddings were measured for D17 and D18 across seeds 0–2. This does not replace the pending full modality-combination, neighborhood-retention/homogeneity, and thinning/permutation experiments.

## Exact experiment and results

For each learned modality block, the workflow reports embedding dimension, norm and variance summaries, pairwise distance energy, sampled mean absolute dot product, and its relative share across modalities. All blocks had dimension 32, weight 1.0, and no normalization before concatenation.

| dataset | modality | mean relative absolute-dot contribution | seed range |
|---|---|---:|---:|
| D17 | RNA | 0.488936 | 0.485589–0.492589 |
| D17 | ATAC | 0.511064 | 0.507411–0.514411 |
| D18 | RNA | 0.267009 | 0.256064–0.273227 |
| D18 | ATAC | 0.348314 | 0.335362–0.355195 |
| D18 | ADT | 0.384677 | 0.372388–0.408574 |

D17 was close to balanced between RNA and ATAC. D18 was not equal: ADT contributed most by this diagnostic and RNA least, with the ordering stable across seeds.

## Evidence

- Exact 27-row table: `revision_results/phase2/02_modality/modality_block_contribution_full.csv`
- Source runs: corrected full GARQ seeds 0–2 for D17 and D18.
- Reviewer mapping: R2 Major 1 (primary) and R1 Major 2 (supporting representation evidence).

## Safe wording and prohibited claims

Safe wording: “Measured block contributions were near-balanced for D17 RNA/ATAC, whereas D18 showed stable unequal contributions (ADT > ATAC > RNA) under equal configured weights.”

Do not claim that equal configured weights imply equal learned influence, that these dot-product shares prove biological fidelity, or that R2 Major 1 is complete. Full corrected-data combination, neighborhood retention/homogeneity, and perturbation results remain missing.
