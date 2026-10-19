# TITA sim2sim

Execution domains: `VALIDATION_SIM` for playback, `ROBOT_READ_ONLY` for the
real2sim state mirror. Current TITA PPO and FlashSAC policies are supported.

From the repository root, with no manual export or environment activation:

```bash
python3 sim2sim/sim2sim_ros2_jazzy/launch/sim2sim.launch.py \
  --ckpt lab/ddt_lab/logs/flash_sac/<run>/model_15000/actor.pt

python3 sim2sim/sim2sim_ros2_jazzy/launch/sim2sim.launch.py \
  --ckpt lab/ddt_lab/logs/rsl_rl/<experiment>/<run>/model_1800.pt
```

`--ckpt` accepts a PPO `.pt`, FlashSAC `actor.pt`, or FlashSAC model directory.
Playback starts in the splay pose (`idle`). Keyboard: `1` splay -> sit
(`transform_up`), `0` policy (only after sit), `6` idle, `2` reset, `w/s`
forward/back, `a/d` yaw, `r` stop, `Ctrl-C` exit. Headless runs stand up and enter
RL automatically. Commands ramp at 0.5 units/s and return to zero after 0.5 seconds
without a key. Interactive caps remain 0.2 m/s and 0.3 rad/s.

The only checkpoint selector is `--ckpt`. `--headless --steps 1000` runs
finite control steps; `--prepare-only` verifies the export without opening MuJoCo.

```text
sim2sim_ros2_jazzy/
  launch/
    sim2sim.launch.py          # checkpoint playback
    real2sim.launch.py         # read-only ROS state mirror
  config/tita.yaml             # shared MuJoCo model / mirror defaults
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
