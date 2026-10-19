"""DESKTOP_DRY_RUN: offline post-Ctrl+C motor/IMU CAN feedback; no socket."""
from collections import Counter
from pathlib import Path
import hashlib,json,struct
import numpy as np
root=Path(__file__).resolve().parents[2]/'docs/exp/2026-10-18/flashsac_shutdown_torque_review'
p=root/'after_ctrl_c_can.log';frames={0x108:[],0x109:[]};counts=Counter()
for line in p.open():
    fields=line.split();stamp=float(fields[0][1:-1]);cid=int(fields[2].split('#')[0],16);counts[cid]+=1
    if cid in frames:
        raw=bytes.fromhex(fields[2].split('##',1)[1][1:]);assert len(raw)==64
        values=np.array([struct.unpack_from('<Ifff',raw,16*i) for i in range(4)])
        frames[cid].append(np.r_[stamp,values.ravel()])
r={'execution_domain':'DESKTOP_DRY_RUN','evidence_status':'SUSPICIOUS',
'checkpoint_sha256':'79f9175bb8c3be0c5138866e30891b90cc1282b6c98023cdb76c2e33b229068c',
'capture_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'CAN_ID_counts':{hex(k):v for k,v in counts.items()},'motors':{},
'interpretation':'Firmware-reported torque and native encoder pose only; not calibrated external force. No commands were sent during capture.'}
for cid,side in [(0x108,'left'),(0x109,'right')]:
    data=np.array(frames[cid]);assert len(data)>100
    m=data[:,1:].reshape(-1,4,4);assert np.isfinite(m).all()
    r['motors'][side]={'samples':len(m),'duration_s':float(data[-1,0]-data[0,0]),
        'q_mean_rad':m[:,:,1].mean(axis=0).tolist(),'q_first_rad':m[0,:,1].tolist(),'q_last_rad':m[-1,:,1].tolist(),
        'dq_abs_max_rad_s':abs(m[:,:,2]).max(axis=0).tolist(),
        'reported_torque_mean_nm':m[:,:,3].mean(axis=0).tolist(),
        'reported_torque_min_nm':m[:,:,3].min(axis=0).tolist(),'reported_torque_max_nm':m[:,:,3].max(axis=0).tolist()}
(root/'post_stop_metrics.json').write_text(json.dumps(r,indent=2)+'\n')
print(json.dumps(r,indent=2))
