"""Author-authorized same-compression Figure 4b frozen-assignment analysis.

This module is called only with the explicit --allow-nonexact-k option.  It
keeps the original requested K=403 in every table, but reports the realized K
of each frozen file without changing memberships.  No model is retrained.
"""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Sequence, Tuple

import numpy as np
import pandas as pd

from .fig4b_mast_exact_assignment import (
    ALLOWED_ASSIGNMENT_KEYS,
    ASSIGNMENT_PATHS,
    CANONICAL_ATAC,
    CANONICAL_RNA,
    EXPECTED_N,
    LABEL_KEYS,
    METHOD_ORDER,
    PROFILE_PATHS,
    REQUESTED_K,
    _audit_h5ad,
    _candidate_keys,
    _fast_fingerprint,
    _numeric_row_order,
)

EXPECTED_MAST_COUNT = 74
MARKERS = ("KIT", "TPSAB1", "TPSB2", "CPA3", "MS4A2", "HDC", "GATA2")


def _bh(values: Sequence[float]) -> np.ndarray:
    p = np.asarray(values, dtype=float)
    result = np.full(len(p), np.nan, dtype=float)
    finite = np.isfinite(p)
    if not finite.any():
        return result
    indices = np.flatnonzero(finite)
    order = indices[np.argsort(p[indices], kind="stable")]
    running = 1.0
    for rank in range(len(order) - 1, -1, -1):
        index = int(order[rank])
        running = min(running, p[index] * len(order) / (rank + 1))
        result[index] = running
    return result


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _md_table(frame: pd.DataFrame, digits: int = 4) -> str:
    if frame.empty:
        return "(no rows)"
    columns = [str(column) for column in frame.columns]
    output = ["| " + " | ".join(columns) + " |", "|" + "|".join("---" for _ in columns) + "|"]
    for values in frame.itertuples(index=False, name=None):
        rendered = []
        for value in values:
            if isinstance(value, (float, np.floating)):
                rendered.append("NA" if pd.isna(value) else f"{float(value):.{digits}f}")
            else:
                rendered.append(str(value))
        output.append("| " + " | ".join(rendered) + " |")
    return "\n".join(output)


def _partition_equivalent(left: Iterable[Any], right: Iterable[Any]) -> bool:
    forward: Dict[str, str] = {}
    reverse: Dict[str, str] = {}
    left_values = [str(v) for v in left]
    right_values = [str(v) for v in right]
    if len(left_values) != len(right_values):
        return False
    for a, b in zip(left_values, right_values):
        if a in forward and forward[a] != b:
            return False
        if b in reverse and reverse[b] != a:
            return False
        forward[a] = b
        reverse[b] = a
    return True


def _choose_key(method: str, candidates: Sequence[str], obs: Any) -> Tuple[str, str]:
    if len(candidates) == 1:
        return candidates[0], "single allowed candidate"
    if (
        method == "MetaCell V2"
        and "metacell" in candidates
        and "membership" in candidates
        and _partition_equivalent(obs["metacell"], obs["membership"])
    ):
        return (
            "metacell",
            "author override: metacell selected; membership is partition-equivalent",
        )
    raise ValueError("multiple candidate assignment keys are not equivalent")


def _audit_and_load() -> Tuple[str, List[str], pd.DataFrame, pd.DataFrame, Dict[str, np.ndarray], Dict[str, str]]:
    import anndata as ad

    canonical = ad.read_h5ad(CANONICAL_RNA, backed="r")
    atac = ad.read_h5ad(CANONICAL_ATAC, backed="r")
    try:
        ids = [str(v) for v in canonical.obs_names]
        label_key = next((key for key in LABEL_KEYS if key in canonical.obs.columns), None)
        if label_key is None:
            raise ValueError("no canonical label key")
        labels = [str(v) for v in canonical.obs[label_key].astype(str)]
        if canonical.n_obs != EXPECTED_N or atac.n_obs != EXPECTED_N:
            raise ValueError("canonical n_obs does not equal 16143")
        if list(map(str, atac.obs_names)) != ids:
            raise ValueError("canonical RNA/ATAC IDs differ")
        if labels.count("Mast Cells") != EXPECTED_MAST_COUNT:
            raise ValueError("canonical Mast Cells count is not 74")
    finally:
        canonical.file.close()
        atac.file.close()

    inventory_paths = {"canonical RNA": CANONICAL_RNA, "canonical ATAC": CANONICAL_ATAC}
    inventory_paths.update({f"assignment {key}": value for key, value in ASSIGNMENT_PATHS.items()})
    inventory_paths.update({f"profile {key}": value for key, value in PROFILE_PATHS.items()})
    inventory = pd.DataFrame([_audit_h5ad(path, label) for label, path in inventory_paths.items()])
    alignment_rows: List[Dict[str, Any]] = []
    groups_by_method: Dict[str, np.ndarray] = {}
    selected_keys: Dict[str, str] = {}
    for method in METHOD_ORDER:
        obj = ad.read_h5ad(ASSIGNMENT_PATHS[method], backed="r")
        try:
            candidates = _candidate_keys(obj.obs, len(ids))
            key, resolution = _choose_key(method, candidates, obj.obs)
            groups = obj.obs[key].astype(str).to_numpy()
            assignment_ids = [str(v) for v in obj.obs_names]
            id_set_equal = set(assignment_ids) == set(ids)
            order_equal = assignment_ids == ids
            if id_set_equal:
                groups = groups[pd.Index(assignment_ids).get_indexer(pd.Index(ids))]
                alignment = "cell-ID set equality; reordered by canonical IDs"
            elif _numeric_row_order(assignment_ids, len(ids)):
                if label_key not in obj.obs.columns or [str(v) for v in obj.obs[label_key].astype(str)] != labels:
                    raise ValueError("numeric row-order lacks exact label-vector provenance")
                alignment = "verified numeric row order by exact canonical label vector"
            else:
                raise ValueError("assignment IDs do not align to canonical IDs")
            unique, counts = np.unique(groups, return_counts=True)
            realized = int(len(unique))
            alignment_rows.append(
                {
                    "method": method,
                    "assignment_path": ASSIGNMENT_PATHS[method],
                    "candidate_keys": ";".join(candidates),
                    "assignment_key": key,
                    "candidate_key_resolution": resolution,
                    "n_cells": len(ids),
                    "requested_K": REQUESTED_K,
                    "realized_K": realized,
                    "k_difference": realized - REQUESTED_K,
                    "requested_compression_ratio": REQUESTED_K / len(ids),
                    "realized_compression_ratio": realized / len(ids),
                    "min_group_size": int(counts.min()),
                    "median_group_size": float(np.median(counts)),
                    "max_group_size": int(counts.max()),
                    "id_set_equality": id_set_equal,
                    "order_equality": order_equal,
                    "row_order_verified_by_label_vector": alignment.startswith("verified"),
                    "status": "PASS" if realized == REQUESTED_K else "PASS_AUTHOR_NONEXACT_K",
                    "reason": "" if realized == REQUESTED_K else "same nominal compression input; realized K retained",
                    "alignment": alignment,
                    "fingerprint": _fast_fingerprint(ASSIGNMENT_PATHS[method]),
                }
            )
            groups_by_method[method] = groups
            selected_keys[method] = key
        finally:
            obj.file.close()
    return label_key, labels, inventory, pd.DataFrame(alignment_rows), groups_by_method, selected_keys


def _group_table(groups: Sequence[str], labels: Sequence[str], target: str) -> Tuple[pd.DataFrame, int, float]:
    from scipy.stats import fisher_exact

    y = np.asarray([str(value) == target for value in labels], dtype=bool)
    n_total = len(y)
    n_target = int(y.sum())
    abundance = n_target / n_total
    frame = pd.DataFrame({"metacell_id": [str(v) for v in groups], "target": y.astype(int)})
    table = frame.groupby("metacell_id", sort=False).agg(
        metacell_size=("target", "size"), mast_count=("target", "sum")
    ).reset_index()
    table["purity"] = table.mast_count / table.metacell_size
    table["fold_enrichment"] = table.purity / abundance
    table["fisher_p"] = [
        fisher_exact(
            [[int(m), int(s - m)], [int(n_target - m), int(n_total - n_target - (s - m))]],
            alternative="greater",
        ).pvalue
        for m, s in zip(table.mast_count, table.metacell_size)
    ]
    table["fisher_q"] = _bh(table.fisher_p)
    table["is_target_containing"] = table.mast_count >= 1
    table["is_associated"] = (
        (table.mast_count >= 3) & (table.fold_enrichment >= 5) & (table.fisher_q < 0.05)
    )
    table["is_majority"] = table.purity > 0.5
    table["is_high_purity"] = table.purity >= 0.7
    return table, n_target, abundance


def _sizes(series: pd.Series, prefix: str) -> Dict[str, Any]:
    if len(series) == 0:
        return {f"{prefix}_{name}": np.nan for name in ("min", "q1", "median", "mean", "q3", "max")}
    return {
        f"{prefix}_min": float(series.min()),
        f"{prefix}_q1": float(series.quantile(0.25)),
        f"{prefix}_median": float(series.median()),
        f"{prefix}_mean": float(series.mean()),
        f"{prefix}_q3": float(series.quantile(0.75)),
        f"{prefix}_max": float(series.max()),
    }


def _summary(table: pd.DataFrame, n_target: int, abundance: float, method: str, key: str, n_cells: int, realized: int, alignment: str) -> Dict[str, Any]:
    containing = table[table.is_target_containing]
    associated = table[table.is_associated]
    majority = table[table.is_majority]
    high = table[table.is_high_purity]
    pooled = lambda frame: float(frame.mast_count.sum() / frame.metacell_size.sum()) if len(frame) else np.nan
    majority_recall = float(majority.mast_count.sum() / n_target)
    majority_precision = pooled(majority)
    majority_f1 = (
        float(2 * majority_recall * majority_precision / (majority_recall + majority_precision))
        if majority_recall + majority_precision > 0
        else 0.0
    )
    weights = containing.mast_count.to_numpy(dtype=float) / n_target
    hhi = float(np.sum(weights * weights))
    norm_hhi = (
        float((hhi - 1 / len(containing)) / (1 - 1 / len(containing)))
        if len(containing) > 1
        else 1.0
    )
    ranked = table.sort_values(
        ["fold_enrichment", "fisher_q", "mast_count", "metacell_id"],
        ascending=[False, True, False, True],
        kind="mergesort",
    )
    return {
        "dataset": "D17 Human_Kidney_Cancer",
        "method": method,
        "assignment_key": key,
        "alignment": alignment,
        "n_cells": n_cells,
        "requested_K": REQUESTED_K,
        "realized_K": realized,
        "k_difference": realized - REQUESTED_K,
        "requested_compression_ratio": REQUESTED_K / n_cells,
        "realized_compression_ratio": realized / n_cells,
        "cells_per_realized_metacell": n_cells / realized,
        "mast_count": n_target,
        "mast_abundance": abundance,
        "majority_recall": majority_recall,
        "associated_recall": float(associated.mast_count.sum() / n_target) if len(associated) else np.nan,
        "majority_precision": majority_precision,
        "majority_f1": majority_f1,
        "high_purity_recall": float(high.mast_count.sum() / n_target),
        "maximum_purity": float(table.purity.max()),
        "associated_purity_median": float(associated.purity.median()) if len(associated) else np.nan,
        "associated_purity_weighted": pooled(associated),
        "associated_purity_min": float(associated.purity.min()) if len(associated) else np.nan,
        "associated_purity_max": float(associated.purity.max()) if len(associated) else np.nan,
        "max_fold_enrichment": float(table.fold_enrichment.max()),
        "mast_containing_metacell_count": int(len(containing)),
        "associated_metacell_count": int(len(associated)),
        "majority_metacell_count": int(len(majority)),
        "high_purity_metacell_count": int(len(high)),
        "top1_capture": float(ranked.head(1).mast_count.sum() / n_target),
        "top3_capture": float(ranked.head(3).mast_count.sum() / n_target),
        "top5_capture": float(ranked.head(5).mast_count.sum() / n_target),
        "hhi": hhi,
        "normalized_hhi": norm_hhi,
        "status": "PASS",
        "k_status": "EXACT_K403" if realized == REQUESTED_K else "AUTHOR_ACCEPTED_SAME_COMPRESSION_NONEXACT_K",
    } | _sizes(containing.metacell_size, "target_containing_size") | _sizes(associated.metacell_size, "associated_size") | _sizes(majority.metacell_size, "majority_size")


def _permutations(groups: Sequence[str], n_target: int, abundance: float, repetitions: int = 10000, seed: int = 20260907) -> Tuple[np.ndarray, List[str]]:
    codes, _ = pd.factorize([str(v) for v in groups], sort=False)
    sizes = np.bincount(codes)
    k = len(sizes)
    rng = np.random.default_rng(seed)
    values = np.empty((repetitions, 7), dtype=float)
    metrics = ["maximum_purity", "maximum_fold_enrichment", "top1_capture", "top3_capture", "top5_capture", "hhi", "normalized_hhi"]
    stable = np.arange(k)
    for index in range(repetitions):
        sampled = rng.choice(len(codes), n_target, replace=False)
        counts = np.bincount(codes[sampled], minlength=k)
        purity = counts / sizes
        fold = purity / abundance
        order = np.lexsort((stable, -counts, -fold))
        positive = counts[counts > 0].astype(float) / n_target
        hhi = float(np.sum(positive * positive))
        norm = float((hhi - 1 / len(positive)) / (1 - 1 / len(positive))) if len(positive) > 1 else 1.0
        values[index] = [
            float(purity.max()), float(fold.max()),
            float(counts[order[:1]].sum() / n_target),
            float(counts[order[:3]].sum() / n_target),
            float(counts[order[:5]].sum() / n_target), hhi, norm,
        ]
    return values, metrics


def _marker_validation(groups_by_method: Mapping[str, Sequence[str]], tables: Mapping[str, pd.DataFrame]) -> pd.DataFrame:
    import anndata as ad
    from scipy import sparse
    from scipy.stats import mannwhitneyu

    obj = ad.read_h5ad(CANONICAL_RNA, backed="r")
    try:
        names = [str(v) for v in obj.var_names]
        present = [marker for marker in MARKERS if marker in names]
        missing = [marker for marker in MARKERS if marker not in names]
        if len(present) < 4:
            return pd.DataFrame([{"method": method, "status": "SKIPPED_MARKER_COUNT_LT4", "markers_present": ";".join(present), "markers_missing": ";".join(missing)} for method in METHOD_ORDER])
        indices = [names.index(marker) for marker in present]
        values = obj[:, indices].X
        if sparse.issparse(values):
            values = values.toarray()
        values = np.asarray(values, dtype=float)
        try:
            total = np.asarray(obj.X.sum(axis=1)).ravel().astype(float)
        except Exception:
            total = np.maximum(values.sum(axis=1), 1.0)
        scores = np.log1p(values / np.maximum(total[:, None], 1.0) * 10000.0).mean(axis=1)
        rows: List[Dict[str, Any]] = []
        for method in METHOD_ORDER:
            group_scores = pd.DataFrame({"metacell_id": groups_by_method[method], "score": scores}).groupby("metacell_id", sort=False).score.mean()
            associated_ids = set(tables[method].loc[tables[method].is_associated, "metacell_id"].astype(str))
            a = group_scores[group_scores.index.isin(associated_ids)].to_numpy()
            b = group_scores[~group_scores.index.isin(associated_ids)].to_numpy()
            if len(a) and len(b):
                p_value = float(mannwhitneyu(a, b, alternative="two-sided").pvalue)
                effect = float(np.median(a) - np.median(b))
                status = "PASS"
            else:
                p_value, effect, status = np.nan, np.nan, "INSUFFICIENT_ASSOCIATED_GROUPS"
            rows.append({"method": method, "status": status, "markers_present": ";".join(present), "markers_missing": ";".join(missing), "associated_group_count": len(a), "nonassociated_group_count": len(b), "associated_score_median": float(np.median(a)) if len(a) else np.nan, "nonassociated_score_median": float(np.median(b)) if len(b) else np.nan, "median_score_effect_associated_minus_other": effect, "wilcoxon_or_mannwhitney_p": p_value})
        result = pd.DataFrame(rows)
        result["bh_q"] = _bh(result.wilcoxon_or_mannwhitney_p)
        result["coherence_result"] = np.where(
            (result.bh_q < 0.05) & (result.median_score_effect_associated_minus_other > 0),
            "Mast-associated metacells show coherent Mast-cell marker expression",
            "Mast-associated metacells do not show BH-significant higher marker score",
        )
        return result
    finally:
        obj.file.close()


def _three_populations(groups_by_method: Mapping[str, Sequence[str]], labels: Sequence[str]) -> pd.DataFrame:
    rows: List[Dict[str, Any]] = []
    present = set(labels)
    for method in METHOD_ORDER:
        for target in ("Mast Cells", "T Cells", "Myeloid Cells"):
            if target not in present:
                rows.append({"method": method, "population": target, "status": "BLOCKED_LABEL_ABSENT"})
                continue
            table, count, _ = _group_table(groups_by_method[method], labels, target)
            majority = table[table.is_majority]
            rows.append({"method": method, "population": target, "status": "PASS", "target_count": count, "abundance": count / len(labels), "majority_recall": float(majority.mast_count.sum() / count), "majority_metacell_count": len(majority), "maximum_purity": float(table.purity.max()), "median_majority_metacell_size": float(majority.metacell_size.median()) if len(majority) else np.nan})
    return pd.DataFrame(rows)


def _figures(out: Path, summary: pd.DataFrame, tables: Mapping[str, pd.DataFrame], permutations: pd.DataFrame) -> None:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    colors = {"GARQ": "#0072B2", "MetaQ": "#D55E00", "SEACells": "#009E73", "MetaCell V2": "#CC79A7", "SuperCell": "#E69F00"}
    positions = np.arange(len(METHOD_ORDER))
    indexed = summary.set_index("method").reindex(METHOD_ORDER)
    fig, axes = plt.subplots(2, 2, figsize=(11, 8))
    width = 0.36
    axes[0, 0].bar(positions - width / 2, indexed.associated_recall.fillna(0), width, label="Associated recall")
    axes[0, 0].bar(positions + width / 2, indexed.majority_recall, width, label="Majority recall")
    axes[0, 0].set_ylim(0, 1)
    axes[0, 0].set_ylabel("Mast-cell recall")
    axes[0, 0].legend(fontsize=8)
    axes[0, 1].bar(positions, indexed.maximum_purity, color=[colors[m] for m in METHOD_ORDER])
    axes[0, 1].axhline(0.5, ls="--", color="gray")
    axes[0, 1].axhline(0.7, ls=":", color="gray")
    axes[0, 1].set_ylim(0, 1)
    axes[0, 1].set_ylabel("Maximum purity")
    axes[1, 0].bar(positions, indexed.associated_metacell_count, color=[colors[m] for m in METHOD_ORDER])
    for x, value, majority_count in zip(positions, indexed.associated_metacell_count, indexed.majority_metacell_count):
        axes[1, 0].text(x, float(value) + 0.1, f"majority={int(majority_count)}", ha="center", fontsize=7)
    axes[1, 0].set_ylabel("Associated metacell count")
    for index, method in enumerate(METHOD_ORDER):
        associated = tables[method][tables[method].is_associated]
        if len(associated):
            x = np.full(len(associated), index) + np.linspace(-0.12, 0.12, len(associated))
            axes[1, 1].scatter(x, associated.metacell_size, color=colors[method], s=18, alpha=0.75)
            axes[1, 1].plot([index - 0.12, index + 0.12], [associated.metacell_size.median()] * 2, color="black", lw=2)
    axes[1, 1].set_ylabel("Associated metacell size")
    for axis in axes.flat:
        axis.set_xticks(positions, METHOD_ORDER, rotation=22, ha="right")
        axis.grid(axis="y", alpha=0.2)
    fig.suptitle("Figure 4b Mast-cell quantitative panel; frozen assignments")
    fig.tight_layout()
    for extension in ("pdf", "svg"):
        fig.savefig(out / f"Fig4b_mast_quantitative_panel.{extension}", bbox_inches="tight")
    fig.savefig(out / "Fig4b_mast_quantitative_panel.png", dpi=300, bbox_inches="tight")
    plt.close(fig)

    fig, axes = plt.subplots(2, 2, figsize=(11, 8))
    for method in METHOD_ORDER:
        row = indexed.loc[method]
        axes[0, 0].scatter(method, row.top1_capture, color=colors[method])
        axes[0, 1].scatter(method, row.top3_capture, color=colors[method])
        axes[1, 0].scatter(method, row.top5_capture, color=colors[method])
        axes[1, 1].scatter(method, row.max_fold_enrichment, color=colors[method])
    axes[0, 0].set_title("Top-1 capture")
    axes[0, 1].set_title("Top-3 capture")
    axes[1, 0].set_title("Top-5 capture")
    axes[1, 1].set_title("Maximum fold enrichment")
    for axis in axes.flat[:3]:
        axis.set_ylim(0, 1)
    for axis in axes.flat:
        axis.tick_params(axis="x", rotation=22)
        axis.grid(axis="y", alpha=0.2)
    fig.suptitle("Figure 4b Mast-cell localized enrichment")
    fig.tight_layout()
    for extension in ("pdf", "svg"):
        fig.savefig(out / f"FigS_mast_localized_enrichment.{extension}", bbox_inches="tight")
    fig.savefig(out / "FigS_mast_localized_enrichment.png", dpi=300, bbox_inches="tight")
    plt.close(fig)
    (out / "Fig4b_layout_mockup.txt").write_text(
        "Replace the original Figure 4b Mast-cell binary cell with Fig4b_mast_quantitative_panel; retain the original UMAP as qualitative context.\n",
        encoding="utf-8",
    )


def _write_response_and_report(
    out: Path,
    inventory: pd.DataFrame,
    alignment: pd.DataFrame,
    summary: pd.DataFrame,
    marker: pd.DataFrame,
    populations: pd.DataFrame,
    permutations: pd.DataFrame,
) -> None:
    garq = summary.loc[summary.method == "GARQ"].iloc[0]
    garq_p = permutations[permutations.method == "GARQ"]
    p_top3 = float(garq_p.loc[garq_p.metric == "top3_capture", "empirical_p"].iloc[0])
    p_hhi = float(garq_p.loc[garq_p.metric == "normalized_hhi", "empirical_p"].iloc[0])
    criterion = bool(garq.associated_metacell_count >= 1 and garq.associated_recall >= 0.2 and garq.max_fold_enrichment >= 5 and p_top3 < 0.05 and p_hhi < 0.05)
    method_ok: Dict[str, bool] = {}
    for row in summary.itertuples():
        method_p = permutations[permutations.method == row.method]
        method_ok[row.method] = bool(row.associated_metacell_count >= 1 and row.associated_recall >= 0.2 and row.max_fold_enrichment >= 5 and float(method_p.loc[method_p.metric == "top3_capture", "empirical_p"].iloc[0]) < 0.05 and float(method_p.loc[method_p.metric == "normalized_hhi", "empirical_p"].iloc[0]) < 0.05)
    only_garq = criterion and all(not value for method, value in method_ok.items() if method != "GARQ")
    if criterion and only_garq:
        outcome = "A"
        wording = "Mast-cell-associated information remained locally identifiable after GARQ aggregation, and the preregistered retention criterion was not met by the other methods."
    elif criterion:
        outcome = "B"
        wording = "Mast-cell-associated metacells remained identifiable in the GARQ space; localized enrichment and strict majority recovery varied across methods."
    else:
        outcome = "C"
        wording = "The frozen assignment did not meet the preregistered GARQ localized-retention criterion; the binary statement is replaced by quantitative results."
    report = f"""# D17 Figure 4b Mast-cell quantitative review

Status: COMPLETE_WITH_AUTHOR_NONEXACT_K_OVERRIDE

This frozen-assignment analysis did not retrain or modify any method. The
original nominal target is K=403. The author explicitly authorized continuation
with the same nominal compression input when a frozen method realizes a
different K; the realized K is retained and shown in every result.

## Executive summary

Canonical metadata is D17 Human_Kidney_Cancer with label key celltype and
16,143 cells. The exact Mast Cells count is {int(garq.mast_count)}
({float(garq.mast_abundance):.4%}).

GARQ majority recall={float(garq.majority_recall):.4f}; associated
recall={float(garq.associated_recall):.4f}; maximum purity={float(garq.maximum_purity):.4f};
associated metacell count={int(garq.associated_metacell_count)}; associated size
median/range={garq.associated_size_median:.2f}/{garq.associated_size_min:.2f}--{garq.associated_size_max:.2f};
top-3 capture={float(garq.top3_capture):.4f}; permutation P={p_top3:.4g};
normalized-HHI permutation P={p_hhi:.4g}.

Marker coherence: {marker.loc[marker.method == "GARQ", "coherence_result"].iloc[0] if "coherence_result" in marker else "not available"}.
Only GARQ supported: {"YES" if only_garq else "NO"}. Recommended outcome:
{outcome}. {wording}

## Assignment keys and alignment

{_md_table(alignment[["method", "candidate_keys", "assignment_key", "realized_K", "requested_compression_ratio", "realized_compression_ratio", "id_set_equality", "row_order_verified_by_label_vector", "status", "reason"]])}

MetaCell V2 contained metacell and membership. They were partition-equivalent,
so the author-authorized key is metacell. SuperCell used its sole metacell key.
Numeric row-order IDs were accepted only when the canonical label vector
verified provenance.

## Requested and realized K

Requested ratio is 403/16143={REQUESTED_K / EXPECTED_N:.8f}. Realized K is not
corrected:

{_md_table(summary[["method", "requested_K", "realized_K", "k_difference", "requested_compression_ratio", "realized_compression_ratio", "cells_per_realized_metacell"]])}

## Recall, purity, number, and size

{_md_table(summary[["method", "majority_recall", "associated_recall", "majority_precision", "majority_f1", "high_purity_recall", "maximum_purity", "associated_purity_median", "associated_purity_weighted", "associated_metacell_count", "majority_metacell_count", "high_purity_metacell_count", "associated_size_min", "associated_size_median", "associated_size_max"]])}

Associated means at least three Mast Cells, at least five-fold enrichment, and
within-method BH q<0.05 from one-sided Fisher exact tests. Majority is purity
greater than 0.5; high purity is at least 0.7. NA denotes no associated group.

## Enrichment and permutation

{_md_table(permutations[permutations.metric.isin(["top3_capture", "normalized_hhi"])] [["method", "metric", "observed", "null_mean", "null_q95", "empirical_p"]])}

All seven permutation statistics for all five methods are in
fig4b_mast_permutation_summary.csv. Each method used 10,000 fixed-assignment
label permutations with random seed 20260907 and P=(1+count(null>=observed))/10001.

## RNA marker coherence

{_md_table(marker)}

## Three-population secondary check

{_md_table(populations)}

## Cross-method interpretation

The five methods share the nominal compression input but do not share an
identical realized K. Exact Figure 4b and the separate Phase-2 K=323
three-seed post-hoc analysis remain separate; see
FIG4B_K403_VS_PHASE2_K323_CONSISTENCY.md. Enrichment is not strict majority
recovery. D17 labels are study-derived, not an independent ground truth.

Recommended wording:

{wording}

## File index

input_inventory.csv; id_alignment_checks.csv; resolved_config.yaml;
fig4b_mast_metacell_level.csv; fig4b_mast_method_summary.csv;
fig4b_mast_permutation_summary.csv; fig4b_mast_top_metacells.csv;
fig4b_mast_marker_validation.csv; fig4b_three_population_summary.csv;
Fig4b_mast_quantitative_panel.pdf/svg/png; FigS_mast_localized_enrichment.pdf/svg/png;
Supplementary_Table_Fig4b_Mast.csv; Supplementary_Table_Fig4b_Mast.tex.

## Limitations

This is a post-hoc frozen-assignment analysis. The non-exact realized K values
for MetaCell V2 and SuperCell are an author-authorized limitation. The analysis
does not establish causal regulation, trajectory superiority, or independent
ground truth.
"""
    (out / "D17_FIG4B_MAST_EXACT_REPORT.md").write_text(report, encoding="utf-8")
    response = f"""% D17 Figure 4b Mast-cell response-ready material
\\section*{{Response to Reviewer 2 Minor Comment 4}}

We thank the reviewer for requesting quantitative support for the Mast-cell
retention statement. We re-evaluated the five frozen Figure 4b assignments
without retraining or changing any assignment. The canonical D17 metadata
contains 74 Mast Cells among 16,143 cells (0.46\\%). Strict majority recall
(purity >0.5) is reported separately from associated recall (at least three
Mast Cells, at least five-fold enrichment, and BH-adjusted one-sided Fisher
q<0.05), together with purity, metacell number, size, top-k capture, and
fixed-assignment permutation tests.

The author confirmed that MetaCell V2 and SuperCell used the same nominal
compression input. We therefore report their realized K values rather than
silently forcing K=403. This is a same-compression comparison, not an
exact-realized-K=403 comparison.

\\subsection*{{Changes in the revised manuscript}}

We replace the binary Mast-cell checkmark/cross with the quantitative panel
Fig4b_mast_quantitative_panel and Supplementary Table
Supplementary_Table_Fig4b_Mast. The revised text distinguishes visual
localization, strict majority recovery, and localized enrichment, and calls
the D17 annotation study-derived.

\\subsection*{{Revised Results paragraph}}

Mast Cells comprised 74 of 16,143 cells (0.46\\%). GARQ majority recall was
{float(garq.majority_recall):.3f}, associated recall was {float(garq.associated_recall):.3f},
maximum purity was {float(garq.maximum_purity):.3f}, and the number of associated
metacells was {int(garq.associated_metacell_count)}. Top-three capture was
{float(garq.top3_capture):.3f} with permutation P={p_top3:.4g}; normalized-HHI
permutation P={p_hhi:.4g}. {wording}

\\subsection*{{Revised Figure 4b caption}}

Quantitative evaluation of Mast-cell organization in five frozen Figure 4b
assignments. Panels show associated and strict-majority recall, maximum purity
with 0.5 and 0.7 reference lines, associated metacell count with majority count,
and associated-metacell sizes. The nominal requested K was 403; realized K is
reported for each method because the author authorized the same-compression
comparison without post-hoc K correction.

\\subsection*{{Supplementary Methods}}

For metacell M_k, purity was p_k=m_k/|M_k|. Associated metacells required
m_k>=3, at least five-fold enrichment over global abundance, and BH-adjusted
one-sided Fisher q<0.05. Majority was p_k>0.5 and high purity p_k>=0.7.
Assignments and sizes were preserved for 10,000 label permutations with seed
20260907. No marker was used to select a threshold or assignment.

\\subsection*{{Supplementary Table LaTeX}}

The compact table is in Supplementary_Table_Fig4b_Mast.tex and the complete
metacell-level table is in fig4b_mast_metacell_level.csv.
"""
    (out / "D17_FIG4B_MAST_RESPONSE_READY.tex").write_text(response, encoding="utf-8")


def run_formal(output_dir: Path, figure_dir: Path, n_permutations: int = 10000) -> int:
    output_dir.mkdir(parents=True, exist_ok=True)
    label_key, labels, inventory, alignment, groups_by_method, selected_keys = _audit_and_load()
    tables: Dict[str, pd.DataFrame] = {}
    summaries: List[Dict[str, Any]] = []
    all_meta: List[pd.DataFrame] = []
    all_top: List[pd.DataFrame] = []
    permutation_rows: List[Dict[str, Any]] = []
    for method in METHOD_ORDER:
        row = alignment.loc[alignment.method == method].iloc[0]
        table, target_count, abundance = _group_table(groups_by_method[method], labels, "Mast Cells")
        tables[method] = table
        summary = _summary(table, target_count, abundance, method, selected_keys[method], len(labels), int(row.realized_K), row.alignment)
        null, metrics = _permutations(groups_by_method[method], target_count, abundance, n_permutations)
        observed = [summary["maximum_purity"], summary["max_fold_enrichment"], summary["top1_capture"], summary["top3_capture"], summary["top5_capture"], summary["hhi"], summary["normalized_hhi"]]
        for index, metric in enumerate(metrics):
            permutation_rows.append({"method": method, "assignment": "figure4b_original_assignment", "metric": metric, "observed": observed[index], "null_mean": float(null[:, index].mean()), "null_sd": float(null[:, index].std(ddof=1)), "null_q95": float(np.quantile(null[:, index], 0.95)), "empirical_p": float((1 + np.sum(null[:, index] >= observed[index] - 1e-15)) / (n_permutations + 1)), "n_permutations": n_permutations, "random_seed": 20260907})
        summaries.append(summary)
        meta = table.copy()
        meta.insert(0, "method", method)
        meta.insert(1, "assignment_key", selected_keys[method])
        meta.insert(2, "requested_K", REQUESTED_K)
        meta.insert(3, "realized_K", int(row.realized_K))
        all_meta.append(meta)
        top = table.sort_values(["fold_enrichment", "fisher_q", "mast_count", "metacell_id"], ascending=[False, True, False, True], kind="mergesort").head(5).copy()
        top.insert(0, "method", method)
        top.insert(1, "assignment_key", selected_keys[method])
        top.insert(2, "requested_K", REQUESTED_K)
        top.insert(3, "realized_K", int(row.realized_K))
        all_top.append(top)
    summary_frame = pd.DataFrame(summaries)
    meta_frame = pd.concat(all_meta, ignore_index=True)
    top_frame = pd.concat(all_top, ignore_index=True)
    permutation_frame = pd.DataFrame(permutation_rows)
    marker_frame = _marker_validation(groups_by_method, tables)
    population_frame = _three_populations(groups_by_method, labels)
    for method, key in selected_keys.items():
        inventory.loc[inventory.label == f"assignment {method}", "selected_assignment_key"] = key
    inventory.to_csv(output_dir / "input_inventory.csv", index=False)
    alignment.to_csv(output_dir / "id_alignment_checks.csv", index=False)
    summary_frame.to_csv(output_dir / "fig4b_mast_method_summary.csv", index=False)
    meta_frame.to_csv(output_dir / "fig4b_mast_metacell_level.csv", index=False)
    permutation_frame.to_csv(output_dir / "fig4b_mast_permutation_summary.csv", index=False)
    top_frame.to_csv(output_dir / "fig4b_mast_top_metacells.csv", index=False)
    marker_frame.to_csv(output_dir / "fig4b_mast_marker_validation.csv", index=False)
    population_frame.to_csv(output_dir / "fig4b_three_population_summary.csv", index=False)
    summary_frame[["method", "assignment_key", "requested_K", "realized_K", "mast_count", "majority_recall", "associated_recall", "maximum_purity", "associated_metacell_count", "majority_metacell_count", "associated_size_median", "associated_size_min", "associated_size_max", "top3_capture", "normalized_hhi"]].to_csv(output_dir / "Supplementary_Table_Fig4b_Mast.csv", index=False)
    latex = ["\\begin{table}[ht]", "\\centering", "\\caption{Frozen-assignment Mast-cell summary.}", "\\begin{tabular}{lrrrrrrrr}", "\\toprule", "Method & K & Mast & Majority recall & Associated recall & Max purity & Associated n & Majority n & Median size \\\\", "\\midrule"]
    for row in summary_frame.itertuples(index=False):
        fmt = lambda value: "NA" if pd.isna(value) else f"{float(value):.3f}"
        latex.append(f"{row.method} & {row.realized_K} & {row.mast_count} & {fmt(row.majority_recall)} & {fmt(row.associated_recall)} & {fmt(row.maximum_purity)} & {row.associated_metacell_count} & {row.majority_metacell_count} & {fmt(row.associated_size_median)} \\\\")
    latex.extend(["\\bottomrule", "\\end{tabular}", "\\end{table}"])
    (output_dir / "Supplementary_Table_Fig4b_Mast.tex").write_text("\n".join(latex) + "\n", encoding="utf-8")
    _figures(output_dir, summary_frame, tables, permutation_frame)
    consistency = output_dir / "FIG4B_K403_VS_PHASE2_K323_CONSISTENCY.md"
    phase2 = Path("revision_results/phase2/06_kidney/mast_posthoc/mast_run_level_summary.csv")
    consistency_text = [
        "# Figure 4b K=403 versus Phase-2 K=323 consistency",
        "",
        "The exact original Figure 4b frozen assignments and the Phase-2 K=323 three-seed post-hoc analysis are reported separately and are not averaged.",
        "",
        "Original Figure 4b: nominal requested K=403; author-authorized same-compression realized K values are "
        + ", ".join(f"{row.method}={int(row.realized_K)}" for row in summary_frame.itertuples()) + ".",
        "",
    ]
    if phase2.exists():
        phase2_frame = pd.read_csv(phase2)
        consistency_text.extend(["Phase-2 K=323 method means:", "", _md_table(phase2_frame.groupby("method", as_index=False).agg(seeds=("seed", "nunique"), mean_associated_recall=("associated_recall", "mean"), mean_strict_recall=("strict_recall", "mean"), mean_max_purity=("max_purity", "mean"))), ""])
    consistency_text.append("Differences may reflect aggregation resolution, the specific frozen assignment, and method/output provenance.")
    consistency.write_text("\n".join(consistency_text) + "\n", encoding="utf-8")
    _write_response_and_report(output_dir, inventory, alignment, summary_frame, marker_frame, population_frame, permutation_frame)
    (output_dir / "resolved_config.yaml").write_text(
        "dataset: D17 Human_Kidney_Cancer\n"
        f"canonical_label_key: {label_key}\n"
        f"requested_K: {REQUESTED_K}\n"
        f"n_cells: {len(labels)}\n"
        f"mast_count: {labels.count('Mast Cells')}\n"
        f"n_permutations: {n_permutations}\n"
        "random_seed: 20260907\n"
        "allow_nonexact_realized_K: true\n"
        "author_override: same nominal compression input; report realized K\n"
        f"selected_assignment_keys: {json.dumps(selected_keys, ensure_ascii=False)}\n",
        encoding="utf-8",
    )
    (output_dir / "INPUT_AUDIT.md").write_text(
        "All five frozen assignments were audited from resolved_config.yaml. "
        "See input_inventory.csv and id_alignment_checks.csv for fingerprints, "
        "candidate keys, realized K, and provenance.\n",
        encoding="utf-8",
    )
    (output_dir / "DRY_RUN.md").write_text(
        "Status: PASS_AUTHOR_OVERRIDE\n\n"
        "Formal frozen-assignment quantification completed after the author "
        "explicitly authorized same-compression realized K values rather than "
        "requiring every method to realize K=403.\n",
        encoding="utf-8",
    )
    hashes = []
    for path in sorted(output_dir.iterdir()):
        if path.is_file() and path.name != "output_file_hashes.csv":
            hashes.append({"file": path.name, "sha256": _sha256(path), "bytes": path.stat().st_size})
    pd.DataFrame(hashes).to_csv(output_dir / "output_file_hashes.csv", index=False)
    print(json.dumps({"status": "PASS_AUTHOR_OVERRIDE", "methods": METHOD_ORDER, "realized_K": {row.method: int(row.realized_K) for row in summary_frame.itertuples()}, "output_dir": str(output_dir)}, indent=2))
    return 0
