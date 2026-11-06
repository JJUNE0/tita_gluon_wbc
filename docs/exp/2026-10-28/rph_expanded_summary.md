# Expanded TITA roll/pitch/height command ranges

- Date: 2026-10-28
- Execution Domain: `TRAINING_SIM`, `VALIDATION_SIM`
- Policy Checkpoint SHA256 / ONNX Hash: `N/A` — no trained policy loaded or training started.
- Evidence Status: `PASS` for configuration/runtime tests; `SUSPICIOUS` for simultaneous extreme pose feasibility; learned tracking is `NOT_TESTED`.
- Current branch: `agent/codex/tita-walk`

## Requested behavior

The user requested height 0.27–0.42 m, roll up to 30 degrees and pitch up to
15 degrees. The configuration now samples these ranges independently:

| Command | Range |
| --- | --- |
| Roll | +/-30 degrees, +/-0.5235988 rad |
| Pitch | +/-15 degrees, +/-0.2617994 rad |
| Base-link height above the plane | 0.27–0.42 m |

`joint_mirror.weight` remains zero. The nominal target remains `[0, 0, 0.335]`.
Rate limits remain 0.15 rad/s for roll/pitch and 0.02 m/s for height. Pose
resampling now takes 10–12 seconds: full roll reversal takes approximately
6.98 seconds and full height reversal takes 7.5 seconds, so the previous
6–8 second interval could replace a target before it was reached.

The projected-gravity tracking cost supports these angles. At the extreme
roll/pitch combination, `cos(30 deg)*cos(15 deg) = 0.8365`, so the inherited
upright factor still equals one at the commanded pose.

Changed files:

- `mj_lab/robots/tita/flat_env_roll_pitch_height_cfg.py`: expanded ranges and longer pose hold interval.
- `test/test_mjlab_roll_pitch_height.py`: exercise expanded command/reward endpoints and allow time to finish the longer height ramp.
- `test/check_roll_pitch_height_feasibility.py`: configurable grid, variable wheel spacing and separate hard-limit versus PD-equilibrium searches.
- This report and `rph_expanded_*` evidence files.

Pre-edit source copies/status are in `rph_expanded_before_*`. The task diff is
`rph_expanded_changes.diff`. Existing unrelated changes were preserved; no
staging, commit or publication was requested.

## Observed feasibility

The nominal grid uses roll `[-30, 0, 30]` degrees, pitch `[-15, 0, 15]` degrees
and height `[0.27, 0.335, 0.345, 0.42]` m: 36 samples.

The earlier probe fixed wheel Y positions at +/-0.2835 m. This is a sufficient
stance construction but is unnecessarily restrictive for large roll. The
expanded probe allows wheel spacing from 0.35 to 0.75 m, with the COM at least
2 cm inside the lateral wheel support interval. Vertical forces are chosen
from the COM projection. Hard joint limits, base/knee clearance and 60 Nm leg
torque limits are checked. Self-collision remains disabled as in training.

- `PASS`, **36/36 nominal static samples**, when searching physical hard joint
  limits without enforcing policy PD target limits. Log/data:
  `rph_expanded_hard_limits.log`, `rph_expanded_hard_limits.json`.
- `SUSPICIOUS`, **30/36 samples**, when enforcing current nominal PD target
  bounds: hip +/-0.7 rad, shoulder 0.3–1.3 rad, knee -2.2 to -0.8 rad.
  Actual joint positions are allowed to deflect under load; required targets
  are computed as `q + torque / kp`. Multi-start searches are used for
  unresolved samples. Maximum leg torque among feasible samples is 23.345 Nm.
  Log/data: `rph_expanded_pd_equilibrium.log`, `rph_expanded_pd_equilibrium.json`.

The six unresolved samples under current PD target limits are:

| Roll | Pitch | Height |
| --- | --- | --- |
| +/-30 deg | -15 deg | 0.27 m |
| +/-30 deg | -15 deg | 0.42 m |
| +/-30 deg | +15 deg | 0.42 m |

These searches retain geometric residuals of about 4.7–6.5 mm and nominal PD
target violations of 0.027–0.035 rad. A failed finite search is not a proof of
impossibility. Roll +/-30 degrees at zero pitch has feasible static solutions
at every tested height, including both 0.27 and 0.42 m. All tested pitch/height
combinations at zero roll also have feasible solutions under the PD limits.

Initial fixed-width and actual-position-envelope searches are retained in
`rph_expanded_fixed.*` and `rph_expanded_free.*` as intermediate diagnostics.
Their constrained actual-position assumption is stricter than a PD target
constraint and should not be used to declare a pose impossible.

## Executed validation

- `PASS`: `python -m pytest -q test/test_mjlab_roll_pitch_height.py` — **13 passed** in 7.66 seconds, including the native CUDA four-environment/100-step smoke test. Log: `rph_expanded_tests.log`.
- `PASS`: required `./scripts/agent-check.sh` — Python syntax, URDF parsing, diff integrity and experiment-directory checks. Log: `rph_expanded_agent_check.log`.
- `PASS`: final task diff reviewed against saved pre-edit copies; unrelated files not edited by this task.

Static checks use nominal mass, gains, vertical support forces and disabled
self-collision. They do not establish dynamic feasibility, friction margins,
robustness to randomization or learned tracking accuracy. Independent range
sampling includes the unresolved corner combinations; no automatic coupling
or clipping has been added. Training quality, reward tuning and any action
range expansion remain `NOT_TESTED`.
