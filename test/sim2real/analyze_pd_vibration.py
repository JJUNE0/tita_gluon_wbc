"""DESKTOP_DRY_RUN: policy-update torque steps and PD chatter proxies in copied FlashSAC bags.

Reads ``TrainingSample`` + ``MotorFeedback`` read-only. Both are logged only on policy ticks (50 Hz),
so content above 25 Hz is aliased and an audible rattle is not resolved directly. Two properties of
the 500 Hz loop in ``tita_node.cpp`` (zero-order-hold targets, torque recomputed every 2 ms, no
action filter) still make each policy tick informative:

- ``MotorFeedback.previous_computed_torque`` is the last command under the old action (2 ms before
  the sample) and ``TrainingSample.computed_torque`` the first command under the new one. Their
  difference is the torque step injected at each policy update:
  ``Kp * d(target)`` (wheels: ``Kd * d(target velocity)``) plus a 2 ms state-change residual
  ``-Kp dq_2ms - Kd d(dq)_2ms``.
- Kd/Kp is the same for 60/1.5 and 92/2.3, so the residual divided by Kp is a kinematic quantity
  that can be compared across the two gain sets.

``computed`` torque is the controller command, not measured torque; ``reported`` is the SDK value.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sqlite3
from pathlib import Path

import numpy as np
from rclpy.serialization import deserialize_message
from scipy.signal import welch
from tita_controller.msg import MotorFeedback, TrainingSample

ROOT = Path(__file__).resolve().parents[2]
INTERFACE = ROOT / 'sim2real/tita_ws/src/tita_controller/policies/flashsac_80000/config.json'
JOINTS = ['joint_left_leg_1', 'joint_left_leg_2', 'joint_left_leg_3', 'joint_left_leg_4',
          'joint_right_leg_1', 'joint_right_leg_2', 'joint_right_leg_3', 'joint_right_leg_4']
GROUPS = {'hip': [0, 4], 'thigh': [1, 5], 'knee': [2, 6], 'wheel': [3, 7]}
LIMIT = np.array([60., 60., 60., 12., 60., 60., 60., 12.])
LOW_LOAD = np.array([2., 2., 2., .2, 2., 2., 2., .2])  # |tau| below this counts as low load [N m]
NEUTRAL = np.array([.02, .02, .03])
DECIMATION = 10
BANDS = [(0.3, 3.), (3., 8.), (8., 15.), (15., 25.)]


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def runs(mask: np.ndarray) -> list[tuple[int, int]]:
    edges = np.flatnonzero(np.diff(np.r_[0, mask.astype(int), 0]))
    return list(zip(edges[::2], edges[1::2]))


def rms(x: np.ndarray) -> float:
    x = x[np.isfinite(x)]
    return float(np.sqrt(np.mean(x ** 2))) if len(x) else float('nan')


def load(bag: Path, terms: list[dict]) -> dict:
    db = next(bag.resolve().glob('*.db3'))
    with sqlite3.connect(f'file:{db}?mode=ro', uri=True) as conn:
        assert conn.execute('PRAGMA quick_check').fetchone()[0] == 'ok'
        ids = dict(conn.execute('SELECT name,id FROM topics'))

        def rows(topic, cls):
            return [deserialize_message(b, cls) for b, in conn.execute(
                'SELECT data FROM messages WHERE topic_id=? ORDER BY timestamp', (ids[topic],))]
        samples = rows('/sim2real/training_sample', TrainingSample)
        feedback = {f.sequence_id: f for f in rows('/sim2real/motor_feedback', MotorFeedback)} \
            if '/sim2real/motor_feedback' in ids else {}
    get = lambda name: np.array([getattr(s, name) for s in samples])
    d = dict(db=str(db), db_sha256=digest(db), tick=get('control_tick').astype(np.int64),
             mono=get('monotonic_ns').astype(np.int64), state=get('state').astype(str),
             command=get('command'), action=get('action_raw').astype(float), tau=get('computed_torque'),
             q=get('joint_position'), dq=get('joint_velocity'), gyro=get('angular_velocity'),
             bias=get('wheel_velocity_bias'))
    assert np.all(np.diff(d['mono']) > 0)
    n = len(samples)
    d['tau_prev'] = np.full((n, 8), np.nan)
    d['reported'] = np.full((n, 8), np.nan)
    for i, s in enumerate(samples):
        f = feedback.get(s.sequence_id)
        if f is None:
            continue
        assert f.control_tick == s.control_tick and f.monotonic_ns == s.monotonic_ns
        if f.previous_torque_sent:
            d['tau_prev'][i] = f.previous_computed_torque
        if f.valid:
            d['reported'][i] = f.reported_torque
    # Native-order targets from the policy-order ONNX output (adapter.hpp: action * scale + offset).
    target = np.full((n, 8), np.nan)
    for i, term in enumerate(terms):
        j = JOINTS.index(term['joint'])
        target[:, j] = np.clip(d['action'][:, i] * term['scale'] + term['offset'], *term['clip'])
    d['target'] = target
    d['native_of_policy'] = [JOINTS.index(term['joint']) for term in terms]
    return d


def fit_gains(d: dict, rl: np.ndarray) -> dict:
    """Least-squares Kp/Kd per joint from the logged command (unclipped RL samples)."""
    out = {}
    for j in range(8):
        sel = rl & (np.abs(d['tau'][:, j]) < LIMIT[j] - 1e-6)
        y = d['tau'][sel, j]
        if j in (3, 7):
            x = (d['target'][sel, j] - d['dq'][sel, j])[:, None]
        else:
            x = np.c_[d['target'][sel, j] - d['q'][sel, j], -d['dq'][sel, j]]
        coef, *_ = np.linalg.lstsq(x, y, rcond=None)
        out[JOINTS[j]] = dict(kp=0. if j in (3, 7) else float(coef[0]), kd=float(coef[-1]),
                              residual_rms=rms(y - x @ coef), samples=int(sel.sum()))
    return out


def band_powers(x: np.ndarray, segments: list[tuple[int, int]], fs: float = 50.) -> dict:
    """Welch PSD averaged over contiguous segments of at least 128 samples (per column)."""
    psd, weight, freq = 0., 0, None
    for a, b in segments:
        if b - a < 128:
            continue
        freq, p = welch(x[a:b] - x[a:b].mean(0), fs=fs, nperseg=128, axis=0)
        psd, weight = psd + p * (b - a), weight + (b - a)
    if not weight:
        return {}
    psd = psd / weight
    df = freq[1] - freq[0]
    total = psd[freq >= BANDS[0][0]].sum(0) * df
    bands = {f'{lo:g}-{hi:g}Hz': (psd[(freq >= lo) & (freq < hi)].sum(0) * df).tolist() for lo, hi in BANDS}
    above = freq >= 1.
    peak = freq[above][np.argmax(psd[above], axis=0)]
    return dict(power=total.tolist(), bands=bands, peak_hz_above_1=np.atleast_1d(peak).tolist())


def analyze(label: str, bag: Path, terms: list[dict], settle: float) -> dict:
    d = load(bag, terms)
    t = (d['mono'] - d['mono'][0]) * 1e-9
    rl = d['state'] == 'rl'
    assert np.max(np.abs(d['bias'][rl])) == 0, 'velocity bias active; this review assumes bias OFF'
    gains = fit_gains(d, rl)
    kp = np.array([gains[n]['kp'] for n in JOINTS])
    kd = np.array([gains[n]['kd'] for n in JOINTS])

    # Phase of each RL sample: startup (< 3 s after entry), neutral hold, moving.
    age = np.zeros(len(t))
    neutral_age = np.zeros(len(t))
    neutral = np.all(np.abs(d['command']) <= NEUTRAL, axis=1)
    entries = []
    for a, b in runs(rl):
        entries.append(a)
        age[a:b] = t[a:b] - t[a]
        for i in range(a + 1, b):
            neutral_age[i] = neutral_age[i - 1] + (t[i] - t[i - 1]) if neutral[i] and neutral[i - 1] else 0.
    phases = {
        'rl_all': rl,
        'startup_0to3s': rl & (age < 3.),
        'neutral_hold': rl & (age >= 3.) & neutral & (neutral_age >= settle),
        'moving': rl & (age >= 3.) & ~neutral,
    }
    # Consecutive policy ticks inside RL: tau_prev[k] was computed with action[k-1].
    pair = np.zeros(len(t), bool)
    pair[1:] = rl[1:] & rl[:-1] & (np.diff(d['tick']) == DECIMATION) & np.isfinite(d['tau_prev'][1:, 0])
    unclipped = (np.abs(d['tau']) < LIMIT - 1e-6) & (np.abs(d['tau_prev']) < LIMIT - 1e-6)
    d_target = np.full_like(d['target'], np.nan)
    d_target[1:] = d['target'][1:] - d['target'][:-1]
    feedforward = np.where(kp > 0, kp * d_target, kd * d_target)  # torque step from the target change
    step = d['tau'] - d['tau_prev']
    residual = step - feedforward  # -Kp dq_2ms - Kd d(dq)_2ms when unclipped
    within = np.full_like(step, np.nan)
    within[1:] = d['tau_prev'][1:] - d['tau'][:-1]  # 18 ms change under a constant target
    d_action = np.full_like(d['action'], np.nan)
    d_action[1:] = d['action'][1:] - d['action'][:-1]
    d_action_native = np.full_like(d_action, np.nan)
    d_action_native[:, d['native_of_policy']] = d_action
    reversal = (np.sign(d['tau']) != np.sign(d['tau_prev'])) & (np.abs(d['tau']) > .05) & (np.abs(d['tau_prev']) > .05)
    dq_step = np.full_like(d['dq'], np.nan)
    dq_step[1:] = d['dq'][1:] - d['dq'][:-1]

    result = dict(label=label, bag_db3=d['db'], bag_db3_sha256=d['db_sha256'], fitted_gains=gains,
                  rl_entries_s=[float(t[a]) for a in entries], phases={})
    for name, mask in phases.items():
        p = mask & pair
        ok = p[:, None] & unclipped
        per_joint = {}
        for j, joint in enumerate(JOINTS):
            sel = ok[:, j]
            per_joint[joint] = dict(
                pairs=int(sel.sum()),
                d_action_rms=rms(d_action_native[p, j]),
                feedforward_step_rms=rms(feedforward[sel, j]),
                feedforward_step_p99=float(np.percentile(np.abs(feedforward[sel, j]), 99)) if sel.any() else None,
                update_step_rms=rms(step[sel, j]),
                residual_2ms_rms=rms(residual[sel, j]),
                residual_2ms_over_kp_rms=rms(residual[sel, j] / kp[j]) if kp[j] > 0 else None,
                within_18ms_rms=rms(within[sel, j]),
                tau_mean=float(np.mean(d['tau'][mask, j])) if mask.any() else None,
                tau_std=float(np.std(d['tau'][mask, j])) if mask.any() else None,
                low_load_fraction=float(np.mean(np.abs(d['tau'][mask, j]) < LOW_LOAD[j])) if mask.any() else None,
                reversal_at_update_fraction=float(np.mean(reversal[p, j])) if p.any() else None,
                sign_changes_per_s=float(np.sum(np.diff(np.sign(d['tau'][mask, j])) != 0) / (mask.sum() * .02))
                if mask.sum() > 1 else None,
                clip_fraction=float(np.mean(np.abs(d['tau'][mask, j]) >= LIMIT[j] - 1e-6)) if mask.any() else None,
                dq_rms=rms(d['dq'][mask, j]),
                dq_step_rms=rms(dq_step[p, j]),
                reported_minus_previous_rms=rms(d['reported'][p, j] - d['tau_prev'][p, j]),
            )
        segs = [(a, b) for a, b in runs(mask)]
        result['phases'][name] = dict(
            samples=int(mask.sum()), pairs=int(p.sum()), seconds=float(mask.sum() * .02), joints=per_joint,
            gyro_rms=[rms(d['gyro'][mask, i]) for i in range(3)],
            gyro_step_rms=[rms(np.diff(d['gyro'][:, i])[p[1:]]) for i in range(3)],
            psd_action=band_powers(d['action'], segs), psd_torque=band_powers(d['tau'], segs),
            psd_dq=band_powers(d['dq'], segs), psd_gyro=band_powers(d['gyro'], segs))
    # RL entry handoff (sit controller -> policy) and clipping near entry.
    result['entry'] = []
    for a in entries:
        w = slice(a, min(a + 50, len(t)))
        result['entry'].append(dict(
            t_s=float(t[a]),
            first_step=(d['tau'][a] - d['tau_prev'][a]).tolist(),
            leg_clip_samples_first_1s=int(np.sum(np.abs(d['tau'][w][:, [0, 1, 2, 4, 5, 6]]) >= 60. - 1e-6)),
            wheel_clip_samples_first_1s=int(np.sum(np.abs(d['tau'][w][:, [3, 7]]) >= 12. - 1e-6)),
            max_abs_tau_first_1s=np.max(np.abs(d['tau'][w]), axis=0).tolist()))
    series = dict(t=t, rl=rl, state=d['state'], step=step, feedforward=feedforward, residual=residual,
                  within=within, tau=d['tau'], tau_prev=d['tau_prev'], reported=d['reported'], action=d['action'],
                  dq=d['dq'], q=d['q'], gyro=d['gyro'], command=d['command'], neutral_hold=phases['neutral_hold'],
                  moving=phases['moving'], startup=phases['startup_0to3s'])
    return result, series


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--run', action='append', required=True, metavar='LABEL=BAG_DIR')
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--interface', type=Path, default=INTERFACE, help='bundle config.json with action terms')
    parser.add_argument('--settle', type=float, default=1.0)
    args = parser.parse_args()
    out = args.output.resolve()
    assert out.is_relative_to(ROOT / 'docs/exp')
    out.mkdir(parents=True, exist_ok=True)
    config = json.loads(args.interface.read_text())
    terms = config['policy_interface']['actions']
    report = dict(execution_domain='DESKTOP_DRY_RUN', interface=str(args.interface),
                  interface_sha256=digest(args.interface), runs=[])
    arrays = {}
    for spec in args.run:
        label, bag = spec.split('=', 1)
        result, series = analyze(label, Path(bag), terms, args.settle)
        report['runs'].append(result)
        arrays.update({f'{label}__{k}': v for k, v in series.items()})
    (out / 'pd_vibration.json').write_text(json.dumps(report, indent=2) + '\n')
    np.savez_compressed(out / 'pd_vibration_series.npz', **arrays)

    print('[DESKTOP_DRY_RUN] fitted leg/wheel gains (Kp, Kd) per run:')
    for r in report['runs']:
        g = r['fitted_gains']
        print(f"  {r['label']}: " + ', '.join(f"{n[6:]} {g[n]['kp']:.2f}/{g[n]['kd']:.3f}" for n in JOINTS))
    for phase in ('neutral_hold', 'moving', 'startup_0to3s'):
        print(f'\n== {phase}')
        for r in report['runs']:
            ph = r['phases'][phase]
            print(f"  {r['label']}: {ph['seconds']:.1f} s, gyro step rms {np.round(ph['gyro_step_rms'], 3).tolist()}")
            for group, idx in GROUPS.items():
                vals = [ph['joints'][JOINTS[j]] for j in idx]
                fmt = lambda key, nd=2: '/'.join('nan' if v[key] is None else f'{v[key]:.{nd}f}' for v in vals)
                print(f"    {group:5s} da {fmt('d_action_rms', 3)} ff {fmt('feedforward_step_rms')} "
                      f"p99 {fmt('feedforward_step_p99')} step {fmt('update_step_rms')} r2ms {fmt('residual_2ms_rms')} "
                      f"r/kp {fmt('residual_2ms_over_kp_rms', 4)} 18ms {fmt('within_18ms_rms')} "
                      f"tau {fmt('tau_mean', 1)}+-{fmt('tau_std', 1)} low {fmt('low_load_fraction')} "
                      f"rev {fmt('reversal_at_update_fraction')} sgn/s {fmt('sign_changes_per_s', 1)} "
                      f"clip {fmt('clip_fraction', 3)} dqstep {fmt('dq_step_rms', 3)} rep-prev {fmt('reported_minus_previous_rms')}")
    print('\n== RL entry')
    for r in report['runs']:
        for e in r['entry']:
            print(f"  {r['label']} @ {e['t_s']:.1f} s: first step {np.round(e['first_step'], 1).tolist()}, "
                  f"clip leg/wheel {e['leg_clip_samples_first_1s']}/{e['wheel_clip_samples_first_1s']}, "
                  f"max|tau| 1 s {np.round(e['max_abs_tau_first_1s'], 1).tolist()}")


if __name__ == '__main__':
    main()
