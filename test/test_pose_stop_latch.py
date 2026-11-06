"""TRAINING_SIM / VALIDATION_SIM: deceleration latch in pose/sit-stand tasks."""

import math
from pathlib import Path
import sys

import numpy as np
import pytest
import torch
from mjlab.envs import ManagerBasedRlEnv

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT/'sim2sim/sim2sim_ros2_jazzy')]
from mj_lab.checkpoint import playback_contract
from mj_lab.flash_sac import TitaFlashSACEnv
from mj_lab.robots.tita import mdp
from mj_lab.robots.tita.flat_env_roll_pitch_height_cfg import TitaFlatRollPitchHeightEnvCfg
from mj_lab.robots.tita.sit_stand_env_cfg import TitaSitStandEnvCfg
from sim2sim_ros2_jazzy.adapter import ObservationBuilder, ObsState
from sim2sim_ros2_jazzy.checkpoint import observation_layout, simulation_config


@pytest.mark.parametrize('factory', [TitaFlatRollPitchHeightEnvCfg, TitaSitStandEnvCfg])
def test_body_velocity_latch_and_reward_follow_coast_then_hold(factory):
    if not torch.cuda.is_available():
        pytest.skip('Native mjlab physics requires CUDA')
    cfg = factory(4, play=True)
    mapping = {name:getattr(cfg, name) for name in ('action_gain_negative', 'action_gain_positive') if hasattr(cfg, name)}
    env = TitaFlashSACEnv(ManagerBasedRlEnv(cfg, device='cuda:0'), **mapping)
    try:
        raw, robot = env.env, env.env.scene['robot']
        env.reset()
        v = mdp.velocity(raw)
        v.target.zero_()
        v.time_left[:] = 1e9
        v.radius_scale.fill_(1.)
        saved = playback_contract(cfg)
        names = list(robot.joint_names)
        layout = observation_layout(saved['observations']['policy'], {}, names)
        playback = simulation_config(saved, saved['scene']['robot']['init_state'], layout)
        playback['policy_interface'] = {'observations':layout}
        builder = ObservationBuilder(playback)
        origin = robot.data.root_link_pos_w.clone()

        def sample(distance, vx=0., vy=0., wz=0.):
            q = robot.data.default_joint_pos.clone()
            q[:, [names.index('joint_left_leg_4'), names.index('joint_right_leg_4')]] = distance/.0925
            pose = torch.cat((origin.clone(), q.new_tensor([1., 0., 0., 0.]).repeat(4, 1)), dim=1)
            pose[:, 0] += distance
            robot.write_joint_state_to_sim(q, torch.zeros_like(q))
            robot.write_root_link_pose_to_sim(pose)
            speed = torch.zeros(4, 6, device=env.device)
            speed[:, 0], speed[:, 1], speed[:, 5] = vx, vy, wz
            robot.write_root_link_velocity_to_sim(speed)
            raw.sim.forward()
            raw.command_manager.compute(raw.step_dt)
            d = robot.data
            state = ObsState(d.joint_pos[0].cpu().numpy(), d.joint_vel[0].cpu().numpy(),
                d.root_link_quat_w[0].cpu().numpy(), d.root_link_ang_vel_b[0].cpu().numpy(),
                v.command[0].cpu().numpy(), np.zeros(8), d.root_link_lin_vel_b[0].cpu().numpy())
            error = mdp.observation(raw, 'wheel_position_error')[:, 0]
            np.testing.assert_allclose(builder.wheel_position_error(state), error[:1].cpu().numpy(), atol=1e-6)
            reward = mdp.reward(raw, 'zero_command_position_drift')
            return float(error[0]), float(reward[0])

        for distance, speed in ((0., .5), (.05, .3), (.10, .15)):
            assert sample(distance, vx=speed) == (0., 0.)
            torch.testing.assert_close(v.position_anchor[:, 0], origin[:, 0]+distance)
        assert sample(.12, vy=.11) == (0., 0.)
        assert sample(.14, wz=.16) == (0., 0.)
        assert sample(.16, vx=.05) == (0., 1.)
        error, reward = sample(.18)
        assert error == pytest.approx(.02, abs=1e-6)
        assert reward == pytest.approx(math.exp(-8*.02), abs=1e-5)
        assert sample(.28, vx=.4) == (0., 0.)
        assert sample(.38, vx=.05) == (0., 1.)
        for distance in np.arange(.48, 1.09, .1):
            sample(float(distance), vx=.02)
        error, reward = sample(1.06)
        assert error == pytest.approx(.28, abs=1e-6)
        assert reward == pytest.approx(math.exp(-8*.28), abs=1e-5)
        before = v.wheel_error[1:].clone()
        raw.reset(env_ids=torch.tensor([0], device=env.device))
        assert not v.wheel_stationary[0] and not v.position_latched[0]
        torch.testing.assert_close(v.wheel_error[1:], before, atol=0, rtol=0)
        if isinstance(cfg, TitaSitStandEnvCfg):
            cfg.set_training_step(20000, raw)
            env.reset()
            v.radius_scale.fill_(1.)
            v.target[:, 0] = .5
            v.time_left[:] = 1e9
            pose = raw.command_manager.get_term('base_pose')
            pose.command[:] = pose.target[:] = pose.command.new_tensor([0., 0., .1])
            pose.time_left[:] = 1e9
            # The velocity sampler requests movement, but low height emits zero.
            # Both runtimes must latch from that final, observed zero command.
            assert sample(0., vx=.4) == (0., 0.)
            assert (v.command == 0).all()
            assert sample(.10, vx=.05) == (0., 1.)
            error, _ = sample(.12)
            assert error == pytest.approx(.02, abs=1e-6)
    finally:
        env.close()
