# TITA sim2sim

The checked-in Teacher80k + residual10k / LPF60 recipe is in
[the publication guide](../docs/lpf60_residual.md). Historical run paths below
are examples and are not additional distributed checkpoints.

Execution Domain: `VALIDATION_SIM`. Run from the repository root.
Default policy selection: [`config/policies.json`](config/policies.json).
The public launchers are `sim2sim.launch.py` and `sim2sim.residual.torque.launch.py`.
The original base launcher is unchanged. Robot assets remain at their existing
paths because both training and playback reference them.

## Teacher playback

```bash
~/venvs/tita_mjlab/bin/python sim2sim/sim2sim_ros2_jazzy/launch/sim2sim.launch.py
```

With no checkpoint argument, the `teacher` entry in the selection JSON is used.
The residual launcher additionally reads `residual_torque`. Paths resolve relative
to that JSON, so changing a selection does not require editing Python. Use
`--config /path/to/policies.json` for another named selection. Existing `--ckpt`
and `--learned-residual` arguments remain one-run overrides. Direct Python launch
supports these defaults; the untouched base ROS launch still requires `ckpt:=...`.

For a shorter command after changing directory:

```bash
cd sim2sim/sim2sim_ros2_jazzy/launch
~/venvs/tita_mjlab/bin/python sim2sim.launch.py
~/venvs/tita_mjlab/bin/python sim2sim.residual.torque.launch.py
```

`--ckpt` also accepts other supported PPO `.pt`, FlashSAC `actor.pt`, or saved
model directories. Saved observation order, action scales, PD, gait/support
and normalization metadata determine playback. Export/cache validation remains
automatic. Keep each checkpoint's saved configuration next to its weights.

## Teacher + torque residual

```bash
# Current default: Teacher80k + hardware-tested torque48k.
~/venvs/tita_mjlab/bin/python sim2sim/sim2sim_ros2_jazzy/launch/sim2sim.residual.torque.launch.py

# Select a checkpoint folder, actor.pt, or a run root with latest.json.
~/venvs/tita_mjlab/bin/python sim2sim/sim2sim_ros2_jazzy/launch/sim2sim.residual.torque.launch.py \
  --learned-residual docs/exp/2026-11-08/residual_torque_sharednoisebias_rpfull_postpd8ms4096_b8096_s42_50k_v1
```

Selecting a training checkpoint registers weights and saved contracts under
`checkpoints/<framework>/task/<family>/<task>/<YYYYMMDD>/<step>/` in both domains.
See [checkpoint registry](checkpoints/README.md). Current config selects the
registered Teacher80k `policy.pt` and torque48k `residual.policy.pt`.

A run root resolves `latest.json` once at startup; it does not hot-swap policies.
The matching frozen Teacher hash is checked. This runtime supports the saved
250Hz torque residual, Teacher50Hz, PD/physics500Hz contract. Residual torque is
held across the two 2ms physics steps and added to PD before final effort clipping.
Residual is allowed only in RL at exact-zero current/target velocity commands,
with pose commands inside that checkpoint's trained ranges and the UI switch ON.
Its wheel displacement reference is fixed during a stop, without a velocity latch
or wheel-error input clip. Teacher retains its own saved observation semantics.

Experiment1 uses Teacher-shared noisy sensor samples during training. Playback
starts without injected noise/delay; the UI can add them. Action residual variants
remain archived. Saved torque LPF contracts are supported in the public runtime.

The selected 10k candidates have short config presets:

```bash
# Experiment2: noise/bias + LPF60, selected 10k.
~/venvs/tita_mjlab/bin/python sim2sim/sim2sim_ros2_jazzy/launch/sim2sim.residual.torque.launch.py \
  --config sim2sim/config/lpf60_10k.json --lpf 60

# Experiment1: noise/bias, selected 10k (no trained filter).
~/venvs/tita_mjlab/bin/python sim2sim/sim2sim_ros2_jazzy/launch/sim2sim.residual.torque.launch.py \
  --config sim2sim/config/noise_10k.json
```

`--lpf HZ` filters only residual torque at 500Hz: a one-pole matched filter,
`y += (1-exp(-2*pi*HZ/500))*(requested-y)`. Fresh PD torque is then added,
followed by final effort clipping and any UI torque delay. Teacher references
and PD torque are not filtered. The residual actor still observes its previous
requested torque, before filtering. Filter state clears on reset and gate loss;
the downstream torque-delay history retains its normal behavior.

Omitting `--lpf` restores the checkpoint's trained cutoff (60Hz for Experiment2,
disabled for Experiment1). `--lpf 0` bypasses it. Other finite cutoffs between 0
and 250Hz are playback overrides; their difference from training is recorded in
the run evidence. With ROS launch, use `lpf:=60` or `lpf:=0` (`auto` is default).

## Controls and perturbations

- Terminal: `1` prepare, wait for sit, `0` RL; `6` idle, `2` reset, `Ctrl+C` exit.
- Velocity: `w/s` forward/back, `a/d` yaw, `q/e` lateral when supported, `r` stop.
- Pose: `j/l` roll, `i/k` pitch, `u/o` height, `p` nominal pose.
  `--pose ROLL_DEG PITCH_DEG HEIGHT_M` also selects a saved-range target.
- Residual window: ON/OFF, mouse-attached mass (0–5kg), torso push (0–50N),
  ground friction, sensor Gaussian standard deviations, torque-delay min/max.
  Double-click a robot link in MuJoCo to attach/move mass; hold the push button
  to apply world +X force. Defaults are 2kg selection and 20N selection; neither
  is applied until requested.

UI torque lag is applied to the combined eight-joint torque after PD; it is
resampled per physics tick. Equal min/max values give a fixed lag. This differs
from training's episode-fixed 0/2/4/6/8ms sampling. After switching residual OFF,
commands already in the delay history can persist until its maximum lag expires.
UI changes are recorded with playback evidence.

Velocity caps come from `config/tita.yaml` intersected with the checkpoint's
saved ranges. Simulated keyboard/ROS velocity commands retain their existing
ramp; the latest hardware joystick mapping is immediate. Pose commands retain
their saved ramp in both domains.

## Finite verification

```bash
~/venvs/tita_mjlab/bin/python sim2sim/sim2sim_ros2_jazzy/launch/sim2sim.launch.py \
  --ckpt mj_lab/logs/flash_sac/tita_mjlab_112630_629104/model_80000 \
  --headless --steps 1000
~/venvs/tita_mjlab/bin/python sim2sim/sim2sim_ros2_jazzy/launch/sim2sim.residual.torque.launch.py \
  --headless --steps 1000
```

Headless mode prepares and enters RL automatically. `--prepare-only` validates
exports/contracts without opening the simulator. Evidence is written under
`docs/exp/YYYY-MM-DD/`. Finite execution establishes pipeline operation; it does
not establish long-term stability or hardware performance.

Historical action/BFM/read-only mirror launchers and their full residual runtime:
`test/legacy/sim2sim_20261108/`. Original files and move manifests are also in
`docs/exp/2026-11-08/backup/`; those are historical sources, not active entrypoints.
