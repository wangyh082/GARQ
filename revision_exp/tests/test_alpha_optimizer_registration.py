from revision_exp.audit.e0 import capture_parameter_registration


def test_alpha_is_created_after_optimizer_and_recreated():
    _rows, summary = capture_parameter_registration()
    assert summary["alpha_present_before_forward"] is False
    assert summary["alpha_in_optimizer_after_forward"] is False
    assert summary["alpha_recreated_each_forward"] is True
