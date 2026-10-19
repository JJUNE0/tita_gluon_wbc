"""VALIDATION_SIM: finish the M4-only branch without overwriting failed evidence.

Completed unchanged control trials are hash-verified and reused. Only interrupted
lag trials need the saturation-aware collector. Old M4/M5 gates and coefficients
remain read-only. Shadow is permitted by stable completion, not performance PASS.
"""
import argparse
import json
from pathlib import Path
import shutil
import time

from m4_mismatch_stages import PREVIOUS,authorize_m4,jobs,summarize,job_run
from flash_overnight_model_stages import REPO,CKPT,parallel,prepared_config,write,sha256
from run_m4_followup_pipeline import stage_record,verify


def saturated_job(*args):
    # Only the recording assertion differs. The exact control equations, gain,
    # adapter, saturation, and all statistical success predicates are unchanged.
    import m4_mismatch_stages
    from m4_control_utils import rollout_control
    m4_mismatch_stages.rollout_control=rollout_control
    return job_run(*args)


def collect(root,plan,source):
    out=root/'mismatch';out.mkdir()
    batch=jobs();rows=[];missing=[];cached={}
    for job in batch:
        folder=source/'mismatch'/job['id'];info=folder/'results.json'
        if not info.is_file():missing.append(job);continue
        old=json.loads(info.read_text());assert old['job']==job
        assert sorted(r['group'] for r in old['rows'])==['A','F1','M4','bias_only']
        expected={p.name:sha256(p) for p in folder.iterdir() if p.is_file()}
        shutil.copytree(folder,out/job['id'])
        for name,h in expected.items():assert sha256(out/job['id']/name)==h
        cached[job['id']]=dict(source=str(folder),sha256=expected)
        rows.extend(old['rows'])
    write(out/'manifest.json',dict(execution_domain='VALIDATION_SIM',jobs=batch,
        reused_completed=cached,recovered_jobs=missing,old_stage5_thresholds_unchanged=True,
        collector_fix='Actual residual can be smaller than request at wheel saturation; record both instead of aborting.',
        source= str(source),gain_sha256=sha256(PREVIOUS/'gains_frozen.json')))
    cfg=json.loads(prepared_config(CKPT).read_text())
    gain=json.loads((PREVIOUS/'gains_frozen.json').read_text())['models']['M4']
    parts=parallel(saturated_job,missing,plan['workers'],cfg,str(out),gain)
    rows += [r for part in parts for r in part]
    assert len(rows)==432
    write(out/'metrics.json',dict(execution_domain='VALIDATION_SIM',rows=rows))
    result=summarize(rows);result.update(collection_complete=True,reused_jobs=len(cached),recovered_jobs=len(missing))
    return result


def imported_shadow(root,shadow_root,stable):
    record=json.loads((shadow_root/'02_shadow.json').read_text())
    verify(record['source_sha256']);verify(record['artifacts_sha256'],shadow_root)
    result=record['result']
    assert set(result['eligible_for_adaptive'])<=set(stable)
    write(root/'shadow_reference.json',dict(root=str(shadow_root),record_sha256=sha256(shadow_root/'02_shadow.json'),
        all_artifacts_verified=True,stable_conditions=stable,
        scope='settled conditions; entry identification/adaptation NOT_TESTED'))
    return dict(result,source_root=str(shadow_root),imported_record_sha256=sha256(shadow_root/'02_shadow.json'))


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root',type=Path,required=True)
    parser.add_argument('--source',type=Path,required=True)
    parser.add_argument('--shadow-root',type=Path,required=True)
    parser.add_argument('--workers',type=int,default=3)
    args=parser.parse_args();root=args.root.resolve();source=args.source.resolve();shadow=args.shadow_root.resolve()
    assert root.is_relative_to(REPO/'docs/exp') and not root.exists();root.mkdir(parents=True)
    assert json.loads((source/'01_mismatch.json').read_text())['status']=='FAIL'
    write(root/'00_authorization.json',authorize_m4())
    prior=json.loads((source/'plan.json').read_text())
    plan=dict(prior,workers=args.workers,collector_recovery_source=str(source),shadow_root=str(shadow),
        old_failed_collection_preserved=True,source_recovery='reuse completed identical trials, collect only missing saturation cases',
        adaptive_success='all3 complete, each accepts >=1 gain, median base IAE <=90% fixed, >=2/3 paired wins; pitch/wheel/final-speed limits',
        shadow_scope='settled only; entry remains fixed-controller robustness evaluation')
    write(root/'plan.json',plan);verify(plan['protected_sha256'])
    sources=[Path(__file__).resolve(),REPO/'test/run_m4_followup_pipeline.py',REPO/'test/m4_mismatch_stages.py',REPO/'test/m4_control_utils.py']
    mismatch=stage_record(root,'01_mismatch',lambda:collect(root,plan,source),sources)
    if not mismatch.get('collection_complete'):
        write(root/'02_shadow.json',dict(status='NOT_TESTED',reason='Incomplete mismatch collection'));return
    stable=[k for k,v in mismatch['conditions'].items() if k.startswith('settled/') and v['stable_completed']]
    # The independently running shadow phase must finish before its gate can be
    # consumed; an unfinished/failed/exception record never authorizes a gain.
    while True:
        path=shadow/'02_shadow.json'
        if path.is_file() and json.loads(path.read_text()).get('status') in ['PASS','FAIL']:break
        time.sleep(2.)
    shadow_files=[p for p in shadow.rglob('*') if p.is_file()]
    decision=stage_record(root,'02_shadow',lambda:imported_shadow(root,shadow,stable),sources+shadow_files)
    if decision.get('gate') is not True:
        write(root/'03_adaptive.json',dict(status='NOT_TESTED',reason='No condition with independent shadow PASS'))
    else:
        from m4_adaptive_stages import run_adaptive
        stage_record(root,'03_adaptive',lambda:run_adaptive(root,plan,decision,shadow,source),
            sources+shadow_files+[REPO/'test/m4_adaptive_stages.py',REPO/'test/m4_shadow_stages.py'])
    verify(plan['protected_sha256'])


if __name__=='__main__':main()
