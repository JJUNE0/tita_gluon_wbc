"""DESKTOP_DRY_RUN: portable fixtures for x86/ARM supporting sit comparison."""
import argparse
from pathlib import Path
import numpy as np
from validate_sit_transitions import library, SupportingSit
p=argparse.ArgumentParser();p.add_argument('mode',choices=['generate','verify']);p.add_argument('folder',type=Path);p.add_argument('--actual',type=Path);a=p.parse_args()
if a.mode=='generate':
    lib=library();rng=np.random.default_rng(80000);records=[];expected=[]
    limits=np.array([60,60,60,12,60,60,60,12.])
    for _ in range(1000):
        q=np.array([0.,.8,-1.5,0.,0.,.8,-1.5,0.])+rng.normal(0,.1,8)
        dq=rng.normal(0,.4,8);previous=rng.normal(0,2,8)
        imu=rng.normal(size=4);imu/=np.linalg.norm(imu);gyro=rng.normal(0,.1,3)
        sample=q+rng.normal(0,.1,8);velocity=rng.normal(0,1,8)
        current_imu=rng.normal(size=4);current_imu/=np.linalg.norm(current_imu)
        current_gyro=rng.normal(0,.1,3);elapsed=rng.uniform(0,6)
        reference=SupportingSit(q,dq,previous,limits,4.,imu,gyro,0.,[30,5,1],lib.sit_angle(q,imu),.3)
        angle=lib.sit_angle(sample,current_imu)
        expected.append(np.r_[angle,reference.torque(sample,velocity,elapsed,current_imu,current_gyro,angle)])
        records.append(np.r_[q,dq,previous,imu,gyro,sample,velocity,current_imu,current_gyro,elapsed])
    np.savetxt(a.folder/'replay_input.txt',records,fmt='%.17g')
    np.savetxt(a.folder/'replay_expected.txt',expected,fmt='%.17g')
    print('PASS DESKTOP_DRY_RUN generated 1000 portable reference fixtures')
else:
    expected=np.loadtxt(a.folder/'replay_expected.txt');actual=np.loadtxt(a.actual)
    np.testing.assert_allclose(actual,expected,atol=1e-9,rtol=1e-10)
    print('PASS DESKTOP_DRY_RUN x86/ARM reference replay; max absolute error',abs(actual-expected).max())
