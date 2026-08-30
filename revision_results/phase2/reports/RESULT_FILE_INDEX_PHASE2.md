# Result file index — Phase 2

The authoritative machine-readable inventory is `revision_results/phase2/manifests/run_manifest_phase2.json` (48 entries). SHA256 integrity is recorded in `revision_results/phase2/manifests/MANIFEST_PHASE2.sha256`.

## Requested-K matched benchmark

- `01_size_resolution/full_benchmark_long.csv`: 48 runs (4 datasets × 4 methods × 3 seeds).
- `01_size_resolution/metacell_size_summary.csv`: 48 common-evaluator size summaries.
- `01_size_resolution/per_type_metrics_long.csv`: 840 dataset/method/seed/type rows.
- `01_size_resolution/matchedK_focal_rare_long.csv`: 96 focal rare-state rows.
- `01_size_resolution/matchedK_focal_rare_summary.csv`: 32 method/type summaries.
- `01_size_resolution/matchedK_focal_rare_paired_contrasts.csv`: 24 paired GARQ-minus-baseline contrasts.

Large cell-level assignments, source H5ADs, official MetaQ metacell H5ADs, and reconstructable matrices are intentionally excluded from Git and the bundle. Server-side logs retain failed and successful retries. The ZIP contains reports, source adapters/workflows, audit/environment records, small summary tables, manifest and checksum.
