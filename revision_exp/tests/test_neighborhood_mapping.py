import numpy as np

from revision_exp.workflows.neighborhood_mapping import neighbor_jaccard


def test_neighbor_jaccard_is_label_order_invariant():
    a = np.array([[1, 2, 3], [0, 2, 4]])
    b = np.array([[3, 2, 1], [0, 3, 4]])
    result = neighbor_jaccard(a, b)
    assert result[0] == 1.0
    assert result[1] == 0.5


def test_neighbor_jaccard_identical():
    assert np.all(neighbor_jaccard(np.array([[1, 2]]), np.array([[1, 2]])) == 1.0)
