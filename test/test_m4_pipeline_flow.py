"""DESKTOP_DRY_RUN: performance FAIL and shadow authorization stay distinct."""
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import run_m4_pipeline as pipeline


class Flow(unittest.TestCase):
    def test_only_stable_settled_conditions_allow_shadow(self):
        result=dict(collection_complete=True,gate=False,conditions={
            'settled/gain0.8':dict(gate=False,stable_completed=True),
            'settled/lag0.05':dict(gate=False,stable_completed=False),
            'entry/nominal':dict(gate=True,stable_completed=True)})
        self.assertEqual(pipeline.continuation_conditions(result),['settled/gain0.8'])
        result['collection_complete']=False
        self.assertEqual(pipeline.continuation_conditions(result),[])

    def test_failed_shadow_never_calls_adaptive(self):
        with tempfile.TemporaryDirectory(dir=Path(__file__).parent) as name:
            root=Path(name)
            mismatch=dict(collection_complete=True,gate=False,
                conditions={'settled/gain0.8':dict(stable_completed=True)})
            with patch.object(pipeline,'stage_record',side_effect=[mismatch,dict(gate=False)]) as stage:
                with patch.object(pipeline,'run_adaptive') as adaptive:
                    pipeline.execute(root,dict(reuse_completed_source=None),'adaptive')
                    adaptive.assert_not_called()
                    self.assertEqual(stage.call_count,2)
            self.assertIn('No independently validated',(root/'03_adaptive.json').read_text())


if __name__=='__main__':unittest.main()
