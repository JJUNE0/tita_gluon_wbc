"""DESKTOP_DRY_RUN: constrained RLS objectives and sensor-only local validation.

No simulator, domain parameter or ground-truth argument enters an estimator.
"""
import copy
from collections import deque
import hashlib
import json
from pathlib import Path
import shutil
import subprocess

import numpy as np

from m4_shadow_stages import ConstrainedRLS
from m4_joint_adaptation import nominal,BIAS,LOW,HIGH,advance
from nominal_m4_diagnosis import REPO,CKPT,sha256,read_new,unique_baselines
from run_static_target_adaptation import write
from flash_cold_start_abc import fit_batch,information

NOMINAL_ROOT=REPO/'docs/exp/2026-10-16/nominal_m4_identification_diagnosis/run_01'
ABC=REPO/'docs/exp/2026-10-16/cold_start_abc_diagnostics/run_01'
SOURCES=['online_local_m4.py','run_online_local_m4.py','test_online_local_m4.py','analyze_online_local_m4.py']
A_SETTINGS=[dict(name='A1_plain',method='plain',forgetting=1.,P=0.,mean='nominal'),
    dict(name='A2_weighted_batch',method='batch',forgetting=.9995,P=100.,mean='nominal'),
    dict(name='A3_recursive',method='recursive',forgetting=.9995,P=100.,mean='nominal'),
    dict(name='A4_lambda1_P100',method='recursive',forgetting=1.,P=100.,mean='nominal'),
    dict(name='A4_lambda1_P1e8',method='recursive',forgetting=1.,P=1e8,mean='nominal'),
    dict(name='A4_lambda1_P1e8_zero',method='recursive',forgetting=1.,P=1e8,mean='zero')]
B_SETTINGS=[dict(name='local20',window=20.,forgetting=1.,P=1e8),
    dict(name='local10',window=10.,forgetting=1.,P=1e8),
    dict(name='cumulative_weak',window=None,forgetting=1.,P=1e8),
    dict(name='cumulative_original',window=None,forgetting=.9995,P=100.),
    dict(name='cumulative_P100',window=None,forgetting=1.,P=100.)]
CHECKPOINTS=[10.,30.,60.]


def training_allowed(time):
    """Validation transitions are permanently excluded, including later windows."""
    return not any(t-1e-9<=time<t+4.-1e-9 for t in CHECKPOINTS)


def features(streams,prior=None):
    r=ConstrainedRLS(nominal()if prior is None else prior);X=[];Y=[]
    for z,u,mask in streams:
        x=(z[:-1]-r.ref)/r.scale;y=(z[1:]-r.ref)/r.scale;y[:,0]-=x[:,0]
        X.append(np.column_stack([x[:,1:],(u-BIAS)/.05,np.ones(len(u))])[mask]);Y.append(y[mask])
    return np.concatenate(X),np.concatenate(Y)


def objective(X,Y,forgetting=1.,P=100.,mean='nominal',prior=None):
    """Independent augmented SVD solution of the exact finite-prior RLS cost."""
    estimator=ConstrainedRLS(nominal()if prior is None else prior);n=len(X);details=[]
    w=forgetting**np.arange(n-1,-1,-1);alpha=forgetting**n/P
    for g in estimator.groups:
        columns=g['columns'];rows=g['rows'];theta0=g['theta'].copy()
        if mean=='zero':theta0[:]=0.
        d=np.vstack([np.sqrt(w)[:,None]*X[:,columns],np.sqrt(alpha)*np.eye(len(columns))])
        target=np.vstack([np.sqrt(w)[:,None]*Y[:,rows],np.sqrt(alpha)*theta0.T])
        coefficient,_,rank,s=np.linalg.lstsq(d,target,rcond=None)
        # SVD covariance avoids squaring the augmented design condition.
        _,singular,V=np.linalg.svd(d,full_matrices=False)
        g['theta']=coefficient.T;g['P']=(V.T/singular**2)@V
        details.append(dict(rank=int(rank),augmented_condition=float(s[0]/s[-1])))
    estimator.count=n
    return estimator,details


def theta_difference(a,b):
    return max(float(np.linalg.norm(x['theta']-y['theta'])/max(np.linalg.norm(y['theta']),1e-15))for x,y in zip(a.groups,b.groups))


class LocalRLS(ConstrainedRLS):
    """20ms covariance RLS, exact window downdates, same-objective SVD candidates.

    Candidate refinement is predefined numerical stabilization, not a new cost.
    The live recursion and its discrepancy are retained for audit.
    """
    def __init__(self,setting,prior=None):
        self.setting=copy.deepcopy(setting)
        super().__init__(nominal()if prior is None else prior,forgetting=setting['forgetting'],prior_covariance=setting['P'])
        self.buffer=deque();self.rebuilds=[];self.rejected=[]

    def expire(self,time):
        window=self.setting['window']
        if window is None:return
        assert self.forgetting==1.
        while self.buffer and self.buffer[0][0]<=time-window+1e-9:
            _,feature,target=self.buffer.popleft();self.features.pop(0)
            try:
                for g in self.groups:
                    p=feature[g['columns']];q=g['P']@p;denominator=1.-p@q
                    if denominator<=1e-8:raise FloatingPointError('downdate denominator')
                    gain=q/denominator;g['theta']-=np.outer(target[g['rows']]-g['theta']@p,gain)
                    g['P']+=np.outer(q,q)/denominator;g['P']=(g['P']+g['P'].T)*.5
            except (FloatingPointError,ValueError):self.rebuild(time,'downdate conditioning')

    def rebuild(self,time,reason):
        if self.buffer:
            X=np.asarray([r[1]for r in self.buffer]);Y=np.asarray([r[2]for r in self.buffer])
            exact,_=objective(X,Y,self.forgetting,self.setting['P'],prior=self.original)
        else:exact=ConstrainedRLS(self.original,forgetting=self.forgetting,prior_covariance=self.setting['P'])
        for current,other in zip(self.groups,exact.groups):current['theta']=other['theta'];current['P']=other['P']
        self.rebuilds.append(dict(time=time,reason=reason))

    def observe(self,time,before,u,after,eligible=True):
        self.expire(time)
        if not eligible:
            self.rejected.append(dict(time=time,reason='validation_or_safety_exclusion'));return
        x=(np.asarray(before)-self.ref)/self.scale;y=(np.asarray(after)-self.ref)/self.scale;y[0]-=x[0]
        f=np.r_[x[1:],(u-BIAS)/.05,1.]
        old_count=self.count;self.buffer.append((float(time),f,y))
        try:super().update(before,u,after)
        except FloatingPointError:
            self.features=[r[1]for r in self.buffer];self.count=old_count+1
            self.rebuild(time,'nonfinite covariance recursion; exact same-objective rebuild')
        if self.count%250==0 and min(np.linalg.eigvalsh(g['P']).min()for g in self.groups)<=0.:self.rebuild(time,'covariance positivity')

    def freeze(self,time):
        self.expire(time)
        if len(self.buffer)<25:return dict(status='NOT_TESTED',reason='samples<25',samples=len(self.buffer))
        X=np.asarray([r[1]for r in self.buffer]);Y=np.asarray([r[2]for r in self.buffer])
        exact,details=objective(X,Y,self.forgetting,self.setting['P'],prior=self.original)
        # Information uses observed regressors, not the artificial prior rows.
        rms=np.maximum(np.sqrt(np.mean(X**2,axis=0)),1e-12);s=np.linalg.svd(X/rms,compute_uv=False)
        rank=int(np.sum(s>s[0]*1e-8));other=np.delete(X/rms,23,axis=1);signal=X[:,23]/rms[23]
        innovation=signal-other@np.linalg.lstsq(other,signal,rcond=1e-8)[0]
        fraction=float(innovation@innovation/max(signal@signal,1e-20));condition=float(s[0]/max(s[-1],1e-300))
        minimum=min(float(np.linalg.eigvalsh(g['P']).min())for g in exact.groups)
        info=dict(samples=len(X),rank=rank,condition=condition,input_innovation=fraction,P_min=minimum,
            gate=bool(len(X)>=250 and rank==25 and condition<=1e6 and fraction>=.01 and minimum>0.))
        model=exact.model();model['active_samples']=len(X)
        return dict(status='FROZEN',model=model,raw_recursive_model=self.model(),information=info,
            recursion_vs_exact=theta_difference(self,exact),numerical_refinement='same prior/forgetting objective, no projection',
            first_training_time=self.buffer[0][0],last_training_time=self.buffer[-1][0],created=time,
            training_times=[r[0]for r in self.buffer],SVD=details)


def validate_candidate(model,states,inputs):
    """Only subsequent actual sensor/known commands. No Direct B or snapshots."""
    x=np.asarray(states);u=np.asarray(inputs);n=len(u);scores={};all_gate=True
    for h in [5,25,50,100]:
        starts=np.arange(0,n-h+1,5);pred=x[starts].copy()
        with np.errstate(over='ignore',invalid='ignore'):
            for j in range(h):pred=np.asarray([advance(model,z,v)for z,v in zip(pred,u[starts+j])])
            error=np.sqrt(np.mean((pred[:,:2]-x[starts+h,:2])**2,axis=0));signal=np.maximum(np.sqrt(np.mean((x[starts+h,:2]-x[starts,:2])**2,axis=0)),[1e-7,1e-5])
        norm=error/signal;gate=bool(np.isfinite(error).all()and np.all(error<=2e-5)and np.all(norm<=.3));all_gate&=gate
        scores[str(h)]=dict(RMSE=error.tolist(),NRMSE=norm.tolist(),gate=gate)
    full={}
    for length in [100,200]:
        pred=x[0].copy();errors=[]
        with np.errstate(over='ignore',invalid='ignore'):
            for j in range(length):pred=advance(model,pred,u[j]);errors.append(pred[:2]-x[j+1,:2])
            rmse=np.sqrt(np.mean(np.asarray(errors)**2,axis=0));signal=np.maximum(np.sqrt(np.mean((x[1:length+1,:2]-x[0,:2])**2,axis=0)),[1e-7,1e-5])
        limit=np.array([2e-5,2e-5])if length==100 else np.array([5e-5,2e-5]);gate=bool(np.isfinite(rmse).all()and np.all(rmse<=limit)and np.all(rmse/signal<=.3));all_gate&=gate
        full[str(length)]=dict(RMSE=rmse.tolist(),NRMSE=(rmse/signal).tolist(),gate=gate)
    # Conditional B regression has different information from offline matched Direct B.
    X,_=features([(x,u,np.ones(n,dtype=bool))]);rms=np.maximum(np.sqrt(np.mean(X**2,axis=0)),1e-12);singular=np.linalg.svd(X/rms,compute_uv=False)
    rank=int(np.sum(singular>singular[0]*1e-8));condition=float(singular[0]/max(singular[-1],1e-300))
    coefficient=np.linalg.lstsq(X/rms,x[1:,1],rcond=1e-8)[0]/rms;bv=float(coefficient[23]/.05)
    relative=float(abs(model['B'][1]-bv)/max(abs(bv),1e-12));b_gate=bool(rank==25 and condition<=1e6 and model['B'][1]*bv>0 and relative<=.3)
    return dict(gate=bool(all_gate and b_gate),prediction_gate=bool(all_gate),rolling=scores,full=full,
        conditional_B=dict(value=bv,relative_error=relative,rank=rank,condition=condition,gate=b_gate,kind='subsequent sensor regression; not Direct B'))


def initialize(root):
    assert not root.exists();root.mkdir(parents=True)
    previous=json.loads((NOMINAL_ROOT/'plan.json').read_text());protected=dict(previous['protected_sha256'])
    for folder in [NOMINAL_ROOT,ABC]:protected.update({str(p):sha256(p)for p in folder.rglob('*')if p.is_file()})
    protected.update({str(p):sha256(p)for p in (REPO/'test').glob('*.py')if p.name not in SOURCES})
    plan=dict(execution_domain='VALIDATION_SIM',analysis_domain='DESKTOP_DRY_RUN',checkpoint_sha256=sha256(CKPT/'actor.pt'),
        source_sha256={str(REPO/'test'/s):sha256(REPO/'test'/s)for s in SOURCES},protected_sha256=protected,
        tracked_diff_sha256=hashlib.sha256(subprocess.check_output(['git','diff','--binary'])).hexdigest(),
        A=dict(settings=A_SETTINGS,cohorts=['nominal10','nominal30','nominal60','nominal1000','friction0.2post'],
            reuse_only=True,freeze_before_scoring=True,A2_A3_relative_theta_tolerance=1e-7,selection='none; B settings fixed independently of A outcomes'),
        B=dict(settings=B_SETTINGS,domains=[dict(name='nominal',effect={}),dict(name='friction0.2',effect=dict(friction=.2))],
            amplitudes=[.01,.02],development=[dict(seed=s,pitch=p)for s,p in zip([900,901,902],[-.035,0.,.035])],
            test=[dict(seed=s,pitch=p)for s in [910,911]for p in [-.035,0.,.035]],duration=64.,checkpoints=CHECKPOINTS,
            training='single physical rollout; no clones/DirectB; update20ms known applied command; include residual band cap samples but exclude known native command clipping, nonfinite and sensor posture/leg violations; no GT-derived eligibility',
            validation='candidate frozen at10/30/60; subsequent4s continuous sensor sequence. Exclude these transitions permanently from all estimators, now and later.',
            probes='trainPRBS outside windows; new validation sine/PRBS/bipulse in windows; only sensor safety and raw fixed control interior margin amplitude+0.002 permit excitation',
            candidate='raw covariance RLS updated every20ms; candidate SVD refinement solves exactly same fixed prior/forgetting cost; retain raw model and discrepancy',
            initial_goal='firstRL p_hold immutable; nominal fixed regression centering and raw M4; no FK correction',
            prediction='all rolling0.1/0.5/1/2s absolute p/v RMSE<=20um/20um_s and NRMSE<=30%; full2s<=20/20,full4s<=50/20; conditionalB rank25,condition<=1e6,sign/error<=30%',
            information='observed rank25,condition<=1e6,input innovation>=1%,positive P,samples>=250; no prior rows counted as excitation',
            selection='C method/amplitude determined from dev3/3 at least one verified candidate per trial, priority local20/local10/cumulative_weak/original/P100, amp0.01 before0.02; heldout6/6 confirmation required'),
        C=dict(conditional=True,domains_independent=True,starts=[dict(seed=s,pitch=p)for s in [940,941]for p in [-.035,0.,.035]],
            arms=['Fixed','BiasReference','AdaptiveK','Full'],duration=180.,candidate_times=[10.,30.,60.,90.,120.,150.],
            permission='only verified same frozen candidate, training info and future validation, current interior/safety/support, DARE, nominal/candidate rho, per/cumulative25%,K raw jump0.003 and joint0.005',
            operating='B1 5s past quiet p integral0.5,max0.0005Nm/s; reference20s past average,10s cadence; originalp/vgoal fixed; existing comfort limits; operating estimate gates independent of RLS rank',
            quiet='sensor speedRMS<=0.001,pitchstd<=0.002,5s unsaturated; existing reference_target and common joint jump guards; freeze all control parameters during candidate validation',
            fairness='all4 arms same proposed probe process and actuator budget; actual probe effort depends safe gate and is scored; compare original firstRL target full0-180s',
            success='completion6/6; fullIAE median>=10% reduction vs both Fixed and BiasReference,paired>=4/6 each,last5RMSE<=120%; actual targetK adoption separately reported; absolute hold maxplanar<=50mm,terminal<=10mm,last5speed<=0.2mm/s',
            implementation='new experimental control source only if B admits a branch; freeze that source before C; never relax B or gain guards'),
        limits=dict(residual=[LOW,HIGH],slew=2.,wheel=12.,initial_ramp_s=1.5),
        no_QR_threshold_state_changes=True,no_snapshots_or_labels_in_estimator=True,no_hardware=True,no_policy_runtime_changes=True)
    write(root/'plan.json',plan);(root/'plan.sha256').write_text(sha256(root/'plan.json')+'\n')
    for s in SOURCES:shutil.copy2(REPO/'test'/s,root/(s+'.source.txt'))
    shutil.copy2('/tmp/online_local_m4_status_before.txt',root/'status_before.txt')


def verify(root,full=False):
    plan=json.loads((root/'plan.json').read_text());assert sha256(root/'plan.json')==(root/'plan.sha256').read_text().strip()
    for p,h in plan['source_sha256'].items():assert sha256(Path(p))==h,p
    if full:
        for p,h in plan['protected_sha256'].items():assert sha256(Path(p))==h,p
    return plan
