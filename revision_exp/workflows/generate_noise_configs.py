"""Generate preregistered E2 count-level noise configs."""

from __future__ import annotations

from pathlib import Path

import yaml


def main() -> None:
    output = Path("revision_exp/configs/noise")
    output.mkdir(parents=True, exist_ok=True)
    base = {
        "task": "legacy_garq",
        "implementation_tag": "diagnostic_variant_modality_noise",
        "dataset": "D5",
        "data_files": [
            "/home/zhangpeiru/data/RNA+ADT/D5/D5_rna.h5ad",
            "/home/zhangpeiru/data/RNA+ADT/D5/D5_adt.h5ad",
        ],
        "data_types": ["RNA", "ADT"],
        "matrix_sources": ["X", "X"],
        "label_key": "celltype",
        "cell_limit": 2000,
        "subset_seed": 1729,
        "requested_K": 40,
        "epochs": 6,
        "batch_size": 256,
        "k_knn": 5,
        "seed": 0,
        "device": "cuda",
        "deterministic": True,
        "anchors_init": "Kmeans",
        "converge_threshold": 10,
        "min_available_ram_gb": 32,
        "min_free_gpu_gb": 8,
        "result_root": "revision_results",
        "force": False,
    }
    conditions = [("baseline_counts_p1", [None, None])]
    for modality_index, modality in enumerate(base["data_types"]):
        for probability_index, probability in enumerate((0.75, 0.5, 0.25)):
            perturbations = [None, None]
            perturbations[modality_index] = {
                "kind": "binomial_thinning",
                "p": probability,
                "seed": 8100 + 100 * modality_index + probability_index,
            }
            conditions.append((f"{modality}_thin_{probability:g}", perturbations))
        perturbations = [None, None]
        perturbations[modality_index] = {
            "kind": "cell_permutation",
            "seed": 8199 + 100 * modality_index,
        }
        conditions.append((f"{modality}_cell_permutation", perturbations))
    for condition, perturbations in conditions:
        config = {
            "config_id": f"E2_D5_noise_{condition}_smoke_seed0_v1",
            **base,
            "modality_perturbations": perturbations,
            "noise_condition": condition,
            "output_subdir": f"02_modality/noise/D5/{condition}",
        }
        (output / f"e2_D5_noise_{condition}.yaml").write_text(
            yaml.safe_dump(config, sort_keys=False), encoding="utf-8"
        )


if __name__ == "__main__":
    main()
