# Reviewer evidence matrix — Phase 2

Status is evidence-based and may be PARTIAL.

| ID | Question | Experiment/status | Exact evidence | Safe reply | Do not claim | Paths / missing |
|---|---|---|---|---|---|---|
| R1-M1 | Metacell size range and large groups | READY FOR REPLY at primary resolution | 48 size rows, all realized K within target ±5%; cross-method median/P95/max/CV reported | We report cross-method full size distributions and outliers on corrected data. | Uniformly bounded sizes or a completed 0.01/0.05 frontier | `R1_MAJOR1_SIZE_RESOLUTION_REPORT.md`; sensitivity frontier pending |
| R1-M2 / R2-M1 | Modality dominance/shared anchors | REPLY-READY (negative/qualified) | 21 full-data modality-combination runs, 162 neighborhood rows, 9,123 anchor rows, and 36 corrected permutation/thinning runs. Full-trimodal kNN15 retention was 0.109/0.086/0.071 for RNA/ATAC/ADT; perturbation mean ARI ranged 0.037–0.215 and was often seed-sensitive. | We added full modality, neighborhood, and perturbation analyses and narrowed the claim to shared aggregation because broad fidelity/robustness was not supported. | Full trimodal superiority, uniform modality preservation, or consistent noise robustness | `reports/R2_MAJOR1_MULTIMODAL_ANCHOR_REPLY_REPORT.md`; `02_modality/d18_noise_full_summary.csv`; `02_modality/d18_modality_neighborhood_full.csv` |
| R1-M3 / R2-M5 | Dense conversion and scalability | PARTIAL | D18 peak RSS ~82.45 GB versus GPU allocation ~1.71 GB | CPU RSS, GPU allocated and GPU reserved are now reported separately. | Low total memory based on GPU-only values | `08_scalability/stage_profile.csv`; D13/D16 scaling missing |
| R1-M4 | Under/overused anchors and split terminology | PARTIAL | Correct full runs first execute local branch at step 88; no NaN/Inf | The released method repositions a fixed anchor set with usage-weighted updates. | Anchor creation/splitting | traces; matched-K schedule ablation missing |
| R1-M5 | Batch correction workflow | DEFERRED | D13/D16 identities confirmed | We clarified the intended metacell-then-common-MOFA workflow. | Improved batch correction | unified MOFA+ results missing |
| R1-M6 | scATAC-specific EpiCarousel | PARTIAL | Official 0.0.2 full D11 K=193/192 and D17 K=323/322 PASS | We added official EpiCarousel as an ATAC-derived assignment comparator. | Superiority before common biological metrics | `03_controlled_benchmark/epicarousel_*`; evaluator pending |
| R2-M2 | Representation/aggregation/K confounding | PARTIAL | 48 runs have realized K within target ±5%; SEACells/KMeans share fixed PCA/LSI/CLR; MetaQ/GARQ remain native | We distinguish fixed-representation controls from native pipelines and report requested/realized K. | Attributing all differences to aggregation | fixed-representation GARQ bypass and representation grid missing |
| R2-M3 | Kidney trajectory baseline | DEFERRED | D17 GARQ and EpiCarousel assignments ready | A common quantitative trajectory comparison is required before a GARQ-specific claim. | GARQ trajectory superiority | E6 tables missing |
| R2-M4 | D18 effect may be generic averaging | PARTIAL / MOFA+ AND RNA–PROTEIN REPLY-READY | Common 15-factor MOFA+ and 15 RNA–ADT pairs completed for GARQ/KMeans/MetaQ/SEACells × 3 seeds. SEACells had the highest mean MOFA ARI (0.656 vs GARQ 0.623); prespecified partial correlations were method-dependent. | We added matched-method downstream comparisons and do not find uniform GARQ-specific superiority. | GARQ-specific downstream advantage or non-circular association validation | `reports/R2_D18_MOFA_RNA_PROTEIN_REPLY_REPORT.md`; peak–gene, TF–gene, feature exclusion/cross-fit still missing |
| Purity | 0.5/0.7 inconsistency | COMPLETE for evaluator definitions | majority `>0.5`; high-purity `>=0.7` | Both thresholds are explicitly separated. | Treating them as interchangeable | `per_type_metrics_long.csv` |
| Mast | Undefined retained/lost | COMPLETE for requested-K evaluator | D17 Mast mean F1: GARQ 0, KMeans 0, MetaQ 0.345, SEACells 0.087 | We replace binary retained/lost with precision, recall, F1 and explicit purity criteria. | GARQ preservation or superiority | `matchedK_focal_rare_summary.csv`; trajectory pending |

## R2 Minor Comment 4 — Figure 4b Mast-cell frozen assignments

**Status: COMPLETE / REPLY-READY with author-authorized same-compression,
non-exact-K acceptance.** The canonical D17 label contains 74 Mast Cells out
of 16,143 (0.4584%). The frozen assignments used the same nominal compression
ratio (`403/16143=0.02496438`) for all methods; realized K was GARQ=403,
MetaQ=403, SEACells=403, MetaCell V2=429 and SuperCell=404. MetaCell V2 had
two partition-equivalent candidate columns (`metacell` and `membership`); the
`metacell` column was retained. SuperCell had one `metacell` column.

| method | associated recall | maximum purity | associated groups | top-3 capture | top-3 permutation P | strict majority recall |
|---|---:|---:|---:|---:|---:|---:|
| GARQ | 0.5676 | 0.3016 | 4 | 0.4865 | 0.0001 | 0 |
| MetaQ | 0.5811 | 0.2200 | 7 | 0.3784 | 0.0001 | 0 |
| SEACells | 0.2297 | 0.2727 | 5 | 0.1216 | 0.0002 | 0 |
| MetaCell V2 | 0.1622 | 0.0870 | 3 | 0.1351 | 0.0004 | 0 |
| SuperCell | 0.2297 | 0.2857 | 4 | 0.0541 | 0.3520 | 0 |

All seven pre-specified Mast markers were present and coherent in each method,
but no method reached strict majority or high-purity recovery. Safe reply:
“Mast-cell-associated metacells remained identifiable in the GARQ space;
localized enrichment and strict majority recovery varied across methods.” Do
not claim exact K=403 for MetaCell V2/SuperCell, exclusive GARQ recovery, or
GARQ superiority. Full per-metacell, permutation, marker, three-population and
figure outputs are in `fig4b/reviewer_mast_quantification/`; the dedicated
delivery report is `R2_MINOR4_FIG4B_MAST_REPORT.md`. The initial strict-K
blocker remains preserved in `dry_run.driver.log` and `DRY_RUN.md`.

## Requested-K focal rare-state verdict

The common three-seed comparison is mixed and often negative for GARQ. Mean GARQ-minus-baseline F1 includes D18 DC.Myeloid versus SEACells -0.640, D5 Treg versus KMeans -0.453, D17 Mast Cells versus MetaQ -0.345, D11 gdT versus KMeans -0.104, and D18 Platelets versus KMeans -0.048. Narrow favorable differences include D5 cDC2 versus MetaQ +0.316 and D18 Platelets versus MetaQ/SEACells +0.014/+0.018. No method recovered D18 T.DoubleNegative. Safe conclusion: requested-K evidence does not support consistent GARQ rare-state superiority.

Dataset fingerprints, config IDs, method versions, seeds and K are stored in the referenced tables, resolved configs and manifests.
