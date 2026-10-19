"""VALIDATION_SIM / DESKTOP_DRY_RUN: diagnose bias, limiting and online models.

Existing controllers, models, evidence and success criteria are read-only.
Previously unsaved RLS candidates are reconstructed from the original causal
streams and checked against every recorded gain. New physical branches use
prescribed torques only; no new controller or gain tuning is introduced.
"""
import argparse
import copy
import hashlib
import json
from pathlib import Path
import subprocess
from types import SimpleNamespace

import numpy as np

from m4_mismatch_stages import PREVIOUS
from m4_shadow_stages import ConstrainedRLS, ShadowRunner, reproduce
from m4_adaptive_stages import GainMonitor
from flash_overnight_model_stages import REPO, CKPT, BIAS, KEYS, parallel, prepared_config, write, sha256, limited
from analyze_flash_state_learning import state, evaluate, summarize
from eval_flash_stop_release import inputs_for

OLD=REPO/'docs/exp/2026-10-16/m4_followup_pipeline'
COLD=OLD/'cold_adaptive/adaptive'
WARM=OLD/'run_final/adaptive'
LEGS=[0,1,2,4,5,6]


def arrays(path):
    with np.load(path) as z:return {k:z[k].copy() for k in z}


def nominal():
    return json.loads((PREVIOUS/'affine_models_frozen.json').read_text())['models']['M4']


def fixed_gain():
    return json.loads((PREVIOUS/'gains_frozen.json').read_text())['models']['M4']


def defect(model,zref,rref=BIAS):
    A,B=np.asarray(model['A']),np.asarray(model['B'])
    ref=np.asarray(model['state_reference'])
    c=np.asarray(model['c_center'])
    # Centered evaluation avoids cancellation of large nonzero internal states.
    return (A-np.eye(len(B)))@(np.asarray(zref)-ref)+B*(rref-BIAS)+c


def steady_error(model,K,zref):
    A,B=np.asarray(model['A']),np.asarray(model['B']);K=np.asarray(K)
    M=np.eye(len(B))-A+np.outer(B,K)
    d=defect(model,zref);error=np.linalg.solve(M,d)
    residual_input=float(BIAS-K@error)
    return dict(error=error.tolist(),input=residual_input,defect=d.tolist(),condition=float(np.linalg.cond(M)),
        spectral_radius=float(max(abs(np.linalg.eigvals(A-np.outer(B,K))))),
        equation_residual=float(np.linalg.norm(M@error-d)),
        interpretation='Algebraic unconstrained affine prediction, not a verified physical equilibrium.')


def applied_gains(after,K0):
    """K recorded AFTER transition t applies to transition t+1."""
    return np.vstack([K0,np.asarray(after)[:-1]])


def limit_sequence(raw):
    previous=0.;result=[]
    for i,x in enumerate(raw):
        previous=limited(float(x),previous,i*.02);result.append(previous)
    return np.asarray(result)


def torque_metrics(fixed,adaptive,gain):
    K0=np.asarray(gain['K']);ka=applied_gains(adaptive['gain_K_after_step'],K0)
    xf=state(fixed);xa=state(adaptive)
    xf[:,0]-=xf[0,0];xa[:,0]-=xa[0,0]
    ef=xf[:-1]-gain['reference'];ea=xa[:-1]-gain['reference']
    rf=-ef@K0;ra=-np.einsum('ij,ij->i',ka,ea)
    np.testing.assert_allclose(rf,fixed['raw_correction'],atol=1e-10,rtol=1e-10)
    np.testing.assert_allclose(ra,adaptive['raw_correction'],atol=1e-10,rtol=1e-10)
    np.testing.assert_allclose(limit_sequence(rf),fixed['correction'],atol=1e-10)
    np.testing.assert_allclose(limit_sequence(ra),adaptive['correction'],atol=1e-10)
    # Same-state counterfactual isolates K changes from trajectory divergence.
    counter_raw=-np.einsum('ij,ij->i',ka,ef);counter=limit_sequence(counter_raw)
    delta=adaptive['actual_u']-fixed['actual_u'];weights=np.asarray(nominal()['state_std'])
    windows={}
    for label,start,end in [('full',0,3000),('first10s',0,500),('after10s',500,3000),('last5s',2750,3000)]:
        s=slice(start,end);rows={}
        for name,z,e in [('Fixed',fixed,ef),('Adaptive',adaptive,ea)]:
            correction=z['actual_u'][s]-BIAS
            q=250000.*np.sum(e[s,:2]**2,axis=1)
            u=400.*correction**2
            rows[name]=dict(raw_over_cap_fraction=float(np.mean(abs(z['raw_correction'][s])>.05)),
                actual_at_cap_fraction=float(np.mean(abs(z['correction'][s])>=.05-1e-8)),
                mean_residual=float(np.mean(z['actual_u'][s])),
                residual_RMS=float(np.sqrt(np.mean(z['actual_u'][s]**2))),
                wheel_RMS=float(np.sqrt(np.mean(z['physical_motor'][s,:,[3,7]]**2))),
                sensor_Q_cost=float(.02*np.sum(q)),residual_R_cost=float(.02*np.sum(u)),
                Q_plus_R_cost=float(.02*np.sum(q+u)),
                base_IAE=float(np.trapz(abs(z['base_path'][start:end+1]),dx=.02)),
                base_velocity_RMS=float(np.sqrt(np.mean(z['base_velocity'][s]**2))))
        windows[label]=dict(groups=rows,residual_difference_RMS=float(np.sqrt(np.mean(delta[s]**2))),
            residual_difference_peak=float(max(abs(delta[s]))),
            same_state_raw_K_effect_RMS=float(np.sqrt(np.mean((counter_raw[s]-rf[s])**2))),
            same_state_limited_K_effect_RMS=float(np.sqrt(np.mean((counter[s]-fixed['correction'][s])**2))))
    changes=np.flatnonzero(abs(delta)>1e-7)
    return dict(windows=windows,first_actual_residual_difference_s=float(changes[0]*.02) if len(changes) else None,
        final_scaled_K_change=float(np.linalg.norm((ka[-1]-K0)*weights)/np.linalg.norm(K0*weights)),
        final_unscaled_K_change=float(np.linalg.norm(ka[-1]-K0)/np.linalg.norm(K0)),
        first7s_motor_exact=bool(np.array_equal(fixed['physical_motor'][:350],adaptive['physical_motor'][:350])),
        K_time_alignment='after[t] is used at t+1',cost_definition='dt sum Qp*sensor_p_error^2+Qv*sensor_v^2+R*(actual_u-bias)^2')


def reconstruct_case(item,output):
    out=Path(output)/item['id'];out.mkdir()
    model=nominal();gain=fixed_gain();rls=ConstrainedRLS(model)
    prefix=arrays(COLD/item['id']/'common_identification_prefix.npz')
    z=state(prefix);z[:,0]-=z[0,0]
    for i,u in enumerate(prefix['actual_u']):rls.update(z[i],u,z[i+1])
    prefix_model=rls.model()
    adaptive=arrays(COLD/item['id']/'Adaptive_M4.npz');fixed=arrays(COLD/item['id']/'M4.npz')
    fake=SimpleNamespace(observation={k:adaptive[k][0] for k in KEYS})
    monitor=GainMonitor(fake,rls,copy.deepcopy(gain),model,float(adaptive['sensor'][0,0]))
    models=[];max_difference=0.
    for i,u in enumerate(adaptive['actual_u']):
        before=monitor.state();pending=monitor.pending;old_count=len(monitor.events)
        fake.observation={k:adaptive[k][i+1] for k in KEYS}
        monitor.update(before,dict(actual_u=float(u)))
        max_difference=max(max_difference,float(max(abs(np.asarray(monitor.gain['K'])-adaptive['gain_K_after_step'][i]))))
        if len(monitor.events)>old_count:
            models.append(dict(created_step=pending['created'],decision_step=monitor.count,
                accepted=monitor.events[-1]['accepted'],model=pending['model'],K_after=copy.deepcopy(monitor.gain['K'])))
    old=json.loads((COLD/item['id']/'gain_updates.json').read_text())
    assert len(monitor.events)==len(old['events']) and monitor.accepted==old['accepted']
    assert max_difference<1e-7,max_difference
    for a,b in zip(monitor.events,old['events']):
        assert (a['created_step'],a['decision_step'],a['accepted'])==(b['created_step'],b['decision_step'],b['accepted'])
        np.testing.assert_allclose(a['future_2s_pv_RMSE'],b['future_2s_pv_RMSE'],rtol=1e-8,atol=1e-13)
    write(out/'recovered_models.json',dict(prefix=prefix_model,candidates=models,final=rls.model(),
        gain_replay_max_difference=max_difference,events_reproduced=True,no_refit_on_new_data=True))
    metrics=torque_metrics(fixed,adaptive,gain)
    # Evaluate both K values on each SAME model to separate forcing from gain.
    refs=np.asarray(gain['reference']);defects=[]
    support=state(prefix);support[:,0]-=support[0,0]
    za=state(adaptive);za[:,0]-=za[0,0]
    for row in models:
        m=row['model'];tick=row['decision_step'];observed=np.vstack([support,za[:tick+1]])
        lower,upper=observed.min(0),observed.max(0)
        d=defect(m,refs);scale=ConstrainedRLS(m).scale;B=np.asarray(m['B'])
        db=d/scale;bs=B/scale;dr=-float(bs@db/(bs@bs))
        predictions={}
        for label,K in [('Fixed_K',gain['K']),('Adopted_K',row['K_after'])]:
            pred=steady_error(m,K,refs);eq=np.asarray(pred['error'])+refs
            pred['hidden_coordinates_inside_past_range']=int(np.sum((eq[1:]>=lower[1:])&(eq[1:]<=upper[1:])))
            pred['hidden_coordinate_count']=23;pred['input_inside_command_cap']=bool(abs(pred['input']-BIAS)<=.05)
            predictions[label]=pred
        tail=za[2750:3000].mean(0);u=float(adaptive['actual_u'][2750:3000].mean())
        defects.append(dict(created_step=row['created_step'],decision_step=tick,
            reference_defect=d.tolist(),scaled_reference_defect_norm=float(np.linalg.norm(db)),
            one_step_defect_minimizer_input=BIAS+dr,
            one_step_minimizer_is_not_equilibrium=True,
            scaled_irreducible_defect_norm=float(np.linalg.norm(db+bs*dr)),
            hidden_reference_coordinates_inside_past_range=int(np.sum((refs[1:]>=lower[1:])&(refs[1:]<=upper[1:]))),
            empirical_tail_model_defect=defect(m,tail,u).tolist(),predicted_steady=predictions))
    write(out/'log_diagnostics.json',dict(item=item,torque=metrics,affine=defects,
        gain_reconstruction_max_difference=max_difference))
    print('[DESKTOP_DRY_RUN] reconstructed',item['id'],max_difference,flush=True)
    return dict(id=item['id'],condition=item['condition'],torque=metrics,affine=defects)


def replay(r,trace,snapshots=()):
    saved={}
    for i in range(len(trace['actual_u'])+1):
        for key in KEYS:np.testing.assert_array_equal(r.observation[key],trace[key][i])
        if i in snapshots:saved[i]=r.effect_snapshot()
        if i<len(trace['actual_u']):
            transition=r.step(float(trace['requested_u'][i]))
            for key,value in transition.items():np.testing.assert_array_equal(value,trace[key][i])
    return saved


def hold_metrics(trace):
    n=len(trace['actual_u']);t=np.arange(n+1)*.02
    from analyze_flash_odometry import integrate_path
    base=integrate_path(trace['base_position'],trace['rpy'][:,2]);axle=integrate_path(trace['position'],trace['rpy'][:,2])
    rows={}
    for label,start in [('first10s',0.),('middle10s',10.),('last10s',20.)]:
        mask=(t>=start)&(t<start+10.)
        rows[label]=dict(base_velocity_mean=float(np.mean(trace['base_velocity'][mask])),
            base_velocity_RMS=float(np.sqrt(np.mean(trace['base_velocity'][mask]**2))),
            sensor_velocity_mean=float(np.mean(trace['sensor'][mask,1])),base_position_range=float(np.ptp(base[mask])))
    return dict(windows=rows,base_final_path=float(base[-1]),axle_final_path=float(axle[-1]),
        max_planar_drift=float(max(np.linalg.norm(trace['base_position'][:,:2]-trace['base_position'][0,:2],axis=1))),
        pitch_std=float(np.std(trace['sensor'][t>=20.,2])),yaw_change=float(np.unwrap(trace['rpy'][:,2])[-1]-trace['rpy'][0,2]))


def validate_models(models,data,inputs,direct):
    result={}
    for label,model in models.items():
        model=dict(model,indices=list(range(24)))
        summary=summarize(evaluate(model,np.asarray(data),np.asarray(inputs)))
        rel=float(abs(model['B'][1]/direct[1]-1))
        gate=bool(np.all(np.asarray(summary['full2s']['nrmse'])<=.3) and all(
            np.all(np.asarray(summary['horizons'][str(h)]['nrmse'])<=.3) for h in [5,25,50,100])
            and model['B'][1]*direct[1]>0 and rel<=.3)
        result[label]=dict(gate=gate,summary=summary,Bv_error=rel,Bv=model['B'][1],direct_Bv=float(direct[1]))
    return result


def physical_case(item,cfg,output,recovered):
    out=Path(output)/item['id'];out.mkdir();r=ShadowRunner(cfg,item['test'])
    try:
        reproduce(r,item['test'],OLD/'run')
        prefix=arrays(COLD/item['id']/'common_identification_prefix.npz');replay(r,prefix)
        common=r.effect_snapshot()
        adaptive=arrays(COLD/item['id']/'Adaptive_M4.npz');fixed=arrays(COLD/item['id']/'M4.npz')
        snaps=replay(r,adaptive,[350,1600,3000])
        bundle=json.loads((Path(recovered)/item['id']/'recovered_models.json').read_text())
        frozen=sha256(Path(recovered)/item['id']/'recovered_models.json');validations=[]
        for tick,snapshot in snaps.items():
            applicable=[m for m in bundle['candidates'] if m['accepted'] and m['decision_step']<=tick]
            latest=applicable[-1]
            models=dict(nominal=nominal(),prefix=bundle['prefix'],adopted_model=latest['model'])
            if tick==3000:models['latest_RLS']=bundle['final']
            hold=float(adaptive['actual_u'][tick-1]);r.effect_restore(snapshot)
            base,fail=r.rollout(np.full(200,hold));assert not fail
            np.savez_compressed(out/f'baseline_t{tick}.npz',**base)
            deltas=[];inputs=[];probe_rows=[]
            families=['validation_sine','validation_prbs','pulse_pos','pulse_neg','step_pos','step_neg','bipulse_pos','bipulse_neg']
            for i,family in enumerate(families):
                probe=inputs_for(family,.01,190817+item['test']['pitch_index']*31+tick+i,200)
                request=np.clip(hold+probe,BIAS-.05,BIAS+.05)
                r.effect_restore(snapshot);response,fail=r.rollout(request);assert not fail
                np.testing.assert_array_equal(response['action'][0],base['action'][0])
                delta=state(response)-state(base);du=response['actual_u']-base['actual_u']
                np.testing.assert_array_equal(delta[0],np.zeros(24));assert max(abs(du))>1e-5
                deltas.append(delta);inputs.append(du)
                name=f'{family}_t{tick}.npz';np.savez_compressed(out/name,**response)
                probe_rows.append(dict(family=family,trace=name,actual_probe_peak=float(max(abs(du)))))
            direct=[]
            for sign in [1.,-1.]:
                r.effect_restore(snapshot);response,fail=r.rollout([hold+sign*.005]);assert not fail;direct.append(response)
            B=(state(direct[0])[1]-state(direct[1])[1])/(direct[0]['actual_u'][0]-direct[1]['actual_u'][0])
            validations.append(dict(tick=tick,model_created_step=latest['created_step'],model_decision_step=latest['decision_step'],
                hold=hold,models=validate_models(models,deltas,inputs,B),direct_B=B.tolist(),probes=probe_rows))
        # Bias diagnosis: all prescribed constants start from the SAME Fixed endpoint.
        r.effect_restore(common);fixed_snap=replay(r,fixed,[3000])[3000]
        center=float(fixed['actual_u'][2750:3000].mean())
        holds=[]
        for label,u in [('nominal_bias',BIAS),('fixed_tail_input',center),('tail_minus',center-.005),('tail_plus',center+.005)]:
            assert abs(u-BIAS)<=.05
            r.effect_restore(fixed_snap);trace,fail=r.rollout(np.full(1500,u));assert not fail
            np.savez_compressed(out/('hold_'+label+'.npz'),**trace)
            holds.append(dict(label=label,input=u,metrics=hold_metrics(trace)))
        assert sha256(Path(recovered)/item['id']/'recovered_models.json')==frozen
        result=dict(item=item,validation=validations,holds=holds,
            fixed_and_adaptive_full_replay_exact=True,model_hash_unchanged=True,
            no_online_updates_or_feedback_in_new_branches=True)
        write(out/'results.json',result)
        print('[VALIDATION_SIM] diagnostic branches',item['id'],flush=True)
        return result
    finally:r.env.close()


def protected():
    files=[p for p in OLD.rglob('*') if p.is_file()]
    files+=list((REPO/'test').glob('*m4*.py'))
    files+=[PREVIOUS/'affine_models_frozen.json',PREVIOUS/'gains_frozen.json',CKPT/'actor.pt',prepared_config(CKPT)]
    return {str(p.relative_to(REPO)):sha256(p) for p in files if p.name!='diagnose_m4_adaptive_causes.py'}


def verify(plan):
    for name,h in plan['protected_sha256'].items():assert sha256(REPO/name)==h,name


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root',type=Path,required=True)
    parser.add_argument('--stage',choices=['logs','sim'],required=True)
    parser.add_argument('--workers',type=int,default=3)
    args=parser.parse_args();root=args.root.resolve();assert root.is_relative_to(REPO/'docs/exp')
    if args.stage=='logs':
        assert not root.exists();root.mkdir(parents=True)
        items=json.loads((OLD/'run_final/adaptive/manifest.json').read_text())['items']
        plan=dict(execution_domain='VALIDATION_SIM',checkpoint_sha256=sha256(CKPT/'actor.pt'),
            protected_sha256=protected(),workers=args.workers,items=items,
            snapshot_ticks=[350,1600,3000],probe_amplitude=.01,probe_duration_s=4.,constant_duration_s=30.,
            prediction_gate='unchanged: first2s and rolling0.1/0.5/1/2s p/v median NRMSE<=30%,direct Bv sign/error<=30%',
            no_controller_change=True,no_QR_search=True,no_model_refit_on_new_data=True,
            identification_reconstruction='Original causal cold RLS streams; check all gains and future-prediction scores',
            bias_scan='nominal bias, empirical fixed tail input and +/-0.005Nm, same physical Fixed snapshot; finite30s not equilibrium proof',
            script_sha256=sha256(Path(__file__)))
        write(root/'plan.json',plan)
        out=root/'logs';out.mkdir()
        result=parallel(reconstruct_case,items,args.workers,str(out));write(root/'log_results.json',dict(rows=result))
    else:
        plan=json.loads((root/'plan.json').read_text());verify(plan)
        assert sha256(Path(__file__))==plan['script_sha256'],'Collector changed after preregistration'
        out=root/'physical';assert not out.exists();out.mkdir()
        cfg=json.loads(prepared_config(CKPT).read_text())
        result=parallel(physical_case,plan['items'],args.workers,cfg,str(out),str(root/'logs'))
        write(root/'physical_results.json',dict(rows=result))
    verify(plan)
    print('[DESKTOP_DRY_RUN] protected inputs unchanged',len(plan['protected_sha256']),flush=True)


if __name__=='__main__':main()
