# TITA+GLUON 16-Environment EE Goal Visualization

- Execution Domain: `VALIDATION_SIM`
- Evidence Status: `PASS`
- Policy checkpoint: `model_6200.pt`
- Policy checkpoint SHA256: `8845511a6096a39f65507c7f8a7de49820c0302bee836e8ff1b2dd5aa8cc54b5`
- Training run: `2026-08-09_17-15-39_massless_sensor_rma_teacher_v2`

## Change

The curriculum-arm Play configuration now displays 16 robots. Each robot has one
magenta sphere at the final `gluon_2L6_4L3_link6` position of its active smooth
joint-trajectory segment. The marker stays fixed during the segment and changes
only when a new segment goal is selected. Training configurations keep debug
visualization disabled.

The marker position is computed from the complete combined-robot URDF chain from
TITA `base_link`, through the mount, to GLUON `link6`, then transformed by each
simulated robot's root pose into world coordinates.

## Evidence

Command:

```bash
/home/cocel/isaac/env_isaaclab/bin/python \
  test/test_tita_gluon_curriculum_arm_smoke.py \
  --headless --num-envs 4
```

Observed result:

```text
TITA_GLUON_CURRICULUM_ARM_SMOKE,domain=VALIDATION_SIM,status=PASS,...,
initial_link6_fk_error_m=3.37174782e-07,...
```

The test also verified that the Play configuration requests exactly 16
environments, enables the per-robot EE marker, preserves the eight-dimensional
TITA action contract, and exercises moving GLUON commands.

The first test attempt was `FAIL` because the new URDF fields were missing from
the curriculum action instance. The configuration was corrected before the
passing rerun.

## GUI Run

The GUI was launched with 16 environments and `model_6200.pt`. The process
initialized the `/Visuals/TitaGluon/segment_goal_link6` point-instancer without a
runtime exception and was left open for operator inspection.

## Future Training Logging

The curriculum RMA Teacher runner now defaults to:

- logger: `wandb`
- W&B project: `tita-gluon-moo-teacher`
- run name: `phase1-fixed-to-phase2-expanded-arm`

CLI arguments may still override the default run name for later phases. The
currently active run remains TensorBoard-only because its logger was selected at
process startup.

## Unresolved Risks

- The marker represents the URDF `link6` frame origin, not a future gripper/tool
  center point. A tool transform must be added after the gripper model is fixed.
- Isaac Sim emitted its existing Fabric point-instancer prototype warning for
  command markers and the new goal marker. No callback or simulation failure was
  observed, but visual appearance still requires operator confirmation in the GUI.
- W&B logging requires valid local W&B authentication/network access when the next
  training process starts.
