# CO-RL MOO port reset

- Execution Domain: `TRAINING_SIM`
- Policy Checkpoint SHA256 / ONNX Hash: `N/A` (source cleanup and import planning)
- Evidence Status: `PASS`
- Robot hardware commands: none
- Branch: `dev_gluon`

## Purpose

Remove the failed MOO-on-rsl_rl implementation before importing the requested
CO-RL source stack from `isaaclab_add_reward_autotuning`.

## Changes

- Removed the MOO-specific rsl_rl algorithm, rollout storage, discriminator,
  runner, environment, reward manager, domain manager, task registrations,
  `moo_ppo` scripts, and their MOO-specific tests/debug scripts.
- Removed MOO-only exports and helper/reward terms added to the standard manager
  and locomotion MDP modules.
- Preserved generic rsl_rl tools, NP3O, estimator code, checkpoints, ONNX files,
  deployment configs, experiment records, and unrelated robot work.
- Recorded the source import layout and dependency closure in
  `docs/plan/co_rl_moo_import.md`.

## Observations

- The requested source `tita_env` is not standalone. It imports sibling `mdp`,
  `sensors`, and `terrain_config` packages and a TITA asset configuration.
- The source repository is on branch `agent/antigravity/tita-migration` at
  `e01cd60964e7ac3d25937f98eb6bc758a7b69f03`, with working-tree modifications
  and untracked TITA files. File hashes are therefore required for provenance.
- The source TITA asset points to an obsolete absolute `DDT_Lab` URDF path and
  cannot run unchanged in this workspace.

## Verification

Executed checks:

```text
old failed-port runtime import scan: none
old failed-port source-file scan: none
modified Python py_compile: PASS
./scripts/agent-check.sh:
  Python syntax: 256 passed, 0 failed
  URDF XML parse: 8 passed
  final result: PASS
```

This `PASS` applies only to removing the failed port and recording the import
plan. CO-RL has not yet been copied, imported, or executed in this workspace.
