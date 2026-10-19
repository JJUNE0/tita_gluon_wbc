# Four sphere-wheel candidates — deployment/build

- Execution Domains: `DESKTOP_DRY_RUN`, `ROBOT_READ_ONLY`, `ROBOT_STATE_CHANGING`, `ROBOT_COMMAND_FREE_RUNTIME`.
- Evidence Status: **PASS** requested deployment/build and command-free verification; physical behaviour **NOT_TESTED**.
- Operator authorization (2026-10-19): “이 정책들 실기체 배포 및 빌드해줘”. No controller/motor execution authorized or performed.
- Branch: `agent/codex/dev_tita_gluon`; no commit/push.

## Policy identity

| Candidate | Bundle | Source run / folder | Actor SHA256 | ONNX SHA256 | Saved filter |
|---|---|---|---|---|---|
| ② 60k | `flashsac_sphere2_60000` | `tita_flash_sac_220437_199621/model_60000` | `a4c2bfbf6a58240a6623ee8bb8d863774b9336f62df7de3d1993b76725334b2a` | `b744091bb984f3540ec9517f4d3a8a70b5d76cf0f1c7a811d122baac15017040` | `none` |
| ① 70k | `flashsac_sphere1_70000` | `tita_flash_sac_220437_190135/model_70000` | `8e23cf5d1844a6d825482939e5cfc455cd672dd566b2320570080ff606782c77` | `df54bb61b09c681aad403b41ae52dc83807002f2832b8f969c2ba56a441297d7` | `ma2_legs` |
| ① 90k | `flashsac_sphere1_90000` | `tita_flash_sac_220437_190135/model_90000` | `df2a03faeb6e054310c8cc0c2c11f811c1f6e845dd87a66c40ff3cd29dd8b311` | `08d57aa5b0d63063ddcd1f64a08fc545f7ad2ab317aa1c1044cb80ea15a0710a` | `ma2_legs` |
| ③ 70k | `flashsac_sphere3_70000` | `tita_flash_sac_034313_051978/model_70000` | `b9d411eaee09753d3bb6a00d12da8a3f18ce205b2c95faec954c91699e811263` | `204693483d123b77d9ad1698819ee10179ba27b5881bc8a41c1e5fc138ee16ff` | `ma2_legs` |

All identities were matched against the operator's table, actual actor/ONNX bytes, `ddt.json`, exported config and manifest. [bundles.json](bundles.json) records full deployment/source config hashes and tasks. Source exports remain unchanged. ONNX files are copied byte-for-byte; each config changes only command caps from exported 0.2/0.3 to existing real 1.0/1.0.

## Runtime behaviour and scope

All candidates retain the existing 34-observation encoder/IMU interface, eight native-order actions, 50 Hz inference and 500 Hz live feedback PD. Wheel position error: radius 0.0925 m, clip ±0.3 m, scale 5, neutral thresholds 0.02/0.02/0.03; existing reset/unwrap behaviour is retained. Training observations and gains match deployed PosMA2. The only action-layout difference is that candidate ② has no six-leg MA2; it is preserved as requested.

RL Kp `[60,60,92,0,60,60,92,0]`; Kd `[1.5,1.5,2.3,0.5,1.5,1.5,2.3,0.5]`; torque caps `[60,60,60,12,60,60,60,12]` Nm. `leg_action_filter:=auto` restores none for ② and MA2 for the other three. Wheels pass through; raw `last_action` remains the policy history. Velocity bias defaults OFF. Existing state machine, joystick buttons and command ramp remain unchanged. Default policy remains A80k and all previous bundles remain selectable.

Joystick caps remain **±1 m/s and ±1 rad/s**, with existing 0.5/s ramp. Candidate ③ was trained at ±1.5 m/s / ±3 rad/s without a ramp; deployment does not raise real limits or remove the ramp. Its full training command range is not exercised by the default real joystick settings.

Product changes: four new `src/tita_controller/policies/flashsac_sphere*/{policy.onnx,config.json,manifest.json}` bundles; `launch/flashsac.launch.py` adds four pin tuples; workspace `run_flashsac.sh` adds four allowed bundles and their run-log hashes; workspace `README.md` documents mapping/commands. Controller C++, generic launch, headers, messages, CMake and older bundles were not changed. Existing installed tita_node binary SHA remains `a5c3e897f7d73408a8695f4c2dc77b6e28768efb55ad62c364aa2deee0ebde76`.

New preparation/verification/deployment helpers are `test/sim2real/prepare_sphere_candidates.py`, `verify_sphere_candidates.py`, `deploy_sphere_candidates.sh`; pinned specs and inference fixtures live in `test/sim2real/sphere_candidates/`. Payload contains only 26 explicitly listed files, including command-free test fixtures ([payload file checksums](source_payload.sha256)). Scoped [local diff](local_changes.diff) inspected; unrelated pre-existing changes retained.

## Verification

| Check | Status / result | Evidence |
|---|---|---|
| User actor/ONNX pins, export config pins, saved interface/gains/filters; native Torch action gains | PASS, all four | [prepare.log](prepare.log) |
| Desktop deterministic ONNX vs native Torch | PASS, 256 samples each; 1,024 total | [desktop_verify.log](desktop_verify.log), [desktop_parity.json](desktop_parity.json) |
| Public launch hash/config/auto-filter and generic node parameters (ExecuteProcess/Node mocked) | PASS, all four; all eight frozen bundles' hashes validated | [desktop_verify.log](desktop_verify.log) |
| Runner logging/refusal/cleanup/launch regression | PASS, 27 tests | [logging_tests.log](logging_tests.log) |
| Shell syntax, Python helper compile, scoped diff whitespace | PASS | `bash -n` runner/deploy helper; `py_compile` preparation/verification; `git diff --check -- sim2real/tita_ws test/sim2real` |
| Humble aarch64 tita_controller build/install | PASS, one package, 2.34 s (resources only) | [build.log](build.log), [deploy_console.log](deploy_console.log) |
| Installed/source byte equality, pinned configs/ONNX, executable unchanged, linkage | PASS | [verify_console.log](verify_console.log), [installed.sha256](installed.sha256), [linkage.log](linkage.log) |
| ARM C++ repeated deterministic ONNX vs native Torch | PASS, 256 samples each; 1,024 total | [arm_parity.json](arm_parity.json) |
| Vendor service PID/start timestamp/active state unchanged | PASS | [before](service_before.txt), [after](service_after.txt); no service stop/restart |
| Whole-repository agent-check | FAIL due to six existing trailing-whitespace errors in `my_flat_env_cfg.py:431,437,443,449,455,461`; syntax 655 PASS, URDF 8 PASS | [agent_check.log](agent_check.log) |
| Physical standing/tracking/drift/vibration, calibrated torque, joystick response and hardware timing | NOT_TESTED | Agent never launched the controller, SDK, ROS nodes or CAN/MCU commands |

Maximum action errors in the fresh comparison:

| Candidate | Desktop | ARM |
|---|---|---|
| ② 60k | 3e-06 | 2.86e-06 |
| ① 70k | 3.34e-06 | 2.86e-06 |
| ① 90k | 2.62e-06 | 2.74e-06 |
| ③ 70k | 2.38e-06 | 2.5e-06 |

Inference equality proves the installed model/action calculation matches Torch; it does not establish improved physical yaw/drift or vibration. No new dynamics rollout was performed. Prior screening and its limitations are in [sphere_wheel_screen.md](../sphere_wheel_screen.md).

## Backup and execution

SBC backup: `~/tita_ws/docs/exp/2026-10-19/sphere_candidates_deployment/before_deployment.tar.gz`, containing previous source/resources, runner/README and installed tita_controller. [backup.sha256](backup.sha256) records its hash. Deployment checked existing source/executable hashes before writing and refused if the overlay controller/joystick was running. Vendor `/opt/tita` installation was left alone; stable service PID does not establish live joystick health.

Run one selected bundle at a time, sourcing the rebuilt overlay:

```bash
cd ~/tita_ws
source /opt/ros/humble/setup.bash
source install/setup.bash
ros2 launch tita_controller flashsac.launch.py \
  output_enabled:=true policy:=flashsac_sphere2_60000
```

Replace only `policy:=...` using the table above. Leave the filter at auto for the intended candidate comparison. Commands above have not been executed by the agent. Existing console/ROS/bag/summary logging remains under `~/tita_ws/docs/exp/YYYY-MM-DD/<selected_bundle>_*`.
