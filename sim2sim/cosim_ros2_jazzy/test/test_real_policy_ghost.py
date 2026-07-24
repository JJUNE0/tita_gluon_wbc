from dataclasses import replace
from pathlib import Path

import numpy as np
import pytest
import yaml

from cosim_ros2_jazzy.mujoco_env import TitaMujocoEnv
from cosim_ros2_jazzy.real_policy_core import (
    NATIVE_JOINT_NAMES,
    RealPolicyEngine,
    RealSnapshot,
    apply_kinematic_preview,
    gate_status,
    native_joint_arrays,
    policy_action_to_native,
    reset_mujoco_from_snapshot,
)
from cosim_ros2_jazzy.relay_protocol import (
    RelayCommand,
    RelayPacketError,
    command_for_transmit,
    command_from_packet,
    decode_packet_line,
    encode_packet,
)


ROOT = Path(__file__).resolve().parents[2]


class CommandPolicy:
    def act(self, obs, history):
        action = np.zeros(8, dtype=np.float32)
        action[6] = float(obs[6] + obs[8])
        action[7] = float(obs[6] - obs[8])
        return action


class NonFinitePolicy:
    def act(self, obs, history):
        return np.asarray([np.nan] + [0.0] * 7, dtype=np.float32)


def cfg():
    with (ROOT / "cosim_ros2_jazzy" / "config" / "tita.yaml").open(encoding="utf-8") as stream:
        return yaml.safe_load(stream)


def snapshot():
    return RealSnapshot(
        joint_pos_native=np.asarray([0.1, 0.8, -1.5, 0.0, 0.1, 0.8, -1.5, 0.0], dtype=np.float32),
        joint_vel_native=np.zeros(8, dtype=np.float32),
        base_quat_wxyz=np.asarray([1.0, 0.0, 0.0, 0.0], dtype=np.float32),
        base_ang_vel=np.zeros(3, dtype=np.float32),
        base_pos=np.asarray([0.0, 0.0, 0.4], dtype=np.float32),
        base_lin_vel=np.zeros(3, dtype=np.float32),
    )


def test_sensor_only_v1_packet_decode_is_backward_compatible():
    packet = {"schema": "tita_state_relay.v1", "seq": 1, "joint_states": {"available": False}}
    assert decode_packet_line(encode_packet(packet).strip())["seq"] == 1
    assert not command_from_packet(packet).valid


def test_v2_command_decode_and_nonfinite_rejection():
    packet = {
        "schema": "tita_state_relay.v2", "seq": 2,
        "command": RelayCommand("processed_twist", True, 123, 0.1, 0.0, -0.2).as_packet(),
    }
    command = command_from_packet(decode_packet_line(encode_packet(packet).strip()))
    assert command.valid and (command.linear_x, command.linear_y, command.angular_z) == (0.1, 0.0, -0.2)
    with pytest.raises(RelayPacketError):
        decode_packet_line(b'{"schema":"tita_state_relay.v2","command":{"linear_x":NaN}}')
    with pytest.raises(RelayPacketError):
        decode_packet_line(b'{"schema":"tita_state_relay.v1","joint_states":{"available":true,"position":["bad"]}}')


def test_command_stale_is_zero_and_invalid():
    command = RelayCommand("processed_twist", True, 10, 0.2, 0.0, 0.1)
    stale = command_for_transmit(command, 1_000_000_000, 2_000_000_000, 0.5)
    assert not stale.valid
    assert (stale.linear_x, stale.linear_y, stale.angular_z) == (0.0, 0.0, 0.0)


def test_fsm_and_sensor_gate_fail_closed():
    allowed = {"balance"}
    assert gate_status(sensor_received=True, sensors_fresh=True, values_finite=True,
                       fsm_received=False, fsm_mode="", allowed_modes=allowed, connected=True) == "blocked:fsm_not_received"
    assert gate_status(sensor_received=True, sensors_fresh=True, values_finite=True,
                       fsm_received=True, fsm_mode="balance", allowed_modes=allowed, connected=True).startswith("ready:")
    assert gate_status(sensor_received=True, sensors_fresh=False, values_finite=True,
                       fsm_received=True, fsm_mode="balance", allowed_modes=allowed, connected=True) == "blocked:sensor_stale"


def test_native_action_command_observation_and_shapes():
    positions = list(range(8))
    pos, vel = native_joint_arrays(list(NATIVE_JOINT_NAMES), positions, [0.0] * 8)
    assert pos.tolist() == list(map(float, positions))
    policy = np.asarray(range(8), dtype=np.float32)
    assert policy_action_to_native(policy).tolist() == list(map(float, range(8)))
    engine = RealPolicyEngine(cfg(), CommandPolicy())
    frame = engine.step(snapshot(), np.asarray([0.1, 0.0, 0.2], dtype=np.float32))
    assert frame.obs_current.shape == (33,)
    assert frame.obs_history.shape == (10, 33)
    assert np.allclose(frame.obs_current[6:9], [0.2, 0.0, 0.05])
    assert frame.action_policy.shape == (8,)
    assert frame.virtual_leg_target_native.shape == (6,)
    assert frame.virtual_wheel_vel_native.shape == (2,)
    assert np.all(np.isfinite(frame.virtual_leg_target_native))
    assert np.all(np.isfinite(frame.virtual_wheel_vel_native))


def test_nonfinite_action_fails_closed():
    with pytest.raises(ValueError, match="non-finite policy action"):
        RealPolicyEngine(cfg(), NonFinitePolicy()).step(snapshot(), np.zeros(3, dtype=np.float32))


def test_zero_forward_yaw_ghost_mapping_and_snapshot_reset():
    pytest.importorskip("mujoco")
    configuration = cfg()
    configuration["control"]["real_time"] = False
    env = TitaMujocoEnv(configuration, viewer_enabled=False)
    try:
        snap = snapshot()
        planar_odom_snap = replace(snap, base_pos=np.asarray([1.0, -2.0, 0.0], dtype=np.float32))
        ghost_snap = replace(
            planar_odom_snap,
            base_pos=np.asarray([1.0, -2.0, 0.4], dtype=np.float32),
        )
        reset_mujoco_from_snapshot(env, ghost_snap)
        assert np.allclose(env.base_pos(), [1.0, -2.0, 0.4])
        assert np.allclose(env.joint_pos(), ghost_snap.joint_pos_native)
        engine = RealPolicyEngine(configuration, CommandPolicy())
        zero = engine.step(snap, np.zeros(3, dtype=np.float32))
        forward = engine.step(snap, np.asarray([0.1, 0.0, 0.0], dtype=np.float32))
        yaw = engine.step(snap, np.asarray([0.0, 0.0, 0.2], dtype=np.float32))
        assert np.allclose(zero.virtual_wheel_vel_native, [0.0, 0.0])
        assert np.sign(forward.virtual_wheel_vel_native[0]) == np.sign(forward.virtual_wheel_vel_native[1])
        assert np.sign(yaw.virtual_wheel_vel_native[0]) == -np.sign(yaw.virtual_wheel_vel_native[1])

        base_before = env.base_pos().copy()
        wheel_before = env.joint_pos()[[3, 7]].copy()
        apply_kinematic_preview(env, forward, 0.02)
        assert np.allclose(env.base_pos(), base_before)
        assert np.allclose(env.joint_pos()[[0, 1, 2, 4, 5, 6]], forward.virtual_leg_target_native)
        assert np.allclose(
            env.joint_pos()[[3, 7]],
            wheel_before + forward.virtual_wheel_vel_native * 0.02,
        )
        assert np.allclose(env.data.ctrl, 0.0)
    finally:
        env.close()


def test_static_sender_and_ghost_have_no_robot_command_publishers():
    package = ROOT / "cosim_ros2_jazzy" / "cosim_ros2_jazzy"
    sender = (package / "tita_state_relay_sender.py").read_text(encoding="utf-8")
    ghost = (package / "tita_real_policy_ghost_node.py").read_text(encoding="utf-8")
    launch = (ROOT / "cosim_ros2_jazzy" / "launch" / "tita_real_policy_ghost.launch.py").read_text(encoding="utf-8")
    assert "create_publisher" not in sender
    assert 'base = "/cosim_ros2_jazzy/real_policy"' in ghost
    forbidden = ("ros2 topic pub", "LocomotionCmd", "ExecuteProcess", "OnShutdown")
    assert not any(token in sender + ghost + launch for token in forbidden)
