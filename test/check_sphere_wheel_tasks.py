"""TRAINING_SIM (environment check): 2026-10-18 sphere-wheel experiment tasks before training.

For each task, creates it through the FlashSAC config path (``apply_env_cfg``) and checks:
- wheel collision prims in the spawned USD are spheres (radius 0.0925), other collisions unchanged;
- policy observation 34, action 8;
- leg action terms: MA2 (exp 1, 3) or plain joint position (exp 2); wheels unchanged;
- command ranges (exp 3: lin_vel_x +-1.5, ang_vel_z +-3.0);
- 30 random-action steps stay finite.
Reference task ``DDT-Velocity-Flat-Tita-My-PosKneeMA2-v0`` is reported for comparison (cylinder wheels).
No training. Run with the Isaac Lab interpreter.
"""

from __future__ import annotations

import argparse
import json
import sys
import traceback
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
TASKS = {
    'DDT-Velocity-Flat-Tita-My-PosKneeMA2-v0': dict(shape='Cylinder', ma2=True, lin=(-1.0, 1.0), ang=(-1.5, 1.5)),
    'DDT-Velocity-Flat-Tita-My-PosKneeMA2-Sphere-v0': dict(shape='Sphere', ma2=True, lin=(-1.0, 1.0), ang=(-1.5, 1.5)),
    'DDT-Velocity-Flat-Tita-My-PosKnee-Sphere-v0': dict(shape='Sphere', ma2=False, lin=(-1.0, 1.0), ang=(-1.5, 1.5)),
    'DDT-Velocity-Flat-Tita-My-PosKneeMA2-Sphere-Fast-v0': dict(shape='Sphere', ma2=True, lin=(-1.5, 1.5), ang=(-3.0, 3.0),
                                                                ramp=1000.0),
    'DDT-Velocity-Flat-Tita-My-PosKnee-Sphere-Fast-v0': dict(shape='Sphere', ma2=False, lin=(-1.5, 1.5), ang=(-3.0, 3.0),
                                                             ramp=1000.0),
    'DDT-Velocity-Flat-Tita-My-PosKnee-v0': dict(shape='Cylinder', ma2=False, lin=(-1.0, 1.0), ang=(-1.5, 1.5)),
}
LEGS = ('joint_pos_0', 'joint_pos_1', 'joint_pos_2', 'joint_pos_4', 'joint_pos_5', 'joint_pos_6')


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--task', choices=list(TASKS), required=True)
    parser.add_argument('--num-envs', type=int, default=16)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    sys.path.insert(0, str(REPO / 'lab/ddt_lab/scripts/flash_sac'))
    from runtime import setup_imports
    setup_imports(False)
    from isaaclab.app import AppLauncher

    app = AppLauncher(headless=True, device='cpu').app
    code = 0
    try:
        import gymnasium as gym
        import torch
        import ddt_lab.tasks  # noqa: F401
        from isaaclab_tasks.utils import load_cfg_from_registry, parse_env_cfg
        from pxr import Usd, UsdGeom
        import isaacsim.core.utils.stage as stage_utils

        expect = TASKS[args.task]
        cfg = parse_env_cfg(args.task, device='cpu', num_envs=args.num_envs)
        load_cfg_from_registry(args.task, 'flash_sac_cfg_entry_point').apply_env_cfg(cfg)
        env = gym.make(args.task, cfg=cfg)
        raw = env.unwrapped
        obs, _ = env.reset()
        stage = stage_utils.get_current_stage()
        shapes = {}
        # URDF import makes instanceable collision prims; include instance proxies.
        for prim in Usd.PrimRange(stage.GetPseudoRoot(), Usd.TraverseInstanceProxies()):
            path = str(prim.GetPath())
            if not path.startswith('/World/envs/env_0/Robot/') or 'collision' not in path.lower():
                continue
            if prim.IsA(UsdGeom.Gprim):
                link = path.split('/')[5]
                entry = dict(type=prim.GetTypeName(), path=path)
                if prim.IsA(UsdGeom.Sphere):
                    entry['radius'] = float(UsdGeom.Sphere(prim).GetRadiusAttr().Get())
                if prim.IsA(UsdGeom.Cylinder):
                    entry['radius'] = float(UsdGeom.Cylinder(prim).GetRadiusAttr().Get())
                    entry['height'] = float(UsdGeom.Cylinder(prim).GetHeightAttr().Get())
                shapes.setdefault(link, []).append(entry)
        manager = raw.action_manager
        leg_classes = {name: type(manager.get_term(name)).__name__ for name in LEGS}
        wheel_classes = {name: type(manager.get_term(name)).__name__ for name in ('joint_vel_3', 'joint_vel_7')}
        command_cfg = raw.command_manager.get_term('base_velocity').cfg
        ranges = command_cfg.ranges
        policy_obs = obs['policy'] if isinstance(obs, dict) else obs
        finite = True
        for _ in range(30):
            action = torch.rand((args.num_envs, manager.total_action_dim)) * 2 - 1
            obs, *_ = env.step(action)
            o = obs['policy'] if isinstance(obs, dict) else obs
            finite &= bool(torch.isfinite(o).all())
        wheel_shapes = [s for link in ('left_leg_4', 'right_leg_4') for s in shapes.get(link, [])]
        checks = {
            'wheel_collision_shape': all(s['type'] == expect['shape'] for s in wheel_shapes) and len(wheel_shapes) == 2,
            'wheel_radius_0.0925': bool(wheel_shapes) and all(abs(s['radius'] - 0.0925) < 1e-6 for s in wheel_shapes),
            'obs_34': int(policy_obs.shape[-1]) == 34,
            'action_8': int(manager.total_action_dim) == 8,
            'leg_filter': all((c == 'MA2JointPositionAction') == expect['ma2'] for c in leg_classes.values()),
            'wheel_terms_unchanged': all(c == 'JointVelocityAction' for c in wheel_classes.values()),
            'lin_vel_x_range': tuple(ranges.lin_vel_x) == expect['lin'],
            'ang_vel_z_range': tuple(ranges.ang_vel_z) == expect['ang'],
            'ramp_rate': float(command_cfg.ramp_rate) == expect.get('ramp', 0.5),
            'finite_30_steps': finite,
        }
        result = dict(execution_domain='TRAINING_SIM', task=args.task, asset_path=cfg.scene.robot.spawn.asset_path,
                      checks=checks, collision_shapes=shapes, leg_classes=leg_classes, wheel_classes=wheel_classes,
                      ranges=dict(lin_vel_x=list(ranges.lin_vel_x), ang_vel_z=list(ranges.ang_vel_z),
                                  ramp_rate=float(command_cfg.ramp_rate)),
                      evidence_status='PASS' if all(checks.values()) else 'FAIL')
        (args.output / f'{args.task}.json').write_text(json.dumps(result, indent=1))
        print(json.dumps(dict(task=args.task, evidence_status=result['evidence_status'], checks=checks,
                              wheel_shapes=wheel_shapes, leg_classes=sorted(set(leg_classes.values())),
                              asset_path=result['asset_path']), indent=1))
        code = 0 if all(checks.values()) else 1
        env.close()
    except Exception:
        traceback.print_exc()
        code = 2
    finally:
        app.close()
    sys.exit(code)


if __name__ == '__main__':
    main()
