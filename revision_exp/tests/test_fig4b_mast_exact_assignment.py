from revision_exp.workflows.fig4b_mast_exact_assignment import _numeric_row_order


def test_numeric_row_order_requires_complete_zero_based_sequence():
    assert _numeric_row_order(range(4), 4)
    assert not _numeric_row_order([0, 1, 3, 2], 4)
    assert not _numeric_row_order([1, 2, 3, 4], 4)
