"""ROBOT_READ_ONLY: bounded subscriptions, no publishers/SDK/mode/service changes."""
from collections import Counter
import json
import time

import rclpy
from diagnostic_msgs.msg import DiagnosticArray
from rclpy.qos import QoSProfile, ReliabilityPolicy
from std_msgs.msg import Float64
from tita_locomotion_interfaces.msg import LocomotionCmd


def main():
    rclpy.init()
    node = rclpy.create_node('vendor_recovery_readonly_probe')
    counts = Counter()
    diagnostics = Counter()
    qos = QoSProfile(depth=10, reliability=ReliabilityPolicy.BEST_EFFORT)

    def status(msg):
        counts['status'] += 1
        for entry in msg.status:
            diagnostics.update((v.key, v.value) for v in entry.values)

    subs = [node.create_subscription(DiagnosticArray, '/tita4252763/system/status', status, qos),
            node.create_subscription(Float64, '/tita4252763/robot_vel',
                                     lambda msg: counts.update(['robot_vel']), qos),
            node.create_subscription(LocomotionCmd, '/tita4252763/command/passive/command',
                                     lambda msg: counts.update(['passive']), qos)]
    start = time.monotonic()
    try:
        while time.monotonic()-start < 6.:
            rclpy.spin_once(node, timeout_sec=.1)
        result = {'execution_domain': 'ROBOT_READ_ONLY', 'seconds': time.monotonic()-start,
                  'counts': dict(counts),
                  'diagnostics': {key: {value: n for (name, value), n in diagnostics.items() if name == key}
                                  for key, _ in diagnostics}}
        result['core_diagnostics_ok'] = all(
            diagnostics[(key, 'OK')] > 0 and diagnostics[(key, 'Timeout')] == 0
            for key in ('Joy', 'BodyImu', 'Robot'))
        result['passive_and_velocity_restored'] = counts['passive'] > 0 and counts['robot_vel'] > 0
        result['evidence_status'] = 'PASS' if result['core_diagnostics_ok'] and result['passive_and_velocity_restored'] else 'SUSPICIOUS'
        print(json.dumps(result, indent=2), flush=True)
    finally:
        for sub in subs:
            node.destroy_subscription(sub)
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
