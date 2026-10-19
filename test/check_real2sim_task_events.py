"""TRAINING_SIM (environment check): verify the real-to-sim task variant's randomization in a live env.

Creates the registered task with the FlashSAC config path (``apply_env_cfg``), resets it, and checks:
- leg Kp/Kd = default * shared scale * per-joint jitter within the configured bounds, shared factor
  visible as a high across-joint correlation of log(Kp) (theory ~0.77 for the default ranges);
- wheel Kp/Kd still follow the previous independent +-20 % variation;
- PhysX DOF friction [static, dynamic, viscous] within the configured ranges per joint group;
- a few zero-action steps produce finite observations; observation/action sizes stay 33/8 (+critic).
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--task', default='DDT-Velocity-Flat-Tita-My-Real2Sim-v0')
    parser.add_argument('--num-envs', type=int, default=256)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--kp-range', type=float, nargs=2, default=[0.4, 1.26],
                        help='expected leg Kp/Kd scale bounds (shared factor x jitter)')
    parser.add_argument('--expect-nominal-fraction', type=float, default=None,
                        help='check the fraction of envs whose shared leg factor is exactly 1.0 (+-0.08)')
    args = parser.parse_args()
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
        legs, wheels = robot.actuators['legs'], robot.actuators['wheels']
        kp, kd = legs.stiffness / 60.0, legs.damping / 1.5
        wkp_default = robot.data.default_joint_stiffness[:, wheels.joint_indices]
        wkd = wheels.damping / 0.5
        log_kp = torch.log(kp)
        corr = torch.corrcoef(log_kp.T)
        off_diag = corr[~torch.eye(corr.shape[0], dtype=torch.bool)]
        props = robot.root_physx_view.get_dof_friction_properties()
        leg_ids = robot.find_joints('.*_leg_[1-3]')[0]
        wheel_ids = robot.find_joints('.*_leg_4')[0]
        leg_f, wheel_f = props[:, leg_ids], props[:, wheel_ids]
        finite = True
        for _ in range(20):
            obs, _, _, _, _ = env.step(torch.zeros(args.num_envs, env.unwrapped.action_manager.total_action_dim))
            finite &= all(torch.isfinite(v).all().item() for v in obs.values())
        report = dict(
            execution_domain='TRAINING_SIM (environment check; no training)', task=args.task, num_envs=args.num_envs,
            obs_dims={k: list(v.shape) for k, v in obs.items()},
            action_dim=int(env.unwrapped.action_manager.total_action_dim),
            leg_kp_scale=dict(min=kp.min().item(), max=kp.max().item(), mean=kp.mean().item()),
            leg_kd_scale=dict(min=kd.min().item(), max=kd.max().item(), mean=kd.mean().item()),
            leg_kp_kd_same_env_ratio_logstd=float(torch.log(kp / kd).std()),
            leg_logkp_across_joint_corr_mean=float(off_diag.mean()),
            wheel_kp_default=float(wkp_default.abs().max()), wheel_kd_scale=dict(min=wkd.min().item(), max=wkd.max().item()),
            leg_friction=dict(static_min=leg_f[..., 0].min().item(), static_max=leg_f[..., 0].max().item(),
                              dynamic_over_static_max=float((leg_f[..., 1] / leg_f[..., 0].clamp(min=1e-9)).max()),
                              viscous_max=leg_f[..., 2].max().item()),
            wheel_friction=dict(static_min=wheel_f[..., 0].min().item(), static_max=wheel_f[..., 0].max().item(),
                                dynamic_over_static_max=float((wheel_f[..., 1] / wheel_f[..., 0].clamp(min=1e-9)).max()),
                                viscous_max=wheel_f[..., 2].max().item()),
            finite_after_20_steps=bool(finite))
        sums = env.unwrapped.reward_manager._episode_sums
        report['reward_episode_sums_env_mean'] = {k: float(v.mean()) for k, v in sums.items()}
        report['reward_terms_finite'] = all(bool(torch.isfinite(v).all()) for v in sums.values())
        shared = getattr(robot, 'real2sim_leg_output_scale', None)
        if shared is not None:
            report['leg_shared_factor'] = dict(nominal_fraction=float((shared == 1.0).float().mean()),
                                               min=float(shared.min()), max=float(shared.max()))
        checks = dict(
            policy_obs_33=report['obs_dims']['policy'][-1] == 33, action_8=report['action_dim'] == 8,
            leg_kp_bounds=args.kp_range[0] - 1e-4 <= report['leg_kp_scale']['min'] and report['leg_kp_scale']['max'] <= args.kp_range[1] + 1e-4,
            leg_kd_bounds=args.kp_range[0] - 1e-4 <= report['leg_kd_scale']['min'] and report['leg_kd_scale']['max'] <= args.kp_range[1] + 1e-4,
            leg_shared_factor=report['leg_logkp_across_joint_corr_mean'] > 0.6,
            wheel_kd_bounds=0.8 - 1e-4 <= report['wheel_kd_scale']['min'] and report['wheel_kd_scale']['max'] <= 1.2 + 1e-4,
            leg_friction_bounds=report['leg_friction']['static_min'] >= 0 and report['leg_friction']['static_max'] <= 4.0 + 1e-5,
            wheel_friction_bounds=report['wheel_friction']['static_min'] >= 0 and report['wheel_friction']['static_max'] <= 0.4 + 1e-5,
            dynamic_le_static=max(report['leg_friction']['dynamic_over_static_max'],
                                  report['wheel_friction']['dynamic_over_static_max']) <= 1.0 + 1e-5,
            no_viscous=max(report['leg_friction']['viscous_max'], report['wheel_friction']['viscous_max']) == 0.0,
            finite=report['finite_after_20_steps'], reward_terms_finite=report['reward_terms_finite'])
        if args.expect_nominal_fraction is not None:
            checks['nominal_fraction'] = abs(report['leg_shared_factor']['nominal_fraction']
                                             - args.expect_nominal_fraction) <= 0.08
        report['checks'] = {k: bool(v) for k, v in checks.items()}
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
