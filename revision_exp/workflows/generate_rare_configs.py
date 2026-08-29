"""Generate reachable E1 rare-abundance broad-screen smoke configs.

The eligible labels and counts below are an auditable snapshot of the recovered
D5/D11 ``celltype`` columns.  The preregistered rule is source abundance <= 5%
and source support >= 50; a target is emitted only when it lowers abundance.
"""

import hashlib
from pathlib import Path
import re

import yaml


def main() -> None:
    output = Path("revision_exp/configs/rare_subsampling")
    output.mkdir(parents=True, exist_ok=True)
    registry_path = Path("revision_exp/data_registry/datasets.yaml")
    registry = yaml.safe_load(registry_path.read_text(encoding="utf-8"))["datasets"]
    datasets = {
        "D5": {
            "data_types": ["RNA", "ADT"],
            "source_n_cells": 8670,
            "eligible_counts": {
                "Non classical monocytes": 410,
                "gdT cells": 400,
                "MAIT-NKT cells": 389,
                "CD8 naive": 352,
                "CD8 memory": 349,
                "Neutrophils": 249,
                "T-NK-B cell doublets": 191,
                "Memory B": 182,
                "CD4 naive II": 160,
                "NK-T doublets": 157,
                "CD56bright CD16dim NK": 148,
                "Platelet-bound monocytes": 138,
                "NK-monocyte doublets": 115,
                "Regulatory T cells": 71,
                "conventional DC": 67,
                "CD4 and CD8 activated memory": 56,
                "plasmacytoid DC": 52,
            },
        },
        "D11": {
            "data_types": ["RNA", "ATAC"],
            "source_n_cells": 9876,
            "eligible_counts": {
                "CD14+ Mono": 458,
                "NK": 421,
                "Lymph prog": 327,
                "B1 B": 326,
                "CD4+ T naive": 299,
                "Erythroblast": 266,
                "cDC2": 160,
                "MK/E prog": 120,
                "HSC": 108,
                "CD16+ Mono": 99,
                "Normoblast": 90,
                "G/M prog": 66,
            },
            # Preregistered paper example retained despite support < 50.
            "required_example_counts": {"Plasma cell": 26},
        },
    }
    # Preserve the eight already executed configuration hashes exactly.
    existing_seeds = {
        ("D5", "Regulatory T cells", 0.005): 9101,
        ("D5", "Regulatory T cells", 0.002): 9102,
        ("D5", "conventional DC", 0.005): 9103,
        ("D5", "conventional DC", 0.002): 9104,
        ("D11", "Plasma cell", 0.002): 9105,
        ("D11", "cDC2", 0.01): 9106,
        ("D11", "cDC2", 0.005): 9107,
        ("D11", "cDC2", 0.002): 9108,
    }
    planned_abundances = (0.01, 0.005, 0.002)
    common = {
        "task": "legacy_garq",
        "implementation_tag": "diagnostic_variant_rare_subsampling",
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
        dataset_registry = registry[dataset]
        if int(dataset_registry["n_cells"]) != specification["source_n_cells"]:
            raise ValueError(f"Registry cell count changed for {dataset}")
        data_files = [dataset_registry["modalities"][m] for m in specification["data_types"]]
        counts = {
            **specification["eligible_counts"],
            **specification.get("required_example_counts", {}),
        }
        for target_label, source_count in counts.items():
            source_abundance = source_count / specification["source_n_cells"]
            abundances = tuple(a for a in planned_abundances if a < source_abundance)
            slug = re.sub(r"[^A-Za-z0-9+.-]+", "-", target_label).strip("-")
            for abundance in abundances:
                abundance_tag = f"{abundance:g}"
                condition_seed = existing_seeds.get((dataset, target_label, abundance))
                if condition_seed is None:
                    identity = f"{dataset}\0{target_label}\0{abundance_tag}".encode()
                    condition_seed = 10000 + int(hashlib.sha256(identity).hexdigest()[:8], 16) % 1000000
                config = {
                    "config_id": f"E1_{dataset}_rare_{slug}_abundance_{abundance_tag}_broad_seed0_v1",
                    "dataset": dataset,
                    "data_files": data_files,
                    "data_types": specification["data_types"],
                    **common,
                    "rare_subsampling": {
                        "label_key": "celltype",
                        "target_label": target_label,
                        "target_abundance": abundance,
                        "seed": condition_seed,
                    },
                    "output_subdir": (
                        f"01_size_resolution/rare_subsampling/{dataset}/{slug}/"
                        f"abundance_{abundance_tag}_broad_seed0"
                    ),
                }
                path = output / f"e1_{dataset}_rare_{slug}_abundance_{abundance_tag}.yaml"
                path.write_text(yaml.safe_dump(config, sort_keys=False), encoding="utf-8")


if __name__ == "__main__":
    main()
