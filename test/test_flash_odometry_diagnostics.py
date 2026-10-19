"""DESKTOP_DRY_RUN: contact geometry and common-point transport identities."""

import unittest

import numpy as np
from scipy.spatial.transform import Rotation

from diagnose_flash_odometry import contact_terms


class OdometryDiagnosticsTests(unittest.TestCase):
    def test_random_contact_identity_and_heading_invariance(self):
        rng = np.random.default_rng(17105)
        for _ in range(200):
            yaw = rng.uniform(-np.pi,np.pi)
            f = np.array([np.cos(yaw),np.sin(yaw),0.])
            l = np.array([-np.sin(yaw),np.cos(yaw),0.])
            v,w,d,g = rng.normal(size=(4,3))
            radius = .0925
            terms = contact_terms(radius,f,l,v,w,d,g)
            reconstructed = terms['height']+terms['yaw']-terms['slip']-terms['ground']
            self.assertAlmostEqual(reconstructed,radius*(w@l)-v@f,places=12)
            rotation = Rotation.from_euler('z',rng.uniform(-3.,3.))
            transformed = contact_terms(radius,*[rotation.apply(x) for x in [f,l,v,w,d,g]])
            for k in terms:self.assertAlmostEqual(terms[k],transformed[k],places=12)

    def test_ideal_centered_contact_has_no_yaw_geometry_term(self):
        f,l = np.eye(3)[:2]
        radius = .0925
        omega = np.array([0.,.2,-.0084])
        offset = np.array([0.,0.,-radius])
        velocity = -np.cross(omega,offset)
        terms = contact_terms(radius,f,l,velocity,omega,offset,np.zeros(3))
        self.assertEqual(terms['height'],0.)
        self.assertEqual(terms['yaw'],0.)
        self.assertAlmostEqual(terms['slip'],0.)

    def test_lateral_contact_offset_yaw_and_contact_choice(self):
        f,l = np.eye(3)[:2]
        r = .0925
        w = np.array([0.,0.,-.0084])
        offsets = [np.array([0.,-.015,-r]),np.array([0.,.018,-r])]
        v = np.array([-.00001,0.,0.])
        terms = [contact_terms(r,f,l,v,w,d,np.zeros(3)) for d in offsets]
        self.assertGreater(terms[1]['yaw'],0.)
        self.assertLess(terms[0]['yaw'],0.)
        for weights in [[.86,.14],[.5,.5],[1.,0.]]:
            total = sum(a*(t['height']+t['yaw']-t['slip']) for a,t in zip(weights,terms))
            self.assertAlmostEqual(total,r*(w@l)-v@f,places=14)
        # A geometrical attribution changes when a representative contact changes;
        # the measured center-velocity error remains the same.
        self.assertNotAlmostEqual(sum(.5*t['yaw'] for t in terms),terms[0]['yaw'])

    def test_rigid_point_transport_yaw_sign(self):
        f,l = np.eye(3)[:2]
        omega = np.array([0.,0.,-.0084])
        offset = np.array([.02,-.0015,-.25])
        root_v = np.array([.000009,0.,0.])
        point_v = root_v+np.cross(omega,offset)
        yaw_term = -omega[2]*(offset@l)
        self.assertAlmostEqual((point_v-root_v)@f,yaw_term)
        self.assertAlmostEqual(yaw_term,-.0000126)


if __name__=='__main__':
    unittest.main(verbosity=2)
