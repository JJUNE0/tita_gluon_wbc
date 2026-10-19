"""DESKTOP_DRY_RUN: authorization and no false success on missing/failed data."""
import copy
import tempfile
from pathlib import Path
import unittest

from m4_mismatch_stages import authorize_m4, summarize
from run_m4_followup_pipeline import stage_record
from flash_overnight_model_stages import write


class Gates(unittest.TestCase):
    def test_original_fail_is_preserved_with_m4_authorization(self):
        result = authorize_m4()
        self.assertIs(result['gate'], True)
        self.assertIs(result['old_aggregate_stage4'], False)
        self.assertIs(result['old_M5_stage4'], False)

    def test_performance_fail_does_not_prevent_shadow_diagnosis(self):
        rows = []
        for i in range(6):
            for group, iae in [('M4', 2.), ('bias_only', 1.)]:
                rows.append(dict(context=str(i),condition='gain0.8',regime='settled',group=group,
                    complete=True,base={'IAE':iae},max_planar_drift=.1,failure=[]))
        result = summarize(rows)
        self.assertFalse(result['gate'])
        self.assertFalse(result['conditions']['settled/gain0.8']['gate'])
        self.assertTrue(result['conditions']['settled/gain0.8']['stable_completed'])
        changed = copy.deepcopy(rows);changed[0]['complete']=False
        self.assertFalse(summarize(changed)['conditions']['settled/gain0.8']['stable_completed'])
        self.assertFalse(summarize([])['gate'])

    def test_stage_does_not_overwrite_failed_evidence_and_rejects_tampering(self):
        # Test files stay inside test/, per project policy.
        with tempfile.TemporaryDirectory(dir=Path(__file__).parent) as name:
            root = Path(name).resolve();write(root/'plan.json',{})
            first = stage_record(root,'stage',lambda:dict(gate=False),[])
            self.assertFalse(first['gate'])
            def forbidden(): raise AssertionError('must not rerun')
            self.assertEqual(stage_record(root,'stage',forbidden,[]),first)
            write(root/'plan.json',{'changed':True})
            with self.assertRaises(RuntimeError):stage_record(root,'stage',forbidden,[])


if __name__=='__main__':unittest.main()
