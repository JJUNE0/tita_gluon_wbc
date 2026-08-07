#!/usr/bin/env python3
"""View the combined TITA+GLUON draft with its sampled reachability shell."""

import argparse

from isaaclab.app import AppLauncher


parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument(
    "--reachability-map",
    type=str,
    default="test/eval_logs/tita_gluon_reachability_q6_zero.npz",
)
parser.add_argument("--reachability-opacity", type=float, default=0.04)
parser.add_argument(
    "--max-frames",
    type=int,
    default=0,
    help="Exit after this many rendered frames; zero keeps the GUI open.",
)
AppLauncher.add_app_launcher_args(parser)
args_cli = parser.parse_args()
app_launcher = AppLauncher(args_cli)
simulation_app = app_launcher.app


import json  # noqa: E402
from pathlib import Path  # noqa: E402

import numpy as np  # noqa: E402
import omni.usd  # noqa: E402
from pxr import Gf, UsdGeom, Vt  # noqa: E402

import isaaclab.sim as sim_utils  # noqa: E402
from isaaclab.assets import Articulation  # noqa: E402
from isaaclab.assets.articulation import ArticulationCfg  # noqa: E402
from isaaclab.sim import SimulationContext  # noqa: E402


REPO_ROOT = Path(__file__).resolve().parents[1]
COMBINED_URDF = (
    REPO_ROOT
    / "sim2sim"
    / "tita_gluon_urdf"
    / "urdf"
    / "tita_gluon_2L6_4L3.urdf"
)
TITA_STAND_Q_RAD = {
    "joint_left_leg_1": 0.1,
    "joint_left_leg_2": 0.8,
    "joint_left_leg_3": -1.5,
    "joint_left_leg_4": 0.0,
    "joint_right_leg_1": 0.1,
    "joint_right_leg_2": 0.8,
    "joint_right_leg_3": -1.5,
    "joint_right_leg_4": 0.0,
}
GLUON_WORK_Q_RAD = {
    "gluon_2L6_4L3_axis_joint_1": 0.0,
    "gluon_2L6_4L3_axis_joint_2": 0.8,
    "gluon_2L6_4L3_axis_joint_3": 1.6,
    "gluon_2L6_4L3_axis_joint_4": 0.8,
    "gluon_2L6_4L3_axis_joint_5": 0.0,
    "gluon_2L6_4L3_axis_joint_6": 0.0,
}


def create_reachability_surface(map_path: Path, opacity: float) -> None:
    if not 0.0 < opacity <= 1.0:
        raise ValueError("--reachability-opacity must be in (0, 1]")
    if not map_path.is_file():
        raise FileNotFoundError(f"reachability map not found: {map_path}")
    with np.load(map_path, allow_pickle=False) as reachability:
        metadata = json.loads(reachability["metadata_json"].item())
        vertices = np.asarray(
            reachability["surface_vertices_tita_b_m"], dtype=np.float32
        )
        faces = np.asarray(reachability["surface_faces"], dtype=np.int32)
    stage = omni.usd.get_context().get_stage()
    mesh = UsdGeom.Mesh.Define(stage, "/Visuals/TitaFrameReachability")
    mesh.GetPointsAttr().Set(Vt.Vec3fArray.FromNumpy(vertices))
    mesh.GetFaceVertexCountsAttr().Set(Vt.IntArray([3] * len(faces)))
    mesh.GetFaceVertexIndicesAttr().Set(Vt.IntArray.FromNumpy(faces.reshape(-1)))
    mesh.GetSubdivisionSchemeAttr().Set(UsdGeom.Tokens.none)
    mesh.CreateDoubleSidedAttr(True)
    mesh.CreateDisplayColorAttr().Set(Vt.Vec3fArray([Gf.Vec3f(0.05, 0.75, 1.0)]))
    mesh.CreateDisplayOpacityAttr().Set(Vt.FloatArray([opacity]))
    print(
        "reachability_surface,status=LOADED,frame=tita_base_link,"
        f"evidence={metadata.get('evidence_status', 'UNKNOWN')},"
        f"vertices={len(vertices)},faces={len(faces)},opacity={opacity:.6g}",
        flush=True,
    )


def main() -> int:
    if args_cli.headless and args_cli.max_frames <= 0:
        raise ValueError("headless runs require --max-frames")
    if args_cli.max_frames < 0:
        raise ValueError("--max-frames must be non-negative")
    if not COMBINED_URDF.is_file():
        raise FileNotFoundError(COMBINED_URDF)

    reachability_path = Path(args_cli.reachability_map).expanduser()
    if not reachability_path.is_absolute():
        reachability_path = REPO_ROOT / reachability_path

    sim = SimulationContext(
        sim_utils.SimulationCfg(device=args_cli.device, dt=1.0 / 200.0, render_interval=4)
    )
    sim.set_camera_view((1.25, 1.15, 0.95), (0.0, 0.0, 0.28))
    light_cfg = sim_utils.DomeLightCfg(intensity=2600.0, color=(0.82, 0.82, 0.82))
    light_cfg.func("/World/Light", light_cfg)
    ground_cfg = sim_utils.GroundPlaneCfg(color=(0.16, 0.16, 0.16), size=(4.0, 4.0))
    ground_cfg.func("/World/Ground", ground_cfg, translation=(0.0, 0.0, -0.42))

    combined_cfg = ArticulationCfg(
        prim_path="/World/TitaGluon",
        spawn=sim_utils.UrdfFileCfg(
            asset_path=str(COMBINED_URDF),
            fix_base=True,
            merge_fixed_joints=False,
            replace_cylinders_with_capsules=False,
            collider_type="convex_hull",
            self_collision=False,
            force_usd_conversion=True,
            activate_contact_sensors=False,
            rigid_props=sim_utils.RigidBodyPropertiesCfg(
                disable_gravity=True,
                linear_damping=0.0,
                angular_damping=0.0,
                max_depenetration_velocity=5.0,
            ),
            articulation_props=sim_utils.ArticulationRootPropertiesCfg(
                enabled_self_collisions=False,
                solver_position_iteration_count=8,
                solver_velocity_iteration_count=1,
            ),
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
            joint_pos={**TITA_STAND_Q_RAD, **GLUON_WORK_Q_RAD},
            joint_vel={".*": 0.0},
        ),
        soft_joint_pos_limit_factor=0.95,
        actuators={},
    )
    robot = Articulation(combined_cfg)
    create_reachability_surface(reachability_path.resolve(), args_cli.reachability_opacity)

    sim.reset()
    robot.update(0.0)
    required_joints = set(TITA_STAND_Q_RAD) | set(GLUON_WORK_Q_RAD)
    missing_joints = sorted(required_joints - set(robot.joint_names))
    if missing_joints:
        raise RuntimeError(f"combined articulation is missing joints: {missing_joints}")
    print(
        "TITA_GLUON_REACHABILITY_VIEWER,domain=VALIDATION_SIM,status=PASS,"
        f"joints={len(robot.joint_names)},bodies={len(robot.body_names)},"
        "tita_pose=policy_stand,gluon_pose=WORK,hardware_commands=0",
        flush=True,
    )

    frame_count = 0
    while simulation_app.is_running():
        sim.render()
        frame_count += 1
        if args_cli.max_frames > 0 and frame_count >= args_cli.max_frames:
            break
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    finally:
        simulation_app.close()
