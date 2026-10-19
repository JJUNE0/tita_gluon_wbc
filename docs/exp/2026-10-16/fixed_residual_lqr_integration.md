# Fixed M4 residual LQR — minimal Sim2Sim integration

Date: 2026-10-16 (Asia/Seoul)

Execution Domain: **VALIDATION_SIM**; repository checks: **DESKTOP_DRY_RUN**.

Policy Checkpoint SHA256: `6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05`

ONNX SHA256: `f44f07ed44970e3ff565eae67fd9229adf0be5c02215591c52a691ffcbb71b2a`

Evidence Status: **PASS** — targeted tests, reference controller parity and finite CLI execution. **FAIL** — repository agent-check due to six pre-existing whitespace violations. **SUSPICIOUS** — DDS socket/interface permission errors in this sandbox; external ROS message transport was not verified. **NOT_TESTED** — 180-second drift benchmark, GUI, hardware and Sim2Real.

## Behavior and execution path

`real2sim.launch.py` launches a read-only hardware-state mirror without policy or torque application. Following the requested Sim2Sim purpose, `--fixed_residual_lqr` is added to **sim2sim.launch.py** and its existing CLI. The path clarification was asked asynchronously; with no reply, the stated Sim2Sim assumption was used. No real2sim or hardware path was changed.

CLI flag → runtime ROS parameter → Sim2SimNode → ResidualWheelLQR update using the previous raw actor action → frozen FlashSAC inference using the same refreshed sensor clone → native leg/wheel PD at each physics substep → bounded additive wheel torque.

The 24-state order is encoder position/velocity, IMU Euler pitch/pitch derivative, previous raw policy action8, native leg position6/velocity6. The M4 indices in the archived 25-state M4/M5 bundle omit yaw rate. K/reference are copied exactly from `docs/exp/2026-10-15/flash_overnight_pipeline/run_final/gains_frozen.json`, model `M4`; runtime does not load experiment artifacts or recompute K/A/B/c. Only the matching model_60000 checkpoint SHA and 20 ms control period are accepted.

Total wheel residual is `0.4828 - K @ (z - reference)`, with the feedback correction clipped to ±0.05 Nm and smoothed over 1.5 s; the total including bias starts from zero with 2 Nm/s slew. Signed torque is split equally between the wheels and clipped to existing per-wheel effort limits. Online RLS, probing, gain/reference/bias adaptation are absent. Existing PD command hysteresis, encoder/IMU estimation and torque application are shared. Each zero-command hold captures its position origin once; movement commands release the residual through slew, and leaving RL/reset clears it immediately.

## Changed files

- `sim2sim/sim2sim_ros2_jazzy/sim2sim_ros2_jazzy/residual_wheel_lqr.py`: frozen M4 implementation, 63 lines.
- `sim2sim/sim2sim_ros2_jazzy/sim2sim_ros2_jazzy/residual_wheel_pd.py`: extract the target calculation as a method to reuse existing estimation/gating/torque logic.
- `sim2sim/sim2sim_ros2_jazzy/sim2sim_ros2_jazzy/sim2sim_node.py`: opt-in M4 construction and causal previous-action delivery.
- `sim2sim/sim2sim_ros2_jazzy/sim2sim_ros2_jazzy/cli.py`: mutually exclusive PD/M4 flags, parameter forwarding and run evidence.
- `sim2sim/sim2sim_ros2_jazzy/launch/sim2sim.launch.py`: CLI/ROS launch option.
- `test/test_fixed_residual_lqr.py`: integration and numerical regression checks.
- This report, task diff, verification logs and generated CLI run JSON/summary in this date directory.

Pre-existing untracked runtime files were snapshotted before editing. Changes are additive to that baseline; existing unrelated work was preserved. The reviewed task diff is [fixed_residual_lqr_integration.diff](fixed_residual_lqr_integration.diff).

## Observed metrics / behavior / log summary

- **PASS:** four tests in [fixed_residual_lqr_tests.log](fixed_residual_lqr_tests.log). Frozen constants match the archived M4 exactly. Over 60 seconds / 3,000 closed-loop steps after the original 8-second prefix, residual output differs from the original control equation by at most **2.09e-9 Nm** on the same evolving states. Sensor-cache preservation, previous-action alignment and signed wheel application are checked. This is equation/estimator parity, not an exact archived-trajectory or 180-second IAE reproduction.
- **PASS:** disabling both residual flags produces exactly the original pre-residual node's state, motor command and action traces for 500 steps. Enabled actual-node tests cover additive wheel torque, unchanged leg torques, effort bounds, movement release, re-entry, reset and checkpoint rejection. CLI and ROS launch forwarding and conflicting option rejection are tested.
- **PASS:** existing `ResidualTests` regression suite, three tests, in [fixed_residual_lqr_pd_regression.log](fixed_residual_lqr_pd_regression.log). The log preserves an initial failed unittest module lookup; rerunning the existing test file directly selected and passed all three tests.
- **PASS:** end-to-end CLI headless 700 control steps; `fixed_residual_lqr=true` and clean teardown recorded in [fixed_residual_lqr_cli_smoke.log](fixed_residual_lqr_cli_smoke.log). This includes startup and is a finite playback check.
- **FAIL:** [agent-check log](fixed_residual_lqr_agent_check.log), from pre-existing trailing whitespace at lines 431/437/443/449/455/461 of `lab/ddt_lab/ddt_lab/tasks/manager_based/locomotion/robots/tita/my_flat_env_cfg.py`. Python syntax: **458 passed, 0 failed**; URDF XML: **8 passed**. Task source/test whitespace checked independently: PASS. The unrelated file was not edited.

## Reproduction

Interactive viewer from the repository root:

```bash
python3 sim2sim/sim2sim_ros2_jazzy/launch/sim2sim.launch.py \
  --ckpt lab/ddt_lab/logs/flash_sac/tita_flash_sac_115632_883848/model_60000 \
  --fixed_residual_lqr
```

Press `1` for stand-up, wait for sit, then `0` for RL. `w/s/a/d` commands release hold; `r` returns to zero command. Finite playback adds `--headless --steps 700`. ROS launch uses `fixed_residual_lqr:=true` with the existing `ckpt:=...` argument. PD and M4 cannot be enabled together.

Checks actually executed:

```bash
source /opt/ros/jazzy/setup.bash
PYTHONDONTWRITEBYTECODE=1 MPLCONFIGDIR=/tmp/lqr_mpl OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 \
ROS_DOMAIN_ID=87 ROS_LOCALHOST_ONLY=1 ROS_LOG_DIR=/tmp/fixed_m4_ros_logs \
/home/cocel/venvs/cosim_ros2_jazzy/bin/python test/test_fixed_residual_lqr.py
/home/cocel/venvs/cosim_ros2_jazzy/bin/python test/test_residual_wheel_pd.py ResidualTests -v
python3 sim2sim/sim2sim_ros2_jazzy/launch/sim2sim.launch.py \
  --ckpt lab/ddt_lab/logs/flash_sac/tita_flash_sac_115632_883848/model_60000 \
  --fixed_residual_lqr --headless --steps 700
./scripts/agent-check.sh
```

Remaining limits: no absolute position-hold success claim or reproduction of the previously reported IAE. The normal scene/startup differs from the archived floor-only experiment. The simulated bias/gain has no validated hardware torque mapping. No hardware deployment or physical commands were executed.

Branch: `agent/codex/dev_tita_gluon`. No commit, push or PR.
