#!/usr/bin/env python3
"""P0 headless runtime validation for the GLUON 2L6/4L3 IsaacLab asset."""

import argparse
import hashlib
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
    GLUON_2L6_4L3_USD_PATH,
    GLUON_BODY_NAMES,
    GLUON_END_EFFECTOR_BODY,
    GLUON_EXPECTED_TOTAL_MASS_KG,
    GLUON_JOINT_NAMES,
)


MODEL_ROOT = REPO_ROOT / "sim2sim" / "robot" / "gluon"
MODEL_CONTRACT_PATH = MODEL_ROOT / "config" / "model_contract.json"
POSITION_TOLERANCE_M = 1.0e-3
MASS_TOLERANCE_KG = 1.0e-5
ROOT_DRIFT_TOLERANCE_M = 1.0e-6
LIMIT_TOLERANCE_RAD = 1.0e-6


def check(condition: bool, label: str, detail: str, failures: list[str]) -> None:
    status = "PASS" if condition else "FAIL"
    print(f"check,status={status},name={label},{detail}", flush=True)
    if not condition:
        failures.append(f"{label}: {detail}")


def main() -> None:
    failures: list[str] = []
    contract = json.loads(MODEL_CONTRACT_PATH.read_text(encoding="utf-8"))
    interface = contract["interface_v1"]
    sim_urdf_info = contract["sim_urdf"]
    expected_urdf_path = MODEL_ROOT / sim_urdf_info["relative_path"]
    actual_sha256 = hashlib.sha256(expected_urdf_path.read_bytes()).hexdigest()
    manifest_path = MODEL_ROOT / "usd" / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    expected_usd_path = REPO_ROOT / manifest["output_usd"]["relative_path"]
    actual_usd_sha256 = hashlib.sha256(expected_usd_path.read_bytes()).hexdigest()

    check(
        GLUON_2L6_4L3_URDF_PATH.resolve() == expected_urdf_path.resolve(),
        "asset_path",
        f"asset={GLUON_2L6_4L3_URDF_PATH},contract={expected_urdf_path}",
        failures,
    )
    check(
        actual_sha256 == sim_urdf_info["sha256"],
        "sim_urdf_sha256",
        f"actual={actual_sha256},contract={sim_urdf_info['sha256']}",
        failures,
    )
    check(
        GLUON_2L6_4L3_USD_PATH.resolve() == expected_usd_path.resolve(),
        "asset_usd_path",
        f"asset={GLUON_2L6_4L3_USD_PATH},manifest={expected_usd_path}",
        failures,
    )
    check(
        actual_usd_sha256 == manifest["output_usd"]["sha256"],
        "asset_usd_sha256",
        f"actual={actual_usd_sha256},manifest={manifest['output_usd']['sha256']}",
        failures,
    )
    check(
        list(GLUON_JOINT_NAMES) == interface["joint_names"],
        "asset_contract_joint_names",
        f"asset={list(GLUON_JOINT_NAMES)},contract={interface['joint_names']}",
        failures,
    )

    sim = SimulationContext(sim_utils.SimulationCfg(device=args_cli.device, dt=0.005))
    robot_cfg = GLUON_2L6_4L3_CFG.copy()
    robot_cfg.prim_path = "/World/Gluon"
    robot = Articulation(robot_cfg)

    sim.reset()
    robot.update(sim.get_physics_dt())

    check(robot.is_fixed_base, "fixed_base", f"value={robot.is_fixed_base}", failures)
    check(
        tuple(robot.joint_names) == GLUON_JOINT_NAMES,
        "runtime_joint_order",
        f"runtime={robot.joint_names},expected={list(GLUON_JOINT_NAMES)}",
        failures,
    )
    check(
        tuple(robot.body_names) == GLUON_BODY_NAMES,
        "runtime_body_order",
        f"runtime={robot.body_names},expected={list(GLUON_BODY_NAMES)}",
        failures,
    )
    check(
        GLUON_END_EFFECTOR_BODY in robot.body_names,
        "end_effector_body",
        f"name={GLUON_END_EFFECTOR_BODY},bodies={robot.body_names}",
        failures,
    )

    expected_limits = torch.tensor(
        [interface["joint_soft_limits_rad"][name] for name in GLUON_JOINT_NAMES],
        device=sim.device,
        dtype=robot.data.joint_pos_limits.dtype,
    )
    runtime_limits = robot.data.joint_pos_limits[0]
    limit_error = float(torch.max(torch.abs(runtime_limits - expected_limits)).item())
    check(
        limit_error <= LIMIT_TOLERANCE_RAD,
        "runtime_joint_limits",
        f"max_abs_error_rad={limit_error:.3e},limits={runtime_limits.detach().cpu().tolist()}",
        failures,
    )

    joint6_index = robot.joint_names.index("axis_joint_6")
    joint6_limits = runtime_limits[joint6_index].detach().cpu().tolist()
    expected_joint6_limits = interface["joint_soft_limits_rad"]["axis_joint_6"]
    check(
        max(abs(a - b) for a, b in zip(joint6_limits, expected_joint6_limits, strict=True))
        <= LIMIT_TOLERANCE_RAD,
        "joint6_limits_150_deg",
        f"runtime={joint6_limits},expected={expected_joint6_limits}",
        failures,
    )

    total_mass = float(robot.data.default_mass[0].sum().item())
    expected_mass = float(contract["urdf"]["expected_total_mass_kg"])
    check(
        math.isclose(total_mass, expected_mass, rel_tol=0.0, abs_tol=MASS_TOLERANCE_KG),
        "total_mass",
        f"runtime_kg={total_mass:.12g},contract_kg={expected_mass:.12g}",
        failures,
    )
    check(
        math.isclose(
            GLUON_EXPECTED_TOTAL_MASS_KG,
            expected_mass,
            rel_tol=0.0,
            abs_tol=1.0e-12,
        ),
        "asset_contract_mass",
        f"asset_kg={GLUON_EXPECTED_TOTAL_MASS_KG:.12g},contract_kg={expected_mass:.12g}",
        failures,
    )

    zero_position = torch.zeros_like(robot.data.joint_pos)
    zero_velocity = torch.zeros_like(robot.data.joint_vel)
    robot.write_joint_state_to_sim(zero_position, zero_velocity)
    robot.reset()
    robot.update(sim.get_physics_dt())
    initial_root_position = robot.data.root_link_pos_w.clone()

    for _ in range(200):
        robot.set_joint_position_target(zero_position)
        robot.write_data_to_sim()
        sim.step(render=False)
        robot.update(sim.get_physics_dt())

    finite_tensors = (
        robot.data.joint_pos,
        robot.data.joint_vel,
        robot.data.body_link_pose_w,
        robot.data.default_mass,
        robot.data.default_inertia,
    )
    finite_state = all(torch.isfinite(value).all().item() for value in finite_tensors)
    check(finite_state, "finite_runtime_state", f"value={finite_state}", failures)

    root_drift = float(torch.linalg.vector_norm(robot.data.root_link_pos_w - initial_root_position).item())
    check(
        root_drift <= ROOT_DRIFT_TOLERANCE_M,
        "fixed_base_root_drift",
        f"drift_m={root_drift:.3e}",
        failures,
    )

    ee_index = robot.body_names.index(GLUON_END_EFFECTOR_BODY)
    ee_position_base, _ = subtract_frame_transforms(
        robot.data.root_link_pos_w,
        robot.data.root_link_quat_w,
        robot.data.body_link_pos_w[:, ee_index],
        robot.data.body_link_quat_w[:, ee_index],
    )
    expected_ee_position = torch.tensor(
        interface["home_end_effector_position_base_m"],
        device=sim.device,
        dtype=ee_position_base.dtype,
    )
    ee_position_error = float(
        torch.linalg.vector_norm(ee_position_base[0] - expected_ee_position).item()
    )
    check(
        ee_position_error <= POSITION_TOLERANCE_M,
        "home_ee_position_base",
        f"runtime_m={ee_position_base[0].detach().cpu().tolist()},"
        f"contract_m={interface['home_end_effector_position_base_m']},"
        f"error_m={ee_position_error:.3e}",
        failures,
    )

    print(f"summary,failures={len(failures)}", flush=True)
    if failures:
        print("GLUON_P0_RUNTIME: FAIL", flush=True)
        for failure in failures:
            print(f"- {failure}", flush=True)
        raise SystemExit(1)
    print("GLUON_P0_RUNTIME: PASS", flush=True)


if __name__ == "__main__":
    try:
        main()
    finally:
        simulation_app.close(skip_cleanup=True)
