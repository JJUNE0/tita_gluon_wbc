from pathlib import Path

import numpy as np
import pytest

from tita_low_level_sdk.action_adapter import DryRunActionAdapter
from tita_low_level_sdk.policy_gate import PolicyDryRunGate
from tita_low_level_sdk import stage2_production_preflight


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


def test_stage2_preflight_reports_actual_direct_entry_path(tmp_path, monkeypatch):
    workspace = tmp_path / "src"
    upstream = workspace / "ddt_ros2_control"
    controller_root = workspace / "tita_stage1_controller"
    lowlevel = tmp_path / "tita_low_level_sdk"
    policy = tmp_path / "policy.onnx"
    policy.write_bytes(b"fake")

    (controller_root / "config").mkdir(parents=True)
    (controller_root / "launch").mkdir(parents=True)
    (upstream / "interaction" / "teleop_command" / "src").mkdir(parents=True)
    (lowlevel / "launch").mkdir(parents=True)

    (controller_root / "config" / "tita_stage2_controllers.yaml").write_text(
        (
            "/**:\n"
            "  tita_stage1_controller:\n"
            "    ros__parameters:\n"
            "      stage1_only: false\n"
            "      transform_up:\n"
            "        stand_jpos: [-0.05, 0.9, -2.6, 0.0, 0.05, 0.9, -2.6, 0.0]\n"
            "      safety:\n"
            "        max_angular_velocity_rad_s: 2.5\n"
            "      stage2:\n"
            "        enabled: true\n"
            "        rl_running_seconds: 0.0\n"
            "        require_zero_joystick: false\n"
            "        joy_command_limits: [1.0, 0.0, 1.0]\n"
            "        joy_command_gain: 0.75\n"
            "        joy_command_ramp_rate: 0.5\n"
            "        joy_command_stop_seconds: 0.5\n"
            f"        policy_path: {policy}\n"
            "        policy_sha256: 6bcd8c4028507dc636f58eee64ad9cfb9c7cc2d948889df4217ba91ba9e8a121\n"
            "        max_leg_target_delta_rad: 1.0\n"
            "        max_wheel_velocity_rad_s: 15.0\n"
            "        max_repeated_clipping: 5\n"
            "        max_inference_seconds: 0.010\n"
            "        policy_rate_hz: 50.0\n"
            "        allow_clipped_rl_diagnostic: true\n"
        ),
        encoding="utf-8",
    )
    (controller_root / "launch" / "stage1_hardware.launch.py").write_text(
        "joy_only = True\nreceive_only = True\ndirect_joy_reader = True\n",
        encoding="utf-8",
    )
    (upstream / "interaction" / "teleop_command" / "src" / "teleop_command_node.cpp").write_text(
        "bool joy_only = true; bool receive_only = true; const char* direct_joy_reader = \"on\";\n",
        encoding="utf-8",
    )
    (upstream / "interaction" / "teleop_command" / "src" / "elrs_emwave_device.cpp").write_text(
        "bool joy_only = true; bool receive_only = true; const char* direct_joy_reader = \"on\";\n",
        encoding="utf-8",
    )
    (lowlevel / "launch" / "direct_rl_mode.launch.py").write_text(
        "\n".join(
            [
                '("execute_vendor_stop", "false")',
                '("execute_start_bash", "false")',
                '("enable_hardware_output", "false")',
                '("operator_arm", "false")',
            ]
        ) + "\n",
        encoding="utf-8",
    )

    monkeypatch.setattr(
        stage2_production_preflight,
        "inspect_stage1",
        lambda args: {"ready": True, "blockers": [], "plugin_files": {"ok": True}},
    )
    monkeypatch.setattr(
        stage2_production_preflight,
        "sha256",
        lambda path: "6bcd8c4028507dc636f58eee64ad9cfb9c7cc2d948889df4217ba91ba9e8a121",
    )

    class FakeRunner:
        def __init__(self, _policy_path):
            self.status = type(
                "Status",
                (),
                {
                    "loaded": True,
                    "detail": "loaded",
                    "input_names": ("nn_input0",),
                    "output_names": ("nn_output", "estimator"),
                },
            )()
            self.last_inference_ms = 0.0
            self.estimator_output_name = "estimator"

        def act(self, observation):
            del observation
            self.last_inference_ms = 1.0
            return np.zeros(8, dtype=np.float32)

        def act_with_estimator(self, observation):
            return self.act(observation), np.zeros(3, dtype=np.float32)

    monkeypatch.setattr(stage2_production_preflight, "OnnxPolicyRunner", FakeRunner)

    report = stage2_production_preflight.inspect(
        type(
            "Args",
            (),
            {
                "upstream": str(upstream),
                "install": str(tmp_path / "install"),
                "lowlevel": str(lowlevel),
                "policy": str(policy),
                "output": "",
            },
        )()
    )

    assert report["ready"] is True
    assert report["controller_entry_path"] == "transform_up -> five_second_stand -> RL_RUNNING"
    assert report["policy_stand_bridge_enabled"] is False
    assert report["transition_wait_seconds"] == pytest.approx(0.0)
    assert report["transition_blend_seconds"] == pytest.approx(0.0)
    assert report["joystick_command_ramp_rate"] == pytest.approx(0.5)
    assert report["joystick_command_stop_seconds"] == pytest.approx(0.5)
