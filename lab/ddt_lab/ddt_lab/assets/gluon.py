"""Isaac Lab asset configuration for the standalone GLUON 2L6/4L3 arm.

The actuator values in this module are a simulation baseline.  They are not a
claim about the gains or torque limits configured in the real INNFOS drive.
"""

from pathlib import Path

import isaaclab.sim as sim_utils
from isaaclab.actuators import ImplicitActuatorCfg
from isaaclab.assets.articulation import ArticulationCfg


DDT_LAB_ROOT = Path(__file__).resolve().parents[4]
GLUON_DESCRIPTION_DIR = DDT_LAB_ROOT / "gluon" / "gluon_2L6_4L3_urdf"
GLUON_2L6_4L3_URDF_PATH = GLUON_DESCRIPTION_DIR / "urdf" / "gluon_2L6_4L3_sim.urdf"

GLUON_JOINT_NAMES = tuple(f"axis_joint_{index}" for index in range(1, 7))
GLUON_BODY_NAMES = ("base_link",) + tuple(f"link{index}" for index in range(1, 7))
GLUON_END_EFFECTOR_BODY = "link6"
GLUON_HOME_JOINT_POS = {joint_name: 0.0 for joint_name in GLUON_JOINT_NAMES}
GLUON_EXPECTED_TOTAL_MASS_KG = 4.267611380601286

# Confirmed in the local GL_2L6_4L3 model database: axes 1--3 are limited to
# 120 deg/s and axes 4--6 to 200 deg/s.  The effort and PD values below remain
# provisional SIM_NOMINAL values until actuator-response identification is done.
GLUON_SIM_NOMINAL_VELOCITY_LIMIT_RAD_S = {
    "axis_joint_[1-3]": 2.0943951023931953,
    "axis_joint_[4-6]": 3.490658503988659,
}
GLUON_SIM_NOMINAL_EFFORT_LIMIT_NM = {
    "axis_joint_[1-2]": 18.0,
    "axis_joint_[3-6]": 10.0,
}
GLUON_SIM_NOMINAL_STIFFNESS = {
    "axis_joint_[1-2]": 80.0,
    "axis_joint_[3-6]": 40.0,
}
GLUON_SIM_NOMINAL_DAMPING = {
    "axis_joint_[1-2]": 4.0,
    "axis_joint_[3-6]": 2.0,
}


GLUON_2L6_4L3_CFG = ArticulationCfg(
    spawn=sim_utils.UrdfFileCfg(
        asset_path=str(GLUON_2L6_4L3_URDF_PATH),
        fix_base=True,
        merge_fixed_joints=True,
        replace_cylinders_with_capsules=False,
        collider_type="convex_hull",
        self_collision=False,
        activate_contact_sensors=False,
        rigid_props=sim_utils.RigidBodyPropertiesCfg(
            disable_gravity=False,
            linear_damping=0.0,
            angular_damping=0.0,
            max_depenetration_velocity=5.0,
        ),
        articulation_props=sim_utils.ArticulationRootPropertiesCfg(
            enabled_self_collisions=False,
            solver_position_iteration_count=8,
            solver_velocity_iteration_count=1,
        ),
        # Avoid inheriting an accidental importer drive.  The actuator block
        # below is the single source of the SIM_NOMINAL joint-drive settings.
        joint_drive=sim_utils.UrdfConverterCfg.JointDriveCfg(
            target_type="none",
            gains=sim_utils.UrdfConverterCfg.JointDriveCfg.PDGainsCfg(
                stiffness=0.0,
                damping=0.0,
            ),
        ),
    ),
    init_state=ArticulationCfg.InitialStateCfg(
        pos=(0.0, 0.0, 0.0),
        # The canonical ROS URDF expresses this mounting transform through a
        # world->base_link fixed joint.  The sim variant removes the empty
        # world link, so apply the same -pi/2 rotation about Y at the root.
        rot=(0.7071067811865476, 0.0, -0.7071067811865475, 0.0),
        joint_pos=GLUON_HOME_JOINT_POS,
        joint_vel={".*": 0.0},
    ),
    soft_joint_pos_limit_factor=0.95,
    actuators={
        "arm_sim_nominal": ImplicitActuatorCfg(
            joint_names_expr=["axis_joint_[1-6]"],
            velocity_limit_sim=GLUON_SIM_NOMINAL_VELOCITY_LIMIT_RAD_S,
            effort_limit_sim=GLUON_SIM_NOMINAL_EFFORT_LIMIT_NM,
            stiffness=GLUON_SIM_NOMINAL_STIFFNESS,
            damping=GLUON_SIM_NOMINAL_DAMPING,
            friction=0.0,
        ),
    },
)
"""Fixed-base standalone GLUON configuration for Phase-A reach training."""
