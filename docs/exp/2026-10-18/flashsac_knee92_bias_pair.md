# Knee-only PD 92/2.3: velocity-bias OFF vs ON

- Date: 2026-10-18 (Asia/Seoul).
- Execution Domains: `ROBOT_READ_ONLY` (copy existing completed recordings), `DESKTOP_DRY_RUN` (SQLite decode, production C++ math replay and plot).
- Evidence Status: decoding/reconstruction PASS; drift-removal benefit SUSPICIOUS (no demonstrated improvement in this pair; separate operator trials). Hardware modifications and new physical tests NOT_TESTED / not performed.
- Policy checkpoint SHA256: `79f9175bb8c3be0c5138866e30891b90cc1282b6c98023cdb76c2e33b229068c`.
- ONNX SHA256: `26f0d86b65a68475fb8a315fb31e829ae16eaa2cf16dabbbcf38e69f28c933e9`.
- Config SHA256: `a24c2137969f854fc98cc3027884dbbadad4060f18db7758b028c12ca1405719`.
- Executable SHA256, both runs: `2e3949c0b445fa328ab33ac7b152d3096170e17e1a863a2a8494fdb79dc0d9ff`.
- Branch: `agent/codex/dev_tita_gluon`; no commit/push.
- Operator annotation: no hand-applied disturbances; sticks were moved. Recorded command profiles differ between runs. No external support/contact sensor was used.

## Result

Bias was enabled and actually applied. It reached its additional **-0.8 Nm per wheel cap** at about 4.104 s from RL entry, and reached the same cap again at 17.884 s after command exit/reacquisition. It was capped for **88.61% of eligible samples**. There were no posture-guard inhibition intervals. The log does not support an explanation that bias simply failed to switch on or was disabled by its pitch guard.

The initial neutral 5–10 s windows are before the first stick maneuver in both runs:

| Mean, seconds 5–10 after RL entry | OFF, 12:56:18 | ON, 12:59:11 |
|---|---:|---:|
| FK/encoder/IMU forward speed estimate | -0.02969 m/s | -0.04576 m/s |
| Simple wheel rolling proxy | -0.02254 m/s | -0.03678 m/s |
| Pitch | 6.649 deg | 7.240 deg |
| Baseline policy/PD wheel command | -0.1004 Nm | +0.5836 Nm |
| Additional wheel correction | 0 Nm | -0.8000 Nm |
| Final computed wheel command | -0.1004 Nm | -0.2164 Nm |

Torque columns are means across both wheels in native coordinates, not calibrated measured torque. Speed is a rolling-contact FK estimate, not external localization. Each window contains 250 samples. Zero-command drift remains in both; this pair shows no speed improvement in that window. Initial acquisition velocities also differ (OFF shadow -0.05545 m/s; ON logged -0.06621 m/s), so the difference cannot be assigned solely to enabling bias.

The ON policy/PD contribution directly opposes the external correction: **+0.584 - 0.800 = -0.216 Nm**. Its mean magnitude is about 73% of the added correction. Across runs, the baseline contribution changes by +0.684 Nm while the external correction changes by -0.800 Nm. This is consistent with coupled balance/posture compensation consuming much of the external correction; the cross-run difference is not an isolated same-state causal effect. A frozen policy can change its output as sensor observations change.

Pitch shifts by +0.591 deg across these windows. ON has lower pitch standard deviation (0.100 vs 0.116 deg), so this window primarily shows a changed mean posture, rather than evidence of increased pitch oscillation. This also does not establish unchanged joint vibration at other frequencies.

## Timing and resets

OFF RL lasted 38.738 s; ON RL lasted 34.464 s. Inputs were not matched: OFF used forward commands up to +1 m/s and yaw up to 1 rad/s; ON's first maneuver reached about +0.701 m/s without yaw, and the later maneuver included reverse/yaw. Whole-RL averages are therefore inappropriate measures of bias benefit.

Actual ON holds, seconds relative to RL entry:

| Neutral hold | Acquired / eligible begins | First cap reached | Outcome |
|---|---:|---:|---|
| 0.000–10.604 s | 3.004 s | 4.104 s | Mean last 3 s speed -0.04941 m/s, correction -0.8 Nm |
| 13.784–28.464 s | 16.784 s | 17.884 s | Mean last 3 s speed -0.02600 m/s, correction -0.8 Nm |
| 32.024–34.464 s | Not reached | Not reached | Only 2.44 s neutral before returning to sit; correction stays zero |

Hysteresis permits the hold to persist briefly into a command ramp, until its exit thresholds are crossed. ON had 966 eligible samples of 1725 RL samples (**56%**). Commands reset the acquired average, pitch reference and integral; every new neutral hold waits another 3 s. These timings agree with the console's two acquisition messages. The final neutral interval is shorter than acquisition, so bias never re-enables there.

The second ON hold improves while -0.8 Nm is held, but natural settling is also present in OFF. For example OFF's last neutral tail reaches about -0.02600 m/s without any bias. Neither within-run settling nor these unmatched tails isolates the effect of the correction.

## Implementation finding and interpretation

`WheelVelocityBias` ignores the first second, averages speed and pitch during 1–3 s, then starts an integral law from zero torque. It has a 1 s bound ramp, 0.8 Nm/s slew, 0.8 Nm additional effort bound and tracking anti-windup. The acquired speed seeds the filtered speed estimate, not torque. Once capped, the integral tracks the capped output and cannot accumulate further correction. The current cap corresponds to bias +/-0.148 m/s or wheel reference offsets +/-1.6 rad/s at radius 0.0925 m and wheel Kd0.5.

The acquired pitch (about 6.005 deg, then 5.786 deg) is only a cutoff reference. It does not regulate pitch to zero or adjust leg references. A 5 deg change latches correction off, but the approximately 7.2 deg biased posture stayed inside that guard. Therefore a moderate posture shift can persist while the correction remains saturated.

Supported conclusion: the correction output is working as implemented, but its available authority is exhausted while a coupled policy/posture response opposes it. Reacquisition gaps also limit coverage after commands. A wrong physical response sign is not proven or excluded by recorded-state math replay. Host-reported send failure, long sample gaps, final +/-12 Nm wheel clipping and pitch-guard shutdown do not explain the steady 5–10 s result: all RL snapshots report valid sensors/policy/output/transport, maximum sample dt is about 20.6 ms, and wheel final torque clipping in this window is zero.

For the next implementation experiment, compare the existing torque bias against a pitch-aware correction or a neutral-only policy-command offset in simulation, using this exact 80000 policy and mixed gains. Any cap/gain change should be evaluated with pitch and policy/bias torque decomposition together: a larger cap alone may move the mean posture further without eliminating drift. No controller modification or deployment was made in this review.

## Evidence and reproducibility

Local copies of both complete bags, original summaries and console logs are in [flashsac_knee92_bias_pair/](flashsac_knee92_bias_pair/). Original robot paths remain under `~/tita_ws/docs/exp/2026-10-18/`. See [comparison plot](flashsac_knee92_bias_pair/comparison.png), [metrics and source hashes](flashsac_knee92_bias_pair/metrics.json), [analysis output](flashsac_knee92_bias_pair/analysis.log).

New offline helper: `test/sim2real/analyze_knee92_bias_pair.py`. It uses `TrainingSample` messages from the isolated desktop build and the existing pure C++ `velocity_bias_runtime.cpp` helper. No ONNX inference, ROS nodes, SDK construction or CAN sender is used. Command-zero shadow replay exposes the velocity estimate only; it is not a simulated corrected trajectory. OFF hold episodes in metrics are explicitly labelled hypothetical, not applied bias.

Executed checks: both SQLite quick checks PASS; monotonic timestamps and contiguous sequence IDs PASS; RL sensor/policy/output/transport flags PASS; all replay values finite; ON logged diagnostics versus actual C++ law replay maximum error **0**; both final torque reconstruction errors **8.88e-16 Nm**; additional correction bound and logged delta checks PASS. Production config, policy, controller and state-machine files are unchanged in this analysis task.

Both logs contain the new ten-zero-command shutdown transport message. It confirms the host attempted and accepted those sends, not a motor acknowledgement or independently measured torque release. The later forced cleanup and teleop SIGBUS remain separate from the steady-RL bias finding.

Required final agent-check: overall FAIL from the same six pre-existing trailing-whitespace errors in `my_flat_env_cfg.py`; Python syntax 566 PASS and URDF parsing 8 PASS. See [agent-check log](flashsac_knee92_bias_pair/agent_check.log). Final production-resource/node/bias hashes match their prior snapshots; the only new code is the offline helper. Scoped review is recorded in `completion_integrity.json`.
