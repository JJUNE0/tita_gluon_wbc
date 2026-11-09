# TITA mjlab + FlashSAC

Execution domains: `TRAINING_SIM` for training; `VALIDATION_SIM` for playback/export.

`robots/tita/flat_env_cfg.py` and `robots/tita/walk/walk_env_cfg.py` run native mjlab managers and
MuJoCo Warp GPU physics. The learner is the existing, unmodified
`isaac_lab/ddt_lab/scripts/flash_sac/vendor/flash_rl` FlashSAC implementation.
This entry point does not use mjlab's default PPO runner.

The TITA environments are grouped by task:

```text
robots/tita/
├── flat_env_cfg.py       # Base driving environment / Teacher defaults
├── common/               # Robot model, motors, shared MDP functions
├── residual/             # Frozen Teacher + torque residual; optional training-only LPF
├── roll_pitch_height/    # Roll, pitch and height goals
├── sit_stand/            # Sit/stand and height-only cycles
├── stand_one_leg/        # Left/right reference, anchor and support commands
└── walk/                 # Walking and inline wheel-assisted stepping
```

`inline` remains the training CLI default and the base of the alternating
one-leg task. `support_command` selects left, right or both supports;
`support_velocity` adds velocity goals. Both remain supported in their task
folders. Task names and training commands are unchanged. The package initializer
preserves the old module paths for existing checkpoint `env.pkl` files and
trial scripts; new code should import from the task folders.

From the repository root, install in a separate Python 3.12 environment:

```bash
git submodule update --init --recursive third_party/mjlab
uv venv --python /usr/bin/python3.12 ~/venvs/tita_mjlab
uv pip install --python ~/venvs/tita_mjlab/bin/python \
  -e third_party/mjlab -e mj_lab 'torch==2.9.1' --torch-backend=cu128
source ~/venvs/tita_mjlab/bin/activate
```

The installed mjlab source is the official v1.6.0 tag, commit
`0fb8a681136be94ffc636a3dd423cabb97d91f10`. The tested environment uses
Torch 2.9.1+cu128, MuJoCo/MuJoCo Warp 3.11.0, Warp 1.18.0 and an RTX 3090.
Keep this environment separate from Isaac and the ROS sim2sim interpreter.

```bash
# Combined driving and stepping, from scratch (default task)
python -m mj_lab.scripts.train --task inline --num_envs 1024 --steps 100000

# Driving
python -m mj_lab.scripts.train --task flat --num_envs 1024 --steps 100000

# Hybrid walking: wheel-balanced standing at zero command
python -m mj_lab.scripts.train --task walk --num_envs 1024 --steps 100000
```

`robots/tita/walk/inline_env_cfg.py` inherits flat's wheel actions, PD, full domain
randomization, reset distributions and command ranges (vx +/-1.5 m/s,
vy 0, yaw +/-3 rad/s). A fixed half of environment IDs samples only vx, with
vy/yaw zero; the other half retains flat's mixed driving/turning/standing
sampling. The gait activates only for nonzero vx and zero yaw. Standing,
turning in place and combined translation/turning have no gait.

Inline's full left/right cycle is 2 s (0.5 Hz), with feet offset by 1 s.
Stance fraction 80% gives each foot a 0.4 s swing; the remaining cycle includes
double support. The clearance target is 4 cm. Both wheels retain the flat
velocity action scale 20 during gait. Contact/clearance rewards specify the
foot timing, and a small stance-push reward encourages the supporting leg to
move backwards relative to the body (opposite for reverse commands). Its
6 cm stroke target bounds the push speed to 0.0375 m/s, or the command speed
if smaller; it does not require the legs to provide all translation.

Flat's mirror penalty is masked during gait, and hip/shoulder deviation
weights become -0.1 during gait; outside gait their flat values are retained.
Base/knee contact termination and a -10 termination reward are enabled.
The settled position latch/moving anchor is retained. Inline actor/critic
dimensions are 40/44. New experiments omit both `--resume` and `--warm_start`.
Default single-environment inline previews show stop (1 s), forward (4 s),
backward (3 s), turn (1 s), stop (1 s), repeated every 10 s; explicit
`--command` overrides this schedule and the training cohort sampler.

W&B logging is enabled by default in `tita_flat_flash_sac`. Videos are uploaded
every 10,000 vector steps, with commanded and actual body-frame vx/vy overlays.
Each video is 500 control steps / 10 seconds. Checkpoints are saved every 5,000
steps under `mj_lab/logs/flash_sac/tita_mjlab_<run>/model_<step>/`.
Metrics, summaries and video evidence are recorded in `docs/exp/YYYY-MM-DD/`.

### Single-leg standing (code prepared; training is not started automatically)

For command-selected support, start a fresh experiment:

```bash
python -m mj_lab.scripts.train --task support_command --num_envs 1024 --steps 100000
```

`support_command_env_cfg.py` extends the reference balance task with discrete
goals: **0 = left support / right lift, 1 = right support / left lift, 2 = both
wheels grounded**. At each episode reset, sample left/right/both with
probabilities **0.4/0.4/0.2**, then hold that goal until the next reset. There is
no within-episode resampling or gait phase. These are episode probabilities;
fractions of physical simulation time can differ if episode lengths differ. vx/vy/yaw remain
zero and both wheel actions remain active. Actor/critic dimensions are 38/42,
including a three-element one-hot goal, with eight actions.

Modes 0/1 retain all reference-task reward weights, selecting the requested
support side symmetrically. Mode 2 uses **all 18 flat reward terms and their
original coefficients**, with no additional single-leg alive/pose/termination
terms. Manager keys are prefixed `one_leg_` and `flat_`; each environment uses
only the set selected by its command. Flat hold anchors and wheel integrals
are updated only for mode-2 rows. Common observations, resets, PD/actions,
physical/randomization settings and base/knee termination are retained; this
copies flat's reward set, not its randomized velocity commands or reset ranges.
Per-mode commanded seconds and successful seconds are logged separately.

Native checkpoint playback accepts `--support-mode 0`, `1`, or `2` to pin a
goal. New episode-fixed previews hold the sampled goal until reset and annotate
the goal and episode age in the video. Saved older timed-support configs retain their 3–5 s training
sampler and default single-environment 2 -> 0 -> 2 -> 1 video demonstration.
Older fixed-side checkpoints retain their behavior.

The `support_velocity` task adds locomotion to the same support goals:

```bash
python -m mj_lab.scripts.train --task support_velocity --num_envs 4096 --steps 100000
```

Each 6–8-second velocity-command resample chooses stationary with probability 0.5;
otherwise vx and yaw are independently uniform in ±0.5 m/s and ±0.5 rad/s. vy is zero.
This sampling is independent of the episode-fixed 40/40/20 support goal. It is a
probability mixture, not a fixed half of environment IDs. During single support,
the original stationary penalty is used only inside the command zero band. Moving
commands instead activate linear/yaw tracking bonuses with weights 2/1 and std 0.5.
Other single-support reward weights and all 18 both-support flat terms stay the same.
No gait is added; both wheel actions remain active. Dimensions remain actor 38,
critic 42 and actions 8. New experiments start without resume/warm-start; the old
`support_command` task and its saved zero-command policies remain available.
Support video overlays show vx/vy, commanded/actual yaw, support goal and episode age.

For the fixed-side reference experiment, use a fresh run:

```bash
python -m mj_lab.scripts.train --task stand_one_leg_reference --num_envs 1024 --steps 100000
```

`stand_one_leg_reference_env_cfg.py` requests left-wheel support and right-wheel
clearance throughout the episode. It has no gait clock, alternating feet, or
mode transition; actor/critic dimensions are 35/39. Both wheel actions remain
active. It starts from the nominal standing pose, with zero velocity commands
and reset velocities, and retains motor delay/gain/knee-output and physics DR.

An alive bonus (+2) accompanies partial clearance credit (+2, saturated at
4 cm), a small grounded-right-wheel cost (-0.5 effective), and a loose pose hint
(+0.5). The hint favors roll magnitude 20–40 degrees and both leg_1 angle
magnitudes 25–40 degrees, with gradual credit below these ranges and fading
credit above them. The operator's RViz pose is a style reference; angle signs,
sagittal joints, wheel angles, and the entire joint pose are not imposed.
The existing tilt, stationary, action-rate, acceleration and termination costs
remain -1, -0.5, -0.005, -2.5e-7 and -10. Base/knee contacts still terminate.
Reward weights are multiplied by the 0.02 s control timestep.

`Episode_Metrics/single_support_fraction` requires left contact, no right
contact, at least 1 cm right-wheel clearance, and no failure termination.
`single_support_time_s` is total supported lift time, not the longest continuous
hold. Double-contact fraction, peak clearance and pose-hint score are logged
separately. Timeout alone can mean successful two-foot standing and is not
evidence of successful one-leg balance. Older alternating checkpoints retain
their original configuration and remain playable.

`robots/tita/stand_one_leg/stand_one_leg_env_cfg.py` reuses inline's observations, actions,
wheel balance, physics and randomization, with vx/vy/yaw commands fixed to zero.
The first 2 s train double-support balance: both wheel contacts earn positive
reward while gait stays off. Gait then runs even at zero command. Its
2 s cycle and 75% stance ratio request 0.5 s swing per foot, offset by 1 s.
Reset uses nominal joint positions and zero base/joint velocities; delay,
motor-gain, knee-output and the other existing domain randomizations remain on.
Base/knee contact termination remains active during the initial 2 s too.

The reward has six terms: scheduled contact/clearance (+2), support-leg tilt
(-1), planar velocity/world-Z angular velocity (-0.5), action changes (-0.005),
joint accelerations (-2.5e-7), and termination (-10). `dof_acc_l2` is the name
of the single joint-acceleration term; it calls `joint_acc_l2` on all eight
joints, including wheels. Its coefficient matches flat's -2.5e-7.
The stationary cost is `-0.5 * (vx_world^2 + vy_world^2 + 0.1*wz_world^2)`;
it does not penalize position or body roll/pitch angles. World-Z angular
velocity is not generally equal to the derivative of Euler yaw at large tilt.
During gait the contact term requires the correct foot to support the robot. Each swing-foot
contact or missing stance-foot contact subtracts one from its raw score (effective
cost -2 per mismatch before timestep scaling), including during double support.
Swing clearance
gets linear credit up to 4 cm, with no extra credit above it; this is a clearance
target rather than a hard maximum. Both feet are requested down during double
support. The support axis is the `*_leg_2` hip pivot to the `*_leg_4` wheel center;
its cost is `1 - cos(tilt)` only during single support.

There is no body-flat, roll/pitch-rate, joint-deviation, base-height or exact pose
imitation objective. Body tilt and the free leg can balance the robot; knee/base
ground-contact termination remains active. No separate COM target is imposed.
Policy/critic dimensions remain 40/44. Wheel actions stay enabled for balance.
New stationary step-in-place checkpoints record `sim_reset_on_policy_entry`.
The simulator restores the saved initial standing state on policy entry,
including reentry, so the actor receives the same kind of start as training.

When explicitly starting a new experiment, omit resume/warm-start:

```bash
python -m mj_lab.scripts.train --task stand_one_leg --num_envs 1024 \
  --steps 100000 --headless
```

```bash
# Resume saved environment and learner state; replay is rebuilt.
python -m mj_lab.scripts.train --task walk --resume <checkpoint> --steps 100000

# Compatible weights with the current environment and fresh learner state.
python -m mj_lab.scripts.train --task walk --warm_start <checkpoint>

# Native deterministic playback/video, from the saved training configuration.
python -m mj_lab.scripts.play --checkpoint <checkpoint> --steps 500 \
  --video docs/exp/2026-10-27/mjlab_preview.mp4 --command 0 0 0
```

The native player is headless. Flat, fixed-wheel walk and hybrid walk checkpoints
can also use the existing interactive sim2sim viewer. Hybrid playback restores
the saved gait-dependent wheel gate: wheel policy control while gait is disabled,
zero wheel velocity targets during gait. The same flag is fed to the actor and
used for all physics substeps. Saved command thresholds, ramp and settling time
are restored; mjlab's episode-step clock is used for exact settling boundaries.

Export once from the Isaac environment (the export script does not start Isaac
Sim), then run the existing launcher:

```bash
~/isaac/env_isaaclab/bin/python isaac_lab/ddt_lab/scripts/flash_sac/export.py \
  --checkpoint <checkpoint>
python3 sim2sim/sim2sim_ros2_jazzy/launch/sim2sim.launch.py --ckpt <checkpoint>
```

`env.pkl` and `mjlab_env.yaml` contain the native config. `env.yaml` is a derived
playback interface for the existing exporter; it does not import Isaac classes.
Weights, normalization, optimizer and action gain metadata use the shared
FlashSAC format. `ddt.json` records the backend, source revision and file hashes.

| Setting | flat | walk |
|---|---|---|
| Policy / critic dimensions | 35 / 39 | 40 / 44 |
| Actions | 8, native L1–4 then R1–4 | Same; wheel scale 20 while standing, target 0 during gait |
| Observation joint order | L1,R1,L2,R2,L3,R3,L4,R4 | Same |
| Command vx / vy / yaw | ±1.5 / 0 / ±3 | ±0.5 / ±0.5 / 0 |
| Settle / ramp | 0 s / immediate | 1 s / 0.3 per second |
| Gait | — | 0.8 s, stance 60%, clearance 4 cm; off at zero command |
| Hip / shoulder deviation | −1.0 / −0.5 | Standing: −1.0 / −0.5; moving: −0.1 / −0.1 |
| Roll-rate / pitch-rate weights | Combined xy −0.05 | −0.02 / −0.1 |
| Contact termination | Base | Base and knees; termination reward −10 |

Both tasks use 5 ms physics steps and 20 ms control steps, spherical wheel
collision surfaces, leg PD 60/1.5, knee PD 92/2.3 and wheel PD 0/0.5, with
60/60/12 Nm limits. Delays of 0–4 physics steps are sampled at reset and held
through the episode. mjlab fuses motors with the same delay settings, so they
share the sampled command-bus lag. Gain and knee output randomization remain
enabled. Flat wheel velocity scale is 20, matching the current Isaac config;
the shared runner additionally applies its piecewise action gains.

Walk uses the gait-enabled observation as its mode indicator. The actor/critic
have 40/44 inputs, including the inherited wheel position error (scale 5,
clipped to +/-0.3 m before scaling). This encoder/leg-angle/pitch odometry
accumulates while standing at zero command. It is zero during gait and anchors
again on return to standing, excluding the final walking interval. New configs
also require actual planar speed below 0.1 m/s and absolute yaw rate below
0.15 rad/s. During deceleration or a fast push the reference follows the robot;
the first settled sample establishes a new zero. The internal integral is
bounded to +/-0.3 m (moving anchor), so excess displacement does not wind up
behind an observation clip. The zero-command position reward uses the same
speed conditions and a moving XY anchor within 0.3 m. Heading hold is unchanged.
Simulation currently uses true body velocity for this gate; a robot runtime
would need an equivalent velocity estimate. The velocity changes latch logic,
not the policy input dimension. These settings are saved in the playback
contract; older saved configs retain their original command-only behavior.
This adds
one input to the earlier 39/43 walk policies, so those weights cannot resume
or warm-start the new observation layout; use a fresh run. Saved older layouts
remain playable with their original dimensions and odometry behavior.
After the one-second settling window, the gait
starts when emitted planar command magnitude exceeds 0.02 m/s or yaw-rate
magnitude exceeds 0.03 rad/s. Within that deadband the gait stops and both wheel
policy actions use the inherited driving scale. During gait the processed wheel
targets are zeroed per environment; raw action history and motor gains/delays
are preserved. Gait-contact/clearance rewards are active only during gait.
Deviation manager weights remain the flat values, with per-environment factors
0.1 for hip and 0.2 for shoulder while moving, giving effective weights −0.1
for both. Old saved fixed-wheel configs keep their original behavior on resume;
start fresh or use weights-only warm start to use the new hybrid configuration.

MuJoCo contact dynamics differ from PhysX. Static/dynamic friction and
restitution cannot be copied directly: this port uses randomized sliding
friction (flat 0.2–1.6; walk 0.8–1.2), default MuJoCo contact damping, and
robot geometry priority so the ground does not mask friction randomization.
Flat keeps mass/inertia/CoM/push and observation bias randomization; walk keeps
the selected bootstrap settings without those perturbations. Do not compare
learning curves as if the physics and every randomization were identical.

Validation:

```bash
python -m pytest -q test/test_mjlab_tita.py
./scripts/agent-check.sh
```

Short learner, resume, video and sim2sim checks establish pipeline operation.
They do not establish a trained walking policy; run a full experiment for that.

## Frozen Teacher with torque residual

Execution Domain: `TRAINING_SIM`. The canonical runner is
`mj_lab.scripts.train_residual_torque`, organized around Experiment1:
Teacher-shared sensor noise/bias, random height/roll/pitch commands and
post-PD torque delay. Teacher remains frozen; residual Actor/critics, replay,
optimizers and entropy temperature initialize fresh.

```bash
~/venvs/tita_mjlab/bin/python -m mj_lab.scripts.train_residual_torque \
  --teacher sim2sim/checkpoints/mjlab/task/base_velocity/height_roll_pitch/20261108/80000 \
  --reference-config mj_lab/config/residual_lpf60_10k.json \
  --output docs/exp/2026-11-08/my_new_torque_run \
  --num-envs 4096 --batch-size 8096 --steps 50000
```

Use a new output directory. The reference supplies learner settings, not weights
or replay. Defaults: gamma0.99,1M replay transitions,100k warmup transitions,
two updates per vector step,10s episodes, seed42, checkpoints every2k vector
steps, evolving-training video every10k, online W&B logging and final matched
Teacher/candidate evaluation. Local artifacts, source copies, hashes, initial
state checks, metrics and upload receipts remain in the dated output folder.

Teacher runs50Hz, residual250Hz and PD/physics500Hz. The normalized eight-axis
Actor output is scaled once to ±10Nm; PD + residual is effort-clipped then
passed through the post-PD actuator command history. Each environment samples
a common motor lag from0/2/4/6/8ms on reset and holds it for that episode.
Native reference-command delay is disabled to avoid adding a second lag model.
Residual output holds between its4ms updates; the PD state feedback updates2ms.

The Actor has44 features ×10 frames (440 inputs); asymmetric critic754 inputs.
Joint/gyro/gravity sensor corruption is shared with Teacher, including the saved
bias/delay/noise pipeline, rather than drawing a second independent sample.
Residual has its own fixed stop wheel-displacement reference, no velocity latch
and no wheel-error input clip. Teacher's saved wheel/heading observation behavior
is unchanged. Existing rewards and their coefficients remain the Experiment1
values. Initial pose/velocity perturbations and initial push are disabled;
payload, physical DR and subsequent push scheduling remain enabled.

Pose command targets are randomly resampled: height0.27–0.42m, roll±30°,
pitch±15° by default, with30% nominal targets and5–8s resampling intervals.
These are command targets using the saved pose ramp, not random teleports.
`--pose-command-mode height` limits the sampler to height only.

### Experiment2: residual-only LPF60

Add `--residual-lpf-hz 60` to the same runner, using a different output directory.
The native one-pole filter updates at500Hz on residual torque before it joins
PD. The rest of the pipeline and episode-fixed torque delay remain the same.
Its saved manifest explicitly records the filter. Current sim2sim and Sim2Real
restore this residual-only filter at500Hz before fresh PD, clipping and delay.
The published Teacher80k/residual10k pair and fresh10k training command are in
[the LPF60 guide](../docs/lpf60_residual.md). Historical experiment output paths
below are local examples; the published recipe does not require them.

### Internal structure and playback

- `robots/tita/residual/__init__.py`: `TorqueResidualEnv` / `TorqueResidualEnvCfg`
  expose the Experiment1 environment.
- `flat_env_residual_torque.py`: native Teacher/reward/DR/torque environment.
- `flat_env_residual_torque_delay.py`: post-PD motor-command delay.
- `flat_env_residual_torque_pose_delay.py`: random pose command sampling.
- `flat_env_residual_torque_sensor_delay.py`: shared Teacher sensor interface.
- `flat_env_residual_torque_lpf_delay.py`: optional Experiment2 filter.
- `scripts/residual_training.py`: shared learner, rendering and evidence helpers.
- `scripts/train_residual.py`: render-only compatibility path for the live
  Experiment1's video subprocess; it is no longer a training entrypoint.

These internal layers retain their native dynamics. Historical action residual
and duplicate trainer sources are archived in
`docs/exp/2026-11-08/backup/retired_training/`.
For torque-only playback use
[`sim2sim.residual.torque.launch.py`](../sim2sim/sim2sim_ros2_jazzy/launch/sim2sim.residual.torque.launch.py);
see the [sim2sim instructions](../sim2sim/README.md).

## Play and automatic checkpoint registration

Execution Domain: `VALIDATION_SIM`. The default Teacher is read from
`sim2sim/config/policies.json`, so the current policy needs no long path:

```bash
~/venvs/tita_mjlab/bin/python -m mj_lab.scripts.play --steps 1000

# Select a new training checkpoint once; both registries are populated.
~/venvs/tita_mjlab/bin/python -m mj_lab.scripts.play \
  --checkpoint mj_lab/logs/flash_sac/<run>/model_<step> --steps 1000

# Native video; save evidence inside docs/exp/YYYY-MM-DD/.
~/venvs/tita_mjlab/bin/python -m mj_lab.scripts.play --steps 1000 \
  --video docs/exp/2026-11-08/teacher_play.mp4

# MuJoCo sim2sim defaults come from the same selection config.
~/venvs/tita_mjlab/bin/python sim2sim/sim2sim_ros2_jazzy/launch/sim2sim.launch.py
~/venvs/tita_mjlab/bin/python sim2sim/sim2sim_ros2_jazzy/launch/sim2sim.residual.torque.launch.py
```

Native play accepts the registered checkpoint folder or `policy.pt` as well.
For example, `--checkpoint sim2sim/checkpoints/mjlab/task/base_velocity/height_roll_pitch/20261108/80000`.
Registration preserves native playback states and saved sensor/action contracts;
it does not change learning or replace the config-selected hardware policy.
See [registry layout](../sim2sim/checkpoints/README.md).

### Pre-shared-sensor LPF comparison (2026-11-09)

`--actor-sensor-mode clean --residual-lpf-hz 60` keeps the old full-pose torque
Actor's simulated proprioception and existing error-input path while adding only
the500Hz residual filter. Teacher noise/bias/delay remains enabled as saved.
The default `teacher_shared` profile is unchanged. A fresh4096/b8096/50k comparison
is queued after candidate validation; do not launch a duplicate. Exact settings
and queue evidence: `docs/exp/2026-11-09/clean_lpf60_queued_training.md`.
