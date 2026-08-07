# GLUON P0 runtime URDF baseline

- Date: 2026-08-05
- Execution Domain: `VALIDATION_SIM`
- Branch: `dev_gluon`
- Policy Checkpoint SHA256 or ONNX Hash: N/A (asset validation)
- IsaacLab revision: `549768529e3859845794a05b8fd3dfd00edadc9e`
- Canonical URDF SHA256: `eb6bbc1f2305fac3da832a911f00efbc82b5c7af57d905b3008bc5531707089e`
- Sim URDF SHA256: `b9b25074b7a417a9e499f14fee852699ac6f8a00ab4b137f90ec843eccc8ede4`
- Evidence Status: `PASS`

## Objective

Correct the IsaacLab GLUON description path and validate the runtime-imported
six-axis articulation against the P0 model contract. The validation checks the
fixed base, exact joint/body order, all joint limits including q6 at +/-150
degrees, total mass, finite state, root drift, and q=0 `link6` position in the
`base_link` frame.

## Command

```bash
timeout 240s env PYTHONUNBUFFERED=1 \
  /home/cocel/isaac/env_isaaclab/bin/python \
  test/test_gluon_asset_runtime.py --headless

timeout 240s env PYTHONUNBUFFERED=1 \
  /home/cocel/isaac/env_isaaclab/bin/python \
  lab/ddt_lab/scripts/gluon/smoke_gluon_asset.py --headless

timeout 240s env PYTHONUNBUFFERED=1 \
  /home/cocel/isaac/env_isaaclab/bin/python \
  lab/ddt_lab/scripts/gluon/smoke_gluon_reach_env.py --headless
```

## Result

The first launcher attempt used `IsaacLab/isaaclab.sh -p` without an activated
environment and failed before importing the asset:

```text
[ERROR] Unable to find any Python executable at path:
/home/cocel/isaac/IsaacLab/_isaac_sim/python.sh
```

The verified local environment was then invoked directly. Runtime evidence:

```text
check,status=PASS,name=fixed_base,value=True
check,status=PASS,name=runtime_joint_order,runtime=[axis_joint_1..axis_joint_6]
check,status=PASS,name=runtime_body_order,runtime=[base_link,link1..link6]
check,status=PASS,name=runtime_joint_limits,max_abs_error_rad=2.384e-07
check,status=PASS,name=joint6_limits_150_deg,
  runtime=[-2.6179935932159424,2.6179935932159424]
check,status=PASS,name=total_mass,
  runtime_kg=4.2676115036,contract_kg=4.2676113806
check,status=PASS,name=finite_runtime_state,value=True
check,status=PASS,name=fixed_base_root_drift,drift_m=0.000e+00
check,status=PASS,name=home_ee_position_base,error_m=1.949e-07
summary,failures=0
GLUON_P0_RUNTIME: PASS

GLUON_ASSET_SMOKE: PASS
GLUON_REACH_ENV_SMOKE: PASS
```

Observed reach environment contract:

```text
num_envs=4
policy_observation_shape=(4, 25)
action_shape=(4, 6)
joint_names=[axis_joint_1..axis_joint_6]
```

## Risks

- The description path is source-tree-relative and assumes the local editable
  workspace layout.
- `isaaclab.sh -p` requires the IsaacLab environment to be activated on this
  workstation; automation currently uses the explicit environment Python.
- No physical robot, ROS hardware bridge, or actuator command is part of this
  validation.
