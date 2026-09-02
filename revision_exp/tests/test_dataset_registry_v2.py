from pathlib import Path

import yaml


def test_confirmed_dataset_label_keys_match_audited_obs_columns() -> None:
    registry_path = Path("revision_exp/data_registry/datasets_v2.yaml")
    datasets = yaml.safe_load(registry_path.read_text(encoding="utf-8"))["datasets"]
    assert datasets["D5"]["label_key_candidate"] == "celltype"
    assert datasets["D11"]["label_key_candidate"] == "cell_type"
    assert datasets["D16"]["label_key_candidate"] == "cell_type"
    assert datasets["D17"]["label_key_candidate"] == "celltype"
    assert datasets["D18"]["label_key_candidate"] == "celltype"
