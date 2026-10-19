# Recent FlashSAC command response and zero-command drift

- Execution Domains: ROBOT_READ_ONLY (retrieve completed recordings and source hashes), DESKTOP_DRY_RUN (offline analysis and plotting).
- Evidence Status: PASS for copy integrity, command delivery, finite signals, computed torque equations and measured yaw response; SUSPICIOUS for sustained neutral wheel drift and return-to-sit tilt; NOT_TESTED for calibrated chassis velocity and disturbance rejection specifications.
- Policy checkpoint SHA256: `6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05`.
- ONNX SHA256: `f44f07ed44970e3ff565eae67fd9229adf0be5c02215591c52a691ffcbb71b2a`.
- Latest config SHA256: `d429ad9e60c25137d4bb5e2f26cb50a469fbcecf3a28af0076918a49eb7c035d`.
- Branch: `agent/codex/dev_tita_gluon`.

## Main finding

The latest run contains sustained zero-command wheel drift well after RL
entry. It also shows strong agreement between yaw commands and measured body
angular velocity. These behaviors can coexist: transient command response and
posture recovery do not establish that zero-speed tracking has no offset.
This recording resolves the previous uncertainty that neutral observations
were limited to the initial entry transient.

All times below are relative to RL entry. Wheel-equivalent velocity means
`0.0925 * (left_wheel_velocity + right_wheel_velocity) / 2` m/s. It assumes
rolling without slip and ignores leg/body rotation; it is not measured chassis
velocity. Debug torque is a computed command, not applied motor torque.

## Runs and integrity

| Run start (KST) | RL span | Config maximum forward/yaw | CAN_TX errors |
| --- | ---: | --- | ---: |
| 22:21:39 | 39.66 s | 0.2 m/s / 0.3 rad/s | 0 |
| 22:32:17 | 71.16 s | 1.0 m/s / 1.0 rad/s | 0 |

Run IDs: `flashsac_60000_222139_051376383_output_true` and
`flashsac_60000_223217_076704901_output_true`.
Both summaries include Finished markers and finalized bag metadata.
SBC and desktop SHA256 values agree for both databases and their metadata;
SQLite quick_check is OK. The interrupted retrieval was checked before use.

A few topics have one fewer sample than others. Analysis uses nearest receipt
timestamps within 8 ms and disallows reuse of a matched sample. Two reference
cycles are excluded from each run: 3,499/3,501 and 5,501/5,503 retained.
Largest retained offset is 3.11 ms in the first run and 3.88 ms in the latest.
Recomputing the action adapter reproduces recorded RL torque within
7.63e-6 N m in both runs. All analyzed numeric signals are finite.

## Zero-command drift is present beyond startup

The latest run has a continuous 24.62-second neutral interval from
RL+11.14 to +35.76 s. Both recorded sticks are zero, and policy commands
remain below 0.01 in physical units. After excluding the first two seconds
of this interval, all commands and both sticks are exactly zero in the
retained 1,131 samples, spanning approximately 22.6 s.

Across those samples:

- Mean measured wheel velocities: -0.526 / -0.854 rad/s.
- Mean policy wheel targets: -2.173 / -2.471 rad/s.
- Mean computed wheel torques: -0.756 / -0.775 N m.
- Wheel-equivalent velocity mean -0.064 m/s, median -0.138 m/s;
  negative in 68.5% of samples.

The interval includes large unlabelled responses, possibly the operator's
reported disturbance tests. Its aggregate mean is not an isolated constant
drift rate. More informative low-posture-variation examples are:

| Zero-command interval | Mean wheel equivalent (m/s) | Pitch mean/std (degrees) | Mean wheel targets L/R (rad/s) | Mean computed wheel torques L/R (N m) |
| --- | ---: | --- | --- | --- |
| RL+13.14 to +14.14 s | -0.202 | 0.40 / 0.12 | -2.90 / -3.11 | -0.400 / -0.425 |
| RL+24.14 to +25.14 s | -0.202 | 2.00 / 0.08 | -2.82 / -3.09 | -0.384 / -0.386 |

Both wheels remain negative throughout each example. The second occurs
approximately 24 seconds after RL entry. This cannot be attributed solely to
the first sit-to-RL kick. The policy actively requests negative common wheel
motion while the input command is zero; it is not just failing to receive a
forward stick command. Small pitch variation does not prove absence of an
external force, so these are descriptive examples rather than force-free
calibration trials. Their different mean pitches also do not identify a
single IMU offset correction.

The earlier 22:21 run contains no continuous neutral interval of at least
three seconds under the same criteria, so it cannot supply an equivalent
steady-neutral comparison.

## Command response and reported disturbance recovery

The latest maximum absolute observed commands reach 1.0 m/s and 1.0 rad/s.
For RL samples after the first two seconds with absolute yaw command >=0.1
rad/s (931 samples), commanded yaw and measured body gyro z have correlation
0.9977 and RMSE 0.0667 rad/s. Body gyro z approximates heading rate at small
roll/pitch; the metric is not an independent world-frame heading estimator.
Positive and negative yaw responses visibly follow the command ramps.

For forward >=0.15 m/s and absolute yaw <0.03 rad/s, the latest run has 498
samples: average command +0.472 m/s and average wheel-equivalent response
+0.249 m/s. Reverse samples under the corresponding criterion (72 samples)
average -0.333 m/s command and -0.633 m/s wheel equivalent. These selections
include transients, unequal command ranges and operator interventions; their
means are not a settled tracking gain. The time series shows correct common
wheel response to large forward/reverse commands while neutral drift remains.
The older low-limit run's forward selection averages +0.194 m/s command and
+0.060 m/s wheel equivalent. This is descriptive, not a controlled A/B test.

RL tilt peaks at 10.87 degrees in the latest run. The policy continues running
through several zero-command oscillatory responses. This is consistent with
the operator's report of recovering from disturbances, but no external force
sensor or push-event markers exist in the bag. Disturbance amplitude,
recovery time and return to the original position cannot be certified from
these signals alone.

## Interpretation and next diagnosis

Joystick neutral bias and missing command delivery are not supported as the
cause of the long neutral interval: raw sticks and delivered commands are
both zero. No CAN send error appears. The torque equation also matches the
configured action adapter. Hardware torque sign/unit calibration is still
distinct from these software checks.

The current 33-element actor input contains angular velocity, gravity,
commands, joint positions, joint velocities and last actions. There is no
direct measured chassis forward velocity or absolute position input, and the
runtime has no separate position-hold/integral correction. A learned balance
policy can therefore retain a translational offset even when posture and yaw
responses look good. The observed negative common wheel targets support
investigating the closed-loop balance point and dynamics rather than treating
the problem as only a joystick scale issue.

The operator also reports forward drift in MuJoCo with this same policy.
That is operator evidence, not a simulation rerun in this review. Opposite
directions in simulation and hardware make copying a simulation bias value
inappropriate without checking the real operating point. IMU frame/reference,
leg posture, center of mass and actuator response remain hypotheses; this
recording does not isolate one root cause.

Next comparison should separate zero-input balance before/after disturbances,
use repeated no-touch neutral trials, and check IMU/leg pose and common wheel
response against simulation. If a residual is evaluated later, neutral
common-mode drift and yaw/command response should be separate acceptance
metrics. No residual, RLS, gain, bias, reference or probing change is enabled
by this analysis.

## Additional transition finding

At RL+71.17 s the latest run selects return_to_sit. At +72.12 s, approximately
0.95 s later, it enters damp with recorded tilt 37.31 degrees, exceeding the
0.65 rad (37.24 degree) tilt threshold. Thus posture return did not complete
normally in this run. Whether the operator was supporting or repositioning
the robot at that moment is not recorded. This deserves separate review from
the RL neutral drift. During RL, left/right wheel torque limits are reached
in only 0.365% / 0.225% of publication samples, so persistent saturation does
not explain the whole drift interval.

Both runs still require TERM then KILL at shutdown; the joystick exits -2
after interrupt. Shutdown behavior remains unresolved.

## Artifacts and checks

- Added offline analyzer: `test/sim2real/analyze_flashsac_drift.py`.
- Added this report, raw run copies and SHA256/retrieval logs in this dated directory.
- Each run adds `_drift_analysis.json` and `_drift_analysis.png`.
- PASS: analyzer executed on both bags; log `flashsac_recent_drift_analysis.log`.
  Latest plot visually inspected.
- Required repository check: `flashsac_recent_drift_agent_check.log`; known
  unrelated trailing-whitespace failures and individual test results are retained there.
- No production source edits, deployment, robot controller execution, MCU
  mode changes, service changes or torque tests occurred in this review.
- Existing tracked diff SHA256 before review:
  `40076fca037839dbd955f4644f404a0e3ea6c8b5e7a3fc86a79bb15150ddab47`.
