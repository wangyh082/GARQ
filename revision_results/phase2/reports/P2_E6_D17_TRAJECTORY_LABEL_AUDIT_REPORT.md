# P2-E6 D17 trajectory label audit

Status: **BLOCKED / AUTHOR LABEL MAPPING REQUIRED**  
Reviewer mapping: **R2 Major 3**.

## Required preregistered states

The authoritative Phase-2 plan specifies a fixed trajectory among:

1. `Tumor Epithelial` (root),
2. `Tumor Cells (Dedifferentiated)`,
3. `Stressed Tumor (p53+)`.

## Exact D17 source labels

The confirmed D17 RNA source `/home/zhangpeiru/data/analysis/new/kidney_rna_updated.h5ad` has 16,143 cells and the following relevant `celltype` values:

- `Tumor Epithelial`: 3,279 cells.
- `Tumor (Neuronal-like)`: 1,430 cells.
- `Stressed Tumor (p53+)`: 1,002 cells.
- `Tumor Cells (Dedifferentiated)`: **absent**.

The remaining labels are Proximal Tubule, Podocytes, Myeloid Cells, Parietal Epithelial Cells, Low Quality / Dying, Injured PT-like, T Cells, Mast Cells, and Endothelial Cells.

## Search result

Repository-wide results consistently use `Tumor (Neuronal-like)` for the confirmed D17 source and existing assignments. No verified mapping file or source annotation equating it to `Tumor Cells (Dedifferentiated)` was found.

## Why the trajectory was not silently run

Replacing `Tumor Cells (Dedifferentiated)` with `Tumor (Neuronal-like)` changes the biological state definition. Labels are central to fixing the trajectory clusters and state ordering, so this is not an engineering compatibility substitution and cannot be inferred from name similarity.

## Required author decision

Choose one and document its provenance:

1. Confirm that `Tumor (Neuronal-like)` is the intended current name for the manuscript's `Tumor Cells (Dedifferentiated)` state; then run the fixed three-state trajectory with an explicit alias record.
2. Provide the authoritative D17 annotation file containing `Tumor Cells (Dedifferentiated)`.
3. Revise the trajectory state definition in the response/manuscript and explain why.

## Acceptance criteria for continuation

- Written mapping or authoritative annotation path.
- No label chosen based on favorable trajectory performance.
- Root remains `Tumor Epithelial` unless the author explicitly revises it.
- The same state mapping, feature set, Slingshot parameters, UCell sets and evaluation metrics are frozen for every method and seed.

## Available environment

The trajectory environment gate passed separately: Slingshot 2.18.0, SingleCellExperiment 1.32.0, UCell 2.14.0 and tradeSeq 1.24.0.

## What must not be claimed

- Do not state that D17 cross-method trajectory metrics are complete.
- Do not silently relabel `Tumor (Neuronal-like)` as dedifferentiated.
- Do not select a substitute state using trajectory correlation or other outcome metrics.
