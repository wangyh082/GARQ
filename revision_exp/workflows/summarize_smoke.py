"""Consolidate traceable E1/E2 smoke outputs with the independent evaluator."""

from __future__ import annotations

import itertools
from pathlib import Path

import pandas as pd

from revision_exp.metrics.assignment import compare_assignments


def _concat(files: list[Path], output: Path) -> None:
    frames = [pd.read_csv(path).assign(source_file=str(path)) for path in files]
    output.parent.mkdir(parents=True, exist_ok=True)
    pd.concat(frames, ignore_index=True).to_csv(output, index=False)


def _combination(path: Path) -> str:
    return path.parent.name.replace("_seed0", "").replace("_", "+")


def _canonical_cell_ids(dataset: str, values: pd.Series) -> pd.Series:
    values = values.astype(str)
    if dataset == "D18":
        return values.str.replace(r"\.([0-9]+)$", r"-\1", regex=True)
    return values


def summarize(result_root: Path) -> None:
    e1_root = result_root / "01_size_resolution"
    e2_root = result_root / "02_modality"
    tables = result_root / "tables"
    e1_files = sorted(e1_root.glob("smoke/*/*/metacell_size_long.csv"))
    _concat(e1_files, e1_root / "metacell_size_long.csv")
    _concat(
        sorted(e1_root.glob("smoke/*/*/metacell_size_summary.csv")),
        e1_root / "metacell_size_summary.csv",
    )
    _concat(
        sorted(e1_root.glob("smoke/*/*/per_type_metrics_long.csv")),
        e1_root / "per_type_metrics_long.csv",
    )

    assignment_files = sorted(e2_root.glob("smoke/*/*/cell_assignments.csv"))
    runs: dict[str, dict[str, tuple[Path, pd.DataFrame]]] = {}
    summary_rows = []
    for assignment_path in assignment_files:
        frame = pd.read_csv(assignment_path)
        dataset = str(frame["dataset"].iloc[0])
        combination = _combination(assignment_path)
        runs.setdefault(dataset, {})[combination] = (assignment_path, frame)
        summary_path = assignment_path.with_name("metacell_size_summary.csv")
        summary = pd.read_csv(summary_path).iloc[0].to_dict()
        summary.update({"modality_combination": combination, "source_file": str(summary_path)})
        summary_rows.append(summary)

    comparison_rows = []
    for dataset, combinations in sorted(runs.items()):
        for name_a, name_b in itertools.combinations(sorted(combinations), 2):
            path_a, frame_a = combinations[name_a]
            path_b, frame_b = combinations[name_b]
            left = frame_a[["cell_id", "metacell_id"]].copy()
            right = frame_b[["cell_id", "metacell_id"]].copy()
            left["cell_id"] = _canonical_cell_ids(dataset, left["cell_id"])
            right["cell_id"] = _canonical_cell_ids(dataset, right["cell_id"])
            aligned = left.merge(right, on="cell_id", validate="one_to_one", suffixes=("_a", "_b")
            )
            if len(aligned) != len(frame_a) or len(aligned) != len(frame_b):
                raise ValueError(f"Incomplete cell-id overlap for {dataset}: {name_a} vs {name_b}")
            row = {
                "dataset": dataset,
                "combination_a": name_a,
                "combination_b": name_b,
                "source_assignment_a": str(path_a),
                "source_assignment_b": str(path_b),
            }
            row.update(compare_assignments(aligned["metacell_id_a"].to_numpy(), aligned["metacell_id_b"].to_numpy()))
            comparison_rows.append(row)

    e2_root.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(summary_rows).to_csv(e2_root / "modality_combination_metrics.csv", index=False)
    pd.DataFrame(comparison_rows).to_csv(e2_root / "modality_assignment_agreement.csv", index=False)
    _concat(
        sorted(e2_root.glob("smoke/*/*/per_type_metrics_long.csv")),
        e2_root / "per_type_metrics_long.csv",
    )
    tables.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(comparison_rows).to_csv(tables / "E2_smoke_assignment_agreement.csv", index=False)


if __name__ == "__main__":
    summarize(Path("revision_results"))
