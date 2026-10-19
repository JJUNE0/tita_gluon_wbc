"""VALIDATION_SIM: shadow starts only from six completed Fixed M4 baselines.

This independent phase can run concurrently with the remaining drift-entry
collection. It reads only already completed, hash-bound settled mismatch data.
Initial-entry adaptive identification is a separate domain and remains untested.
"""
import argparse
import json
from pathlib import Path

from m4_mismatch_stages import authorize_m4, summarize
from m4_shadow_stages import run_shadow
from flash_overnight_model_stages import REPO, write, sha256
from run_m4_followup_pipeline import stage_record, verify


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root',type=Path,required=True)
    parser.add_argument('--source',type=Path,required=True)
    parser.add_argument('--workers',type=int,default=3)
    args=parser.parse_args();root=args.root.resolve();source=args.source.resolve()
    assert root.is_relative_to(REPO/'docs/exp') and not root.exists();root.mkdir(parents=True)
    authorization=authorize_m4();write(root/'00_authorization.json',authorization)
    rows=[];protected={}
    for p in sorted((source/'mismatch').glob('settled_*/results.json')):
        info=json.loads(p.read_text());rows+=info['rows']
        protected[str(p.relative_to(REPO))]=sha256(p)
        q=p.parent/'M4.npz';protected[str(q.relative_to(REPO))]=sha256(q)
    decision=summarize(rows)
    eligible=[name for name,r in decision['conditions'].items() if r['stable_completed']]
    assert eligible
    source_plan=json.loads((source/'plan.json').read_text())
    plan=dict(source_plan,workers=args.workers,eligible=eligible,shadow_scope='settled only',
        prerequisite_decision=decision,completed_input_sha256=protected,
        note='Performance FAIL does not authorize gain changes; stable completion authorizes shadow only. '
            'All six completed M4 traces required per condition; no unfinished data read.')
    write(root/'plan.json',plan);verify(protected)
    sources=[Path(__file__).resolve(),REPO/'test/m4_shadow_stages.py',REPO/'test/run_m4_followup_pipeline.py',REPO/'test/m4_mismatch_stages.py']
    stage_record(root,'02_shadow',lambda:run_shadow(root,plan,eligible,source),sources)
    verify(protected);verify(source_plan['protected_sha256'])


if __name__=='__main__':main()
