"""TRAINING_SIM / VALIDATION_SIM: inline command mix, timing and wheel drive."""

from pathlib import Path
import sys
from types import SimpleNamespace

import numpy as np
import pytest
import torch

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / 'sim2sim/sim2sim_ros2_jazzy'))
from mj_lab.checkpoint import plain, playback_contract
from mj_lab.flash_sac import TitaFlashSACEnv
from mj_lab.robots.tita import mdp
from mj_lab.robots.tita.flat_env_cfg import TitaFlatEnvCfg
from mj_lab.robots.tita.walk.inline_env_cfg import TitaInlineEnvCfg
from mj_lab.robots.tita.common.robot_cfg import JOINTS
from mjlab.envs import ManagerBasedRlEnv
from sim2sim_ros2_jazzy.adapter import ActionAdapter, ObservationBuilder
from sim2sim_ros2_jazzy.checkpoint import action_layout, observation_layout, simulation_config


@pytest.fixture(scope='module')
def inline_env():
    cfg = TitaInlineEnvCfg(num_envs=8)
    cfg.seed = 42
    env = TitaFlashSACEnv(ManagerBasedRlEnv(cfg, device='cuda:0'))
    yield env
    env.close()


def test_flat_actions_physics_and_randomization_are_inherited(inline_env):
    env = inline_env
    cfg = TitaInlineEnvCfg(num_envs=8)
    flat = TitaFlatEnvCfg(num_envs=8)
    assert (env.actor_obs_dim, env.critic_obs_dim, env.action_dim) == (40, 44, 8)
    assert plain(cfg.actions) == plain(flat.actions)
    assert plain(cfg.events) == plain(flat.events)
    assert plain(cfg.scene) == plain(flat.scene)
    assert plain(cfg.sim) == plain(flat.sim)
    for name, term in flat.rewards.items():
        if name == 'ang_vel_xy_l2':
            assert name not in cfg.rewards
            continue
        assert cfg.rewards[name].weight == term.weight
        if name not in ('joint_mirror', 'joint_deviation_hip', 'joint_deviation_shoulder', 'flat_orientation_l2'):
            assert plain(cfg.rewards[name]) == plain(term)
    v = cfg.commands['base_velocity']
    assert (v.lin_vel_x, v.lin_vel_y, v.ang_vel_z) == ((-1.5, 1.5), (0., 0.), (-3., 3.))
    assert cfg.commands['gait'].frequency_range_hz == (.5, .5)
    assert cfg.commands['gait'].stance_fraction == .8


def test_gait_penalties_relax_only_during_straight_gait():
    cfg, flat = TitaInlineEnvCfg(num_envs=4), TitaFlatEnvCfg(num_envs=4)
    # Forward/backward gait and stationary/turning rows share identical states.
    enabled = torch.tensor([[1.], [1.], [0.], [0.]])
    gravity = torch.tensor([[.1, .2, -.95]]).repeat(4, 1)
    angular = torch.tensor([[2., 3., 4.]]).repeat(4, 1)
    position = torch.tensor([[.1, .2, .3, 0., .4, .5, .6, 0.]]).repeat(4, 1)
    d = SimpleNamespace(projected_gravity_b=gravity, root_link_ang_vel_b=angular,
                        joint_pos=position, default_joint_pos=torch.zeros_like(position))
    env = SimpleNamespace(scene={'robot': SimpleNamespace(data=d, joint_names=JOINTS)},
        command_manager=SimpleNamespace(get_command=lambda _: enabled, get_term=lambda _: None))

    def value(name):
        term = cfg.rewards[name]
        return term.weight * term.func(env, **term.params)

    up = 1.  # This near-upright state is above the existing 0.7 saturation.
    torch.testing.assert_close(value('ang_vel_roll_l2'), torch.tensor([-.01, -.01, -.05, -.05]) * 2.**2 * up)
    torch.testing.assert_close(value('ang_vel_pitch_l2'), torch.tensor([-.03, -.03, -.05, -.05]) * 3.**2 * up)
    # Splitting roll/pitch must preserve the old combined cost outside gait.
    before = flat.rewards['ang_vel_xy_l2']
    torch.testing.assert_close((value('ang_vel_roll_l2') + value('ang_vel_pitch_l2'))[2:],
                              (before.weight * before.func(env, **before.params))[2:])
    for name, moving, standing, raw in (
        ('flat_orientation_l2', -1., -5., (.1**2 + .2**2) * up),
        ('joint_deviation_hip', -.02, -1., .1 + .4),
        ('joint_deviation_shoulder', -.02, -.5, .2 + .5),
    ):
        torch.testing.assert_close(value(name), torch.tensor([moving, moving, standing, standing]) * raw)
    # The existing mirror exemption remains limited to gait.
    assert not value('joint_mirror')[:2].any()
    before = flat.rewards['joint_mirror']
    torch.testing.assert_close(value('joint_mirror')[2:], (before.weight * before.func(env, **before.params))[2:])


def test_fixed_half_straight_cohort_and_partial_resampling(inline_env):
    env = inline_env
    env.reset()
    v = mdp.velocity(env.env)
    ids = torch.arange(8, device=env.device)
    standing = v.cfg.rel_standing_envs
    v.cfg.rel_standing_envs = 1.
    try:
        for _ in range(20):
            v._resample_command(ids)
            assert not v.target[:4, 1:].any()
            assert not v.target[4:].any()
            assert (v.target[:4, 0] != 0).all()
        before = v.target.clone()
        v._resample_command(ids[[0, 5]])
        torch.testing.assert_close(v.target[[1, 2, 3, 4, 6, 7]], before[[1, 2, 3, 4, 6, 7]])
    finally:
        v.cfg.rel_standing_envs = standing
    env.reset()


def test_only_straight_commands_enable_gait_and_wheels_keep_driving(inline_env):
    env = inline_env
    raw = env.env
    env.reset()
    v, gait = mdp.velocity(raw), raw.command_manager.get_term('gait')
    v.time_left[:] = 1e9
    v.target[:] = v.target.new_tensor([[.5, 0, 0], [-.5, 0, 0], [0, 0, 0], [0, 0, .5],
                                    [.5, 0, .5], [-.5, 0, -.5], [.5, .1, 0], [.01, 0, 0]])
    raw.episode_length_buf[:] = 60
    raw.command_manager.compute(raw.step_dt)
    torch.testing.assert_close(gait.command[:, 0], v.target.new_tensor([1, 1, 0, 0, 0, 0, 0, 0]))
    raw.action_manager.process_action(torch.ones(8, 8, device=env.device))
    for name in ('joint_vel_3', 'joint_vel_7'):
        torch.testing.assert_close(raw.action_manager.get_term(name)._processed_actions, torch.full((8, 1), 20., device=env.device))
    saved = playback_contract(raw.cfg)
    layout = observation_layout(saved['observations']['policy'], {}, list(JOINTS))
    cfg = simulation_config(saved, saved['scene']['robot']['init_state'], layout)
    actions = action_layout(saved['actions'], {}, list(JOINTS), saved['scene']['robot']['init_state'])
    cfg['policy_interface'] = dict(observations=layout, actions=actions)
    assert sum(t.get('gate') == 'always' for t in actions) == 2
    adapter = ActionAdapter(cfg)
    for enabled in (False, True):
        np.testing.assert_allclose(adapter.targets(np.ones(8), gait_enabled=enabled)[[3, 7]], [20., 20.])
    # Compare saved native and sim2sim gating for the same emitted commands.
    for row in range(8):
        builder = ObservationBuilder(cfg)
        for _ in range(60):
            builder.advance_gait(v.command[row].cpu().numpy())
        assert bool(builder.gait_enabled) == bool(gait.command[row, 0])
    env.reset()


def test_two_second_cycle_has_point_four_second_swing_and_single_support(inline_env):
    env = inline_env
    raw = env.env
    env.reset()
    v, gait = mdp.velocity(raw), raw.command_manager.get_term('gait')
    v.target[:] = v.target.new_tensor([.5, 0, 0])
    v.time_left[:] = 1e9
    gait.phase.zero_()
    raw.episode_length_buf[:] = 60
    swings = []
    for _ in range(100):
        raw.command_manager.compute(raw.step_dt)
        stance, height = mdp.gait_reference(gait.phase, gait.command[:, 0], gait.cfg.stance_fraction)
        assert stance.any(dim=1).all()
        assert (height <= .040001).all()
        swings.append((~stance[0]).cpu().numpy())
    swings = np.asarray(swings)
    np.testing.assert_allclose(swings.sum(axis=0) * raw.step_dt, [.4, .4], atol=.04)
    starts = [np.flatnonzero(swings[:, side])[0] for side in (0, 1)]
    assert abs(starts[0] - starts[1]) * raw.step_dt == pytest.approx(1., abs=.04)
    assert ((~swings).all(axis=1)).sum() * raw.step_dt == pytest.approx(1.2, abs=.04)
    env.reset()


def test_stance_push_removes_rigid_body_motion_and_reverses_for_backward():
    # World translation and yaw rotation alone must not count as leg push.
    offset = torch.tensor([[[1., 0., 0.], [-1., 0., 0.]]])
    linear = torch.tensor([[1., 2., 0.]])
    angular = torch.tensor([[0., 0., 3.]])
    rigid = linear[:, None] + torch.cross(angular[:, None].expand_as(offset), offset, dim=-1)
    quat = torch.tensor([[2**-.5, 0., 0., 2**-.5]])
    d = SimpleNamespace(body_link_pos_w=offset, root_link_pos_w=torch.zeros(1, 3),
        root_link_ang_vel_w=angular, root_link_lin_vel_w=linear,
        root_link_quat_w=quat, projected_gravity_b=torch.tensor([[0., 0., -1.]]))
    gait = SimpleNamespace(phase=torch.zeros(1), frequency=torch.tensor([.5]),
        command=torch.tensor([[1.]]), cfg=SimpleNamespace(stance_fraction=.8))
    velocity = SimpleNamespace(command=torch.tensor([[.5, 0., 0.]]))
    env = SimpleNamespace(scene={'robot': SimpleNamespace(data=d, body_names=['left_leg_4', 'right_leg_4'])},
        command_manager=SimpleNamespace(get_term=lambda name: gait if name == 'gait' else velocity))
    speed = .06 * .5 / .8
    d.body_link_lin_vel_w = rigid + torch.tensor([0., -speed, 0.])
    torch.testing.assert_close(mdp.stance_push(env), torch.ones(1))
    d.body_link_lin_vel_w = rigid
    assert float(mdp.stance_push(env)[0]) < 1.
    velocity.command[:, 0] = -.5
    d.body_link_lin_vel_w = rigid + torch.tensor([0., speed, 0.])
    torch.testing.assert_close(mdp.stance_push(env), torch.ones(1))
    gait.command.zero_()
    assert not mdp.stance_push(env).any()


def test_contact_schedule_handles_mjlab_negative_support_forces():
    # Both support and one-foot swing must be recognized for either wrench sign.
    force = torch.tensor([[[0., 0., -130.], [0., 0., -130.]],
                          [[0., 0., 130.], [0., 0., 130.]],
                          [[0., 0., 0.], [0., 0., -130.]],
                          [[0., 0., 0.], [0., 0., 130.]],
                          [[0., 0., 0.], [0., 0., 0.]]])
    gait = SimpleNamespace(phase=torch.tensor([0., 0., .9, .9, 0.]),
        command=torch.ones(5, 1), cfg=SimpleNamespace(stance_fraction=.8))
    robot = SimpleNamespace(data=SimpleNamespace(projected_gravity_b=torch.tensor([[0., 0., -1.]]).repeat(5, 1)))
    env = SimpleNamespace(scene={'robot': robot, 'feet': SimpleNamespace(data=SimpleNamespace(force=force))},
        command_manager=SimpleNamespace(get_term=lambda _: gait))
    value = mdp.contact_schedule(env)
    torch.testing.assert_close(value[:4], torch.ones(4))
    assert value[4] == pytest.approx(float(np.exp(-4)))
    gait.command.zero_()
    assert not mdp.contact_schedule(env, only_when_enabled=True).any()
