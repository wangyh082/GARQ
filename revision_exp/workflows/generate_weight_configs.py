"""Generate preregistered E2 explicit modality-weight smoke configs."""

from __future__ import annotations

from pathlib import Path

import yaml


def main() -> None:
    output = Path("revision_exp/configs/weights")
    output.mkdir(parents=True, exist_ok=True)
    datasets = {
        "D5": {
            "data_files": [
                "/home/zhangpeiru/data/RNA+ADT/D5/D5_rna.h5ad",
                "/home/zhangpeiru/data/RNA+ADT/D5/D5_adt.h5ad",
            ],
            "data_types": ["RNA", "ADT"],
        },
        "D11": {
            "data_files": [
                "/home/zhangpeiru/data/11_GSE194122/11_GSE194122_rna.h5ad",
                "/home/zhangpeiru/data/11_GSE194122/11_GSE194122_atac.h5ad",
            ],
            "data_types": ["RNA", "ATAC"],
        },
        "D17": {
            "data_files": [
                "/home/zhangpeiru/data/analysis/new/kidney_rna_updated.h5ad",
                "/home/zhangpeiru/data/analysis/new/kidney_atac_updated.h5ad",
            ],
            "data_types": ["RNA", "ATAC"],
        },
        "D18": {
            "data_files": [
                "/home/zhangpeiru/data/RNA_ATAC_ADT/GSE158013/GSE158013_rna.h5ad",
                "/home/zhangpeiru/data/RNA_ATAC_ADT/GSE158013/GSE158013_atac.h5ad",
                "/home/zhangpeiru/data/RNA_ATAC_ADT/GSE158013/GSE158013_adt.h5ad",
            ],
            "data_types": ["RNA", "ATAC", "ADT"],
            "obs_name_canonicalization": [
                None,
                None,
                {"pattern": r"\.([0-9]+)$", "replacement": r"-\1"},
            ],
        },
    }
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
    for dataset, specification in datasets.items():
        modalities = specification["data_types"]
        conditions = [("equal_weights", None, "none", 1.0)]
        for index, modality in enumerate(modalities):
            for weight in (0.0, 0.25, 0.5, 2.0):
                weights = [1.0] * len(modalities)
                weights[index] = weight
                conditions.append(
                    (f"{modality}_lambda_{weight:g}", weights, modality, weight)
                )
        for condition, weights, weighted_modality, weight in conditions:
            config = {
                "config_id": f"E2_{dataset}_weight_{condition}_smoke_seed0_v1",
                "task": "legacy_garq",
                "implementation_tag": "diagnostic_variant_modality_weight",
                "dataset": dataset,
                **specification,
                **runtime,
                "modality_weights": weights,
                "weighted_modality": weighted_modality,
                "weight_lambda": weight,
                "output_subdir": f"02_modality/weights/{dataset}/{condition}",
            }
            (output / f"e2_{dataset}_weight_{condition}.yaml").write_text(
                yaml.safe_dump(config, sort_keys=False), encoding="utf-8"
            )


if __name__ == "__main__":
    main()
