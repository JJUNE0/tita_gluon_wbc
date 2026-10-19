"""DESKTOP_DRY_RUN: train-only M4 affine fitting and held-out absolute prediction.

Existing operating-point traces are reused without modification. The physical
model z_next=A*z+B*r+c is evaluated before any conditional LQR design.
"""

import argparse
import json
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

from analyze_flash_state_learning import state, rms
from analyze_flash_stop_local import fit_local, predict, metric
from analyze_flash_operating_local import summarize_all
from eval_flash_operating_local import BIAS, REPO, write, sha256

SOURCE = REPO/'docs/exp/2026-10-15/flash_operating_local/full'
BASE_LIMITS = {'2s': [2e-5, 2e-5], '8s': [5e-5, 2e-5]}


def load_absolute(root, split):
    records, baselines, direct = [], [], []
    for path in sorted(root.glob('*/results.json')):
        info = json.loads(path.read_text())
        if info['job']['split'] != split:
            continue
        assert info['evidence_status'] == 'PASS'
        direct.extend(info['direct_B'])
        seen = set()
        for row in info['responses']:
            with np.load(path.parent/row['trace']) as trace, np.load(path.parent/row['baseline']) as base:
                z, b = state(trace), state(base)
                anchor = float(b[0, 0])
                z[:, 0] -= anchor
                b[:, 0] -= anchor
                np.testing.assert_array_equal(z[0], b[0])
                np.testing.assert_array_equal(trace['previous_action'][1:], trace['action'])
                np.testing.assert_array_equal(trace['previous_action'][:-1], trace['history'])
                common = dict(context=info['job']['id'], seed=info['job']['seed'],
                              mode='frozen', start_rl_s=row['start_rl_s'])
                records.append(dict(**common, family=row['family'], amplitude=row['amplitude'],
                    absolute=z, base=b, delta=z-b, u=trace['actual_u'].copy(),
                    base_u=base['actual_u'].copy()))
                if row['baseline'] not in seen:
                    baselines.append(dict(**common, family='zero', amplitude=0., absolute=b,
                        base=b, delta=np.zeros_like(b), u=base['actual_u'].copy()))
                    seen.add(row['baseline'])
    return records, baselines, direct


def evaluate_affine(model, records):
    z = np.asarray([r['absolute'] for r in records])
    u = np.asarray([r['u'] for r in records])
    response = np.asarray([r['delta'] for r in records])
    A, B = np.asarray(model['A']), np.asarray(model['B'])
    ref, ur = np.asarray(model['state_reference']), model['input_reference']
    c = np.asarray(model['c_center'])
    one = (z[:, :-1]-ref)@A.T + (u[:, :, None]-ur)*B + c + ref
    prediction = predict(model, z[:, 0], u)
    stats = {'one_step': metric(one-z[:, 1:], response[:, 1:]), 'horizons': {}}
    for end in [100, 200, 400]:
        stats[f'full{end//50}s'] = metric(prediction[:, 1:end+1]-z[:, 1:end+1], response[:, 1:end+1])
    for h in [5, 25, 50, 100, 200]:
        starts = np.arange(0, u.shape[1]-h+1, 10)
        value = z[:, starts]-ref
        for k in range(h):
            value = value@A.T + (u[:, starts+k, None]-ur)*B + c
        stats['horizons'][str(h)] = metric(value+ref-z[:, starts+h], response[:, starts+h])
    return stats, prediction


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, default=SOURCE)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    out, source = args.output.resolve(), args.source.resolve()
    assert out.is_relative_to(REPO/'docs/exp') and not out.exists()
    out.mkdir(parents=True)
    original = json.loads((source/'manifest.json').read_text())
    protected = dict(original['protected_sha256'])
    inputs = list(source.glob('**/*.npz')) + list(source.glob('**/*.json'))
    protected.update({str(p.relative_to(REPO)): sha256(p) for p in inputs})
    for name in ['eval_flash_operating_local.py', 'analyze_flash_operating_local.py',
                 'analyze_flash_stop_local.py', 'analyze_flash_state_learning.py']:
        p = REPO/'test'/name
        protected[str(p.relative_to(REPO))] = sha256(p)
    write(out/'manifest.json', dict(execution_domain='DESKTOP_DRY_RUN', source=str(source.relative_to(REPO)),
        checkpoint_sha256=original['checkpoint_sha256'], onnx_sha256=original['onnx_sha256'],
        script_sha256=sha256(Path(__file__)), protected_sha256=protected,
        primary='median absolute prediction error normalized by matched response <=30% for first2s and rolling0.1/0.5/1/2s; Bv sign/error<=30%',
        baseline_gate='all18 test baselines: 2s p/v RMSE <=0.02mm/0.02mm/s; 8s <=0.05mm/0.02mm/s',
        baseline_limits_SI=BASE_LIMITS, fit='M4 only; train probes plus unique baselines; scaled LS, causal action B rows0, translation symmetry',
        no_equilibrium_solve=True, scope='finite absolute-state prediction; conditional LQR is a separate stage'))
    train, train_base, _ = load_absolute(source, 'train')
    model = fit_local(train+train_base, 'M4', affine=True)
    A, B = np.asarray(model['A']), np.asarray(model['B'])
    ref = np.asarray(model['state_reference'])
    c_absolute = ref - A@ref - B*model['input_reference'] + np.asarray(model['c_center'])
    model['c_absolute'] = c_absolute.tolist()
    operating_reference = np.concatenate([r['absolute'] for r in train_base]).mean(0)
    operating_reference[:2] = 0.
    model['operating_reference'] = operating_reference.tolist()
    model['operating_reference_defect'] = (A@operating_reference+B*BIAS+c_absolute-operating_reference).tolist()
    path = out/'affine_model_frozen.json'
    write(path, dict(execution_domain='DESKTOP_DRY_RUN', evidence_status='NOT_TESTED', model=model,
        train_probes=len(train), train_baselines=len(train_base),
        checkpoint_sha256=original['checkpoint_sha256'], models_frozen_before_test=True,
        train_seeds=sorted({r['seed'] for r in train}), script_sha256=sha256(Path(__file__)),
        reference='train baseline hidden-state mean, p=0,v=0; finite reference, not solved static equilibrium'))
    model_hash = sha256(path)
    test, test_base, direct = load_absolute(source, 'test')
    assert not {r['seed'] for r in train}&{r['seed'] for r in test}
    stats, predictions = evaluate_affine(model, test)
    summary = summarize_all(stats)
    Bv = float(np.median([r['sensor_B'][1] for r in direct]))
    B_error = abs(B[1]-Bv)/abs(Bv)
    primary = all(np.all(np.asarray(summary['horizons'][str(h)]['nrmse']) <= .3) for h in [5,25,50,100])
    primary = bool(primary and np.all(np.asarray(summary['full2s']['nrmse']) <= .3) and B_error <= .3 and B[1]*Bv>0)
    baselines = []
    for row in test_base:
        z, u = row['absolute'][None], row['u'][None]
        pred = predict(model, z[:, 0], u)
        omit = predict(model, z[:, 0], u, omit_offset=True)
        entry = {k:row[k] for k in ['context', 'start_rl_s']}
        for end in [100, 400]:
            entry[f'{end//50}s_rmse'] = rms(pred[0,1:end+1,:2]-z[0,1:end+1,:2], 0).tolist()
            entry[f'{end//50}s_omit_center_offset_rmse'] = rms(omit[0,1:end+1,:2]-z[0,1:end+1,:2], 0).tolist()
        entry['pass'] = all(np.all(np.asarray(entry[k+'_rmse']) <= BASE_LIMITS[k]) for k in BASE_LIMITS)
        baselines.append(entry)
    baseline_pass = all(r['pass'] for r in baselines)
    passed = primary and baseline_pass
    write(out/'summary.json', dict(execution_domain='DESKTOP_DRY_RUN', evidence_status='PASS' if passed else 'FAIL',
        gate=passed, response_gate=primary, baseline_gate=baseline_pass, metrics=summary,
        direct_Bv=Bv, fitted_Bv=float(B[1]), Bv_relative_error=B_error, baselines=baselines,
        model_sha256=model_hash, test_probes=len(test), test_baselines=len(test_base),
        test_seeds=sorted({r['seed'] for r in test}), condition=model['scaled_condition'],
        note='Reuses earlier held-out traces; new coefficients use train only. No equilibrium or infinite-horizon extrapolation.'))
    write(out/'prediction_metrics.json', dict(execution_domain='DESKTOP_DRY_RUN',
        traces=[{k:r[k] for k in ['context','family','amplitude','start_rl_s']} for r in test],
        metrics={key:({h:{m:v.tolist() for m,v in row.items()} for h,row in value.items()} if key=='horizons'
            else {m:v.tolist() for m,v in value.items()}) for key,value in stats.items()}))
    for family in ['pulse_pos', 'validation_prbs']:
        i = next(i for i,r in enumerate(test) if r['family']==family and r['amplitude']==.05)
        row = test[i]
        fig, axes = plt.subplots(2,1,figsize=(10,6),sharex=True)
        t = np.arange(401)*.02
        for k,ax in enumerate(axes):
            ax.plot(t,row['absolute'][:,k]*1000,'k',label='MuJoCo actual state')
            ax.plot(t,predictions[i,:,k]*1000,label='M4 affine, all states predicted')
            ax.set_ylabel(['local p [mm]','v [mm/s]'][k]); ax.grid(alpha=.3)
        axes[0].legend(); axes[-1].set_xlabel('time after branch [s]')
        fig.tight_layout(); fig.savefig(out/f'affine_{family}.png',dpi=150); plt.close(fig)
    assert sha256(path)==model_hash
    assert all(sha256(REPO/p)==h for p,h in protected.items())
    write(out/'integrity.json',dict(execution_domain='DESKTOP_DRY_RUN',evidence_status='PASS',
        protected_hashes_preserved=True, frozen_model_unchanged=True, hidden_states_predicted=True,
        fit_train_only=True, disjoint_initial_seeds=True))
    print('[DESKTOP_DRY_RUN]', 'affine gate',passed,'response',primary,'baseline',baseline_pass,
          'full2',summary['full2s']['nrmse'],'rolling2',summary['horizons']['100']['nrmse'],flush=True)


if __name__ == '__main__':
    main()
