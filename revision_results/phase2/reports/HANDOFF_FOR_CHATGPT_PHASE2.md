# GARQ Phase 2 handoff for ChatGPT

## First-page facts

- Status: **PARTIAL substantive evidence freeze**.
- Base: `5da45adcd62f1be8ee318d8742c80c59cb242ca2`.
- Phase 1: `cfaf79bdcbc26840b6cbf67e3531d6fab6540a09`.
- Phase 2 branch: `revision/major-review-experiments-phase2`; final delivery commit is recorded in the manifest.
- Correct D5: `/home/zhangpeiru/data/RNA+ADT/D8/D8_rna.h5ad` + `D8_adt.h5ad`; fingerprints in `audit/data_inventory.csv`.
- Correct D11: `/home/zhangpeiru/data/RNA+ATAC/pbmc10k/10x-Multiome-Pbmc10k-RNA.h5ad` + ATAC counterpart; fingerprints in the same audit.
- Invalidated Phase-1 evidence: 6,600 historical D5/D11-labelled file rows are excluded from corresponding manuscript biological claims.
- Completed P0/Tier-1 components: Gate 0, quarantine, tests, corrected full GARQ D5/D11/D17/D18 ×3 seeds, requested-K matched official SEACells/MetaQ and KMeans ×3 seeds (48/48 common-evaluator passes), official EpiCarousel full D11/D17, combined size/per-type summaries, the qualified R1 Major 3/R2 Major 5 implementation-scale unit (D13 five-point series, D16 full profile, D5/D11 training batch-size and inference order diagnostics), and the R2 Minor 4 Figure 4b frozen-assignment Mast analysis under the author-approved same-compression/non-exact-K rule.
- Missing: 0.01/0.05 resolution frontiers, focal full-data subsampling, matched-K full E4 variants, D17 common trajectory, D18 MOFA+/held-out cross-fit, sparse-safe/global-graph equivalence, and the unified D13–D16 batch-integration benchmark.

## Twenty most important results/checks

1. D5 is BMMC_batch1 with 12,103 cells, not the Phase-1 8,670-cell mapping.
2. D11 is 10Xpbmc10k with 9,631 cells, not GSE194122 with 9,876 cells.
3. D5/D11 modality row hashes pass; sampled X is count-like.
4. All 6,600 Phase-1 D5/D11 file rows are quarantined from corresponding biological claims.
5. Corrected full GARQ completed 12/12 runs, 300 epochs each.
6. D5 realized K is 237/239/236 from requested 242.
7. D11 realized K is 193/193/193 from requested 193.
8. D17 realized K is 323/323/323 from requested 323.
9. D18 realized K is 497/493/486 from requested 510; all remain within 5%.
10. D5 Treg abundance is 0.1652% and F1 is zero in all three seeds.
11. D5 cDC2 F1 is 0.868/0.847/0.857.
12. D11 Plasma F1 is 1/0/1, demonstrating seed instability.
13. D11 gdT F1 is 0.729/0.665/0.602.
14. D17 Mast Cells abundance is 0.4584%; F1 and strict recovery are zero in all three seeds.
15. D18 Platelets F1 is 0.803/0.814 for seeds 0/1; two other rare labels have seed0 F1 zero.
16. Full-length runs first execute the local anchor branch at quantized step 88.
17. No anchor NaN/Inf was recorded in corrected full runs.
18. D18 seed0 size median/P95/max is 49/91/572, a substantial upper tail.
19. D18 peak CPU RSS is about 82.45 GB, while peak GPU allocation is about 1.71 GB.
20. Requested-K focal rare-state evidence does not show consistent GARQ superiority: large negative mean-F1 contrasts include DC.Myeloid vs SEACells -0.640, Treg vs KMeans -0.453, and Mast Cells vs MetaQ -0.345; cDC2 vs MetaQ is favorable at +0.316.

21. Figure 4b R2 Minor 4 used the exact D17 Mast count (74/16,143) and the
author-approved nominal compression input. Realized K was 403/403/403/429/404
for GARQ/MetaQ/SEACells/MetaCell V2/SuperCell. GARQ associated recall was
0.5676 and maximum purity 0.3016; strict majority recovery was zero for every
method, so only-GARQ support is not supported.

22. R1 Major 3/R2 Major 5 implementation-scale unit: D13 five-point seed-0
scaling completed through 161,764 cells; D16 corrected full profile completed
at K=645/645; D5/D11 training batch-size and frozen-checkpoint inference
diagnostics all passed. D13 full peak CPU RSS was ~202.9 GiB; D16 was ~207.84
GiB during preprocessing. Mean permutation ARI at inference batch 1,024 was
0.575 (D5) and 0.694 (D11), so the batch-local graph is not order-invariant.

Official EpiCarousel full D11 and D17 also pass at realized K 192 and 322 respectively, with documented compatibility shims. All 12 SEACells, 12 MetaQ and 12 KMeans corrected-data baseline runs passed the common evaluator. No method recovered D18 T.DoubleNegative in any seed.

## Four claim verdicts

- Rare-state preservation: **NOT SUPPORTED as a broad superiority claim** by requested-K four-method evidence; results are cell-type dependent. Realized-K and subsampling analyses remain incomplete.
- Multimodal fidelity: **INCONCLUSIVE**, because full modality and perturbation grids remain absent.
- Scalability: **PARTIALLY_SUPPORTED (implementation-level)**. D13/D16 and D5/D11 batch/order diagnostics are present, but the series is non-monotonic and one-seed for D13/D16; CPU memory is substantial and unified batch integration/global-graph equivalence remains absent.
- GARQ-specific downstream advantage: **INCONCLUSIVE**, pending kidney trajectory and D18 held-out analysis.

## Disputes and required checks

Check that manuscript terminology never says anchors are created/split. Check all memory claims distinguish CPU RSS, GPU allocated and GPU reserved. Keep the D13 25k/50k empty-anchor and size-tail instability visible and do not claim linear or uniform scaling. Treat R1-M3/R2-M5 as qualified implementation-level evidence only. Check D5 seed1/2 label-key correction language: training/assignments were unchanged because labels are evaluator-only; 12,103 IDs matched. Check that native EpiCarousel is described as pipeline-level and that all compatibility shims for EpiCarousel, SEACells and MetaQ are disclosed. For Figure 4b, keep MetaCell V2/SuperCell realized K=429/404 visible and do not call them exact-K=403. Do not transform requested-K matching into realized-K matching or the negative/mixed evidence into a superiority conclusion.

## Key files

Read `PHASE2_EXPERIMENT_REPORT.md`, `REVIEWER_EVIDENCE_MATRIX_PHASE2.md`, `R1_MAJOR3_R2_MAJOR5_SCALABILITY_REPORT.md`, `R2_MINOR4_FIG4B_MAST_REPORT.md`, audit tables, `01_size_resolution/*.csv`, `08_scalability/`, `fig4b/reviewer_mast_quantification/`, failures and the manifest. Large assignments and raw data are intentionally excluded from Git/bundle.
