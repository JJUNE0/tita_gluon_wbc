# Review of the first two new-button hardware runs

- Execution Domains: ROBOT_READ_ONLY (retrieve completed run evidence), DESKTOP_DRY_RUN (offline SQLite/CDR analysis and plotting).
- Evidence Status: PASS for recorded button/state flow, finite signals and computed torque equations; SUSPICIOUS for RL-entry transient and shutdown; NOT_TESTED for unsupported/free balancing or applied-torque calibration.
- Policy checkpoint SHA256: `6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05`.
- ONNX SHA256: `f44f07ed44970e3ff565eae67fd9229adf0be5c02215591c52a691ffcbb71b2a`.
- Branch: `agent/codex/dev_tita_gluon`.

The operator asked for a results review, then reported turning the robot off.
Both complete run bags/consoles/summaries had already been copied locally.
No further SSH connection was made after that message. No robot process,
service, mode or torque command was changed during the review.

## Run 1: 22:17:10 KST, full RL and return sequence

Run ID: `flashsac_60000_221710_783365433_output_true`.
Recorded-state span 38.061 s; 1,909 synchronized publication cycles.
Times below are relative to the first recorded state.

| Event | Time |
| --- | --- |
| Short right press/release; no transition | 3.730–3.935 s |
| Right startup hold begins | 5.672 s |
| Transform_up | 6.675 s |
| Sit | 16.286 s |
| Left axis 4 down | 20.131 s |
| RL | 20.140 s |
| Left axis 4 up | 28.852 s |
| Return_to_sit | 28.854 s |
| Sit again | 31.054 s |

This confirms the short-press cancellation, approximately one-second startup
hold, release of the startup hold without stopping, RL selection on left down,
and 2.2-second pose return on left up. Axis 6 changes and axis 4 changes align
with the intended right/left actions in this operator-run sequence.

RL lasted approximately 8.714 s in recorded state timestamps (8.722 s in console
state timestamps). RL data contains 437 publication samples. All recorded
observations/actions/torques, positions, velocities and tilt values are finite.
Body tilt during RL peaked at 6.13 degrees. Final sit leg-angle errors are
approximately 0.27–2.40 degrees relative to the configured sit target, excluding
wheel angles. This is evidence of pose tracking, not proof of unsupported balance.

The operator confirmed deliberately moving forward/yaw sticks. The inferred
policy commands reached 0.20 m/s forward and 0.171 rad/s yaw; nonzero commands
occurred in approximately 85.6% of RL samples. These inputs are intentional,
not evidence of a neutral-stick offset.

Recomputing the policy action adapter from recorded action/q/dq reproduces
the computed torque topic with maximum error 4.77e-6 N m. The topic records
computed commands; applied motor torque/sign/unit calibration cannot be inferred
from that equation match alone.

**Transient requiring attention:** RL entry shows a brief wheel-speed peak of
18.73 rad/s left and 14.56 rad/s right. Left wheel command reaches its 12 N m
limit in one of the 437 recorded RL samples. The rest of this run has no
sustained recorded torque saturation. Peak body tilt across the full run is
8.76 degrees during the return phase. A future RL-entry target/torque blend is
worth evaluating before treating this as a validated motion controller; no
such implementation change was made in this review. The 50 Hz recording does
not capture every 500 Hz command peak.

## Run 2: 22:18:02 KST, software stop during preparation

Run ID: `flashsac_60000_221802_906489108_output_true`.
Recorded-state span 14.121 s; 709 publication cycles. Right hold starts at
5.421 s; transform_up begins at 6.424 s. Releasing that hold at 7.226 s does not
stop. A new axis-6 down edge at 8.403 s precedes estop at 8.406 s.
Thus the stop was triggered by the new right press rather than a joystick gap:
largest inter-message joy gap was 12.2 ms, below the 0.5 s timeout.

The approximately 3 ms difference is between bag receipt timestamps; it is not
a certified end-to-end hardware response bound. Recorded estop command exactly
matches clipped `-Kd*dq` with the original damping gains (maximum equation
error zero in recorded floating-point values). No further transition out of
estop occurs when right is released at 9.413 s. Policy action remains zero
throughout this run. After 0.5 s in estop, maximum recorded joint-speed magnitude
is 0.105 rad/s. The largest whole-run tilt, 25.97 degrees, occurs before estop;
the estop phase itself peaks at 6.52 degrees.

## Shared findings and limits

- No CAN_TX errors appear in either saved console. No policy failure/nonfinite
  diagnostic or fault-damp transition appears during the recorded run flow.
- Both summaries finalize with runner exit 130 after operator interrupt and
  rosbag metadata exists. Both joystick processes nevertheless exit -7 (SIGBUS)
  during shutdown, and controller groups require TERM then KILL. Graceful
  SDK/joystick shutdown remains unresolved.
- Publication-cycle pairing uses equal topic counts and maximum cross-topic
  receipt-time spread of 2.75 ms in run 1 and 1.48 ms in run 2. State/event
  interpretation combines the console, joy edges and recorded state topic.
- State-flow and computed-command PASS does not establish a successful free
  balancing, torque calibration or residual-control experiment.

## Artifacts and checks

Raw copies remain unmodified under both run prefixes, including SQLite bags,
metadata, console, bag-console and summary. Offline results add `_review.json`
and `_review.png` for each run. The initial snapshot of the latest run was
active, so copying was deferred until its Finished marker/metadata appeared.
No live SQLite database was copied or mutated.

Analyzer: `test/sim2real/review_flashsac_runs.py` (new file); it opens finalized
SQLite files read-only, checks topic-cycle pairing and writes metrics/plots.
Execution log: `flashsac_buttons_results_analysis.log`, exit 0 on both bags.
Plot visually inspected. No production controller source was edited.

Required `./scripts/agent-check.sh`: FAIL solely from existing trailing
whitespace in `my_flat_env_cfg.py` lines 431, 437, 443, 449, 455 and 461; fast
Python syntax and eight URDF parse checks pass. See
`flashsac_buttons_results_agent_check.log`. No commit or push.
