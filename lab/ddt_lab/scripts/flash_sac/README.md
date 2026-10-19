# TITA FlashSAC

Execution Domain: `TRAINING_SIM` for training; `VALIDATION_SIM` for playback.

This port defaults to the selected `DDT-Velocity-Flat-Tita-v0` task from
`flat_env_cfg.py`: 35 policy observations, sphere wheels, no leg MA2 filter,
and zero heading warmup (the headw0 50k/65k training configuration).
It vendors the PyTorch FlashSAC learner from
`wolf-quadruped/rl/FlashSAC`; the Wolf terrain/curriculum adapters are replaced
with a native TITA adapter. The source fork, local patches, file hashes and MIT
license are recorded under `vendor/`.

Historical `*-My-*` experiment IDs retain their original settings. The deleted
`my_flat_env_cfg` module is aliased to `real2sim/base_env_cfg.py` for old saved
config pickles; it does not select the new flat task.

TITA training defaults live in
`ddt_lab/tasks/manager_based/locomotion/robots/tita/agents/flash_sac_cfg.py`.
`TitaFlatFlashSACRunnerCfg` manages rollout/replay/CLI defaults and estimator
handling; its `agent` (`FlashSACAlgorithmCfg`) manages network sizes, learning
rates, reward normalization, discount and temperature settings. The flat train
and Play tasks register this class as `flash_sac_cfg_entry_point`. CLI options
override runner defaults; resume restores the checkpoint's model/schedule and
action gains.

Activate the existing Isaac Lab environment. Its installed `ddt_lab` must point
at this repository; the scripts also add this repository's extension to
`sys.path`. FlashSAC needs PyTorch, NumPy and Gymnasium, which Isaac Lab already
uses. TensorBoard is needed for the default logger; `--logger console` omits it.
W&B is optional and selected with `--logger wandb`; install `wandb` in the same
Python environment if it is missing. No external FlashSAC checkout, Hydra
composition or JAX installation is needed.

```bash
source /home/cocel/isaac/env_isaaclab/bin/activate
cd /home/cocel/Desktop/Research/tita_gluon_wbc/lab/ddt_lab

# Short integration run: 4 envs, 8 vector steps, replay warmup and real updates.
python scripts/flash_sac/train.py \
  --task DDT-Velocity-Flat-Tita-v0 \
  --num_envs 4 --steps 8 --buffer_size 128 --min_buffer 8 \
  --batch_size 8 --save_every 8 --log_every 1 \
  --logger console --headless

# Full training: --steps counts vector steps, not PPO iterations.
python scripts/flash_sac/train.py \
  --task DDT-Velocity-Flat-Tita-v0 \
  --num_envs 1024 --steps 100000 --headless

# W&B logging. Authenticate with `wandb login` if this environment needs it.
python scripts/flash_sac/train.py \
  --task DDT-Velocity-Flat-Tita-v0 \
  --num_envs 4096 --steps 100000 --device cuda:0 --headless \
  --logger wandb --wandb_project tita_flat_flash_sac
```

`wandb_project`, `wandb_entity`, `run_name`, `wandb_mode` and `wandb_run_id` are
configurable in `agents/flash_sac_cfg.py` or through matching CLI options.
The default logger remains TensorBoard; W&B's default project is
`tita_flat_flash_sac`. W&B records the resolved agent config, reward weights,
observation dimensions and the same metrics as the local JSONL stream: rewards,
episode statistics, learner losses and scalar Isaac environment metrics.
Each learner metric keeps its latest value across critic-only updates, so
periodic actor losses remain available with the default two updates per step.
Charts use the `step` field (vector environment steps) as their axis.

Use `--wandb_mode offline` for local-only W&B recording. When no mode is passed,
the SDK honors `WANDB_MODE`. W&B files and run-ID metadata are stored beneath
`docs/exp/YYYY-MM-DD/`; model checkpoints remain local in `logs/flash_sac/`.
Weights are not automatically uploaded. To continue an online W&B run during
model resume, pass `--logger wandb --wandb_run_id <id>` alongside `--resume`;
omitting the ID creates a new W&B run. The SDK ignores run resume in offline
mode. The run ID is recorded in `<run>_wandb.json`.

Defaults follow the Wolf integration: 3-step returns, 2 critic updates per
vector step after warmup, actor updates every 2 critic updates, 1,000,000 replay
transitions, 100,000 warmup transitions, batch size 2048, and reward
normalization. Network dimensions follow the FlashSAC source config. Compilation
and AMP are opt-in (`--compile`, `--amp`). Replay uses the selected training
device; if its estimated allocation exceeds 80% of free GPU memory, the default
falls back to CPU. An explicit `--buffer_device cuda:0` instead fails with an
allocation explanation; `--buffer_device cpu` always uses host replay.

Checkpoint directories are written to
`lab/ddt_lab/logs/flash_sac/tita_flash_sac_<run>/model_<step>/`.
They contain actor/critic/target/temperature weights, optimizer and scheduler
state, normalization, the saved environment config, and `ddt.json` with
actor/config SHA256 hashes and observation dimensions.

All run summaries, metric JSONL, CLI args and TensorBoard events are recorded in
`docs/exp/YYYY-MM-DD/`. A summary labels warmup-only runs `SUSPICIOUS`, launch
failures `BLOCKED`, and numerical errors during training `FAIL`. `PASS` means
the requested steps and finite learner updates completed; it does not establish
that the learned robot locomotion is good.

```bash
# Deterministic playback in the saved environment, including its randomization.
python scripts/flash_sac/play.py \
  --checkpoint logs/flash_sac/<run>/model_100000 \
  --num_envs 16 --steps 1000

# Resume optimizer/network state; --steps is the total target vector step.
python scripts/flash_sac/train.py \
  --resume logs/flash_sac/<run>/model_100000 \
  --num_envs 1024 --steps 150000 --headless
```

Resume refills replay and starts fresh simulator episodes. It restores the
checkpoint's learning schedule and model hyperparameters. Checkpoints are not
exact continuation snapshots of simulator, replay or RNG state. Load only
trusted checkpoint directories: PyTorch and the saved environment config use
Python serialization.

The actor consumes the selected 35-dimensional `policy` group; the critic
consumes its own 39-dimensional `critic` group. These are packed as
`[policy, critic]`, with an explicit critic offset. `estimator_target` is not
used: `use_velocity_estimator=False` disables that group on FlashSAC's run config
before native environment creation, including resume/playback. The shared
`TitaFlatEnvCfg` keeps the group for PPO. Changing the flag to `True` fails
with an explanation because estimator/replay/loss integration is not implemented.
The PPO-specific learned velocity estimator and its supervised auxiliary
loss are absent from this FlashSAC baseline. The new actor therefore differs
from the current PPO estimator actor, while using the same task configuration.

The actor and replay use 8 normalized actions in `[-1, 1]`. The adapter maps
these to native actions with per-joint positive/negative gains from the runner
config. Native order is left hip/shoulder/knee/wheel, then the same right joints.
Positive gains are `(2.4, 2, 2.8, 6)` on each side; negative gains are
`(3.2, 2, 2.8, 6)`. Zero remains the default pose. With the existing native
scales this gives hip offsets `[-0.8, +0.6] rad`, shoulder offsets `±0.5 rad`,
knee offsets `±0.7 rad`, and wheel velocity targets `±30 rad/s`.
The resulting leg targets are hip `[-0.7, 0.7]`, shoulder `[0.3, 1.3]`, knee
`[-2.2, -0.8] rad`, inside the task's soft position limits. Target bounds do not
guarantee actual joint velocity bounds under the delayed PD actuator.
Checkpoint `ddt.json`, run `action_mapping.json` and W&B config record the
resolved gains. Playback/resume always restore saved gains; older checkpoints
without piecewise mapping metadata retain their original unit gains.
Isaac Lab's existing joint order, native scales, default offsets and actuator
limits apply afterward; last-action observations and action rewards see the
mapped native actions. Enlarging gains also enlarges physical exploration for
the same normalized noise; the initial range experiment retains learner/noise
settings to measure this effect.
The task config, rewards, command ranges and domain randomization are preserved.
The adapter captures true terminal observations before native auto-reset, so
n-step replay cuts returns at termination/timeouts and bootstraps timeouts from
the final state. It requires flat, concatenated `policy`/`critic` groups without
observation history or stateful modifiers; the selected flat task meets this
contract.

MuJoCo playback uses the shared TITA PPO/FlashSAC checkpoint loader:

```bash
# VALIDATION_SIM: repository root, no manual export/environment activation.
python3 sim2sim/sim2sim_ros2_jazzy/launch/sim2sim.launch.py \
  --ckpt lab/ddt_lab/logs/flash_sac/<run>/model_15000/actor.pt

# Finite check without viewer or keyboard.
python3 sim2sim/sim2sim_ros2_jazzy/launch/sim2sim.launch.py \
  --ckpt lab/ddt_lab/logs/flash_sac/<run>/model_15000/actor.pt \
  --headless --steps 1000
```

The same `--ckpt` accepts a PPO `model_N.pt` or a FlashSAC model directory.
The loader reads `env.yaml`, `agent.json`/`agent.yaml`, resolved
`policy_interface.json` when available, and FlashSAC `ddt.json`.
It verifies ONNX/PyTorch parity and caches the prepared policy under
`<checkpoint-parent>/sim2sim/<checkpoint-stem>/`.
FlashSAC signed action gains are embedded once in the exported actor; the
adapter then applies the saved native joint scales and offsets. Native
policy actions feed back into the last-action observation.

Keyboard: `w/s` forward/back, `a/d` yaw, `r` stop, `1` reset, `0` policy,
`6` idle, `Ctrl-C` exit. Playback starts in the training default pose with
RL enabled. Interactive command caps are 0.2 m/s and 0.3 rad/s. Simulation ROS
uses localhost domain 87. Evidence goes under `docs/exp/YYYY-MM-DD/`.

See [sim2sim README](../../../../sim2sim/README.md) for structure, ROS launch,
and the read-only state mirror. Current MuJoCo PD does not reproduce training
actuator delay or reset bias randomization. Finite execution checks do not
establish locomotion quality.

```bash
# DESKTOP_DRY_RUN: CPU checks without Isaac Sim startup.
PYTHONDONTWRITEBYTECODE=1 TORCHDYNAMO_DISABLE=1 \
  /home/cocel/isaac/env_isaaclab/bin/python \
  -m unittest discover -s test -p 'test_flash_sac*.py' -v
```

Run `./scripts/agent-check.sh` for required syntax, XML and diff checks.
