"""VALIDATION_SIM: fresh affine confirmation and reusable whole-state snapshots."""

import argparse
from concurrent.futures import ProcessPoolExecutor, as_completed
import gzip
import json
from pathlib import Path
import pickle

import numpy as np

from eval_flash_operating_local import StateRunner, STATE_KEYS, BIAS, REPO, CKPT, cases
from eval_flash_pv_models import prepared_config, write, sha256
from eval_flash_constant_hold import metrics as hold_metrics
from eval_flash_stop_release import inputs_for
from analyze_flash_state_learning import state


def collect(cfg,job,output):
    out = Path(output)/job['id']
    out.mkdir()
    r = StateRunner(cfg,job)
    try:
        prefix_s = 8. if job['approach']=='zero' else 30.
        tau = 0.
        startup = []
        for tick in range(round(prefix_s/.02)):
            failures = r.failures()
            if tick<50:
                if failures:startup.append(dict(tick=tick,failures=failures))
            else:
                assert not failures,(job,tick,failures)
            tau = min(.6,tau+.04) if job['approach']=='high' else 0.
            r.step(tau)
        rows,steps,snapshots = [],[],{}
        ticks = [round(t/.02) for t in job['times']]
        for tick in range(max(ticks)+401):
            assert not r.failures(),(job,tick,r.failures())
            rows.append({k:r.observation[k].copy() for k in STATE_KEYS})
            if tick in ticks:snapshots[tick]=r.snapshot()
            if tick<max(ticks)+400:
                tau = float(np.clip(BIAS,tau-.04,tau+.04))
                steps.append(r.step(tau))
        prefix = {k:np.asarray([v[k] for v in rows]) for k in STATE_KEYS}
        prefix.update({k:np.asarray([v[k] for v in steps]) for k in steps[0]})
        np.savez_compressed(out/'prefix.npz',**prefix)
        acquisitions,responses,direct = [],[],[]
        limits = r.env.model.jnt_range[r.leg_joints]
        for tick,snapshot in snapshots.items():
            history = {k:v[tick-12000:tick+1] if k in STATE_KEYS else v[tick-12000:tick] for k,v in prefix.items()}
            gate = hold_metrics(history,limits,True,240.)
            acquisitions.append(dict(start_hold_s=tick*.02,start_rl_s=prefix_s+tick*.02,metrics=gate))
            assert gate['operating_gate'],(job,tick,gate)
            snapshot_path = out/f'snapshot_t{tick}.pkl.gz'
            with gzip.open(snapshot_path,'wb',compresslevel=1) as f:pickle.dump(snapshot,f)
            with gzip.open(snapshot_path,'rb') as f:restored=pickle.load(f)
            r.restore(restored)
            baseline,failures = r.rollout(np.full(400,BIAS))
            assert not failures
            for k in STATE_KEYS:
                np.testing.assert_array_equal(baseline[k],prefix[k][tick:tick+401])
            for k in steps[0]:
                np.testing.assert_array_equal(baseline[k],prefix[k][tick:tick+400])
            base_name = f'zero_t{tick}.npz'
            np.savez_compressed(out/base_name,**baseline)
            for i,(family,amplitude) in enumerate(cases('test')):
                seed = int(np.random.SeedSequence([job['seed'],job['pitch_index'],tick,i,19410]).generate_state(1)[0])
                probe = inputs_for(family,amplitude,seed,400)
                r.restore(snapshot)
                trace,failures = r.rollout(BIAS+probe)
                assert not failures and len(trace['sensor'])==401
                assert max(abs(trace['actual_u']-trace['requested_u']))<1e-6
                np.testing.assert_array_equal(trace['action'][0],baseline['action'][0])
                for k in STATE_KEYS:np.testing.assert_array_equal(trace[k][0],baseline[k][0])
                name = f'{family}_a{amplitude:g}_t{tick}.npz'
                np.savez_compressed(out/name,**trace)
                responses.append(dict(trace=name,baseline=base_name,family=family,amplitude=amplitude,
                    start_rl_s=prefix_s+tick*.02,start_hold_s=tick*.02,bias=BIAS,input_seed=seed))
            r.restore(snapshot);plus,pf=r.rollout([BIAS+.01])
            r.restore(snapshot);minus,mf=r.rollout([BIAS-.01])
            assert not pf and not mf
            np.testing.assert_array_equal(plus['action'][0],minus['action'][0])
            du = plus['actual_u'][0]-minus['actual_u'][0]
            direct.append(dict(start_hold_s=tick*.02,amplitude=.01,
                sensor_B=((state(plus)[1]-state(minus)[1])/du).tolist(),
                gt_B=((plus['gt'][1]-minus['gt'][1])/du).tolist()))
        write(out/'results.json',dict(execution_domain='VALIDATION_SIM',evidence_status='PASS',job=job,
            acquisitions=acquisitions,responses=responses,direct_B=direct,startup_violations=startup,
            snapshot_serialization_exact=True,F1_enabled=False,model_used_for_control=False))
        result = dict(id=job['id'],responses=len(responses),snapshots=len(snapshots),direct_pairs=len(direct))
        print('[VALIDATION_SIM]',result,flush=True)
        return result
    finally:
        r.env.close()


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--model',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True)
    p.add_argument('--workers',type=int,default=3)
    args = p.parse_args()
    out = args.output.resolve()
    assert out.is_relative_to(REPO/'docs/exp') and not out.exists()
    out.mkdir(parents=True)
    cfg_path = prepared_config(CKPT)
    bundle = json.loads(args.model.read_text())
    protected = {str(p.relative_to(REPO)):sha256(p) for p in [args.model.resolve(),cfg_path,cfg_path.parent/'policy.onnx',CKPT/'actor.pt',Path(__file__).resolve()]}
    jobs = []
    for seed in [220,221]:
        for i,pitch in enumerate([-.035,0.,.035]):
            approach = 'zero' if (seed+i)%2==0 else 'high'
            jobs.append(dict(id=f'test_s{seed}_p{pitch:+.3f}_{approach}',seed=seed,pitch=pitch,
                pitch_index=i,split='test',approach=approach,times=[1000.,1120.]))
    write(out/'manifest.json',dict(execution_domain='VALIDATION_SIM',checkpoint_sha256=bundle['checkpoint_sha256'],
        onnx_sha256=bundle['onnx_sha256'],protected_sha256=protected,jobs=jobs,
        fitted_before_collection=True,F1_enabled=False,bias=BIAS,role='fresh affine test; no fitting or LQR',
        source_sha256=sha256(Path(__file__))))
    results = []
    with ProcessPoolExecutor(max_workers=args.workers) as pool:
        futures = [pool.submit(collect,json.loads(cfg_path.read_text()),job,str(out)) for job in jobs]
        for future in as_completed(futures):results.append(future.result())
    assert all(sha256(REPO/p)==h for p,h in protected.items())
    write(out/'completion.json',dict(execution_domain='VALIDATION_SIM',evidence_status='PASS',results=results,
        protected_hashes_preserved=True,probes=sum(r['responses'] for r in results),
        snapshots=sum(r['snapshots'] for r in results),direct_pairs=sum(r['direct_pairs'] for r in results)))


if __name__=='__main__':
    main()
