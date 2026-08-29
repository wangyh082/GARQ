from revision_exp.audit.e0 import anchor_update_trace


def test_continuous_update_and_delayed_local_branch():
    trace = anchor_update_trace(100)
    # The long-update expression is scheduled for every anchor on every step,
    # but its beta rapidly underflows, so scheduled and effective updates are
    # deliberately audited as different quantities.
    assert all(row["scheduled_long_update_anchor_count"] == 6 for row in trace)
    assert trace[0]["all_anchors_displaced"] is True
    assert any(row["effective_displacement_anchor_count"] == 0 for row in trace[1:87])
    first_local = next(row["step"] for row in trace if row["local_branch_condition"])
    assert first_local == 88
    assert trace[0]["usage_sum"] < trace[-1]["usage_sum"] <= 1.0001
