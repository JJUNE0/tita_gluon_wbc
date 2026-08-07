# GLUON P1 URDF-to-USD conversion

- Date: 2026-08-05
- Execution Domain: `VALIDATION_SIM`
- Branch: `dev_gluon`
- Policy Checkpoint SHA256 or ONNX Hash: N/A (asset conversion)
- IsaacLab revision: `549768529e3859845794a05b8fd3dfd00edadc9e`
- Canonical URDF SHA256: `eb6bbc1f2305fac3da832a911f00efbc82b5c7af57d905b3008bc5531707089e`
- Sim URDF SHA256: `b9b25074b7a417a9e499f14fee852699ac6f8a00ab4b137f90ec843eccc8ede4`
- Output USD SHA256: `a5b9514205ae7b3de4321ab308fc6e8aa4f3b17533c172fe53f7269a5b49a42d`
- Output bundle SHA256: `ac95b231160d0a2b6f08bbd59af3c23e391bb6c8d1a094dc044709e0570577b4`
- Evidence Status: `PASS`

## Objective

Generate the fixed-base GLUON USD reproducibly from the contract-pinned sim
URDF and write a machine-readable provenance manifest.

## Command

```bash
timeout 300s env PYTHONUNBUFFERED=1 \
  /home/cocel/isaac/env_isaaclab/bin/python \
  lab/ddt_lab/scripts/gluon/convert_gluon_urdf_to_usd.py --headless
```

The conversion command was executed twice with `force_usd_conversion=True`.
The generated asset was then checked with:

```bash
timeout 300s env PYTHONUNBUFFERED=1 \
  /home/cocel/isaac/env_isaaclab/bin/python \
  test/test_gluon_urdf_usd_equivalence.py --headless

timeout 300s env PYTHONUNBUFFERED=1 \
  /home/cocel/isaac/env_isaaclab/bin/python \
  test/test_gluon_asset_runtime.py --headless
```

## Importer options

- `fix_base=True`
- `merge_fixed_joints=False`
- `force_usd_conversion=True`
- `make_instanceable=False`
- joint drive `target_type=none`, `stiffness=0`, `damping=0`

## Result

Both forced conversions produced identical hashes:

```text
first_output_usd_hash=a5b9514205ae7b3de4321ab308fc6e8aa4f3b17533c172fe53f7269a5b49a42d
second_output_usd_hash=a5b9514205ae7b3de4321ab308fc6e8aa4f3b17533c172fe53f7269a5b49a42d
first_output_bundle_hash=ac95b231160d0a2b6f08bbd59af3c23e391bb6c8d1a094dc044709e0570577b4
second_output_bundle_hash=ac95b231160d0a2b6f08bbd59af3c23e391bb6c8d1a094dc044709e0570577b4
GLUON_USD_REPRODUCIBILITY: PASS
```

The initial full-bundle check was `SUSPICIOUS`: only the generated
`config.yaml` differed because IsaacLab appended wall-clock time. The wrapper
now normalizes that footer while preserving the actual UTC creation time in
`manifest.json`. All runtime USD layers were byte-identical before and after
this correction.

URDF/USD runtime equivalence evidence:

```text
joint_limit_equivalence,max_abs_error_rad=0.000e+00
usd_contract_joint_limits,max_abs_error_rad=2.384e-07
total_mass_equivalence,error_kg=0.000e+00
q0 position error=1.192e-07 m, orientation error=0 deg
q_local1 position error=5.960e-08 m, orientation error=0 deg
q_local2 position error=8.941e-08 m, orientation error=0 deg
q6_test position error=1.192e-07 m, orientation error=0 deg
q6 position change=2.565e-10 m
q6 orientation change=29.999953 deg
GLUON_URDF_USD_EQUIVALENCE: PASS
GLUON_P0_RUNTIME: PASS
GLUON_ASSET_SMOKE: PASS
GLUON_REACH_ENV_SMOKE: PASS
```

`GLUON_2L6_4L3_CFG` now loads the validated USD and retains the explicit root
rotation and `ImplicitActuatorCfg` simulation baseline.

Repository validation after all P1 changes:

```text
./scripts/agent-check.sh
Python syntax: 284 passed, 0 failed
XML / URDF: 8 files passed
Final result: PASS

## Completion-audit correction

During the final 2026-08-05 audit, the original equivalence test was found to
copy `GLUON_2L6_4L3_CFG` for both articulations after that production config
had been switched to USD loading. It therefore compared USD against USD even
though the instances were labelled URDF and USD. The test was corrected so
the first articulation explicitly uses `UrdfFileCfg` with the contract-pinned
`gluon_2L6_4L3_sim.urdf`, while the second uses the generated USD.

Execution Domain: `VALIDATION_SIM`

```bash
timeout 300s env PYTHONUNBUFFERED=1 \
  /home/cocel/isaac/env_isaaclab/bin/python \
  test/test_gluon_urdf_usd_equivalence.py --headless --device cpu
```

Corrected direct evidence:

```text
equivalence_sources,urdf=.../gluon_2L6_4L3_sim.urdf,usd=.../gluon_2L6_4L3.usd
joint_limit_equivalence,max_abs_error_rad=0.000e+00
total_mass_equivalence,urdf_kg=4.2676115036,usd_kg=4.2676115036,error_kg=0.000e+00
q0_ee_position,error_m=8.941e-08
q_local1_ee_position,error_m=1.192e-07
q_local2_ee_position,error_m=5.960e-08
q6_test_ee_position,error_m=8.941e-08
GLUON_URDF_USD_EQUIVALENCE: PASS
```

The correction preserves the phase result as `PASS`, now with direct
URDF-to-generated-USD evidence rather than an accidental same-source check.
```

## Risks

- `config.yaml` contains absolute local paths emitted by IsaacLab. Byte-level
  reproducibility is proven for repeated conversion in this workspace; a
  different checkout path may change that metadata file.
- Collision boxes remain the conservative Phase-A approximation declared in
  the model contract.
- No real robot, ROS hardware bridge, SDK, or actuator command is in scope.
