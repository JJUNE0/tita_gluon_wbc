# TITA sim2sim

Execution domains: `VALIDATION_SIM` for playback, `ROBOT_READ_ONLY` for the
real2sim state mirror. Current TITA PPO and FlashSAC policies are supported.

From the repository root, with no manual export or environment activation:

```bash
python3 sim2sim/sim2sim_ros2_jazzy/launch/sim2sim.launch.py \
  --ckpt isaac_lab/ddt_lab/logs/flash_sac/<run>/model_15000/actor.pt

python3 sim2sim/sim2sim_ros2_jazzy/launch/sim2sim.launch.py \
  --ckpt isaac_lab/ddt_lab/logs/rsl_rl/<experiment>/<run>/model_1800.pt
```

`--ckpt` accepts a PPO `.pt`, FlashSAC `actor.pt`, or FlashSAC model directory.
Playback starts in the splay pose (`idle`). Keyboard: `1` splay -> sit
(`transform_up`), `0` policy (only after sit), `6` idle, `2` reset, `w/s`
forward/back, `a/d` yaw, `r` stop, `Ctrl-C` exit. Headless runs stand up and enter
RL automatically. Commands ramp at 0.5 units/s and return to zero after 0.5 seconds
without a key. Set simulation command caps in
`sim2sim/sim2sim_ros2_jazzy/config/tita.yaml`, then restart playback:

```yaml
command:
  max_lin_x: 0.2  # forward/backward, m/s
  max_lin_y: 0.2  # lateral, m/s
  max_ang_z: 0.3  # yaw rate, rad/s
```

The effective range is the intersection of these symmetric caps and the saved
training range on each axis. A zero cap disables that axis; an axis disabled in
training stays disabled. The same limits apply to keyboard, ROS Twist and
headless commands. Changing the YAML invalidates the export cache automatically.
This configures requested velocity; actual robot velocity can differ.

The only checkpoint selector is `--ckpt`. `--headless --steps 1000` runs
finite control steps; `--prepare-only` verifies the export without opening MuJoCo.

Support-command checkpoints also accept `--support-mode 0` (left wheel supports),
`1` (right supports), or `2` (both grounded). Playback defaults to mode 2 from
the saved contract. For example:

```bash
python3 sim2sim/sim2sim_ros2_jazzy/launch/sim2sim.launch.py \
  --ckpt mj_lab/logs/flash_sac/<support_run>/model_100000 --support-mode 0
```

Keep the existing `1` then `0` startup keys. During playback, `7`, `8`, `9`
select support modes 0, 1, 2 without resetting physics. The existing simulated
`cmd_key` topic accepts `support_left`, `support_right`, `support_both`.

Support-velocity checkpoints use the same launcher: vx/yaw come from their saved
ranges (currently ±0.5 m/s and ±0.5 rad/s); vy remains zero. Use `w/s` for vx,
`a/d` for yaw and `r` to stop. The 50/50 command mixture is a training sampler;
interactive playback follows operator commands.

`1` physically performs the existing preparation, then `0` enters RL without
resetting position, velocity or simulation time. Legacy `sim_reset_on_policy_entry`
metadata is ignored by current playback. Only the explicit `2` reset key respawns
the simulation. During support-policy RL, total tilt beyond
`control.support_fall_tilt_deg` in `config/tita.yaml` (default 55 degrees) stops
policy evaluation and enters bounded joint-velocity damping. Commands/actions are
cleared; prepare again before reentering RL. This is simulation behavior, not a
hardware deployment. Runtime reports include tilt-fault count and final state.
Support goals are three one-hot inputs, separate from velocity commands;
there is no gait phase or automatic alternation in sim2sim. Mode
selection is rejected for checkpoints without this observation.

## Roll, pitch and height commands

`flat_roll_pitch_height` checkpoints use the same launcher, with an optional pose target:

```bash
python3 sim2sim/sim2sim_ros2_jazzy/launch/sim2sim.launch.py \
  --ckpt mj_lab/logs/flash_sac/<pose_run>/model_N --pose 0 0 0.335
```

`--pose ROLL_DEG PITCH_DEG HEIGHT_M` uses degrees for the two angles and metres
for absolute base_link height above the flat ground. The saved policy observation
receives radians/radians/metres in its original order and scale. Defaults,
ranges and ramp rates come from the checkpoint. Current pose policies allow
roll ±30 degrees, pitch ±15 degrees and height 0.27–0.42 m, starting at
0/0/0.335. Their saved rates are 0.15 rad/s, 0.15 rad/s and 0.02 m/s. The first
RL observation is nominal; the command advances once after each RL physics step.

In the launching terminal, `1` then `0` prepares and enters RL without a physics
reset. `j/l` changes target roll by ±1 degree, `i/k` target pitch by ±1 degree,
and `u/o` target height by ±1 cm. `p` restores the saved nominal pose. Targets
stay latched after releasing a pose key; `r` stops velocity while retaining the
pose target. `2` explicitly resets physics and restores nominal pose. Existing
`w/s`, `a/d` velocity/yaw controls remain available. The viewer shows target,
emitted command and actual roll/pitch/height.

The simulation `geometry_msgs/Vector3` topic `/tita/command/manager/cmd_pose`
accepts x=roll radians, y=pitch radians, z=absolute height metres. ROS/keyboard
targets are bounded by saved ranges; non-finite ROS requests are ignored.
Out-of-range CLI targets are rejected. Pose targets can also be supplied to
headless runs, for example `--headless --steps 500 --pose 10 -5 0.35`.
Runtime reports record target, emitted and actual pose in radians/radians/metres.
These three actor inputs are distinct from the same-width support-mode one-hot
inputs. Legacy policies retain their existing layouts and controls.

Walking checkpoints use the same launcher and are detected from their saved
`gait` observation. Walk actors receive the saved five gait values
`[enabled, sin(phase), cos(phase), frequency, stance_fraction]`. Its clock advances
once per RL physics step, including at zero velocity when `step_in_place` is set.
Frequency, settle time, thresholds, PD and action masks come from the checkpoint;
vx/vy/yaw ranges also respect the YAML caps above. A randomized training frequency range uses its midpoint
for deterministic playback; the initial leading phase is zero.

```bash
# VALIDATION_SIM: model directory or its actor.pt both work.
python3 sim2sim/sim2sim_ros2_jazzy/launch/sim2sim.launch.py \
  --ckpt isaac_lab/ddt_lab/logs/flash_sac/<walk_run>/model_100000

# Fixed headless command: vx=0.2m/s, vy=0, yaw-rate=0.
python3 sim2sim/sim2sim_ros2_jazzy/launch/sim2sim.launch.py \
  --ckpt isaac_lab/ddt_lab/logs/flash_sac/<walk_run>/model_100000 \
  --headless --steps 1000 --command 0.2 0 0
```

Walk follows the same `idle` (splay) -> `transform_up` -> `sit` -> `rl` state
machine as driving. In the viewer, press `1`, wait for sit, then press `0`;
`6` returns to idle and `2` resets to splay/idle. Headless playback performs
the transition and enters RL automatically. Gait time stays at zero outside
RL; each policy entry restarts the saved initial settle and command ramp
before reaching a requested target. The flat training
ground and converted sphere-wheel collisions are selected automatically;
simulation uses nominal PD without sampling training randomization. The viewer
follows the robot and shows commanded/actual body vx/vy. Keyboard: hold `w/s`
for forward/back, `q/e` for lateral left/right, `a/d` for yaw when its saved range
allows it, `r` for zero velocity (gait follows the saved `step_in_place` setting), and `2` to reset
the pose, command, action history and gait clock. `Ctrl-C` exits.
`--command VX VY WZ` requires headless mode and values inside the effective limits;
out-of-range values are rejected with the allowed range.
Wheel residual controllers are rejected for walk checkpoints.
Fixed-wheel walk requires both saved wheel velocity actions to have scale and
offset zero. Hybrid mjlab checkpoints may instead save
`GaitGatedWheelVelocityAction` on both wheels: when gait is disabled, scaled and
clipped wheel policy targets are enabled; when gait is enabled, those processed
targets are zero. The gate follows the same flag seen by the actor and stays
fixed through each control step's physics substeps. Raw previous-action feedback
is preserved. The viewer shows whether wheel policy control is ON or OFF.
Partial wheel gates, gates without a gait observation and unknown gate metadata
are rejected. mjlab command/gait settling uses its episode-step clock; existing
Isaac clock behavior is preserved. Playback does not overwrite measured wheel
velocity or lock a joint; zero targets retain the saved damping.
New mjlab hybrid walk policies have 40 inputs, adding wheel position error
while standing. The saved `gait_name` on that term suppresses encoder odometry
during gait and resets its anchor when returning to standing. Earlier 39-input
walk checkpoints keep their original layout; adding an observation requires
retraining the policy.
Saved `velocity_thresholds` optionally defer the wheel-position latch until
body planar speed and yaw rate are small. While coasting, or on the first
settled sample, the reference follows the measured odometry. Saved
`moving_anchor` bounds the reference's distance from current odometry instead
of allowing hidden integral windup. These options require a finite body linear
velocity input; the main simulator provides it. They are opt-in checkpoint
metadata, preserving older policies' original observation behavior.
Inline checkpoints use the same launcher. Their saved `straight_only` flag
disables gait for stop/turn/mixed commands, and explicit `wheel_enable: always`
on both wheel velocity actions preserves driving during foot lifts. Their
0.5 Hz frequency and 80% stance ratio give a 2 s full cycle, 1 s left/right
offset and 0.4 s swing per foot. Legacy walk's wheel gate is preserved.

`stand_one_leg` checkpoints also use this launcher. Their saved zero velocity
ranges, `step_in_place: true`, 0.5 Hz gait and 75% stance ratio restore a 2 s
cycle with a 0.5 s swing per foot. Both wheel policy actions stay enabled for
balance. Press `1`, wait for sit, then `0`. New stationary balance checkpoints
recorded `sim_reset_on_policy_entry` in older exports; current playback preserves
the prepared physical state when entering RL. Their first 2 s train
double-support balance before gait starts without any velocity key. Older
checkpoints keep their saved settling time and startup behavior.
`r` keeps the zero command
and stepping continues; `6` leaves policy control and stops the gait clock.

```bash
python3 sim2sim/sim2sim_ros2_jazzy/launch/sim2sim.launch.py \
  --ckpt mj_lab/logs/flash_sac/<stand_run>/model_<step>
```

Later model directories use the same command and are exported automatically.
Successful playback does not establish physical single-leg balance.

```text
sim2sim_ros2_jazzy/
  launch/
    sim2sim.launch.py          # checkpoint playback
    real2sim.launch.py         # read-only ROS state mirror
  config/tita.yaml             # simulation command caps / shared model / mirror defaults
  sim2sim_ros2_jazzy/
    checkpoint.py             # saved layout, PPO/FlashSAC export, parity, cache
    adapter.py                # observation/action mapping and native PD
    mujoco_env.py             # physics and viewer lifecycle
    sim2sim_node.py            # policy loop and terminal controls
    state_machine.py           # idle (splay) -> sit -> rl startup sequence
    real2sim_node.py           # incoming state -> MuJoCo state
    cli.py                    # environment bootstrap and evidence logging
```

Weights alone do not encode joint names, observation order, or action scales.
Keep `env.yaml` and `agent.json`/`agent.yaml` beside the checkpoint, one directory
above it, or in the run's `params/`. FlashSAC also needs its `ddt.json`.
New training saves resolved names and observation scales in `policy_interface.json`.
Existing checkpoints use the saved TITA configuration and the Isaac articulation
order verified against the current training environment.

The adapter reads observation terms in saved order, clips before observation
scaling, and maps actions using saved joint names, scale, offset, and processed
target clipping. PPO normalization and its velocity estimator, when present,
are embedded in the exported policy. FlashSAC signed gains are embedded once;
the adapter then applies native joint scales. Last-action observations retain
policy action order.

`--leg_action_filter auto` is the default. Saved `MA2JointPositionAction` terms
select MA2 for the six leg actions; ordinary position actions select no filter.
Wheels pass through and `last_action` keeps the unfiltered output. Explicit
`none`, `ma2_legs` or `ma2_notch_legs` overrides remain available for experiments.
The 34-input PosKneeMA2 actor is selected from its saved layout, without a
task-specific YAML or manual observation dimension.

`WheelPositionError` uses encoder/IMU rolling distance
`s = radius * mean(q_wheel + pitch + q_thigh + q_knee)` and reports
`clip(s - reference, +/-clip_m) * scale` while all commands are within the saved
zero thresholds. Outside that band the reference follows `s` and the error is
zero. Reset and RL reentry relatch the reference. Wheel angles are unwrapped
between policy ticks (travel must be less than pi radians per tick). Radius,
thresholds, clip and scale come from the checkpoint; inference uses the nominal
radius and omits training noise/randomization. Python and robot C++ use the
same definition and exported parameters; an unknown observation/action type
still fails export explicitly.

Exports cache under `<checkpoint-parent>/sim2sim/<checkpoint-stem>/`.
Checkpoint/configuration, adapter source, generated config, and ONNX hashes
invalidate stale caches. Evidence and ROS logs go into `docs/exp/YYYY-MM-DD/`.
Simulation ROS uses localhost domain 87. Terminal input and policy stepping
share one executor, and physics runs on the control timer. MuJoCo does not reproduce training actuator delay or
reset bias randomization. Finite runtime checks establish execution, not quality.

The launcher uses the installed Isaac Python and the existing MuJoCo Python
at `~/venvs/cosim_ros2_jazzy/bin/python`. The virtual environment name stays;
it is independent of the renamed source package. Override interpreter paths
with `--isaac-python` and `--mujoco-python`.

For ROS integration, build only this package:

```bash
source /opt/ros/jazzy/setup.bash
colcon --log-base docs/exp/$(date +%F)/sim2sim_build_logs build \
  --symlink-install --base-paths sim2sim/sim2sim_ros2_jazzy \
  --packages-select sim2sim_ros2_jazzy \
  --build-base sim2sim/.ros2/build --install-base sim2sim/.ros2/install
source sim2sim/.ros2/install/setup.bash

# VALIDATION_SIM: ROS uses ckpt:=; direct Python uses --ckpt.
ros2 launch sim2sim_ros2_jazzy sim2sim.launch.py \
  ckpt:=/absolute/path/to/checkpoint.pt headless:=true steps:=1000

# ROBOT_READ_ONLY: operator-selected incoming state topics.
ros2 launch sim2sim_ros2_jazzy real2sim.launch.py real_tita_ns:=tita4252763
```

real2sim subscribes to `<namespace>/joint_states`,
`<namespace>/imu_sensor_broadcaster/imu`, and `<namespace>/chassis/odometry`.
It sets MuJoCo state and calls `mj_forward`; it never runs policy physics or
publishes robot control commands. Debug state topics are under `/real2sim/`.
Odometry position mirroring is off by default; enable with
`mirror_base_position:=true`.

Old cosim, GLUON/MOO replay, relay/ghost launches, checkpoint-specific YAMLs,
and their obsolete helpers were removed from the active execution tree.
Exact pre-cleanup contents, including local edits, are backed up in
`docs/exp/2026-10-14/sim2sim_cleanup_before.tar.gz`.
Robot descriptions are managed under `robot/{tita,gluon,tita_gluon}/`.
See [robot asset layout](robot/README.md).

The [minimum-code policy](AGENTS.md) applies to future changes here. There is one
saved policy interface, one export verification path, and one simulation loop.
Unused history/fallback adapters, debug action containers, automatic run/step
selection and the separate keyboard worker have been removed. Code clarity
and required validation take precedence over saving individual lines.

## Ground friction

`sim2sim/sim2sim_ros2_jazzy/config/tita.yaml` sets `model.ground_friction` (current value `0.8`).
Edit this dimensionless sliding coefficient and restart the checkpoint launcher. Values such as
`0.2`, `0.8`, or `1.6` apply to actual terrain contacts, including wheel contacts; terrain priority
prevents a larger wheel coefficient from overriding low values. Torsional/rolling entries are unchanged.
MuJoCo clamps contact friction to its small positive minimum when the configured value is zero.
The export cache includes this setting, so the normal launcher refreshes an older prepared config.
Directly running a previously exported `config.json` retains that export's value.
The robot XML and training randomization are not modified.
