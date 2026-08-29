# Reviewer evidence matrix — Phase 2

Status is evidence-based and may be PARTIAL.

| ID | Question | Experiment/status | Exact evidence | Safe reply | Do not claim | Paths / missing |
|---|---|---|---|---|---|---|
| R1-M1 | Metacell size range and large groups | PARTIAL: 12 full GARQ runs | D17 seed0 median/P95/max 53/72.9/85; D18 seed0 49/91/572 | We now report full size distributions and outliers for corrected full-data runs. | Uniformly bounded sizes; cross-method advantage | `01_size_resolution/metacell_size_summary.csv`; baseline size tables missing |
| R1-M2 / R2-M1 | Modality dominance/shared anchors | PARTIAL | 27 block-contribution rows across 12 runs; full grids pending | We instrumented modality contributions and will limit interpretation to measured blocks. | Natural equal weighting or robust shared fidelity | `02_modality/modality_block_contribution_full.csv`; perturbation/grid missing |
| R1-M3 / R2-M5 | Dense conversion and scalability | PARTIAL | D18 peak RSS ~82.45 GB versus GPU allocation ~1.71 GB | CPU RSS, GPU allocated and GPU reserved are now reported separately. | Low total memory based on GPU-only values | `08_scalability/stage_profile.csv`; D13/D16 scaling missing |
| R1-M4 | Under/overused anchors and split terminology | PARTIAL | Correct full runs first execute local branch at step 88; no NaN/Inf | The released method repositions a fixed anchor set with usage-weighted updates. | Anchor creation/splitting | traces; matched-K schedule ablation missing |
| R1-M5 | Batch correction workflow | DEFERRED | D13/D16 identities confirmed | We clarified the intended metacell-then-common-MOFA workflow. | Improved batch correction | unified MOFA+ results missing |
| R1-M6 | scATAC-specific EpiCarousel | PARTIAL | Official 0.0.2 full D11 K=193/192 and D17 K=323/322 PASS | We added official EpiCarousel as an ATAC-derived assignment comparator. | Superiority before common biological metrics | `03_controlled_benchmark/epicarousel_*`; evaluator pending |
| R2-M2 | Representation/aggregation/K confounding | DEFERRED | Native EpiCarousel and GARQ are explicitly pipeline-level | We distinguish native pipelines from fixed-representation aggregation controls. | Attributing all differences to aggregation | fixed-representation full table missing |
| R2-M3 | Kidney trajectory baseline | DEFERRED | D17 GARQ and EpiCarousel assignments ready | A common quantitative trajectory comparison is required before a GARQ-specific claim. | GARQ trajectory superiority | E6 tables missing |
| R2-M4 | D18 effect may be generic averaging | DEFERRED | Three-seed GARQ assignments and resource profiles complete | We do not yet attribute downstream gains specifically to GARQ. | GARQ-specific downstream advantage | MOFA+/cross-fit missing |
| Purity | 0.5/0.7 inconsistency | COMPLETE for evaluator definitions | majority `>0.5`; high-purity `>=0.7` | Both thresholds are explicitly separated. | Treating them as interchangeable | `per_type_metrics_long.csv` |
| Mast | Undefined retained/lost | PARTIAL | D17 Mast 0.4584%; F1 and majority/high-purity all zero across 3 GARQ seeds | We replace binary retained/lost with precision, recall, F1 and purity criteria. | Preservation of Mast Cells | matched-K baseline and trajectory pending |

Dataset fingerprints, config IDs, method versions, seeds and K are stored in the referenced tables, resolved configs and manifests.
