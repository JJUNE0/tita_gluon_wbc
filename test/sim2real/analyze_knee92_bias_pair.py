"""DESKTOP_DRY_RUN: paired recorded-state bias replay; no nodes, SDK or CAN.

Uses the current pinned 80000 deployment config. A command-zero shadow replay
only exposes the FK velocity estimate; it does not predict a new trajectory.
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
from tita_controller.msg import TrainingSample

REPO = Path(__file__).resolve().parents[2]
PACKAGE = REPO / 'sim2real/tita_ws/src/tita_controller'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def blocks(mask):
    ind = np.flatnonzero(mask)
    return np.split(ind, np.flatnonzero(np.diff(ind) > 1) + 1) if len(ind) else []


def stats(value):
    if not len(value):
        return None
    return dict(mean=float(np.mean(value)), std=float(np.std(value)),
                min=float(np.min(value)), max=float(np.max(value)),
                mean_abs=float(np.mean(abs(value))), rms=float(np.sqrt(np.mean(value**2))))


def load(bag):
    db = next(bag.glob('*.db3'))
    sha = digest(db)
    with sqlite3.connect(f'file:{db}?mode=ro', uri=True) as conn:
        assert conn.execute('PRAGMA quick_check').fetchone()[0] == 'ok'
        topic = conn.execute("SELECT id FROM topics WHERE name='/sim2real/training_sample'").fetchone()
        frames = [deserialize_message(r[0], TrainingSample) for r in conn.execute(
            'SELECT data FROM messages WHERE topic_id=? ORDER BY timestamp', topic)]
    get = lambda key: np.array([getattr(f, key) for f in frames])
    mono, sequence = get('monotonic_ns').astype(np.int64), get('sequence_id').astype(np.int64)
    assert (np.diff(mono) > 0).all() and (np.diff(sequence) == 1).all()
    d = {'rl': get('state') == 'rl'}
    assert len(blocks(d['rl'])) == 1
    d['t'] = (mono - mono[d['rl']][0]) * 1e-9
    d['dt'] = np.r_[.02, np.diff(mono)*1e-9]
    for name, field in dict(q='joint_position', dq='joint_velocity', quat='quaternion_wxyz',
            gyro='angular_velocity', command='command', action='action_raw',
            torque='computed_torque', offsets='wheel_velocity_bias', diag='velocity_bias_diagnostics').items():
        d[name] = get(field)
        assert np.isfinite(d[name]).all(), name
    for field in ('sensors_valid', 'policy_valid', 'output_enabled', 'torque_sent'):
        assert get(field)[d['rl']].all(), field
    assert digest(db) == sha
    d['source_db'], d['source_db_sha256'] = str(db.relative_to(REPO)), sha
    return d


def replay(binary, d, header, zero_command=False):
    dt = d['dt'].copy()
    dt[np.flatnonzero(d['rl'])[0]] = .02
    command = np.zeros_like(d['command']) if zero_command else d['command']
    rows = np.c_[d['rl'], dt, command, d['q'], d['dq'], d['quat'], d['gyro'], d['action']]
    stream = io.StringIO()
    np.savetxt(stream, np.array(header)[None], fmt='%.17g')
    np.savetxt(stream, rows, fmt='%.17g')
    result = subprocess.run([str(binary), 'status'], input=stream.getvalue(),
                            text=True, capture_output=True, check=True)
    return np.loadtxt(io.StringIO(result.stdout), ndmin=2)


def torque(action, d, cfg, corrected):
    native = [f'joint_{side}_leg_{i}' for side in ('left', 'right') for i in range(1, 5)]
    target = np.zeros_like(action, dtype=float)
    velocity = np.zeros(8, dtype=bool)
    for i, term in enumerate(cfg['policy_interface']['actions']):
        j = native.index(term['joint'])
        target[:, j] = np.clip(action[:, i]*term['scale'] + term['offset'],
                               *(term['clip'] or [-1e9, 1e9]))
        velocity[j] = term['kind'] == 'velocity'
    if corrected:
        target[:, [3, 7]] += d['offsets']
    kp, kd = [np.array(cfg['robot'][k]) for k in ('joint_kp', 'joint_kd')]
    out = kp*(target-d['q']) - kd*d['dq']
    out[:, velocity] = kd[velocity]*(target[:, velocity] - d['dq'][:, velocity])
    return np.clip(out, -np.array(cfg['robot']['torque_limit']), cfg['robot']['torque_limit'])


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--root', type=Path, required=True)
    args = p.parse_args()
    root = args.root.resolve()
    cfg_path = PACKAGE / 'policies/flashsac_80000/config.json'
    cfg = json.loads(cfg_path.read_text())
    geo = json.loads((PACKAGE / 'config/velocity_bias_geometry.json').read_text())
    assert digest(cfg_path) == 'a24c2137969f854fc98cc3027884dbbadad4060f18db7758b028c12ca1405719'
    native = [f'joint_{side}_leg_{i}' for side in ('left', 'right') for i in range(1, 5)]
    terms = []
    for a in cfg['policy_interface']['actions']:
        terms.extend([native.index(a['joint']), int(a['kind'] == 'velocity'),
                      a['scale'], a['offset'], *(a['clip'] or [-1e9, 1e9])])
    header = [*geo['xyz'], *geo['rpy'], *geo['axis'], geo['wheel_radius'], 1.,
              *cfg['robot']['joint_kp'], *cfg['robot']['joint_kd'], *cfg['robot']['torque_limit'], *terms]
    cases = dict(off=next(root.glob('*125618*_bag')), on=next(root.glob('*125911*_bag')))
    report = dict(execution_domain='DESKTOP_DRY_RUN', evidence_status='SUSPICIOUS',
        checkpoint_sha256=cfg['policy_interface']['checkpoint_sha256'],
        onnx_sha256=cfg['policy_interface']['onnx_sha256'], config_sha256=digest(cfg_path), cases={})
    signals = {}
    with tempfile.TemporaryDirectory(dir=REPO/'test/sim2real', prefix='knee92_pair_') as temp:
        binary = Path(temp)/'runtime'
        subprocess.run(['g++', '-std=c++17', '-O2', '-Wall', '-Wextra', '-Werror', '-pedantic',
            '-isystem', '/usr/include/eigen3', '-I', str(PACKAGE/'include'),
            str(REPO/'test/sim2real/velocity_bias_runtime.cpp'), '-o', str(binary)], check=True)
        for name, path in cases.items():
            d = load(path)
            r = replay(binary, d, header)
            shadow = replay(binary, d, header, True)
            t, rl = d['t'], d['rl']
            assert r.shape == (len(t), 29)
            if name == 'on':
                np.testing.assert_allclose(r[rl, :9], d['diag'][rl, :9], atol=1e-5, rtol=1e-5)
            else:
                assert not d['offsets'][rl].any() and not d['diag'][rl].any()
            baseline = torque(d['action'].astype(float), d, cfg, False)
            corrected = torque(d['action'].astype(float), d, cfg, True)
            error = float(abs(corrected[rl]-d['torque'][rl]).max())
            assert error < 1e-8
            added = d['torque']-baseline
            np.testing.assert_allclose(added[rl][:, [3, 7]], d['diag'][rl, 9:11], atol=1e-6)
            assert abs(added[rl]).max() <= .8+1e-8
            w, x, y, z = d['quat'].T
            pitch = np.degrees(np.arcsin(np.clip(2*(w*y-z*x), -1, 1)))
            neutral = rl & (abs(d['command']) <= np.array([.02, .02, .03])).all(axis=1)
            eligible = rl & (d['diag'][:, 1] > .5)
            common = lambda a: a[:, [3, 7]].mean(axis=1)
            speed = shadow[:, 3]
            def window(mask):
                ind = np.flatnonzero(mask)
                if len(ind) < 2:
                    return {'samples': len(ind)}
                return dict(samples=len(ind), start_s=float(t[ind[0]]), end_s=float(t[ind[-1]]),
                    fk_speed_m_s=stats(speed[mask]), wheel_proxy_m_s=stats(geo['wheel_radius']*common(d['dq'])[mask]),
                    pitch_deg=stats(pitch[mask]), command_x=stats(d['command'][mask, 0]),
                    command_yaw=stats(d['command'][mask, 2]), added_nm=stats(common(added)[mask]),
                    baseline_nm=stats(common(baseline)[mask]), final_nm=stats(common(d['torque'])[mask]),
                    cap_fraction=float((abs(common(added)[mask]) >= .7999).mean()),
                    estimated_displacement_m=float(np.sum(speed[mask]*d['dt'][mask])),
                    wheel_saturation_fraction=(abs(d['torque'][mask][:, [3, 7]]) >= 11.9999).mean(axis=0).tolist())
            episodes = []
            for ind in blocks((r[:, 0] > .5) & rl):
                mask = np.zeros(len(t), dtype=bool); mask[ind] = True
                active = ind[r[ind, 1] > .5]
                entry = dict(start_s=float(t[ind[0]]), end_s=float(t[ind[-1]]),
                    actual_controller=(name == 'on'), acquisition=window(mask & (r[:, 2] >= 1.) & (r[:, 2] < 3.)))
                if len(active):
                    i, last = active[0], active[-1]
                    cap = active[abs(common(added)[active]) >= .7999] if name == 'on' else []
                    entry.update(acquired_s=float(t[i]), drift_acquired_m_s=float(r[i, 27]),
                        pitch_reference_deg=float(np.degrees(r[i, 28])), eligible=window(mask & (r[:, 1] > .5)),
                        last_3s=window(mask & (t >= max(t[i]+1., t[last]-3.)) & (t <= t[last])),
                        first_cap_s=float(t[cap[0]]) if len(cap) else None)
                episodes.append(entry)
            guard = []
            for ind in blocks(rl & (r[:, 26] > .5)):
                i = ind[0]
                guard.append(dict(start_s=float(t[i]), end_s=float(t[ind[-1]]),
                    pitch_deg=float(pitch[i]), reference_deg=float(np.degrees(r[i, 28])),
                    velocity=float(r[i, 3])))
            result = dict(source_db=d['source_db'], source_db_sha256=d['source_db_sha256'],
                rl_samples=int(rl.sum()), rl_duration_s=float(t[rl][-1]),
                rl_dt_s=stats(d['dt'][rl]), torque_reconstruction_error_nm=error,
                logged_diag_replay_max_error=float(abs(r[rl, :9]-d['diag'][rl, :9]).max()) if name == 'on' else None,
                all_neutral=window(neutral), neutral_5_10=window(neutral & (t >= 5) & (t < 10)),
                neutral_5_12=window(neutral & (t >= 5) & (t < 12)),
                eligible=window(eligible), episodes=episodes, guard_intervals=guard,
                command_intervals=[dict(start_s=float(t[i[0]]), end_s=float(t[i[-1]]),
                    x_min=float(d['command'][i, 0].min()), x_max=float(d['command'][i, 0].max()),
                    yaw_abs_max=float(abs(d['command'][i, 2]).max())) for i in blocks(rl & ~neutral)],
                neutral_windows=[window(neutral & (t >= lo) & (t < lo+2)) for lo in np.arange(3., t[rl][-1], 2.)])
            report['cases'][name] = result
            signals[name] = dict(t=t, rl=rl, speed=speed, pitch=pitch, command=d['command'],
                baseline=common(baseline), added=common(added), final=common(d['torque']),
                eligible=d['diag'][:, 1], hold_age=d['diag'][:, 2], inhibited=r[:, 26],
                pitch_ref=np.degrees(r[:, 28]))
            np.savez_compressed(root/f'{name}_signals.npz', **signals[name])
    report['limitations'] = [
        'Separate operator trials; command, external contact and initial posture may differ.',
        'FK/encoder/IMU velocity assumes rolling contact; no independent chassis displacement measurement.',
        'Computed torque and transport success do not prove calibrated motor torque.',
        'Recorded-state replay validates implementation, not feedback sign or a counterfactual plant trajectory.',
        'OFF controller episodes describe hypothetical gate timing on recorded states, not applied bias.']
    report['sources'] = {str(p.relative_to(REPO)): digest(p) for p in
        [Path(__file__), cfg_path, PACKAGE/'include/tita_controller/velocity_bias.hpp',
         PACKAGE/'include/tita_controller/adapter.hpp', REPO/'test/sim2real/velocity_bias_runtime.cpp']}
    (root/'metrics.json').write_text(json.dumps(report, indent=2)+'\n')
    fig, axes = plt.subplots(5, 2, figsize=(14, 12), sharex='col', constrained_layout=True)
    for col, name in enumerate(('off', 'on')):
        d = signals[name]; m=d['rl']; t=d['t'][m]
        axes[0,col].plot(t,d['command'][m,0],label='forward command')
        axes[0,col].plot(t,d['command'][m,2],label='yaw command')
        axes[1,col].plot(t,d['speed'][m],label='FK estimated speed')
        axes[1,col].axhline(0,color='gray',ls=':')
        axes[2,col].plot(t,d['pitch'][m],label='pitch')
        if name=='on': axes[2,col].plot(t,np.where(d['hold_age'][m]>=3,d['pitch_ref'][m],np.nan),ls='--',label='acquired reference')
        axes[3,col].plot(t,d['baseline'][m],label='policy/PD')
        axes[3,col].plot(t,d['added'][m],label='added bias')
        axes[3,col].plot(t,d['final'][m],alpha=.65,label='final')
        axes[3,col].axhline(.8,color='gray',ls=':')
        axes[3,col].axhline(-.8,color='gray',ls=':')
        axes[4,col].plot(t,d['eligible'][m],label='eligible')
        if name=='on':axes[4,col].plot(t,d['inhibited'][m],label='guard inhibited')
        axes[0,col].set_title('Bias '+name.upper())
        axes[4,col].set_xlabel('Seconds from RL entry')
        for row,unit in enumerate(('m/s; rad/s','m/s estimate','degrees','Nm per wheel','flag')):
            axes[row,col].set_ylabel(unit);axes[row,col].grid(alpha=.2);axes[row,col].legend(fontsize=8)
    fig.suptitle('Same policy / knee-only PD: recorded OFF vs bounded bias ON\nSeparate operator trials; torque is computed command, speed is a rolling-contact estimate')
    fig.savefig(root/'comparison.png',dpi=160);plt.close(fig)
    for name,value in report['cases'].items():
        print(name,json.dumps(value,indent=2))


if __name__ == '__main__':
    main()
