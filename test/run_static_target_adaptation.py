"""VALIDATION_SIM: static target deployment, Phase0 first, independent domain gates."""
import argparse
from concurrent.futures import ProcessPoolExecutor, as_completed
import copy
import csv
import fcntl
import hashlib
import json
from pathlib import Path
import shutil
import subprocess

import numpy as np

from static_target_domain import StaticRunner, StartupFailure, sensor_state, KEYS, REPO, CKPT, prepared_config
from static_target_learner import StaticLearner, MASKS
from m4_joint_adaptation import Command, fixed_gain, nominal, BIAS, LOW, HIGH
from m4_shadow_stages import prediction_gate
from analyze_flash_state_learning import state
from eval_flash_stop_release import inputs_for
from flash_overnight_model_stages import sha256
from flash_overnight_control_stages import rollout_control, anchor
from m4_mismatch_stages import PREVIOUS

ARMS=list(MASKS)
SOURCES=['static_target_domain.py','static_target_learner.py','run_static_target_adaptation.py','test_static_target_adaptation.py']


def clean(value):
    if isinstance(value,dict):return {k:clean(v) for k,v in value.items()}
    if isinstance(value,(list,tuple)):return [clean(v) for v in value]
    if isinstance(value,np.ndarray):return clean(value.tolist())
    if isinstance(value,(np.floating,float)):return float(value) if np.isfinite(value) else None
    if isinstance(value,np.integer):return int(value)
    return value


def write(path,value):
    path.write_text(json.dumps(clean(value),indent=2,allow_nan=False)+'\n')


def score(trace,complete,failure):
    t=np.arange(len(trace['sensor']))*.02;p=trace['base_path'];v=trace['base_velocity'][:,0]
    def window(start,end):
        mask=(t>=start)&(t<=end)
        if not mask.any():return None
        steps=mask[:-1]
        return dict(IAE=float(np.trapz(abs(p[mask]),t[mask])),position_RMSE=float(np.sqrt(np.mean(p[mask]**2))),
            max_sagittal=float(max(abs(p[mask]))),max_planar=float(max(np.linalg.norm(trace['base_position'][mask,:2]-trace['base_position'][0,:2],axis=1))),
            speed_RMS=float(np.sqrt(np.mean(v[mask]**2))),pitch_RMS=float(np.sqrt(np.mean((trace['sensor'][mask,2]-fixed_gain()['reference'][2])**2))),
            wheel_RMS=float(np.sqrt(np.mean(trace['physical_motor'][steps][:,:,[3,7]]**2))) if steps.any() else None)
    good=(abs(p)<=.001)&(abs(v)<=.0002);last=None;recover=None
    # Require a prior departure, followed by continuous5s return; no false recovery0.
    left=np.flatnonzero(~good)
    if len(left):
        for i in range(int(left[0])+1,len(t)):
            last=i if not good[i] else last
            if last is not None and i-last>=250:recover=float(t[i-249]);break
    tail=window(max(0.,t[-1]-5.),t[-1]);last20=window(max(0.,t[-1]-20.),t[-1])
    full=window(0.,t[-1]);terminal=float(p[-1])
    hold=bool(complete and full['max_planar']<=.05 and abs(terminal)<=.01 and tail['speed_RMS']<=.0002 and not failure)
    return dict(complete=complete,failure=failure,end_s=float(t[-1]),full=full,calibration=window(0.,min(60.,t[-1])),
        post_calibration=window(60.,t[-1]) if t[-1]>=60. else None,last5=tail,last20=last20,
        terminal_error=terminal,absolute_hold=hold,recovery_s=recover,
        yaw_change=float(np.unwrap(trace['rpy'][:,2])[-1]-trace['rpy'][0,2]),
        max_midpoint=float(max(abs(trace['midpoint_path']))),
        incomplete_full_horizon=not complete)


def guard(r,t):
    failure=r.failures()
    # Intended crouched RL transition is logged, never relabelled a steady-state limit PASS.
    if t<1.:failure=[f for f in failure if f not in ['base_height_limit','leg_joint_limit']]
    return failure


def collect(r,arm,seed,duration,permit_K=False,probes=False):
    p_hold=float(r.observation['sensor'][0]);goal=r.observation['base_position'].copy()
    gain=fixed_gain();K0=np.asarray(gain['K']);ref0=np.asarray(gain['reference'])
    learner=None if arm in ['Flash','Bias','Fixed'] else StaticLearner(MASKS[arm],r.env.model.jnt_range[r.leg_joints].copy(),permit_K)
    command=Command(previous=0.);requested_probe=inputs_for('train_prbs',.01,seed+9721,round(duration/.02))
    rows=[];steps=[];extras=[];failure=[];startup_limits=[];path=0.;midpath=0.;previous=None
    snapshots={};known_input=0.;N=round(duration/.02)
    for i in range(N+1):
        obs={k:r.observation[k].copy()for k in KEYS};obs['base_path']=np.array(path);obs['midpoint_path']=np.array(midpath)
        if previous is not None:
            angle=previous['rpy'][2]+((obs['rpy'][2]-previous['rpy'][2]+np.pi)%(2*np.pi)-np.pi)/2
            heading=np.array([np.cos(angle),np.sin(angle),0.])
            path+=float((obs['base_position']-previous['base_position'])@heading)
            midpath+=float((obs['position']-previous['position'])@heading)
            obs['base_path']=np.array(path);obs['midpoint_path']=np.array(midpath)
        rows.append(obs);previous=obs
        if i%250==0:r.env.assert_static()
        original_failure=r.failures()
        if i<50 and original_failure:startup_limits.append(dict(t=i*.02,reasons=original_failure))
        failure=guard(r,i*.02)
        if failure or i==N:break
        z=sensor_state(r,p_hold)
        K,bias,ref=learner.values() if learner is not None else (K0,BIAS,ref0)
        probe=0.
        raw=bias-float(K@(z-ref))
        safe_probe=(i>=100 and i<3000 and abs(z[1])<.02 and abs(z[2])<.2
            and LOW+.012<raw<HIGH-.012 and not original_failure)
        if probes and arm not in ['Flash','Bias','Fixed'] and safe_probe:probe=float(requested_probe[i])
        if arm=='Flash':u=0.;details=dict(K_used=K0.copy(),bias=0.,reference_used=ref0.copy(),effective_offset=float(K0@ref0),global_clipped=False,raw_correction=0.)
        elif arm=='Bias':
            u=float(np.clip(BIAS,command.previous-.04,command.previous+.04));command.previous=u
            details=dict(K_used=K0.copy(),bias=BIAS,reference_used=ref0.copy(),effective_offset=float(BIAS+K0@ref0),global_clipped=False,raw_correction=0.)
        else:u,details=command.compute(z,K,bias,ref,probe)
        tr=r.step(u);known_input=float(tr['actual_u'])
        assert abs(known_input)<=abs(u)+1e-6
        if learner is not None:learner.observe(z,known_input,sensor_state(r,p_hold),details['global_clipped'] or bool(original_failure))
        details.update(probe=probe,raw_requested=u,software_residual=known_input,
            physical_saturation=bool(np.any(abs(tr['physical_motor'][:,[3,7]])>=12.-1e-6)))
        steps.append(tr);extras.append(details)
        if i+1 in [3000,N]:snapshots[i+1]=r.full_snapshot()
    trace={k:np.asarray([row[k]for row in rows])for k in rows[0]}
    if steps:
        trace.update({k:np.asarray([row[k]for row in steps])for k in steps[0]})
        trace.update({k:np.asarray([row[k]for row in extras])for k in extras[0]})
        np.testing.assert_array_equal(trace['previous_action'][:-1],trace['history'])
        np.testing.assert_array_equal(trace['previous_action'][1:],trace['action'])
        np.testing.assert_array_equal(trace['physical_motor'][:,:,[0,1,2,4,5,6]],trace['flash'][:,:,[0,1,2,4,5,6]])
    else:trace['physical_motor']=np.empty((0,4,8))
    trace['p_hold']=np.array(p_hold);trace['goal_base_position']=goal
    result=score(trace,not failure and len(steps)==N,failure)
    result.update(startup_limit_events=startup_limits,p_hold=p_hold,goal_base_position=goal.tolist(),
        target_hash_constant=r.env.fingerprint()==r.env.initial_fingerprint,
        software_saturation_fraction=float(np.mean(trace['global_clipped'])) if steps else None,
        physical_saturation_fraction=float(np.mean(trace['physical_saturation'])) if steps else None,
        probe_energy=float(.02*np.sum(trace['probe']**2)) if steps else 0.,
        new_target_K_adoptions=len(learner.K_adoptions)if learner else 0)
    return trace,result,learner,snapshots


def validate(r,snapshot,model,out,seed,previous_command):
    """Offline harness only: no return data are fed into online learner."""
    r.full_restore(snapshot);hold=BIAS;bridge=[]
    while abs(previous_command-hold)>1e-12:
        if guard(r,2.):return dict(gate=False,reason='offline_bridge_guard')
        command=float(np.clip(hold,previous_command-.04,previous_command+.04))
        actual=float(r.step(command)['actual_u'])
        bridge.append(dict(requested=command,actual=actual));previous_command=command
    write(out/'bridge.json',dict(execution_domain='VALIDATION_SIM',steps=bridge,reason='slew to interior input before all matched offline branches'))
    snapshot=r.full_snapshot()
    def rollout(inputs):
        rows=[];actual=[]
        for i in range(len(inputs)+1):
            rows.append({k:r.observation[k].copy()for k in KEYS})
            if guard(r,2.):return None,None
            if i<len(inputs):actual.append(float(r.step(float(inputs[i]))['actual_u']))
        return {k:np.asarray([x[k]for x in rows])for k in KEYS},np.asarray(actual)
    base,bu=rollout(np.full(200,hold))
    if base is None:return dict(gate=False,reason='offline_baseline_guard')
    np.savez_compressed(out/'baseline.npz',**base,actual_u=bu)
    deltas=[];us=[]
    families=['validation_sine','validation_prbs','pulse_pos','pulse_neg','step_pos','step_neg','bipulse_pos','bipulse_neg']
    for i,f in enumerate(families):
        r.full_restore(snapshot);probe,pu=rollout(hold+inputs_for(f,.01,seed+i,200))
        if probe is None:return dict(gate=False,reason='offline_probe_guard',family=f)
        np.savez_compressed(out/(f+'.npz'),**probe,actual_u=pu)
        np.testing.assert_array_equal(state(probe)[0],state(base)[0]);deltas.append(state(probe)-state(base));us.append(pu-bu)
    direct=[]
    for sign in [1.,-1.]:
        r.full_restore(snapshot);x,u=rollout([hold+sign*.005])
        if x is None:return dict(gate=False,reason='offline_direct_B_guard')
        direct.append((state(x)[1],u[0]))
    B=(direct[0][0]-direct[1][0])/(direct[0][1]-direct[1][1])
    value=prediction_gate(dict(model,indices=list(range(24))),deltas,us,float(B[1]))
    value['Direct_B']=B.tolist()
    return value


def run_job(job,cfg,root):
    out=Path(root)/job['id'];out.mkdir();r=None
    try:
        r=StaticRunner(cfg,dict(seed=job['seed'],pitch=job['pitch']),job['effect'])
        np.savez_compressed(out/'startup.npz',**{k:np.asarray([row[k]for row in r.env.startup])for k in ['qpos','qvel','motor']})
        write(out/'physics.json',dict(r.env.metadata,contacts=r.contact_metadata()))
        common=r.full_snapshot();initial=state({k:np.asarray([r.observation[k]])for k in KEYS})[0]
        result=[]
        for arm in job['arms']:
            r.full_restore(common)
            np.testing.assert_array_equal(state({k:np.asarray([r.observation[k]])for k in KEYS})[0],initial)
            trace,stats,learner,snapshots=collect(r,arm,job['seed'],job['duration'],job.get('permit_K',False),job.get('probes',False))
            np.savez_compressed(out/(arm+'.npz'),**trace)
            record=dict(arm=arm,**stats)
            if learner is not None:
                details=learner.report();write(out/(arm+'_learning.json'),details)
                if (stats['complete'] and job.get('validate',False) and abs(trace['sensor'][-1,1])<=.02
                        and not stats['failure'] and not np.any(trace['global_clipped'][-250:])
                        and not np.any(trace['physical_saturation'][-250:])):
                    snapshot=snapshots[round(job['duration']/.02)]
                    for mode,m in [('full',details['full_model']),('partial',details['partial_model'])]:
                        folder=out/(arm+'_'+mode+'_validation');folder.mkdir()
                        verdict=validate(r,snapshot,m,folder,job['seed']+17000,float(trace['raw_requested'][-1]))
                        write(folder/'verdict.json',verdict);record[mode+'_model_gate']=verdict['gate']
                    if learner.K_adoptions:
                        folder=out/(arm+'_adopted_validation');folder.mkdir()
                        verdict=validate(r,snapshot,learner.K_adoptions[-1]['model'],folder,job['seed']+17000,float(trace['raw_requested'][-1]))
                        write(folder/'verdict.json',verdict);record['adopted_model_gate']=verdict['gate']
                else:record['model_validation']='NOT_TESTED unsafe/incomplete/recent input saturation or validation not scheduled'
            result.append(record);write(out/'results.json',dict(job=job,rows=result,source_domain='nominal MuJoCo prior',target_static=True))
        r.env.assert_static()
        print('[VALIDATION_SIM]',job['id'],[(x['arm'],x['complete'],x['new_target_K_adoptions'])for x in result],flush=True)
        return dict(job=job,rows=result)
    except StartupFailure as exc:
        env=exc.env
        np.savez_compressed(out/'startup_failure.npz',**{k:np.asarray([row[k]for row in env.startup])for k in ['qpos','qvel','motor']})
        write(out/'physics.json',env.metadata)
        result=dict(job=job,rows=[dict(arm=arm,complete=False,failure=['startup'],end_s=0.,
            startup_failure_time_s=float(env.data.time),detail=str(exc),absolute_hold=False)for arm in job['arms']])
        env.close()
        write(out/'results.json',result);print('[VALIDATION_SIM]',job['id'],'STARTUP FAIL',str(exc),flush=True);return result
    finally:
        if r is not None:r.env.close()


def parallel(jobs,cfg,out,workers):
    out.mkdir();rows=[]
    with ProcessPoolExecutor(max_workers=workers)as pool:
        futures=[pool.submit(run_job,j,cfg,str(out))for j in jobs]
        for f in as_completed(futures):rows.append(f.result())
    return rows


def make_plan(root,workers):
    assert not root.exists();root.mkdir(parents=True)
    single=[('nominal',{}),('gain0.8',dict(gain=.8)),('gain1.2',dict(gain=1.2)),
        ('mass1.15',dict(mass=1.15)),('mass1.30',dict(mass=1.30)),('friction0.2',dict(friction=.2)),
        ('friction0.8',dict(friction=.8)),('lag0.02',dict(lag=.02)),('lag0.05',dict(lag=.05)),
        ('com-0.005',dict(com=-.005)),('com+0.005',dict(com=.005))]
    rng=np.random.default_rng(160610)
    combos=[('combo_gain_low_friction',dict(gain=float(rng.uniform(.88,.92)),friction=float(rng.uniform(.55,.65))),['gain0.8','friction0.2','friction0.8']),
        ('combo_gain_high_friction',dict(gain=float(rng.uniform(1.08,1.12)),friction=float(rng.uniform(.65,.75))),['gain1.2','friction0.2','friction0.8']),
        ('combo_com_gain',dict(gain=float(rng.uniform(.88,.92)),com=float(rng.uniform(-.003,-.002))),['gain0.8','com-0.005']),
        ('combo_mass_friction',dict(mass=float(rng.uniform(1.06,1.10)),friction=float(rng.uniform(.55,.65))),['mass1.15','friction0.2','friction0.8'])]
    pilot=[dict(seed=seed,pitch=p)for seed,p in zip([600,601,602],[-.035,0.,.035])]
    held=[dict(seed=s,pitch=p)for s in [610,611]for p in [-.035,0.,.035]]
    audit=json.loads((REPO/'docs/exp/2026-10-16/static_target_adaptation/repository_audit.json').read_text())
    protected=copy.deepcopy(audit['protected_sha256'])
    cfg_path=prepared_config(CKPT);cfg=json.loads(cfg_path.read_text())
    dependencies=[cfg_path,Path(cfg['policy']['path']),REPO/cfg['model']['scene_xml'],
                  PREVIOUS/'affine_models_frozen.json',PREVIOUS/'gains_frozen.json']
    dependencies+=[p for p in (REPO/'test').glob('*.py') if p.name!='analyze_static_target_adaptation.py']
    for p in dependencies:protected[str(p)]=sha256(p)
    plan=dict(execution_domain='VALIDATION_SIM',specification='Full user-supplied static Target specification in clarification reply',
        workers=workers,single_domains=[dict(name=n,effect=e)for n,e in single],
        combined_domains=[dict(name=n,effect=e,prerequisites=p)for n,e,p in combos],pilot=pilot,heldout=held,
        randomization='Frozen RNG160610 held-out composite values; independent per-domain seed order shuffled with RNG160611',
        source_sha256={str(REPO/'test'/p):sha256(REPO/'test'/p)for p in SOURCES},
        protected_sha256=protected,tracked_diff_sha256=audit['tracked_diff_sha256'],
        policy_sha256=sha256(CKPT/'actor.pt'),nominal_prior='offline nominal MuJoCo calibration; NOT Isaac-only source identification',
        pilot_s=60.,calibration_s=60.,post_s=120.,primary_s=180.,arms=ARMS,
        absolute_hold=dict(complete=True,max_planar_m=.05,terminal_sagittal_m=.01,last5_velocity_m_s=.0002),
        comparison=dict(median_full_IAE_ratio=.9,paired_wins=4,total=6),
        safety=dict(roll_pitch_rad=.65,RL_height_m=.18,leg_limit_tolerance_rad=.01,
            declared_crouched_transition_grace_s=1.,startup_height_m=.025,startup_tilt_rad=.9,
            operational_p_m=.25,pilot_tail_speed_m_s=.05,probe_speed_m_s=.02),
        limits=dict(residual=[LOW,HIGH],slew_Nm_s=2.,wheel_Nm=12.,ramp_s=1.5,
            initial_slew_transition='from residual0: first0.26s may lie below lower band, same for all residual arms; never exceeds upper band'),
        model_gate=dict(horizons_s=[.1,.5,1.,2.],NRMSE=.3,absolute_pv_RMSE=2e-5,B_error=.3,
            information_rank=25,condition=1e6,input_innovation=.01,candidate_every_s=5.,subsequent_validation_s=4.),
        online_B='independent conditional B regression on future sensor validation window; offline matched Direct B separately required for scientific model verdict',
        K_protocol='strict: same-state Direct B unavailable in a causal single rollout; candidates remain shadow unless a separately authorized protocol is preregistered',
        allow_conditional_B_for_K=False,
        gain_guard=dict(per_update=.25,cumulative_nominal=.25,blend=.1,raw_jump=.003,joint_jump=.005),
        probes='max0.01Nm, same seeded PRBS for online arms during0-60s, only safe non-saturated support; effort/drift counted',
        source_model='24-state full affine constrained RLS; A-frozen B/c and B2 finite-horizon proposals shadow only',
        startup_calibration='Nominal-only construction smoke showed intended crouch minheight0.06398m; .08m startup guard was corrected before any Target pilot/manifest freeze',
        no_threshold_changes=True,no_hardware=True,no_source_runtime_changes=True)
    write(root/'plan.json',plan);(root/'plan.sha256').write_text(sha256(root/'plan.json')+'\n')
    write(root/'domain_manifest.json',dict(single=plan['single_domains'],combined=plan['combined_domains'],pilot=pilot,heldout=held))
    return plan


def verify(plan,root):
    assert sha256(root/'plan.json')==(root/'plan.sha256').read_text().strip()
    for p,h in {**plan['protected_sha256'],**plan['source_sha256']}.items():assert sha256(Path(p))==h,p
    current=hashlib.sha256(subprocess.check_output(['git','diff','--binary'])).hexdigest()
    if current!=plan['tracked_diff_sha256']:
        # Concurrent edits outside frozen execution inputs are preserved and audited.
        # The hard assertions above still reject every changed model/source/config.
        names=subprocess.check_output(['git','diff','--name-only'],text=True).splitlines()
        write(root/'external_tracked_changes.json',dict(execution_domain='DESKTOP_DRY_RUN',
            evidence_status='SUSPICIOUS',baseline_sha256=plan['tracked_diff_sha256'],current_sha256=current,
            frozen_execution_inputs_unchanged=True,preserved_without_revert=True,
            tracked_files=[dict(path=p,mtime=Path(p).stat().st_mtime if Path(p).exists()else None)for p in names]))


def make_jobs(domains,starts,arms,duration,kind,**flags):
    jobs=[dict(id=f'{d["name"]}_s{s["seed"]}_p{s["pitch"]:+.3f}',domain=d['name'],effect=d['effect'],
          **s,arms=arms,duration=duration,kind=kind,**flags)for d in domains for s in starts]
    np.random.default_rng(160611).shuffle(jobs)
    return jobs


def safe_domains(safety):
    good=[];verdict={}
    for domain in sorted({x['job']['domain']for x in safety}):
        rows=[r for x in safety if x['job']['domain']==domain for r in x['rows']if r['arm']=='Fixed']
        safe=bool(len(rows)==3 and all(r['complete'] and r['last5']['speed_RMS']<=.05 and abs(r['terminal_error'])<=.25 for r in rows))
        verdict[domain]=dict(safe=safe,reason='3/3 Fixed stable operational completion' if safe else 'Fixed pilot failure or outside operational envelope')
        if safe:good.append(domain)
    return good,verdict


def execute(root,plan,resume):
    cfg=json.loads(prepared_config(CKPT).read_text());state_file=root/'pipeline_state.json'
    status=json.loads(state_file.read_text())if state_file.exists()else dict(status='RUNNING',stages={})
    def stage(name,operation):
        verify(plan,root)
        old=status['stages'].get(name)
        if old:
            assert resume and old['status']=='COMPLETE' and sha256(root/old['artifact'])==old['sha256']
            return json.loads((root/old['artifact']).read_text())['rows']
        status['stages'][name]=dict(status='RUNNING');write(state_file,status)
        try:
            rows=operation();path=root/(name+'.json');write(path,dict(rows=rows))
            verify(plan,root)
            status['stages'][name]=dict(status='COMPLETE',artifact=path.name,sha256=sha256(path))
            write(state_file,status);print('[VALIDATION_SIM] STAGE COMPLETE',name,flush=True);return rows
        except Exception as exc:
            status['status']='ERROR';status['stages'][name]=dict(status='ERROR',reason=repr(exc));write(state_file,status);raise
    # All Phase0 baselines finish before any Fixed/adaptation pilot runs.
    phase0=stage('00_phase0',lambda:parallel(make_jobs(plan['single_domains'],plan['pilot'],['Flash'],60.,'phase0'),cfg,root/'phase0',plan['workers']))
    safety=stage('01_safety',lambda:parallel(make_jobs(plan['single_domains'],plan['pilot'],['Bias','Fixed'],60.,'safety'),cfg,root/'safety',plan['workers']))
    safe,verdict=safe_domains(safety);write(root/'safety_gates.json',verdict)
    domains=[d for d in plan['single_domains']if d['name']in safe]
    shadow=stage('02_shadow',lambda:parallel(make_jobs(domains,plan['pilot'],['KOnly'],60.,'shadow',permit_K=False,probes=True,validate=True),cfg,root/'shadow',plan['workers']))
    shadow_gate={d['name']:all(x['rows'][0].get('full_model_gate',False) for x in shadow if x['job']['domain']==d['name']) for d in domains}
    write(root/'shadow_gates.json',shadow_gate)
    def primary():
        jobs=make_jobs(domains,plan['heldout'],ARMS,180.,'primary',probes=True,validate=True)
        for j in jobs:j['permit_K']=shadow_gate[j['domain']] and plan['allow_conditional_B_for_K']
        return parallel(jobs,cfg,root/'primary',plan['workers'])
    stage('03_primary',primary)
    # Compound physics values were preregistered; no outcome-selected parameter tuning.
    combos=[d for d in plan['combined_domains']if all(n in safe for n in d['prerequisites'])]
    combo_pilot=stage('04_composite_pilot',lambda:parallel(make_jobs(combos,plan['pilot'],['Flash','Bias','Fixed'],60.,'composite_pilot'),cfg,root/'composite_pilot',plan['workers']))
    cs,cg=safe_domains(combo_pilot);write(root/'composite_gates.json',dict(pilots=cg,not_tested=[dict(domain=d['name'],reason='unsafe single-factor prerequisite')for d in plan['combined_domains']if d not in combos]))
    combo_shadow=stage('05_composite_shadow',lambda:parallel(make_jobs([d for d in combos if d['name']in cs],plan['pilot'],['KOnly'],60.,'composite_shadow',permit_K=False,probes=True,validate=True),cfg,root/'composite_shadow',plan['workers']))
    combo_gate={d['name']:all(x['rows'][0].get('full_model_gate',False)for x in combo_shadow if x['job']['domain']==d['name'])for d in combos if d['name']in cs}
    def combined():
        jobs=make_jobs([d for d in combos if d['name']in cs],plan['heldout'],ARMS,180.,'composite_primary',probes=True,validate=True)
        for j in jobs:j['permit_K']=combo_gate[j['domain']] and plan['allow_conditional_B_for_K']
        return parallel(jobs,cfg,root/'composite_primary',plan['workers'])
    stage('06_composite_primary',combined)
    status['status']='COMPLETE';write(state_file,status)


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--root',type=Path,required=True)
    p.add_argument('--workers',type=int,default=3);p.add_argument('--resume',action='store_true')
    args=p.parse_args();root=args.root.resolve();assert root.is_relative_to(REPO/'docs/exp')
    plan=json.loads((root/'plan.json').read_text())if args.resume else make_plan(root,args.workers)
    with (root/'coordinator.lock').open('w')as lock:
        fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB);execute(root,plan,args.resume)


if __name__=='__main__':main()
