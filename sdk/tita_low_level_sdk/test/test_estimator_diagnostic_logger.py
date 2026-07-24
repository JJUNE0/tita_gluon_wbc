from __future__ import annotations

import pytest

from tita_low_level_sdk.estimator_diagnostic_logger import (
    POLICY_DIAGNOSTIC_COLUMNS,
    validated_policy_diagnostic,
)


def test_estimator_policy_diagnostic_schema_is_fixed_and_complete():
    assert len(POLICY_DIAGNOSTIC_COLUMNS) == 81
    assert POLICY_DIAGNOSTIC_COLUMNS[0:4] == (
        "controller_monotonic_ns",
        "controller_sequence",
        "controller_state",
        "inference_ms",
    )
    assert "estimator_mps_x" in POLICY_DIAGNOSTIC_COLUMNS
    assert "wheel_no_slip_integral_m" in POLICY_DIAGNOSTIC_COLUMNS
    assert POLICY_DIAGNOSTIC_COLUMNS[-1] == "imu_ang_vel_2"


def test_estimator_policy_diagnostic_rejects_wrong_width_and_nonfinite():
    assert len(validated_policy_diagnostic((0.0,) * 81)) == 81
    with pytest.raises(ValueError, match="width"):
        validated_policy_diagnostic((0.0,) * 80)
    values = [0.0] * 81
    values[10] = float("nan")
    with pytest.raises(ValueError, match="NaN or Inf"):
        validated_policy_diagnostic(tuple(values))
