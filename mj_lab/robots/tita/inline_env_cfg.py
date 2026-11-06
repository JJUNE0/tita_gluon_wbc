"""TRAINING_SIM: flat driving with alternating foot lifts on straight commands."""

from mjlab.managers import ObservationTermCfg, RewardTermCfg, TerminationTermCfg

from . import mdp
from .flat_env_cfg import TitaFlatEnvCfg


class TitaInlineEnvCfg(TitaFlatEnvCfg):
    def __init__(self, num_envs=1024, play=False):
        super().__init__(num_envs, play)
        velocity = self.commands["base_velocity"]
        velocity.rel_straight_envs = .5
        velocity.wheel_error_gait_name = "gait"
        velocity.wheel_error_velocity_thresholds = (.1, .15)
        velocity.wheel_error_moving_anchor = True
        self.commands["gait"] = mdp.GaitCommandCfg(
            resampling_time_range=(1e9, 1e9), frequency_range_hz=(.5, .5),
            stance_fraction=.8, step_in_place=False, straight_only=True,
            yaw_threshold=0.)
        for group in self.observations.values():
            group.terms["gait"] = ObservationTermCfg(func=mdp.observation, params={"kind": "gait"})
        for name, moving_weight in (
            ("joint_deviation_hip", -.02), ("joint_deviation_shoulder", -.02),
            ("joint_mirror", 0.), ("flat_orientation_l2", -1.),
        ):
            term = self.rewards[name]
            term.func = mdp.mode_scaled_joint_deviation
            # Relax only during straight gait; standing/turning retain flat costs.
            term.params["moving_scale"] = moving_weight / term.weight
        angular_weight = self.rewards.pop("ang_vel_xy_l2").weight
        for name, axis, moving_weight in (("roll", 0, -.01), ("pitch", 1, -.03)):
            self.rewards[f"ang_vel_{name}_l2"] = RewardTermCfg(
                func=mdp.mode_scaled_joint_deviation, weight=angular_weight,
                params={"kind": "ang_vel_axis_l2", "axis": axis,
                        "moving_scale": moving_weight / angular_weight})
        self.rewards.update(
            gait_contact=RewardTermCfg(func=mdp.contact_schedule, weight=2., params={"only_when_enabled": True}),
            gait_clearance=RewardTermCfg(func=mdp.wheel_clearance, weight=1., params={"clearance_m": .04, "only_when_enabled": True}),
            gait_stance_push=RewardTermCfg(func=mdp.stance_push, weight=.5, params={"stride_m": .06, "std": .1}),
            termination=RewardTermCfg(func=mdp.reward, weight=-10., params={"kind": "termination"}))
        self.terminations["knee_contact"] = TerminationTermCfg(func=mdp.illegal_contact, params={"sensor": "knees", "threshold": 1.})


def make_inline_env_cfg(num_envs=1024, play=False):
    return TitaInlineEnvCfg(num_envs, play)
