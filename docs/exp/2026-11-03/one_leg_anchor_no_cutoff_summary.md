# Remove the support-position failure cutoff and restart both sides

Execution Domains: TRAINING_SIM, VALIDATION_SIM, DESKTOP_DRY_RUN.

Evidence Status: SUSPICIOUS — modified-task tests PASS; replacement full-run
startup and remote online metrics PASS. Learned behavior NOT_TESTED.

Policy Checkpoint SHA256, preserved prior left20k:
`f202306efe2fed4ff4bf50e729d93162fa37afa1bfb8643311e0bd6f606848c4`.
Policy Checkpoint SHA256, preserved prior right20k:
`027eead8f52b9aab9d10deb4c5e758e64ed8d4eaee8bfe2b6e89422d26f48d0c`.
Replacement main checkpoint hashes: PENDING until their first scheduled saves.

Branch: `agent/codex/tita-walk`.

## Behavior change

Operator requested removing immediate termination when the support wheel
leaves the initial 10 cm radius. Fresh left/right anchor tasks now terminate
only on inherited base contact, knee contact, or the 20 s time limit. The
support anchor, position/speed costs, slow-yaw allowance, 4–8 cm swing target,
COM proximity, wheel-overlap cost, all weights, physics, observation/action
interface, and DR remain unchanged. Crossing 10 cm is logged and can fail the
strict success metric, but no longer resets the environment.

The old `support_drift_failure` callable remains for earlier env.pkl files;
the new configuration does not register it. Existing checkpoints keep their
saved cutoff when replayed; no saved checkpoint was patched.

The evaluator supports both old and new termination lists and now reports
`has_support_drift_termination` and `outside_10cm_fraction`. The persistent
runner accepts a label so replacement runs use separate state/log/artifact
names without overwriting the earlier experiment.

## Prior run diagnosis and operator-linked baseline

At20k, the sampled left/right logs showed226/254 support-drift terminations,
zero base/knee terminations and zero timeouts. The last100 completed episodes
had mean lengths4.19/3.68 control steps (0.0838/0.0736 s at50 Hz). These are
step counts in `episode_length_mean`, not seconds. The data show extreme
early failure termination by the task's added rule; they do not isolate all
effects of the new rewards.

The operator linked [baseline s8fqfbo2](https://forge.coreweave.com/wandb/bjy6614-postech/tita_flat_flash_sac/runs/s8fqfbo2),
the original independent fixed-left reference run
`tita_mjlab_201526_016988`. Remote W&B history was read with the authenticated
SDK; matching local history is also available. At5000 vector steps its
reported episode mean single-support time was13.8801 s, versus0.03393 s in
the new cutoff run. At500/1000 steps the baseline had0.1070/0.1215 s.
This supports earlier acquisition of supported lifts; the historical logs do
not measure seconds from each reset to the first successful lift.

The baseline also had a reported mean episode peak swing clearance of0.2699 m
at5000 steps and0.5405 m at10000 steps, above the operator's newly requested
low-lift objective. It differs in both termination and reward design (loose
pose_hint, weak base-speed cost, no COM/height shaping); therefore this is not
a controlled attribution of the slowdown solely to the cutoff. This revision
removes only the requested cutoff, retaining the low-lift and positioning goal.
Remote evidence: `one_leg_anchor_no_cutoff_baseline_remote.json`.

## Experiment transition

Both previous main producers received verified PID-specific SIGINT at20168
vector steps /40136 learner updates. Last complete checkpoints at20000 are
preserved in their original run directories. Their generic trainer result is
FAIL/KeyboardInterrupt because this was an intentional operator-requested
replacement, not a numerical training failure. Scheduled20k video rendering
and W&B cleanup were allowed to finish. Stop provenance and previous sampled
metrics: `one_leg_anchor_no_cutoff_previous_stop.json`.

Replacement: independent fresh left/right policies, 1024 environments each,
100000 vector steps, seed42, identical FlashSAC/replay/update settings, online
W&B, checkpoints every5000 and40 s videos every10000 control steps. No
resume/warm start. A frozen64-environment final evaluation and W&B evidence
upload remain scheduled after producer completion. Label `no_cutoff` keeps
the new logs/state separate from the stopped experiment.

## Validation and scope

- PASS: 15 scoped tests, including actual CUDA partial-reset/anchor isolation,
  world translation of25 cm without termination or anchor relatching on both
  sides, timeout semantics, saved interface, and legacy reference regressions.
  `one_leg_anchor_no_cutoff_tests.log`; three inherited mass/inertia warnings.
- PASS: fresh left/right native CLI probes, 1024 environments, full1M replay,
  16 vector steps and22 finite learner updates each. Console logging/no videos;
  minimum replay4096 and batch256 are short-probe-only overrides.
  Logs: `one_leg_anchor_no_cutoff_{left,right}_probe.log`.
- PASS: actual saved env.pkl comparison to the preserved20k environments;
  both sides differ only by removing the support_drift term. All rewards,
  observations, actions, events and remaining settings compare exactly equal.
  `one_leg_anchor_no_cutoff_config_comparison.json` records probe hashes.
- PASS evaluator execution / SUSPICIOUS untrained quality: first-episode1 s,
  4-environment frozen probe. No drift termination is present; max observed
  drift11.95 cm, outside10cm samples10.8%, drift failure fraction0. No successful
  anchored-low support; all untrained episodes eventually fail other conditions.
  `one_leg_anchor_no_cutoff_eval_probe.json` and NPZ/log.
- PASS: `./scripts/agent-check.sh`, direct log
  `one_leg_anchor_no_cutoff_agent_check.log`.
- PASS: source audit found exactly the four intended source edits and no
  deletion or unrelated source change. Incremental diffs inspected;
  `one_leg_anchor_no_cutoff_source_audit.json` and `_incremental.diff`.
- Local console-only learner/evaluation probes explicitly opt out of W&B and
  scheduled video; full training uses online W&B.

Changed files: `mj_lab/robots/tita/stand_one_leg_anchor_env_cfg.py`,
`test/test_mjlab_one_leg_anchor.py`, `test/evaluate_one_leg_anchor.py`,
`test/run_one_leg_anchor_experiment.py`, and this dated experiment evidence.
Existing training CLI/registry, reference tasks, other sources and checkpoints
are preserved. No commit, publication, or hardware action.

## Actual replacement startup

Persistent session: `tita_one_leg_no_cutoff_20261103`; runner PID567942.

| Side | Run ID | PID | Observed step / updates | W&B |
|---|---|---:|---:|---|
| left | tita_mjlab_124132_110309 | 567949 | 200 /202 | [online](https://forge.coreweave.com/wandb/bjy6614-postech/tita_flat_flash_sac/runs/z4dxrfj4) |
| right | tita_mjlab_124132_110350 | 567950 | 200 /202 | [online](https://forge.coreweave.com/wandb/bjy6614-postech/tita_flat_flash_sac/runs/uiky37na) |

Remote W&B API confirmed both producers running and step100 /2 updates visible
at the remote check; local direct logs subsequently showed200 /202 for each.
`one_leg_anchor_no_cutoff_wandb_startup.json`. Startup/configuration/finite
execution PASS; final policy quality NOT_TESTED. Final evaluation and10000-step
videos are scheduled, not yet claimed successful. Source hashes and the final
incremental diff are recorded; no unrelated source changed.

Probe checkpoint SHA256 left:
`8217619d1b75234a78cbbd90ddfc8f9b3f9e612dd47f106445e6eb3e78bfe2fa`.
Probe checkpoint SHA256 right:
`7f8e034d2206169d61b8b512e6b682cf1a48c13170fdcd0662a6fb0a155bdf2d`.
These are16-step local plumbing probes, not the main policy hashes or learned
quality measurements. Main hashes are pending step5000 and populate the live
`one_leg_anchor_no_cutoff_{left,right}_state.json` files after saving.
