"""DESKTOP_DRY_RUN: neutral-hold pitch, drift and leg load per RL segment of a copied FlashSAC bag.

Reads the bag read-only (``TrainingSample`` + ``MotorFeedback``). Unlike
``analyze_motor_feedback_run.py`` it accepts several RL entries (rl -> return_to_sit -> sit -> rl)
and does not replay a policy bundle. Speed is the existing encoder/IMU/FK reconstruction (no ground
truth); ``computed`` torque is the command, ``reported`` is the SDK value (not a calibrated Nm).
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sqlite3
import sys
from pathlib import Path

import numpy as np
from rclpy.serialization import deserialize_message
from tita_controller.msg import MotorFeedback, TrainingSample

sys.path.insert(0, str(Path(__file__).resolve().parent))
from analyze_motor_feedback_run import fk_velocity  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
GEOMETRY = ROOT / 'sim2real/tita_ws/src/tita_controller/config/velocity_bias_geometry.json'
NEUTRAL = np.array([.02, .02, .03])


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def runs(mask: np.ndarray) -> list[tuple[int, int]]:
    edges = np.flatnonzero(np.diff(np.r_[0, mask.astype(int), 0]))
    return list(zip(edges[::2], edges[1::2]))


def stats(x: np.ndarray) -> dict:
    return dict(mean=float(np.mean(x)), std=float(np.std(x)), min=float(np.min(x)), max=float(np.max(x)))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--bag', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--settle', type=float, default=1.0, help='neutral age before a sample counts as held [s]')
    parser.add_argument('--min-window', type=float, default=0.5, help='shortest neutral window reported [s]')
    args = parser.parse_args()
    out = args.output.resolve()
    assert out.is_relative_to(ROOT / 'docs/exp')
    out.mkdir(parents=True, exist_ok=True)
    db = next(args.bag.resolve().glob('*.db3'))
    with sqlite3.connect(f'file:{db}?mode=ro', uri=True) as conn:
        assert conn.execute('PRAGMA quick_check').fetchone()[0] == 'ok'
        ids = dict(conn.execute('SELECT name,id FROM topics'))
        samples = [deserialize_message(b, TrainingSample) for b, in conn.execute(
            'SELECT data FROM messages WHERE topic_id=? ORDER BY timestamp', (ids['/sim2real/training_sample'],))]
        feedback = {}
        if '/sim2real/motor_feedback' in ids:
            for b, in conn.execute('SELECT data FROM messages WHERE topic_id=? ORDER BY timestamp',
                                   (ids['/sim2real/motor_feedback'],)):
                f = deserialize_message(b, MotorFeedback)
                feedback[f.sequence_id] = f
    get = lambda name: np.array([getattr(s, name) for s in samples])
    mono = get('monotonic_ns').astype(np.int64)
    assert np.all(np.diff(mono) > 0)
    state = get('state')
    rl = state == 'rl'
    q, dq, quat, gyro, command, torque, bias = [get(n) for n in (
        'joint_position', 'joint_velocity', 'quaternion_wxyz', 'angular_velocity', 'command', 'computed_torque',
        'wheel_velocity_bias')]
    assert np.isfinite(np.c_[q, dq, quat, gyro, command, torque]).all()
    assert np.max(np.abs(bias[rl])) == 0, 'velocity bias active; this review assumes bias OFF'
    reported = np.full_like(torque, np.nan)
    for i, s in enumerate(samples):
        f = feedback.get(s.sequence_id)
        if f is not None and f.valid:
            reported[i] = f.reported_torque
    t = (mono - mono[0]) * 1e-9
    dt = np.r_[.02, np.diff(mono) * 1e-9]
    w, x, y, z = quat.T
    pitch = np.degrees(np.arcsin(np.clip(2 * (w * y - z * x), -1, 1)))
    velocity = fk_velocity(q, dq, quat, gyro, dt, rl, json.loads(GEOMETRY.read_text()))

    segments = []
    for k, (a, b) in enumerate(runs(rl)):
        idx = np.arange(a, b)
        ts = t[idx] - t[a]
        neutral = np.all(np.abs(command[idx]) <= NEUTRAL, axis=1)
        age = np.zeros(len(idx))
        for i in range(1, len(idx)):
            age[i] = age[i - 1] + dt[idx[i]] if neutral[i] and neutral[i - 1] else 0.
        held = neutral & (age >= args.settle) & (ts >= 3.0)
        windows = []
        for wa, wb in runs(held):
            sel = idx[wa:wb]
            if t[sel[-1]] - t[sel[0]] < args.min_window:
                continue
            windows.append(dict(
                start_s=float(ts[wa]), end_s=float(ts[wb - 1]), samples=int(len(sel)),
                fk_speed=stats(velocity[sel]), pitch_deg=stats(pitch[sel]),
                knee_q=[float(q[sel, 2].mean()), float(q[sel, 6].mean())],
                thigh_q=[float(q[sel, 1].mean()), float(q[sel, 5].mean())],
                hip_q=[float(q[sel, 0].mean()), float(q[sel, 4].mean())],
                knee_tau_computed=[float(torque[sel, 2].mean()), float(torque[sel, 6].mean())],
                knee_tau_reported=[float(np.nanmean(reported[sel, 2])), float(np.nanmean(reported[sel, 6]))],
                wheel_tau_computed=[float(torque[sel, 3].mean()), float(torque[sel, 7].mean())]))
        start = idx[ts < 3.0]
        moving = idx[~neutral]
        segments.append(dict(
            index=k, start_s=float(t[a]), duration_s=float(t[b - 1] - t[a]), frames=int(b - a),
            command_abs_max=np.abs(command[idx]).max(0).tolist(),
            moving_fraction=float(len(moving) / len(idx)),
            startup_0to3s=dict(pitch_peak_deg=float(np.max(np.abs(pitch[start]))),
                               wheel_tau_computed_peak=float(np.max(np.abs(torque[start][:, [3, 7]]))),
                               wheel_tau_reported_peak=float(np.nanmax(np.abs(reported[start][:, [3, 7]])))
                               if np.isfinite(reported[start][:, [3, 7]]).any() else None),
            held_neutral=dict(samples=int(held.sum()),
                              fk_speed=stats(velocity[idx][held]) if held.any() else None,
                              pitch_deg=stats(pitch[idx][held]) if held.any() else None),
            neutral_windows=windows))
    transitions = [dict(t_s=float(t[i]), state=str(state[i])) for i in range(len(state))
                   if i == 0 or state[i] != state[i - 1]]
    report = dict(execution_domain='DESKTOP_DRY_RUN', bag_db3=str(db), bag_db3_sha256=digest(db),
                  geometry_sha256=digest(GEOMETRY), samples=len(samples), feedback=len(feedback),
                  transitions=transitions, segments=segments,
                  notes='speed = encoder/IMU/FK estimate; computed torque = command; reported = SDK value')
    (out / 'segments.json').write_text(json.dumps(report, indent=2) + '\n')
    np.savez_compressed(out / 'signals.npz', t=t, state=state.astype(str), rl=rl, q=q, dq=dq, quat=quat, gyro=gyro,
                        command=command, torque=torque, reported=reported, pitch=pitch, velocity=velocity)
    print('[DESKTOP_DRY_RUN] transitions:', ', '.join(f"{tr['state']}@{tr['t_s']:.1f}" for tr in transitions))
    for s in segments:
        h = s['held_neutral']
        print(f"segment {s['index']}: {s['duration_s']:.1f} s, moving {s['moving_fraction']:.0%}, |cmd|max "
              f"{np.round(s['command_abs_max'], 2).tolist()}, startup pitch peak {s['startup_0to3s']['pitch_peak_deg']:.1f} deg, "
              f"wheel peak cmd/rep {s['startup_0to3s']['wheel_tau_computed_peak']:.2f}/{s['startup_0to3s']['wheel_tau_reported_peak']}")
        if h['samples']:
            print(f"   held neutral n={h['samples']}: FK speed {h['fk_speed']['mean']:+.3f}+-{h['fk_speed']['std']:.3f} m/s, "
                  f"pitch {h['pitch_deg']['mean']:.2f}+-{h['pitch_deg']['std']:.2f} deg")
        for wdw in s['neutral_windows']:
            print(f"   window {wdw['start_s']:5.1f}-{wdw['end_s']:5.1f} s n={wdw['samples']:3d}: v {wdw['fk_speed']['mean']:+.3f} "
                  f"pitch {wdw['pitch_deg']['mean']:.2f}+-{wdw['pitch_deg']['std']:.2f} knee {np.round(wdw['knee_q'], 3).tolist()} "
                  f"thigh {np.round(wdw['thigh_q'], 3).tolist()} hip {np.round(wdw['hip_q'], 3).tolist()} "
                  f"knee tau cmd/rep {np.round(wdw['knee_tau_computed'], 1).tolist()}/{np.round(wdw['knee_tau_reported'], 1).tolist()} "
                  f"wheel tau {np.round(wdw['wheel_tau_computed'], 2).tolist()}")


if __name__ == '__main__':
    main()
