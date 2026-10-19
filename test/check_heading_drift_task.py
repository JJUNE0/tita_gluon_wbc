"""TRAINING_SIM (environment check): ``DDT-Velocity-Flat-Tita-My-PosKneeMA2-Sphere-Fast-Heading-v0`` before training.

Creates the task through the FlashSAC config path and checks:
- policy observation 34 (unchanged interface), critic = experiment-3 critic + 1 (``heading_drift_error``);
- sphere wheels, MA2 legs, commands +-1.5 / +-3.0, ramp 1000 (experiment 3 base);
- ``ZeroCommandHeadingDrift`` by direct state writes (no policy, so no stepping-based balance needed):
  no reward before warmup, anchor at warmup, +0.2 rad root yaw -> error 0.2 and reward exp(-5 * 0.2),
  a non-zero command drops the anchor, the error wraps across +-pi, reset clears it;
- the critic observation equals the reward's heading error (times scale 2);
- 30 random-action steps stay finite.
No training. Run with the Isaac Lab interpreter.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
import traceback
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
TASK = 'DDT-Velocity-Flat-Tita-My-PosKneeMA2-Sphere-Fast-Heading-v0'
BASE = 'DDT-Velocity-Flat-Tita-My-PosKneeMA2-Sphere-Fast-v0'


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--num-envs', type=int, default=8)
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
        from ddt_lab.tasks.manager_based.locomotion.robots.tita.real2sim import observations as obs_mod

        base_cfg = parse_env_cfg(BASE, device='cpu', num_envs=args.num_envs)
        cfg = parse_env_cfg(TASK, device='cpu', num_envs=args.num_envs)
        load_cfg_from_registry(TASK, 'flash_sac_cfg_entry_point').apply_env_cfg(cfg)
        base_critic_terms = [k for k, v in base_cfg.observations.critic.to_dict().items() if isinstance(v, dict) and 'func' in v]
        env = gym.make(TASK, cfg=cfg)
        raw = env.unwrapped
        env.reset()
        dims = raw.observation_manager.group_obs_dim
        critic_terms = raw.observation_manager.active_terms['critic']
        rm = raw.reward_manager
        term_cfg = rm.get_term_cfg('zero_command_heading_drift')
        term, params = term_cfg.func, term_cfg.params
        robot = raw.scene['robot']
        command = raw.command_manager.get_term('base_velocity')
        n = args.num_envs
        checks = {}

        def zero_command():
            command.vel_command_b[:] = 0.0
            command._emitted_command_b[:] = 0.0

        def call():
            return term(raw, **params)

        def refresh():
            raw.scene.write_data_to_sim()
            raw.sim.step(render=False)
            raw.scene.update(raw.physics_dt)

        def set_yaw(env_id, yaw_delta):
            pose = torch.cat([robot.data.root_pos_w, robot.data.root_quat_w], dim=1).clone()
            half = yaw_delta / 2.0
            rz = torch.tensor([math.cos(half), 0.0, 0.0, math.sin(half)])
            w1, x1, y1, z1 = rz
            w2, x2, y2, z2 = pose[env_id, 3:7]
            pose[env_id, 3:7] = torch.stack([w1 * w2 - x1 * x2 - y1 * y2 - z1 * z2, w1 * x2 + x1 * w2 + y1 * z2 - z1 * y2,
                                             w1 * y2 - x1 * z2 + y1 * w2 + z1 * x2, w1 * z2 + x1 * y2 - y1 * x2 + z1 * w2])
            robot.write_root_pose_to_sim(pose[env_id:env_id + 1], env_ids=torch.tensor([env_id]))

        upright = torch.clamp(-robot.data.projected_gravity_b[:, 2], 0, 0.7) / 0.7
        zero_command()
        term.reset(None)
        rewards = [call() for _ in range(term.warmup_steps - 1)]
        checks['no_reward_before_warmup'] = bool(all((r == 0).all() for r in rewards)) and not term.anchor_set.any()
        r = call()
        checks['anchor_at_warmup'] = bool(term.anchor_set.all()) and bool(torch.allclose(r, upright, atol=1e-5))
        set_yaw(0, 0.2)
        refresh()
        zero_command()
        upright = torch.clamp(-robot.data.projected_gravity_b[:, 2], 0, 0.7) / 0.7
        r = call()
        e = term.heading_error.clone()
        checks['yaw_step_error_0.2'] = abs(float(e[0]) - 0.2) < 0.01 and float(e[1:].abs().max()) < 0.01
        checks['yaw_step_reward_exp'] = abs(float(r[0]) - math.exp(-params['sharpness'] * float(e[0])) * float(upright[0])) < 1e-4
        critic_value = obs_mod.heading_drift_error(raw)[:, 0]
        checks['critic_obs_equals_reward_error'] = bool(torch.allclose(critic_value, e))
        command._emitted_command_b[1, 0] = 0.5
        r = call()
        checks['command_drops_anchor'] = (not bool(term.anchor_set[1])) and float(r[1]) == 0.0 and float(term.heading_error[1]) == 0.0
        zero_command()
        yaw = float(torch.atan2(2 * (robot.data.root_quat_w[2, 0] * robot.data.root_quat_w[2, 3]
                                     + robot.data.root_quat_w[2, 1] * robot.data.root_quat_w[2, 2]),
                                1 - 2 * (robot.data.root_quat_w[2, 2] ** 2 + robot.data.root_quat_w[2, 3] ** 2)))
        term.anchor_yaw[2] = yaw - 2 * math.pi + 0.1
        call()
        # yaw - anchor = 2 pi - 0.1, which must wrap to -0.1
        checks['error_wraps_pi'] = abs(float(term.heading_error[2]) + 0.1) < 1e-3
        term.reset(torch.tensor([0]))
        checks['reset_clears'] = float(term.heading_error[0]) == 0.0 and not bool(term.anchor_set[0])
        checks['policy_obs_34'] = int(dims['policy'][0]) == 34
        checks['critic_terms_base_plus_heading'] = critic_terms == base_critic_terms + ['heading_drift_error']
        checks['heading_reward_weight_1'] = float(term_cfg.weight) == 1.0
        command_cfg = command.cfg
        checks['exp3_base'] = (tuple(command_cfg.ranges.lin_vel_x) == (-1.5, 1.5) and tuple(command_cfg.ranges.ang_vel_z) == (-3.0, 3.0)
                               and float(command_cfg.ramp_rate) == 1000.0 and 'sphere_wheels' in cfg.scene.robot.spawn.asset_path
                               and type(raw.action_manager.get_term('joint_pos_0')).__name__ == 'MA2JointPositionAction')
        env.reset()
        finite = True
        for _ in range(30):
            obs, rew, *_ = env.step(torch.rand((n, raw.action_manager.total_action_dim)) * 2 - 1)
            finite &= bool(torch.isfinite(obs['policy']).all() and torch.isfinite(obs['critic']).all() and torch.isfinite(rew).all())
        checks['finite_30_steps'] = finite
        result = dict(execution_domain='TRAINING_SIM', task=TASK, checks=checks, dims={k: list(v) for k, v in dims.items()},
                      critic_terms=critic_terms, base_critic_terms=base_critic_terms, params=params,
                      warmup_steps=term.warmup_steps, evidence_status='PASS' if all(checks.values()) else 'FAIL')
        (args.output / 'heading_task_check.json').write_text(json.dumps(result, indent=1, default=str))
        print(json.dumps(dict(evidence_status=result['evidence_status'], checks=checks, dims=result['dims']), indent=1))
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
