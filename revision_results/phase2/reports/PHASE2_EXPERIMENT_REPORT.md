# GARQ Phase 2 reviewer-facing experiment report

Status: **PARTIAL, substantive evidence freeze**. Results below are full-data unless explicitly called smoke. Missing Tier-1 comparisons are reported, not silently omitted.

## 1. Executive summary

Gate 0 corrected the two dataset identities that invalidated the Phase-1 biological interpretation: D5 is BMMC_batch1 (12,103 cells, RNA+ADT), and D11 is 10Xpbmc10k (9,631 cells, RNA+ATAC). All 6,600 historical files labelled D5/D11 were quarantined from manuscript biological claims. On the corrected inputs, GARQ completed 300-epoch, three-seed full-data runs for D5, D11, D17 and D18 at requested K/n=0.02. Requested/realized K stayed within 5% in all 12 runs. Official EpiCarousel 0.0.2 completed full D11 and D17 ATAC assignments after documented API/data-container compatibility shims.

The primary-resolution comparison is now realized-K matched within ±5% for GARQ, official SEACells 0.3.3, official MetaQ 1.0.6, and KMeans: 48/48 dataset-method-seed runs passed the common evaluator. MetaQ calibration used only the seed-0 requested/realized K relation and froze the mapping for seeds 1–2; no labels or biological metrics entered calibration. The rare-state evidence is mixed and frequently unfavorable to GARQ. GARQ was below KMeans/SEACells for D5 Treg, below MetaQ/SEACells for D17 Mast Cells, and below KMeans/SEACells for D18 DC.Myeloid; no method recovered D18 T.DoubleNegative. Full-length GARQ runs show the local anchor branch first executes at quantized step 88. D18 GARQ is computationally feasible but CPU-memory-heavy (about 82.45 GB peak RSS per seed), while peak GPU allocation was about 1.71 GB.

The Figure 4b Mast-cell frozen-assignment analysis for R2 Minor Comment 4 is
now complete under an explicit author override: all methods used the same
nominal compression input, while the realized K values are GARQ=403,
MetaQ=403, SEACells=403, MetaCell V2=429 and SuperCell=404. The exact D17
Mast count is 74/16,143 (0.4584%). GARQ associated recall was 0.5676 and its
maximum purity was 0.3016, but strict majority and high-purity recovery were
zero; MetaQ, SEACells, MetaCell V2 and SuperCell likewise had zero strict
majority recovery. The only-GARQ interpretation is not supported; the
review-safe outcome is that Mast-cell-associated metacells were identifiable
but enrichment and strict recovery varied by method. The report, response
draft, tables, figures, non-exact-K rationale and preserved strict-audit
failure evidence are under `fig4b/reviewer_mast_quantification/` and the
dedicated `R2_MINOR4_FIG4B_MAST_REPORT.md`.

The implementation-scale delivery unit for R1 Major 3 and R2 Major 5 is also
complete at a qualified implementation level. A five-point, one-seed D13
series reaches the full 161,764-cell dataset; a corrected D16 full profile,
four training batch sizes × three seeds on D5/D11, and 110 frozen-checkpoint
inference batch/order evaluations are all PASS. The results expose
non-monotonic size tails and sensitivity to the released batch-local graph,
so they support execution feasibility and explicit memory reporting, not a
claim of uniform scalability or batch/order invariance. See
`R1_MAJOR3_R2_MAJOR5_SCALABILITY_REPORT.md`.

## 2. Git, environments and hardware

- Base commit: `5da45adcd62f1be8ee318d8742c80c59cb242ca2`.
- Phase 1 commit: `cfaf79bdcbc26840b6cbf67e3531d6fab6540a09`.
- Phase 2 branch: `revision/major-review-experiments-phase2`.
- Gate-0 Phase 2 commit: `59d295dddda624b43f01ca89c31c4209e70e2b5c`.
- GARQ environment: Conda `MetqQ2`; final server test suite: 43 passed, 13 warnings (the earlier 28-test checkpoint is retained in historical reports).
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

Official SEACells 0.3.3 and MetaQ 1.0.6 completed D5/D11/D17/D18 × seeds 0–2. KMeans completed the same 12 cells of the design. All used requested K/n=0.02 and the fixed equal-weight representation; all assignments were evaluated by the common evaluator. SEACells needed a writable, C-contiguous numerical copy because full-data NNDescent rejects read-only mmap input; the initial failures are retained. MetaQ required an explicit package-directory import shim, absolute input resolution before its output-directory `chdir`, creation of its expected `figures/` directory, and omission of a broken label-only plotting path; labels were used only by the external evaluator. Row-order cell-ID restoration was accepted only after invariant paired-order checks, including D18 canonicalization. MetaQ D5's first batch status is nonzero solely because an empty metadata path was passed after successful assignment; separate evaluator recoveries all passed and the original evidence remains. Official EpiCarousel 0.0.2 passed a correct-D11 2,000-cell smoke and full D11/D17. MetaCell 0.9.5 and MOFA+ 0.7.2 import, but confirmatory results remain pending. SuperCell remains uninstalled. Separately, the Figure 4b frozen MetaCell V2 and SuperCell files were quantified under the author-approved same-compression rule (realized K=429 and 404); these are not exact-K baseline training runs.

## 6. Fairness and preregistration

Primary resolution is requested K/n=0.02. Labels do not enter GARQ training or K calibration. All seeds and negative outcomes are retained. Pipeline-level and fixed-representation comparisons are kept distinct. EpiCarousel uses ATAC alone for assignment. Majority retention is purity >0.5 and high-purity recovery is purity >=0.7.

## 7. Methods P2-E1–E8

- E1: full-data instrumented legacy GARQ plus requested-K matched SEACells, MetaQ and fixed-representation KMeans, seeds 0–2, K/n=0.02 on corrected D5/D11/D17/D18; common assignment, size and per-type evaluator (48/48 runs).
- E2: block contribution traces were exported for all 12 core GARQ runs. The corrected D18 extension is now complete for seven modality combinations × three seeds, 162 neighborhood/homogeneity rows, 9,123 anchor-level compactness rows, and 36 valid full-data permutation/thinning runs. The initial RNA-permutation seeds 0/1 were invalid because perturbations were silently skipped at full size; their evidence is preserved and excluded, and the compatibility-equivalent corrected grid is reported separately.
- E3: fixed-representation SEACells/KMeans and official MetaQ controls on four datasets, with all realized K within target ±5%, plus official EpiCarousel full ATAC assignments for D11/D17. The 0.01/0.05 frontiers remain pending.
- E4: full-length legacy traces establish actual branch execution; matched-K schedule variants remain pending.
- E5: registry mapping is complete; unified MOFA+ multi-batch runs are pending.
- E6: D17 assignments exist for GARQ and EpiCarousel; common Slingshot/UCell comparison is pending.
- E7: D18 GARQ assignments exist for three seeds; MOFA+ and cross-fit held-out analyses are pending.
- E8: stage-level wall, CPU RSS and GPU allocation/reservation were recorded for all 12 GARQ runs; the D13 five-point scaling series, corrected D16 full profile, D5/D11 training batch-size grid and frozen-checkpoint inference order diagnostic are complete. Sparse-safe/global-graph equivalence and the unified D13–D16 batch-integration benchmark remain pending.

## 8. Results P2-E1–E8

Twelve GARQ runs passed. D5 realized K=237/239/236 for requested 242; D11=193/193/193 for requested 193; D17=323/323/323 for requested 323; D18=497/493/486 for requested 510. D17 seed0 size median/P95/max was 53/72.9/85. D18 seed0 was 49/91/572, showing a long upper tail; seed2 max was 988.

Rare results: D5 Treg abundance 0.1652%, F1=0 for all seeds; D5 cDC2 F1=0.868/0.847/0.857. D11 Plasma abundance 0.1246%, F1=1/0/1; gdT F1=0.729/0.665/0.602. D17 Mast Cells abundance 0.4584%, F1=0 and no majority/high-purity recovery for all seeds. D18 seed0 T.DoubleNegative and DC.Myeloid F1=0; Platelets F1=0.803 and seed1 0.814.

Across three seeds, mean focal F1 (GARQ / KMeans / realized-K-calibrated MetaQ / SEACells) was: D5 Treg 0 / 0.453 / 0 / 0.365; D5 cDC2 0.858 / 0.880 / 0.769 / 0.853; D11 Plasma 0.667 / 0.333 / 0.959 / 0.907; D11 gdT 0.665 / 0.769 / 0.711 / 0.724; D17 Mast Cells 0 / 0 / 0.345 / 0.087; D18 DC.Myeloid 0 / 0.222 / 0 / 0.640; D18 Platelets 0.794 / 0.842 / 0.791 / 0.775; and D18 T.DoubleNegative 0 for all methods. These are descriptive paired three-seed realized-K-within-±5% comparisons, not inferential evidence. GARQ was modestly above MetaQ for D5 cDC2 (+0.088) and nearly identical for D18 Platelets (+0.003); negative contrasts include D18 DC.Myeloid versus SEACells (-0.640), D5 Treg versus KMeans (-0.453), D17 Mast Cells versus MetaQ (-0.345), and D11 Plasma versus MetaQ (-0.292).

All corrected full-length runs first executed the local anchor branch at quantized step 88 and recorded no anchor NaN/Inf. Therefore the Phase-1 35-step observation was a short-run limitation, not evidence that the branch never executes.

D5 wall time was 1,066–1,088 s and peak RSS about 5.43 GB. D11 wall was 965–999 s and peak RSS about 22.86 GB. D17 seed0 wall was 1,501 s and peak RSS 24.93 GB. D18 seeds 0/1 wall was 3,506/3,488 s and peak RSS about 82.45 GB. Peak GPU allocation was approximately 0.23 GB on D5 and 1.71–1.77 GB on the larger modalities; CPU RSS is the limiting memory quantity.

Sources: `revision_results/phase2/01_size_resolution/full_benchmark_long.csv`, `metacell_size_summary.csv`, `per_type_metrics_long.csv`, `revision_results/phase2/02_modality/modality_block_contribution_full.csv`, and `revision_results/phase2/08_scalability/stage_profile.csv`. Config IDs and fingerprints are in resolved configs/manifests.

Implementation-scale results are reported in the dedicated R1 Major 3/R2
Major 5 unit. D13 (seed 0) completed at 10k/25k/50k/100k/full with realized
K 200/472/762/1,999/3,234 and peak CPU RSS 13.3/32.0/63.2/125.7/202.9 GiB;
the 50k point had 238 empty anchors and Gini 0.670, whereas the full point
had one empty anchor and Gini 0.107. D16 corrected full seed 0 completed at
K=645/645 with 207.84 GiB peak CPU RSS during preprocessing and 1.58/2.29 GB
peak GPU allocated/reserved memory during inference. D5/D11 batch-size means
show GPU reserved memory rising to 2.106/17.895 GB at batch 2048, while mean
membership ARI versus batch 256 remained low (D5 0.1302; D11 0.0412). At
inference batch 1,024, cell-order permutations produced mean ARI 0.5746 on
D5 and 0.6942 on D11. These exact values support a qualified
implementation-level scalability statement and a negative batch/order
invariance finding; they do not establish biological quality or a global-graph
solution.

## 9. Negative results and uncertainty

Rare-state recovery is not consistently positive, and the realized-K-within-±5% baselines directly contradict a broad GARQ superiority claim. D5 seed1/2 used an incorrect evaluation label key; training was label-blind and unchanged, and all 12,103 IDs were matched for post-hoc evaluator correction. Baseline failures and compatibility retries were retained. EpiCarousel required documented compatibility shims and its native pipeline is not a fixed-representation comparison. D18 CPU memory is high. Representation remains partly confounded because GARQ and MetaQ are native pipelines while KMeans and SEACells share the fixed representation.

## 10. Central claim verdicts

- Rare-state preservation: **NOT SUPPORTED as a broad superiority claim** by the realized-K-within-±5% four-method comparison; results are cell-type dependent and often favor a baseline. Full rare-state subsampling is still missing.
- Multimodal fidelity: **NOT SUPPORTED as a strong robustness claim**; the completed full-data modality and perturbation grids show limited within-anchor neighbor retention, very low cross-modality kNN overlap, and low or strongly seed-dependent perturbation ARI. The narrower statement that GARQ produces a shared multimodal aggregation is supported.
- Scalability: **PARTIALLY_SUPPORTED (implementation-level)**. D13 five-point scaling, corrected D16 full profiling and D5/D11 batch/order diagnostics are complete, but the series is non-monotonic, one-seed, and CPU-memory-heavy; sparse-safe/global-graph equivalence and unified batch integration remain missing.
- GARQ-specific downstream advantage: **INCONCLUSIVE**; D17 trajectory and D18 held-out cross-fit comparisons are not complete.

## 11. Reviewer-comment evidence

R1 size questions are directly addressed by 12 full runs and size tables. R1-M2/R2-M1 modality questions now have a completed corrected D18 modality grid, neighborhood/homogeneity evaluation, and perturbation grid; the reply must report the negative/qualified robustness finding. Dense-conversion concerns are supported by stage profiles, the D13 scaling series and D16 full profile; the reply must distinguish CPU RSS from GPU allocation/reservation and report the non-monotonic 25k/50k behavior. R1-M3/R2-M5 are reply-ready with this qualified implementation-level evidence, while R1-M5 remains partial because unified batch integration is not complete. Anchor terminology is corrected to “continuous usage-weighted repositioning of a fixed anchor set”; full runs show first local execution at step 88. EpiCarousel is now represented by official full D11/D17 assignments. Kidney trajectory and D18 specificity remain open. See the evidence matrix, `R1_MAJOR3_R2_MAJOR5_SCALABILITY_REPORT.md` and `R2_MAJOR1_MULTIMODAL_ANCHOR_REPLY_REPORT.md` for reply-safe wording.

## 12. Candidate manuscript changes

Correct D5/D11 identities everywhere; remove Phase-1 biological numbers derived from the wrong mappings. Replace “split/create anchors” with the operational term above. Define CPU RSS separately from GPU allocation. Avoid “consistently preserves rare states” and any downstream-superiority statement until matched-K baselines and held-out comparisons are complete. Report the D18 metacell-size upper tail.

## 13. Blockers and deferred work

Completed Tier-1 items include primary-resolution realized-K-within-±5% GARQ/SEACells/MetaQ/KMeans on corrected D5/D11/D17/D18 (three seeds; 48/48 common-evaluator passes) and the qualified R1-M3/R2-M5 implementation-scale unit (D13 five-point series, D16 full profile, D5/D11 training batch-size and inference order diagnostics). Deferred Tier-1 items are focal full-data subsampling, 0.01/0.05 resolution frontiers, matched-K full E4 variants, D17 trajectory, D18 MOFA+/cross-fit, sparse-safe/global-graph equivalence, and the unified D13–D16 batch-integration benchmark. Details and package failures are in `BLOCKED_OR_DEFERRED_PHASE2.md` and `FAILURE_LOG_PHASE2.md`.

## 14. Reproducibility commands

Run tests with `python -m pytest -q revision_exp/tests`. GARQ runs use `python -m revision_exp.run --config <resolved Phase-2 config>`. Baselines use `revision_exp.workflows.matched_baseline_fixed` plus the official adapters; rebuild the combined tables with `python -m revision_exp.workflows.summarize_matched_baselines`. Commands and stderr, including failed retries, are preserved under `revision_results/phase2/logs/`.

## 15. File index

See `revision_results/phase2/reports/RESULT_FILE_INDEX_PHASE2.md` and `revision_results/phase2/manifests/run_manifest_phase2.json`.
