# FlashSAC current training status

Execution Domain: TRAINING_SIM; required repository checks: DESKTOP_DRY_RUN.

Evidence Status: PASS for process/log/checkpoint checks; SUSPICIOUS for ongoing policy quality, with no deterministic evaluation performed in this status check.

Observed at (Asia/Seoul): 2026-10-14T17:48:05.915261+09:00

Policy Checkpoint SHA256 (expanded bounds, model_15000/actor.pt): f330e86adeb4b5be2ed276fae01063df63e15bc625d8ad0125746263c42e73a2

Branch: agent/codex/dev_tita_gluon.

The user requested current training status and whether the robot is surviving. PID 3749238 was directly observed running; baseline PID 3301796 remains paused. No training process, hyperparameter, environment config or source code was modified by this status check.

At the monitoring snapshot, the new run reached 21000 / 100000 vector steps, 41948 learner updates, and 86016000 transitions. All 210 logged rows have finite scalar values. The saved 15000-step actor hash was verified against checkpoint metadata.

Matched vector-step window: 19100–21000, 20 logged rows per run.

| Logged metric | Original bounds | Expanded bounds |
|---|---:|---:|
| Mean completed-episode duration, s | 2.8066 | 19.8994 |
| Mean completed-episode return | 5.5099 | 36.1819 |
| Weighted XY tracking episode reward | 0.2216 | 1.7487 |
| Most-recent termination cause: timeout | 0.555% | 98.987% |
| Most-recent termination cause: base contact | 99.445% | 1.013% |

Maximum episode duration is 20 s; control period is 0.02 s. Current mean duration is close to the horizon and substantially longer than the original bounds at matched training steps. This supports the hypothesis that the original physical action range constrained learning. Resolved learner settings had been verified identical at launch, including repeated noise; this is still a single-seed comparison, not proof that action range explains all convergence differences or that FlashSAC now matches PPO.

The episode-duration metric averages the last 100 completed episodes, then this report averages 20 overlapping log samples; these are not independent trials. Isaac TerminationManager stores the latest termination reason per environment and logs its mean across the environment population, so the timeout percentage is a proxy and must not be labeled an exact 20-second trial survival probability. Step termination/truncation counters are sampled only every 100 steps and cannot recover all event counts.

The XY reward includes weight 2, control dt and upright scaling, is summed over each episode and divided by the fixed 20-second maximum. Its increase includes surviving longer, so reward ratios must not be presented as pure tracking-accuracy ratios. The command error metric divides accumulated errors by the maximum command duration (8 s), rather than actual episode duration; no direct old/new per-step error comparison is asserted. Fixed-speed rollout success and physical velocity/standstill drift remain NOT_TESTED for this checkpoint in this check.

Evidence JSON: tita_flash_sac_action_ranges_status_20261014_174805.json. Source metrics: tita_flash_sac_172127_928297_metrics.jsonl and tita_flash_sac_133201_468020_metrics.jsonl.

W&B: https://wandb.ai/bjy6614-postech/tita_flat_flash_sac/runs/5v50prs6

Changed files in this status task: this new report and its JSON snapshot; the required agent-check log. Actual required checks and final source-integrity verification are recorded after creation in the status check log.
