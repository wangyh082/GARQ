# D17 Figure 4b Mast-cell quantitative review

Status: COMPLETE_WITH_AUTHOR_NONEXACT_K_OVERRIDE

This frozen-assignment analysis did not retrain or modify any method. The
original nominal target is K=403. The author explicitly authorized continuation
with the same nominal compression input when a frozen method realizes a
different K; the realized K is retained and shown in every result.

## Executive summary

Canonical metadata is D17 Human_Kidney_Cancer with label key celltype and
16,143 cells. The exact Mast Cells count is 74
(0.4584%).

GARQ majority recall=0.0000; associated
recall=0.5676; maximum purity=0.3016;
associated metacell count=4; associated size
median/range=61.00/53.00--68.00;
top-3 capture=0.4865; permutation P=9.999e-05;
normalized-HHI permutation P=9.999e-05.

Marker coherence: Mast-associated metacells show coherent Mast-cell marker expression.
Only GARQ supported: NO. Recommended outcome:
B. Mast-cell-associated metacells remained identifiable in the GARQ space; localized enrichment and strict majority recovery varied across methods.

## Assignment keys and alignment

| method | candidate_keys | assignment_key | realized_K | requested_compression_ratio | realized_compression_ratio | id_set_equality | row_order_verified_by_label_vector | status | reason |
|---|---|---|---|---|---|---|---|---|---|
| GARQ | metacell | metacell | 403 | 0.0250 | 0.0250 | False | True | PASS |  |
| MetaQ | metacell | metacell | 403 | 0.0250 | 0.0250 | False | True | PASS |  |
| SEACells | SEACell | SEACell | 403 | 0.0250 | 0.0250 | True | False | PASS |  |
| MetaCell V2 | metacell;membership | metacell | 429 | 0.0250 | 0.0266 | True | False | PASS_AUTHOR_NONEXACT_K | same nominal compression input; realized K retained |
| SuperCell | metacell | metacell | 404 | 0.0250 | 0.0250 | False | True | PASS_AUTHOR_NONEXACT_K | same nominal compression input; realized K retained |

MetaCell V2 contained metacell and membership. They were partition-equivalent,
so the author-authorized key is metacell. SuperCell used its sole metacell key.
Numeric row-order IDs were accepted only when the canonical label vector
verified provenance.

## Requested and realized K

Requested ratio is 403/16143=0.02496438. Realized K is not
corrected:

| method | requested_K | realized_K | k_difference | requested_compression_ratio | realized_compression_ratio | cells_per_realized_metacell |
|---|---|---|---|---|---|---|
| GARQ | 403 | 403 | 0 | 0.0250 | 0.0250 | 40.0571 |
| MetaQ | 403 | 403 | 0 | 0.0250 | 0.0250 | 40.0571 |
| SEACells | 403 | 403 | 0 | 0.0250 | 0.0250 | 40.0571 |
| MetaCell V2 | 403 | 429 | 26 | 0.0250 | 0.0266 | 37.6294 |
| SuperCell | 403 | 404 | 1 | 0.0250 | 0.0250 | 39.9579 |

## Recall, purity, number, and size

| method | majority_recall | associated_recall | majority_precision | majority_f1 | high_purity_recall | maximum_purity | associated_purity_median | associated_purity_weighted | associated_metacell_count | majority_metacell_count | high_purity_metacell_count | associated_size_min | associated_size_median | associated_size_max |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| GARQ | 0.0000 | 0.5676 | NA | 0.0000 | 0.0000 | 0.3016 | 0.1508 | 0.1728 | 4 | 0 | 0 | 53.0000 | 61.0000 | 68.0000 |
| MetaQ | 0.0000 | 0.5811 | NA | 0.0000 | 0.0000 | 0.2200 | 0.1471 | 0.1478 | 7 | 0 | 0 | 26.0000 | 47.0000 | 51.0000 |
| SEACells | 0.0000 | 0.2297 | NA | 0.0000 | 0.0000 | 0.2727 | 0.1765 | 0.1328 | 5 | 0 | 0 | 11.0000 | 22.0000 | 46.0000 |
| MetaCell V2 | 0.0000 | 0.1622 | NA | 0.0000 | 0.0000 | 0.0870 | 0.0727 | 0.0710 | 3 | 0 | 0 | 46.0000 | 55.0000 | 68.0000 |
| SuperCell | 0.0000 | 0.2297 | NA | 0.0000 | 0.0000 | 0.2857 | 0.0744 | 0.0714 | 4 | 0 | 0 | 27.0000 | 52.0000 | 107.0000 |

Associated means at least three Mast Cells, at least five-fold enrichment, and
within-method BH q<0.05 from one-sided Fisher exact tests. Majority is purity
greater than 0.5; high purity is at least 0.7. NA denotes no associated group.

## Enrichment and permutation

| method | metric | observed | null_mean | null_q95 | empirical_p |
|---|---|---|---|---|---|
| GARQ | top3_capture | 0.4865 | 0.0528 | 0.0811 | 0.0001 |
| GARQ | normalized_hhi | 0.0780 | 0.0014 | 0.0024 | 0.0001 |
| MetaQ | top3_capture | 0.3784 | 0.0653 | 0.0946 | 0.0001 |
| MetaQ | normalized_hhi | 0.0376 | 0.0012 | 0.0022 | 0.0001 |
| SEACells | top3_capture | 0.1216 | 0.0457 | 0.0676 | 0.0002 |
| SEACells | normalized_hhi | 0.0057 | 0.0016 | 0.0028 | 0.0003 |
| MetaCell V2 | top3_capture | 0.1351 | 0.0823 | 0.0946 | 0.0004 |
| MetaCell V2 | normalized_hhi | 0.0060 | 0.0012 | 0.0021 | 0.0001 |
| SuperCell | top3_capture | 0.0541 | 0.0465 | 0.0676 | 0.3520 |
| SuperCell | normalized_hhi | 0.0134 | 0.0032 | 0.0062 | 0.0004 |

All seven permutation statistics for all five methods are in
fig4b_mast_permutation_summary.csv. Each method used 10,000 fixed-assignment
label permutations with random seed 20260907 and P=(1+count(null>=observed))/10001.

## RNA marker coherence

| method | status | markers_present | markers_missing | associated_group_count | nonassociated_group_count | associated_score_median | nonassociated_score_median | median_score_effect_associated_minus_other | wilcoxon_or_mannwhitney_p | bh_q | coherence_result |
|---|---|---|---|---|---|---|---|---|---|---|---|
| GARQ | PASS | KIT;TPSAB1;TPSB2;CPA3;MS4A2;HDC;GATA2 |  | 4 | 399 | 0.7708 | 0.0000 | 0.7708 | 0.0000 | 0.0000 | Mast-associated metacells show coherent Mast-cell marker expression |
| MetaQ | PASS | KIT;TPSAB1;TPSB2;CPA3;MS4A2;HDC;GATA2 |  | 7 | 396 | 0.8619 | 0.0000 | 0.8619 | 0.0000 | 0.0000 | Mast-associated metacells show coherent Mast-cell marker expression |
| SEACells | PASS | KIT;TPSAB1;TPSB2;CPA3;MS4A2;HDC;GATA2 |  | 5 | 398 | 0.8202 | 0.0000 | 0.8202 | 0.0000 | 0.0001 | Mast-associated metacells show coherent Mast-cell marker expression |
| MetaCell V2 | PASS | KIT;TPSAB1;TPSB2;CPA3;MS4A2;HDC;GATA2 |  | 3 | 426 | 0.4370 | 0.0000 | 0.4370 | 0.0006 | 0.0006 | Mast-associated metacells show coherent Mast-cell marker expression |
| SuperCell | PASS | KIT;TPSAB1;TPSB2;CPA3;MS4A2;HDC;GATA2 |  | 4 | 400 | 0.5053 | 0.0000 | 0.5053 | 0.0001 | 0.0001 | Mast-associated metacells show coherent Mast-cell marker expression |

## Three-population secondary check

| method | population | status | target_count | abundance | majority_recall | majority_metacell_count | maximum_purity | median_majority_metacell_size |
|---|---|---|---|---|---|---|---|---|
| GARQ | Mast Cells | PASS | 74 | 0.0046 | 0.0000 | 0 | 0.3016 | NA |
| GARQ | T Cells | PASS | 88 | 0.0055 | 0.6705 | 1 | 0.8676 | 68.0000 |
| GARQ | Myeloid Cells | PASS | 682 | 0.0422 | 0.8592 | 10 | 1.0000 | 62.5000 |
| MetaQ | Mast Cells | PASS | 74 | 0.0046 | 0.0000 | 0 | 0.2200 | NA |
| MetaQ | T Cells | PASS | 88 | 0.0055 | 0.7045 | 2 | 0.8235 | 41.0000 |
| MetaQ | Myeloid Cells | PASS | 682 | 0.0422 | 0.8886 | 16 | 1.0000 | 44.0000 |
| SEACells | Mast Cells | PASS | 74 | 0.0046 | 0.0000 | 0 | 0.2727 | NA |
| SEACells | T Cells | PASS | 88 | 0.0055 | 0.2614 | 2 | 1.0000 | 12.5000 |
| SEACells | Myeloid Cells | PASS | 682 | 0.0422 | 0.9223 | 76 | 1.0000 | 9.0000 |
| MetaCell V2 | Mast Cells | PASS | 74 | 0.0046 | 0.0000 | 0 | 0.0870 | NA |
| MetaCell V2 | T Cells | PASS | 88 | 0.0055 | 0.0000 | 0 | 0.3529 | NA |
| MetaCell V2 | Myeloid Cells | PASS | 682 | 0.0422 | 0.7038 | 11 | 1.0000 | 46.0000 |
| SuperCell | Mast Cells | PASS | 74 | 0.0046 | 0.0000 | 0 | 0.2857 | NA |
| SuperCell | T Cells | PASS | 88 | 0.0055 | 0.1932 | 2 | 0.8000 | 11.0000 |
| SuperCell | Myeloid Cells | PASS | 682 | 0.0422 | 0.6525 | 31 | 1.0000 | 13.0000 |

## Cross-method interpretation

The five methods share the nominal compression input but do not share an
identical realized K. Exact Figure 4b and the separate Phase-2 K=323
three-seed post-hoc analysis remain separate; see
FIG4B_K403_VS_PHASE2_K323_CONSISTENCY.md. Enrichment is not strict majority
recovery. D17 labels are study-derived, not an independent ground truth.

Recommended wording:

Mast-cell-associated metacells remained identifiable in the GARQ space; localized enrichment and strict majority recovery varied across methods.

## File index

input_inventory.csv; id_alignment_checks.csv; resolved_config.yaml;
fig4b_mast_metacell_level.csv; fig4b_mast_method_summary.csv;
fig4b_mast_permutation_summary.csv; fig4b_mast_top_metacells.csv;
fig4b_mast_marker_validation.csv; fig4b_three_population_summary.csv;
Fig4b_mast_quantitative_panel.pdf/svg/png; FigS_mast_localized_enrichment.pdf/svg/png;
Supplementary_Table_Fig4b_Mast.csv; Supplementary_Table_Fig4b_Mast.tex.

## Limitations

This is a post-hoc frozen-assignment analysis. The non-exact realized K values
for MetaCell V2 and SuperCell are an author-authorized limitation. The analysis
does not establish causal regulation, trajectory superiority, or independent
ground truth.
