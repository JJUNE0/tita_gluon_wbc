"""Curriculum terms specific to the conditioned GLUON payload motion."""

from __future__ import annotations

from collections.abc import Sequence
from typing import TYPE_CHECKING

import torch

from .actions import SmoothRandomJointPositionAction

if TYPE_CHECKING:
    from isaaclab.envs import ManagerBasedRLEnv


def linearly_widen_gluon_workspace(
    env: ManagerBasedRLEnv,
    env_ids: Sequence[int],
    action_term_name: str,
    start_step: int,
    end_step: int,
    start_scale: float = 0.0,
    end_scale: float = 1.0,
) -> torch.Tensor:
    """Expand validated WORK-to-waypoint rays from fixed arm to full range.

    This deliberately scales conditioned joint-space rays.  It is a safe
    curriculum backend for the current waypoint set, not a claim of uniform
    Cartesian end-effector sampling.  A future IK sampler can preserve this
    scalar curriculum interface while replacing the trajectory backend.
    """
    if end_step <= start_step:
        raise ValueError("end_step must be greater than start_step")
    if not 0.0 <= start_scale <= end_scale <= 1.0:
        raise ValueError("workspace scales must satisfy 0 <= start <= end <= 1")

    step = int(env.common_step_counter)
    fraction = min(max((step - start_step) / (end_step - start_step), 0.0), 1.0)
    scale = start_scale + (end_scale - start_scale) * fraction

    action_term = env.action_manager.get_term(action_term_name)
    if not isinstance(action_term, SmoothRandomJointPositionAction):
        raise TypeError(
            f"action term {action_term_name!r} must be SmoothRandomJointPositionAction, "
            f"got {type(action_term).__name__}"
        )
    action_term.set_workspace_scale(scale)
    return torch.tensor(scale, dtype=torch.float32, device=env.device)
