# FlashSAC vs Fixed M4 — 1 / 5 / 15 minute drift videos

Date: 2026-10-16 (Asia/Seoul)

Execution Domain: **VALIDATION_SIM**; artifact/repository checks: **DESKTOP_DRY_RUN**.

Policy Checkpoint SHA256: `6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05`

ONNX SHA256: `f44f07ed44970e3ff565eae67fd9229adf0be5c02215591c52a691ffcbb71b2a`

Evidence Status: **PASS** — both continuous 900-second rollouts, matched initial state, trajectory audit and all three MP4 verifications. **FAIL** — repository agent-check from pre-existing whitespace errors. Hardware is **NOT_TESTED**.

## Videos and observed drift

Left: FlashSAC only. Right: FlashSAC + Fixed M4 Residual LQR. Real-time playback, 10 fps, H.264 / yuv420p, 1280 × 1000. Each clip includes the exact endpoint frame, adding 0.1 s to its playback duration.

| Simulation horizon | Video | FlashSAC final distance | Fixed M4 final distance | Fixed M4 maximum distance |
|---|---|---:|---:|---:|
| 60 s | [1 minute](fixed_m4_drift_videos/flashsac_vs_fixed_m4_01min.mp4) | 0.929398 m | 0.015466 m | 0.022468 m |
| 300 s | [5 minutes](fixed_m4_drift_videos/flashsac_vs_fixed_m4_05min.mp4) | 5.360065 m | 0.215878 m | 0.215878 m |
| 900 s | [15 minutes](fixed_m4_drift_videos/flashsac_vs_fixed_m4_15min.mp4) | 16.147370 m | 0.671575 m | 0.671575 m |

Distance means `norm(base_link_xy(t) - base_link_xy(0))`, measured from the common start of the displayed experiment. It is planar Euclidean displacement, not cumulative travel, encoder position, or the previous 180-second longitudinal IAE. Both panels use the same world camera and graph scale within each video; camera/plot bounds fit that video's full horizon. Yellow crosses/dots mark the start, colored trails show motion, and the follow camera provides equal-magnification posture detail. Render-only trails never contact the robot.

`yaw total` is signed, unwrapped cumulative yaw change from the start:

| Horizon | FlashSAC yaw total | Fixed M4 yaw total |
|---|---:|---:|
| 60 s | −3.77° | −5.02° |
| 300 s | −17.36° | −25.37° |
| 900 s | −79.41° | −250.66° |

The last M4 value corresponds to a final heading offset of +109.34° modulo 360°. **Position drift decreases, but heading drift remains and is larger for M4 in this trial.** These videos do not demonstrate strict absolute position/orientation hold or hardware safety.

## Matched simulation setup

- Frozen `tita_flash_sac_115632_883848/model_60000`; nominal flat-floor MuJoCo, seed 270, pitch perturbation 0, zero velocity/yaw commands, no external disturbance.
- Reuse the existing research Runner for stand-up and a common 8-second FlashSAC-only RL prefix. Restore an identical snapshot for each controller; start the displayed clock and position origin after that prefix. Each controller runs continuously for 900 s; shorter videos show the corresponding prefixes of those same runs.
- Both actors use the Runner's refreshed current IMU clone, keeping sensor timing equal to isolate the residual effect. This is the synchronized research comparison, not a claim of identical cached sensor timing to the no-flag ROS CLI.
- Fixed M4 uses the production `ResidualWheelLQR` class: fixed K/reference/bias, bias 0.4828 Nm, correction ±0.05 Nm, 1.5 s correction ramp, total slew 2 Nm/s, signed equal wheel split and existing effort limits. Its output is applied through the existing native PD/policy Runner callback; per-step comparison with the production `apply()` method is asserted. No online estimation, probing or adaptation.
- Ground-truth base position is used only for evaluation/rendering. The controller uses encoder/IMU observations, previous raw policy actions, and native leg position/velocity.
- The Runner disables non-floor world obstacle contacts identically in both groups, as in the earlier nominal M4 experiments. Videos hide those inactive obstacles. No deployment, ROS transport, robot commands, or hardware were involved.

## Executed checks and evidence

- Both rollouts completed **900 s / 45,000 control transitions**, with no existing fall/attitude/height/joint-limit failure. Each trace retains 45,001 sensor/action/base samples at 20 ms and 9,001 physics poses at 100 ms.
- [Trajectory audit](fixed_m4_drift_videos/trajectory_audit.json): exact initial qpos/qvel/action/base equality; finite state; residual slew ≤0.04 Nm per control step, bounded input, and requested/applied residual agreement within 1e-6 Nm. Independent `math.hypot` endpoint metrics match the report. Wheel effort bounds were asserted at every collected control step.
- [Metrics](fixed_m4_drift_videos/metrics.json), [FlashSAC status](fixed_m4_drift_videos/group_0_status.json), [M4 status](fixed_m4_drift_videos/group_1_status.json), and raw `group_0.npz` / `group_1.npz` are retained.
- Renderer restores recorded qpos/qvel into separate MuJoCo data and asserts that rendered base position matches the recorded evaluation position at every frame. The original physics is never advanced or modified during rendering.
- [1-minute verification](fixed_m4_drift_videos/video_60_verification.json): **601 frames / 60.1 s, PASS**. [5-minute verification](fixed_m4_drift_videos/video_300_verification.json): **3,001 frames / 300.1 s, PASS**. [15-minute verification](fixed_m4_drift_videos/video_900_verification.json): **9,001 frames / 900.1 s, PASS**. Each JSON records the video SHA256, NVIDIA renderer, frame count, codec and ffprobe output.
- First/last PNG frames are retained for visual review. All three endpoints were visually inspected for panel alignment, readable metrics, start markers, camera scale and matching posture magnification. The long-horizon fixed world view necessarily shows a smaller robot; equal-magnification follow views and quantitative plots retain the detail.
- Initial collection saved both complete trajectories before a NumPy 1.26 `trapezoid` summary error. The compatible `trapz` summary stage was then rerun against those unchanged data. The original collection log preserves the error. Slow/interrupted rendering attempts were replaced by the final GPU renders; attempt logs remain, and partial preview MP4s were removed.
- [Agent-check](fixed_m4_drift_videos/agent_check.log): **FAIL** due to six pre-existing trailing-whitespace lines in `lab/ddt_lab/ddt_lab/tasks/manager_based/locomotion/robots/tita/my_flat_env_cfg.py` (431/437/443/449/455/461). Python syntax **459 passed / 0 failed**, URDF XML **8 passed**. No unrelated source was edited. Task source whitespace and protected source/policy hash checks passed.

## Changed files and reproduction

Only one new test/render script was added: `test/render_fixed_m4_drift_comparison.py`. Other additions are this report and the experiment artifacts under `docs/exp/2026-10-16/fixed_m4_drift_videos/`. The production policy, residual controllers, launchers and Runner sources were read-only and protected by [before](fixed_m4_drift_videos/source_hashes_before.json) / [final](fixed_m4_drift_videos/source_hashes_final.json) hashes. [Task source diff](fixed_m4_drift_videos/task.diff) was reviewed.

For a new output directory under a date-only experiment directory, copy/create a plan before collection. Collection refuses to overwrite traces and rendering refuses to overwrite its MP4.

```bash
PYTHONDONTWRITEBYTECODE=1 MPLCONFIGDIR=/tmp/lqr_mpl OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 \
/home/cocel/venvs/cosim_ros2_jazzy/bin/python test/render_fixed_m4_drift_comparison.py \
  --output docs/exp/2026-10-16/NEW_OUTPUT --stage collect

__EGL_VENDOR_LIBRARY_FILENAMES=/usr/share/glvnd/egl_vendor.d/10_nvidia.json \
MUJOCO_GL=egl PYTHONDONTWRITEBYTECODE=1 MPLCONFIGDIR=/tmp/lqr_mpl \
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 \
/home/cocel/venvs/cosim_ros2_jazzy/bin/python test/render_fixed_m4_drift_comparison.py \
  --output docs/exp/2026-10-16/NEW_OUTPUT --stage render --duration 60
```

Repeat rendering with `--duration 300` and `--duration 900`. The GPU render required sandbox escalation to access the local NVIDIA graphics driver; automatic review allowed it. No user confirmation or robot authorization was requested. `--stage summarize` regenerates metrics from already saved traces.

Remaining limitations: one matched initial condition, nominal simulation only, and no statistical generalization or strict station-keeping claim. Branch: `agent/codex/dev_tita_gluon`. No commit, push or PR.
