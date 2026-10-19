"""DESKTOP_DRY_RUN: M0..M4 state ablation and nested-context learning curves.

All candidate matrices are frozen before test arrays are opened. Every selected
action/leg state is predicted recursively; only a window's initial measured
state is supplied. No LQR gain is computed or deployed.
"""

import argparse
import hashlib
import json
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

from eval_flash_state_learning import MODELS, REPO, OLD, write, sha256

HORIZONS = [5, 10, 25, 50, 100]
FLOOR = np.array([1e-7, 1e-5])


def rms(values, axis):
    return np.sqrt(np.mean(np.asarray(values)**2, axis=axis))


def state(trace):
    return np.concatenate([trace[k] for k in ['sensor', 'previous_action', 'leg_position', 'leg_velocity']], axis=1)


def load(root, split):
    records, contexts, direct = [], [], []
    for path in sorted(root.glob('*/results.json')):
        info = json.loads(path.read_text())
        if info['job']['split'] != split:
            continue
        assert info['evidence_status'] == 'PASS'
        contexts.append(info['job']['id'])
        direct.extend(info['direct_B'])
        for row in info['responses']:
            with np.load(path.parent/row['trace']) as current, np.load(path.parent/row['baseline']) as base:
                np.testing.assert_array_equal(current['previous_action'][:-1], current['history'])
                np.testing.assert_array_equal(current['previous_action'][1:], current['action'])
                delta = state(current)-state(base)
                np.testing.assert_array_equal(delta[0], np.zeros(24))
                records.append(dict(context=info['job']['id'], **row, z=delta,
                    u=current['actual_u']-base['actual_u'], gt=current['gt']-base['gt']))
    return records, contexts, direct


def fit(x_full, y_full, u, name):
    indices = MODELS[name]
    x, y = x_full[:, indices], y_full[:, indices]
    n = len(indices)
    target = y.copy()
    target[:, 0] -= x[:, 0]
    z = np.column_stack([x[:, 1:], u])
    scales = rms(z, 0)
    scales = np.where(scales > 1e-14, scales, 1.)
    coeff, _, rank, singular = np.linalg.lstsq(z/scales, target, rcond=1e-10)
    unscaled = (coeff/scales[:, None]).T
    A = np.zeros((n, n)); A[0, 0] = 1.
    A[:, 1:], B = unscaled[:, :-1].copy(), unscaled[:, -1].copy()
    action_rows = [i for i, index in enumerate(indices) if 4 <= index < 12]
    if action_rows:
        # a[t] is evaluated before r[t] is applied; next previous-action has no
        # direct current-residual dependence. Its state dependence is still fitted.
        ac = np.linalg.lstsq(z[:, :-1]/scales[:-1], target[:, action_rows], rcond=1e-10)[0]
        A[np.ix_(action_rows, range(1, n))] = (ac/scales[:-1, None]).T
        B[action_rows] = 0.
    ru = u-x[:, 1:]@np.linalg.lstsq(x[:, 1:], u, rcond=None)[0]
    return dict(name=name, indices=indices, dimension=n, A=A.tolist(), B=B.tolist(),
        samples=len(u), rank=int(rank), rms_scaled_condition=float(singular[0]/singular[-1]),
        input_innovation_energy_fraction=float(ru@ru/(u@u)),
        action_B_zero_rows=action_rows, position_translation_symmetry=True,
        training_one_step_pv_rmse=rms((x@A.T+u[:, None]*B-y)[:, :2], 0).tolist(),
        spectral_radius=float(max(abs(np.linalg.eigvals(A)))))


def predict(A, B, initial, inputs):
    """Batched full-state prediction; accepts no future measured state argument."""
    value = initial.copy()
    predictions = [value.copy()]
    for k in range(inputs.shape[1]):
        value = value@A.T+inputs[:, k, None]*B
        predictions.append(value.copy())
    result = np.stack(predictions, axis=1)
    if not np.isfinite(result).all():
        raise FloatingPointError('Frozen model free prediction diverged to nonfinite values')
    return result


def metric(prediction, actual):
    error = rms(prediction[..., :2]-actual[..., :2], 1)
    signal = rms(actual[..., :2], 1)
    return dict(rmse=error, signal_rms=signal, nrmse=error/np.maximum(signal, FLOOR))


def evaluate(model, data, inputs):
    A, B = np.asarray(model['A']), np.asarray(model['B'])
    z = data[:, :, model['indices']]
    one = z[:, :-1]@A.T+inputs[:, :, None]*B
    stats = dict(one_step=metric(one, z[:, 1:]),
        full2s=metric(predict(A, B, z[:, 0], inputs[:, :100])[:, 1:], z[:, 1:101]), horizons={})
    for h in HORIZONS:
        starts = np.arange(0, inputs.shape[1]-h+1, 10)
        value = z[:, starts].copy()
        for k in range(h):
            value = value@A.T+inputs[:, starts+k, None]*B
        if not np.isfinite(value).all():
            raise FloatingPointError('Nonfinite rolling-window prediction')
        stats['horizons'][str(h)] = metric(value, z[:, starts+h])
    return stats


def summarize(stats):
    result = {key: {m: np.median(v, axis=0).tolist() for m, v in stats[key].items()}
        for key in ['one_step', 'full2s']}
    result['horizons'] = {h: {m: np.median(v, axis=0).tolist() for m, v in values.items()}
        for h, values in stats['horizons'].items()}
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, required=True)
    args = parser.parse_args()
    root = args.root.resolve()
    manifest = json.loads((root/'manifest.json').read_text())
    archive = manifest['stage'] == 'archive'
    train, contexts, train_direct = load(root, 'train')
    count_list = [len(contexts)] if archive else [1, 2, 3, 6, 12, 24]
    orders = [0] if archive else [701, 702, 703]
    models = []
    for order_seed in orders:
        order = list(contexts) if archive else np.random.default_rng(order_seed).permutation(contexts).tolist()
        for count in count_list:
            if count == len(contexts) and order_seed != orders[0]:
                continue
            subset = [r for r in train if r['context'] in order[:count]]
            x = np.concatenate([r['z'][:-1] for r in subset])
            y = np.concatenate([r['z'][1:] for r in subset])
            u = np.concatenate([r['u'] for r in subset])
            for name in MODELS:
                model = fit(x, y, u, name)
                model.update(context_count=count, response_count=len(subset),
                    order_seed=order_seed, contexts=order[:count])
                models.append(model)
            print('[DESKTOP_DRY_RUN] frozen candidate fits', order_seed, count, len(subset), flush=True)
    model_path = root/'state_models_frozen.json'
    if model_path.exists():
        raise RuntimeError('Refusing to overwrite frozen models')
    if archive:
        original = json.loads((OLD/'models.json').read_text())['models']
        for new, old in [('M0', 'M1'), ('M1', 'M2')]:
            current = next(m for m in models if m['name'] == new)
            np.testing.assert_allclose(current['A'], original[old]['A'], atol=1e-10, rtol=1e-9)
            np.testing.assert_allclose(current['B'], original[old]['B'], atol=1e-10, rtol=1e-9)
    write(model_path, dict(execution_domain='DESKTOP_DRY_RUN', evidence_status='NOT_TESTED',
        models=models, training_contexts=contexts, checkpoint_sha256=manifest['checkpoint_sha256'],
        script_sha256=sha256(Path(__file__)), models_frozen_before_test=True,
        constraints='position translation; current input cannot affect next previous action',
        no_LQR=True))
    model_hash = sha256(model_path)
    test, test_contexts, direct = load(root, 'validation' if archive else 'test')
    assert not (set(contexts)&set(test_contexts))
    # Full independent cohort, same test arrays for every state set/data level.
    data = np.asarray([r['z'] for r in test])
    inputs = np.asarray([r['u'] for r in test])
    gt = np.asarray([r['gt'] for r in test])
    b_reference = np.median([r['sensor_B'] for r in direct], axis=0)
    results, full_records = [], {}
    for model in models:
        stats = evaluate(model, data, inputs)
        summary = summarize(stats)
        b = np.asarray(model['B'])[:2]
        relative = abs(b-b_reference[:2])/np.maximum(abs(b_reference[:2]), FLOOR)
        summary.update(name=model['name'], context_count=model['context_count'],
            response_count=model['response_count'], transitions=model['samples'],
            order_seed=model['order_seed'], B_pv=b.tolist(), B_relative_error_pv=relative.tolist(),
            B_sign_match_pv=(np.sign(b)==np.sign(b_reference[:2])).tolist())
        summary['prediction_gate'] = all(v <= .3 for h in ['5', '25', '50', '100']
            for v in summary['horizons'][h]['nrmse']) and all(v <= .3 for v in summary['full2s']['nrmse'])
        summary['B_gate'] = bool(relative[1] <= .3 and b[1]*b_reference[1] > 0)
        summary['diagnostic_gate'] = summary['prediction_gate'] and summary['B_gate']
        results.append(summary)
        if model['context_count'] == len(contexts):
            record = []
            for i, row in enumerate(test):
                entry = {k: row[k] for k in ['context', 'family', 'amplitude', 'start_rl_s']}
                entry['full2s'] = {k: v[i].tolist() for k, v in stats['full2s'].items()}
                entry['horizons'] = {h: {k: v[i].tolist() for k, v in values.items()}
                    for h, values in stats['horizons'].items()}
                record.append(entry)
            full_records[model['name']] = record
            prediction = predict(np.asarray(model['A']), np.asarray(model['B']), data[:, 0, model['indices']], inputs[:, :100])
            summary['GT_full2s'] = {k: np.median(v, axis=0).tolist()
                for k, v in metric(prediction[:, 1:, :2], gt[:, 1:101]).items()}
        print('[DESKTOP_DRY_RUN] scored', model['name'], model['context_count'], model['order_seed'],
            'full2s', summary['full2s']['nrmse'], 'Berr', relative[1], flush=True)
    full = {r['name']: r for r in results if r['context_count'] == len(contexts)}
    write(root/'learning_curve.json', dict(execution_domain='DESKTOP_DRY_RUN', results=results,
        context_counts=count_list, order_seeds=orders, note='Related deterministic contexts; order spread is descriptive, not confidence intervals.'))
    write(root/'full_data_metrics.json', full_records)
    write(root/'state_summary.json', dict(execution_domain='VALIDATION_SIM',
        evidence_status='PASS' if any(r['diagnostic_gate'] for r in full.values()) else 'FAIL',
        full_models=full, train_responses=len(train), test_responses=len(test),
        train_contexts=len(contexts), test_contexts=len(test_contexts),
        direct_B_reference=b_reference.tolist(), direct_pairs_train=len(train_direct), direct_pairs_test=len(direct),
        model_sha256=model_hash, old_scalar_models_reproduced=archive,
        interpretation='Status is model-prediction gates, not collection integrity or control stability.'))
    for metric_name, title in [('full2s', 'First2s free response'), ('100', '2s rolling prediction')]:
        fig, axes = plt.subplots(1, 2, figsize=(11, 4))
        for name in MODELS:
            selected = [r for r in results if r['name'] == name]
            counts = sorted({r['response_count'] for r in selected})
            for i, ax in enumerate(axes):
                values = [[(r['full2s'] if metric_name=='full2s' else r['horizons'][metric_name])['nrmse'][i]*100
                    for r in selected if r['response_count']==count] for count in counts]
                ax.plot(counts, [np.median(v) for v in values], 'o-', label=name)
                ax.fill_between(counts, [min(v) for v in values], [max(v) for v in values], alpha=.12)
        for ax, variable in zip(axes, ['p', 'v']):
            ax.set_xscale('log'); ax.set_xlabel('Training response count (whole contexts)')
            ax.set_ylabel(f'{variable} median NRMSE [%]'); ax.grid(True); ax.legend(fontsize=8)
            ax.axhline(30, color='grey', linestyle=':')
        fig.suptitle(title+'; shaded range across3 fixed nested orders')
        fig.tight_layout(); fig.savefig(root/f'learning_{metric_name}.png', dpi=160); plt.close(fig)
    fig, axes = plt.subplots(1, 2, figsize=(11, 4))
    for name, values in full.items():
        for i, ax in enumerate(axes):
            ax.plot(np.array(HORIZONS)*.02, [values['horizons'][str(h)]['nrmse'][i]*100 for h in HORIZONS], 'o-', label=name)
    for ax, variable in zip(axes, ['p', 'v']):
        ax.set_ylabel(f'{variable} NRMSE [%]'); ax.set_xlabel('Free prediction horizon [s]')
        ax.axhline(30, color='grey', linestyle=':'); ax.grid(True); ax.legend()
    fig.tight_layout(); fig.savefig(root/'state_horizons.png', dpi=160); plt.close(fig)
    # Saved full hidden-state predictions make the lack of future state injection reviewable.
    example_index = next(i for i, r in enumerate(test) if r['family'] in ['validation_prbs'] and r['amplitude']==.25)
    example = test[example_index]
    fig, axes = plt.subplots(3, 1, figsize=(11, 9), sharex=True)
    t = np.arange(len(example['u'])+1)*.02
    axes[0].step(t[:-1], example['u'], where='post'); axes[0].set_ylabel('Total residual [Nm]')
    saved = dict(actual_full24=example['z'], actual_gt=example['gt'], actual_input=example['u'])
    for i, ax in enumerate(axes[1:]):
        ax.plot(t, example['z'][:, i], color='black', label='MuJoCo')
        for name in MODELS:
            m = next(v for v in models if v['name']==name and v['context_count']==len(contexts))
            prediction = predict(np.asarray(m['A']), np.asarray(m['B']), example['z'][None, 0, m['indices']], example['u'][None])[0]
            saved[name+'_predicted_all_states'] = prediction
            ax.plot(t, prediction[:, i], '--', label=name)
        ax.set_ylabel(['Delta p [m]', 'Delta v [m/s]'][i]); ax.legend(fontsize=8)
    for ax in axes: ax.grid(True)
    axes[-1].set_xlabel('Time since matched branch [s]')
    fig.suptitle(str(example['context'])+f', RL{example["start_rl_s"]}s, PRBS0.25Nm')
    fig.tight_layout(); fig.savefig(root/'response_example.png', dpi=160); plt.close(fig)
    np.savez_compressed(root/'hidden_state_prediction_example.npz', **saved)
    assert sha256(model_path) == model_hash
    assert all(sha256(REPO/p)==value for p, value in manifest['protected_sha256'].items())
    write(root/'analysis_integrity.json', dict(execution_domain='DESKTOP_DRY_RUN', evidence_status='PASS',
        all_candidates_frozen_before_test=True, models_preserved=True, protected_sources_preserved=True,
        history_alignment_checked=True, predicts_all_selected_states=True,
        future_state_injection=False, contexts_disjoint=True, same_test_for_all_models=True,
        script_sha256=sha256(Path(__file__)), original_baseline_matrices_reproduced=archive,
        LQR_designed=False, stop_affine_designed=False))


if __name__ == '__main__':
    main()
