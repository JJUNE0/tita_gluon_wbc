"""VALIDATION_SIM: actual Sim2SimNode/ONNX/MuJoCo at 500/50 Hz, raw-history contract.

Finite integration smoke, not a stability-margin or real robot vibration test.
"""
import argparse
import json
from pathlib import Path
import sys
import tempfile
import numpy as np
import rclpy
from scipy.signal import iirnotch, lfilter, lfilter_zi
from std_msgs.msg import String

REPO=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(REPO/'sim2sim/sim2sim_ros2_jazzy'))
from sim2sim_ros2_jazzy.sim2sim_node import Sim2SimNode


class Sink:
    def publish(self,message):
        self.message=message


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output',type=Path,required=True)
    args=p.parse_args()
    cfg=json.loads((REPO/'sim2real/tita_ws/src/tita_controller/policies/flashsac_80000/config.json').read_text())
    cfg['control'].update(sim_timestep=.002,decimation=10)
    results=[]
    with tempfile.TemporaryDirectory(dir=REPO/'test/sim2real',prefix='ma2_sim_') as temp:
        path=Path(temp)/'config.json';path.write_text(json.dumps(cfg))
        for mode in ('none','ma2_legs','ma2_notch_legs'):
            rclpy.init(args=['--ros-args','-p',f'config:={path}','-p','viewer:=false',
                            '-p',f'leg_action_filter:={mode}'])
            node=None
            try:
                node=Sim2SimNode()
                node.obs_pub,node.action_pub,node.applied_pub=Sink(),Sink(),Sink()
                previous=None;rl_steps=0;pitch=[]
                b,a=iirnotch(8.3,3.,fs=50);zi=None
                for tick in range(1000):
                    old_raw=node.last_action.copy()
                    node._step()
                    assert np.isfinite(np.r_[node.env.data.qpos,node.env.data.qvel]).all()
                    if node.sm.state!='rl':
                        previous=None;continue
                    raw=node.last_action.copy()
                    applied=np.array(node.applied_pub.message.data,dtype=np.float32)
                    np.testing.assert_array_equal(node.obs_pub.message.data[-8:],old_raw)
                    expected=raw.copy()
                    if mode!='none' and previous is not None:
                        j=[0,1,2,4,5,6]
                        expected[j]=.5*raw[j]+.5*previous[j]
                    if mode=='ma2_notch_legs':
                        if previous is None:
                            zi=np.array([lfilter_zi(b,a)*expected[j] for j in range(8)])
                        for j in [0,1,2,4,5,6]:
                            values,zi[j]=lfilter(b,a,[expected[j]],zi=zi[j])
                            expected[j]=values[0]
                        np.testing.assert_allclose(applied,expected,atol=1e-6,rtol=1e-6)
                    else:
                        np.testing.assert_array_equal(applied,expected)
                    previous=raw;rl_steps+=1
                    w,x,y,z=node.env.base_quat_sensor()
                    pitch.append(float(np.degrees(np.arcsin(np.clip(2*(w*y-z*x),-1,1)))))
                assert rl_steps>100
                node._cmd_key_cb(String(data='reset'));node._step()
                assert node.leg_filter.previous is None and not node.last_action.any()
                results.append(dict(mode=mode,steps=1000,rl_steps=rl_steps,
                    max_abs_pitch_deg=max(abs(np.array(pitch))),raw_history='PASS',
                    applied_sequence='PASS',reset='PASS'))
            finally:
                if node:
                    node.env.close();node.destroy_node()
                rclpy.try_shutdown()
    result=dict(execution_domain='VALIDATION_SIM',evidence_status='PASS',
        detail='Finite integration smoke only; no hardware or vibration stability claim',cases=results)
    args.output.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))


if __name__=='__main__':
    main()
