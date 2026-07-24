# MOO Manager RSL-RL Porting Plan

## 1. Objective

Port the relevant `moo_ppo`, `moo_reward_manager`, and `domain_managers`
functionality from:

```text
/home/cocel/Desktop/Research/isaaclab_add_reward_autotuning
```

into `tita_gluon_wbc`, adapting it to the project's installed RSL-RL 3.1.2
interfaces instead of copying the source repository's custom `co_rl` stack.

The first deliverable is a minimal, traceable vertical slice:

```text
TITA flat task
  + feed-forward ActorCritic
  + single GPU
  + nonmotion MOO features
  + MOORewardManager
  + MOOPPO
  + checkpoint save/load
```

Execution domain for implementation and initial validation:
`TRAINING_SIM` / `VALIDATION_SIM`.

Hardware deployment and robot commands are out of scope.

## 2. Source and Target Architecture

The source implementation has the following data flow:

```text
environment
  -> MOORewardManager computes reward and delta
  -> extras["delta"]
  -> MOO_OnPolicyRunner
  -> MOOPPO.process_env_step()
  -> MOORolloutStorage
  -> MOOPPO.update()
  -> discriminator update
  -> shared discriminator used by MOORewardManager
  -> potential metric drives DomainManager
```

The target implementation must preserve this flow while using the installed
RSL-RL 3.1.2 contracts:

```text
RslRlVecEnvWrapper
  -> extras["delta"]
  -> MOOOnPolicyRunner
  -> MOOPPO
  -> MOORolloutStorage
  -> discriminator update
  -> MOORewardManager
  -> DomainManager
```

The installed `rsl_rl` package must not be edited. All extensions must live
inside `ddt_lab`.

## 3. Proposed File Layout

```text
lab/ddt_lab/ddt_lab/
├── algorithms/
│   └── moo/
│       ├── __init__.py
│       ├── moo_ppo.py
│       ├── moo_rollout_storage.py
│       ├── discriminator.py
│       └── normalization.py
├── managers/
│   ├── moo_reward_manager/
│   │   ├── __init__.py
│   │   ├── moo_reward_manager.py
│   │   └── moo_reward_term_cfg.py
│   └── domain_managers/
│       ├── __init__.py
│       ├── domain_manager.py
│       └── domain_manager_term_cfg.py
└── runners/
    ├── __init__.py
    └── moo_on_policy_runner.py

lab/ddt_lab/scripts/moo_ppo/
├── train.py
└── play.py
```

The `scripts/moo_ppo/` directory should contain entry points only. Reusable
algorithm and manager code belongs in the `ddt_lab` package.

## 4. Initial Support Boundary

The first implementation must support:

- feed-forward `ActorCritic`
- single-GPU training
- `nonmotion` MOO mode
- TITA flat locomotion task
- standard RSL-RL PPO observations represented by `TensorDict`
- MOO checkpoint save/load

The first implementation must explicitly reject or leave disabled:

- recurrent policies
- motion/GRU discriminator mode
- RND
- symmetry augmentation
- multi-GPU training
- RMA teacher/student
- offline dataset storage
- t-SNE, sklearn, and source-specific visualization code

These features may be added only after the initial vertical slice passes its
regression and checkpoint tests.

## 5. Transition Timing Contract

One stored transition is defined as:

```text
obs_t
action_t
env.step(action_t)
reward_t
delta_t
done_t
obs_t+1
```

RSL-RL records `obs_t` in `PPO.act()` before stepping the environment. The MOO
environment must calculate `delta_t` after applying `action_t` and return it
through `extras["delta"]`. `MOOPPO.process_env_step()` must then store:

```text
(obs_t, action_t, reward_t, delta_t, done_t)
```

Required invariants:

- `delta.shape == (num_envs, delta_dim)`
- delta is on the algorithm device before storage
- delta contains no NaN or Inf values
- delta and reward belong to the same environment step
- reset environments do not leak motion history into the next episode

## 6. MOO Rollout Storage

Implement `MOORolloutStorage` as an RSL-RL 3.1.2-compatible extension of
`rsl_rl.storage.RolloutStorage`.

Required changes:

1. Add `delta` to the transition object.
2. Allocate a delta buffer with shape:

   ```text
   (num_steps_per_env, num_envs, delta_dim)
   ```

3. Copy `transition.delta` in `add_transitions()`.
4. Return `delta_batch` from `mini_batch_generator()`.
5. Add recurrent delta batching only when recurrent support is implemented.
6. Preserve the RSL-RL `TensorDict` observation behavior.

The generator return contract and `MOOPPO.update()` must be changed together.
Tests must fail clearly if a plain RSL-RL storage object is accidentally used.

## 7. MOOPPO

Implement `MOOPPO` as an extension of `rsl_rl.algorithms.PPO`, pinned to the
installed RSL-RL 3.1.2 behavior.

Required overrides:

- `__init__()`
- `init_storage()`
- `process_env_step()`
- `update()`

### 7.1 Initialization

`MOOPPO` owns:

- policy and policy optimizer inherited from PPO
- discriminator
- discriminator optimizer
- delta normalizer
- reward EMA
- MOO hyperparameters
- reference or attachment interface to `MOORewardManager`

`init_storage()` must create `MOORolloutStorage` using `delta_dim`.

### 7.2 Environment-Step Processing

`process_env_step()` must preserve all stock RSL-RL behavior:

- observation normalization update
- reward and done recording
- timeout bootstrapping
- policy reset

It must additionally validate and store `extras["delta"]`.

Missing delta must be a configuration error for a MOO task. It must not
silently substitute zeros.

### 7.3 Update

Each mini-batch update must perform:

1. discriminator update using `delta_batch`
2. stock PPO policy/value update
3. metric aggregation

The initial implementation should preserve the installed PPO update as closely
as possible, following the existing `PPOWithEstimator` version-pinned pattern.

The returned loss dictionary should include at least:

- `value_function`
- `surrogate`
- `entropy`
- `moo_discriminator`
- `moo_policy_probability`
- `moo_delta_abs`

Policy and discriminator optimizers must own disjoint parameter sets.

## 8. Discriminator and Normalization Utilities

Port only the source components required by the initial MOO path:

- `DiscriminatorMLP`
- gradient penalty
- logit regularization
- optional weight regularization
- `DiffNormalizer`
- `EMA`

The initial nonmotion discriminator consumes:

```text
normalized_delta + configured policy observation group
```

The observation group must be configured explicitly rather than assuming a
source-specific key such as `stack_policy`.

All utility state required to reproduce reward calculation must implement
`state_dict()` and `load_state_dict()`.

## 9. MOORewardManager

Implement a project-local manager compatible with the installed Isaac Lab
`RewardManager` API.

Responsibilities:

- resolve `MOORewardTermCfg` entries
- calculate each error feature
- validate feature dimensions
- concatenate features into raw delta
- maintain optional motion history
- calculate potential reward
- calculate discriminator reward
- calculate feature-matching reward
- optionally normalize the total MOO reward
- expose debug metrics

Reward composition:

```text
reward =
    w_potential * reward_potential
  + w_discriminator * reward_discriminator
  + w_feature_matching * reward_feature_matching
```

The implementation must address the following source-code issues:

- do not silently treat term-evaluation failures as dimension one
- make normalized/raw delta semantics explicit
- restore discriminator train/eval state after reward inference
- reject missing discriminator attachment before the first environment step
- validate feature shape stability across steps
- prevent motion history leakage across resets

Configuration should be separated into:

```text
MOORewardManagerCfg:
  mode
  window_size
  observation group
  feature terms

MOOAlgorithmCfg:
  discriminator architecture
  discriminator learning rate
  regularization
  reward normalization
  reward weights
```

## 10. Runner Integration

A stock `OnPolicyRunner` algorithm-name monkeypatch is not sufficient because
the algorithm requires manager metadata and the manager requires the
algorithm-owned discriminator.

Implement `MOOOnPolicyRunner` with this initialization order:

```text
create environment
  -> create MOORewardManager without learning components
  -> wrap with RslRlVecEnvWrapper
  -> create MOOOnPolicyRunner
  -> read env.unwrapped.moo_reward_manager metadata
  -> create MOOPPO and MOORolloutStorage
  -> attach discriminator, normalizer, and EMA to manager
  -> allow the first env.step()
```

The runner should reuse stock RSL-RL logging and learning behavior wherever
possible. Custom code should be limited to:

- MOO algorithm construction
- manager attachment
- MOO metric logging
- extended checkpoint save/load

## 11. Environment Integration

Do not copy the source `ManagerBasedMOORLEnv.step()` wholesale without first
diffing it against the installed Isaac Lab `ManagerBasedRLEnv`.

Prefer the smallest project-local extension that provides:

- `cfg.moo_rewards`
- `MOORewardManager` creation
- configured policy observation input to the manager
- `extras["delta"]`
- optional `DomainManager`
- MOO episode metrics

The environment must preserve:

- termination and timeout ordering
- recorder hooks
- reset ordering
- command updates
- interval events
- observation history updates
- `RslRlVecEnvWrapper` timeout behavior

Register MOO tasks under separate Gym IDs so existing PPO, estimator, and NP3O
tasks remain unchanged.

Suggested initial task:

```text
DDT-Velocity-Flat-Tita-MOO-RSL-v0
```

## 12. DomainManager

Port the source curriculum-aware domain manager only after the MOO vertical
slice is stable.

Proposed data flow:

```text
MOORewardManager potential score
  -> completed-episode samples
  -> DomainManager gate buffer
  -> confidence calculation
  -> difficulty-level update
  -> randomization-range interpolation
```

The curriculum input must be defined as an episode-level value. Step-wise
global means must not be mixed with episode completion samples.

Required state:

- difficulty level
- gate samples
- last gate mean
- last confidence
- current randomization ranges

Required decisions:

- whether `scipy.stats` remains a dependency
- how Student-t confidence is calculated without SciPy, if removed
- which event parameters support interpolation
- how `add` and `scale` operations choose their neutral baseline
- how tuple, per-axis, and nested ranges are validated

Curriculum state must be included in checkpoint save/load.

## 13. Checkpoint Contract

MOO checkpoints should include:

```python
{
    "model_state_dict": ...,
    "optimizer_state_dict": ...,
    "moo_discriminator_state_dict": ...,
    "moo_discriminator_optimizer_state_dict": ...,
    "moo_delta_normalizer_state_dict": ...,
    "moo_reward_ema_state_dict": ...,
    "moo_domain_state": ...,
    "moo_schema_version": 1,
    "iter": ...,
    "infos": ...,
}
```

Load modes:

1. **MOO resume**
   - restore every MOO and PPO state
2. **Plain PPO warm start**
   - load policy state only
   - initialize discriminator, normalizer, EMA, and domain state from config
   - require an explicit option; never infer this mode silently
3. **Play/export**
   - policy-only inference may omit the discriminator
   - MOO reward diagnostics require the discriminator and normalization state

Checkpoint compatibility errors must report the missing field and expected
schema version.

## 14. Configuration and Entry Points

Add project-local config classes for:

- MOO PPO algorithm
- discriminator
- MOO reward manager
- MOO reward terms
- domain curriculum
- TITA flat MOO runner

Add dedicated:

- `scripts/moo_ppo/train.py`
- `scripts/moo_ppo/play.py`

The scripts should follow the existing RSL-RL entry-point pattern while
constructing `MOOOnPolicyRunner`.

Existing plain PPO, estimator, and NP3O entry points must not be modified unless
a shared, backward-compatible registration change is unavoidable.

## 15. Implementation Phases

### Phase 0 — Freeze Interfaces

- record installed RSL-RL version and relevant source hashes
- document source-to-target symbol mapping
- fix the supported observation group
- fix delta and reward timing
- define checkpoint schema

### Phase 1 — Independent Components

- discriminator
- normalizer
- EMA
- MOO term config
- CPU unit tests

### Phase 2 — Reward Manager

- nonmotion feature calculation
- reward components
- attachment validation
- reset behavior
- debug metrics
- fake-discriminator tests

### Phase 3 — Storage and PPO

- delta transition/storage
- feed-forward mini-batch generator
- discriminator update
- stock PPO loss preservation
- tensor-shape and gradient-ownership tests

### Phase 4 — Runner and Checkpoints

- manager attachment
- MOO logging
- full save/load
- plain PPO warm-start behavior

### Phase 5 — TITA Flat Integration

- separate MOO Gym task
- environment and runner configs
- one-environment initialization
- one-iteration smoke test
- short multi-environment training

### Phase 6 — Domain Curriculum

- completed-episode gate
- confidence calculation
- range interpolation
- checkpoint resume
- fixed-seed behavior test

### Phase 7 — Deferred Extensions

- rough terrain
- motion/GRU discriminator
- recurrent policy
- symmetry
- multi-GPU
- RMA teacher/student

## 16. Test Plan

All new test and debug files must live under `/test/`.

### Unit Tests

- MOO term shape validation
- raw and normalized delta behavior
- motion buffer reset behavior
- discriminator forward and gradient penalty
- normalizer and EMA state round-trip
- rollout transition insertion
- mini-batch delta alignment
- policy/discriminator optimizer parameter separation
- DomainManager interpolation and gate decisions

### Integration Tests

1. import and configuration resolution
2. one-env headless initialization
3. deterministic single-step delta/reward alignment
4. one training iteration
5. checkpoint save/load round-trip
6. resume for additional iterations
7. plain PPO warm start with explicit option
8. short fixed-seed curriculum run

### Regression Tests

- existing plain PPO task still initializes
- estimator PPO still resolves its custom classes
- NP3O task remains unchanged
- no MOO code runs for non-MOO tasks

Every completed experiment or validation run must be recorded under:

```text
docs/exp/YYYY-MM-DD/<task_or_run_name>.md
```

Each entry must include:

- execution domain
- policy checkpoint SHA256 or ONNX hash
- evidence status
- observed metrics and log summary

## 17. Completion Criteria

The initial port is complete only when all of the following have direct
evidence:

- MOO-disabled behavior preserves the expected PPO baseline
- delta is stored with the correct transition
- discriminator parameters change during training
- the reward manager uses the updated discriminator
- policy and discriminator optimizers update only their owned parameters
- reset behavior does not leak feature history
- checkpoint round-trip reproduces policy output and MOO reward diagnostics
- DomainManager advances only when its configured gate passes
- existing PPO, estimator, and NP3O paths show no regression
- `./scripts/agent-check.sh` passes
- validation evidence is recorded in `docs/exp/`

## 18. Known Risks

- The source code is coupled to a custom `co_rl` stack and cannot be copied
  directly into RSL-RL 3.1.2.
- RSL-RL storage and observations use `TensorDict`, unlike the source flat
  tensor implementation.
- Reward calculation depends on an algorithm-owned discriminator, creating an
  initialization-order contract.
- Copying an entire Isaac Lab environment `step()` is vulnerable to upstream
  version drift.
- Symmetry augmentation is undefined for delta features unless a corresponding
  delta transformation is designed.
- Multi-GPU support requires explicit discriminator parameter and optimizer
  synchronization.
- DomainManager currently introduces SciPy and depends on EventManager internal
  behavior.
- The repository already contains unrelated working-tree changes, which must
  remain untouched throughout implementation.

## 19. Recommended First Implementation Slice

Implement and validate only:

```text
TITA flat
  -> nonmotion MOORewardManager
  -> extras["delta"]
  -> feed-forward MOORolloutStorage
  -> MOOPPO
  -> MOOOnPolicyRunner
  -> full MOO checkpoint round-trip
```

Add `DomainManager` only after this path has direct `PASS` evidence. This keeps
reward learning failures separate from curriculum failures and makes the first
change reviewable.
