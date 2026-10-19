# Robot asset layout

Execution Domain: DESKTOP_DRY_RUN; GLUON runtime validation: VALIDATION_SIM.
Evidence Status: PASS for the executed checks below.
Policy Checkpoint SHA256: N/A (asset relocation; no policy trained or deployed).
Branch: `agent/codex/dev_tita_gluon`. No commit, push or hardware command.

## Result and changed files

Robot assets now live in `sim2sim/robot/{tita,gluon,tita_gluon}/`:

- `tita/urdf/tita.urdf` and `tita/meshes/`, with minimal ROS asset package
  metadata (`tita_urdf`).
- `gluon/`: canonical/sim URDF, source URDF, meshes, USD, model contract,
  generators and the existing `gluon_2l6_4l3_urdf` package metadata.
  `gluon_2L6_4L3_assembly.urdf` preserves the distinct combined-model variant.
  The legacy model is `urdf/gluon.urdf` with `meshes/legacy/`.
- `tita_gluon/`: the two combined URDFs, USD, generators and existing
  `tita_gluon_urdf` ROS viewer launches. Combined models reference the sibling
  TITA/GLUON meshes. Seven verified-identical mesh copies were deduplicated.

Removed the old top-level `sim2sim/gluon_2L6_4L3_urdf/` and
`sim2sim/tita_gluon_urdf/` directories by moving their contents.
Updated `lab/ddt_lab/ddt_lab/assets/{gluon,tita_co_rl}.py`, the combined task's
`env_cfg.py`, `scripts/gluon/convert_gluon_urdf_to_usd.py`, and seven model
consumers in `test/`. Updated asset generators/viewers, USD provenance paths,
calibration relative path and bundle hashes, both READMEs, and the active
Cartesian graph's three resource path/hash metadata fields. Graph coordinates,
nodes, edges and joint data are unchanged. Added `robot/README.md` and the
relocation verifier `test/check_robot_asset_layout.py`.

Only mesh resource filenames were changed in URDF bodies. Joint names/order,
transforms, masses, inertias, limits and collision geometry were preserved.
Standalone and combined GLUON variants were kept separate because their
physical definitions differ. Existing ROS viewer commands remain available.

Before-task backup: `robot_urdf_layout_before.tar.gz`, SHA256
`43b8599cb6691e0bf81473c7db298e18e24a2152f33af2e5a5da3bac8b7d38b9`.
Active graph metadata is separately backed up in
`robot_urdf_graph_metadata_before.tar.gz`.

## Observed metrics / behavior / log summary

| Executed check | Evidence |
| --- | --- |
| All eight URDFs, complete XML model semantics before/after | PASS |
| Runtime-model mesh contents and paths | PASS, 104 mesh references have identical bytes |
| Two combined URDF generators | PASS, reproduce the stored model semantics and resolve all meshes |
| ROS package build | PASS, three packages (`robot_urdf_build.log`) |
| Five installed viewer launch descriptions | PASS, --show-args and evaluated descriptions; 83 mesh references resolve (`robot_urdf_layout_checks.log`) |
| Existing GLUON IK tests | PASS, 19 tests (`robot_urdf_ik_tests.log`) |
| Existing GLUON Isaac Lab asset runtime test | PASS, 16 checks, zero failures (`robot_urdf_gluon_runtime.log`) |

Native GLUON metrics: total mass 4.2676115036 kg; maximum joint-limit error
2.384e-7 rad; fixed-base drift 0.0 m; home end-effector error 1.949e-7 m.

Unchanged GLUON asset hashes:

- Canonical URDF: `eb6bbc1f2305fac3da832a911f00efbc82b5c7af57d905b3008bc5531707089e`.
- Sim URDF: `b9b25074b7a417a9e499f14fee852699ac6f8a00ab4b137f90ec843eccc8ede4`.
- USD: `a5b9514205ae7b3de4321ab308fc6e8aa4f3b17533c172fe53f7269a5b49a42d`.

Required final gate: `./scripts/agent-check.sh`, recorded in
`robot_urdf_agent_check.log`. The task-relative diff was inspected against the
backup contents (`robot_urdf_layout_task_relative.diff`). Unrelated source and
hardware files were preserved; no pre-existing changes were reverted/staged.

## Limits

The historical `left_gravity_source.urdf` is generator input and retains its
original package URIs; it is not a runtime model. Historical reports and saved
reachability artifacts retain their original provenance paths/hashes. Combined
URDF byte hashes change because mesh filenames changed; the existing strict
reachability-cache hash check remains enabled, so old caches must be regenerated
before rebuilding a graph against the relocated URDF. The live graph's numeric
data was preserved and its resource metadata updated after semantic equivalence
verification. Full retraining and hardware execution remain NOT_TESTED.
