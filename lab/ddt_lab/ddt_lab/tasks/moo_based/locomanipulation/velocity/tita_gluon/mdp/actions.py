"""Action terms owned by the TITA+GLUON locomanipulation task."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import MISSING
import math
import xml.etree.ElementTree as ET

import torch

import isaaclab.sim as sim_utils
from isaaclab.assets import Articulation
from isaaclab.managers import ActionTerm, ActionTermCfg
from isaaclab.markers import VisualizationMarkers
from isaaclab.markers.config import VisualizationMarkersCfg
from isaaclab.utils import configclass
from isaaclab.utils.math import (
    quat_apply,
    quat_apply_inverse,
    quat_conjugate,
    quat_from_matrix,
    quat_mul,
)

from ..sequential_inspection import ArmOption, ExecutorEvent, ExecutorState, build_option_mask


QUINTIC_MAX_DPHASE = 1.875
QUINTIC_MAX_D2PHASE = 10.0 / math.sqrt(3.0)


def quintic_smoothstep(phase: torch.Tensor) -> torch.Tensor:
    """Return a zero-velocity, zero-acceleration interpolation factor."""
    phase = torch.clamp(phase, 0.0, 1.0)
    return phase**3 * (10.0 + phase * (-15.0 + 6.0 * phase))


def minimum_quintic_duration(
    joint_delta: torch.Tensor,
    max_velocity_rad_s: float,
    max_acceleration_rad_s2: float,
) -> torch.Tensor:
    """Return the minimum segment duration satisfying quintic qd/qdd limits."""
    if joint_delta.ndim < 1:
        raise ValueError("joint_delta must have at least one dimension")
    if max_velocity_rad_s <= 0.0 or not math.isfinite(max_velocity_rad_s):
        raise ValueError("max_velocity_rad_s must be finite and positive")
    if max_acceleration_rad_s2 <= 0.0 or not math.isfinite(max_acceleration_rad_s2):
        raise ValueError("max_acceleration_rad_s2 must be finite and positive")
    largest_delta = torch.amax(torch.abs(joint_delta), dim=-1)
    velocity_duration = QUINTIC_MAX_DPHASE * largest_delta / max_velocity_rad_s
    acceleration_duration = torch.sqrt(
        QUINTIC_MAX_D2PHASE * largest_delta / max_acceleration_rad_s2
    )
    return torch.maximum(velocity_duration, acceleration_duration)


class FixedJointPositionAction(ActionTerm):
    """Apply a fixed joint-position target without consuming policy actions.

    The term deliberately has zero action dimensions.  It therefore keeps the
    low-level TITA policy at eight actions while applying the GLUON PD target at
    every physics step through the same action-manager boundary.
    """

    cfg: FixedJointPositionActionCfg

    def __init__(self, cfg: FixedJointPositionActionCfg, env):
        super().__init__(cfg, env)
        if not isinstance(self._asset, Articulation):
            raise TypeError("FixedJointPositionAction requires an Articulation asset")

        self._joint_ids, self._joint_names = self._asset.find_joints(
            cfg.joint_names, preserve_order=cfg.preserve_order
        )
        if len(self._joint_ids) != len(cfg.target_joint_pos):
            raise ValueError(
                "target_joint_pos must contain one value per selected joint: "
                f"received {len(cfg.target_joint_pos)} values for {len(self._joint_ids)} joints"
            )

        target = torch.tensor(cfg.target_joint_pos, dtype=torch.float32, device=self.device)
        self._target_joint_pos = target.unsqueeze(0).repeat(self.num_envs, 1)
        self._raw_actions = torch.empty((self.num_envs, 0), device=self.device)
        self._apply_target()

    @property
    def action_dim(self) -> int:
        return 0

    @property
    def raw_actions(self) -> torch.Tensor:
        return self._raw_actions

    @property
    def processed_actions(self) -> torch.Tensor:
        return self._target_joint_pos

    @property
    def joint_names(self) -> list[str]:
        return self._joint_names

    def process_actions(self, actions: torch.Tensor):
        if actions.shape != self._raw_actions.shape:
            raise ValueError(
                f"Expected zero-width fixed-target actions with shape {self._raw_actions.shape}, "
                f"received {actions.shape}"
            )

    def apply_actions(self):
        self._apply_target()

    def reset(self, env_ids: Sequence[int] | None = None) -> None:
        self._apply_target(env_ids)

    def _apply_target(self, env_ids: Sequence[int] | None = None) -> None:
        if env_ids is None:
            target = self._target_joint_pos
        else:
            target = self._target_joint_pos[env_ids]
        self._asset.set_joint_position_target(target, joint_ids=self._joint_ids, env_ids=env_ids)


@configclass
class FixedJointPositionActionCfg(ActionTermCfg):
    """Configuration for :class:`FixedJointPositionAction`."""

    class_type: type[ActionTerm] = FixedJointPositionAction
    joint_names: list[str] = MISSING
    target_joint_pos: tuple[float, ...] = MISSING
    preserve_order: bool = True


class SmoothRandomJointPositionAction(ActionTerm):
    """Move through a conditioned waypoint set without policy action dimensions.

    Every environment independently alternates between the configured center
    posture and a randomly selected waypoint.  Each segment follows a quintic
    joint-space interpolation, whose duration is increased when necessary to
    satisfy configured velocity and acceleration limits.  Returning through
    the center prevents unvalidated direct waypoint-to-waypoint connections.
    """

    cfg: SmoothRandomJointPositionActionCfg

    def __init__(self, cfg: SmoothRandomJointPositionActionCfg, env):
        super().__init__(cfg, env)
        if not isinstance(self._asset, Articulation):
            raise TypeError("SmoothRandomJointPositionAction requires an Articulation asset")

        self._joint_ids, self._joint_names = self._asset.find_joints(
            cfg.joint_names, preserve_order=cfg.preserve_order
        )
        self._kinematic_chain = self._load_kinematic_chain(
            cfg.kinematic_urdf_path, cfg.end_effector_link_name
        )
        joint_count = len(self._joint_ids)
        if len(cfg.center_joint_pos) != joint_count:
            raise ValueError(
                "center_joint_pos must contain one value per selected joint: "
                f"received {len(cfg.center_joint_pos)} values for {joint_count} joints"
            )
        if not cfg.waypoint_joint_pos:
            raise ValueError("waypoint_joint_pos must contain at least one waypoint")
        if any(len(waypoint) != joint_count for waypoint in cfg.waypoint_joint_pos):
            raise ValueError("every waypoint must contain one value per selected joint")
        self._validate_range(cfg.segment_duration_range_s, "segment_duration_range_s", positive=True)
        self._validate_range(cfg.dwell_time_range_s, "dwell_time_range_s", positive=False)
        if cfg.max_velocity_rad_s <= 0.0 or not math.isfinite(cfg.max_velocity_rad_s):
            raise ValueError("max_velocity_rad_s must be finite and positive")
        if cfg.max_acceleration_rad_s2 <= 0.0 or not math.isfinite(cfg.max_acceleration_rad_s2):
            raise ValueError("max_acceleration_rad_s2 must be finite and positive")
        if not math.isfinite(cfg.initial_workspace_scale) or not 0.0 <= cfg.initial_workspace_scale <= 1.0:
            raise ValueError("initial_workspace_scale must be finite and within [0, 1]")

        self._center_joint_pos = torch.tensor(
            cfg.center_joint_pos, dtype=torch.float32, device=self.device
        )
        self._waypoint_joint_pos = torch.tensor(
            cfg.waypoint_joint_pos, dtype=torch.float32, device=self.device
        )
        self._workspace_scale = float(cfg.initial_workspace_scale)
        configured_targets = torch.cat(
            (self._center_joint_pos.unsqueeze(0), self._waypoint_joint_pos), dim=0
        )
        if not bool(torch.isfinite(configured_targets).all()):
            raise ValueError("center and waypoint targets must be finite")
        soft_limits = self._asset.data.soft_joint_pos_limits[0, self._joint_ids]
        outside_limits = torch.logical_or(
            configured_targets < soft_limits[:, 0], configured_targets > soft_limits[:, 1]
        )
        if bool(torch.any(outside_limits)):
            target_index, joint_index = torch.nonzero(outside_limits, as_tuple=False)[0].tolist()
            target_name = "center" if target_index == 0 else f"waypoint[{target_index - 1}]"
            raise ValueError(
                f"{target_name} joint {self._joint_names[joint_index]} is outside runtime soft limits"
            )

        self._raw_actions = torch.empty((self.num_envs, 0), device=self.device)
        self._target_joint_pos = self._center_joint_pos.unsqueeze(0).repeat(self.num_envs, 1)
        self._segment_start = self._target_joint_pos.clone()
        self._segment_goal = self._target_joint_pos.clone()
        self._segment_elapsed_s = torch.zeros(self.num_envs, device=self.device)
        self._segment_duration_s = torch.ones(self.num_envs, device=self.device)
        self._dwell_remaining_s = torch.zeros(self.num_envs, device=self.device)
        self._is_moving = torch.zeros(self.num_envs, dtype=torch.bool, device=self.device)
        self._at_center = torch.ones(self.num_envs, dtype=torch.bool, device=self.device)
        self._destination_is_center = torch.ones(
            self.num_envs, dtype=torch.bool, device=self.device
        )
        self._waypoint_indices = torch.full(
            (self.num_envs,), -1, dtype=torch.long, device=self.device
        )
        self._completed_segment_count = torch.zeros(
            self.num_envs, dtype=torch.long, device=self.device
        )
        self.reset()

    @staticmethod
    def _validate_range(
        value_range: tuple[float, float], name: str, *, positive: bool
    ) -> None:
        if len(value_range) != 2:
            raise ValueError(f"{name} must have exactly two values")
        lower, upper = value_range
        minimum = 0.0 if not positive else torch.finfo(torch.float32).eps
        if not math.isfinite(lower) or not math.isfinite(upper):
            raise ValueError(f"{name} values must be finite")
        if lower < minimum or upper < lower:
            comparator = "positive" if positive else "non-negative"
            raise ValueError(f"{name} must be ordered and {comparator}")

    @property
    def action_dim(self) -> int:
        return 0

    @property
    def raw_actions(self) -> torch.Tensor:
        return self._raw_actions

    @property
    def processed_actions(self) -> torch.Tensor:
        return self._target_joint_pos

    @property
    def joint_names(self) -> list[str]:
        return self._joint_names

    @property
    def completed_segment_count(self) -> torch.Tensor:
        return self._completed_segment_count

    @property
    def waypoint_indices(self) -> torch.Tensor:
        return self._waypoint_indices

    @property
    def workspace_scale(self) -> float:
        """Fraction of every validated WORK-to-waypoint ray currently enabled."""
        return self._workspace_scale

    @property
    def segment_goal_ee_pos_b(self) -> torch.Tensor:
        """Final link6 position of each active segment in the robot base frame."""
        return self._forward_end_effector(self._segment_goal)

    def set_workspace_scale(self, scale: float) -> None:
        """Set the global conditioned-workspace fraction for future segments."""
        scale = float(scale)
        if not math.isfinite(scale) or not 0.0 <= scale <= 1.0:
            raise ValueError("workspace scale must be finite and within [0, 1]")
        self._workspace_scale = scale

    def process_actions(self, actions: torch.Tensor) -> None:
        if actions.shape != self._raw_actions.shape:
            raise ValueError(
                "Expected zero-width random-trajectory actions with shape "
                f"{self._raw_actions.shape}, received {actions.shape}"
            )

    def apply_actions(self) -> None:
        self._advance_trajectory()
        self._asset.set_joint_position_target(
            self._target_joint_pos, joint_ids=self._joint_ids
        )

    def reset(self, env_ids: Sequence[int] | None = None) -> None:
        env_ids_tensor = self._resolve_env_ids(env_ids)
        self._target_joint_pos[env_ids_tensor] = self._center_joint_pos
        self._segment_start[env_ids_tensor] = self._center_joint_pos
        self._segment_goal[env_ids_tensor] = self._center_joint_pos
        self._segment_elapsed_s[env_ids_tensor] = 0.0
        self._segment_duration_s[env_ids_tensor] = 1.0
        self._is_moving[env_ids_tensor] = False
        self._at_center[env_ids_tensor] = True
        self._destination_is_center[env_ids_tensor] = True
        self._waypoint_indices[env_ids_tensor] = -1
        self._completed_segment_count[env_ids_tensor] = 0
        self._dwell_remaining_s[env_ids_tensor] = self._sample_uniform(
            self.cfg.dwell_time_range_s, len(env_ids_tensor)
        )
        self._asset.set_joint_position_target(
            self._target_joint_pos[env_ids_tensor],
            joint_ids=self._joint_ids,
            env_ids=env_ids_tensor,
        )

    def _resolve_env_ids(self, env_ids: Sequence[int] | None) -> torch.Tensor:
        if env_ids is None:
            return torch.arange(self.num_envs, device=self.device, dtype=torch.long)
        if isinstance(env_ids, slice):
            return torch.arange(self.num_envs, device=self.device, dtype=torch.long)[env_ids]
        return torch.as_tensor(env_ids, device=self.device, dtype=torch.long).reshape(-1)

    def _sample_uniform(self, value_range: tuple[float, float], count: int) -> torch.Tensor:
        lower, upper = value_range
        if upper == lower:
            return torch.full((count,), lower, device=self.device)
        return lower + (upper - lower) * torch.rand(count, device=self.device)

    def _advance_trajectory(self) -> None:
        dt = self._env.sim.get_physics_dt()
        moving_at_start = self._is_moving.clone()
        moving_ids = torch.nonzero(moving_at_start, as_tuple=False).squeeze(-1)
        if len(moving_ids) > 0:
            self._segment_elapsed_s[moving_ids] += dt
            phase = torch.clamp(
                self._segment_elapsed_s[moving_ids] / self._segment_duration_s[moving_ids],
                0.0,
                1.0,
            )
            blend = quintic_smoothstep(phase).unsqueeze(-1)
            self._target_joint_pos[moving_ids] = self._segment_start[moving_ids] + blend * (
                self._segment_goal[moving_ids] - self._segment_start[moving_ids]
            )
            completed = phase >= 1.0
            completed_ids = moving_ids[completed]
            if len(completed_ids) > 0:
                self._target_joint_pos[completed_ids] = self._segment_goal[completed_ids]
                self._is_moving[completed_ids] = False
                self._at_center[completed_ids] = self._destination_is_center[completed_ids]
                self._completed_segment_count[completed_ids] += 1
                self._dwell_remaining_s[completed_ids] = self._sample_uniform(
                    self.cfg.dwell_time_range_s, len(completed_ids)
                )

        stationary_ids = torch.nonzero(~moving_at_start, as_tuple=False).squeeze(-1)
        if len(stationary_ids) > 0:
            self._dwell_remaining_s[stationary_ids] -= dt
            ready_ids = stationary_ids[self._dwell_remaining_s[stationary_ids] <= 0.0]
            if len(ready_ids) > 0:
                self._start_segments(ready_ids)

    def _start_segments(self, env_ids: torch.Tensor) -> None:
        # Difficulty zero is the fixed-arm first curriculum stage.  Avoid
        # generating degenerate WORK-to-WORK segments and simply keep holding.
        if self._workspace_scale == 0.0:
            self._target_joint_pos[env_ids] = self._center_joint_pos
            self._segment_start[env_ids] = self._center_joint_pos
            self._segment_goal[env_ids] = self._center_joint_pos
            self._is_moving[env_ids] = False
            self._at_center[env_ids] = True
            self._destination_is_center[env_ids] = True
            self._dwell_remaining_s[env_ids] = self._sample_uniform(
                self.cfg.dwell_time_range_s, len(env_ids)
            )
            return

        self._segment_start[env_ids] = self._target_joint_pos[env_ids]
        from_center = self._at_center[env_ids]
        waypoint_env_ids = env_ids[from_center]
        return_env_ids = env_ids[~from_center]

        if len(waypoint_env_ids) > 0:
            waypoint_indices = torch.randint(
                len(self._waypoint_joint_pos),
                (len(waypoint_env_ids),),
                device=self.device,
            )
            self._waypoint_indices[waypoint_env_ids] = waypoint_indices
            full_waypoints = self._waypoint_joint_pos[waypoint_indices]
            self._segment_goal[waypoint_env_ids] = self._center_joint_pos + self._workspace_scale * (
                full_waypoints - self._center_joint_pos
            )
            self._destination_is_center[waypoint_env_ids] = False
        if len(return_env_ids) > 0:
            self._segment_goal[return_env_ids] = self._center_joint_pos
            self._destination_is_center[return_env_ids] = True

        joint_delta = self._segment_goal[env_ids] - self._segment_start[env_ids]
        nominal_duration = self._sample_uniform(
            self.cfg.segment_duration_range_s, len(env_ids)
        )
        required_duration = minimum_quintic_duration(
            joint_delta,
            self.cfg.max_velocity_rad_s,
            self.cfg.max_acceleration_rad_s2,
        )
        self._segment_duration_s[env_ids] = torch.maximum(
            nominal_duration, required_duration
        )
        self._segment_elapsed_s[env_ids] = 0.0
        self._is_moving[env_ids] = True

    def _load_kinematic_chain(
        self, urdf_path: str, end_effector_link_name: str
    ) -> tuple[dict[str, object], ...]:
        """Load the URDF chain from its root link to the configured EE link."""
        root = ET.parse(urdf_path).getroot()
        joints_by_child = {
            joint.find("child").attrib["link"]: joint
            for joint in root.findall("joint")
        }
        chain_xml = []
        child_link = end_effector_link_name
        while child_link in joints_by_child:
            joint = joints_by_child[child_link]
            chain_xml.append(joint)
            child_link = joint.find("parent").attrib["link"]
        if not chain_xml:
            raise ValueError(
                f"No URDF kinematic chain ends at link {end_effector_link_name!r}"
            )
        chain_xml.reverse()

        selected_indices = {name: index for index, name in enumerate(self._joint_names)}
        found_selected = set()
        chain = []
        for joint in chain_xml:
            joint_name = joint.attrib["name"]
            joint_type = joint.attrib.get("type", "fixed")
            if joint_type not in ("fixed", "revolute", "continuous"):
                raise ValueError(
                    f"Unsupported {joint_type!r} joint {joint_name!r} in EE kinematic chain"
                )
            origin = joint.find("origin")
            xyz = self._parse_urdf_vector(origin, "xyz", (0.0, 0.0, 0.0))
            rpy = self._parse_urdf_vector(origin, "rpy", (0.0, 0.0, 0.0))
            q_index = selected_indices.get(joint_name)
            if joint_type != "fixed" and q_index is None:
                raise ValueError(
                    f"Movable URDF chain joint {joint_name!r} is not selected by the action term"
                )
            if q_index is not None:
                found_selected.add(joint_name)
            axis_element = joint.find("axis")
            axis = self._parse_urdf_vector(axis_element, "xyz", (1.0, 0.0, 0.0))
            axis_norm = torch.linalg.vector_norm(axis)
            if joint_type != "fixed" and float(axis_norm) <= 0.0:
                raise ValueError(f"URDF joint {joint_name!r} has a zero rotation axis")
            if float(axis_norm) > 0.0:
                axis = axis / axis_norm
            chain.append(
                {
                    "name": joint_name,
                    "xyz": xyz,
                    "rotation": self._rpy_rotation_matrix(rpy),
                    "axis": axis,
                    "q_index": q_index,
                }
            )
        missing = set(self._joint_names) - found_selected
        if missing:
            raise ValueError(
                "Selected joints are not on the configured EE chain: "
                + ", ".join(sorted(missing))
            )
        return tuple(chain)

    def _parse_urdf_vector(
        self,
        element: ET.Element | None,
        attribute: str,
        default: tuple[float, float, float],
    ) -> torch.Tensor:
        values = default if element is None else tuple(
            float(value) for value in element.attrib.get(attribute, " ".join(map(str, default))).split()
        )
        if len(values) != 3:
            raise ValueError(f"URDF {attribute} must contain three values, got {values}")
        return torch.tensor(values, dtype=torch.float32, device=self.device)

    @staticmethod
    def _rpy_rotation_matrix(rpy: torch.Tensor) -> torch.Tensor:
        """Return a URDF fixed-axis roll-pitch-yaw rotation matrix."""
        roll, pitch, yaw = rpy.unbind()
        sr, cr = torch.sin(roll), torch.cos(roll)
        sp, cp = torch.sin(pitch), torch.cos(pitch)
        sy, cy = torch.sin(yaw), torch.cos(yaw)
        return torch.stack(
            (
                torch.stack((cy * cp, cy * sp * sr - sy * cr, cy * sp * cr + sy * sr)),
                torch.stack((sy * cp, sy * sp * sr + cy * cr, sy * sp * cr - cy * sr)),
                torch.stack((-sp, cp * sr, cp * cr)),
            )
        )

    @staticmethod
    def _axis_angle_rotation(axis: torch.Tensor, angle: torch.Tensor) -> torch.Tensor:
        """Return batched Rodrigues rotation matrices for one normalized axis."""
        x, y, z = axis.unbind()
        zero = torch.zeros((), device=axis.device, dtype=axis.dtype)
        skew = torch.stack(
            (
                torch.stack((zero, -z, y)),
                torch.stack((z, zero, -x)),
                torch.stack((-y, x, zero)),
            )
        )
        outer = axis.unsqueeze(1) * axis.unsqueeze(0)
        identity = torch.eye(3, device=axis.device, dtype=axis.dtype)
        cosine = torch.cos(angle).reshape(-1, 1, 1)
        sine = torch.sin(angle).reshape(-1, 1, 1)
        return cosine * identity + sine * skew + (1.0 - cosine) * outer

    def _forward_end_effector(self, joint_pos: torch.Tensor) -> torch.Tensor:
        """Compute the configured EE link origin in the articulation root frame."""
        batch_size = joint_pos.shape[0]
        rotation = torch.eye(3, device=self.device).unsqueeze(0).repeat(batch_size, 1, 1)
        position = torch.zeros((batch_size, 3), device=self.device)
        for joint in self._kinematic_chain:
            xyz = joint["xyz"].expand(batch_size, -1)
            position += torch.bmm(rotation, xyz.unsqueeze(-1)).squeeze(-1)
            fixed_rotation = joint["rotation"].expand(batch_size, -1, -1)
            rotation = torch.bmm(rotation, fixed_rotation)
            q_index = joint["q_index"]
            if q_index is not None:
                rotation = torch.bmm(
                    rotation,
                    self._axis_angle_rotation(joint["axis"], joint_pos[:, q_index]),
                )
        return position

    def _forward_end_effector_pose_jacobian(
        self, joint_pos: torch.Tensor
    ) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        """Return EE position, rotation, and geometric Jacobian in root frame."""
        batch_size = joint_pos.shape[0]
        joint_count = joint_pos.shape[1]
        rotation = torch.eye(3, device=self.device).unsqueeze(0).repeat(batch_size, 1, 1)
        position = torch.zeros((batch_size, 3), device=self.device)
        joint_origins = torch.zeros((batch_size, joint_count, 3), device=self.device)
        joint_axes = torch.zeros_like(joint_origins)
        for joint in self._kinematic_chain:
            xyz = joint["xyz"].expand(batch_size, -1)
            position += torch.bmm(rotation, xyz.unsqueeze(-1)).squeeze(-1)
            fixed_rotation = joint["rotation"].expand(batch_size, -1, -1)
            rotation = torch.bmm(rotation, fixed_rotation)
            q_index = joint["q_index"]
            if q_index is not None:
                joint_origins[:, q_index] = position
                joint_axes[:, q_index] = torch.bmm(
                    rotation, joint["axis"].expand(batch_size, -1).unsqueeze(-1)
                ).squeeze(-1)
                rotation = torch.bmm(
                    rotation,
                    self._axis_angle_rotation(joint["axis"], joint_pos[:, q_index]),
                )
        linear = torch.linalg.cross(
            joint_axes,
            position.unsqueeze(1) - joint_origins,
            dim=-1,
        ).transpose(1, 2)
        angular = joint_axes.transpose(1, 2)
        return position, rotation, torch.cat((linear, angular), dim=1)

    def _set_debug_vis_impl(self, debug_vis: bool) -> None:
        if debug_vis and not hasattr(self, "_ee_goal_visualizer"):
            marker_cfg = VisualizationMarkersCfg(
                prim_path="/Visuals/TitaGluon/segment_goal_link6",
                markers={
                    "goal": sim_utils.SphereCfg(
                        radius=0.035,
                        visual_material=sim_utils.PreviewSurfaceCfg(
                            diffuse_color=(1.0, 0.15, 0.8)
                        ),
                    )
                },
            )
            self._ee_goal_visualizer = VisualizationMarkers(marker_cfg)
        if hasattr(self, "_ee_goal_visualizer"):
            self._ee_goal_visualizer.set_visibility(debug_vis)

    def _debug_vis_callback(self, event) -> None:
        if not hasattr(self, "_ee_goal_visualizer") or not hasattr(self, "_kinematic_chain"):
            return
        goal_pos_b = self.segment_goal_ee_pos_b
        goal_pos_w = self._asset.data.root_link_pos_w + quat_apply(
            self._asset.data.root_link_quat_w, goal_pos_b
        )
        self._ee_goal_visualizer.visualize(translations=goal_pos_w)


@configclass
class SmoothRandomJointPositionActionCfg(ActionTermCfg):
    """Configuration for conditioned smooth random joint trajectories."""

    class_type: type[ActionTerm] = SmoothRandomJointPositionAction
    joint_names: list[str] = MISSING
    center_joint_pos: tuple[float, ...] = MISSING
    waypoint_joint_pos: tuple[tuple[float, ...], ...] = MISSING
    segment_duration_range_s: tuple[float, float] = (2.5, 4.0)
    dwell_time_range_s: tuple[float, float] = (0.25, 0.75)
    max_velocity_rad_s: float = math.radians(20.0)
    max_acceleration_rad_s2: float = math.radians(40.0)
    initial_workspace_scale: float = 1.0
    preserve_order: bool = True
    kinematic_urdf_path: str = MISSING
    end_effector_link_name: str = MISSING


class SequentialInspectionJointPositionAction(SmoothRandomJointPositionAction):
    """Persistent graph/local-servo executor that consumes no low-level actions.

    High-level wrappers call :meth:`request_options` explicitly. Graph motion
    returns through the configured center and uses only configured center-to-hub
    rays. Local motion updates the world target in the articulation root frame
    and applies damped position-plus-facing differential IK without rebuilding
    a complete path. Rotation about the inspection axis is intentionally free.

    The local AABB is a candidate runtime gate until its bounds are produced by
    the offline mesh-validation job. No collision guarantee is made here.
    """

    cfg: SequentialInspectionJointPositionActionCfg

    def __init__(self, cfg: SequentialInspectionJointPositionActionCfg, env):
        # SmoothRandomJointPositionAction supplies URDF FK, checked hub data,
        # joint buffers, and quintic helpers. Its init invokes reset once, so
        # this subclass reset delegates until the executor buffers exist.
        super().__init__(cfg, env)
        self._executor_state = torch.full(
            (self.num_envs,), int(ExecutorState.IDLE), dtype=torch.long, device=self.device
        )
        self._active_option = torch.full(
            (self.num_envs,), int(ArmOption.HOLD), dtype=torch.long, device=self.device
        )
        self._current_target_index = torch.zeros(
            self.num_envs, dtype=torch.long, device=self.device
        )
        self._prepared_target_index = torch.full(
            (self.num_envs,), -1, dtype=torch.long, device=self.device
        )
        self._prepared_hub_index = torch.full(
            (self.num_envs,), -1, dtype=torch.long, device=self.device
        )
        self._at_stow = torch.ones(self.num_envs, dtype=torch.bool, device=self.device)
        self._graph_phase = torch.full(
            (self.num_envs,), -1, dtype=torch.long, device=self.device
        )
        self._graph_destination_hub = torch.full(
            (self.num_envs,), -1, dtype=torch.long, device=self.device
        )
        self._dwell_elapsed_s = torch.zeros(self.num_envs, device=self.device)
        self._option_progress = torch.zeros(self.num_envs, device=self.device)
        self._position_error_norm_m = torch.zeros(self.num_envs, device=self.device)
        self._orientation_error_norm_rad = torch.zeros(self.num_envs, device=self.device)
        self._joint_limit_margin_rad = torch.zeros(self.num_envs, device=self.device)
        self._last_event = torch.full(
            (self.num_envs,), int(ExecutorEvent.NONE), dtype=torch.long, device=self.device
        )
        self._target_sequence_valid = torch.zeros(
            self.num_envs, dtype=torch.bool, device=self.device
        )
        self._target_position_w = torch.zeros(
            (self.num_envs, cfg.target_count, 3), device=self.device
        )
        self._target_quat_w = torch.zeros(
            (self.num_envs, cfg.target_count, 4), device=self.device
        )
        self._target_quat_w[..., 0] = 1.0
        self._target_hub_indices = torch.zeros(
            (self.num_envs, cfg.target_count), dtype=torch.long, device=self.device
        )
        hub_pos, hub_rot, _ = self._forward_end_effector_pose_jacobian(
            self._waypoint_joint_pos
        )
        self._hub_ee_pos_b = hub_pos
        self._hub_ee_quat_b = quat_from_matrix(hub_rot)
        self._soft_limits = self._asset.data.soft_joint_pos_limits[0, self._joint_ids]
        self.reset()

    @property
    def executor_state(self) -> torch.Tensor:
        return self._executor_state

    @property
    def active_option(self) -> torch.Tensor:
        return self._active_option

    @property
    def current_target_index(self) -> torch.Tensor:
        return self._current_target_index

    @property
    def prepared_target_index(self) -> torch.Tensor:
        return self._prepared_target_index

    @property
    def option_progress(self) -> torch.Tensor:
        return self._option_progress

    @property
    def position_error_norm_m(self) -> torch.Tensor:
        return self._position_error_norm_m

    @property
    def orientation_error_norm_rad(self) -> torch.Tensor:
        return self._orientation_error_norm_rad

    @property
    def joint_limit_margin_rad(self) -> torch.Tensor:
        return self._joint_limit_margin_rad

    @property
    def last_event(self) -> torch.Tensor:
        return self._last_event

    @property
    def at_stow(self) -> torch.Tensor:
        return self._at_stow

    @property
    def task_complete(self) -> torch.Tensor:
        return self._current_target_index >= self.cfg.target_count

    @property
    def hub_ee_pos_b(self) -> torch.Tensor:
        return self._hub_ee_pos_b

    @property
    def hub_ee_quat_b(self) -> torch.Tensor:
        return self._hub_ee_quat_b

    @property
    def current_target_pos_w(self) -> torch.Tensor:
        indices = torch.clamp(self._current_target_index, max=self.cfg.target_count - 1)
        return self._target_position_w[torch.arange(self.num_envs, device=self.device), indices]

    @property
    def current_target_quat_w(self) -> torch.Tensor:
        indices = torch.clamp(self._current_target_index, max=self.cfg.target_count - 1)
        return self._target_quat_w[torch.arange(self.num_envs, device=self.device), indices]

    @property
    def local_region_valid(self) -> torch.Tensor:
        return self._local_region_valid(self.cfg.local_region_half_extent_m)

    def _local_region_valid(
        self, half_extent_m: tuple[float, float, float]
    ) -> torch.Tensor:
        valid = self._target_sequence_valid & ~self.task_complete
        if not bool(torch.any(valid)):
            return valid
        target_pos_b = quat_apply_inverse(
            self._asset.data.root_link_quat_w,
            self.current_target_pos_w - self._asset.data.root_link_pos_w,
        )
        target_indices = torch.clamp(self._current_target_index, max=self.cfg.target_count - 1)
        hub_indices = self._target_hub_indices[
            torch.arange(self.num_envs, device=self.device), target_indices
        ]
        hub_pos = self._hub_ee_pos_b[hub_indices]
        half_extent = target_pos_b.new_tensor(half_extent_m)
        return valid & torch.all(torch.abs(target_pos_b - hub_pos) <= half_extent, dim=-1)

    def option_mask(self, validated_stow_path: torch.Tensor | None = None) -> torch.Tensor:
        if validated_stow_path is None:
            validated_stow_path = torch.ones(
                self.num_envs, dtype=torch.bool, device=self.device
            )
        return build_option_mask(
            self._executor_state,
            self._current_target_index,
            self._prepared_target_index,
            self.cfg.target_count,
            self.local_region_valid,
            validated_stow_path,
        )

    def set_target_sequence(
        self,
        target_position_w: torch.Tensor,
        target_quat_w: torch.Tensor,
        target_hub_indices: torch.Tensor,
        env_ids: Sequence[int] | None = None,
    ) -> None:
        env_ids_tensor = self._resolve_env_ids(env_ids)
        expected_pos = (len(env_ids_tensor), self.cfg.target_count, 3)
        expected_quat = (len(env_ids_tensor), self.cfg.target_count, 4)
        expected_hubs = (len(env_ids_tensor), self.cfg.target_count)
        if target_position_w.shape != expected_pos:
            raise ValueError(f"target_position_w must have shape {expected_pos}")
        if target_quat_w.shape != expected_quat:
            raise ValueError(f"target_quat_w must have shape {expected_quat}")
        if target_hub_indices.shape != expected_hubs:
            raise ValueError(f"target_hub_indices must have shape {expected_hubs}")
        if not bool(torch.isfinite(target_position_w).all() and torch.isfinite(target_quat_w).all()):
            raise ValueError("target sequence contains NaN or Inf")
        if bool(
            torch.any(
                (target_hub_indices < 0)
                | (target_hub_indices >= len(self._waypoint_joint_pos))
            )
        ):
            raise ValueError("target hub index is outside the configured hub set")
        quat_norm = torch.linalg.vector_norm(target_quat_w, dim=-1, keepdim=True)
        if bool(torch.any(quat_norm < 1.0e-6)):
            raise ValueError("target quaternion has near-zero norm")
        self._target_position_w[env_ids_tensor] = target_position_w
        self._target_quat_w[env_ids_tensor] = target_quat_w / quat_norm
        self._target_hub_indices[env_ids_tensor] = target_hub_indices.long()
        self._target_sequence_valid[env_ids_tensor] = True

    def begin_bootstrap(self, env_ids: Sequence[int] | None = None) -> torch.Tensor:
        env_ids_tensor = self._resolve_env_ids(env_ids)
        eligible = (
            self._target_sequence_valid[env_ids_tensor]
            & (self._executor_state[env_ids_tensor] == int(ExecutorState.IDLE))
            & (self._current_target_index[env_ids_tensor] == 0)
        )
        accepted_ids = env_ids_tensor[eligible]
        if len(accepted_ids) > 0:
            hubs = self._target_hub_indices[accepted_ids, 0]
            self._active_option[accepted_ids] = int(ArmOption.PREPARE_NEXT)
            self._start_graph(accepted_ids, hubs)
            self._last_event[accepted_ids] = int(ExecutorEvent.OPTION_ACCEPTED)
        return accepted_ids

    def reselect_current_target_hubs(
        self,
        env_ids: Sequence[int] | None = None,
        candidate_hub_indices: torch.Tensor | None = None,
    ) -> torch.Tensor:
        """Select the nearest base-frame graph hub for each current target.

        Reselection is admitted only while the executor is idle at STOW, so
        the subsequent route is one of the stored WORK-to-node graph edges.
        The method changes routing metadata only; it never commands motion.
        """
        env_ids_tensor = self._resolve_env_ids(env_ids)
        current = self._current_target_index[env_ids_tensor]
        eligible = (
            self._target_sequence_valid[env_ids_tensor]
            & (self._executor_state[env_ids_tensor] == int(ExecutorState.IDLE))
            & self._at_stow[env_ids_tensor]
            & (current < self.cfg.target_count)
        )
        selected_env_ids = env_ids_tensor[eligible]
        if len(selected_env_ids) == 0:
            return torch.empty(0, dtype=torch.long, device=self.device)
        if candidate_hub_indices is None:
            candidates = torch.arange(
                len(self._waypoint_joint_pos), dtype=torch.long, device=self.device
            )
        else:
            candidates = candidate_hub_indices.to(device=self.device, dtype=torch.long)
            if candidates.ndim != 1 or len(candidates) == 0:
                raise ValueError("candidate_hub_indices must be a non-empty vector")
            if bool(torch.any((candidates < 0) | (candidates >= len(self._waypoint_joint_pos)))):
                raise ValueError("candidate hub index is outside the graph catalog")
        selected_targets = self._current_target_index[selected_env_ids]
        target_pos_b = quat_apply_inverse(
            self._asset.data.root_link_quat_w[selected_env_ids],
            self._target_position_w[selected_env_ids, selected_targets]
            - self._asset.data.root_link_pos_w[selected_env_ids],
        )
        candidate_positions = self._hub_ee_pos_b[candidates]
        distance = torch.linalg.vector_norm(
            target_pos_b[:, None, :] - candidate_positions[None, :, :], dim=-1
        )
        chosen = candidates[torch.argmin(distance, dim=-1)]
        self._target_hub_indices[selected_env_ids, selected_targets] = chosen
        return chosen

    def request_options(
        self,
        options: torch.Tensor,
        validated_stow_path: torch.Tensor | None = None,
    ) -> torch.Tensor:
        if options.shape != (self.num_envs,):
            raise ValueError(f"options must have shape ({self.num_envs},)")
        options = options.long()
        if bool(torch.any((options < 0) | (options >= len(ArmOption)))):
            raise ValueError("arm option index is outside [0, 3]")
        mask = self.option_mask(validated_stow_path)
        accepted = mask[torch.arange(self.num_envs, device=self.device), options]
        self._last_event[:] = int(ExecutorEvent.OPTION_REJECTED)
        self._last_event[accepted] = int(ExecutorEvent.OPTION_ACCEPTED)

        stow_ids = torch.nonzero(
            accepted & (options == int(ArmOption.STOW)), as_tuple=False
        ).squeeze(-1)
        if len(stow_ids) > 0:
            self._active_option[stow_ids] = int(ArmOption.STOW)
            self._start_graph(
                stow_ids, torch.full_like(stow_ids, -1, dtype=torch.long)
            )
        prepare_ids = torch.nonzero(
            accepted & (options == int(ArmOption.PREPARE_NEXT)), as_tuple=False
        ).squeeze(-1)
        if len(prepare_ids) > 0:
            target_indices = self._current_target_index[prepare_ids]
            hubs = self._target_hub_indices[prepare_ids, target_indices]
            self._active_option[prepare_ids] = int(ArmOption.PREPARE_NEXT)
            self._start_graph(prepare_ids, hubs)
        execute_ids = torch.nonzero(
            accepted & (options == int(ArmOption.EXECUTE_CURRENT)), as_tuple=False
        ).squeeze(-1)
        if len(execute_ids) > 0:
            self._active_option[execute_ids] = int(ArmOption.EXECUTE_CURRENT)
            self._executor_state[execute_ids] = int(ExecutorState.LOCAL_TARGET_SERVO)
            self._dwell_elapsed_s[execute_ids] = 0.0
            self._option_progress[execute_ids] = 0.0
        return accepted

    def trigger_emergency_hold(
        self, env_ids: Sequence[int] | None = None, *, local_region_exit: bool = False
    ) -> None:
        env_ids_tensor = self._resolve_env_ids(env_ids)
        measured = self._asset.data.joint_pos[env_ids_tensor][:, self._joint_ids]
        self._target_joint_pos[env_ids_tensor] = measured
        self._executor_state[env_ids_tensor] = int(ExecutorState.EMERGENCY_HOLD)
        self._active_option[env_ids_tensor] = int(ArmOption.HOLD)
        self._is_moving[env_ids_tensor] = False
        self._last_event[env_ids_tensor] = int(
            ExecutorEvent.LOCAL_REGION_EXIT if local_region_exit else ExecutorEvent.SAFETY_ABORT
        )

    def apply_actions(self) -> None:
        self._advance_option_executor()
        self._asset.set_joint_position_target(
            self._target_joint_pos, joint_ids=self._joint_ids
        )

    def reset(self, env_ids: Sequence[int] | None = None) -> None:
        if not hasattr(self, "_executor_state"):
            super().reset(env_ids)
            return
        env_ids_tensor = self._resolve_env_ids(env_ids)
        self._target_joint_pos[env_ids_tensor] = self._center_joint_pos
        self._segment_start[env_ids_tensor] = self._center_joint_pos
        self._segment_goal[env_ids_tensor] = self._center_joint_pos
        self._segment_elapsed_s[env_ids_tensor] = 0.0
        self._segment_duration_s[env_ids_tensor] = 1.0
        self._is_moving[env_ids_tensor] = False
        self._executor_state[env_ids_tensor] = int(ExecutorState.IDLE)
        self._active_option[env_ids_tensor] = int(ArmOption.HOLD)
        self._current_target_index[env_ids_tensor] = 0
        self._prepared_target_index[env_ids_tensor] = -1
        self._prepared_hub_index[env_ids_tensor] = -1
        self._at_stow[env_ids_tensor] = True
        self._graph_phase[env_ids_tensor] = -1
        self._graph_destination_hub[env_ids_tensor] = -1
        self._dwell_elapsed_s[env_ids_tensor] = 0.0
        self._option_progress[env_ids_tensor] = 0.0
        self._position_error_norm_m[env_ids_tensor] = 0.0
        self._orientation_error_norm_rad[env_ids_tensor] = 0.0
        self._joint_limit_margin_rad[env_ids_tensor] = 0.0
        self._last_event[env_ids_tensor] = int(ExecutorEvent.NONE)
        self._target_sequence_valid[env_ids_tensor] = False
        self._asset.set_joint_position_target(
            self._target_joint_pos[env_ids_tensor],
            joint_ids=self._joint_ids,
            env_ids=env_ids_tensor,
        )

    def _start_graph(self, env_ids: torch.Tensor, destination_hubs: torch.Tensor) -> None:
        self._executor_state[env_ids] = int(ExecutorState.GRAPH_EXECUTION)
        self._graph_destination_hub[env_ids] = destination_hubs
        self._option_progress[env_ids] = 0.0
        has_previous_hub = self._prepared_hub_index[env_ids] >= 0
        return_ids = env_ids[has_previous_hub]
        center_ids = env_ids[~has_previous_hub]
        if len(return_ids) > 0:
            goals = self._waypoint_joint_pos[self._prepared_hub_index[return_ids]]
            self._begin_graph_segment(return_ids, goals, phase=0)
        if len(center_ids) > 0:
            goals = self._center_joint_pos.unsqueeze(0).expand(len(center_ids), -1)
            self._begin_graph_segment(center_ids, goals, phase=1)

    def _begin_graph_segment(
        self, env_ids: torch.Tensor, goals: torch.Tensor, *, phase: int
    ) -> None:
        measured = self._asset.data.joint_pos[env_ids][:, self._joint_ids]
        self._segment_start[env_ids] = measured
        self._target_joint_pos[env_ids] = measured
        self._segment_goal[env_ids] = goals
        required = minimum_quintic_duration(
            goals - measured,
            self.cfg.max_velocity_rad_s,
            self.cfg.max_acceleration_rad_s2,
        )
        nominal = self._sample_uniform(self.cfg.segment_duration_range_s, len(env_ids))
        self._segment_duration_s[env_ids] = torch.maximum(required, nominal)
        self._segment_elapsed_s[env_ids] = 0.0
        self._is_moving[env_ids] = True
        self._graph_phase[env_ids] = phase

    def _advance_option_executor(self) -> None:
        dt = self._env.sim.get_physics_dt()
        graph_ids = torch.nonzero(
            self._executor_state == int(ExecutorState.GRAPH_EXECUTION), as_tuple=False
        ).squeeze(-1)
        if len(graph_ids) > 0:
            self._advance_graph(graph_ids, dt)
        local_ids = torch.nonzero(
            (self._executor_state == int(ExecutorState.LOCAL_TARGET_SERVO))
            | (self._executor_state == int(ExecutorState.DWELL)),
            as_tuple=False,
        ).squeeze(-1)
        if len(local_ids) > 0:
            self._advance_local_servo(local_ids, dt)

    def _advance_graph(self, env_ids: torch.Tensor, dt: float) -> None:
        self._segment_elapsed_s[env_ids] += dt
        phase = torch.clamp(
            self._segment_elapsed_s[env_ids] / self._segment_duration_s[env_ids],
            0.0,
            1.0,
        )
        blend = quintic_smoothstep(phase).unsqueeze(-1)
        self._target_joint_pos[env_ids] = self._segment_start[env_ids] + blend * (
            self._segment_goal[env_ids] - self._segment_start[env_ids]
        )
        self._option_progress[env_ids] = phase
        completed_ids = env_ids[phase >= 1.0]
        if len(completed_ids) == 0:
            return
        self._target_joint_pos[completed_ids] = self._segment_goal[completed_ids]
        self._is_moving[completed_ids] = False
        # Snapshot the completed phase before starting any successor segment.
        # _begin_graph_segment mutates _graph_phase; reading that live tensor
        # again in this loop would make a newly-created phase 1/2 segment look
        # completed in the same physics tick and skip its actual trajectory.
        completed_phases = self._graph_phase[completed_ids].clone()
        for graph_phase in (0, 1, 2):
            phase_ids = completed_ids[completed_phases == graph_phase]
            if len(phase_ids) == 0:
                continue
            if graph_phase == 0:
                goals = self._center_joint_pos.unsqueeze(0).expand(len(phase_ids), -1)
                self._begin_graph_segment(phase_ids, goals, phase=1)
            elif graph_phase == 1:
                destination = self._graph_destination_hub[phase_ids]
                to_hub = destination >= 0
                hub_ids = phase_ids[to_hub]
                stow_ids = phase_ids[~to_hub]
                if len(hub_ids) > 0:
                    goals = self._waypoint_joint_pos[destination[to_hub]]
                    self._begin_graph_segment(hub_ids, goals, phase=2)
                if len(stow_ids) > 0:
                    self._finish_graph(stow_ids, at_stow=True)
            else:
                self._finish_graph(phase_ids, at_stow=False)

    def _finish_graph(self, env_ids: torch.Tensor, *, at_stow: bool) -> None:
        self._executor_state[env_ids] = int(ExecutorState.IDLE)
        self._active_option[env_ids] = int(ArmOption.HOLD)
        self._graph_phase[env_ids] = -1
        self._option_progress[env_ids] = 1.0
        self._at_stow[env_ids] = at_stow
        if at_stow:
            self._prepared_target_index[env_ids] = -1
            self._prepared_hub_index[env_ids] = -1
        else:
            self._prepared_target_index[env_ids] = self._current_target_index[env_ids]
            self._prepared_hub_index[env_ids] = self._graph_destination_hub[env_ids]

    def _advance_local_servo(self, env_ids: torch.Tensor, dt: float) -> None:
        exit_half_extent = tuple(
            extent + self.cfg.local_region_exit_margin_m
            for extent in self.cfg.local_region_half_extent_m
        )
        valid = self._local_region_valid(exit_half_extent)[env_ids]
        invalid_ids = env_ids[~valid]
        if len(invalid_ids) > 0:
            self.trigger_emergency_hold(invalid_ids, local_region_exit=True)
        env_ids = env_ids[valid]
        if len(env_ids) == 0:
            return

        q_current = self._asset.data.joint_pos[env_ids][:, self._joint_ids]
        ee_pos_b, ee_rot_b, jacobian = self._forward_end_effector_pose_jacobian(q_current)
        root_pos_w = self._asset.data.root_link_pos_w[env_ids]
        root_quat_w = self._asset.data.root_link_quat_w[env_ids]
        target_pos_b = quat_apply_inverse(
            root_quat_w, self.current_target_pos_w[env_ids] - root_pos_w
        )
        target_quat_b = quat_mul(
            quat_conjugate(root_quat_w), self.current_target_quat_w[env_ids]
        )
        position_error = target_pos_b - ee_pos_b
        inspection_axis = target_pos_b.new_tensor((0.0, 0.0, 1.0)).expand(
            len(env_ids), -1
        )
        target_facing_b = quat_apply(target_quat_b, inspection_axis)
        ee_facing_b = ee_rot_b[:, :, 2]
        facing_error = torch.linalg.cross(ee_facing_b, target_facing_b, dim=-1)
        facing_cosine = torch.clamp(
            torch.sum(ee_facing_b * target_facing_b, dim=-1), -1.0, 1.0
        )
        facing_error_angle = torch.acos(facing_cosine)
        self._position_error_norm_m[env_ids] = torch.linalg.vector_norm(
            position_error, dim=-1
        )
        self._orientation_error_norm_rad[env_ids] = facing_error_angle
        self._joint_limit_margin_rad[env_ids] = torch.minimum(
            q_current - self._soft_limits[:, 0],
            self._soft_limits[:, 1] - q_current,
        ).amin(dim=-1)
        if self.cfg.local_orientation_gain > 0.0:
            twist = torch.cat(
                (
                    self.cfg.local_position_gain * position_error,
                    self.cfg.local_orientation_gain * facing_error,
                ),
                dim=-1,
            )
            # Project angular velocity into the target-axis tangent plane.
            # Without this projection a zero command along the inspection
            # axis would incorrectly constrain roll instead of leaving it
            # free.
            identity_3 = torch.eye(3, device=self.device).expand(len(env_ids), -1, -1)
            facing_projector = identity_3 - target_facing_b.unsqueeze(-1) * (
                target_facing_b.unsqueeze(1)
            )
            task_jacobian = torch.cat(
                (
                    jacobian[:, :3],
                    torch.bmm(facing_projector, jacobian[:, 3:]),
                ),
                dim=1,
            )
        else:
            # A zero orientation gain is an explicit position-only contract.
            # Keeping zero-valued angular rows here would still constrain the
            # nullspace to preserve orientation and can drive a distant IK
            # branch into joint limits.
            twist = self.cfg.local_position_gain * position_error
            task_jacobian = jacobian[:, :3]
        jacobian_t = task_jacobian.transpose(1, 2)
        regularized = torch.bmm(task_jacobian, jacobian_t) + (
            self.cfg.local_damping**2
        ) * torch.eye(task_jacobian.shape[1], device=self.device).unsqueeze(0)
        dls_inverse = torch.bmm(
            jacobian_t,
            torch.linalg.solve(
                regularized,
                torch.eye(task_jacobian.shape[1], device=self.device).expand(
                    len(env_ids), -1, -1
                ),
            ),
        )
        qd = torch.bmm(dls_inverse, twist.unsqueeze(-1)).squeeze(-1)
        hub_indices = self._prepared_hub_index[env_ids]
        q_nominal = self._waypoint_joint_pos[hub_indices]
        null_projector = torch.eye(6, device=self.device).unsqueeze(0) - torch.bmm(
            dls_inverse, task_jacobian
        )
        qd += torch.bmm(
            null_projector,
            (self.cfg.local_nullspace_gain * (q_nominal - q_current)).unsqueeze(-1),
        ).squeeze(-1)
        qd = torch.clamp(qd, -self.cfg.local_max_velocity_rad_s, self.cfg.local_max_velocity_rad_s)
        q_command = self._target_joint_pos[env_ids] + dt * qd
        q_command = torch.maximum(
            torch.minimum(q_command, self._soft_limits[:, 1]), self._soft_limits[:, 0]
        )
        self._target_joint_pos[env_ids] = q_command

        position_ok = torch.linalg.vector_norm(position_error, dim=-1) <= self.cfg.position_tolerance_m
        orientation_ok = facing_error_angle <= self.cfg.orientation_tolerance_rad
        pose_ok = position_ok & orientation_ok
        local_state = self._executor_state[env_ids]
        servo_ids = env_ids[local_state == int(ExecutorState.LOCAL_TARGET_SERVO)]
        servo_ok = pose_ok[local_state == int(ExecutorState.LOCAL_TARGET_SERVO)]
        entered_dwell = servo_ids[servo_ok]
        if len(entered_dwell) > 0:
            self._executor_state[entered_dwell] = int(ExecutorState.DWELL)
            self._dwell_elapsed_s[entered_dwell] = 0.0

        dwell_mask = local_state == int(ExecutorState.DWELL)
        dwell_ids = env_ids[dwell_mask]
        dwell_ok = pose_ok[dwell_mask]
        lost_ids = dwell_ids[~dwell_ok]
        if len(lost_ids) > 0:
            self._executor_state[lost_ids] = int(ExecutorState.LOCAL_TARGET_SERVO)
            self._dwell_elapsed_s[lost_ids] = 0.0
        stable_ids = dwell_ids[dwell_ok]
        if len(stable_ids) > 0:
            self._dwell_elapsed_s[stable_ids] += dt
            self._option_progress[stable_ids] = torch.clamp(
                self._dwell_elapsed_s[stable_ids] / self.cfg.dwell_time_s, max=1.0
            )
            complete_ids = stable_ids[
                self._dwell_elapsed_s[stable_ids] >= self.cfg.dwell_time_s
            ]
            if len(complete_ids) > 0:
                self._current_target_index[complete_ids] += 1
                self._executor_state[complete_ids] = int(ExecutorState.IDLE)
                self._active_option[complete_ids] = int(ArmOption.HOLD)
                self._option_progress[complete_ids] = 1.0
                task_done = self._current_target_index[complete_ids] >= self.cfg.target_count
                self._last_event[complete_ids] = int(ExecutorEvent.TARGET_COMPLETED)
                self._last_event[complete_ids[task_done]] = int(ExecutorEvent.TASK_COMPLETED)


@configclass
class SequentialInspectionJointPositionActionCfg(SmoothRandomJointPositionActionCfg):
    """Configuration for the persistent sequential-inspection executor."""

    class_type: type[ActionTerm] = SequentialInspectionJointPositionAction
    target_count: int = 4
    # Go/No-Go candidate only: includes observed frozen-locomotion tracking
    # drift.  These extents are not an offline collision-validated region.
    local_region_half_extent_m: tuple[float, float, float] = (0.22, 0.10, 0.10)
    local_region_exit_margin_m: float = 0.05
    local_damping: float = 0.03
    local_position_gain: float = 2.0
    local_orientation_gain: float = 1.5
    local_nullspace_gain: float = 0.15
    local_max_velocity_rad_s: float = math.radians(20.0)
    position_tolerance_m: float = 0.05
    orientation_tolerance_rad: float = math.radians(12.0)
    dwell_time_s: float = 0.3
