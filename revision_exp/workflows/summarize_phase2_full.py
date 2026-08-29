"""Aggregate completed Phase 2 full-data GARQ runs into preregistered long tables."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd


def _concat(paths: list[Path]) -> pd.DataFrame:
    return pd.concat([pd.read_csv(path) for path in paths], ignore_index=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase2-root", type=Path, default=Path("revision_results/phase2"))
    args = parser.parse_args()
    out = args.phase2_root / "01_size_resolution"
    (args.phase2_root / "02_modality").mkdir(parents=True, exist_ok=True)
    (args.phase2_root / "08_scalability").mkdir(parents=True, exist_ok=True)
    run_dirs = sorted(
        path.parent
        for path in out.glob("*/GARQ/full_seed*_K002/*.done.json")
        if json.loads(path.read_text())["status"] == "PASS"
    )
    if not run_dirs:
        raise RuntimeError("No completed Phase 2 full-data GARQ runs found")

    size = _concat([path / "metacell_size_summary.csv" for path in run_dirs])
    per_type = _concat([path / "per_type_metrics_long.csv" for path in run_dirs])
    block = _concat([path / "modality_block_contribution.csv" for path in run_dirs])
    stages = _concat([path / "stage_profile.csv" for path in run_dirs])

    keys = ["dataset", "method", "seed", "implementation_tag", "resolution"]
    macro = (
        per_type.groupby(keys, as_index=False)
        .agg(
            cell_type_count=("cell_type", "nunique"),
            balanced_accuracy=("cell_recall", "mean"),
            macro_precision=("cell_precision", "mean"),
            macro_recall=("cell_recall", "mean"),
            macro_f1=("cell_f1", "mean"),
            mean_purity_unweighted=("purity_unweighted", "mean"),
            mean_majority_retention=("majority_retention", "mean"),
            mean_high_purity_recovery=("high_purity_recovery", "mean"),
        )
    )
    weighted_rows = []
    for group_key, frame in per_type.groupby(keys, sort=True):
        support = frame["support"].to_numpy(float)
        denom = support.sum()
        weighted_rows.append(
            dict(
                zip(keys, group_key),
                weighted_precision=float(np.average(frame["cell_precision"], weights=support)),
                weighted_recall=float(np.average(frame["cell_recall"], weights=support)),
                weighted_f1=float(np.average(frame["cell_f1"], weights=support)),
                evaluated_cells=int(denom),
            )
        )
    benchmark = size.merge(macro, on=keys, how="left", validate="one_to_one")
    benchmark = benchmark.merge(pd.DataFrame(weighted_rows), on=keys, how="left", validate="one_to_one")

    runtime_rows = []
    for run_dir in run_dirs:
        done = json.loads(next(run_dir.glob("*.done.json")).read_text())
        assignments = pd.read_csv(run_dir / "cell_assignments.csv", usecols=["dataset", "seed"])
        runtime_rows.append(
            {
                "dataset": assignments["dataset"].iloc[0],
                "seed": int(assignments["seed"].iloc[0]),
                "wall_time_seconds": float(done["wall_time_seconds"]),
                "peak_cpu_rss_bytes": int(done["peak_cpu_rss_bytes"]),
                "run_id": done["run_id"],
            }
        )
    benchmark = benchmark.merge(pd.DataFrame(runtime_rows), on=["dataset", "seed"], how="left", validate="one_to_one")

    size.to_csv(out / "metacell_size_summary.csv", index=False)
    per_type.to_csv(out / "per_type_metrics_long.csv", index=False)
    benchmark.to_csv(out / "full_benchmark_long.csv", index=False)
    block.to_csv(args.phase2_root / "02_modality" / "modality_block_contribution_full.csv", index=False)
    stages.to_csv(args.phase2_root / "08_scalability" / "stage_profile.csv", index=False)
    print(json.dumps({"runs": len(run_dirs), "datasets": sorted(size.dataset.unique()), "rows": {"benchmark": len(benchmark), "size": len(size), "per_type": len(per_type), "block": len(block), "stages": len(stages)}}, indent=2))


if __name__ == "__main__":
    main()
