# FlashSAC forward-command and backward-drift diagnosis

- Execution Domain: DESKTOP_DRY_RUN (offline analysis of completed robot recordings).
- Evidence Status: PASS for recorded command delivery and numerical observations; SUSPICIOUS for RL-entry reverse wheel response and weak forward response; NOT_TESTED for the physical root cause and steady neutral balance.
- Policy checkpoint SHA256: `6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05`.
- ONNX SHA256: `f44f07ed44970e3ff565eae67fd9229adf0be5c02215591c52a691ffcbb71b2a`.
- Branch: `agent/codex/dev_tita_gluon`.
- Source run: `flashsac_60000_221710_783365433_output_true` (437 RL publication samples, approximately 8.7 s).

The operator reports that yaw worked, the robot drifted backward at neutral,
and forward stick did not produce visible forward travel. The robot was
subsequently powered off. This diagnosis uses the previously retrieved local
bag only; no further SSH, deployment, mode change or torque command occurred.

## Recorded evidence

Policy commands are recovered from observation indices 6:9 by dividing by
`[2, 2, 0.25]`. Native wheel indices are 3 and 7. Their velocity targets are
`20 * action`; the recorded controller command is
`clip(0.5 * (target - measured_velocity), -12, 12)` N m.
The prior full-run review reproduced the action adapter to within 4.77e-6 N m.
This validates the software equation, not applied torque or hardware sign.

| Selection | Samples | Forward command mean (m/s) | Wheel target mean L/R (rad/s) | Measured wheel speed mean L/R (rad/s) |
| --- | ---: | ---: | --- | --- |
| First RL second, neutral command | 51 | 0 | -5.52 / -6.00 | -3.88 / -4.22 |
| Forward >= 0.195 m/s, absolute yaw < 0.01 rad/s, excluding first second | 143 | 0.19994 | +0.69 / +0.24 | +0.15 / +0.11 |

The forward selection comprises samples from multiple intervals, not a single
settled constant-command experiment. Its average yaw command is -0.000574 rad/s.
The mean of the two wheel targets is negative in 31.5% of those samples; the
mean measured wheel speed is negative in 39.2%. Forward input reaches the
policy, but its resulting common wheel motion remains weak and sometimes
negative. The saved console has no CAN_TX errors.

At the first RL publication, all commands are zero but wheel targets are
-18.97 / -22.20 rad/s, with computed wheel torques -9.46 / -11.11 N m.
Both measured wheel speeds are initially near zero. Thus the initial negative
wheel motion is actively requested by the policy/controller rather than
being explained by a missing forward input alone.

There is also a leg-target discontinuity: measured third-joint angles are
approximately -2.64 rad on both sides at entry, whereas the first policy
targets are approximately -2.08 / -2.04 rad. The sit-to-RL transition switches
directly to policy targets and gains. This makes the entry transition a
concrete suspect for the initial kick; it does not establish the cause of
continued neutral drift.

## Interpretation and limits

The evidence is consistent with the reported backward drift and poor forward
tracking. It establishes a strong entry transient and inadequate recorded
wheel response to forward commands. It does not isolate a persistent neutral
bias: the neutral selection contains only 63 samples and is dominated by the
first second of RL. The observation mapping, IMU frame/offset, leg pose,
physical center of mass and actuator response remain possible sources of a
simulation-to-hardware balance mismatch; none is proven by this recording.
Yaw motion alone does not establish common-mode wheel torque signs/units.

No base translational velocity is recorded. Wheel-derived speed in the JSON
assumes a 0.0925 m radius, no slip and no leg/body rotation, and must not be
reported as measured chassis travel. Debug torque is computed command,
not measured applied motor torque.

A future operator-approved neutral-only recording should separate the entry
transient from subsequent balance behavior, with wheel signs/units and IMU
orientation checked against the established mapping. An entry blend can be
evaluated separately; it must not be presented as a proven steady-drift fix.
No gain, bias, reference, residual, RLS or probing change was made here.

## Artifacts and validation

- Added this report and `flashsac_forward_diagnosis.json`; production code unchanged.
- Offline read-only bag analysis completed successfully and produced the JSON.
- Mandatory `./scripts/agent-check.sh`: see `flashsac_forward_agent_check.log`.
  FAIL from the pre-existing trailing whitespace in `my_flat_env_cfg.py`;
  individual checks are recorded in that log.
- Tracked diff SHA256 before this documentation change:
  `40076fca037839dbd955f4644f404a0e3ea6c8b5e7a3fc86a79bb15150ddab47`.
