# Rebuttal Evidence Draft — Phase 2

Status: VERIFIED EVIDENCE DRAFT; not the final rebuttal.

## Rare-state and matched-resolution concern

**What we did.** We reran corrected D5, D11, D17 and D18 at requested K/n=0.02 for three seeds with GARQ, official SEACells 0.3.3, official MetaQ 1.0.6 and KMeans. SEACells and KMeans share a fixed equal-weight PCA/LSI/CLR representation. All 48 assignments used the same evaluator and explicit majority (>0.5) and high-purity (>=0.7) definitions.

**What we found.** Results were cell-type dependent and often unfavorable to GARQ. GARQ mean F1 was lower than SEACells for D18 DC.Myeloid by 0.640, lower than KMeans for D5 Treg by 0.453, and lower than MetaQ for D17 Mast Cells by 0.345. GARQ exceeded MetaQ for D5 cDC2 by 0.316, while D18 Platelet differences versus MetaQ/SEACells were only +0.014/+0.018. All methods had F1=0 for D18 T.DoubleNegative.

**What we can safely say.** Full-data requested-K comparisons were added and show heterogeneous preservation rather than a consistent winner.

**What we cannot say.** GARQ consistently or significantly outperforms competing metacell methods, or that requested-K matching removes realized-K confounding.

**Candidate English paragraph.** “We added three-seed, full-data comparisons on the corrected D5, D11, D17, and D18 datasets using GARQ, SEACells, MetaQ, and a fixed-representation KMeans control at the same requested compression level. Rare-state recovery was heterogeneous across datasets and cell types, and several focal states were recovered better by a baseline. We therefore narrowed the manuscript claim and report all favorable, unfavorable, and null outcomes.”

Tables: `matchedK_focal_rare_summary.csv`, `matchedK_focal_rare_paired_contrasts.csv`, `full_benchmark_long.csv`.
