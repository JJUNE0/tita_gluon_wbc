"""DESKTOP_DRY_RUN: posture audit of existing VALIDATION_SIM recordings only."""

import hashlib
import json
from pathlib import Path

import numpy as np

REPO = Path(__file__).resolve().parents[1]
SOURCE = REPO / 'docs/exp/2026-10-17/velocity_bias_grid_video'
OUTPUT = REPO / 'docs/exp/2026-10-17/velocity_bias_sim_real_posture_review'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    plan = json.loads((SOURCE / 'plan.json').read_text())
    rows, hashes = [], {}
    for condition in plan['conditions']:
        pair = []
        for group in range(2):
            root = SOURCE / condition['name']
            config_path = root / 'config.json'
            config = json.loads(config_path.read_text())
            wheel_kd = np.asarray(config['robot']['joint_kd'])[[3, 7]]
            np.testing.assert_array_equal(wheel_kd, [.5, .5])
            hashes[str(config_path.relative_to(REPO))] = digest(config_path)
            path = root / f'group_{group}.npz'
            hashes[str(path.relative_to(REPO))] = digest(path)
            status = json.loads((root / f'group_{group}_status.json').read_text())
            assert status['evidence_status'] == 'PASS' and status['duration_s'] == 300
            with np.load(path) as trace:
                state, bias = trace['state'], trace['velocity_bias']
                assert state.shape == (15001, 9) and len(bias) == len(state)
                assert np.isfinite(state).all() and np.isfinite(bias).all()
                time = np.arange(len(state)) * .02
                tail = time >= 280
                pitch = np.degrees(state[:, 5])
                row = dict(condition=condition['name'], mode='velocity_bias' if group else 'baseline',
                    tail_window_s=[280, 300], tail_mean_pitch_deg=float(pitch[tail].mean()),
                    tail_demeaned_pitch_rms_deg=float(pitch[tail].std()),
                    post_2s_peak_abs_pitch_deg=float(abs(pitch[time >= 2]).max()),
                    tail_mean_bias_m_s=float(bias[tail].mean()),
                    # Policy-specific preclip PD increment magnitude; not calibrated motor torque.
                    tail_mean_added_torque_magnitude_per_wheel_nm=float(abs(bias[tail]).mean() * wheel_kd.mean() / .0925),
                    max_drift_m=status['max_drift_m'], checkpoint_sha256=status['checkpoint_sha256'],
                    onnx_sha256=status['onnx_sha256'])
                pair.append(row)
        shift = pair[1]['tail_mean_pitch_deg'] - pair[0]['tail_mean_pitch_deg']
        for row in pair:
            row['paired_mean_pitch_shift_deg'] = shift
        rows.extend(pair)
    assert len({row['checkpoint_sha256'] for row in rows}) == 1
    for relative, before in hashes.items():
        assert digest(REPO / relative) == before
    OUTPUT.mkdir(parents=True, exist_ok=True)
    result = dict(execution_domain='DESKTOP_DRY_RUN', source_domain='VALIDATION_SIM', evidence_status='PASS',
                  source_hashes=hashes, source_hashes_unchanged=True, dt_s=.02, rows=rows,
                  torque_note='Kd=0.5, radius=0.0925; magnitude before effort clip, not measured torque')
    (OUTPUT / 'metrics.json').write_text(json.dumps(result, indent=2, allow_nan=False) + '\n')
    print('DESKTOP_DRY_RUN: source integrity / shapes / finite values PASS; no simulation or hardware run')
    for row in rows:
        print(f"{row['condition']:24} {row['mode']:13} "
              f"pitch={row['tail_mean_pitch_deg']:+.4f}deg "
              f"pitch_rms={row['tail_demeaned_pitch_rms_deg']:.5f}deg "
              f"bias={row['tail_mean_bias_m_s']:+.5f}m/s "
              f"added_magnitude={row['tail_mean_added_torque_magnitude_per_wheel_nm']:.4f}Nm")


if __name__ == '__main__':
    main()
