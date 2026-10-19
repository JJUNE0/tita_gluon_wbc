"""VALIDATION_SIM: calibrate MuJoCo static parameters so the identified vendor stand controller stands like the robot.

Same controller as ``sim_vendor_push.py`` (identified from the 19:27 push captures). The grid covers base CoM x
shift, thigh/knee torque-unit scale and wheel torque-unit scale. The target is the real quiet stand of the same
height: zero drift, pitch and thigh angle. Fitted on ``mid``; ``high`` is a cross-check of the same parameters.
Sim-only. A good match is necessary but not sufficient evidence of a correct plant model.
"""

from __future__ import annotations

import argparse
import itertools
import json
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
import sys

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import sim_vendor_push as svp  # noqa: E402


def job(args):
    height, com_dx, s_thigh, s_knee, s_wheel = args
    law = svp.identify(height)
    r = svp.run(law, dict(hip=s_knee, thigh=s_thigh, knee=s_knee, wheel=s_wheel), 20., 0., 30., com_dx)
    real = law['real_quiet']
    return dict(height=height, com_dx=com_dx, s_thigh=s_thigh, s_knee=s_knee, s_wheel=s_wheel, fault=r['fault'],
                pitch_deg=r['pitch_deg'], thigh=r['thigh'], knee=r['knee'], drift_cm_per_10s=r['drift_cm_per_10s'],
                real_pitch_deg=real['pitch_deg'], real_thigh=real['thigh'], real_knee=law['posture'][2])


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--output', type=Path, default=svp.REPO / 'docs/exp/2026-10-18/vendor_lqr_reproduction/calibration')
    parser.add_argument('--heights', nargs='+', default=['mid', 'high'])
    parser.add_argument('--workers', type=int, default=6)
    args = parser.parse_args()
    out = args.output.resolve()
    assert out.is_relative_to(svp.REPO / 'docs/exp')
    out.mkdir(parents=True, exist_ok=True)
    grid = list(itertools.product(args.heights, [-0.03, -0.02, -0.01, 0., 0.01, 0.02], [0.65, 1.0], [0.65], [0.9, 1.0, 1.15]))
    with ProcessPoolExecutor(args.workers) as pool:
        rows = list(pool.map(job, grid))
    (out / 'results.json').write_text(json.dumps(rows, indent=2) + '\n')
    for r in sorted(rows, key=lambda r: (r['height'], r['s_thigh'], r['s_wheel'], r['com_dx'])):
        print(f"{r['height']:4s} com {r['com_dx']*100:+4.0f} cm thigh x{r['s_thigh']:.2f} wheel x{r['s_wheel']:.2f} | "
              f"drift {r['drift_cm_per_10s']:+7.2f} cm/10s pitch {r['pitch_deg']:5.2f} (real {r['real_pitch_deg']:.2f}) "
              f"thigh {r['thigh']:.3f} (real {r['real_thigh']:.3f}) knee {r['knee']:.3f} (real {r['real_knee']:.3f}) "
              f"{'FALL' if r['fault'] else ''}")


if __name__ == '__main__':
    main()
