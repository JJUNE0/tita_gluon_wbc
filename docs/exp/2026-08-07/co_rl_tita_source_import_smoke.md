# CO-RL TITA source import and headless smoke

- Execution Domain: `TRAINING_SIM`
- Evidence Status: `PASS`
- Branch: `dev_gluon`
- Robot hardware commands: none
- Source repository: `/home/cocel/Desktop/Research/isaaclab_add_reward_autotuning`
- Source branch / HEAD: `agent/antigravity/tita-migration` / `e01cd60964e7ac3d25937f98eb6bc758a7b69f03`
- Policy checkpoint: `logs/co_rl/Tita_Flat_Stand_Drive-v3-mooppo/mooppo/2026-08-07_12-19-45_imported_headless_smoke_retry/model_0.pt`
- Policy checkpoint SHA256: `e520da824f699f29f7be67465a09a8e56c994561b1a7d7ae0c8937e5347901e5`
- ONNX hash: `N/A` (export was outside this import smoke)

## Imported runtime

- Copied the requested CO-RL runner/algorithm tree to `lab/scripts/co_rl`.
- Copied the TITA MOO task and its direct `mdp`, sensor, terrain, asset,
  environment, MOO-manager, and domain-manager dependency closure under
  `lab/ddt_lab/ddt_lab`.
- Rewrote source `lab.flamingo` namespaces and Gym entry points to `ddt_lab`.
- Registered five TITA MOO Gym tasks through `ddt_lab.tasks`.
- Preserved the source TITA actuator/initial-state configuration while replacing
  its stale absolute URDF path with the byte-identical local workspace URDF.
- Source working-tree provenance is recorded in
  `co_rl_source_import_manifest.sha256`.

## Test evidence

### Runner-integrated environment smoke

```text
command: PYTHONPATH=<repo>/lab:<repo>/lab/ddt_lab \
  /home/cocel/isaac/env_isaaclab/bin/python \
  test/test_co_rl_tita_headless_smoke.py \
  --headless --num-envs 1 --steps 4
result: PASS (exit code 0)
environment: ManagerBasedMOORLEnv
actions: 8
MOO feature_dim / delta_dim: 20 / 20
observation groups: stack_policy=32, none_stack_policy=4,
  priv_extrio=2, priv_prio=3, priv_physical=20
runner injection: discriminator, delta normalizer, and reward EMA set
steps: 4; observations, rewards, extras, and deltas finite
```

### Bounded training smoke

```text
command: PYTHONPATH=<repo>/lab:<repo>/lab/ddt_lab \
  /home/cocel/isaac/env_isaaclab/bin/python lab/scripts/co_rl/train.py \
  --task Isaac-Velocity-Flat-Tita-GTBaseVel-TargetHeight-v3-moo-ppo \
  --algo mooppo --num_envs 1 --max_iterations 1 \
  --run_name imported_headless_smoke_retry --headless
result: PASS (exit code 0)
rollout: 24 timesteps
update: one MOO-PPO learning iteration
mean reward: 0.00
value loss: 0.0452
surrogate loss: -0.1039
discriminator loss: 15777.8406
domain level: 0.0000
checkpoint: model_0.pt, 5,225,697 bytes
```

The generated checkpoint loaded on CPU with keys
`model_state_dict`, `ppo_optimizer_state_dict`,
`disc_optimizer_state_dict`, `infos`, and `iter`; all inspected tensor values
were finite.

## Diagnosed failures and fixes

1. A direct raw-environment step failed with
   `MOORewardManager: Discriminator not set`. This is the source runtime contract,
   not a reward implementation failure: `MOO_OnPolicyRunner` performs the
   required manager injection. The smoke now constructs the wrapper and runner
   before stepping.
2. The first bounded training attempt completed its rollout/update but failed
   while writing a dirty-worktree Git diff because GitPython returned surrogate
   code points for undecodable bytes. The provenance writer now escapes only
   those code points and emits valid UTF-8; the retry completed successfully.

## Warnings and unresolved scope

- Isaac Sim reported existing URDF merge-body deprecations, render-interval
  mismatch, CPU powersave, IOMMU, and shared Kit key-value database warnings.
  None stopped the smoke.
- The smoke is TITA-only and demonstrates runtime integration, not learned
  policy quality or convergence.
- Source-parity comparison and `play.py` behavior are not yet fully validated.
- The dynamic TITA+GLUON environment remains a later phase.
- A separate 4096-environment training job was already running during this
  smoke. It was observed read-only and was not signaled or modified.

## Completion checks

```text
stale namespace/import scan: PASS (no lab.flamingo, deleted MOO-port, or
  source-workspace absolute paths in imported runtime)
./scripts/agent-check.sh: PASS
  Python syntax: 362 passed, 0 failed
  URDF XML parse: 8 passed
  whitespace/conflict-marker integrity: PASS
  experiment directory/log checks: PASS
```
