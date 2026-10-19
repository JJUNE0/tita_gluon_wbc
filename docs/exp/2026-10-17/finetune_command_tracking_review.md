# Fine-tuned policy: per-command tracking review

Execution Domain: DESKTOP_DRY_RUN (analysis of existing VALIDATION_SIM traces)

Evidence Status: SUSPICIOUS — reverse tracking and residual yaw after rotation regress despite better aggregate metrics.

Policy Checkpoint SHA256 (source): `6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05`

Policy Checkpoint SHA256 (candidate): `86ae7466db5680d41038d230cee0fec347c100a7139060b21dc40af96bc57baf`

Branch: `agent/codex/dev_tita_gluon`.

## Observed metrics / behavior / log summary

Reanalyzed the 120-second flat-floor command trace, seed104. Each phase lasts 20 seconds.
The table reports the mean of the final 10 seconds of each phase. Forward velocity is
MuJoCo body-frame ground truth; yaw rate is body gyro z, rather than independent heading rate.
The student runs without any residual controller. No new training, simulation, hardware
connection or policy/source change was performed for this review.

| Phase | Command vx / yaw (m/s, rad/s) | Source mean vx | Candidate mean vx | Source mean yaw | Candidate mean yaw |
| --- | --- | ---: | ---: | ---: | ---: |
| initial_stop | +0.000 / +0.000 | +0.017696 | -0.000801 | -0.000964 | -0.001459 |
| forward | +0.100 / +0.000 | +0.256300 | +0.234495 | +0.005025 | +0.004193 |
| stop_after_forward | +0.000 / +0.000 | +0.017895 | -0.000093 | -0.000964 | -0.001447 |
| reverse | -0.100 / +0.000 | -0.227363 | -0.245834 | -0.006650 | -0.005825 |
| yaw | +0.000 / +0.200 | +0.011483 | -0.003394 | +0.152648 | +0.179213 |
| final_stop | +0.000 / +0.000 | +0.013599 | +0.000814 | -0.046057 | -0.055106 |

Reverse steady-window forward RMSE increased from 0.127364 to
0.145834 m/s (+14.5%). Forward +0.1 m/s improved,
but still travels about 0.2345 m/s: existing command gain error remains. Positive yaw
tracking improved during rotation, while yaw after the subsequent stop worsened from
about -0.0461 to -0.0551 rad/s. Better forward stopping does not establish full pose/yaw hold.

Earlier aggregate full-sequence forward RMSE was 0.082904 -> 0.080890 m/s, and yaw RMSE
0.052687 -> 0.047258 rad/s. These aggregate acceptance criteria were met, but they do
not establish per-command non-regression. Stops and forward/yaw improvements can mask
reverse degradation. This review qualifies the earlier aggregate acceptance result.

The runtime `--velocity_bias` controller resets/decays its correction during moving
commands. The learned student changes eight constant output mean biases, which apply
at all commands, with no zero-command gate. Its demonstrations were collected only at
zero command. Consequently moving-command behavior has no per-command preservation guarantee.

This is one deterministic command sequence and one held-out initial condition, not a
speed sweep or repeated isolated command trials. Negative yaw, other nonzero speeds,
changed physics and hardware preservation remain NOT_TESTED by this command review.
The appropriate next comparison is balanced stop/forward/reverse/both-yaw data, an
original-policy behavior preservation loss on moving commands, and separate per-command
acceptance thresholds. General velocity tracking improvement is not established.

Machine-readable per-phase full-window and final-10-second RMSE, BC-only comparison,
and trace hashes are in `finetune_command_tracking_review.json`. The original traces
remain in `finetune_improvement/heldout_flat/`.

Only this report, its JSON and the completion-check log were added by this review.
Repository check output: `finetune_command_tracking_agent_check.log`.
