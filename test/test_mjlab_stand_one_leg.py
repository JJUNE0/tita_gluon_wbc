"""TRAINING_SIM: single-leg contact, free body tilt and zero-command gait."""

from pathlib import Path
import sys
from types import SimpleNamespace

import cloudpickle
import pytest
import torch
from mjlab.envs import ManagerBasedRlEnv

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / 'sim2sim/sim2sim_ros2_jazzy'))
from mj_lab.checkpoint import plain, playback_contract
from mj_lab.flash_sac import TitaFlashSACEnv
from mj_lab.robots.tita import mdp
from mj_lab.robots.tita.inline_env_cfg import TitaInlineEnvCfg
from mj_lab.robots.tita.stand_one_leg_env_cfg import (
    TitaStandOneLegEnvCfg, gait_support, stationary, support_leg_tilt,
)
from sim2sim_ros2_jazzy.adapter import ObservationBuilder
from sim2sim_ros2_jazzy.checkpoint import observation_layout, simulation_config


def fake_env(count):
    # Hip/foot pairs on left and right; actual hip pivot is the leg_2 origin.
    names = ['left_leg_2', 'left_leg_4', 'right_leg_2', 'right_leg_4']
    pos = torch.tensor([[[0., .2, .4], [0., .2, .0925],
                         [0., -.2, .4], [0., -.2, .0925]]]).repeat(count, 1, 1)
    data = SimpleNamespace(body_link_pos_w=pos, root_link_lin_vel_w=torch.zeros(count, 3),
        root_link_ang_vel_w=torch.zeros(count, 3), projected_gravity_b=torch.tensor([[0., 0., -1.]]).repeat(count, 1))
    force = torch.zeros(count, 2, 3)
    gait = SimpleNamespace(phase=torch.full((count,), .875), command=torch.ones(count, 5),
                           cfg=SimpleNamespace(stance_fraction=.75))
    scene = {'robot': SimpleNamespace(data=data, body_names=names), 'feet': SimpleNamespace(data=SimpleNamespace(force=force))}
    class Scene(dict):
        env_origins = torch.zeros(count, 3)
    return SimpleNamespace(scene=Scene(scene), command_manager=SimpleNamespace(get_term=lambda _: gait))


def test_contact_clearance_requires_correct_support_and_has_no_grounded_swing_bonus():
    env = fake_env(8)
    pos, force = env.scene['robot'].data.body_link_pos_w, env.scene['feet'].data.force
    pos[:, 1, 2] += .04  # left swing; right support at phase .875
    force[:, 1, 2] = -130.
    force[1, 0, 2] = -130.  # both grounded: no swing credit
    force[2, :, 2] = torch.tensor([-130., 0.])  # wrong support foot
    force[3] = 0.  # both airborne
    pos[4, 1, 2] -= .02  # half clearance
    pos[5, 1, 2] += .04  # higher clearance adds no bonus
    gait = env.command_manager.get_term('gait')
    gait.phase[6] = .1  # double support
    force[6, :, 2] = 130.  # force sign must not matter
    gait.command[7, 0] = 0.
    # Swing contact and missing stance contact each cost one; swapping feet costs two.
    torch.testing.assert_close(gait_support(env), torch.tensor([1., -1., -2., -1., .5, 1., 1., 0.]))
    # A change of world origin must not change physical clearance credit.
    env.scene.env_origins[:, 2] = 3.
    pos[:, :, 2] += 3.
    torch.testing.assert_close(gait_support(env), torch.tensor([1., -1., -2., -1., .5, 1., 1., 0.]), atol=1e-5, rtol=1e-5)


def test_support_axis_uses_world_vertical_and_ignores_swing_leg():
    env = fake_env(5)
    pos = env.scene['robot'].data.body_link_pos_w
    pos[:, 0] += torch.tensor([10., 0., 0.])  # swing leg may move freely
    pos[1, 2] = pos[1, 3] + torch.tensor([.2, 0., .2])  # 45-degree supporting leg
    pos[2, 2] = pos[2, 3] + torch.tensor([0., 0., -.2])  # inverted axis is not vertical support
    gait = env.command_manager.get_term('gait')
    gait.phase[3] = .1
    gait.command[4, 0] = 0.
    torch.testing.assert_close(support_leg_tilt(env), torch.tensor([0., 1.-2**-.5, 2., 0., 0.]))


def test_body_tilt_and_roll_pitch_rate_are_unpenalized():
    env = fake_env(4)
    data, force = env.scene['robot'].data, env.scene['feet'].data.force
    data.body_link_pos_w[:, 1, 2] += .04
    force[:, 1, 2] = -130.
    data.projected_gravity_b[:] = torch.tensor([[0., 0., -1.], [0., .5, -.866], [0., .866, -.5], [0., 1., 0.]])
    data.root_link_ang_vel_w[:, :2] = torch.tensor([2., 3.])
    torch.testing.assert_close(gait_support(env), torch.ones(4))
    torch.testing.assert_close(support_leg_tilt(env), torch.zeros(4))
    torch.testing.assert_close(stationary(env), torch.zeros(4))
    data.root_link_lin_vel_w[0, :2] = torch.tensor([.2, .3])
    data.root_link_ang_vel_w[0, 2] = 2.
    assert stationary(env)[0] == pytest.approx(.53)


def test_first_two_seconds_reward_double_support_without_body_flat_constraint():
    env = fake_env(4)
    gait = env.command_manager.get_term('gait')
    gait.command[:, 0] = 0.
    force = env.scene['feet'].data.force
    force[:3, 1, 2] = -130.
    force[:2, 0, 2] = -130.
    env.scene['robot'].data.projected_gravity_b[1] = torch.tensor([0., 1., 0.])
    torch.testing.assert_close(gait_support(env), torch.tensor([1., 1., 0., 0.]))


def test_acceleration_regularization_is_one_term_including_legs_and_wheels():
    cfg = TitaStandOneLegEnvCfg(2)
    assert 'joint_acc_l2' not in cfg.rewards  # dof_acc_l2 is the name, not another cost.
    term = cfg.rewards['dof_acc_l2']
    assert term.weight == -2.5e-7 and term.params == {'kind': 'joint_acc_l2'}
    env = fake_env(2)
    data = env.scene['robot'].data
    data.joint_acc = torch.zeros(2, 8)
    data.joint_acc[0, 0] = 100.  # leg
    data.joint_acc[1, 3] = 100.  # wheel
    data.projected_gravity_b[1] = torch.tensor([0., 1., 0.])
    result = term.weight * term.func(env, **term.params)
    torch.testing.assert_close(result, torch.tensor([-.0025, -.0025]))


@pytest.fixture(scope='module')
def one_leg_env():
    if not torch.cuda.is_available():
        pytest.skip('Native mjlab physics requires CUDA')
    cfg = TitaStandOneLegEnvCfg(8)
    cfg.seed = 42
    wrapped = TitaFlashSACEnv(ManagerBasedRlEnv(cfg, device='cuda:0'))
    yield wrapped
    wrapped.close()


def test_native_config_zero_commands_timing_and_saved_gait(one_leg_env):
    env, raw = one_leg_env, one_leg_env.env
    cfg, parent = raw.cfg, TitaInlineEnvCfg(8)
    for key in ('actions', 'observations', 'sim'):
        assert plain(getattr(cfg, key)) == plain(getattr(parent, key))
    for name, term in parent.events.items():
        if name not in ('reset_base', 'reset_joints'):
            assert plain(cfg.events[name]) == plain(term)
    assert cfg.events['reset_joints'].params['position_range'] == (1., 1.)
    assert all(bounds == (0., 0.) for bounds in cfg.events['reset_base'].params['velocity_range'].values())
    assert set(cfg.rewards) == {'gait_support', 'support_leg_tilt', 'stationary', 'action_rate', 'dof_acc_l2', 'termination'}
    assert (env.actor_obs_dim, env.critic_obs_dim, env.action_dim) == (40, 44, 8)
    env.reset()
    d = raw.scene['robot'].data
    torch.testing.assert_close(d.joint_pos, d.default_joint_pos)
    torch.testing.assert_close(d.root_link_lin_vel_w, torch.zeros_like(d.root_link_lin_vel_w))
    velocity, gait = mdp.velocity(raw), raw.command_manager.get_term('gait')
    assert not gait.command[:, 0].any()  # initial settling
    for age in (50, 99, 100):
        raw.episode_length_buf[:] = age
        raw.command_manager.compute(raw.step_dt)
        assert not gait.command[:, 0].any()
    raw.episode_length_buf[:] = 120
    gait.phase.zero_()
    swings = []
    for _ in range(100):
        raw.command_manager.compute(raw.step_dt)
        assert not velocity.command.any() and gait.command[:, 0].all()
        stance, _ = mdp.gait_reference(gait.phase, gait.command[:, 0], gait.cfg.stance_fraction)
        assert stance.any(dim=1).all()
        swings.append((~stance[0]).cpu())
    swings = torch.stack(swings)
    torch.testing.assert_close(swings.sum(dim=0) * raw.step_dt, torch.tensor([.5, .5]), atol=.02, rtol=0.)
    starts = [torch.nonzero(swings[:, side])[0].item() for side in (0, 1)]
    # Float32 phase thresholds can move the crossing by one control tick.
    assert abs(abs(starts[0]-starts[1]) - round(1. / raw.step_dt)) <= 1
    saved = playback_contract(cfg)
    assert saved['sim_reset_on_policy_entry'] is True
    layout = observation_layout(saved['observations']['policy'], {}, list(raw.scene['robot'].joint_names))
    playback = simulation_config(saved, saved['scene']['robot']['init_state'], layout)
    assert all(bounds == [0., 0.] for bounds in playback['sim_command_ranges'].values())
    assert playback['sim_reset_on_policy_entry'] is True
    legacy = dict(saved)
    del legacy['sim_reset_on_policy_entry']
    assert 'sim_reset_on_policy_entry' not in simulation_config(legacy, saved['scene']['robot']['init_state'], layout)
    with pytest.raises(ValueError, match='must be boolean'):
        simulation_config(dict(saved, sim_reset_on_policy_entry='true'), saved['scene']['robot']['init_state'], layout)
    playback['policy_interface'] = {'observations': layout}
    builder = ObservationBuilder(playback)
    for _ in range(100):
        builder.advance_gait([0., 0., 0.])
    assert not builder.gait_enabled
    builder.advance_gait([0., 0., 0.])
    assert builder.gait_enabled
    env.reset()


def test_contact_termination_remains_active_during_the_standing_phase(one_leg_env):
    env, raw = one_leg_env, one_leg_env.env
    env.reset()
    robot = raw.scene['robot']
    pose = robot.data.root_link_pose_w.clone()
    pose[:, 2] = .08
    pose[:, 3:] = pose.new_tensor([0., 1., 0., 0.])
    robot.write_root_link_pose_to_sim(pose)
    robot.write_root_link_velocity_to_sim(torch.zeros(8, 6, device=env.device))
    raw.sim.forward()
    assert not raw.command_manager.get_command('gait')[:, 0].any()
    _, _, _, terminated, _, _ = env.step(torch.zeros(8, 8, device=env.device))
    assert terminated.all()
    env.reset()


def test_native_finite_steps_and_environment_pickle(one_leg_env):
    env = one_leg_env
    env.reset()
    for _ in range(120):
        obs, _, reward, _, _, _ = env.step(torch.zeros(8, 8, device=env.device))
        assert torch.isfinite(obs).all() and torch.isfinite(reward).all()
    restored = cloudpickle.loads(cloudpickle.dumps(env.env.cfg))
    assert plain(restored.rewards) == plain(env.env.cfg.rewards)
    assert restored.commands['gait'].step_in_place
