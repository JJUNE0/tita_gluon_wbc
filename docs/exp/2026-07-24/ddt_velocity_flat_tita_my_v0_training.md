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

## Gap observed (sim-to-sim)

Zero-command drift is worse in MuJoCo than in Isaac Lab's own physics: **0.089 m/s (MuJoCo) vs 0.054 m/s (Isaac)** — roughly 1.6x, plus a transient base-height dip in MuJoCo not seen in the Isaac-side metrics. Not yet root-caused. Candidates to check next: actuator/PD gain mismatch between the two engines' interpretations of the exported action interface, MJCF corrected-inertials assumptions, or the estimator's learned base_lin_vel diverging under MuJoCo's contact model. No sim-to-real or hardware step has been taken on this checkpoint.
