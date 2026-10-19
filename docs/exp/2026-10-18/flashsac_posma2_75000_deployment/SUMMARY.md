# PosKneeMA2 model_75000 deployment

- Execution Domains: `DESKTOP_DRY_RUN`, `ROBOT_READ_ONLY`, `ROBOT_STATE_CHANGING`, `ROBOT_COMMAND_FREE_RUNTIME`.
- Evidence Status: **PASS** build/install/command-free inference; physical operation **NOT_TESTED**.
- Authorization: operator requested “75k … 로봇켯으니 배포 후 빌드 ㄱ” on 2026-10-18. Deployment/build only; controller not launched.
- Branch: `agent/codex/dev_tita_gluon`; no commit/push.
- Source: `lab/ddt_lab/logs/flash_sac/tita_flash_sac_180212_290240/model_75000`.
- Checkpoint SHA256: `9c22f34e0e3b9d7840f29250c214452bb84cadde6037d277d90df55221e84150`.
- ONNX SHA256: `128734f230868b947c9eac59ef647b8394043c6603781a335fd4e3b4700a2001`.
- Config SHA256: `45a2e773f5ccf43b770829184b22537a6de1ce8da092727264446ac32287c28a`.

## Change

Added selectable SHA256-pinned `flashsac_posma2_75000` bundle. Existing 50k remains selectable and the default policy stays A80k. ONNX copied unchanged from verified sim2sim export. Saved control/robot/observation/action/filter layouts are identical to PosMA2 50k. Only command caps change from exported 0.2/0.3 to established real caps 1 m/s / 1 rad/s.

Runtime settings: 34 observations, eight native-order actions, 50 Hz policy / 500 Hz feedback PD, saved six-leg MA2 automatically selected, raw last_action retained. Knee Kp/Kd 92/2.3; other legs 60/1.5; wheel Kd 0.5; torque caps legs 60 / wheels 12 Nm. Velocity bias OFF by default. Existing state-machine and joystick controls retained.

Changed product files: new `policies/flashsac_posma2_75000/{policy.onnx,config.json,manifest.json}`, `launch/flashsac.launch.py` bundle pins, root `run_flashsac.sh` allowlist/run hash, `README.md` usage. New helpers/fixtures are under `test/sim2real/`: `prepare_posma2_75000_fixture.py`, `check_posma2_75000_launch.py`, `deploy_posma2_75000.sh`, `posma2_75000/`. Existing controller C++, generic launch and headers were verified against SBC before deployment and not modified. Installed tita_node executable SHA remains `a5c3e897f7d73408a8695f4c2dc77b6e28768efb55ad62c364aa2deee0ebde76`.

Scoped [diff](local_changes.diff) inspected; payload contains only listed resources and command-free fixtures. Pre-existing unrelated workspace changes retained. No vendor service stop/restart, MCU request or CAN transmission. Vendor service PID/start timestamp/active state unchanged ([before](service_before.txt), [after](service_after.txt)); this does not verify live joystick response.

## Verification

| Check | Result | Evidence |
|---|---|---|
| Source hashes, saved-interface/gain identity, native Torch action gain mapping | PASS | [fixture.log](fixture.log); source export manifest parity 256 samples, max error 3.46e-6 |
| Fresh desktop Torch/ONNX, 256 x 34 inputs | PASS | [desktop_parity.json](desktop_parity.json), max action error 3.58e-6 |
| Public launch config/pins/auto-filter, four bundles; ExecuteProcess mocked | PASS | [launch_check.log](launch_check.log) |
| Runner/launch/logging/refusal/cleanup tests (27) | PASS | [logging_tests.log](logging_tests.log) |
| Shell syntax, scoped diff whitespace | PASS | `bash -n` on runner/deploy helper; `git diff --check -- sim2real/tita_ws test/sim2real` |
| SBC Humble aarch64 package build | PASS | [build.log](build.log), one package in 1.86 s (resource update) |
| Installed resources byte equality/pins, linkage, executable unchanged | PASS | [verify_console.log](verify_console.log), [installed.sha256](installed.sha256), [linkage.log](linkage.log) |
| ARM C++ ONNX vs native Torch, 256 samples, deterministic repeat inference | PASS | [arm_parity.json](arm_parity.json), max error 3.52e-06 |
| Whole-repository agent-check | FAIL | [agent_check.log](agent_check.log); existing six trailing-whitespace errors in `my_flat_env_cfg.py:431,437,443,449,455,461`; Python syntax 649 PASS, URDF 8 PASS |
| New dynamics rollout, physical standing/yaw/drift/torque/timing | NOT_TESTED | No controller or hardware test run in this task |

## Backup and operator command

SBC backup: `~/tita_ws/docs/exp/2026-10-18/flashsac_posma2_75000_deployment/before_deployment.tar.gz`; [backup checksum](backup.sha256). Contains former source/resources/runner/README and installed tita_controller. Existing hashes checked before applying payload.

```bash
cd ~/tita_ws
source /opt/ros/humble/setup.bash
source install/setup.bash
ros2 launch tita_controller flashsac.launch.py \
  output_enabled:=true policy:=flashsac_posma2_75000
```

MA2 is automatic; velocity bias remains OFF. Agent has not executed this command. Console/bag/summary logging remains enabled under `~/tita_ws/docs/exp/YYYY-MM-DD/flashsac_posma2_75000_*`. The 50k yaw-drift diagnosis is in [the previous review](../flashsac_posma2_50000_202450_review.md); output parity establishes correct deployment, not improved physical yaw or drift.
