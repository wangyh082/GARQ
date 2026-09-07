"""Render the exact Figure 4b audit/dry-run evidence as a reviewer report."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--result-dir", required=True, type=Path)
    args = parser.parse_args()
    result = args.result_dir.resolve()
    dry = result / "DRY_RUN.md"
    inv = result / "input_inventory.csv"
    align = result / "id_alignment_checks.csv"
    report = result / "D17_FIG4B_MAST_EXACT_REPORT.md"
    rows = list(csv.DictReader(inv.open(encoding="utf-8"))) if inv.exists() else []
    arows = list(csv.DictReader(align.open(encoding="utf-8"))) if align.exists() else []
    with report.open("w", encoding="utf-8") as fh:
        fh.write("# D17 Figure 4b Mast-cell exact assignment report\n\n")
        fh.write("Status: **BLOCKED at required dry-run gate** unless all five frozen assignments are exact K=403 and cell-ID alignment is verified.\n\n")
        fh.write("This report follows `GARQ_Fig4b_MastCells_Exact_Assignment_Codex_Prompt.md`; no training, K selection, assignment change, or result-driven threshold change was performed.\n\n")
        fh.write("## Dry-run evidence\n\n")
        fh.write(f"- Input inventory: `{inv}`\n- ID alignment: `{align}`\n- Dry-run log: `{dry}`\n\n")
        fh.write("## Assignment audit\n\n| Method | Candidate key(s) | Realized K | ID/order check | Status | Reason |\n|---|---|---:|---|---|---|\n")
        for r in arows:
            check = "ID set" if r.get("id_set_equality") == "True" else ("verified row order" if r.get("row_order_verified_by_label_vector") == "True" else "unverified")
            fh.write(f"| {r.get('method','')} | {r.get('candidate_keys','')} | {r.get('realized_K','')} | {check} | {r.get('status','')} | {r.get('reason','')} |\n")
        fh.write("\n## Input inventory\n\n")
        fh.write(f"Audited H5AD files: {len(rows)}. Full paths and fast fingerprints are in `{inv}`.\n\n")
        fh.write("## Scientific boundary\n\n")
        fh.write("The attached specification requires one exact frozen K=403 assignment per method and forbids silently deleting groups, remapping K, or substituting a different file. Any Mast-cell recall, purity, enrichment, or permutation result would be non-exact while the audit blockers remain. A diagnostic non-exact analysis requires an explicit author decision and must be labelled separately.\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
