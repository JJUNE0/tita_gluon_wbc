"""DESKTOP_DRY_RUN: recorded sensor/command analysis; no ROS node or robot SDK."""
import argparse
import hashlib
import json
from pathlib import Path
import sqlite3
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from rclpy.serialization import deserialize_message
from tita_controller.msg import TrainingSample, MotorFeedback
from validate_sit_transitions import library, SupportingSit, REPO

p=argparse.ArgumentParser(description=__doc__);p.add_argument('root',type=Path);a=p.parse_args()
db=next(a.root.rglob('*.db3')); before=hashlib.sha256(db.read_bytes()).hexdigest()
with sqlite3.connect(f'file:{db.resolve()}?mode=ro',uri=True) as c:
    assert c.execute('PRAGMA quick_check').fetchone()[0]=='ok'
    topics={name:i for i,name in c.execute('SELECT id,name FROM topics')}
    samples=[deserialize_message(raw,TrainingSample) for raw, in c.execute('SELECT data FROM messages WHERE topic_id=? ORDER BY timestamp',(topics['/sim2real/training_sample'],))]
    feedback={m.sequence_id:m for raw, in c.execute('SELECT data FROM messages WHERE topic_id=? ORDER BY timestamp',(topics['/sim2real/motor_feedback'],)) for m in [deserialize_message(raw,MotorFeedback)]}
get=lambda name:np.array([getattr(s,name) for s in samples])
mono=get('monotonic_ns').astype(np.int64);seq=get('sequence_id').astype(np.int64);tick=get('control_tick').astype(np.int64)
assert np.all(np.diff(mono)>0) and np.all(np.diff(seq)==1)
t=(mono-mono[0])*1e-9;states=get('state');q=get('joint_position');dq=get('joint_velocity');quat=get('quaternion_wxyz');gyro=get('angular_velocity');tau=get('computed_torque');command=get('command')
assert all(np.isfinite(v).all() for v in [q,dq,quat,gyro,tau,command])
w,x,y,z=quat.T
pitch=np.degrees(np.arcsin(np.clip(2*(w*y-z*x),-1,1)))
roll=np.degrees(np.arctan2(2*(w*x+y*z),1-2*(x*x+y*y)))
cfg=json.loads((REPO/'sim2real/tita_ws/src/tita_controller/policies/flashsac_80000/config.json').read_text())
actions=get('action_raw').astype(float);targets=np.zeros_like(actions)
for j,term in enumerate(cfg['policy_interface']['actions']):
    targets[:,j]=actions[:,j]*term['scale']+term['offset']
lib=library();angles=np.array([lib.sit_angle(qq,ii) for qq,ii in zip(q,quat)])
changes=np.r_[0,np.flatnonzero(states[1:]!=states[:-1])+1];ends=np.r_[changes[1:],len(t)]
limits=np.array([60,60,60,12,60,60,60,12.])
segments=[]
for n,(start,end) in enumerate(zip(changes,ends)):
    mask=np.arange(start,end); tail=mask[t[mask]>=t[end-1]-min(1.,(t[end-1]-t[start])/2)]
    entry={'state':str(states[start]),'start_s':float(t[start]),'duration_s':float(t[end-1]-t[start]),'samples':len(mask),
           'pitch_entry_deg':float(pitch[start]),'pitch_min_deg':float(pitch[mask].min()),'pitch_max_deg':float(pitch[mask].max()),
           'pitch_tail_mean_deg':float(pitch[tail].mean()),'pitch_tail_std_deg':float(pitch[tail].std()),
           'roll_abs_peak_deg':float(abs(roll[mask]).max()),'com_angle_tail_deg':float(np.degrees(angles[tail]).mean()),
           'tail_native_q_rad':q[tail].mean(axis=0).tolist(),'tail_mean_wheel_dq_rad_s':float(dq[tail][:,[3,7]].mean()),
           'command_x_range': [float(command[mask,0].min()),float(command[mask,0].max())],
           'command_yaw_range':[float(command[mask,2].min()),float(command[mask,2].max())],
           'wheel_torque_clip_fraction':float((abs(tau[mask][:,[3,7]])>=11.999).mean())}
    if states[start]=='rl':
        neutral=mask[(abs(command[mask])<np.array([.02,.02,.03])).all(axis=1)]
        entry['neutral_samples']=len(neutral)
        if len(neutral):entry['neutral_pitch_deg']={'mean':float(pitch[neutral].mean()),'min':float(pitch[neutral].min()),'max':float(pitch[neutral].max())}
        quiet=neutral[(t[neutral]>=t[start]+2.) & (abs(gyro[neutral,1])<.1)]
        if len(quiet):
            yaw=np.arctan2(2*(w[quiet]*z[quiet]+x[quiet]*y[quiet]),1-2*(y[quiet]**2+z[quiet]**2))
            rr=np.radians(roll[quiet])
            level=np.c_[np.cos(rr/2)*np.cos(yaw/2),np.sin(rr/2)*np.cos(yaw/2),
                        np.sin(rr/2)*np.sin(yaw/2),np.cos(rr/2)*np.sin(yaw/2)]
            flat_angles=np.array([lib.sit_angle(qq,ii) for qq,ii in zip(q[quiet],level)])
            entry['quiet_neutral_after_2s']={'definition':'command abs <= [.02,.02,.03], 2 s after RL entry, abs gyro_y < .1 rad/s; not proof of no hand contact/base motion',
                'samples':len(quiet),'pitch_mean_deg':float(pitch[quiet].mean()),'pitch_std_deg':float(pitch[quiet].std()),
                'pitch_p10_p90_deg':np.percentile(pitch[quiet],[10,90]).tolist(),
                'nominal_com_angle_mean_deg':float(np.degrees(angles[quiet]).mean()),
                'same_leg_pose_body_level_com_angle_mean_deg':float(np.degrees(flat_angles).mean()),
                'native_q_mean_rad':q[quiet].mean(axis=0).tolist(),
                'policy_native_target_mean':targets[quiet].mean(axis=0).tolist(),
                'computed_torque_mean_nm':tau[quiet].mean(axis=0).tolist(),
                'common_wheel_torque_mean_nm':float(tau[quiet][:,[3,7]].mean())}
    segments.append(entry)

replays=[];refangles=np.full(len(t),np.nan);blend_all=np.full(len(t),np.nan);replay_tau=np.full_like(tau,np.nan)
for start in changes:
    if states[start] not in ('return_to_sit','estop'):continue
    following=changes[changes>start]; end=int(following[0]) if len(following) else len(t)
    # Sit continuation preserves the same supporting controller after the 4 s path.
    if end<len(t) and states[end]=='sit':
        after=changes[changes>end];end=int(after[0]) if len(after) else len(t)
    assert start and states[start-1]=='rl'
    f=feedback[int(seq[start])]
    assert f.header==samples[start].header and f.monotonic_ns==samples[start].monotonic_ns
    previous=np.array(f.previous_computed_torque)
    controller=SupportingSit(q[start],dq[start],previous,limits,4.,quat[start],gyro[start],0.,[30.,5.,1.],angles[start],.3)
    ids=np.arange(start,end);elapsed=(tick[ids]-tick[start]+1)*.002
    alpha=np.clip(elapsed/4.,0,1);alpha=alpha*alpha*(3-2*alpha)
    refangles[ids]=(1-alpha)*angles[start]
    fold=np.clip((-.5*(q[ids,2]+q[ids,6])-2.35)/.3,0,1);blend_all[ids]=1-fold*fold*(3-2*fold)
    for i,e in zip(ids,elapsed):replay_tau[i]=controller.torque(q[i],dq[i],e,quat[i],gyro[i],angles[i])
    error=float(abs(replay_tau[ids]-tau[ids]).max())
    assert error<1e-7,error
    pivots=[]
    for pivot in [0,.5,1,2,3,4,5,8]:
        i=int(ids[np.argmin(abs(elapsed-pivot))])
        if abs(elapsed[i-start]-pivot)>.04:continue
        pivots.append({'event_s':float(elapsed[i-start]),'pitch_deg':float(pitch[i]),'roll_deg':float(roll[i]),
                       'com_angle_deg':float(np.degrees(angles[i])),'com_reference_deg':float(np.degrees(refangles[i])),
                       'balance_blend':float(blend_all[i]),'mean_wheel_tau_nm':float(tau[i,[3,7]].mean()),
                       'mean_wheel_dq_rad_s':float(dq[i,[3,7]].mean()),'native_q_rad':q[i].tolist()})
    lowest=int(ids[np.argmin(pitch[ids])])
    lowblend=ids[blend_all[ids]<.1]
    replays.append({'pitch_min_deg':float(pitch[lowest]),'pitch_min_after_s':float((tick[lowest]-tick[start])*.002),
                    'blend_at_pitch_min':float(blend_all[lowest]),
                    'first_balance_under_10pct_s':float((tick[lowblend[0]]-tick[start])*.002) if len(lowblend) else None,
                    'state':str(states[start]),'start_s':float(t[start]),'torque_replay_max_error_nm':error,'snapshots':pivots})

rl=states=='rl'
rebuilt=np.array(cfg['robot']['joint_kp'])*(targets-q)-np.array(cfg['robot']['joint_kd'])*dq
rebuilt[:,[3,7]]=np.array(cfg['robot']['joint_kd'])[[3,7]]*(targets[:,[3,7]]-dq[:,[3,7]])
rebuilt=np.clip(rebuilt,-limits,limits)
rl_pd_error=float(abs(rebuilt[rl]-tau[rl]).max())
assert rl_pd_error<1e-8,rl_pd_error
result={'execution_domain':'DESKTOP_DRY_RUN','evidence_status':'SUSPICIOUS',
        'checkpoint_sha256':'79f9175bb8c3be0c5138866e30891b90cc1282b6c98023cdb76c2e33b229068c',
        'onnx_sha256':'26f0d86b65a68475fb8a315fb31e829ae16eaa2cf16dabbbcf38e69f28c933e9','database_sha256':before,
        'rl_pd_reconstruction_max_error_nm':rl_pd_error,'samples':len(t),'sequence_gaps':int((np.diff(seq)!=1).sum()),'sensors_invalid':int((~get('sensors_valid')).sum()),
        'outputs_disabled':int((~get('output_enabled')).sum()),'failed_torque_transport':int((~get('torque_sent')).sum()),
        'max_wheel_bias':float(abs(get('wheel_velocity_bias')).max()),
        'sample_interval_ms':{'median':float(np.median(np.diff(mono)*1e-6)),'p99':float(np.percentile(np.diff(mono)*1e-6,99)),'max':float((np.diff(mono)*1e-6).max())},
        'segments':segments,'supporting_sit_replays':replays,
        'same_policy_nominal_sim':{},
        'limits':['IMU pitch is not independently calibrated floor-relative body attitude.','Nominal FK CoM is a model estimate, not a physical CoM measurement.','No contact force/base position/physical robot counterfactual available.']}
sim=REPO/'docs/exp/2026-10-18/slow_sit_80000_deploy/nominal/nominal_neutral_s42_t8_continue_rl.npz'
if sim.exists():
    rr=np.load(sim)['rows']; mask=rr[:,0]>=5.
    result['same_policy_nominal_sim']={'source':str(sim.relative_to(REPO)),'source_sha256':hashlib.sha256(sim.read_bytes()).hexdigest(),
       'window':'event-relative 5..8 s, continued RL, command zero, bias OFF',
       'pitch_mean_deg':float(np.degrees(rr[mask,9]).mean()),'pitch_std_deg':float(np.degrees(rr[mask,9]).std()),
       'native_q_mean_rad':rr[mask,14:22].mean(axis=0).tolist()}
(a.root/'analysis.json').write_text(json.dumps(result,indent=2)+'\n')
np.savez_compressed(a.root/'signals.npz',t=t,state=states,q=q,dq=dq,pitch=pitch,roll=roll,com_angle=angles,com_reference=refangles,balance_blend=blend_all,torque=tau,command=command)
fig,axes=plt.subplots(4,1,figsize=(13,11),sharex=True,constrained_layout=True)
axes[0].plot(t,pitch,label='IMU pitch');axes[0].plot(t,roll,label='IMU roll',alpha=.6);axes[0].axhline(0,color='gray',ls=':');axes[0].set_ylabel('degrees')
axes[1].plot(t,np.degrees(angles),label='nominal FK CoM lean');axes[1].plot(t,np.degrees(refangles),label='sit CoM reference',ls='--');axes[1].set_ylabel('degrees')
axes[2].plot(t,tau[:,3],label='left wheel torque');axes[2].plot(t,tau[:,7],label='right wheel torque');axes[2].set_ylabel('computed Nm')
axes[3].plot(t,command[:,0],label='command x (m/s)');axes[3].plot(t,command[:,2],label='command yaw (rad/s)');axes[3].plot(t,blend_all,label='sit balance blend',alpha=.7);axes[3].set_ylabel('command / blend');axes[3].set_xlabel('seconds from first recorded sample')
for ax in axes:
    for i in changes[1:]:ax.axvline(t[i],ls=':',color='black',alpha=.4)
    ax.grid(alpha=.2);ax.legend(loc='upper right',fontsize=8)
for i in changes[1:]:axes[0].annotate(str(states[i]),(t[i],axes[0].get_ylim()[1]),rotation=90,va='top',fontsize=8)
fig.suptitle('Recorded FlashSAC 80000: pitch, CoM reference and supporting sit (bias OFF)')
fig.savefig(a.root/'pitch_overview.png',dpi=150);plt.close(fig)
fig,axes=plt.subplots(3,2,figsize=(12,9),sharex=True,constrained_layout=True)
for col,event in enumerate(replays):
    start=event['start_s'];relative=t-start
    mask=(relative>=-.5)&(relative<=5.)
    axes[0,col].plot(relative[mask],pitch[mask],label='IMU pitch')
    axes[0,col].plot(relative[mask],roll[mask],label='IMU roll')
    axes[0,col].set_title(event['state'])
    axes[1,col].plot(relative[mask],blend_all[mask],label='wheel balance multiplier')
    axes[2,col].plot(relative[mask],q[mask,1],label='left thigh')
    axes[2,col].plot(relative[mask],q[mask,2],label='left knee')
    axes[0,col].axhline(0,color='gray',ls=':')
    for row in range(3):
        axes[row,col].axvline(2.,color='gray',ls=':')
        axes[row,col].grid(alpha=.2);axes[row,col].legend(fontsize=8)
    axes[2,col].set_xlabel('seconds after transition')
axes[0,0].set_ylabel('degrees');axes[1,0].set_ylabel('fraction');axes[2,0].set_ylabel('joint radians')
fig.suptitle('Recorded sit transitions: pitch dip and knee-based balance fade')
fig.savefig(a.root/'sit_pitch_detail.png',dpi=150);plt.close(fig)
assert hashlib.sha256(db.read_bytes()).hexdigest()==before
for s in segments:print(s['state'],round(s['duration_s'],3),'pitch range',round(s['pitch_min_deg'],2),round(s['pitch_max_deg'],2),'tail',round(s['pitch_tail_mean_deg'],2),'COM tail',round(s['com_angle_tail_deg'],2))
for e in replays:
 print('REPLAY',e['state'],e['torque_replay_max_error_nm'])
 for s in e['snapshots']:print('snapshot',s['event_s'],round(s['pitch_deg'],2),round(s['com_angle_deg'],2),'blend',round(s['balance_blend'],3))
print('PASS DESKTOP_DRY_RUN: DB integrity, finite sensors, source torque replay; physical cause remains model-based inference')
