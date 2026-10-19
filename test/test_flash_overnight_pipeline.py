"""DESKTOP_DRY_RUN: stage-gate failures must prevent downstream experiments."""

import json
from pathlib import Path
import tempfile
import unittest

from run_flash_overnight_pipeline import run_stages,gate_passed,verify_record
from eval_flash_pv_models import REPO,write


class PipelineChecks(unittest.TestCase):
    def fixture(self):
        temporary = tempfile.TemporaryDirectory(dir=REPO/'test',prefix='pipeline_unit_')
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name)
        write(root/'plan.json',{'unit_test':True})
        return root,{'stages':{}}

    def test_failed_affine_never_calls_gain_or_control(self):
        root,state = self.fixture();calls=[]
        def runner(root,stage,plan):
            calls.append(stage)
            return dict(gate=stage==1)
        result = run_stages(root,{},state,5,runner)
        self.assertEqual(calls,[1,2])
        self.assertEqual(result['stages']['2']['status'],'FAIL')
        self.assertEqual(result['stages']['3']['status'],'NOT_TESTED')
        self.assertFalse(result['scientific_success'])

    def test_missing_gate_and_exception_fail_closed(self):
        self.assertFalse(gate_passed({'gate':'true','evidence_status':'PASS'}))
        self.assertFalse(gate_passed({'gate':True,'evidence_status':'NOT_TESTED'}))
        for payload in [{},None]:
            root,state = self.fixture();calls=[]
            def runner(root,stage,plan):
                calls.append(stage)
                if payload is None:raise ValueError('injected collector failure')
                return payload
            result = run_stages(root,{},state,2,runner)
            self.assertEqual(calls,[1]);self.assertEqual(result['stages']['1']['status'],'FAIL')

    def test_resume_verifies_and_never_repeats_failed_stage(self):
        root,state = self.fixture()
        state = run_stages(root,{},state,2,lambda root,stage,plan:dict(gate=stage==1))
        calls=[]
        again = run_stages(root,{},state,5,lambda *args:calls.append(args))
        self.assertEqual(calls,[])
        self.assertTrue(again['terminal'])

    def test_tampered_stage_evidence_is_rejected(self):
        root,state = self.fixture()
        state = run_stages(root,{},state,1,lambda *args:dict(gate=True))
        record = state['stages']['1'];path=root/record['artifact']
        payload=json.loads(path.read_text());payload['gate']=False;write(path,payload)
        with self.assertRaises(RuntimeError):verify_record(root,record)

    def test_cached_gate_rejects_modified_matrix_or_gain(self):
        from run_flash_overnight_pipeline import artifact_hashes
        from eval_flash_pv_models import sha256
        for stage,name in [(2,'affine_models_frozen.json'),(3,'gains_frozen.json')]:
            root,state=self.fixture()
            write(root/name,{'coefficient':1.})
            write(root/'evidence.json',{'gate':True,'evidence_status':'PASS'})
            record=dict(status='PASS',artifact='evidence.json',artifact_sha256=sha256(root/'evidence.json'),
                artifacts_sha256=artifact_hashes(root,stage))
            self.assertTrue(verify_record(root,record))
            write(root/name,{'coefficient':2.})
            with self.assertRaises(RuntimeError):verify_record(root,record)

    def test_skip_reason_is_updated_when_a_later_resume_fails(self):
        root,state=self.fixture()
        state=run_stages(root,{},state,1,lambda *args:dict(gate=True))
        self.assertIn('not yet requested',state['stages']['5']['reason'])
        state=run_stages(root,{},state,2,lambda *args:dict(gate=False))
        self.assertIn('prerequisite stage 2 failed',state['stages']['5']['reason'])


if __name__=='__main__':unittest.main(verbosity=2)
