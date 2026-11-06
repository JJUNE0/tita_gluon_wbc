"""TRAINING_SIM / VALIDATION_SIM: height cycles, 30-degree exits and playback."""

from dataclasses import replace
import math
from pathlib import Path
import sys
from types import SimpleNamespace

import cloudpickle
import numpy as np
import pytest
import torch
from mjlab.envs import ManagerBasedRlEnv
from mjlab.utils.lab_api.math import quat_from_euler_xyz

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT/'sim2sim/sim2sim_ros2_jazzy')]
from mj_lab.checkpoint import plain, playback_contract
from mj_lab.flash_sac import TitaFlashSACEnv
from mj_lab.robots.tita import mdp
from mj_lab.robots.tita.height_only_env_cfg import HeightCycleCommandCfg, TitaHeightOnlyEnvCfg, excessive_roll_pitch
from mj_lab.robots.tita.sit_stand_env_cfg import TitaSitStandEnvCfg
from sim2sim_ros2_jazzy.checkpoint import observation_layout, simulation_config
from sim2sim_ros2_jazzy.state_machine import SPLAY_POSE


def command_env(count):
    class Scene(dict):
        env_origins = torch.zeros(count, 3)
    position = torch.zeros(count, 3)
    position[:, 2] = .335
    velocity = SimpleNamespace(command=torch.zeros(count, 3))
    return SimpleNamespace(num_envs=count, device='cpu',
        scene=Scene(robot=SimpleNamespace(data=SimpleNamespace(root_link_pos_w=position))),
        command_manager=SimpleNamespace(get_term=lambda _: velocity))


def test_cycle_has_separate_ramp_and_hold_and_completes_within_20s():
    torch.manual_seed(42)
    env = command_env(128)
    command = HeightCycleCommandCfg(resampling_time_range=(1e9, 1e9)).build(env)
    command.reset(torch.arange(128))
    assert (command.target[:, 2] == .335).all()
    assert (command.time_left >= 1.).all() and (command.time_left <= 3.).all()
    for _ in range(1000):
        old = command.command.clone()
        counter = command.command_counter.clone()
        # Ideal physical tracking, except row 0 deliberately never sits.
        mdp.data(env).root_link_pos_w[:, 2] = old[:, 2]
        mdp.data(env).root_link_pos_w[0, 2] = .335
        command.compute(.02)
        assert ((command.command-old).abs() <= torch.tensor([.003, .003, .001])+1e-7).all()
        assert (command.command[:, :2] == 0).all()
        assert command.command[:, 2].min() >= .08 and command.command[:, 2].max() <= .335
        changed = command.command_counter != counter
        if changed.any():
            expected = (command.target[changed, 2]-old[changed, 2]).abs()/.05 + command.dwell_s[changed]
            torch.testing.assert_close(command.time_left[changed], expected)
        assert (command.dwell_s >= 1.).all() and (command.dwell_s <= 3.).all()
    assert (command.command_counter >= 4).all()
    assert command.metrics['completed_cycles'][0] == 0.
    assert (command.metrics['completed_cycles'][1:] >= 1.).all()
    assert (command.metrics['sit_time_s'][1:] > 0).all()


def test_partial_reset_does_not_change_other_cycle_state():
    env = command_env(4)
    command = HeightCycleCommandCfg(resampling_time_range=(1e9, 1e9)).build(env)
    command.reset(torch.arange(4))
    for _ in range(400):
        mdp.data(env).root_link_pos_w[:, 2] = command.command[:, 2]
        command.compute(.02)
    fields = [command.command, command.target, command.time_left, command.command_counter,
              command._next_low, command._saw_sit, command.dwell_s, *command.metrics.values()]
    before = [value.clone() for value in fields]
    command.reset(torch.tensor([0]))
    command.compute(0., torch.tensor([0]))
    for value, old in zip(fields, before):
        torch.testing.assert_close(value[1:], old[1:], atol=0, rtol=0)


def test_roll_pitch_failure_uses_each_axis_and_both_signs():
    angles = torch.tensor([[0., 0.], [29.9, 0.], [30.1, 0.], [-30.1, 0.], [25., 25.], [0., -30.1]])
    q = quat_from_euler_xyz(*torch.deg2rad(angles).T, torch.zeros(len(angles)))
    env = SimpleNamespace(scene={'robot':SimpleNamespace(data=SimpleNamespace(root_link_quat_w=q))})
    torch.testing.assert_close(excessive_roll_pitch(env), torch.tensor([False, False, True, True, False, True]))


@pytest.mark.parametrize('changes', [
    {'dwell_time_range':(0., 3.)}, {'height_range':(.335, .335)},
    {'height_range':(.08, .30)}, {'ramp_rates':(.15, .15, 0.)},
    {'roll_range':(-.1, .1)}, {'height_motion_range':(.3, .4)},
])
def test_invalid_height_cycle_settings(changes):
    cfg = replace(HeightCycleCommandCfg(resampling_time_range=(1e9, 1e9)), **changes)
    with pytest.raises(ValueError):
        cfg.build(command_env(2))


def test_config_keeps_dr_full_idle_envelope_and_saved_playback():
    cfg, parent = TitaHeightOnlyEnvCfg(4), TitaSitStandEnvCfg(4)
    for name in ('scene', 'sim', 'events', 'actions', 'observations'):
        assert plain(getattr(cfg, name)) == plain(getattr(parent, name))
    assert cfg.episode_length_s == 20.
    assert cfg.curriculum_transition_step is None and not cfg.set_training_step(100000)
    assert set(cfg.terminations) == {'time_out', 'roll_pitch'}
    assert cfg.terminations['roll_pitch'].params['limit_deg'] == 30.
    for name, term in parent.rewards.items():
        assert plain(cfg.rewards[name]) == plain(term)
    assert cfg.rewards['termination'].weight == -10.
    velocity = cfg.commands['base_velocity']
    assert velocity.lin_vel_x == velocity.lin_vel_y == velocity.ang_vel_z == (0., 0.)
    assert velocity.rel_standing_envs == 1.
    defaults = np.asarray(list(cfg.scene.entities['robot'].init_state.joint_pos.values()))
    gains = np.where(SPLAY_POSE >= defaults, cfg.action_gain_positive, cfg.action_gain_negative)
    assert (abs((SPLAY_POSE-defaults)/(.25*gains)) <= 1.+1e-6).all()
    saved = cloudpickle.loads(cloudpickle.dumps(cfg))
    contract = playback_contract(saved)
    layout = observation_layout(contract['observations']['policy'], {}, list(contract['scene']['robot']['init_state']['joint_pos']))
    runtime = simulation_config(contract, contract['scene']['robot']['init_state'], layout)
    assert runtime['policy']['obs_dim'] == 38
    assert runtime['pose_command']['height_range'] == [.08, .335]
    assert runtime['pose_command']['ramp_rates'][2] == .05
    assert all(value == [0., 0.] for value in runtime['sim_command_ranges'].values())


def test_native_height_only_environment_without_any_learner_updates():
    if not torch.cuda.is_available():
        pytest.skip('Native mjlab validation requires CUDA')
    cfg = TitaHeightOnlyEnvCfg(8)
    env = TitaFlashSACEnv(ManagerBasedRlEnv(cfg, device='cuda:0'),
        action_gain_negative=cfg.action_gain_negative, action_gain_positive=cfg.action_gain_positive)
    try:
        assert (env.actor_obs_dim, env.critic_obs_dim, env.action_dim) == (38, 42, 8)
        obs = env.reset(seed=42)
        for _ in range(60):
            obs, terminal_obs, reward, _, _, _ = env.step(torch.zeros(8, 8, device=env.device))
            assert torch.isfinite(obs).all() and torch.isfinite(terminal_obs).all() and torch.isfinite(reward).all()
            assert not env.env.command_manager.get_command('base_velocity').any()
            assert not env.env.command_manager.get_command('base_pose')[:, :2].any()
        raw, robot = env.env, env.env.scene['robot']
        pose = robot.data.root_link_pose_w.clone()
        pose[:, 2] = .08
        pose[:, 3:] = pose.new_tensor([1., 0., 0., 0.])
        robot.write_root_link_pose_to_sim(pose)
        raw.sim.forward()
        raw.episode_length_buf[:] = 0
        raw.termination_manager.compute()
        assert not raw.termination_manager.terminated.any()
        roll = torch.full((8,), math.radians(-31.), device=env.device)
        pose[:, 3:] = quat_from_euler_xyz(roll, torch.zeros_like(roll), torch.zeros_like(roll))
        robot.write_root_link_pose_to_sim(pose)
        raw.sim.forward()
        raw.termination_manager.compute()
        assert raw.termination_manager.terminated.all()
    finally:
        env.close()
