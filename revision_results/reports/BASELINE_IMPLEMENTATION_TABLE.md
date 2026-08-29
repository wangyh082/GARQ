# Baseline implementation table

本表记录当前实际运行边界；未运行的官方 baseline 不以替代实现冒充。

| Method | Source/version | Input and preprocessing | K handling | Status |
|---|---|---|---|---|
| GARQ | released repository base `5da45ad`; instrumented on experiment branch | native released dense preprocessing and learned multimodal embedding | requested K; realized K reported independently | D5/D11 legacy smoke and D5/D11/D17/D18 modality smoke complete |
| KMeans | scikit-learn 1.1.3 `KMeans`, `n_init=10`, fixed seed | shared fixed representation: RNA normalize/log/HVG/PCA50; ATAC TF-IDF/LSI50 with predeclared depth-correlation rule; ADT CLR/PCA; feature standardization, per-cell L2, equal concatenation | exact requested K=40 in current smoke | D5/D11/D17/D18 seed-0 smoke complete |
| MiniBatchKMeans | scikit-learn 1.1.3 `MiniBatchKMeans`, `n_init=10`, batch size 256, fixed seed | identical fixed representation used by KMeans | exact requested K=40 in current smoke | D5/D11/D17/D18 seed-0 smoke complete |
| MetaQ | official implementation not yet recovered/installed | must preserve native pipeline and separately disclose representation | pending | BLOCKED/PENDING |
| SEACells | official implementation not yet installed | native end-to-end plus fixed-embedding adapter if compatible | pending realized-K matching | PENDING |
| MetaCell V2 | official R implementation not yet installed | native end-to-end only unless official API accepts fixed embedding | pending | PENDING |
| SuperCell | official R implementation not yet installed | native end-to-end only unless official API accepts fixed embedding | pending | PENDING |
| EpiCarousel | official implementation for DOI `10.1093/bioinformatics/btae191` not yet retrieved | ATAC-only assignments; paired RNA/ADT aggregated only after assignment | pending | PENDING for D11/D16/D17 |
| WNN | established integration control; implementation not yet configured | same selected cells and fixed preprocessing universe | pending | PENDING |
| MOFA+ | dependency/environment not yet configured | same views, factor count and seed across methods | pending | PENDING, not silently replaced |

## Current fixed-representation smoke boundary

All current runs use 2,000 uniformly selected cells, seed 0, requested K=40. Both KMeans controls realized exactly K=40. KMeans size Gini ranges 0.146–0.219; MiniBatchKMeans ranges 0.289–0.461. These are aggregation controls, not substitutes for all required official baselines and not yet a multi-seed primary benchmark.

D5 predeclared rare examples show a tradeoff: fixed-representation KMeans controls have substantially more balanced sizes than GARQ smoke, while Regulatory T cells and conventional DC each have recall/F1=0 in both KMeans controls. This negative/positive mixture is retained without method selection.

For ATAC, the first LSI component is removed only when its absolute Pearson correlation with total depth is at least 0.5: removed for D11 (`r=-0.506`) and D18 (`r=-0.626`), retained for D17 (`r=-0.389`). Full provenance is stored per run.
