#!/usr/bin/env python3
"""Headless import and physics-contract smoke test for the standalone GLUON."""

import argparse
import math

from isaaclab.app import AppLauncher


parser = argparse.ArgumentParser(description=__doc__)
AppLauncher.add_app_launcher_args(parser)
args_cli = parser.parse_args()
app_launcher = AppLauncher(args_cli)
simulation_app = app_launcher.app


import torch  # noqa: E402

import isaaclab.sim as sim_utils  # noqa: E402
from isaaclab.assets import Articulation  # noqa: E402
from isaaclab.sim import SimulationContext  # noqa: E402
from isaaclab.utils.math import subtract_frame_transforms  # noqa: E402

from ddt_lab.assets.gluon import (  # noqa: E402
    GLUON_2L6_4L3_CFG,
    GLUON_BODY_NAMES,
    GLUON_END_EFFECTOR_BODY,
    GLUON_EXPECTED_TOTAL_MASS_KG,
    GLUON_JOINT_NAMES,
)


def main() -> None:
    sim = SimulationContext(sim_utils.SimulationCfg(device=args_cli.device, dt=0.005))
    cfg = GLUON_2L6_4L3_CFG.copy()
    cfg.prim_path = "/World/Gluon"
    robot = Articulation(cfg)

    sim.reset()
    robot.update(sim.get_physics_dt())

    failures: list[str] = []
    if not robot.is_fixed_base:
        failures.append("articulation is not fixed-base")
    if tuple(robot.joint_names) != GLUON_JOINT_NAMES:
        failures.append(f"joint order {robot.joint_names} != {list(GLUON_JOINT_NAMES)}")
    if tuple(robot.body_names) != GLUON_BODY_NAMES:
        failures.append(f"body order {robot.body_names} != {list(GLUON_BODY_NAMES)}")
    if GLUON_END_EFFECTOR_BODY not in robot.body_names:
        failures.append(f"missing end-effector body {GLUON_END_EFFECTOR_BODY}")

    total_mass = float(robot.data.default_mass[0].sum().item())
    if not math.isclose(total_mass, GLUON_EXPECTED_TOTAL_MASS_KG, rel_tol=0.0, abs_tol=1.0e-5):
        failures.append(
            f"PhysX total mass {total_mass:.12g} != expected {GLUON_EXPECTED_TOTAL_MASS_KG:.12g}"
        )

    initial_root_pose = robot.data.root_link_pose_w.clone()
    zero_target = torch.zeros((1, len(GLUON_JOINT_NAMES)), device=sim.device)
    for _ in range(20):
        robot.set_joint_position_target(zero_target)
        robot.write_data_to_sim()
        sim.step(render=False)
        robot.update(sim.get_physics_dt())

    tensors = (
        robot.data.joint_pos,
        robot.data.joint_vel,
        robot.data.body_link_pose_w,
        robot.data.default_mass,
        robot.data.default_inertia,
    )
    if not all(torch.isfinite(value).all().item() for value in tensors):
        failures.append("non-finite state, mass, or inertia after stepping")
    root_pose_drift = float(torch.max(torch.abs(robot.data.root_link_pose_w - initial_root_pose)).item())
    if root_pose_drift > 1.0e-6:
        failures.append(f"fixed root pose drifted by {root_pose_drift:.3e}")

    limits = robot.data.joint_pos_limits[0].detach().cpu().tolist()
    ee_index = robot.body_names.index(GLUON_END_EFFECTOR_BODY)
    ee_pos_b, ee_quat_b = subtract_frame_transforms(
        robot.data.root_link_pos_w,
        robot.data.root_link_quat_w,
        robot.data.body_link_pos_w[:, ee_index],
        robot.data.body_link_quat_w[:, ee_index],
    )
    print(f"fixed_base={robot.is_fixed_base}", flush=True)
    print(f"joint_names={robot.joint_names}", flush=True)
    print(f"body_names={robot.body_names}", flush=True)
    print(f"end_effector={GLUON_END_EFFECTOR_BODY}", flush=True)
    print(f"joint_position_limits={limits}", flush=True)
    print(f"home_ee_position_base={ee_pos_b[0].detach().cpu().tolist()}", flush=True)
    print(f"home_ee_quaternion_base_wxyz={ee_quat_b[0].detach().cpu().tolist()}", flush=True)
    print(f"total_mass_kg={total_mass:.12g}", flush=True)
    print(f"root_pose_max_drift={root_pose_drift:.3e}", flush=True)

    if failures:
        print("GLUON_ASSET_SMOKE: FAIL", flush=True)
        for failure in failures:
            print(f"- {failure}", flush=True)
        raise SystemExit(1)
    print("GLUON_ASSET_SMOKE: PASS", flush=True)


if __name__ == "__main__":
    try:
        main()
    finally:
        # Full Kit cleanup can stall for minutes on this workstation after a
        # headless URDF smoke test.  No persistent stage is being saved here.
        simulation_app.close(skip_cleanup=True)
