#!/usr/bin/env python3
"""MuJoCo zero-command drift probe -- headless, ground-truth base position.

Unlike the real hardware log (no base position, only wheel-spin proxies) or
Isaac Lab's ``eval_behavior.py`` (its own physics engine), MuJoCo here gives
an exact ``qpos[0:3]`` world-frame base position, so this is a true meter
measurement of standstill drift, not a proxy. Reuses the same
``TitaMujocoEnv``/``ObservationBuilder``/``ActionAdapter`` deployment pipeline
as the other cosim_ros2_jazzy scripts.

Domain: DESKTOP_DRY_RUN. Offline, no ROS2, no hardware, no live viewer node.
"""
from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import yaml

from cosim_ros2_jazzy.action_adapter import ActionAdapter
from cosim_ros2_jazzy.mujoco_env import TitaMujocoEnv
from cosim_ros2_jazzy.obs_builder import ObsState, ObservationBuilder


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    parser.add_argument("--settle_s", type=float, default=1.0)
    parser.add_argument("--hold_s", type=float, default=10.0)
    parser.add_argument("--walk_vx", type=float, default=0.0, help="If >0, walk forward at this vx before stopping.")
    parser.add_argument("--walk_ramp_s", type=float, default=1.0)
    parser.add_argument("--walk_cruise_s", type=float, default=3.0)
    parser.add_argument("--walk_decel_s", type=float, default=1.5)
    parser.add_argument("--checkpoint_every_s", type=float, default=5.0, help="Print drift-so-far at this cadence.")
    args = parser.parse_args()

    import onnxruntime as ort

    with open(Path(args.config).expanduser(), "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    cfg["viewer"]["enabled"] = False
    cfg["control"]["real_time"] = False

    env = TitaMujocoEnv(cfg, viewer_enabled=False)
    env.reset()
    obs_builder = ObservationBuilder(cfg)
    adapter = ActionAdapter(cfg)
    session = ort.InferenceSession(cfg["policy"]["path"], providers=["CPUExecutionProvider"])
    input_name = cfg["policy"]["input_obs_name"]
    obs_dim = int(cfg["policy"]["obs_dim"])
    action_dim = int(cfg["policy"]["action_dim"])
    joint_names = list(cfg["robot"]["joint_names"])
    default_angles = np.asarray(cfg["robot"]["default_joint_angles"], dtype=np.float32)

    policy_dt = env.model.opt.timestep * env.decimation

    def n_steps(seconds: float) -> int:
        return max(1, round(seconds / policy_dt))

    last_action = np.zeros(action_dim, dtype=np.float32)

    def build_obs(cmd_vx: float = 0.0) -> np.ndarray:
        state = ObsState(
            joint_pos=env.joint_pos(),
            joint_vel=env.joint_vel(),
            base_quat_wxyz=env.base_quat_sensor(),
            base_ang_vel=env.base_ang_vel(),
            command=np.array([cmd_vx, 0.0, 0.0], dtype=np.float32),
            last_action=last_action,
        )
        return obs_builder.build(state)

    init_obs = build_obs()
    obs_builder.reset_history(init_obs)

    def run_phase(count: int, record: bool, cmd_fn=lambda i: 0.0) -> list[dict]:
        nonlocal last_action
        rows = []
        for i in range(count):
            obs = build_obs(float(cmd_fn(i)))
            action = session.run(None, {input_name: obs.reshape(1, obs_dim).astype(np.float32)})[0]
            action = np.asarray(action, dtype=np.float32).reshape(action_dim)

            def torque_callback(jp, jv, _action=action):
                t, _ = adapter.compute(_action, jp, jv)
                return t

            env.step_with_torque_callback(torque_callback, sleep=False)
            obs_builder.push_history(obs)
            _, debug = adapter.compute(action, env.joint_pos(), env.joint_vel())
            last_action = debug.action_raw_by_joint.astype(np.float32)
            if record:
                rows.append({"t": i * policy_dt, "base_pos": env.base_pos().copy(), "joint_pos": env.joint_pos().copy()})
        return rows

    run_phase(n_steps(args.settle_s), record=False)

    if args.walk_vx > 0.0:
        ramp_n = n_steps(args.walk_ramp_s)
        run_phase(ramp_n, record=False, cmd_fn=lambda i: args.walk_vx * (i + 1) / ramp_n)
        run_phase(n_steps(args.walk_cruise_s), record=False, cmd_fn=lambda i: args.walk_vx)
        decel_n = n_steps(args.walk_decel_s)
        run_phase(decel_n, record=False, cmd_fn=lambda i: args.walk_vx * (1 - (i + 1) / decel_n))

    start_pos = env.base_pos().copy()
    rows = run_phase(n_steps(args.hold_s), record=True)

    final_pos = rows[-1]["base_pos"]
    disp = final_pos - start_pos
    disp_xy = float(np.linalg.norm(disp[:2]))

    print("=" * 70)
    print(f"[RESULT] config={args.config}")
    print(f"[RESULT] policy={cfg['policy']['path']}")
    if args.walk_vx > 0.0:
        print(f"[RESULT] pre-phase: walked at {args.walk_vx} m/s, then decelerated to 0, THEN held zero-command")
    print("-" * 70)
    print(f"zero-command hold ({args.hold_s:.1f}s), ground-truth MuJoCo base position:")
    print(f"  start xyz = {start_pos.tolist()}")
    print(f"  final xyz = {final_pos.tolist()}")
    print(f"  displacement dx={disp[0]:+.4f} dy={disp[1]:+.4f} dz={disp[2]:+.4f} m")
    print(f"  planar |xy| drift = {disp_xy:.4f} m  (mean vx-equiv = {disp_xy/args.hold_s:.4f} m/s)")
    print("-" * 70)
    print("drift-so-far checkpoints:")
    ckpt_every_n = max(1, round(args.checkpoint_every_s / policy_dt))
    for i in range(ckpt_every_n - 1, len(rows), ckpt_every_n):
        d = np.linalg.norm(rows[i]["base_pos"][:2] - start_pos[:2])
        print(f"  t={rows[i]['t']:.1f}s  drift so far = {d:.4f} m")
    print("-" * 70)
    print(f"{'joint':<20}{'default':>10}{'final':>10}{'delta':>10}{'max|delta|':>12}")
    joint_pos_seq = np.stack([r["joint_pos"] for r in rows], axis=0)  # (T, 8)
    final_jp = joint_pos_seq[-1]
    max_dev = np.max(np.abs(joint_pos_seq - default_angles[None, :]), axis=0)
    for i, name in enumerate(joint_names):
        print(
            f"{name:<20}{default_angles[i]:>10.4f}{final_jp[i]:>10.4f}"
            f"{final_jp[i]-default_angles[i]:>10.4f}{max_dev[i]:>12.4f}"
        )

    z_seq = np.array([r["base_pos"][2] for r in rows])
    print("-" * 70)
    print(
        f"[SUMMARY] config={Path(args.config).stem} walk_vx={args.walk_vx} hold_s={args.hold_s} "
        f"drift_final_m={disp_xy:.4f} z_start={z_seq[0]:.4f} z_min={z_seq.min():.4f} "
        f"z_max={z_seq.max():.4f} z_final={z_seq[-1]:.4f}"
    )
    print("=" * 70)

    env.close()


if __name__ == "__main__":
    main()
