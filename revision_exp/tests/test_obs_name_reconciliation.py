import numpy as np
import pytest

from revision_exp.workflows.legacy import _canonicalize_obs_names


def test_d18_adt_batch_separator_canonicalization():
    names = np.array(["CAATGTCAGTGAACGA.6", "CATTGTAAGCGCTAAT.3"])
    rule = {"pattern": r"\.([0-9]+)$", "replacement": r"-\1"}
    assert _canonicalize_obs_names(names, rule).tolist() == [
        "CAATGTCAGTGAACGA-6",
        "CATTGTAAGCGCTAAT-3",
    ]


def test_canonicalization_rejects_duplicates():
    names = np.array(["A.1", "A-1"])
    rule = {"pattern": r"\.([0-9]+)$", "replacement": r"-\1"}
    with pytest.raises(ValueError, match="duplicate"):
        _canonicalize_obs_names(names, rule)
