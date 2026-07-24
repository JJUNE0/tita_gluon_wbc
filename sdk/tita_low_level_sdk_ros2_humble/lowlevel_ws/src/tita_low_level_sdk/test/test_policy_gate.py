from pathlib import Path

import numpy as np
import pytest

from tita_low_level_sdk.action_adapter import DryRunActionAdapter
from tita_low_level_sdk.policy_gate import PolicyDryRunGate


def make_gate(allowed=None, require_fsm_freshness=True):
    return PolicyDryRunGate(
        allowed_modes=[] if allowed is None else allowed,
        fsm_timeout_sec=0.5,
        require_fsm_freshness=require_fsm_freshness,
        fsm_settle_time_sec=2.0,
        require_pose_gate=True,
        require_motion_gate=True,
        max_leg_position_error_rad=0.35,
        max_base_angular_velocity_rad_s=0.5,
        max_projected_gravity_norm_error=0.15,
    )


def evaluate(gate, now):
    return gate.evaluate(now, True, True, 0.1, 0.1, np.asarray([0.0, 0.0, -1.0]))


def test_empty_allowed_modes_blocks():
    gate = make_gate()
    gate.update_mode("candidate", 0.0)
    assert evaluate(gate, 3.0).status == "blocked:no_allowed_fsm_modes_configured"


def test_stale_fsm_blocks():
    gate = make_gate(["candidate"])
    gate.update_mode("candidate", 0.0)
    assert evaluate(gate, 0.6).status == "blocked:fsm_stale"


def test_fsm_not_received_blocks():
    gate = make_gate(["balance"], require_fsm_freshness=False)
    assert evaluate(gate, 3.0).status == "blocked:fsm_not_received"


def test_event_driven_balance_settles_and_remains_ready_without_republish():
    gate = make_gate(["balance"], require_fsm_freshness=False)
    gate.update_mode("balance", 0.0)
    assert evaluate(gate, 0.1).status == "blocked:fsm_settling"
    assert evaluate(gate, 2.1).ready
    assert evaluate(gate, 100.0).ready


def test_event_driven_idle_blocks_immediately():
    gate = make_gate(["balance"], require_fsm_freshness=False)
    gate.update_mode("balance", 0.0)
    assert evaluate(gate, 2.1).ready
    gate.update_mode("idle", 2.2)
    assert evaluate(gate, 2.2).status == "blocked:fsm_mode_not_allowed:idle"


def test_sensor_stale_blocks_with_event_driven_fsm():
    gate = make_gate(["balance"], require_fsm_freshness=False)
    gate.update_mode("balance", 0.0)
    result = gate.evaluate(2.1, False, True, 0.1, 0.1, [0, 0, -1])
    assert not result.ready


def test_mode_mismatch_blocks():
    gate = make_gate(["candidate"])
    gate.update_mode("different", 0.0)
    assert evaluate(gate, 0.1).status == "blocked:fsm_mode_not_allowed:different"


def test_allowed_mode_settles_then_becomes_ready_with_fresh_updates():
    gate = make_gate(["candidate"])
    gate.update_mode("candidate", 0.0)
    assert evaluate(gate, 0.1).status == "blocked:fsm_settling"
    gate.update_mode("candidate", 2.0)
    result = evaluate(gate, 2.1)
    assert result.ready
    assert result.status == "ready:policy_dryrun"


def test_mode_change_blocks_immediately():
    gate = make_gate(["candidate"])
    gate.update_mode("candidate", 0.0)
    gate.update_mode("candidate", 2.0)
    assert evaluate(gate, 2.1).ready
    gate.update_mode("different", 2.2)
    assert evaluate(gate, 2.2).status == "blocked:fsm_mode_not_allowed:different"


def test_pose_motion_and_nonfinite_fail_closed():
    gate = make_gate(["candidate"])
    gate.update_mode("candidate", 0.0)
    gate.update_mode("candidate", 2.0)
    assert gate.evaluate(2.1, True, True, 0.36, 0.1, [0, 0, -1]).status == "blocked:pose_gate"
    assert gate.evaluate(2.1, True, True, 0.1, 0.6, [0, 0, -1]).status == "blocked:motion_gate"
    assert gate.evaluate(2.1, True, False, 0.1, 0.1, [0, 0, -1]).status == "blocked:pose_gate"
    assert gate.evaluate(2.1, True, True, 0.1, 0.1, [np.nan, 0, -1]).status == "blocked:pose_gate"


def test_action_adapter_outputs_finite_split_targets_and_rejects_nan():
    adapter = DryRunActionAdapter()
    result = adapter.compute(np.zeros(8, dtype=np.float32))
    assert result.virtual_joint_target_native.shape == (8,)
    assert result.virtual_leg_target_native.shape == (6,)
    assert result.virtual_wheel_vel_native.shape == (2,)
    assert np.all(np.isfinite(result.virtual_joint_target_native))
    assert np.all(result.target_type_mask_native == np.asarray([1, 1, 1, 2, 1, 1, 1, 2]))
    with pytest.raises(ValueError):
        adapter.compute(np.asarray([np.nan] + [0.0] * 7))


def test_static_read_only_publisher_and_launch_audit():
    root = Path(__file__).resolve().parents[1]
    launch_source = (root / "launch" / "sim2real.launch.py").read_text(encoding="utf-8")
    node_source = (root / "tita_low_level_sdk" / "dryrun_node.py").read_text(encoding="utf-8")
    forbidden = (
        "ros2 topic pub",
        "cmd_key",
        "cmd_twist",
        "cmd_pose",
        "LocomotionCmd",
        "command/user",
        "command/active",
        "command/manager",
    )
    assert not any(token in launch_source for token in forbidden)
    publisher_lines = [line for line in node_source.splitlines() if "create_publisher(" in line]
    assert publisher_lines
    assert 'base = "/tita_lowlevel/dryrun"' in node_source
    assert not any("prefix" in line for line in publisher_lines)
