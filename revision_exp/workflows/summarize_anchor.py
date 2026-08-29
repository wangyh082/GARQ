"""Collect E4 smoke traces and label-permutation-invariant comparisons."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from revision_exp.metrics.assignment import compare_assignments


def main() -> None:
    root = Path("revision_results/04_anchor")
    trace_tables = []
    summary_rows = []
    for dataset in ("D5", "D11"):
        legacy_dir = root / f"{dataset}_legacy_continuous_smoke"
        legacy_ids = pd.read_csv(legacy_dir / "cell_assignments.csv")["metacell_id"].to_numpy()
        for run_dir in sorted(root.glob(f"{dataset}_*_smoke")):
            trace = pd.read_csv(run_dir / "anchor_dynamics_step.csv")
            trace.insert(0, "run", run_dir.name)
            trace.insert(0, "dataset", dataset)
            trace_tables.append(trace)
            assignments = pd.read_csv(run_dir / "cell_assignments.csv")["metacell_id"].to_numpy()
            comparison = compare_assignments(legacy_ids, assignments)
            size = pd.read_csv(run_dir / "metacell_size_summary.csv").iloc[0]
            summary_rows.append(
                {
                    "dataset": dataset,
                    "run": run_dir.name,
                    "implementation_tag": size["implementation_tag"],
                    "requested_K": int(size["requested_K"]),
                    "realized_K": int(size["realized_K"]),
                    "size_gini": float(size["size_gini"]),
                    "size_median": float(size["size_median"]),
                    "size_max": float(size["size_max"]),
                    "ARI_vs_legacy": comparison["ARI"],
                    "NMI_vs_legacy": comparison["NMI"],
                    "VI_nats_vs_legacy": comparison["VI_nats"],
                    "coassignment_agreement_rand_vs_legacy": comparison["coassignment_agreement_rand"],
                    "quantized_steps": len(trace),
                    "reposition_steps": int(trace["reposition_due"].sum()),
                    "local_branch_steps": int(trace["local_branch_executed"].sum()),
                    "manual_displacement_anchor_events": int(trace["manual_displacement_anchor_count"].sum()),
                    "final_usage_perplexity": float(trace["usage_perplexity"].iloc[-1]),
                    "final_usage_gini": float(trace["usage_gini"].iloc[-1]),
                    "anchor_nan_count_max": int(trace["anchor_nan_count"].max()),
                    "anchor_inf_count_max": int(trace["anchor_inf_count"].max()),
                }
            )
    pd.concat(trace_tables, ignore_index=True).to_csv(root / "anchor_dynamics_step.csv", index=False)
    pd.DataFrame(summary_rows).to_csv(root / "anchor_schedule_ablation.csv", index=False)


if __name__ == "__main__":
    main()
