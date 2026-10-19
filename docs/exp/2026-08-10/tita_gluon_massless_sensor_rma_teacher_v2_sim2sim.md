# TITA+GLUON massless-sensor RMA teacher v2 MuJoCo sim-to-sim

- Date: 2026-08-10
- Execution Domain: `VALIDATION_SIM`
- Evidence Status: `PASS`
- Training run: `2026-08-09_17-15-39_massless_sensor_rma_teacher_v2`
- Selected checkpoint: `model_9000.pt`
- Checkpoint SHA256: `6b540459bd8ad833e2822d1a3bcad8bdc87f556877a37fc066f39dfd463dfc3b`
- Actor ONNX SHA256: `b3ff952603fdc896be304e0420cef60c952da370a11e77b611855a1488ab0c93`
- Privileged encoder ONNX SHA256: `a1e47cda04db613dcc52e6403053f6829224d8b227bd3a0ce57926e48497e7c0`

## Scope

Added the operator-facing ROS2 state-machine launch `tita_gluon_mujoco_sim2sim.launch.py` and config `tita_gluon_20260809_9000_rma_teacher.yaml`. The existing `mujoco_policy_node` FSM remains the control authority (`idle`, guarded transform-up, stand hold, then `rl_0`). `sim2sim/tita_gluon_mujoco_sim2sim.py` remains the ONNX exporter and direct diagnostic path.

The MuJoCo environment dynamically combines the corrected free-base TITA MJCF with the moving GLUON subtree converted from the combined URDF. GLUON holds the work pose outside policy states and starts its training-matched trajectory only in `rl_0` or `shadow_rl0`. No robot hardware or network command path was used.

Policy contract:

- teacher actor input: 108 (`policy_obs[92] + privileged latent[16]`)
- privileged encoder input/output: 25 -> 16
- actor output: 8 TITA actions
- policy rate: 50 Hz (`dt=0.005`, decimation 4)
- GLUON: independent implicit-PD center/waypoint/center trajectory, full workspace scale

## Artifact verification

The script exported both ONNX files directly from `model_9000.pt`. ONNX reference outputs were compared with the checkpoint-backed PyTorch modules using deterministic random batches:

- actor max absolute error: `1.192e-07`
- encoder max absolute error: `1.192e-07`
- fixed ONNX contracts: actor `[1,108] -> [1,8]`, encoder `[1,25] -> [1,16]`

Compiled MuJoCo model contract:

- `nq=21`, `nv=20`, `nu=14`, `nbody=18`
- total explicit mass: `30.958567923 kg`
- fixed base composite mass: `13.311143923 kg`
- TITA actuator effort limits: leg `55 Nm`, wheel `36 Nm`
- GLUON actuator effort limits: joints 1-2 `18 Nm`, joints 3-6 `10 Nm`

## Direct closed-loop result

Command:

```bash
/home/cocel/venvs/cosim_ros2_jazzy/bin/python \
  sim2sim/tita_gluon_mujoco_sim2sim.py \
  --headless --duration-s 10 --no-real-time --log-every-s 10
```

Observed result:

- sim time: `10.000 s`
- minimum base height: `0.3499 m`
- maximum base tilt: `3.107 deg`
- maximum absolute actor action: `1.4751`
- maximum GLUON tracking error: `0.0394 rad`
- non-finite state/action: none
- terminal evidence: `PASS`

## ROS2 FSM result

Launch command:

```bash
ros2 launch cosim_ros2_jazzy tita_gluon_mujoco_sim2sim.launch.py \
  viewer:=false keyboard:=false joystick:=false
```

Observed guarded transition sequence:

```text
idle -> reference_transform_up -> reference_stand_hold -> rl_0
```

- premature `rl_0` command while idle: rejected as expected
- transform duration: `8.388 s`
- policy-state observation duration: `15 s`
- final state: `rl_0`
- final base height: `0.373815 m`
- final roll/pitch maximum magnitude: `2.647 deg`
- maximum absolute actor action: `1.759349`
- GLUON motion after policy activation: `0.354094 rad`
- `/joint_states`: TITA 8 + GLUON 6 names/positions/velocities/efforts
- terminal evidence: `PASS`

Backward-compatibility smoke: the prior TITA-only RMA teacher config compiled with `nq=15`, `nu=8`, `obs_dim=68`, and `auxiliary_arm_enabled=false` (`PASS`).

## GLUON base visual alignment correction

Operator comparison against the combined URDF viewer found that the first joint
axis was correct but the stationary GLUON base mesh was rotated. The combined
URDF defines the base visual origin as `xyz="0 0 0"` and
`rpy="1.570796 0 1.570796"`; the hand-built MJCF base geom previously omitted
that visual-only transform.

The model builder now reads the base visual origin from the configured combined
URDF and converts its fixed-axis RPY to MuJoCo's WXYZ quaternion. The resulting
quaternion for this asset is approximately `[0.5000001634, 0.5, 0.4999998366,
0.5]`. The geom remains visual-only (`contype=0`, `conaffinity=0`, `density=0`),
so the correction does not modify collision geometry, mass, inertia, or joint
frames.

Automated point-cloud comparison transformed all 2,511 unique base STL vertices
through the URDF visual chain and the compiled MJCF geom chain:

- maximum MJCF-to-URDF nearest-vertex error: `3.808004501504e-09 m`
- maximum URDF-to-MJCF nearest-vertex error: `3.808004501504e-09 m`
- operator viewer comparison after rebuild: base visual matches the URDF
- Evidence Status: `PASS`

## Known sim-gap risks

- MuJoCo uses deterministic ground friction `0.8`; the training environment randomized friction.
- The training TITA actuator used a randomized action delay up to four physics steps; this validation runner intentionally uses deterministic zero delay.
- GLUON self-collisions and TITA-to-GLUON collisions are disabled to match articulation-wide self-collision settings; GLUON-to-ground collisions remain enabled.
- This result is simulation-only and does not authorize robot deployment or hardware commands.
