# Result file index — Phase 2

The authoritative machine-readable inventory is `revision_results/phase2/manifests/run_manifest_phase2.json`; its current entry count and SHA256 are recorded in the JSON/checksum pair. `revision_results/phase2/GARQ_phase2_handoff_bundle.zip` contains the small report and summary subset. SHA256 integrity is recorded in `revision_results/phase2/manifests/MANIFEST_PHASE2.sha256`.

## Requested-K matched benchmark

- `01_size_resolution/full_benchmark_long.csv`: 48 runs (4 datasets × 4 methods × 3 seeds).
- `01_size_resolution/metacell_size_summary.csv`: 48 common-evaluator size summaries.
- `01_size_resolution/per_type_metrics_long.csv`: 840 dataset/method/seed/type rows.
- `01_size_resolution/matchedK_focal_rare_long.csv`: 96 focal rare-state rows.
- `01_size_resolution/matchedK_focal_rare_summary.csv`: 32 method/type summaries.
- `01_size_resolution/matchedK_focal_rare_paired_contrasts.csv`: 24 paired GARQ-minus-baseline contrasts.

Large cell-level assignments, source H5ADs, official MetaQ metacell H5ADs, and reconstructable matrices are intentionally excluded from Git and the bundle. Server-side logs retain failed and successful retries. The ZIP contains reports, source adapters/workflows, audit/environment records, small summary tables, manifest and checksum.

## R1 Major 3 / R2 Major 5 implementation-scale unit

- `08_scalability/d13_scaling_series.csv`: five D13 seed-0 sizes through the full 161,764-cell run.
- `08_scalability/stage_profile.csv`: stage-level wall, CPU RSS and GPU allocation/reservation for the 12 corrected full GARQ runs.
- `08_scalability/training_batch_size.csv`: 24 D5/D11 training batch-size rows (256/512/1024/2048 × seeds 0–2).
- `08_scalability/training_batch_size_assignment_stability.csv`: 18 same-seed assignment-stability contrasts against batch 256.
- `08_scalability/inference_stability/D5/seed0_K002/batch_size_order_stability.csv` and the corresponding D11 file: 55 frozen-checkpoint evaluations per dataset.
- `08_scalability/D16/GARQ/full_seed0_profile_K002_retry2/metacell_size_summary.csv` and `stage_profile.csv`: corrected D16 full profile summaries.
- `R1_MAJOR3_R2_MAJOR5_SCALABILITY_REPORT.md`: dedicated PASS/FAIL evidence, exact results, safe reply wording and limitations.

Large D13 anchor traces, cell assignments and checkpoints remain server-side;
failed configurations and driver logs are preserved under the server
`revision_results/phase2/logs/` directory.

## R2 Minor Comment 4 — Figure 4b Mast analysis

Frozen-assignment deliverables are under
`fig4b/reviewer_mast_quantification/`:

- `D17_FIG4B_MAST_EXACT_REPORT.md` and `D17_FIG4B_MAST_RESPONSE_READY.tex`;
- `fig4b_mast_method_summary.csv`, `fig4b_mast_permutation_summary.csv`,
  `fig4b_mast_metacell_level.csv`, `fig4b_three_population_summary.csv`;
- `fig4b_mast_marker_validation.csv`, `fig4b_mast_top_metacells.csv`, and
  `Supplementary_Table_Fig4b_Mast.csv/.tex`;
- `Fig4b_mast_quantitative_panel.{pdf,svg,png}` and
  `FigS_mast_localized_enrichment.{pdf,svg,png}`;
- `input_inventory.csv`, `id_alignment_checks.csv`, `resolved_config.yaml`,
  `output_file_hashes.csv`, `formal_run.driver.log`, and preserved strict
  blocker evidence (`DRY_RUN.md`, `dry_run.driver.log`).

The dedicated reviewer delivery report is
`R2_MINOR4_FIG4B_MAST_REPORT.md`. MetaCell V2 and SuperCell retain realized
K=429 and K=404 under the author-approved same-compression rule; these are not
reported as exact-K=403 runs.
