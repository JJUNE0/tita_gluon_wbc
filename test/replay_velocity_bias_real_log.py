"""DESKTOP_DRY_RUN: passive velocity-bias replay; never estimates closed-loop hardware benefit."""

import argparse
import json
from pathlib import Path
import sqlite3
import sys

import numpy as np
from scipy.spatial.transform import Rotation

from velocity_bias_campaign import REPO, VelocityLaw, digest, write
from sim2sim.lqr.estimator import Sensors, WheelOdometry
from sim2sim.lqr.model import Description
from sim2sim_ros2_jazzy.checkpoint import read_yaml
from sim2sim_ros2_jazzy.adapter import NATIVE_JOINTS
from sim2sim_ros2_jazzy.velocity_bias import VelocityBias


def main():
    from rclpy.serialization import deserialize_message
    from rosidl_runtime_py.utilities import get_message
    sys.path.insert(0, str(REPO / 'test/sim2real'))
    from analyze_flashsac_drift import nearest
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, required=True)
    parser.add_argument('--parameters', type=Path, required=True)
    parser.add_argument('--label', required=True)
    parser.add_argument('--runtime-guard', action='store_true')
    args = parser.parse_args()
    root = args.root.resolve()
    run = 'flashsac_60000_223217_076704901_output_true'
    source = REPO / 'docs/exp/2026-10-16'
    database = next((source / f'{run}_bag').glob('*.db3'))
    cfg = json.loads((REPO / 'sim2real/tita_ws/src/tita_controller/policies/flashsac_60000/config.json').read_text())
    parameters = json.loads(args.parameters.read_text())
    output = root / 'real_shadow' / args.label
    if output.exists():
        raise FileExistsError(output)
    output.mkdir(parents=True)
    before = digest(database)
    with sqlite3.connect(f'file:{database}?mode=ro', uri=True) as connection:
        assert connection.execute('PRAGMA quick_check').fetchone()[0] == 'ok'
        topics = {i: (name, get_message(kind)) for i, name, kind in connection.execute('SELECT id,name,type FROM topics')}
        rows = {name: [] for name, _ in topics.values()}
        for tid, stamp, data in connection.execute('SELECT topic_id,timestamp,data FROM messages ORDER BY timestamp'):
            name, cls = topics[tid]
            rows[name].append((stamp / 1e9, deserialize_message(data, cls)))
    reference = rows['/sim2real/debug/obs']
    stamps = np.array([t for t, _ in reference])
    names = ['/sim2real/debug/state', '/tita4252763/joint_states', '/tita4252763/imu_sensor_broadcaster/imu']
    aligned = []
    valid = np.ones(len(stamps), dtype=bool)
    for name in names:
        times = np.array([t for t, _ in rows[name]])
        indices = nearest(times, stamps)
        valid &= (abs(times[indices] - stamps) <= .008) & np.r_[True, np.diff(indices) > 0]
        aligned.append([rows[name][i][1] for i in indices])
    command_indices = None
    offset = 0
    for term in cfg['policy_interface']['observations']:
        if term['kind'] == 'commands':
            command_indices = offset + np.arange(term['size'])
            command_scale = np.asarray(term['scale'])
        offset += term['size']
    assert command_indices is not None
    source_cfg = read_yaml(next(p for p in cfg['policy_interface']['sources'] if p.endswith('env.yaml')))
    description = Description(source_cfg['scene']['robot']['spawn']['asset_path'])
    estimator = WheelOdometry(description, 0., wrapped_encoders=True)
    law = None
    previous_offset = None
    previous_stamp = None
    age = 0.
    observations = []
    for index in np.flatnonzero(valid):
        stamp = stamps[index]
        dt = .02 if previous_stamp is None else stamp - previous_stamp
        assert dt > 0
        previous_stamp = stamp
        state, joint, imu = (messages[index] for messages in aligned)
        order = [list(joint.name).index(name) for name in NATIVE_JOINTS]
        q = np.asarray(joint.position)[order]
        dq = np.asarray(joint.velocity)[order]
        quat = np.array([imu.orientation.w, imu.orientation.x, imu.orientation.y, imu.orientation.z])
        quat /= np.linalg.norm(quat)
        gyro = np.array([imu.angular_velocity.x, imu.angular_velocity.y, imu.angular_velocity.z])
        raw = estimator.observe(Sensors(q, dq, quat, gyro), dt)
        rotation = Rotation.from_quat(quat[[1, 2, 3, 0]])
        roll, pitch, yaw = rotation.as_euler('xyz')
        frames, _ = description.frames(q)
        offset = rotation.apply(np.mean([frames[name][:3, 3] for name in description.wheel_links], axis=0))
        correction = 0. if previous_offset is None else (offset - previous_offset) @ [np.cos(yaw), np.sin(yaw), 0.] / dt
        previous_offset = offset
        velocity = raw[1] - correction
        command = np.asarray(reference[index][1].data)[command_indices] / command_scale
        if state.data != 'rl' or dt > .06 or np.any(abs(command) >= [.04, .04, .06]):
            law = None
            age = 0.
        elif law is None and np.all(abs(command) <= [.02, .02, .03]):
            if args.runtime_guard:
                gains = dict(parameters)
                gains['response_sign'] = gains.pop('sign', 1.)
                law = VelocityBias(**gains)
            else:
                law = VelocityLaw(parameters)
        bias = 0.
        eligible = False
        if law is not None:
            if args.runtime_guard:
                eligible = (age + 1e-9 >= 1.2 and max(abs(roll), abs(pitch)) <= .3
                            and abs(velocity) <= 1.)
                bias = law.update(float(velocity), dt, enabled=eligible)
            else:
                bias = law.step(float(velocity), dt, age)
                eligible = True
            age += dt
        observations.append([stamp, *command, raw[1], velocity, bias, float(law is not None), float(eligible)])
    values = np.asarray(observations)
    active = values[:, 7] > 0
    assert active.any() and np.isfinite(values).all()
    assert np.max(abs(values[:, 6])) <= parameters['limit'] + 1e-12
    np.savez_compressed(output / 'shadow.npz', values=values,
                        columns=['receipt_time', 'cmd_x', 'cmd_y', 'cmd_yaw', 'raw_speed', 'fk_speed', 'velocity_bias', 'active', 'eligible'])
    assert digest(database) == before
    result = dict(execution_domain='DESKTOP_DRY_RUN', evidence_status='PASS', run=run,
                  checkpoint_sha256=cfg['policy_interface']['checkpoint_sha256'],
                  onnx_sha256=cfg['policy_interface']['onnx_sha256'], bag_sha256=before,
                  parameters=parameters, samples=int(len(values)), active_samples=int(active.sum()),
                  runtime_guard=args.runtime_guard, eligible_samples=int(values[:, 8].sum()),
                  raw_active_mean_m_s=float(values[active, 4].mean()), fk_active_mean_m_s=float(values[active, 5].mean()),
                  bias_min_m_s=float(values[:, 6].min()), bias_max_m_s=float(values[:, 6].max()),
                  no_robot_commands=True, original_bag_unchanged=True,
                  limitations=['Replay uses observed baseline states; no corrected hardware trajectory is inferred.',
                               'No chassis ground truth; wheel slip and sensor-frame assumptions remain unvalidated.',
                               'Nearest receipt-time alignment is not hardware synchronization.'])
    write(output / 'result.json', result)
    (output / 'summary.md').write_text('# Passive real-log velocity-bias replay\n\nExecution Domain: DESKTOP_DRY_RUN\n\n'
        f'Policy Checkpoint SHA256: {result["checkpoint_sha256"]}\n\nEvidence Status: PASS (replay only)\n\n'
        f'Observed metrics / behavior / log summary:\n\n```json\n{json.dumps(result, indent=2)}\n```\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
