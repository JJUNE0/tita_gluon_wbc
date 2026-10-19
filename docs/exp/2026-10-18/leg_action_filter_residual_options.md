# Remaining 8–9 Hz leg/pitch motion: next filter candidates

- Date: 2026-10-18 (Asia/Seoul).
- Execution Domain: `DESKTOP_DRY_RUN` (existing real metrics review and standalone transfer-function calculation).
- Evidence Status: response calculations PASS; new closed-loop/hardware attenuation NOT_TESTED.
- Policy checkpoint SHA256: `79f9175bb8c3be0c5138866e30891b90cc1282b6c98023cdb76c2e33b229068c`.
- ONNX SHA256: `26f0d86b65a68475fb8a315fb31e829ae16eaa2cf16dabbbcf38e69f28c933e9`.
- Config SHA256: `a24c2137969f854fc98cc3027884dbbadad4060f18db7758b028c12ca1405719`.
- Branch: `agent/codex/dev_tita_gluon`; no publication.

The operator asks to focus on remaining vibration. This review covers that scope only. No production code/config, deployment or physical commands are changed.

## Suggested next comparison

Retain the existing leg MA2 for its 25 Hz rejection. First investigate **MA2 plus a narrow second-order notch around 8.2–8.5 Hz on the same six leg actions**. A starting design grid is center 7.5/8.2/9 Hz and Q2/3/4; these are candidates for validation, not established hardware settings. Keep wheel actions unfiltered, raw observation history unchanged, and existing applied/teacher logging semantics.

The recorded neutral spectrum has the same approximately 8.20 Hz peak in raw/applied actions, shoulder/knee speed, pitch and pitch-rate. This motivates a targeted frequency candidate. It does not identify a mechanical resonance independently of policy feedback or establish that the frequency will remain fixed under other operating conditions.

At 50 Hz, calculations for illustrative center 8.2 Hz/Q3 give:

| Filter | Gain at 3 Hz | Gain at 8.2 Hz | Gain at 25 Hz | Phase at 3 Hz |
|---|---:|---:|---:|---:|
| Current MA2 | 0.982 | 0.870 | 0 | -10.8 deg |
| EMA0.5 replacing MA2 | 0.884 | 0.583 | 0.333 | -19.0 deg |
| MA2 followed by EMA0.5 | 0.868 | 0.507 | 0 | -29.8 deg |
| MA2 followed by notch | 0.971 | 0 at exact center | 0 | -19.5 deg |

The notch-combination gain at 8.6 Hz is approximately 0.24; see the JSON for unrounded values. This preserves 25 Hz rejection and reduces the selected band while keeping more 3 Hz amplitude than the EMA cascade. Phase at an exact transfer zero is undefined and recorded as null.

The notch shape is frequency selective. Q controls center frequency divided by the -3 dB bandwidth; Q3 at 8.2 Hz is approximately 2.7 Hz bandwidth. [SciPy's primary documentation](https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.iirnotch.html) defines the second-order notch and its Q convention. Numeric values here were calculated locally, not taken from a robot-control recommendation in that documentation.

## Tradeoffs and limits

- A standalone stable IIR notch is not proof of a stable robot loop. At frequencies below the notch it adds lag; the illustrative combination's phase at 5 Hz is about -37.1 deg versus MA2 -18 deg. Suppressing 8 Hz may expose a different mode.
- Increasing boxcar length introduces broad delay; simply cascading EMA0.5 adds about 30 deg phase lag at 8.2 Hz (combined about -59.5 deg). Stronger smoothing is not a monotonic stability improvement.
- EMA0.5 by itself remains a useful alternative to compare, but it restores a nonzero 25 Hz path. Its earlier sim study covered low-frequency behavior; that does not prove the remaining real 8 Hz motion will disappear.
- Lowering knee Kp can reduce loop gain but also changes load support/posture that motivated 92/2.3. This is a separate gain tradeoff, not a free attenuation mechanism.
- Filtering a recorded action sequence can verify spectral attenuation and finite state handling; it cannot demonstrate how the policy and robot will react after the filter changes.

Next validation should compare MA2 alone, EMA0.5 replacement and MA2+notch using current gains and the same raw-history meaning. Check finite initialization/reset, DC support, transient torque peaks, applied/feedback spectra, pitch motion and command tracking across delay/plant conditions. The nominal plant did not reproduce the real 8–9 Hz mode, so any sim pass remains limited; no existing result proves this candidate on hardware. Future deployment/execution is outside this advice request.

## Saved evidence

[Calculated response JSON](leg_action_filter_residual_options.json) includes the config/checkpoint hash, sample rate, center/Q and notch pole radii. Candidate poles lie inside the unit circle; this is only a filter arithmetic check. Related real data: [first MA2 trial](leg_action_filter_real_review.md).

Only this note and response JSON are added. Production hashes match the preceding deployment manifest; note whitespace review PASS. Required [agent-check](leg_action_filter_residual_options_agent_check.log) is overall FAIL from the six pre-existing `my_flat_env_cfg.py` trailing-whitespace errors; Python syntax 586 PASS and URDF parsing 8 PASS.
