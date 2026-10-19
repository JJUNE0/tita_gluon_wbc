"""DESKTOP_DRY_RUN: response prediction audit of the original frozen F-2 A/B."""

import argparse
from collections import defaultdict
import csv
import json
from pathlib import Path
import sys

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

sys.path.insert(0, str(Path(__file__).resolve().parent))
from eval_flash_closed_loop_residual import fit_model, score

REPO = Path(__file__).resolve().parents[1]
ORIGINAL = REPO / 'docs/exp/2026-10-15/flash_torque_residual'
HORIZONS = [1, 5, 10, 25, 50, 100]
FLOOR = np.array([1e-7, 1e-5, 1e-7, 1e-5])


def write(path, value):
    path.write_text(json.dumps(value, indent=2, allow_nan=False) + '\n')


def rms(value):
    return np.sqrt(np.mean(np.asarray(value) ** 2, axis=0))


def error_metrics(prediction, actual, origin=None):
    error = prediction - actual
    signal = rms(actual)
    denominator = np.maximum(signal, FLOOR)
    result = dict(rmse=rms(error).tolist(), signal_rms=signal.tolist(),
        response_nrmse=(rms(error) / denominator).tolist(),
        response_skill=(1. - np.mean(error ** 2, axis=0) / denominator ** 2).tolist())
    if origin is not None:
        change = actual - origin
        result['change_rms'] = rms(change).tolist()
        result['change_nrmse'] = (rms(error) / np.maximum(rms(change), FLOOR)).tolist()
    else:
        change = actual
    predicted_change = prediction - origin if origin is not None else prediction
    valid = abs(change) > FLOOR
    result['direction_agreement'] = [float(np.mean(np.sign(predicted_change[valid[:, i], i]) ==
        np.sign(change[valid[:, i], i]))) if valid[:, i].any() else 1. for i in range(4)]
    result['direction_sample_counts'] = valid.sum(0).tolist()
    return result


def predictions(A, B, delta, u):
    one_step = delta[:-1] @ A.T + u[:, None] * B[:, 0]
    full = np.empty_like(delta)
    full[0] = delta[0]
    for i in range(len(u)):
        full[i + 1] = A @ full[i] + B[:, 0] * u[i]
    return one_step, full


def evaluate(A, B, delta, u):
    one, full = predictions(A, B, delta, u)
    outcome = dict(one_step=error_metrics(one, delta[1:], delta[:-1]),
        persistence=error_metrics(delta[:-1], delta[1:], delta[:-1]),
        omit_B=error_metrics(delta[:-1] @ A.T, delta[1:], delta[:-1]),
        full_from_start=error_metrics(full[1:], delta[1:]), horizons={})
    for h in HORIZONS:
        starts = np.arange(0, len(u) - h + 1, 5)
        if not len(starts):
            continue
        prediction = delta[starts].copy()
        for offset in range(h):
            prediction = prediction @ A.T + u[starts + offset, None] * B[:, 0]
        outcome['horizons'][str(h)] = error_metrics(prediction, delta[starts + h], delta[starts])
    return outcome


def median_metric(values, key):
    return np.median(np.asarray([v[key] for v in values]), axis=0).tolist()


def summarize(records):
    output = {}
    for source in ['sensor', 'gt']:
        groups = {}
        for key in ['one_step', 'persistence', 'omit_B', 'full_from_start']:
            values = [r[source][key] for r in records]
            groups[key] = {m: median_metric(values, m) for m in values[0]}
        groups['horizons'] = {}
        for h in HORIZONS:
            values = [r[source]['horizons'][str(h)] for r in records if str(h) in r[source]['horizons']]
            if values:
                groups['horizons'][str(h)] = {m: median_metric(values, m) for m in values[0]}
        output[source] = groups
    return output


def archive_audit(A, B):
    data = np.load(ORIGINAL / 'f2_closed/identification.npz')
    afit, bfit, diagnostics = fit_model(data['x'], data['y'], data['u'])
    np.testing.assert_allclose(afit, A, atol=1e-10, rtol=1e-10)
    np.testing.assert_allclose(bfit, B, atol=1e-10, rtol=1e-10)
    original_model = json.loads((ORIGINAL / 'f2_closed/model.json').read_text())
    heldout = score(A, B, data['heldout_x'], data['heldout_y'], data['heldout_u'])
    np.testing.assert_allclose(heldout['component_rms'], original_model['heldout_prediction']['component_rms'], atol=1e-14)
    baseline = { (r['seed'], r['pitch_delta_rad']): r for r in
        map(json.loads, (ORIGINAL / 'f1_nominal/results.jsonl').read_text().splitlines()) if r['label'] == 'A'}
    datasets = {}
    for name, filename in [('heldout_probes', 'probe_results.jsonl'), ('heldout_feedback', 'results.jsonl')]:
        xs, ys, us, gx, gy = [], [], [], [], []
        for row in map(json.loads, (ORIGINAL / 'f2_closed' / filename).read_text().splitlines()):
            if row['seed'] != 44 or (name == 'heldout_feedback' and row['alpha'] == 0):
                continue
            original = np.load(ORIGINAL / 'f1_nominal' / baseline[(row['seed'], row['pitch_delta_rad'])]['trace'])
            current = np.load(ORIGINAL / 'f2_closed' / row['trace'])
            delta = current['synchronized_state'] - original['synchronized_state']
            gt = current['gt_state'] - original['gt_state']
            # One scalar applied-total torque per t -> t+1 transition; no shift.
            u = (current['command_substeps'][1:, :, [3, 7]] - current['flash_substeps'][1:, :, [3, 7]]).sum(2).mean(1)
            t = current['time'][:-1]
            mask = (t >= 2.) & (t < 10.5) & ~((t >= 2.96) & (t <= 3.3))
            xs.append(delta[:-1][mask]); ys.append(delta[1:][mask]); us.append(u[mask])
            gx.append(gt[:-1][mask]); gy.append(gt[1:][mask])
        x, y, u = np.concatenate(xs), np.concatenate(ys), np.concatenate(us)
        truth_x, truth_y = np.concatenate(gx), np.concatenate(gy)
        entry = dict(samples=len(x))
        for source, a, b in [('sensor', x, y), ('gt', truth_x, truth_y)]:
            entry[source] = dict(model=error_metrics(a @ A.T + u[:, None] * B[:, 0], b, a),
                persistence=error_metrics(a, b, a), omit_B=error_metrics(a @ A.T, b, a))
        datasets[name] = entry
    return dict(execution_domain='DESKTOP_DRY_RUN', evidence_status='PASS', model_reproduced=True,
        original_heldout_score=heldout, datasets=datasets, diagnostics=diagnostics)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, required=True)
    args = parser.parse_args()
    root = args.root.resolve()
    model = json.loads((ORIGINAL / 'f2_closed/model.json').read_text())
    A, B = np.asarray(model['A_closed']), np.asarray(model['B_res'])
    write(root / 'archive_audit.json', archive_audit(A, B))
    records = []
    b_records = []
    integrity = []
    training = np.load(ORIGINAL / 'f2_closed/identification.npz')
    low, high = training['x'][:, 1:].min(0), training['x'][:, 1:].max(0)
    example = None
    for stage in ['primary', 'transfer']:
        for context in sorted((root / stage).glob('*/results.json')):
            info = json.loads(context.read_text())
            integrity.append(dict(context=info['job']['id'], exact_zero_replays=info['branch_zero_exact_replays']))
            b_records.extend(info['direct_B'])
            for row in info['responses']:
                directory = context.parent
                current, baseline = np.load(directory / row['trace']), np.load(directory / row['baseline'])
                u = current['actual_u'] - baseline['actual_u']
                assert len(u) + 1 == len(current['sensor'])
                np.testing.assert_array_equal(current['sensor'][0], baseline['sensor'][0])
                np.testing.assert_array_equal(current['gt'][0], baseline['gt'][0])
                entry = dict(stage=stage, **row)
                for source in ['sensor', 'gt']:
                    delta = current[source] - baseline[source]
                    entry[source] = evaluate(A, B, delta, u)
                    entry[source]['regressor_box_coverage'] = float(np.mean(np.all(
                        (delta[:, 1:] >= low) & (delta[:, 1:] <= high), axis=1)))
                records.append(entry)
                if stage == 'primary' and row['seed'] == 45 and row['pitch'] == 0. and row['start_s'] == 6. and row['family'] == 'prbs' and row['amplitude'] == .25:
                    example = (current, baseline, row)
    write(root / 'response_metrics.json', records)
    write(root / 'direct_B.json', b_records)
    summaries = {}
    for stage in ['primary', 'transfer']:
        subset = [r for r in records if r['stage'] == stage]
        result = summarize(subset)
        result['traces'] = len(subset)
        result['gate_nrmse_at_horizons'] = {str(h): result['sensor']['horizons'][str(h)]['response_nrmse'] for h in [5, 25, 50]}
        result['response_gate_pass_v_pitch'] = all(result['sensor']['horizons'][str(h)]['response_nrmse'][i] <= .3
            for h in [5, 25, 50] for i in [1, 2])
        result['direction_gate_pass_v_pitch'] = all(result['sensor']['horizons'][str(h)]['direction_agreement'][i] >= .9
            for h in [5, 25, 50] for i in [1, 2])
        result['families'] = {f: summarize([r for r in subset if r['family'] == f]) for f in sorted({r['family'] for r in subset})}
        result['amplitudes'] = {str(a): summarize([r for r in subset if r['amplitude'] == a])
            for a in sorted({r['amplitude'] for r in subset})}
        inside = [r for r in subset if r['sensor']['regressor_box_coverage'] >= .95]
        result['regressor_box_coverage_median'] = float(np.median([r['sensor']['regressor_box_coverage'] for r in subset]))
        result['mostly_in_training_box'] = dict(traces=len(inside), summary=summarize(inside)) if inside else None
        result['pooled_direction'] = {}
        for h in HORIZONS:
            values = [r['sensor']['horizons'][str(h)] for r in subset]
            counts = np.asarray([v['direction_sample_counts'] for v in values])
            directions = np.asarray([v['direction_agreement'] for v in values])
            result['pooled_direction'][str(h)] = (np.sum(counts * directions, 0) / np.maximum(counts.sum(0), 1)).tolist()
        b_subset = [r for r in b_records if r['actor'] == ('cached' if stage == 'primary' else 'sync')]
        result['direct_B'] = {}
        for source in ['sensor', 'gt']:
            values = np.asarray([r[source + '_B'] for r in b_subset])
            result['direct_B'][source] = dict(median=np.median(values, 0).tolist(),
                min=values.min(0).tolist(), max=values.max(0).tolist(),
                empirical_over_model=(np.median(values, 0) / B[:, 0]).tolist())
        summaries[stage] = result
    passed = summaries['primary']['response_gate_pass_v_pitch'] and summaries['primary']['direction_gate_pass_v_pitch']
    write(root / 'summary.json', dict(execution_domain='VALIDATION_SIM', evidence_status='PASS' if passed else 'FAIL',
        note='Status concerns prediction accuracy; runtime and trace integrity are recorded separately.',
        original_A=A.tolist(), original_B=B.tolist(), datasets=summaries))
    with (root / 'metrics.csv').open('w') as stream:
        columns = ['stage', 'context', 'family', 'amplitude', 'start_s', 'source', 'method',
                   'v_rmse', 'pitch_rmse', 'v_response_nrmse', 'pitch_response_nrmse']
        writer = csv.DictWriter(stream, fieldnames=columns); writer.writeheader()
        for r in records:
            for source in ['sensor', 'gt']:
                for method in ['one_step', 'persistence', 'omit_B', 'full_from_start']:
                    m = r[source][method]
                    writer.writerow(dict(stage=r['stage'], context=r['context'], family=r['family'],
                        amplitude=r['amplitude'], start_s=r['start_s'], source=source, method=method,
                        v_rmse=m['rmse'][1], pitch_rmse=m['rmse'][2],
                        v_response_nrmse=m['response_nrmse'][1], pitch_response_nrmse=m['response_nrmse'][2]))
    current, baseline, label = example
    delta = current['sensor'] - baseline['sensor']; truth = current['gt'] - baseline['gt']
    u = current['actual_u'] - baseline['actual_u']; one, full = predictions(A, B, delta, u)
    t = np.arange(len(delta)) * .02
    fig, axes = plt.subplots(3, 1, figsize=(11, 9), sharex=True)
    axes[0].step(t[:-1], u, where='post'); axes[0].set_ylabel('Actual total residual [Nm]')
    for ax, component, units in [(axes[1], 1, 'Delta velocity [m/s]'), (axes[2], 2, 'Delta pitch [rad]')]:
        ax.plot(t, delta[:, component], label='MuJoCo sensor-state response')
        ax.plot(t, truth[:, component], ':', label='MuJoCo GT response')
        ax.plot(t, full[:, component], '--', label='Frozen A/B free run from identical start')
        ax.set_ylabel(units); ax.legend(fontsize=8)
    for ax in axes: ax.grid(True)
    axes[-1].set_xlabel('Time since branch [s]')
    fig.suptitle('Unseen PRBS, seed45/pitch0, original actor, branch at6s')
    fig.tight_layout(); fig.savefig(root / 'response_example.png', dpi=150)
    fig, axes = plt.subplots(1, 2, figsize=(11, 4))
    values = [r for r in b_records if r['actor'] == 'cached']
    for ax, component, units in [(axes[0], 1, 'B velocity [(m/s)/Nm]'), (axes[1], 2, 'B pitch [rad/Nm]')]:
        for amp in [.01, .02, .04]:
            subset = [r['sensor_B'][component] for r in values if r['amplitude'] == amp]
            ax.scatter(np.full(len(subset), amp), subset, alpha=.5, label=f'{amp:g}Nm')
        ax.axhline(B[component, 0], color='red', label='Frozen identified B')
        empirical = np.median([r['sensor_B'][component] for r in values])
        ax.set_title(f'Model {B[component, 0]:.6g}; measured median {empirical:.6g}')
        ax.set_xlabel('One-step total torque amplitude [Nm]'); ax.set_ylabel(units); ax.grid(True); ax.legend(fontsize=8)
    fig.tight_layout(); fig.savefig(root / 'direct_B_comparison.png', dpi=150)
    write(root / 'analysis_integrity.json', dict(execution_domain='DESKTOP_DRY_RUN', evidence_status='PASS',
        branch_controls=integrity, traces=len(records), direct_B_tests=len(b_records),
        original_model_refit_reproduction=True, state_input_alignment='N+1 states,N inputs; u[k] drives x[k+1]'))
    for stage, result in summaries.items():
        print('[VALIDATION_SIM]', stage, result['traces'], 'traces; full-run NRMSE',
            result['sensor']['full_from_start']['response_nrmse'], 'B ratios', result['direct_B']['sensor']['empirical_over_model'])


if __name__ == '__main__':
    main()
