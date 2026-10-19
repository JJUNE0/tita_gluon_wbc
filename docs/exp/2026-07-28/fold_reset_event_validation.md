# TITA Fold Reset Event Validation

- Execution Domain: `TRAINING_SIM`
- Policy Checkpoint SHA256: `N/A` (environment reset validation; no policy loaded)
- Evidence Status: `PASS` for environment construction and reset; `BLOCKED` for the subsequent policy step

## Change

Added `reset_joints_by_fold_offset`, which samples one interpolation factor per
environment along the TITA default-to-fold joint posture and then adds small
per-joint noise. The MOO TITA environment uses interpolation range `[0.0,
0.85]`, position noise `[-0.03, 0.03]` rad, and initial joint velocity
`[-0.1, 0.1]` rad/s.

## Evidence

Command:

```bash
PYTHONUNBUFFERED=1 PYTHONPATH=lab/ddt_lab \
  /home/cocel/isaac/env_isaaclab/bin/python test/test_headless_moo_env.py
```

Observed:

- Isaac Sim environment creation: PASS
- Event manager registered `reset_robot_joints`: PASS
- Reset of 16 CUDA environments: PASS
- Policy observation after reset: finite tensor with shape `(16, 33)`: PASS
- Subsequent step: BLOCKED by the expected unattached-discriminator guard in
  the environment-only test; this occurred after reset and is unrelated to the
  reset event.

Repository audit:

```text
./scripts/agent-check.sh
Python syntax: 279 passed, 0 failed
URDF XML: 9 passed
Final result: PASS
```

## Remaining Risk

The exact fold endpoint is not sampled yet. The interpolation maximum is 0.85
because the articulation soft joint limits clamp the official `leg_3=-2.70`
rad fold target. A full endpoint rollout requires a separate transition-limit
and root-pose validation.
