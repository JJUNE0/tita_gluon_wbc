"""DESKTOP_DRY_RUN: decode an existing candump log; no socket or robot access.

Uses the public packed API structs. Returned torque is firmware telemetry,
not independent force measurement. Idle data cannot identify actuator gain.
"""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import struct

import numpy as np

REPO = Path(__file__).resolve().parents[2]


def summary(a):
    return dict(mean=np.mean(a, axis=0).tolist(), std=np.std(a, axis=0).tolist(),
                min=np.min(a, axis=0).tolist(), max=np.max(a, axis=0).tolist())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--capture', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--history', type=Path, help='Previously recorded command/feedback column projection')
    args = parser.parse_args()
    assert args.output.resolve().is_relative_to(REPO / 'docs/exp')
    args.output.mkdir(parents=True, exist_ok=True)
    frames = []
    for line in args.capture.read_text().splitlines():
        m = re.fullmatch(r'\(([^)]+)\) (\S+) ([0-9A-F]+)##([0-9A-F])([0-9A-F]*)', line)
        if m is None:
            raise ValueError(f'Unexpected candump line: {line[:80]}')
        frames.append((float(m[1]), int(m[3], 16), bytes.fromhex(m[5])))
    assert frames and all(b[0] >= a[0] for a, b in zip(frames, frames[1:]))
    duration = frames[-1][0] - frames[0][0]
    assert duration > 0.
    report = dict(execution_domain='DESKTOP_DRY_RUN', evidence_status='PASS',
        checkpoint_sha256='381e846e3ffb1d5a9ed629c02b55c9740ec3c5b089ca443f38b3d73b6abbd730',
        note='Installed policy provenance only; FlashSAC was not running during capture.',
        capture_sha256=hashlib.sha256(args.capture.read_bytes()).hexdigest(),
        frames=len(frames), duration_s=duration,
        frame_counts={hex(k): v for k, v in sorted(Counter(r[1] for r in frames).items())},
        motor_feedback={}, sdk_commands={}, unknown_zero_frames={}, imu={},
        limitations=['No torque was requested by this audit.',
                     'Idle feedback near zero does not identify output gain or current limit.',
                     'Firmware telemetry torque may be estimated and share its conversion with command.',
                     'Motor temperature/current/gear ratio/Kt are not in the decoded public motor struct.'])
    arrays = {}
    for side, cid in [('left', 0x108), ('right', 0x109)]:
        selected = [r for r in frames if r[1] == cid]
        assert selected and all(len(r[2]) == 64 for r in selected)
        values = np.asarray([[struct.unpack_from('<Ifff', r[2], i*16) for i in range(4)]
                             for r in selected])
        assert np.isfinite(values).all()
        # Timestamp is supplied per motor; q/dq/torque are the following floats.
        report['motor_feedback'][side] = dict(frames=len(values),
            hz=(len(values)-1)/(selected[-1][0]-selected[0][0]),
            position_rad=summary(values[:, :, 1]), velocity_rad_s=summary(values[:, :, 2]),
            reported_torque_nm=summary(values[:, :, 3]))
        arrays[side] = values
        arrays[side+'_receive_time'] = np.array([r[0] for r in selected])
    for cid in range(0x120, 0x124):
        selected = [r for r in frames if r[1] == cid]
        report['sdk_commands'][hex(cid)] = dict(frames=len(selected))
        if selected:
            assert all(len(r[2]) == 48 for r in selected)
            a = np.asarray([[struct.unpack_from('<Ifffff', r[2], i*24) for i in range(2)]
                            for r in selected])
            assert np.isfinite(a).all()
            report['sdk_commands'][hex(cid)]['commanded_torque_nm'] = summary(a[:, :, 5])
            arrays[hex(cid)] = a
    for cid in range(0x110, 0x114):
        selected = [r for r in frames if r[1] == cid]
        if selected:
            report['unknown_zero_frames'][hex(cid)] = dict(frames=len(selected),
                all_payload_bytes_zero=all(not any(r[2]) for r in selected),
                note='Different CAN-ID family; no nonzero-payload field semantics assumed.')
    imu = [r for r in frames if r[1] == 0x118]
    assert imu and all(len(r[2]) == 48 for r in imu)
    values = np.asarray([struct.unpack('<I11f', r[2]) for r in imu])
    assert np.isfinite(values).all()
    x, y, z, w = values[:, 7:11].T
    norm = np.sqrt(x*x+y*y+z*z+w*w)
    assert abs(norm-1.).max() < .01
    pitch = np.degrees(np.arcsin(np.clip(2*(w*y-z*x), -1., 1.)))
    report['imu'] = dict(frames=len(imu), pitch_deg=summary(pitch),
                         note='No external level reference; not an IMU calibration measurement.')
    if args.history:
        history = json.loads(args.history.read_text())
        a = np.asarray(history['rows'], dtype=float)
        assert np.isfinite(a).all()
        columns = {k: i for i, k in enumerate(history['columns'])}
        t = (a[:, columns['monotonic_ns']] - a[0, columns['monotonic_ns']])*1e-9
        assert (np.diff(t) > 0).all()
        valid = (a[:, columns['written']] > .5) & (a[:, columns['read_valid']] > .5)
        hist = dict(source=history['source'], source_sha256=history['source_sha256'],
            source_bytes=history['source_bytes'], rows=len(a), duration_s=float(t[-1]),
            session_filename_epoch=1784091897, median_dt_s=float(np.median(np.diff(t))),
            selection='written/read_valid; |command|>3 Nm; command range<0.5 Nm over centered 11 samples',
            interpretation='Historical firmware feedback only, not calibrated physical torque; not a current FlashSAC run.',
            joints=[])
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        fig, axes = plt.subplots(2, 3, figsize=(12, 7), constrained_layout=True)
        for axis, j in zip(axes.flat, [0, 1, 2, 4, 5, 6]):
            x = a[:, columns[f'final_torque{j}']]
            y = a[:, columns[f'measured_effort{j}']]
            windows = np.lib.stride_tricks.sliding_window_view(x, 11)
            stable = np.zeros(len(x), dtype=bool)
            stable[5:-5] = np.ptp(windows, axis=1) < .5
            mask = valid & stable & (abs(x) > 3.)
            assert mask.sum() > 100
            gain = float(x[mask] @ y[mask] / (x[mask] @ x[mask]))
            hist['joints'].append(dict(native_joint=j, samples=int(mask.sum()),
                feedback_command_gain=gain, median_ratio=float(np.median(y[mask]/x[mask])),
                rms_difference_nm=float(np.sqrt(np.mean((x[mask]-y[mask])**2)))))
            selected = np.flatnonzero(mask)[::max(1, int(mask.sum())//1500)]
            axis.scatter(x[selected], y[selected], s=3, alpha=.25)
            limits = [float(x[mask].min()), float(x[mask].max())]
            axis.plot(limits, limits, 'k--', lw=1, label='feedback = command')
            axis.plot(limits, np.array(limits)*.6, 'r:', lw=1, label='feedback = 0.6 command')
            axis.set(title=f'Joint {j}: ratio {gain:.3f}', xlabel='Command (Nm)', ylabel='Firmware feedback (Nm)')
            axis.grid(alpha=.2)
        axes[0, 0].legend(fontsize=7)
        fig.suptitle('Historical session (2026-07-15); slow command segments; not physical torque calibration')
        fig.savefig(args.output / 'historical_torque_tracking.png', dpi=150)
        plt.close(fig)
        report['historical_feedback'] = hist
    np.savez_compressed(args.output / 'motor_feedback.npz', **arrays)
    (args.output / 'passive_metrics.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
