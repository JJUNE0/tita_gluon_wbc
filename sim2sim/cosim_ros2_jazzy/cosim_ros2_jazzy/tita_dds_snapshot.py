#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import subprocess
from datetime import datetime
from pathlib import Path


ROS_ENV_PREFIXES = ("ROS", "RMW", "DDS", "FAST", "CYCLONE")
SENSOR_TOPICS = (
    "{ns}/joint_states",
    "{ns}/imu_sensor_broadcaster/imu",
    "{ns}/chassis/odometry",
)


def _run(cmd: list[str]) -> dict[str, object]:
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True)
    except FileNotFoundError as exc:
        return {
            "cmd": cmd,
            "returncode": 127,
            "stdout": "",
            "stderr": str(exc),
        }
    return {
        "cmd": cmd,
        "returncode": proc.returncode,
        "stdout": proc.stdout,
        "stderr": proc.stderr,
    }


def _format_result(result: dict[str, object]) -> str:
    cmd = " ".join(str(part) for part in result["cmd"])
    return (
        f"$ {cmd}\n"
        f"returncode: {result['returncode']}\n"
        f"stdout:\n{result['stdout']}\n"
        f"stderr:\n{result['stderr']}\n"
    )


def _filtered_env() -> dict[str, str]:
    return {
        key: value
        for key, value in sorted(os.environ.items())
        if key.upper().startswith(ROS_ENV_PREFIXES)
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Capture a read-only ROS 2 / DDS snapshot for TITA debugging.")
    parser.add_argument("--namespace", default="tita4252763")
    parser.add_argument("--output-dir", default="~/tita_dds_debug")
    parser.add_argument("--label", default="")
    args = parser.parse_args()

    namespace = str(args.namespace).strip("/")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    label = f"_{args.label}" if str(args.label).strip() else ""
    output_dir = Path(args.output_dir).expanduser() / f"{timestamp}{label}"
    output_dir.mkdir(parents=True, exist_ok=True)

    commands = [
        ["ip", "-br", "addr"],
        ["ip", "route"],
        ["ros2", "doctor", "--report"],
        ["ros2", "node", "list"],
        ["ros2", "topic", "list"],
    ]
    topic_checks = [topic.format(ns=f"/{namespace}") for topic in SENSOR_TOPICS]

    report: dict[str, object] = {
        "timestamp": timestamp,
        "namespace": namespace,
        "env": _filtered_env(),
        "commands": [],
    }

    text_chunks: list[str] = [
        f"output_dir: {output_dir}",
        f"namespace: /{namespace}",
        "read_only: true",
        "",
        "filtered_env:",
        json.dumps(report["env"], indent=2, sort_keys=True),
        "",
    ]

    for cmd in commands:
        result = _run(cmd)
        report["commands"].append(result)
        text_chunks.append(_format_result(result))

    for topic in topic_checks:
        result = _run(["ros2", "topic", "info", topic, "--verbose"])
        report["commands"].append(result)
        text_chunks.append(_format_result(result))

    text_path = output_dir / "snapshot.txt"
    json_path = output_dir / "snapshot.json"
    text_path.write_text("\n".join(text_chunks), encoding="utf-8")
    json_path.write_text(json.dumps(report, indent=2), encoding="utf-8")

    print(text_path)
    print(json_path)


if __name__ == "__main__":
    main()
