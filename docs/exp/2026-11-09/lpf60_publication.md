# LPF60 residual stack and selected checkpoint publication

- Execution Domain: DESKTOP_DRY_RUN / VALIDATION_SIM.
- Evidence Status: PASS for the executed source, bundle, native simulation and build checks below. Hardware operation and policy-quality certification: NOT_TESTED.
- Teacher Checkpoint SHA256: `5487e3584fddbdfc87b7485bb2ad4c7da8069a7679b1975789d64419e7482334`.
- Residual Checkpoint SHA256: `d6672529ee247a92b7043f50bb6deb501a65becbf760761a412b33d5701b6002`.
- Preparation branch: `agent/codex/publish-lpf60-stack`, based on `60195758fa200e0d904434379fa0f013bde19f8c`.
- Publication target: `main`, explicitly requested by the user. Preparation, edits and tests were performed in an isolated worktree; the live working branch and staging index were preserved. No force push or hardware deployment is part of this task.

## Published behavior and files

Native mjlab environments are grouped into common, residual, roll_pitch_height,
walk, sit_stand and stand_one_leg packages. Legacy imports/pickles retain module
aliases; flat_env_cfg.py is unchanged. The shared-sensor torque training runner
supports saved residual-only LPF60, with Teacher50Hz, residual250Hz and fresh
PD/physics/filter500Hz, then effort clipping and common post-PD torque delay.

The exact selected Teacher80k/residual10k bundles, native sidecars and existing
hash-validated hardware ONNX exports are included under sim2sim/checkpoints and
sim2real/checkpoints. Identical binary contents share Git blob objects. No other
checkpoint histories or experiment datasets are added. The residual registry is
a playback bundle, not a residual optimizer/replay resume checkpoint.

Public configs select this pair. A small tracked learner reference replaces the
local docs/exp configuration dependency in the fresh10k training command. The
mjlab install metadata excludes the unrequested BFM package. The shared FlashSAC
play helper, sim2sim runtime and Sim2Real ROS sources are synchronized with the
current implementation. Required prebuilt amd64/arm64 SDK libraries are included
unchanged with their Apache-2.0 license and notice; other build outputs remain
ignored. Existing root hardware ONNX/config/manifests remain byte-identical;
relocated native sim2sim exports regenerate in ignored per-checkpoint caches.

[The execution guide](../../lpf60_residual.md) contains exact installation,
training, simulation and build commands. Publishing/building does not authorize
robot operation, and the real launcher is not run during these checks.

## Direct verification

1. Published-pair portable pytest: **4 passed**, one existing native mass-only
   DR warning. Checks every bundle file hash in both stores, matching Teacher/
   residual export contract, selection paths, exact learner reference and twelve
   finite native GPU residual steps with the published Teacher.
2. Native task regressions: **107 passed, 8 skipped, 1 deselected** in85.60s.
   Covers flat/walk, inline, pose, sit/stand, height-only, left/right reference/
   anchor and support tasks. Flat-fixture walk-only checks skip; the large4096-
   world case was explicitly deselected. The12 warnings are existing native
   mass-without-inertia randomization warnings.
3. Relocated sim2sim: **1000 control steps PASS**, final RL state,4450 residual
   inferences, LPF60 restored and matched to training. ONNX parity on256 samples:
   max absolute error3.933906555175781e-6. No viewer threads remained. This
   establishes execution, not balance/locomotion quality.
4. Standalone C++ LPF/ORT test: **PASS**. Filter500Hz with held250Hz requests,
   bypass, gate/expiry/epoch reset, shared440-frame mapping, requested pre-filter
   history and measured wheel odometry checked without SDK/CAN/robot execution.
5. Full x86_64 ROS build: **4 packages finished** (ros_utils, tita_robot,
   teleop_command, tita_controller),4min59s. CMake/header-install warnings only.
   The first build exposed missing SDK shared-library files; the licensed
   dependencies were added and the build rerun successfully. ONNX Runtime used
   an existing local copy of the CMake-pinned dependency, avoiding a redundant
   download. No generated controller or SDK example executable was launched.
6. Repository completion gate: `./scripts/agent-check.sh`; direct local output
   in `lpf60_publication_agent_check.log`. Final staged diff and scope reviewed.

Validation was explicitly local/offline; no new W&B training/evaluation run was
started by publication. Source training: [jv68rep7](https://forge.coreweave.com/wandb/bjy6614-postech/tita_sac_residual_amp/runs/jv68rep7).
Existing thesis comparison experiments in the original workspace remain active
and their results are not included or represented as completed by this change.

## Scope and limits

Only requested training/task/runtime code, selected pair, necessary dependencies,
regression tests and publication documentation are staged. Existing read-only
real2sim, fine-tuning and legacy FlashSAC launch files/entrypoints are preserved
from main; local cleanup deletions are excluded from this publication. BFM, datasets,
training histories, current thesis trial data and build/install/cache outputs
are excluded. The staged payload has about45.7MB of unique file content before
Git compression; individual files are below GitHub's100MB limit.

The ARM64 library is included but no ARM64 build or hardware operation was
performed. Stored absolute source paths are provenance; relocation was tested
through the fresh native export. A fixed checkpoint's observed simulation
behavior does not establish generalization or sim-to-real quality. Local logs
and detailed JSON scope receipts are retained in this worktree rather than
publishing unrelated experiment histories.
