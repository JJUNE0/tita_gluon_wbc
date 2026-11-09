"""TRAINING_SIM: task packages and compatibility with saved native configs.

Old ``env.pkl`` files reference modules directly under this package. Register
those names as aliases of the relocated modules so existing checkpoints and
trial scripts continue to load. New callers should use the task subpackages.
The common aliases must exist before importing the unchanged flat config.
"""

from importlib import import_module as _import_module
import sys as _sys

_LEGACY_MODULES = {
    "robot_cfg": "common.robot_cfg",
    "mdp": "common.mdp",
    "flat_env_roll_pitch_height_cfg": "roll_pitch_height.flat_env_roll_pitch_height_cfg",
    "walk_env_cfg": "walk.walk_env_cfg",
    "inline_env_cfg": "walk.inline_env_cfg",
    "stand_one_leg_env_cfg": "stand_one_leg.stand_one_leg_env_cfg",
    "stand_one_leg_reference_env_cfg": "stand_one_leg.stand_one_leg_reference_env_cfg",
    "stand_one_leg_anchor_env_cfg": "stand_one_leg.stand_one_leg_anchor_env_cfg",
    "support_command_env_cfg": "stand_one_leg.support_command_env_cfg",
    "sit_stand_env_cfg": "sit_stand.sit_stand_env_cfg",
    "height_only_env_cfg": "sit_stand.height_only_env_cfg",
    "flat_env_residual_torque": "residual.flat_env_residual_torque",
}

for _old, _new in _LEGACY_MODULES.items():
    _module = _import_module(f".{_new}", __name__)
    _sys.modules[f"{__name__}.{_old}"] = _module
    globals()[_old] = _module

del _old, _new, _module
