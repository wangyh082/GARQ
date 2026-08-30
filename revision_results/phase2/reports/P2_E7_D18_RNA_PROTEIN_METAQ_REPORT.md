# P2-E7 D18 RNA–protein — MetaQ seeds 0–2

## Status and reviewer mapping

**PASS for all three seeds.** These descriptive full-feature runs contribute to R2 Major 4 but are not confirmatory; feature-excluded reruns and SEACells remain outstanding.

## Experiment and exact findings

Corrected D18 realized-K-matched MetaQ assignments, 25,517 cells, realized K=511/505/517. Fifteen mapped RNA–ADT pairs per seed; RNA library/log1p and ADT log1p/CLR metacell profiles. Pearson, Spearman, dominant-cell-type partial Pearson, and 1,000-resample bootstrap intervals were computed.

| seed | pair | Pearson r | partial r | bootstrap 95% CI |
|---:|---|---:|---:|---:|
| 0 | NCAM1–CD56 | 0.713734 | 0.363087 | [0.272814, 0.452627] |
| 0 | CD8A–CD8a | 0.671288 | 0.302406 | [0.196849, 0.393952] |
| 1 | NCAM1–CD56 | 0.723954 | 0.356384 | [0.249270, 0.451117] |
| 1 | CD8A–CD8a | 0.702980 | 0.365218 | [0.263058, 0.456937] |
| 2 | NCAM1–CD56 | 0.699673 | 0.316249 | [0.219361, 0.410363] |
| 2 | CD8A–CD8a | 0.674439 | 0.324879 | [0.231966, 0.408313] |

All 45 rows were complete and finite; no MetaQ run failed. Both prespecified partial associations were positive with intervals above zero across all seeds.

## Evidence

- Exact rows: `revision_results/phase2/07_trimodal/rna_protein/MetaQ_seed{0,1,2}.csv`
- Server logs: `/data/zhangpeiru/GARQ_revision/revision_results/phase2/logs/P2_E7_D18_RNAPROTEIN_MetaQ_seed{0,1,2}.driver.log`
- Workflow: `revision_exp/workflows/d18_rna_protein_benchmark.py`

## Safe wording and limitations

Safe interim wording: “Across three descriptive realized-K-matched MetaQ aggregations, both prespecified RNA–protein pairs retained positive within-cell-type associations.”

Do not call these causal, held-out, or de-circularized. These full-feature assignments used the markers being evaluated. The results are also unfavorable to any claim that positive association recovery is GARQ-specific: MetaQ effects are comparably or more strongly positive in these prespecified pairs.
