"""DESKTOP_DRY_RUN: compare real raw/applied MA2 and pre-filter bags, read-only.

All physics metrics are recorded telemetry; no new plant run or robot command.
"""
import argparse
import json
from pathlib import Path
import sqlite3

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from rclpy.serialization import deserialize_message
from tita_controller.msg import ActionFilterSample, TrainingSample
import analyze_pd_vibration as pd

REPO=Path(__file__).resolve().parents[2]


def rms(x):
    return np.sqrt(np.mean(x*x,axis=0)).tolist()


def load(bag,cfg,filtered):
    d=pd.load(bag,cfg['policy_interface']['actions'])
    with sqlite3.connect(f"file:{d['db']}?mode=ro",uri=True) as c:
        topics=dict(c.execute('SELECT name,id FROM topics'))
        rows=lambda name,cls:[deserialize_message(b,cls) for b, in c.execute(
            'SELECT data FROM messages WHERE topic_id=? ORDER BY timestamp',(topics[name],))]
        samples=rows('/sim2real/training_sample',TrainingSample)
        filters=rows('/sim2real/action_filter_sample',ActionFilterSample) if filtered else []
    table={(f.sequence_id,f.monotonic_ns):f for f in filters}
    assert len(table)==len(filters)
    get=lambda key:np.array([getattr(s,key) for s in samples])
    d['valid']=get('sensors_valid');d['policy_valid']=get('policy_valid')
    d['quat']=get('quaternion_wxyz');d['teacher']=get('teacher_action')
    d['applied']=d['action'].copy()
    d['missing_filter']=0
    for i,s in enumerate(samples):
        if not filtered:continue
        f=table.get((s.sequence_id,s.monotonic_ns))
        if f is None:
            d['missing_filter']+=1
            assert s.state!='rl', 'Missing applied RL sample'
            continue
        assert f.control_tick==s.control_tick and f.leg_action_filter=='ma2_legs'
        d['applied'][i]=f.action_applied
    rl=d['state']=='rl';d['rl']=rl
    assert get('sensors_valid')[rl].all() and get('policy_valid')[rl].all()
    assert get('output_enabled')[rl].all() and get('torque_sent')[rl].all()
    assert not d['bias'][rl].any()
    d['t']=(d['mono']-d['mono'][rl][0])*1e-9
    d['dt']=np.r_[.02,np.diff(d['mono'])*1e-9]
    assert (np.diff(get('sequence_id').astype(np.int64))==1).all()
    raw=d['action'].astype(np.float32)
    expected=raw.copy();previous=None
    legs=[i for i,t in enumerate(cfg['policy_interface']['actions'])
          if t['joint'] not in ('joint_left_leg_4','joint_right_leg_4')]
    for i,s in enumerate(samples):
        if s.state!='rl':previous=None;continue
        if filtered and previous is not None:
            expected[i,legs]=.5*raw[i,legs]+.5*previous[legs]
        previous=raw[i].copy()
    error=float(abs(expected[rl]-d['applied'][rl]).max())
    assert error==0.
    d['filter_replay_error']=error
    target=np.empty_like(d['action'])
    for i,a in enumerate(cfg['policy_interface']['actions']):
        j=pd.JOINTS.index(a['joint'])
        target[:,j]=np.clip(d['applied'][:,i]*a['scale']+a['offset'],*(a['clip'] or [-np.inf,np.inf]))
    d['target']=target
    d['teacher_error']=float(abs(d['teacher'][rl]-d['applied'][rl]).max())
    assert d['teacher_error']<1e-6
    kp,kd,limit=[np.array(cfg['robot'][k]) for k in ('joint_kp','joint_kd','torque_limit')]
    rebuilt=kp*(target-d['q'])-kd*d['dq']
    rebuilt[:,[3,7]]=kd[[3,7]]*(target[:,[3,7]]-d['dq'][:,[3,7]])
    rebuilt=np.clip(rebuilt,-limit,limit)
    d['torque_error']=float(abs(rebuilt[rl]-d['tau'][rl]).max());assert d['torque_error']<1e-8
    w,x,y,z=d['quat'].T
    d['pitch']=np.degrees(np.arcsin(np.clip(2*(w*y-z*x),-1,1)))
    d['roll']=np.degrees(np.arctan2(2*(w*x+y*z),1-2*(x*x+y*y)))
    d['tilt']=np.arccos(np.clip(1-2*(x*x+y*y),-1,1))
    d['pair']=np.r_[False,rl[1:]&rl[:-1]&(np.diff(d['tick'])==10)]
    age=np.zeros(len(rl));neutral_age=np.zeros(len(rl))
    neutral=(abs(d['command'])<=np.array([.02,.02,.03])).all(axis=1)
    for a,b in pd.runs(rl):
        age[a:b]=d['t'][a:b]-d['t'][a]
        for i in range(a+1,b):
            if neutral[i] and neutral[i-1]:neutral_age[i]=neutral_age[i-1]+d['dt'][i]
    d['neutral']=rl&neutral&(age>=3)&(neutral_age>=3)
    return d


def metrics(d,mask,cfg):
    pair=mask&d['pair']
    raw_delta=np.r_[np.zeros((1,8)),np.diff(d['action'],axis=0)]
    applied_delta=np.r_[np.zeros((1,8)),np.diff(d['applied'],axis=0)]
    target_delta=np.r_[np.zeros((1,8)),np.diff(d['target'],axis=0)]
    kp,kd=[np.array(cfg['robot'][k]) for k in ('joint_kp','joint_kd')]
    ff=target_delta*np.where(kp>0,kp,kd)
    step=d['tau']-d['tau_prev']
    sel=pair&np.isfinite(step).all(axis=1)
    segments=pd.runs(mask)
    def lag(value):
        consecutive=pair[1:]&pair[:-1]
        return [float(np.corrcoef(value[1:,j][consecutive],value[:-1,j][consecutive])[0,1])
                if np.std(value[1:,j][consecutive])>1e-9 else 0. for j in range(8)]
    def alt(value):
        # Average absolute parity projection within each contiguous neutral interval.
        terms=[];weights=[]
        for a,b in segments:
            if b-a<100:continue
            phase=(-1.)**np.arange(b-a)
            terms.append(abs(np.mean((value[a:b]-value[a:b].mean(0))*phase[:,None],axis=0)))
            weights.append(b-a)
        return np.average(terms,axis=0,weights=weights).tolist() if terms else None
    return dict(samples=int(mask.sum()),seconds=float(d['dt'][mask].sum()),
        intervals=[[float(d['t'][a]),float(d['t'][b-1])] for a,b in segments],
        pitch_mean_deg=float(d['pitch'][mask].mean()),pitch_std_deg=float(d['pitch'][mask].std()),
        raw_step_rms=rms(raw_delta[pair]),applied_step_rms=rms(applied_delta[pair]),
        raw_delta_lag1=lag(raw_delta),applied_delta_lag1=lag(applied_delta),
        raw_25hz_amp=alt(d['action']),applied_25hz_amp=alt(d['applied']),
        velocity_25hz_amp=alt(d['dq']),
        target_torque_step_rms_nm=rms(ff[pair]),actual_update_step_rms_nm=rms(step[sel]),
        state_residual_2ms_rms_nm=rms((step-ff)[sel]),
        reported_minus_previous_rms_nm=rms((d['reported']-d['tau_prev'])[sel]),
        torque_std_nm=d['tau'][mask].std(0).tolist(),torque_mean_nm=d['tau'][mask].mean(0).tolist(),
        joint_speed_step_rms=rms(np.r_[np.zeros((1,8)),np.diff(d['dq'],axis=0)][pair]),
        gyro_step_rms=rms(np.r_[np.zeros((1,3)),np.diff(d['gyro'],axis=0)][pair]),
        wheel_proxy_mean_m_s=float((.0925*d['dq'][mask][:,[3,7]].mean(1)).mean()),
        psd_pitch=pd.band_powers(d['pitch'][:,None],segments),
        psd_raw=pd.band_powers(d['action'],segments),psd_applied=pd.band_powers(d['applied'],segments),
        psd_velocity=pd.band_powers(d['dq'],segments),psd_gyro=pd.band_powers(d['gyro'],segments),
        final_torque_clip_fraction=(abs(d['tau'][mask])>=np.array(cfg['robot']['torque_limit'])-1e-6).mean(0).tolist())


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,required=True)
    args=p.parse_args();out=args.output.resolve()
    cfg_path=REPO/'sim2real/tita_ws/src/tita_controller/policies/flashsac_80000/config.json'
    cfg=json.loads(cfg_path.read_text());assert pd.digest(cfg_path)=='a24c2137969f854fc98cc3027884dbbadad4060f18db7758b028c12ca1405719'
    paths={'off':REPO/'docs/exp/2026-10-18/flashsac_knee92_bias_pair/flashsac_80000_125618_839843723_output_true_bag',
           'ma2':next(out.glob('*135923*_bag'))}
    cases={};signals={}
    for name,path in paths.items():
        d=load(path,cfg,name=='ma2');signals[name]=d;rl=d['rl'];events=[]
        for i in np.flatnonzero(np.r_[True,d['state'][1:]!=d['state'][:-1]]):
            events.append(dict(t_s=float(d['t'][i]),state=d['state'][i],valid=bool(d['valid'][i]),
                pitch_deg=float(d['pitch'][i]),roll_deg=float(d['roll'][i]),tilt_rad=float(d['tilt'][i])))
        damp=np.flatnonzero(d['state']=='damp');fault=[]
        if len(damp):
            i=damp[0]
            for k in range(max(0,i-5),min(len(rl),i+6)):
                fault.append(dict(t_s=float(d['t'][k]),state=d['state'][k],valid=bool(d['valid'][k]),
                    pitch_deg=float(d['pitch'][k]),roll_deg=float(d['roll'][k]),tilt_rad=float(d['tilt'][k])))
        cases[name]=dict(source_db=d['db'],source_db_sha256=d['db_sha256'],
            rl_duration_s=float(d['t'][rl][-1]),rl_dt_max_s=float(d['dt'][rl].max()),
            missing_filter_frames=d['missing_filter'],filter_replay_max_error=d['filter_replay_error'],
            teacher_applied_max_error=d['teacher_error'],torque_reconstruction_max_error_nm=d['torque_error'],
            fitted_gains=pd.fit_gains(d,rl),neutral_hold=metrics(d,d['neutral'],cfg),
            first_neutral_5_10=metrics(d,d['neutral']&(d['t']>=5)&(d['t']<10),cfg),
            matched_initial_3_7p8=metrics(d,d['neutral']&(d['t']>=3)&(d['t']<7.8),cfg),
            state_events=events,damp_window=fault,
            neutral_blocks=[dict(start_s=float(d['t'][a]),end_s=float(d['t'][b-1]))
                            for a,b in pd.runs(d['neutral'])])
        np.savez_compressed(out/f'{name}_signals.npz',**{k:v for k,v in d.items() if isinstance(v,np.ndarray)})
    report=dict(execution_domain='DESKTOP_DRY_RUN',evidence_status='SUSPICIOUS',
        operator_annotation='Only sticks; no hand-applied disturbances reported',
        checkpoint_sha256=cfg['policy_interface']['checkpoint_sha256'],onnx_sha256=cfg['policy_interface']['onnx_sha256'],
        config_sha256=pd.digest(cfg_path),cases=cases,
        limitations=['Separate command profiles and starting postures; not a randomized paired trial.',
            '50 Hz samples alias content above 25 Hz; no direct acoustic measurement.',
            'Computed command and SDK torque feedback are not calibrated joint force.',
            'A sample showing no fault cannot rule out a 500 Hz fault between logged frames.'],
        sources={str(p.relative_to(REPO)):pd.digest(p) for p in (Path(__file__),REPO/'test/sim2real/analyze_pd_vibration.py',cfg_path)})
    (out/'metrics.json').write_text(json.dumps(report,indent=2)+'\n')
    fig,axes=plt.subplots(5,2,figsize=(14,12),sharex='col',constrained_layout=True)
    for col,name in enumerate(('off','ma2')):
        d=signals[name];mask=d['rl'];t=d['t'][mask]
        axes[0,col].plot(t,d['command'][mask,0],label='vx');axes[0,col].plot(t,d['command'][mask,2],label='yaw')
        axes[1,col].plot(t,d['pitch'][mask],label='pitch')
        axes[2,col].plot(t,d['action'][mask,2],label='raw knee L',lw=.7)
        axes[2,col].plot(t,d['applied'][mask,2],label='applied knee L',lw=.7)
        axes[3,col].plot(t,d['tau'][mask,2],label='computed knee L',lw=.6)
        axes[4,col].plot(t,d['dq'][mask,2],label='knee L speed',lw=.6)
        axes[0,col].set_title(name.upper())
        for row,unit in enumerate(('command','deg','action','Nm','rad/s')):
            axes[row,col].set_ylabel(unit);axes[row,col].grid(alpha=.2);axes[row,col].legend(fontsize=8)
        axes[4,col].set_xlabel('Seconds from RL entry')
    fig.suptitle('Real MA2 leg filter vs same-gain OFF run; separate operator trials')
    fig.savefig(out/'comparison.png',dpi=160);plt.close(fig)
    fig,axes=plt.subplots(4,2,figsize=(13,9),sharex='col',constrained_layout=True)
    for col,name in enumerate(('off','ma2')):
        d=signals[name];mask=d['rl']&(d['t']>=5)&(d['t']<6);t=d['t'][mask]
        axes[0,col].plot(t,d['action'][mask,2],label='raw knee L',marker='.',ms=3)
        axes[0,col].plot(t,d['applied'][mask,2],label='applied knee L',marker='.',ms=3)
        axes[1,col].plot(t,d['tau'][mask,2],label='computed knee L',marker='.',ms=3)
        axes[2,col].plot(t,d['dq'][mask,2],label='knee L speed',marker='.',ms=3)
        axes[3,col].plot(t,d['pitch'][mask],label='pitch',marker='.',ms=3)
        axes[0,col].set_title(name.upper())
        for row,unit in enumerate(('action','Nm','rad/s','deg')):
            axes[row,col].set_ylabel(unit);axes[row,col].grid(alpha=.2);axes[row,col].legend(fontsize=8)
        axes[3,col].set_xlabel('Seconds from RL entry')
    fig.suptitle('One neutral second: 25 Hz alternation reduced; remaining motion has a different frequency')
    fig.savefig(out/'neutral_zoom.png',dpi=160);plt.close(fig)
    print(json.dumps(report,indent=2))


if __name__=='__main__':main()
