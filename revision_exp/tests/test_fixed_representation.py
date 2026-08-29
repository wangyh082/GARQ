import anndata as ad
import numpy as np
from scipy import sparse

from revision_exp.workflows.fixed_representation import _adt_pca, _atac_lsi


def test_atac_lsi_is_finite_and_records_depth_rule():
    rng = np.random.default_rng(21)
    counts = sparse.csr_matrix(rng.poisson(0.4, size=(30, 20)).astype(float))
    embedding, provenance = _atac_lsi(ad.AnnData(counts), seed=0)
    assert embedding.shape[0] == 30
    assert np.isfinite(embedding).all()
    assert provenance["remove_first_component_threshold_abs_correlation"] == 0.5


def test_adt_clr_pca_dimension_is_capped_at_features_minus_one():
    rng = np.random.default_rng(22)
    counts = rng.poisson(2.0, size=(25, 8)).astype(float)
    embedding, provenance = _adt_pca(ad.AnnData(counts), seed=0)
    assert embedding.shape == (25, 7)
    assert provenance["components"] == 7
    assert np.isfinite(embedding).all()
