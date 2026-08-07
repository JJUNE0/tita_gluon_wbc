# CO-RL MOO source import plan

## 1. Scope and execution domain

- Execution Domain: `TRAINING_SIM`
- Target branch: `dev_gluon`
- Hardware commands: none
- Source repository: `/home/cocel/Desktop/Research/isaaclab_add_reward_autotuning`
- Source branch: `agent/antigravity/tita-migration`
- Source HEAD: `e01cd60964e7ac3d25937f98eb6bc758a7b69f03`

The source repository has tracked and untracked working-tree changes. The import
must therefore copy the current working-tree files, not assume that `HEAD`
contains the requested TITA implementation. A manifest will record every copied
source path and SHA256 before namespace adaptation.

The first acceptance target is source-faithful TITA-only MOO training through
`co_rl`. TITA+GLUON dynamics and moving-arm observations are a separate follow-up
change after the imported baseline passes. This separation prevents upstream
porting failures from being confused with combined-robot modeling failures.

## 2. Removed failed port

The previous implementation reimplemented MOO on top of the installed
`rsl_rl`. It is not reused. The reset removes only its MOO-specific algorithm,
runner, environment, managers, task registrations, launch scripts, and tests.

The following are intentionally retained:

- generic `scripts/rsl_rl` training tools
- NP3O and estimator implementations
- checkpoints, ONNX files, W&B data, and experiment records
- Sim2Sim deployment configurations for historical policies
- unrelated TITA and GLUON code

## 3. Source-to-destination mapping

| Source | Destination | Policy |
|---|---|---|
| `scripts/co_rl/` | `lab/scripts/co_rl/` | Copy the complete 62-file working-tree snapshot. |
| `lab/flamingo/tasks/moo_based/locomotion/velocity/tita_env/` | `lab/ddt_lab/ddt_lab/tasks/moo_based/locomotion/velocity/tita_env/` | Copy all 8 files. |
| `lab/flamingo/isaaclab/isaaclab/envs/moo_envs/` | `lab/ddt_lab/ddt_lab/envs/moo_envs/` | Copy both environment files. |
| `lab/flamingo/isaaclab/isaaclab/managers/domain_managers/` | `lab/ddt_lab/ddt_lab/managers/domain_managers/` | Copy all 3 files. |
| `lab/flamingo/isaaclab/isaaclab/managers/moo_managers/` | `lab/ddt_lab/ddt_lab/managers/moo_managers/` | Copy all 3 files. |

### Required dependency closure

The requested `tita_env` directory is not self-contained. It directly imports
the following source packages, so they must be copied as part of the same
reviewable import:

| Additional source | Destination |
|---|---|
| `lab/flamingo/tasks/moo_based/locomotion/velocity/mdp/` | `lab/ddt_lab/ddt_lab/tasks/moo_based/locomotion/velocity/mdp/` |
| `lab/flamingo/tasks/moo_based/locomotion/velocity/sensors/` | `lab/ddt_lab/ddt_lab/tasks/moo_based/locomotion/velocity/sensors/` |
| `lab/flamingo/tasks/moo_based/locomotion/velocity/terrain_config/` | `lab/ddt_lab/ddt_lab/tasks/moo_based/locomotion/velocity/terrain_config/` |
| `lab/flamingo/assets/tita/tita.py` | `lab/ddt_lab/ddt_lab/assets/tita_co_rl.py` |

Package `__init__.py` files for `tasks/moo_based`, `locomotion`, and `velocity`
will be created from the corresponding source package semantics so that the
existing `ddt_lab.tasks` recursive importer registers the Gym tasks.

The source TITA asset has an obsolete absolute URDF path under `DDT_Lab`.
`tita_co_rl.py` will preserve the source actuator and initial-state values while
resolving the same model from this workspace. It must not silently substitute
the current `DDT_TITA_CFG`, whose actuator limits, gains, initial pose, and soft
limits differ from the source task.

## 4. Minimal adaptations after byte-for-byte copy

Algorithm and reward behavior must remain unchanged during the baseline port.
Only these integration edits are allowed initially:

1. Rewrite `lab.flamingo...` imports and Gym entry points to `ddt_lab...`.
2. Keep `scripts.co_rl...` imports valid from `lab/scripts/co_rl`; remove the
   source's duplicate ambiguous `from core...` import in favor of one canonical
   package path.
3. Rewrite MOO environment imports in both vector wrappers to
   `ddt_lab.envs.moo_envs`.
4. Export `MOORewardManager`, `MOORewardTermCfg`, `DomainManager`, and
   `DomainManagerTermCfg` through the local package `__init__.py` files.
5. Register only the copied TITA MOO tasks through `ddt_lab.tasks`.
6. In `play.py`, make the unrelated Flamingo constraint-environment dependency
   optional or remove that branch if it is unused by MOO playback. Do not copy
   unrelated constraint-RL code merely to satisfy an eager import.
7. Add explicit Python dependencies used by the copied code only after an
   import audit. The current Isaac environment already resolves Torch,
   Gymnasium, Zarr, W&B, and scikit-learn.

No reward formula, observation ordering, curriculum equation, optimizer,
network, runner update, or checkpoint schema should be edited in this import
phase.

## 5. Provenance hashes before import

Aggregate SHA256 values over sorted `path + file SHA256` lists from the current
source working tree:

| Source root | Aggregate SHA256 |
|---|---|
| `scripts/co_rl` | `caf3cafd1713a2468f15adf326ebf0a1d8e907816a1c2fe4320c53070f7dc966` |
| `.../tita_env` | `2bf4b8b977779221a0102ab652e425d59f22ce6caa0ecf9456712b64157fe712` |
| `.../envs/moo_envs` | `b0f869fbec84bcc35f134e117a58ac21e11deb6cd76fdb285d0df9fe5440ccd8` |
| `.../managers/domain_managers` | `f69a8f8a59ed5a77ea12dfd9e77fd5a837828d501c4f8dd288baef25e4decb22` |
| `.../managers/moo_managers` | `e4442e76fa8d359f0848af669ae49d7a1116e46a7e6680348ea0a293e310e9f0` |

## 6. Verification gates

### Gate A: static source audit

- no import of `lab.flamingo` remains in imported runtime code
- no import of the deleted `ddt_lab.algorithms.moo`, old runner, or
  `tasks.moo_manager_based` remains
- all copied Python files compile with the project Isaac Python
- task registration resolves the five source TITA task IDs

### Gate B: environment construction

Create a test under `/test` that launches one or two headless environments and
checks:

- `ManagerBasedMOORLEnv` is the unwrapped environment
- MOO reward manager and domain manager are constructed once
- observation group names and dimensions match the runner configuration
- action dimension is 8
- reset and a bounded zero-action step produce finite tensors

### Gate C: bounded CO-RL smoke training

Run a small headless job with one or two environments and one or two learning
iterations. Verify:

- `MOO_OnPolicyRunner` is selected for `--algo mooppo`
- rollout collection and one update finish without NaN/Inf
- reward feature/delta dimensions remain stable
- a checkpoint is written and can be loaded by `play.py`

This gate is a smoke test, not evidence that the policy has learned.

### Gate D: source-parity baseline

Before adding GLUON, compare the imported TITA-only environment contract with
the source: robot model hash, actuator configuration, command ranges,
observation ordering/scales, action mapping, reward feature ordering, domain
curriculum, simulation dt, and decimation.

### Gate E: TITA+GLUON extension

Only after A-D pass:

1. introduce a dynamic combined TITA+GLUON asset;
2. add collision-checked, smooth arm trajectories;
3. add measured and desired GLUON motion to the locomotion observation;
4. retain the imported TITA-only task as a regression baseline;
5. validate fixed arm, slow moving arm, and full-envelope curricula separately.

## 7. Completion protocol

Every implementation phase must run `./scripts/agent-check.sh`, inspect the
task-only diff, and record the executed test evidence under
`docs/exp/YYYY-MM-DD/`. No long training, hardware execution, commit, push, or
deployment is implied by this plan.

## 8. Implementation status — 2026-08-07

- Gates A and B: `PASS`.
- Gate C bounded training smoke: `PASS` for one environment, one learning
  iteration, 24 collected timesteps, checkpoint creation, and checkpoint tensor
  loading/finiteness.
- Gate D source-parity baseline: `NOT_TESTED`; this is the next validation gate.
- Gate E TITA+GLUON extension: `NOT_TESTED`; it remains intentionally separate
  from the imported TITA-only baseline.

The environment must not be stepped before `MOO_OnPolicyRunner` constructs
`MOOPPO`, because that constructor injects the discriminator, delta normalizer,
and reward EMA into `MOORewardManager`. The checked-in headless smoke follows
this actual runtime contract.
