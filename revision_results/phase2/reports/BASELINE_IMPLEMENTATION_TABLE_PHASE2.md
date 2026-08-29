# Baseline Implementation Table — Phase 2

Audit date: 2026-08-29

| Method | Official source/package | Version | Environment | Gate status | Notes |
|---|---|---:|---|---|---|
| GARQ | repository under revision | Phase 1 `cfaf79b` | `MetqQ2` | PASS | Full tests: 28 passed, 13 warnings. |
| MetaQ | `XLearning-SCU/MetaQ`, package `metaq-sc` | 1.0.6 | `MetqQ2` | IMPORT PASS; correct-data smoke pending | Existing `MetaQ` env has NumPy/Pandas ABI failures and is not used. |
| SEACells | `dpeerlab/SEACells` | 0.3.3 | `seacells` | IMPORT PASS; correct-data smoke pending | Official PyPI/source implementation. |
| EpiCarousel | `BioX-NKU/EpiCarousel`, PyPI `epicarousel` | 0.0.2 | project `.venvs/epicarousel_py311` | D11 correct-data smoke PASS | Official ATAC construction; 2,000 cells, requested/realized K=40, wall 28.60 s, peak RSS 888,652 KiB. Compatibility-only adapter is disclosed below. |
| MetaCell V2 | Python package `metacells` | 0.9.5 | `metacells2` | IMPORT PASS; smoke pending | Native/end-to-end comparison only where appropriate. |
| SuperCell | `GfellerLab/SuperCell` | — | — | NOT INSTALLED | Installation deferred until primary Tier 1 baselines are complete. |
| MOFA+ | `bioFAM/mofapy2` | 0.7.2 | `mofa` | IMPORT PASS; fit smoke pending | Same configuration will be used across assignments. |

## EpiCarousel compatibility disclosure

The PyPI package is the official implementation. Two compatibility-only changes were required; neither changes feature preprocessing, Walktrap construction, aggregation, or parameters:

1. SnapATAC2 2.9 returns `obs`/`var` as Polars DataFrames, whereas EpiCarousel 0.0.2 assumes an older orientation. The adapter converts them to Pandas without changing values or order.
2. NumPy removed `np.int`/`np.float`; these aliases were replaced by the equivalent built-in `int`/`float` in the installed launcher. Patched launcher SHA256: `83233fb9d8910662ca885a9b4ff6859a4bc0511f8482411567db26fd2ff5e357`.

Adapter: `revision_exp/methods/epicarousel_adapter.py`.

Smoke evidence: `revision_results/phase2/baseline_smoke/epicarousel_D11_adapter/summary.json`. After assignment export and verification, the reproducible 35 MiB subset H5AD and 590 MiB of duplicate/intermediate EpiCarousel H5AD files were removed to respect the project storage budget; cell IDs, assignments, parameters, fingerprints, and summary remain.
