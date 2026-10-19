"""TRAINING_SIM (environment check): ``DDT-Velocity-Flat-Tita-My-PosKneeMA2-Sphere-Fast-HeadingObs-v0`` before training.

Checks (direct calls with a patched yaw-rate source; no policy, so no stepping-based balance needed):
- policy observation 35 with ``heading_error`` last; critic = parent critic + ``heading_error``;
- ``GyroHeadingError``: 0 during warmup, integrates (yaw rate + bias) * step_dt after warmup, output clip
  +-0.5 rad with the internal integral kept, a command outside the zero band resets it, reset clears it,
  per-episode policy bias within +-0.0014 rad/s, critic copy without bias;
- heading drift reward and its critic term are still present; 30 random-action steps stay finite.
No training. Run with the Isaac Lab interpreter.
"""

from __future__ import annotations

import argparse
import json
import sys
import traceback
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
REFERENCE = 'DDT-Velocity-Flat-Tita-My-PosKneeMA2-Sphere-Fast-HeadingObs-v0'
# task -> (critic base task, critic terms added on top, leg MA2, (lin_vel_x max, ang_vel_z max, ramp))
TASKS = {
    REFERENCE: ('DDT-Velocity-Flat-Tita-My-PosKneeMA2-Sphere-Fast-Heading-v0', ['heading_error'], True, (1.5, 3.0, 1000.0)),
    'DDT-Velocity-Flat-Tita-My-PosKnee-Sphere-HeadingObs-v0': (
        'DDT-Velocity-Flat-Tita-My-PosKnee-Sphere-v0', ['heading_drift_error', 'heading_error'], False, (1.0, 1.5, 0.5)),
    'DDT-Velocity-Flat-Tita-My-PosKnee-Sphere-HeadingObsW0-v0': (
        'DDT-Velocity-Flat-Tita-My-PosKnee-Sphere-v0', ['heading_drift_error', 'heading_error'], False, (1.0, 1.5, 0.5)),
}
WARMUP = {'DDT-Velocity-Flat-Tita-My-PosKnee-Sphere-HeadingObsW0-v0': 0.0}  # heading warmup [s]; others 1.0


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--task', choices=list(TASKS), default=REFERENCE)
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

        TASK = args.task
        base_task, added, expect_ma2, (lin_max, ang_max, ramp) = TASKS[TASK]
        base_cfg = parse_env_cfg(base_task, device='cpu', num_envs=args.num_envs)
        base_critic = [k for k, v in base_cfg.observations.critic.to_dict().items() if isinstance(v, dict) and 'func' in v]
        reference_cfg = parse_env_cfg(REFERENCE, device='cpu', num_envs=args.num_envs)
        cfg = parse_env_cfg(TASK, device='cpu', num_envs=args.num_envs)
        load_cfg_from_registry(TASK, 'flash_sac_cfg_entry_point').apply_env_cfg(cfg)
        warmup = WARMUP.get(TASK, 1.0)

        def comparable(term):  # heading cfg without the warmup, which is checked separately
            d = term.to_dict()
            d.get('params', {}).pop('warmup_s', None)
            return json.dumps(d, sort_keys=True, default=str)
        same = lambda a, b: comparable(a) == comparable(b)
        warmups = [cfg.rewards.zero_command_heading_drift.params['warmup_s'], cfg.observations.policy.heading_error.params['warmup_s'],
                   cfg.observations.critic.heading_error.params['warmup_s']]
        heading_terms_same = (same(cfg.rewards.zero_command_heading_drift, reference_cfg.rewards.zero_command_heading_drift)
                              and same(cfg.observations.policy.heading_error, reference_cfg.observations.policy.heading_error)
                              and same(cfg.observations.critic.heading_error, reference_cfg.observations.critic.heading_error)
                              and same(cfg.observations.critic.heading_drift_error, reference_cfg.observations.critic.heading_drift_error))
        env = gym.make(TASK, cfg=cfg)
        raw = env.unwrapped
        env.reset()
        om = raw.observation_manager
        names = om.active_terms
        policy_term = om._group_obs_term_cfgs['policy'][names['policy'].index('heading_error')]
        critic_term = om._group_obs_term_cfgs['critic'][names['critic'].index('heading_error')]
        term, params = policy_term.func, policy_term.params
        command = raw.command_manager.get_term('base_velocity')
        n, dt = args.num_envs, raw.step_dt
        checks = {}

        def zero_command():
            command.vel_command_b[:] = 0.0
            command._emitted_command_b[:] = 0.0

        rate = 0.1
        term._yaw_rate = lambda: torch.full((n,), rate)
        zero_command()
        term.reset(None)
        bias = term.bias.clone()
        checks['policy_bias_in_range'] = bool((bias.abs() <= 0.0014 + 1e-9).all()) and float(bias.std()) > 0
        critic_term.func.reset(None)
        checks['critic_bias_zero'] = bool((critic_term.func.bias == 0).all())
        outs = [term(raw, **params)[:, 0].clone() for _ in range(term.warmup_steps)]
        checks['zero_during_warmup'] = bool(all((o == 0).all() for o in outs))
        k = 10
        for _ in range(k):
            out = term(raw, **params)[:, 0].clone()
        expected = (rate + bias) * dt * k
        checks['integrates_after_warmup'] = bool(torch.allclose(out, expected, atol=1e-6))
        for _ in range(400):
            out = term(raw, **params)[:, 0].clone()
        checks['output_clipped_internal_kept'] = bool(torch.allclose(out, torch.full((n,), params['clip_rad']))) \
            and float(term.error.min()) > params['clip_rad']
        command._emitted_command_b[1, 2] = 0.5
        out = term(raw, **params)[:, 0].clone()
        checks['command_resets'] = float(out[1]) == 0.0 and float(term.error[1]) == 0.0 and float(out[0]) > 0
        zero_command()
        term.reset(torch.tensor([0]))
        checks['reset_clears'] = float(term.error[0]) == 0.0 and float(term.hold_steps[0]) == 0.0
        checks['policy_obs_35_heading_last'] = int(om.group_obs_dim['policy'][0]) == 35 and names['policy'][-1] == 'heading_error'
        checks['critic_terms_base_plus_heading'] = names['critic'] == base_critic + added
        checks['heading_terms_same_as_reference'] = heading_terms_same
        checks['heading_warmup'] = warmups == [warmup] * 3 and term.warmup_steps == max(1, round(warmup / dt))
        reward_term = raw.reward_manager.get_term_cfg('zero_command_heading_drift')
        zero_command()
        reward_term.func.reset(None)
        reward_term.func(raw, **reward_term.params)
        checks['reward_anchor_after_warmup_steps'] = bool(reward_term.func.anchor_set.all()) == (reward_term.func.warmup_steps == 1)
        leg = type(raw.action_manager.get_term('joint_pos_0')).__name__
        checks['leg_filter'] = (leg == 'MA2JointPositionAction') == expect_ma2
        ccfg = command.cfg
        checks['commands'] = (tuple(ccfg.ranges.lin_vel_x) == (-lin_max, lin_max) and tuple(ccfg.ranges.ang_vel_z) == (-ang_max, ang_max)
                              and float(ccfg.ramp_rate) == ramp)
        checks['sphere_wheels'] = 'sphere_wheels' in cfg.scene.robot.spawn.asset_path
        checks['heading_drift_reward_present'] = 'zero_command_heading_drift' in raw.reward_manager.active_terms
        checks['policy_scale_2_noise'] = float(policy_term.scale) == 2.0 and policy_term.noise is not None and critic_term.noise is None
        env.reset()
        finite = True
        for _ in range(30):
            obs, rew, *_ = env.step(torch.rand((n, raw.action_manager.total_action_dim)) * 2 - 1)
            finite &= bool(torch.isfinite(obs['policy']).all() and torch.isfinite(obs['critic']).all() and torch.isfinite(rew).all())
        checks['finite_30_steps'] = finite
        result = dict(execution_domain='TRAINING_SIM', task=TASK, leg_action=leg, checks=checks,
                      dims={k: list(v) for k, v in om.group_obs_dim.items()}, policy_terms=names['policy'],
                      critic_terms=names['critic'], params=params, warmup_steps=term.warmup_steps,
                      evidence_status='PASS' if all(checks.values()) else 'FAIL')
        (args.output / f'{TASK}_check.json').write_text(json.dumps(result, indent=1, default=str))
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
