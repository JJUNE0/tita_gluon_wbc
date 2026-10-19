# Known issue: `reference_transform_up` handoff instability

**Status: unresolved at the code level.** This is a structural limitation, not a
tuning problem — do not spend time re-tuning `stand_jpos`/`stand_timer` expecting to
"fix" it; read this file first.

## Symptom

During the `reference_transform_up` FSM state (and `reference_stand_hold`), the
robot can visibly tilt/pitch before the RL policy takes over. Multiple pose/timing
tuning attempts were made across checkpoints in this line of work (factor=0.5 pose,
then factor=0.1 pose, `stand_timer` swept 2.0 → 4.0 → 7.0s) — none fully eliminated
the tilt.

## Root cause

`reference_transform_up`/`reference_stand_hold` run a purely **open-loop, high-gain
reference PD hold with NO active wheel balance**. The config key
`use_imu_wheel_balance` under `reference_transform_up:` is a **dead/unused key** —
grep confirms no code in `mujoco_policy_node.py` ever reads it. So whatever
`stand_jpos` is configured, if it isn't a naturally CoM-balanced static pose, the
robot will slowly tip regardless of `stand_timer` length. This was validated
empirically across several pose/timer combinations (see prior config comment blocks,
e.g. `tita_moo_stand_drive_20260806_8000_heightnorm_v2.yaml`,
`tita_moo_stand_drive_20260807_4999_heightnorm_v3.yaml`).

## Current mitigation (not a fix)

The user explicitly instructed reverting `reference_transform_up.stand_jpos` back to
the original ad-hoc pose:
```
[-0.05, 0.9, -2.6, 0.0, 0.05, 0.9, -2.6, 0.0]
```
(as opposed to poses data-derived from each checkpoint's own
`reset_joints_by_fold_offset` sampling range, e.g. a "factor=0.1" interpolated pose).
This pose sits off the training reset's sampled line for the 08-06/08-07/08-08
checkpoints (`interpolation_range=[0.0, 0.1]`), so expect the documented
OOD-handoff tilt behavior. **Do not silently "correct" this back to a
data-derived pose in a new config — it was an explicit, standing user instruction,
not a placeholder.** If the user wants it changed again, they will say so.

## If picking this up as a real fix (not requested yet)

The actual fix would require either (a) adding active balance control (wheel
velocity servo driven by pitch error, similar to `transform_up`'s
`use_wheel_balance: true` path, which DOES read and act on `pitch_kp`/`pitch_kd`/
`wheel_vel_limit`) to the `reference_transform_up` state, or (b) deriving
`stand_jpos` from each checkpoint's own actual CoM-balanced standing pose rather than
an ad-hoc value. Neither has been attempted — this is scoped out of every task so
far in this line of work.
