import torch

from revision_exp.audit.e0 import attention_dependency, capture_tensor_shapes


def test_attention_sequence_length_is_one():
    evidence = capture_tensor_shapes()
    assert evidence["sequence_length_observed"] == [1]


def test_other_cell_does_not_change_encoder_target():
    evidence = attention_dependency()[0]
    assert evidence["sequence_length"] == 1
    assert evidence["target_output_max_abs_change"] == 0.0
