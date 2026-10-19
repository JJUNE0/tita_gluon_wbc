#!/usr/bin/env python3
"""Headless runtime equivalence test for the GLUON sim URDF and generated USD."""

import argparse
import json
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
from isaaclab.utils.math import subtract_frame_transforms  # noqa: E402


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "lab" / "ddt_lab"))

from ddt_lab.assets.gluon import (  # noqa: E402
    GLUON_2L6_4L3_CFG,
    GLUON_2L6_4L3_URDF_PATH,
    GLUON_BODY_NAMES,
    GLUON_END_EFFECTOR_BODY,
    GLUON_JOINT_NAMES,
)


MODEL_ROOT = REPO_ROOT / "sim2sim" / "robot" / "gluon"
CONTRACT_PATH = MODEL_ROOT / "config" / "model_contract.json"
USD_PATH = MODEL_ROOT / "usd" / "gluon_2L6_4L3.usd"
POSITION_TOLERANCE_M = 1.0e-3
ORIENTATION_TOLERANCE_RAD = math.radians(0.5)
LIMIT_TOLERANCE_RAD = 1.0e-6
MASS_TOLERANCE_KG = 1.0e-5

SAMPLES_DEG = {
    "q0": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    "q_local1": [5.0, -5.0, 5.0, -5.0, 5.0, 0.0],
    "q_local2": [-10.0, 10.0, -10.0, 10.0, -10.0, 0.0],
    "q6_test": [0.0, 0.0, 0.0, 0.0, 0.0, 30.0],
}


def check(condition: bool, label: str, detail: str, failures: list[str]) -> None:
    status = "PASS" if condition else "FAIL"
    print(f"check,status={status},name={label},{detail}", flush=True)
    if not condition:
        failures.append(f"{label}: {detail}")


def quaternion_distance(q_a: torch.Tensor, q_b: torch.Tensor) -> torch.Tensor:
    """Return sign-invariant shortest angular distance for WXYZ quaternions."""
    q_a = torch.nn.functional.normalize(q_a, dim=-1)
    q_b = torch.nn.functional.normalize(q_b, dim=-1)
    dot = torch.sum(q_a * q_b, dim=-1).abs().clamp(max=1.0)
    return 2.0 * torch.acos(dot)


def end_effector_pose_base(robot: Articulation) -> tuple[torch.Tensor, torch.Tensor]:
    ee_index = robot.body_names.index(GLUON_END_EFFECTOR_BODY)
    return subtract_frame_transforms(
        robot.data.root_link_pos_w,
        robot.data.root_link_quat_w,
        robot.data.body_link_pos_w[:, ee_index],
        robot.data.body_link_quat_w[:, ee_index],
    )


def main() -> None:
    failures: list[str] = []
    contract = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
    interface = contract["interface_v1"]

    check(USD_PATH.is_file(), "usd_exists", f"path={USD_PATH}", failures)

    sim = SimulationContext(sim_utils.SimulationCfg(device=args_cli.device, dt=0.005))

    urdf_cfg = GLUON_2L6_4L3_CFG.copy()
    urdf_cfg.prim_path = "/World/GluonUrdf"
    urdf_cfg.init_state.pos = (-1.0, 0.0, 0.0)
    # GLUON_2L6_4L3_CFG intentionally loads the validated USD in production.
    # Override the spawn config here so this side of the comparison is really
    # imported from the contract-pinned URDF rather than comparing USD to USD.
    urdf_cfg.spawn = sim_utils.UrdfFileCfg(
        asset_path=str(GLUON_2L6_4L3_URDF_PATH),
        fix_base=True,
        merge_fixed_joints=False,
        replace_cylinders_with_capsules=False,
        collider_type="convex_hull",
        self_collision=False,
        force_usd_conversion=True,
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
        joint_drive=sim_utils.UrdfConverterCfg.JointDriveCfg(
            target_type="none",
            gains=sim_utils.UrdfConverterCfg.JointDriveCfg.PDGainsCfg(
                stiffness=0.0,
                damping=0.0,
            ),
        ),
    )

    usd_cfg = GLUON_2L6_4L3_CFG.copy()
    usd_cfg.prim_path = "/World/GluonUsd"
    usd_cfg.init_state.pos = (1.0, 0.0, 0.0)
    usd_cfg.spawn = sim_utils.UsdFileCfg(
        usd_path=str(USD_PATH),
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
    )

    print(
        f"equivalence_sources,urdf={GLUON_2L6_4L3_URDF_PATH},usd={USD_PATH}",
        flush=True,
    )

    urdf_robot = Articulation(urdf_cfg)
    usd_robot = Articulation(usd_cfg)
    sim.reset()
    urdf_robot.update(sim.get_physics_dt())
    usd_robot.update(sim.get_physics_dt())

    for label, robot in (("urdf", urdf_robot), ("usd", usd_robot)):
        check(robot.is_fixed_base, f"{label}_fixed_base", f"value={robot.is_fixed_base}", failures)
        check(
            tuple(robot.joint_names) == GLUON_JOINT_NAMES,
            f"{label}_joint_order",
            f"actual={robot.joint_names},expected={list(GLUON_JOINT_NAMES)}",
            failures,
        )
        check(
            tuple(robot.body_names) == GLUON_BODY_NAMES,
            f"{label}_body_order",
            f"actual={robot.body_names},expected={list(GLUON_BODY_NAMES)}",
            failures,
        )

    limit_error = float(
        torch.max(
            torch.abs(urdf_robot.data.joint_pos_limits[0] - usd_robot.data.joint_pos_limits[0])
        ).item()
    )
    check(
        limit_error <= LIMIT_TOLERANCE_RAD,
        "joint_limit_equivalence",
        f"max_abs_error_rad={limit_error:.3e}",
        failures,
    )

    expected_limits = torch.tensor(
        [interface["joint_soft_limits_rad"][name] for name in GLUON_JOINT_NAMES],
        device=sim.device,
        dtype=usd_robot.data.joint_pos_limits.dtype,
    )
    contract_limit_error = float(
        torch.max(torch.abs(usd_robot.data.joint_pos_limits[0] - expected_limits)).item()
    )
    check(
        contract_limit_error <= LIMIT_TOLERANCE_RAD,
        "usd_contract_joint_limits",
        f"max_abs_error_rad={contract_limit_error:.3e}",
        failures,
    )

    urdf_mass = float(urdf_robot.data.default_mass[0].sum().item())
    usd_mass = float(usd_robot.data.default_mass[0].sum().item())
    mass_error = abs(urdf_mass - usd_mass)
    check(
        mass_error <= MASS_TOLERANCE_KG,
        "total_mass_equivalence",
        f"urdf_kg={urdf_mass:.12g},usd_kg={usd_mass:.12g},error_kg={mass_error:.3e}",
        failures,
    )

    zero_velocity = torch.zeros((1, len(GLUON_JOINT_NAMES)), device=sim.device)
    sample_poses: dict[str, dict[str, tuple[torch.Tensor, torch.Tensor]]] = {}
    for sample_name, sample_deg in SAMPLES_DEG.items():
        joint_position = torch.deg2rad(torch.tensor([sample_deg], device=sim.device))
        for robot in (urdf_robot, usd_robot):
            robot.write_joint_state_to_sim(joint_position, zero_velocity)
            robot.reset()
        sim.forward()
        urdf_robot.update(0.0)
        usd_robot.update(0.0)

        urdf_pose = end_effector_pose_base(urdf_robot)
        usd_pose = end_effector_pose_base(usd_robot)
        sample_poses[sample_name] = {"urdf": urdf_pose, "usd": usd_pose}
        position_error = float(torch.linalg.vector_norm(urdf_pose[0] - usd_pose[0]).item())
        orientation_error = float(quaternion_distance(urdf_pose[1], usd_pose[1]).item())
        check(
            position_error <= POSITION_TOLERANCE_M,
            f"{sample_name}_ee_position",
            f"error_m={position_error:.3e},urdf={urdf_pose[0][0].cpu().tolist()},"
            f"usd={usd_pose[0][0].cpu().tolist()}",
            failures,
        )
        check(
            orientation_error <= ORIENTATION_TOLERANCE_RAD,
            f"{sample_name}_ee_orientation",
            f"error_deg={math.degrees(orientation_error):.6f}",
            failures,
        )

    for label in ("urdf", "usd"):
        q0_position, q0_quaternion = sample_poses["q0"][label]
        q6_position, q6_quaternion = sample_poses["q6_test"][label]
        q6_position_delta = float(torch.linalg.vector_norm(q6_position - q0_position).item())
        q6_orientation_delta = float(quaternion_distance(q6_quaternion, q0_quaternion).item())
        check(
            q6_position_delta <= POSITION_TOLERANCE_M,
            f"{label}_q6_position_invariance",
            f"delta_m={q6_position_delta:.3e}",
            failures,
        )
        check(
            abs(q6_orientation_delta - math.radians(30.0)) <= ORIENTATION_TOLERANCE_RAD,
            f"{label}_q6_orientation_change",
            f"delta_deg={math.degrees(q6_orientation_delta):.6f},expected_deg=30",
            failures,
        )

    print(f"summary,failures={len(failures)}", flush=True)
    if failures:
        print("GLUON_URDF_USD_EQUIVALENCE: FAIL", flush=True)
        for failure in failures:
            print(f"- {failure}", flush=True)
        raise SystemExit(1)
    print("GLUON_URDF_USD_EQUIVALENCE: PASS", flush=True)


if __name__ == "__main__":
    try:
        main()
    finally:
        simulation_app.close(skip_cleanup=True)
