# Remove the legacy lab alias and consolidate Isaac logs

Execution Domains: DESKTOP_DRY_RUN, TRAINING_SIM, VALIDATION_SIM

Evidence Status: PASS for path migration, preserved data, native Isaac checks
and representative checkpoint playback without the alias.

Policy Checkpoint SHA256:

- Isaac walk 100k: `3ec4745778cd8cbcdc4338915ca86ae1f6bc7067f3f583918b42a9c7f9c86aa1`
- Legacy headw0 65k: `ff083cbfc8a8571009a27454e75dc88463e9ebc796fa79e8782ccb4a5bea239d`

Branch: `agent/codex/tita-walk`. No commit, push, PR or hardware operation.

## Files and behavior

- Removed the local `lab -> isaac_lab` symlink after its users were checked.
  No target directory or checkpoint was deleted.
- Isaac model logs were already physically inside `isaac_lab/ddt_lab/logs/`
  (about 8.2 GB) and `isaac_lab/logs/` (about 1.8 GB). All 1,970 weight/data
  files retain their original sizes, devices and inodes.
- Moved the old repository-root `wandb/` directory to
  `isaac_lab/wandb/from_repo_root/`. Existing `isaac_lab/wandb/` runs were not
  overwritten. All 114 archived files have identical SHA256 values and the
  `latest-run`/debug-log symlinks remain valid.
- Removed the empty repository-root `logs/` directory.
- Canonicalized 54 generated desktop export `config.json` files and their
  source dictionary keys from the old absolute prefix to `isaac_lab`.
  Numeric policy/PD/action/observation settings and weight files were preserved.
  Their 54 manifests have matching config hashes and invalidated cache
  fingerprints, so the normal launcher revalidates before using an old export.
  Relocated caches are labelled NOT_TESTED until the exporter validates them.
- Updated `.vscode/launch.json`, `.vscode/settings.json` and active
  `.omc/project-memory.json` path references.
- Updated root `README.md` and `.gitignore` to remove the compatibility-link
  instructions/rule, and updated the old migration audit's alias expectation
  in `test/check_mjlab_migration.py`.
- Added the one-off migration/verification helper `test/cleanup_lab_alias.py`.
  Its source and incremental task diffs were inspected after execution.

Migration records: `lab_alias_cleanup.json` and
`lab_alias_cleanup_before.tar.gz`. The archive backs up generated cache/editor
metadata; no policy weights were rewritten. Existing unrelated workspace edits
and staged directory renames were preserved.

## Historical provenance and frozen policy bundles

Historical experiment reports, run metadata, old W&B program records and
hash-pinned robot policy bundles retain their original source-path strings.
Those are historical provenance rather than active alias dependencies.

The existing robot parameter builder was evaluated as a pure function without
importing ROS launch or creating any robot node: all 13 policy bundles use
their bundle-local `policy.onnx`. All 37 frozen bundle files remain byte-identical;
neither their hashes nor hardware deployment settings were changed.

The two old VSCode MOO launch profiles already pointed to removed historical
MOO scripts before this task. Only their directory prefixes were updated;
this path cleanup does not restore obsolete training entry points.

## Executed checks

Observed Metrics / Behavior / Log Summary:

- PASS: `lab`, root `logs` and root `wandb` are absent; canonical Isaac log
  directories and moved W&B archive exist.
- PASS: checkpoint/data file inventory unchanged after symlink removal;
  archived W&B file hashes and frozen policy bundle hashes unchanged.
- PASS: no old alias dependencies in `.pth`, `.egg-link` or editable import
  finders for the active Isaac, mjlab and MuJoCo Python environments.
- PASS: active VSCode/project-memory paths no longer use `/lab/`.
- PASS: native Isaac walk environment: 73/73 checks after removing the alias.
  `lab_alias_cleanup_isaac_checks.json` / `.log`.
- PASS: legacy 65k checkpoint automatically refreshed its relocated export,
  passed ONNX parity and completed 200 headless MuJoCo steps.
  `lab_alias_cleanup_legacy_playback.log`.
- PASS: current Isaac walk 100k checkpoint completed 200 headless MuJoCo steps.
  `lab_alias_cleanup_walk_playback.log`.
- PASS: ongoing mjlab hybrid training remained alive and advanced beyond
  21,100 vector steps / 42,002 learner updates after alias removal.
- PASS: `./scripts/agent-check.sh`; `lab_alias_cleanup_agent_check.log`.

Only representative relocated exports were executed; remaining historical
desktop caches will be revalidated when selected by the normal launcher.
The checks establish path usability and finite execution, not policy quality.
No physical robot command, deployment or shutdown was performed.
