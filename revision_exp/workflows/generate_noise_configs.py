"""Generate preregistered E2 count-level noise configs."""

from __future__ import annotations

from pathlib import Path

import yaml


def main() -> None:
    output = Path("revision_exp/configs/noise")
    output.mkdir(parents=True, exist_ok=True)
    runtime = {
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
    datasets = {
        "D5": {
            "data_files": [
                "/home/zhangpeiru/data/RNA+ADT/D5/D5_rna.h5ad",
                "/home/zhangpeiru/data/RNA+ADT/D5/D5_adt.h5ad",
            ],
            "data_types": ["RNA", "ADT"],
            "matrix_sources": ["X", "X"],
        },
        "D11": {
            "data_files": [
                "/home/zhangpeiru/data/11_GSE194122/11_GSE194122_rna.h5ad",
                "/home/zhangpeiru/data/11_GSE194122/11_GSE194122_atac.h5ad",
            ],
            # D11 RNA .X is log-normalized; thinning must use raw integer counts.
            "data_types": ["RNA", "ATAC"],
            "matrix_sources": ["counts", "X"],
        },
        "D17": {
            "data_files": [
                "/home/zhangpeiru/data/analysis/new/kidney_rna_updated.h5ad",
                "/home/zhangpeiru/data/analysis/new/kidney_atac_updated.h5ad",
            ],
            "data_types": ["RNA", "ATAC"],
            "matrix_sources": ["X", "X"],
        },
        "D18": {
            "data_files": [
                "/home/zhangpeiru/data/RNA_ATAC_ADT/GSE158013/GSE158013_rna.h5ad",
                "/home/zhangpeiru/data/RNA_ATAC_ADT/GSE158013/GSE158013_atac.h5ad",
                "/home/zhangpeiru/data/RNA_ATAC_ADT/GSE158013/GSE158013_adt.h5ad",
            ],
            "data_types": ["RNA", "ATAC", "ADT"],
            "matrix_sources": ["X", "X", "X"],
            "obs_name_canonicalization": [
                None,
                None,
                {"pattern": r"\.([0-9]+)$", "replacement": r"-\1"},
            ],
        },
    }
    for dataset, specification in datasets.items():
        n_modalities = len(specification["data_types"])
        conditions = [("baseline_counts_p1", [None] * n_modalities)]
        for modality_index, modality in enumerate(specification["data_types"]):
            for probability_index, probability in enumerate((0.75, 0.5, 0.25)):
                perturbations = [None] * n_modalities
                perturbations[modality_index] = {
                    "kind": "binomial_thinning",
                    "p": probability,
                    "seed": 8100 + 100 * modality_index + probability_index,
                }
                conditions.append(
                    (f"{modality}_thin_{probability:g}", perturbations)
                )
            perturbations = [None] * n_modalities
            perturbations[modality_index] = {
                "kind": "cell_permutation",
                "seed": 8199 + 100 * modality_index,
            }
            conditions.append((f"{modality}_cell_permutation", perturbations))
        for condition, perturbations in conditions:
            config = {
                "config_id": f"E2_{dataset}_noise_{condition}_smoke_seed0_v1",
                "task": "legacy_garq",
                "implementation_tag": "diagnostic_variant_modality_noise",
                "dataset": dataset,
                **specification,
                **runtime,
                "modality_perturbations": perturbations,
                "noise_condition": condition,
                "output_subdir": f"02_modality/noise/{dataset}/{condition}",
            }
            (output / f"e2_{dataset}_noise_{condition}.yaml").write_text(
                yaml.safe_dump(config, sort_keys=False), encoding="utf-8"
            )


if __name__ == "__main__":
    main()
