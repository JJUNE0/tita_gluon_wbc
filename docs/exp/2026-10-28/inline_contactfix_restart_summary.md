# Restart inline training after contact-force sign correction

Execution Domains: TRAINING_SIM, DESKTOP_DRY_RUN.

Evidence Status: PASS for stopping the old run, verified fresh training launch,
source hashes and historical mjlab config audit. Corrected policy foot lifting
and 100k completion are NOT_TESTED. A fresh Isaac physics/force retest was not
executed (NOT_TESTED); its source/API path was inspected.

Policy Checkpoint SHA256 (preserved old inline model_40000):
`091dd6df185de10d9b1d6848ef9eb3f667e9f668e9822967248816df3a012dd7`.
New run checkpoint SHA256: N/A until its first scheduled 5,000-step save.
Branch: `agent/codex/tita-walk`. No commit, push, PR, robot command or deployment.

## Previous walk scope

Yes: previous mjlab walking used the same
`mj_lab.robots.tita.mdp:contact_schedule` reward, including the completed
fixed-wheel 100k walk and later hybrid walk. Their common pre-fix function
compared signed world z against +5 N. Native mjlab forces on this sensor path
are negative when the wheels support the robot, so these prior experiments
also had incorrect gait-contact classification. This establishes an affected
reward term, not that every aspect of each policy failed to learn.

Saved configs verified in this turn:

- `mj_lab/logs/flash_sac/tita_mjlab_014010_434558/model_100000`; actor SHA256 `0868450122ce8a8e41ae04e42c0b1ff2d0567ffcad3f9c27e35315aef4f18913`.
- `mj_lab/logs/flash_sac/tita_mjlab_085110_097268/model_40000`; actor SHA256 `32eb7b6dcdb16571b963de54cfab2ed14658fa499f75ef6c416f5d4dc71ee993`.
- `mj_lab/logs/flash_sac/tita_mjlab_093903_465777/model_50000`; actor SHA256 `6051d031f8df0c0d0f267613c9e3493f0c555d1d63ad6947690ca52a3016afaa`.

All reference the same shared reward with weight 2. The original function and
actual negative support-force measurements are preserved in
`inline_lift_30000_summary.md`, `inline_lift_contact_sign_diagnosis.json` and
`inline_lift_before_mj_lab__robots__tita__mdp.py.txt`. One other earlier run's
checkpoint directory was unavailable during this audit:
`tita_mjlab_103305_882054`; its historical report was left
untouched rather than claiming a new checkpoint verification.

Isaac walk uses a different function and sensor path:
`isaac_lab/.../robots/tita/walk_mdp.py:_contacts` reads
`contact_forces.data.net_forces_w`. The installed Isaac ContactSensor source
describes these as world-frame normal forces **on the rigid body**, populated
by PhysX `get_net_contact_forces`. This differs from the mjlab contact-wrench
orientation used in the port. The demonstrated mjlab sign error must not be
attributed to the Isaac run solely because both versions compare a z component.
Isaac training sources were not changed or freshly rerun in this task.

Flat driving does not configure this gait-contact reward, so it is not directly
affected by this defect. Base/knee termination already uses force magnitude.

## Correction and validation

The shared mjlab reward now detects contact using force magnitude >5 N,
independent of sign. This source correction was completed and checked during
the preceding analysis task; no further production-code changes were needed
for this restart.

Executed on the same corrected code before launch:

- PASS: 29 native tests / 8 task-specific skips, including positive/negative
  support, one-foot swing, both unsupported and disabled-gait masking;
  `inline_lift_contact_regression.log`.
- PASS: `./scripts/agent-check.sh`, rerun for this restart report;
  `inline_contactfix_restart_agent_check.log`.

No other reward coefficient, action mapping, gait/command setting, sensor
configuration or FlashSAC hyperparameter was changed for this restart.

## Stopped run and new experiment

Old run `tita_mjlab_105509_377182` received SIGINT and exited at step
44,246 / 88,293 updates. Its automatic FAIL/KeyboardInterrupt
result records the requested interruption. The preserved last checkpoint is
`mj_lab/logs/flash_sac/tita_mjlab_105509_377182/model_40000`. No weights were loaded
from it into the new experiment.

New run: `tita_mjlab_114239_024280`.

- PID 1149474; tmux `mjlab_inline_contactfix_20261028_114235`.
- **Fresh actor, critic, optimizer, observation/reward normalization and
  replay**. Saved args explicitly show resume=None and warm_start=None.
- 1,024 environments, 512 straight-only and 512 mixed flat commands;
  seed 42, CUDA 0, FlashSAC, 100,000 requested vector steps.
- Full gait cycle 2 s (0.5 Hz), left/right offset 1 s, per-foot swing 0.4 s;
  wheel drive retained. Actor/critic dimensions 40/44.
- Checkpoint every 5,000 steps; W&B video every 10,000, 500 frames with existing
  vx/vy overlay and stop/forward/backward/turn preview schedule.
- Verified initial snapshot: 1,200 steps /
  2,202 finite updates. This is launch health, not learned
  foot-lift evidence.
- W&B: https://forge.coreweave.com/wandb/bjy6614-postech/tita_flat_flash_sac/runs/bao6gz19
- Checkpoints: `mj_lab/logs/flash_sac/tita_mjlab_114239_024280/model_<step>`.
- Console: `inline_contactfix_training_console.log`; metrics:
  `tita_mjlab_114239_024280_metrics.jsonl`; exact argv and source SHA256:
  `inline_contactfix_training_launch.json`.

The old trainer is confirmed exited and the new trainer's source hashes match
the corrected files. The new run has not been hot-patched.

## Files and review

Created/updated experiment evidence only in this turn:
`inline_contactfix_previous_stop.json`, `inline_contactfix_training_launch.json`,
`inline_contactfix_prior_walk_audit.json`, this report, console/check logs and
the new run's normal evidence. No additional production source changes, commit
or publication were made. The previous task's correction to `mdp.py` and its
regression remain in place.

Starting status: `inline_contactfix_restart_preexisting_status.txt`. Final
status/diffs were inspected; pre-existing edits/staged renames were preserved
and no unrelated source files were changed. Remaining work is to evaluate
physical foot lift on checkpoints from this corrected run; the old policies'
measurements do not establish the new policy's performance.
