# TITA training asset comparison and relocation

- Date: 2026-10-19 (Asia/Seoul)
- Execution Domain: DESKTOP_DRY_RUN; target consumer is TRAINING_SIM.
- Policy Checkpoint SHA256 / ONNX Hash: N/A; no policy was loaded, trained, or exported.
- Evidence Status: PASS for source comparison, mesh comparison, isolated conversion tests, and agent check.
- Branch: `agent/codex/real2sim-interview-pt`.

## Historical source and comparison

The deleted source was read from the local Git object database without restoring
the removed workspace:

- Commit: `c8c159d37a6760916ed22a4d029961762bbde7a9` (parent of the workspace-removal commit).
- Path: `tita_gluon_ws/src/ddt_ros2_control/urdfs/tita_description/urdf/robot.urdf`.
- Git blob: `a682fbdd9560c429bfd57148e828fb169d0324e3`.
- Historical URDF SHA256: `0941b83136cd5c8c89bbb33165bff515a3a988d33319b67c8b06bfb9c71350ce`.
- Current path: `sim2sim/robot/tita/urdf/tita.urdf`.
- Current URDF SHA256: `6f0678b23a537e2e8ad9948ab994cb9fa50b91699cf04847b60a769da6b9bf07`.

These files are not byte-identical. The complete XML matches after accounting
for exactly these representational differences:

1. Nine mesh references use `../meshes/` instead of `package://tita_description/meshes/`.
2. Four fixed joints are renamed: `spad`, `spad1`, `left_camera`, and `ch201`
   acquire the `_joint` suffix. Their parent/child links, transforms, and types match.
3. Both leg-3 `iyy` values lose trailing whitespace (`0.004094 ` -> `0.004094`).

Masses, inertias, origins, collision geometry, all eight movable joints, limits,
and the remaining XML match. All nine referenced STL files are byte-identical
to the corresponding historical Git blobs. This establishes source-level
physical-model equivalence, while preserving the explicit fixed-joint name
difference. No references to those four joint names were found in training
Python code; the training asset config also has `merge_fixed_joints=True`.

## Changed files and behavior

- `lab/ddt_lab/ddt_lab/assets/ddt_robot.py`: TITA's `asset_path` now resolves to
  the tracked `sim2sim/robot/tita/urdf/tita.urdf`. D1's existing path is unchanged.
- `lab/ddt_lab/ddt_lab/tasks/manager_based/locomotion/robots/tita/real2sim/env_cfg.py`:
  `sphere_wheel_urdf` makes relative mesh paths absolute relative to the source
  URDF before writing the cached copy; legacy package paths remain supported.
- `test/test_tita_training_asset.py`: historical comparison and regression checks.
- This report and associated logs under `docs/exp/2026-10-19/`.

Data flow: the TITA environment imports `DDT_TITA_CFG`, passes its source path to
`sphere_wheel_urdf`, and gives the resulting cached URDF to the Isaac Lab importer.
The cache can therefore resolve every mesh outside the original source directory.
Only the existing wheel-cylinder-to-sphere conversion changes collision geometry.
Other pre-existing working-tree diffs were compared with the task-start snapshot
and remained byte-identical. No sim2sim source assets were edited.

## Observed metrics / log summary

- `python3 test/test_tita_training_asset.py HistoricalAssetTest`: PASS, 2 tests.
  [Comparison output](tita_asset_comparison.log).
- `python3 test/test_tita_training_asset.py`: PASS, 5 tests, including both mesh
  path styles, cache reuse, target asset selection, unchanged non-wheel model
  data, and same-radius sphere conversion.
  [Test output](tita_training_asset_tests.log).
- `./scripts/agent-check.sh`: PASS, exit 0; 676 Python syntax checks and 8 URDF
  XML parses passed; diff integrity and experiment directory checks passed.
  [Agent check output](tita_training_asset_agent_check.log).

## Limits

Isaac Sim import/physics execution and full FlashSAC training: NOT_TESTED. The
conversion tests execute the actual helper extracted via AST without starting
Isaac Sim; they do not establish runtime importer equivalence or policy quality.
Fixed-joint names differ, so external consumers referring to the old names would
need review. No robot commands, commits, pushes, or hardware deployment.
