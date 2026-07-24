from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

import numpy as np
import yaml

from .action_adapter import DryRunActionAdapter
from .onnx_policy_runner import OnnxPolicyRunner
from .real_obs_builder import RealObservationBuilder
from .stage1_production_preflight import inspect as inspect_stage1, sha256


EXPECTED_POLICY_SHA256 = "339b120f8021d5bca196787d8952bf764c927ad77a3fa2796cbf49811b9c9132"
ACTION_GRAPH_POLICY_SHA256 = "6e7ebf274703d92b022480abd688d0628fdb81dfde341ba56c9600f0eaf86ea3"


def inspect(args: argparse.Namespace) -> dict[str, object]:
    stage1_args = argparse.Namespace(upstream=args.upstream, install=args.install, output="")
    stage1 = inspect_stage1(stage1_args)
    report: dict[str, object] = {
        "command_output": "DISABLED",
        "stage1_path_ready": bool(stage1.get("ready")),
        "stage1_blockers": list(stage1.get("blockers", [])),
        "blockers": [],
    }
    blockers: list[str] = report["blockers"]  # type: ignore[assignment]
    if not report["stage1_path_ready"]:
        blockers.append("STAGE1_PRODUCTION_PATH")

    upstream = Path(args.upstream).resolve()
    controller_root = upstream.parent / "tita_stage1_controller"
    config_path = controller_root / "config/tita_stage2_controllers.yaml"
    report["stage2_controller_config"] = str(config_path)
    if not config_path.is_file():
        blockers.append("MISSING_STAGE2_CONFIG")
        config: dict[str, object] = {}
    else:
        config = yaml.safe_load(config_path.read_text(encoding="utf-8"))[
            "/**"
        ]["tita_stage1_controller"]["ros__parameters"]

    policy_path = Path(args.policy).resolve()
    report["policy_path"] = str(policy_path)
    report["policy_sha256"] = sha256(policy_path) if policy_path.is_file() else "missing"
    if report["policy_sha256"] != EXPECTED_POLICY_SHA256:
        blockers.append("POLICY_HASH_MISMATCH")
    runner = OnnxPolicyRunner(str(policy_path))
    report["policy_loaded"] = runner.status.loaded
    report["policy_detail"] = runner.status.detail
    report["policy_input_names"] = runner.status.input_names
    report["policy_output_names"] = runner.status.output_names
    if not runner.status.loaded:
        blockers.append("POLICY_LOAD_OR_INTERFACE")
    report["action_graph_reference_sha256"] = ACTION_GRAPH_POLICY_SHA256
    report["estimator_output_available"] = bool(runner.estimator_output_name)
    if not report["estimator_output_available"]:
        blockers.append("ESTIMATOR_OUTPUT_MISSING")

    if config:
        stage2 = config["stage2"]  # type: ignore[index]
        transform = config["transform_up"]  # type: ignore[index]
        report["stage2_enabled"] = bool(stage2["enabled"])
        report["stage1_only"] = bool(config["stage1_only"])
        report["rl_running_seconds"] = float(stage2["rl_running_seconds"])
        report["configured_max_angular_velocity_rad_s"] = float(
            config["safety"]["max_angular_velocity_rad_s"]  # type: ignore[index]
        )
        report["zero_command_mode_requires_centered_joystick"] = bool(
            stage2["require_zero_joystick"]
        )
        report["joystick_command_limits"] = list(map(float, stage2["joy_command_limits"]))
        report["joystick_command_gain"] = float(stage2.get("joy_command_gain", 1.0))
        report["joystick_command_ramp_rate"] = float(
            stage2.get("joy_command_ramp_rate", 0.0)
        )
        report["joystick_command_stop_seconds"] = float(
            stage2.get("joy_command_stop_seconds", 0.0)
        )
        report["joystick_effective_command_limits"] = [
            value * report["joystick_command_gain"]
            for value in report["joystick_command_limits"]
        ]
        if not report["stage2_enabled"] or report["stage1_only"]:
            blockers.append("STAGE2_MODE_CONFIG")
        if report["joystick_command_ramp_rate"] != 0.5:
            blockers.append("JOYSTICK_COMMAND_RAMP_RATE")
        if report["joystick_command_stop_seconds"] != 0.5:
            blockers.append("JOYSTICK_COMMAND_STOP_SECONDS")
        if float(stage2["rl_running_seconds"]) != 0.0:
            blockers.append("RL_RUNNING_DURATION")
        legacy_transition_fields = {
            "handoff_seconds", "handoff_settle_seconds", "rl_prepare_seconds",
            "rl_prepare_timeout_seconds", "rl_blend_seconds", "policy_stand_jpos",
        }
        report["legacy_transition_fields_present"] = sorted(
            legacy_transition_fields.intersection(stage2)
        )
        if report["legacy_transition_fields_present"]:
            blockers.append("LEGACY_POLICY_TRANSITION_CONFIG")
        configured_policy_path = Path(str(stage2["policy_path"])).expanduser()
        report["configured_policy_path"] = str(configured_policy_path)
        if configured_policy_path.is_file() and configured_policy_path.resolve() != policy_path:
            blockers.append("POLICY_PATH_CONFIG_MISMATCH")
        if str(stage2["policy_sha256"]) != EXPECTED_POLICY_SHA256:
            blockers.append("POLICY_SHA_CONFIG_MISMATCH")

        # Command-free RL entry check at the exact official standing target. My26 consumes only
        # the current 33-D proprio frame; its base velocity estimator is embedded in the graph.
        # This matches the production path: official TransformUp, five continuous
        # stable seconds, then the native policy target on the next controller cycle.
        builder = RealObservationBuilder()
        adapter = DryRunActionAdapter(
            float(stage2["max_leg_target_delta_rad"]),
            float(stage2["max_wheel_velocity_rad_s"]),
        )
        # Production enters the policy from the exact official TransformUp stand.
        q = np.asarray(transform["stand_jpos"], dtype=np.float32)
        report["controller_entry_path"] = "transform_up -> five_second_stand -> RL_RUNNING"
        report["policy_stand_bridge_enabled"] = False
        report["policy_entry_source_pose"] = np.asarray(
            transform["stand_jpos"], dtype=float
        ).tolist()
        report["transition_wait_seconds"] = 0.0
        report["transition_blend_seconds"] = 0.0
        dq = np.zeros(8, dtype=np.float32)
        quat_wxyz = np.asarray([1.0, 0.0, 0.0, 0.0], dtype=np.float32)
        command = np.zeros(3, dtype=np.float32)
        action_policy = np.zeros(8, dtype=np.float32)
        max_leg_stand_delta = 0.0
        max_abs_exact_wheel = 0.0
        max_inference_ms = 0.0
        estimator_abs_max = np.zeros(3, dtype=np.float32)
        first_action: list[float] = []
        for frame in range(max(50, int(float(stage2["policy_rate_hz"])))):
            observation, _ = builder.build(q, dq, quat_wxyz, np.zeros(3), command)
            action_policy, estimator_scaled = runner.act_with_estimator(observation)
            estimator_abs_max = np.maximum(estimator_abs_max, np.abs(estimator_scaled))
            # The custom policy output is already native left-then-right order.
            action_native = action_policy.copy()
            targets = adapter.compute(action_native)
            if frame == 0:
                first_action = action_policy.astype(float).tolist()
            leg_indices = np.asarray([0, 1, 2, 4, 5, 6], dtype=np.int64)
            wheel_indices = np.asarray([3, 7], dtype=np.int64)
            max_leg_stand_delta = max(
                max_leg_stand_delta,
                float(np.max(np.abs(targets.policy_target_native[leg_indices] - q[leg_indices]))),
            )
            max_abs_exact_wheel = max(
                max_abs_exact_wheel,
                float(np.max(np.abs(targets.policy_target_native[wheel_indices]))),
            )
            max_inference_ms = max(max_inference_ms, float(runner.last_inference_ms))
            # During Stage 1 no policy command is selected, so the first Stage 2
            # observation has the zero previous-action value used in sim2sim.
            builder.set_last_action(np.zeros(8, dtype=np.float32))

        report["observation_shape"] = int(observation.size)
        report["history_shape"] = int(builder.history.size)
        report["action_shape"] = int(action_policy.size)
        report["history_order"] = "none"
        report["first_standing_action_policy_order"] = first_action
        report["max_leg_target_delta_from_policy_stand_rad"] = max_leg_stand_delta
        report["max_leg_target_delta_from_official_stand_rad"] = max_leg_stand_delta
        report["max_abs_exact_wheel_target_rad_s"] = max_abs_exact_wheel
        report["max_inference_ms"] = max_inference_ms
        report["estimator_scaled_abs_max"] = estimator_abs_max.astype(float).tolist()
        report["estimator_units"] = "scaled base_lin_vel; divide by 2.0 for m/s"
        if (observation.size, builder.history.size, action_policy.size) != (33, 0, 8):
            blockers.append("POLICY_SHAPES")
        if max_inference_ms > float(stage2["max_inference_seconds"]) * 1000.0:
            blockers.append("INFERENCE_DEADLINE")
        report["native_policy_target_clipping_enabled"] = False

    launch_text = (controller_root / "launch/stage1_hardware.launch.py").read_text(
        encoding="utf-8"
    )
    teleop_text = (
        upstream / "interaction/teleop_command/src/teleop_command_node.cpp"
    ).read_text(encoding="utf-8")
    crsf_text = (
        upstream / "interaction/teleop_command/src/elrs_emwave_device.cpp"
    ).read_text(encoding="utf-8")
    report["direct_joy_receive_only_path"] = all(
        marker in launch_text + teleop_text + crsf_text
        for marker in ("joy_only", "receive_only", "direct_joy_reader")
    )
    if not report["direct_joy_receive_only_path"]:
        blockers.append("DIRECT_JOY_PATH")
    report["default_launch_inert"] = all(
        marker in (Path(args.lowlevel) / "launch/direct_rl_mode.launch.py").read_text(
            encoding="utf-8"
        )
        for marker in (
            '("execute_vendor_stop", "false")',
            '("execute_start_bash", "false")',
            '("enable_hardware_output", "false")',
            '("operator_arm", "false")',
        )
    )
    if not report["default_launch_inert"]:
        blockers.append("DEFAULT_LAUNCH_NOT_INERT")

    report["ready"] = not blockers
    report["decision"] = "READY_FOR_JOYSTICK_RL_STAGE2" if not blockers else "BLOCKED"
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description="Command-free TITA Stage 2 production preflight")
    parser.add_argument("--upstream", default="/home/robot/tita_ws/src/ddt_ros2_control")
    parser.add_argument("--install", default="/home/robot/tita_ws/install")
    parser.add_argument("--lowlevel", default="/home/robot/tita_ws/src/tita_low_level_sdk")
    parser.add_argument(
        "--policy",
        default="/home/robot/tita_ws/policy/policy_my33_2999_estimator_diagnostic.onnx",
    )
    parser.add_argument("--output", default="")
    args = parser.parse_args()
    try:
        report = inspect(args)
    except Exception as error:
        report = {
            "ready": False, "decision": "FAIL", "blockers": [str(error)],
            "command_output": "DISABLED",
        }
    rendered = json.dumps(report, indent=2, sort_keys=True)
    print(rendered)
    if args.output:
        Path(args.output).write_text(rendered + "\n", encoding="utf-8")
    return 0 if report.get("ready") else 2


if __name__ == "__main__":
    sys.exit(main())
