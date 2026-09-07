# R2 Minor Comment 4 — Figure 4b Mast-cell quantitative evidence

Status: **PASS — author-authorized same-compression, non-exact-K analysis**.

This report is the reviewer-comment delivery unit for R2 Minor Comment 4. It
records the frozen-assignment analysis requested for Figure 4b and keeps the
strict-K dry-run blocker as evidence. The author explicitly authorized using
the same nominal compression input for MetaCell V2 and SuperCell even though
their frozen assignment files realize K=429 and K=404 rather than K=403. No
method was retrained, edited, or selected using labels or outcomes.

## Experiment and configuration

- Dataset: D17 `Human_Kidney_Cancer`, canonical metadata `celltype`, 16,143
  cells; exact `Mast Cells` count 74 (0.4584%).
- Frozen assignment files and canonical cell-type vector were audited before
  quantification. Requested nominal ratio is `K/n=403/16143=0.02496438`
  (reported as 0.0250).
- Methods: GARQ, MetaQ, SEACells, MetaCell V2, SuperCell.
- Association definition: at least 3 target cells, at least 5-fold enrichment,
  one-sided Fisher exact test with within-method BH q<0.05; majority purity
  `>0.5`; high-purity purity `>=0.7`.
- Marker panel: KIT, TPSAB1, TPSB2, CPA3, MS4A2, HDC, GATA2.
- Permutations: 10,000 fixed-assignment label permutations, seed 20260907,
  empirical `P=(1+count(null>=observed))/10001`.
- Command executed on `node01` in `/data/zhangpeiru/GARQ_revision`:

  ```bash
  /home/zhangpeiru/.conda/envs/MetqQ2/bin/python -m revision_exp.workflows.fig4b_mast_exact_assignment \
    --figure-dir ./fig4b \
    --output-dir ./fig4b/reviewer_mast_quantification \
    --allow-nonexact-k --n-permutations 10000
  ```

## Individual experiment status

| method | assignment key | requested K | realized K | status | note |
|---|---:|---:|---:|---|---|
| GARQ | `metacell` | 403 | 403 | PASS | exact K and canonical label alignment |
| MetaQ | `metacell` | 403 | 403 | PASS | exact K and canonical label alignment |
| SEACells | `SEACell` | 403 | 403 | PASS | exact K; ID set equality verified |
| MetaCell V2 | `metacell` | 403 | 429 | PASS_AUTHOR_NONEXACT_K | `metacell` and `membership` are partition-equivalent; `metacell` retained |
| SuperCell | `metacell` | 403 | 404 | PASS_AUTHOR_NONEXACT_K | sole candidate key; realized K retained |

The initial strict audit was **BLOCKED** for MetaCell V2 (multiple candidate
columns, both K=429) and SuperCell (sole candidate K=404). Its preserved
evidence is `dry_run.driver.log`, `DRY_RUN.md`, and the earlier synchronized
strict-audit commit. The author decision changed only the acceptance rule for
this frozen analysis; it did not alter assignments.

## Exact results

| method | associated recall | max purity | associated groups | associated size median (range) | top-3 capture | top-3 permutation P | normalized-HHI permutation P |
|---|---:|---:|---:|---:|---:|---:|---:|
| GARQ | 0.5676 | 0.3016 | 4 | 61 (53–68) | 0.4865 | 0.0001 | 0.0001 |
| MetaQ | 0.5811 | 0.2200 | 7 | 47 (26–51) | 0.3784 | 0.0001 | 0.0001 |
| SEACells | 0.2297 | 0.2727 | 5 | 22 (11–46) | 0.1216 | 0.0002 | 0.0003 |
| MetaCell V2 | 0.1622 | 0.0870 | 3 | 55 (46–68) | 0.1351 | 0.0004 | 0.0001 |
| SuperCell | 0.2297 | 0.2857 | 4 | 52 (27–107) | 0.0541 | 0.3520 | 0.0004 |

Strict majority recall and high-purity recovery were 0 for all five methods.
All seven RNA markers were present and showed significant associated-vs-other
coherence for every method (GARQ median score effect 0.7708; BH q<0.001).
Thus localized enrichment is detectable, but no method produces a strict
majority Mast metacell in this frozen comparison. `Only GARQ supported` is
**NO**; the evidence supports Outcome B.

## Reply-safe wording

> We re-evaluated the frozen Figure 4b assignments using the exact D17 Mast
> Cell label (74/16,143 cells), a pre-specified enrichment test, and 10,000
> fixed-label permutations. GARQ showed significant localized enrichment
> (associated recall 0.568; maximum purity 0.302), while strict majority and
> high-purity recovery were zero. MetaQ, SEACells, MetaCell V2 and SuperCell
> showed method-dependent enrichment with realized K=403, 403, 429 and 404,
> respectively, under the same nominal compression input. We therefore
> report Mast-cell-associated metacells as identifiable, but do not claim
> exclusive GARQ recovery or superiority.

## Claims explicitly prohibited

- Do not call MetaCell V2/SuperCell an exact-K=403 comparison; their realized
  K values are 429 and 404 and must remain visible.
- Do not claim majority Mast-cell recovery, high-purity recovery, exclusive
  GARQ detection, or GARQ superiority.
- Do not merge these frozen Figure 4b results with the separate Phase-2 K=323
  three-seed D17 post-hoc analysis.
- D17 `celltype` labels are study-derived annotations, not an independent
  ground truth; enrichment is not causal regulation or trajectory evidence.

## Evidence paths and verification

Server result directory:
`/data/zhangpeiru/GARQ_revision/fig4b/reviewer_mast_quantification/`

Primary report and response:

- `D17_FIG4B_MAST_EXACT_REPORT.md`
- `D17_FIG4B_MAST_RESPONSE_READY.tex`

Primary tables and figures:

- `fig4b_mast_method_summary.csv`
- `fig4b_mast_permutation_summary.csv`
- `fig4b_mast_metacell_level.csv`
- `fig4b_three_population_summary.csv`
- `Supplementary_Table_Fig4b_Mast.csv/.tex`
- `Fig4b_mast_quantitative_panel.{pdf,svg,png}`
- `FigS_mast_localized_enrichment.{pdf,svg,png}`

Run and audit evidence: `formal_run.driver.log`, `input_inventory.csv`,
`id_alignment_checks.csv`, `resolved_config.yaml`, `output_file_hashes.csv`,
`DRY_RUN.md`, and preserved `dry_run.driver.log`.

Verification: targeted Figure 4b tests passed (`4 passed`); the final server
Phase-2 suite passed (`43 passed, 13 warnings`). No project process was running during
the final resource check, so no other user's process was stopped.

## Limitations

This is a post-hoc frozen-assignment analysis. The same-compression/non-exact-K
acceptance is an author decision, not a claim of exact resolution matching.
The analysis is descriptive and does not replace the remaining Phase-2
trajectory, cross-fitting, or multi-batch evidence.
