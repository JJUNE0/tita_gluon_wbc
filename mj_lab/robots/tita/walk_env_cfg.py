"""TRAINING_SIM: wheel-balanced standing and alternating walking on command.

Standing: gait off, driving wheel scale, flat hip/shoulder deviation weights.
Moving: gait on, zero wheel target, hip and shoulder effective weights -0.1.
The five gait observations expose the active mode without adding dimensions.
"""

from dataclasses import fields

from mjlab.managers import ObservationTermCfg, RewardTermCfg, TerminationTermCfg

from . import mdp
from .flat_env_cfg import TitaFlatEnvCfg


class TitaWalkEnvCfg(TitaFlatEnvCfg):
    def __init__(self, num_envs=1024, play=False):
        super().__init__(num_envs, play)
        velocity = self.commands["base_velocity"]
        velocity.lin_vel_x = velocity.lin_vel_y = (-.5, .5)
        velocity.ang_vel_z = (0.0, 0.0)
        velocity.ramp_rate, velocity.initial_phase_time = .3, 1.0
        velocity.sensor_bias = False
        velocity.wheel_error_gait_name = "gait"
        velocity.wheel_error_velocity_thresholds = (.1, .15)
        velocity.wheel_error_moving_anchor = True
        for sensor in self.scene.sensors:
            sensor.history_length = self.decimation
        self.commands["gait"] = mdp.GaitCommandCfg(resampling_time_range=(1e9, 1e9), step_in_place=False)
        for group in self.observations.values():
            group.terms["gait"] = ObservationTermCfg(func=mdp.observation, params={"kind": "gait"})
        for name in ("joint_vel_3", "joint_vel_7"):
            inherited = self.actions[name]
            self.actions[name] = mdp.GaitGatedWheelVelocityActionCfg(
                **{item.name: getattr(inherited, item.name) for item in fields(inherited) if item.init},
                gait_name="gait")
        for name in ("joint_mirror", "zero_command_wheel_action", "ang_vel_xy_l2"):
            del self.rewards[name]
        for name in ("joint_deviation_hip", "joint_deviation_shoulder"):
            term = self.rewards[name]
            term.func = mdp.mode_scaled_joint_deviation
            # Flat weights are -1.0 / -0.5; moving weights are both -0.1.
            term.params["moving_scale"] = -0.1 / term.weight
        for name, axis, weight in (("roll", 0, -.02), ("pitch", 1, -.1)):
            self.rewards[f"ang_vel_{name}_l2"] = RewardTermCfg(func=mdp.reward, weight=weight, params={"kind": "ang_vel_axis_l2", "axis": axis})
        self.rewards.update(
            gait_contact=RewardTermCfg(func=mdp.contact_schedule, weight=2.0, params={"only_when_enabled": True}),
            gait_clearance=RewardTermCfg(func=mdp.wheel_clearance, weight=1.0, params={"clearance_m": .04, "only_when_enabled": True}),
            termination=RewardTermCfg(func=mdp.reward, weight=-10.0, params={"kind": "termination"}))
        self.terminations["knee_contact"] = TerminationTermCfg(func=mdp.illegal_contact, params={"sensor": "knees", "threshold": 1.0})
        for name in ("add_base_mass", "add_base_inertia", "add_base_com", "push_robot"):
            del self.events[name]
        self.events["physics_material"].params["ranges"] = (.8, 1.2)
        self.events["reset_base"].params["velocity_range"] = {axis: (0., 0.) for axis in ("x", "y", "z", "roll", "pitch", "yaw")}
        self.events["reset_joints"].params["position_range"] = (1.0, 1.0)


def make_walk_env_cfg(num_envs=1024, play=False):
    return TitaWalkEnvCfg(num_envs, play)
