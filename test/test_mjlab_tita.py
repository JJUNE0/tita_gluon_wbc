"""TRAINING_SIM / VALIDATION_SIM: native CUDA physics and FlashSAC contracts.

Run with the dedicated mjlab interpreter; does not start Isaac or robot control.
"""

from pathlib import Path
import math
import sys
from types import SimpleNamespace

import pytest
import torch

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
from mj_lab.flash_sac import TitaFlashSACEnv, runtime
from mj_lab.checkpoint import playback_contract
from mj_lab.robots.tita import mdp
from mj_lab.robots.tita.flat_env_cfg import TitaFlatEnvCfg
from mj_lab.robots.tita.walk.walk_env_cfg import TitaWalkEnvCfg
from mj_lab.robots.tita.common.robot_cfg import JOINTS, OBS_JOINTS
from mjlab.envs import ManagerBasedRlEnv


@pytest.fixture(scope="module", params=["flat", "walk"])
def native_env(request):
    if not torch.cuda.is_available():
        pytest.skip("Native mjlab validation requires CUDA")
    cfg = (TitaWalkEnvCfg if request.param == "walk" else TitaFlatEnvCfg)(num_envs=4)
    cfg.seed = 42
    env = TitaFlashSACEnv(ManagerBasedRlEnv(cfg, device="cuda:0"))
    yield request.param, env
    env.close()


def test_dimensions_order_and_pd(native_env):
    task, env = native_env
    assert (env.actor_obs_dim, env.critic_obs_dim, env.action_dim) == ((40, 44, 8) if task == "walk" else (35, 39, 8))
    raw = env.env
    assert tuple(raw.scene["robot"].joint_names) == JOINTS
    assert raw.step_dt == .02 and raw.physics_dt == .005
    expected = [(60., 1.5, 60.), (92., 2.3, 60.), (0., .5, 12.)]
    for actuator, gains in zip(raw.scene["robot"].actuators, expected):
        assert (actuator.cfg.stiffness, actuator.cfg.damping, actuator.cfg.effort_limit) == gains
    env.reset()
    clean = mdp.observation(raw, "joint_pos", critic=True)
    ids = [raw.scene["robot"].joint_names.index(n) for n in OBS_JOINTS]
    expected_q = (raw.scene["robot"].data.joint_pos - raw.scene["robot"].data.default_joint_pos)[:, ids]
    expected_q[:, -2:] = 0
    torch.testing.assert_close(clean, expected_q)


def test_fixed_delays_randomized_gains_and_wheel_targets(native_env):
    task, env = native_env
    raw = env.env
    env.reset()
    before = [a._delay_buffer.current_lags.clone() for a in raw.scene["robot"].actuators]
    for a in raw.scene["robot"].actuators:
        ratio = a.damping / a.default_damping
        if a.cfg.stiffness == 92:
            assert (ratio >= .55 * .8 - 1e-6).all() and (ratio <= 1.2 + 1e-6).all()
        else:
            assert (ratio >= .8 - 1e-6).all() and (ratio <= 1.2 + 1e-6).all()
    env.step(torch.ones(4, 8, device=env.device))
    for lag, a in zip(before, raw.scene["robot"].actuators):
        torch.testing.assert_close(lag, a._delay_buffer.current_lags)
    for name in ("joint_vel_3", "joint_vel_7"):
        target = raw.action_manager.get_term(name)._processed_actions
        # During the reset settling window the hybrid walk is in standing mode.
        torch.testing.assert_close(target, torch.full_like(target, 100.0))


def test_timeout_terminal_snapshot_partial_reset(native_env):
    task, env = native_env
    raw = env.env
    obs = env.reset()
    raw.episode_length_buf[0] = raw.max_episode_length - 1
    # Give the ending row a distinct state so reset vs terminal is observable.
    robot = raw.scene["robot"]
    root = robot.data.root_link_pose_w[:1].clone()
    root[:, 2] += .2
    robot.write_root_link_pose_to_sim(root, env_ids=torch.tensor([0], device=env.device))
    next_obs, replay_next, reward, terminated, truncated, _ = env.step(torch.zeros(4, 8, device=env.device))
    assert truncated[0] and not terminated[0]
    assert raw.episode_length_buf[0] == 0 and (raw.episode_length_buf[1:] == 1).all()
    assert not torch.equal(next_obs[0], replay_next[0])
    torch.testing.assert_close(next_obs[1:], replay_next[1:], atol=0, rtol=0)
    preserved = replay_next.clone()
    env.step(torch.zeros(4, 8, device=env.device))
    torch.testing.assert_close(replay_next, preserved, atol=0, rtol=0)
    assert obs.shape == next_obs.shape and torch.isfinite(reward).all()


def test_contact_force_history_and_actual_base_termination(native_env):
    _, env = native_env
    raw = env.env
    env.reset()
    robot = raw.scene["robot"]
    pose = robot.data.root_link_pose_w.clone()
    # Invert the robot so the base is the only ground support. With upright
    # extended legs the solver can lift the base before it carries any force.
    pose[:, 2] = .08
    pose[:, 3:] = pose.new_tensor([0., 1., 0., 0.])
    robot.write_joint_state_to_sim(robot.data.default_joint_pos.clone(), torch.zeros_like(robot.data.joint_vel))
    robot.write_root_link_velocity_to_sim(torch.zeros(4, 6, device=env.device))
    robot.write_root_link_pose_to_sim(pose)
    raw.sim.forward()
    _, _, terminated, _, _ = raw.step(torch.zeros(4, 8, device=env.device))
    assert terminated.all()
    assert mdp.illegal_contact(raw, "base").all()
    assert raw.scene["base"].data.force_history.shape == (4, 1, raw.cfg.scene.sensors[-1].history_length, 3)
    env.reset()


def test_zero_velocity_gait_and_partial_reset(native_env):
    task, env = native_env
    if task != "walk":
        pytest.skip("Gait is specific to the walk task")
    raw = env.env
    env.reset()
    gait, velocity = raw.command_manager.get_term("gait"), mdp.velocity(raw)
    velocity.target.zero_()
    assert not gait.command[:, 0].any()
    raw.episode_length_buf[:] = 60
    raw.command_manager.compute(raw.step_dt)
    assert not gait.command[:, 0].any()
    torch.testing.assert_close(velocity.command, torch.zeros_like(velocity.command))
    velocity.target[1:, 0] = .3
    for _ in range(5):
        raw.command_manager.compute(raw.step_dt)
    assert gait.command[0, 0] == 0 and gait.command[1:, 0].all()
    old_phase = gait.phase.clone()
    for _ in range(3):
        raw.observation_manager.compute()
    torch.testing.assert_close(gait.phase, old_phase, atol=0, rtol=0)
    raw.reset(env_ids=torch.tensor([0], device=env.device))
    torch.testing.assert_close(gait.phase[1:], old_phase[1:], atol=0, rtol=0)
    assert gait.command[0, 0] == 0
    assert (gait.command[1:, 0] == 1).all()


def test_velocity_ramp_keeps_target_during_settle(native_env):
    task, env = native_env
    if task != "walk":
        pytest.skip("Settling ramp is specific to the walk task")
    raw = env.env
    env.reset()
    v = mdp.velocity(raw)
    v.target[:] = v.target.new_tensor([.5, -.5, 0.])
    raw.command_manager.compute(raw.step_dt)
    assert not v.command.any()
    torch.testing.assert_close(v.target[0], v.target.new_tensor([.5, -.5, 0.]))
    raw.episode_length_buf[:] = 51
    raw.command_manager.compute(raw.step_dt)
    torch.testing.assert_close(v.command[0], v.target.new_tensor([.006, -.006, 0.]))


def test_playback_contract_matches_native(native_env):
    task, env = native_env
    sys.path.insert(0, str(REPO / "sim2sim/sim2sim_ros2_jazzy"))
    from sim2sim_ros2_jazzy.checkpoint import observation_layout, action_layout, simulation_config
    saved = playback_contract(env.env.cfg)
    layout = observation_layout(saved["observations"]["policy"], {}, list(JOINTS))
    assert sum(o["size"] for o in layout) == env.actor_obs_dim
    for term in layout:
        if term["kind"] in ("joint_pos", "joint_vel"):
            assert term["joints"] == list(OBS_JOINTS)
    if task == "walk":
        for name in ("joint_vel_3", "joint_vel_7"):
            assert saved["actions"][name]["class_type"] == "GaitGatedWheelVelocityAction"
            assert saved["actions"][name]["scale"] == 20.
            assert saved["actions"][name]["wheel_enable"] == "gait_disabled"
        actions = action_layout(saved["actions"], {}, list(JOINTS), saved["scene"]["robot"]["init_state"])
        assert {term["joint"] for term in actions if term.get("gate") == "gait_disabled"} == {JOINTS[3], JOINTS[7]}
    else:
        actions = action_layout(saved["actions"], {}, list(JOINTS), saved["scene"]["robot"]["init_state"])
        assert [a["joint"] for a in actions] == list(JOINTS)
        assert [actions[i]["scale"] for i in (3, 7)] == [20., 20.]
    cfg = simulation_config(saved, saved["scene"]["robot"]["init_state"], layout)
    assert cfg["model"]["wheel_collision"] == "sphere" and cfg["model"]["flat_ground"]
    if task == "walk":
        assert cfg["gait_command"]["clock"] == "episode_steps"
        position = next(term for term in layout if term["kind"] == "wheel_position_error")
        assert position["scale"] == 5.0 and position["params"]["gait_name"] == "gait"
        assert position["params"]["velocity_thresholds"] == [.1, .15]
        assert position["params"]["moving_anchor"] is True


def test_gait_reference_double_support_and_4cm():
    phase = torch.tensor([0., .1, .6, .8])
    stance, height = mdp.gait_reference(phase, torch.ones(4))
    assert stance.any(dim=1).all()
    torch.testing.assert_close(height[-1, 0], torch.tensor(.04))
    torch.testing.assert_close(height[stance], torch.zeros_like(height[stance]))


def test_roll_pitch_weights_and_reward_kernel():
    cfg = TitaWalkEnvCfg(1)
    assert cfg.rewards["joint_deviation_hip"].weight == -1.0
    assert cfg.rewards["joint_deviation_shoulder"].weight == -.5
    for name in ("joint_deviation_hip", "joint_deviation_shoulder"):
        term = cfg.rewards[name]
        assert term.weight * term.params["moving_scale"] == pytest.approx(-.1)
    assert cfg.rewards["ang_vel_roll_l2"].weight == -.02
    assert cfg.rewards["ang_vel_pitch_l2"].weight == -.1
    assert "ang_vel_xy_l2" not in cfg.rewards
    fake_data = SimpleNamespace(root_link_ang_vel_b=torch.tensor([[2., 3., 4.]]), projected_gravity_b=torch.tensor([[0., 0., -1.]]))
    fake = SimpleNamespace(scene={"robot": SimpleNamespace(data=fake_data)}, command_manager=SimpleNamespace(get_term=lambda _: None))
    torch.testing.assert_close(mdp.reward(fake, "ang_vel_axis_l2", axis=0), torch.tensor([4.]))
    torch.testing.assert_close(mdp.reward(fake, "ang_vel_axis_l2", axis=1), torch.tensor([9.]))


def test_knee_history_threshold_in_native_manager(native_env):
    task, env = native_env
    if task != "walk":
        pytest.skip("Knee termination is specific to the walk task")
    raw = env.env
    env.reset()
    history = raw.scene["knees"].data.force_history
    history.zero_()
    history[0, 0, 2, 0] = 1.01
    history[1, 1, 1, 0] = .99
    torch.testing.assert_close(mdp.illegal_contact(raw, "knees"), torch.tensor([True, False, False, False], device=env.device))
    result = raw.termination_manager.compute()
    assert result[0] and raw.termination_manager.terminated[0]
    assert not raw.termination_manager.time_outs[0]
    env.reset()


def test_reward_parity_against_isaac_source():
    """Execute the existing kernels without importing or launching Isaac Sim."""
    import ast
    source = REPO / "isaac_lab/ddt_lab/ddt_lab/tasks/manager_based/locomotion/mdp/rewards.py"
    names = {"track_lin_vel_xy_exp", "track_ang_vel_z_exp", "lin_vel_z_l2", "ang_vel_xy_l2", "flat_orientation_l2", "base_height_l2", "action_rate_l2"}
    tree = ast.parse(source.read_text())
    functions = [node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name in names]
    namespace = {"torch": torch, "SceneEntityCfg": lambda name: SimpleNamespace(name=name)}
    module = ast.Module(body=[ast.ImportFrom(module="__future__", names=[ast.alias(name="annotations")], level=0), *functions], type_ignores=[])
    exec(compile(ast.fix_missing_locations(module), str(source), "exec"), namespace)
    g = torch.Generator().manual_seed(7)
    rand = lambda *shape: torch.randn(*shape, generator=g)
    d = SimpleNamespace(root_link_lin_vel_b=rand(10, 3), root_link_ang_vel_b=rand(10, 3),
        projected_gravity_b=rand(10, 3), root_link_pos_w=rand(10, 3))
    d.root_lin_vel_b, d.root_ang_vel_b, d.root_pos_w = d.root_link_lin_vel_b, d.root_link_ang_vel_b, d.root_link_pos_w
    cmd = rand(10, 3)
    manager = SimpleNamespace(get_command=lambda _: cmd, get_term=lambda _: SimpleNamespace(command=cmd))
    class Scene(dict):
        env_origins = torch.zeros(10, 3)
    fake = SimpleNamespace(scene=Scene(robot=SimpleNamespace(data=d)), command_manager=manager,
                           action_manager=SimpleNamespace(action=rand(10, 8), prev_action=rand(10, 8)))
    for name in names:
        kwargs = {"std": .5, "command_name": "base_velocity"} if name.startswith("track_") else {"target_height": .335} if name == "base_height_l2" else {}
        expected = namespace[name](fake, **kwargs)
        kwargs.pop("command_name", None)
        torch.testing.assert_close(mdp.reward(fake, name, **kwargs), expected)


def test_velocity_metrics_match_isaac_scaling_without_reset_overcount(native_env):
    _, env = native_env
    raw = env.env
    env.reset()
    velocity = mdp.velocity(raw)
    assert all(not value.any() for value in velocity.metrics.values())
    d = raw.scene["robot"].data
    divisor = velocity.cfg.resampling_time_range[1] / raw.step_dt
    expected_xy = (velocity.command[:, :2] - d.root_link_lin_vel_b[:, :2]).norm(dim=1) / divisor
    expected_yaw = (velocity.command[:, 2] - d.root_link_ang_vel_b[:, 2]).abs() / divisor
    velocity.compute(raw.step_dt)
    torch.testing.assert_close(velocity.metrics["error_vel_xy"], expected_xy)
    torch.testing.assert_close(velocity.metrics["error_vel_yaw"], expected_yaw)
    snapshot = {key: value.clone() for key, value in velocity.metrics.items()}
    velocity.compute(0.0, env_ids=torch.tensor([0], device=env.device))
    for key, previous in snapshot.items():
        torch.testing.assert_close(velocity.metrics[key], previous, atol=0, rtol=0)


def test_hybrid_mixed_modes_gate_targets_and_keep_raw_actions(native_env):
    task, env = native_env
    if task != "walk":
        pytest.skip("Hybrid action gate is specific to walk")
    raw = env.env
    env.reset()
    gait = raw.command_manager.get_term("gait")
    gait.command[:, 0] = torch.tensor([0., 1., 0., 1.], device=env.device)
    actions = torch.full((4, 8), 2., device=env.device)
    raw.action_manager.process_action(actions)
    for name in ("joint_vel_3", "joint_vel_7"):
        term = raw.action_manager.get_term(name)
        torch.testing.assert_close(term._processed_actions[:, 0], actions.new_tensor([40., 0., 40., 0.]))
        torch.testing.assert_close(term.raw_action, torch.full((4, 1), 2., device=env.device))
    torch.testing.assert_close(raw.action_manager.action, actions)
    gait.command[:, 0] = 1 - gait.command[:, 0]
    raw.action_manager.process_action(-actions)
    for name in ("joint_vel_3", "joint_vel_7"):
        torch.testing.assert_close(raw.action_manager.get_term(name)._processed_actions[:, 0], actions.new_tensor([0., -40., 0., -40.]))
    env.reset()


def test_hybrid_deviation_weights_and_gait_rewards_per_environment(native_env):
    task, env = native_env
    if task != "walk":
        pytest.skip("Hybrid rewards are specific to walk")
    raw = env.env
    env.reset()
    gait = raw.command_manager.get_term("gait")
    gait.command[:, 0] = torch.tensor([0., 1., 0., 1.], device=env.device)
    robot = raw.scene["robot"]
    q = robot.data.default_joint_pos.clone()
    q[:, [0, 1, 4, 5]] += .1
    robot.write_joint_state_to_sim(q, torch.zeros_like(q))
    raw.sim.forward()
    for name, standing_weight in (("joint_deviation_hip", -1.), ("joint_deviation_shoulder", -.5)):
        term = raw.cfg.rewards[name]
        contribution = term.weight * term.func(raw, **term.params)
        torch.testing.assert_close(contribution, q.new_tensor([.2 * standing_weight, -.02, .2 * standing_weight, -.02]))
    for function in (mdp.contact_schedule, mdp.wheel_clearance):
        masked = function(raw, only_when_enabled=True)
        original = function(raw)
        torch.testing.assert_close(masked[[0, 2]], torch.zeros(2, device=env.device))
        torch.testing.assert_close(masked[[1, 3]], original[[1, 3]])
    env.reset()


def test_hybrid_sim2sim_matches_native_gate_and_clock(native_env):
    task, env = native_env
    if task != "walk":
        pytest.skip("Hybrid clock/action parity is specific to walk")
    import ast
    import numpy as np
    sys.path.insert(0, str(REPO / "sim2sim/sim2sim_ros2_jazzy"))
    from sim2sim_ros2_jazzy.adapter import ActionAdapter, ObservationBuilder
    from sim2sim_ros2_jazzy.checkpoint import action_layout, observation_layout, simulation_config
    raw = env.env
    env.reset()
    saved = playback_contract(raw.cfg)
    layout = observation_layout(saved["observations"]["policy"], {}, list(JOINTS))
    cfg = simulation_config(saved, saved["scene"]["robot"]["init_state"], layout)
    cfg["policy_interface"] = {"observations": layout, "actions": action_layout(saved["actions"], {}, list(JOINTS), saved["scene"]["robot"]["init_state"])}
    builder, adapter = ObservationBuilder(cfg), ActionAdapter(cfg)
    # Execute the actual post-physics command/gait block without importing ROS.
    source = REPO / "sim2sim/sim2sim_ros2_jazzy/sim2sim_ros2_jazzy/sim2sim_node.py"
    cls = next(n for n in ast.parse(source.read_text()).body if isinstance(n, ast.ClassDef) and n.name == "Sim2SimNode")
    method = next(n for n in cls.body if isinstance(n, ast.FunctionDef) and n.name == "_step")
    block = next(n for n in ast.walk(method) if isinstance(n, ast.If)
                 and ast.unparse(n.test) == "self.walking"
                 and any(isinstance(child, ast.Call) and isinstance(child.func, ast.Attribute)
                         and child.func.attr == "advance_gait" for child in ast.walk(n)))
    function = ast.parse("def update(self):\n    pass").body[0]
    function.body = block.body
    namespace = {"np": np}
    exec(compile(ast.fix_missing_locations(ast.Module(body=[function], type_ignores=[])), str(source), "exec"), namespace)
    runtime = SimpleNamespace(cfg=cfg, command_ramp=cfg["sim_command_ramp"], command=np.zeros(3, dtype=np.float32), command_target=np.zeros(3, dtype=np.float32), obs_builder=builder, env=SimpleNamespace(control_dt=.02, viewer=None))
    v, gait = mdp.velocity(raw), raw.command_manager.get_term("gait")
    v.time_left[:] = 1e9
    gait.phase.zero_()
    action = np.linspace(-6, 6, 8, dtype=np.float32)
    for target in ([.3, 0., 0.], [0., 0., 0.], [0., -.3, 0.], [0., 0., 0.]):
        runtime.command_target[:] = target
        v.target[:] = torch.tensor(target, device=env.device)
        for _ in range(100):
            raw.action_manager.process_action(torch.tensor(action, device=env.device).repeat(4, 1))
            native_targets = torch.cat([raw.action_manager.get_term(name)._processed_actions for name in raw.cfg.actions], dim=1)[0].cpu().numpy()
            np.testing.assert_allclose(adapter.targets(action, gait_enabled=builder.gait_enabled), native_targets, atol=1e-5)
            raw.episode_length_buf += 1
            raw.command_manager.compute(raw.step_dt)
            namespace["update"](runtime)
            np.testing.assert_allclose(runtime.command, v.command[0].cpu().numpy(), atol=1e-7)
            np.testing.assert_allclose(builder.gait_command(), gait.command[0].cpu().numpy(), atol=1e-6)
    env.reset()


def test_standing_wheel_odometry_matches_sim2sim_and_reanchors(native_env):
    task, env = native_env
    if task != "walk":
        pytest.skip("Gait-gated wheel odometry is specific to hybrid walk")
    import numpy as np
    sys.path.insert(0, str(REPO / "sim2sim/sim2sim_ros2_jazzy"))
    from sim2sim_ros2_jazzy.adapter import ObservationBuilder, ObsState
    from sim2sim_ros2_jazzy.checkpoint import observation_layout, simulation_config
    raw = env.env
    env.reset()
    v, gait = mdp.velocity(raw), raw.command_manager.get_term("gait")
    v.target.zero_()
    v.time_left[:] = 1e9
    v.radius_scale.fill_(1.)
    raw.episode_length_buf[:] = 60
    v.compute(raw.step_dt)
    saved = playback_contract(raw.cfg)
    layout = observation_layout(saved["observations"]["policy"], {}, list(JOINTS))
    cfg = simulation_config(saved, saved["scene"]["robot"]["init_state"], layout)
    cfg["policy_interface"] = {"observations": layout}
    builders = [ObservationBuilder(cfg) for _ in range(4)]
    position_index = sum(term["size"] for term in layout[:next(i for i, term in enumerate(layout) if term["kind"] == "wheel_position_error")])
    robot = raw.scene["robot"]

    def sample():
        d = robot.data
        expected = mdp.observation(raw, "wheel_position_error")[:, 0].cpu().numpy()
        for row, builder in enumerate(builders):
            builder.gait_enabled = bool(gait.command[row, 0])
            state = ObsState(d.joint_pos[row].cpu().numpy(), d.joint_vel[row].cpu().numpy(),
                             d.root_link_quat_w[row].cpu().numpy(), d.root_link_ang_vel_b[row].cpu().numpy(),
                             v.command[row].cpu().numpy(), np.zeros(8), d.root_link_lin_vel_b[row].cpu().numpy())
            observed = builder.build(state)
            assert observed.shape == (40,)
            np.testing.assert_allclose(observed[position_index] / 5., expected[row], atol=1e-6)
        # Actor/critic observation reads must not advance encoder integration.
        torch.testing.assert_close(mdp.observation(raw, "wheel_position_error")[:, 0], torch.as_tensor(expected, device=env.device))
        return expected

    sample()
    for angle, flags in ((.2, [0, 0, 0, 0]), (.4, [0, 1, 0, 1]),
                         (1.6, [0, 1, 0, 1]), (2., [0, 0, 0, 0]),
                         (2.2, [0, 0, 0, 0]), (4.2, [0, 0, 0, 0])):
        q = robot.data.default_joint_pos.clone()
        q[:, [3, 7]] = angle
        robot.write_joint_state_to_sim(q, torch.zeros_like(q))
        raw.sim.forward()
        v.compute(raw.step_dt)  # Uses the mode active during the last interval.
        gait.command[:, 0] = torch.tensor(flags, device=env.device)
        values = sample()
        if angle == .2:
            np.testing.assert_allclose(values, .2 * .0925, atol=1e-6)
        elif angle in (.4, 1.6, 2.):
            np.testing.assert_allclose(values[[1, 3]], 0., atol=1e-6)
        elif angle == 2.2:
            np.testing.assert_allclose(values[[1, 3]], .2 * .0925, atol=1e-6)
        elif angle == 4.2:
            np.testing.assert_allclose(values[[0, 2]], .3, atol=1e-6)
    preserved = v.wheel_error[1:].clone()
    raw.reset(env_ids=torch.tensor([0], device=env.device))
    torch.testing.assert_close(v.wheel_error[1:], preserved)
    assert mdp.observation(raw, "wheel_position_error")[0, 0] == 0
    env.reset()


def test_stop_latch_coasting_push_moving_anchor_and_reward(native_env):
    task, env = native_env
    if task != "walk":
        pytest.skip("Settled stop latch is enabled for new hybrid walk")
    import numpy as np
    sys.path.insert(0, str(REPO / "sim2sim/sim2sim_ros2_jazzy"))
    from sim2sim_ros2_jazzy.adapter import ObservationBuilder, ObsState
    from sim2sim_ros2_jazzy.checkpoint import observation_layout, simulation_config
    raw = env.env
    env.reset()
    v, gait = mdp.velocity(raw), raw.command_manager.get_term("gait")
    v.target.zero_()
    v.time_left[:] = 1e9
    v.radius_scale.fill_(1.)
    gait.command[:, 0] = 0
    raw.episode_length_buf[:] = 60
    saved = playback_contract(raw.cfg)
    layout = observation_layout(saved["observations"]["policy"], {}, list(JOINTS))
    cfg = simulation_config(saved, saved["scene"]["robot"]["init_state"], layout)
    cfg["policy_interface"] = {"observations": layout}
    builder = ObservationBuilder(cfg)
    robot = raw.scene["robot"]
    origin = robot.data.root_link_pos_w.clone()

    def sample(distance, vx=0., vy=0., wz=0.):
        q = robot.data.default_joint_pos.clone()
        q[:, [3, 7]] = distance / .0925
        pose = torch.cat((origin.clone(), q.new_tensor([1., 0., 0., 0.]).repeat(4, 1)), dim=1)
        pose[:, 0] += distance
        robot.write_joint_state_to_sim(q, torch.zeros_like(q))
        robot.write_root_link_pose_to_sim(pose)
        speed = torch.zeros(4, 6, device=env.device)
        speed[:, 0], speed[:, 1], speed[:, 5] = vx, vy, wz
        robot.write_root_link_velocity_to_sim(speed)
        raw.sim.forward()
        v.compute(raw.step_dt)
        d = robot.data
        state = ObsState(d.joint_pos[0].cpu().numpy(), d.joint_vel[0].cpu().numpy(),
                         d.root_link_quat_w[0].cpu().numpy(), d.root_link_ang_vel_b[0].cpu().numpy(),
                         v.command[0].cpu().numpy(), np.zeros(8), d.root_link_lin_vel_b[0].cpu().numpy())
        error = mdp.observation(raw, "wheel_position_error")[:, 0]
        np.testing.assert_allclose(builder.wheel_position_error(state), error[:1].cpu().numpy(), atol=1e-6)
        contribution = mdp.reward(raw, "zero_command_position_drift")
        return float(error[0]), float(contribution[0])

    # Command is already zero, but encoder and true pose continue moving.
    for distance, speed in ((0., .5), (.05, .3), (.10, .15)):
        error, reward = sample(distance, vx=speed)
        assert error == 0 and reward == 0
        torch.testing.assert_close(v.position_anchor[:, 0], origin[:, 0] + distance)
    # Linear speed alone is insufficient: lateral motion or yaw also prevents hold.
    for distance, vy, wz in ((.12, .11, 0.), (.14, 0., .16)):
        assert sample(distance, vy=vy, wz=wz) == (0., 0.)
    assert sample(.16, vx=.05) == (0., 1.)  # First settled sample anchors here.
    error, reward = sample(.18)
    assert error == pytest.approx(.02, abs=1e-6)
    assert reward == pytest.approx(math.exp(-8 * .02), abs=1e-5)
    # A fast shove releases the reference; the displaced settled point is new zero.
    assert sample(.28, vx=.4) == (0., 0.)
    assert sample(.38, vx=.05) == (0., 1.)
    # Slow displacement keeps the hold engaged and exercises anti-windup.
    for distance in np.arange(.48, 1.09, .1):
        sample(float(distance), vx=.02)
    assert float(v.wheel_error[0]) == pytest.approx(.3, abs=1e-6)
    assert float((robot.data.root_link_pos_w - v.position_anchor)[0, :2].norm()) == pytest.approx(.3, abs=1e-6)
    error, reward = sample(1.06)
    assert error == pytest.approx(.28, abs=1e-6)  # No hidden integral beyond the cap.
    assert reward == pytest.approx(math.exp(-8 * .28), abs=1e-5)
    before = v.wheel_stationary[1:].clone()
    raw.reset(env_ids=torch.tensor([0], device=env.device))
    assert not v.wheel_stationary[0] and not v.position_latched[0]
    torch.testing.assert_close(v.wheel_stationary[1:], before)
    env.reset()
