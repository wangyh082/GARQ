# E1 targeted rare-abundance broad screen

## Scope and implementation status

This is a **diagnostic smoke broad screen**, not the complete preregistered E1 rare-cell experiment. It uses the recovered D5 (RNA+ADT) and D11 (RNA+ATAC) data, 2,000 cells per run, requested K=40, training seed 0, six epochs, and one independently seeded targeted subset per condition. The implementation is tagged `diagnostic_variant_rare_subsampling`. All 29 eligible recovered-data types (17 in D5 and 12 in D11) were selected algorithmically by source abundance <=5% and source support >=50; D11 Plasma cell was additionally retained as a preregistered paper example despite support 26.

Sampling is deterministic and without replacement. Each run stores the source abundance, requested and realized abundance, target-cell count, source-cell count, and SHA256 of the selected cell IDs in `subset_provenance.json`. Unit tests separately verify exact support, determinism, rejection of abundance-increasing requests, and failure on missing labels.

## Selection rule and reachable conditions

The plan requests target abundances 1%, 0.5%, and 0.2% for the broad screen. A condition is generated only when it is a true downsampling of the named population; target cells are never duplicated or oversampled to raise their abundance.

- D5 Regulatory T cells: 71/8,670 = 0.8189%; reachable targets 0.5% and 0.2%. The 1% condition is not reachable by downsampling.
- D5 conventional DC: 67/8,670 = 0.7728%; reachable targets 0.5% and 0.2%. The 1% condition is not reachable by downsampling.
- D11 Plasma cell: 26/9,876 = 0.2633%; reachable target 0.2%. The 1% and 0.5% conditions are not reachable by downsampling.
- D11 cDC2: 160/9,876 = 1.6201%; targets 1%, 0.5%, and 0.2% are reachable.
- D11 gdT is absent from the recovered labels and therefore cannot be tested on this file.

Applying the same reachability rule to every eligible type generated 82 conditions: 47 in D5 and 35 in D11 (the latter includes the Plasma-cell exception). There were 30 runs at 0.2%, 29 at 0.5%, and 23 at 1%. Config generation stores the audited source counts and uses a stable SHA256-derived subset seed for each newly generated dataset/type/abundance identity. The eight configurations executed in the initial pilot retain their original seeds and byte-identical configuration hashes.

Other D1-D4, D6-D10, and D12 inputs have not been recovered from the specified data root, so a complete D1-D12 algorithmic screen is not yet possible. D16 Schwann Cell belongs to the confirmatory requirements and D16 is also not recovered.

## Results

All 82 generated configurations completed with PASS status and all 82 have subset provenance. Realized support was exact: 4 cells at 0.2%, 10 at 0.5%, and 20 at 1% in each 2,000-cell subset. Realized K ranged from 33 to 40 for requested K=40, so requested and realized K must not be conflated.

The result is predominantly negative in this smoke setting. At 0.2%, only 2/30 runs had nonzero target-type F1, no run had nonzero majority retention or high-purity recovery, and mean/median recall were 0.0167/0. At 0.5%, 3/29 had nonzero F1, 1/29 had nonzero majority retention, none had high-purity recovery, and mean/median recall were 0.0276/0. At 1%, 8/23 had nonzero F1, 4/23 had nonzero majority retention, 3/23 had nonzero high-purity recovery, and mean/median recall were 0.0739/0. Overall, only 13/82 runs had nonzero F1.

The strongest isolated F1 was 0.632 for D5 plasmacytoid DC at 0.5% (precision 0.667, recall 0.600), but high-purity recovery remained 0. Other nonzero F1 values ranged from 0.091 to 0.571 and must not be selected as standalone evidence of general preservation. Crucially, every reachable condition for the preregistered examples D5 Regulatory T cells, D5 conventional DC, D5 gdT cells, D11 Plasma cell, and D11 cDC2 had precision, recall, F1, majority retention, and high-purity recovery equal to 0. These data do not support a general rare-state-preservation claim at 0.2%-1% abundance under the tested short-run configuration.

Primary numeric evidence: `revision_results/01_size_resolution/rare_subsampling_long.csv`. Run-level assignments, per-type tables, size summaries, manifests, resolved configurations, logs, and subset provenance remain under `revision_results/01_size_resolution/rare_subsampling/` and the corresponding manifest/config directories.

## Interpretation limits and required follow-up

This evidence must not be treated as confirmatory because it has only two datasets, one subset/training seed per condition, 2,000-cell subsets, six training epochs, and GARQ only. The preregistered confirmatory test still requires at least six datasets, at least two eligible types per dataset, target abundances 2%, 1%, 0.5%, 0.2%, and 0.1%, five independent seeds, full metacell reconstruction per condition, matched compression resolution, and the planned baselines. Full-data and longer-training runs may differ, but that is presently untested.

Reconstructable H5AD subset caches were deleted after successful validation to respect the project storage budget. Cell-level assignments are retained as the traceability unit, while embeddings are not committed. The exact selection rule, seeds, source paths, selected-cell hashes, configs, and provenance were retained, so the caches can be regenerated without changing the recorded experiment definition.
