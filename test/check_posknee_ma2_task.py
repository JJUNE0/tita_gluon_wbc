"""TRAINING_SIM (environment check): live checks of ``DDT-Velocity-Flat-Tita-My-PosKneeMA2-v0`` before training.

Creates the task through the FlashSAC config path (``apply_env_cfg``) and checks:
- policy observation 34 (33 + ``wheel_position_error``), actions 8, and the policy-interface dump;
- actuator groups:
  - legs (hip/shoulder) 60/1.5 x +-20 % independent;
  - knees 92/2.3 x shared log-U[0.55, 1.0] x jitter 0.8-1.2;
  - wheels Kd 0.5 x +-20 %;
- base-only CoM offsets within +-1.5 cm;
- MA2: applied leg targets = default + scale * mean(current, previous raw action), first step raw, wheels raw;
- wheel_position_error:
  - 0 while a command is active;
  - latched near 0 at zero command;
  - its change matches ground-truth wheel-centre displacement along heading.

No training. Run with the Isaac Lab interpreter.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import traceback
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
TASK = 'DDT-Velocity-Flat-Tita-My-PosKneeMA2-v0'


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--num-envs', type=int, default=128)
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
        from ddt_lab.policy_interface import save_policy_interface
        from isaaclab_tasks.utils import load_cfg_from_registry, parse_env_cfg

        cfg = parse_env_cfg(TASK, device='cpu', num_envs=args.num_envs)
        load_cfg_from_registry(TASK, 'flash_sac_cfg_entry_point').apply_env_cfg(cfg)
        env = gym.make(TASK, cfg=cfg)
        raw = env.unwrapped
        obs, _ = env.reset()
        robot = raw.scene['robot']
        legs, knees, wheels = robot.actuators['legs'], robot.actuators['knees'], robot.actuators['wheels']
        knee_kp, knee_kd = knees.stiffness / 92.0, knees.damping / 2.3
        leg_kp, leg_kd = legs.stiffness / 60.0, legs.damping / 1.5
        wheel_kd = wheels.damping / 0.5
        coms = robot.root_physx_view.get_coms()[:, :, :3].cpu()
        base_id = robot.find_bodies('base_link')[0][0]
        com_offset = coms[:, base_id] - coms[:, base_id].mean(0)  # spread around the common URDF value
        other_spread = float((coms[:, [i for i in range(coms.shape[1]) if i != base_id]]
                              - coms[:1, [i for i in range(coms.shape[1]) if i != base_id]]).abs().max())
        interface = save_policy_interface(raw, args.output / 'policy_interface.json')

        # MA2 check with deterministic alternating actions on all eight terms.
        manager = raw.action_manager
        terms = {name: manager.get_term(name) for name in manager.active_terms}
        n, dim = args.num_envs, manager.total_action_dim
        a1 = torch.full((n, dim), 0.4)
        a2 = torch.full((n, dim), -0.2)
        env.reset()
        manager.process_action(a1)
        first = {k: t.processed_actions.clone() for k, t in terms.items()}
        manager.process_action(a2)
        second = {k: t.processed_actions.clone() for k, t in terms.items()}
        ma2 = {}
        for name, term in terms.items():
            offset, scale = term._offset, term._scale
            if name.startswith('joint_pos'):
                ok1 = torch.allclose(first[name], offset + scale * 0.4, atol=1e-6)
                ok2 = torch.allclose(second[name], offset + scale * 0.1, atol=1e-6)
            else:
                ok1 = torch.allclose(first[name], offset + scale * 0.4, atol=1e-6)
                ok2 = torch.allclose(second[name], offset + scale * -0.2, atol=1e-6)
            ma2[name] = bool(ok1 and ok2)
        raw_last = torch.allclose(manager.action, a2)

        # Position-error logic on the live term instance with written states (no physics stepping): latch at
        # zero command, wheel/pitch/leg contributions, follow while commanded. The physical sign of the leg
        # correction was checked in MuJoCo (test/sim2real/check_wheel_odometry_sign.py).
        env.reset()
        names = raw.observation_manager.active_terms['policy']
        index = names.index('wheel_position_error')
        term = raw.observation_manager._group_obs_term_cfgs['policy'][index].func
        params = raw.observation_manager._group_obs_term_cfgs['policy'][index].params
        command = raw.command_manager.get_term('base_velocity')
        joint_ids = {j: robot.joint_names.index(j) for j in robot.joint_names}

        def evaluate():
            return term(raw, **params).squeeze(1).clone()

        def set_joints(delta):
            q = robot.data.joint_pos.clone()
            for name, value in delta.items():
                q[:, joint_ids[name]] += value
            robot.write_joint_state_to_sim(q, torch.zeros_like(q))

        command._emitted_command_b[:] = 0.0
        latched = evaluate()
        set_joints({'joint_left_leg_4': 0.1, 'joint_right_leg_4': 0.1})
        wheel_step = evaluate()
        set_joints({'joint_left_leg_2': 0.05, 'joint_right_leg_2': 0.05})
        thigh_step = evaluate() - wheel_step
        command._emitted_command_b[:, 0] = 0.3
        commanded = evaluate()
        set_joints({'joint_left_leg_4': 0.2, 'joint_right_leg_4': 0.2})
        commanded_moving = evaluate()
        command._emitted_command_b[:] = 0.0
        relatched = evaluate()
        set_joints({'joint_left_leg_4': 10.0, 'joint_right_leg_4': 10.0})
        clipped = evaluate()
        radius = term.radius
        position_check = dict(
            latched_abs_max=latched.abs().max().item(),
            wheel_0p1rad_over_radius=dict(min=(wheel_step / (0.1 * radius)).min().item(),
                                          max=(wheel_step / (0.1 * radius)).max().item()),
            thigh_0p05rad_over_radius=dict(min=(thigh_step / (0.05 * radius)).min().item(),
                                           max=(thigh_step / (0.05 * radius)).max().item()),
            radius_scale=dict(min=(radius / 0.0925).min().item(), max=(radius / 0.0925).max().item()),
            commanded_abs_max=max(commanded.abs().max().item(), commanded_moving.abs().max().item()),
            relatched_abs_max=relatched.abs().max().item(),
            clipped_max=clipped.max().item())
        obs, _, _, _, _ = env.step(torch.zeros(n, dim))
        report = dict(
            execution_domain='TRAINING_SIM (environment check; no training)', task=TASK, num_envs=n,
            obs_dims={k: list(v.shape) for k, v in obs.items()}, action_dim=int(dim),
            policy_terms=names, policy_interface_terms=[o['name'] for o in interface['observations']],
            knee_kp_scale=dict(min=knee_kp.min().item(), max=knee_kp.max().item(), mean=knee_kp.mean().item()),
            knee_kd_scale=dict(min=knee_kd.min().item(), max=knee_kd.max().item()),
            leg_kp_scale=dict(min=leg_kp.min().item(), max=leg_kp.max().item()),
            leg_kd_scale=dict(min=leg_kd.min().item(), max=leg_kd.max().item()),
            wheel_kd_scale=dict(min=wheel_kd.min().item(), max=wheel_kd.max().item()),
            knee_joints=list(knees.joint_names), leg_joints=list(legs.joint_names), wheel_joints=list(wheels.joint_names),
            base_com_spread_m=dict(min=com_offset.min(0).values.tolist(), max=com_offset.max(0).values.tolist()),
            other_body_com_spread_m=other_spread,
            ma2_terms_ok=ma2, last_action_raw=bool(raw_last),
            position_error_logic=position_check,
            finite_after_step=bool(all(torch.isfinite(v).all().item() for v in obs.values())))
        (args.output / 'check.json').write_text(json.dumps(report, indent=2) + '\n')
        print(json.dumps(report, indent=1))
        env.close()
    except Exception:
        traceback.print_exc()
        code = 1
    sys.stdout.flush()
    os._exit(code)


if __name__ == '__main__':
    main()
