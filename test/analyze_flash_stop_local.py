"""DESKTOP_DRY_RUN: frozen M2/M4 near-stop delta and affine prediction tests."""

import argparse
import json
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

from analyze_flash_state_learning import state, rms, FLOOR, HORIZONS, summarize
from eval_flash_state_learning import MODELS
from eval_flash_pv_models import REPO, write, sha256

OLD_MODELS = REPO/'docs/exp/2026-10-15/flash_state_learning/expanded/state_models_frozen.json'


def load(root, split):
    records, direct, acquisition = [], [], []
    for path in sorted(root.glob('*/results.json')):
        info = json.loads(path.read_text())
        if info['job']['split'] != split:
            continue
        direct.extend(info['direct_B'])
        acquisition.extend(info['acquisition'])
        for row in info['responses']:
            with np.load(path.parent/row['trace']) as z, np.load(path.parent/row['baseline']) as b:
                absolute, base = state(z), state(b)
                absolute[:, 0] -= info['anchor_sensor_p']
                base[:, 0] -= info['anchor_sensor_p']
                np.testing.assert_array_equal(absolute[0], base[0])
                np.testing.assert_array_equal(z['previous_action'][:-1], z['history'])
                np.testing.assert_array_equal(z['previous_action'][1:], z['action'])
                u = z['actual_u'].copy()
                bu = b['actual_u'].copy()
                if row['mode'] == 'feedback':
                    u -= z['bias']; bu -= b['bias']
                records.append(dict(**row, context=info['job']['id'], absolute=absolute,
                    base=base, delta=absolute-base, u=u, base_u=bu, du=u-bu,
                    gt=z['gt']-b['gt'], total_u=z['actual_u'].copy(),
                    base_total_u=b['actual_u'].copy()))
    return records, direct, acquisition


def fit_local(records, name, affine=False):
    indices = MODELS[name]
    mode = records[0]['mode']
    n = len(indices)
    key = 'absolute' if affine else 'delta'
    uk = 'u' if affine else 'du'
    x = np.concatenate([r[key][:-1, indices] for r in records])
    y = np.concatenate([r[key][1:, indices] for r in records])
    u = np.concatenate([r[uk] for r in records])
    ref = x.mean(0) if affine else np.zeros(n)
    uref = float(u.mean()) if affine else 0.
    xc, yc, uc = x-ref, y-ref, u-uref
    first = 1 if mode == 'frozen' else 0
    target = yc.copy()
    if first:
        target[:, 0] -= xc[:, 0]
    z = np.column_stack([xc[:, first:], uc])
    if affine:
        z = np.column_stack([z, np.ones(len(z))])
    scale = np.maximum(rms(z, 0), 1e-14)
    coeff, _, rank, singular = np.linalg.lstsq(z/scale, target, rcond=1e-10)
    coeff = (coeff/scale[:, None]).T
    A = np.zeros((n, n))
    if first:
        A[0, 0] = 1.
    A[:, first:] = coeff[:, :n-first]
    B = coeff[:, n-first].copy()
    c = coeff[:, -1].copy() if affine else np.zeros(n)
    # Action is computed before the current external residual torque is applied.
    action = list(range(4, 12))
    j = n-first
    za = np.delete(z, j, axis=1)
    sa = np.delete(scale, j)
    ac = np.linalg.lstsq(za/sa, target[:, action], rcond=1e-10)[0]
    ac = (ac/sa[:, None]).T
    A[np.ix_(action, range(first, n))] = ac[:, :n-first]
    B[action] = 0.
    if affine:
        c[action] = ac[:, -1]
    return dict(name=name, mode=mode, kind='affine' if affine else 'delta', indices=indices,
        A=A.tolist(), B=B.tolist(), c_center=c.tolist(), state_reference=ref.tolist(), input_reference=uref,
        samples=len(u), rank=int(rank), scaled_condition=float(singular[0]/singular[-1]),
        spectral_radius=float(max(abs(np.linalg.eigvals(A)))),
        position_translation_symmetry=bool(first), action_B_zero_rows=action,
        state_std=np.maximum(x.std(0), 1e-9).tolist(), train_min=x.min(0).tolist(), train_max=x.max(0).tolist(),
        training_pv_rmse=rms((xc@A.T+uc[:, None]*B+c-yc)[:, :2], 0).tolist())


def predict(model, initial, inputs, omit_offset=False):
    A, B = np.asarray(model['A']), np.asarray(model['B'])
    ref = np.asarray(model.get('state_reference', np.zeros(len(B))))
    uref = model.get('input_reference', 0.)
    c = np.zeros(len(B)) if omit_offset else np.asarray(model.get('c_center', np.zeros(len(B))))
    value = initial-ref
    rows = [initial.copy()]
    for t in range(inputs.shape[1]):
        value = value@A.T+(inputs[:, t, None]-uref)*B+c
        rows.append(value+ref)
    result = np.stack(rows, 1)
    assert np.isfinite(result).all()
    return result


def metric(error, response):
    err, signal = rms(error[..., :2], 1), rms(response[..., :2], 1)
    return dict(rmse=err, signal_rms=signal, nrmse=err/np.maximum(signal, FLOOR))


def evaluate(model, records):
    indices = model['indices']
    affine = model.get('kind') == 'affine'
    key = 'absolute' if affine else 'delta'
    uk = 'u' if affine else 'du'
    z = np.asarray([r[key][:, indices] for r in records])
    response = np.asarray([r['delta'][:, indices] for r in records])
    u = np.asarray([r[uk] for r in records])
    # No future measured state enters predict(); measured matched-baseline arrays
    # are used only to define the response normalization denominator.
    n, length = u.shape
    one = predict(model, z[:, :-1].reshape(-1, len(indices)), u.reshape(-1, 1))[:, 1].reshape(n, length, -1)
    full = predict(model, z[:, 0], u[:, :100])[:, 1:]
    stats = dict(one_step=metric(one-z[:, 1:], response[:, 1:]),
        full2s=metric(full-z[:, 1:101], response[:, 1:101]), horizons={})
    for h in HORIZONS:
        starts = np.arange(0, length-h+1, 10)
        initial = z[:, starts].reshape(-1, len(indices))
        inputs = np.stack([u[:, start:start+h] for start in starts], 1).reshape(-1, h)
        output = predict(model, initial, inputs)[:, -1].reshape(n, len(starts), -1)
        stats['horizons'][str(h)] = metric(output-z[:, starts+h], response[:, starts+h])
    return summarize(stats), stats


def equilibrium(model):
    """Diagnostic affine steady solution, not a new controller or gain."""
    A, B = np.asarray(model['A']), np.asarray(model['B'])
    ref, c = np.asarray(model['state_reference']), np.asarray(model['c_center'])
    scale = np.asarray(model['state_std'])
    fixed = np.zeros(len(B)); fixed[1] = -ref[1]
    D = A-np.eye(len(B))
    matrix = np.column_stack([D[:, 2:]*scale[2:], B*.1])/scale[:, None]
    rhs = -(D@fixed+c)/scale
    solution, _, rank, singular = np.linalg.lstsq(matrix, rhs, rcond=1e-10)
    center = fixed.copy(); center[2:] = solution[:-1]*scale[2:]
    du = solution[-1]*.1
    residual = D@center+B*du+c
    actual = center+ref
    return dict(residual_input=model['input_reference']+float(du), state=actual.tolist(),
        one_step_defect=residual.tolist(), equation_rank=int(rank),
        scaled_equation_residual_rms=float(np.sqrt(np.mean((residual/scale)**2))),
        hidden_state_outside_training_range=int(np.sum((actual[2:] < np.asarray(model['train_min'])[2:]) |
            (actual[2:] > np.asarray(model['train_max'])[2:]))),
        note='Algebraic extrapolation at v=0; needs separate MuJoCo validation; not an exact nonlinear equilibrium')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, required=True)
    args = parser.parse_args()
    root = args.root.resolve()
    train, _, _ = load(root, 'train')
    models = []
    for mode in ['frozen', 'feedback']:
        rows = [r for r in train if r['mode'] == mode]
        assert rows, mode
        for name in ['M2', 'M4']:
            models += [fit_local(rows, name), fit_local(rows, name, affine=True)]
    path = root/'models_frozen.json'
    if path.exists():
        raise RuntimeError('Refusing to overwrite frozen matrices')
    write(path, dict(execution_domain='DESKTOP_DRY_RUN', evidence_status='NOT_TESTED', models=models,
        frozen_before_test=True, script_sha256=sha256(Path(__file__)),
        training_contexts=sorted(set(r['context'] for r in train)),
        affine_equilibrium={m['name']: equilibrium(m) for m in models if m['mode']=='frozen' and m['kind']=='affine'}))
    model_hash = sha256(path)
    test, direct, acquisitions = load(root, 'test')
    assert not set(r['context'] for r in train)&set(r['context'] for r in test)
    old = json.loads(OLD_MODELS.read_text())['models']
    for name in ['M2', 'M4']:
        m = dict(next(m for m in old if m['name']==name and m['context_count']==24))
        m.update(mode='frozen', kind='moving_transfer')
        models.append(m)
    results, details = [], {}
    for model in models:
        rows = [r for r in test if r['mode'] == model['mode']]
        summary, full = evaluate(model, rows)
        b = np.median([r['sensor_B'][:2] for r in direct if r['mode']==model['mode']], 0)
        relative = abs(np.asarray(model['B'])[:2]-b)/np.maximum(abs(b), FLOOR)
        passed = all(np.all(np.asarray(summary['horizons'][str(h)]['nrmse']) <= .3) for h in [5, 25, 50, 100])
        passed = passed and all(v <= .3 for v in summary['full2s']['nrmse']) and relative[1] <= .3
        key = f"{model['mode']}_{model['name']}_{model['kind']}"
        summary.update(mode=model['mode'], name=model['name'], kind=model['kind'],
            direct_B_reference=b.tolist(), B_pv=model['B'][:2], B_relative_error=relative.tolist(),
            diagnostic_gate=bool(passed), scaled_condition=model.get('scaled_condition'),
            spectral_radius=model.get('spectral_radius'), response_count=len(rows))
        if model['kind']=='affine':
            baseline = []
            for r in rows:
                if (r['context'], r['start_rl_s']) in [v['key'] for v in baseline]:
                    continue
                z = r['base'][:, model['indices']]
                u = r['base_u'][None, :100]
                pred = predict(model, z[None, 0], u)[0]
                no_c = predict(model, z[None, 0], u, omit_offset=True)[0]
                baseline.append(dict(key=(r['context'], r['start_rl_s']),
                    rmse=rms(pred[1:, :2]-z[1:101, :2], 0).tolist(),
                    omit_c_rmse=rms(no_c[1:, :2]-z[1:101, :2], 0).tolist(),
                    actual_v_mean=float(z[1:101, 1].mean()), predicted_v_mean=float(pred[1:, 1].mean()),
                    total_residual_mean=float(r['base_total_u'][:100].mean())))
            summary['baseline_absolute'] = baseline
        results.append(summary)
        details[key] = {k: ({h: {q: v.tolist() for q, v in val.items()} for h, val in value.items()}
            if k == 'horizons' else {q: v.tolist() for q, v in value.items()}) for k, value in full.items()}
        print('[DESKTOP_DRY_RUN]', key, summary['full2s']['nrmse'], summary['diagnostic_gate'], flush=True)
    write(root/'prediction_metrics.json', dict(execution_domain='DESKTOP_DRY_RUN', results=details))
    write(root/'summary.json', dict(execution_domain='DESKTOP_DRY_RUN', evidence_status='SUSPICIOUS',
        results=results, acquisitions=acquisitions, models_sha256=model_hash,
        primary_metrics='matched p/v response; affine absolute error normalized by matched response, not absolute offset',
        old_models_sha256=sha256(OLD_MODELS), no_LQR=True))
    # One deterministic positive pulse chosen by family/amplitude/context, not error.
    rows = [r for r in test if r['mode']=='frozen' and r['family']=='pulse_pos' and r['amplitude']==.25]
    row = rows[0]
    fig, axes = plt.subplots(2, 1, figsize=(10, 7), sharex=True)
    time = np.arange(201)*.02
    for component, ax in enumerate(axes):
        ax.plot(time, row['delta'][:, component]*1000, 'k', label='MuJoCo matched response')
        for m in models:
            if m['mode']!='frozen' or m['kind']=='affine':
                continue
            z = row['delta'][:, m['indices']]
            output = predict(m, z[None, 0], row['du'][None])[0]
            ax.plot(time, output[:, component]*1000, label=f"{m['name']} {m['kind']}")
        ax.set_ylabel(['position [mm]', 'velocity [mm/s]'][component]); ax.grid(alpha=.3)
    axes[0].legend(fontsize=8); axes[-1].set_xlabel('time after branch [s]')
    fig.tight_layout(); fig.savefig(root/'pulse_transfer.png', dpi=150); plt.close(fig)
    assert sha256(path) == model_hash
    write(root/'analysis_integrity.json', dict(execution_domain='DESKTOP_DRY_RUN', evidence_status='PASS',
        models_unchanged_after_test=True, frozen_before_test=True, test_used_for_fit=False,
        all_hidden_states_predicted_recursively=True, affine_baseline_only_used_for_evaluation=True,
        source_sha256=sha256(Path(__file__))))


if __name__ == '__main__':
    main()
