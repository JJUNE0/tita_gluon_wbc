#!/usr/bin/env python3
"""Automated sim2sim probe: does the shoulder (L2/R2) oscillation / settle-spike
show up under real deployment conditions, not just in the Isaac Lab eval?

Drives the live MuJoCo sim2sim node (``mujoco_policy_node``) through the same
scripted velocity-command sequence as ``scripts/np3o/eval_behavior.py`` /
``scripts/rsl_rl/eval_behavior.py`` (settle -> zero_hold -> ramp_up -> cruise
-> decel), but over real ROS2 topics against the actually-running deployment
stack instead of Isaac Lab -- so results are directly comparable to the sim
FFT/drift numbers already collected, and show whether the reset-randomization
settle spike / shoulder shake is something a real robot would actually feel.

Requires a mujoco_policy_node already running (viewer optional) with the
robot in ``idle`` state. This script drives the FSM itself:
idle -> reference_transform_up -> (poll debug/state until settled) -> rl_0
-> scripted cmd_twist sequence -> report + CSV.

Usage:
    source /opt/ros/jazzy/setup.bash
    source install/setup.bash
    source ~/venvs/cosim_ros2_jazzy/bin/activate
    python3 cosim_ros2_jazzy/scripts/probe_shoulder_oscillation.py \\
        --out analysis_runs/sim2sim_shoulder_probe.csv
"""

import argparse
import csv
import os
import time

import rclpy
from geometry_msgs.msg import Twist
from rclpy.node import Node
from sensor_msgs.msg import JointState
from std_msgs.msg import String

JOINT_NAMES = [
    "joint_left_leg_1", "joint_left_leg_2", "joint_left_leg_3", "joint_left_leg_4",
    "joint_right_leg_1", "joint_right_leg_2", "joint_right_leg_3", "joint_right_leg_4",
]
# matches tita.yaml robot.default_joint_angles / standing_joint_angles
DEFAULT_JOINT_POS = [0.1, 0.8, -1.5, 0.0, 0.1, 0.8, -1.5, 0.0]


class ShoulderProbe(Node):
    def __init__(self, tita_ns: str):
        super().__init__("shoulder_oscillation_probe")
        self.cmd_key_pub = self.create_publisher(String, f"/{tita_ns}/command/manager/cmd_key", 10)
        self.cmd_twist_pub = self.create_publisher(Twist, f"/{tita_ns}/command/manager/cmd_twist", 10)
        self.state_sub = self.create_subscription(
            String, "/cosim_ros2_jazzy/debug/state", self._state_cb, 10
        )
        self.joint_sub = self.create_subscription(JointState, "/joint_states", self._joint_cb, 10)
        self.latest_state = None
        self.latest_joint_pos = None  # dict name -> position

    def _state_cb(self, msg: String) -> None:
        self.latest_state = msg.data

    def _joint_cb(self, msg: JointState) -> None:
        self.latest_joint_pos = dict(zip(msg.name, msg.position))

    def send_cmd_key(self, key: str) -> None:
        self.cmd_key_pub.publish(String(data=key))

    def send_twist(self, vx: float, wz: float = 0.0) -> None:
        msg = Twist()
        msg.linear.x = vx
        msg.angular.z = wz
        self.cmd_twist_pub.publish(msg)


def wait_for(node: ShoulderProbe, predicate, timeout_s: float, poll_hz: float = 20.0) -> bool:
    deadline = time.time() + timeout_s
    period = 1.0 / poll_hz
    while time.time() < deadline:
        rclpy.spin_once(node, timeout_sec=period)
        if predicate():
            return True
    return False


def main():
    parser = argparse.ArgumentParser(description="Sim2sim shoulder-oscillation / settle-spike probe.")
    parser.add_argument("--tita_ns", type=str, default="tita")
    parser.add_argument("--ramp_vx", type=float, default=0.75)
    parser.add_argument("--zero_hold_s", type=float, default=3.0)
    parser.add_argument("--ramp_up_s", type=float, default=1.5)
    parser.add_argument("--cruise_s", type=float, default=4.0)
    parser.add_argument("--decel_s", type=float, default=0.5)
    parser.add_argument("--post_stop_s", type=float, default=2.0)
    parser.add_argument("--control_hz", type=float, default=50.0)
    parser.add_argument("--transform_up_timeout_s", type=float, default=8.0)
    parser.add_argument("--out", type=str, default="analysis_runs/sim2sim_shoulder_probe.csv")
    args = parser.parse_args()

    rclpy.init()
    node = ShoulderProbe(args.tita_ns)

    print("[INFO] waiting for /joint_states...")
    if not wait_for(node, lambda: node.latest_joint_pos is not None, timeout_s=10.0):
        raise RuntimeError("No /joint_states received -- is mujoco_policy_node running?")

    print("[INFO] sending reference_transform_up")
    node.send_cmd_key("reference_transform_up")
    time.sleep(0.2)  # let the FSM register the command before we start polling
    ok = wait_for(
        node,
        lambda: node.latest_state == "reference_stand_hold",
        timeout_s=args.transform_up_timeout_s,
    )
    if not ok:
        print(f"[WARN] transform_up did not report 'reference_stand_hold' within "
              f"{args.transform_up_timeout_s}s (last state={node.latest_state}); proceeding anyway")
    time.sleep(0.5)  # extra settle margin, matches manual practice established this session

    print("[INFO] sending rl_0")
    node.send_cmd_key("rl_0")
    time.sleep(0.3)

    dt = 1.0 / args.control_hz
    phases = [
        ("zero_hold", int(args.zero_hold_s / dt), lambda i, n: 0.0),
        ("ramp_up", int(args.ramp_up_s / dt), lambda i, n: args.ramp_vx * (i + 1) / n),
        ("cruise", int(args.cruise_s / dt), lambda i, n: args.ramp_vx),
        ("decel", int(args.decel_s / dt), lambda i, n: args.ramp_vx * (1.0 - (i + 1) / n)),
        ("post_stop", int(args.post_stop_s / dt), lambda i, n: 0.0),
    ]

    log = []
    t0 = time.time()
    for name, n_steps, cmd_fn in phases:
        for i in range(n_steps):
            vx = cmd_fn(i, n_steps)
            node.send_twist(vx, 0.0)
            rclpy.spin_once(node, timeout_sec=dt)
            if node.latest_joint_pos is None:
                continue
            row = {"phase": name, "step": i, "t": time.time() - t0, "cmd_vx": vx}
            for jname, default in zip(JOINT_NAMES, DEFAULT_JOINT_POS):
                pos = node.latest_joint_pos.get(jname)
                row[f"dev_{jname}"] = abs(pos - default) if pos is not None else float("nan")
            log.append(row)

    node.send_twist(0.0, 0.0)

    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
    fieldnames = ["phase", "step", "t", "cmd_vx"] + [f"dev_{n}" for n in JOINT_NAMES]
    with open(args.out, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(log)
    print(f"[INFO] wrote {len(log)} rows to {args.out}")

    # summary: L2/R2 deviation, cruise vs decel (same framing as eval_behavior.py)
    def stats(phase, joint):
        vals = [r[f"dev_{joint}"] for r in log if r["phase"] == phase]
        if not vals:
            return None, None
        return sum(vals) / len(vals), max(vals)

    print("\n" + "=" * 60)
    print(f"joint                 dev cruise(avg/max)   dev decel(avg/max)")
    for j in ["joint_left_leg_2", "joint_right_leg_2"]:
        c_avg, c_max = stats("cruise", j)
        d_avg, d_max = stats("decel", j)
        tag = "  <-- shoulder/thigh"
        print(f"{j:<20}  {c_avg:.4f}/{c_max:.4f}          {d_avg:.4f}/{d_max:.4f}{tag}")
    print("=" * 60)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
