"""Summarize E1 targeted rare-abundance runs into the planned long table."""

import json
from pathlib import Path

import pandas as pd


def main() -> None:
    result_root = Path("revision_results")
    root = result_root / "01_size_resolution" / "rare_subsampling"
    rows = []
    for done_path in sorted(root.glob("**/*.done.json")):
        run_dir = done_path.parent
        done = json.loads(done_path.read_text(encoding="utf-8"))
        config = json.loads(Path(done["resolved_config"]).read_text(encoding="utf-8"))
        provenance = json.loads((run_dir / "subset_provenance.json").read_text(encoding="utf-8"))
        size = pd.read_csv(run_dir / "metacell_size_summary.csv").iloc[0]
        per_type = pd.read_csv(run_dir / "per_type_metrics_long.csv")
        target_label = config["rare_subsampling"]["target_label"]
        target = per_type.loc[per_type["cell_type"] == target_label]
        if len(target) != 1:
            raise ValueError(f"Expected one target row for {target_label!r} in {run_dir}")
        target = target.iloc[0]
        rows.append(
            {
                "dataset": config["dataset"],
                "method": "GARQ",
                "seed": config["seed"],
                "subset_seed": config["rare_subsampling"]["seed"],
                "target_cell_type": target_label,
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
    pd.DataFrame(rows).to_csv(root.parent / "rare_subsampling_long.csv", index=False)


if __name__ == "__main__":
    main()
