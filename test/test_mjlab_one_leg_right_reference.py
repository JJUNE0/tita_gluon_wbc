"""TRAINING_SIM: mirrored right-only objectives and unchanged saved left task."""

from copy import deepcopy
import math
from pathlib import Path
import sys

import cloudpickle
import torch

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT / 'sim2sim/sim2sim_ros2_jazzy')]
from mj_lab.checkpoint import plain, playback_contract
from mj_lab.robots.tita.common.robot_cfg import JOINTS
from mj_lab.robots.tita.stand_one_leg.stand_one_leg_reference_env_cfg import (
    TitaStandOneLegReferenceEnvCfg, TitaStandOneLegRightReferenceEnvCfg,
    balance_metric, fixed_support, pose_hint, support_leg_tilt,
)
from sim2sim_ros2_jazzy.checkpoint import observation_layout, simulation_config
from test_mjlab_one_leg_reference import fake_env


def right_support_examples():
    env = fake_env(3)
    robot = env.scene['robot']
    robot.data.body_link_pos_w[0, 0, 2] += .04
    robot.data.body_link_pos_w[1, 1, 2] += .04
    hips = robot.data.body_link_pos_w.clone()
    hips[:, :, 2] += .3
    hips[:, 0, 0] += .1
    robot.data.body_link_pos_w = torch.cat((robot.data.body_link_pos_w, hips), dim=1)
    robot.body_names += ['left_leg_2', 'right_leg_2']
    env.scene['feet'].data.force[:, :, 2] = torch.tensor([[0., 130.], [130., 0.], [130., 130.]])
    angle = math.radians(-30.)
    robot.data.root_link_quat_w[:] = torch.tensor([math.cos(angle/2), math.sin(angle/2), 0., 0.])
    robot.data.joint_pos[:, [0, 4]] = math.radians(30.)
    return env


def test_right_reward_metrics_and_vertical_axis_use_the_requested_side():
    env = right_support_examples()
    torch.testing.assert_close(fixed_support(env, support_side='right'), torch.tensor([1., -1.25, -.25]))
    torch.testing.assert_close(balance_metric(env, 'single_support_fraction', 'right'), torch.tensor([1., 0., 0.]))
    torch.testing.assert_close(balance_metric(env, 'single_support_time_s', 'right'), torch.tensor([.02, 0., 0.]))
    torch.testing.assert_close(balance_metric(env, 'double_support_fraction', 'right'), torch.tensor([0., 0., 1.]))
    torch.testing.assert_close(pose_hint(env, support_side='right'), torch.tensor([1., 0., 1.]))
    torch.testing.assert_close(support_leg_tilt(env, 'right'), torch.zeros(3))
    assert (support_leg_tilt(env, 'left') > 0).all()
    env.termination_manager.terminated[0] = True
    assert balance_metric(env, 'single_support_fraction', 'right')[0] == 0.


def test_reward_and_success_measurements_are_mirror_equivalent():
    right = right_support_examples()
    left = deepcopy(right)
    robot = left.scene['robot']
    robot.data.body_link_pos_w = robot.data.body_link_pos_w[:, [1, 0, 3, 2]].clone()
    robot.data.body_link_pos_w[:, :, 1] *= -1
    robot.data.root_link_quat_w[:, 1] *= -1
    left.scene['feet'].data.force = left.scene['feet'].data.force[:, [1, 0]].clone()
    for function in (fixed_support, pose_hint, support_leg_tilt):
        torch.testing.assert_close(function(right, support_side='right'), function(left))
    for kind in ('single_support_fraction', 'single_support_time_s', 'double_support_fraction', 'swing_clearance_m', 'pose_hint'):
        torch.testing.assert_close(balance_metric(right, kind, 'right'), balance_metric(left, kind))


def test_right_config_changes_only_selected_reward_and_metric_sides():
    left, right = TitaStandOneLegReferenceEnvCfg(16), TitaStandOneLegRightReferenceEnvCfg(16)
    normalized = deepcopy(right)
    for name in ('single_support', 'pose_hint', 'support_leg_tilt'):
        assert normalized.rewards[name].params.pop('support_side') == 'right'
    for term in normalized.metrics.values():
        assert term.params.pop('support_side') == 'right'
    assert plain(left) == plain(normalized)
    saved = cloudpickle.loads(cloudpickle.dumps(right))
    assert plain(saved) == plain(right)
    assert saved.rewards['single_support'].params['support_side'] == 'right'
    assert all(term.params['support_side'] == 'right' for term in saved.metrics.values())
    contract = playback_contract(saved)
    layout = observation_layout(contract['observations']['policy'], {}, list(JOINTS))
    playback = simulation_config(contract, contract['scene']['robot']['init_state'], layout)
    assert sum(term['size'] for term in layout) == 35
    assert playback['sim_reset_on_policy_entry'] is True
    assert list(contract['commands']) == ['base_velocity']
    assert all(value == [0., 0.] for value in playback['sim_command_ranges'].values())
