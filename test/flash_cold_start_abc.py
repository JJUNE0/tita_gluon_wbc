"""DESKTOP_DRY_RUN: frozen ABC diagnostic protocol and sensor-only math."""
import argparse
import copy
import hashlib
import json
from pathlib import Path
import shutil
import subprocess

import numpy as np
from scipy.spatial.transform import Rotation

from run_static_target_adaptation import write, sha256, REPO, CKPT
from m4_joint_adaptation import nominal, BIAS, SUPPORT_HALF_WIDTH, fixed_gain
from m4_shadow_stages import ConstrainedRLS
from sim2sim_ros2_jazzy.adapter import NATIVE_JOINTS

OLD=REPO/'docs/exp/2026-10-16/static_target_adaptation/run_05'
SOURCES=['flash_cold_start_abc.py','diagnose_flash_cold_start_ab.py',
    'collect_flash_target_offline_id.py','analyze_flash_cold_start_abc.py','test_flash_cold_start_abc.py']


def sensor_geometry(description,q,dq,quat,gyro):
    """Only encoder/IMU inputs; no simulator data or root velocity/position."""
    R=Rotation.from_quat(np.asarray(quat)[[1,2,3,0]]).as_matrix()
    frames,axes=description.frames(q);centers=np.asarray([frames[n][:3,3]for n in description.wheel_links])
    derivative=[]
    children={j.get('name'):j.find('child').get('link')for j in description.joints}
    for center,chain in zip(centers,description.wheel_chains()):
        derivative.append(sum((np.cross(axes[NATIVE_JOINTS[i]],center-frames[children[NATIVE_JOINTS[i]]][:3,3])*dq[i]
            for i in chain),start=np.zeros(3)))
    d=centers.mean(0);d_world=R@d;omega=R@gyro
    roll,pitch,yaw=Rotation.from_matrix(R).as_euler('xyz')
    f=np.array([np.cos(yaw),np.sin(yaw),0.]);l=np.array([-np.sin(yaw),np.cos(yaw),0.])
    leg=R@np.mean(derivative,axis=0)
    return dict(offset_body=d,offset_world=d_world,R=R,yaw=yaw,
        velocity_leg=float(leg@f),velocity_pitch=float((omega@l)*d_world[2]),
        velocity_yaw=float(-omega[2]*(d_world@l)),transport_velocity=float((np.cross(omega,d_world)+leg)@f))


def discrete_transport(previous,current):
    """Exact symmetric product split; sums to heading-projected delta(R*d)."""
    R0,R1=previous['R'],current['R'];d0,d1=previous['offset_body'],current['offset_body']
    y0,y1=previous['yaw'],current['yaw'];dy=(y1-y0+np.pi)%(2*np.pi)-np.pi
    f=np.array([np.cos(y0+dy/2),np.sin(y0+dy/2),0.])
    Z0=Rotation.from_euler('z',y0).as_matrix();Z1=Rotation.from_euler('z',y1).as_matrix()
    H0,H1=Z0.T@R0,Z1.T@R1;e0,e1=H0@d0,H1@d1
    leg=(Z1+Z0)/2@((H1+H0)/2@(d1-d0))
    tilt=(Z1+Z0)/2@((H1-H0)@((d1+d0)/2))
    yaw=(Z1-Z0)@((e1+e0)/2)
    total=float((R1@d1-R0@d0)@f)
    terms=np.array([leg@f,tilt@f,yaw@f])
    assert abs(terms.sum()-total)<1e-12
    return terms,total


def information(z,u,mask):
    prior=nominal();ref=np.asarray(prior['state_reference']);scale=ConstrainedRLS(prior).scale
    X=np.column_stack([(z[:-1,1:]-ref[1:])/scale[1:],(u-BIAS)/.05,np.ones(len(u))])[mask]
    if len(X)<2:return dict(samples=len(X),rank=0,condition=None,innovation=None,gate=False)
    rms=np.maximum(np.sqrt(np.mean(X**2,axis=0)),1e-12);X=X/rms
    sv=np.linalg.svd(X,compute_uv=False);rank=int(np.sum(sv>sv[0]*1e-8))
    others=np.delete(X,23,axis=1);signal=X[:,23];innovation=signal-others@np.linalg.lstsq(others,signal,rcond=1e-8)[0]
    fraction=float(innovation@innovation/max(signal@signal,1e-20));condition=float(sv[0]/max(sv[-1],1e-300))
    return dict(samples=len(X),rank=rank,condition=condition,innovation=fraction,
        input_RMS=float(np.sqrt(np.mean((u[mask]-BIAS)**2))),input_std=float(np.std(u[mask])),singular_values=sv.tolist(),
        gate=bool(len(X)>=250 and rank==25 and condition<=1e6 and fraction>=.01))


def fit_batch(streams,partial=False):
    """Scaled affine OLS, original fixed centering; structural constraints exact."""
    prior=nominal();rls=ConstrainedRLS(prior,partial=partial);rows=[];targets=[]
    for z,u,mask in streams:
        x=(z[:-1]-rls.ref)/rls.scale;y=(z[1:]-rls.ref)/rls.scale
        y[:,0]-=x[:,0]
        if partial:y-=x[:,1:]@(rls.A[:,1:]*rls.scale[None,1:]/rls.scale[:,None]).T
        rows.append(np.column_stack([x[:,1:],(u-BIAS)/.05,np.ones(len(u))])[mask]);targets.append(y[mask])
    X,Y=np.concatenate(rows),np.concatenate(targets)
    if len(X)<25:raise ValueError('insufficient affine samples')
    ranks=[];conditions=[]
    for g in rls.groups:
        features=X[:,g['columns']];rms=np.maximum(np.sqrt(np.mean(features**2,axis=0)),1e-12)
        coef,_,rank,sv=np.linalg.lstsq(features/rms,Y[:,g['rows']],rcond=1e-8)
        g['theta']=(coef/rms[:,None]).T;ranks.append(int(rank));conditions.append(float(sv[0]/max(sv[-1],1e-300)))
    rls.count=len(X);model=rls.model();model['fit_method']='offline scaled affine LS rcond1e-8'
    return model,dict(samples=len(X),group_rank=ranks,group_condition=conditions)


def fit_rls(streams,partial=False):
    rls=ConstrainedRLS(nominal(),partial=partial)
    for z,u,mask in streams:
        for i in np.flatnonzero(mask):rls.update(z[i],float(u[i]),z[i+1])
    return rls.model(),rls.diagnostics()if rls.count>=25 else dict(samples=rls.count,gate=False)


def initialize(root):
    assert not root.exists();root.mkdir(parents=True)
    oldplan=json.loads((OLD/'plan.json').read_text());safe=json.loads((OLD/'safety_gates.json').read_text())
    domains=[d for d in oldplan['single_domains']if safe[d['name']]['safe']]
    protected={str(p):sha256(p)for p in OLD.rglob('*')if p.is_file()}
    for p in oldplan['protected_sha256']:protected[p]=sha256(Path(p))
    plan=dict(execution_domain='VALIDATION_SIM',analysis_domain='DESKTOP_DRY_RUN',policy_sha256=sha256(CKPT/'actor.pt'),
        source_root=str(OLD),protected_sha256=protected,source_sha256={str(REPO/'test'/p):sha256(REPO/'test'/p)for p in SOURCES},
        tracked_diff_sha256=hashlib.sha256(subprocess.check_output(['git','diff','--binary'])).hexdigest(),
        domains=domains,unsafe_not_tested=[d['name']for d in oldplan['single_domains']if not safe[d['name']]['safe']],
        A=dict(cases='safe6 domains x pilot3 starts x Flash/Fixed; exact old first10s replay + saved transform_up states',
            correction='offline only: encoder path minus sensor FK offset increment; gyro/leg transport velocity',
            times=[1.,5.,10.],no_contact_assumption_for_transport=True),
        B=dict(cases='old shadow KOnly24 and primary/composite KOnly/E6:96 trajectories',
            masks=['all_after1s','unsaturated_after1s','deployed_eligibility'],
            B_truth='existing matched offline Direct B only; missing contexts NOT_TESTED',
            physical_torque='total physical wheel torque, not an observable isolated residual after motor gain/lag'),
        C=dict(train=[dict(seed=s,pitch=p)for s,p in zip([720,721,722],[-.035,0.,.035])],
            test=[dict(seed=s,pitch=p)for s in [730,731]for p in [-.035,0.,.035]],duration_s=60.,
            training_windows=dict(transient=[1.,60.],post=[10.,60.]),primary_window='post',
            control='Frozen FlashSAC + bias0.4828 + guarded0.01Nm train PRBS/sine; no LQR or adaptation',
            test_control='same fixed bias, no probing until separate offline branch',test_snapshot_s=[10.,60.],
            validation='8 new4s families amplitude0.01, matched baseline, Direct B +/-0.005; no GT estimator input',
            models=['transient_LS','transient_RLS','post_LS','post_RLS','post_LS_Bc','post_RLS_Bc'],
            seed_order=[720,721,722],model_freeze_before_test=True,
            masks='timewindow, finite, no known software/native command clipping; physical actuator clipping audited separately, never an estimator label; no position-support exclusion because exact translation symmetry',
            primary_domain_gate='6/6 heldout60s snapshots: paired and absolute normalized <=30%, B sign/error<=30%, baseline2s<=20um/20um_s,4s<=50um/20um_s; information reported separately',
            no_hidden_state_injection=True,no_oracle_model_to_online=True),
        limits=dict(residual=[.4328,.5328],slew=2.,wheel=12.,probe=.01,probe_start_s=2.,probe_velocity=.02,probe_pitch=.2),
        metrics=dict(horizons=[5,25,50,100],NRMSE=.3,p_floor=1e-7,v_floor=1e-5,Direct_B_error=.3,
            baseline2s=[2e-5,2e-5],baseline4s=[5e-5,2e-5],information_rank=25,condition=1e6,innovation=.01),
        scope='A/B/C only; D/E/F, new controller/estimator activation, new gain, budget widening NOT_TESTED',
        no_QR_tuning=True,no_state_expansion=True,no_hardware=True)
    write(root/'plan.json',plan);(root/'plan.sha256').write_text(sha256(root/'plan.json')+'\n')
    for name in SOURCES:shutil.copy2(REPO/'test'/name,root/(name+'.source.txt'))
    shutil.copy2('/tmp/phase_abc_status_before.txt',root/'status_before.txt')
    return plan


def verify(root,full=False):
    plan=json.loads((root/'plan.json').read_text());assert sha256(root/'plan.json')==(root/'plan.sha256').read_text().strip()
    for p,h in plan['source_sha256'].items():assert sha256(Path(p))==h,p
    if full:
        for p,h in plan['protected_sha256'].items():assert sha256(Path(p))==h,p
    return plan


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--init',type=Path,required=True);a=p.parse_args();initialize(a.init.resolve())
