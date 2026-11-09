"""TRAINING_SIM: mixed velocity/support goals, reward masks and 4096-environment smoke."""

import json
from pathlib import Path
import sys
from types import SimpleNamespace

import pytest
import torch

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT / 'test'), str(ROOT / 'sim2sim/sim2sim_ros2_jazzy')]
from mjlab.envs import ManagerBasedRlEnv
from mj_lab.checkpoint import plain, playback_contract
from mj_lab.flash_sac import TitaFlashSACEnv
from mj_lab.robots.tita.stand_one_leg.support_command_env_cfg import (
    TitaSupportCommandEnvCfg, TitaSupportVelocityEnvCfg, reward_by_mode,
)
from sim2sim_ros2_jazzy.checkpoint import observation_layout, simulation_config
from test_mjlab_support_command import fake_env


def test_new_task_preserves_balance_physics_and_old_task():
    new, old = TitaSupportVelocityEnvCfg(), TitaSupportCommandEnvCfg()
    assert new.scene.num_envs == 4096
    velocity = new.commands['base_velocity']
    assert velocity.lin_vel_x == velocity.ang_vel_z == (-.5, .5)
    assert velocity.lin_vel_y == (0., 0.) and velocity.rel_standing_envs == .5
    assert new.commands['support'].mode_probabilities == (.4, .4, .2)
    assert new.commands['support'].episode_fixed and 'gait' not in new.commands
    for name in ('actions', 'events', 'sim', 'terminations'):
        assert plain(getattr(new, name)) == plain(getattr(old, name))
    for name, term in old.rewards.items():
        assert new.rewards[name].weight == term.weight
        if name != 'one_leg_stationary':
            assert plain(new.rewards[name]) == plain(term)
    assert new.rewards['one_leg_stationary'].params['command_mode'] == 'standing'
    assert 'command_mode' not in old.rewards['one_leg_stationary'].params
    assert old.commands['base_velocity'].lin_vel_x == (0., 0.)
    assert new.rewards['one_leg_track_lin_vel_xy_exp'].weight == 2.
    assert new.rewards['one_leg_track_ang_vel_z_exp'].weight == 1.


def test_velocity_sampler_half_stationary_and_independent_of_support():
    torch.manual_seed(42)
    cfg = TitaSupportVelocityEnvCfg()
    env = SimpleNamespace(num_envs=20000, device='cpu')
    velocity = cfg.commands['base_velocity'].build(env)
    support = cfg.commands['support'].build(env)
    ids = torch.arange(env.num_envs)
    support.reset(ids)
    velocity._resample_command(ids)
    command = velocity.target
    standing = (command == 0.).all(dim=1)
    assert abs(standing.float().mean().item()-.5) < .015
    assert not command[:, 1].any()
    assert command.abs().max() <= .5
    assert (command[~standing, 0].abs() > 0).all() and (command[~standing, 2].abs() > 0).all()
    for mode in (0, 1, 2):
        assert abs(standing[support.mode == mode].float().mean().item()-.5) < .03
    print('TRAINING_SIM sampler:', json.dumps({'standing_fraction':standing.float().mean().item(),
          'support_counts':support.mode.bincount(minlength=3).tolist()}))


def test_stationary_and_tracking_rewards_do_not_conflict():
    env = fake_env([0, 1, 2, 0, 1, 2])
    command = torch.tensor([[0., 0., 0.]]*3 + [[.5, 0., .5]]*3)
    support = env.command_manager.get_term('support')
    velocity = SimpleNamespace(command=command)
    env.command_manager.get_term = lambda name: support if name == 'support' else velocity
    env.command_manager.get_command = lambda name: command
    d = env.scene['robot'].data
    d.projected_gravity_b = torch.tensor([[0., -.5, -.866]]*6)
    d.root_link_lin_vel_b = command.clone()
    d.root_link_lin_vel_b[:, 2] = 0.
    d.root_link_ang_vel_b = torch.stack((torch.zeros(6), torch.zeros(6), command[:, 2]), dim=1)
    d.root_link_lin_vel_w = d.root_link_lin_vel_b.clone()
    d.root_link_ang_vel_w = d.root_link_ang_vel_b.clone()
    cfg = TitaSupportVelocityEnvCfg(6)
    for name in ('track_lin_vel_xy_exp', 'track_ang_vel_z_exp'):
        term = cfg.rewards['one_leg_'+name]
        torch.testing.assert_close(term.func(env, **term.params), torch.tensor([0., 0., 0., 1., 1., 0.]))
    term = cfg.rewards['one_leg_stationary']
    assert not term.func(env, **term.params).any()
    d.root_link_lin_vel_w[:] = .2
    actual = term.func(env, **term.params)
    assert (actual[:2] > 0).all() and not actual[2:].any()
    # Moving but ignoring the command earns less than correctly tracking it.
    term = cfg.rewards['one_leg_track_lin_vel_xy_exp']
    good = term.func(env, **term.params)
    d.root_link_lin_vel_b.zero_()
    assert (term.func(env, **term.params)[3:5] < good[3:5]).all()


def test_velocity_ranges_survive_export_and_runtime_caps():
    cfg = TitaSupportVelocityEnvCfg(4)
    saved = playback_contract(cfg)
    from mj_lab.robots.tita.common.robot_cfg import JOINTS
    layout = observation_layout(saved['observations']['policy'], {}, list(JOINTS))
    runtime = simulation_config(saved, saved['scene']['robot']['init_state'], layout)
    assert runtime['policy']['obs_dim'] == 38
    assert runtime['sim_command_ranges']['lin_vel_x'] == [-.5, .5]
    assert runtime['sim_command_ranges']['ang_vel_z'] == [-.5, .5]
    assert runtime['sim_command_ranges']['lin_vel_y'] == [0., 0.]


def test_native_4096_environments_have_finite_transitions():
    if not torch.cuda.is_available():
        pytest.skip('Native mjlab physics requires CUDA')
    cfg = TitaSupportVelocityEnvCfg(4096)
    cfg.seed = 42
    env = TitaFlashSACEnv(ManagerBasedRlEnv(cfg, device='cuda:0'))
    try:
        obs = env.reset(seed=42)
        assert env.num_envs == 4096 and (env.actor_obs_dim, env.critic_obs_dim) == (38, 42)
        for _ in range(40):
            obs, terminal_obs, reward, _, _, _ = env.step(torch.zeros(4096, 8, device=env.device))
            assert torch.isfinite(obs).all() and torch.isfinite(terminal_obs).all() and torch.isfinite(reward).all()
        command = env.env.command_manager.get_command('base_velocity')
        ratio = (command == 0.).all(dim=1).float().mean().item()
        assert .45 < ratio < .55
        print(f'TRAINING_SIM native 4096-env PASS: observation={tuple(obs.shape)}, stationary fraction={ratio:.5f}')
    finally:
        env.close()
