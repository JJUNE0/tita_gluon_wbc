"""Bounded desktop tests for the sequential-inspection Go/No-Go contract."""

from __future__ import annotations

from pathlib import Path
import importlib.util
import json
import sys

import numpy as np
import pytest
import torch


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "lab" / "ddt_lab"))
sys.path.insert(0, str(REPO_ROOT / "lab"))

MODULE_PATH = (
    REPO_ROOT
    / "lab"
    / "ddt_lab"
    / "ddt_lab"
    / "tasks"
    / "moo_based"
    / "locomanipulation"
    / "velocity"
    / "tita_gluon"
    / "sequential_inspection.py"
)
SPEC = importlib.util.spec_from_file_location("tita_gluon_sequential_inspection", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
inspection = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = inspection
SPEC.loader.exec_module(inspection)

ArmOption = inspection.ArmOption
CoordinatorObservation = inspection.CoordinatorObservation
ExecutorEvent = inspection.ExecutorEvent
ExecutorState = inspection.ExecutorState
ExecutorStepInput = inspection.ExecutorStepInput
SequentialInspectionExecutor = inspection.SequentialInspectionExecutor
StopAndGoController = inspection.StopAndGoController
TunedConcurrentScheduler = inspection.TunedConcurrentScheduler
build_option_mask = inspection.build_option_mask
build_high_level_policy_observation = inspection.build_high_level_policy_observation
build_phase_conditioned_trigger_contract = inspection.build_phase_conditioned_trigger_contract
compute_go_no_go_reward = inspection.compute_go_no_go_reward
decode_phase_conditioned_action = inspection.decode_phase_conditioned_action
local_region_contains = inspection.local_region_contains
sample_target_layout = inspection.sample_target_layout
from scripts.co_rl.core.modules import HybridActorCritic  # noqa: E402
from scripts.co_rl.core.algorithms.ppo import PPO  # noqa: E402


def test_option_mask_separates_policy_option_from_executor_state() -> None:
    states = torch.tensor(
        [
            int(ExecutorState.IDLE),
            int(ExecutorState.IDLE),
            int(ExecutorState.GRAPH_EXECUTION),
            int(ExecutorState.DWELL),
            int(ExecutorState.EMERGENCY_HOLD),
        ]
    )
    mask = build_option_mask(
        states,
        current_target_index=torch.tensor([0, 1, 1, 1, 1]),
        prepared_target_index=torch.tensor([-1, 1, 0, 1, 1]),
        target_count=4,
        local_region_valid=torch.tensor([False, True, True, True, True]),
        validated_stow_path=torch.tensor([True, True, True, True, True]),
    )
    assert mask[0].tolist() == [True, True, True, False]
    assert mask[1].tolist() == [True, True, False, True]
    assert torch.all(mask[2:, ArmOption.HOLD])
    assert not torch.any(mask[2:, 1:])


def test_executor_persists_option_and_requires_full_dwell() -> None:
    executor = SequentialInspectionExecutor(target_count=2, dwell_time_s=0.3)
    assert executor.begin_bootstrap() == ExecutorEvent.OPTION_ACCEPTED
    assert executor.state == ExecutorState.GRAPH_EXECUTION
    assert (
        executor.request(
            ArmOption.EXECUTE_CURRENT,
            local_region_valid=True,
            validated_stow_path=True,
        )
        == ExecutorEvent.OPTION_REJECTED
    )
    executor.step(0.1, ExecutorStepInput(graph_finished=True))
    assert executor.state == ExecutorState.IDLE
    assert executor.prepared_target_index == 0

    assert (
        executor.request(
            ArmOption.EXECUTE_CURRENT,
            local_region_valid=True,
            validated_stow_path=True,
        )
        == ExecutorEvent.OPTION_ACCEPTED
    )
    executor.step(0.1, ExecutorStepInput(pose_within_tolerance=True))
    assert executor.state == ExecutorState.DWELL
    assert executor.step(0.1, ExecutorStepInput(pose_within_tolerance=True)) == ExecutorEvent.NONE
    assert executor.step(0.1, ExecutorStepInput(pose_within_tolerance=False)) == ExecutorEvent.NONE
    assert executor.state == ExecutorState.LOCAL_TARGET_SERVO
    executor.step(0.1, ExecutorStepInput(pose_within_tolerance=True))
    assert executor.step(0.1, ExecutorStepInput(pose_within_tolerance=True)) == ExecutorEvent.NONE
    assert executor.step(0.2, ExecutorStepInput(pose_within_tolerance=True)) == ExecutorEvent.TARGET_COMPLETED
    assert executor.current_target_index == 1
    assert executor.prepared_target_index == 0


def test_executor_holds_before_validated_recovery() -> None:
    executor = SequentialInspectionExecutor()
    executor.begin_bootstrap()
    assert executor.step(0.02, ExecutorStepInput(cbf_infeasible=True)) == ExecutorEvent.SAFETY_ABORT
    assert executor.state == ExecutorState.EMERGENCY_HOLD
    assert executor.begin_validated_recovery(False) == ExecutorEvent.OPTION_REJECTED
    assert executor.state == ExecutorState.EMERGENCY_HOLD
    assert executor.begin_validated_recovery(True) == ExecutorEvent.RECOVERY_STARTED
    assert executor.state == ExecutorState.RECOVERY
    assert executor.step(0.02, ExecutorStepInput(recovery_finished=True)) == ExecutorEvent.RECOVERY_COMPLETED
    assert executor.at_stow


def test_local_region_and_target_randomization_are_bounded() -> None:
    target = torch.tensor([[0.03, -0.02, 0.01], [0.031, 0.0, 0.0]])
    hub = torch.zeros_like(target)
    assert local_region_contains(target, hub, (0.03, 0.03, 0.03)).tolist() == [True, False]
    first = sample_target_layout(17)
    second = sample_target_layout(17)
    assert first == second
    assert [target.label for target in first] == [
        "LEFT_HIGH",
        "RIGHT_LOW",
        "LEFT_LOW",
        "RIGHT_HIGH",
    ]


def test_classical_baselines_have_distinct_overlap_contracts() -> None:
    moving = CoordinatorObservation(
        target_index=1,
        target_count=4,
        longitudinal_distance_m=0.7,
        yaw_error_rad=0.1,
        local_region_valid=False,
        prepared_for_current=False,
        at_stow=False,
        executor_state=ExecutorState.GRAPH_EXECUTION,
    )
    stop_go = StopAndGoController().command(moving)
    concurrent = TunedConcurrentScheduler(
        start_distance_m=0.9, arm_motion_speed_scale=0.4
    ).command(moving)
    assert stop_go.vx_cmd_m_s == 0.0
    assert stop_go.yaw_rate_cmd_rad_s == 0.0
    assert concurrent.vx_cmd_m_s == 0.2
    assert concurrent.arm_option == ArmOption.HOLD


def test_concurrent_scheduler_brakes_smoothly_during_local_servo() -> None:
    controller = TunedConcurrentScheduler(
        start_distance_m=0.9, arm_motion_speed_scale=0.4
    )
    near_target = CoordinatorObservation(
        target_index=0,
        target_count=4,
        longitudinal_distance_m=0.05,
        yaw_error_rad=0.0,
        local_region_valid=True,
        prepared_for_current=True,
        at_stow=False,
        executor_state=ExecutorState.LOCAL_TARGET_SERVO,
    )
    command = controller.command(near_target)
    assert command.vx_cmd_m_s == pytest.approx(0.03)
    assert command.arm_option == ArmOption.HOLD


def test_stop_and_go_waits_for_measured_base_stop_before_execute() -> None:
    controller = StopAndGoController()
    moving = CoordinatorObservation(
        target_index=0,
        target_count=4,
        longitudinal_distance_m=0.05,
        yaw_error_rad=0.0,
        local_region_valid=True,
        prepared_for_current=True,
        at_stow=False,
        executor_state=ExecutorState.IDLE,
        base_speed_m_s=0.08,
        base_yaw_rate_rad_s=0.01,
    )
    braking = controller.command(moving)
    assert braking.vx_cmd_m_s == 0.0
    assert braking.arm_option == ArmOption.HOLD
    stopped = CoordinatorObservation(**{**moving.__dict__, "base_speed_m_s": 0.01})
    assert controller.command(stopped).arm_option == ArmOption.EXECUTE_CURRENT


def test_stop_and_go_aligns_prepared_hub_to_measured_world_target() -> None:
    controller = StopAndGoController()
    misaligned = CoordinatorObservation(
        target_index=1,
        target_count=4,
        longitudinal_distance_m=0.0,
        yaw_error_rad=0.0,
        local_region_valid=False,
        prepared_for_current=True,
        at_stow=False,
        executor_state=ExecutorState.IDLE,
        target_minus_hub_x_m=0.4,
    )
    assert controller.command(misaligned).vx_cmd_m_s > 0.0
    behind = CoordinatorObservation(
        **{**misaligned.__dict__, "target_minus_hub_x_m": -0.4}
    )
    assert controller.command(behind).vx_cmd_m_s < 0.0
    lateral = CoordinatorObservation(
        **{
            **misaligned.__dict__,
            "target_minus_hub_x_m": 0.0,
            "target_minus_hub_y_m": 0.4,
        }
    )
    lateral_command = controller.command(lateral)
    assert lateral_command.vx_cmd_m_s > 0.0
    assert lateral_command.yaw_rate_cmd_rad_s > 0.0


def test_hybrid_actor_respects_mask_and_has_finite_joint_log_probability() -> None:
    torch.manual_seed(5)
    actor = HybridActorCritic(
        num_actor_obs=12,
        num_critic_obs=12,
        num_actions=3,
        actor_hidden_dims=[32, 16],
        critic_hidden_dims=[32, 16],
        activation="elu",
        init_noise_std=0.5,
        continuous_action_dim=2,
        discrete_action_dim=2,
        action_mask_obs_start=-4,
    )
    observations = torch.randn(128, 12)
    observations[:, -4:] = torch.tensor([1.0, 0.0, 0.0, 0.0])
    actions = actor.act(observations)
    assert actions.shape == (128, 3)
    assert set(actions[:, 2].long().tolist()) == {0}
    assert torch.all(torch.isfinite(actor.get_actions_log_prob(actions)))
    assert torch.all(torch.isfinite(actor.entropy))
    assert actor.action_mean.shape == actions.shape
    assert actor.action_std.shape == actions.shape
    greedy = actor.act_inference(observations)
    assert set(greedy[:, 2].long().tolist()) == {0}


def test_phase_conditioned_action_decoder_bounds_and_resolves_trigger() -> None:
    actions = torch.tensor([[2.0, -4.0, 1.0], [-0.5, 0.25, 1.0], [0.0, 0.0, 0.0]])
    option_mask = torch.tensor(
        [[1, 1, 1, 0], [1, 1, 0, 1], [1, 1, 0, 0]], dtype=torch.bool
    )
    vx, yaw, option, valid = decode_phase_conditioned_action(actions, option_mask)
    assert torch.allclose(vx, torch.tensor([0.75, -0.375, 0.0]))
    assert torch.allclose(yaw, torch.tensor([-1.0, 0.25, 0.0]))
    assert option.tolist() == [int(ArmOption.PREPARE_NEXT), int(ArmOption.EXECUTE_CURRENT), 0]
    assert valid.tolist() == [True, True, True]


def test_invalid_trigger_degrades_to_hold_and_is_reported() -> None:
    actions = torch.tensor([[0.0, 0.0, 1.0]])
    option_mask = torch.tensor([[1, 1, 0, 0]], dtype=torch.bool)
    _, _, option, valid = decode_phase_conditioned_action(actions, option_mask)
    assert option.item() == int(ArmOption.HOLD)
    assert not valid.item()


def test_selected_inspection_hubs_are_present_in_mesh_validated_graph() -> None:
    graph_path = (
        REPO_ROOT
        / "lab/ddt_lab/ddt_lab/tasks/moo_based/locomanipulation/velocity/tita_gluon/data"
        / "tita_gluon_cartesian_work_hub_graph.npz"
    )
    with np.load(graph_path) as graph:
        metadata = json.loads(graph["metadata_json"].item())
        positions = graph["node_ee_pos_tita_b_m"]
        edges = {tuple(edge) for edge in graph["edge_index"].tolist()}
        selected = (23, 111, 18, 208)
        assert all((0, node_id) in edges for node_id in selected)
        assert metadata["collision_clearance_m"] == 0.01
        assert metadata["joint_limit_margin_deg"] == 10.0
        assert metadata["max_path_joint_step_deg"] == 2.0
        left_high, right_low, left_low, right_high = positions[list(selected)]
        assert left_high[1] > 0.1 and left_high[2] > 0.5
        assert right_low[1] < -0.1 and right_low[2] < 0.5
        assert left_low[1] > 0.1 and left_low[2] < 0.5
        assert right_high[1] < -0.1 and right_high[2] > 0.5


def test_high_level_observation_tail_contains_binary_mask_and_trigger_phase() -> None:
    batch_size = 3
    zeros_3 = torch.zeros(batch_size, 3)
    option_mask = torch.tensor(
        [[1, 0, 1, 0], [1, 1, 0, 0], [1, 0, 0, 0]], dtype=torch.bool
    )
    observation = build_high_level_policy_observation(
        current_target_pos_b=zeros_3,
        current_target_facing_b=zeros_3,
        next_target_pos_b=zeros_3,
        next_target_facing_b=zeros_3,
        base_lin_vel_b=torch.zeros(batch_size, 2),
        base_yaw_rate=torch.zeros(batch_size),
        arm_joint_pos=torch.zeros(batch_size, 6),
        arm_joint_vel=torch.zeros(batch_size, 6),
        executor_state=torch.tensor([0, 1, 3]),
        active_option=torch.tensor([0, 2, 3]),
        option_progress=torch.tensor([0.0, 0.5, 1.0]),
        current_target_index=torch.tensor([0, 1, 3]),
        target_count=4,
        previous_base_command=torch.zeros(batch_size, 2),
        option_mask=option_mask,
    )
    assert observation.shape == (batch_size, inspection.HIGH_LEVEL_OBSERVATION_DIM)
    trigger_mask, trigger_phase = build_phase_conditioned_trigger_contract(option_mask)
    assert torch.equal(
        observation[:, inspection.HIGH_LEVEL_ACTION_MASK_START : inspection.HIGH_LEVEL_ACTION_MASK_START + 2].bool(),
        trigger_mask,
    )
    assert torch.equal(
        observation[:, inspection.HIGH_LEVEL_ACTION_MASK_START + 2 :].bool(),
        trigger_phase,
    )


def test_go_no_go_reward_rewards_progress_and_penalizes_abort() -> None:
    reward = compute_go_no_go_reward(
        previous_target_distance_m=torch.tensor([1.0, 1.0]),
        target_distance_m=torch.tensor([0.8, 1.0]),
        route_progress_delta_m=torch.tensor([0.1, 0.0]),
        target_completed=torch.tensor([True, False]),
        task_completed=torch.tensor([False, False]),
        base_command_delta_norm=torch.tensor([0.0, 0.0]),
        option_rejected=torch.tensor([False, False]),
        local_abort=torch.tensor([False, True]),
        fall=torch.tensor([False, False]),
        high_level_dt_s=0.1,
    )
    assert reward[0] > 5.0
    assert reward[1] < -4.0


def test_ppo_behavior_cloning_anchor_requires_complete_hybrid_reference() -> None:
    actor = HybridActorCritic(
        num_actor_obs=6,
        num_critic_obs=6,
        num_actions=3,
        actor_hidden_dims=[8],
        critic_hidden_dims=[8],
        continuous_action_dim=2,
        discrete_action_dim=2,
    )
    algorithm = PPO(actor, device="cpu")
    observations = torch.zeros(4, 6)
    actions = torch.tensor(
        [[0.1, 0.0, 0.0], [0.2, 0.1, 0.0], [0.3, 0.0, 1.0], [0.4, -0.1, 1.0]]
    )
    algorithm.set_behavior_cloning_reference(
        observations, actions, coefficient=2.0, batch_size=3
    )
    assert algorithm.behavior_cloning_coefficient == 2.0
    assert algorithm.behavior_cloning_batch_size == 3
    assert algorithm.behavior_cloning_reference_outputs.shape == (4, 4)
    algorithm.set_actor_learning_rate_scale(0.1)
    assert [group["lr"] for group in algorithm.optimizer.param_groups] == [1.0e-4, 1.0e-3]

    with pytest.raises(ValueError, match="every discrete class"):
        algorithm.set_behavior_cloning_reference(
            observations,
            torch.zeros(4, 3),
            coefficient=1.0,
            batch_size=2,
        )
