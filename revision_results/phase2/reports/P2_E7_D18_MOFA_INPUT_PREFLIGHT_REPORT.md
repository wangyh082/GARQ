# P2-E7 D18 cross-method MOFA+ input preflight

Status: **PASS (input-integrity experiment; MOFA+ biological fit pending)**  
Reviewer mapping: **R2 Major 4**.

## Experiment and exact result

The 12 D18 assignments (GARQ, KMeans, MetaQ and SEACells × seeds 0–2) were checked against all three authoritative source modalities before common MOFA+ aggregation.

- Every run contains 25,517 rows and 25,517 unique cell IDs.
- Every assignment ID set equals the RNA source ID set.
- Assignment row order equals RNA source order for all 12 runs.
- RNA and ATAC source order is exactly equal.
- RNA and ADT source order is exactly equal after the preregistered ADT `.N` → `-N` canonicalization.
- Realized K: GARQ 497/493/486; KMeans 510/510/510; MetaQ 511/505/517; SEACells 510/510/510.

Machine-readable outputs:

- `revision_results/phase2/07_trimodal/mofa_input_assignment_preflight.csv`
- `revision_results/phase2/07_trimodal/mofa_input_assignment_preflight.json`

## Safe conclusion

The same 25,517 paired D18 cells can be aggregated under every method/seed assignment without cell-set or modality-order confounding. This removes an input-alignment blocker for the cross-method MOFA+ comparison.

## Scientific limitation

No D18 MOFA+ biological model was fitted in this experiment. Factor count, feature universe, normalization, view scaling, convergence and downstream evaluation must still be frozen and run identically. This PASS does not show GARQ-specific downstream performance.

## What must not be claimed

- Do not report MOFA+, clustering or held-out results as complete.
- Do not interpret alignment PASS as biological agreement.
- Do not choose method-specific features or MOFA+ settings after inspecting performance.
