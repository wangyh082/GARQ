# Dataset Identity Audit — Phase 2

## Status

D5, D11, D13, D16, D17 and D18 are CONFIRMED by manuscript-authoritative cell/feature dimensions, modality, and paired identifier hashes.

## Critical correction

- Correct D5: `/home/zhangpeiru/data/RNA+ADT/D8/D8_rna.h5ad` + `D8_adt.h5ad` (12,103 cells; 9,786 RNA genes; 25 ADTs). The `D8` directory label is historical and is not used as identity evidence.
- Correct D11: `/home/zhangpeiru/data/RNA+ATAC/pbmc10k/10x-Multiome-Pbmc10k-RNA.h5ad` + `10x-Multiome-Pbmc10k-ATAC.h5ad` (9,631 cells; 29,095 genes; 107,194 peaks).
- Phase 1 D5 (8,670 cells) and D11 (9,876 cells/GSE194122) biological outputs are quarantined. Candidate D4/D7 correspondences are not silent relabels.

## Count sources

All confirmed candidate `.X` matrices sampled as non-negative, integer-valued counts. `INPUT_MATRIX_PROVENANCE.csv` records sparsity, dtype, extrema, integer fraction, zero fraction, raw/layer presence, and normalization risk.

## Pairing

RNA/ADT or RNA/ATAC row order is exact for D5, D11, D13, D16 and D17. D18 is exact after the predeclared ADT terminal `.number` to `-number` canonicalization; the canonicalized identifiers are unique and position-wise equal.

## Evidence files

- `data_inventory.csv`
- `INPUT_MATRIX_PROVENANCE.csv`
- `dataset_registry_conflicts.csv`
- `phase1_result_validity.csv`
- `revision_exp/data_registry/datasets_v2.yaml`

No source dataset was modified or copied.
