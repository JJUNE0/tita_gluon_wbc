"""DESKTOP_DRY_RUN: atomic bias-OFF bag analysis; no ROS nodes or robot commands.

Source ROS and the desktop TrainingSample overlay before execution. The native
observer runs in a pure-math subprocess against recorded states only. Its shadow
bias is never applied to a plant and cannot predict corrected robot motion.
"""
import argparse
import hashlib
import io
import json
from pathlib import Path
import sqlite3
import subprocess
import tempfile

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from rclpy.serialization import deserialize_message
from scipy.spatial.transform import Rotation
from tita_controller.msg import TrainingSample

REPO = Path(__file__).resolve().parents[2]
PACKAGE = REPO / 'sim2real/tita_ws/src/tita_controller'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def stats(values):
    return dict(mean=float(np.mean(values)), std=float(np.std(values)),
                min=float(np.min(values)), max=float(np.max(values)))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('bag', type=Path)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--sim', type=Path, required=True)
    args = parser.parse_args()
    args.bag, args.output, args.sim = args.bag.resolve(), args.output.resolve(), args.sim.resolve()
    args.output.mkdir(parents=True, exist_ok=True)
    db = next(args.bag.glob('*.db3'))
    before = digest(db)
    with sqlite3.connect(f'file:{db}?mode=ro', uri=True) as conn:
        assert conn.execute('PRAGMA quick_check').fetchone()[0] == 'ok'
        topic = conn.execute("SELECT id FROM topics WHERE name='/sim2real/training_sample'").fetchone()
        assert topic
        frames = [deserialize_message(row[0], TrainingSample) for row in conn.execute(
            'SELECT data FROM messages WHERE topic_id=? ORDER BY timestamp', topic)]
        counts = dict(conn.execute('SELECT topics.name,count(*) FROM messages JOIN topics ON messages.topic_id=topics.id GROUP BY topics.id'))
    sequence = np.array([f.sequence_id for f in frames], dtype=np.int64)
    mono = np.array([f.monotonic_ns for f in frames], dtype=np.int64)
    assert np.all(np.diff(mono) > 0)
    states = np.array([f.state for f in frames])
    rl = states == 'rl'
    assert np.count_nonzero(rl & ~np.r_[False, rl[:-1]]) == 1, 'Expected one RL episode'
    t = (mono-mono[rl][0])*1e-9
    dt = np.r_[.02, np.diff(mono)*1e-9]
    field = lambda key: np.array([getattr(f, key) for f in frames])
    q, dq, quat, gyro = [field(k) for k in ('joint_position', 'joint_velocity', 'quaternion_wxyz', 'angular_velocity')]
    command, action, teacher, torque, offsets, diag = [field(k) for k in (
        'command', 'action_raw', 'teacher_action', 'computed_torque', 'wheel_velocity_bias', 'velocity_bias_diagnostics')]
    assert np.isfinite(np.c_[q, dq, quat, gyro, command, action, teacher, torque, offsets, diag]).all()
    assert np.max(abs(offsets[rl])) == 0., 'Not a bias-OFF baseline'
    assert np.max(abs(command[rl])) <= .02, 'Not a neutral baseline'
    assert np.max(abs(teacher[rl]-action[rl])) < 1e-6
    cfg_path = PACKAGE / 'policies/flashsac_60000/config.json'
    cfg = json.loads(cfg_path.read_text())
    geometry_path = PACKAGE / 'config/velocity_bias_geometry.json'
    geometry = json.loads(geometry_path.read_text())
    native = [f'joint_{side}_leg_{i}' for side in ('left', 'right') for i in range(1, 5)]
    terms = []
    for term in cfg['policy_interface']['actions']:
        terms.extend([native.index(term['joint']), int(term['kind'] == 'velocity'),
                      term['scale'], term['offset'], *(term['clip'] or [-1e9, 1e9])])
    header = [*geometry['xyz'], *geometry['rpy'], *geometry['axis'], geometry['wheel_radius'], 1.,
              *cfg['robot']['joint_kp'], *cfg['robot']['joint_kd'], *cfg['robot']['torque_limit'], *terms]
    rows = np.c_[rl, dt, command, q, dq, quat, gyro, action]
    stream = io.StringIO()
    np.savetxt(stream, np.array(header)[None], fmt='%.17g')
    np.savetxt(stream, rows, fmt='%.17g')
    with tempfile.TemporaryDirectory(dir=REPO/'test/sim2real', prefix='free_drift_') as temp:
        binary = Path(temp)/'runtime'
        subprocess.run(['g++', '-std=c++17', '-O2', '-Wall', '-Wextra', '-Werror', '-pedantic',
                        '-I/usr/include/eigen3', '-I', str(PACKAGE/'include'),
                        str(REPO/'test/sim2real/velocity_bias_runtime.cpp'), '-o', str(binary)], check=True)
        output = subprocess.run([str(binary), 'on'], input=stream.getvalue(),
                                capture_output=True, text=True, check=True)
    shadow = np.loadtxt(io.StringIO(output.stdout), ndmin=2)
    assert shadow.shape == (len(frames), 25)
    reconstruction_error = float(abs(shadow[rl, 17:25]-torque[rl]).max())
    assert reconstruction_error < 1e-4, 'Baseline action/PD reconstruction failed'
    velocity = shadow[:, 3]
    # Independent geometric evaluation checks the native float telemetry replay.
    origins = Rotation.from_euler('xyz', np.array(geometry['rpy']).reshape(8, 3)).as_matrix()
    xyz = np.array(geometry['xyz']).reshape(8, 3)
    axes = np.array(geometry['axis']).reshape(8, 3)
    radius = geometry['wheel_radius']
    reference = np.zeros(len(frames))
    previous = None
    for index in range(len(frames)):
        if not rl[index] or not 0 < dt[index] <= .06:
            previous = None
            continue
        rot = Rotation.from_quat(quat[index, [1, 2, 3, 0]]).as_matrix()
        yaw = np.arctan2(rot[1, 0], rot[0, 0])
        lateral = np.array([-np.sin(yaw), np.cos(yaw), 0.])
        forward = np.array([np.cos(yaw), np.sin(yaw), 0.])
        rate, offset = 2*lateral@(rot@gyro[index]), np.zeros(3)
        for side in range(2):
            rotation, position = rot.copy(), np.zeros(3)
            for j in range(4*side, 4*side+4):
                position += rotation@xyz[j]
                rotation = rotation@origins[j]
                rate += (lateral@(rotation@axes[j]))*dq[index, j]
                rotation = rotation@Rotation.from_rotvec(axes[j]*q[index, j]).as_matrix()
            offset += position/2
        reference[index] = radius*rate/2
        if previous is not None:
            reference[index] -= (offset-previous)@forward/dt[index]
        previous = offset
    observer_error = float(abs(reference[rl]-velocity[rl]).max())
    assert observer_error < 1e-5, 'Observer replay/independent FK mismatch'
    w, x, y, z = quat.T
    pitch = np.degrees(np.arcsin(np.clip(2*(w*y-z*x), -1, 1)))
    roll = np.degrees(np.arctan2(2*(w*x+y*z), 1-2*(x*x+y*y)))
    common = lambda a: a[:, [3, 7]].mean(axis=1)
    wheel_proxy = radius*common(dq)
    sim = np.load(args.sim)['state']
    sim_t = np.arange(len(sim))*.02
    windows = []
    for lo, hi in [(0, 2), (.5, 2), (2, 5), (5, 10), (2, float(t[rl][-1])+.001)]:
        mask = rl & (t >= lo) & (t < hi)
        sm = (sim_t >= lo) & (sim_t < hi)
        windows.append(dict(start_s=lo, end_s=hi, real_samples=int(mask.sum()),
            real_fk_velocity_m_s=stats(velocity[mask]), real_wheel_proxy_m_s=stats(wheel_proxy[mask]),
            real_pitch_deg=stats(pitch[mask]), real_roll_deg=stats(roll[mask]),
            real_gyro_y_rad_s=stats(gyro[mask, 1]), real_mean_wheel_torque_nm=stats(common(torque)[mask]),
            sim_fk_velocity_m_s=stats(sim[sm, 8]), sim_ground_truth_velocity_m_s=stats(sim[sm, 3]),
            sim_pitch_deg=stats(np.degrees(sim[sm, 5]))))
    near2 = np.flatnonzero(rl & (t >= 2.))[0]
    eligible = np.flatnonzero(rl & (shadow[:, 1] > .5))
    onset = int(eligible[0]) if len(eligible) else None
    flags = {key: int(np.count_nonzero(~field(key)[rl])) for key in
             ('sensors_valid', 'policy_valid', 'output_enabled', 'torque_sent', 'teacher_action_valid')}
    assert not any(flags.values()), 'RL frame validity/output flag failure'
    result = dict(execution_domain='DESKTOP_DRY_RUN', evidence_status='SUSPICIOUS',
        annotation='Operator labels this run pure free drift, without hand support or intentional command.',
        run=args.bag.name.removesuffix('_bag'), checkpoint_sha256=cfg['policy_interface']['checkpoint_sha256'],
        onnx_sha256=cfg['policy_interface']['onnx_sha256'], frames=len(frames), topic_counts=counts,
        rl_samples=int(rl.sum()), rl_last_sample_s=float(t[rl][-1]),
        sequence_missing=int(np.maximum(np.diff(sequence)-1, 0).sum()), sequence_nonincreasing=int((np.diff(sequence) <= 0).sum()),
        sample_dt_s=stats(dt[1:]), rl_dt_s=stats(dt[rl]), rl_dt_over_30ms=int((dt[rl] > .03).sum()),
        command_abs_max=np.abs(command[rl]).max(axis=0).tolist(), bias_offset_abs_max=float(abs(offsets[rl]).max()),
        logged_diagnostics_abs_max=float(abs(diag[rl]).max()), rl_false_flags=flags,
        baseline_torque_reconstruction_error_nm=reconstruction_error, independent_observer_error_m_s=observer_error,
        teacher_action_error=float(abs(teacher[rl]-action[rl]).max()),
        at_2s=dict(real_time=float(t[near2]), real_fk_m_s=float(velocity[near2]),
                   real_wheel_proxy_m_s=float(wheel_proxy[near2]), real_pitch_deg=float(pitch[near2]),
                   sim_fk_m_s=float(sim[100, 8]), sim_ground_truth_m_s=float(sim[100, 3]),
                   sim_pitch_deg=float(np.degrees(sim[100, 5]))),
        shadow_first_eligible=None if onset is None else dict(time=float(t[onset]),
            estimated_velocity_m_s=float(velocity[onset]), seeded_integral_m_s=float(shadow[onset, 5]),
            seeded_equivalent_nm_per_wheel=float(.5*shadow[onset, 5]/radius)),
        windows=windows, source_sha256={str(p.relative_to(REPO)): digest(p) for p in
            (db, cfg_path, geometry_path, PACKAGE/'include/tita_controller/velocity_bias.hpp',
             REPO/'test/sim2real/velocity_bias_runtime.cpp', args.sim, Path(__file__))},
        limitations=['No external chassis ground-truth velocity or distance: encoders may slip and sensor frames may be wrong.',
                     'Sim time is rollout time, real time is RL entry; startup states and stand-up processes differ.',
                     'Shadow seed is math on baseline states, not an observed bias-ON robot outcome.',
                     'Torque is a computed command; torque_sent is transport acceptance, not measured torque.',
                     '50 Hz snapshots cannot validate 2 ms deadlines or exclude higher-frequency aliasing.'])
    assert digest(db) == before
    (args.output/'metrics.json').write_text(json.dumps(result, indent=2)+'\n')
    np.savez_compressed(args.output/'signals.npz', t=t, rl=rl, q=q, dq=dq, quat=quat, gyro=gyro,
        command=command, action=action, teacher=teacher, torque=torque, pitch=pitch, roll=roll,
        velocity=velocity, wheel_proxy=wheel_proxy, shadow=shadow)
    fig, ax = plt.subplots(4, 1, figsize=(12, 12), sharex=True, constrained_layout=True)
    ax[0].plot(t[rl], velocity[rl], label='Real: passive IMU/FK estimate')
    ax[0].plot(t[rl], wheel_proxy[rl], label='Real: wheel rolling proxy', alpha=.65)
    sm = sim_t <= t[rl][-1]
    ax[0].plot(sim_t[sm], sim[sm, 8], label='Nominal sim: FK estimate', alpha=.8)
    ax[0].plot(sim_t[sm], sim[sm, 3], label='Nominal sim: ground truth', ls='--')
    ax[0].set_ylabel('Forward speed (m/s)')
    ax[1].plot(t[rl], pitch[rl], label='Real: pitch')
    ax[1].plot(t[rl], roll[rl], label='Real: roll', alpha=.6)
    ax[1].plot(sim_t[sm], np.degrees(sim[sm, 5]), label='Nominal sim: pitch', ls='--')
    ax[1].set_ylabel('degrees')
    ax[2].plot(t[rl], torque[rl, 3], label='Left computed wheel torque', alpha=.7)
    ax[2].plot(t[rl], torque[rl, 7], label='Right computed wheel torque', alpha=.7)
    ax[2].set_ylabel('Nm')
    ax[3].plot(t[rl], command[rl, 0], label='Forward command')
    ax[3].plot(t[rl], offsets[rl, 0], label='Recorded left bias (rad/s)', ls='--')
    ax[3].set_ylabel('m/s; rad/s')
    ax[3].set_xlabel('Seconds from real RL entry / nominal sim rollout start')
    for axis in ax:
        axis.axvline(2, color='gray', ls=':', label='2 s reference')
        axis.grid(alpha=.2)
        axis.legend(loc='best', fontsize=8)
    fig.suptitle('FlashSAC bias OFF: operator-labelled free drift\nReal velocity is estimated; no external ground truth')
    fig.savefig(args.output/'free_drift_comparison.png', dpi=160)
    plt.close(fig)
    print(json.dumps({k: v for k, v in result.items() if k not in ('source_sha256', 'topic_counts')}, indent=2))


if __name__ == '__main__':
    main()
