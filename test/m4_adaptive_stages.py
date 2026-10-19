"""VALIDATION_SIM: condition-gated online M4 gain candidates and actual comparison."""
import copy
import json
from pathlib import Path

import numpy as np

from m4_mismatch_stages import PREVIOUS
from m4_shadow_stages import ConstrainedRLS, ShadowRunner, reproduce, train_one, IX
from m4_control_utils import rollout_control
from flash_overnight_control_stages import anchor
from flash_overnight_model_stages import CKPT, BIAS, current, parallel, prepared_config, write, sha256, lqr_gain


def checked_gain(model,nominal,gain,current_K,error):
    A,B=np.asarray(model['A']),np.asarray(model['B'])
    candidate,diagnostics=lqr_gain(A,B,model['state_std'],np.asarray(gain['Q']),gain['R'])
    candidate=np.asarray(candidate).reshape(-1)
    # One predetermined small blend; failed candidates are rejected, not tuned.
    blended=.9*np.asarray(current_K)+.1*candidate
    nominal_A,nominal_B=np.asarray(nominal['A']),np.asarray(nominal['B'])
    rho_new=float(max(abs(np.linalg.eigvals(A-np.outer(B,blended)))))
    rho_nominal=float(max(abs(np.linalg.eigvals(nominal_A-np.outer(nominal_B,blended)))))
    jump=float(abs((blended-np.asarray(current_K))@error))
    weights=np.maximum(model['state_std'],1e-9)
    relative=float(np.linalg.norm((blended-np.asarray(gain['K']))*weights)/
        max(np.linalg.norm(np.asarray(gain['K'])*weights),1e-12))
    good=bool(np.isfinite(blended).all() and rho_new<1.-1e-8 and rho_nominal<1.-1e-8 and jump<=.005 and relative<=.25)
    return blended,dict(gate=good,rho_candidate=rho_new,rho_nominal=rho_nominal,
        command_jump_Nm=jump,scaled_gain_change_fraction=relative,DARE=diagnostics)


class GainMonitor:
    """Causal sensor-only candidate validation on the next two seconds of data."""
    def __init__(self,runner,rls,gain,nominal,p_target):
        self.r=runner;self.rls=rls;self.gain=gain;self.nominal=nominal;self.p_target=p_target
        self.pending=None;self.count=0;self.accepted=0;self.events=[];self.K_history=[]

    def state(self):
        z=current(self.r)[IX].copy();z[0]-=self.p_target;return z

    def update(self,before,transition):
        after=self.state();self.count+=1
        self.rls.update(before,transition['actual_u'],after)
        if self.pending is not None:
            p=self.pending;m=p['model'];ref=np.asarray(m['state_reference'])
            p['pred']=ref+np.asarray(m['A'])@(p['pred']-ref)+np.asarray(m['B'])*(transition['actual_u']-BIAS)+m['c_center']
            p['error'].append(p['pred'][:2]-after[:2])
            if len(p['error'])==100:
                error=np.sqrt(np.mean(np.asarray(p['error'])**2,axis=0))
                record=dict(created_step=p['created'],decision_step=self.count,
                    future_2s_pv_RMSE=error.tolist(),information=p['information'],accepted=False)
                try:
                    K,diagnostics=checked_gain(m,self.nominal,self.gain,self.gain['K'],after-self.gain['reference'])
                    record['candidate']=diagnostics
                    if p['information']['gate'] and np.all(error<=[.00002,.00002]) and diagnostics['gate']:
                        self.gain['K']=K.tolist();self.accepted+=1;record['accepted']=True
                except Exception as e:record['rejection']=type(e).__name__+': '+str(e)
                self.events.append(record);self.pending=None
        if self.pending is None and self.count%250==0:
            m=self.rls.model();self.pending=dict(model=m,pred=after.copy(),error=[],created=self.count,
                information=self.rls.diagnostics())
        self.K_history.append(np.asarray(self.gain['K']).copy())


def adaptive_job(item,cfg,output,mismatch_source,nominal,gain):
    out=Path(output)/item['id'];out.mkdir();r=ShadowRunner(cfg,item['test'])
    try:
        reproduce(r,item['test'],Path(mismatch_source))
        shadow_file=Path(item['shadow_directory'])/'models_frozen.json'
        frozen=json.loads(shadow_file.read_text())['full']
        # Common 60s identification prefix: both evaluated controllers receive
        # exactly the same state after this prefix; no controller gets extra data.
        rls,_,prefix,complete=train_one(r,frozen,gain,item['test']['seed']+41093)
        assert complete
        np.savez_compressed(out/'common_identification_prefix.npz',**prefix)
        snapshot=r.effect_snapshot();pre=anchor(r);p_target=float(r.observation['sensor'][0])
        rows=[];monitor=None
        for group in ['A','bias_only','F1','M4','Adaptive_M4']:
            r.effect_restore(snapshot);mutable=copy.deepcopy(gain)
            original=r.step
            if group=='Adaptive_M4':
                learner=copy.deepcopy(rls);monitor=GainMonitor(r,learner,mutable,nominal,p_target)
                def observed_step(u):
                    before=monitor.state();transition=original(u);monitor.update(before,transition);return transition
                r.step=observed_step
            try:
                trace,stats=rollout_control(r,group,mutable if group in ['M4','Adaptive_M4'] else None,
                    60.,pre,p_target)
            finally:r.step=original
            if group=='Adaptive_M4':trace['gain_K_after_step']=np.asarray(monitor.K_history)
            np.savez_compressed(out/(group+'.npz'),**trace)
            rows.append(dict(group=group,**stats))
        write(out/'gain_updates.json',dict(accepted=monitor.accepted,events=monitor.events,
            sensor_only=True,no_GT_gate_or_control=True,update_interval_s=5.,future_validation_s=2.,
            candidate_source_sha256=sha256(shadow_file)))
        result=dict(condition=item['condition'],id=item['id'],rows=rows,accepted_updates=monitor.accepted,
            common_initial_full_snapshot=True,shadow_gate_previously_passed=True)
        write(out/'results.json',result)
        print('[VALIDATION_SIM] adaptive',item['id'],'accepted',monitor.accepted,flush=True)
        return result
    finally:r.env.close()


def adaptive_summary(results):
    summaries={}
    for condition in sorted({r['condition'] for r in results}):
        selected=[r for r in results if r['condition']==condition]
        fixed=[next(x for x in r['rows'] if x['group']=='M4') for r in selected]
        adapted=[next(x for x in r['rows'] if x['group']=='Adaptive_M4') for r in selected]
        stable=bool(len(selected)==3 and all(a['complete'] and b['complete'] for a,b in zip(fixed,adapted)))
        wins=sum(b['base']['IAE']<a['base']['IAE'] for a,b in zip(fixed,adapted))
        IAE_ratio=float(np.median([r['base']['IAE'] for r in adapted])/max(np.median([r['base']['IAE'] for r in fixed]),1e-15))
        gain_used=all(r['accepted_updates']>0 for r in selected)
        limits=all(b['pitch_RMS']<=max(1.25*a['pitch_RMS'],.002) and b['wheel_torque_RMS']<=1.25*a['wheel_torque_RMS']
            and b['last5_base_speed_RMS'] is not None and b['last5_base_speed_RMS']<=max(1.1*a['last5_base_speed_RMS'],.0002)
            for a,b in zip(fixed,adapted) if a['complete'] and b['complete'])
        summaries[condition]=dict(gate=bool(stable and gain_used and limits and IAE_ratio<=.9 and wins>=2),
            complete=stable,actual_gain_updates=gain_used,paired_wins=wins,pairs=len(selected),IAE_ratio=IAE_ratio,
            accepted_updates=[r['accepted_updates'] for r in selected])
    return dict(gate=bool(summaries and any(v['gate'] for v in summaries.values())),conditions=summaries,
        note='Actual superiority requires accepted gain changes and >=10% median base IAE reduction with limits; '
            'one condition PASS does not imply general robustness. Rejected candidates retain the previous validated gain.')


def run_adaptive(root,plan,shadow,shadow_root=None,mismatch_source=None):
    shadow_root=Path(shadow_root) if shadow_root is not None else root
    mismatch_source=Path(mismatch_source) if mismatch_source is not None else root
    assert shadow['gate'] is True and shadow['eligible_for_adaptive']
    out=root/'adaptive';out.mkdir()
    manifest=json.loads((shadow_root/'shadow/manifest.json').read_text())
    items=[]
    for pair in manifest['pairs']:
        if pair['condition'] not in shadow['eligible_for_adaptive']:continue
        item=dict(pair,shadow_directory=str(shadow_root/'shadow'/pair['id']))
        result=json.loads((Path(item['shadow_directory'])/'results.json').read_text());assert result['gate'] is True
        assert sha256(Path(item['shadow_directory'])/'models_frozen.json')==result['frozen_sha256']
        items.append(item)
    write(out/'manifest.json',dict(items=items,execution_domain='VALIDATION_SIM',
        criterion='all3 complete, actual accepted gain in each, median base IAE<=90% fixed,>=2/3 paired wins; pitch/wheel/final-speed limits',
        gain_guard='same Q/R; blend0.1; scaled gain deviation<=25%; raw command jump<=0.005Nm; '
            'rho<1 for nominal and candidate; candidate must predict subsequent2s p/v within0.02mm/0.02mm/s',
        input_limits='unchanged bias0.4828Nm,correction0.05Nm,ramp1.5s,slew2Nm/s',
        common_prefix_s=60.,evaluation_s=60.,no_GT_identification=True,no_QR_search=True))
    nominal=json.loads((PREVIOUS/'affine_models_frozen.json').read_text())['models']['M4']
    gain=json.loads((PREVIOUS/'gains_frozen.json').read_text())['models']['M4']
    cfg=json.loads(prepared_config(CKPT).read_text())
    results=parallel(adaptive_job,items,plan['workers'],cfg,str(out),str(mismatch_source),nominal,gain)
    write(out/'all_results.json',dict(rows=results))
    return adaptive_summary(results)
