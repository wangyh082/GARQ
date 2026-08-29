"""Summarize recovered-dataset E1 confirmatory-design smoke runs."""

import json
from pathlib import Path

import pandas as pd


def main() -> None:
    root = Path("revision_results/01_size_resolution/rare_confirmatory")
    rows = []
    for done_path in sorted(root.glob("**/*.done.json")):
        run_dir = done_path.parent
        done = json.loads(done_path.read_text(encoding="utf-8"))
        config = json.loads(Path(done["resolved_config"]).read_text(encoding="utf-8"))
        provenance = json.loads((run_dir / "subset_provenance.json").read_text(encoding="utf-8"))
        size = pd.read_csv(run_dir / "metacell_size_summary.csv").iloc[0]
        per_type = pd.read_csv(run_dir / "per_type_metrics_long.csv")
        label = config["rare_subsampling"]["target_label"]
        target = per_type.loc[per_type["cell_type"] == label]
        if len(target) != 1:
            raise ValueError(f"Expected one target row for {label!r} in {run_dir}")
        target = target.iloc[0]
        rows.append(
            {
                "dataset": config["dataset"],
                "method": "GARQ",
                "seed": config["seed"],
                "subset_seed": config["rare_subsampling"]["seed"],
                "target_cell_type": label,
                "source_abundance": provenance["source_target_abundance"],
                "target_abundance": provenance["target_abundance_requested"],
                "realized_abundance": provenance["target_abundance_realized"],
                "support": int(target["support"]),
                "requested_K": int(size["requested_K"]),
                "realized_K": int(size["realized_K"]),
                "cell_precision": target["cell_precision"],
                "cell_recall": target["cell_recall"],
                "cell_f1": target["cell_f1"],
                "purity_unweighted": target["purity_unweighted"],
                "purity_weighted": target["purity_weighted"],
                "majority_retention": target["majority_retention"],
                "high_purity_recovery": target["high_purity_recovery"],
                "run_id": done["run_id"],
            }
        )
    frame = pd.DataFrame(rows)
    if frame.empty:
        raise ValueError(f"No completed confirmatory runs found under {root}")
    frame = frame.sort_values(
        ["dataset", "target_cell_type", "target_abundance", "seed"]
    ).reset_index(drop=True)
    frame.to_csv(root.parent / "rare_confirmatory_smoke_long.csv", index=False)

    group_keys = ["dataset", "method", "target_cell_type", "target_abundance"]
    grouped = frame.groupby(group_keys, sort=True, dropna=False)
    summary = grouped.agg(
        n_seeds=("seed", "nunique"),
        support=("support", "first"),
        realized_abundance_mean=("realized_abundance", "mean"),
        realized_abundance_sd=("realized_abundance", "std"),
        realized_K_mean=("realized_K", "mean"),
        realized_K_sd=("realized_K", "std"),
        cell_precision_mean=("cell_precision", "mean"),
        cell_precision_sd=("cell_precision", "std"),
        cell_recall_mean=("cell_recall", "mean"),
        cell_recall_sd=("cell_recall", "std"),
        cell_f1_mean=("cell_f1", "mean"),
        cell_f1_sd=("cell_f1", "std"),
        purity_unweighted_mean=("purity_unweighted", "mean"),
        purity_unweighted_sd=("purity_unweighted", "std"),
        purity_weighted_mean=("purity_weighted", "mean"),
        purity_weighted_sd=("purity_weighted", "std"),
        majority_retention_mean=("majority_retention", "mean"),
        majority_retention_sd=("majority_retention", "std"),
        high_purity_recovery_mean=("high_purity_recovery", "mean"),
        high_purity_recovery_sd=("high_purity_recovery", "std"),
    ).reset_index()
    summary["nonzero_f1_runs"] = grouped["cell_f1"].apply(
        lambda values: int((values > 0).sum())
    ).to_numpy()
    summary["majority_retention_runs"] = grouped["majority_retention"].apply(
        lambda values: int((values > 0).sum())
    ).to_numpy()
    summary["high_purity_recovery_runs"] = grouped["high_purity_recovery"].apply(
        lambda values: int((values > 0).sum())
    ).to_numpy()
    summary.to_csv(
        root.parent / "rare_confirmatory_smoke_summary.csv", index=False
    )


if __name__ == "__main__":
    main()
