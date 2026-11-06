# Original pose settings with settled wheel-position reference

Execution Domain: TRAINING_SIM

Evidence Status: SUSPICIOUS — main training in progress; setup/finite updates PASS; learned behavior NOT_TESTED.

Policy Checkpoint SHA256 (main run): PENDING until first scheduled checkpoint at step 5000.

Baseline policy SHA256: 5002e3e3aa32a116d0221dca2ab52d6855b1b792045b1b5ea9374bbbe00a1408

Validation policy SHA256: 42fb38ad2376a64f3a7fbdfddc88812db6372220e78b65c523b0aee17f50d19c (separate 16-step setup probe).

User intent: reproduce the best overall original roll/pitch/height experiment and add only the wheel-position stopping behavior.

Important clarification: original model_25000 already observes wheel_position_error and heading_error. No extra coordinate observation was added. The experiment changes settling/latching and moving-anchor behavior, with actor/critic dimensions remaining 38/42.

Baseline: /home/cocel/Desktop/Research/tita_gluon_wbc/mj_lab/logs/flash_sac/tita_mjlab_202755_365015/model_25000

Original settings retained:

| Setting | Value |
|---|---|
| Task / learner | flat_roll_pitch_height / FlashSAC |
| Environments / seed / budget | 4096 / 42 / 100000 vector steps |
| Velocity goals | vx +/-1.5 m/s, vy 0, yaw +/-3 rad/s; resample 6–8 s |
| Zero velocity draw | 10% |
| Pose goals | roll +/-30 deg, pitch +/-15 deg, height 0.27–0.42 m |
| Nominal pose draw | 20%, roll/pitch 0 and height 0.335 m |
| Pose ramp / sampling | 0.15 rad/s roll/pitch, 0.02 m/s height; resample 10–12 s |
| Episode / contact termination | 20 s / base contact only |
| Height / orientation weights | -10 / -5 |
| Hip / shoulder / angular XY weights | -1 / -0.5 / -0.05 |
| Mirror / termination reward | 0 / absent, preserved exactly from this baseline |
| Action-rate / joint-acceleration weights | -0.01 / -2.5e-7 |
| Action gains per leg, both signs | [2.8, 2, 2.8, 6]; native position scale 0.25, wheel velocity scale 20 |
| PD leg 1–2 / knee / wheel | 60/1.5, 92/2.3, 0/0.5 |
| Replay / warmup / batch | 1000000 / 100000 / 2048 transitions |
| Updates / gamma / n-step | 2 per vector step / 0.99 / 3 |
| Actor / critic | 2 blocks of 128 / 2 blocks of 256 |
| Learning rate | 0.0003 to 0.00015; 200000-update decay |
| Delay/gain/terrain/reset/push/sensor DR | identical saved configuration |

Only environment changes confirmed by complete native config comparison:

- commands.base_velocity.wheel_error_velocity_thresholds: None -> (0.1 m/s planar body speed, 0.15 rad/s yaw). The existing near-zero command bands must also hold.
- commands.base_velocity.wheel_error_moving_anchor: False -> True; bound the wheel-integral reference and world-position reward anchor to the existing 0.3 m limit.
- commands.base_velocity.stop_state_after_pose: False -> True; update stop state once from the final command emitted after pose handling.

Reward functions/weights are preserved; stop-reference eligibility changes the existing position-hold observation and reward reference behavior. This is not a new absolute x/y pose estimator.

Execution/verification:

- Native latch regression: PASS, 1 selected test; 1 unrelated sit/stand case deselected. Verifies coasting does not latch, settled state latches, moving reference bounds error, and sim2sim/training wheel errors agree. Log: pose_baseline_latch_tests.log.
- Real fresh CLI probe: 4096 environments, 16 steps, 14 finite updates; PASS. Probe: /home/cocel/Desktop/Research/tita_gluon_wbc/mj_lab/logs/flash_sac/tita_mjlab_112428_632381/model_16.
- Full saved native-config comparison: PASS, exactly the three changes above; all action gains and dimensions equal.
- Effective FlashSAC config reconstructed from original 100k arguments: PASS, zero learner differences.
- The first raw/pre-construction learner comparison flagged automatically derived entropy/compile fields. The checker was corrected to compare effective post-construction configs; initial log retained as pose_baseline_latch_config_check_initial.log.
- Main launch arguments compared to original: only run name, video length 500 -> 2000 frames, and the new inactive standing_height_only=False field differ. No resume or warm start.
- python3 -m py_compile and new-file whitespace/diff inspection: PASS.
- ./scripts/agent-check.sh: PASS, direct log pose_baseline_latch_agent_check.log.
- Source hash audit: PASS, no existing source changes or deletions.

Changes: new verification script test/check_pose_baseline_latch_config.py and experiment evidence under docs/exp/2026-10-31. Existing training/controller source already implemented the intended three changes, so no production source edit was needed.

Main run:

- Run ID: tita_mjlab_112630_629104
- Checkpoints: /home/cocel/Desktop/Research/tita_gluon_wbc/mj_lab/logs/flash_sac/tita_mjlab_112630_629104
- W&B online: https://forge.coreweave.com/wandb/bjy6614-postech/tita_flat_flash_sac/runs/c66lkeht
- Initialization: from scratch; no checkpoint weights/optimizer loaded.
- Latest observed step: 900; finite learner updates: 1748.
- Save every 5000 steps; video every 10000 steps, 2000 frames using the saved playback contract and velocity overlay.
- Persistent tmux session: tita_pose_baseline_latch_20261031
- Console: pose_baseline_latch_training.log; launch details: pose_baseline_latch_launch.json.

Limits: configuration and startup validation do not establish trained performance. Whether the old pose behavior is retained while stop rollback improves requires later checkpoint evaluation. No physical robot actions.

Branch: agent/codex/tita-walk. No commit or publication.
