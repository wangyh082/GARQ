import pandas as pd

from revision_exp.metrics.metacell import per_type_table


def test_majority_and_high_purity_thresholds_are_distinct():
    frame = pd.DataFrame(
        {
            "cell_id": [f"c{i}" for i in range(10)],
            "metacell_id": [0] * 10,
            "cell_type": ["A"] * 6 + ["B"] * 4,
        }
    )
    result = per_type_table(frame, {"dataset": "synthetic"}).set_index("cell_type")
    assert result.loc["A", "majority_retention"] == 1.0
    assert result.loc["A", "high_purity_recovery"] == 0.0


def test_exact_point_seven_counts_as_high_purity():
    frame = pd.DataFrame(
        {
            "cell_id": [f"c{i}" for i in range(10)],
            "metacell_id": [0] * 10,
            "cell_type": ["A"] * 7 + ["B"] * 3,
        }
    )
    result = per_type_table(frame, {"dataset": "synthetic"}).set_index("cell_type")
    assert result.loc["A", "high_purity_recovery"] == 1.0
