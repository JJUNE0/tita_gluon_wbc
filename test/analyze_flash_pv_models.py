"""DESKTOP_DRY_RUN: train-only M1/M2 fitting and held-out p/v response validation."""

import argparse
import csv
import hashlib
import json
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

FLOOR = np.array([1e-7, 1e-5])
HORIZONS = [5, 25, 50, 100]


def write(path, value):
    path.write_text(json.dumps(value, indent=2, allow_nan=False)+'\n')


def rms(value):
    return np.sqrt(np.mean(np.asarray(value)**2, axis=0))


def fit_model(x, y, u, dimension):
    x, y = x[:, :dimension], y[:, :dimension]
    target = y.copy()
    target[:, 0] -= x[:, 0]
    z = np.column_stack([x[:, 1:], u])
    scale = rms(z)
    if np.any(scale < 1e-12):
        raise ValueError('Unexcited regressor')
    coefficients, _, rank, singular = np.linalg.lstsq(z/scale, target, rcond=1e-10)
    if rank != dimension:
        raise ValueError('Rank deficient design')
    values = (coefficients/scale[:, None]).T
    A = np.zeros((dimension, dimension))
    A[0, 0] = 1.
    A[:, 1:] = values[:, :-1]
    B = values[:, -1]
    ru = u-x[:, 1:] @ np.linalg.lstsq(x[:, 1:], u, rcond=None)[0]
    return dict(A=A.tolist(), B=B.tolist(), dimension=dimension,
        states=['p', 'v', 'pitch', 'pitch_rate'][:dimension],
        training_samples=len(u), rank=int(rank), rms_scaled_condition=float(singular[0]/singular[-1]),
        remaining_input_energy=float(ru@ru/(u@u)),
        training_one_step_pv_rmse=rms((x@A.T+u[:, None]*B-y)[:, :2]).tolist(),
        position_translation_symmetry=True)


def free_run(A, B, initial, inputs):
    result = np.empty((len(inputs)+1, len(initial)))
    result[0] = initial
    for i, u in enumerate(inputs):
        result[i+1] = A@result[i]+B*u
    return result


def errors(predicted, actual):
    error = rms(predicted[:, :2]-actual[:, :2])
    signal = rms(actual[:, :2])
    return dict(rmse=error.tolist(), signal_rms=signal.tolist(),
        nrmse=(error/np.maximum(signal, FLOOR)).tolist(), below_floor=(signal<FLOOR).tolist())


def evaluate(model, delta, inputs):
    A, B = np.asarray(model['A']), np.asarray(model['B'])
    x = delta[:, :len(B)]
    predicted = free_run(A, B, x[0], inputs)
    result = dict(one_step=errors(x[:-1]@A.T+inputs[:, None]*B, x[1:]),
        persistence=errors(x[:-1], x[1:]),
        one_step_change_rms=rms((x[1:]-x[:-1])[:, :2]).tolist(),
        full2s=errors(predicted[1:], x[1:]), horizons={})
    for h in HORIZONS:
        starts = np.arange(0, len(inputs)-h+1, 5)
        pred = x[starts].copy()
        for step in range(h):
            pred = pred@A.T+inputs[starts+step, None]*B
        result['horizons'][str(h)] = errors(pred, x[starts+h])
    return result, predicted


def load_responses(root, split):
    result, direct, contexts = [], [], []
    for path in sorted(root.glob(f'{split}_*/results.json')):
        info = json.loads(path.read_text())
        assert info['job']['split'] == split and info['evidence_status'] == 'PASS'
        contexts.append(dict(id=info['job']['id'], seed=info['job']['seed'], pitch=info['job']['pitch'],
            zero_replays=len(info['exact_zero_replay_ticks']), startup_violations=info['startup_violations']))
        direct.extend(info['direct_B'])
        for row in info['responses']:
            with np.load(path.parent/row['trace']) as current, np.load(path.parent/row['baseline']) as baseline:
                actual = current['actual_u']-baseline['actual_u']
                assert len(actual)+1 == len(current['sensor']) == 101
                np.testing.assert_array_equal(current['sensor'][0], baseline['sensor'][0])
                result.append(dict(context=info['job']['id'], **row, inputs=actual,
                    sensor=current['sensor']-baseline['sensor'], gt=current['gt']-baseline['gt']))
    return result, direct, contexts


def median_metric(records, method):
    values = [r[method] for r in records]
    return {key: np.median([v[key] for v in values], axis=0).tolist()
            for key in ['rmse', 'signal_rms', 'nrmse']}


def summarize(records):
    result = {key: median_metric(records, key) for key in ['one_step', 'persistence', 'full2s']}
    result['horizons'] = {str(h): {k: np.median([r['horizons'][str(h)][k] for r in records], axis=0).tolist()
        for k in ['rmse', 'signal_rms', 'nrmse']} for h in HORIZONS}
    result['below_floor_traces_full2s'] = np.sum([r['full2s']['below_floor'] for r in records], axis=0).tolist()
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, required=True)
    args = parser.parse_args()
    root = args.root.resolve()
    manifest = json.loads((root/'manifest.json').read_text())
    train, train_b, train_contexts = load_responses(root, 'train')
    assert len(train) == 108
    x = np.concatenate([r['sensor'][:-1] for r in train])
    y = np.concatenate([r['sensor'][1:] for r in train])
    u = np.concatenate([r['inputs'] for r in train])
    models = {name: fit_model(x, y, u, dim) for name, dim in [('M1', 2), ('M2', 4)]}
    # Freeze matrices before opening held-out response arrays. No validation tuning.
    model_path = root/'models.json'
    if model_path.exists():
        raise RuntimeError('Models already frozen; use a new evidence directory for another analysis')
    write(model_path, dict(execution_domain='DESKTOP_DRY_RUN', evidence_status='NOT_TESTED',
        checkpoint_sha256=manifest['checkpoint_sha256'], models=models, training_contexts=train_contexts,
        script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        LQR_gain_designed=False, uses_validation=False))
    frozen_hash = hashlib.sha256(model_path.read_bytes()).hexdigest()
    np.savez_compressed(root/'training_data.npz', x=x, y=y, u=u)
    validation, val_b, val_contexts = load_responses(root, 'validation')
    assert len(validation) == 324
    assert not ({c['seed'] for c in train_contexts} & {c['seed'] for c in val_contexts})
    direct = np.median([r['sensor_B'] for r in val_b], axis=0)
    summary, records, pulse_records = {}, [], []
    for name, model in models.items():
        selected = []
        for row in validation:
            entry = {key: row[key] for key in ['context', 'family', 'amplitude', 'start_rl_s', 'input_seed']}
            entry['model'] = name
            for source in ['sensor', 'gt']:
                stats, _ = evaluate(model, row[source], row['inputs'])
                entry[source] = stats
            records.append(entry); selected.append(entry)
            if row['family'].startswith('pulse'):
                start = int(np.flatnonzero(abs(row['inputs'])>1e-7)[-1]+1)
                assert max(abs(row['inputs'][start:])) <= 1e-7
                A, B = np.asarray(model['A']), np.asarray(model['B'])
                actual = row['sensor'][start:, :len(B)]
                pred = free_run(A, B, actual[0], np.zeros(len(actual)-1))
                pulse_records.append(dict(model=name, context=row['context'], family=row['family'],
                    amplitude=row['amplitude'], start_rl_s=row['start_rl_s'],
                    zero_start_s=start*.02, metrics=errors(pred[1:], actual[1:])))
        stats = {source: summarize([r[source] for r in selected]) for source in ['sensor', 'gt']}
        stats['families'] = {family: summarize([r['sensor'] for r in selected if r['family'] == family])
            for family in sorted({r['family'] for r in selected})}
        stats['amplitudes'] = {str(amp): summarize([r['sensor'] for r in selected if r['amplitude'] == amp])
            for amp in [.1, .25, .5]}
        pulse = [r['metrics'] for r in pulse_records if r['model'] == name]
        stats['pulse_zero_input'] = {k: np.median([v[k] for v in pulse], axis=0).tolist()
            for k in ['rmse', 'signal_rms', 'nrmse']}
        relative_b = abs(np.asarray(model['B'])[:2]-direct[:2])/np.maximum(abs(direct[:2]), FLOOR)
        gate_prediction = all(value <= .3 for h in [5, 25, 50]
            for value in stats['sensor']['horizons'][str(h)]['nrmse']) and all(v <= .3 for v in stats['sensor']['full2s']['nrmse'])
        stats['direct_B_relative_error_pv'] = relative_b.tolist()
        stats['gate_prediction_pv'] = gate_prediction
        stats['gate_direct_B_velocity'] = bool(relative_b[1] <= .3)
        stats['gate_pass'] = gate_prediction and stats['gate_direct_B_velocity']
        summary[name] = stats
    write(root/'response_metrics.json', records)
    write(root/'pulse_metrics.json', pulse_records)
    write(root/'direct_B_summary.json', dict(train_median=np.median([r['sensor_B'] for r in train_b], axis=0).tolist(),
        validation_sensor_median=direct.tolist(), validation_gt_median=np.median([r['gt_B'] for r in val_b], axis=0).tolist(),
        validation_sensor_min=np.min([r['sensor_B'] for r in val_b], axis=0).tolist(),
        validation_sensor_max=np.max([r['sensor_B'] for r in val_b], axis=0).tolist(), train_pairs=len(train_b), validation_pairs=len(val_b)))
    verdict = 'M1 sufficient under recorded diagnostic gates' if summary['M1']['gate_pass'] else (
        'M2 sufficient; M1 insufficient' if summary['M2']['gate_pass'] else 'Both insufficient; no LQR design justified by these data')
    write(root/'summary.json', dict(execution_domain='VALIDATION_SIM',
        evidence_status='PASS' if any(v['gate_pass'] for v in summary.values()) else 'FAIL',
        verdict=verdict, models=summary, train_traces=len(train), validation_traces=len(validation),
        train_transitions=len(u), validation_transitions=sum(len(r['inputs']) for r in validation),
        validation_contexts=val_contexts, model_sha256=frozen_hash,
        interpretation='Status concerns p/v prediction, not runtime integrity or closed-loop control performance.'))
    with (root/'metrics.csv').open('w') as stream:
        writer = csv.writer(stream)
        writer.writerow(['model', 'context', 'family', 'amplitude', 'source', 'method', 'p_rmse', 'v_rmse', 'p_nrmse', 'v_nrmse'])
        for row in records:
            for source in ['sensor', 'gt']:
                for method in ['one_step', 'persistence', 'full2s']:
                    m = row[source][method]
                    writer.writerow([row['model'], row['context'], row['family'], row['amplitude'], source,
                        method, *m['rmse'], *m['nrmse']])
    for source in ['sensor', 'gt']:
        fig, axes = plt.subplots(1, 2, figsize=(10, 4))
        for name in models:
            for i, ax in enumerate(axes):
                ax.plot(np.array(HORIZONS)*.02,
                    [summary[name][source]['horizons'][str(h)]['nrmse'][i]*100 for h in HORIZONS], 'o-', label=name)
        for ax, variable in zip(axes, ['p', 'v']):
            ax.axhline(30, color='grey', linestyle=':', label='Recorded30% gate')
            ax.set_title(f'{source}: {variable} response prediction'); ax.set_ylabel('Median trace NRMSE [%]')
            ax.set_xlabel('Free prediction horizon [s]'); ax.legend(); ax.grid(True)
        fig.tight_layout(); fig.savefig(root/f'horizons_{source}.png', dpi=160); plt.close(fig)
    for family in ['validation_prbs', 'pulse_pos']:
        row = next(r for r in validation if r['context']=='validation_s82_p+0.000' and r['start_rl_s']==6. and r['amplitude']==.25 and r['family']==family)
        fig, axes = plt.subplots(3, 1, figsize=(10, 8), sharex=True)
        t = np.arange(101)*.02
        axes[0].step(t[:-1], row['inputs'], where='post'); axes[0].set_ylabel('Total residual [Nm]')
        for i, ax in enumerate(axes[1:]):
            ax.plot(t, row['sensor'][:, i], label='MuJoCo measured response')
            ax.plot(t, row['gt'][:, i], ':', label='GT response')
            for name, model in models.items():
                _, prediction = evaluate(model, row['sensor'], row['inputs'])
                ax.plot(t, prediction[:, i], '--', label=name)
            ax.set_ylabel(['Delta p [m]', 'Delta v [m/s]'][i]); ax.legend(fontsize=8)
        for ax in axes: ax.grid(True)
        axes[-1].set_xlabel('Time since full-state branch [s]')
        fig.suptitle(f'model_60000 sync actor, seed82/pitch0, RL6s, {family}, 0.25Nm')
        fig.tight_layout(); fig.savefig(root/f'response_{family}.png', dpi=160); plt.close(fig)
    assert hashlib.sha256(model_path.read_bytes()).hexdigest() == frozen_hash
    write(root/'analysis_integrity.json', dict(execution_domain='DESKTOP_DRY_RUN', evidence_status='PASS',
        same_train_data_for_both=True, distinct_train_validation_seeds=True, models_frozen_before_validation=True,
        frozen_models_preserved=True, validation_responses=len(validation), LQR_implemented=False,
        primary_metrics='p/v only', script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()))
    print('[DESKTOP_DRY_RUN]', verdict)
    for name in models:
        print(name, 'B', models[name]['B'], 'full2s p/v NRMSE', summary[name]['sensor']['full2s']['nrmse'],
            'gates', summary[name]['gate_prediction_pv'], summary[name]['gate_direct_B_velocity'])


if __name__ == '__main__':
    main()
