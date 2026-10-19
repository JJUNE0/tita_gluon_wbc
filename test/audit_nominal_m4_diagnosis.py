"""DESKTOP_DRY_RUN: saved-evidence audit and preregistered paired8s supplement.

Added after model freezing; computes no fit and cannot select or replace a model.
"""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess

import numpy as np

from nominal_m4_diagnosis import REPO,TIMES,SOURCES,verify,write,sha256,read_new
from analyze_flash_state_learning import predict,metric


def audit(root):
    plan=verify(root,full=True);models=json.loads((root/'models_frozen.json').read_text())['models']
    legacy=json.loads((root/'legacy_models.json').read_text());comparisons=json.loads((root/'comparison.json').read_text())['rows']
    data={t:read_new(root,'test',t)[0]for t in TIMES};supplement=[]
    for row in comparisons:
        key=row['key'];model=legacy[key[6:]]if key.startswith('prior_')else models[key]['model'];records=data[row['test_time']]
        if not records:continue
        z=np.asarray([r['delta']for r in records]);u=np.asarray([r['u']-r['base_u']for r in records])
        free=predict(np.asarray(model['A']),np.asarray(model['B']),z[:,0],u)
        stats=metric(free[:,1:],z[:,1:])
        supplement.append(dict(key=key,test_time=row['test_time'],full8={k:np.median(v,axis=0).tolist()for k,v in stats.items()}))
    write(root/'paired_eight_second_metrics.json',dict(execution_domain='DESKTOP_DRY_RUN',source='preregistered supplemental metric, saved model and test arrays only',rows=supplement,no_fit=True))
    collection=[];files=0;native_leg=[0,1,2,4,5,6]
    for split in ['train','test']:
        rows=json.loads((root/(split+'_results.json')).read_text())['rows'];assert len(rows)==6
        for result in rows:
            assert result['prefix_complete']and result['target_static']and result['goal_never_reset']and result['no_model_in_control']
            folder=root/split/result['job']['id'];physics=json.loads((folder/'physics.json').read_text());assert physics['configured_before_first_step']and physics['target']=={}
            with np.load(folder/'prefix.npz')as t:
                assert float(t['p_hold'])==float(t['sensor'][0,0])==result['p_hold']and len(t['actual_u'])==50000
                np.testing.assert_array_equal(t['previous_action'][:-1],t['history']);np.testing.assert_array_equal(t['previous_action'][1:],t['action'])
                np.testing.assert_array_equal(t['physical_motor'][:,:,native_leg],t['flash'][:,:,native_leg])
                assert np.max(abs(t['physical_motor'][:,:,[3,7]]))<=12.000001
                assert t['actual_u'][13:].min()>=.4328-1e-6 and t['actual_u'].max()<=.5328+1e-6
                assert np.max(abs(np.diff(np.r_[0.,t['requested_u']])))/.02<=2.000001
            for snap in result['snapshots']:
                assert snap['status']=='COMPLETE'and snap['baseline_exact_replay'];directory=folder/snap['folder']
                if snap['time']==1000.:assert snap['settled_gate']['operating_gate']
                for f in directory.glob('*.npz'):
                    with np.load(f)as t:
                        np.testing.assert_array_equal(t['previous_action'][:-1],t['history']);np.testing.assert_array_equal(t['previous_action'][1:],t['action'])
                        np.testing.assert_array_equal(t['physical_motor'][:,:,native_leg],t['flash'][:,:,native_leg])
                        assert np.max(abs(t['physical_motor'][:,:,[3,7]]))<=12.000001
                        assert t['actual_u'].min()>=.4328-1e-6 and t['actual_u'].max()<=.5328+1e-6
                        assert np.max(abs(np.diff(np.r_[.4828,t['requested_u']])))/.02<=2.000001
                    files+=1
                collection.append(dict(split=split,case=result['job']['id'],time=snap['time'],responses=len(snap['responses'])))
    assert len(collection)==48 and sum(x['responses']for x in collection)==816 and files==960
    mh=sha256(root/'models_frozen.json');assert mh==(root/'models_frozen.sha256').read_text().strip()
    for entry in models.values():
        m=entry['model'];expected=np.zeros(24);expected[0]=1
        np.testing.assert_array_equal(np.asarray(m['A'])[:,0],expected);np.testing.assert_array_equal(np.asarray(m['B'])[4:12],np.zeros(8))
    current=hashlib.sha256(subprocess.check_output(['git','diff','--binary'])).hexdigest()
    branch=subprocess.check_output(['git','branch','--show-current'],text=True).strip();assert branch.startswith('agent/')
    extra=Path(__file__);shutil.copy2(extra,root/(extra.name+'.source.txt'))
    source={str(REPO/'test'/s):sha256(REPO/'test'/s)for s in SOURCES};source[str(extra)]=sha256(extra)
    tests=(root/'unit_tests.log').read_text();assert 'Ran 4 tests'in tests and 'OK'in tests
    check=(root/'agent_check.log').read_text();assert check.rstrip().endswith('FAIL')and check.count('trailing whitespace.')==6
    report=root.parent/'SUMMARY.md';assert report.exists()
    owned=[REPO/'test'/s for s in SOURCES]+[extra,report,root.parent/'PLAN.md',root/'REPORT.md'];diff=[]
    for p in owned:
        c=subprocess.run(['git','diff','--no-index','--check','/dev/null',str(p)],capture_output=True,text=True)
        assert c.returncode in [0,1]and not c.stdout and not c.stderr,(p,c.stdout,c.stderr)
        d=subprocess.run(['git','diff','--no-index','--','/dev/null',str(p)],capture_output=True,text=True);assert d.returncode==1;diff.append(d.stdout)
    (root.parent/'task.diff').write_text('\n'.join(diff))
    write(root/'completion_audit.json',dict(execution_domain='DESKTOP_DRY_RUN',evidence_status='PASS'if current==plan['tracked_diff_sha256']else'SUSPICIOUS',
        meaning='Evidence integrity; scientific pass/fail remains per comparison',branch=branch,plan_sha256=sha256(root/'plan.json'),models_sha256=mh,
        sources=source,protected_files=len(plan['protected_sha256']),tracked_diff_unchanged=current==plan['tracked_diff_sha256'],
        new_streams=12,snapshots=48,probes=816,baselines=48,Direct_B_pairs=48,trace_NPZ=files,models=len(models),comparisons=len(comparisons),
        train_test_seeds_disjoint=not {x['seed']for x in plan['starts']['train']}&{x['seed']for x in plan['starts']['test']},
        core_sources_frozen_before_collection=True,post_collection_audit_source=sha256(extra),no_fit_or_selection_in_audit=True,
        known_command_and_action_timing=True,leg_path_preserved=True,no_goal_reset=True,no_controller_RLS_policy_QR_changes=True,
        tests='4 unit tests PASS; legacy fitter and physical replay checks in separate JSON',agent_check='FAIL: six pre-existing trailing-whitespace lines',
        task_diff_sha256=sha256(root.parent/'task.diff'),no_hardware=True,no_commit_push=True,collection=collection))
    verify(root,full=True)
    print('DESKTOP_DRY_RUN completion audit',len(collection),'snapshots',len(supplement),'paired8s evaluations',flush=True)


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);a=p.parse_args();audit(a.root.resolve())
