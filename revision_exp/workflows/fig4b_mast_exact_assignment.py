"""Exact Figure 4b Mast-cell assignment audit and quantification.

The workflow intentionally refuses to infer a different K or silently resolve
ambiguous assignment columns.  ``--dry-run`` is the required first step and
writes a complete input/audit record even when the exact Figure 4b preconditions
are not met.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Sequence


CANONICAL_RNA = "/home/zhangpeiru/data/analysis/new/kidney_rna_updated.h5ad"
CANONICAL_ATAC = "/home/zhangpeiru/data/analysis/new/kidney_atac_updated.h5ad"
REQUESTED_K = 403
EXPECTED_N = 16143
METHOD_ORDER = ["GARQ", "MetaQ", "SEACells", "MetaCell V2", "SuperCell"]
ASSIGNMENT_PATHS = {
    "GARQ": "/home/zhangpeiru/results/1_ours/RNA_ATAC/kidney/kidney403_403metacell_k5_ids.h5ad",
    "MetaQ": "/home/zhangpeiru/results/2_MetaQ/RNA_ATAC/kidney/kidney403_403metacell_ids.h5ad",
    "SEACells": "/home/zhangpeiru/vscode/SEACells-main/ours/save/RNA+ATAC/kidney/kidney_ad.h5ad",
    "MetaCell V2": "/home/zhangpeiru/results/4_mc2/RNA_ATAC/kidney/kidney_metacells2_ad.h5ad",
    "SuperCell": "/home/zhangpeiru/results/5_supercell/RNA_ATAC/kidney/kidney_supercell.h5ad",
}
PROFILE_PATHS = {
    "GARQ RNA": "/home/zhangpeiru/data/analysis/new/kidney_403metacell_rna.h5ad",
    "GARQ ATAC": "/home/zhangpeiru/data/analysis/new/kidney_403metacell_atac.h5ad",
    "MetaQ RNA": "/home/zhangpeiru/results/2_MetaQ/RNA_ATAC/kidney/kidney_RNA_403metacell.h5ad",
    "MetaQ ATAC": "/home/zhangpeiru/results/2_MetaQ/RNA_ATAC/kidney/kidney_ATAC_403metacell.h5ad",
    "SEACells RNA": "/home/zhangpeiru/vscode/SEACells-main/ours/save/RNA+ATAC/kidney/kidney_rna_metacells.h5ad",
    "SEACells ATAC": "/home/zhangpeiru/vscode/SEACells-main/ours/save/RNA+ATAC/kidney/kidney_atac_metacells.h5ad",
    "MetaCell V2 RNA": "/home/zhangpeiru/results/4_mc2/RNA_ATAC/kidney/kidney_rna_metacells.h5ad",
    "MetaCell V2 ATAC": "/home/zhangpeiru/results/4_mc2/RNA_ATAC/kidney/kidney_atac_metacells.h5ad",
    "SuperCell RNA": "/home/zhangpeiru/results/5_supercell/RNA_ATAC/kidney/kidney_rna_metacells.h5ad",
    "SuperCell ATAC": "/home/zhangpeiru/results/5_supercell/RNA_ATAC/kidney/kidney_atac_metacells.h5ad",
}
ALLOWED_ASSIGNMENT_KEYS = (
    "metacell",
    "metacell_id",
    "SEACell",
    "SEACells",
    "supercell",
    "membership",
    "cluster",
)
LABEL_KEYS = ("celltype", "cell_type", "annotation", "CellType")


def _fast_fingerprint(path: str, chunk_size: int = 1024 * 1024) -> str:
    """Return a reproducible fingerprint without hashing multi-GB H5AD files."""
    st = os.stat(path)
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        first = fh.read(chunk_size)
        h.update(first)
        if st.st_size > chunk_size:
            fh.seek(max(0, st.st_size - chunk_size))
            h.update(fh.read(chunk_size))
    return f"fastsha256:{h.hexdigest()}:size={st.st_size}:mtime_ns={st.st_mtime_ns}"


def _jsonable(value: Any) -> Any:
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    if isinstance(value, (list, tuple)):
        return [_jsonable(v) for v in value]
    if isinstance(value, Mapping):
        return {str(k): _jsonable(v) for k, v in value.items()}
    return str(value)


def _audit_h5ad(path: str, label: str) -> Dict[str, Any]:
    row: Dict[str, Any] = {"label": label, "absolute_path": os.path.abspath(path)}
    if not os.path.exists(path):
        row.update({"exists": False, "status": "BLOCKED_MISSING_FILE"})
        return row
    row.update(
        {
            "exists": True,
            "file_size": os.path.getsize(path),
            "fingerprint": _fast_fingerprint(path),
        }
    )
    try:
        import anndata as ad

        obj = ad.read_h5ad(path, backed="r")
        row.update(
            {
                "n_obs": int(obj.n_obs),
                "n_vars": int(obj.n_vars),
                "obs_names_unique": bool(obj.obs_names.is_unique),
                "obs_columns": json.dumps(list(obj.obs.columns), ensure_ascii=False),
                "obsm_keys": json.dumps(list(obj.obsm.keys()), ensure_ascii=False),
                "layers": json.dumps(list(obj.layers.keys()), ensure_ascii=False),
                "x_type": type(obj.X).__name__,
                "x_dtype": str(getattr(obj.X, "dtype", "unknown")),
                "status": "PASS_AUDIT",
            }
        )
        obj.file.close()
    except Exception as exc:  # pragma: no cover - environment-specific HDF5 errors
        row.update({"status": "BLOCKED_READ_ERROR", "error": repr(exc)})
    return row


def _write_csv(path: Path, rows: Sequence[Mapping[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    keys: List[str] = []
    for row in rows:
        for key in row:
            if key not in keys:
                keys.append(key)
    with path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=keys, extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({k: _jsonable(row.get(k, "")) for k in keys})


def _candidate_keys(obs: Any, n_total: int) -> List[str]:
    candidates: List[str] = []
    for key in ALLOWED_ASSIGNMENT_KEYS:
        if key not in obs.columns:
            continue
        series = obs[key]
        if len(series) != n_total or bool(series.isna().any()):
            continue
        if int(series.nunique(dropna=False)) > 0:
            candidates.append(key)
    return candidates


def _numeric_row_order(obs_names: Iterable[Any], n_total: int) -> bool:
    values = [str(v) for v in obs_names]
    return values == [str(i) for i in range(n_total)]


def _canonical_labels(obj: Any, label_key: str) -> List[str]:
    return [str(v) for v in obj.obs[label_key].astype(str).tolist()]


def _audit_assignments(canonical: Any, label_key: str) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    canonical_ids = [str(v) for v in canonical.obs_names]
    canonical_labels = _canonical_labels(canonical, label_key)
    n_total = len(canonical_ids)
    for method in METHOD_ORDER:
        path = ASSIGNMENT_PATHS[method]
        row: Dict[str, Any] = {
            "method": method,
            "assignment_path": path,
            "requested_K": REQUESTED_K,
            "n_cells": "",
            "candidate_keys": "",
            "assignment_key": "",
            "realized_K": "",
            "min_group_size": "",
            "median_group_size": "",
            "max_group_size": "",
            "id_set_equality": False,
            "order_equality": False,
            "row_order_verified_by_label_vector": False,
            "status": "BLOCKED",
            "reason": "",
        }
        try:
            import anndata as ad

            obj = ad.read_h5ad(path, backed="r")
            row["n_cells"] = int(obj.n_obs)
            candidates = _candidate_keys(obj.obs, n_total)
            row["candidate_keys"] = ";".join(candidates)
            if not candidates:
                row["reason"] = "no allowed non-null assignment key"
                rows.append(row)
                obj.file.close()
                continue
            if len(candidates) > 1:
                row["reason"] = "multiple candidate assignment keys; manual semantic resolution required"
                rows.append(row)
                obj.file.close()
                continue
            key = candidates[0]
            row["assignment_key"] = key
            groups = obj.obs[key].astype(str).to_numpy()
            unique, counts = __import__("numpy").unique(groups, return_counts=True)
            row.update(
                {
                    "realized_K": int(len(unique)),
                    "min_group_size": int(counts.min()),
                    "median_group_size": float(__import__("numpy").median(counts)),
                    "max_group_size": int(counts.max()),
                }
            )
            ids = [str(v) for v in obj.obs_names]
            row["id_set_equality"] = set(ids) == set(canonical_ids)
            row["order_equality"] = ids == canonical_ids
            if not row["id_set_equality"] and _numeric_row_order(ids, n_total):
                if label_key in obj.obs.columns and _canonical_labels(obj, label_key) == canonical_labels:
                    row["row_order_verified_by_label_vector"] = True
                    row["reason"] = "numeric row-order IDs verified by exact canonical label vector"
                else:
                    row["reason"] = "numeric row-order IDs lack verifiable canonical label vector"
            if int(row["realized_K"]) != REQUESTED_K:
                row["reason"] = (row["reason"] + "; " if row["reason"] else "") + "realized K is not exact Figure 4b K=403"
            if not row["id_set_equality"] and not row["row_order_verified_by_label_vector"]:
                row["reason"] = (row["reason"] + "; " if row["reason"] else "") + "cell-ID alignment not verified"
            if int(row["realized_K"]) == REQUESTED_K and (row["id_set_equality"] or row["row_order_verified_by_label_vector"]):
                row["status"] = "PASS"
            obj.file.close()
        except Exception as exc:
            row["reason"] = f"read/audit error: {exc!r}"
        rows.append(row)
    return rows


def _write_config(path: Path, figure_dir: Path, output_dir: Path, n_permutations: int) -> None:
    config = {
        "dataset": "D17 Human_Kidney_Cancer",
        "figure_dir": str(figure_dir),
        "output_dir": str(output_dir),
        "requested_K": REQUESTED_K,
        "n_cells_expected": EXPECTED_N,
        "canonical_label_priority": list(LABEL_KEYS),
        "associated_definition": {"m_min": 3, "fold_enrichment_min": 5, "bh_q_max": 0.05},
        "permutation": {"n_permutations": n_permutations, "random_seed": 20260907},
        "method_order": METHOD_ORDER,
        "assignment_paths": ASSIGNMENT_PATHS,
        "profile_paths": PROFILE_PATHS,
        "analysis_mode": "exact_frozen_figure4b_assignment",
    }
    with path.open("w", encoding="utf-8") as fh:
        try:
            import yaml

            yaml.safe_dump(config, fh, sort_keys=False, allow_unicode=True)
        except Exception:
            json.dump(config, fh, indent=2, ensure_ascii=False)


def run_audit(figure_dir: Path, output_dir: Path, n_permutations: int, dry_run: bool) -> int:
    output_dir.mkdir(parents=True, exist_ok=True)
    inventory_paths = {"canonical RNA": CANONICAL_RNA, "canonical ATAC": CANONICAL_ATAC}
    inventory_paths.update({f"assignment {k}": v for k, v in ASSIGNMENT_PATHS.items()})
    inventory_paths.update({f"profile {k}": v for k, v in PROFILE_PATHS.items()})
    inventory = [_audit_h5ad(path, label) for label, path in inventory_paths.items()]
    _write_csv(output_dir / "input_inventory.csv", inventory)

    blockers: List[str] = []
    if not figure_dir.exists():
        blockers.append(f"Figure 4b source directory does not exist: {figure_dir}")
    canonical_rows = [r for r in inventory if r["label"] == "canonical RNA"]
    try:
        import anndata as ad

        canonical = ad.read_h5ad(CANONICAL_RNA, backed="r")
        label_key = next((k for k in LABEL_KEYS if k in canonical.obs.columns), None)
        if canonical.n_obs != EXPECTED_N:
            blockers.append(f"canonical RNA n_obs={canonical.n_obs}, expected {EXPECTED_N}")
        atac = ad.read_h5ad(CANONICAL_ATAC, backed="r")
        if list(map(str, canonical.obs_names)) != list(map(str, atac.obs_names)):
            blockers.append("canonical RNA/ATAC obs_names are not identical")
        if label_key is None:
            blockers.append("no exact-priority label key found in canonical RNA")
        else:
            labels = set(_canonical_labels(canonical, label_key))
            if "Mast Cells" not in labels:
                blockers.append("exact label 'Mast Cells' is absent from canonical metadata")
            with (output_dir / "canonical_label_audit.json").open("w", encoding="utf-8") as fh:
                json.dump({"label_key": label_key, "n_total": canonical.n_obs, "unique_labels": sorted(labels), "mast_count": _canonical_labels(canonical, label_key).count("Mast Cells")}, fh, indent=2, ensure_ascii=False)
            alignment = _audit_assignments(canonical, label_key)
            for row in alignment:
                if row["status"] != "PASS":
                    blockers.append(f"{row['method']}: {row['reason']}")
        _write_csv(output_dir / "id_alignment_checks.csv", alignment if label_key else [])
        canonical.file.close()
        atac.file.close()
    except Exception as exc:
        blockers.append(f"canonical metadata audit failed: {exc!r}")
        _write_csv(output_dir / "id_alignment_checks.csv", [])

    _write_config(output_dir / "resolved_config.yaml", figure_dir, output_dir, n_permutations)
    status = "BLOCKED" if blockers else "PASS"
    with (output_dir / "DRY_RUN.md").open("w", encoding="utf-8") as fh:
        fh.write("# Figure 4b Mast exact-assignment dry-run\n\n")
        fh.write(f"Status: **{status}**\n\n")
        fh.write(f"Figure directory: `{figure_dir}` (exists={figure_dir.exists()})\n\n")
        fh.write("The dry-run does not train or modify any assignment.\n\n")
        if blockers:
            fh.write("## Blocking findings\n\n")
            for item in blockers:
                fh.write(f"- {item}\n")
            fh.write("\nFormal quantification was not started because the attached specification requires exact K=403 and unambiguous ID alignment.\n")
        else:
            fh.write("All exact preconditions passed; the formal run may proceed.\n")
    if dry_run or blockers:
        return 2 if blockers else 0
    # The full computation is intentionally kept behind the validated gate.
    # It is implemented in a follow-up step so that a failed dry-run can never
    # accidentally produce a scientifically mislabelled Figure 4b result.
    raise RuntimeError("formal computation gate reached without an implementation")


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--figure-dir", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--n-permutations", type=int, default=10000)
    args = parser.parse_args(argv)
    return run_audit(args.figure_dir.resolve(), args.output_dir.resolve(), args.n_permutations, args.dry_run)


if __name__ == "__main__":
    raise SystemExit(main())
