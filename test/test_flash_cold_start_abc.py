"""DESKTOP_DRY_RUN: independent kinematic, affine and information checks."""
import copy
import json
import unittest

import numpy as np
from scipy.spatial.transform import Rotation

from flash_cold_start_abc import sensor_geometry,discrete_transport,fit_batch,information,nominal,BIAS
from collect_flash_target_offline_id import absolute_score
from static_target_domain import CKPT,prepared_config
from sim2sim.lqr.model import Description
from sim2sim_ros2_jazzy.checkpoint import read_yaml


class DiagnosticsTests(unittest.TestCase):
    def test_sensor_fk_velocity_matches_independent_finite_difference(self):
        cfg=json.loads(prepared_config(CKPT).read_text());source=read_yaml(next(p for p in cfg['policy_interface']['sources']if p.endswith('env.yaml')))
        desc=Description(source['scene']['robot']['spawn']['asset_path']);rng=np.random.default_rng(121)
        q=rng.normal(0.,.2,8);dq=rng.normal(0.,.1,8);rot=Rotation.from_euler('xyz',[.1,-.2,.4]);quat=rot.as_quat()[[3,0,1,2]]
        g=sensor_geometry(desc,q,dq,quat,np.zeros(3));epsilon=1e-6
        lo=sensor_geometry(desc,q-epsilon*dq,dq,quat,np.zeros(3));hi=sensor_geometry(desc,q+epsilon*dq,dq,quat,np.zeros(3))
        f=np.array([np.cos(g['yaw']),np.sin(g['yaw']),0.]);expected=(hi['offset_world']-lo['offset_world'])@f/(2*epsilon)
        self.assertAlmostEqual(g['velocity_leg'],expected,places=9)

    def test_discrete_leg_tilt_yaw_sum_and_heading_invariance(self):
        rng=np.random.default_rng(73)
        for _ in range(30):
            pair=[]
            for i in range(2):
                rot=Rotation.from_euler('xyz',rng.normal(0.,.2,3));pair.append(dict(R=rot.as_matrix(),yaw=rot.as_euler('xyz')[2],offset_body=rng.normal(0.,.1,3)))
            terms,total=discrete_transport(*pair);self.assertAlmostEqual(sum(terms),total,places=13)
            Q=Rotation.from_euler('z',.8).as_matrix();rotated=[dict(v,R=Q@v['R'],yaw=v['yaw']+.8)for v in pair]
            np.testing.assert_allclose(discrete_transport(*rotated)[0],terms,atol=1e-14)

    def test_pure_yaw_transport_sign_and_sensor_correction(self):
        d=np.array([0.,-.002,-.3]);a=dict(R=np.eye(3),yaw=0.,offset_body=d)
        b=dict(R=Rotation.from_euler('z',-.1).as_matrix(),yaw=-.1,offset_body=d)
        parts,total=discrete_transport(a,b)
        self.assertLess(total,0.);self.assertAlmostEqual(parts[0],0.);self.assertAlmostEqual(parts[1],0.)
        # Fixed base, ideal no-slip midpoint odometry: subtracting transport gives0.
        encoder_path=total;self.assertAlmostEqual(encoder_path-total,0.)

    def test_known_nonzero_affine_coefficients_and_structural_constraints(self):
        rng=np.random.default_rng(94);prior=nominal();ref=np.asarray(prior['state_reference'])
        A=rng.normal(0.,.02,(24,24));A[:,0]=0.;A[0,0]=1.
        B=rng.normal(0.,.02,24);B[4:12]=0.;c=rng.normal(0.,.001,24);streams=[]
        for i in range(600):
            x=ref+rng.normal(0.,.05,24);u=BIAS+rng.normal(0.,.02);y=ref+A@(x-ref)+B*(u-BIAS)+c
            streams.append((np.asarray([x,y]),np.asarray([u]),np.asarray([True])))
        model,diag=fit_batch(streams)
        np.testing.assert_allclose(model['A'],A,atol=1e-10);np.testing.assert_allclose(model['B'],B,atol=1e-10)
        np.testing.assert_allclose(model['c_center'],c,atol=1e-10);self.assertEqual(diag['group_rank'],[25,24])
        partial,_=fit_batch(streams,partial=True);np.testing.assert_array_equal(partial['A'],prior['A'])

    def test_constant_or_state_explained_input_is_not_excitation(self):
        rng=np.random.default_rng(11);z=rng.normal(0.,.01,(1001,24));mask=np.ones(1000,dtype=bool)
        constant=information(z,np.full(1000,BIAS),mask);self.assertFalse(constant['gate']);self.assertLess(constant['rank'],25)
        coupled=information(z,BIAS+z[:-1,1],mask);self.assertLess(coupled['innovation'],1e-10)

    def test_absolute_offset_error_is_not_hidden_by_paired_response(self):
        A=np.eye(24)*.8;A[:,0]=0.;A[0,0]=1.;B=np.zeros(24);B[:2]=[.001,.1]
        model=dict(A=A.tolist(),B=B.tolist(),state_reference=np.ones(24).tolist(),c_center=np.zeros(24).tolist())
        u=np.tile(BIAS+.01*np.sin(np.arange(200)*.17),(8,1));x=np.zeros((8,201,24));x[:,0]=1.
        for i in range(200):x[:,i+1]=1.+(x[:,i]-1.)@A.T+(u[:,i,None]-BIAS)*B
        response=x-1.;good=absolute_score(model,x,u,response);self.assertTrue(good['gate'])
        bad=copy.deepcopy(model);bad['c_center'][0]=.001;self.assertFalse(absolute_score(bad,x,u,response)['gate'])


if __name__=='__main__':unittest.main()
