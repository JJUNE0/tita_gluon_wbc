"""Leg action filter for the real-to-sim variants of the My flat TITA task.

``MA2JointPositionAction`` applies the mean of the current and the previous raw policy action as the joint
position target. Its gain at 25 Hz is zero and its DC gain is one. The ActionManager keeps the raw actions, so
the ``last_action`` observation and the action-rate reward are unchanged. The first step after a reset uses
the raw action (no half step from zero). This matches the deployed ``leg_action_filter:=ma2_legs`` option.
"""

from __future__ import annotations

from collections.abc import Sequence

import torch

from isaaclab.envs.mdp.actions.actions_cfg import JointPositionActionCfg
from isaaclab.envs.mdp.actions.joint_actions import JointPositionAction
from isaaclab.utils import configclass


class MA2JointPositionAction(JointPositionAction):
    """Joint position action whose applied target is the 2-tap average of raw policy actions."""

    cfg: MA2JointPositionActionCfg

    def __init__(self, cfg: MA2JointPositionActionCfg, env):
        super().__init__(cfg, env)
        self._previous = torch.zeros_like(self._raw_actions)
        self._fresh = torch.ones(self.num_envs, dtype=torch.bool, device=self.device)

    def process_actions(self, actions: torch.Tensor):
        filtered = torch.where(self._fresh.unsqueeze(1), actions, 0.5 * (actions + self._previous))
        self._previous[:] = actions
        self._fresh[:] = False
        super().process_actions(filtered)

    def reset(self, env_ids: Sequence[int] | None = None) -> None:
        super().reset(env_ids)
        self._fresh[slice(None) if env_ids is None else env_ids] = True


@configclass
class MA2JointPositionActionCfg(JointPositionActionCfg):
    class_type: type = MA2JointPositionAction
