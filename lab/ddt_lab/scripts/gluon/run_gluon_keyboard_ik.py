#!/usr/bin/env python3
"""Interactive base-frame cylindrical control for GLUON using bounded position-only DLS."""

import argparse

from isaaclab.app import AppLauncher


parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument(
    "--max-steps",
    type=int,
    default=0,
    help="Exit after this many physics steps; zero keeps the GUI running.",
)
parser.add_argument(
    "--scripted-target-offset-m",
    type=float,
    nargs=3,
    metavar=("DX", "DY", "DZ"),
    help="Apply one base-frame offset from the startup EE target for headless validation.",
)
parser.add_argument(
    "--scripted-target-position-m",
    type=float,
    nargs=3,
    metavar=("X", "Y", "Z"),
    help="Apply one absolute base-frame target after entering WORK mode.",
)
parser.add_argument(
    "--final-error-limit-m",
    type=float,
    default=None,
    help="Return failure if final Cartesian error exceeds this value.",
)
parser.add_argument(
    "--run-corner-trajectory",
    action="store_true",
    help="Run the closed W2 eight-vertex cylindrical path after entering WORK.",
)
parser.add_argument(
    "--trajectory-speed-m-s",
    type=float,
    default=0.06,
    help="Cylindrical metric speed for the W2 vertex trajectory.",
)
parser.add_argument(
    "--keyboard-speed-m-s",
    type=float,
    default=0.10,
    help="Metric target speed while a cylindrical coordinate key is held.",
)
parser.add_argument(
    "--max-joint-slew-deg-s",
    type=float,
    default=40.0,
    help="Maximum per-joint command slew used by HOME, WORK, and Cartesian IK.",
)
parser.add_argument(
    "--trajectory-corner-tolerance-m",
    type=float,
    default=0.005,
    help="Measured EE tolerance required before advancing to the next corner.",
)
parser.add_argument(
    "--log-segment-dynamics",
    action="store_true",
    help="Aggregate joint, torque, and oscillation diagnostics for each trajectory segment.",
)
parser.add_argument(
    "--status-log-every-controls",
    type=int,
    default=25,
    help="Print the verbose IK status every N control ticks; zero disables it.",
)
parser.add_argument(
    "--reachability-map",
    type=str,
    default=None,
    help=(
        "Optional collision-aware .npz map from "
        "test/analyze_tita_gluon_reachability.py. The shell is transformed "
        "back into this standalone GLUON base frame for display."
    ),
)
parser.add_argument(
    "--reachability-opacity",
    type=float,
    default=0.10,
    help="Display opacity for --reachability-map (0, 1].",
)
AppLauncher.add_app_launcher_args(parser)
args_cli = parser.parse_args()
app_launcher = AppLauncher(args_cli)
simulation_app = app_launcher.app


import json  # noqa: E402
import math  # noqa: E402
import os  # noqa: E402
import sys  # noqa: E402
import traceback  # noqa: E402
from pathlib import Path  # noqa: E402

import numpy as np  # noqa: E402
import torch  # noqa: E402

import isaaclab.sim as sim_utils  # noqa: E402
from isaaclab.assets import Articulation  # noqa: E402
from isaaclab.devices import Se3Keyboard, Se3KeyboardCfg  # noqa: E402
from isaaclab.markers import VisualizationMarkers, VisualizationMarkersCfg  # noqa: E402
from isaaclab.markers.config import FRAME_MARKER_CFG  # noqa: E402
from isaaclab.sim import SimulationContext  # noqa: E402
from isaaclab.utils.math import (  # noqa: E402
    combine_frame_transforms,
    matrix_from_quat,
    subtract_frame_transforms,
)


REPO_ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(REPO_ROOT / "lab" / "ddt_lab"))

from ddt_lab.assets.gluon import (  # noqa: E402
    GLUON_2L6_4L3_CFG,
    GLUON_END_EFFECTOR_BODY,
    GLUON_JOINT_NAMES,
)
from ddt_lab.gluon_ik import (  # noqa: E402
    DEFAULT_CONTROL_DT_S,
    DEFAULT_MAX_TARGET_LEAD_M,
    GLUON_HOME_JOINT_POS_RAD,
    GLUON_WORK_JOINT_POS_RAD,
    WORKSPACE_W2_RADIUS_MAX_M,
    WORKSPACE_W2_RADIUS_MIN_M,
    WORKSPACE_W2_THETA_CENTER_RAD,
    WORKSPACE_W2_THETA_HALF_RANGE_RAD,
    WORKSPACE_W2_X_MAX_M,
    WORKSPACE_W2_X_MIN_M,
    advance_cylindrical_workspace_goal,
    apply_cylindrical_workspace_increment,
    bounded_joint_target_step,
    bounded_position_dls_step,
    cartesian_to_cylindrical_workspace,
    clamp_workspace,
    cylindrical_workspace_to_cartesian,
    limit_target_lead,
    physx_com_jacobian_to_link_position_jacobian_b,
    sample_cylindrical_workspace_path,
    workspace_cylindrical_vertex_loop,
)


PHYSICS_DT_S = 1.0 / 200.0
CONTROL_DECIMATION = 4
JOINT_MODE_TOLERANCE_RAD = math.radians(2.0)
JOINT_MODE_SETTLE_CONTROLS = 25
TRAJECTORY_CORNER_DWELL_CONTROLS = 5


def create_reachability_surface(map_path: Path, opacity: float) -> None:
    """Create a non-colliding USD visualization from an offline map artifact."""
    import omni.usd
    from pxr import Gf, UsdGeom, Vt

    if not 0.0 < opacity <= 1.0:
        raise ValueError("--reachability-opacity must be in (0, 1]")
    if not map_path.is_file():
        raise FileNotFoundError(f"reachability map not found: {map_path}")
    with np.load(map_path, allow_pickle=False) as reachability:
        required = (
            "metadata_json",
            "surface_vertices_gluon_b_m",
            "surface_faces",
        )
        missing = [name for name in required if name not in reachability]
        if missing:
            raise ValueError(f"reachability map is missing arrays: {missing}")
        metadata = json.loads(reachability["metadata_json"].item())
        vertices = np.asarray(
            reachability["surface_vertices_gluon_b_m"], dtype=np.float32
        )
        faces = np.asarray(reachability["surface_faces"], dtype=np.int32)
    if vertices.ndim != 2 or vertices.shape[1] != 3:
        raise ValueError(f"invalid reachability vertices shape: {vertices.shape}")
    if faces.ndim != 2 or faces.shape[1] != 3:
        raise ValueError(f"invalid reachability faces shape: {faces.shape}")

    stage = omni.usd.get_context().get_stage()
    mesh = UsdGeom.Mesh.Define(stage, "/Visuals/TitaGluonReachability")
    mesh.GetPointsAttr().Set(Vt.Vec3fArray.FromNumpy(vertices))
    mesh.GetFaceVertexCountsAttr().Set(Vt.IntArray([3] * len(faces)))
    mesh.GetFaceVertexIndicesAttr().Set(Vt.IntArray.FromNumpy(faces.reshape(-1)))
    mesh.GetSubdivisionSchemeAttr().Set(UsdGeom.Tokens.none)
    mesh.CreateDoubleSidedAttr(True)
    mesh.CreateDisplayColorAttr().Set(Vt.Vec3fArray([Gf.Vec3f(0.05, 0.75, 1.0)]))
    mesh.CreateDisplayOpacityAttr().Set(Vt.FloatArray([opacity]))
    print(
        "reachability_surface,status=LOADED,"
        f"map={map_path},status={metadata.get('evidence_status', 'UNKNOWN')},"
        f"frame=gluon_base_link,vertices={len(vertices)},faces={len(faces)},"
        f"opacity={opacity:.6g}",
        flush=True,
    )


TRAJECTORY_MAX_PLANNER_LEAD_M = 0.008
TRAJECTORY_RADIAL_SPEED_SCALE = 0.5
DIAGNOSTIC_SIGN_FLIP_MIN_RAD_S = 0.05


class TrajectorySegmentDiagnostics:
    """Aggregate control- and physics-rate evidence for one Cartesian segment."""

    def __init__(self, segment_index: int, start_b: torch.Tensor, target_b: torch.Tensor):
        self.segment_index = segment_index
        self.start_b = start_b.detach().clone()
        self.target_b = target_b.detach().clone()
        self.control_samples = 0
        self.physics_samples = 0
        self.min_sigma = float("inf")
        self.max_goal_error_m = 0.0
        self.max_servo_error_m = 0.0
        self.slew_limited_controls = 0
        self.target_lead_limited_controls = 0
        self.max_abs_command_slew_rad_s = torch.zeros_like(start_b.new_zeros(6))
        self.max_abs_joint_position_error_rad = torch.zeros_like(start_b.new_zeros(6))
        self.max_abs_joint_velocity_rad_s = torch.zeros_like(start_b.new_zeros(6))
        self.max_abs_joint_acceleration_rad_s2 = torch.zeros_like(start_b.new_zeros(6))
        self.max_abs_estimated_computed_torque_nm = torch.zeros_like(start_b.new_zeros(6))
        self.max_abs_estimated_applied_torque_nm = torch.zeros_like(start_b.new_zeros(6))
        self.max_estimated_torque_ratio = torch.zeros_like(start_b.new_zeros(6))
        self.torque_clip_counts = torch.zeros(6, dtype=torch.int64, device=start_b.device)
        self.velocity_sign_flip_counts = torch.zeros(
            6, dtype=torch.int64, device=start_b.device
        )
        self.command_sign_flip_counts = torch.zeros(
            6, dtype=torch.int64, device=start_b.device
        )
        self._previous_joint_velocity = None
        self._previous_command_slew = None

    def observe_control(
        self,
        *,
        sigma_min: float,
        goal_error_m: float,
        servo_error_m: float,
        command_before: torch.Tensor,
        command_after: torch.Tensor,
        slew_limited: bool,
        target_lead_limited: bool,
    ) -> None:
        self.control_samples += 1
        self.min_sigma = min(self.min_sigma, sigma_min)
        self.max_goal_error_m = max(self.max_goal_error_m, goal_error_m)
        self.max_servo_error_m = max(self.max_servo_error_m, servo_error_m)
        self.slew_limited_controls += int(slew_limited)
        self.target_lead_limited_controls += int(target_lead_limited)
        command_slew = (command_after - command_before) / DEFAULT_CONTROL_DT_S
        self.max_abs_command_slew_rad_s = torch.maximum(
            self.max_abs_command_slew_rad_s, torch.abs(command_slew)
        )
        if self._previous_command_slew is not None:
            flips = (
                (command_slew * self._previous_command_slew < 0.0)
                & (torch.abs(command_slew) >= DIAGNOSTIC_SIGN_FLIP_MIN_RAD_S)
                & (
                    torch.abs(self._previous_command_slew)
                    >= DIAGNOSTIC_SIGN_FLIP_MIN_RAD_S
                )
            )
            self.command_sign_flip_counts += flips.to(torch.int64)
        self._previous_command_slew = command_slew.detach().clone()

    def observe_physics(
        self,
        *,
        joint_position: torch.Tensor,
        joint_position_target: torch.Tensor,
        joint_velocity: torch.Tensor,
        estimated_computed_torque: torch.Tensor,
        estimated_applied_torque: torch.Tensor,
        effort_limits: torch.Tensor,
    ) -> None:
        self.physics_samples += 1
        position_error = torch.abs(joint_position_target - joint_position)
        abs_velocity = torch.abs(joint_velocity)
        abs_computed_torque = torch.abs(estimated_computed_torque)
        abs_applied_torque = torch.abs(estimated_applied_torque)
        safe_effort_limits = torch.clamp(torch.abs(effort_limits), min=1.0e-9)
        torque_ratio = abs_computed_torque / safe_effort_limits
        self.max_abs_joint_position_error_rad = torch.maximum(
            self.max_abs_joint_position_error_rad, position_error
        )
        self.max_abs_joint_velocity_rad_s = torch.maximum(
            self.max_abs_joint_velocity_rad_s, abs_velocity
        )
        self.max_abs_estimated_computed_torque_nm = torch.maximum(
            self.max_abs_estimated_computed_torque_nm, abs_computed_torque
        )
        self.max_abs_estimated_applied_torque_nm = torch.maximum(
            self.max_abs_estimated_applied_torque_nm, abs_applied_torque
        )
        self.max_estimated_torque_ratio = torch.maximum(
            self.max_estimated_torque_ratio, torque_ratio
        )
        self.torque_clip_counts += (abs_computed_torque > safe_effort_limits).to(
            torch.int64
        )
        if self._previous_joint_velocity is not None:
            acceleration = (
                joint_velocity - self._previous_joint_velocity
            ) / PHYSICS_DT_S
            self.max_abs_joint_acceleration_rad_s2 = torch.maximum(
                self.max_abs_joint_acceleration_rad_s2, torch.abs(acceleration)
            )
            flips = (
                (joint_velocity * self._previous_joint_velocity < 0.0)
                & (abs_velocity >= DIAGNOSTIC_SIGN_FLIP_MIN_RAD_S)
                & (
                    torch.abs(self._previous_joint_velocity)
                    >= DIAGNOSTIC_SIGN_FLIP_MIN_RAD_S
                )
            )
            self.velocity_sign_flip_counts += flips.to(torch.int64)
        self._previous_joint_velocity = joint_velocity.detach().clone()

    @staticmethod
    def _values(tensor: torch.Tensor, precision: int = 6) -> str:
        return "[" + ",".join(f"{value:.{precision}g}" for value in tensor.tolist()) + "]"

    @staticmethod
    def _integer_values(tensor: torch.Tensor) -> str:
        return "[" + ",".join(str(int(value)) for value in tensor.tolist()) + "]"

    def log_line(self) -> str:
        return (
            "trajectory_segment_dynamics,"
            f"segment={self.segment_index},"
            f"start_b={self._values(self.start_b)},target_b={self._values(self.target_b)},"
            f"control_samples={self.control_samples},physics_samples={self.physics_samples},"
            f"min_sigma={self.min_sigma:.9g},max_goal_error_m={self.max_goal_error_m:.9g},"
            f"max_servo_error_m={self.max_servo_error_m:.9g},"
            f"slew_limited_controls={self.slew_limited_controls},"
            f"target_lead_limited_controls={self.target_lead_limited_controls},"
            f"max_abs_command_slew_rad_s={self._values(self.max_abs_command_slew_rad_s)},"
            "max_abs_joint_position_error_rad="
            f"{self._values(self.max_abs_joint_position_error_rad)},"
            f"max_abs_joint_velocity_rad_s={self._values(self.max_abs_joint_velocity_rad_s)},"
            "max_abs_joint_acceleration_rad_s2="
            f"{self._values(self.max_abs_joint_acceleration_rad_s2)},"
            "max_abs_estimated_computed_torque_nm="
            f"{self._values(self.max_abs_estimated_computed_torque_nm)},"
            "max_abs_estimated_applied_torque_nm="
            f"{self._values(self.max_abs_estimated_applied_torque_nm)},"
            f"max_estimated_torque_ratio={self._values(self.max_estimated_torque_ratio)},"
            f"torque_clip_counts={self._integer_values(self.torque_clip_counts)},"
            "velocity_sign_flip_counts="
            f"{self._integer_values(self.velocity_sign_flip_counts)},"
            "command_sign_flip_counts="
            f"{self._integer_values(self.command_sign_flip_counts)}"
        )


class OperatorFlags:
    """Mutable callback state shared with the Omniverse keyboard subscriber."""

    def __init__(self) -> None:
        self.reset_target = False
        self.home_mode = False
        self.work_mode = False
        self.corner_trajectory = False
        self.target_updates_paused = False
        self.exit_requested = False

    def request_reset(self) -> None:
        self.reset_target = True

    def request_home(self) -> None:
        self.home_mode = True

    def request_work(self) -> None:
        self.work_mode = True

    def request_corner_trajectory(self) -> None:
        self.corner_trajectory = True

    def toggle_pause(self) -> None:
        self.target_updates_paused = not self.target_updates_paused

    def request_exit(self) -> None:
        self.exit_requested = True


def create_status_window():
    """Create a small GUI panel without importing omni.ui in headless runs."""
    if args_cli.headless:
        return None, {}
    import omni.ui as ui

    labels = {}
    window = ui.Window("GLUON IK Status", width=680, height=330)
    with window.frame:
        with ui.VStack(spacing=4):
            ui.Label("base_link cylindrical keyboard control")
            for key in (
                "mode",
                "state",
                "frame",
                "workspace",
                "trajectory",
                "goal_cyl",
                "goal",
                "servo_target",
                "current",
                "error",
                "singular",
                "q6",
                "pause",
            ):
                labels[key] = ui.Label(f"{key}: --")
    return window, labels


def update_status_window(labels: dict, values: dict[str, str]) -> None:
    for key, value in values.items():
        if key in labels:
            labels[key].text = f"{key}: {value}"


def main() -> int:
    if args_cli.headless and args_cli.max_steps <= 0:
        raise ValueError("headless runs require --max-steps to prevent an infinite process")
    if args_cli.max_steps < 0:
        raise ValueError("--max-steps must be non-negative")
    if args_cli.final_error_limit_m is not None and args_cli.final_error_limit_m <= 0.0:
        raise ValueError("--final-error-limit-m must be positive")
    if args_cli.trajectory_speed_m_s <= 0.0:
        raise ValueError("--trajectory-speed-m-s must be positive")
    if args_cli.keyboard_speed_m_s <= 0.0:
        raise ValueError("--keyboard-speed-m-s must be positive")
    if args_cli.max_joint_slew_deg_s <= 0.0:
        raise ValueError("--max-joint-slew-deg-s must be positive")
    if args_cli.status_log_every_controls < 0:
        raise ValueError("--status-log-every-controls must be non-negative")
    if args_cli.trajectory_corner_tolerance_m <= 0.0:
        raise ValueError("--trajectory-corner-tolerance-m must be positive")
    if not 0.0 < args_cli.reachability_opacity <= 1.0:
        raise ValueError("--reachability-opacity must be in (0, 1]")
    if (
        args_cli.scripted_target_offset_m is not None
        and args_cli.scripted_target_position_m is not None
    ):
        raise ValueError(
            "--scripted-target-offset-m and --scripted-target-position-m are mutually exclusive"
        )
    if args_cli.run_corner_trajectory and (
        args_cli.scripted_target_offset_m is not None
        or args_cli.scripted_target_position_m is not None
    ):
        raise ValueError("corner trajectory cannot be combined with a scripted target")

    sim_cfg = sim_utils.SimulationCfg(device=args_cli.device, dt=PHYSICS_DT_S, render_interval=4)
    sim = SimulationContext(sim_cfg)
    # The model root applies -90 deg about world Y, so base +X points roughly
    # along world +Z. Aim the camera at the transformed arm volume.
    sim.set_camera_view((1.0, 0.8, 0.85), (-0.08, 0.0, 0.30))

    light_cfg = sim_utils.DomeLightCfg(intensity=2500.0, color=(0.8, 0.8, 0.8))
    light_cfg.func("/World/Light", light_cfg)
    ground_cfg = sim_utils.GroundPlaneCfg(color=(0.18, 0.18, 0.18), size=(4.0, 4.0))
    ground_cfg.func("/World/Ground", ground_cfg, translation=(0.0, 0.0, -0.10))

    robot_cfg = GLUON_2L6_4L3_CFG.copy()
    robot_cfg.prim_path = "/World/Gluon"
    robot = Articulation(robot_cfg)
    if args_cli.reachability_map is not None:
        reachability_path = Path(args_cli.reachability_map).expanduser()
        if not reachability_path.is_absolute():
            reachability_path = REPO_ROOT / reachability_path
        create_reachability_surface(
            reachability_path.resolve(), args_cli.reachability_opacity
        )

    target_marker_cfg = VisualizationMarkersCfg(
        prim_path="/Visuals/GluonTarget",
        markers={
            "accepted": sim_utils.SphereCfg(
                radius=0.012,
                visual_material=sim_utils.PreviewSurfaceCfg(diffuse_color=(0.1, 0.9, 0.2)),
            ),
            "limited": sim_utils.SphereCfg(
                radius=0.014,
                visual_material=sim_utils.PreviewSurfaceCfg(diffuse_color=(1.0, 0.2, 0.05)),
            ),
        },
    )
    target_marker = VisualizationMarkers(target_marker_cfg)
    frame_cfg = FRAME_MARKER_CFG.copy()
    frame_cfg.markers.pop("connecting_line")
    frame_cfg.markers["frame"].scale = (0.05, 0.05, 0.05)
    current_marker = VisualizationMarkers(frame_cfg.replace(prim_path="/Visuals/GluonCurrentEE"))
    trajectory_corner_cfg = VisualizationMarkersCfg(
        prim_path="/Visuals/GluonW2TrajectoryVertices",
        markers={
            "corner": sim_utils.SphereCfg(
                radius=0.006,
                visual_material=sim_utils.PreviewSurfaceCfg(
                    diffuse_color=(1.0, 0.15, 0.65),
                    emissive_color=(0.15, 0.01, 0.06),
                    roughness=0.8,
                ),
            )
        },
    )
    trajectory_corner_marker = VisualizationMarkers(trajectory_corner_cfg)
    trajectory_path_cfg = VisualizationMarkersCfg(
        prim_path="/Visuals/GluonW2TrajectoryPath",
        markers={
            "path": sim_utils.SphereCfg(
                radius=0.0022,
                visual_material=sim_utils.PreviewSurfaceCfg(
                    diffuse_color=(1.0, 0.92, 0.25),
                    emissive_color=(0.10, 0.08, 0.01),
                    roughness=0.9,
                ),
            ),
        },
    )
    trajectory_path_marker = VisualizationMarkers(trajectory_path_cfg)

    sim.reset()
    robot.update(PHYSICS_DT_S)
    if tuple(robot.joint_names) != GLUON_JOINT_NAMES:
        raise RuntimeError(f"joint order mismatch: {robot.joint_names}")
    if not robot.is_fixed_base:
        raise RuntimeError("GLUON keyboard IK requires a fixed-base articulation")

    ee_body_index = robot.body_names.index(GLUON_END_EFFECTOR_BODY)
    ee_jacobian_index = ee_body_index - 1
    jacobian_shape = tuple(robot.root_physx_view.get_jacobians().shape)
    if ee_jacobian_index < 0 or jacobian_shape[1] != len(robot.body_names) - 1:
        raise RuntimeError(
            "fixed-base Jacobian contract failed: "
            f"body_index={ee_body_index},jacobian_index={ee_jacobian_index},"
            f"jacobian_shape={jacobian_shape},body_count={len(robot.body_names)}"
        )
    print(
        "jacobian_contract,status=PASS,"
        f"body={GLUON_END_EFFECTOR_BODY},body_index={ee_body_index},"
        f"jacobian_index={ee_jacobian_index},shape={jacobian_shape}",
        flush=True,
    )

    root_pos_w = robot.data.root_link_pos_w
    root_quat_w = robot.data.root_link_quat_w
    ee_pos_b, _ = subtract_frame_transforms(
        root_pos_w,
        root_quat_w,
        robot.data.body_link_pos_w[:, ee_body_index],
        robot.data.body_link_quat_w[:, ee_body_index],
    )
    # HOME q=0 is intentionally outside W2. Cylindrical clamping starts only
    # after the conditioned WORK posture is reached.
    home_position_b = ee_pos_b[0].clone()
    trajectory_path_cylindrical = workspace_cylindrical_vertex_loop(home_position_b)
    trajectory_path_b = cylindrical_workspace_to_cartesian(
        trajectory_path_cylindrical
    )
    trajectory_corners_b = trajectory_path_b[:-1]
    corner_count = trajectory_corners_b.shape[0]
    corner_root_pos_w = root_pos_w.expand(corner_count, -1)
    corner_root_quat_w = root_quat_w.expand(corner_count, -1)
    trajectory_corners_w, _ = combine_frame_transforms(
        corner_root_pos_w,
        corner_root_quat_w,
        trajectory_corners_b,
        None,
    )
    trajectory_corner_marker.visualize(trajectory_corners_w)
    trajectory_path_samples_cylindrical = sample_cylindrical_workspace_path(
        trajectory_path_cylindrical
    )
    trajectory_path_samples_b = cylindrical_workspace_to_cartesian(
        trajectory_path_samples_cylindrical
    )
    path_sample_count = trajectory_path_samples_b.shape[0]
    path_root_pos_w = root_pos_w.expand(path_sample_count, -1)
    path_root_quat_w = root_quat_w.expand(path_sample_count, -1)
    trajectory_path_samples_w, _ = combine_frame_transforms(
        path_root_pos_w,
        path_root_quat_w,
        trajectory_path_samples_b,
        None,
    )
    trajectory_path_marker.visualize(trajectory_path_samples_w)
    goal_position_b = home_position_b.clone()
    goal_cylindrical = cartesian_to_cylindrical_workspace(goal_position_b)
    scripted_offset = (
        goal_position_b.new_tensor(args_cli.scripted_target_offset_m)
        if args_cli.scripted_target_offset_m is not None
        else None
    )
    scripted_position = (
        goal_position_b.new_tensor(args_cli.scripted_target_position_m)
        if args_cli.scripted_target_position_m is not None
        else None
    )
    scripted_target_pending = scripted_offset is not None or scripted_position is not None

    q_previous_command = robot.data.joint_pos[0].clone()
    q_home = q_previous_command.new_tensor(GLUON_HOME_JOINT_POS_RAD)
    q_work = q_previous_command.new_tensor(GLUON_WORK_JOINT_POS_RAD)
    soft_limits = robot.data.soft_joint_pos_limits[0]
    if bool(torch.any(q_home < soft_limits[:, 0]) or torch.any(q_home > soft_limits[:, 1])):
        raise RuntimeError("HOME joint posture exceeds runtime soft limits")
    if bool(torch.any(q_work < soft_limits[:, 0]) or torch.any(q_work > soft_limits[:, 1])):
        raise RuntimeError("WORK joint posture exceeds runtime soft limits")
    q_nominal = q_work.clone()
    max_joint_slew_rad_s = math.radians(args_cli.max_joint_slew_deg_s)
    control_mode = "MOVE_TO_WORK" if args_cli.headless else "HOME"
    startup_command_delta = float(
        torch.max(torch.abs(q_previous_command - robot.data.joint_pos[0])).item()
    )
    if startup_command_delta != 0.0:
        raise RuntimeError(f"startup command discontinuity: {startup_command_delta}")
    # Populate the implicit-actuator runtime buffers before the first watchdog
    # read. In particular, soft_joint_vel_limits are zero until this write.
    robot.set_joint_position_target(q_previous_command.unsqueeze(0))
    robot.write_data_to_sim()

    flags = OperatorFlags()
    keyboard = None
    if not args_cli.headless:
        keyboard = Se3Keyboard(
            Se3KeyboardCfg(
                sim_device=sim.device,
                pos_sensitivity=args_cli.keyboard_speed_m_s * DEFAULT_CONTROL_DT_S,
                rot_sensitivity=0.0,
                gripper_term=False,
            )
        )
        keyboard.add_callback("R", flags.request_reset)
        keyboard.add_callback("H", flags.request_home)
        keyboard.add_callback("Z", flags.request_work)
        keyboard.add_callback("P", flags.request_corner_trajectory)
        keyboard.add_callback("SPACE", flags.toggle_pause)
        keyboard.add_callback("ESCAPE", flags.request_exit)
        print(keyboard, flush=True)

    status_window, status_labels = create_status_window()
    print(
        "GLUON_KEYBOARD_IK_START,domain=VALIDATION_SIM,physics_hz=200,control_hz=50,"
        "keys=H:HOME,Z:WORK,P:cylindrical_trajectory,"
        "W/S:+/-X,A/D:+/-radius,Q/E:+/-theta_arc,"
        "R:reset,SPACE:pause,ESC:exit,"
        "input_coordinates=base_link_cylindrical_about_plus_x,"
        "base_x_is_world_z=1,base_z_is_world_minus_x=1,"
        f"keyboard_speed_m_s={args_cli.keyboard_speed_m_s:.6g},"
        f"trajectory_speed_m_s={args_cli.trajectory_speed_m_s:.6g},"
        f"max_joint_slew_deg_s={args_cli.max_joint_slew_deg_s:.6g},"
        f"segment_dynamics_log={int(args_cli.log_segment_dynamics)},"
        f"active_workspace=W2,x_m=[{WORKSPACE_W2_X_MIN_M},{WORKSPACE_W2_X_MAX_M}],"
        f"radius_m=[{WORKSPACE_W2_RADIUS_MIN_M},{WORKSPACE_W2_RADIUS_MAX_M}],"
        f"theta_center_deg={math.degrees(WORKSPACE_W2_THETA_CENTER_RAD):.6g},"
        f"theta_half_range_deg={math.degrees(WORKSPACE_W2_THETA_HALF_RANGE_RAD):.6g}",
        flush=True,
    )

    step_count = 0
    control_count = 0
    joint_limit_violations = 0
    velocity_limit_violations = 0
    max_velocity_ratio = 0.0
    max_command_slew_rad_s = 0.0
    max_abs_q6_rad = abs(float(robot.data.joint_pos[0, 5].item()))
    final_error_m = float("inf")
    max_goal_error_m = 0.0
    target_lead_limit_count = 0
    work_mode_entry_count = 0
    work_settle_control_count = 0
    latest_state = control_mode
    trajectory_start_pending = args_cli.run_corner_trajectory
    trajectory_active = False
    trajectory_waypoint_index = 0
    trajectory_corner_dwell_count = 0
    trajectory_reached_count = 0
    trajectory_completed_count = 0
    trajectory_max_accepted_corner_error_m = 0.0
    trajectory_origin_b = None
    trajectory_segment_diagnostics = {}
    active_physics_segment_index = None

    while simulation_app.is_running() and not flags.exit_requested:
        if args_cli.max_steps > 0 and step_count >= args_cli.max_steps:
            break

        if step_count % CONTROL_DECIMATION == 0:
            root_pos_w = robot.data.root_link_pos_w
            root_quat_w = robot.data.root_link_quat_w
            ee_pos_w = robot.data.body_link_pos_w[:, ee_body_index]
            ee_quat_w = robot.data.body_link_quat_w[:, ee_body_index]
            ee_pos_b, _ = subtract_frame_transforms(
                root_pos_w, root_quat_w, ee_pos_w, ee_quat_w
            )

            q_current = robot.data.joint_pos[0]
            actual_velocity = torch.abs(robot.data.joint_vel[0])
            command_before_update = q_previous_command.clone()
            if flags.home_mode:
                previous_mode = control_mode
                control_mode = "HOME"
                trajectory_active = False
                trajectory_start_pending = False
                trajectory_corner_dwell_count = 0
                active_physics_segment_index = None
                goal_position_b = home_position_b.clone()
                goal_cylindrical = cartesian_to_cylindrical_workspace(goal_position_b)
                flags.home_mode = False
                flags.reset_target = False
                print(
                    f"mode_transition,from={previous_mode},to=HOME,trigger=H",
                    flush=True,
                )
            elif flags.work_mode:
                previous_mode = control_mode
                control_mode = "MOVE_TO_WORK"
                trajectory_active = False
                trajectory_start_pending = False
                trajectory_corner_dwell_count = 0
                active_physics_segment_index = None
                goal_position_b = ee_pos_b[0].clone()
                goal_cylindrical = cartesian_to_cylindrical_workspace(goal_position_b)
                flags.work_mode = False
                flags.reset_target = False
                work_settle_control_count = 0
                print(
                    f"mode_transition,from={previous_mode},to=MOVE_TO_WORK,trigger=Z",
                    flush=True,
                )
            if flags.corner_trajectory:
                flags.corner_trajectory = False
                if trajectory_active:
                    trajectory_active = False
                    trajectory_start_pending = False
                    trajectory_corner_dwell_count = 0
                    active_physics_segment_index = None
                    goal_position_b = ee_pos_b[0].clone()
                    goal_cylindrical = cartesian_to_cylindrical_workspace(
                        goal_position_b
                    )
                    print("trajectory_cancel,trigger=P", flush=True)
                elif control_mode == "WORK":
                    trajectory_active = True
                    trajectory_start_pending = False
                    trajectory_waypoint_index = 0
                    trajectory_corner_dwell_count = 0
                    goal_position_b = ee_pos_b[0].clone()
                    goal_cylindrical = cartesian_to_cylindrical_workspace(
                        goal_position_b
                    )
                    trajectory_origin_b = goal_position_b.clone()
                    trajectory_segment_diagnostics.clear()
                    print(
                        f"trajectory_start,trigger=P,waypoints={len(trajectory_path_b)}",
                        flush=True,
                    )
                else:
                    previous_mode = control_mode
                    control_mode = "MOVE_TO_WORK"
                    trajectory_start_pending = True
                    trajectory_corner_dwell_count = 0
                    active_physics_segment_index = None
                    work_settle_control_count = 0
                    goal_position_b = ee_pos_b[0].clone()
                    goal_cylindrical = cartesian_to_cylindrical_workspace(
                        goal_position_b
                    )
                    print(
                        f"mode_transition,from={previous_mode},to=MOVE_TO_WORK,trigger=P",
                        flush=True,
                    )

            diagnostic_segment_index = (
                trajectory_waypoint_index if trajectory_active else None
            )
            jacobian_com_w = robot.root_physx_view.get_jacobians()[
                0, ee_jacobian_index, :, :5
            ]
            rotation_w_b = matrix_from_quat(root_quat_w)
            jacobian_b = physx_com_jacobian_to_link_position_jacobian_b(
                jacobian_com_w=jacobian_com_w,
                com_position_w=robot.data.body_com_pos_w[0, ee_body_index],
                link_position_w=ee_pos_w[0],
                rotation_w_b=rotation_w_b[0],
            )
            sigma_min = float(torch.linalg.svdvals(jacobian_b)[-1].item())
            workspace_clamped = False
            target_lead_limited = False
            joint_clamped = False
            slew_limited = False
            servo_error_m = 0.0
            joint_mode_error_rad = 0.0
            used_cartesian_ik = False
            trajectory_completed_this_tick = False
            radial_only_segment = False

            if control_mode in ("HOME", "MOVE_TO_WORK"):
                target_joint_position = q_home if control_mode == "HOME" else q_work
                q_command, joint_clamped, slew_limited = bounded_joint_target_step(
                    target_joint_position=target_joint_position,
                    q_previous_command=q_previous_command,
                    joint_soft_limits=soft_limits,
                    max_slew_rad_s=max_joint_slew_rad_s,
                )
                joint_mode_error_rad = float(
                    torch.max(torch.abs(target_joint_position - q_current)).item()
                )
                q_previous_command = q_command.clone()
                robot.set_joint_position_target(q_previous_command.unsqueeze(0))
                servo_target_position_b = ee_pos_b[0].clone()
                if control_mode == "HOME":
                    goal_position_b = home_position_b.clone()
                    latest_state = control_mode
                else:
                    goal_position_b = ee_pos_b[0].clone()
                    if (
                        joint_mode_error_rad <= JOINT_MODE_TOLERANCE_RAD
                        and not slew_limited
                    ):
                        work_settle_control_count += 1
                    else:
                        work_settle_control_count = 0
                    if work_settle_control_count >= JOINT_MODE_SETTLE_CONTROLS:
                        control_mode = "WORK"
                        work_mode_entry_count += 1
                        goal_position_b, workspace_clamped = clamp_workspace(
                            ee_pos_b[0].clone()
                        )
                        if workspace_clamped:
                            raise RuntimeError(
                                "WORK posture EE is outside configured workspace: "
                                f"{ee_pos_b[0].tolist()}"
                            )
                        if scripted_target_pending:
                            requested_scripted_target = (
                                scripted_position
                                if scripted_position is not None
                                else goal_position_b + scripted_offset
                            )
                            goal_position_b, workspace_clamped = clamp_workspace(
                                requested_scripted_target
                            )
                            scripted_target_pending = False
                        goal_cylindrical = cartesian_to_cylindrical_workspace(
                            goal_position_b
                        )
                        print(
                            "mode_transition,from=MOVE_TO_WORK,to=WORK,"
                            f"trigger=joint_settled,q_error_rad={joint_mode_error_rad:.6g},"
                            f"settle_controls={work_settle_control_count},"
                            f"goal_b={goal_position_b.tolist()}",
                            flush=True,
                        )
                        if trajectory_start_pending:
                            trajectory_active = True
                            trajectory_start_pending = False
                            trajectory_waypoint_index = 0
                            trajectory_corner_dwell_count = 0
                            trajectory_origin_b = goal_position_b.clone()
                            trajectory_segment_diagnostics.clear()
                            print(
                                "trajectory_start,trigger=work_ready,"
                                f"waypoints={len(trajectory_path_b)},"
                                f"speed_m_s={args_cli.trajectory_speed_m_s:.6g},"
                                f"corner_tolerance_m={args_cli.trajectory_corner_tolerance_m:.6g}",
                                flush=True,
                            )
                        latest_state = "WORK_READY"
                    else:
                        latest_state = control_mode
            else:
                used_cartesian_ik = True
                if flags.reset_target:
                    trajectory_active = False
                    trajectory_start_pending = False
                    trajectory_corner_dwell_count = 0
                    active_physics_segment_index = None
                    goal_position_b, _ = clamp_workspace(ee_pos_b[0].clone())
                    goal_cylindrical = cartesian_to_cylindrical_workspace(
                        goal_position_b
                    )
                    flags.reset_target = False
                elif trajectory_active:
                    if not flags.target_updates_paused:
                        waypoint_b = trajectory_path_b[trajectory_waypoint_index]
                        waypoint_cylindrical = trajectory_path_cylindrical[
                            trajectory_waypoint_index
                        ]
                        planner_lead_m = float(
                            torch.linalg.vector_norm(goal_position_b - ee_pos_b[0]).item()
                        )
                        waypoint_delta_cylindrical = (
                            waypoint_cylindrical - goal_cylindrical
                        )
                        radial_only_segment = bool(
                            torch.abs(waypoint_delta_cylindrical[1]) > 1.0e-5
                            and torch.abs(waypoint_delta_cylindrical[0]) <= 1.0e-5
                            and torch.abs(waypoint_delta_cylindrical[2]) <= 1.0e-5
                        )
                        if planner_lead_m <= TRAJECTORY_MAX_PLANNER_LEAD_M:
                            trajectory_speed_scale = (
                                TRAJECTORY_RADIAL_SPEED_SCALE
                                if radial_only_segment
                                else 1.0
                            )
                            goal_cylindrical, planned_corner_reached = (
                                advance_cylindrical_workspace_goal(
                                    goal_cylindrical,
                                    waypoint_cylindrical,
                                    args_cli.trajectory_speed_m_s
                                    * trajectory_speed_scale
                                    * DEFAULT_CONTROL_DT_S,
                                )
                            )
                            goal_position_b = cylindrical_workspace_to_cartesian(
                                goal_cylindrical
                            )
                        else:
                            planned_corner_reached = bool(
                                torch.equal(goal_cylindrical, waypoint_cylindrical)
                            )
                        measured_corner_error_m = float(
                            torch.linalg.vector_norm(waypoint_b - ee_pos_b[0]).item()
                        )
                        if (
                            planned_corner_reached
                            and measured_corner_error_m
                            <= args_cli.trajectory_corner_tolerance_m
                        ):
                            trajectory_corner_dwell_count += 1
                        else:
                            trajectory_corner_dwell_count = 0
                        if trajectory_corner_dwell_count >= TRAJECTORY_CORNER_DWELL_CONTROLS:
                            trajectory_reached_count += 1
                            trajectory_max_accepted_corner_error_m = max(
                                trajectory_max_accepted_corner_error_m,
                                measured_corner_error_m,
                            )
                            print(
                                "trajectory_corner_reached,"
                                f"index={trajectory_waypoint_index},"
                                f"count={len(trajectory_path_b)},"
                                f"target_b={waypoint_b.tolist()},"
                                f"error_m={measured_corner_error_m:.9g},"
                                f"sigma_min={sigma_min:.9g}",
                                flush=True,
                            )
                            trajectory_waypoint_index += 1
                            trajectory_corner_dwell_count = 0
                            if trajectory_waypoint_index >= len(trajectory_path_b):
                                trajectory_active = False
                                trajectory_completed_count += 1
                                trajectory_completed_this_tick = True
                                print(
                                "trajectory_complete,"
                                    f"completed_count={trajectory_completed_count},"
                                    f"reached_count={trajectory_reached_count},"
                                    "unique_vertices=8,"
                                    f"max_accepted_corner_error_m="
                                    f"{trajectory_max_accepted_corner_error_m:.9g}",
                                    flush=True,
                                )
                elif keyboard is not None and not flags.target_updates_paused:
                    requested_cylindrical = apply_cylindrical_workspace_increment(
                        goal_cylindrical, keyboard.advance()[:3]
                    )
                    requested_goal = cylindrical_workspace_to_cartesian(
                        requested_cylindrical
                    )
                    # A held key cannot outrun the slew-limited arm.  This is
                    # a teleoperation reference, not a queued long move.
                    goal_position_b, _ = limit_target_lead(
                        requested_goal,
                        ee_pos_b[0],
                        DEFAULT_MAX_TARGET_LEAD_M,
                    )
                    goal_cylindrical = cartesian_to_cylindrical_workspace(
                        goal_position_b
                    )

                goal_position_b, workspace_clamped = clamp_workspace(goal_position_b)
                goal_cylindrical = cartesian_to_cylindrical_workspace(
                    goal_position_b
                )
                servo_target_position_b, target_lead_limited = limit_target_lead(
                    goal_position_b,
                    ee_pos_b[0],
                    DEFAULT_MAX_TARGET_LEAD_M,
                )
                target_lead_limit_count += int(target_lead_limited)
                result = bounded_position_dls_step(
                    jacobian_position_b=jacobian_b,
                    q_current=q_current,
                    q_previous_command=q_previous_command,
                    q_nominal=q_nominal,
                    current_position_b=ee_pos_b[0],
                    target_position_b=servo_target_position_b,
                    joint_soft_limits=soft_limits,
                    max_slew_rad_s=max_joint_slew_rad_s,
                )
                servo_target_position_b = result.target_clamped
                servo_error_m = result.position_error_norm_m
                joint_clamped = result.joint_limit_clamped
                slew_limited = result.slew_limited
                q_previous_command = result.q_command.clone()
                robot.set_joint_position_target(q_previous_command.unsqueeze(0))

            command_slew = float(
                torch.max(torch.abs(q_previous_command - command_before_update)).item()
                / DEFAULT_CONTROL_DT_S
            )
            max_command_slew_rad_s = max(max_command_slew_rad_s, command_slew)

            lower = robot.data.soft_joint_pos_limits[0, :, 0]
            upper = robot.data.soft_joint_pos_limits[0, :, 1]
            joint_limit_violations += int(
                bool(torch.any(q_previous_command < lower - 1.0e-6))
                or bool(torch.any(q_previous_command > upper + 1.0e-6))
            )
            velocity_limits = robot.data.soft_joint_vel_limits[0]
            velocity_ratio = actual_velocity / torch.clamp(velocity_limits, min=1.0e-9)
            max_velocity_ratio = max(max_velocity_ratio, float(torch.max(velocity_ratio).item()))
            velocity_over = actual_velocity > velocity_limits + 1.0e-5
            if bool(torch.any(velocity_over)):
                velocity_limit_violations += 1
                print(
                    f"velocity_watchdog,actual_rad_s={actual_velocity.tolist()},"
                    f"limits_rad_s={velocity_limits.tolist()},ratio={velocity_ratio.tolist()}",
                    flush=True,
                )
            max_abs_q6_rad = max(max_abs_q6_rad, abs(float(q_current[5].item())))
            goal_error_m = float(
                torch.linalg.vector_norm(goal_position_b - ee_pos_b[0]).item()
            )
            final_error_m = goal_error_m
            max_goal_error_m = max(max_goal_error_m, goal_error_m)
            if used_cartesian_ik:
                if trajectory_completed_this_tick:
                    latest_state = "TRAJECTORY_COMPLETE"
                elif trajectory_active:
                    latest_state = f"TRAJECTORY_{result.state}"
                else:
                    latest_state = "HOLD" if goal_error_m <= 0.001 else result.state

            if args_cli.log_segment_dynamics and diagnostic_segment_index is not None:
                if trajectory_origin_b is None:
                    raise RuntimeError("trajectory diagnostics missing trajectory origin")
                segment_diagnostics = trajectory_segment_diagnostics.get(
                    diagnostic_segment_index
                )
                if segment_diagnostics is None:
                    segment_start_b = (
                        trajectory_origin_b
                        if diagnostic_segment_index == 0
                        else trajectory_path_b[diagnostic_segment_index - 1]
                    )
                    segment_diagnostics = TrajectorySegmentDiagnostics(
                        diagnostic_segment_index,
                        segment_start_b,
                        trajectory_path_b[diagnostic_segment_index],
                    )
                    trajectory_segment_diagnostics[
                        diagnostic_segment_index
                    ] = segment_diagnostics
                segment_diagnostics.observe_control(
                    sigma_min=sigma_min,
                    goal_error_m=goal_error_m,
                    servo_error_m=servo_error_m,
                    command_before=command_before_update,
                    command_after=q_previous_command,
                    slew_limited=slew_limited,
                    target_lead_limited=target_lead_limited,
                )
                active_physics_segment_index = diagnostic_segment_index

            goal_pos_w, _ = combine_frame_transforms(
                root_pos_w, root_quat_w, goal_position_b.unsqueeze(0), None
            )
            limited = workspace_clamped or latest_state in ("SATURATED", "UNREACHABLE")
            target_marker.visualize(goal_pos_w, marker_indices=[1 if limited else 0])
            current_marker.visualize(ee_pos_w, ee_quat_w)

            status_values = {
                "mode": control_mode,
                "state": latest_state,
                "frame": "base_link (+X=world +Z, +Y=world +Y, +Z=world -X)",
                "workspace": (
                    f"W2 X=[{WORKSPACE_W2_X_MIN_M:.2f},{WORKSPACE_W2_X_MAX_M:.2f}] m, "
                    f"r=[{WORKSPACE_W2_RADIUS_MIN_M:.2f},{WORKSPACE_W2_RADIUS_MAX_M:.2f}] m, "
                    f"theta={math.degrees(WORKSPACE_W2_THETA_CENTER_RAD):.0f}"
                    f"+/-{math.degrees(WORKSPACE_W2_THETA_HALF_RANGE_RAD):.0f} deg"
                ),
                "trajectory": (
                    f"active={trajectory_active},waypoint="
                    f"{min(trajectory_waypoint_index + 1, len(trajectory_path_b))}/"
                    f"{len(trajectory_path_b)},completed={trajectory_completed_count}"
                ),
                "goal_cyl": (
                    f"X={float(goal_cylindrical[0]):.4f} m, "
                    f"r={float(goal_cylindrical[1]):.4f} m, "
                    f"theta_offset={math.degrees(float(goal_cylindrical[2])):.2f} deg"
                ),
                "goal": "[" + ", ".join(f"{v:.4f}" for v in goal_position_b.tolist()) + "] m",
                "servo_target": "["
                + ", ".join(f"{v:.4f}" for v in servo_target_position_b.tolist())
                + "] m",
                "current": "[" + ", ".join(f"{v:.4f}" for v in ee_pos_b[0].tolist()) + "] m",
                "error": (
                    f"joint={math.degrees(joint_mode_error_rad):.2f} deg"
                    if control_mode in ("HOME", "MOVE_TO_WORK")
                    else f"goal={goal_error_m * 1000.0:.2f} mm"
                ),
                "singular": f"sigma_min={sigma_min:.3e}",
                "q6": f"{math.degrees(float(q_current[5].item())):.3f} deg",
                "pause": str(flags.target_updates_paused),
            }
            update_status_window(status_labels, status_values)
            if (
                args_cli.status_log_every_controls > 0
                and control_count % args_cli.status_log_every_controls == 0
            ):
                print(
                    f"ik,mode={control_mode},state={latest_state},"
                    f"goal_b={goal_position_b.tolist()},"
                    f"goal_cylindrical={goal_cylindrical.tolist()},"
                    f"servo_target_b={servo_target_position_b.tolist()},"
                    f"current_b={ee_pos_b[0].tolist()},goal_error_m={goal_error_m:.6g},"
                    f"servo_error_m={servo_error_m:.6g},"
                    f"joint_mode_error_rad={joint_mode_error_rad:.6g},"
                    f"sigma_min={sigma_min:.6g},"
                    f"workspace_clamped={int(workspace_clamped)},"
                    f"target_lead_limited={int(target_lead_limited)},"
                    f"joint_clamped={int(joint_clamped)},"
                    f"slew_limited={int(slew_limited)},"
                    f"trajectory_active={int(trajectory_active)},"
                    f"trajectory_waypoint_index={trajectory_waypoint_index},"
                    f"q6_rad={float(q_current[5].item()):.6g},"
                    f"q={q_current.tolist()},q_command={q_previous_command.tolist()}",
                    flush=True,
                )
            control_count += 1

        robot.write_data_to_sim()
        sim.step(render=not args_cli.headless)
        robot.update(PHYSICS_DT_S)
        if (
            args_cli.log_segment_dynamics
            and active_physics_segment_index is not None
            and active_physics_segment_index in trajectory_segment_diagnostics
        ):
            trajectory_segment_diagnostics[
                active_physics_segment_index
            ].observe_physics(
                joint_position=robot.data.joint_pos[0],
                joint_position_target=q_previous_command,
                joint_velocity=robot.data.joint_vel[0],
                estimated_computed_torque=robot.data.computed_torque[0],
                estimated_applied_torque=robot.data.applied_torque[0],
                effort_limits=robot.data.joint_effort_limits[0],
            )
        step_count += 1
        if args_cli.run_corner_trajectory and trajectory_completed_count > 0:
            break

    del status_window
    if args_cli.log_segment_dynamics:
        ordered_segment_diagnostics = [
            trajectory_segment_diagnostics[index]
            for index in sorted(trajectory_segment_diagnostics)
        ]
        for segment_diagnostics in ordered_segment_diagnostics:
            print(segment_diagnostics.log_line(), flush=True)
        if ordered_segment_diagnostics:
            min_sigma_segment = min(
                ordered_segment_diagnostics, key=lambda item: item.min_sigma
            )
            max_acceleration_segment = max(
                ordered_segment_diagnostics,
                key=lambda item: float(
                    torch.max(item.max_abs_joint_acceleration_rad_s2).item()
                ),
            )
            max_acceleration_value, max_acceleration_joint = torch.max(
                max_acceleration_segment.max_abs_joint_acceleration_rad_s2, dim=0
            )
            max_torque_ratio_segment = max(
                ordered_segment_diagnostics,
                key=lambda item: float(torch.max(item.max_estimated_torque_ratio).item()),
            )
            max_torque_ratio_value, max_torque_ratio_joint = torch.max(
                max_torque_ratio_segment.max_estimated_torque_ratio, dim=0
            )
            most_velocity_flips_segment = max(
                ordered_segment_diagnostics,
                key=lambda item: int(torch.sum(item.velocity_sign_flip_counts).item()),
            )
            print(
                "trajectory_dynamics_extrema,"
                f"min_sigma_segment={min_sigma_segment.segment_index},"
                f"min_sigma={min_sigma_segment.min_sigma:.9g},"
                f"max_acceleration_segment={max_acceleration_segment.segment_index},"
                f"max_acceleration_joint={int(max_acceleration_joint.item()) + 1},"
                f"max_acceleration_rad_s2={float(max_acceleration_value.item()):.9g},"
                f"max_torque_ratio_segment={max_torque_ratio_segment.segment_index},"
                f"max_torque_ratio_joint={int(max_torque_ratio_joint.item()) + 1},"
                f"max_estimated_torque_ratio={float(max_torque_ratio_value.item()):.9g},"
                "most_velocity_flips_segment="
                f"{most_velocity_flips_segment.segment_index},"
                "most_velocity_flips_total="
                f"{int(torch.sum(most_velocity_flips_segment.velocity_sign_flip_counts).item())}",
                flush=True,
            )
    summary = (
        f"summary,mode={control_mode},state={latest_state},steps={step_count},"
        f"controls={control_count},work_mode_entry_count={work_mode_entry_count},"
        f"final_error_m={final_error_m:.9g},joint_limit_violations={joint_limit_violations},"
        f"velocity_limit_violations={velocity_limit_violations},"
        f"max_velocity_ratio={max_velocity_ratio:.9g},"
        f"max_command_slew_rad_s={max_command_slew_rad_s:.9g},"
        f"configured_max_joint_slew_rad_s={max_joint_slew_rad_s:.9g},"
        f"max_goal_error_m={max_goal_error_m:.9g},"
        f"target_lead_limit_count={target_lead_limit_count},"
        f"trajectory_reached_count={trajectory_reached_count},"
        f"trajectory_completed_count={trajectory_completed_count},"
        f"trajectory_max_accepted_corner_error_m="
        f"{trajectory_max_accepted_corner_error_m:.9g},"
        f"max_abs_q6_deg={math.degrees(max_abs_q6_rad):.9g},"
        f"startup_command_delta_rad={startup_command_delta:.9g}"
    )
    print(summary, flush=True)

    failures = []
    if joint_limit_violations:
        failures.append("joint soft-limit violation")
    if velocity_limit_violations:
        failures.append("runtime joint velocity-limit violation")
    if max_command_slew_rad_s > max_joint_slew_rad_s + 1.0e-5:
        failures.append("command slew violation")
    if max_abs_q6_rad > math.radians(0.5):
        failures.append("q6 hold violation")
    if args_cli.headless and work_mode_entry_count == 0:
        failures.append("headless run did not reach WORK mode")
    if args_cli.run_corner_trajectory:
        if trajectory_completed_count == 0:
            failures.append("corner trajectory did not complete")
        if trajectory_reached_count != len(trajectory_path_b):
            failures.append(
                f"corner trajectory reached {trajectory_reached_count}/"
                f"{len(trajectory_path_b)} waypoints"
            )
        if (
            trajectory_max_accepted_corner_error_m
            > args_cli.trajectory_corner_tolerance_m
        ):
            failures.append("corner trajectory tolerance violation")
    if not math.isfinite(final_error_m):
        failures.append("non-finite Cartesian error")
    if args_cli.final_error_limit_m is not None and final_error_m > args_cli.final_error_limit_m:
        failures.append(
            f"final error {final_error_m:.6g} m exceeds {args_cli.final_error_limit_m:.6g} m"
        )
    if failures:
        print("GLUON_KEYBOARD_IK: FAIL", flush=True)
        for failure in failures:
            print(f"- {failure}", flush=True)
        return 1
    print("GLUON_KEYBOARD_IK: PASS", flush=True)
    return 0


if __name__ == "__main__":
    try:
        exit_code = main()
    except KeyboardInterrupt:
        print("GLUON_KEYBOARD_IK: INTERRUPTED", flush=True)
        exit_code = 130
    except Exception:
        traceback.print_exc()
        exit_code = 1
    if exit_code != 0:
        # Isaac Sim's fast-close path exits with status zero and can mask a
        # pending SystemExit. A failing validation must remain observable by
        # shell/CI, so let the OS reclaim simulator resources on this path.
        sys.stdout.flush()
        sys.stderr.flush()
        os._exit(exit_code)
    simulation_app.close(skip_cleanup=True)
