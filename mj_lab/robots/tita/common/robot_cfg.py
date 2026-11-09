"""TRAINING_SIM: TITA model and delayed PD motors for MuJoCo Warp."""

from pathlib import Path

import mujoco
from mjlab.actuator import IdealPdActuatorCfg
from mjlab.entity import EntityArticulationInfoCfg, EntityCfg

REPO_ROOT = Path(__file__).resolve().parents[4]
ROBOT_XML = REPO_ROOT / "sim2sim/robot/tita/mujoco_corrected/robot.xml"
JOINTS = tuple(f"joint_{side}_leg_{i}" for side in ("left", "right") for i in range(1, 5))
OBS_JOINTS = tuple(f"joint_{side}_leg_{i}" for i in range(1, 5) for side in ("left", "right"))
WHEELS = ("left_leg_4", "right_leg_4")
INITIAL_Q = (0.0, 0.8, -1.5, 0.0) * 2


def get_spec():
    # Reuse the corrected URDF inertias/kinematics; never edit the source asset.
    spec = mujoco.MjSpec.from_file(str(ROBOT_XML))
    # Scene-level solver settings are configured by SimulationCfg.
    spec.option.cone = mujoco.mjtCone.mjCONE_PYRAMIDAL
    spec.option.impratio = 1.0
    for actuator in list(spec.actuators):
        spec.delete(actuator)
    for geom in spec.geoms:
        if geom.contype or geom.conaffinity:
            geom.name = geom.parent.name + "_collision"
            # Ground contacts only: Isaac's selected task disables self collision.
            geom.contype, geom.conaffinity, geom.condim = 0, 1, 3
            geom.priority = 1  # Robot friction DR must override the plane's coefficient.
            geom.friction = [1.0, 0.005, 0.0001]
            if geom.parent.name in WHEELS:
                geom.type = mujoco.mjtGeom.mjGEOM_SPHERE
                geom.size = [0.0925, 0.0, 0.0]
    return spec


def robot_cfg():
    common = dict(effort_limit=60.0, delay_min_lag=0, delay_max_lag=4,
                  delay_hold_prob=1.0, armature=0.0, frictionloss=0.0,
                  viscous_damping=0.0)
    return EntityCfg(
        spec_fn=get_spec,
        init_state=EntityCfg.InitialStateCfg(
            pos=(0.0, 0.0, 0.4), joint_pos=dict(zip(JOINTS, INITIAL_Q)),
            joint_vel={".*": 0.0}),
        articulation=EntityArticulationInfoCfg(
            soft_joint_pos_limit_factor=0.9,
            actuators=(
                IdealPdActuatorCfg(target_names_expr=(".*_leg_[12]",), stiffness=60.0, damping=1.5, **common),
                IdealPdActuatorCfg(target_names_expr=(".*_leg_3",), stiffness=92.0, damping=2.3, **common),
                IdealPdActuatorCfg(target_names_expr=(".*_leg_4",), stiffness=0.0, damping=0.5,
                                   **{**common, "effort_limit": 12.0}),
            )),
    )
