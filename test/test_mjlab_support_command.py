"""TRAINING_SIM / VALIDATION_SIM: support-mode goals and symmetric rewards."""

import math
from pathlib import Path
import sys
from types import SimpleNamespace

import cloudpickle
import numpy as np
import pytest
import torch
from mjlab.envs import ManagerBasedRlEnv

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO/'sim2sim/sim2sim_ros2_jazzy'))
from mj_lab.checkpoint import plain, playback_contract
from mj_lab.flash_sac import TitaFlashSACEnv
from mj_lab.robots.tita import mdp
from mj_lab.robots.tita.flat_env_cfg import TitaFlatEnvCfg
from mj_lab.robots.tita.common.robot_cfg import JOINTS, INITIAL_Q
from mj_lab.robots.tita.stand_one_leg.stand_one_leg_reference_env_cfg import TitaStandOneLegReferenceEnvCfg
from mj_lab.robots.tita.stand_one_leg.support_command_env_cfg import (
    SupportModeCommandCfg, TitaSupportCommandEnvCfg, achieved_support, pose_hint, support_leg_tilt, support_reward,
)
from sim2sim_ros2_jazzy.adapter import ObservationBuilder, ObsState
from sim2sim_ros2_jazzy.checkpoint import observation_layout, simulation_config


def fake_env(modes):
    count = len(modes)
    pos = torch.tensor([[[0., .2, .4], [0., .2, .0925],
                         [0., -.2, .4], [0., -.2, .0925]]]).repeat(count, 1, 1)
    angle = math.radians(30.)
    data = SimpleNamespace(body_link_pos_w=pos, joint_pos=torch.full((count, 8), angle),
        root_link_quat_w=torch.tensor([[math.cos(angle/2), math.sin(angle/2), 0., 0.]]).repeat(count, 1))
    robot = SimpleNamespace(data=data, body_names=['left_leg_2', 'left_leg_4', 'right_leg_2', 'right_leg_4'], joint_names=list(JOINTS))
    class Scene(dict):
        env_origins = torch.zeros(count, 3)
    command = SimpleNamespace(mode=torch.tensor(modes))
    return SimpleNamespace(scene=Scene(robot=robot, feet=SimpleNamespace(data=SimpleNamespace(force=torch.zeros(count, 2, 3)))),
        command_manager=SimpleNamespace(get_term=lambda _: command), step_dt=.02,
        termination_manager=SimpleNamespace(terminated=torch.zeros(count, dtype=torch.bool)))


def test_left_right_both_and_wrong_support_rewards():
    env = fake_env([0, 1, 2, 0, 1, 2, 2])
    pos, force = env.scene['robot'].data.body_link_pos_w, env.scene['feet'].data.force
    force[0, 0, 2], pos[0, 3, 2] = -130., .1325  # left support, right lifted
    force[1, 1, 2], pos[1, 1, 2] = 130., .1325  # mirrored support; force sign irrelevant
    force[2, :, 2] = -130.  # both requested and grounded
    force[3:5, :, 2] = -130.  # grounded swing in either single-support mode
    force[5, 0, 2] = -130.  # both requested but only one contact
    torch.testing.assert_close(support_reward(env), torch.tensor([1., 1., 1., -.25, -.25, 0., -1.]))
    torch.testing.assert_close(pose_hint(env), torch.tensor([1., 1., 0., 1., 1., 0., 0.]))
    actual = achieved_support(env).gather(1, env.command_manager.get_term('support').mode[:, None]).squeeze(1)
    assert actual.tolist() == [True, True, True, False, False, False, False]
    env.termination_manager.terminated[0] = True
    assert not achieved_support(env)[0].any()
    # The successful right-only physical pose is incorrect for a left command.
    env.command_manager.get_term('support').mode[1] = 0
    assert support_reward(env)[1] == pytest.approx(-1.25)


def test_tilt_selects_requested_leg_and_is_off_for_both_mode():
    env = fake_env([0, 1, 2])
    pos = env.scene['robot'].data.body_link_pos_w
    pos[:, 0] = pos[:, 1] + torch.tensor([.2, 0., .2])
    torch.testing.assert_close(support_leg_tilt(env), torch.tensor([1.-2**-.5, 0., 0.]))


def test_saved_support_observation_and_all_runtime_modes():
    cfg, parent = TitaSupportCommandEnvCfg(4), TitaStandOneLegReferenceEnvCfg(4)
    assert 'gait' not in cfg.commands
    for name in ('actions', 'events', 'sim', 'terminations'):
        assert plain(getattr(cfg, name)) == plain(getattr(parent, name))
    for name, term in parent.rewards.items():
        actual = cfg.rewards['one_leg_'+name]
        assert actual.weight == term.weight and actual.params['single_support'] is True
    flat = TitaFlatEnvCfg(4)
    assert len(cfg.rewards) == len(parent.rewards)+len(flat.rewards)
    for name, term in flat.rewards.items():
        actual = cfg.rewards['flat_'+name]
        assert actual.weight == term.weight
        assert actual.params['source_func'] is term.func
        assert actual.params['source_params'] == term.params
        assert actual.params['single_support'] is False
    saved = playback_contract(cfg)
    assert saved['commands']['support']['mode_names'] == ['left', 'right', 'both']
    assert saved['commands']['support']['episode_fixed'] is True
    assert saved['commands']['support']['mode_probabilities'] == [.4, .4, .2]
    assert playback_contract(cloudpickle.loads(cloudpickle.dumps(cfg))) == saved
    layout = observation_layout(saved['observations']['policy'], {}, list(JOINTS))
    playback = simulation_config(saved, saved['scene']['robot']['init_state'], layout)
    playback['policy_interface'] = {'observations': layout}
    assert playback['policy']['obs_dim'] == 38 and 'gait_command' not in playback
    builder = ObservationBuilder(playback)
    state = ObsState(np.array(INITIAL_Q), np.zeros(8), np.array([1., 0., 0., 0.]),
                     np.zeros(3), np.zeros(3), np.zeros(8), np.zeros(3))
    for selected in (2, 0, 1, 2):
        state.support_mode = selected
        np.testing.assert_array_equal(builder.build(state)[-3:], np.eye(3)[selected])
    for invalid in (-1, 3, True, .5):
        state.support_mode = invalid
        with pytest.raises(ValueError, match='Support mode'):
            builder.build(state)
    saved['commands']['support']['encoding'] = 'scalar'
    with pytest.raises(ValueError, match='Invalid saved support'):
        simulation_config(saved, saved['scene']['robot']['init_state'], layout)


def test_episode_sampling_distribution_and_no_within_episode_changes():
    torch.manual_seed(42)
    cfg = SupportModeCommandCfg(resampling_time_range=(1e9, 1e9),
                               episode_fixed=True, mode_probabilities=(.4, .4, .2))
    command = cfg.build(SimpleNamespace(num_envs=20000, device='cpu'))
    command.reset(torch.arange(20000))
    command.compute(0.)
    fractions = command.mode.bincount(minlength=3).float()/20000
    torch.testing.assert_close(fractions, torch.tensor([.4, .4, .2]), atol=.015, rtol=0.)
    previous_mode, previous_command = command.mode.clone(), command.command.clone()
    for _ in range(25):
        command.compute(1.)
    torch.testing.assert_close(command.mode, previous_mode)
    torch.testing.assert_close(command.command, previous_command)
    command.time_left.zero_()  # Even timer expiry must not change an episode-fixed target.
    command.compute(0.)
    torch.testing.assert_close(command.mode, previous_mode)


def test_saved_legacy_config_keeps_timed_sampling():
    cfg = SupportModeCommandCfg(resampling_time_range=(3., 5.))
    # Saved configs from before these fields existed use class defaults.
    del cfg.episode_fixed
    del cfg.mode_probabilities
    command = cfg.build(SimpleNamespace(num_envs=128, device='cpu'))
    command.reset(torch.arange(128))
    command.compute(0.)
    assert ((command.time_left >= 3.) & (command.time_left <= 5.)).all()
    previous = command.mode.clone()
    command.time_left.zero_()
    command.compute(0.)
    assert (command.mode != previous).all()


def test_native_episode_goals_manual_override_and_partial_reset_is_scoped():
    if not torch.cuda.is_available():
        pytest.skip('Native mjlab physics requires CUDA')
    cfg = TitaSupportCommandEnvCfg(16)
    cfg.seed = 42
    env = TitaFlashSACEnv(ManagerBasedRlEnv(cfg, device='cuda:0'))
    try:
        raw = env.env
        env.reset(seed=42)
        assert (env.actor_obs_dim, env.critic_obs_dim, env.action_dim) == (38, 42, 8)
        support = raw.command_manager.get_term('support')
        assert torch.isinf(support.time_left).all()
        old = support.mode.clone()
        for _ in range(25):
            support.compute(1.)
        torch.testing.assert_close(support.mode, old)
        previous = support.mode.clone(), support.time_left.clone()
        raw.reset(env_ids=torch.tensor([0], device=env.device))
        torch.testing.assert_close(support.mode[1:], previous[0][1:])
        torch.testing.assert_close(support.time_left[1:], previous[1][1:])
        raw.episode_length_buf[:] = 50
        for selected in (0, 1, 2):
            support.set_mode(selected)
            obs = raw.observation_manager.compute(update_history=True)
            expected = torch.nn.functional.one_hot(torch.full((16,), selected, device=env.device), 3).float()
            torch.testing.assert_close(obs['policy'][:, -3:], expected)
            torch.testing.assert_close(obs['critic'][:, -3:], expected)
            assert (raw.episode_length_buf == 50).all()
        for _ in range(180):
            obs, _, reward, _, _, _ = env.step(torch.zeros(16, 8, device=env.device))
            assert torch.isfinite(obs).all() and torch.isfinite(reward).all()
        assert not raw.command_manager.get_command('base_velocity').any()
    finally:
        env.close()


def test_native_flat_reward_equivalence_and_inactive_state_isolation():
    if not torch.cuda.is_available():
        pytest.skip('Native mjlab physics requires CUDA')
    cfg = TitaSupportCommandEnvCfg(6)
    cfg.seed = 42
    env = TitaFlashSACEnv(ManagerBasedRlEnv(cfg, device='cuda:0'))
    try:
        raw = env.env
        env.reset(seed=42)
        command = raw.command_manager.get_term('support')
        command.mode[:] = torch.arange(6, device=env.device) % 3
        command._update_command()
        active = command.mode == 2
        raw.action_manager.action[:, [3, 7]] = 2.
        velocity = mdp.velocity(raw)
        fields = ('position_anchor', 'heading_anchor', 'anchor_set', 'position_latched', 'wheel_integral')
        before = {name:getattr(velocity, name).clone() for name in fields}
        flat = TitaFlatEnvCfg(6)
        expected = {name:term.func(raw, **term.params).clone() for name,term in flat.rewards.items()}
        expected_state = {name:getattr(velocity, name).clone() for name in fields}
        for name,value in before.items():
            getattr(velocity, name).copy_(value)
        for name in flat.rewards:
            term = cfg.rewards['flat_'+name]
            actual = term.func(raw, **term.params)
            torch.testing.assert_close(actual[active], expected[name][active])
            torch.testing.assert_close(actual[~active], torch.zeros_like(actual[~active]))
        for name in fields:
            torch.testing.assert_close(getattr(velocity, name)[active], expected_state[name][active])
            torch.testing.assert_close(getattr(velocity, name)[~active], before[name][~active])
        for name,term in cfg.rewards.items():
            if name.startswith('one_leg_'):
                actual = term.func(raw, **term.params)
                assert not actual[active].any()  # No alive/termination/regularizer from this set in mode 2.
    finally:
        env.close()
