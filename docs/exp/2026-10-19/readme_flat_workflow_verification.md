# Root README flat workflow and environment verification

- Execution Domain: `DESKTOP_DRY_RUN`, `TRAINING_SIM`, `VALIDATION_SIM`.
- Policy Checkpoint SHA256: `fb5413bd26b558b5850da0ea327c3b6cd5d8dfd2d85f7b1634849d1bd8ef5057`.
- ONNX SHA256: `5a89428077ea33154872882b21d3e04337cb11f209b58fb96230c1f011d7b389`.
- Evidence Status: `PASS` for flat training/export/finite playback/heading parity and documentation checks; `FAIL` for the legacy whole-workspace build; real-robot rebuild/deployment/runtime `NOT_TESTED`.
- Branch: `agent/codex/promote-tita-flat-cfg`.
- No commit, push, remote deployment, service stop, CAN initialization or robot runtime was performed. ROS `--show-args` only inspected installed launch arguments.

## Documentation changes

`README.md` now documents the canonical `DDT-Velocity-Flat-Tita-v0` FlashSAC workflow: short/full training, saved-checkpoint selection, Isaac playback, verified ONNX preparation, MuJoCo headless/viewer playback, the existing headw0 65k robot bundle and the generic export loader for a newly trained checkpoint. Paths and setup prerequisites distinguish desktop Isaac Python 3.11, desktop MuJoCo/ROS Jazzy Python 3.12, and the robot's previously documented ROS Humble workspace.

The original two setup code blocks are preserved byte-for-byte. Added notes explain that they start independently at the repository root, need the ROS underlay, and do not establish that the legacy whole-workspace build works today. The README distinguishes fixed SHA256-pinned robot bundles from arbitrary new exports and describes the public launch's service stop/recording/MCU effects, including with motor output disabled.

Only authored files in this request: `README.md` and this report. Training/export/playback also generated the evidence summaries listed below and an ignored smoke checkpoint. Existing source/config worktree modifications from previous work were retained. Isolated build/install directories created under `test/` were removed after their logs were recorded; original workspace build/install directories were not rebuilt or removed.

## Environment and setup checks

| Check | Evidence Status | Direct observation |
|---|---|---|
| Isaac package metadata | `PASS` | Python 3.11 environment exists; `isaaclab` extension 0.47.2 is editable from `~/isaac/IsaacLab-v2.3.0/source/isaaclab`; Isaac Sim 5.1.0.0; Torch 2.7.0+cu128. |
| Current `ddt_lab` editable registration | `SUSPICIOUS` | `python -m pip show ddt_lab` reports package not found. Repository training scripts add their own extension path and ran successfully. No installed environment was changed. |
| Editable install metadata dry run | `PASS` | From `lab/ddt_lab`: `python -m pip install --dry-run --no-deps --no-build-isolation --no-index -e . --report ../../docs/exp/2026-10-19/readme_editable_dry_run.json` exited 0: `Would install ddt_lab-0.1.0`. Actual installation and default network-backed build isolation were not tested. |
| MuJoCo runtime dependencies | `PASS` | With `/opt/ros/jazzy/setup.bash` sourced, `~/venvs/cosim_ros2_jazzy/bin/python` imports `mujoco`, `onnxruntime`, `rclpy`, `yaml`, `numpy`. Python 3.12.3, MuJoCo 3.10.0, ONNX Runtime 1.27.0. |
| Legacy ROS source discovery | `PASS` | Jazzy `colcon list --base-paths src` in `tita_gluon_ws` discovers 17 packages. |
| Legacy installed overlay | `FAIL` | After sourcing its existing `install/setup.bash`, `ros2 pkg prefix tita_stage1_controller` reports package not found. `ddt_ros2_control` is a directory grouping multiple packages, not a ROS package selector. |
| Legacy build, sandbox attempt | `BLOCKED` | `readme_legacy_build.log`: GitHub DNS lookup unavailable while fetching lodepng. |
| Legacy build, local host retry | `FAIL` | `readme_legacy_build_host.log`: 3 packages finished, `mujoco_sim_ros2` failed on missing `mujocoConfig.cmake`/`mujoco-config.cmake`, 13 packages not processed. External lodepng fetch succeeded in this retry. Python MuJoCo installation alone did not satisfy this CMake dependency. |
| Installed current TITA launch | `SUSPICIOUS` | `ros2 pkg prefix tita_controller` resolves to local `sim2real/tita_ws/install/tita_controller`. Both installed launches accept `--show-args`, but installed public launch lacks the current source's policy/filter selectors. Rebuild is required before using the documented source's bundle selection. |
| Official installation URL | `PASS` | The existing [official installation page](https://isaac-sim.github.io/IsaacLab/main/source/setup/installation/isaaclab_pip_installation.html) resolves; its current `main` page differs from the installed checkout. Its Python-version notes distinguish Isaac Sim 5.x/Python 3.11 from 4.x/Python 3.10. No upgrade was performed. |

Legacy build command, executed locally with Jazzy sourced and isolated output directories:

```bash
colcon --log-base docs/exp/2026-10-19/readme_legacy_colcon_host build \
  --base-paths tita_gluon_ws/src \
  --build-base test/readme_legacy_build --install-base test/readme_legacy_install \
  --symlink-install --executor sequential
```

Installed/source public launch SHA256 at inspection:

```text
source:    01b243086a14124c1cd5a2642da078909065841fdba30af8554a8bed20c10ddf
installed: 7371e951a267a14ea48d559e078258149bf827f2265ee109fad8c6f108ee533b
```

## Actual flat workflow checks

Smoke checkpoint: `lab/ddt_lab/logs/flash_sac/tita_flash_sac_160631_549105/model_8`. This is an eight-step installation smoke artifact, not a usable locomotion policy or a deployment candidate.

| Check | Evidence Status | Observed metrics / log summary |
|---|---|---|
| Training CLI and sim2sim CLI | `PASS` | Both `--help` commands exit 0; the documented task/step/export/interpreter flags are supported. |
| Isaac FlashSAC training | `PASS` | Canonical flat task, 4 envs, 8 vector steps, 10 learner updates; checkpoint saved. `readme_flat_training_smoke.log`, `tita_flash_sac_160631_549105_summary.md`. |
| ONNX export and parity | `PASS` | `--prepare-only` on the smoke model exits 0; 35 actor observations, 8 outputs; 256 samples, maximum absolute error `4.76837158203125e-06`. `readme_flat_export.log`, `tita_policy_export_160727_234306_summary.md`. |
| MuJoCo finite playback | `PASS` | `--headless --steps 100` exits 0; 100 policy steps, saved leg filter `none`, residual/velocity bias off, viewer threads stopped. `readme_flat_sim2sim.log`, `tita_sim2sim_160815_782219_summary.md`. This does not establish locomotion quality. |
| Python/C++ heading observation parity | `PASS` | `test/sim2real/test_heading_parity.py <smoke-model>/sim2sim/actor`: 4,000 steps, 35 inputs, total max error `1.1920928955078125e-07`, heading max error 0, 17 resets, warmup 0. `readme_flat_heading_parity.log`. No SDK or hardware runtime initialized. |
| Original setup preservation | `PASS` | Extracted the original README's two bash blocks from Git and checked both remain exact substrings of the edited README. |
| README shell syntax | `PASS` | All 17 bash blocks checked with `bash -n`. Relative documentation/code links were checked for existence. |

Final repository validation: `./scripts/agent-check.sh`, direct output in `readme_flat_agent_check.log`. Final README/report diff inspection separates this request's documentation changes from the pre-existing worktree modifications.

Not tested: clean-machine Isaac or ROS installation, actual `pip install -e .`, newly documented MuJoCo environment creation, full 100k-step training, viewer keyboard interaction, SBC build, SSH/copy/deployment, or any physical robot commands. Existing 65k real-run position-hold and turning limitations remain unchanged. The legacy build dependency failure is documented; fixing that workspace is outside this documentation request.
