"""VALIDATION_SIM: constrained M4 RLS, never connected to the control gain.

Training uses only synchronized sensor state and commanded residual. Full A/B/c
and B/c-only candidates are both retained; the full constrained model is primary.
Independent physical branches evaluate its torque response after coefficients
are frozen. The baseline command is held fixed during these validation forks.
"""

import copy
import gzip
import json
from pathlib import Path
import pickle

import numpy as np

from m4_mismatch_stages import PREVIOUS, apply_physics_effect, jobs
from flash_overnight_control_stages import EffectRunner
from flash_overnight_model_stages import (REPO, CKPT, BIAS, KEYS, current, vector,
    limited, parallel, prepared_config, write, sha256)
from analyze_flash_state_learning import evaluate, summarize, state
from eval_flash_stop_release import inputs_for

IX = [0,1,2,3]+list(range(5,25))


class ConstrainedRLS:
    """Position-translation invariant affine RLS with causal action B rows zero."""
    def __init__(self, model, partial=False, forgetting=.9995, prior_covariance=100.):
        self.original=copy.deepcopy(model)
        self.ref=np.asarray(model['state_reference'])
        floor=np.r_[.0001,.001,.001,.01,np.full(8,.05),np.full(6,.01),np.full(6,.05)]
        self.scale=np.maximum(model['state_std'],floor)
        self.A=np.asarray(model['A']).copy();self.B=np.asarray(model['B']).copy()
        self.c=np.asarray(model['c_center']).copy()
        self.partial=partial;self.forgetting=forgetting;self.count=0
        self.groups=[];self.features=[];self.history=[]
        # A's first column remains [1,0,...]. Actions at t are computed before u[t].
        for action in [False,True]:
            rows=np.arange(4,12) if action else np.r_[np.arange(4),np.arange(12,24)]
            columns=([] if partial else list(range(23)))+([] if action else [23])+[24]
            theta=np.column_stack([self.A[:,1:]*self.scale[None,1:]/self.scale[:,None],
                self.B*.05/self.scale,self.c/self.scale])[np.ix_(rows,columns)]
            self.groups.append(dict(rows=rows,columns=columns,theta=theta,
                P=np.eye(len(columns))*prior_covariance))

    def update(self, z, u, next_z):
        x=(np.asarray(z)-self.ref)/self.scale
        y=(np.asarray(next_z)-self.ref)/self.scale
        target=y.copy();target[0]-=x[0]
        if self.partial:target-=x[1:]@(self.A[:,1:]*self.scale[None,1:]/self.scale[:,None]).T
        feature=np.r_[x[1:],(u-BIAS)/.05,1.]
        if not np.isfinite(np.r_[target,feature]).all():raise FloatingPointError('Nonfinite sensor sample')
        self.features.append(feature)
        for g in self.groups:
            p=feature[g['columns']];P=g['P'];q=P@p
            gain=q/(self.forgetting+p@q)
            g['theta']+=np.outer(target[g['rows']]-g['theta']@p,gain)
            P=(P-np.outer(gain,q))/self.forgetting
            g['P']=(P+P.T)*.5
            if not np.isfinite(g['theta']).all() or not np.isfinite(g['P']).all():
                raise FloatingPointError('Nonfinite RLS coefficient/covariance')
        self.count+=1
        if self.count%50==0:
            frozen=self.model();self.history.append(dict(step=self.count,B_v=frozen['B'][1],
                covariance_trace=sum(float(np.trace(g['P'])) for g in self.groups)))

    def model(self):
        A=self.A.copy();B=self.B.copy();c=self.c.copy()
        for g in self.groups:
            rows=g['rows']
            for j,col in enumerate(g['columns']):
                value=g['theta'][:,j]*self.scale[rows]
                if col<23:A[rows,col+1]=value/self.scale[col+1]
                elif col==23:B[rows]=value/.05
                else:c[rows]=value
        B[4:12]=0.
        result=copy.deepcopy(self.original)
        result.update(A=A.tolist(),B=B.tolist(),c_center=c.tolist(),
            c_absolute=(self.ref-A@self.ref-B*BIAS+c).tolist(),indices=list(range(24)),
            update_count=self.count,mode='B/c only' if self.partial else 'constrained full A/B/c')
        return result

    def diagnostics(self):
        x=np.asarray(self.features);energy=np.sqrt(np.mean(x*x,axis=0))
        scaled=x/np.maximum(energy,1e-12)
        singular=np.linalg.svd(scaled,compute_uv=False)
        rank=int(np.sum(singular>singular[0]*1e-8))
        other=np.delete(scaled,23,axis=1);input_=scaled[:,23]
        innovation=input_-other@np.linalg.lstsq(other,input_,rcond=1e-8)[0]
        fraction=float(innovation@innovation/max(input_@input_,1e-20))
        minimum=min(float(np.linalg.eigvalsh(g['P']).min()) for g in self.groups)
        condition=float(singular[0]/max(singular[-1],1e-300))
        return dict(samples=self.count,rank=rank,regressors=25,scaled_condition=condition,
            singular_values=singular.tolist(),input_innovation_fraction=fraction,
            covariance_min_eigenvalue=minimum,forgetting=self.forgetting,prior_covariance=100.,
            gate=bool(rank==25 and condition<=1e6 and fraction>=.01 and minimum>0. and self.count>=250),
            note='Conservative information gate for full updates; prediction accuracy is separately required.')


class ShadowRunner(EffectRunner):
    def effect_snapshot(self):
        return self.snapshot(),self.motor_state.copy()

    def effect_restore(self,snapshot):
        self.restore(snapshot[0]);self.motor_state=snapshot[1].copy()


def reproduce(r,job,root):
    if job['regime']=='settled':
        with gzip.open(PREVIOUS/'fresh'/job['source_id']/'snapshot_t50000.pkl.gz','rb') as f:r.restore(pickle.load(f))
    else:
        for i in range(400):
            if i>=50:assert not r.failures()
            r.step(0.)
    apply_physics_effect(r,job['effect']);r.enable_effect(job['effect'])
    path=root/'mismatch'/job['id']/'M4.npz'
    with np.load(path) as archive:
        assert len(archive['sensor'])==3001
        for i in range(3001):
            for key in KEYS:np.testing.assert_array_equal(r.observation[key],archive[key][i])
            if i<3000:
                tr=r.step(float(archive['requested_u'][i]))
                for key,value in tr.items():np.testing.assert_array_equal(value,archive[key][i])
        return float(archive['actual_u'][-1])


def train_one(r,model,gain,seed):
    rls=ConstrainedRLS(model);partial=ConstrainedRLS(model,partial=True)
    start=r.effect_snapshot();p_target=float(r.observation['sensor'][0])
    noise=inputs_for('train_prbs',.02,seed,3000)
    states=[];steps=[];raw=[];extra=[];previous=0.
    for i in range(3001):
        states.append({k:r.observation[k].copy() for k in KEYS})
        if i==3000 or r.failures():break
        z=current(r)[IX].copy();z[0]-=p_target
        feedback=float(-np.asarray(gain['K'])@(z-gain['reference']))
        # Exploration shares the existing total correction cap/ramp/slew.
        correction=limited(feedback+noise[i],previous,i*.02);previous=correction
        tr=r.step(BIAS+correction);next_z=current(r)[IX].copy();next_z[0]-=p_target
        rls.update(z,tr['actual_u'],next_z);partial.update(z,tr['actual_u'],next_z)
        steps.append(tr);raw.append(feedback);extra.append(correction)
    trace={k:np.asarray([s[k] for s in states]) for k in KEYS}
    trace.update({k:np.asarray([s[k] for s in steps]) for k in steps[0]})
    trace.update(raw_correction=np.asarray(raw),correction=np.asarray(extra),requested_probe=noise[:len(steps)])
    completed=len(steps)==3000 and not r.failures()
    # Learning-disabled replay of the exact commands must leave the plant identical.
    r.effect_restore(start)
    for i in range(len(steps)+1):
        for key in KEYS:np.testing.assert_array_equal(r.observation[key],trace[key][i])
        if i<len(steps):
            for key,value in r.step(float(trace['requested_u'][i])).items():
                np.testing.assert_array_equal(value,trace[key][i])
    return rls,partial,trace,completed


def prediction_gate(model,data,u,direct_v):
    stats=evaluate(model,np.asarray(data),np.asarray(u));summary=summarize(stats)
    b_error=float(abs(model['B'][1]/direct_v-1))
    passed=bool(np.all(np.asarray(summary['full2s']['nrmse'])<=.3) and all(
        np.all(np.asarray(summary['horizons'][str(h)]['nrmse'])<=.3) for h in [5,25,50,100])
        and model['B'][1]*direct_v>0 and b_error<=.3)
    return dict(gate=passed,prediction=summary,B_v=model['B'][1],direct_B_v=direct_v,B_relative_error=b_error)


def shadow_job(pair,cfg,output,root,model,gain):
    out=Path(output)/pair['id'];out.mkdir();root=Path(root)
    train=ShadowRunner(cfg,pair['train'])
    try:
        reproduce(train,pair['train'],root)
        rls,partial,trace,complete=train_one(train,model,gain,pair['train']['seed']+9713)
        np.savez_compressed(out/'training.npz',**trace)
        full_model,small_model=rls.model(),partial.model()
        model_file=out/'models_frozen.json'
        write(model_file,dict(full=full_model,partial=small_model,history=rls.history,
            diagnostics=rls.diagnostics(),training_complete=complete,
            sensor_only=True,learning_disabled_exact_replay=True))
        frozen=sha256(model_file)
    finally:train.env.close()
    test=ShadowRunner(cfg,pair['test'])
    try:
        hold=reproduce(test,pair['test'],root);snapshot=test.effect_snapshot()
        base,fail=test.rollout(np.full(200,hold));assert not fail
        np.savez_compressed(out/'baseline.npz',**base)
        cases=['validation_sine','validation_prbs','pulse_pos','pulse_neg','step_pos','step_neg','bipulse_pos','bipulse_neg']
        data=[];inputs=[];rows=[]
        for i,family in enumerate(cases):
            probe=inputs_for(family,.02,pair['test']['seed']+8837+i,200)
            request=np.clip(hold+probe,BIAS-.05,BIAS+.05)
            test.effect_restore(snapshot);response,fail=test.rollout(request);assert not fail
            delta=state(response)-state(base);du=response['actual_u']-base['actual_u']
            np.testing.assert_array_equal(delta[0],np.zeros(24))
            np.testing.assert_array_equal(response['action'][0],base['action'][0])
            data.append(delta);inputs.append(du)
            np.savez_compressed(out/(family+'.npz'),**response)
            rows.append(dict(family=family,probe_peak=float(max(abs(du)))))
        direct=[]
        for sign in [1.,-1.]:
            test.effect_restore(snapshot)
            value=float(np.clip(hold+sign*.01,BIAS-.05,BIAS+.05))
            response,fail=test.rollout([value]);assert not fail;direct.append(response)
        denominator=direct[0]['actual_u'][0]-direct[1]['actual_u'][0]
        assert denominator>.001
        B=(state(direct[0])[1]-state(direct[1])[1])/denominator
        np.testing.assert_array_equal(B[4:12],np.zeros(8))
        output_models={name:prediction_gate(m,data,inputs,float(B[1])) for name,m in
            [('full',full_model),('partial',small_model),('nominal',dict(model,indices=list(range(24))))]}
        full_pass=bool(complete and rls.diagnostics()['gate'] and output_models['full']['gate'])
        assert sha256(model_file)==frozen
        result=dict(gate=full_pass,pair=pair,models=output_models,information=rls.diagnostics(),
            training_complete=complete,training_steps=rls.count,no_gain_updates=True,
            learning_disabled_replay_exact=True,independent_initial_conditions=True,
            measured_direct_B=B.tolist(),validation_responses=rows,frozen_sha256=frozen,
            input_definition='commanded total residual, before unknown wheel gain/lag; no GT or effect label in RLS',
            validation_baseline_command=hold,outer_LQR_disabled_in_both_validation_forks=True)
        write(out/'results.json',result)
        print('[VALIDATION_SIM] shadow',pair['id'],'PASS' if full_pass else 'FAIL',flush=True)
        return result
    finally:test.env.close()


def run_shadow(root,plan,eligible,source_root=None):
    out=root/'shadow';out.mkdir()
    source_root=Path(source_root) if source_root is not None else root
    model=json.loads((PREVIOUS/'affine_models_frozen.json').read_text())['models']['M4']
    gain=json.loads((PREVIOUS/'gains_frozen.json').read_text())['models']['M4']
    all_jobs=jobs();pairs=[]
    for condition in eligible:
        regime,name=condition.split('/')
        selected=[j for j in all_jobs if j['regime']==regime and j['condition']==name]
        seeds=sorted({j['seed'] for j in selected});assert len(seeds)==2
        for pitch in [-.035,0.,.035]:
            a=next(j for j in selected if j['seed']==seeds[0] and j['pitch']==pitch)
            b=next(j for j in selected if j['seed']==seeds[1] and j['pitch']==pitch)
            pairs.append(dict(id=f'{regime}_{name}_p{pitch:+.3f}',condition=condition,train=a,test=b))
    manifest=dict(execution_domain='VALIDATION_SIM',pairs=pairs,primary='full constrained A/B/c RLS',
        comparison='B/c only; A fixed; no model selection after validation',duration_s=60.,
        exploration_total_peak=.02,shared_correction_cap=.05,forgetting=.9995,prior_covariance=100.,
        information_gate='rank25 at relative1e-8, RMS-scaled condition<=1e6, input innovation>=1%, positive finite P, samples>=250',
        independent_prediction_gate=plan['shadow_gate'],models_frozen_before_test=True,
        covariance_state_scaling='max(nominal std, [0.1mm,1mm/s,1mrad,0.01rad/s,action0.05,legq0.01,legdq0.05])',
        no_effect_label_or_GT_training=True,no_control_gain_updates=True,
        mismatch_source=str(source_root),
        source_sha256={str(p):sha256(p) for pair in pairs for job in [pair['train'],pair['test']]
            for p in [source_root/'mismatch'/job['id']/'M4.npz',source_root/'mismatch'/job['id']/'results.json']})
    write(out/'manifest.json',manifest)
    cfg=json.loads(prepared_config(CKPT).read_text())
    results=parallel(shadow_job,pairs,plan['workers'],cfg,str(out),str(source_root),model,gain)
    for p,h in manifest['source_sha256'].items():assert sha256(Path(p))==h,p
    conditions={}
    for condition in eligible:
        rows=[r for r in results if r['pair']['condition']==condition]
        conditions[condition]=dict(gate=bool(len(rows)==3 and all(r['gate'] for r in rows)),
            prediction_pass_count=sum(r['models']['full']['gate'] for r in rows),
            information_pass_count=sum(r['information']['gate'] for r in rows),pairs=len(rows))
    write(out/'all_results.json',dict(rows=results))
    # Adaptive application is eligible only in explicitly validated conditions.
    passing=[k for k,v in conditions.items() if v['gate']]
    return dict(gate=bool(passing),all_conditions_pass=all(v['gate'] for v in conditions.values()),
        conditions=conditions,eligible_for_adaptive=passing,pairs=len(results),
        full_validation_status='PASS' if all(v['gate'] for v in conditions.values()) else 'FAIL',
        note='Top gate means at least one specific condition allows conditional adaptive validation, not global ID success.')
