"""DESKTOP_DRY_RUN: passive vendor CAN capture vs recorded frozen FlashSAC.

No socket, publishers, services, robot SDK construction or control commands.
"""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import struct
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

p=argparse.ArgumentParser(description=__doc__);p.add_argument('capture',type=Path);p.add_argument('--output',type=Path,required=True);p.add_argument('--phase',choices=['stand','commands'],required=True);a=p.parse_args()
a.output.mkdir(parents=True,exist_ok=True)
counts=Counter(); lengths={}; decoded={i:[] for i in [0x108,0x109,0x118,0x12d,*range(0x120,0x124)]};zero=Counter();mode=Counter();mode_rows=[];first=None;last=None
pattern=re.compile(r'^\(([^)]+)\)\s+(\S+)\s+([0-9A-Fa-f]+)(##[0-9A-Fa-f]|#)([0-9A-Fa-f]*)$')
for line in a.capture.open():
    m=pattern.fullmatch(line.strip());assert m,line[:100]
    t=float(m[1]);cid=int(m[3],16);raw=bytes.fromhex(m[5]);counts[cid]+=1
    lengths.setdefault(cid,Counter())[len(raw)]+=1
    zero[cid]+=not any(raw)
    if first is None:first=t
    last=t
    if cid in [0x108,0x109]:
        assert len(raw)==64
        row=np.array([struct.unpack_from('<Ifff',raw,16*j) for j in range(4)])
        decoded[cid].append(np.r_[t,row.ravel()])
    elif cid==0x118:
        assert len(raw)==48
        decoded[cid].append([t,*struct.unpack('<I11f',raw)])
    elif cid==0x12d:
        assert len(raw)>=40
        decoded[cid].append([t,*struct.unpack_from('<I9f',raw)])
    elif cid in range(0x120,0x124):
        assert len(raw)==48
        row=np.array([struct.unpack_from('<Ifffff',raw,24*j) for j in range(2)])
        decoded[cid].append(np.r_[t,row.ravel()])
    elif cid==0x103 and len(raw)>=7:
        ts,key=struct.unpack_from('<IH',raw)
        if key==0x1001:
            mode[raw[6]]+=1;mode_rows.append([t,raw[6]])
assert first is not None and last>first
arr={cid:np.asarray(v,dtype=float) for cid,v in decoded.items() if v}
assert all(np.isfinite(v).all() for v in arr.values())
imu=arr[0x118];tt=imu[:,0];x,y,z,w=imu[:,8:12].T
norm=np.sqrt(x*x+y*y+z*z+w*w)
# Apply the same quaternion validity envelope and normalization as tita_node.
assert abs(norm*norm-1).max()<.1
x,y,z,w=x/norm,y/norm,z/norm,w/norm
pitch=np.degrees(np.arcsin(np.clip(2*(w*y-z*x),-1,1)))
roll=np.degrees(np.arctan2(2*(w*x+y*z),1-2*(x*x+y*y)))
def nearest(stamp,reference):
    j=np.clip(np.searchsorted(stamp,reference),0,len(stamp)-1);l=np.maximum(0,j-1)
    return np.where(abs(stamp[l]-reference)<abs(stamp[j]-reference),l,j)
q=[];dq=[];effort=[];alignment={}
for cid in [0x108,0x109]:
    data=arr[cid];idx=nearest(data[:,0],tt);error=abs(data[idx,0]-tt);alignment[hex(cid)]=float(error.max())
    motors=data[idx,1:].reshape(-1,4,4)
    q.append(motors[:,:,1]);dq.append(motors[:,:,2]);effort.append(motors[:,:,3])
q=np.c_[*q];dq=np.c_[*dq];effort=np.c_[*effort]
# Same thigh-angle branch used by the hardware node.
for j in [1,5]:q[:,j]=np.where(q[:,j]<-2.5,q[:,j]+2*np.pi,q[:,j])
assert max(alignment.values())<.02
stats=lambda v:{'mean':np.mean(v,axis=0).tolist(),'std':np.std(v,axis=0).tolist(),'min':np.min(v,axis=0).tolist(),'max':np.max(v,axis=0).tolist()}
result={'execution_domain':'DESKTOP_DRY_RUN','evidence_status':'PASS','policy_checkpoint_sha256':'N/A: company controller, no FlashSAC process',
        'comparison_checkpoint_sha256':'79f9175bb8c3be0c5138866e30891b90cc1282b6c98023cdb76c2e33b229068c',
        'operator_condition':'normal floor standing; same as prior RL, corrected by operator (not externally measured)',
        'phase':a.phase,'capture_sha256':hashlib.sha256(a.capture.read_bytes()).hexdigest(),'duration_s':last-first,'frames':sum(counts.values()),
        'CAN_ID_counts':{hex(k):v for k,v in sorted(counts.items())},'payload_lengths':{hex(k):dict(v) for k,v in lengths.items()},
        'motor_imu_alignment_max_s':alignment,'pitch_deg':stats(pitch),'roll_deg':stats(roll),
        'q_native_rad':stats(q),'dq_native_rad_s':stats(dq),'firmware_reported_torque_nm':stats(effort),
        'imu_hz':(len(tt)-1)/(tt[-1]-tt[0]),
        'raw_quaternion_norm':{'min':float(norm.min()),'max':float(norm.max()),'outside_1pct_fraction':float((abs(norm-1)>.01).mean()),'normalized_for_pitch':True},'firmware_robot_mode_values':dict(mode),
        'all_zero_CAN_families':{hex(k):{'frames':counts[k],'zero_payload_frames':zero[k]} for k in range(0x110,0x114) if counts[k]},
        'sdk_motor_command_frames':{},'channel_input':None,
        'limits':['Reported Nm is firmware telemetry, not calibrated torque.','Wheel velocity is a wheel-based proxy, not measured base velocity.','Unpublished factory targets/gains/internal control cannot be recovered from external telemetry alone.']}
for cid in range(0x120,0x124):
    entry={'frames':counts[cid]}
    if cid in arr:
        m=arr[cid][:,1:].reshape(-1,2,6)
        entry.update(position=stats(m[:,:,1]),kp=stats(m[:,:,2]),velocity=stats(m[:,:,3]),kd=stats(m[:,:,4]),feedforward_torque=stats(m[:,:,5]))
    result['sdk_motor_command_frames'][hex(cid)]=entry
if 0x12d in arr:
    channels=arr[0x12d]
    result['channel_input']={'samples':len(channels),'fields':['forward','yaw','pitch','roll','height','split','tilt','forward_accel','yaw_accel'],'values':stats(channels[:,2:])}
# Company ROS joint_states may remap/sign-correct encoder fields: check it against
# decoded packets before reporting protocol-native values as robot-native values.
ros_check={'status':'NOT_TESTED'}
try:
    import sqlite3
    from rclpy.serialization import deserialize_message
    from sensor_msgs.msg import JointState
    db=next(a.capture.parent.glob(a.capture.name.replace('_can.log','_bag')+'/*.db3'))
    with sqlite3.connect(f'file:{db.resolve()}?mode=ro',uri=True) as conn:
        assert conn.execute('PRAGMA quick_check').fetchone()[0]=='ok'
        topic=conn.execute("SELECT id FROM topics WHERE name='/tita4252763/joint_states'").fetchone()
        messages=[(stamp*1e-9,deserialize_message(raw,JointState)) for stamp,raw in conn.execute('SELECT timestamp,data FROM messages WHERE topic_id=? ORDER BY timestamp',topic)] if topic else []
    if messages:
        native=[f'joint_{side}_leg_{j}' for side in ['left','right'] for j in range(1,5)]
        valid=[]
        for stamp,msg in messages:
            if not set(native).issubset(msg.name):continue
            if tt[0]+.02<stamp<tt[-1]-.02:valid.append((stamp,msg))
        ts=np.array([v[0] for v in valid]);index=nearest(tt,ts)
        rq=np.array([[m.position[m.name.index(n)] for n in native] for _,m in valid])
        for j in [1,5]:rq[:,j]=np.where(rq[:,j]<-2.5,rq[:,j]+2*np.pi,rq[:,j])
        err=np.abs(np.arctan2(np.sin(q[index]-rq),np.cos(q[index]-rq)))
        ros_check={'status':'PASS' if np.quantile(err,.99)<.03 else 'SUSPICIOUS','samples':len(valid),
                   'comparison':'periodic angular difference; receive-time nearest alignment, not acquisition-time synchronization',
                   'q_legs_abs_error_p99_rad':float(np.quantile(err[:,[0,1,2,4,5,6]],.99)),
                   'q_wheels_abs_error_p99_rad':float(np.quantile(err[:,[3,7]],.99)),
                   'q_abs_error_p99_rad':float(np.quantile(err,.99)),'q_abs_error_max_rad':float(err.max()),
                   'joint_names':native}
except (ImportError,StopIteration) as e:ros_check['reason']=str(e)
result['ROS_joint_mapping_check']=ros_check
mode_rows=np.asarray(mode_rows,dtype=float)
mode_at_imu=mode_rows[np.clip(np.searchsorted(mode_rows[:,0],tt,side='right')-1,0,len(mode_rows)-1),1].astype(int)
changes=np.r_[0,np.flatnonzero(mode_rows[1:,1]!=mode_rows[:-1,1])+1]
result['firmware_mode_changes']=[{'time_s':float(mode_rows[i,0]-tt[0]),'mode_value':int(mode_rows[i,1])} for i in changes]
standing=mode_at_imu==3
result['STAND_only']={'samples':int(standing.sum()),'pitch_deg':stats(pitch[standing]),'q_native_rad':stats(q[standing])}
if 0x12d in arr:
    cc=arr[0x12d];ci=np.clip(np.searchsorted(cc[:,0],tt,side='right')-1,0,len(cc)-1)
    cmd=cc[ci,2:4];proxy=.0925*dq[:,[3,7]].mean(axis=1)
    selected=standing&(abs(cmd[:,0])<.02)&(abs(cmd[:,1])<.03)
    result['STAND_neutral']={'samples':int(selected.sum()),'pitch_deg':stats(pitch[selected]) if selected.any() else None}
    motion=standing&((abs(cmd[:,0])>=.1)|(abs(cmd[:,1])>=.1))
    result['STAND_commanded']={'samples':int(motion.sum()),'pitch_deg':stats(pitch[motion]) if motion.any() else None,
        'forward_range':stats(cmd[standing,0]),'yaw_range':stats(cmd[standing,1]),
        'wheel_proxy_m_s':stats(proxy[standing]),'imu_gyro_z':stats(imu[standing,7]),
        'forward_to_wheel_proxy_correlation':float(np.corrcoef(cmd[standing,0],proxy[standing])[0,1]) if cmd[standing,0].std()>.01 else None,
        'yaw_to_gyro_z_correlation':float(np.corrcoef(cmd[standing,1],imu[standing,7])[0,1]) if cmd[standing,1].std()>.01 else None,
        'note':'same-time correlations, not delay-corrected tracking errors; wheel proxy is not ground-truth base velocity'}

# Comparison is retrospective: quiet neutral RL frames, not simultaneous trials.
prior=a.output.parents[0]/'flashsac_80000_105921_pitch_review/analysis.json'
if prior.exists():
    old=json.loads(prior.read_text());result['prior_RL_quiet_neutral']=[s['quiet_neutral_after_2s'] for s in old['segments'] if s['state']=='rl']
np.savez_compressed(a.output/(a.phase+'_signals.npz'),t=tt-tt[0],unix=tt,q=q,dq=dq,effort=effort,pitch=pitch,roll=roll,
                    channels=arr.get(0x12d,np.empty((0,11))),mode=mode_at_imu,gyro=imu[:,5:8])
(a.output/(a.phase+'_metrics.json')).write_text(json.dumps(result,indent=2)+'\n')
fig,axes=plt.subplots(4,1,figsize=(12,10),sharex=True,constrained_layout=True);t=tt-tt[0]
axes[0].plot(t,pitch,label='pitch');axes[0].plot(t,roll,label='roll');axes[0].set_ylabel('IMU deg')
for j in [1,2,5,6]:axes[1].plot(t,q[:,j],label=f'joint {j}')
axes[1].set_ylabel('rad')
axes[2].plot(t,.0925*dq[:,3],label='left wheel proxy');axes[2].plot(t,.0925*dq[:,7],label='right wheel proxy');axes[2].set_ylabel('m/s proxy')
if 0x12d in arr:
    c=arr[0x12d];axes[3].plot(c[:,0]-tt[0],c[:,2],label='channel forward');axes[3].plot(c[:,0]-tt[0],c[:,3],label='channel yaw')
else:
    axes[3].plot(t,effort[:,2],label='left knee firmware Nm');axes[3].plot(t,effort[:,6],label='right knee firmware Nm')
axes[3].set_xlabel('seconds from first IMU frame');axes[3].set_ylabel('channel / Nm')
for ax in axes:ax.grid(alpha=.2);ax.legend(loc='upper right',fontsize=8)
fig.suptitle('Company baseline: '+a.phase+' (passive receive only)');fig.savefig(a.output/(a.phase+'_overview.png'),dpi=150);plt.close(fig)
print('PASS DESKTOP_DRY_RUN',a.phase,'duration',result['duration_s'],'frames',result['frames'],'pitch',result['pitch_deg'])
print('ROS joint mapping',ros_check)
print('motor command frame counts',{k:v['frames'] for k,v in result['sdk_motor_command_frames'].items()},'channel inputs',None if result['channel_input'] is None else result['channel_input']['samples'])
