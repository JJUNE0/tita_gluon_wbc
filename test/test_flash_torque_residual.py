"""DESKTOP_DRY_RUN: bounds, wheel addition and exact alpha-zero rollout."""

import json
from pathlib import Path
import sys
import tempfile
import unittest

import numpy as np

sys.path.insert(0,str(Path(__file__).resolve().parent))
from eval_flash_torque_residual import (PositionVelocityResidual, DEFAULT_RESIDUAL,
    additive_torque, run, replay_check, ARCHIVE, policy_config, read_yaml, Description, LEGS, WHEELS)


class ResidualTests(unittest.TestCase):
    def test_bounds_ramp_slew_and_wheel_addition(self):
        residual=PositionVelocityResidual(DEFAULT_RESIDUAL,.25,0.)
        previous=0.
        for tick in range(200):
            u,raw,ramp=residual.command(np.array([10. if tick<100 else -10.,1.,0.,0.]),tick*.02,.02)
            self.assertLessEqual(abs(u),.25+1e-12)
            self.assertLessEqual(abs(u-previous),.04+1e-12)
            self.assertGreaterEqual(ramp,0.)
            self.assertLessEqual(ramp,1.)
            previous=u
        original=np.arange(8,dtype=np.float32)
        added=additive_torque(original,.5,np.array([1.,-1.]))
        np.testing.assert_array_equal(added[LEGS],original[LEGS])
        np.testing.assert_array_equal(added[WHEELS],original[WHEELS]+[.25,-.25])
        np.testing.assert_array_equal(original,np.arange(8,dtype=np.float32))
        self.assertEqual(PositionVelocityResidual(DEFAULT_RESIDUAL,1.,0.).command(np.ones(4),0.,.02)[0],0.)

    def test_alpha_zero_full_rollout_matches_archived_a(self):
        cfg=json.loads((ARCHIVE/'config.json').read_text())
        parameters=json.loads((ARCHIVE/'manifest.json').read_text())['nominal_parameters']
        policy=policy_config()
        source=read_yaml(next(p for p in policy['policy_interface']['sources'] if p.endswith('env.yaml')))
        description=Description(source['scene']['robot']['spawn']['asset_path'])
        # Temporary test artifacts belong under test/ and are removed at exit.
        with tempfile.TemporaryDirectory(prefix='residual_alpha_zero_',dir=Path(__file__).parent) as folder:
            output=Path(folder)
            r=run(policy,cfg,description,parameters,42,0.,'F-1_a0','synchronized',output,alpha=0.)
            self.assertEqual(max(replay_check(r,output).values()),0.)
            self.assertFalse(r['failures'])
            self.assertEqual(r['residual_peak_total_nm'],0.)
            self.assertEqual(r['audit']['leg_torque_max_error_nm'],0.)
            with np.load(output/r['trace']) as trace:
                np.testing.assert_array_equal(trace['command_substeps'],trace['flash_substeps'])


if __name__=='__main__':
    unittest.main(verbosity=2)
