# D17 Mast Cells Existing-Assignment Post-hoc Analysis

## Executive summary

Under the strict majority criterion, GARQ did not achieve complete Mast-cell recovery. Nevertheless, the existing assignments showed partial localized preservation (mean associated recall 61.7%; maximum purity 0.153–0.270; maximum enrichment 33.3–59.0-fold). GARQ's evidence level is **B**. Comparative superiority is **not supported** under the preregistered all-comparator, same-seed rule. The original binary/unique-retention wording should therefore be replaced by quantitative strict, enrichment, and permutation results.

## Inputs and provenance

This analysis used frozen assignments only; it did not retrain, tune, or alter assignments. Dataset: `D17 Human_Kidney_Cancer`; exact label: `Mast Cells`; target count: 74/16143 (0.4584%); requested K: 323; seeds: 0–2. Metadata SHA256: `c2f4bc8313fa68c7e1c670fce74f287dca3865b0c039070babb10bd1f4125e25`. Assignment paths and SHA256 hashes are recorded in `input_inventory.csv`; exact ID-set checks are in `id_alignment_checks.csv`. Available methods were GARQ, MetaQ, SEACells, and KMeans. MetaCell V2 and SuperCell assignments were unavailable.

## Definitions

Strict majority recovery uses purity >0.5; high purity uses purity >=0.7. An associated metacell requires at least 3 Mast Cells, >=5-fold enrichment, and within-run Fisher/BH q<0.05. Top-k capture ranks by enrichment, q-value, Mast count, and stable metacell ID. Fixed-assignment label permutations (10,000 per method/seed) test concentration using maximum purity/enrichment, top-1/top-3 capture, HHI, and normalized HHI.

## Results

| method | seed | realized_K | strict_recall | strict_f1 | associated_metacell_count | associated_recall | max_purity | max_fold_enrichment | top3_capture | normalized_hhi | evidence_level |
|---|---|---|---|---|---|---|---|---|---|---|---|
| GARQ | 0 | 323 | 0.0000 | 0.0000 | 5 | 0.5676 | 0.2703 | 58.9591 | 0.4459 | 0.0761 | B |
| GARQ | 1 | 323 | 0.0000 | 0.0000 | 6 | 0.6351 | 0.1724 | 37.6118 | 0.3108 | 0.0480 | B |
| GARQ | 2 | 323 | 0.0000 | 0.0000 | 6 | 0.6486 | 0.1528 | 33.3283 | 0.4459 | 0.0576 | B |
| MetaQ | 0 | 323 | 0.2297 | 0.3505 | 4 | 0.6216 | 0.7391 | 161.2403 | 0.5676 | 0.0919 | A |
| MetaQ | 1 | 323 | 0.1757 | 0.2796 | 6 | 0.6892 | 0.6842 | 149.2596 | 0.4730 | 0.0746 | A |
| MetaQ | 2 | 323 | 0.2162 | 0.3478 | 4 | 0.6081 | 0.8889 | 193.9099 | 0.5541 | 0.1019 | A |
| SEACells | 0 | 323 | 0.0000 | 0.0000 | 6 | 0.3514 | 0.3846 | 83.9033 | 0.1622 | 0.0119 | B |
| SEACells | 1 | 323 | 0.0811 | 0.1446 | 6 | 0.3378 | 0.6667 | 145.4324 | 0.1757 | 0.0110 | A |
| SEACells | 2 | 323 | 0.0000 | 0.0000 | 6 | 0.3378 | 0.2143 | 46.7461 | 0.2027 | 0.0110 | B |
| KMeans | 0 | 323 | 0.0000 | 0.0000 | 5 | 0.5135 | 0.1591 | 34.7055 | 0.2838 | 0.0354 | B |
| KMeans | 1 | 323 | 0.0000 | 0.0000 | 6 | 0.5135 | 0.1628 | 35.5126 | 0.2703 | 0.0322 | B |
| KMeans | 2 | 323 | 0.0000 | 0.0000 | 7 | 0.6486 | 0.1857 | 40.5133 | 0.3514 | 0.0449 | B |

Permutation results for the two evidence-gating concentration measures:

| method | seed | metric | observed | null_mean | null_q95 | empirical_p |
|---|---|---|---|---|---|---|
| GARQ | 0 | top3_capture | 0.4459 | 0.0682 | 0.0946 | 0.0001 |
| GARQ | 0 | normalized_hhi | 0.0761 | 0.0016 | 0.0026 | 0.0001 |
| GARQ | 1 | top3_capture | 0.3108 | 0.0653 | 0.0946 | 0.0001 |
| GARQ | 1 | normalized_hhi | 0.0480 | 0.0016 | 0.0027 | 0.0001 |
| GARQ | 2 | top3_capture | 0.4459 | 0.0690 | 0.0946 | 0.0001 |
| GARQ | 2 | normalized_hhi | 0.0576 | 0.0016 | 0.0027 | 0.0001 |
| MetaQ | 0 | top3_capture | 0.5676 | 0.0718 | 0.1081 | 0.0001 |
| MetaQ | 0 | normalized_hhi | 0.0919 | 0.0016 | 0.0026 | 0.0001 |
| MetaQ | 1 | top3_capture | 0.4730 | 0.0672 | 0.0946 | 0.0001 |
| MetaQ | 1 | normalized_hhi | 0.0746 | 0.0016 | 0.0026 | 0.0001 |
| MetaQ | 2 | top3_capture | 0.5541 | 0.0675 | 0.0946 | 0.0001 |
| MetaQ | 2 | normalized_hhi | 0.1019 | 0.0016 | 0.0026 | 0.0001 |
| SEACells | 0 | top3_capture | 0.1622 | 0.0508 | 0.0811 | 0.0001 |
| SEACells | 0 | normalized_hhi | 0.0119 | 0.0019 | 0.0033 | 0.0001 |
| SEACells | 1 | top3_capture | 0.1757 | 0.0505 | 0.0811 | 0.0001 |
| SEACells | 1 | normalized_hhi | 0.0110 | 0.0020 | 0.0033 | 0.0001 |
| SEACells | 2 | top3_capture | 0.2027 | 0.0508 | 0.0811 | 0.0001 |
| SEACells | 2 | normalized_hhi | 0.0110 | 0.0020 | 0.0033 | 0.0001 |
| KMeans | 0 | top3_capture | 0.2838 | 0.0808 | 0.1081 | 0.0001 |
| KMeans | 0 | normalized_hhi | 0.0354 | 0.0016 | 0.0027 | 0.0001 |
| KMeans | 1 | top3_capture | 0.2703 | 0.0823 | 0.1081 | 0.0001 |
| KMeans | 1 | normalized_hhi | 0.0322 | 0.0016 | 0.0026 | 0.0001 |
| KMeans | 2 | top3_capture | 0.3514 | 0.0798 | 0.1081 | 0.0001 |
| KMeans | 2 | normalized_hhi | 0.0449 | 0.0016 | 0.0028 | 0.0001 |

All six permutation statistics are in `mast_permutation_summary.csv`; metacell-level Fisher/BH results and sizes are in `mast_metacell_level_metrics.csv`.

## Interpretation

Visual detectability in a UMAP, strict majority recovery, and partial localized preservation are distinct. The evidence level above was assigned automatically from the preregistered thresholds. Enrichment or concentration does not by itself establish strict recovery. No UMAP-only conclusion was used.

## Figure and table mapping

Replace the Mast-cell portion of Figure 4b with `Fig4b_mast_quantitative` and place the enrichment/capture panel in a Supplementary Figure. Use `mast_run_level_summary.csv` and `mast_metacell_level_metrics.csv` as the source for a new Supplementary Table. Replace any binary statement that GARQ uniquely retained Mast Cells with: “Under the strict majority criterion, GARQ did not achieve complete Mast-cell recovery. Nevertheless, the existing assignments showed partial localized preservation (mean associated recall 61.7%; maximum purity 0.153–0.270; maximum enrichment 33.3–59.0-fold).”

## Limitations

D17 annotations are study-derived. This post-hoc analysis did not retrain or optimize assignments. UMAP is qualitative and was not used as a retention criterion. Enrichment evidence is not equivalent to strict recovery. MetaCell V2 and SuperCell assignments were unavailable. Only three seeds were available. Comparator claims are restricted to matched existing assignments and do not establish trajectory superiority.
