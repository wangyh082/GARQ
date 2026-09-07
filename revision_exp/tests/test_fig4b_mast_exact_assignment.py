import numpy as np

from revision_exp.workflows.fig4b_mast_exact_assignment import _bh, _numeric_row_order
from revision_exp.workflows.fig4b_mast_formal import _group_table, _partition_equivalent


def test_numeric_row_order_requires_complete_zero_based_sequence():
    assert _numeric_row_order(range(4), 4)
    assert not _numeric_row_order([0, 1, 3, 2], 4)
    assert not _numeric_row_order([1, 2, 3, 4], 4)


def test_partition_equivalence_allows_id_renaming_but_not_membership_change():
    assert _partition_equivalent(["a", "a", "b", "c"], [10, 10, 20, 30])
    assert not _partition_equivalent(["a", "a", "b", "c"], [10, 20, 20, 30])


def test_bh_is_monotone_and_preserves_finite_order():
    q = _bh([0.001, 0.02, 0.5])
    assert np.all(np.isfinite(q))
    assert q[0] <= q[1] <= q[2]


def test_group_table_uses_strict_majority_and_associated_definition():
    groups = ["a", "a", "b", "b", "c", "c"]
    labels = ["Mast Cells", "Mast Cells", "Mast Cells", "other", "other", "other"]
    table, n_target, abundance = _group_table(groups, labels, "Mast Cells")
    assert n_target == 3
    assert abundance == 0.5
    # purity exactly 0.5 is not majority; the two-cell group is excluded.
    assert not bool(table.loc[table.metacell_id == "b", "is_majority"].iloc[0])
    assert not bool(table.loc[table.metacell_id == "b", "is_associated"].iloc[0])
