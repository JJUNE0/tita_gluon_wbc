"""Pure position-only DLS helpers for the GLUON keyboard IK application."""

from dataclasses import dataclass
import math

import torch


# Historical Cartesian validation gates. HOME q=0 is intentionally outside
# these gates and is handled by a joint-space mode.
WORKSPACE_W0_MIN_M = (0.43, -0.01, -0.17)
WORKSPACE_W0_MAX_M = (0.49, 0.05, -0.10)
WORKSPACE_W1_MIN_M = (0.36, -0.08, -0.20)
WORKSPACE_W1_MAX_M = (0.48, 0.09, -0.11)
# W2 is a cylindrical sector about joint1's base +X axis. The theta coordinate
# is represented as an unwrapped offset from the conditioned WORK direction,
# avoiding the +/-pi branch cut inside the active sector.
WORKSPACE_W2_X_MIN_M = 0.36
WORKSPACE_W2_X_MAX_M = 0.48
WORKSPACE_W2_RADIUS_MIN_M = 0.13
WORKSPACE_W2_RADIUS_MAX_M = 0.21
WORKSPACE_W2_THETA_CENTER_RAD = math.radians(-70.0)
WORKSPACE_W2_THETA_HALF_RANGE_RAD = math.radians(105.0)
DEFAULT_CONTROL_DT_S = 1.0 / 50.0
DEFAULT_DAMPING = 0.01
DEFAULT_DLS_GAIN = 2.0
DEFAULT_NULLSPACE_GAIN = 0.1
DEFAULT_MAX_SLEW_RAD_S = math.radians(20.0)
DEFAULT_MAX_TARGET_LEAD_M = 0.010
DEFAULT_POSITION_TOLERANCE_M = 0.001
DEFAULT_SINGULAR_VALUE_THRESHOLD = 1.0e-4
DEFAULT_CORNER_TRAJECTORY_SPEED_M_S = 0.06
DEFAULT_CORNER_TRAJECTORY_TOLERANCE_M = 0.005
GLUON_HOME_JOINT_POS_RAD = (0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
GLUON_WORK_JOINT_POS_RAD = (0.0, 0.8, 1.6, 0.8, 0.0, 0.0)
WORKSPACE_VERTEX_LOOP_BITS = (
    (0, 0, 0),
    (0, 0, 1),
    (1, 0, 1),
    (1, 1, 1),
    (0, 1, 1),
    (0, 1, 0),
    (1, 1, 0),
    (1, 0, 0),
    (0, 0, 0),
)


@dataclass(frozen=True)
class GluonIKStep:
    """One bounded DLS command and the metrics used to explain it."""

    q_command: torch.Tensor
    target_clamped: torch.Tensor
    position_error_norm_m: float
    smallest_singular_value: float
    workspace_clamped: bool
    joint_limit_clamped: bool
    slew_limited: bool
    state: str


def _require_shape(value: torch.Tensor, shape: tuple[int, ...], name: str) -> None:
    if value.shape != shape:
        raise ValueError(f"{name} must have shape {shape}, got {tuple(value.shape)}")
    if not bool(torch.isfinite(value).all()):
        raise ValueError(f"{name} contains NaN or Inf")


def wrap_angle_to_pi(angle_rad: torch.Tensor) -> torch.Tensor:
    """Wrap angles to [-pi, pi] without leaving the tensor device."""
    return torch.atan2(torch.sin(angle_rad), torch.cos(angle_rad))


def cartesian_to_cylindrical_workspace(
    position_b: torch.Tensor,
    theta_center_rad: float = WORKSPACE_W2_THETA_CENTER_RAD,
) -> torch.Tensor:
    """Convert base XYZ to [axial X, radius, theta offset] about base +X."""
    if position_b.shape[-1] != 3:
        raise ValueError(f"position_b last dimension must be 3, got {position_b.shape}")
    if not bool(torch.isfinite(position_b).all()):
        raise ValueError("position_b contains NaN or Inf")
    radius = torch.linalg.vector_norm(position_b[..., 1:3], dim=-1)
    theta = torch.atan2(position_b[..., 2], position_b[..., 1])
    theta_offset = wrap_angle_to_pi(theta - theta_center_rad)
    return torch.stack((position_b[..., 0], radius, theta_offset), dim=-1)


def cylindrical_workspace_to_cartesian(
    cylindrical: torch.Tensor,
    theta_center_rad: float = WORKSPACE_W2_THETA_CENTER_RAD,
) -> torch.Tensor:
    """Convert [axial X, radius, unwrapped theta offset] to base XYZ."""
    if cylindrical.shape[-1] != 3:
        raise ValueError(f"cylindrical last dimension must be 3, got {cylindrical.shape}")
    if not bool(torch.isfinite(cylindrical).all()):
        raise ValueError("cylindrical contains NaN or Inf")
    theta = theta_center_rad + cylindrical[..., 2]
    return torch.stack(
        (
            cylindrical[..., 0],
            cylindrical[..., 1] * torch.cos(theta),
            cylindrical[..., 1] * torch.sin(theta),
        ),
        dim=-1,
    )


def clamp_workspace(target_position_b: torch.Tensor) -> tuple[torch.Tensor, bool]:
    """Clamp a base-frame XYZ target to the active W2 cylindrical sector."""
    _require_shape(target_position_b, (3,), "target_position_b")
    cylindrical = cartesian_to_cylindrical_workspace(target_position_b)
    lower = cylindrical.new_tensor(
        (
            WORKSPACE_W2_X_MIN_M,
            WORKSPACE_W2_RADIUS_MIN_M,
            -WORKSPACE_W2_THETA_HALF_RANGE_RAD,
        )
    )
    upper = cylindrical.new_tensor(
        (
            WORKSPACE_W2_X_MAX_M,
            WORKSPACE_W2_RADIUS_MAX_M,
            WORKSPACE_W2_THETA_HALF_RANGE_RAD,
        )
    )
    inside = bool(
        torch.logical_and(
            torch.all(cylindrical >= lower), torch.all(cylindrical <= upper)
        )
    )
    if inside:
        return target_position_b.clone(), False
    clamped_cylindrical = torch.maximum(torch.minimum(cylindrical, upper), lower)
    return cylindrical_workspace_to_cartesian(clamped_cylindrical), True


def workspace_cylindrical_vertex_loop(reference: torch.Tensor) -> torch.Tensor:
    """Return the closed eight-vertex W2 loop in [X, radius, theta offset]."""
    if reference.ndim == 0:
        raise ValueError("reference must have at least one dimension")
    lower = reference.new_tensor(
        (
            WORKSPACE_W2_X_MIN_M,
            WORKSPACE_W2_RADIUS_MIN_M,
            -WORKSPACE_W2_THETA_HALF_RANGE_RAD,
        )
    )
    upper = reference.new_tensor(
        (
            WORKSPACE_W2_X_MAX_M,
            WORKSPACE_W2_RADIUS_MAX_M,
            WORKSPACE_W2_THETA_HALF_RANGE_RAD,
        )
    )
    vertices = []
    for bits in WORKSPACE_VERTEX_LOOP_BITS:
        selector = reference.new_tensor(bits, dtype=torch.bool)
        vertices.append(torch.where(selector, upper, lower))
    return torch.stack(vertices)


def advance_cylindrical_workspace_goal(
    current_goal_cylindrical: torch.Tensor,
    waypoint_cylindrical: torch.Tensor,
    max_step_m: float,
) -> tuple[torch.Tensor, bool]:
    """Advance in W2 coordinates using local cylindrical arc-length metric."""
    _require_shape(current_goal_cylindrical, (3,), "current_goal_cylindrical")
    _require_shape(waypoint_cylindrical, (3,), "waypoint_cylindrical")
    if max_step_m <= 0.0 or not math.isfinite(max_step_m):
        raise ValueError("max_step_m must be finite and positive")
    delta = waypoint_cylindrical - current_goal_cylindrical
    mean_radius = 0.5 * (
        current_goal_cylindrical[1] + waypoint_cylindrical[1]
    )
    metric_delta = torch.stack((delta[0], delta[1], mean_radius * delta[2]))
    distance = float(torch.linalg.vector_norm(metric_delta).item())
    if distance <= max_step_m:
        return waypoint_cylindrical.clone(), True
    return current_goal_cylindrical + (max_step_m / distance) * delta, False


def apply_cylindrical_workspace_increment(
    current_goal_cylindrical: torch.Tensor,
    metric_increment: torch.Tensor,
) -> torch.Tensor:
    """Apply keyboard [dX, dR, tangential arc] increments to a W2 goal."""
    _require_shape(current_goal_cylindrical, (3,), "current_goal_cylindrical")
    _require_shape(metric_increment, (3,), "metric_increment")
    radius = torch.clamp(
        current_goal_cylindrical[1], min=WORKSPACE_W2_RADIUS_MIN_M
    )
    coordinate_increment = torch.stack(
        (metric_increment[0], metric_increment[1], metric_increment[2] / radius)
    )
    return current_goal_cylindrical + coordinate_increment


def sample_cylindrical_workspace_path(
    cylindrical_waypoints: torch.Tensor,
    max_spacing_m: float = 0.008,
) -> torch.Tensor:
    """Sample a cylindrical polyline densely enough for a wire/path marker."""
    if cylindrical_waypoints.ndim != 2 or cylindrical_waypoints.shape[1] != 3:
        raise ValueError(
            "cylindrical_waypoints must have shape (N, 3), got "
            f"{tuple(cylindrical_waypoints.shape)}"
        )
    if cylindrical_waypoints.shape[0] < 2:
        raise ValueError("cylindrical_waypoints must contain at least two points")
    if max_spacing_m <= 0.0 or not math.isfinite(max_spacing_m):
        raise ValueError("max_spacing_m must be finite and positive")
    sampled_segments = []
    for index in range(cylindrical_waypoints.shape[0] - 1):
        start = cylindrical_waypoints[index]
        end = cylindrical_waypoints[index + 1]
        delta = end - start
        mean_radius = 0.5 * (start[1] + end[1])
        metric_delta = torch.stack((delta[0], delta[1], mean_radius * delta[2]))
        metric_length_m = float(torch.linalg.vector_norm(metric_delta).item())
        sample_count = max(1, int(math.ceil(metric_length_m / max_spacing_m)))
        fractions = torch.linspace(
            0.0,
            1.0,
            sample_count + 1,
            device=start.device,
            dtype=start.dtype,
        )
        if index > 0:
            fractions = fractions[1:]
        sampled_segments.append(start.unsqueeze(0) + fractions.unsqueeze(1) * delta)
    return torch.cat(sampled_segments, dim=0)


def advance_cartesian_goal(
    current_goal: torch.Tensor,
    waypoint: torch.Tensor,
    max_step_m: float,
) -> tuple[torch.Tensor, bool]:
    """Advance an absolute Cartesian goal toward a waypoint at bounded speed."""
    _require_shape(current_goal, (3,), "current_goal")
    _require_shape(waypoint, (3,), "waypoint")
    if max_step_m <= 0.0 or not math.isfinite(max_step_m):
        raise ValueError("max_step_m must be finite and positive")
    offset = waypoint - current_goal
    distance = float(torch.linalg.vector_norm(offset).item())
    if distance <= max_step_m:
        return waypoint.clone(), True
    return current_goal + (max_step_m / distance) * offset, False


def limit_target_lead(
    target_position_b: torch.Tensor,
    current_position_b: torch.Tensor,
    max_lead_m: float = DEFAULT_MAX_TARGET_LEAD_M,
) -> tuple[torch.Tensor, bool]:
    """Limit a Cartesian servo target to a ball around the current EE.

    Keyboard input can otherwise move the target tens of millimetres ahead of
    a slew-limited robot in a fraction of a second.  The local target is kept
    near the measured end effector while a farther operator goal can remain
    queued separately by the application.
    """
    _require_shape(target_position_b, (3,), "target_position_b")
    _require_shape(current_position_b, (3,), "current_position_b")
    if max_lead_m <= 0.0 or not math.isfinite(max_lead_m):
        raise ValueError("max_lead_m must be finite and positive")
    offset = target_position_b - current_position_b
    distance = float(torch.linalg.vector_norm(offset).item())
    if distance <= max_lead_m:
        return target_position_b.clone(), False
    scale = max_lead_m / distance
    return current_position_b + scale * offset, True


def bounded_joint_target_step(
    *,
    target_joint_position: torch.Tensor,
    q_previous_command: torch.Tensor,
    joint_soft_limits: torch.Tensor,
    control_dt_s: float = DEFAULT_CONTROL_DT_S,
    max_slew_rad_s: float = DEFAULT_MAX_SLEW_RAD_S,
) -> tuple[torch.Tensor, bool, bool]:
    """Move a six-axis joint command toward a target with limits and slew.

    Returns the next command, whether the requested target was clamped by a
    joint limit, and whether the step was slew-limited.
    """
    _require_shape(target_joint_position, (6,), "target_joint_position")
    _require_shape(q_previous_command, (6,), "q_previous_command")
    _require_shape(joint_soft_limits, (6, 2), "joint_soft_limits")
    if control_dt_s <= 0.0 or not math.isfinite(control_dt_s):
        raise ValueError("control_dt_s must be finite and positive")
    if max_slew_rad_s <= 0.0 or not math.isfinite(max_slew_rad_s):
        raise ValueError("max_slew_rad_s must be finite and positive")
    if bool(torch.any(joint_soft_limits[:, 0] > joint_soft_limits[:, 1])):
        raise ValueError("joint soft lower limits exceed upper limits")
    target_within_limits = torch.maximum(
        torch.minimum(target_joint_position, joint_soft_limits[:, 1]),
        joint_soft_limits[:, 0],
    )
    joint_limit_clamped = not bool(torch.equal(target_within_limits, target_joint_position))
    max_delta = max_slew_rad_s * control_dt_s
    requested_delta = target_within_limits - q_previous_command
    command_delta = torch.clamp(requested_delta, -max_delta, max_delta)
    slew_limited = not bool(torch.equal(command_delta, requested_delta))
    q_command = q_previous_command + command_delta
    return q_command, joint_limit_clamped, slew_limited


def physx_com_jacobian_to_link_position_jacobian_b(
    *,
    jacobian_com_w: torch.Tensor,
    com_position_w: torch.Tensor,
    link_position_w: torch.Tensor,
    rotation_w_b: torch.Tensor,
) -> torch.Tensor:
    """Move a PhysX COM Jacobian to the link origin and express it in base.

    PhysX reports each rigid-body Jacobian at its center of mass in world
    coordinates. The GLUON Cartesian contract controls the ``link6`` frame
    origin, so the linear rows require the rigid-body point-shift term before
    rotation into ``base_link``.
    """
    if jacobian_com_w.ndim != 2 or jacobian_com_w.shape[0] != 6:
        raise ValueError(f"jacobian_com_w must have shape (6, N), got {jacobian_com_w.shape}")
    _require_shape(com_position_w, (3,), "com_position_w")
    _require_shape(link_position_w, (3,), "link_position_w")
    _require_shape(rotation_w_b, (3, 3), "rotation_w_b")
    if not bool(torch.isfinite(jacobian_com_w).all()):
        raise ValueError("jacobian_com_w contains NaN or Inf")
    offset_com_to_link_w = link_position_w - com_position_w
    angular_columns_w = jacobian_com_w[3:6].transpose(0, 1)
    point_shift_w = torch.linalg.cross(
        angular_columns_w,
        offset_com_to_link_w.expand_as(angular_columns_w),
    ).transpose(0, 1)
    link_linear_w = jacobian_com_w[:3] + point_shift_w
    return rotation_w_b.transpose(0, 1) @ link_linear_w


def bounded_position_dls_step(
    *,
    jacobian_position_b: torch.Tensor,
    q_current: torch.Tensor,
    q_previous_command: torch.Tensor,
    q_nominal: torch.Tensor,
    current_position_b: torch.Tensor,
    target_position_b: torch.Tensor,
    joint_soft_limits: torch.Tensor,
    control_dt_s: float = DEFAULT_CONTROL_DT_S,
    damping: float = DEFAULT_DAMPING,
    dls_gain: float = DEFAULT_DLS_GAIN,
    nullspace_gain: float = DEFAULT_NULLSPACE_GAIN,
    max_slew_rad_s: float = DEFAULT_MAX_SLEW_RAD_S,
    q6_hold_rad: float = 0.0,
    position_tolerance_m: float = DEFAULT_POSITION_TOLERANCE_M,
    singular_value_threshold: float = DEFAULT_SINGULAR_VALUE_THRESHOLD,
) -> GluonIKStep:
    """Compute a safe q1--q5 DLS step while driving q6 toward its hold target.

    All Cartesian quantities and the Jacobian must use the ``base_link`` frame.
    The returned command is clamped to runtime soft limits and to a per-control
    tick slew bound. If q6 is disturbed, its command approaches zero through
    the same slew bound instead of introducing a discontinuity.
    """
    _require_shape(jacobian_position_b, (3, 5), "jacobian_position_b")
    _require_shape(q_current, (6,), "q_current")
    _require_shape(q_previous_command, (6,), "q_previous_command")
    _require_shape(q_nominal, (6,), "q_nominal")
    _require_shape(current_position_b, (3,), "current_position_b")
    _require_shape(target_position_b, (3,), "target_position_b")
    _require_shape(joint_soft_limits, (6, 2), "joint_soft_limits")
    if control_dt_s <= 0.0:
        raise ValueError("control_dt_s must be positive")
    if damping <= 0.0:
        raise ValueError("damping must be positive")
    if dls_gain <= 0.0:
        raise ValueError("dls_gain must be positive")
    if not 0.0 <= nullspace_gain <= 1.0:
        raise ValueError("nullspace_gain must be in [0, 1]")
    if max_slew_rad_s <= 0.0:
        raise ValueError("max_slew_rad_s must be positive")
    if bool(torch.any(joint_soft_limits[:, 0] > joint_soft_limits[:, 1])):
        raise ValueError("joint soft lower limits exceed upper limits")

    target_clamped, workspace_clamped = clamp_workspace(target_position_b)
    position_error = target_clamped - current_position_b
    error_norm = float(torch.linalg.vector_norm(position_error).item())

    singular_values = torch.linalg.svdvals(jacobian_position_b)
    smallest_singular_value = float(singular_values[-1].item())
    jacobian_transpose = jacobian_position_b.transpose(0, 1)
    regularized = jacobian_position_b @ jacobian_transpose
    regularized = regularized + (damping**2) * torch.eye(
        3, device=regularized.device, dtype=regularized.dtype
    )
    dls_inverse = jacobian_transpose @ torch.linalg.solve(
        regularized, torch.eye(3, device=regularized.device, dtype=regularized.dtype)
    )
    delta_q_active = dls_gain * (dls_inverse @ position_error)
    nullspace_projector = torch.eye(
        5, device=jacobian_position_b.device, dtype=jacobian_position_b.dtype
    ) - dls_inverse @ jacobian_position_b
    delta_q_active = delta_q_active + nullspace_gain * (
        nullspace_projector @ (q_nominal[:5] - q_current[:5])
    )

    q_candidate = q_current.clone()
    q_candidate[:5] = q_current[:5] + delta_q_active
    q_candidate[5] = q6_hold_rad
    q_within_limits = torch.maximum(
        torch.minimum(q_candidate, joint_soft_limits[:, 1]), joint_soft_limits[:, 0]
    )
    joint_limit_clamped = not bool(torch.equal(q_within_limits, q_candidate))

    max_delta = max_slew_rad_s * control_dt_s
    command_delta = torch.clamp(q_within_limits - q_previous_command, -max_delta, max_delta)
    slew_limited = not bool(torch.equal(command_delta, q_within_limits - q_previous_command))
    q_command = q_previous_command + command_delta
    q_command = torch.maximum(
        torch.minimum(q_command, joint_soft_limits[:, 1]), joint_soft_limits[:, 0]
    )
    if not bool(torch.isfinite(q_command).all()):
        raise RuntimeError("DLS produced a non-finite joint command")

    if error_norm <= position_tolerance_m:
        state = "HOLD"
    elif smallest_singular_value < singular_value_threshold:
        state = "UNREACHABLE"
    elif workspace_clamped or joint_limit_clamped or slew_limited:
        state = "SATURATED"
    else:
        state = "TRACKING"

    return GluonIKStep(
        q_command=q_command,
        target_clamped=target_clamped,
        position_error_norm_m=error_norm,
        smallest_singular_value=smallest_singular_value,
        workspace_clamped=workspace_clamped,
        joint_limit_clamped=joint_limit_clamped,
        slew_limited=slew_limited,
        state=state,
    )
