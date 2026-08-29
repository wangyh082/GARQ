import numpy as np
import pytest

from revision_exp.workflows.legacy import _select_targeted_abundance_indices


def test_targeted_abundance_sampling_is_exact_and_without_replacement() -> None:
    labels = np.asarray(["rare"] * 20 + ["common"] * 80)
    indices, info = _select_targeted_abundance_indices(
        labels, n_cells=50, target_label="rare", target_abundance=0.1, seed=7
    )
    assert len(indices) == len(np.unique(indices)) == 50
    assert int((labels[indices] == "rare").sum()) == 5
    assert info["target_abundance_realized"] == 0.1


def test_targeted_abundance_sampling_is_deterministic() -> None:
    labels = np.asarray(["rare"] * 20 + ["common"] * 80)
    first, _ = _select_targeted_abundance_indices(labels, 50, "rare", 0.1, 11)
    second, _ = _select_targeted_abundance_indices(labels, 50, "rare", 0.1, 11)
    assert np.array_equal(first, second)


def test_targeted_abundance_sampling_rejects_upsampling() -> None:
    labels = np.asarray(["rare"] * 5 + ["common"] * 95)
    with pytest.raises(ValueError, match="upsampling is prohibited"):
        _select_targeted_abundance_indices(labels, 50, "rare", 0.1, 3)


def test_targeted_abundance_sampling_rejects_missing_label() -> None:
    labels = np.asarray(["common"] * 100)
    with pytest.raises(ValueError, match="upsampling is prohibited"):
        _select_targeted_abundance_indices(labels, 50, "rare", 0.01, 3)
