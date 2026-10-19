# Static CoM / mass / friction — five-minute FlashSAC vs Fixed M4 videos

Date: 2026-10-16 (Asia/Seoul)

Execution Domain: **VALIDATION_SIM**; source/artifact checks: **DESKTOP_DRY_RUN**.

Policy Checkpoint SHA256: `6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05`

ONNX SHA256: `f44f07ed44970e3ff565eae67fd9229adf0be5c02215591c52a691ffcbb71b2a`

Evidence Status: **PASS** — six 300-second rollouts, paired initial-state equality, actual physics/contact checks, nominal regression and three MP4 verifications. **FAIL** — repository agent-check due to six pre-existing whitespace errors. **NOT_TESTED** — hardware, other initial conditions, combined perturbations or retuned controllers. Simulation completion PASS is not a station-keeping success claim.

## Videos and observed metrics

All videos are 1x playback, 10 fps, 1280 × 1000 H.264/yuv420p, 3,001 frames / 300.1 seconds including the exact 300-second endpoint. Left is frozen FlashSAC only; right adds the production frozen M4 residual. The condition is printed above both panels. Yellow marks show the initial position; world camera, trajectory and distance scales are equal within each pair; follow views have equal posture magnification. Fog is disabled so distant trails remain visible. Large travel ranges necessarily make the robot smaller in the fixed world view.

| Condition / video | FlashSAC final distance | Fixed M4 final distance | FlashSAC maximum distance | Fixed M4 maximum distance |
|---|---:|---:|---:|---:|
| [base_link CoM +5 mm along local X](fixed_m4_mismatch_videos/com_plus_5mm/flashsac_vs_fixed_m4_05min.mp4) | 9.979364 m | 4.586855 m | 9.979364 m | 4.586855 m |
| [All non-world body mass/inertia +15%](fixed_m4_mismatch_videos/mass_plus_15pct/flashsac_vs_fixed_m4_05min.mp4) | 26.107037 m | 28.974705 m | 26.107037 m | 28.974705 m |
| [Floor + wheel sliding friction μ=0.2](fixed_m4_mismatch_videos/friction_mu_02/flashsac_vs_fixed_m4_05min.mp4) | 0.527083 m | 0.004936 m | 1.462152 m | 0.015722 m |

Distance is the planar Euclidean distance of `base_link` from the common displayed starting position, not cumulative travel. The low-friction FlashSAC path returns closer to its start after traveling a loop; its 0.527 m endpoint must be read together with the 1.462 m peak and trajectory. These values are not the earlier longitudinal position IAE.

| Condition | FlashSAC cumulative yaw | Fixed M4 cumulative yaw |
|---|---:|---:|
| CoM +5 mm | −12.14° | −19.73° |
| Mass/inertia +15% | −44.28° | −41.33° |
| Sliding μ=0.2 | −402.19° | −437.09° |

`yaw total` is unwrapped cumulative yaw change. **The fixed nominal M4 reduces drift in the CoM case, increases it in the +15% mass case, and has small translational drift but large heading drift in the low-friction case.** In the mass case both controllers also travel in the opposite longitudinal direction to the earlier nominal example. No gain/bias/reference was retuned after seeing these results. Each condition has one matched initial-condition pair; no statistical robustness or hardware conclusion is drawn.

## Frozen setup and physical meaning

The user selected the existing experiment range. The three cases were frozen in [plan.json](fixed_m4_mismatch_videos/plan.json) before collecting outcomes, using the prior `test/run_static_target_adaptation.py` condition values. One factor changes per case; all other model arrays match the nominal model exactly.

- CoM: shift only `base_link`'s inertial CoM by +0.005 m along its local X axis. This is a **body CoM** change, not a 5 mm shift of the entire robot CoM. At the same configuration it shifts the whole-robot CoM by about **2.2115 mm**. Body mass, inertia about the translated CoM, mesh and joint frames remain unchanged.
- Mass: scale every non-world body mass and principal inertia by 1.15, preserving CoM locations. Total model mass changes from **25.69095789 kg to 29.54460157 kg**. This is uniform mass scaling, not a localized payload model.
- Friction: set both floor and wheel geometry sliding coefficients to **0.2**; nominal floor μ is **1.0**. Other friction components and other geometries are unchanged. Actual floor-wheel contact friction at the displayed start was checked to be 0.2, rather than assuming that changing one geom changes the effective contact.

`StaticRunner` / `StaticEnv` apply each target **before the first startup physics step** and preserve it through stand-up, a common 8-second FlashSAC-only RL prefix, snapshot branching and the full 300-second comparison. Within each condition both controllers restore the same physics, estimator/history and motor-state snapshot. Across different conditions startup is allowed to evolve differently under its own physics; those starting states are not claimed to be identical.

Both actors use the existing research Runner's refreshed IMU sensor clone. The 24-state production `ResidualWheelLQR` uses nominal fixed K/reference/bias, 0.4828 Nm bias, ±0.05 Nm correction, 1.5-second correction ramp, total slew 2 Nm/s and native wheel effort limits. The previous raw policy action is passed causally. There is no RLS, probing, gain selection, reference or bias adaptation. Native policy leg/wheel PD remains active. Ground-truth position is used for evaluation/rendering only.

The same non-floor world obstacles are disabled as in the earlier nominal videos. No physical robot commands, deployment or ROS message transport were used.

## Executed verification

- **PASS:** six full 300-second trajectories / 90,000 total control transitions; no existing fall, attitude, height or joint-limit stop. Native and physical motor arrays were asserted equal at every control step; signed residual application was checked against the production `apply()` method, with per-wheel effort ≤12 Nm.
- **PASS:** [physics_audit.json](fixed_m4_mismatch_videos/physics_audit.json) independently compares actual mass/inertia/CoM/friction arrays against the nominal model plus exactly one planned change. Actual floor-wheel contacts are included. Per-condition `physics.json` and `model_physics.npz` retain the target, total mass, startup timing and model fingerprint.
- **PASS:** [trajectory_audit.json](fixed_m4_mismatch_videos/trajectory_audit.json): 15,001 state samples and 3,001 render poses per group; exact paired initial sensor/action/qpos/qvel/base state; finite data; residual magnitude/slew constraints; applied/requested residual agreement; independent `math.hypot` endpoint metrics. Physics fingerprints remain fixed through both branches.
- **PASS:** a no-change `StaticRunner` reproduces the previous nominal video's actions and physics exactly for 5 seconds after the common prefix. This checks that the static-physics wrapper itself does not introduce a nominal control difference.
- **PASS:** all three renderers use the same recorded physical model fingerprint, restore recorded qpos/qvel into separate MuJoCo data, and verify rendered base position against trajectory data at every frame. No physics is stepped during rendering.
- **PASS:** frame count, video length and codec checked with ffprobe. Per-condition `video_300_verification.json` records 3,001 frames, 300.1 seconds, NVIDIA RTX 3090 renderer, target/model fingerprint and MP4 SHA256. All three final PNG frames were visually inspected for condition labels, metrics, matched scales and posture views.
- **FAIL:** [agent_check.log](fixed_m4_mismatch_videos/agent_check.log) from existing trailing whitespace in `lab/ddt_lab/ddt_lab/tasks/manager_based/locomotion/robots/tita/my_flat_env_cfg.py`, lines 431/437/443/449/455/461. Python syntax **460 passed / 0 failed**, URDF XML **8 passed**. The unrelated file was not edited.

The GPU render required sandbox escalation for the local NVIDIA graphics device; automatic review allowed it. No user approval was needed for robot access because none was performed.

## Changes and reproduction

- New `test/render_fixed_m4_mismatch_comparison.py`: paired static-physics collection and reuse of the existing renderer.
- Updated `test/render_fixed_m4_drift_comparison.py`: optional summary horizons, renderer environment factory, visible condition/footer text and disabled rendering fog. The nominal collection/controller path and existing media files were preserved.
- Added this report and artifacts under `docs/exp/2026-10-16/fixed_m4_mismatch_videos/`. No production/controller/launcher/physics helper source was edited. The original renderer is saved as `renderer_before.source.txt` for the task diff; protected files are hash-checked.

Use a fresh output root with the same reviewed plan and condition subdirectories; collection/rendering refuses to overwrite trajectories/MP4s.

```bash
PYTHONDONTWRITEBYTECODE=1 MPLCONFIGDIR=/tmp/lqr_mpl OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 \
/home/cocel/venvs/cosim_ros2_jazzy/bin/python test/render_fixed_m4_mismatch_comparison.py \
  --output docs/exp/2026-10-16/NEW_OUTPUT --condition com_plus_5mm --stage collect

__EGL_VENDOR_LIBRARY_FILENAMES=/usr/share/glvnd/egl_vendor.d/10_nvidia.json \
MUJOCO_GL=egl PYTHONDONTWRITEBYTECODE=1 MPLCONFIGDIR=/tmp/lqr_mpl \
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 \
/home/cocel/venvs/cosim_ros2_jazzy/bin/python test/render_fixed_m4_mismatch_comparison.py \
  --output docs/exp/2026-10-16/NEW_OUTPUT --condition com_plus_5mm --stage render
```

Repeat with `mass_plus_15pct` and `friction_mu_02`. Branch: `agent/codex/dev_tita_gluon`. No commit, push or PR.
