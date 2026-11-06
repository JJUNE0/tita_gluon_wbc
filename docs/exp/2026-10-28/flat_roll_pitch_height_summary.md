# TITA flat roll/pitch/height command configuration

- Date: 2026-10-28
- Execution Domain: `TRAINING_SIM`, `VALIDATION_SIM`
- Policy Checkpoint SHA256 / ONNX Hash: `N/A` — configuration and nominal-model checks; no policy trained or loaded.
- Evidence Status: `PASS` for the tests below; learned command tracking is `NOT_TESTED`.
- Branch: `agent/codex/tita-walk`

## Behavior and scope

`TitaFlatRollPitchHeightEnvCfg` inherits `TitaFlatEnvCfg`. It adds a `base_pose`
command in `[roll_rad, pitch_rad, height_m]` order to both actor and critic
observations. Dimensions become 38/42, with the original eight actions. Height
is the `base_link` origin above the flat terrain/environment origin, not COM
height. Existing velocity commands, actions, resets, domain randomization,
terminations and physics settings are retained.

Initial command ranges:

| Command | Range | Maximum change per second |
| --- | --- | --- |
| Roll | -0.10 to +0.10 rad, approximately +/-5.7 degrees | 0.15 rad/s |
| Pitch | -0.15 to +0.15 rad, approximately +/-8.6 degrees | 0.15 rad/s |
| Height | 0.30 to 0.37 m | 0.02 m/s |

Targets resample every 6–8 seconds, with 20% nominal `[0, 0, 0.335]` targets.
Each reset starts the command at that nominal pose; the command then approaches
the sampled target with the stated rate limits. Observations and rewards use
the same current, rate-limited command. Observation evaluation does not advance
commands, and partial resets only reset selected command rows.

`base_height_l2` measures squared height error relative to the command.
`flat_orientation_l2` compares current projected-gravity XY to the gravity XY
implied by commanded roll and pitch: `[sin(pitch), -sin(roll)*cos(pitch)]`.
Yaw is unconstrained. The inherited upright factor is retained; the nominal
pose gives exactly the parent's two reward values.

`joint_mirror.weight = 0`, as requested by the user, to permit unequal leg
extension for roll. All other reward weights are inherited, including height
`-10` and orientation `-5`.

## Changed files

- `mj_lab/robots/tita/flat_env_roll_pitch_height_cfg.py`: command sampler, rate limits, observations, tracking costs, per-episode roll/pitch/height absolute-error metrics and subclass.
- `mj_lab/scripts/train.py`: `--task flat_roll_pitch_height` selection.
- `mj_lab/checkpoint.py`: preserve pose observation and command settings in checkpoint metadata.
- `mj_lab/scripts/play.py`: native playback `--pose-command ROLL PITCH HEIGHT`, with finite/range validation against saved bounds. Native reset and rate limits still apply.
- `test/test_mjlab_roll_pitch_height.py`: command distribution, rate limits, reset isolation, reward geometry, inherited settings, serialization and native CUDA rollout checks.
- `test/check_roll_pitch_height_feasibility.py`: 27-point nominal double-support IK and static torque/PD-envelope probe.
- This report and `flat_roll_pitch_height_*` evidence files in this directory.

The repository already contained extensive tracked changes and untracked
`mj_lab` files. Pre-edit source copies and Git status are saved as
`flat_roll_pitch_height_before_*`; task changes relative to those copies are
in `flat_roll_pitch_height_changes.diff`. No unrelated files were edited,
staged or reverted by this task. No commit or publication was requested.

## Executed checks and evidence

- `PASS`: command/reward/config CPU tests — **12 passed**, one native test deselected. Log: `flat_roll_pitch_height_unit_tests.log`.
- `PASS`: full new suite plus existing flat/walk regression suite — **36 passed, 8 skipped**, 12.36 seconds. The eight skips are existing gait/standing tests that do not apply to the corresponding task variant; the new native test ran. Log: `flat_roll_pitch_height_native_tests.log`.
- `PASS`: native CUDA environment creation, 38/42/8 dimensions, target resampling, partial reset isolation, observation purity, metrics registration and 100 finite zero-action control steps across four environments. This is a runtime smoke test, not trained balance or tracking evidence.
- `PASS`: 27/27 static combinations of roll `[-0.1, 0, 0.1]`, pitch `[-0.15, 0, 0.15]` and height `[0.30, 0.335, 0.37]`. Maximum kinematic residual `1.87e-13 m`; minimum base/knee ground clearance `0.05353 m`; maximum nominal leg torque `18.903 Nm` against 60 Nm limits; nominal PD target-envelope violation `0 rad`. Evidence: `flat_roll_pitch_height_feasibility.json` and `.log`.
- `PASS`: training and playback CLI help. Logs: `flat_roll_pitch_height_train_help.log`, `flat_roll_pitch_height_play_help.log`.
- `PASS`: required `./scripts/agent-check.sh` — 732 Python files parsed, 8 URDFs parsed, diff integrity and experiment directory checks passed. Log: `flat_roll_pitch_height_agent_check.log`.

The existing mass-randomization warning appears in the native test log: mass
and inertia randomization are separate inherited events. This task does not
change their behavior.

## Usage and remaining limits

Use the dedicated mjlab environment, from the repository root:

```bash
# TRAINING_SIM: new task; no training was started by this change.
source ~/venvs/tita_mjlab/bin/activate
python -m mj_lab.scripts.train --task flat_roll_pitch_height --headless --num_envs 1024 --steps 100000

# VALIDATION_SIM: after training, pin a pose target while stopped.
python -m mj_lab.scripts.play --checkpoint /path/to/model_STEP --command 0 0 0 --pose-command 0.10 -0.15 0.35
```

- `NOT_TESTED`: learner updates, converged tracking accuracy, full trained-policy playback and video. A fresh policy is needed because the original flat observations were 35/39, rather than 38/42.
- Static checks use the nominal model, vertical wheel support forces and nominal PD gains. They do not establish continuous-range feasibility, dynamic stability, disturbance recovery or behavior under friction/gain/COM randomization.
- Original velocity ranges remain +/-1.5 m/s and +/-3 rad/s. Simultaneous extreme velocity and pose commands are not dynamically validated.
- The inherited height coefficient gives only `-0.009` at 3 cm error with upright factor 1. Existing joint-deviation and motion costs can compete with posture changes. If height tracking remains weak, measure `height_error_m` and tune the height coefficient or posture regularizers in a separate training comparison.
- The existing external `sim2sim` adapter does not implement `base_pose` inputs. It rejects this checkpoint's pose command explicitly (`Unsupported generated command: base_pose`), as verified by the new test. This change supports native mjlab training/checkpoints/playback; external sim2sim and hardware behavior remain unimplemented and untested.
