"""TRAINING_SIM: height-controlled sitting/rising, with the flat task at height.

First learn standing above 25 cm with contact termination. At 20000 training
steps, low goals allow base/knee support and do not request driving or tilt.
The 7 cm goal is soft: upright base collision geometry bottoms near 7.9 cm.
Set curriculum_transition_step=None for standing-only height training: retain
25–50 cm goals and contact termination for the entire run.
"""

from dataclasses import dataclass

import torch
from mjlab.managers import TerminationTermCfg

from ..common import mdp
from ..roll_pitch_height.flat_env_roll_pitch_height_cfg import TitaFlatRollPitchHeightEnvCfg, pose_observation


def height_scaled_penalty(env, kind):
    """Relax the old standing posture/contact costs only for low height goals."""
    motion_range = env.cfg.commands["base_pose"].height_motion_range
    if motion_range is None:
        return mdp.reward(env, kind)
    lo, hi = motion_range
    scale = ((pose_observation(env)[:, 2] - lo) / (hi - lo)).clamp(0., 1.)
    return mdp.reward(env, kind) * scale


def curriculum_contact(env, sensor):
    if env.cfg.curriculum_stage == 1:
        return mdp.illegal_contact(env, sensor)
    return torch.zeros(env.num_envs, dtype=torch.bool, device=env.device)


@dataclass(init=False)
class TitaSitStandEnvCfg(TitaFlatRollPitchHeightEnvCfg):
    # Saved with the native config: playback uses the checkpoint's stage and
    # never advances the curriculum using the short evaluation rollout clock.
    curriculum_transition_step: int | None = 20_000
    curriculum_stage: int = 1

    def __init__(self, num_envs=4096, play=False):
        super().__init__(num_envs, play)
        self.curriculum_transition_step = 20_000
        self.curriculum_stage = 1
        # Pose sampling stays independent: zero velocity must also be learned
        # at varied roll/pitch/height goals. Resample stop/move in every env so
        # the policy practices moving-to-stopped transitions as well.
        self.commands["base_velocity"].rel_standing_envs = .5
        self.rewards["base_height_l2"].weight = -50.
        pose = self.commands["base_pose"]
        pose.height_range = (.25, .5)
        pose.height_target_bands = None
        pose.height_motion_range = None
        pose.ramp_rates = (.15, .15, .04)
        # A full 43 cm sweep takes 10.75 s; allow time to hold each goal.
        pose.resampling_time_range = (14., 16.)
        self.episode_length_s = 40.
        for name, sensor in (("base_contact", "base"), ("knee_contact", "knees")):
            self.terminations[name] = TerminationTermCfg(func=curriculum_contact, params={"sensor": sensor})
        for name in ("undesired_contacts", "joint_deviation_hip", "joint_deviation_shoulder"):
            self.rewards[name].func = height_scaled_penalty
        # q_target = q_default + .25 * gain(sign(a)) * a, |a| <= 1.
        # Covers IDLE (+/-.75, 1.2, -2.7), plus knee extension to -.7 rad.
        # The -2.7 target matches IDLE; actual joint limits still apply.
        self.action_gain_negative = (3., 2., 4.8, 6.) * 2
        self.action_gain_positive = (3., 2., 3.2, 6.) * 2

    def set_training_step(self, step, env=None):
        """Called before a training transition, using vector steps, not updates."""
        if self.curriculum_transition_step is None:
            return False
        stage = 1 if step < self.curriculum_transition_step else 2
        if self.curriculum_stage == stage:
            return False
        self.curriculum_stage = stage
        pose = self.commands["base_pose"]
        pose.height_range = (.25, .5) if stage == 1 else (.07, .5)
        pose.height_target_bands = None if stage == 1 else ((.07, .12), (.335, .5))
        pose.height_motion_range = None if stage == 1 else (.20, .27)
        if env is not None:
            # CommandManager deep-copies term configs; update its live sampler
            # as well as the native config saved by checkpointing.
            command = env.command_manager.get_term("base_pose")
            for name in ("height_range", "height_target_bands", "height_motion_range"):
                setattr(command.cfg, name, getattr(pose, name))
        return True
