# RMATeacher architecture (checkpoint `2026-08-08_16-12-19/model_9999.pt`)

This is the newest checkpoint deployed, and the **first one in this line of work
whose network architecture differs structurally** from every prior checkpoint
(which were all plain `ActorCritic`). Any future checkpoint might revert to plain
`ActorCritic` or use yet another architecture — always check
`params/agent.yaml` (`policy.class_name`) and the checkpoint's `state_dict` keys
before assuming either shape.

## What RMATeacher is

RMA = Rapid Motor Adaptation. Instead of a single actor MLP over the proprioceptive
observation, there are two networks:

- **Encoder**: `privileged_obs` (25-dim, only available in sim) → latent `z` (16-dim).
  Implementation: `spectral_norm`-wrapped `nn.Linear` layers, `hidden_dims=[256,128]`,
  ELU activation. Source: `scripts/co_rl/core/modules/teacher_student.py` in
  `isaaclab_add_reward_autotuning` (classes `Encoder`, `RMATeacher`, `RMAStudent`).
- **Actor**: same 68-dim proprio+cmd observation as prior checkpoints
  (`MooStandDriveObservationBuilder`'s own contract: 28 base + base_lin_vel_x/y/z +
  base_height, `num_policy_stacks=1`), **concatenated with the 16-dim `z`** → 84-dim
  input → 8 actions.

So at inference time: `z = Encoder(privileged_obs)`; `actions = Actor(concat(obs_68, z))`.

This deployment therefore runs **two ONNX graphs per control step** instead of one.

## Registered gym task ID (for `play.py` export)

`Isaac-Velocity-Flat-Tita-RMATeacher-TargetHeight-v3-moo-ppo`

**Do not** use `Isaac-Velocity-Flat-Tita-GTBaseVel-v3-moo-ppo` (the task ID used for
prior checkpoints) — that builds a plain 68-dim `ActorCritic` and fails to load this
checkpoint's `state_dict` with a shape mismatch
(`size mismatch for actor.0.weight: ... torch.Size([512, 84]) ... torch.Size([512, 68])`).
Always grep `tita_env/__init__.py` in the training repo for the correct registered ID
for a given checkpoint rather than assuming.

## `privileged_obs` composition (25-dim, in order)

Derived by tracing `_get_privileged_obs()` in `play.py`
(`sorted([k for k in obs_dict if k.startswith("priv_")])` → alphabetical group order:
`priv_extrio` → `priv_physical` → `priv_prio`) and the corresponding `env.yaml` term
declarations for this run.

| Segment | Dims | Source | Scale |
|---|---|---|---|
| `is_contact` (left, right leg_4/wheel) | 2 | `body_in_contact()`, force threshold 1.0N | unscaled (0/1) |
| `body_mass` | 1 | base_link mass | ×0.1 |
| `body_com` | 3 | base_link local inertial CoM offset | ×10 |
| `actuator_kp` | 8 | joint kp, **isaac joint order** | ×0.01 |
| `actuator_kd` | 8 | joint kd, **isaac joint order** | ×1.0 |
| `base_lin_vel_x/y/z` | 3 | body-frame linear velocity | ×[2.0, 1.0, 0.25] |

Total: 2+1+3+8+8+3 = 25. Implemented in `obs_builder.py::build_rma_privileged_obs()`
(see `03_code_changes.md`).

### Why "live/nominal" MuJoCo values are correct here

Isaac's training-time `priv_physical.*` observation functions return
**post-domain-randomization** absolute values (`root_physx_view.get_masses()`,
`get_coms()`, actuator gains after per-episode randomization). This MuJoCo sim2sim
harness runs a single fixed MJCF with **no per-episode domain randomization**, so the
"nominal"/live value read directly from the MuJoCo model *is* the correct analog of
what Isaac's privileged observation would return for an unrandomized episode — no
attempt is made to replicate Isaac's DR distribution here.

## Exported ONNX artifacts

- Encoder: `tita_gluon_ws/deploy/tita/policy_moo_stand_drive_20260808_9999_rma_encoder.onnx`
  — input `privileged_obs` `[1,25]`, output `z` `[1,16]`. Exported via a standalone
  pure-torch script (no Isaac Sim launch needed) that loads the `encoder.*` keys from
  `model_9999.pt`'s state_dict into a freshly-instantiated
  `Encoder(input_dim=25, output_dim=16, hidden_dims=[256,128], activation="elu")` —
  confirmed `missing: []`, `unexpected: []` on load.
- Actor: `tita_gluon_ws/deploy/tita/policy_moo_stand_drive_20260808_9999_rma_actor.onnx`
  — input `obs` `[1,84]`, output `actions` `[1,8]`.
  SHA256: `caa4645a6b3ff5e608b5705c520f5947eb954b4d8ec38acdc51cec50350e1f27`
  Exported via:
  ```bash
  python scripts/co_rl/play.py \
    --task Isaac-Velocity-Flat-Tita-RMATeacher-TargetHeight-v3-moo-ppo \
    --algo mooppo --num_policy_stacks 1 --checkpoint model_9999.pt \
    --num_envs 1 --headless
  ```
  (run from `isaaclab_add_reward_autotuning` repo root). `play.py` runs an infinite
  render loop after export — **kill the process after the ONNX files appear**:
  `ps aux | grep "[c]o_rl/play.py" | awk '{print $2}' | xargs -r kill -9`
- Source checkpoint:
  `/home/cocel/Desktop/Research/isaaclab_add_reward_autotuning/logs/co_rl/Tita_Flat_Stand_Drive-v3-mooppo/mooppo/2026-08-08_16-12-19/model_9999.pt`
  SHA256: `df81ed501e6b3ebecb67a5819a79be43cd17122ba78bd021db8c392fcb882891`

## Height-command range for this checkpoint

`widen_height_range` curriculum term: `start_range=(0.32,0.38)`,
`end_range=(0.25,0.45)`, `start_step=24000`, `end_step=120000` (env steps).
`model_9999` is the **final training iteration**, far past `end_step`, so the
curriculum is fully widened to `(0.25, 0.45)` by this checkpoint. Confirmed against
the live `feature_functions_common.py` constants:
```
_NATURAL_STANDING_HEIGHT = 0.35
_HEIGHT_NORM_CENTER = 0.35        # (0.25 + 0.45) / 2
_HEIGHT_NORM_HALF_RANGE = 0.10    # (0.45 - 0.25) / 2
```
→ config uses `height_norm_center: 0.35`, `height_norm_half_range: 0.10`,
`command.default_height_m: 0.35` (do NOT copy forward the prior checkpoint's
`0.325`/`0.095`, which was for a still-narrow-range early-training checkpoint).
