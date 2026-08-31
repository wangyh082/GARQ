# P2-E7 D18 RNA–protein — SEACells seeds 0–2

## Status and reviewer mapping

**PASS for all three seeds.** These descriptive full-feature runs complete the SEACells arm and the planned four-method descriptive screen for R2 Major 4. Feature-exclusion remains required for confirmatory use.

## Exact findings

Corrected D18 matched-K SEACells assignments, 25,517 cells, realized K=510; 15 mapped RNA–ADT pairs per seed; RNA library/log1p, ADT log1p/CLR, dominant-cell-type partial Pearson, and 1,000-resample bootstrap intervals.

| seed | pair | Pearson r | partial r | bootstrap 95% CI |
|---:|---|---:|---:|---:|
| 0 | NCAM1–CD56 | 0.698170 | 0.385638 | [0.282930, 0.467162] |
| 0 | CD8A–CD8a | 0.667607 | 0.269854 | [0.193862, 0.339371] |
| 1 | NCAM1–CD56 | 0.687744 | 0.290854 | [0.198504, 0.380688] |
| 1 | CD8A–CD8a | 0.689453 | 0.320714 | [0.242421, 0.390671] |
| 2 | NCAM1–CD56 | 0.700871 | 0.364380 | [0.270121, 0.448554] |
| 2 | CD8A–CD8a | 0.684908 | 0.301251 | [0.218718, 0.372432] |

All 45 rows were finite; no run failed.

## Evidence and limitations

- Exact rows: `revision_results/phase2/07_trimodal/rna_protein/SEACells_seed{0,1,2}.csv`
- Logs: `/data/zhangpeiru/GARQ_revision/revision_results/phase2/logs/P2_E7_D18_RNAPROTEIN_SEACells_seed{0,1,2}.driver.log`
- Workflow: `revision_exp/workflows/d18_rna_protein_benchmark.py`

Safe wording: “Both prespecified pairs remained positively associated within dominant cell type across three descriptive SEACells aggregations.” Do not call this causal, held-out, or de-circularized. SEACells' NCAM1–CD56 mean partial correlation exceeded GARQ's, which argues against GARQ specificity.

