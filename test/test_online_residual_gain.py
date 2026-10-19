"""DESKTOP_DRY_RUN: distinguish time trends from gain effects; audit guards/parity."""

import json
from pathlib import Path
import sys
import tempfile
import unittest

import numpy as np

sys.path.insert(0,str(Path(__file__).resolve().parent))
from eval_online_residual_gain import (OnlineAlpha,ADAPTATION,fit_probe_gradient,run_episode,
    ARCHIVE,policy_config,read_yaml,Description,WHEELS,LEGS)


class OnlineGainTests(unittest.TestCase):
    def test_guard_activation_before_learning_start_is_reported(self):
        gain=OnlineAlpha()
        unsafe=np.array([0.,0.,.1,2.])
        gain.observe(unsafe,.1,0.)
        self.assertEqual(gain.guards,1)
        gain.observe(unsafe,.1,.02)
        self.assertEqual(gain.guards,1)
        gain.observe(np.array([0.,0.,.1,0.]),.1,.04)
        gain.observe(unsafe,.1,.06)
        self.assertEqual(gain.guards,2)

    def test_time_trend_separated_from_actual_probe_effect(self):
        dose=.1*np.array([1,-1,-1,1,-1,1,1,-1])
        t=np.arange(8,dtype=float)
        for gradient in (0.,-2.,2.):
            windows=[dict(time=float(time),alpha_offset=float(alpha),cost=float(3+.2*time+.1*time*time+gradient*alpha))
                     for time,alpha in zip(t,dose)]
            fitted=fit_probe_gradient(windows)
            self.assertTrue(fitted['valid'])
            self.assertAlmostEqual(fitted['gradient'],gradient,places=10)

    def test_uncertain_time_only_cost_no_update_and_guard(self):
        gain=OnlineAlpha()
        previous=1.
        for tick in range(3101):
            t=tick*.02
            # Constant sensor state implies no causal benefit from any alpha.
            gain.observe(np.array([.1,.01,.1,0.]),.1,t)
            alpha=gain.command_alpha(t,.02)
            self.assertGreaterEqual(alpha,.5)
            self.assertLessEqual(alpha,2.)
            self.assertLessEqual(abs(alpha-previous),.005+1e-12)
            previous=alpha
        self.assertEqual(gain.accepted,0)
        self.assertEqual(gain.centre,1.)
        self.assertGreaterEqual(gain.rejected,2)
        gain.centre=1.5
        gain.observe(np.array([.1,0.,.4,0.]),.1,63.)
        self.assertEqual(gain.centre,1.)
        self.assertEqual(gain.guards,1)

    def test_learning_disabled_matches_fixed_f1_in_mismatch(self):
        cfg=json.loads((ARCHIVE/'config.json').read_text())
        parameters=json.loads((ARCHIVE/'manifest.json').read_text())['nominal_parameters']
        policy=policy_config();source=read_yaml(next(p for p in policy['policy_interface']['sources'] if p.endswith('env.yaml')))
        description=Description(source['scene']['robot']['spawn']['asset_path'])
        mismatch=next(m for m in cfg['mismatches'] if m['name']=='gain_0.8')
        with tempfile.TemporaryDirectory(prefix='online_gain_parity_',dir=Path(__file__).parent) as directory:
            output=Path(directory)
            fixed=run_episode(policy,cfg,description,parameters,mismatch,42,0.,'F-1',output)
            disabled=run_episode(policy,cfg,description,parameters,mismatch,42,0.,'G-disabled',output,
                learn=True,alpha_learning=False)
            with np.load(output/fixed['trace']) as a,np.load(output/disabled['trace']) as b:
                for key in ('state','policy_observation','policy_action','gt_position','motor_substeps','residual_total_nm'):
                    np.testing.assert_array_equal(a[key],b[key])
            self.assertEqual(disabled['accepted_updates'],0)

    def test_alpha_above_one_keeps_physical_residual_cap(self):
        cfg=json.loads((ARCHIVE/'config.json').read_text())
        parameters=json.loads((ARCHIVE/'manifest.json').read_text())['nominal_parameters']
        policy=policy_config();source=read_yaml(next(p for p in policy['policy_interface']['sources'] if p.endswith('env.yaml')))
        description=Description(source['scene']['robot']['spawn']['asset_path'])
        with tempfile.TemporaryDirectory(prefix='online_gain_cap_',dir=Path(__file__).parent) as directory:
            output=Path(directory)
            r=run_episode(policy,cfg,description,parameters,{'name':'nominal'},42,0.,'G-max',output,
                learn=True,alpha_learning=False,adapt_config=dict(ADAPTATION,alpha_initial=2.))
            with np.load(output/r['trace']) as trace:
                self.assertLessEqual(abs(trace['residual_total_nm']).max(),1.)
                self.assertLessEqual(abs(np.diff(trace['residual_total_nm'])).max(),.04+1e-12)
                self.assertGreater(abs(trace['residual_total_nm']).max(),.5)
                np.testing.assert_array_equal(trace['command_substeps'][:,:,LEGS],trace['flash_substeps'][:,:,LEGS])


if __name__=='__main__':
    unittest.main(verbosity=2)
