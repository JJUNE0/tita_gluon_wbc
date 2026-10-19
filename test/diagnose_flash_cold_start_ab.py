"""VALIDATION_SIM: original cold-start replay; DESKTOP_DRY_RUN: input diagnostics."""
import argparse
from concurrent.futures import ProcessPoolExecutor
import json
from pathlib import Path

import numpy as np

from flash_cold_start_abc import (OLD,verify,write,sensor_geometry,discrete_transport,information,fit_rls)
from static_target_domain import StaticRunner,CKPT,prepared_config
from run_static_target_adaptation import KEYS
from diagnose_flash_odometry import point_velocity
from sim2sim.lqr.estimator import WheelOdometry,Sensors
from analyze_flash_state_learning import state
from m4_joint_adaptation import BIAS,nominal,fixed_gain,SUPPORT_HALF_WIDTH
from m4_shadow_stages import prediction_gate


def measurement(r,data,p,v):
    q=data.qpos[r.env.qpos_addr].astype(np.float32).astype(float)
    dq=data.qvel[r.env.qvel_addr].astype(np.float32).astype(float)
    quat=data.sensor('trunk_quat').data.copy();gyro=data.sensor('trunk_gyro').data.copy()
    geometry=sensor_geometry(r.description,q,dq,quat,gyro)
    base=r.env.model.body('base_link').id
    P=data.xpos[base].copy();A=data.xpos[r.wheel_bodies].mean(0)
    vb,_=point_velocity(r,data,P,base)
    va=np.mean([point_velocity(r,data,data.xpos[b],b)[0]for b in r.wheel_bodies],axis=0)
    f=np.array([np.cos(geometry['yaw']),np.sin(geometry['yaw']),0.])
    return dict(**geometry,base=P,axle=A,sensor_p=p,sensor_v=v,base_v=float(vb@f),axle_v=float(va@f),
        FK_offset_error=float(np.linalg.norm(geometry['offset_world']-(A-P))),
        velocity_transport_error=float(geometry['transport_velocity']-(va-vb)@f))


def paths(records):
    n=len(records);base=np.zeros(n);axle=np.zeros(n);parts=np.zeros((n,3));transport=np.zeros(n)
    for i in range(1,n):
        a,b=records[i-1:i+1];dy=(b['yaw']-a['yaw']+np.pi)%(2*np.pi)-np.pi
        f=np.array([np.cos(a['yaw']+dy/2),np.sin(a['yaw']+dy/2),0.])
        base[i]=base[i-1]+(b['base']-a['base'])@f;axle[i]=axle[i-1]+(b['axle']-a['axle'])@f
        term,total=discrete_transport(a,b);parts[i]=parts[i-1]+term;transport[i]=transport[i-1]+total
    sensor=np.asarray([r['sensor_p']for r in records]);sensor-=sensor[0]
    result=dict(base_path=base,axle_path=axle,sensor_path=sensor,transport_parts=parts,
        corrected_base_path=sensor-transport,transport=transport,rolling_remainder=sensor-axle)
    result.update({k:np.asarray([r[k]for r in records])for k in records[0]})
    result['path_identity_closure']=(sensor-base)-((sensor-axle)+(axle-base))
    return result


def phase_a_job(job):
    folder=Path(job['out']);folder.mkdir();cfg=json.loads(prepared_config(CKPT).read_text())
    r=StaticRunner(cfg,job['job'],job['effect']);old=OLD/'safety'/job['id']
    try:
        with np.load(old/'startup.npz')as original:
            for key in ['qpos','qvel','motor']:np.testing.assert_array_equal([v[key]for v in r.env.startup],original[key])
        original_estimator=(r.estimator.position,r.estimator.previous)
        startup=[];estimator=WheelOdometry(r.description,0.)
        data=r.env.mujoco.MjData(r.env.model)
        for record in r.env.startup:
            data.qpos[:]=record['qpos'];data.qvel[:]=record['qvel'];r.env.mujoco.mj_forward(r.env.model,data)
            sensors=Sensors(data.qpos[r.env.qpos_addr].astype(np.float32),data.qvel[r.env.qvel_addr].astype(np.float32),
                data.sensor('trunk_quat').data.copy(),data.sensor('trunk_gyro').data.copy())
            p,v,*_=estimator.observe(sensors,.02);startup.append(measurement(r,data,p,v))
        np.savez_compressed(folder/'transform_up.npz',**paths(startup))
        assert r.estimator.position==original_estimator[0]
        initial=r.full_snapshot();out=[]
        for arm,source in [('Flash',OLD/'phase0'/job['id']),('Fixed',old)]:
            r.full_restore(initial);records=[]
            with np.load(source/(arm+'.npz'))as trace:
                N=min(500,len(trace['raw_requested']))
                for i in range(N+1):
                    for key in KEYS:np.testing.assert_array_equal(r.observation[key],trace[key][i])
                    before=r.env.data.qpos.copy(),r.env.data.qvel.copy(),r.estimator.position
                    record=measurement(r,r.sensors,*r.observation['sensor'][:2]);records.append(record)
                    np.testing.assert_array_equal(before[0],r.env.data.qpos);np.testing.assert_array_equal(before[1],r.env.data.qvel);assert before[2]==r.estimator.position
                    if i<N:
                        tr=r.step(float(trace['raw_requested'][i]))
                        for key,value in tr.items():np.testing.assert_array_equal(value,trace[key][i])
            result=paths(records);np.savez_compressed(folder/(arm+'.npz'),**result)
            checks=[]
            for t in [1.,5.,10.]:
                i=round(t/.02)
                if i>N:continue
                checks.append(dict(t=t,original_gap=float(result['sensor_path'][i]-result['base_path'][i]),
                    corrected_gap=float(result['corrected_base_path'][i]-result['base_path'][i]),
                    leg=float(result['transport_parts'][i,0]),tilt=float(result['transport_parts'][i,1]),yaw=float(result['transport_parts'][i,2]),
                    transport_GT=float(result['axle_path'][i]-result['base_path'][i]),rolling_remainder=float(result['rolling_remainder'][i])))
            out.append(dict(arm=arm,exact_replay=True,steps=N,checks=checks,
                FK_error_max=float(max(result['FK_offset_error'])),velocity_transport_error_max=float(max(abs(result['velocity_transport_error']))),
                transport_path_error_max=float(max(abs(result['transport']-(result['axle_path']-result['base_path']))))))
        r.env.assert_static();row=dict(job=job,rows=out,startup_exact=True,
            startup_note='Original odometry is first initialized at RL entry; saved transform_up sensor odometry is a separate offline reconstruction, not original runtime history.')
        write(folder/'results.json',row);print('VALIDATION_SIM A exact',job['id'],flush=True);return row
    finally:r.env.close()


def phase_b_job(job):
    folder=Path(job['folder']);arm=job['arm'];out=Path(job['out']);out.mkdir()
    details=json.loads((folder/(arm+'_learning.json')).read_text())
    with np.load(folder/(arm+'.npz'))as a:
        trace=dict(a);z=state(trace);z[:,0]-=float(trace['p_hold']);u=trace['actual_u'];N=len(u)
        eligible=np.arange(N)>=50
        finite=np.isfinite(z[:-1]).all(1)&np.isfinite(z[1:]).all(1)&np.isfinite(u)
        software=np.asarray(trace['global_clipped'])|(abs(trace['raw_requested']-u)>1e-6)
        physical=np.asarray(trace['physical_saturation'])
        supported=np.all(abs(z[1:]-np.asarray(fixed_gain()['reference']))<=SUPPORT_HALF_WIDTH,axis=1)
        # Original learner also rejects logged initial posture/leg warnings.
        warned=np.zeros(N,dtype=bool)
        for e in job['row']['startup_limit_events']:
            i=round(e['t']/.02)
            if i<N:warned[i]=bool(e['reasons'])
        deployed=finite&~trace['global_clipped']&supported&~warned
        masks=dict(all_after1s=finite&eligible,unsaturated_after1s=finite&eligible&~software&~physical,deployed_eligibility=deployed)
        common=dict(steps=N,global_cap_fraction=float(np.mean(trace['global_clipped'])),
            software_delivery_clip_fraction=float(np.mean(abs(trace['raw_requested']-u)>1e-6)),physical_total_clip_fraction=float(np.mean(physical)),
            requested_actual_RMS=float(np.sqrt(np.mean((trace['raw_requested']-u)**2))),
            raw_requested_RMS=float(np.sqrt(np.mean((trace.get('pre_global_clip',trace['bias']+trace['raw_correction'])-trace['raw_requested'])**2))),
            physical_total_wheel_RMS=float(np.sqrt(np.mean(trace['physical_motor'][:,:,[3,7]]**2))))
        verdict_file=folder/(arm+'_full_validation')/'verdict.json';validation=None
        if verdict_file.exists():validation=json.loads(verdict_file.read_text())
        rows=[]
        for name,mask in masks.items():
            inf=information(z,u,mask);model,diag=fit_rls([(z,u,mask)])
            if name=='deployed_eligibility':
                for key in ['A','B','c_center']:np.testing.assert_array_equal(model[key],details['full_model'][key])
                assert model['update_count']==details['full_model']['update_count']
            Btruth=validation.get('direct_B_v')if validation else None
            row=dict(mask=name,information=inf,RLS=diag,B_v=model['B'][1],
                B_relative_error=None if Btruth is None else abs(model['B'][1]/Btruth-1),direct_B_v=Btruth,
                B_status='NOT_TESTED'if Btruth is None else('PASS'if model['B'][1]*Btruth>0 and abs(model['B'][1]/Btruth-1)<=.3 else'FAIL'),
                rho=float(max(abs(np.linalg.eigvals(np.asarray(model['A'])[1:,1:])))))
            write(out/(name+'_model.json'),model);rows.append(row)
        stats=dict(phase=job['phase'],case=folder.name,domain=job['domain'],arm=arm,commands=common,rows=rows,deployed_model_exact=True)
        write(out/'results.json',stats);return stats


def main():
    p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);p.add_argument('--stage',choices=['A','B'],required=True);p.add_argument('--workers',type=int,default=3);args=p.parse_args()
    root=args.root.resolve();plan=verify(root,full=True);dest=root/args.stage;assert not dest.exists();dest.mkdir()
    jobs=[]
    if args.stage=='A':
        safe={d['name']:d['effect']for d in plan['domains']}
        for case in json.loads((OLD/'01_safety.json').read_text())['rows']:
            job=case['job']
            if job['domain']in safe:jobs.append(dict(id=job['id'],job=job,effect=safe[job['domain']],out=str(dest/job['id'])))
        function=phase_a_job
    else:
        for phase in ['shadow','primary','composite_shadow','composite_primary']:
            for file in (OLD/phase).glob('*/results.json'):
                data=json.loads(file.read_text())
                for row in data['rows']:
                    if row['arm']in ['KOnly','E6']:
                        jobs.append(dict(folder=str(file.parent),row=row,arm=row['arm'],domain=data['job']['domain'],phase=phase,out=str(dest/(phase+'_'+file.parent.name+'_'+row['arm']))))
        function=phase_b_job
    with ProcessPoolExecutor(max_workers=args.workers)as pool:results=list(pool.map(function,jobs))
    verify(root,full=True);write(root/(args.stage+'_results.json'),dict(execution_domain='VALIDATION_SIM'if args.stage=='A'else'DESKTOP_DRY_RUN',rows=results))
    print(args.stage,'COMPLETE',len(results),flush=True)


if __name__=='__main__':main()
