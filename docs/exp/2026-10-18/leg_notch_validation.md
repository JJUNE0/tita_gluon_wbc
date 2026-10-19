# MA2 + leg notch: sim implementation, comparisons and local real-controller port

- Date: 2026-10-18 (Asia/Seoul).
- Execution Domains: `DESKTOP_DRY_RUN` (math/parity/build), `VALIDATION_SIM` (native 500 Hz / policy 50 Hz rollouts and runtime smoke), `ROBOT_STATE_CHANGING` (approved source deployment/build), `ROBOT_COMMAND_FREE_RUNTIME` (ARM filter and mocked launch checks), `ROBOT_READ_ONLY` (final process/policy snapshot).
- Evidence Status: implementation/parity/local and SBC builds PASS; installed ARM checks PASS; primary paired regression gate PASS; proxy strict speed-preservation gate FAIL in two improving cases; physical 8–9 Hz attenuation NOT_TESTED.
- Checkpoint SHA256: `79f9175bb8c3be0c5138866e30891b90cc1282b6c98023cdb76c2e33b229068c`.
- ONNX SHA256: `26f0d86b65a68475fb8a315fb31e829ae16eaa2cf16dabbbcf38e69f28c933e9`.
- Config SHA256: `a24c2137969f854fc98cc3027884dbbadad4060f18db7758b028c12ca1405719` (unchanged).
- Branch: `agent/codex/dev_tita_gluon`; no commit/push.

## Implemented candidate

`leg_action_filter=ma2_notch_legs`: first average current/previous raw policy action on six legs, then apply a second-order notch. Candidate startup settings are **8.3 Hz / Q3 at 50 Hz**. Wheels pass through. Raw `last_action`, 500 Hz live-feedback PD, state-machine gains, torque limits, actor and velocity-bias behavior are unchanged. First RL action seeds the notch's DC state rather than zero, and RL exit/fault resets its state.

The notch is transposed direct-form II with double-precision internal state and float32 applied output, using coefficients equivalent to SciPy `iirnotch`. Invalid frequency/Q/bandwidth is rejected; nonfinite output faults through the existing node path. Raw/applied/teacher logging keeps its previous meaning. The run summary and node startup log record frequency and Q. No ROS message schema changes are needed; the filter mode is carried by the existing ActionFilterSample and the fixed startup parameters are in the run summary.

The option exists in Python sim2sim adapter/node/CLI/launch and local C++ real controller/launch/runner. Default remains `none`; `ma2_legs` is preserved. New parameters are `leg_notch_hz` (8.3) and `leg_notch_q` (3.0).

## Fresh simulation comparisons

All runs use the frozen A80k policy and mixed 60/60/92 leg gains. Physical leg-output scales are hypotheses, not new measured hardware calibration. The intended point is hip/shoulder/knee `1/1/0.65`; radius, plant assets and native C++ observation/PD/state bridge are unchanged. No velocity bias, hand force or online adaptation is introduced.

1. **Screen: 24 stand jobs**, seed42, knee scale0.65, delay0/12 ms. Baselines none/MA2/EMA0.5 and nine notches (center7.5/8.3/9 Hz, Q2/3/4). Faults0. Some wider/lower notches degrade delayed-loop pitch: center7.5/Q2 at12 ms has pitch std1.087 deg versus MA2 0.013 deg. This is evidence against treating arbitrary notch settings as equivalent.
2. **Confirm: 40 jobs / 20 fresh paired comparisons**, chosen8.3/Q3 versus MA2. Stand25 s and drive60 s; forward/reverse0.6 m/s, yaw+/-1 rad/s and stop reentry. Knee scales0.55/0.65/0.78; delays0/12 ms throughout, plus4/8 ms at0.65; additional seeds7/123 at0.65. Faults0. All predefined paired gates PASS.
3. **Proxy: 12 jobs / 6 pairs**, preemphasis gains0.5/1/1.5 and delay0/4 ms at scale0.65. Faults0. This is an artificial gain proxy, not an identified model of the observed real 8 Hz motion.

Total **76 fresh MuJoCo rollouts, no fall/nonfinite/startup faults**. This does not mean every quality gate passes or that the physical robot is stable.

Primary gate thresholds: no new faults; startup pitch increase <=2 deg; stand pitch std increase <=1 deg; stand signed speed change <=0.03 m/s; drive absolute tracking-error degradation <=0.05 (vx/wz units), stop speed degradation <=0.03 m/s; clipping fraction increase <=0.01. These are engineering regression comparisons, not certified hardware safety limits. Script and JSON preserve the actual criteria.

## Selected-point results

Nominal scale0.65, stand, seed42:

| Delay | MA2 startup pitch peak | MA2+notch startup peak | Notch settled pitch std / mean speed |
|---|---:|---:|---:|
| 0 ms | 7.39 deg | 7.98 deg | 0.013 deg / -0.0046 m/s |
| 12 ms | 10.29 deg | 11.16 deg | 0.013 deg / -0.0045 m/s |

Across the 20 confirm pairs, largest startup peak increase is **1.102 deg**. Steady support and command tracking remain within the comparison tolerances. The weak-knee0.55 plant already drifts at approximately0.12 m/s under MA2; notch does not repair that physical mismatch. Passing a relative regression gate does not establish zero absolute drift in all plants.

At strongest proxy gain1.5:

| Delay | MA2 pitch std / mean speed | Notch pitch std / mean speed |
|---|---:|---:|
| 0 ms | 1.639 deg / +0.0897 m/s | 0.011 deg / -0.0058 m/s |
| 4 ms | 4.202 deg / +0.1464 m/s | 0.497 deg / +0.0132 m/s |

The proxy's strict **signed speed-preservation** check FAILS these two pairs because speeds change by -0.0955 and -0.1332 m/s. The recorded absolute drift and pitch variation improve; the gate was not loosened/relabelled to hide these failures. These remain substantial changed dynamics in a synthetic plant. The main confirm gate passes20/20.

## Executed software checks

- PASS: 2 Python/SciPy tests, coefficients/response, arbitrary reordered joints, DC and first-action initialization, reset, wheel identity, exact8.3 Hz plus25 Hz attenuation after settling, invalid parameters.
- PASS: 4 C++/Python tests including random streams/resets, custom7.5/Q2,8.3/Q3,9/Q4 parameters, period2, teacher/PD reconstruction and preserved OFF/MA2 behavior. C++ self-check includes notch DC/reset and stopband response. Cross-language tolerance2e-6 for notch; existing non-notch parity remains exact.
- PASS: 24 existing/extended mock lifecycle tests plus one new invalid-notch test. Public ROS launch with mocked services/CAN/controller forwards mode/frequency/Q and bias, preserving output-disabled semantics. Invalid-notch tests reject before runner construction. Its first isolated test had a fixture ROS_LOG_DIR pointing at the read-only home directory; the fixture was corrected and rerun PASS, with the initial failure log retained.
- PASS: actual Sim2SimNode + ONNX + MuJoCo runtime integration, OFF/MA2/notch, 1000 steps each (890 RL each), 500/50 Hz. Independent SciPy reference confirms applied notch sequence; raw observation history and reset checked. Finite smoke only, not a vibration/stability-quality benchmark.
- PASS: local real `tita_controller` compile/link,22.1 s package /22.2 s total. Existing CMake CMP0135 warning only. The real robot node was not executed.

Evidence: [screen](leg_notch_validation/screen/results.json), [confirm](leg_notch_validation/confirm_q3/results.json), [confirm assessment](leg_notch_validation/confirm_q3/assessment.json), [proxy](leg_notch_validation/proxy_q3/results.json), [proxy assessment](leg_notch_validation/proxy_q3/assessment.json), [C++/Python checks](leg_notch_validation/cpp_python_tests.log), [runtime](leg_notch_validation/runtime.json), [build](leg_notch_validation/desktop_build.log).

## Scope, physical limits and deployment

The nominal plant does not reproduce the real residual8–9 Hz mode. This study checks low-frequency behavior, delayed-loop regressions and a synthetic gain proxy. Physical notch attenuation, new oscillation modes, hardware phase margin and actual joint sound/force remain NOT_TESTED. There is no basis to describe this candidate as proven safe on the real robot.

The operator separately approved SBC deployment/rebuild after the implementation, tests, local build and payload were ready. On 2026-10-18, six scoped real-controller resources and the pure C++ filter test were copied to `/home/robot/tita_ws`. Existing source and installed controller were first archived to `/home/robot/tita_ws/docs/exp/2026-10-18/leg_notch_validation/before_deployment.tar.gz`; its checksum is in [backup.sha256](leg_notch_validation/backup.sha256). All six expected-before hashes matched before replacement, and all payload source hashes matched afterward.

SBC `tita_controller` build PASS: 38.3 s package / 38.8 s total, ROS Humble / aarch64. ARM C++ filter checks PASS, including first action/DC/reset, stopband, wheel identity, raw preservation, mapping and teacher/bias reconstruction. Installed launch checks PASS for all three modes, center8.3/Q3, policy pins, mixed gains and torque limits; message serialization/uint64 and dynamic linkage checks PASS. Launch actions were mocked, and the real controller/SDK were never constructed. Installed launch files and runner match the deployed sources. [Build log](leg_notch_validation/remote_build.log), [verification log](leg_notch_validation/remote_verify.log), [installed binary checksum](leg_notch_validation/executable_after.sha256).

Final read-only snapshot confirms no `tita_node` process, company service still inactive, and preserved ONNX/config hashes. No service, MCU mode or motor-output commands were issued. Physical behavior remains NOT_TESTED. The selectable option still defaults OFF. [Final snapshot](leg_notch_validation/remote_final_snapshot.log).

Operator command after sourcing the rebuilt overlay:

```bash
cd ~/tita_ws
source /opt/ros/humble/setup.bash
source install/setup.bash
ros2 launch tita_controller flashsac.launch.py \
  output_enabled:=true leg_action_filter:=ma2_notch_legs \
  leg_notch_hz:=8.3 leg_notch_q:=3.0
```

Velocity bias remains OFF by default. This command is documented for the operator; it was not executed during deployment.

Only scoped sim2sim/real filter plumbing, logging/README and test files changed. Checkpoint/config, schemas, state machine and shutdown release helper remain unchanged. Before snapshots, source hashes and reviewed diffs are in `leg_notch_validation/`. Final scope/diff checks PASS; all 18 prepared source hashes still match and all other scanned sources are preserved. Required [agent-check after deployment](leg_notch_validation/agent_check_deployment.log) is overall FAIL from six pre-existing `my_flat_env_cfg.py` trailing-whitespace errors; Python syntax 605 PASS and URDF parsing 8 PASS. Scope/source integrity is recorded in `completion_integrity.json`.
