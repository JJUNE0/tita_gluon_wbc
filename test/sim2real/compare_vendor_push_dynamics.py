"""VALIDATION_SIM: push responses of the calibrated sim + identified vendor controller vs real push events.

Plant hypotheses:
- base CoM x -2 cm (static calibration, docs/exp/2026-10-18/vendor_lqr_reproduction.md);
- thigh/knee/hip torque unit 0.65;
- wheel torque unit 0.9 / 1.0 / 1.15.

Pushes are 0.1 s horizontal base forces of +-60 / +-100 / +-150 N at 25 s (after the start-up transient). Each run reports peak speed, settle
time (|v| < 0.05 m/s), travel and peak pitch change, in the same terms as the real events
(``real_push_events.log``).
"""

from __future__ import annotations

import itertools
import json
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import sim_vendor_push as svp  # noqa: E402

OUT = svp.REPO / 'docs/exp/2026-10-18/vendor_lqr_reproduction/push_dynamics'


def job(args):
    height, s_wheel, force = args
    law = svp.identify(height)
    r = svp.run(law, dict(hip=.65, thigh=.65, knee=.65, wheel=s_wheel), 40., force, 25., -0.02)
    return dict(height=height, s_wheel=s_wheel, force=force, **{k: r.get(k) for k in (
        'fault', 'push_peak_speed', 'push_peak_pitch_deg', 'settle_s', 'push_travel_m', 'drift_cm_per_10s')})


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    grid = list(itertools.product(['mid', 'high'], [0.9, 1.0, 1.15], [60., -60., 100., -100., 150., -150.]))
    with ProcessPoolExecutor(6) as pool:
        rows = list(pool.map(job, grid))
    (OUT / 'results.json').write_text(json.dumps(rows, indent=2) + '\n')
    for r in rows:
        if r['fault'] or r['push_peak_speed'] is None:
            print(f"{r['height']:4s} wheel x{r['s_wheel']:.2f} push {r['force']:+5.0f} N: FAULT {r['fault']}")
            continue
        print(f"{r['height']:4s} wheel x{r['s_wheel']:.2f} push {r['force']:+5.0f} N: peak v {r['push_peak_speed']:.2f} m/s, "
              f"peak |dpitch| {r['push_peak_pitch_deg']:4.1f} deg, settle {r['settle_s']:.1f} s, travel {r['push_travel_m']:+.2f} m, "
              f"pre-push drift {r['drift_cm_per_10s']:+.2f} cm/10s")


if __name__ == '__main__':
    main()
