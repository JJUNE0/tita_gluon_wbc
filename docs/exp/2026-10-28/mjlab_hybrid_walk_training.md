# mjlab hybrid standing/walking experiment

Execution Domains: TRAINING_SIM, VALIDATION_SIM

Evidence Status: PASS for implementation checks and live learner launch.
Completion and quality at 100,000 vector steps are NOT_TESTED while running.

Policy Checkpoint SHA256 (validation actor, model_60):
`d0bbae97577c5e953767cf9c792d1b38524d930b74c87ed776693783ecdb5665`

Full-run checkpoint hash: pending the first 5,000-step checkpoint; native
`ddt.json` files will record the actual actor/config/source hashes.

Branch: `agent/codex/tita-walk`. No commit, push, PR or hardware operation.

## Requested behavior

This changes mjlab walk only. The flat environment definition and robot PD
configuration, FlashSAC learner, Isaac sources and sim2sim sources are preserved.
314 protected source files were hashed before and after the change; all match.

| Mode | Gait | Wheel velocity policy targets | Hip deviation | Shoulder deviation |
|---|---|---|---:|---:|
| Standing / zero-command deadband | Off | Driving scale 20, with the existing FlashSAC gains | −1.0 | −0.5 |
| Moving / gait enabled | On | Zero | −0.1 | −0.1 |

The gait uses the existing emitted-command thresholds: planar magnitude >0.02
m/s or yaw magnitude >0.03 rad/s after the existing one-second settling window.
Within that deadband gait time does not advance. No noisy measured velocity is
used to choose the mode. vx/vy command ranges remain ±0.5 m/s, yaw 0, ramp
0.3/s. Mode switching is binary in this experiment.

`GaitGatedWheelVelocityAction` gates the processed target separately for every
environment, after normal scaling/offset/clipping. Raw action and previous-action
observations remain intact. Motor gains, torque caps and reset-sampled command
delay remain unchanged. The delayed actuator can briefly retain its previous
target during a mode transition; joint velocity is never overwritten or locked.

The existing gait-enabled observation indicates mode. Actor/critic dimensions
remain 39/43, actions remain 8. Gait contact/clearance rewards are zero while
standing. Deviation terms keep the flat manager weights and multiply moving
values by 0.1 for hip and 0.2 for shoulder, giving the requested effective −0.1
for both. Other selected walk rewards and termination conditions are retained.

## Files and compatibility

- `mj_lab/robots/tita/mdp.py`: mode-gated velocity action, mode-dependent
  deviation scaling, explicit gait thresholds and enabled-only gait rewards.
- `mj_lab/robots/tita/walk_env_cfg.py`: compose the hybrid environment using
  inherited flat wheel scales/deviation weights and the requested moving weights.
- `mj_lab/checkpoint.py`: save the real custom action type and gating metadata.
- `mj_lab/README.md`: hybrid configuration and native playback instructions.
- `test/test_mjlab_tita.py`: updated hybrid contracts and mixed-batch checks.

Old saved fixed-wheel environments keep their old action classes, step-in-place
setting and deviation weights when resumed. Old native checkpoint playback was
executed successfully. A new hybrid checkpoint needs the native mjlab player
for now: the unchanged sim2sim loader explicitly rejects the custom gated-action
type instead of applying the wrong wheel behavior. That restriction follows the
requested MJLab-only scope.

## Executed checks

Observed Metrics / Behavior / Log Summary:

- PASS: native CUDA suite: 20 passed, 5 inapplicable cases skipped.
  `mjlab_hybrid_native_checks.log`.
- PASS: mixed environments apply wheel targets [40,0,40,0], then [0,−40,0,−40]
  after mode reversal; raw actions remain unchanged.
- PASS: physical joint deviations produce flat standing penalties and exactly
  −0.1 effective hip/shoulder moving weights. Gait rewards are zero in standing.
- PASS: zero-command gait off; moving gait on after settling/ramp; partial reset
  isolation, command diagnostics, PD/delay bounds and terminal snapshots.
- PASS: FlashSAC validation: 60 vector steps, 55 finite updates, checkpoint save.
  `mjlab_hybrid_learner_check.log` and `mjlab_hybrid_validation_record.json`.
- PASS: saved hybrid checkpoint native playback and 80-frame vx/vy video.
  `mjlab_hybrid_native_preview.json` / `.mp4`.
- PASS: old walk 100k native checkpoint playback.
  `mjlab_hybrid_legacy_walk_check.log`.
- PASS: protected-source hashes; no Isaac/sim2sim/flat/robot/learner changes.
  `mjlab_hybrid_protected_source_hashes.json`.
- PASS: `./scripts/agent-check.sh`; `mjlab_hybrid_agent_check.log`.
- PASS: live training verified at step 1,100 with 2,002 learner updates and
  finite logs. Full-run completion is pending.

## Running experiment

Started from scratch, 1,024 environments, seed 42, CUDA 0, target 100,000 vector
steps. Existing FlashSAC defaults are retained. Checkpoints every 5,000 steps;
online W&B and 500-frame CMD/ACT vx/vy videos every 10,000 steps.

- Run: `tita_mjlab_085110_097268`
- Run name: `tita_mjlab_hybrid_zero_wheel_hip01_shoulder01_s42`
- PID at verification: 994292
- Detached tmux: `mjlab_hybrid_walk_20261028_085106`
- Weights/configs: `mj_lab/logs/flash_sac/tita_mjlab_085110_097268/`
- Console: `docs/exp/2026-10-28/mjlab_hybrid_walk_training_console.log`
- Metrics: `docs/exp/2026-10-28/tita_mjlab_085110_097268_metrics.jsonl`
- Launch/source provenance: `mjlab_hybrid_walk_training_launch.json`
- [W&B run](https://forge.coreweave.com/wandb/bjy6614-postech/tita_flat_flash_sac/runs/8hv13hz7)

Short native checks establish implementation and logging operation. The wheel
balance behavior is newly learned; neither successful gait quality nor reliable
mode transitions have yet been demonstrated by a fully trained hybrid policy.
