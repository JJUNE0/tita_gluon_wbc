"""VALIDATION_SIM: five physically stable guarded shock comparators.

Model confidence is NOT promoted. A failed model keeps the runtime gain gate
closed; this supplemental protocol still measures that guarded controller as a
comparison arm. The original stricter admission/result files are immutable.
"""
import argparse
import copy
import json
from pathlib import Path
import shutil

import numpy as np

from eval_m4_joint_pipeline import (REPO,CKPT,KEYS,EFFECTS,parallel,shock_job,prepared_config,
    write,sha256,arrays,verify)


def comparison_decision(original):
    result=copy.deepcopy(original)
    for condition,arms in result['conditions'].items():
        for name,gate in arms.items():
            gate['original_admissible']=bool(gate.get('admissible',False))
            gate['admissible']=bool(gate.get('physical_stable',False))
            gate['comparison_only']=bool(gate['admissible'] and not gate['original_admissible'])
            # Crucially preserve model_gate AND performance as originally judged.
    result['protocol']='Physical stability admits guarded simulation comparators; model/performance gates unchanged.'
    return result


def run(source,out,workers):
    assert not out.exists() and out.is_relative_to(REPO/'docs/exp');out.mkdir(parents=True)
    original=json.loads((source/'online_decision.json').read_text())
    study=json.loads((source/'plan.json').read_text());verify(study)
    for p,h in study['source_sha256'].items():assert sha256(REPO/p)==h,p
    decision=comparison_decision(original)
    write(out/'online_decision.json',decision)
    jobs=[dict(j,change_gain=EFFECTS[j['condition']]['gain']) for j in study['jobs']
        if j['condition']!='nominal' and any(v['performance'] for v in original['conditions'].get(j['condition'],{}).values())]
    files={}
    for job in study['acquisition']:
        folder=out/'acquisition'/job['id'];folder.mkdir(parents=True)
        for name in ['snapshot.pkl.gz','results.json']:
            src=source/'acquisition'/job['id']/name;dst=folder/name;shutil.copy2(src,dst)
            h=sha256(src);assert sha256(dst)==h;files[str(src)]=h
    for item in study['training']:
        folder=out/'training'/item['id'];folder.mkdir(parents=True)
        src=source/'training'/item['id']/'frozen.json';shutil.copy2(src,folder/src.name);files[str(src)]=sha256(src)
    metadata=dict(study,source_root=str(source),protocol='guarded_simulation_comparators',jobs=jobs,
        guarded_admission='All6 physically stable, original model/performance flags preserved; '
            'K-only/Full keep last accepted K when candidate model fails, never apply a failed gain.',
        original_online_decision_sha256=sha256(source/'online_decision.json'),
        exact_shared_input_and_state_files=files,driver_sha256=sha256(Path(__file__)),
        no_controller_or_gain_guard_change=True,no_post_change_results_used_for_admission=True)
    write(out/'plan.json',metadata);(out/'shock').mkdir()
    cfg=json.loads(prepared_config(CKPT).read_text())
    rows=parallel(shock_job,jobs,workers,cfg,str(out)) if jobs else []
    for path,h in files.items():assert sha256(Path(path))==h
    assert sha256(source/'online_decision.json')==metadata['original_online_decision_sha256']
    assert sha256(Path(__file__))==metadata['driver_sha256']
    write(out/'shock_results.json',dict(rows=rows,status='TESTED' if rows else 'NOT_TESTED',
        reason=None if rows else 'No condition passed preceding online performance gate',
        primary_supplemental_five_arm_comparison=True))
    print('[VALIDATION_SIM] guarded shock complete',len(rows),'contexts',flush=True)


def compare_shared(source,out):
    old=json.loads((source/'shock_results.json').read_text())['rows']
    new=json.loads((out/'shock_results.json').read_text())['rows'];count=0
    for case in old:
        matched=next(c for c in new if c['job']['id']==case['job']['id'])
        for row in case['rows']:
            corresponding=next(x for x in matched['rows'] if x['group']==row['group'])
            a=arrays(source/'shock'/case['job']['id']/row['trace']);b=arrays(out/'shock'/case['job']['id']/corresponding['trace'])
            for key in KEYS+['policy_observation','action','history','physical_motor','actual_u','requested_u','K_used','bias','reference_used']:
                np.testing.assert_array_equal(a[key],b[key])
            count+=1
    write(out/'shared_comparator_replay.json',dict(execution_domain='DESKTOP_DRY_RUN',evidence_status='PASS',
        original_common_arms_exact=count,no_old_result_overwrite=True,no_double_counting=True))


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--source',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True);p.add_argument('--workers',type=int,default=3)
    p.add_argument('--compare-shared',action='store_true');args=p.parse_args()
    if args.compare_shared:compare_shared(args.source.resolve(),args.output.resolve())
    else:run(args.source.resolve(),args.output.resolve(),args.workers)
