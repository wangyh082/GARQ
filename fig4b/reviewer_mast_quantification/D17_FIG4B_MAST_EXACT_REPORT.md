# D17 Figure 4b Mast-cell exact assignment report

Status: **BLOCKED at required dry-run gate** unless all five frozen assignments are exact K=403 and cell-ID alignment is verified.

This report follows `GARQ_Fig4b_MastCells_Exact_Assignment_Codex_Prompt.md`; no training, K selection, assignment change, or result-driven threshold change was performed.

## Dry-run evidence

- Input inventory: `/data/zhangpeiru/GARQ_revision/fig4b/reviewer_mast_quantification/input_inventory.csv`
- ID alignment: `/data/zhangpeiru/GARQ_revision/fig4b/reviewer_mast_quantification/id_alignment_checks.csv`
- Dry-run log: `/data/zhangpeiru/GARQ_revision/fig4b/reviewer_mast_quantification/DRY_RUN.md`

## Assignment audit

| Method | Candidate key(s) | Realized K | ID/order check | Status | Reason |
|---|---|---:|---|---|---|
| GARQ | metacell | 403 | verified row order | PASS | numeric row-order IDs verified by exact canonical label vector |
| MetaQ | metacell | 403 | verified row order | PASS | numeric row-order IDs verified by exact canonical label vector |
| SEACells | SEACell | 403 | ID set | PASS |  |
| MetaCell V2 | metacell;membership |  | unverified | BLOCKED | multiple candidate assignment keys; manual semantic resolution required |
| SuperCell | metacell | 404 | verified row order | BLOCKED | numeric row-order IDs verified by exact canonical label vector; realized K is not exact Figure 4b K=403 |

## Input inventory

Audited H5AD files: 17. Full paths and fast fingerprints are in `/data/zhangpeiru/GARQ_revision/fig4b/reviewer_mast_quantification/input_inventory.csv`.

## Scientific boundary

The attached specification requires one exact frozen K=403 assignment per method and forbids silently deleting groups, remapping K, or substituting a different file. Any Mast-cell recall, purity, enrichment, or permutation result would be non-exact while the audit blockers remain. A diagnostic non-exact analysis requires an explicit author decision and must be labelled separately.
