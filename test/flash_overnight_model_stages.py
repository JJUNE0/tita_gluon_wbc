"""VALIDATION_SIM / DESKTOP_DRY_RUN: gated M4/M5 experiment stage functions.

Production policy/estimator/controller files remain untouched. Sensor coordinates
are unchanged; base-origin physical metrics determine control success.
"""

from concurrent.futures import ProcessPoolExecutor, as_completed
import gzip
import json
from pathlib import Path
import pickle

import numpy as np

from eval_flash_m5_yaw_rate import imu_yaw_rate, SOURCE
from eval_flash_state_learning import StateRunner, STATE_KEYS
from eval_flash_pv_models import REPO, CKPT, prepared_config, write, sha256
from eval_flash_operating_local import BIAS, cases
from eval_flash_stop_release import inputs_for
from eval_flash_constant_hold import metrics as hold_metrics
from analyze_flash_state_learning import state, rms
from analyze_flash_operating_local import evaluate_extended, summarize_all
from analyze_flash_operating_affine import evaluate_affine, BASE_LIMITS
from analyze_flash_stop_local import predict as affine_predict
from analyze_flash_odometry import integrate_path
from eval_flash_fixed_residual_lqr import lqr_gain, limited

M5_ROOT = REPO/'docs/exp/2026-10-15/flash_m5_yaw_rate/full'
KEYS = STATE_KEYS+['yaw_rate','gyro','base_position','base_velocity']
GROUPS = ['bias_only','M4','M5']
CASES = [('zero',0.)]+[('position',v) for v in [-.001,-.0005,.0005,.001]]+[
    ('kick',v) for v in [-.02,-.01,.01,.02]]


class Runner(StateRunner):
    def observe(self):
        result = super().observe()
        d,m = self.sensors,self.env.model
        base = m.body('base_link').id
        position = d.xpos[base].copy()
        jac = np.zeros((3,m.nv))
        self.env.mujoco.mj_jac(m,d,jac,None,position,base)
        yaw = result['rpy'][2]
        result.update(yaw_rate=np.asarray([imu_yaw_rate(result['rpy'],result['gyro'])]),
            base_position=position,base_velocity=np.asarray([(jac@d.qvel)@[np.cos(yaw),np.sin(yaw),0.]]))
        return result

    def rollout(self,inputs):
        rows,steps = [],[]
        for i in range(len(inputs)+1):
            rows.append({k:self.observation[k].copy() for k in KEYS})
            failures = self.failures()
            if failures or i==len(inputs):break
            steps.append(self.step(float(inputs[i])))
        result = {k:np.asarray([r[k] for r in rows]) for k in KEYS}
        if steps:
            result.update({k:np.asarray([s[k] for s in steps]) for k in steps[0]})
            np.testing.assert_array_equal(result['previous_action'][:-1],result['history'])
            np.testing.assert_array_equal(result['previous_action'][1:],result['action'])
        return result,failures


def vector(trace):
    old = state(trace)
    return np.concatenate([old[:,:4],trace['yaw_rate'],old[:,4:]],axis=1)


def current(r):
    return np.r_[r.observation['sensor'],r.observation['yaw_rate'],
        r.observation['previous_action'],r.observation['leg_position'],r.observation['leg_velocity']]


def parallel(function,jobs,workers,*args):
    results = []
    with ProcessPoolExecutor(max_workers=workers) as pool:
        futures = [pool.submit(function,job,*args) for job in jobs]
        for future in as_completed(futures):results.append(future.result())
    return results


def stage1(root,plan):
    original = json.loads((M5_ROOT/'summary.json').read_text())
    frozen = M5_ROOT/'models_frozen.json'
    assert sha256(frozen)==original['model_sha256']
    assert json.loads((M5_ROOT/'completion.json').read_text())['evidence_status']=='PASS'
    assert json.loads((M5_ROOT/'analysis_integrity.json').read_text())['evidence_status']=='PASS'
    details = json.loads((M5_ROOT/'prediction_metrics.json').read_text())['models']
    models = json.loads(frozen.read_text())['models']
    direct = json.loads((M5_ROOT/'direct_B.json').read_text())['median'][1]
    gates = {}
    for model in models:
        d = details[model['name']]
        good = all(np.all(np.median(d['horizons'][str(h)]['nrmse'],axis=0)<=.3) for h in [5,25,50,100])
        good = good and np.all(np.median(d['full2s']['nrmse'],axis=0)<=.3)
        good = bool(good and model['B'][1]*direct>0 and abs(model['B'][1]/direct-1)<=.3)
        gates[model['name']] = good
    return dict(gate=all(gates.values()),model_gates=gates,source=str(frozen.relative_to(REPO)),
        source_sha256=sha256(frozen),M5_relative_improvement=original['improvement_gate'],
        note='Current goal gates affine/LQR on model validity, not M5 superiority. Earlier comparison retained.')


def fit_affine(root):
    path = root/'affine_models_frozen.json'
    assert not path.exists()
    source = M5_ROOT/'models_frozen.json'
    models = json.loads(source.read_text())['models']
    absolute,baselines,base_inputs = [],[],[]
    for p in sorted((M5_ROOT).glob('*/results.json')):
        info = json.loads(p.read_text())
        if info['job']['split']!='train':continue
        seen = set()
        for row in info['responses']:
            with np.load(SOURCE/info['job']['id']/row['trace']) as old, np.load(p.parent/row['trace']) as extra:
                z = np.concatenate([state(old)[:,:4],extra['yaw_rate'],state(old)[:,4:]],axis=1)
            with np.load(SOURCE/info['job']['id']/row['baseline']) as old, np.load(p.parent/row['baseline']) as extra:
                b = np.concatenate([state(old)[:,:4],extra['yaw_rate'],state(old)[:,4:]],axis=1)
                base_u = old['actual_u'].copy()
            anchor = b[0,0]
            z[:,0] -= anchor;b[:,0] -= anchor
            absolute.append(z)
            if row['baseline'] not in seen:
                baselines.append(b);base_inputs.append(base_u);seen.add(row['baseline'])
    calibrated = {}
    for model in models:
        ix = model['indices'];n = len(ix)
        x = np.concatenate([b[:-1,ix] for b in baselines])
        y = np.concatenate([b[1:,ix] for b in baselines])
        all_x = np.concatenate([z[:-1,ix] for z in absolute+baselines])
        ref = x.mean(0);A = np.asarray(model['A']);B = np.asarray(model['B'])
        c = np.mean((y-ref)-(x-ref)@A.T-(np.concatenate(base_inputs)[:,None]-BIAS)*B,axis=0)
        reference = ref.copy();reference[:2] = 0.
        calibrated[model['name']] = dict(model,kind='affine',mode='frozen',state_reference=ref.tolist(),
            input_reference=BIAS,c_center=c.tolist(),c_absolute=(ref-A@ref-B*BIAS+c).tolist(),
            operating_reference=reference.tolist(),operating_reference_defect=((A-np.eye(n))@(reference-ref)+c).tolist(),
            state_std=np.maximum(all_x.std(0),1e-9).tolist(),train_min=all_x.min(0).tolist(),train_max=all_x.max(0).tolist())
    write(path,dict(execution_domain='DESKTOP_DRY_RUN',models=calibrated,AB_unchanged=True,
        train_baselines=len(baselines),train_responses=len(absolute),source_sha256=sha256(source),
        checkpoint_sha256=sha256(CKPT/'actor.pt'),train_seeds=[180,181],bias=BIAS,
        offset_fit='baseline mean one-step defect, A/B fixed; no equilibrium extrapolation'))
    return path


def collect_fresh(job,cfg,output):
    out = Path(output)/job['id'];out.mkdir()
    r = Runner(cfg,job)
    try:
        prefix_s = 8. if job['approach']=='zero' else 30.
        tau = 0.
        for i in range(round(prefix_s/.02)):
            if i>=50:assert not r.failures()
            tau = min(.6,tau+.04) if job['approach']=='high' else 0.
            r.step(tau)
        ticks = [round(t/.02) for t in job['times']]
        states,steps,snapshots = [],[],{}
        for i in range(max(ticks)+401):
            assert not r.failures(),(job,i,r.failures())
            states.append({k:r.observation[k].copy() for k in KEYS})
            if i in ticks:
                snapshots[i] = r.snapshot()
                print('[VALIDATION_SIM]',job['id'],'snapshot',i*.02,flush=True)
            if i<max(ticks)+400:
                tau = float(np.clip(BIAS,tau-.04,tau+.04));steps.append(r.step(tau))
        prefix = {k:np.asarray([s[k] for s in states]) for k in KEYS}
        prefix.update({k:np.asarray([s[k] for s in steps]) for k in steps[0]})
        responses,direct,acquisitions = [],[],[]
        limits = r.env.model.jnt_range[r.leg_joints]
        for tick,snapshot in snapshots.items():
            hist = {k:v[tick-12000:tick+1] if k in KEYS else v[tick-12000:tick] for k,v in prefix.items()}
            gate = hold_metrics(hist,limits,True,240.)
            acquisitions.append(dict(start_hold_s=tick*.02,metrics=gate))
            assert gate['operating_gate'],(job,tick,gate)
            with gzip.open(out/f'snapshot_t{tick}.pkl.gz','wb',compresslevel=1) as f:pickle.dump(snapshot,f)
            with gzip.open(out/f'snapshot_t{tick}.pkl.gz','rb') as f:r.restore(pickle.load(f))
            base,failures = r.rollout(np.full(400,BIAS));assert not failures
            for k in KEYS:np.testing.assert_array_equal(base[k],prefix[k][tick:tick+401])
            for k in steps[0]:np.testing.assert_array_equal(base[k],prefix[k][tick:tick+400])
            base_name = f'zero_t{tick}.npz';np.savez_compressed(out/base_name,**base)
            for i,(family,amplitude) in enumerate(cases('test')):
                seed = int(np.random.SeedSequence([job['seed'],job['pitch_index'],tick,i,30619]).generate_state(1)[0])
                request = BIAS+inputs_for(family,amplitude,seed,400)
                r.restore(snapshot);trace,failures = r.rollout(request);assert not failures
                assert max(abs(trace['actual_u']-request))<1e-6
                for k in KEYS:np.testing.assert_array_equal(trace[k][0],base[k][0])
                np.testing.assert_array_equal(trace['action'][0],base['action'][0])
                np.testing.assert_array_equal(trace['policy_observation'][0],base['policy_observation'][0])
                name = f'{family}_a{amplitude:g}_t{tick}.npz';np.savez_compressed(out/name,**trace)
                responses.append(dict(trace=name,baseline=base_name,family=family,amplitude=amplitude,
                    start_hold_s=tick*.02,start_rl_s=prefix_s+tick*.02,input_seed=seed))
            r.restore(snapshot);plus,pf = r.rollout([BIAS+.01])
            r.restore(snapshot);minus,mf = r.rollout([BIAS-.01]);assert not pf and not mf
            np.testing.assert_array_equal(plus['action'][0],minus['action'][0])
            b = (vector(plus)[1]-vector(minus)[1])/(plus['actual_u'][0]-minus['actual_u'][0])
            np.testing.assert_array_equal(b[5:13],np.zeros(8))
            direct.append(dict(start_hold_s=tick*.02,B=b.tolist()))
        # Save the qualification window rather than another entire1200s archive.
        for tick in ticks:
            window = {k:v[tick-12000:tick+1] if k in KEYS else v[tick-12000:tick] for k,v in prefix.items()}
            np.savez_compressed(out/f'qualification_t{tick}.npz',**window)
        write(out/'results.json',dict(execution_domain='VALIDATION_SIM',evidence_status='PASS',job=job,
            acquisitions=acquisitions,responses=responses,direct_B=direct,exact_snapshot_replay=True,F1=False))
        print('[VALIDATION_SIM]',job['id'],'fresh probes',len(responses),flush=True)
        return dict(id=job['id'],responses=len(responses),snapshots=len(snapshots))
    finally:r.env.close()


def validate_fresh(root):
    model_path = root/'affine_models_frozen.json'
    frozen = sha256(model_path);bundle = json.loads(model_path.read_text())
    rows,baselines,direct,seeds = [],[],[],set()
    for p in sorted((root/'fresh').glob('*/results.json')):
        info = json.loads(p.read_text());seeds.add(info['job']['seed']);direct.extend(info['direct_B']);seen = set()
        for row in info['responses']:
            with np.load(p.parent/row['trace']) as a,np.load(p.parent/row['baseline']) as b:
                z,base = vector(a),vector(b);anchor = base[0,0]
                z[:,0] -= anchor;base[:,0] -= anchor
                item = dict(**row,context=info['job']['id'],absolute=z,delta=z-base,u=a['actual_u'].copy(),
                    du=a['actual_u']-b['actual_u'])
                rows.append(item)
                if row['baseline'] not in seen:
                    baselines.append(dict(absolute=base,u=b['actual_u'].copy(),context=info['job']['id'],start_hold_s=row['start_hold_s']))
                    seen.add(row['baseline'])
    assert not seeds & {180,181,190,191,220,221}
    assert len(rows)==204 and len(baselines)==12 and len(direct)==12
    direct_v = float(np.median([r['B'][1] for r in direct]))
    summaries = {}
    for name,model in bundle['models'].items():
        indices = model['indices']
        ab_stats,_ = evaluate_extended(model,np.asarray([r['delta'] for r in rows]),np.asarray([r['du'] for r in rows]))
        selected = [dict(r,absolute=r['absolute'][:,indices],delta=r['delta'][:,indices]) for r in rows]
        af_stats,_ = evaluate_affine(model,selected)
        ab,af = summarize_all(ab_stats),summarize_all(af_stats)
        b_error = abs(model['B'][1]/direct_v-1)
        def prediction_gate(summary):
            return bool(np.all(np.asarray(summary['full2s']['nrmse'])<=.3) and all(
                np.all(np.asarray(summary['horizons'][str(h)]['nrmse'])<=.3) for h in [5,25,50,100]))
        baseline_rows = []
        for b in baselines:
            z = b['absolute'][:,indices][None]
            pred = affine_predict(model,z[:,0],b['u'][None])
            metrics = {f'{h}s':rms(pred[0,1:h*50+1,:2]-z[0,1:h*50+1,:2],0).tolist() for h in [2,8]}
            good = all(np.all(np.asarray(metrics[key])<=value) for key,value in BASE_LIMITS.items())
            baseline_rows.append(dict(context=b['context'],start_hold_s=b['start_hold_s'],rmse=metrics,gate=bool(good)))
        gate = bool(prediction_gate(ab) and prediction_gate(af) and b_error<=.3 and
            model['B'][1]*direct_v>0 and all(b['gate'] for b in baseline_rows))
        summaries[name] = dict(gate=gate,AB=ab,affine=af,Bv_relative_error=float(b_error),
            direct_Bv=direct_v,baselines=baseline_rows)
        print('[DESKTOP_DRY_RUN]',name,'independent affine gate',gate,'first2',af['full2s']['nrmse'],
            'rolling2',af['horizons']['100']['nrmse'],flush=True)
    assert sha256(model_path)==frozen
    return dict(gate=all(m['gate'] for m in summaries.values()),models=summaries,model_sha256=frozen,
        fresh_seeds=sorted(seeds),probes=len(rows),baselines=len(baselines),direct_pairs=len(direct),
        note='Frozen train-only offsets; new seeds not used in any fit. Sensor-state validity; base GT separately evaluated by control.')


def stage2(root,plan):
    path = fit_affine(root)
    frozen = sha256(path)
    fresh = root/'fresh';fresh.mkdir()
    jobs = []
    for seed in [260,261]:
        for i,pitch in enumerate([-.035,0.,.035]):
            approach = 'zero' if (seed+i)%2==0 else 'high'
            jobs.append(dict(id=f's{seed}_p{pitch:+.3f}_{approach}',seed=seed,pitch=pitch,pitch_index=i,
                split='test',approach=approach,times=[1000.,1120.]))
    config = prepared_config(CKPT)
    write(fresh/'manifest.json',dict(execution_domain='VALIDATION_SIM',jobs=jobs,
        checkpoint_sha256=sha256(CKPT/'actor.pt'),onnx_sha256=sha256(config.parent/'policy.onnx'),
        frozen_before_collection=frozen,probe_s=8,bias=BIAS,F1=False,base_point='base_link origin'))
    results = parallel(collect_fresh,jobs,plan['workers'],json.loads(config.read_text()),str(fresh))
    assert sha256(path)==frozen
    write(fresh/'completion.json',dict(execution_domain='VALIDATION_SIM',evidence_status='PASS',results=results))
    return validate_fresh(root)
