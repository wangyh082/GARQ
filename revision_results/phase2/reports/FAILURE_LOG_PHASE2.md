# Failure Log — Phase 2

Failures are retained; none is silently removed from method tables.

## Source review

- The supplied reviewer DOCX ends mid-sentence at `clearly distinguishable co`; Word rendering confirmed this is the source-file ending. No missing words were inferred.

## Test environment selection

- Base environment: test collection failed because `torch` and `anndata` are absent.
- Existing `MetaQ` environment: 22 passed / 6 failed due to a NumPy/Pandas binary ABI inconsistency.
- Existing `MetaQ2` environment: import failed on a CUDA `libnvJitLink`/`libcusparse` symbol mismatch.
- Existing `MetqQ2` environment: authoritative run PASS, 28 passed / 13 warnings.

## EpiCarousel installation and smoke

- Python 3.8 venv attempt failed because SnapATAC2 build dependencies require Python >=3.9 and the configured mirror lacked `puccinialin`.
- Python 3.11 official package installation succeeded, but the initially selected SnapATAC2 2.9 pulled NumPy 2.x, incompatible with the existing Scanpy API (`np.float_` removed). NumPy was pinned to 1.26.4; import then passed.
- First D11 smoke stopped in upstream `Carousel.data_split`: current SnapATAC2 returns a Polars DataFrame, while upstream assumes its older table orientation.
- Second D11 smoke reached the construction launcher, which stopped on upstream `np.int`/`np.float` aliases removed by NumPy.
- With the two disclosed compatibility-only shims, official D11 ATAC construction PASS: 2,000/2,000 cells assigned, requested K=40, realized K=40.
