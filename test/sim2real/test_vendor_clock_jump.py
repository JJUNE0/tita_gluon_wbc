"""DESKTOP_DRY_RUN: virtual-time reproduction of installed Humble deadline algorithm.

No ROS initialization, robot access, real sleep or host clock modification.
This proves the scheduling mechanism, not the complete vendor idle-fault chain.
"""
import json
from pathlib import Path
import unittest

PERIOD_NS = 2_000_000
OLD_NS = 28_835_394_336
SYNC_NS = 1_792_311_463_593_205_000
ROOT = Path(__file__).resolve().parents[2]


def run_deadlines(start_ns, now_ns, iterations, work_ns=10_000):
    deadline = start_ns
    now = now_ns
    slept = 0
    for _ in range(iterations):
        now += work_ns
        deadline += PERIOD_NS
        delay = max(0, deadline-now)
        slept += delay > 0
        now += delay
    return dict(iterations=iterations, positive_waits=slept,
                remaining_deadline_lag_s=(now-deadline)*1e-9)


class ClockJump(unittest.TestCase):
    def test_normal_start_waits_every_cycle(self):
        self.assertEqual(run_deadlines(OLD_NS, OLD_NS, 10000)['positive_waits'], 10000)

    def test_large_forward_step_remains_behind(self):
        result = run_deadlines(OLD_NS, SYNC_NS, 100000)
        self.assertEqual(result['positive_waits'], 0)
        self.assertGreater(result['remaining_deadline_lag_s'], 1.7e9)

    def test_restart_after_synchronization_rebases_deadline(self):
        self.assertEqual(run_deadlines(SYNC_NS, SYNC_NS, 10000)['positive_waits'], 10000)

    def test_upstream_version_has_matching_vulnerable_constructs(self):
        source = (ROOT/'test/sim2real/vendor_idle_work/ros2_control_node_2.43.1.cpp').read_text()
        self.assertIn('std::chrono::system_clock', source)
        self.assertIn('next_iteration_time += period;', source)
        self.assertIn('std::this_thread::sleep_until(next_iteration_time);', source)
        self.assertNotIn('steady_clock', source)


if __name__ == '__main__':
    stage = ROOT/'docs/exp/2026-10-18/vendor_idle_rootcause'
    stage.mkdir(parents=True, exist_ok=True)
    result = {'execution_domain': 'DESKTOP_DRY_RUN', 'evidence_status': 'PASS (mechanism only)',
              'period_ns': PERIOD_NS, 'old_start_ns': OLD_NS, 'post_sync_now_ns': SYNC_NS,
              'normal': run_deadlines(OLD_NS, OLD_NS, 10000),
              'forward_step': run_deadlines(OLD_NS, SYNC_NS, 100000),
              'rebased': run_deadlines(SYNC_NS, SYNC_NS, 10000),
              'limitation': 'Virtual scheduler only; no proof that every vendor timeout stems from this loop.'}
    (stage/'clock_model.json').write_text(json.dumps(result, indent=2)+'\n')
    unittest.main(verbosity=2)
