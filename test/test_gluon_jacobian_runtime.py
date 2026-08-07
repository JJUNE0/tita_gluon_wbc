#!/usr/bin/env python3
"""Validate the GLUON fixed-base PhysX position Jacobian against finite differences."""

import argparse
import math
import sys
from pathlib import Path

from isaaclab.app import AppLauncher


parser = argparse.ArgumentParser(description=__doc__)
AppLauncher.add_app_launcher_args(parser)
args_cli = parser.parse_args()
args_cli.headless = True
app_launcher = AppLauncher(args_cli)
simulation_app = app_launcher.app


import torch  # noqa: E402

import isaaclab.sim as sim_utils  # noqa: E402
from isaaclab.assets import Articulation  # noqa: E402
from isaaclab.sim import SimulationContext  # noqa: E402
from isaaclab.utils.math import matrix_from_quat, subtract_frame_transforms  # noqa: E402


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "lab" / "ddt_lab"))

from ddt_lab.assets.gluon import (  # noqa: E402
    GLUON_2L6_4L3_CFG,
    GLUON_END_EFFECTOR_BODY,
    GLUON_JOINT_NAMES,
)
from ddt_lab.gluon_ik import (  # noqa: E402
    GLUON_WORK_JOINT_POS_RAD,
    physx_com_jacobian_to_link_position_jacobian_b,
)


def main() -> None:
    sim = SimulationContext(sim_utils.SimulationCfg(device=args_cli.device, dt=0.005))
    cfg = GLUON_2L6_4L3_CFG.copy()
    cfg.prim_path = "/World/Gluon"
    robot = Articulation(cfg)
    sim.reset()
    robot.update(0.0)

    if tuple(robot.joint_names) != GLUON_JOINT_NAMES or not robot.is_fixed_base:
        raise RuntimeError("unexpected GLUON articulation contract")
    ee_body_index = robot.body_names.index(GLUON_END_EFFECTOR_BODY)
    ee_jacobian_index = ee_body_index - 1
    q_sample = torch.deg2rad(
        torch.tensor([[5.0, -5.0, 5.0, -5.0, 5.0, 0.0]], device=sim.device)
    )
    qd_zero = torch.zeros_like(q_sample)

    def set_q_and_get_position(q: torch.Tensor) -> torch.Tensor:
        robot.write_joint_state_to_sim(q, qd_zero)
        robot.reset()
        sim.forward()
        robot.update(0.0)
        position_b, _ = subtract_frame_transforms(
            robot.data.root_link_pos_w,
            robot.data.root_link_quat_w,
            robot.data.body_link_pos_w[:, ee_body_index],
            robot.data.body_link_quat_w[:, ee_body_index],
        )
        return position_b[0].clone()

    set_q_and_get_position(q_sample)
    jacobian_com_w = robot.root_physx_view.get_jacobians()[0, ee_jacobian_index, :, :5].clone()
    jacobian_raw = jacobian_com_w[:3]
    rotation_w_b = matrix_from_quat(robot.data.root_link_quat_w)[0]
    jacobian_rotated = rotation_w_b.transpose(0, 1) @ jacobian_raw
    jacobian_shifted = physx_com_jacobian_to_link_position_jacobian_b(
        jacobian_com_w=jacobian_com_w,
        com_position_w=robot.data.body_com_pos_w[0, ee_body_index],
        link_position_w=robot.data.body_link_pos_w[0, ee_body_index],
        rotation_w_b=rotation_w_b,
    )

    epsilon = 1.0e-3
    jacobian_fd = torch.zeros_like(jacobian_raw)
    for joint_index in range(5):
        q_plus = q_sample.clone()
        q_minus = q_sample.clone()
        q_plus[0, joint_index] += epsilon
        q_minus[0, joint_index] -= epsilon
        position_plus = set_q_and_get_position(q_plus)
        position_minus = set_q_and_get_position(q_minus)
        jacobian_fd[:, joint_index] = (position_plus - position_minus) / (2.0 * epsilon)

    raw_error = float(torch.max(torch.abs(jacobian_raw - jacobian_fd)).item())
    rotated_error = float(torch.max(torch.abs(jacobian_rotated - jacobian_fd)).item())
    shifted_error = float(torch.max(torch.abs(jacobian_shifted - jacobian_fd)).item())
    print(f"jacobian_raw={jacobian_raw.cpu().tolist()}", flush=True)
    print(f"jacobian_rotated={jacobian_rotated.cpu().tolist()}", flush=True)
    print(f"jacobian_shifted={jacobian_shifted.cpu().tolist()}", flush=True)
    print(f"jacobian_finite_difference={jacobian_fd.cpu().tolist()}", flush=True)
    print(
        f"jacobian_error,raw_max_abs={raw_error:.9g},rotated_max_abs={rotated_error:.9g},"
        f"shifted_max_abs={shifted_error:.9g},"
        f"epsilon_rad={epsilon}",
        flush=True,
    )
    if shifted_error > 5.0e-4:
        print("GLUON_JACOBIAN_RUNTIME: FAIL", flush=True)
        raise SystemExit(
            "PhysX raw Jacobian does not match base-frame finite differences; "
            f"raw={raw_error:.3e},rotated={rotated_error:.3e},shifted={shifted_error:.3e}"
        )
    if not math.isfinite(shifted_error):
        raise SystemExit("non-finite Jacobian error")
    print("GLUON_JACOBIAN_RUNTIME: PASS,frame=base_link", flush=True)

    work_q = torch.tensor([GLUON_WORK_JOINT_POS_RAD], device=sim.device)
    work_position_b = set_q_and_get_position(work_q)
    work_jacobian_com_w = robot.root_physx_view.get_jacobians()[
        0, ee_jacobian_index, :, :5
    ].clone()
    work_rotation_w_b = matrix_from_quat(robot.data.root_link_quat_w)[0]
    work_jacobian_b = physx_com_jacobian_to_link_position_jacobian_b(
        jacobian_com_w=work_jacobian_com_w,
        com_position_w=robot.data.body_com_pos_w[0, ee_body_index],
        link_position_w=robot.data.body_link_pos_w[0, ee_body_index],
        rotation_w_b=work_rotation_w_b,
    )
    work_singular_values = torch.linalg.svdvals(work_jacobian_b)
    soft_limits = robot.data.soft_joint_pos_limits[0]
    within_limits = bool(
        torch.all(work_q[0] >= soft_limits[:, 0])
        and torch.all(work_q[0] <= soft_limits[:, 1])
    )
    print(
        f"work_pose,q_rad={work_q[0].cpu().tolist()},"
        f"position_b_m={work_position_b.cpu().tolist()},"
        f"singular_values={work_singular_values.cpu().tolist()},"
        f"within_soft_limits={int(within_limits)}",
        flush=True,
    )
    if not within_limits:
        raise SystemExit("proposed GLUON work pose exceeds runtime soft limits")
    if float(work_singular_values[-1].item()) <= 1.0e-3:
        raise SystemExit(
            "proposed GLUON work pose is insufficiently conditioned: "
            f"sigma_min={float(work_singular_values[-1].item()):.6g}"
        )
    print("GLUON_WORK_POSE_CONDITIONING: PASS", flush=True)


if __name__ == "__main__":
    try:
        main()
    finally:
        simulation_app.close(skip_cleanup=True)
