# Checkpoint deployment history (moo_stand_drive line)

All checkpoints below are from `isaaclab_add_reward_autotuning`, experiment
`Tita_Flat_Stand_Drive-v3-mooppo` (co_rl track, MOOPPO algorithm), unless noted.
Configs live in `sim2sim/cosim_ros2_jazzy/config/`, ONNX exports in
`tita_gluon_ws/deploy/tita/`. Every config file has a detailed provenance comment
block at the top of `policy:` — read the actual file for full detail; this is a
condensed index.

Chronological (oldest → newest):

| Run / checkpoint | Config file | Notes |
|---|---|---|
| `model_4800.pt` | `tita_moo_stand_drive_4800.yaml` | early port |
| `model_4999.pt` (stack1 variant) | `tita_moo_stand_drive_4999_stack1.yaml` | |
| `model_4999.pt` (gtbasevel) | `tita_moo_stand_drive_4999_gtbasevel.yaml` | GT base velocity oracle introduced |
| `model_4999.pt` (targetheight v2) | `tita_moo_stand_drive_4999_targetheight_v2.yaml` | target-height command added |
| `2026-08-03_.../model_2500.pt` | `tita_moo_stand_drive_20260803_2500.yaml` | validated factor=0.5 `stand_jpos` against `interpolation_range=[0.0,0.85]` |
| `2026-08-03_.../model_4999.pt` | `tita_moo_stand_drive_20260803_4999.yaml` | |
| `2026-08-03_.../model_4999.pt` (wide) | `tita_moo_stand_drive_20260803_4999_targetheight_wide.yaml` | |
| `2026-08-04_.../model_4999.pt` (gtheight) | `tita_moo_stand_drive_20260804_4999_gtheight.yaml` | |
| `2026-08-04_.../model_9999.pt` (gtheight) | `tita_moo_stand_drive_20260804_9999_gtheight.yaml` | |
| `2026-08-06_.../model_4999.pt` (heightnorm) | `tita_moo_stand_drive_20260806_4999_heightnorm.yaml` | height-command normalization (`(h-center)/half_range`) introduced |
| `2026-08-06_21-45-27/model_8000.pt` (heightnorm v2) | `tita_moo_stand_drive_20260806_8000_heightnorm_v2.yaml` | `stand_jpos` reverted to original ad-hoc pose per explicit user request (see `04_reference_transform_up_issue.md`); `interpolation_range` narrowed to `[0.0, 0.1]` |
| `2026-08-07_10-50-56/model_4999.pt` (heightnorm v3) | `tita_moo_stand_drive_20260807_4999_heightnorm_v3.yaml` | pos_z range `(0.23, 0.42)`, `height_norm_center=0.325`, `height_norm_half_range=0.095`; `stand_jpos` carried over unchanged |
| **`2026-08-08_16-12-19/model_9999.pt` (RMATeacher)** | **`tita_moo_stand_drive_20260808_9999_rma_teacher.yaml`** | **Latest. Different network architecture (RMATeacher, not plain ActorCritic) — see `02_rma_teacher_architecture.md`. Height range widened via curriculum to its final `(0.25, 0.45)`, so `height_norm_center=0.35`, `height_norm_half_range=0.10` (NOT 0.325/0.095 — do not copy those forward from v3 into any checkpoint whose curriculum has reached `end_step`).** |

## Recurring gotchas across this whole line of work

- **Gym task ID selects the network class.** `play.py --task <id>` determines which
  `co_rl_cfg_entry_point` (and thus `policy.class_name`) gets built. Using the wrong
  task ID silently builds a mismatched-shape network and fails to load the
  checkpoint's `state_dict` — always grep the training repo's `__init__.py` for the
  correct registered task ID for a given checkpoint before exporting, don't assume
  it's the same as the previous checkpoint's task ID.
- **`preserve_order=False` regex-match joint/body ordering.** For a single regex
  pattern matching multiple entities in IsaacLab, resolution follows the asset's own
  body/joint list order. For this TITA articulation that order is
  `[L1, R1, L2, R2, L3, R3, L4, R4]` ("isaac order", interleaved), NOT the
  MuJoCo-native array order `[L1, L2, L3, L4, R1, R2, R3, R4]`. The reindex array
  `[0, 4, 1, 5, 2, 6, 3, 7]` converts native → isaac order. This shows up repeatedly:
  `_MOO_HIP_SHOULDER_IDX`, `_MOO_LEG_IDX`, `_MOO_WHEEL_IDX` in `obs_builder.py`, and
  now `_RMA_ACTUATOR_ISAAC_REINDEX` for the RMA privileged-obs actuator gains.
- **Height-command normalization applies only to the observation**, not to the
  command manager's own internal value or to reward functions (those stay in real
  meters). Config keys: `policy.height_command_normalize`, `policy.height_norm_center`,
  `policy.height_norm_half_range`, `command.default_height_m`. The correct
  center/half-range must be re-derived per checkpoint from that run's
  `feature_functions_common.py` constants (`_HEIGHT_NORM_CENTER`,
  `_HEIGHT_NORM_HALF_RANGE`) or the `widen_height_range` curriculum term's
  `end_range` if the checkpoint's iteration is past the curriculum's `end_step` —
  do NOT assume it's unchanged from the previous checkpoint's config.
- **Never overwrite an existing config file.** Every new checkpoint gets its own
  new, descriptively-named YAML (copy-then-edit from the most similar prior config),
  so old deployments stay reproducible/diffable.
