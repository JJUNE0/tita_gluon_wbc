"""DESKTOP_DRY_RUN: the requested combined budget is the control equation."""
import unittest
import numpy as np
from m4_joint_adaptation import Command,BIAS,LOW,HIGH


class SharedBudget(unittest.TestCase):
    def test_shifted_bias_can_use_entire_unchanged_absolute_band(self):
        z=np.zeros(24);z[0]=.07;K=np.zeros(24);K[0]=1.;reference=np.zeros(24)
        bias=BIAS+.02;wanted=float(np.clip(bias-K@(z-reference),LOW,HIGH))
        command=Command(wanted);command.count=100;command.feedback=-.05
        actual,_=command.compute(z,K,bias,reference)
        self.assertAlmostEqual(actual,wanted,places=12)

    def test_nominal_bias_matches_original_bound_after_activation(self):
        z=np.zeros(24);z[0]=1.;K=np.zeros(24);K[0]=1.;reference=np.zeros(24)
        command=Command(LOW);command.count=100;command.feedback=-.05
        actual,_=command.compute(z,K,BIAS,reference)
        self.assertEqual(actual,LOW)


if __name__=='__main__':unittest.main()
