# Real MA2 + 8.3 Hz notch: smaller target steps, residual body oscillation

- Date: 2026-10-18 (Asia/Seoul).
- Execution Domains: `ROBOT_READ_ONLY` (copy/hash completed experiment), `DESKTOP_DRY_RUN` (offline telemetry analysis).
- Evidence Status: source/copy integrity, independent filter replay and applied PD reconstruction PASS; useful body-vibration suppression SUSPICIOUS / not established; causal diagnosis SUSPICIOUS. No new controller changes or motor trials performed.
- Checkpoint SHA256: `79f9175bb8c3be0c5138866e30891b90cc1282b6c98023cdb76c2e33b229068c`.
- ONNX SHA256: `26f0d86b65a68475fb8a315fb31e829ae16eaa2cf16dabbbcf38e69f28c933e9`.
- Config SHA256: `a24c2137969f854fc98cc3027884dbbadad4060f18db7758b028c12ca1405719` in all three summaries (mixed hip/shoulder60/1.5, knee92/2.3, wheelKd0.5).
- New run: `flashsac_80000_150320_869838811_output_true`, 15:03:20 KST; executable `80c912f103b109868bb6dd50c26404f5144bdff089c5be09a374a145b2672fc8`.
- Baselines: OFF `125618_839843723`, MA2 `135923_560039455`. Velocity bias OFF throughout.
- Branch: `agent/codex/dev_tita_gluon`; no commit/push/deployment.

## Finding

The 8.3 Hz/Q3 notch is functioning exactly as implemented. It further reduces knee command-update steps, but does **not establish a useful reduction of body vibration over MA2 alone** in the common initial neutral interval. Pitch-rate variability and shoulder encoder-speed variability increase there. The dominant recorded body mode is lower than the original target frequency. The operator's impression that the improvement remains disappointing is consistent with these signals.

Do not call the whole run a failure: there is no recorded RL sensor/policy/output/transport failure, and applied target smoothing works. Do not call vibration solved: target smoothing and physical body motion give different answers.

## Common initial zero-command comparison

The notch run first leaves the neutral-command thresholds at RL age5.508 s, earlier than the other trials. The shared initial interval is therefore **3.0–5.508 s** from RL entry, approximately2.5 s /125 samples (MA2 has126 because sample phases differ). Thresholds are abs(vx,vy,yaw) <= (0.02,0.02,0.03). The first3 s of each continuous neutral hold are excluded.

| Metric | OFF | MA2 | MA2 + notch |
|---|---:|---:|---:|
| Knee command update-step RMS L/R [Nm] | 17.983 /19.545 | 1.103 /0.825 | **0.612 /0.553** |
| Pitch mean [deg] | 6.527 | 5.625 | 5.334 |
| Pitch standard deviation [deg] | 0.084 | 0.249 | **0.237** |
| Pitch-rate standard deviation [rad/s] | 0.0239 | 0.1580 | **0.1771** |
| Shoulder speed standard deviation L/R [rad/s] | 0.197 /0.243 | 0.214 /0.181 | **0.349 /0.274** |
| Pitch 7–10 Hz band RMS [deg] | 0.0240 | 0.1967 | **0.2307** |
| Pitch PSD peak above1 Hz | 1.56 Hz | 8.59 Hz | **7.81 Hz** |

Against MA2, knee update steps fall another44.5%/33.0%. Pitch std falls only4.7%, pitch-rate std rises12.1%, shoulder-speed std rises63%/52%, and pitch7–10 Hz RMS rises17.3%. The short initial window does not justify treating small differences as statistically robust causal effects. The strong conclusion is that substantially smoother knee targets have not removed the recorded body mode.

Initial-window PSD uses64-sample Welch windows (0.78125 Hz resolution), identical settings across trials; it cannot precisely identify a resonance center. The low-frequency OFF PSD peak is not a claim that the previous25 Hz joint chatter was absent.

## Longer neutral holds and command-history limitation

All eligible neutral samples total18.0 s OFF,27.0 s MA2,10.44 s notch. MA2 pooled pitch std0.642 deg falls to0.254 deg in the notch run, and pitch-rate std0.283 falls to0.156 rad/s. These are encouraging descriptive pooled values, but **the operator command profiles, durations and entry postures differ**. In particular, MA2 includes substantial forward/reverse maneuvers while the notch trial is dominated by yaw commands. A pooled60% pitch-std reduction is not an isolated notch effect.

With128-sample Welch windows (0.390625 Hz resolution), pooled dominant pitch/gyro mode is8.20 Hz under MA2 versus7.42 Hz under notch. This supports describing the residual as a shifted7–8 Hz mode, rather than declaring the8.3 Hz filter inactive. Closed-loop phase/gain changes or trial conditions could explain it; the comparison does not isolate which. Repeatedly chasing this peak with new notch centers is not yet supported.

The neutral wheel-speed proxy also differs by trial and is not ground-truth chassis velocity; no drift improvement is inferred from it.

## Implementation and telemetry checks

PASS on all three copied bags:

- SQLite quick check, increasing monotonic times, contiguous sequence IDs and matching feedback tick/time.
- Every filtered sample joins its applied-action sample by sequence ID plus monotonic time; mode and control tick match.
- All RL sensor/policy/output-enabled/torque-sent flags are true; wheel velocity bias is zero.
- Independent SciPy MA2/notch replay with DC initial state and per-RL reset: max applied-action error0 in these recordings. No policy/filter implementation was changed to obtain this result.
- Teacher equals applied action, max error0; applied-target native PD reconstruction max error8.88e-16 Nm. Least-squares gains are recorded for cross-checking.
- Notch run has1752 logged RL frames (about35.0 s); maximum inter-sample interval20.55 ms. This does not measure all500 Hz motor/CAN loop deadlines.
- Copied bag, metadata, summary and console hashes match SBC originals. [Hashes](leg_notch_real_review/remote_sha256.txt).

The first offline analysis attempt omitted the wheel velocity-target contribution in its reconstruction formula, then a plot attempted128-point PSD on a shorter interval. Both helper errors were fixed and the full analysis rerun successfully; initial failure logs remain beside the final log. These were analysis-code errors, not controller faults.

## Next investigation

Keep MA2 as the comparison baseline. Before stronger filtering or another notch center, compare leg PD settings and the live joint-velocity feedback path independently in sim, with the observed7–8 Hz body mode as the target metric. Current filtering changes policy position targets; the500 Hz `-Kd*dq` feedback uses live joint velocity and bypasses the action filter. This is a code-path fact, not evidence that the derivative term causes the vibration. A stationary500 Hz joint/torque/IMU capture would make that diagnosis stronger than the current50 Hz record.

No gain/filter settings were changed or deployed in this review. Physical behavior above25 Hz, acoustic rattling, backlash and true torque remain unresolved by50 Hz telemetry. The operator subsequently confirmed stick input only, no hand-applied disturbances, and perceived fore/aft body rocking rather than identifying rapid leg rattling as the main concern. This agrees with residual pitch motion in telemetry, but does not establish its cause or remove differences between command histories.

## Files and validation

- New offline helper: `test/sim2real/analyze_leg_notch_real.py`; existing analyzers imported without edits.
- [Metrics and source hashes](leg_notch_real_review/metrics.json), [analysis log](leg_notch_real_review/analysis.log).
- [Shared-scale comparison](leg_notch_real_review/comparison.png), [one-second neutral zoom](leg_notch_real_review/neutral_zoom.png).
- New copied run files are directly under `docs/exp/2026-10-18/flashsac_80000_150320_869838811*`; previous bags remain in their existing folders.
- Required [agent-check](leg_notch_real_review/agent_check.log): overall FAIL due to the same six pre-existing `my_flat_env_cfg.py` trailing-whitespace errors; Python syntax606 PASS, URDF8 PASS. Final source/scope integrity is recorded in `leg_notch_real_review/completion_integrity.json`. Deployed sources and prior analysis helpers remain unchanged.
