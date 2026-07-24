from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import xml.etree.ElementTree as ET

import yaml


EXPECTED_COMMIT = "e7b32d9746df900680641ff2845ffb0b5ffe99ed"
EXPECTED_START_SHA256 = "0a2bca4a146f9127ad558b50ca745826cc93ee920f3bb9538521555ea94f97b3"
JOINTS = (
    "joint_left_leg_1", "joint_left_leg_2", "joint_left_leg_3", "joint_left_leg_4",
    "joint_right_leg_1", "joint_right_leg_2", "joint_right_leg_3", "joint_right_leg_4",
)
JOINT_COMMAND_INTERFACES = {"position", "velocity", "effort", "kp", "kd"}
HARDWARE_GPIO_COMMAND_INTERFACES = {
    "command_enable", "stage1_state", "controller_sequence", "transform_progress",
    "settle_elapsed", "command_prepared",
    "rl_prepare_elapsed", "rl_blend_alpha", "rl_running_elapsed", "history_valid_count",
    "inference_ms", "joy_fresh", "joy_zero", "repeated_clipping", "logger_flush_request",
    "joy_age_ms", "joy_command_vx", "joy_command_vy", "joy_command_yaw",
} | {f"obs_current{index}" for index in range(33)} | {
    f"{prefix}{index}"
    for prefix in (
        "action_policy", "action_native", "action_scaled", "stand_target", "rl_target",
        "limited_target", "blended_target", "clipping_mask",
        "joy_axis",
    )
    for index in range(8)
}
HARDWARE_GPIO_STATE_INTERFACES = {
    "read_valid", "write_success", "write_sequence", "consecutive_write_failures",
    "motors_online", "dropped_write_log_records", "hardware_output_enabled",
    "motor_api_write_count", "imu_fresh", "motors_fresh", "joint_vectors_valid",
    "state_values_finite", "motor_status_all_online", "motor_status_available",
    "logger_flushed_sequence",
    "last_command_q0", "last_command_q1", "last_command_q2", "last_command_q3",
    "last_command_q4", "last_command_q5", "last_command_q6", "last_command_q7",
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def command(argv: list[str]) -> tuple[int, str, str]:
    result = subprocess.run(
        argv, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        text=True, timeout=10.0, check=False,
    )
    return result.returncode, result.stdout.strip(), result.stderr.strip()


def nested(mapping: dict, *keys: str):
    value = mapping
    for key in keys:
        value = value[key]
    return value


def inspect(args: argparse.Namespace) -> dict[str, object]:
    upstream = Path(args.upstream).resolve()
    install = Path(args.install).resolve()
    report: dict[str, object] = {
        "command_output": "DISABLED",
        "direct_confirmation": "DIRECT_CONFIRMATION_REQUIRES_STAGE1_TEST",
        "blockers": [],
    }
    blockers: list[str] = report["blockers"]  # type: ignore[assignment]

    code, commit, _ = command(["git", "-C", str(upstream), "rev-parse", "HEAD"])
    report["upstream_commit"] = commit if code == 0 else "unavailable"
    if commit != EXPECTED_COMMIT:
        blockers.append("UPSTREAM_COMMIT_MISMATCH")

    start = upstream / "start.bash"
    report["start_bash_path"] = str(start)
    report["start_bash_sha256"] = sha256(start) if start.is_file() else "missing"
    if report["start_bash_sha256"] != EXPECTED_START_SHA256:
        blockers.append("START_BASH_HASH_MISMATCH")

    def installed(package: str, relative: str) -> Path:
        merged = install / relative
        isolated = install / package / relative
        return merged if merged.exists() else isolated

    plugin_files = {
        "hardware_bridge": installed("hardware_bridge", "share/hardware_bridge/hardware_bridge_plugin.xml"),
        "stage1_controller": installed("tita_stage1_controller", "share/tita_stage1_controller/tita_stage1_controller_plugin.xml"),
        "hardware_library": installed("hardware_bridge", "lib/libhardware_bridge.so"),
        "controller_library": installed("tita_stage1_controller", "lib/libtita_stage1_controller.so"),
        "readonly_soak_launch": installed(
            "tita_stage1_controller",
            "share/tita_stage1_controller/launch/direct_readonly_soak.launch.py",
        ),
    }
    report["plugin_files"] = {name: path.is_file() for name, path in plugin_files.items()}
    for name, path in plugin_files.items():
        if not path.is_file():
            blockers.append(f"MISSING_{name.upper()}")
    for key in ("hardware_library", "controller_library"):
        path = plugin_files[key]
        if path.is_file():
            code, output, error = command(["ldd", str(path)])
            report[f"{key}_ldd"] = output
            if code != 0 or "not found" in output or "not found" in error:
                blockers.append(f"UNRESOLVED_{key.upper()}")

    urdf_path = upstream / "urdfs/tita_description/xacro/robot.xacro"
    config_path = upstream.parent / "tita_stage1_controller/config/tita_stage1_controllers.yaml"
    report["controller_config"] = str(config_path)
    if not config_path.is_file():
        blockers.append("MISSING_STAGE1_CONFIG")
    else:
        config = yaml.safe_load(config_path.read_text(encoding="utf-8"))["/**"]["tita_stage1_controller"]["ros__parameters"]
        report["joint_count"] = len(config["joints"])
        report["joint_order"] = config["joints"]
        if tuple(config["joints"]) != JOINTS:
            blockers.append("JOINT_ORDER_MISMATCH")
        fold = config["transform_up"]["fold_jpos"]
        stand = config["transform_up"]["stand_jpos"]
        upstream_config = yaml.safe_load(
            (upstream / "controller/rl_controller/config/tita/controllers.yaml").read_text(encoding="utf-8")
        )["/**"]["tita_rl_controller"]["ros__parameters"]["transform_up"]
        report["transform_up_matches_upstream"] = (
            fold == upstream_config["fold_jpos"] and stand == upstream_config["stand_jpos"]
        )
        if not report["transform_up_matches_upstream"]:
            blockers.append("TRANSFORM_UP_SOURCE_MISMATCH")
        operational_lower = config["safety"]["lower_limits"]
        operational_upper = config["safety"]["upper_limits"]
        transition_lower = config["transform_up"]["transition_lower_limits"]
        transition_upper = config["transform_up"]["transition_upper_limits"]
        fold_violations = [
            {
                "joint": JOINTS[index], "target": target,
                "lower": transition_lower[index], "upper": transition_upper[index],
            }
            for index, target in enumerate(fold)
            if target < transition_lower[index] or target > transition_upper[index]
        ]
        stand_violations = [
            {
                "joint": JOINTS[index], "target": target,
                "lower": operational_lower[index], "upper": operational_upper[index],
            }
            for index, target in enumerate(stand)
            if target < operational_lower[index] or target > operational_upper[index]
        ]
        nesting_violations = [
            JOINTS[index] for index in range(len(JOINTS))
            if transition_lower[index] > operational_lower[index]
            or transition_upper[index] < operational_upper[index]
        ]
        expected_extensions = all(
            transition_lower[index] == (
                -2.7 if index in (2, 6) else operational_lower[index]
            ) and transition_upper[index] == operational_upper[index]
            for index in range(len(JOINTS))
        )
        report["transform_transition_lower_limits"] = transition_lower
        report["operational_lower_limits"] = operational_lower
        report["transform_up_fold_transition_violations"] = fold_violations
        report["standing_operational_violations"] = stand_violations
        report["envelope_nesting_violations"] = nesting_violations
        report["transition_extension_exact_official_l3_r3"] = expected_extensions
        report["transform_up_fold_is_commanded"] = True
        envelope_pass = not fold_violations and not stand_violations and not nesting_violations \
            and expected_extensions
        report["transform_up_limit_semantics"] = (
            "PASS: official fold is inside transition envelope; standing is inside operational envelope"
            if envelope_pass else "BLOCKED: transition/operational envelope mismatch"
        )
        if not envelope_pass:
            blockers.append("TRANSFORM_OPERATIONAL_ENVELOPE_MISMATCH")

        bridge_source = upstream / "hardware/hardware_bridge/src/hardware_bridge_node.cpp"
        controller_source = upstream.parent / "tita_stage1_controller/src/stage1_controller.cpp"
        core_source = upstream.parent / "tita_stage1_controller/src/stage1_core.cpp"
        bridge_text = bridge_source.read_text(encoding="utf-8") if bridge_source.is_file() else ""
        controller_text = (
            controller_source.read_text(encoding="utf-8")
            if controller_source.is_file() else ""
        )
        core_text = core_source.read_text(encoding="utf-8") if core_source.is_file() else ""
        report["downstream_operational_position_clamp_present"] = (
            "std::clamp(mJoints[id].positionCommand" in bridge_text
            or "-2.670354" in bridge_text
        )
        report["hardware_command_correlation_present"] = all(
            marker in bridge_text + controller_text + core_text
            for marker in ("last_command_q", "UNEXPECTED_COMMAND_CLAMP", "record.q[id] = p.back()")
        )
        if report["downstream_operational_position_clamp_present"]:
            blockers.append("DOWNSTREAM_POSITION_CLAMP_PRESENT")
        if not report["hardware_command_correlation_present"]:
            blockers.append("HARDWARE_COMMAND_CORRELATION_MISSING")

    if urdf_path.is_file():
        # Invoke xacro through the current interpreter.  The Desktop Jazzy entry-point has a
        # system-Python shebang while xacro's package metadata lives in the project venv; calling
        # its main function keeps the audit in the same, explicitly selected Python environment.
        code, urdf_xml, error = command([
            sys.executable, "-c", "import xacro; xacro.main()",
            str(urdf_path), "hw_env:=hw",
        ])
        report["description_xacro_valid"] = code == 0
        if code != 0:
            report["description_xacro_error"] = error
            blockers.append("TITA_DESCRIPTION_INVALID")
        else:
            root = ET.fromstring(urdf_xml)
            ros2_control = root.find("ros2_control")
            plugin = None if ros2_control is None else ros2_control.find("hardware/plugin")
            report["hardware_plugin"] = "" if plugin is None else (plugin.text or "").strip()
            if report["hardware_plugin"] != "tita_locomotion::HardwareBridge":
                blockers.append("HARDWARE_PLUGIN_MISMATCH")
            hardware_parameters = {} if ros2_control is None else {
                item.attrib.get("name", ""): (item.text or "").strip()
                for item in ros2_control.findall("hardware/param")
            }
            report["hardware_output_default"] = hardware_parameters.get(
                "hardware_output_enabled", "missing"
            ).lower()
            if report["hardware_output_default"] != "false":
                blockers.append("HARDWARE_OUTPUT_DEFAULT_NOT_DISABLED")
            joint_interface_report: dict[str, list[str]] = {}
            if ros2_control is not None:
                for joint in ros2_control.findall("joint"):
                    name = joint.attrib.get("name", "")
                    commands = {
                        item.attrib.get("name", "") for item in joint.findall("command_interface")
                    }
                    joint_interface_report[name] = sorted(commands)
                    if name in JOINTS and commands != JOINT_COMMAND_INTERFACES:
                        blockers.append(f"JOINT_COMMAND_INTERFACES_{name}")
            report["joint_command_interfaces"] = joint_interface_report
            if set(joint_interface_report) != set(JOINTS):
                blockers.append("HARDWARE_JOINT_SET_MISMATCH")
            gpio = None if ros2_control is None else ros2_control.find("gpio[@name='hardware_bridge']")
            gpio_commands = set() if gpio is None else {
                item.attrib.get("name", "") for item in gpio.findall("command_interface")
            }
            gpio_states = set() if gpio is None else {
                item.attrib.get("name", "") for item in gpio.findall("state_interface")
            }
            report["hardware_gpio_command_interfaces"] = sorted(gpio_commands)
            report["hardware_gpio_state_interfaces"] = sorted(gpio_states)
            if gpio_commands != HARDWARE_GPIO_COMMAND_INTERFACES:
                blockers.append("HARDWARE_GPIO_COMMAND_INTERFACES_MISMATCH")
            if gpio_states != HARDWARE_GPIO_STATE_INTERFACES:
                blockers.append("HARDWARE_GPIO_STATE_INTERFACES_MISMATCH")
    else:
        blockers.append("MISSING_TITA_DESCRIPTION")

    stage1_launch = upstream.parent / "tita_stage1_controller/launch/stage1_hardware.launch.py"
    soak_launch = upstream.parent / "tita_stage1_controller/launch/direct_readonly_soak.launch.py"
    stage1_launch_text = stage1_launch.read_text(encoding="utf-8") if stage1_launch.is_file() else ""
    soak_launch_text = soak_launch.read_text(encoding="utf-8") if soak_launch.is_file() else ""
    report["stage1_launch_output_gate_enabled"] = '"hardware_output_enabled": "true"' in stage1_launch_text
    report["soak_launch_output_gate_disabled"] = '"hardware_output_enabled": "false"' in soak_launch_text
    report["soak_launch_has_stage1_spawner"] = 'arguments=["tita_stage1_controller"' in soak_launch_text
    if not report["stage1_launch_output_gate_enabled"]:
        blockers.append("STAGE1_OUTPUT_GATE_NOT_EXPLICIT")
    if not report["soak_launch_output_gate_disabled"] or report["soak_launch_has_stage1_spawner"]:
        blockers.append("READONLY_SOAK_NOT_INERT")

    report["vendor_service_active"] = command(
        ["systemctl", "is-active", "--quiet", "tita-bringup.service"]
    )[0] == 0
    report["ready"] = not blockers
    report["decision"] = "READY_FOR_DIRECT_STAND_UP_STAGE1" if report["ready"] else "BLOCKED"
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description="Command-free TITA Stage 1 production preflight")
    parser.add_argument("--upstream", default="/home/robot/direct_ws/src/ddt_ros2_control")
    parser.add_argument("--install", default="/home/robot/direct_ws/install")
    parser.add_argument("--output", default="")
    args = parser.parse_args()
    try:
        report = inspect(args)
    except Exception as error:  # fail closed and keep a machine-readable result
        report = {"ready": False, "decision": "FAIL", "blockers": [str(error)], "command_output": "DISABLED"}
    rendered = json.dumps(report, indent=2, sort_keys=True)
    print(rendered)
    if args.output:
        Path(args.output).write_text(rendered + "\n", encoding="utf-8")
    return 0 if report.get("ready") else 2


if __name__ == "__main__":
    sys.exit(main())
