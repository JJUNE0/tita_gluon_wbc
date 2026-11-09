"""TRAINING_SIM / VALIDATION_SIM: fixed support and qualitative pose guidance."""

import math
from pathlib import Path
import sys
from types import SimpleNamespace

import cloudpickle
import pytest
import torch
from mjlab.envs import ManagerBasedRlEnv

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO/'sim2sim/sim2sim_ros2_jazzy'))

from mj_lab.checkpoint import plain, playback_contract
from mj_lab.flash_sac import TitaFlashSACEnv
from mj_lab.robots.tita.flat_env_cfg import TitaFlatEnvCfg
from mj_lab.robots.tita.common.robot_cfg import JOINTS
from mj_lab.robots.tita.stand_one_leg.stand_one_leg_reference_env_cfg import (
    TitaStandOneLegReferenceEnvCfg, balance_metric, fixed_support, pose_hint,
)
from sim2sim_ros2_jazzy.checkpoint import observation_layout, simulation_config


def fake_env(count):
    pos = torch.tensor([[[0., .2, .0925], [0., -.2, .0925]]]).repeat(count, 1, 1)
    data = SimpleNamespace(body_link_pos_w=pos, joint_pos=torch.zeros(count, 8),
                           root_link_quat_w=torch.tensor([[1., 0., 0., 0.]]).repeat(count, 1))
    robot = SimpleNamespace(data=data, joint_names=list(JOINTS), body_names=['left_leg_4', 'right_leg_4'])
    class Scene(dict):
        env_origins = torch.zeros(count, 3)
    return SimpleNamespace(scene=Scene(robot=robot, feet=SimpleNamespace(
        data=SimpleNamespace(force=torch.zeros(count, 2, 3)))), step_dt=.02,
        termination_manager=SimpleNamespace(terminated=torch.zeros(count, dtype=torch.bool)))


def test_fixed_support_distinguishes_lift_partial_lift_and_wrong_support():
    env = fake_env(6)
    force = env.scene['feet'].data.force
    force[:, 0, 2] = -130.
    force[0, 1, 2] = 130.  # Both grounded: small swing contact cost.
    env.scene['robot'].data.body_link_pos_w[1:, 1, 2] += .04
    env.scene['robot'].data.body_link_pos_w[2, 1, 2] -= .02
    force[3] = 0.  # Airborne is not a valid lift.
    force[4, :, 2] = torch.tensor([0., -130.])  # Wrong support foot.
    env.scene['robot'].data.body_link_pos_w[5, 1, 2] += .04
    torch.testing.assert_close(fixed_support(env), torch.tensor([-.25, 1., .5, -1., -1.25, 1.]))
    torch.testing.assert_close(balance_metric(env, 'single_support_fraction'),
                               torch.tensor([0., 1., 1., 0., 0., 1.]))
    env.termination_manager.terminated[1] = True
    assert balance_metric(env, 'single_support_time_s')[1] == 0.
    env.scene.env_origins[:, 2] = 10.
    env.scene['robot'].data.body_link_pos_w[:, :, 2] += 10.
    torch.testing.assert_close(fixed_support(env), torch.tensor([-.25, 1., .5, -1., -1.25, 1.]),
                               atol=2e-5, rtol=2e-5)


def test_pose_hint_is_progressive_bounded_and_does_not_copy_the_whole_pose():
    env = fake_env(6)
    robot = env.scene['robot']
    env.scene['feet'].data.force[:, 0, 2] = -130.
    for row, deg in enumerate([0., 10., 30., -30., 80., 30.]):
        angle = math.radians(deg)
        robot.data.root_link_quat_w[row] = torch.tensor([math.cos(angle/2), math.sin(angle/2), 0., 0.])
    robot.data.joint_pos[:, [0, 4]] = math.radians(30.)
    scores = pose_hint(env)
    assert scores[0] < scores[1] < scores[2]
    assert scores[2] == pytest.approx(1.) and scores[3] == pytest.approx(1.)
    assert scores[4] < scores[2]
    robot.data.joint_pos[:, [1, 2, 3, 5, 6, 7]] = 10.
    torch.testing.assert_close(pose_hint(env), scores)
    robot.data.joint_pos[:, [0, 4]] *= -1
    torch.testing.assert_close(pose_hint(env), scores)
    env.scene['feet'].data.force[5] = 0.
    assert pose_hint(env)[5] == 0.


def test_config_has_no_gait_keeps_regularization_and_preserves_parent_physics():
    cfg, parent = TitaStandOneLegReferenceEnvCfg(4), TitaFlatEnvCfg(4)
    assert list(cfg.commands) == ['base_velocity']
    for name in ('actions', 'observations', 'sim'):
        assert plain(getattr(cfg, name)) == plain(getattr(parent, name))
    for name in parent.events:
        if name not in ('reset_base', 'reset_joints'):
            assert plain(cfg.events[name]) == plain(parent.events[name])
    assert cfg.rewards['alive'].weight == 2.
    assert cfg.rewards['action_rate'].weight == -.005
    assert cfg.rewards['dof_acc_l2'].weight == -2.5e-7
    assert cfg.rewards['termination'].weight == -10.
    assert set(cfg.terminations) == {'time_out', 'base_contact', 'knee_contact'}
    assert cfg.events['reset_joints'].params['position_range'] == (1., 1.)
    assert all(pair == (0., 0.) for pair in cfg.events['reset_base'].params['velocity_range'].values())
    saved = playback_contract(cfg)
    assert 'gait' not in saved['commands']
    assert saved['sim_reset_on_policy_entry'] is True
    layout = observation_layout(saved['observations']['policy'], {}, list(JOINTS))
    playback = simulation_config(saved, saved['scene']['robot']['init_state'], layout)
    assert sum(term['size'] for term in layout) == 35
    assert playback['sim_reset_on_policy_entry'] is True
    assert 'sim_gait' not in playback
    assert all(pair == [0., 0.] for pair in playback['sim_command_ranges'].values())
    restored = cloudpickle.loads(cloudpickle.dumps(cfg))
    assert playback_contract(restored) == saved


def test_native_rewards_metrics_terminal_observation_and_timeout():
    if not torch.cuda.is_available():
        pytest.skip('Native mjlab physics requires CUDA')
    cfg = TitaStandOneLegReferenceEnvCfg(8)
    cfg.seed = 42
    env = TitaFlashSACEnv(ManagerBasedRlEnv(cfg, device='cuda:0'))
    try:
        assert (env.actor_obs_dim, env.critic_obs_dim, env.action_dim) == (35, 39, 8)
        raw = env.env
        env.reset(seed=42)
        torch.testing.assert_close(raw.scene['robot'].data.joint_pos,
                                   raw.scene['robot'].data.default_joint_pos)
        raw.episode_length_buf[:] = raw.max_episode_length-1
        obs, terminal_obs, reward, terminated, truncated, info = env.step(torch.zeros(8, 8, device=env.device))
        assert truncated.all() and not terminated.any()
        assert torch.isfinite(obs).all() and torch.isfinite(terminal_obs).all() and torch.isfinite(reward).all()
        for key in cfg.metrics:
            assert math.isfinite(float(info['log']['Episode_Metrics/'+key]))
        for _ in range(150):
            obs, _, reward, _, _, _ = env.step(torch.zeros(8, 8, device=env.device))
            assert torch.isfinite(obs).all() and torch.isfinite(reward).all()
            assert not raw.command_manager.get_command('base_velocity').any()
        env.reset()
        robot = raw.scene['robot']
        pose = robot.data.root_link_pose_w.clone()
        pose[:, 2], pose[:, 3:] = .08, pose.new_tensor([0., 1., 0., 0.])
        robot.write_root_link_pose_to_sim(pose)
        robot.write_root_link_velocity_to_sim(torch.zeros(8, 6, device=env.device))
        raw.sim.forward()
        _, _, _, terminated, _, _ = env.step(torch.zeros(8, 8, device=env.device))
        assert terminated.all()
    finally:
        env.close()
