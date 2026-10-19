"""DESKTOP_DRY_RUN: comparator admission never promotes failed model confidence."""
import copy
import unittest
from run_joint_guarded_shock import comparison_decision


class ComparatorAdmission(unittest.TestCase):
    def test_failed_model_can_only_be_a_guarded_comparison(self):
        original=dict(conditions={'gain0.8':{'B1_E7':dict(admissible=False,physical_stable=True,
            model_gate=False,performance=False)}})
        before=copy.deepcopy(original);new=comparison_decision(original)['conditions']['gain0.8']['B1_E7']
        self.assertEqual(original,before);self.assertTrue(new['admissible']);self.assertTrue(new['comparison_only'])
        self.assertFalse(new['model_gate']);self.assertFalse(new['performance'])

    def test_physical_failure_remains_unadmitted(self):
        original=dict(conditions={'gain1.2':{'B1_E7':dict(admissible=False,physical_stable=False,
            model_gate=False,performance=False)}})
        self.assertFalse(comparison_decision(original)['conditions']['gain1.2']['B1_E7']['admissible'])

    def test_validated_model_status_is_not_changed(self):
        original=dict(conditions={'gain1.2':{'B1_E6':dict(admissible=True,physical_stable=True,
            model_gate=True,performance=True)}})
        new=comparison_decision(original)['conditions']['gain1.2']['B1_E6']
        self.assertFalse(new['comparison_only']);self.assertTrue(new['performance']);self.assertTrue(new['model_gate'])


if __name__=='__main__':unittest.main()
