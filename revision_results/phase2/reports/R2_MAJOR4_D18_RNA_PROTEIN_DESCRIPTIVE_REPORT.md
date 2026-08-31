# R2 Major 4 — D18 RNA–protein descriptive component

## Delivery status

**Full-feature descriptive screen PASS (12/12); confirmatory component PARTIAL.** GARQ, KMeans, MetaQ, and SEACells were evaluated for seeds 0–2 on corrected D18. Because assignments used the tested RNA/ADT markers, these results cannot substitute for feature-excluded reruns.

## Exact cross-method summary

Each run included 15 mapped RNA–ADT pairs, Pearson/Spearman correlation, dominant-cell-type partial Pearson correlation, and 1,000-resample bootstrap intervals. All 180 rows were finite.

| method | NCAM1–CD56 mean partial r (range) | CD8A–CD8a mean partial r (range) |
|---|---:|---:|
| GARQ | 0.225871 (0.143487–0.324649) | 0.309805 (0.249567–0.392820) |
| KMeans | 0.261381 (0.234655–0.294849) | 0.267695 (0.245415–0.295225) |
| MetaQ | 0.345240 (0.316249–0.363087) | 0.330834 (0.302406–0.365218) |
| SEACells | 0.346957 (0.290854–0.385638) | 0.297273 (0.269854–0.320714) |

Favorable finding: GARQ recovered positive within-cell-type association for both prespecified pairs in every seed, with every bootstrap interval above zero. Negative finding: this was not GARQ-specific. GARQ had the lowest mean NCAM1–CD56 partial correlation, while MetaQ had the highest mean CD8A–CD8a value.

## Failure evidence

GARQ seed0 initially failed before statistics because SciPy 1.11 removed string support from `stats.mode`. The failure log remains preserved. An equivalent unique-count label mode fixed compatibility without changing scientific semantics; all accepted runs then passed.

## Evidence paths

- Combined exact rows: `revision_results/phase2/07_trimodal/rna_protein.csv`
- Per-method reports: `P2_E7_D18_RNA_PROTEIN_*_REPORT.md`
- Server results: `/data/zhangpeiru/GARQ_revision/revision_results/phase2/07_trimodal/rna_protein/`
- Server logs: `/data/zhangpeiru/GARQ_revision/revision_results/phase2/logs/P2_E7_D18_RNAPROTEIN_*.driver.log`

## Safe reply wording and prohibited claims

Safe partial wording: “Across matched-resolution methods and three seeds, both prespecified RNA–protein pairs showed positive within-cell-type associations. The effect was not GARQ-specific; alternative methods were equal or stronger depending on the pair.”

Do not claim held-out reproducibility, causal regulation, de-circularized validation, or completion of R2 Major 4. Feature-excluded assignment reruns, peak–gene, TF–gene, and cross-fit analyses remain outstanding.
