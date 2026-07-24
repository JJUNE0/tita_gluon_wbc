from __future__ import annotations

import argparse
import os
import signal
import subprocess
from datetime import datetime
from pathlib import Path

import rclpy
from rclpy.node import Node


class LowLevelDiscovery(Node):
    """Read-only inventory of controllers, interfaces, graph endpoints, and SDK source references."""

    def __init__(self, tita_ns: str, output_root: str, source_root: str) -> None:
        super().__init__("tita_low_level_discovery")
        self.tita_ns = tita_ns.strip("/")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.output_dir = Path(output_root).expanduser() / f"discovery_{timestamp}"
        self.source_root = Path(source_root).expanduser()

    def run(self) -> Path:
        self.output_dir.mkdir(parents=True, exist_ok=True)
        controller = f"/{self.tita_ns}/controller_manager"
        commands = {
            "controllers.txt": ["ros2", "control", "list_controllers", "-c", controller],
            "hardware_interfaces.txt": ["ros2", "control", "list_hardware_interfaces", "-c", controller],
            "hardware_components.txt": ["ros2", "control", "list_hardware_components", "-c", controller],
            "topics.txt": ["ros2", "topic", "list", "-t"],
            "services.txt": ["ros2", "service", "list"],
            "actions.txt": ["ros2", "action", "list", "-t"],
        }
        patterns = [
            "JointTrajectory", "Float64MultiArray", "hardware_interface", "command_interface",
            "effort", "velocity", "position", "motor", "controller_manager",
        ]
        for filename, command in commands.items():
            self._capture(filename, command, timeout_sec=8)
        for pattern in patterns:
            self._capture(
                f"grep_{pattern}.txt",
                ["grep", "-R", "-n", "--", pattern, str(self.source_root)],
                timeout_sec=20,
            )
        (self.output_dir / "README.txt").write_text(
            "Read-only discovery only. No ROS services were called and no ROS topic was published.\n",
            encoding="utf-8",
        )
        self.get_logger().info(f"Read-only discovery saved to {self.output_dir}")
        return self.output_dir

    def _capture(self, filename: str, command: list[str], timeout_sec: float) -> None:
        try:
            process = subprocess.Popen(
                command,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                start_new_session=True,
            )
            try:
                stdout, stderr = process.communicate(timeout=timeout_sec)
                output = f"$ {' '.join(command)}\nexit_code={process.returncode}\n\n{stdout}{stderr}"
            except subprocess.TimeoutExpired:
                # ros2 control can spawn a child process. Kill the process group to avoid orphans.
                os.killpg(process.pid, signal.SIGTERM)
                stdout, stderr = process.communicate(timeout=2)
                output = (
                    f"$ {' '.join(command)}\nTIMEOUT after {timeout_sec}s; process group terminated\n\n"
                    f"{stdout}{stderr}"
                )
        except Exception as exc:
            output = f"$ {' '.join(command)}\nERROR: {exc}\n"
        (self.output_dir / filename).write_text(output, encoding="utf-8")


def main(args: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Read-only TITA low-level discovery")
    parser.add_argument("--tita-ns", default="tita4252763")
    parser.add_argument("--output-root", default="~/tita_lowlevel_debug")
    parser.add_argument("--source-root", default="~/tita-sdk/src")
    parsed, ros_args = parser.parse_known_args(args=args)
    rclpy.init(args=ros_args)
    node = LowLevelDiscovery(parsed.tita_ns, parsed.output_root, parsed.source_root)
    try:
        node.run()
    finally:
        node.destroy_node()
        rclpy.shutdown()
