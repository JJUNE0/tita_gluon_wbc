#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import signal
import subprocess
import time
from datetime import datetime
from pathlib import Path


SAFE_TOPICS = (
    "{ns}/joint_states",
    "{ns}/imu_sensor_broadcaster/imu",
    "{ns}/chassis/odometry",
)


def _safe_topics(namespace: str) -> list[str]:
    ns = f"/{namespace.strip('/')}"
    return [topic.format(ns=ns) for topic in SAFE_TOPICS]


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Record only the TITA state topics into a rosbag for offline read-only debugging."
    )
    parser.add_argument("--namespace", default="tita4252763")
    parser.add_argument("--output-dir", default="~/tita_dds_debug")
    parser.add_argument("--label", default="tita_real_state")
    parser.add_argument(
        "--duration",
        type=float,
        default=0.0,
        help="Optional duration in seconds. Use 0 to record until Ctrl-C.",
    )
    args = parser.parse_args()

    namespace = str(args.namespace).strip("/")
    topics = _safe_topics(namespace)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = Path(args.output_dir).expanduser()
    bag_prefix = output_dir / f"{args.label}_{timestamp}"
    output_dir.mkdir(parents=True, exist_ok=True)

    metadata = {
        "timestamp": timestamp,
        "namespace": namespace,
        "read_only": True,
        "bag_prefix": str(bag_prefix),
        "topics": topics,
        "forbidden_topics": [
            f"/{namespace}/command/user/command",
            f"/{namespace}/command/manager/cmd_key",
            f"/{namespace}/command/manager/cmd_twist",
            f"/{namespace}/command/manager/cmd_pose",
            f"/{namespace}/command/active/command",
            f"/{namespace}/command/passive/command",
            f"/{namespace}/command/teleop/command",
        ],
    }
    (bag_prefix.with_suffix(".json")).write_text(json.dumps(metadata, indent=2), encoding="utf-8")

    cmd = ["ros2", "bag", "record", "-o", str(bag_prefix), *topics]
    print("Recording read-only topics only:")
    print(" ".join(cmd))

    try:
        proc = subprocess.Popen(cmd)
    except FileNotFoundError as exc:
        print(str(exc))
        return
    try:
        if args.duration and args.duration > 0.0:
            end = time.monotonic() + float(args.duration)
            while time.monotonic() < end and proc.poll() is None:
                time.sleep(0.2)
            if proc.poll() is None:
                proc.send_signal(signal.SIGINT)
                proc.wait(timeout=30)
        else:
            proc.wait()
    except KeyboardInterrupt:
        if proc.poll() is None:
            proc.send_signal(signal.SIGINT)
            proc.wait(timeout=30)
    finally:
        if proc.poll() is None:
            proc.terminate()


if __name__ == "__main__":
    main()
