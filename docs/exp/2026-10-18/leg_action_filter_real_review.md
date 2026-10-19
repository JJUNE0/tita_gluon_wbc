# Real MA2 first trial: 25 Hz reduction and residual 8–9 Hz pitch motion

- Date: 2026-10-18 (Asia/Seoul).
- Execution Domains: `ROBOT_READ_ONLY` (copy completed run), `DESKTOP_DRY_RUN` (read-only SQLite decode and signal analysis).
- Evidence Status: applied-action/teacher/torque reconstruction and measured-signal comparison PASS; physical root-cause interpretation SUSPICIOUS; new controller changes and physical trials NOT_TESTED / not performed.
- Checkpoint SHA256: `79f9175bb8c3be0c5138866e30891b90cc1282b6c98023cdb76c2e33b229068c`.
- ONNX SHA256: `26f0d86b65a68475fb8a315fb31e829ae16eaa2cf16dabbbcf38e69f28c933e9`.
- Config SHA256, both runs: `a24c2137969f854fc98cc3027884dbbadad4060f18db7758b028c12ca1405719` (hip/shoulder 60/1.5; knee 92/2.3; wheel Kd0.5).
- MA2 run: `flashsac_80000_135923_560039455_output_true`, 2026-10-18 13:59:23 KST; executable `bc331b8ed4ee424f461f0053aba93344c3ee41e1fd2bbc95c0defdcf12c9e56c`.
- OFF baseline: `flashsac_80000_125618_839843723_output_true`, 12:56:18 KST; executable `2e3949c0b445fa328ab33ac7b152d3096170e17e1a863a2a8494fdb79dc0d9ff`.
- Velocity bias OFF in both runs. Operator reports only stick input, no hand-applied disturbances. Final physical contact/pose was not separately described.
- Branch: `agent/codex/dev_tita_gluon`; no commit/push.

## Conclusion

The 25 Hz period-2 motion is substantially reduced, not merely a small software-only attenuation. Applied targets, commanded torque updates and encoder speed all change. However, the MA2 trial has a distinct **8–9 Hz pitch/shoulder mode**, so the robot is not vibration-free. The mean leg response is improved at the previous 25 Hz mode while a different body motion remains. Whether the operator's perceived rattle changed cannot be concluded from these 50 Hz recordings alone.

Both trials begin with a neutral interval. Compare the same **3.0–7.8 s from RL entry**, before the first stick input in either run (240 samples / about 4.8 s each):

| Metric | OFF | MA2 |
|---|---:|---:|
| Knee command update-step RMS L/R, Nm | 18.24 / 19.29 | **1.03 / 0.73** |
| Hip command update-step RMS L/R, Nm | 6.23 / 3.69 | **0.42 / 0.34** |
| Shoulder command update-step RMS L/R, Nm | 0.76 / 3.64 | **1.32 / 1.09** |
| Hip 25 Hz encoder speed amplitude L/R, rad/s | 0.520 / 0.494 | **0.00113 / 0.00052** |
| Knee 25 Hz encoder speed amplitude L/R, rad/s | 0.427 / 0.440 | **0.00017 / 0.00519** |
| Pitch mean | 6.55 deg | 5.84 deg |
| Pitch standard deviation | 0.100 deg | **0.335 deg** |
| Pitch-rate adjacent-sample step RMS | 0.0325 rad/s | **0.1531 rad/s** |
| Roll/yaw-rate step RMS | 0.0536 / 0.0695 rad/s | 0.0283 / 0.0186 rad/s |

Knee command step RMS falls approximately **94–96%** in this matched initial window. Left shoulder command steps increase while right shoulder steps decrease; it is inaccurate to describe every joint/frequency as uniformly improved.

Pooled neutral holds give the same qualitative result: OFF knee update-step RMS 17.92/18.11 Nm versus MA2 1.60/1.28 Nm (**91–93% reduction**). Neutral-hold duration is 18 s OFF versus 27 s MA2; the trials' command histories and later conditions differ, so these pooled figures are not an isolated causal paired experiment.

## Why vibration can still be felt

OFF knee/hip raw action delta lag-1 is about -1 and dominant action/joint-speed frequency is 25 Hz. MA2 raw knee delta lag-1 becomes about -0.22/-0.34 over neutral holds, rather than continuing the original pure period-2 output. Thus the policy feedback cycle itself has changed, in addition to averaging the applied commands.

With MA2, action, shoulder and knee speed PSD peaks are about 8.20 Hz; initial-window pitch peak is about 8.59 Hz (128-point Welch resolution 0.390625 Hz). The one-second zoom shows the approximately 8 Hz pitch wave directly. MA2's standalone amplitude at about 8.2 Hz is still approximately 0.87, so this two-tap filter is not a strong suppressor at that frequency. Its phase delay and the hardware/policy dynamics may participate in the remaining mode, but this recorded pair does not isolate the cause.

The earlier artificial-gain simulation proxy sometimes left 2–3 Hz motion. This real 8–9 Hz mode is different: the proxy did not predict its frequency. A more aggressive filter would also change phase/latency, so selecting the next filter requires evaluating that mode, rather than treating the 25 Hz result as complete stability validation.

## Applied path and telemetry integrity

The new `ActionFilterSample` messages join every training sample in this run; no missing filter frames. Raw-to-applied MA2 replay error is **0**, including RL entry/reset; wheel outputs pass through. Teacher equals applied action when bias is OFF, maximum error **0**. Actual PD command reconstruction using applied targets has max error **8.88e-16 Nm**, identical numerical precision to OFF. Least-squares gains independently recover 60/1.5, 60/1.5, 92/2.3 and wheel Kd0.5 in both runs. This supports correct filter insertion and logging semantics.

The existing raw-only vibration analyzer would incorrectly infer gains/target steps if used directly on filtered data. The new helper explicitly reconstructs targets from applied actions and reports raw and applied statistics separately. Torque-update step is current computed command minus the preceding 2 ms command in MotorFeedback. It is not a calibrated physical torque step. SDK feedback deviations and final clipping statistics remain in metrics for inspection.

## Return-to-sit fault

MA2 RL lasts 63.222 s in sampled data. `return_to_sit` starts at 63.242 s; **2.406 s later**, before the planned four-second completion, state becomes `damp` at 65.648 s. At that transition:

- Sensors are valid.
- Pitch is **37.284 deg**, roll 0.365 deg.
- Combined gravity tilt is **0.650752 rad**, above the code's `kFallTilt = 0.65 rad`.
- Immediately preceding samples rise from 33.56 to 36.92 deg pitch.

This sample directly explains the fault as the existing fall-tilt guard. It is not evidence of failed CAN transmission or the filter option failing to start. The subsequent RL rejection follows because state is `damp`, not `sit`.

The MA2 filter applies only in RL; return/sit/fault controllers bypass it and their source code is unchanged. Changed entry joint posture/motion or limitations of the supporting-sit balance remain possible contributors; the return trajectory's underlying root cause is not isolated here. A successful RL vibration reduction does not establish that this run's sit transition completed safely. No guard thresholds or sit controller settings were changed in this analysis.

## Evidence and limits

- [One-second neutral zoom](leg_action_filter_real_review/neutral_zoom.png).
- [Whole-RL comparison](leg_action_filter_real_review/comparison.png).
- [Metrics, source hashes and fault window](leg_action_filter_real_review/metrics.json).
- [Analysis log](leg_action_filter_real_review/analysis.log).
- New helper: `test/sim2real/analyze_leg_filter_real.py`; existing analyzer is imported without modification.
- New MA2 bag/summary/console copies: `docs/exp/2026-10-18/leg_action_filter_real_review/`.
- OFF bag reused from `docs/exp/2026-10-18/flashsac_knee92_bias_pair/`.

50 Hz logs cannot resolve physical vibration above 25 Hz or audible-frequency spectra; aliases and unmeasured contact dynamics remain. Trial durations/command profiles differ. No independent chassis localization, force or acoustic measurements were made. Both runs report successful shutdown zero-torque transport sends; this is not independent motor torque-release verification.

Checks executed: SQLite quick checks; monotonic timestamps/contiguous IDs; complete filter joins; valid RL sensor/policy/output/transport flags; exact MA2 replay; teacher and applied PD reconstruction; fitted gains; saved signal/figure inspection. Only offline analysis code and experiment records were added. Final scope checks confirm prior deployment sources and bag hashes are unchanged; new helper/report diff whitespace checks PASS. Required [agent-check](leg_action_filter_real_review/agent_check.log) remains overall FAIL due to the six pre-existing `my_flat_env_cfg.py` trailing-whitespace errors. Python syntax 586 PASS; URDF parsing 8 PASS. See `completion_integrity.json`.
