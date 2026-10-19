"""DESKTOP_DRY_RUN: preserve paired M4 A/B and calibrate only the affine offset.

The joint absolute LS result is retained. This second, explicit estimator uses
train baselines only for c and requires fresh simulation confirmation.
"""

import argparse
import json
from pathlib import Path

import numpy as np

from analyze_flash_operating_affine import SOURCE, BASE_LIMITS, load_absolute, evaluate_affine
from analyze_flash_operating_local import summarize_all
from analyze_flash_stop_local import predict
from analyze_flash_state_learning import rms
from eval_flash_operating_local import REPO, BIAS, write, sha256


def validate(model, root):
    probes, baselines, direct = load_absolute(root, 'test')
    stats, _ = evaluate_affine(model, probes)
    summary = summarize_all(stats)
    bv = float(np.median([r['sensor_B'][1] for r in direct]))
    b_error = abs(model['B'][1]-bv)/abs(bv)
    response_pass = all(np.all(np.asarray(summary['horizons'][str(h)]['nrmse'])<=.3) for h in [5,25,50,100])
    response_pass = bool(response_pass and np.all(np.asarray(summary['full2s']['nrmse'])<=.3)
                         and b_error<=.3 and model['B'][1]*bv>0)
    rows = []
    for row in baselines:
        z, u = row['absolute'][None], row['u'][None]
        pred = predict(model, z[:,0], u)
        item = {k:row[k] for k in ['context','start_rl_s']}
        for end in [100,400]:
            item[f'{end//50}s_rmse'] = rms(pred[0,1:end+1,:2]-z[0,1:end+1,:2],0).tolist()
        item['pass'] = all(np.all(np.asarray(item[k+'_rmse'])<=BASE_LIMITS[k]) for k in BASE_LIMITS)
        rows.append(item)
    baseline_pass = all(r['pass'] for r in rows)
    return dict(execution_domain='DESKTOP_DRY_RUN',evidence_status='PASS' if response_pass and baseline_pass else 'FAIL',
        gate=response_pass and baseline_pass,response_gate=response_pass,baseline_gate=baseline_pass,
        metrics=summary,baseline_rows=rows,Bv_relative_error=b_error,direct_Bv=bv,
        probe_count=len(probes),baseline_count=len(baselines),seeds=sorted({r['seed'] for r in probes}))


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--stage',choices=['fit','confirm'],required=True)
    p.add_argument('--output',type=Path,required=True)
    p.add_argument('--fresh',type=Path)
    args = p.parse_args()
    out = args.output.resolve()
    if args.stage=='fit':
        assert not out.exists() and out.is_relative_to(REPO/'docs/exp')
        out.mkdir(parents=True)
        original = json.loads((SOURCE/'manifest.json').read_text())
        paired_path = SOURCE/'local_models_frozen.json'
        model = dict(next(m for m in json.loads(paired_path.read_text())['models'] if m['name']=='M4'))
        probes, baselines, _ = load_absolute(SOURCE,'train')
        x = np.concatenate([r['absolute'][:-1] for r in baselines])
        y = np.concatenate([r['absolute'][1:] for r in baselines])
        u = np.concatenate([r['u'] for r in baselines])
        ref = x.mean(0)
        A,B = np.asarray(model['A']),np.asarray(model['B'])
        c = np.mean((y-ref)-(x-ref)@A.T-(u[:,None]-BIAS)*B,axis=0)
        all_x = np.concatenate([r['absolute'][:-1] for r in probes+baselines])
        operating = ref.copy()
        operating[:2] = 0.
        model.update(kind='affine',mode='frozen',state_reference=ref.tolist(),input_reference=BIAS,
            c_center=c.tolist(),c_absolute=(ref-A@ref-B*BIAS+c).tolist(),
            operating_reference=operating.tolist(),
            operating_reference_defect=((A-np.eye(24))@(operating-ref)+c).tolist(),
            state_std=np.maximum(all_x.std(0),1e-9).tolist(),train_min=all_x.min(0).tolist(),train_max=all_x.max(0).tolist())
        path = out/'affine_model_frozen.json'
        write(path,dict(execution_domain='DESKTOP_DRY_RUN',evidence_status='NOT_TESTED',model=model,
            checkpoint_sha256=original['checkpoint_sha256'],onnx_sha256=original['onnx_sha256'],
            paired_model_sha256=sha256(paired_path),AB_unchanged=True,train_seed_set=sorted({r['seed'] for r in probes}),
            offset_fit='ordinary mean baseline one-step defect with A/B held fixed',
            requires_fresh_confirmation=True,baseline_limits_SI=BASE_LIMITS,script_sha256=sha256(Path(__file__))))
        frozen = sha256(path)
        result = validate(model,SOURCE)
        result.update(note='Previously exposed held-out cohort: diagnostic only; not authorization for LQR.',model_sha256=frozen)
        write(out/'old_cohort_diagnostic.json',result)
        assert sha256(path)==frozen
        print('[DESKTOP_DRY_RUN] calibrated offset old cohort',result['gate'],result['metrics']['full2s']['nrmse'],flush=True)
    else:
        assert args.fresh is not None
        path = out/'affine_model_frozen.json'
        frozen = sha256(path)
        bundle = json.loads(path.read_text())
        result = validate(bundle['model'],args.fresh)
        assert not set(result['seeds']) & (set(bundle['train_seed_set'])|{190,191})
        result.update(model_sha256=frozen,fresh_data=str(args.fresh.relative_to(REPO)),
            fresh_initial_conditions=True,no_refit=True)
        assert sha256(path)==frozen
        write(out/'fresh_confirmation.json',result)
        print('[DESKTOP_DRY_RUN] fresh affine confirmation',result['gate'],result['metrics']['full2s']['nrmse'],flush=True)


if __name__=='__main__':
    main()
