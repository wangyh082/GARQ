# R2 Major 1 — D18 full-data neighborhood retention and homogeneity

## Status and reviewer mapping

**PASS for the frozen seven-combination, three-seed D18 evaluator; the finding is predominantly negative for a strong shared-neighborhood claim.** The evaluator covered all 21 corrected full-data modality-combination runs. R2 Major 1 remains PARTIAL until corrected full-data thinning/permutation experiments finish.

## Experiment

The evaluator reused the frozen GARQ embeddings and assignments from RNA, ATAC, ADT, RNA+ATAC, RNA+ADT, ATAC+ADT, and RNA+ATAC+ADT at requested K=510, resolution approximately 0.02, and seeds 0–2. For each learned modality block, it measured the fraction of k-nearest-neighbor edges retained inside the shared anchor assignment at k=5, 15, and 30, per-anchor cosine compactness, pairwise modality-neighborhood Jaccard, and a preregistered percentile-based modality-conflict anchor flag. Neighbors were computed once at k=30 and sliced deterministically for smaller k.

## Exact primary results at k=15

| combination | learned block | mean within-anchor edge fraction | seed range |
|---|---|---:|---:|
| RNA | RNA | 0.181837 | 0.175465–0.186054 |
| ATAC | ATAC | 0.251080 | 0.218354–0.292294 |
| ADT | ADT | 0.330799 | 0.274047–0.359789 |
| RNA+ATAC | RNA | 0.125850 | 0.123040–0.128706 |
| RNA+ATAC | ATAC | 0.080071 | 0.078959–0.081661 |
| RNA+ADT | RNA | 0.156761 | 0.128944–0.176251 |
| RNA+ADT | ADT | 0.118504 | 0.097451–0.131131 |
| ATAC+ADT | ATAC | 0.148462 | 0.145153–0.150830 |
| ATAC+ADT | ADT | 0.133686 | 0.127465–0.140448 |
| RNA+ATAC+ADT | RNA | 0.108772 | 0.089519–0.128604 |
| RNA+ATAC+ADT | ATAC | 0.085616 | 0.069292–0.104905 |
| RNA+ATAC+ADT | ADT | 0.070599 | 0.058387–0.085538 |

Mean cross-modality kNN15 Jaccard was very low: RNA–ATAC 0.005914 in RNA+ATAC; RNA–ADT 0.003929 in RNA+ADT; ATAC–ADT 0.003360 in ATAC+ADT. In the full trimodal arm, mean Jaccard was 0.005962 for RNA–ATAC, 0.004010 for RNA–ADT, and 0.003389 for ATAC–ADT.

The percentile-based conflict-anchor rate was 0.003929–0.011765 for RNA+ATAC, 0.103175–0.125249 for RNA+ADT, 0.102249–0.137652 for ATAC+ADT, and 0.096708–0.111562 for full trimodal. Mean cosine compactness distance in the full trimodal arm was 0.386722 for RNA, 0.339957 for ATAC, and 0.259754 for ADT; lower is more compact.

## Evidence, commands, and verification

- Exact 162-row metrics: `revision_results/phase2/02_modality/d18_modality_neighborhood_full.csv`
- Exact 9,123-row anchor table: `revision_results/phase2/02_modality/d18_modality_anchor_compactness_full.csv`
- Workflow: `revision_exp/workflows/d18_modality_neighborhood_full.py`
- Server log: `/data/zhangpeiru/GARQ_revision/revision_results/phase2/logs/P2_E2_D18_MODALITY_NEIGHBORHOOD_FULL.driver.log`
- Server command: `/home/zhangpeiru/.conda/envs/MetqQ2/bin/python -m revision_exp.workflows.d18_modality_neighborhood_full`
- Runtime: 5:21.20 wall; peak RSS 1,759,588 KiB; exit status 0
- Test suite: `/home/zhangpeiru/.conda/envs/MetqQ2/bin/python -m pytest -q revision_exp/tests` → 28 passed, 13 warnings

## Safe reply wording and limitations

Safe wording: “Across the corrected D18 full-data modality grid, shared assignments retained a measurable but limited fraction of each learned block’s local neighbors. Cross-modality single-cell neighborhoods overlapped only weakly, and approximately 9.7–13.8% of anchors were flagged as modality-conflicting in combinations containing ADT, whereas the RNA+ATAC conflict rate was below 1.2%.”

Do not claim that shared anchors preserve all modality-specific neighborhoods, resolve discordance, or establish multimodal fidelity. The observed low pairwise overlap may reflect genuine modality-specific structure as well as method behavior; it is not itself a biological error rate. The percentile conflict flag is diagnostic rather than a validated biological discordance label. Thinning/permutation evidence is still required before making a noise-robustness claim.
