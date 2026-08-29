"""Aggregate E3 fixed-representation smoke controls."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from revision_exp.metrics.assignment import compare_assignments


def main() -> None:
    root = Path("revision_results/03_controlled_benchmark")
    run_dirs = sorted(root.glob("D*_fixed_representation_smoke"))
    benchmarks = [pd.read_csv(path / "fixed_representation_benchmark.csv") for path in run_dirs]
    per_type = [pd.read_csv(path / "fixed_representation_per_type.csv") for path in run_dirs]
    pd.concat(benchmarks, ignore_index=True).to_csv(root / "fixed_representation_benchmark.csv", index=False)
    pd.concat(per_type, ignore_index=True).to_csv(root / "fixed_representation_per_type.csv", index=False)
    garq_paths = {
        "D5": Path("revision_results/02_modality/smoke/D5/RNA_ADT_seed0/cell_assignments.csv"),
        "D11": Path("revision_results/02_modality/smoke/D11/RNA_ATAC_seed0/cell_assignments.csv"),
        "D17": Path("revision_results/02_modality/smoke/D17/RNA_ATAC_seed0/cell_assignments.csv"),
        "D18": Path("revision_results/02_modality/smoke/D18/RNA_ATAC_ADT_seed0/cell_assignments.csv"),
    }
    rows = []
    for run_dir in run_dirs:
        dataset = run_dir.name.split("_", 1)[0]
        garq = pd.read_csv(garq_paths[dataset]).set_index("cell_id")
        for method in ("KMeans", "MiniBatchKMeans"):
            control = pd.read_csv(run_dir / f"cell_assignments_{method}.csv").set_index("cell_id")
            if set(control.index) != set(garq.index):
                raise ValueError(f"Cell set mismatch for {dataset}/{method}")
            garq_aligned = garq.loc[control.index, "metacell_id"].to_numpy()
            comparison = compare_assignments(garq_aligned, control["metacell_id"].to_numpy())
            rows.append(
                {
                    "dataset": dataset,
                    "seed": 0,
                    "control_method": method,
                    "control_representation": "fixed_equal_weight_PCA_LSI_CLR",
                    "reference_method": "GARQ",
                    "reference_representation": "GARQ_learned_embedding",
                    "comparison_scope": "cross_pipeline_partition_agreement_not_quality",
                    **comparison,
                }
            )
    pd.DataFrame(rows).to_csv(root / "fixed_vs_garq_partition_agreement.csv", index=False)


if __name__ == "__main__":
    main()
