"""TRAINING_SIM / VALIDATION_SIM: full IDLE action envelope and sit/rise goals."""

from dataclasses import replace
from pathlib import Path
import sys
from types import SimpleNamespace

import cloudpickle
import numpy as np
import pytest
import torch

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT / "sim2sim/sim2sim_ros2_jazzy")]
from mj_lab.checkpoint import plain, playback_contract
from mj_lab.robots.tita import mdp
from mj_lab.robots.tita.roll_pitch_height.flat_env_roll_pitch_height_cfg import TitaFlatRollPitchHeightEnvCfg
from mj_lab.robots.tita.sit_stand.sit_stand_env_cfg import TitaSitStandEnvCfg, curriculum_contact, height_scaled_penalty
from mj_lab.robots.tita.common.robot_cfg import INITIAL_Q
from sim2sim_ros2_jazzy import checkpoint
from sim2sim_ros2_jazzy.state_machine import SPLAY_POSE


def command_env(n):
    velocity = SimpleNamespace(command=torch.zeros(n, 3))
    env = SimpleNamespace(num_envs=n, device="cpu", command_manager=SimpleNamespace(get_term=lambda _: velocity))
    return env, velocity


def full_sit_stand(n):
    cfg = TitaSitStandEnvCfg(n)
    cfg.set_training_step(cfg.curriculum_transition_step)
    return cfg


def test_idles_and_upper_standing_targets_fit_action_envelope():
    cfg = TitaSitStandEnvCfg(1)
    negative, positive = np.array(cfg.action_gain_negative), np.array(cfg.action_gain_positive)
    defaults = np.array(INITIAL_Q)
    a = (SPLAY_POSE - defaults) / .25 / np.where(SPLAY_POSE >= defaults, positive, negative)
    assert (np.abs(a) <= 1.+1e-7).all()
    actual = defaults + .25*a*np.where(a >= 0, positive, negative)
    np.testing.assert_allclose(actual, SPLAY_POSE, atol=1e-7)
    # 50 cm static solution requires roughly -0.71 rad knee PD targets.
    np.testing.assert_allclose((defaults - .25*negative)[[0, 2, 4, 6]], [-.75, -2.7, -.75, -2.7])
    np.testing.assert_allclose((defaults + .25*positive)[[2, 6]], [-.7, -.7])
    np.testing.assert_array_equal(positive[[3, 7]], [6., 6.])


def test_task_preserves_physics_dr_and_other_rewards():
    cfg, old = TitaSitStandEnvCfg(4), TitaFlatRollPitchHeightEnvCfg(4)
    for name in ("events", "sim", "scene", "actions", "observations"):
        assert plain(getattr(cfg, name)) == plain(getattr(old, name))
    assert set(cfg.terminations) == {"time_out", "base_contact", "knee_contact"}
    assert set(old.terminations) == {"time_out", "base_contact"}
    assert cfg.episode_length_s == 40.
    assert list(cfg.rewards) == list(old.rewards)
    for name in cfg.rewards:
        if name == "base_height_l2":
            assert cfg.rewards[name].weight == 5*old.rewards[name].weight == -50.
        else:
            assert cfg.rewards[name].weight == old.rewards[name].weight
        if name not in ("undesired_contacts", "joint_deviation_hip", "joint_deviation_shoulder"):
            expected = plain(old.rewards[name])
            if name == "base_height_l2":
                expected['weight'] = -50.
            assert plain(cfg.rewards[name]) == expected
    assert old.commands["base_pose"].height_range == (.27, .42)
    assert not hasattr(old, "action_gain_negative")


@pytest.mark.parametrize('stage', [1, 2])
def test_half_stop_sampling_keeps_varied_pose_goals_and_motion_transitions(stage):
    torch.manual_seed(42)
    cfg = TitaSitStandEnvCfg(10000)
    if stage == 2:
        cfg.set_training_step(20000)
    fake = SimpleNamespace(num_envs=10000, device='cpu', cfg=cfg)
    velocity = cfg.commands['base_velocity'].build(fake)
    pose = cfg.commands['base_pose'].build(fake)
    ids = torch.arange(fake.num_envs)
    velocity._resample_command(ids)
    pose.reset(ids)
    stopped = (velocity.target == 0).all(1)
    assert abs(float(stopped.float().mean())-.5) < .02
    assert ((velocity.target[~stopped, 0] != 0) | (velocity.target[~stopped, 2] != 0)).all()
    # Standstill means zero velocity, not a forced zero roll/pitch/nominal height.
    assert (pose.target[stopped, :2].abs().amax(1) > .1).float().mean() > .2
    assert pose.target[stopped, 2].std() > .05
    assert (pose.target[stopped] == torch.tensor([0.,0.,.335])).all(1).float().mean() > .05
    low = pose.target[:, 2] < .2
    if stage == 2:
        assert low.any() and (pose.target[low, :2] == 0).all()
    previous = stopped.clone()
    velocity._resample_command(ids)
    stopped = (velocity.target == 0).all(1)
    assert (stopped & ~previous).sum() > 1500
    assert (~stopped & previous).sum() > 1500
    saved = cloudpickle.loads(cloudpickle.dumps(cfg))
    assert saved.commands['base_velocity'].rel_standing_envs == .5
    assert saved.rewards['base_height_l2'].weight == -50.


def test_sampling_alternates_per_environment_and_partial_reset_is_local():
    torch.manual_seed(42)
    cfg = full_sit_stand(1).commands["base_pose"]
    fake, velocity = command_env(10000)
    command = cfg.build(fake)
    ids = torch.arange(fake.num_envs)
    command.reset(ids)
    low = command.target[:, 2] <= .12
    assert abs(float(low.float().mean()) - .5) < .02
    assert (command.target[low, :2] == 0).all()
    command._resample_command(ids)
    assert torch.equal(command.target[:, 2] <= .12, ~low)
    command.compute(.02)
    before = [x.clone() for x in (command.command, command.target, command.time_left, command._next_low, velocity.command)]
    command.reset(torch.tensor([0]))
    command.compute(0., torch.tensor([0]))
    for tensor, saved in zip((command.command, command.target, command.time_left, command._next_low, velocity.command), before):
        torch.testing.assert_close(tensor[1:], saved[1:], atol=0, rtol=0)


def test_full_sweep_reaches_both_ends_and_low_motion_is_zero():
    cfg = full_sit_stand(1).commands["base_pose"]
    fake, velocity = command_env(2)
    command = cfg.build(fake)
    command.reset(torch.arange(2))
    command.time_left[:] = 1e9
    previous = command.command.clone()
    for goal in ([.5, -.2, .07], [-.5, .2, .5]):
        command.target[:] = torch.tensor(goal)
        for _ in range(1100):
            # Match CommandManager order: velocity is freshly emitted first.
            velocity.command[:] = torch.tensor([.4, -.1, .3])
            command.compute(.02)
            assert ((command.command - previous).abs() <= torch.tensor(cfg.ramp_rates)*.02 + 1e-7).all()
            low = command.command[:, 2] <= .2
            assert (velocity.command[low] == 0).all()
            assert command.time_left.min() > 0
            previous = command.command.clone()
        expected = [0., 0., .07] if goal[2] < .2 else goal
        torch.testing.assert_close(command.command, torch.tensor(expected).repeat(2, 1))
    dt = torch.tensor([0., .02])
    command.target[:, 2] = .07
    before = command.command.clone()
    velocity.command[:] = 1.
    command.compute(dt)
    torch.testing.assert_close(command.command[0], before[0], atol=0, rtol=0)


def test_low_contact_and_posture_costs_are_gated_by_goal_not_actual_height():
    cfg = full_sit_stand(3)
    pose = torch.tensor([[0., 0., .07], [0., 0., .235], [0., 0., .335]])
    data = SimpleNamespace(projected_gravity_b=torch.tensor([[0., 0., -1.]]).repeat(3, 1),
        joint_pos=torch.tensor([[.75, 1.2, -2.7, 0., -.75, 1.2, -2.7, 0.]]).repeat(3, 1),
        default_joint_pos=torch.tensor(INITIAL_Q).repeat(3, 1))
    force = torch.zeros(3, 2, 3, 3)
    force[..., 2] = 10.
    fake = SimpleNamespace(cfg=cfg,
        scene={"robot": SimpleNamespace(data=data, joint_names=list(cfg.scene.entities['robot'].init_state.joint_pos)),
               "knees": SimpleNamespace(data=SimpleNamespace(force_history=force))},
        command_manager=SimpleNamespace(get_command=lambda _: pose, get_term=lambda _: SimpleNamespace(command=torch.zeros(3, 3))))
    # Persistent contact is charged on successive evaluations, not just onset.
    for _ in range(3):
        for kind in ("undesired_contacts", "joint_deviation_hip", "joint_deviation_shoulder"):
            original = mdp.reward(fake, kind)
            torch.testing.assert_close(height_scaled_penalty(fake, kind), original*torch.tensor([0., .5, 1.]))
        torch.testing.assert_close(mdp.reward(fake, "undesired_contacts"), torch.full((3,), 2.))
    # During standing pretraining the original costs apply at every goal.
    cfg.set_training_step(0)
    for kind in ("undesired_contacts", "joint_deviation_hip", "joint_deviation_shoulder"):
        torch.testing.assert_close(height_scaled_penalty(fake, kind), mdp.reward(fake, kind))


@pytest.mark.parametrize("changes", [
    {"height_motion_range": (.27, .2)}, {"height_motion_range": (.2, float("nan"))},
    {"height_target_bands": ((.01, .12), (.335, .5))},
    {"height_target_bands": ((.07, .4), (.335, .5))},
])
def test_invalid_sit_stand_command_config(changes):
    cfg = replace(full_sit_stand(1).commands["base_pose"], **changes)
    with pytest.raises(ValueError):
        cfg.build(command_env(1)[0])


def test_export_preserves_motion_gate_and_rejects_invalid_saved_gate():
    saved = playback_contract(full_sit_stand(1))
    layout = checkpoint.observation_layout(saved['observations']['policy'], {}, list(saved['scene']['robot']['init_state']['joint_pos']))
    runtime = checkpoint.simulation_config(saved, saved['scene']['robot']['init_state'], layout)
    assert runtime['pose_command']['height_motion_range'] == [.2, .27]
    assert runtime['policy']['obs_dim'] == 38
    for value in ([.27, .2], [.2, float('nan')], [True, .27]):
        saved['commands']['base_pose']['height_motion_range'] = value
        with pytest.raises(ValueError, match='height motion'):
            checkpoint.simulation_config(saved, saved['scene']['robot']['init_state'], layout)


def test_exact_curriculum_boundary_live_sampler_contact_and_saved_stage():
    from copy import deepcopy
    cfg = TitaSitStandEnvCfg(10000)
    fake, _ = command_env(10000)
    command = deepcopy(cfg.commands['base_pose']).build(fake)
    fake.command_manager.get_term = lambda _: command
    fake.cfg = cfg
    force = torch.zeros(10000, 1, 3, 3)
    force[::2, ..., 2] = 10.
    fake.scene = {name: SimpleNamespace(data=SimpleNamespace(force_history=force)) for name in ('base', 'knees')}
    command.reset(torch.arange(10000))
    assert command.target[:, 2].min() >= .25 and command.target[:, 2].max() <= .5
    assert cfg.curriculum_transition_step == 20000
    assert not cfg.set_training_step(19999, fake)
    expected = torch.arange(10000) % 2 == 0
    for sensor in ('base', 'knees'):
        assert torch.equal(curriculum_contact(fake, sensor), expected)
    assert cfg.set_training_step(20000, fake)
    assert cfg.curriculum_stage == 2
    assert command.cfg.height_range == cfg.commands['base_pose'].height_range == (.07, .5)
    assert command.cfg.height_motion_range == (.2, .27)
    command.reset(torch.arange(10000))
    assert (command.target[:, 2] < .12).any()
    assert not cfg.set_training_step(20001, fake)
    for sensor in ('base', 'knees'):
        assert not curriculum_contact(fake, sensor).any()
    saved = cloudpickle.loads(cloudpickle.dumps(cfg))
    assert saved.curriculum_stage == plain(saved)['curriculum_stage'] == 2
    assert saved.curriculum_transition_step == 20000
    assert not saved.set_training_step(25000)
    fake.cfg = saved
    # A playback rollout starts with zero simulation steps but retains stage 2.
    fake.common_step_counter = 0
    assert not curriculum_contact(fake, 'base').any()
