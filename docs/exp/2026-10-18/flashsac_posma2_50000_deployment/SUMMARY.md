# PosKneeMA2 model_50000 deployment

- Execution Domains: `DESKTOP_DRY_RUN`, `ROBOT_READ_ONLY`, `ROBOT_STATE_CHANGING`, `ROBOT_COMMAND_FREE_RUNTIME`.
- Branch: `agent/codex/dev_tita_gluon`; no commit/push.
- Operator authorization: “이거 실기체빌드할건데. 기체 지금켜줄게” (2026-10-18). Scope: policy/support-code deployment and build; no motor execution.
- Policy: `tita_flash_sac_180212_290240/model_50000` (`DDT-Velocity-Flat-Tita-My-PosKneeMA2-v0`).
- Checkpoint SHA256: `baba6974b76d4e8a7b7107cdfab9d2b7bb73695df00419009279549ebd51f992`.
- ONNX SHA256: `4b922a52b4e371f4e1ed28d64a0a9d4211161ba24950a1d5a92d2ccf26918553`.
- Deployment config SHA256: `2b11c12bf531b8fd92558d3b36e04f49aa91fcae7b97f187413b127780bb93be`.
- Evidence Status: **PASS** deployment/build and command-free checks; **NOT_TESTED** physical policy behaviour and CAN execution.

## Behaviour and scope

Added distinct pinned bundle `flashsac_posma2_50000`; the old `flashsac_50000` is a different checkpoint and was not overwritten. Default policy remains A80k. New bundle copies ONNX unchanged and retains the saved 34-element observation layout, action mapping, gains and filter; only joystick caps change from export defaults 0.2/0.3 to the established real caps 1 m/s / 1 rad/s.

- 34 observations, eight actions, 50 Hz actor / 500 Hz live PD.
- Additional observation: encoder/IMU wheel position error; radius 0.0925 m, clip ±0.3 m, scale 5, neutral thresholds 0.02/0.02/0.03. Reference/unwrap reset on RL exit/reentry and policy faults. Wheels must travel less than pi radians between samples for unwrap.
- RL gains: Kp `[60,60,92,0,60,60,92,0]`; Kd `[1.5,1.5,2.3,0.5,1.5,1.5,2.3,0.5]`. Torque caps legs 60 / wheels 12 Nm.
- Public `leg_action_filter:=auto` reads the pinned policy config: new policy selects six-leg MA2, previous A80k/C2 select none. Wheels pass through; `last_action` remains raw. Explicit filter overrides retained. Shell runner also resolves and records auto mode.
- Velocity bias remains OFF by default. No online learning, RLS, probing or gain adaptation added.

Changed local files: new bundle's `policy.onnx`, `config.json`, `manifest.json`; public `flashsac.launch.py`, root `run_flashsac.sh`, `README.md`; logging tests plus preparation/inference/launch/deployment helpers under `test/sim2real/`. The already prepared generic `adapter.hpp`, `tita_node.cpp`, `tita.launch.py` were deployed as dependencies for this 34-observation policy without further local modifications. Their remote-to-local changes were inspected: position-error construction/reset and saved-filter support only. All other headers, messages and CMake matched before deployment. Pre-existing unrelated work was retained. Scoped diffs: [local](local_changes.diff), [robot support](robot_support_changes.diff).

## Verification

| Check | Status | Evidence |
|---|---|---|
| Saved export hashes, actor provenance, native action gain mapping | PASS | [fixture.log](fixture.log); source manifest parity 256 samples, max error 3.99e-6 |
| Fresh desktop ONNX vs native Torch, 256 x 34 input samples | PASS | [desktop_parity.json](desktop_parity.json), max error 3.16e-6 |
| 33/34 observation/filter/PD parity and reset semantics, four tests; 1,000 sequence samples each | PASS | [position_parity.log](position_parity.log), max combined error 1.11e-5 |
| Runner logging/refusal/cleanup/launch tests (25) | PASS | [logging_tests.log](logging_tests.log) |
| Saved MA2 auto-selection and invalid saved filter refusal (two additional tests) | PASS | [auto_filter_tests.log](auto_filter_tests.log) |
| Three source bundles: pinned hashes, dimensions, automatic filter selection | PASS | [launch_check.log](launch_check.log) |
| SBC Humble aarch64 `tita_controller` build | PASS | [build.log](build.log), one package, 44.5 s |
| Installed/source byte comparison, all pins, linkage | PASS | [verify_console.log](verify_console.log), [installed.sha256](installed.sha256), [linkage.log](linkage.log) |
| SBC C++ ONNX vs native Torch, 256 samples, repeated deterministic inference | PASS | [arm_parity.json](arm_parity.json), max error 3.28e-6 |
| Vendor service MainPID/start timestamp/active state unchanged | PASS | [service_before.txt](service_before.txt), [service_after.txt](service_after.txt); service never stopped/restarted |
| Whole-repository agent-check | FAIL | [agent_check.log](agent_check.log): six pre-existing trailing-whitespace errors in `my_flat_env_cfg.py:431,437,443,449,455,461`; syntax 642 PASS, URDF 8 PASS |
| Physical behaviour, standing/drift, torque transmission | NOT_TESTED | Controller never launched; no SDK, ROS node, service mutation or MCU/CAN command in verification |

## SBC backup and execution

SBC backup: `~/tita_ws/docs/exp/2026-10-18/flashsac_posma2_50000_deployment/before_deployment.tar.gz` (source, runner, README and installed tita_controller). Its hash is in [backup.sha256](backup.sha256). Payload is scoped and checked before/after extraction. Vendor `/opt/tita` processes use a separate installation; build does not stop their service. Deployment refuses if this overlay's controller/joystick is running.

Operator execution, after sourcing the rebuilt overlay:

```bash
cd ~/tita_ws
source /opt/ros/humble/setup.bash
source install/setup.bash
ros2 launch tita_controller flashsac.launch.py \
  output_enabled:=true policy:=flashsac_posma2_50000
```

MA2 is automatic; do not add the previous notch or velocity bias for the first comparison. Existing idle → transform_up → sit → RL controls are retained. Runtime console/bags/summaries continue under `~/tita_ws/docs/exp/YYYY-MM-DD/` with the new bundle name. This command has not been executed by the agent. Build/inference parity does not establish physical stability, calibrated torque accuracy, standing quality or hardware timing.
