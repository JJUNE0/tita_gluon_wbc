# DDT-Velocity-Flat-Tita-My-v0 — training + sim-to-sim drift check

## Training

- **Execution Domain**: `TRAINING_SIM`
- **Task**: `DDT-Velocity-Flat-Tita-My-v0` (rsl_rl track, `TitaFlatEstimatorPPORunnerCfg` / `ActorCriticWithEstimator`)
- **Run log dirs**:
  - `lab/ddt_lab/logs/rsl_rl/tita_flat_rslrl_estimator/2026-07-24_17-24-04/` — iter 0→3800, no wandb (pre-dates wandb-default config change)
  - `lab/ddt_lab/logs/rsl_rl/tita_flat_rslrl_estimator/2026-07-24_18-24-21/` — resumed from `model_3800.pt`, iter 3800→6400 (target 8800, stopped early by operator request), wandb-tracked
- **wandb**: project `tita_gluon_wbc`, run `2026-07-24_18-24-21` (id `cofg1inc`) — https://wandb.ai/bjy6614-postech/tita_gluon_wbc/runs/cofg1inc
- **Checkpoint selection**: NOT the final/latest checkpoint. Compared `Train/mean_reward` across all saved (every-100-iter) checkpoints in both log dirs; best was **iter 5800 (mean_reward 49.16)**, vs 49.08 @ 6200 and 48.75 @ 6400 (final).
- **Selected checkpoint**: `lab/ddt_lab/logs/rsl_rl/tita_flat_rslrl_estimator/2026-07-24_18-24-21/model_5800.pt`
  - SHA256: `84561096eb9c1619964b4b2710819bbb70c7ecbbb5cb891c9961fed6d5ed1dfc`
- **Exported ONNX**: `tita_gluon_ws/deploy/tita/policy_my41_5800.onnx`
  - SHA256: `13ab688dbadec802c0874227dd222a4ee2f48889297b147d2b656aa344ff358b`
  - Interface: `nn_input0 [1,33]` → `nn_output [1,8]` (no history input; matches `tita_my40_3400.yaml`-style single-frame configs)
- **Evidence Status**: `PASS` (training completed the requested range without crash; checkpoint/ONNX export verified to load and run)

## Validation 1 — `eval_behavior.py` (Isaac Lab own physics)

- **Execution Domain**: `VALIDATION_SIM`
- **Command**: `scripts/rsl_rl/eval_behavior.py --task=DDT-Velocity-Flat-Tita-My-Play-v0 --checkpoint <model_5800.pt> --num_envs 32 --out test/eval_my_model_5800.csv --headless`
- **Zero-command hold (3.0s)**: drift ≈ **+0.16 m** (mean vx ≈ +0.054 m/s, forward drift)
- **Decel shake** (0.8 m/s → 0 cut, 1.5s window): peak tilt 0.093 rad (final 0.091), peak ang_vel_xy 0.162 rad/s (final 0.052 rad/s) — decays, no divergence
- **Evidence Status**: `PASS`

## Validation 2 — `probe_zero_command_drift_mujoco.py` (MuJoCo, ground-truth base position)

- **Execution Domain**: `DESKTOP_DRY_RUN`
- **Config**: `sim2sim/cosim_ros2_jazzy/config/tita_my41_5800.yaml` (cloned from `tita_my40_3400.yaml`, policy path swapped)
- **Command**: `probe_zero_command_drift_mujoco.py --config config/tita_my41_5800.yaml --settle_s 1.0 --hold_s 5.0` (env: `conda activate cosim`)
- **Zero-command hold (5.0s)**: drift = **0.445 m** (mean vx-equiv 0.089 m/s)
- **Base height**: start 0.375 → min 0.309 → final 0.366 m (transient dip, recovers)
- **Evidence Status**: `PASS` (ran to completion), but see gap below

## Gap observed (sim-to-sim, My41@5800)

Zero-command drift is worse in MuJoCo than in Isaac Lab's own physics: **0.089 m/s (MuJoCo) vs 0.054 m/s (Isaac)** — roughly 1.6x, plus a transient base-height dip in MuJoCo not seen in the Isaac-side metrics. Not yet root-caused. Candidates to check next: actuator/PD gain mismatch between the two engines' interpretations of the exported action interface, MJCF corrected-inertials assumptions, or the estimator's learned base_lin_vel diverging under MuJoCo's contact model. No sim-to-real or hardware step has been taken on this checkpoint.

---

## Training (round 2) — reward retune, My42@1800

- **Execution Domain**: `TRAINING_SIM`
- **Reward changes vs. the run above** (`my_flat_env_cfg.py::MyTitaFlatEnvCfg`):
  - `ang_vel_xy_l2.weight`: -0.01 → **-0.05** (stricter xy angular-velocity penalty)
  - `action_rate_l2.weight`: -0.05 → **-0.01** (looser action-smoothness penalty)
  - `dof_acc_l2.weight`: explicit `-2.5e-6` override removed → falls back to base-class default **-2.5e-7** (looser joint-accel penalty)
  - `track_ang_vel_z_exp.weight` (1.0) and `zero_command_position_drift.sharpness` (8.0): unchanged
  - `rough_env_cfg.py::RewardsCfg.base_height_l2.target_height`: 0.3 → **0.335** (base class shared with My-v0, not overridden there)
- **max_iterations**: changed from a per-run default of 5000 to a **fixed 2000** (`BaseRslRlPpoRunnerCfg.max_iterations = 2000`), per operator instruction going forward.
- **Run**: fresh (not resumed) — `lab/ddt_lab/logs/rsl_rl/tita_flat_rslrl_estimator/2026-07-24_19-16-43/`, iter 0→1999, wandb-tracked.
- **wandb**: project `tita_gluon_wbc`, run `2026-07-24_19-16-43` (id `4ji99dyl`) — https://wandb.ai/bjy6614-postech/tita_gluon_wbc/runs/4ji99dyl
- **Checkpoint selection**: best `Train/mean_reward` among saved (every-100-iter) checkpoints was **iter 1800 (49.94)**, vs 49.22 @ 1999 (final).
- **Selected checkpoint**: `lab/ddt_lab/logs/rsl_rl/tita_flat_rslrl_estimator/2026-07-24_19-16-43/model_1800.pt`
  - SHA256: `30b0c28a0d8af084f5455527fc5fb990ff9737e3408962b362dc90cc1e8721ba`
- **Exported ONNX**: `tita_gluon_ws/deploy/tita/policy_my42_1800.onnx`
  - SHA256: `41d4d5e8f3f7a934675dc3287aff74c027168d9670d8c813e2c798441ab0876c`
- **Evidence Status**: `PASS`

### Validation 1 (round 2) — `eval_behavior.py`

- **Execution Domain**: `VALIDATION_SIM`
- Zero-command hold (3.0s): drift ≈ **+0.185 m** (mean vx ≈ +0.062 m/s) — slightly worse than My41@5800 (+0.16 m)
- Decel shake: peak tilt **0.062 rad** (final 0.057), peak ang_vel_xy **0.121 rad/s** (final 0.109) — better than My41@5800 (peak tilt 0.093, peak ang_vel 0.162)
- **Evidence Status**: `PASS`

### Validation 2 (round 2) — `probe_zero_command_drift_mujoco.py`

- **Execution Domain**: `DESKTOP_DRY_RUN`
- **Config**: `sim2sim/cosim_ros2_jazzy/config/tita_my42_1800.yaml`
- Zero-command hold (5.0s): drift = **0.349 m** (mean vx-equiv 0.070 m/s) — improved vs My41@5800 (0.445 m / 0.089 m/s)
- Base height: start 0.353 → min 0.339 → final 0.346 m (only ~1.4cm dip, much more stable than My41@5800's ~6.6cm dip)
- **Evidence Status**: `PASS`

### Round 2 summary

The reward retune (looser action-rate/dof-accel penalty, stricter ang-vel-xy penalty, higher base-height target) improved MuJoCo-side stability noticeably (drift 0.089→0.070 m/s, base-height dip 6.6cm→1.4cm) and improved Isaac-side decel shake, at the cost of a small regression in Isaac-side zero-command drift (0.054→0.062 m/s). The Isaac-vs-MuJoCo sim-to-sim drift gap persists (0.062 vs 0.070 m/s this round) but is much smaller in absolute terms than round 1's gap (0.054 vs 0.089 m/s).

---

## Training (round 3) — `zero_command_wheel_action` reward, My43@2700

- **Execution Domain**: `TRAINING_SIM`
- **New reward term** (`mdp/rewards.py::zero_command_wheel_action_penalty`, registered in `my_flat_env_cfg.py` as `self.rewards.zero_command_wheel_action`): penalizes `|wheel_action|**4` (quartic, joints `.*_leg_4`) whenever the velocity command is exactly zero (`command_threshold=0.0`, `<=` match — deliberately not a dead-zone, so small nonzero commands are never suppressed). `weight=-0.05`. Targets the raw policy output for the wheel actuators directly, ahead of `wheel_vel_penalty`/`zero_command_position_drift` which only react to the resulting measured velocity/drift.
- **max_iterations**: `3000` (CLI override via `--max_iterations 3000`; the config-level fixed default from round 2 stays at `2000`).
- **Run**: fresh (not resumed) — `lab/ddt_lab/logs/rsl_rl/tita_flat_rslrl_estimator/2026-07-25_15-04-17/`, iter 0→2999, wandb-tracked.
- **wandb**: project `tita_gluon_wbc`, run `2026-07-25_15-04-17` (id `mfgntj2u`) — https://wandb.ai/bjy6614-postech/tita_gluon_wbc/runs/mfgntj2u
- **Interruption note**: an unattended-upgrades NVIDIA driver bump (580.159.03→580.173.02) mid-session broke CUDA (NVML driver/library version mismatch) and killed one training attempt before a reboot; this run is the post-reboot retry, unaffected.
- **Checkpoint selection**: best `Train/mean_reward` among saved (every-100-iter) checkpoints was **iter 2700 (50.18)** — also the best across all three rounds — vs 48.17 @ 2999 (final).
- **Selected checkpoint**: `lab/ddt_lab/logs/rsl_rl/tita_flat_rslrl_estimator/2026-07-25_15-04-17/model_2700.pt`
  - SHA256: `3766e05c683d6f2565bbeb2c21f500f872b243ffe39fb48b40fd3ae7ff608ef8`
- **Exported ONNX**: `tita_gluon_ws/deploy/tita/policy_my43_2700.onnx`
  - SHA256: `ecb0fd3ec56eb9aed5349250e9de11040156f59e3a98c54ae83dadde672a7705`
- **Evidence Status**: `PASS`

### Validation 1 (round 3) — `eval_behavior.py`

- **Execution Domain**: `VALIDATION_SIM`
- Zero-command hold (3.0s): drift ≈ **+0.044 m** (mean vx ≈ +0.015 m/s) — best of all three rounds by a wide margin (My41 +0.16 m, My42 +0.185 m)
- Decel shake: peak tilt 0.069 rad (final 0.057), peak ang_vel_xy **0.255 rad/s** (final 0.071) — peak ang_vel regressed vs My42 (0.121) but final value still decays cleanly, no divergence
- **Evidence Status**: `PASS`

### Validation 2 (round 3) — `probe_zero_command_drift_mujoco.py`

- **Execution Domain**: `DESKTOP_DRY_RUN`
- **Config**: `sim2sim/cosim_ros2_jazzy/config/tita_my43_2700.yaml`
- Zero-command hold (5.0s): drift = **0.022 m** (mean vx-equiv 0.0044 m/s) — ~20x better than My41 (0.445 m), ~16x better than My42 (0.349 m)
- Base height: start 0.319 → min 0.316 → final 0.316 m (~0.2cm dip, essentially flat)
- **Evidence Status**: `PASS`

### Round 3 summary

Adding a direct, immediate penalty on raw wheel-joint action magnitude (rather than only penalizing its downstream consequences) all but eliminated zero-command standstill drift in both Isaac and MuJoCo, and closed the Isaac-vs-MuJoCo sim-to-sim gap that persisted through rounds 1-2. Trade-off: peak angular-velocity shake during hard deceleration got worse (0.121→0.255 rad/s peak in Isaac), though it still decays to a small final value with no sign of divergence. Worth watching in a future decel-focused validation pass, but not treated as a regression severe enough to block using this checkpoint.

---

## Training (round 4) — user manual reward edits on top of My43, My44@2500

- **Execution Domain**: `TRAINING_SIM`
- **Changes vs. My43** (`my_flat_env_cfg.py`, edited directly by the operator, not by the agent):
  - `self.events.base_external_force_torque = None` — disabled the base external-force/torque domain-randomization event
  - `joint_deviation_shoulder.weight`: -0.5 → -1.0
  - `zero_command_wheel_action.weight`: -0.05 → -0.1 (doubled)
- **max_iterations**: `3000` (same as round 3, CLI override).
- **Run**: fresh (not resumed) — `lab/ddt_lab/logs/rsl_rl/tita_flat_rslrl_estimator/2026-07-25_16-21-47/`, iter 0→2999, wandb-tracked.
- **wandb**: project `tita_gluon_wbc`, run `2026-07-25_16-21-47` (id `kqb06uod`) — https://wandb.ai/bjy6614-postech/tita_gluon_wbc/runs/kqb06uod
- **Checkpoint selection**: best `Train/mean_reward` among saved checkpoints was **iter 2500 (53.58)** — the highest raw reward of any round so far — vs 53.20 @ 2999 (final).
- **Selected checkpoint**: `lab/ddt_lab/logs/rsl_rl/tita_flat_rslrl_estimator/2026-07-25_16-21-47/model_2500.pt`
  - SHA256: `eda9cb740012ad433373038b7ad6fb3438b2669de0f7e047d2666826504f043d`
- **Exported ONNX**: `tita_gluon_ws/deploy/tita/policy_my44_2500.onnx`
  - SHA256: `794050ca80524802189138e0e73fd028e119a3d2a8c4329cad6610494a5bb5e3`
- **Evidence Status**: `PASS` (ran to completion), but see regression below

### Validation 1 (round 4) — `eval_behavior.py`

- **Execution Domain**: `VALIDATION_SIM`
- Zero-command hold (3.0s): drift ≈ **+0.153 m** (mean vx ≈ +0.051 m/s) — regressed ~3.5x vs My43 (+0.044 m), back near My41/My42 levels
- Decel shake: peak tilt 0.086 rad (final 0.065), peak ang_vel_xy 0.265 rad/s (final **0.233 rad/s**) — final value regressed heavily vs My43 (final 0.071 rad/s); shake no longer decays cleanly by end of window
- **Evidence Status**: `PASS`, but a clear behavioral regression despite the highest `Train/mean_reward` of any round

### Validation 2 (round 4) — `probe_zero_command_drift_mujoco.py`

- **Execution Domain**: `DESKTOP_DRY_RUN`
- **Config**: `sim2sim/cosim_ros2_jazzy/config/tita_my44_2500.yaml`
- Zero-command hold (5.0s): drift = **0.181 m** (mean vx-equiv 0.036 m/s) — regressed ~8x vs My43 (0.022 m)
- Base height: start 0.373 → min 0.370 → final 0.370 m (small dip, not itself concerning)
- **Evidence Status**: `PASS`, same regression pattern as Validation 1

### Round 4 summary

**Reward-metric/behavior divergence**: this checkpoint has the highest `Train/mean_reward` (53.58) of all four rounds, yet regresses sharply on every zero-command stability metric relative to My43 — Isaac drift 0.044→0.153 m, Isaac decel final ang_vel 0.071→0.233 rad/s (no longer cleanly decaying), MuJoCo drift 0.022→0.181 m (~8x). Not root-caused, but the most likely candidates are the three simultaneous manual edits: disabling `base_external_force_torque` domain randomization (less robustness pressure during training) and doubling `zero_command_wheel_action`'s weight (which may have pushed the policy toward a different, higher-total-reward equilibrium that trades wheel-action stillness for something else, rather than genuinely more stable standstill behavior) are the two most likely levers. **My43@2700 remains the better checkpoint for deployment** despite My44's higher raw reward — this round is a reminder that `Train/mean_reward` alone is not sufficient for checkpoint selection when multiple reward terms are retuned simultaneously; the Isaac/MuJoCo behavioral validation is what actually caught this.
