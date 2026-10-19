"""VALIDATION_SIM: M4-only follow-up, preserving the old M4/M5 verdicts."""

import gzip
import json
from pathlib import Path
import pickle

import numpy as np

from flash_overnight_control_stages import EffectRunner,rollout_control,anchor
from flash_overnight_model_stages import REPO,CKPT,BIAS,current,parallel,prepared_config,write,sha256
from run_flash_overnight_pipeline import verify_record

PREVIOUS = REPO/'docs/exp/2026-10-15/flash_overnight_pipeline/run_final'
GROUPS = ['A','bias_only','F1','M4']
EFFECTS = [('nominal',{}),('mass1.15',{'mass':1.15}),('mass1.30',{'mass':1.30}),
    ('gain0.8',{'gain':.8}),('gain1.2',{'gain':1.2}),('lag0.02',{'lag':.02}),
    ('lag0.05',{'lag':.05}),('friction0.2',{'friction':.2}),('friction0.8',{'friction':.8})]


def authorize_m4(previous=PREVIOUS):
    state=json.loads((previous/'pipeline_state.json').read_text())
    for stage in ['1','2','3','4']:verify_record(previous,state['stages'][stage])
    verdict=json.loads((previous/'04_drift_entry.json').read_text())
    if verdict.get('models',{}).get('M4') is not True:
        raise RuntimeError('M4 individual Stage4 PASS is required')
    if not all(json.loads((previous/name).read_text())['models']['M4']['gate'] is True
        for name in ['02_independent_affine.json','03_fixed_LQR.json']):
        raise RuntimeError('M4 A/B/affine and Fixed-LQR gates are required')
    rows=json.loads((previous/'entry_metrics.json').read_text())['rows']
    baseline={r['context']:r for r in rows if r['group']=='bias_only'}
    selected=[r for r in rows if r['group']=='M4']
    assert len(selected)==6
    good=all(r['complete'] and r['last5_base_speed_RMS']<=.0002 and r['last5_base_position_range']<=.005
        and r['max_planar_drift']<=.8*baseline[r['context']]['max_planar_drift'] for r in selected)
    if not good:raise RuntimeError('Actual M4 Stage4 metrics do not support PASS')
    return dict(gate=True,primary_model='M4',comparison_preserved='M5',
        old_aggregate_stage4=verdict['gate'],old_M5_stage4=verdict['models']['M5'],
        individual_stage4_recomputed=True,old_criteria_unchanged=True,
        note='New user-authorized branch from individual M4 PASS; old aggregate FAIL is not altered.',
        previous=str(previous.relative_to(REPO)),gain_sha256=sha256(previous/'gains_frozen.json'))


def apply_physics_effect(r,effect):
    """Apply mismatch at the branch time, preserving qpos/qvel and all estimators."""
    before=(r.env.data.qpos.copy(),r.env.data.qvel.copy(),r.estimator.position)
    m,mj=r.env.model,r.env.mujoco
    if 'mass' in effect:
        m.body_mass[1:]*=effect['mass'];m.body_inertia[1:]*=effect['mass']
        mj.mj_setConst(m,mj.MjData(m))
    floor=m.geom('floor').id
    wheel_geoms=[i for i in range(m.ngeom) if m.geom_bodyid[i] in r.wheel_bodies]
    if 'friction' in effect:
        # Both sides must change: actual contact friction is not wheel geom alone.
        m.geom_friction[[floor]+wheel_geoms,0]=effect['friction']
    clone=mj.MjData(m);mj.mj_copyData(clone,m,r.env.data);mj.mj_forward(m,clone)
    contact=[dict(geoms=c.geom.tolist(),dimension=int(c.dim),sliding_friction=float(c.friction[0]))
        for c in clone.contact[:clone.ncon] if floor in c.geom]
    np.testing.assert_array_equal(r.env.data.qpos,before[0]);np.testing.assert_array_equal(r.env.data.qvel,before[1])
    assert r.estimator.position==before[2]
    return dict(nonworld_mass_sum=float(m.body_mass[1:].sum()),floor_sliding=float(m.geom_friction[floor,0]),
        wheel_geom_sliding=m.geom_friction[wheel_geoms,0].tolist(),actual_contacts=contact,
        mass_and_inertia_scaled_together='mass' in effect,original_state_unchanged=True)


def job_run(job,cfg,output,gain,duration=60.):
    out=Path(output)/job['id'];out.mkdir()
    r=EffectRunner(cfg,job)
    try:
        if job['regime']=='settled':
            with gzip.open(PREVIOUS/'fresh'/job['source_id']/'snapshot_t50000.pkl.gz','rb') as f:r.restore(pickle.load(f))
        else:
            for i in range(400):
                if i>=50:assert not r.failures()
                r.step(0.)
        common=r.snapshot();first=current(r).copy();pre=anchor(r)
        p_target=float(r.observation['sensor'][0])
        physics=apply_physics_effect(r,job['effect'])
        r.enable_effect(job['effect'])
        rows=[]
        for group in GROUPS:
            r.restore(common)
            r.motor_state=r.env.data.ctrl[np.asarray(r.env.actuator_ids)[[3,7]]].copy()
            np.testing.assert_array_equal(current(r),first)
            trace,stats=rollout_control(r,group,gain if group=='M4' else None,duration,pre,p_target,
                ramp_bias=job['regime']=='entry')
            name=group+'.npz';np.savez_compressed(out/name,**trace)
            row=dict(context=job['context'],regime=job['regime'],condition=job['condition'],
                group=group,trace=name,effect=job['effect'],**stats)
            if job['condition']=='nominal' and (group in ['bias_only','M4'] or
                    (group=='A' and job['regime']=='entry')):
                original=(PREVIOUS/'entry'/f"entry_s{job['seed']}_p{job['pitch']:+.3f}"/(group+'.npz')
                    if job['regime']=='entry' else PREVIOUS/'control'/job['source_id']/f'{group}_zero_+0_t50000.npz')
                # Settled nominal has an intentionally longer60s horizon; compare
                # the common20s prefix, including the actual physics torques.
                with np.load(original) as old:
                    for k in ['sensor','gt','rpy','previous_action','leg_position','leg_velocity',
                        'policy_observation','action','history','motor','flash','base_position','base_velocity']:
                        np.testing.assert_array_equal(trace[k][:len(old[k])],old[k])
                row['nominal_archive_exact']=True
            rows.append(row)
        write(out/'results.json',dict(execution_domain='VALIDATION_SIM',job=job,rows=rows,
            physics=physics,initial_full_snapshot_history_identical=True,no_online_updates=True))
        print('[VALIDATION_SIM]',job['id'],'complete',sum(x['complete'] for x in rows),'/',len(rows),flush=True)
        return rows
    finally:r.env.close()


def jobs(smoke=False):
    result=[]
    old=json.loads((PREVIOUS/'fresh/manifest.json').read_text())['jobs']
    for regime in ['settled','entry']:
        for source in old:
            seed=source['seed'] if regime=='settled' else source['seed']+10
            context=f"{regime}_s{seed}_p{source['pitch']:+.3f}"
            for name,effect in EFFECTS:
                result.append(dict(id=context+'_'+name,context=context,regime=regime,seed=seed,
                    pitch=source['pitch'],pitch_index=source['pitch_index'],source_id=source['id'],
                    condition=name,effect=effect))
    if smoke:return [next(j for j in result if j['regime']=='entry' and j['pitch']==0 and j['condition']=='nominal')]
    return result


def summarize(rows):
    bases={(r['context'],r['condition']):r for r in rows if r['group']=='bias_only'}
    selected=[r for r in rows if r['group']=='M4']
    # Exactly the previous Stage5 M4 predicate: no success threshold is weakened.
    performance=bool(selected) and all(r['complete'] and bases[(r['context'],r['condition'])]['complete'] and
        r['base']['IAE']<=bases[(r['context'],r['condition'])]['base']['IAE'] for r in selected)
    conditions={}
    for regime in sorted({r['regime'] for r in rows}):
        for condition in sorted({r['condition'] for r in rows}):
            subset=[r for r in selected if r['regime']==regime and r['condition']==condition]
            if not subset:continue
            stable=bool(len(subset)==6 and all(r['complete'] for r in subset))
            good=bool(stable and all(bases[(r['context'],condition)]['complete'] and
                r['base']['IAE']<=bases[(r['context'],condition)]['base']['IAE'] for r in subset))
            conditions[regime+'/'+condition]=dict(gate=good,stable_completed=stable,count=len(subset),
                M4_base_IAE_median=float(np.median([r['base']['IAE'] for r in subset])),
                bias_base_IAE_median=float(np.median([bases[(r['context'],condition)]['base']['IAE'] for r in subset])),
                M4_max_planar_median=float(np.median([r['max_planar_drift'] for r in subset])),
                failure_reasons=[r['failure'] for r in subset])
    return dict(gate=bool(performance),conditions=conditions,runs=len(rows),
        old_M4_mismatch_criterion_unchanged=True,groups=GROUPS,
        note='Performance FAIL remains FAIL even if stable completion later permits sensor-only shadow diagnosis. '
            'Nominal entry was outside local identification range; mismatch stability is measured, never assumed.')


def run_mismatch(root,plan,smoke=False):
    out=root/('smoke' if smoke else 'mismatch');out.mkdir()
    gain=json.loads((PREVIOUS/'gains_frozen.json').read_text())['models']['M4']
    cfg=json.loads(prepared_config(CKPT).read_text())
    batch=jobs(smoke)
    write(out/'manifest.json',dict(execution_domain='VALIDATION_SIM',jobs=batch,duration_s=60.,
        primary_model='M4',M5='preserved comparison, no follow-up control',
        gain_sha256=sha256(PREVIOUS/'gains_frozen.json'),groups=GROUPS))
    parts=parallel(job_run,batch,plan['workers'],cfg,str(out),gain)
    rows=[r for part in parts for r in part]
    write(out/'metrics.json',dict(execution_domain='VALIDATION_SIM',rows=rows))
    return summarize(rows)
