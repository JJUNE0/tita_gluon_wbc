#!/usr/bin/env python3
"""Pure-PyTorch tests for the bounded GLUON position-only DLS step."""

import math
import sys
from pathlib import Path

import pytest
import torch


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "lab" / "ddt_lab"))

from ddt_lab.gluon_ik import (  # noqa: E402
    DEFAULT_CORNER_TRAJECTORY_SPEED_M_S,
    DEFAULT_CONTROL_DT_S,
    DEFAULT_MAX_SLEW_RAD_S,
    DEFAULT_MAX_TARGET_LEAD_M,
    WORKSPACE_W0_MAX_M,
    WORKSPACE_W0_MIN_M,
    WORKSPACE_W1_MAX_M,
    WORKSPACE_W1_MIN_M,
    WORKSPACE_W2_RADIUS_MAX_M,
    WORKSPACE_W2_RADIUS_MIN_M,
    WORKSPACE_W2_THETA_CENTER_RAD,
    WORKSPACE_W2_THETA_HALF_RANGE_RAD,
    WORKSPACE_W2_X_MAX_M,
    WORKSPACE_W2_X_MIN_M,
    advance_cylindrical_workspace_goal,
    apply_cylindrical_workspace_increment,
    cartesian_to_cylindrical_workspace,
    bounded_position_dls_step,
    bounded_joint_target_step,
    advance_cartesian_goal,
    clamp_workspace,
    cylindrical_workspace_to_cartesian,
    limit_target_lead,
    physx_com_jacobian_to_link_position_jacobian_b,
    sample_cylindrical_workspace_path,
    workspace_cylindrical_vertex_loop,
)


JOINT_LIMITS = torch.tensor(
    [
        [-2.45, 2.45],
        [-1.54, 1.56],
        [-2.31, 2.26],
        [-2.29, 2.27],
        [-2.29, 2.28],
        [-2.48, 2.48],
    ],
    dtype=torch.float64,
)
FULL_RANK_JACOBIAN = torch.tensor(
    [
        [1.0, 0.0, 0.2, 0.0, 0.1],
        [0.0, 1.0, 0.0, 0.2, 0.0],
        [0.0, 0.0, 1.0, 0.0, 0.3],
    ],
    dtype=torch.float64,
)


def make_step(**overrides):
    arguments = {
        "jacobian_position_b": FULL_RANK_JACOBIAN,
        "q_current": torch.zeros(6, dtype=torch.float64),
        "q_previous_command": torch.zeros(6, dtype=torch.float64),
        "q_nominal": torch.zeros(6, dtype=torch.float64),
        "current_position_b": torch.tensor([0.462, 0.02, -0.136], dtype=torch.float64),
        "target_position_b": torch.tensor([0.47, 0.03, -0.145], dtype=torch.float64),
        "joint_soft_limits": JOINT_LIMITS,
    }
    arguments.update(overrides)
    return bounded_position_dls_step(**arguments)


def test_workspace_clamp_reports_each_boundary() -> None:
    requested_cylindrical = torch.tensor(
        [0.30, 0.25, math.radians(150.0)], dtype=torch.float64
    )
    target = cylindrical_workspace_to_cartesian(requested_cylindrical)
    clamped, changed = clamp_workspace(target)
    assert changed
    clamped_cylindrical = cartesian_to_cylindrical_workspace(clamped)
    assert torch.allclose(
        clamped_cylindrical,
        torch.tensor(
            [WORKSPACE_W2_X_MIN_M, WORKSPACE_W2_RADIUS_MAX_M, math.radians(105.0)],
            dtype=torch.float64,
        ),
    )
    inside = torch.tensor([0.462, 0.02, -0.136], dtype=torch.float64)
    unchanged, changed = clamp_workspace(inside)
    assert not changed
    assert torch.equal(unchanged, inside)
    assert WORKSPACE_W0_MIN_M == (0.43, -0.01, -0.17)
    assert WORKSPACE_W0_MAX_M == (0.49, 0.05, -0.10)
    assert WORKSPACE_W1_MIN_M == (0.36, -0.08, -0.20)
    assert WORKSPACE_W1_MAX_M == (0.48, 0.09, -0.11)
    assert WORKSPACE_W2_X_MAX_M == 0.48
    assert WORKSPACE_W2_RADIUS_MIN_M == 0.13
    assert WORKSPACE_W2_THETA_CENTER_RAD == pytest.approx(math.radians(-70.0))
    assert WORKSPACE_W2_THETA_HALF_RANGE_RAD == pytest.approx(math.radians(105.0))


def test_cylindrical_workspace_round_trip_crosses_absolute_angle_branch_cut() -> None:
    cylindrical = torch.tensor(
        [
            [0.36, 0.13, math.radians(-120.0)],
            [0.42, 0.17, 0.0],
            [0.48, 0.21, math.radians(105.0)],
        ],
        dtype=torch.float64,
    )
    cartesian = cylindrical_workspace_to_cartesian(cylindrical)
    recovered = cartesian_to_cylindrical_workspace(cartesian)
    assert torch.allclose(recovered, cylindrical, atol=1.0e-12)


def test_target_lead_is_bounded_without_changing_direction() -> None:
    current = torch.tensor([0.462, 0.02, -0.136], dtype=torch.float64)
    requested = torch.tensor([0.49, 0.05, -0.10], dtype=torch.float64)
    limited, changed = limit_target_lead(requested, current)
    assert changed
    assert torch.linalg.vector_norm(limited - current).item() == pytest.approx(
        DEFAULT_MAX_TARGET_LEAD_M
    )
    assert torch.nn.functional.cosine_similarity(
        (limited - current).unsqueeze(0),
        (requested - current).unsqueeze(0),
    ).item() == pytest.approx(1.0)


def test_target_inside_lead_ball_is_unchanged() -> None:
    current = torch.tensor([0.462, 0.02, -0.136], dtype=torch.float64)
    requested = current + torch.tensor([0.001, -0.002, 0.003], dtype=torch.float64)
    limited, changed = limit_target_lead(requested, current)
    assert not changed
    assert torch.equal(limited, requested)


def test_joint_mode_step_respects_slew_and_soft_limits() -> None:
    previous = torch.zeros(6, dtype=torch.float64)
    target = torch.tensor([0.0, 0.8, 1.6, 0.8, 0.0, 9.0], dtype=torch.float64)
    command, joint_clamped, slew_limited = bounded_joint_target_step(
        target_joint_position=target,
        q_previous_command=previous,
        joint_soft_limits=JOINT_LIMITS,
    )
    max_delta = DEFAULT_MAX_SLEW_RAD_S * DEFAULT_CONTROL_DT_S
    assert joint_clamped
    assert slew_limited
    assert torch.max(torch.abs(command)).item() == pytest.approx(max_delta)
    assert torch.all(command >= JOINT_LIMITS[:, 0])
    assert torch.all(command <= JOINT_LIMITS[:, 1])


def test_workspace_cylindrical_vertex_loop_visits_each_vertex_and_closes() -> None:
    loop = workspace_cylindrical_vertex_loop(torch.zeros(3, dtype=torch.float64))
    assert loop.shape == (9, 3)
    assert torch.equal(loop[0], loop[-1])
    assert len(torch.unique(loop[:-1], dim=0)) == 8
    edge_deltas = torch.abs(loop[1:] - loop[:-1])
    assert torch.all(torch.count_nonzero(edge_deltas, dim=1) == 1)
    assert bool(torch.isfinite(cylindrical_workspace_to_cartesian(loop)).all())


def test_cylindrical_trajectory_goal_advances_at_bounded_arc_speed() -> None:
    goal = torch.tensor(
        [0.36, 0.13, math.radians(-105.0)], dtype=torch.float64
    )
    waypoint = torch.tensor(
        [0.36, 0.13, math.radians(105.0)], dtype=torch.float64
    )
    max_step = DEFAULT_CORNER_TRAJECTORY_SPEED_M_S * DEFAULT_CONTROL_DT_S
    advanced, reached = advance_cylindrical_workspace_goal(goal, waypoint, max_step)
    assert not reached
    assert advanced[2] > goal[2]
    metric_step = torch.tensor(
        [advanced[0] - goal[0], advanced[1] - goal[1], 0.13 * (advanced[2] - goal[2])]
    )
    assert torch.linalg.vector_norm(metric_step).item() == pytest.approx(max_step)


def test_cylindrical_keyboard_increment_uses_tangential_arc_length() -> None:
    goal = torch.tensor([0.42, 0.20, 0.0], dtype=torch.float64)
    increment = torch.tensor([0.001, -0.002, 0.010], dtype=torch.float64)
    updated = apply_cylindrical_workspace_increment(goal, increment)
    assert torch.allclose(
        updated,
        torch.tensor([0.421, 0.198, 0.05], dtype=torch.float64),
    )


def test_cylindrical_path_sampling_preserves_vertices_and_spacing() -> None:
    loop = workspace_cylindrical_vertex_loop(torch.zeros(3, dtype=torch.float64))
    samples = sample_cylindrical_workspace_path(loop, max_spacing_m=0.008)
    assert samples.shape[0] > loop.shape[0]
    assert torch.equal(samples[0], loop[0])
    assert torch.equal(samples[-1], loop[-1])
    assert torch.allclose(
        cylindrical_workspace_to_cartesian(samples[[0, -1]]),
        cylindrical_workspace_to_cartesian(loop[[0, -1]]),
    )


def test_cartesian_trajectory_goal_advances_at_bounded_speed() -> None:
    goal = torch.tensor([0.36, -0.08, -0.20], dtype=torch.float64)
    waypoint = torch.tensor([0.48, -0.08, -0.20], dtype=torch.float64)
    max_step = DEFAULT_CORNER_TRAJECTORY_SPEED_M_S * DEFAULT_CONTROL_DT_S
    advanced, reached = advance_cartesian_goal(goal, waypoint, max_step)
    assert not reached
    assert torch.linalg.vector_norm(advanced - goal).item() == pytest.approx(max_step)
    final, reached = advance_cartesian_goal(waypoint - 0.5 * (waypoint - goal), waypoint, 1.0)
    assert reached
    assert torch.equal(final, waypoint)


def test_dls_moves_active_joints_and_holds_zero_q6() -> None:
    step = make_step()
    assert step.q_command.shape == (6,)
    assert bool(torch.isfinite(step.q_command).all())
    assert not torch.equal(step.q_command[:5], torch.zeros(5, dtype=torch.float64))
    assert step.q_command[5].item() == 0.0
    assert step.smallest_singular_value > 0.0


def test_com_jacobian_is_shifted_to_link_origin_and_rotated_to_base() -> None:
    jacobian = torch.zeros((6, 2), dtype=torch.float64)
    jacobian[:3] = torch.tensor([[1.0, 0.0], [0.0, 2.0], [0.0, 0.0]])
    jacobian[3:6] = torch.tensor([[0.0, 0.0], [0.0, 0.0], [1.0, -1.0]])
    rotation_w_b = torch.tensor(
        [[0.0, 0.0, 1.0], [0.0, 1.0, 0.0], [-1.0, 0.0, 0.0]],
        dtype=torch.float64,
    )
    shifted = physx_com_jacobian_to_link_position_jacobian_b(
        jacobian_com_w=jacobian,
        com_position_w=torch.zeros(3, dtype=torch.float64),
        link_position_w=torch.tensor([1.0, 0.0, 0.0], dtype=torch.float64),
        rotation_w_b=rotation_w_b,
    )
    expected_link_w = torch.tensor(
        [[1.0, 0.0], [1.0, 1.0], [0.0, 0.0]], dtype=torch.float64
    )
    assert torch.allclose(shifted, rotation_w_b.T @ expected_link_w)


def test_joint_slew_is_limited_to_twenty_degrees_per_second() -> None:
    step = make_step(
        target_position_b=torch.tensor([0.49, 0.05, -0.17], dtype=torch.float64)
    )
    max_delta = DEFAULT_MAX_SLEW_RAD_S * DEFAULT_CONTROL_DT_S
    assert float(torch.max(torch.abs(step.q_command)).item()) <= max_delta + 1.0e-12
    assert step.slew_limited
    assert step.state == "SATURATED"


def test_runtime_soft_limits_are_never_exceeded() -> None:
    limits = JOINT_LIMITS.clone()
    limits[0] = torch.tensor([-0.001, 0.001], dtype=torch.float64)
    step = make_step(joint_soft_limits=limits, max_slew_rad_s=100.0)
    assert step.joint_limit_clamped
    assert torch.all(step.q_command >= limits[:, 0])
    assert torch.all(step.q_command <= limits[:, 1])


def test_disturbed_q6_moves_toward_zero_without_discontinuity() -> None:
    q_current = torch.zeros(6, dtype=torch.float64)
    q_current[5] = math.radians(5.0)
    step = make_step(
        q_current=q_current,
        q_previous_command=q_current.clone(),
        q_nominal=q_current.clone(),
    )
    max_delta = DEFAULT_MAX_SLEW_RAD_S * DEFAULT_CONTROL_DT_S
    assert step.q_command[5] < q_current[5]
    assert (q_current[5] - step.q_command[5]).item() == pytest.approx(max_delta)


def test_singular_unreached_target_is_explicit() -> None:
    singular = torch.zeros((3, 5), dtype=torch.float64)
    step = make_step(jacobian_position_b=singular)
    assert step.state == "UNREACHABLE"
    assert step.smallest_singular_value == 0.0
    assert torch.equal(step.q_command, torch.zeros(6, dtype=torch.float64))


def test_target_hold_has_zero_startup_command_discontinuity() -> None:
    q_current = torch.tensor([0.1, -0.2, 0.3, -0.1, 0.2, 0.0], dtype=torch.float64)
    position = torch.tensor([0.462, 0.02, -0.136], dtype=torch.float64)
    step = make_step(
        q_current=q_current,
        q_previous_command=q_current.clone(),
        q_nominal=q_current.clone(),
        current_position_b=position,
        target_position_b=position.clone(),
    )
    assert step.state == "HOLD"
    assert torch.equal(step.q_command, q_current)


@pytest.mark.parametrize(
    "field,bad_value",
    [
        ("target_position_b", torch.tensor([float("nan"), 0.0, 0.0], dtype=torch.float64)),
        ("jacobian_position_b", torch.full((3, 5), float("inf"), dtype=torch.float64)),
    ],
)
def test_nonfinite_input_is_rejected(field: str, bad_value: torch.Tensor) -> None:
    with pytest.raises(ValueError, match="NaN or Inf"):
        make_step(**{field: bad_value})
