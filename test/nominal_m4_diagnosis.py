"""DESKTOP_DRY_RUN: preregistered Nominal identification comparison, no control."""
import hashlib
import json
from pathlib import Path
import shutil
import subprocess

import numpy as np

from eval_flash_operating_local import REPO, CKPT, BIAS, cases
from eval_flash_pv_models import prepared_config, sha256
from run_static_target_adaptation import write
from analyze_flash_operating_affine import load_absolute, evaluate_affine
from analyze_flash_operating_local import summarize_all
from analyze_flash_stop_local import predict
from analyze_flash_state_learning import state, fit, load
from flash_cold_start_abc import fit_batch

LOCAL=REPO/'docs/exp/2026-10-15/flash_operating_local/full'
AFFINE=REPO/'docs/exp/2026-10-15/flash_affine_lqr'
ABC=REPO/'docs/exp/2026-10-16/cold_start_abc_diagnostics/run_01'
SOURCES=['nominal_m4_diagnosis.py','run_nominal_m4_diagnosis.py',
         'analyze_nominal_m4_diagnosis.py','test_nominal_m4_diagnosis.py']
TIMES=[10.,30.,60.,1000.]
METHODS=['paired_c','joint']
PROFILES=['small','quantity','waveforms','initials','full','full_replicates']


def starts(split):
    return [dict(seed=s,pitch=p,pitch_index=i,split=split,id=f'{split}_s{s}_p{p:+.3f}')
            for s in ([800,801]if split=='train'else[810,811])for i,p in enumerate([-.035,0.,.035])]


def probe_cases(split):
    result=[dict(family=f,amplitude=a,replica=0)for f,a in cases(split)]
    if split=='train':
        result += [dict(family=f,amplitude=.02,replica=j)for j in [1,2]for f in ['train_sine','train_prbs']]
    return result


def choose(records,profile):
    """Prespecified quantity-matched contrasts, never selected by test outcome."""
    chosen=[]
    for row in records:
        seed,pitch=row['seed'],row['pitch'];family=row['family'];amp=row['amplitude'];rep=row.get('replica',0)
        one=seed==800 and pitch==0.;three=seed==800
        two=family in ['train_sine','train_prbs']and amp==.02
        six=family in ['train_sine','train_prbs','pulse_pos','pulse_neg','step_pos','step_neg']and amp==.02
        keep={'small':one and two and rep==0,'quantity':one and two,
              'waveforms':one and six and rep==0,'initials':three and two and rep==0,
              'full':rep==0,'full_replicates':True}[profile]
        if keep:chosen.append(row)
    return chosen


def unique_baselines(records):
    found={}
    for r in records:
        key=(r['context'],r['start_rl_s'])
        if key not in found:
            found[key]=dict(r,absolute=r['base'],u=r['base_u'],delta=np.zeros_like(r['base']),family='zero')
    return list(found.values())


def fit_method(records,method,rcond=1e-10,nominal_center=False):
    """Paired AB+baseline defect vs joint affine LS on the same raw pairs."""
    baseline=unique_baselines(records)
    if nominal_center:
        streams=[(r['absolute'],r['u'],np.ones(len(r['u']),dtype=bool))for r in records+baseline]
        model,diag=fit_batch(streams);model.update(kind='affine',input_reference=BIAS,indices=list(range(24)))
        model['fit_diagnostics']=diag
        return model
    paired=method=='paired_c';rows=records if paired else records+baseline
    x=np.concatenate([r['delta'if paired else'absolute'][:-1]for r in rows])
    y=np.concatenate([r['delta'if paired else'absolute'][1:]for r in rows])
    u=np.concatenate([r['u']-r['base_u']if paired else r['u']for r in rows])
    ref=np.zeros(24)if paired else x.mean(0);uref=0. if paired else float(u.mean())
    xc=x-ref;target=y-ref;target[:,0]-=xc[:,0]
    X=np.column_stack([xc[:,1:],u-uref]+([]if paired else[np.ones(len(u))]))
    scale=np.maximum(np.sqrt(np.mean(X**2,axis=0)),1e-14)
    coefficient,_,rank,sv=np.linalg.lstsq(X/scale,target,rcond=rcond);coefficient=(coefficient/scale[:,None]).T
    A=np.zeros((24,24));A[0,0]=1.;A[:,1:]=coefficient[:,:23];B=coefficient[:,23].copy()
    c=np.zeros(24)if paired else coefficient[:,-1].copy()
    columns=[i for i in range(X.shape[1])if i!=23]
    action=np.linalg.lstsq(X[:,columns]/scale[columns],target[:,4:12],rcond=rcond)[0]/scale[columns,None]
    A[4:12,1:]=action[:23].T;B[4:12]=0.
    if not paired:c[4:12]=action[-1]
    if paired:
        bx=np.concatenate([r['absolute'][:-1]for r in baseline]);by=np.concatenate([r['absolute'][1:]for r in baseline]);bu=np.concatenate([r['u']for r in baseline])
        ref=bx.mean(0);uref=BIAS;c=np.mean((by-ref)-(bx-ref)@A.T-(bu[:,None]-uref)*B,axis=0)
    return dict(name='M4',kind='affine',mode='frozen',indices=list(range(24)),A=A.tolist(),B=B.tolist(),
        state_reference=ref.tolist(),input_reference=uref,c_center=c.tolist(),
        c_absolute=(ref-A@ref-B*uref+c).tolist(),rank=int(rank),scaled_condition=float(sv[0]/max(sv[-1],1e-300)),
        rcond=rcond,method=method,probe_transitions=sum(len(r['u'])for r in records),
        fit_transitions=len(u),baseline_transitions=sum(len(r['u'])for r in baseline),
        response_count=len(records),initial_conditions=len({r['context']for r in records}),
        rho_nonposition=float(max(abs(np.linalg.eigvals(A[1:,1:])))))


def read_new(root,split,time):
    records=[];direct=[]
    for path in sorted((root/split).glob('*/results.json')):
        result=json.loads(path.read_text());job=result['job']
        for snap in result['snapshots']:
            if snap['time']!=time or snap['status']!='COMPLETE':continue
            directory=path.parent/snap['folder']
            with np.load(directory/'baseline.npz')as t:base=state(t);bu=t['actual_u'].copy()
            anchor=base[0,0];base[:,0]-=anchor
            for r in snap['responses']:
                with np.load(directory/r['file'])as t:z=state(t);u=t['actual_u'].copy()
                z[:,0]-=anchor
                records.append(dict(context=job['id'],seed=job['seed'],pitch=job['pitch'],start_rl_s=time,
                    family=r['family'],amplitude=r['amplitude'],replica=r['replica'],absolute=z,base=base,delta=z-base,u=u,base_u=bu))
            direct.append(dict(context=job['id'],time=time,B=np.asarray(snap['Direct_B'])))
    return records,direct


def score(model,records,direct):
    if not records:return dict(status='NOT_TESTED',reason='no complete safe snapshots')
    stats,_=evaluate_affine(model,records);summary=summarize_all(stats)
    ref=float(np.median([r['B'][1]for r in direct]));berr=abs(model['B'][1]/ref-1)
    def response_gate(indices):
        return bool(all(np.all(np.median(stats['horizons'][str(h)]['nrmse'][indices],0)<=.3)for h in [5,25,50,100])and
                    np.all(np.median(stats['full2s']['nrmse'][indices],0)<=.3))
    baselines=unique_baselines(records);base_rows=[]
    for row in baselines:
        prediction=predict(model,row['absolute'][None,0],row['u'][None])[0]
        e=[np.sqrt(np.mean((prediction[1:end+1,:2]-row['absolute'][1:end+1,:2])**2,axis=0))for end in [100,400]]
        base_rows.append(dict(context=row['context'],time=row['start_rl_s'],RMSE2=e[0].tolist(),RMSE8=e[1].tolist(),
            gate=bool(np.all(e[0]<=[2e-5,2e-5])and np.all(e[1]<=[5e-5,2e-5]))))
    contexts=[]
    for ctx in sorted({r['context']for r in records}):
        ix=[i for i,r in enumerate(records)if r['context']==ctx];d=next(r for r in direct if r['context']==ctx)
        bg=bool(model['B'][1]*d['B'][1]>0 and abs(model['B'][1]/d['B'][1]-1)<=.3)
        contexts.append(dict(context=ctx,gate=response_gate(ix)and bg and all(b['gate']for b in base_rows if b['context']==ctx),
            full2=np.median(stats['full2s']['nrmse'][ix],0).tolist(),rolling2=np.median(stats['horizons']['100']['nrmse'][ix],0).tolist()))
    gate=response_gate(list(range(len(records))))and berr<=.3 and model['B'][1]*ref>0 and all(b['gate']for b in base_rows)
    return dict(status='PASS'if gate else'FAIL',gate=bool(gate),metrics=summary,B_error=float(berr),direct_B=ref,
        response_gate=response_gate(list(range(len(records)))),baseline_gate=all(b['gate']for b in base_rows),baselines=base_rows,
        contexts=contexts,passed_contexts=sum(c['gate']for c in contexts),total_contexts=len(contexts),responses=len(records))


def initialize(root):
    assert not root.exists();root.mkdir(parents=True)
    old=json.loads((ABC/'plan.json').read_text());protected=dict(old['protected_sha256'])
    for folder in [LOCAL,AFFINE,ABC]:
        protected.update({str(p):sha256(p)for p in folder.rglob('*')if p.is_file()})
    # Dependencies include all existing test helpers and production execution inputs.
    protected.update({str(p):sha256(p)for p in (REPO/'test').glob('*.py')if p.name not in SOURCES})
    plan=dict(execution_domain='VALIDATION_SIM',analysis_domain='DESKTOP_DRY_RUN',checkpoint_sha256=sha256(CKPT/'actor.pt'),
        source_sha256={str(REPO/'test'/s):sha256(REPO/'test'/s)for s in SOURCES},protected_sha256=protected,
        tracked_diff_sha256=hashlib.sha256(subprocess.check_output(['git','diff','--binary'])).hexdigest(),
        old_success_source=str(LOCAL),old_affine_source=str(AFFINE),previous_C=str(ABC),
        scope='Nominal identification causes only; no RLS tuning, new gain, online control, odometry correction, hardware, D/E/F',
        starts={s:starts(s)for s in ['train','test']},times=TIMES,region='same zero-command constant bias rollout from startup, cold10/30/60 and settled1000s',
        control='frozen FlashSAC/native PD; no LQR, bias0.4828 from firstRL with2Nm/s slew; immutable p_hold; nominal physics throughout',
        train_cases=probe_cases('train'),test_cases=probe_cases('test'),length=400,
        limits=dict(residual=[.4328,.5328],slew=2.,wheel=12.,probe_speed=.02,probe_pitch=.2),
        settled_gate='unchanged past180s within240s hold_metrics, evaluation only; no target/control reset',
        methods=METHODS,profiles=PROFILES,numeric_auxiliary='full profile: paired rcond1e-8, joint rcond1e-8, fixed-nominal centered joint phaseC fitter1e-8',
        quantity_matching='small2 vs quantity6 same2families repeated; waveforms6 at same state; initials6 over3starts; all amplitude.02. full78/full_replicates102',
        additional_stream_fits='same fresh train prefix10-60 and950-1000, joint1e-10 and fixed-nominal1e-8',
        primary='same-region absolute first2s + rolling0.1/0.5/1/2s p/v medianNRMSE<=30%, DirectBv sign/error<=30%, all baselines2s<=20um/20um_s and8s<=50um/20um_s; report both aggregate and6/6 contexts',
        supplemental='paired delta8s, absolute8s, rolling4s; report errors, no relaxed gate',
        legacy='refit original234 paired responses and c18baselines; recalculate306test and204fresh; exact physical replay3old snapshots baseline+PRBS',
        cross_region='full paired/joint models at each train time tested on all4test times, other profiles matched-time only',
        freeze_before_test=True,no_threshold_changes=True,no_policy_QR_state_change=True)
    write(root/'plan.json',plan);(root/'plan.sha256').write_text(sha256(root/'plan.json')+'\n')
    for s in SOURCES:shutil.copy2(REPO/'test'/s,root/(s+'.source.txt'))
    shutil.copy2('/tmp/nominal_m4_identification_status_before.txt',root/'status_before.txt')
    return plan


def verify(root,full=False):
    plan=json.loads((root/'plan.json').read_text());assert sha256(root/'plan.json')==(root/'plan.sha256').read_text().strip()
    for path,h in plan['source_sha256'].items():assert sha256(Path(path))==h,path
    if full:
        for path,h in plan['protected_sha256'].items():assert sha256(Path(path))==h,path
    return plan
