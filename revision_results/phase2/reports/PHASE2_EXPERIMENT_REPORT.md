# GARQ Phase 2 reviewer-facing experiment report

Status: **PARTIAL, substantive evidence freeze**. Results below are full-data unless explicitly called smoke. Missing Tier-1 comparisons are reported, not silently omitted.

## 1. Executive summary

Gate 0 corrected the two dataset identities that invalidated the Phase-1 biological interpretation: D5 is BMMC_batch1 (12,103 cells, RNA+ADT), and D11 is 10Xpbmc10k (9,631 cells, RNA+ATAC). All 6,600 historical files labelled D5/D11 were quarantined from manuscript biological claims. On the corrected inputs, GARQ completed 300-epoch, three-seed full-data runs for D5, D11, D17 and D18 at requested K/n=0.02. Requested/realized K stayed within 5% in all 12 runs. Official EpiCarousel 0.0.2 completed full D11 and D17 ATAC assignments after documented API/data-container compatibility shims.

The current rare-state evidence is negative or unstable rather than uniformly favorable: D5 Treg and D17 Mast Cells had cell-level majority F1=0 in all three seeds; D11 Plasma varied 1/0/1. This is GARQ-only evidence pending matched-K SEACells, MetaQ and KMeans comparisons, so it does not support superiority. Full-length GARQ runs show the local anchor branch first executes at quantized step 88, correcting the earlier 35-step smoke interpretation. D18 is computationally feasible but CPU-memory-heavy (about 82.45 GB peak RSS per seed), while peak GPU allocation was about 1.71 GB.

## 2. Git, environments and hardware

- Base commit: `5da45adcd62f1be8ee318d8742c80c59cb242ca2`.
- Phase 1 commit: `cfaf79bdcbc26840b6cbf67e3531d6fab6540a09`.
- Phase 2 branch: `revision/major-review-experiments-phase2`.
- Gate-0 Phase 2 commit: `59d295dddda624b43f01ca89c31c4209e70e2b5c`.
- GARQ environment: Conda `MetqQ2`; tests: 28 passed, 13 warnings.
- EpiCarousel: official PyPI 0.0.2 in isolated Python 3.11 venv.
- Server: 2 × NVIDIA RTX 4090 (24,564 MiB each), 503 GiB RAM. Jobs were limited to one project-heavy process per GPU.

Source: `revision_results/phase2/environments/`, run manifests and `revision_results/phase2/08_scalability/stage_profile.csv`.

## 3. Dataset identity audit

D5 is `/home/zhangpeiru/data/RNA+ADT/D8/D8_rna.h5ad` plus `D8_adt.h5ad`, shapes 12,103×9,786 and 12,103×25. D11 is `/home/zhangpeiru/data/RNA+ATAC/pbmc10k/10x-Multiome-Pbmc10k-RNA.h5ad` plus the paired ATAC file, shapes 9,631×29,095 and 9,631×107,194. D13, D16, D17 and D18 were also confirmed. Sampled X values were nonnegative integer-like counts; paired row hashes passed. D18 used the preregistered terminal-dot-to-hyphen ADT ID canonicalization.

Source: `revision_results/phase2/audit/DATASET_IDENTITY_AUDIT_PHASE2.md`, `data_inventory.csv`, `INPUT_MATRIX_PROVENANCE.csv`; fingerprints are recorded there and in every run manifest.

## 4. Phase-1 D5/D11 validity correction

The Phase-1 registry mapped D5 to an 8,670-cell dataset and D11 to a 9,876-cell GSE194122 dataset. These do not match the authoritative D5/D11 definitions. The audit classified 6,600 historical paths as invalid for the corresponding manuscript biological claim, while retaining reusable code-behavior evidence. No historical results were silently relabelled.

Source: `revision_results/phase2/audit/phase1_result_validity.csv`.

## 5. Baseline versions

Official EpiCarousel 0.0.2 passed a correct-D11 2,000-cell smoke (K=40) and full D11/D17. Full D17 requested/realized K was 323/322; full D11 was 193/192. Compatibility changes were restricted to SnapATAC2 Polars conversion, dense-chunk to numerically equivalent CSR, NumPy removed aliases, and an anonymous metadata frame when SnapATAC2 could not decode a valid int8 H5AD scalar column. Assignments are exported against source H5AD cell IDs. SEACells 0.3.3, MetaCell 0.9.5 and MOFA+ 0.7.2 import successfully in isolated environments but confirmatory results are pending. Official MetaQ 1.0.6 has a package absolute-import defect; an explicit import shim is required. SuperCell remains uninstalled.

## 6. Fairness and preregistration

Primary resolution is requested K/n=0.02. Labels do not enter GARQ training or K calibration. All seeds and negative outcomes are retained. Pipeline-level and fixed-representation comparisons are kept distinct. EpiCarousel uses ATAC alone for assignment. Majority retention is purity >0.5 and high-purity recovery is purity >=0.7.

## 7. Methods P2-E1–E8

- E1: full-data instrumented legacy GARQ, 300 epochs, seeds 0–2, K/n=0.02 on corrected D5/D11/D17/D18; common assignment, size and per-type evaluator.
- E2: block contribution traces were exported for all 12 runs; the full modality grid and perturbation grid remain pending.
- E3: official EpiCarousel full ATAC assignments for D11/D17; matched-K biological evaluation and other baselines remain pending.
- E4: full-length legacy traces establish actual branch execution; matched-K schedule variants remain pending.
- E5: registry mapping is complete; unified MOFA+ multi-batch runs are pending.
- E6: D17 assignments exist for GARQ and EpiCarousel; common Slingshot/UCell comparison is pending.
- E7: D18 GARQ assignments exist for three seeds; MOFA+ and cross-fit held-out analyses are pending.
- E8: stage-level wall, CPU RSS and GPU allocation/reservation were recorded for all 12 GARQ runs; D13/D16 scaling series is pending.

## 8. Results P2-E1–E8

Twelve GARQ runs passed. D5 realized K=237/239/236 for requested 242; D11=193/193/193 for requested 193; D17=323/323/323 for requested 323; D18=497/493/486 for requested 510. D17 seed0 size median/P95/max was 53/72.9/85. D18 seed0 was 49/91/572, showing a long upper tail; seed2 max was 988.

Rare results: D5 Treg abundance 0.1652%, F1=0 for all seeds; D5 cDC2 F1=0.868/0.847/0.857. D11 Plasma abundance 0.1246%, F1=1/0/1; gdT F1=0.729/0.665/0.602. D17 Mast Cells abundance 0.4584%, F1=0 and no majority/high-purity recovery for all seeds. D18 seed0 T.DoubleNegative and DC.Myeloid F1=0; Platelets F1=0.803 and seed1 0.814.

All corrected full-length runs first executed the local anchor branch at quantized step 88 and recorded no anchor NaN/Inf. Therefore the Phase-1 35-step observation was a short-run limitation, not evidence that the branch never executes.

D5 wall time was 1,066–1,088 s and peak RSS about 5.43 GB. D11 wall was 965–999 s and peak RSS about 22.86 GB. D17 seed0 wall was 1,501 s and peak RSS 24.93 GB. D18 seeds 0/1 wall was 3,506/3,488 s and peak RSS about 82.45 GB. Peak GPU allocation was approximately 0.23 GB on D5 and 1.71–1.77 GB on the larger modalities; CPU RSS is the limiting memory quantity.

Sources: `revision_results/phase2/01_size_resolution/full_benchmark_long.csv`, `metacell_size_summary.csv`, `per_type_metrics_long.csv`, `revision_results/phase2/02_modality/modality_block_contribution_full.csv`, and `revision_results/phase2/08_scalability/stage_profile.csv`. Config IDs and fingerprints are in resolved configs/manifests.

## 9. Negative results and uncertainty

Rare-state recovery is not consistently positive. The current comparison lacks matched-K SEACells, MetaQ and KMeans, so no method-superiority statement is licensed. D5 seed1/2 used an incorrect evaluation label key; training was label-blind and unchanged, and all 12,103 IDs were matched for post-hoc evaluator correction. EpiCarousel required documented compatibility shims and its native pipeline is not a fixed-representation comparison. D18 CPU memory is high. No unfavorable run was removed.

## 10. Central claim verdicts

- Rare-state preservation: **INCONCLUSIVE**; full-data three-seed GARQ is mixed/negative and matched-K baselines are missing.
- Multimodal fidelity: **INCONCLUSIVE**; block diagnostics exist but the full modality/perturbation grid is missing.
- Scalability: **PARTIALLY_SUPPORTED** for execution on D5/D11/D17/D18, but D13/D16 scaling and sparse-safe comparison are missing; CPU memory must be stated explicitly.
- GARQ-specific downstream advantage: **INCONCLUSIVE**; D17 trajectory and D18 held-out cross-fit comparisons are not complete.

## 11. Reviewer-comment evidence

R1 size questions are directly addressed by 12 full runs and size tables. R1/R2 modality questions currently have diagnostic block traces but not sufficient confirmatory perturbations. Dense-conversion concerns are supported by stage profiles and D18 RSS. Anchor terminology is corrected to “continuous usage-weighted repositioning of a fixed anchor set”; full runs show first local execution at step 88. EpiCarousel is now represented by official full D11/D17 assignments. Kidney trajectory and D18 specificity remain open. See the evidence matrix for reply-safe wording.

## 12. Candidate manuscript changes

Correct D5/D11 identities everywhere; remove Phase-1 biological numbers derived from the wrong mappings. Replace “split/create anchors” with the operational term above. Define CPU RSS separately from GPU allocation. Avoid “consistently preserves rare states” and any downstream-superiority statement until matched-K baselines and held-out comparisons are complete. Report the D18 metacell-size upper tail.

## 13. Blockers and deferred work

Deferred Tier-1 items are matched-K SEACells/MetaQ/KMeans, focal full-data subsampling, matched-K E4 variants, D17 trajectory, D18 MOFA+/cross-fit, and D13/D16 full profile. Details and package failures are in `BLOCKED_OR_DEFERRED_PHASE2.md` and `FAILURE_LOG_PHASE2.md`.

## 14. Reproducibility commands

Run tests with `python -m pytest -q revision_exp/tests`. GARQ runs use `python -m revision_exp.run --config <resolved Phase-2 config>`. Rebuild summaries with `python revision_exp/workflows/summarize_phase2_full.py`. EpiCarousel commands and stderr are preserved under `revision_results/phase2/logs/`.

## 15. File index

See `revision_results/phase2/reports/RESULT_FILE_INDEX_PHASE2.md` and `revision_results/phase2/manifests/run_manifest_phase2.json`.
