# Code changes: RMATeacher support in the sim2sim harness

All changes are additive/backward-compatible — the pre-existing single-ONNX
`PolicyRunner` path (used by every non-RMA checkpoint) is untouched in behavior.
All four files are `.py` under a `colcon build --symlink-install` package, so edits
to existing files take effect immediately without rebuilding; only the brand-new
`.yaml` config needed a rebuild (see `05_validation_and_launch.md`).

## `sim2sim/cosim_ros2_jazzy/cosim_ros2_jazzy/mujoco_env.py`

Added three methods to `TitaMujocoEnv` (right after the existing `body_quat()`,
which has its own separate/duplicated body-id-caching pattern — not refactored to
share `_body_id()`, a minor cleanliness item left for later):

```python
def _body_id(self, name: str) -> int: ...          # cached MuJoCo body-name -> id lookup
def body_mass(self, name: str) -> float: ...         # model.body_mass[id]
def body_com(self, name: str) -> np.ndarray: ...      # model.body_ipos[id] (local inertial CoM offset)
def body_in_contact(self, name: str, threshold: float = 1.0) -> bool: ...
    # True if any active contact involving this body has |force| > threshold (N)
    # at the current tick, via mj_contactForce over data.contact / geom_bodyid.
```

## `sim2sim/cosim_ros2_jazzy/cosim_ros2_jazzy/obs_builder.py`

Appended (does not touch the existing `MooStandDriveObservationBuilder`):

```python
_RMA_ACTUATOR_ISAAC_REINDEX = np.array([0, 4, 1, 5, 2, 6, 3, 7])  # native -> isaac joint order

def build_rma_privileged_obs(
    contact_left: bool, contact_right: bool,
    body_mass_kg: float, body_com_m: np.ndarray,
    joint_kp_native: np.ndarray, joint_kd_native: np.ndarray,
    base_lin_vel_b: np.ndarray,
) -> np.ndarray:
    # Assembles the 25-dim privileged_obs vector, see 02_rma_teacher_architecture.md
    # for the exact term order/scales. Raises ValueError if the assembled shape
    # isn't exactly (25,).
```

## `sim2sim/cosim_ros2_jazzy/cosim_ros2_jazzy/policy_runner.py`

- Existing `PolicyRunner.act()` signature extended to accept-and-ignore a
  `privileged_obs` kwarg, purely so both runner classes share a uniform call
  signature at the call site in `mujoco_policy_node.py`.
- New `RmaPolicySpec` dataclass and `RmaTeacherPolicyRunner` class added. Holds two
  `onnxruntime.InferenceSession`s (encoder, actor). `_validate_interface()` checks
  encoder input `[1,25]`/output `[1,16]` and actor input
  `[1, obs_dim + latent_dim]` (= `[1,84]`)/output `[1, action_dim]` (= `[1,8]`) at
  construction time, so a shape mismatch fails loudly at startup rather than at the
  first inference call.
  - **Important config-key nuance**: `RmaPolicySpec.obs_dim` (from `policy.obs_dim`
    in the YAML) is **68** — `MooStandDriveObservationBuilder`'s own output dim, the
    same key/value already used by the non-RMA `PolicyRunner`. The actor's true
    84-dim raw input is derived internally as `obs_dim + latent_dim`, never stored
    directly in config.
- `RmaTeacherPolicyRunner.act(obs_68, history=None, privileged_obs=None)`: runs the
  encoder on `privileged_obs` → `z`, concatenates `[obs_68, z]`, runs the actor,
  returns the 8-dim action. Raises `ValueError` if `privileged_obs is None`.

## `sim2sim/cosim_ros2_jazzy/cosim_ros2_jazzy/mujoco_policy_node.py`

1. Import updated to include `build_rma_privileged_obs` from `obs_builder` and
   `RmaTeacherPolicyRunner` from `policy_runner`.
2. In `__init__`, right after the obs_builder/action_adapter selection:
   ```python
   self.uses_rma_teacher = "rma_encoder_path" in self.cfg.get("policy", {})
   if self.uses_rma_teacher:
       self.policy = RmaTeacherPolicyRunner.from_config(self.cfg)
   else:
       self.policy = PolicyRunner.from_config(self.cfg)
   ```
   → **architecture selection is driven purely by the presence of
   `policy.rma_encoder_path` in the YAML config** — no separate boolean flag needed.
3. In the `rl_0`/`shadow_rl0` step loop:
   ```python
   cycle_obs = self._build_obs()
   self.last_obs = cycle_obs
   privileged_obs = self._build_rma_privileged_obs() if self.uses_rma_teacher else None
   action = self.policy.act(cycle_obs, self.obs_builder.history, privileged_obs=privileged_obs)
   ```
4. New method `_build_rma_privileged_obs(self)` (placed right after `_build_obs()`):
   reads `robot.wheel_body_names` (default `["left_leg_4", "right_leg_4"]`) and
   `robot.base_body_name` from config, computes body-frame `base_lin_vel` via
   `rot.T @ env.base_lin_vel()` (rot from `quat_wxyz_to_rotmat(env.base_quat_sensor())`),
   and calls `build_rma_privileged_obs(...)` with live MuJoCo state.

All four files were syntax-validated via `python3 -c "import ast; ast.parse(...)"`
before the config file was written. No `colcon build` was needed for these `.py`
changes (symlink-install).

## New config file

`sim2sim/cosim_ros2_jazzy/config/tita_moo_stand_drive_20260808_9999_rma_teacher.yaml`
— new `policy:` keys added on top of the standard `moo_stand_drive` interface keys:

```yaml
policy:
  path: ".../policy_moo_stand_drive_20260808_9999_rma_actor.onnx"      # actor
  rma_encoder_path: ".../policy_moo_stand_drive_20260808_9999_rma_encoder.onnx"
  rma_privileged_obs_dim: 25   # optional, defaults to 25 in RmaPolicySpec.from_config
  rma_latent_dim: 16           # optional, defaults to 16
  obs_dim: 68                  # unchanged — MooStandDriveObservationBuilder's own dim
  height_norm_center: 0.35
  height_norm_half_range: 0.10
  # ... (input_obs_name/output_name/action_dim/etc. same as every other moo_stand_drive config)
```

`command.default_height_m: 0.35` was also updated to match (see
`02_rma_teacher_architecture.md` for why 0.35 and not 0.325).
`reference_transform_up.stand_jpos` was left unchanged at the user's previously
explicitly-requested pose (see `04_reference_transform_up_issue.md`).
