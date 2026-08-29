"""Recompute label-dependent metrics from frozen assignments without retraining."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import anndata as ad
import pandas as pd

from revision_exp.metrics.metacell import per_type_table


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", type=Path, required=True)
    parser.add_argument("--source-h5ad", type=Path, required=True)
    parser.add_argument("--source-label-key", required=True)
    parser.add_argument("--implementation-tag", default="instrumented_legacy")
    args = parser.parse_args()

    assignments = pd.read_csv(args.run_dir / "cell_assignments.csv")
    source = ad.read_h5ad(args.source_h5ad, backed="r")
    labels = pd.Series(source.obs[args.source_label_key].astype(str).to_numpy(), index=source.obs_names.astype(str))
    assignments["cell_type"] = assignments["cell_id"].astype(str).map(labels)
    if assignments["cell_type"].isna().any():
        raise ValueError(f"Unmatched labels: {int(assignments['cell_type'].isna().sum())}")
    dataset = str(assignments["dataset"].iloc[0])
    seed = int(assignments["seed"].iloc[0])
    requested_k = int(assignments["requested_K"].iloc[0])
    metadata = {
        "dataset": dataset,
        "method": str(assignments["method"].iloc[0]),
        "seed": seed,
        "implementation_tag": args.implementation_tag,
        "resolution": requested_k / len(assignments),
    }
    result = per_type_table(assignments, metadata)
    result.to_csv(args.run_dir / "per_type_metrics_long.csv", index=False)
    correction = {
        "correction_tag": "evaluation_correction_label_key",
        "training_or_assignment_changed": False,
        "dataset": dataset,
        "seed": seed,
        "source_h5ad": str(args.source_h5ad),
        "source_label_key": args.source_label_key,
        "matched_cells": len(assignments),
        "output": str(args.run_dir / "per_type_metrics_long.csv"),
    }
    (args.run_dir / "evaluation_correction_label_key.json").write_text(json.dumps(correction, indent=2) + "\n")
    print(json.dumps(correction, indent=2))


if __name__ == "__main__":
    main()
