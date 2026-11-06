# Height-only sit/stand configuration and deferred training

Execution Domain: TRAINING_SIM

Evidence Status: SUSPICIOUS — reservation active and setup/queue tests PASS; training has not started and learned behavior NOT_TESTED.

Policy Checkpoint SHA256: PENDING — this fresh policy will initialize only after both predecessor jobs finish.

Configuration source SHA256: 8c070e3e0bdd3946e0232203ca1495a1f19e5d85372d7a72c1fa5f6a8aee4308

User requirements: velocity and roll/pitch commands zero; full sit/stand height changes at 0.05 m/s; abs roll OR pitch over 30 deg terminates; widened IDLE-capable action envelope; keep 20-s episodes (explicit user clarification); random 1–3-s waits at each endpoint; start only after both active one-leg runs finish.

Implemented as a separate height_only task:

- Height goals alternate 0.08 m seated and 0.335 m standing. Every reset first holds the standing reference for 1–3 s.
- Reference height ramps at 0.05 m/s. The sampled 1–3-s dwell starts after the emitted reference reaches the endpoint. Travel time is added to each command timer, so a new target cannot interrupt the descent/ascent.
- One-way reference travel is 5.1 s; the initial standing dwell plus a sit/stand cycle takes 13.2–19.2 s, fitting in 20 s.
- Actual sitting/standing durations and completed sit-then-stand cycles are measured separately using physical root height; issuing a command alone does not count as success.
- vx/vy/yaw and roll/pitch targets are always zero. Wheel control remains available for balance. Observation/action dimensions remain actor 38, critic 42, actions 8.
- Termination: time_out plus per-axis roll_pitch only. Positive or negative roll/pitch >30 deg terminates; yaw is excluded from that test. Base/knee contact is allowed throughout.
- Expanded sit_stand action mapping retained: negative [3,2,4.8,6] per leg, positive [3,2,3.2,6]. It covers IDLE hip +/-0.75, leg_2 1.2, knee -2.7 rad.
- Existing physics, actuator PD/delay/gain DR, friction/reset/push/sensor randomization are preserved. Height loss coefficient is inherited -50; orientation -5 and smoothness terms are retained. Added explicit terminal failure penalty -10.
- Contact and hip/shoulder deviation costs relax by emitted goal height below the inherited 0.20–0.27 m transition range. Contact alone does not terminate a seated episode.
- No late 20000-step curriculum transition.

Reservation mechanics:

- Persistent tmux session: tita_height_only_after_legs_20261031
- Plan: height_only_queue_manifest.json; live state: height_only_queue_state.json; watcher log: height_only_queue_console.log.
- Both captured PID/start-tick/boot-ID identities must exit. Each final model_100000 actor hash and metadata step must verify, and each result must report the matching completed step/checkpoint with PASS or SUSPICIOUS (e.g. a post-training video warning), not FAIL.
- Both predecessors finish video/W&B cleanup before exit. They receive no signals or config changes from the queue.
- Duplicate concurrent queue execution is locked; once=True prevents restarting an already launched job.
- A cancelled, incomplete, corrupt or failed predecessor prevents the height job from starting.
- The queued job runs from scratch: FlashSAC, 4096 envs, seed 42, 100000 vector steps, 1M replay, minimum 100000, batch 2048, two updates per step. Online W&B and videos every 10000 steps (2000 frames); checkpoints every 5000 steps.
- Future checkpoint run ID and W&B URL are generated when the child actually starts. Its console path and final checkpoint/hash/URL are recorded in live queue state.

Observed reservation state: waiting_for_dependencies.
- left: tita_mjlab_201526_016988, last observed step 13100/100000.
- right: tita_mjlab_201526_001807, last observed step 12900/100000.

Verification actually executed:

- Environment/legacy compatibility tests: PASS, 26 tests. Includes ideal reference cycle completion within 20 s, random dwell and rate bounds, actual-vs-command cycle metrics, partial-reset isolation, both signs of per-axis 30-deg failure, widened IDLE targets and 38-D playback contract.
- Native 8-environment validation: zero-action simulation and forced orientation checks passed, with no policy/optimizer creation or learner update. The two existing learner runs were not interrupted. One existing mass/inertia DR warning was recorded.
- Queue tests: PASS, 6 tests including legacy single-dependency behavior, real two-process wait/handoff, failure/corruption preventing launch and completed-queue replay not duplicating training. Test children are synthetic processes, not learners.
- Logs: height_only_tests.log and height_only_queue_tests.log.
- All five task source files compile; new-file whitespace and incremental diff review PASS. Source audit found only the task registry and queue runner changed among existing files; unrelated work preserved.
- ./scripts/agent-check.sh: PASS; direct log height_only_agent_check.log.
- Live reservation check: both predecessor identities still active, queued job pending, no height_only training args/run created.

Changed files:

- Added mj_lab/robots/tita/height_only_env_cfg.py.
- mj_lab/scripts/train.py: register height_only.
- scripts/queue_mjlab_flash_sac.py: optional multiple predecessors/result verification, optional comparison stage and once guard; legacy manifest support retained.
- Added test/test_mjlab_height_only.py and test/test_height_only_queue.py.
- Evidence under docs/exp/2026-10-31/height_only*.

Unresolved limits: reference timing is not a guarantee that the robot tracks or holds each physical pose. Full sit/rise learning and the suitability of the 30-deg limit need evaluation after training. No trained success or hardware readiness is claimed.

Branch: agent/codex/tita-walk. No commit, publication or hardware commands.
