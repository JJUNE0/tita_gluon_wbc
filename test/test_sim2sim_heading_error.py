"""DESKTOP_DRY_RUN: sim2sim ``ObservationBuilder`` heading_error follows the training ``GyroHeadingError`` rule.

Uses the exported config of the 2026-10-19 heading run (35 observations) and synthetic states:
0 during the 1.0 s warmup, then (gyro_z - gyro_bias) * dt integration, output clip +-0.5 rad (x scale 2) with the
internal integral kept, 0 again as soon as a command leaves the zero band, and reset clears it.
Run with the cosim venv: ``python test/test_sim2sim_heading_error.py``.
"""

from pathlib import Path
import json
import sys

import numpy as np

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / 'sim2sim/sim2sim_ros2_jazzy'))
from sim2sim_ros2_jazzy.adapter import ObservationBuilder, ObsState  # noqa: E402

CONFIG = REPO / 'lab/ddt_lab/logs/flash_sac/tita_flash_sac_102630_755853/model_100000/sim2sim/actor/config.json'


def main() -> None:
    cfg = json.loads(CONFIG.read_text())
    builder = ObservationBuilder(cfg)
    layout = cfg['policy_interface']['observations']
    term = [t['name'] for t in layout].index('heading_error')
    index = sum(t['size'] for t in layout[:term])          # position in the observation vector
    assert term == len(layout) - 1 and index == 34 and cfg['policy']['obs_dim'] == 35
    q = np.asarray(cfg['robot']['default_joint_angles'], dtype=np.float64)

    def state(gz, command=(0., 0., 0.)):
        return ObsState(q, np.zeros(8), np.array([1., 0., 0., 0.]), np.array([0., 0., gz]),
                        np.asarray(command, dtype=np.float32), np.zeros(8, dtype=np.float32))

    dt, warmup = builder.dt, builder.heading_warmup
    assert abs(dt - 0.02) < 1e-12 and warmup == 50
    out = [builder.build(state(0.1))[index] for _ in range(warmup)]
    assert all(v == 0 for v in out), 'non-zero during warmup'
    for _ in range(10):
        value = builder.build(state(0.1))[index]
    assert abs(value - 2 * 0.1 * dt * 10) < 1e-6, value
    for _ in range(400):
        value = builder.build(state(0.1))[index]
    assert abs(value - 2 * 0.5) < 1e-6 and builder.heading > 0.5, (value, builder.heading)
    assert builder.build(state(0.1, (0., 0., 0.05)))[index] == 0 and builder.heading == 0.
    builder.gyro_bias = 0.1
    for _ in range(warmup + 10):
        value = builder.build(state(0.1))[index]
    assert abs(value) < 1e-9, value                       # bias exactly cancels the rate
    builder.gyro_bias = 0.
    builder.reset()
    assert builder.heading == 0. and builder.heading_hold == 0
    print('PASS: warmup 0, integration, clip with internal integral, command reset, bias subtraction, reset')


if __name__ == '__main__':
    main()
