# D17 trajectory label conflict

## Status and reviewer mapping

**BLOCKED pending author decision.** This blocks the Reviewer 2 D17 cross-method trajectory unit and the GARQ-specific trajectory comparison. No trajectory was fit and no label was silently substituted.

## Exact conflict

The authoritative Phase 2 plan freezes the trajectory states as:

1. `Tumor Epithelial` (root),
2. `Tumor Cells (Dedifferentiated)`,
3. `Stressed Tumor (p53+)`.

The confirmed D17 metadata `/home/zhangpeiru/data/analysis/new/kidney_rna_updated.h5ad` contains 16,143 cells and only these tumor labels:

- `Tumor Epithelial`: 3,279 cells,
- `Tumor (Neuronal-like)`: 1,430 cells,
- `Stressed Tumor (p53+)`: 1,002 cells.

`Tumor Cells (Dedifferentiated)` does not occur in any obs column. The matched-method assignments use this same cell universe. Treating `Tumor (Neuronal-like)` as the preregistered dedifferentiated state would change biological semantics and requires author approval.

## Evidence and command

The conflict was verified by reading the corrected D17 H5AD in backed mode and enumerating every obs value containing `Tumor` or `Dediff`. Only the three labels above were found. The exact file is fingerprinted in the Phase 2 identity audit; the metadata SHA256 used by the D17 Mast analysis is `c2f4bc8313fa68c7e1c670fce74f287dca3865b0c039070babb10bd1f4125e25`.

Environment verification passed: `/opt/R/4.4.3/bin/Rscript` and the project Phase 2 library can load Slingshot 2.18.0 and SingleCellExperiment 1.32.0. Package availability is not the blocker.

## Decisions and retry plan

Author must choose one of:

1. Confirm that `Tumor (Neuronal-like)` is the renamed/equivalent dedifferentiated state. Then run the frozen three-state Slingshot comparison with an explicit nomenclature disclosure.
2. Provide the authoritative D17 annotation containing `Tumor Cells (Dedifferentiated)` and its mapping to the confirmed 16,143 cells.
3. Redefine the trajectory to the three labels actually present. This is a scientific plan change and must be described as such.

After a decision, the same single-cell PCA/features, Slingshot version/parameters, root, smoothing, and matched assignments will be used for GARQ, MetaQ, SEACells, and KMeans across seeds 0–2. Missing MetaCell V2/SuperCell will remain explicit.

## Prohibited claims

- Do not silently rename `Tumor (Neuronal-like)` to `Tumor Cells (Dedifferentiated)`.
- Do not claim the D17 cross-method trajectory is complete.
- Do not substitute the Mast-cell post-hoc analysis for trajectory evidence.
