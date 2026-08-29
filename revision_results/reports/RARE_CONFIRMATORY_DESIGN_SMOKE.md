# E1 recovered-dataset rare-cell confirmatory-design smoke

## Status and scope

**Status: PASS for the preregistered smoke design; PARTIAL for the full E1 confirmatory requirement.** All 270 generated runs completed with `PASS` manifests. This is a diagnostic smoke experiment on the four recovered datasets D5, D11, D17, and D18. It is not the full confirmatory test required by the revision plan, which requires at least six datasets, at least two eligible cell types per dataset, full-scale training, and method baselines.

Each run used 2,000 cells, requested K=40, six epochs, deterministic training, training seeds 0–4, and a distinct deterministic subset-selection seed. Rare-cell sampling was performed without replacement. A target abundance was omitted when it would require upsampling. The implementation tag is `diagnostic_variant_rare_subsampling`; these results must not be described as the published GARQ result.

## Design and validation

| Item | Result |
|---|---:|
| Generated configs / PASS manifests / provenance records | 270 / 270 / 270 |
| Long-form rows / five-seed condition groups | 270 / 54 |
| Dataset runs | D5 80; D11 80; D17 60; D18 50 |
| Modality checks | 220 dual-modal; 50 tri-modal |
| Target support at 0.1/0.2/0.5/1/2% | 2 / 4 / 10 / 20 / 40 cells |
| Sampling | targeted abundance, without replacement |
| Row-order checks | true for every modality in every run |
| D18 ADT canonicalization | `\.([0-9]+)$` to `-\1`; applied in all 50 D18 runs |
| Accumulated per-run wall time | 4,229.3 seconds |
| Median / maximum per-run wall time | 15.06 / 36.20 seconds |
| Maximum recorded CPU RSS | 6.73 GiB |
| Full test suite | 28 passed, 13 dependency/runtime warnings |

The 14 evaluated cell types were selected before inspecting outcomes: two most abundant eligible types per dataset plus required or biologically important rare types where recoverable. D5 included Non classical monocytes, gdT cells, Regulatory T cells, and conventional DC; D11 included CD14+ Mono, NK, cDC2, and Plasma cell; D17 included Myeloid Cells, Parietal Epithelial Cells, and Mast Cells; D18 included B.Activated, Mono.CD16, and Platelets.

`git diff --check` reports trailing whitespace in 80 D5 assignment files because the source annotation contains the literal label `Erythroid ` with a terminal space. The raw label is deliberately preserved in cell-level evidence rather than silently normalized.

## Results

Across 270 runs, only 31 (11.5%) had nonzero target-cell F1, 15 (5.6%) achieved majority retention, and 9 (3.3%) achieved high-purity recovery. Mean F1 was 0.0346 and median F1 was zero; mean recall was 0.0387 and median recall was zero. Across the 54 five-seed condition groups, 15 had any nonzero-F1 run, only two had nonzero F1 in all five seeds, and no group achieved majority retention or high-purity recovery in all five seeds.

| Target abundance | Runs | Nonzero F1 | Majority retention | High-purity recovery | Mean recall | Mean F1 |
|---:|---:|---:|---:|---:|---:|---:|
| 0.1% | 70 | 1 | 1 | 1 | 0.0143 | 0.0095 |
| 0.2% | 70 | 1 | 1 | 1 | 0.0036 | 0.0057 |
| 0.5% | 55 | 2 | 2 | 2 | 0.0036 | 0.0066 |
| 1% | 40 | 11 | 3 | 3 | 0.0825 | 0.0730 |
| 2% | 35 | 16 | 8 | 2 | 0.1629 | 0.1426 |

| Dataset | Runs | Nonzero F1 | Majority retention | High-purity recovery | Mean recall | Mean F1 |
|---|---:|---:|---:|---:|---:|---:|
| D5 | 80 | 8 | 5 | 5 | 0.0253 | 0.0290 |
| D11 | 80 | 11 | 3 | 1 | 0.0675 | 0.0449 |
| D17 | 60 | 8 | 4 | 1 | 0.0267 | 0.0344 |
| D18 | 50 | 4 | 3 | 2 | 0.0285 | 0.0273 |

The strongest group-level mean was D11 CD14+ Mono at 2% (mean F1 0.4438, SD 0.1295; mean recall 0.730, SD 0.300; all five seeds nonzero, but only two achieved majority retention and none achieved high-purity recovery). D17 Myeloid Cells at 2% was the other all-five-nonzero group (mean F1 0.2867, SD 0.1208; mean recall 0.220, SD 0.119; three majority-retention runs and no high-purity run).

Required/reviewer-relevant recovered examples were weak: D5 Regulatory T cells and conventional DC had zero F1 in all 15 reachable runs each; D11 Plasma cell had zero F1 in all 10 reachable runs; D11 cDC2 had four nonzero-F1 runs among 20, with one majority and one high-purity run. D5 gdT cells had four nonzero-F1 runs among 25, with three majority and three high-purity runs. D17 Mast Cells and D18 Mono.CD16 had zero F1 in all reachable runs. These results do not support a robust rare-state-preservation claim under this smoke setting.

## Interpretation

The abundance trend is directionally favorable at 1–2%, but recovery remains seed-sensitive and the medians are zero at every abundance. Isolated successful seeds must not be presented as confirmatory support. The honest conclusion is that this smoke experiment supplies negative and uncertainty evidence: under 2,000-cell, six-epoch GARQ runs, rare-state recovery is generally absent below 1% and inconsistent even at 1–2%.

## Limitations and deferred work

- Only four datasets were recovered; D1–D4, D6–D10, D12, and D13–D16 remain unavailable or unmapped. The full six-dataset confirmatory requirement is not met.
- D11 has no gdT label in the recovered annotations, and D16 Schwann Cell cannot be tested without D16.
- Runs are smoke-scale (2,000 cells, six epochs), not full-data training.
- No MetaQ, SEACells, MetaCell V2, SuperCell, or realized-K-matched baseline is included here.
- No inferential comparison should be made from the 270 run-level rows as if they were independent biological replicates.
- The broad D5/D11 screen and this confirmatory-design smoke must be reported separately.

## Reproducibility pointers

- Config generator: `revision_exp/workflows/generate_rare_confirmatory_configs.py`
- Configs: `revision_exp/configs/rare_confirmatory/`
- Summarizer: `revision_exp/workflows/summarize_rare_confirmatory.py`
- Long table: `revision_results/01_size_resolution/rare_confirmatory_smoke_long.csv`
- Five-seed summary: `revision_results/01_size_resolution/rare_confirmatory_smoke_summary.csv`
- Per-run evidence: `revision_results/01_size_resolution/rare_confirmatory/`
- Resolved configs and manifests: `revision_results/configs_resolved/` and `revision_results/manifests/`

Recreate the summaries with:

```bash
python -m revision_exp.workflows.summarize_rare_confirmatory
```
