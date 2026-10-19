"""TRAINING_SIM (environment check): verify the CoM-only task variant in a live env.

Checks after the startup event that (1) the base_link CoM equals its URDF value plus a sample from
x [-0.055, -0.015], y [-0.02, 0.02], z [-0.03, 0.03] m, (2) every other body's CoM is identical
across environments (no per-body CoM randomization any more), (3) policy/critic/action sizes are
unchanged and a few zero-action steps stay finite.
"""

from __future__ import annotations

import argparse
import json
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
URDF = REPO / 'tita_gluon_ws/src/ddt_ros2_control/urdfs/tita_description/urdf/robot.urdf'
RANGE = dict(x=(-0.055, -0.015), y=(-0.02, 0.02), z=(-0.03, 0.03))


def urdf_base_com():
    for link in ET.parse(URDF).getroot().findall('link'):
        if link.get('name') == 'base_link':
            return [float(v) for v in link.find('inertial').find('origin').get('xyz').split()]
    raise RuntimeError('base_link inertial not found')


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--task', default='DDT-Velocity-Flat-Tita-My-BaseComShift-v0')
    parser.add_argument('--num-envs', type=int, default=256)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--x-range', type=float, nargs=2, default=list(RANGE['x']), help='expected base CoM x offset range [m]')
    parser.add_argument('--y-range', type=float, nargs=2, default=list(RANGE['y']))
    parser.add_argument('--z-range', type=float, nargs=2, default=list(RANGE['z']))
    args = parser.parse_args()
    RANGE['x'], RANGE['y'], RANGE['z'] = tuple(args.x_range), tuple(args.y_range), tuple(args.z_range)
    args.output.mkdir(parents=True, exist_ok=True)
    sys.path.insert(0, str(REPO / 'lab/ddt_lab/scripts/flash_sac'))
    from runtime import setup_imports
    setup_imports(False)
    from isaaclab.app import AppLauncher

    app = AppLauncher(headless=True, device='cpu').app
    try:
        import gymnasium as gym
        import torch
        import ddt_lab.tasks  # noqa: F401
        from isaaclab_tasks.utils import load_cfg_from_registry, parse_env_cfg

        cfg = parse_env_cfg(args.task, device='cpu', num_envs=args.num_envs)
        load_cfg_from_registry(args.task, 'flash_sac_cfg_entry_point').apply_env_cfg(cfg)
        env = gym.make(args.task, cfg=cfg)
        obs, _ = env.reset()
        robot = env.unwrapped.scene['robot']
        coms = robot.root_physx_view.get_coms()[..., :3]  # (envs, bodies, xyz) in body frames
        names = robot.body_names
        base = names.index('base_link')
        nominal = torch.tensor(urdf_base_com())
        offset = coms[:, base] - nominal
        others = [i for i in range(len(names)) if i != base]
        other_spread = float((coms[:, others].max(0).values - coms[:, others].min(0).values).abs().max())
        finite = True
        for _ in range(20):
            obs, _, _, _, _ = env.step(torch.zeros(args.num_envs, env.unwrapped.action_manager.total_action_dim))
            finite &= all(torch.isfinite(v).all().item() for v in obs.values())
        stats = {axis: dict(min=float(offset[:, i].min()), max=float(offset[:, i].max()), mean=float(offset[:, i].mean()))
                 for i, axis in enumerate('xyz')}
        checks = {f'base_offset_{a}_in_range': RANGE[a][0] - 1e-4 <= stats[a]['min'] and stats[a]['max'] <= RANGE[a][1] + 1e-4
                  for a in 'xyz'}
        checks.update(base_offset_x_mean_near_centre=abs(stats['x']['mean'] - sum(RANGE['x']) / 2) < 0.004,
                      other_bodies_not_randomized=other_spread < 1e-6,
                      policy_obs_33=obs['policy'].shape[-1] == 33, critic_obs_36=obs['critic'].shape[-1] == 36,
                      action_8=env.unwrapped.action_manager.total_action_dim == 8, finite_after_20_steps=bool(finite))
        report = dict(execution_domain='TRAINING_SIM (environment check; no training)', task=args.task,
                      num_envs=args.num_envs, body_names=names, urdf_base_com=nominal.tolist(),
                      base_com_offset_stats=stats, other_bodies_max_spread_m=other_spread,
                      checks={k: bool(v) for k, v in checks.items()})
        report['evidence_status'] = 'PASS' if all(report['checks'].values()) else 'FAIL'
        (args.output / 'event_check.json').write_text(json.dumps(report, indent=2) + '\n')
        print('[TRAINING_SIM] ' + json.dumps(report, indent=1))
        env.close()
    except Exception:
        import traceback
        traceback.print_exc()
        raise
    finally:
        sys.stdout.flush()
        sys.stderr.flush()
        import os
        os._exit(0)  # SimulationApp.close() can hang on this machine; outputs are flushed above


if __name__ == '__main__':
    main()
