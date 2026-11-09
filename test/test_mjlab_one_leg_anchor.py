"""DESKTOP_DRY_RUN / VALIDATION_SIM: fixed anchors, low swings, and free slow yaw."""

from copy import deepcopy
from pathlib import Path
import sys
from types import SimpleNamespace

import cloudpickle
import pytest
import torch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from mj_lab.checkpoint import plain, playback_contract
from mj_lab.flash_sac import TitaFlashSACEnv
from mj_lab.robots.tita.stand_one_leg.stand_one_leg_anchor_env_cfg import (
    TitaStandOneLegAnchorEnvCfg, TitaStandOneLegRightAnchorEnvCfg,
    anchor_metric, support_drift_failure, support_hold, support_motion_cost, support_speed_soft_l1,
    lift_first_support, swing_height_excess, swing_near_com, wheel_overlap_cost, yaw_excess,
)
from mj_lab.robots.tita.stand_one_leg.stand_one_leg_reference_env_cfg import TitaStandOneLegReferenceEnvCfg


def example(side='left'):
    support = 0 if side == 'left' else 1
    command = SimpleNamespace(cfg=SimpleNamespace(support_side=side), support_id=support,
                              swing_id=1-support, support_anchor_xy=torch.zeros(4, 2))
    positions = torch.zeros(4, 2, 3)
    positions[:, support, 2] = .0925
    positions[:, 1-support, 2] = torch.tensor([.1325, .1725, .2125, .1125])
    positions[:, 1-support, 0] = torch.tensor([.04, .10, .20, .30])
    values = SimpleNamespace(body_link_pos_w=positions, body_link_lin_vel_w=torch.zeros(4, 2, 3),
                             root_link_lin_vel_w=torch.zeros(4, 3),
                             root_link_ang_vel_w=torch.zeros(4, 3))
    forces = torch.zeros(4, 2, 3)
    forces[:, support, 2] = 100.
    class Scene(dict):
        env_origins = torch.zeros(4, 3)
    scene = Scene(robot=SimpleNamespace(data=values, body_names=['left_leg_4', 'right_leg_4'],
                                        indexing=SimpleNamespace(root_body_id=0)),
                  feet=SimpleNamespace(data=SimpleNamespace(force=forces)))
    return SimpleNamespace(scene=scene, command_manager=SimpleNamespace(get_term=lambda _: command),
        sim=SimpleNamespace(data=SimpleNamespace(subtree_com=torch.zeros(4, 1, 3))), step_dt=.02,
        termination_manager=SimpleNamespace(terminated=torch.zeros(4, dtype=torch.bool)))


@pytest.mark.parametrize('side', ['left', 'right'])
def test_fixed_position_costs_detect_slow_drift_and_ignore_body_pivot(side):
    env = example(side)
    command = env.command_manager.get_term('base_velocity')
    data = env.scene['robot'].data
    data.body_link_pos_w[:, command.support_id, 0] = torch.tensor([0., .05, .09, .101])
    assert support_drift_failure(env).tolist() == [False, False, False, True]
    data.root_link_lin_vel_w = torch.ones(4, 3)  # Body may orbit the fixed support point.
    torch.testing.assert_close(support_motion_cost(env, 'speed', .1), torch.zeros(4))
    data.body_link_lin_vel_w[:, command.support_id, 0] = .1
    torch.testing.assert_close(support_motion_cost(env, 'speed', .1), torch.ones(4))
    first = support_drift_failure(env).clone()
    support_hold(env)
    anchor_metric(env, 'support_drift_m')
    torch.testing.assert_close(support_drift_failure(env), first)
    assert not command.support_anchor_xy.any()  # No reward/metric side effects.


def test_yaw_deadband_and_height_ceiling_have_separate_objectives():
    env = example()
    env.scene['robot'].data.root_link_ang_vel_w[:, 2] = torch.tensor([0., .5, -.5, 1.])
    torch.testing.assert_close(yaw_excess(env), torch.tensor([0., 0., 0., .25]))
    torch.testing.assert_close(swing_height_excess(env), torch.tensor([0., 0., 1., 0.]), atol=1e-6, rtol=1e-5)
    # Raising a wheel cannot improve its horizontal COM score.
    before = swing_near_com(env)
    env.scene['robot'].data.body_link_pos_w[:, 1, 2] += .1
    torch.testing.assert_close(swing_near_com(env), before)
    assert torch.all(before[:-1] > before[1:])
    env.scene['feet'].data.force[:, 1, 2] = 100.
    assert not swing_near_com(env).any()


def test_com_is_whole_robot_not_torso_and_failed_lifts_never_count():
    env = example()
    env.sim.data.subtree_com[:, 0, 0] = .04
    assert swing_near_com(env)[0] == 1.
    env.termination_manager.terminated[:] = True
    assert not anchor_metric(env, 'anchored_low_support_time_s').any()


def test_tucking_does_not_reward_intersecting_the_support_wheel_as_success():
    env = example()
    # First sample is close to COM but its wheel overlaps the support proxy.
    assert swing_near_com(env)[0] > swing_near_com(env)[-1]
    assert wheel_overlap_cost(env)[0] > 0.
    assert wheel_overlap_cost(env)[-1] == 0.
    assert anchor_metric(env, 'anchored_low_support_fraction')[0] == 0.


def test_mirrored_configs_preserve_legacy_contract_and_only_change_support_side():
    legacy = TitaStandOneLegReferenceEnvCfg(4)
    left, right = TitaStandOneLegAnchorEnvCfg(4), TitaStandOneLegRightAnchorEnvCfg(4)
    for cfg in (left, right):
        for name in ('observations', 'actions', 'events', 'sim'):
            assert plain(getattr(cfg, name)) == plain(getattr(legacy, name))
        assert 'stationary' not in cfg.rewards and cfg.rewards['pose_hint'].weight == .5
        assert set(cfg.terminations) == set(legacy.terminations)
        assert 'support_drift' not in cfg.terminations
        assert playback_contract(cfg) == playback_contract(legacy)
        assert plain(cloudpickle.loads(cloudpickle.dumps(cfg))) == plain(cfg)
    normalized = deepcopy(right)
    normalized.commands['base_velocity'].support_side = 'left'
    for name in ('single_support', 'support_leg_tilt', 'pose_hint'):
        normalized.rewards[name].params['support_side'] = 'left'
    for term in normalized.metrics.values():
        if 'support_side' in term.params:
            term.params['support_side'] = 'left'
    assert plain(normalized) == plain(left)


def test_first_lift_has_priority_without_stronger_wrong_contact_costs():
    env = example()
    cfg = TitaStandOneLegAnchorEnvCfg(4)
    assert cfg.rewards['single_support'].weight == 2.
    assert cfg.rewards['single_support'].params['lift_gain'] == 2.
    assert lift_first_support(env)[0] == pytest.approx(2.)
    env.scene['feet'].data.force[:, 1, 2] = 100.
    env.scene['robot'].data.body_link_pos_w[:, 1, 2] = .0925
    torch.testing.assert_close(lift_first_support(env), torch.full((4,), -.25))
    env.scene['feet'].data.force[:, 0] = 0.
    torch.testing.assert_close(lift_first_support(env), torch.full((4,), -1.25))
    assert cfg.rewards['support_speed'].weight == -.05
    assert cfg.rewards['support_position'].weight == -.05
    assert cfg.rewards['support_hold'].weight == .1
    assert cfg.rewards['swing_near_com'].weight == .1
    assert cfg.rewards['swing_height_excess'].weight == -.05
    # A 12 cm lift is a soft cost of .05 versus full positive lift credit 4.
    env.scene['robot'].data.body_link_pos_w[:, 1, 2] = .2125
    torch.testing.assert_close(.05*swing_height_excess(env), torch.full((4,), .05), atol=1e-6, rtol=1e-5)


def test_velocity_costs_have_no_deadband_or_fast_speed_plateau():
    env = example()
    cfg = TitaStandOneLegAnchorEnvCfg(4)
    yaw = cfg.rewards['yaw_excess']
    assert yaw.weight == -.05 and yaw.params['free_rate_rad_s'] == 0.
    angular = env.scene['robot'].data.root_link_ang_vel_w
    angular[:, 2] = torch.tensor([0., 1e-5, -.1, .1])
    costs = yaw.func(env, **yaw.params)
    assert costs[0] == 0. and costs[1] > 0.
    torch.testing.assert_close(costs[2], costs[3])
    # Legacy saved parameters still retain the former yaw deadband.
    assert yaw_excess(env, free_rate_rad_s=.5).sum() == 0.
    velocity = env.scene['robot'].data.body_link_lin_vel_w
    velocity[:, 0, 0] = torch.tensor([0., 1e-6, .2, 2.])
    costs = support_speed_soft_l1(env)
    assert costs[0] == 0. and torch.all(costs[1:] > costs[:-1])
    before = costs.clone()
    velocity[:, 0, 0] *= -1
    torch.testing.assert_close(support_speed_soft_l1(env), before)
    # Doubling a large speed still increases cost, without quadratic blowup.
    velocity[:, 0, 0] = torch.tensor([1., 2., 4., 8.])
    costs = support_speed_soft_l1(env)
    assert torch.all(costs[1:] > costs[:-1])
    assert torch.all(costs[1:] / costs[:-1] < 2.2)


@pytest.mark.parametrize('cfg_type', [TitaStandOneLegAnchorEnvCfg, TitaStandOneLegRightAnchorEnvCfg])
def test_native_anchor_partial_reset_and_drift_does_not_terminate(cfg_type):
    if not torch.cuda.is_available():
        pytest.skip('Native mjlab requires CUDA')
    from mjlab.envs import ManagerBasedRlEnv
    cfg = cfg_type(4)
    cfg.seed = 42
    env = TitaFlashSACEnv(ManagerBasedRlEnv(cfg, device='cuda:0'))
    try:
        raw = env.env
        assert (env.actor_obs_dim, env.critic_obs_dim, env.action_dim) == (35, 39, 8)
        env.reset(seed=42)
        command, robot = raw.command_manager.get_term('base_velocity'), raw.scene['robot']
        initial = command.support_anchor_xy.clone()
        torch.testing.assert_close(initial, robot.data.body_link_pos_w[:, command.support_id, :2])
        for _ in range(12):
            obs, terminal, reward, _, _, _ = env.step(torch.zeros(4, 8, device=env.device))
            assert torch.isfinite(obs).all() and torch.isfinite(terminal).all() and torch.isfinite(reward).all()
        env.reset(seed=42)
        initial = command.support_anchor_xy.clone()
        # Move two rows; reset only one of them. Only that row gets a new anchor.
        pose = robot.data.root_link_pose_w.clone()
        pose[:2, 0] += .25
        robot.write_root_link_pose_to_sim(pose)
        raw.sim.forward()
        raw.reset(env_ids=torch.tensor([0], device=env.device))
        torch.testing.assert_close(command.support_anchor_xy[1:], initial[1:])
        torch.testing.assert_close(command.support_anchor_xy[0], robot.data.body_link_pos_w[0, command.support_id, :2])
        assert support_drift_failure(raw).tolist() == [False, True, False, False]
        _, _, _, terminated, truncated, info = env.step(torch.zeros(4, 8, device=env.device))
        assert not terminated[1] and not truncated[1]
        assert raw.episode_length_buf[1] == 1
        assert 'support_drift' not in raw.termination_manager.active_terms
        torch.testing.assert_close(command.support_anchor_xy[1], initial[1])
        assert support_drift_failure(raw)[1]  # Outside radius but still running.
        # A timed-out episode remains a truncation, rather than a failure.
        env.reset(seed=42)
        raw.episode_length_buf[:] = raw.max_episode_length-1
        _, _, _, terminated, truncated, info = env.step(torch.zeros(4, 8, device=env.device))
        assert truncated.all() and not terminated.any()
        for key in cfg.metrics:
            assert torch.isfinite(torch.as_tensor(info['log']['Episode_Metrics/'+key]))
    finally:
        env.close()
