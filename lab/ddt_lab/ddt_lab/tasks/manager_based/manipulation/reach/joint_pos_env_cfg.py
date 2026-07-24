"""Phase-A fixed-base position reach environment for the standalone GLUON."""

from isaaclab.managers import SceneEntityCfg
from isaaclab.utils import configclass

import isaaclab_tasks.manager_based.manipulation.reach.mdp as mdp
from isaaclab_tasks.manager_based.manipulation.reach.reach_env_cfg import ReachEnvCfg

from ddt_lab.assets.gluon import GLUON_2L6_4L3_CFG, GLUON_END_EFFECTOR_BODY, GLUON_JOINT_NAMES


GLUON_A0_ACTION_SCALE_RAD = {
    "axis_joint_1": 1.00,
    "axis_joint_2": 0.45,
    "axis_joint_3": 1.00,
    "axis_joint_4": 1.00,
    "axis_joint_5": 1.00,
    "axis_joint_6": 1.00,
}


@configclass
class GluonReachEnvCfg(ReachEnvCfg):
    """Minimal W0/A0 environment used to validate the reach data path.

    The target box is deliberately local to the measured q=0 FK pose.  It is
    not the final collision-filtered workspace.
    """

    def __post_init__(self):
        super().__post_init__()

        self.scene.robot = GLUON_2L6_4L3_CFG.replace(prim_path="{ENV_REGEX_NS}/Robot")
        self.scene.table = None
        self.scene.ground.init_state.pos = (0.0, 0.0, -0.10)
        self.scene.num_envs = 1024
        self.scene.env_spacing = 1.5

        # q=0 FK from the validated Isaac articulation is approximately
        # [0.5762, 0.0, -0.1360] m in base_link.  W0 stays close to it.
        self.commands.ee_pose.body_name = GLUON_END_EFFECTOR_BODY
        self.commands.ee_pose.resampling_time_range = (2.0, 2.0)
        self.commands.ee_pose.ranges.pos_x = (0.52, 0.58)
        self.commands.ee_pose.ranges.pos_y = (-0.04, 0.04)
        self.commands.ee_pose.ranges.pos_z = (-0.18, -0.10)
        self.commands.ee_pose.ranges.roll = (0.0, 0.0)
        self.commands.ee_pose.ranges.pitch = (0.0, 0.0)
        self.commands.ee_pose.ranges.yaw = (0.0, 0.0)

        ee_cfg = SceneEntityCfg("robot", body_names=[GLUON_END_EFFECTOR_BODY])
        self.rewards.end_effector_position_tracking.params["asset_cfg"] = ee_cfg
        self.rewards.end_effector_position_tracking_fine_grained.params["asset_cfg"] = SceneEntityCfg(
            "robot", body_names=[GLUON_END_EFFECTOR_BODY]
        )
        self.rewards.end_effector_orientation_tracking.params["asset_cfg"] = SceneEntityCfg(
            "robot", body_names=[GLUON_END_EFFECTOR_BODY]
        )
        # Position is primary; identity and -identity are the same q=0 nominal
        # orientation, so retain only a weak soft orientation constraint.
        self.rewards.end_effector_orientation_tracking.weight = -0.02

        self.actions.arm_action = mdp.JointPositionActionCfg(
            asset_name="robot",
            joint_names=list(GLUON_JOINT_NAMES),
            scale=GLUON_A0_ACTION_SCALE_RAD,
            use_default_offset=True,
            preserve_order=True,
        )

        self.events.reset_robot_joints.func = mdp.reset_joints_by_offset
        self.events.reset_robot_joints.params["position_range"] = (-0.05, 0.05)
        self.events.reset_robot_joints.params["velocity_range"] = (0.0, 0.0)
        self.events.reset_robot_joints.params["asset_cfg"] = SceneEntityCfg(
            "robot", joint_names=list(GLUON_JOINT_NAMES), preserve_order=True
        )

        self.observations.policy.enable_corruption = False
        self.rewards.joint_vel.params["asset_cfg"] = SceneEntityCfg(
            "robot", joint_names=list(GLUON_JOINT_NAMES), preserve_order=True
        )

        # Phase-A external interface: 200 Hz physics, 50 Hz policy.
        self.sim.dt = 0.005
        self.decimation = 4
        self.sim.render_interval = self.decimation
        self.episode_length_s = 8.0


@configclass
class GluonReachEnvCfg_PLAY(GluonReachEnvCfg):
    def __post_init__(self):
        super().__post_init__()
        self.scene.num_envs = 16
        self.commands.ee_pose.debug_vis = True
        self.observations.policy.enable_corruption = False

