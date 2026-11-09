"""TRAINING_SIM / VALIDATION_SIM: pose goals, reward geometry and native reset flow."""

from dataclasses import replace
import math
from pathlib import Path
import sys
from types import SimpleNamespace

import cloudpickle
import pytest
import torch
from mjlab.envs import ManagerBasedRlEnv
from mjlab.utils.lab_api.math import quat_apply_inverse, quat_from_euler_xyz

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
from mj_lab.checkpoint import plain, playback_contract
from mj_lab.flash_sac import TitaFlashSACEnv
from mj_lab.robots.tita import mdp
from mj_lab.robots.tita.flat_env_cfg import TitaFlatEnvCfg
from mj_lab.robots.tita.roll_pitch_height.flat_env_roll_pitch_height_cfg import (
    RollPitchHeightCommandCfg, TitaFlatRollPitchHeightEnvCfg,
    desired_gravity, pose_error, pose_observation, pose_tracking_l2,
)


def test_sampling_ramp_and_partial_reset():
    torch.manual_seed(42)
    cfg = RollPitchHeightCommandCfg(resampling_time_range=(6., 8.))
    command = cfg.build(SimpleNamespace(num_envs=10000, device='cpu'))
    ids = torch.arange(10000)
    command.reset(ids)
    nominal = torch.tensor([0., 0., .335]).expand_as(command.command)
    torch.testing.assert_close(command.command, nominal)
    nominal_rows = (command.target == nominal).all(1)
    assert abs(nominal_rows.float().mean().item()-.2) < .015
    for axis, bounds in enumerate((cfg.roll_range, cfg.pitch_range, cfg.height_range)):
        assert (command.target[:, axis] >= bounds[0]).all() and (command.target[:, axis] <= bounds[1]).all()
    target = command.target.clone()
    command.compute(.02)
    assert ((command.command-nominal).abs() <= torch.tensor(cfg.ramp_rates)*.02+1e-7).all()
    for _ in range(250):
        command.compute(.02)
    torch.testing.assert_close(command.command, target)
    previous = command.command.clone(), command.target.clone(), command.time_left.clone()
    command.reset(torch.tensor([0]))
    command.compute(0., torch.tensor([0]))
    torch.testing.assert_close(command.command[0], nominal[0])
    for actual, old in zip((command.command, command.target, command.time_left), previous):
        torch.testing.assert_close(actual[1:], old[1:], rtol=0, atol=0)
    # Native auto-reset may provide one dt per environment.
    command.target[:] = torch.tensor([math.radians(30.), -math.radians(15.), .42])
    before = command.command.clone()
    dt = torch.full((10000,), .02)
    dt[0] = 0.
    command.compute(dt)
    torch.testing.assert_close(command.command[0], before[0])
    assert ((command.command-before).abs() <= torch.tensor(cfg.ramp_rates)*dt[:, None]+1e-7).all()


@pytest.mark.parametrize('changes', [
    {'height_range': (0., .4)}, {'roll_range': (.2, -.2)}, {'pitch_range': (-math.pi/2, .1)},
    {'ramp_rates': (.1, 0., .02)}, {'ramp_rates': (.1, float('nan'), .02)},
    {'resampling_time_range': (0., 1.)}, {'rel_nominal_envs': 1.1}, {'nominal_height': float('nan')},
])
def test_invalid_command_configuration(changes):
    cfg = replace(RollPitchHeightCommandCfg(resampling_time_range=(6., 8.)), **changes)
    with pytest.raises(ValueError):
        cfg.build(SimpleNamespace(num_envs=1, device='cpu'))


def fake_env(actual, command, yaw):
    quat = quat_from_euler_xyz(actual[:, 0], actual[:, 1], yaw)
    gravity = quat_apply_inverse(quat, torch.tensor([0., 0., -1.]).expand(len(actual), -1))
    origins = torch.tensor([[0., 0., 1.2]]).repeat(len(actual), 1)
    position = origins.clone()
    position[:, 2] += actual[:, 2]
    class Scene(dict):
        env_origins = origins
    velocity = SimpleNamespace(command=torch.zeros_like(command))
    return SimpleNamespace(scene=Scene(robot=SimpleNamespace(data=SimpleNamespace(
        projected_gravity_b=gravity, root_link_pos_w=position, root_link_quat_w=quat))),
        command_manager=SimpleNamespace(get_command=lambda _: command, get_term=lambda _: velocity))


def test_commanded_reward_zero_at_goal_sign_and_yaw_invariance():
    command = torch.tensor([[math.radians(30.), -math.radians(15.), .27],
                            [-math.radians(30.), math.radians(15.), .42], [.08, .12, .335]])
    yaw = torch.tensor([0., 1.4, -2.5])
    env = fake_env(command, command, yaw)
    torch.testing.assert_close(desired_gravity(command), mdp.data(env).projected_gravity_b)
    for kind in ('base_height_l2', 'flat_orientation_l2'):
        torch.testing.assert_close(pose_tracking_l2(env, kind), torch.zeros(3), atol=1e-12, rtol=0.)
    for axis in range(3):
        torch.testing.assert_close(pose_error(env, axis), torch.zeros(3), atol=3e-7, rtol=0.)
    actual = command.clone()
    actual[:, :2] *= -1.
    actual[:, 2] += .02
    wrong = fake_env(actual, command, yaw)
    assert (pose_tracking_l2(wrong, 'flat_orientation_l2') > .05).all()
    torch.testing.assert_close(pose_tracking_l2(wrong, 'base_height_l2'), torch.full((3,), .02**2))


def test_nominal_goal_matches_parent_reward_exactly():
    actual = torch.tensor([[.1, -.15, .3], [-.1, .15, .37], [.5, -.4, .335]])
    command = torch.tensor([[0., 0., .335]]).repeat(3, 1)
    env = fake_env(actual, command, torch.tensor([0., 1.4, -2.5]))
    for kind in ('base_height_l2', 'flat_orientation_l2'):
        torch.testing.assert_close(pose_tracking_l2(env, kind), mdp.reward(env, kind), atol=0, rtol=0)


def test_inheritance_and_checkpoint_contract():
    cfg, parent = TitaFlatRollPitchHeightEnvCfg(4), TitaFlatEnvCfg(4)
    assert isinstance(cfg, TitaFlatEnvCfg)
    for name in ('actions', 'events', 'sim', 'scene', 'terminations'):
        assert plain(getattr(cfg, name)) == plain(getattr(parent, name))
    velocity, original = plain(cfg.commands['base_velocity']), plain(parent.commands['base_velocity'])
    assert velocity.pop('wheel_error_velocity_thresholds') == [.1, .15]
    assert velocity.pop('wheel_error_moving_anchor') is True
    assert velocity.pop('stop_state_after_pose') is True
    assert original.pop('wheel_error_velocity_thresholds') is None
    assert original.pop('wheel_error_moving_anchor') is False
    assert original.pop('stop_state_after_pose') is False
    assert velocity == original
    assert cfg.rewards['joint_mirror'].weight == 0. and parent.rewards['joint_mirror'].weight == -1.
    for name in parent.rewards:
        if name not in ('joint_mirror', 'base_height_l2', 'flat_orientation_l2'):
            assert plain(cfg.rewards[name]) == plain(parent.rewards[name])
    for name in ('base_height_l2', 'flat_orientation_l2'):
        assert cfg.rewards[name].weight == parent.rewards[name].weight
    saved = playback_contract(cfg)
    assert saved['observations']['policy']['wheel_position_error']['params']['velocity_thresholds'] == [.1, .15]
    assert saved['observations']['policy']['wheel_position_error']['params']['moving_anchor'] is True
    assert saved['commands']['base_pose']['order'] == ['roll', 'pitch', 'height']
    assert saved['observations']['policy']['pose_commands']['params']['command_name'] == 'base_pose'
    assert playback_contract(cloudpickle.loads(cloudpickle.dumps(cfg))) == saved
    # Pose commands are separate from velocity commands despite sharing width 3.
    sys.path.insert(0, str(REPO/'sim2sim/sim2sim_ros2_jazzy'))
    from sim2sim_ros2_jazzy.checkpoint import observation_layout, simulation_config
    layout = observation_layout(saved['observations']['policy'], {}, list(cfg.scene.entities['robot'].init_state.joint_pos))
    assert layout[-1]['kind'] == 'pose_commands' and layout[-1]['size'] == 3
    runtime = simulation_config(saved, saved['scene']['robot']['init_state'], layout)
    assert runtime['pose_command']['nominal_height'] == .335 and runtime['policy']['obs_dim'] == 38


def test_native_observations_metrics_resampling_and_partial_reset():
    if not torch.cuda.is_available():
        pytest.skip('Native mjlab physics requires CUDA')
    cfg = TitaFlatRollPitchHeightEnvCfg(4, play=True)
    cfg.seed = 42
    env = TitaFlashSACEnv(ManagerBasedRlEnv(cfg, device='cuda:0'))
    try:
        raw = env.env
        env.reset(seed=42)
        assert (env.actor_obs_dim, env.critic_obs_dim, env.action_dim) == (38, 42, 8)
        command = raw.command_manager.get_term('base_pose')
        command.target[:] = command.target.new_tensor([math.radians(30.), -math.radians(15.), .42])
        command.compute(.02)
        before = command.command.clone(), command.target.clone(), command.time_left.clone()
        raw.reset(env_ids=torch.tensor([0], device=env.device))
        for actual, old in zip((command.command, command.target, command.time_left), before):
            torch.testing.assert_close(actual[1:], old[1:], atol=0, rtol=0)
        expected = command.command.clone()
        for _ in range(3):
            obs = raw.observation_manager.compute()
            torch.testing.assert_close(obs['policy'][:, -3:], expected)
            torch.testing.assert_close(obs['critic'][:, -3:], expected)
            torch.testing.assert_close(pose_observation(raw), expected)
        command.time_left.zero_()
        command.compute(.02)
        assert (command.time_left > 0).all()
        assert {'roll_error_rad', 'pitch_error_rad', 'height_error_m'} <= set(raw.metrics_manager.active_terms)
        for _ in range(100):
            obs, replay, reward, _, _, _ = env.step(torch.zeros(4, 8, device=env.device))
            assert torch.isfinite(obs).all() and torch.isfinite(replay).all() and torch.isfinite(reward).all()
    finally:
        env.close()
