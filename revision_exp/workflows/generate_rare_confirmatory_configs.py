"""Generate the recovered-dataset E1 confirmatory-design smoke grid."""

import hashlib
from pathlib import Path
import re

import yaml


def main() -> None:
    output = Path("revision_exp/configs/rare_confirmatory")
    output.mkdir(parents=True, exist_ok=True)
    registry = yaml.safe_load(
        Path("revision_exp/data_registry/datasets.yaml").read_text(encoding="utf-8")
    )["datasets"]
    # Counts are an auditable snapshot of the registered RNA label columns. The
    # first two entries per dataset are selected without outcome metrics as the
    # two most abundant types satisfying source abundance <=5% and support >=50.
    # Additional entries are preregistered examples or reviewer-relevant types.
    datasets = {
        "D5": {
            "data_types": ["RNA", "ADT"],
            "counts": {
                "Non classical monocytes": 410,
                "gdT cells": 400,
                "Regulatory T cells": 71,
                "conventional DC": 67,
            },
        },
        "D11": {
            "data_types": ["RNA", "ATAC"],
            "counts": {
                "CD14+ Mono": 458,
                "NK": 421,
                "cDC2": 160,
                "Plasma cell": 26,
            },
        },
        "D17": {
            "data_types": ["RNA", "ATAC"],
            "counts": {
                "Myeloid Cells": 682,
                "Parietal Epithelial Cells": 627,
                "Mast Cells": 74,
            },
        },
        "D18": {
            "data_types": ["RNA", "ATAC", "ADT"],
            "counts": {
                "B.Activated": 845,
                "Mono.CD16": 159,
                "Platelets": 63,
            },
        },
    }
    abundances = (0.02, 0.01, 0.005, 0.002, 0.001)
    for dataset, specification in datasets.items():
        registered = registry[dataset]
        n_source = int(registered["n_cells"])
        data_types = specification["data_types"]
        data_files = [registered["modalities"][m] for m in data_types]
        canonicalization = []
        registry_rules = registered.get("obs_name_canonicalization", {})
        for modality in data_types:
            canonicalization.append(registry_rules.get(modality))
        for label, count in specification["counts"].items():
            source_abundance = count / n_source
            slug = re.sub(r"[^A-Za-z0-9+.-]+", "-", label).strip("-")
            for abundance in (a for a in abundances if a < source_abundance):
                abundance_tag = f"{abundance:g}"
                for seed in range(5):
                    identity = f"confirmatory\0{dataset}\0{label}\0{abundance_tag}\0{seed}".encode()
                    subset_seed = 10000 + int(hashlib.sha256(identity).hexdigest()[:8], 16) % 1000000
                    config = {
                        "config_id": (
                            f"E1_{dataset}_rare_{slug}_abundance_{abundance_tag}"
                            f"_confirmatory_smoke_seed{seed}_v1"
                        ),
                        "dataset": dataset,
                        "data_files": data_files,
                        "data_types": data_types,
                        "task": "legacy_garq",
                        "implementation_tag": "diagnostic_variant_rare_subsampling",
                        "label_key": registered["label_key"],
                        "cell_limit": 2000,
                        "subset_seed": 1729,
                        "requested_K": 40,
                        "epochs": 6,
                        "batch_size": 256,
                        "k_knn": 5,
                        "seed": seed,
                        "device": "cuda",
                        "deterministic": True,
                        "anchors_init": "Kmeans",
                        "converge_threshold": 10,
                        "min_available_ram_gb": 32,
                        "min_free_gpu_gb": 8,
                        "result_root": "revision_results",
                        "force": False,
                        "rare_subsampling": {
                            "label_key": registered["label_key"],
                            "target_label": label,
                            "target_abundance": abundance,
                            "seed": subset_seed,
                        },
                        "output_subdir": (
                            f"01_size_resolution/rare_confirmatory/{dataset}/{slug}/"
                            f"abundance_{abundance_tag}/seed{seed}"
                        ),
                    }
                    if any(canonicalization):
                        config["obs_name_canonicalization"] = canonicalization
                    path = output / (
                        f"e1_{dataset}_rare_{slug}_abundance_{abundance_tag}_seed{seed}.yaml"
                    )
                    path.write_text(yaml.safe_dump(config, sort_keys=False), encoding="utf-8")


if __name__ == "__main__":
    main()
