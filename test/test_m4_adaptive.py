"""DESKTOP_DRY_RUN: reject unvalidated models and check physical gain guards."""
import copy
import json
from pathlib import Path
import unittest
import numpy as np

from m4_adaptive_stages import checked_gain,run_adaptive
from m4_mismatch_stages import PREVIOUS


class AdaptiveGuards(unittest.TestCase):
    def test_nominal_recalculation_matches_frozen_gain(self):
        model=json.loads((PREVIOUS/'affine_models_frozen.json').read_text())['models']['M4']
        gain=json.loads((PREVIOUS/'gains_frozen.json').read_text())['models']['M4']
        K,result=checked_gain(model,model,gain,gain['K'],np.zeros(24))
        self.assertTrue(result['gate'])
        np.testing.assert_allclose(K,gain['K'],atol=1e-6,rtol=1e-6)
        # A large change at the same measured error must fail the raw torque jump guard.
        K2,result=checked_gain(model,model,gain,(np.asarray(gain['K'])*-10).tolist(),np.ones(24))
        self.assertFalse(result['gate']);self.assertGreater(result['command_jump_Nm'],.005)

    def test_failed_shadow_never_creates_adaptive_artifacts(self):
        with self.assertRaises(AssertionError):
            run_adaptive(Path('test/must_not_exist'),{},dict(gate=False,eligible_for_adaptive=[]))
        self.assertFalse(Path('test/must_not_exist').exists())


if __name__=='__main__':unittest.main()
