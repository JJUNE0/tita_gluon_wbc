"""DESKTOP_DRY_RUN: input fairness, causal bias transfer and separate gain guards."""
import unittest
import numpy as np

from eval_m4_bias_reference import SlowBias,bounded_command,gain_changes,LOW,HIGH,BIAS,DT,paired_comparison


class BiasReferenceTests(unittest.TestCase):
    def test_absolute_band_slew_and_reference_independent_bias_ramp(self):
        previous_feedback=0.;previous_total=BIAS;values=[]
        for i in range(500):
            raw=.1 if i<250 else -.1
            total,feedback,request=bounded_command(raw,.52,previous_feedback,previous_total,i)
            self.assertLessEqual(abs(total-previous_total),.04+1e-12)
            self.assertLessEqual(abs(feedback),.05+1e-12)
            self.assertTrue(LOW<=total<=HIGH)
            values.append(total);previous_total=total;previous_feedback=feedback
        self.assertEqual(values[0],BIAS);self.assertEqual(max(values),HIGH)
        self.assertAlmostEqual(values[-1],.47)

    def test_per_update_guard_does_not_imply_nominal_cumulative_guard(self):
        per,cumulative=gain_changes([1.28,2.56],[1.14,2.28],[1.,2.],[.1,.2])
        self.assertLess(per,.25);self.assertGreater(cumulative,.25)
        self.assertAlmostEqual(cumulative,.28)

    def test_bias_uses_past_torque_and_rejects_fast_or_saturated_windows(self):
        learner=SlowBias(BIAS)
        for i in range(249):self.assertFalse(learner.observe(.497,[.01,0.,.05,0.]))
        self.assertEqual(learner.value,BIAS)
        self.assertTrue(learner.observe(.497,[.01,0.,.05,0.]))
        self.assertGreater(learner.value,BIAS)
        self.assertLessEqual(learner.value-BIAS,.0005*DT)
        old=learner.value
        for i in range(250):learner.observe(HIGH,[.01,.01,.05,0.])
        self.assertEqual(learner.value,old)
        for i in range(2500):learner.observe(.497,[.01,0.,.05,0.])
        self.assertLess(abs(learner.value-.497),abs(old-.497))

    def test_incomplete_trial_cannot_pass_effect_gate(self):
        base=dict(complete=True,pitch_RMS_nominal=.001,wheel_RMS=.1,base_IAE=1.,base_last5_RMSE=.1)
        better=dict(base,base_IAE=.8,base_last5_RMSE=.08)
        self.assertTrue(paired_comparison([base]*3,[better]*3)['gate'])
        self.assertFalse(paired_comparison([base]*3,[better,dict(better,complete=False),better])['gate'])


if __name__=='__main__':unittest.main()
