# Right-side zero-target velocity finetuning transition

Execution Domains: TRAINING_SIM, VALIDATION_SIM, DESKTOP_DRY_RUN.

Evidence Status: SUSPICIOUS for learned right policy quality (NOT_TESTED);
right main process and online logging are active. Left training/assessment/upload completed.

Policy Checkpoint SHA256, right initialization source:
`7f5da9261f795218ce7bfca52a6878b5b51f91426cb3313f218ea4d52d840b32`.
Right new checkpoint hash: PENDING until its first scheduled save.

Branch: `agent/codex/tita-walk`.

Operator requested starting the opposite (right support) side. Existing serial
queue is retained to preserve the one-learner-at-a-time preference. Left was
already at98800/100000 when inspected, so it was allowed to finish rather than
interrupt its last scheduled checkpoint. No duplicate right job is launched.

Right source: `mj_lab/logs/flash_sac/tita_mjlab_135938_442647/model_20000`.
The actor hash and saved task `stand_one_leg_anchor_right` were verified.
It will load that right-side actor/critic into the already validated new
reward config: zero yaw deadband, yaw squared cost weight−0.05, and unbounded
soft-L1 support-point speed cost weight−0.05 /scale0.1 m/s. Other lift-first
rewards, physics, PD, reset settings and contact terminations are unchanged.
Current task source SHA256 matches the completed left producer's recorded
source hash `9d197787beb9554712975e1c6733204acd93fb9e125d8c8ab4f06e5db620fe99`.

Right budget:100000 additional vector steps,1024 environments, seed42, fresh
optimizers/replay/reward normalization with network warm start. W&B online,
checkpoints every5000,40 s policy videos every10000 control steps. Its final
64-environment20 s frozen assessment and evidence upload remain scheduled.

At initial inspection, preceding left video uploads for10k through90k all
reported PASS. Left's latest sampled completed-episode log at99100 reported
single support19.88 s, support-point speed0.486 m/s, base speed0.314 m/s and
world yaw speed0.557 rad/s. These are sampled training episode statistics,
not the pending final frozen evaluation or proof of full stationary balance.

Changed files in this follow-up: only this dated transition report. No training
source, reward weight, saved checkpoint, or unrelated user change is modified.
Actual right startup and final checks are appended after observation below.

Left final actor SHA256: `a9645a17fe766c66a539f7aec4e1e32e5b53fa42af6bb948e337e34612697718`.

## Actual right startup

Left finished100000 vector steps /199802 finite updates. Its final frozen
assessment and evidence artifact upload completed before the right process
started. Final evaluation execution PASS; strict stationary/low-lift capability
SUSPICIOUS, as retained in its evaluation JSON. This transition does not claim
perfect left policy quality.

Right producer PID843342; W&B
[online](https://forge.coreweave.com/wandb/bjy6614-postech/tita_flat_flash_sac/runs/p4c2znlg).

Observed right native run ID: `tita_mjlab_180916_898387`. Direct latest step/update snapshot: `600 /1002`.

Actual saved CLI arguments verify right task, requested20k warm-start source,1024 environments and100000 additional steps. Source weights load into a fresh optimizer/replay/normalizer using the modified environment. A separate remote W&B check is recorded in `one_leg_right_zero_velocity_wandb_startup.json`. New checkpoint hash remains pending first5000-step save. Future right video/final assessment uploads are scheduled, not yet claimed executed.

Left execution status: `completed`; evaluation policy quality: `SUSPICIOUS`.
