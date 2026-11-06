"""TRAINING_SIM: selected TITA driving task on mjlab/MuJoCo Warp.

Policy/critic 35/39, native actions 8, physics/control 200/50 Hz.
MuJoCo sliding friction replaces PhysX static/dynamic materials. Restitution
and contact solver parameters are engine specific; this is a port, not a claim
of numerical equivalence between the two physics engines.
"""

import math

from mjlab.envs import ManagerBasedRlEnvCfg
from mjlab.envs import mdp as native
from mjlab.envs.mdp import dr
from mjlab.envs.mdp.actions import JointPositionActionCfg, JointVelocityActionCfg
from mjlab.managers import (
    EventTermCfg, ObservationGroupCfg, ObservationTermCfg, RewardTermCfg,
    SceneEntityCfg, TerminationTermCfg,
)
from mjlab.scene import SceneCfg
from mjlab.sensor import ContactMatch, ContactSensorCfg
from mjlab.sim import MujocoCfg, SimulationCfg
from mjlab.terrains import TerrainEntityCfg
from mjlab.utils.noise import UniformNoiseCfg
from mjlab.viewer.viewer_config import ViewerConfig

from . import mdp
from .robot_cfg import JOINTS, robot_cfg


def observations(critic=False):
    terms = {}
    if critic:
        terms["base_lin_vel"] = ObservationTermCfg(func=mdp.observation, params={"kind": "base_lin_vel", "critic": True}, scale=2.0, clip=(-100, 100))
    for name, scale, noise in (
        ("base_ang_vel", .25, .2), ("projected_gravity", 1.0, .05),
        ("velocity_commands", (2.0, 2.0, .25), 0),
        ("joint_pos", 1.0, .01), ("joint_vel", .05, 1.5),
        ("actions", 1.0, 0), ("wheel_position_error", 5.0, .005),
        *(([("heading_drift_error", 2.0, 0)]) if critic else []),
        ("heading_error", 2.0, .003),
    ):
        terms[name] = ObservationTermCfg(
            func=mdp.observation, params={"kind": name, "critic": critic},
            scale=scale, clip=(-3.2, 3.2) if name == "heading_drift_error" else (-100, 100),
            noise=UniformNoiseCfg(n_min=-noise, n_max=noise) if noise and not critic else None)
    return ObservationGroupCfg(terms=terms, concatenate_terms=True, enable_corruption=not critic)


def contact_sensor(name, bodies):
    return ContactSensorCfg(
        name=name, primary=ContactMatch(mode="body", pattern=bodies, entity="robot"),
        secondary=ContactMatch(mode="body", pattern="terrain"), fields=("found", "force"),
        reduce="netforce", num_slots=1, track_air_time=True, history_length=3)


class TitaFlatEnvCfg(ManagerBasedRlEnvCfg):
    def __init__(self, num_envs=1024, play=False):
        actions = {}
        for i, joint in enumerate(JOINTS):
            wheel = i in (3, 7)
            cls = JointVelocityActionCfg if wheel else JointPositionActionCfg
            actions[f"joint_{'vel' if wheel else 'pos'}_{i}"] = cls(
                entity_name="robot", actuator_names=(joint,), scale=20.0 if wheel else .25,
                clip={".*": (-100.0, 100.0)}, use_default_offset=True)
        weights = {
            "track_lin_vel_xy_exp": 2.0, "track_lin_vel_xy_exp_2": .5,
            "track_lin_vel_xy_exp_3": .5, "track_ang_vel_z_exp": 1.0,
            "lin_vel_z_l2": -2.0, "ang_vel_xy_l2": -.05,
            "dof_torques_l2": -1e-5, "dof_acc_l2": -2.5e-7,
            "action_rate_l2": -.01, "joint_mirror": -1.0,
            "undesired_contacts": -1.0, "flat_orientation_l2": -5.0,
            "base_height_l2": -10.0, "joint_deviation_hip": -1.0,
            "joint_deviation_shoulder": -.5,
            "zero_command_position_drift": 1.0, "zero_command_wheel_action": -.05,
            "zero_command_heading_drift": 1.0,
        }
        rewards = {}
        for name, weight in weights.items():
            kind = {"dof_torques_l2": "joint_torques_l2", "dof_acc_l2": "joint_acc_l2",
                    "track_lin_vel_xy_exp_2": "track_lin_vel_xy_exp",
                    "track_lin_vel_xy_exp_3": "track_lin_vel_xy_exp"}.get(name, name)
            params = {"kind": kind}
            if name.startswith("track_lin_vel"):
                params["std"] = math.sqrt({"track_lin_vel_xy_exp": .25, "track_lin_vel_xy_exp_2": .0625, "track_lin_vel_xy_exp_3": .03125}[name])
            rewards[name] = RewardTermCfg(func=mdp.reward, weight=weight, params=params)
        events = {
            "physics_material": EventTermCfg(func=dr.geom_friction, mode="startup", params={"ranges": (.2, 1.6)}),
            "add_base_mass": EventTermCfg(func=dr.body_mass, mode="startup", params={"ranges": (-.5, 2.0), "operation": "add", "asset_cfg": SceneEntityCfg("robot", body_names="base_link")}),
            "add_base_inertia": EventTermCfg(func=mdp.randomize_inertia, mode="startup"),
            "add_base_com": EventTermCfg(func=dr.body_ipos, mode="startup", params={"ranges": (-.015, .015), "operation": "add", "asset_cfg": SceneEntityCfg("robot", body_names="base_link")}),
            "reset_base": EventTermCfg(func=native.reset_root_state_uniform, mode="reset", params={
                "pose_range": {"x": (-.5, .5), "y": (-.5, .5), "yaw": (-3.14, 3.14)},
                "velocity_range": {axis: (-.5, .5) for axis in ("x", "y", "z", "roll", "pitch", "yaw")}}),
            "reset_joints": EventTermCfg(func=mdp.reset_joints, mode="reset", params={"position_range": (-.5, 1.0)}),
            "randomize_motors": EventTermCfg(func=mdp.randomize_motors, mode="reset"),
            "push_robot": EventTermCfg(func=native.push_by_setting_velocity, mode="interval", interval_range_s=(10.0, 15.0), params={"velocity_range": {"x": (-.5, .5), "y": (-.5, .5)}}),
        }
        super().__init__(
            scene=SceneCfg(num_envs=num_envs, env_spacing=2.5, entities={"robot": robot_cfg()},
                terrain=TerrainEntityCfg(terrain_type="plane"),
                sensors=(contact_sensor("feet", ("left_leg_4", "right_leg_4")),
                         contact_sensor("knees", ("left_leg_3", "right_leg_3")),
                         contact_sensor("base", "base_link"))),
            decimation=4, episode_length_s=20.0, auto_reset=False,
            sim=SimulationCfg(mujoco=MujocoCfg(timestep=.005, cone="elliptic", iterations=20, ls_iterations=10), nconmax=64, njmax=128),
            viewer=ViewerConfig(height=480, width=640, distance=2.0, elevation=-15, azimuth=120,
                                origin_type=ViewerConfig.OriginType.ASSET_ROOT, entity_name="robot"),
            observations={"policy": observations(), "critic": observations(critic=True)},
            actions=actions, rewards=rewards, events=events,
            commands={"base_velocity": mdp.VelocityCommandCfg(resampling_time_range=(6.0, 8.0))},
            terminations={"time_out": TerminationTermCfg(func=mdp.timeout, time_out=True),
                          "base_contact": TerminationTermCfg(func=mdp.illegal_contact, params={"sensor": "base"})})
        if play:
            self.observations["policy"].enable_corruption = False
            self.commands["base_velocity"].sensor_bias = False


def make_flat_env_cfg(num_envs=1024, play=False):
    return TitaFlatEnvCfg(num_envs, play)
