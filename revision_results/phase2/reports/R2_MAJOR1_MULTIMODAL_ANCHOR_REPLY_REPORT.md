# Reviewer 2 Major 1 — multimodal anchor evidence for reply

## Delivery status

**REPLY-READY WITH A NEGATIVE/QUALIFIED CONCLUSION.** All frozen corrected-data evidence planned for this reviewer unit is complete: seven D18 modality combinations × three seeds (21 runs), common neighborhood/homogeneity evaluation, and three modality perturbations × four perturbation levels × three seeds (36 valid runs). The experiments show that GARQ can construct shared assignments, but they do **not** support a strong claim of consistent multimodal fidelity or noise robustness.

Reviewer mapping: Reviewer 2 Major 1 (primary); Reviewer 1 Major 2 (supporting modality-dominance evidence).

## Experiments completed

1. Corrected D18 full-data GARQ at requested K=510, resolution approximately 0.02, seeds 0–2, for RNA, ATAC, ADT, RNA+ATAC, RNA+ADT, ATAC+ADT, and full RNA+ATAC+ADT.
2. Common kNN retention, cosine compactness, cross-modality neighborhood Jaccard, and diagnostic conflict-anchor evaluation on all 21 runs.
3. Full-data count permutation for RNA, ATAC, and ADT, and binomial thinning at retention 0.25, 0.50, and 0.75, each at seeds 0–2. All 36 corrected runs completed and were compared with the same-seed unperturbed full-trimodal assignment.

## Exact findings

### Modality combinations

RNA+ATAC produced macro F1 values of approximately 0.696–0.699 across seeds, whereas full trimodal produced approximately 0.681–0.694. This grid does not show that adding every modality is necessary or uniformly beneficial. Exact run-level results and inputs are in the dedicated seven combination reports and the modality-grid source directories.

### Neighborhood retention and homogeneity

At k=15, the full-trimodal within-anchor neighbor fractions averaged 0.108772 for RNA, 0.085616 for ATAC, and 0.070599 for ADT. Mean cross-modality kNN Jaccard in the full-trimodal arm was 0.005962 (RNA–ATAC), 0.004010 (RNA–ADT), and 0.003389 (ATAC–ADT). The diagnostic conflict-anchor rate was 9.67–11.16% for full trimodal, compared with 0.39–1.18% for RNA+ATAC. These are diagnostic metrics, not biological error rates.

### Perturbation results

| perturbation | modality | mean ARI | seed range | mean macro F1 | largest metacell |
|---|---|---:|---:|---:|---:|
| permutation | RNA | 0.036941 | 0.033632–0.040146 | 0.671084 | 165 |
| permutation | ATAC | 0.039766 | 0.037323–0.041378 | 0.659905 | 161 |
| permutation | ADT | 0.062540 | 0.060845–0.064103 | 0.676044 | 203 |
| thinning 25% retained | RNA | 0.136195 | 0.039989–0.302428 | 0.699182 | 3,126 |
| thinning 25% retained | ATAC | 0.072647 | 0.071492–0.073519 | 0.671616 | 859 |
| thinning 25% retained | ADT | 0.085376 | 0.077607–0.091174 | 0.699761 | 123 |
| thinning 50% retained | RNA | 0.082627 | 0.057747–0.116553 | 0.690115 | 1,617 |
| thinning 50% retained | ATAC | 0.088302 | 0.066664–0.118059 | 0.680825 | 1,584 |
| thinning 50% retained | ADT | 0.090155 | 0.084861–0.093579 | 0.699620 | 132 |
| thinning 75% retained | RNA | 0.088047 | 0.061200–0.124886 | 0.696093 | 1,413 |
| thinning 75% retained | ATAC | 0.143391 | 0.089069–0.250239 | 0.686965 | 911 |
| thinning 75% retained | ADT | 0.215474 | 0.109298–0.334512 | 0.710729 | 1,328 |

Permutation caused very low assignment ARI for every modality. Thinning results were non-monotonic and often seed-sensitive, and several conditions produced extreme size tails. Macro label F1 could remain moderate while membership ARI was low, so label aggregation alone would overstate assignment stability.

## Preserved failure and correction

The first full-data RNA-permutation seeds 0 and 1 exited successfully but were scientifically **FAIL/INVALID**: their assignment files were byte-identical to baseline because the legacy loader materialized perturbations only when `cell_limit` was set. Those outputs remain under `revision_results/phase2/02_modality/noise_full` and are excluded from the table. The compatibility-equivalent fix materializes full data whenever perturbation, non-X modality, or rare sampling is requested; it does not change the perturbation definition. Independent outputs were written to `noise_full_retry1`, and a full-size regression test was added. The corrected grid is 36/36 PASS.

## Safe reply wording

Candidate response:

> We added a corrected full-data D18 analysis spanning all seven modality combinations (three seeds), modality-specific neighborhood retention and anchor homogeneity, and 36 count-permutation/thinning runs evaluated against same-seed unperturbed assignments. Shared assignments retained measurable but limited modality-specific neighborhoods, while cross-modality single-cell kNN overlap was low. Perturbation experiments showed low or strongly seed-dependent assignment preservation despite sometimes moderate label-level F1. We therefore revised the manuscript to describe GARQ as producing a shared multimodal aggregation rather than claiming uniform preservation of modality-specific structure or broad noise robustness.

## Prohibited claims and scientific limitations

- Do not claim that full trimodal input is consistently superior or necessary.
- Do not claim consistent robustness to permutation or thinning.
- Do not use macro F1 alone as evidence of assignment stability.
- Do not interpret the percentile conflict flag as a validated biological discordance label.
- These results test GARQ internally across inputs; they are not a matched-method downstream comparison and do not establish GARQ-specific superiority.
- The perturbation comparison includes training stochasticity because each perturbed run is refit; the same-seed baseline controls the seed but cannot separate every optimization effect.

## Evidence paths and verification

- Run-level perturbation table (36 rows): `revision_results/phase2/02_modality/d18_noise_full_summary.csv`
- Per-cell-type perturbation table: `revision_results/phase2/02_modality/d18_noise_full_per_type.csv`
- Neighborhood table (162 rows): `revision_results/phase2/02_modality/d18_modality_neighborhood_full.csv`
- Anchor compactness table (9,123 rows): `revision_results/phase2/02_modality/d18_modality_anchor_compactness_full.csv`
- Perturbation workflow: `revision_exp/workflows/d18_noise_full.py`
- Summarizer: `revision_exp/workflows/summarize_d18_noise_full.py`
- Server valid results: `/data/zhangpeiru/GARQ_revision/revision_results/phase2/02_modality/noise_full_retry1`
- Server invalid evidence: `/data/zhangpeiru/GARQ_revision/revision_results/phase2/02_modality/noise_full`
- Logs: `/data/zhangpeiru/GARQ_revision/revision_results/phase2/logs/P2_E2_D18_NOISE_FULL*`
- Verification: `python -m pytest -q revision_exp/tests` → 29 passed, 13 warnings; `git diff --check` must pass before delivery.
