"""DESKTOP_DRY_RUN: immutable evidence, wheel-only application and source audit."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess

import numpy as np

from flash_overnight_model_stages import REPO,write,sha256
from run_m4_followup_pipeline import verify

SOURCES=['m4_mismatch_stages.py','run_m4_followup_pipeline.py','test_m4_followup.py',
    'm4_shadow_stages.py','test_m4_shadow.py','m4_control_utils.py','analyze_m4_followup.py',
    'm4_adaptive_stages.py','test_m4_adaptive.py','run_m4_shadow_phase.py',
    'run_m4_recovery_pipeline.py','run_m4_pipeline.py','test_m4_pipeline_flow.py','audit_m4_followup.py',
    'run_m4_coldstart_adaptive.py']
LEGS=[0,1,2,4,5,6]


def audit(evidence,report):
    previous=json.loads((evidence/'previous_evidence_sha256.json').read_text());verify(previous)
    root=evidence/'run_final';plan=json.loads((root/'plan.json').read_text());verify(plan['protected_sha256'])
    recovered_source=Path(plan['collector_recovery_source'])
    recovered_record=json.loads((recovered_source/'01_mismatch.json').read_text())
    verify(recovered_record['source_sha256']);verify(recovered_record['artifacts_sha256'],recovered_source)
    rows=json.loads((root/'mismatch/metrics.json').read_text())['rows'];assert len(rows)==432
    saturation=0;failure=0;leg_error=0.
    for folder in sorted((root/'mismatch').iterdir()):
        if not folder.is_dir():continue
        info=json.loads((folder/'results.json').read_text());first=None
        assert info['initial_full_snapshot_history_identical']
        for row in info['rows']:
            with np.load(folder/row['trace']) as z:
                for key in ['motor','physical_motor']:
                    leg_error=max(leg_error,float(np.max(abs(z[key][:,:,LEGS]-z['flash'][:,:,LEGS]))))
                    assert np.max(abs(z[key][:,:,[3,7]]))<=12.000001
                if first is None:first={k:z[k][0].copy() for k in ['sensor','previous_action','policy_observation','action']}
                else:
                    for k,v in first.items():np.testing.assert_array_equal(z[k][0],v)
                np.testing.assert_array_equal(z['previous_action'][:-1],z['history'])
                np.testing.assert_array_equal(z['previous_action'][1:],z['action'])
                saturation+=int(np.any(abs(z['actual_u']-z['requested_u'])>1e-6))
                if row['group']=='M4':assert max(abs(z['correction']))<=.050000001
                if not row['complete']:
                    failure+=1;assert row['failure'] and row['duration_s']<60.
                    assert row['base']['last5_RMSE'] is None
        physics=info['physics'];mu=info['job']['effect'].get('friction')
        if mu is not None:
            assert physics['actual_contacts']
            assert all(abs(c['sliding_friction']-mu)<1e-12 for c in physics['actual_contacts'])
    assert leg_error==0. and saturation>0 and failure==48
    for name in ['01_mismatch','02_shadow','03_adaptive']:
        record=json.loads((root/(name+'.json')).read_text())
        if record['status'] in ['PASS','FAIL']:
            verify(record['source_sha256']);verify(record['artifacts_sha256'],root)
    cold=evidence/'cold_adaptive'
    cold_record=json.loads((cold/'03_adaptive.json').read_text())
    verify(cold_record['source_sha256']);verify(cold_record['artifacts_sha256'],cold)
    cold_rows=json.loads((cold/'adaptive/all_results.json').read_text())['rows']
    assert len(cold_rows)==9
    for info in cold_rows:
        assert info['common_prefix_and_initial_observation_action_exact']
        folder=cold/'adaptive'/info['id']
        for name,h in info['copied_baseline_sha256'].items():assert sha256(folder/name)==h
    # Task sources are new; preserve a compact reviewable diff including the report.
    pieces=[]
    for path in [REPO/'test'/name for name in SOURCES]+[report]:
        result=subprocess.run(['git','diff','--no-index','--','/dev/null',str(path)],capture_output=True)
        assert result.returncode in [0,1];pieces.append(result.stdout)
    (evidence/'task.diff').write_bytes(b''.join(pieces))
    tracked=subprocess.check_output(['git','diff','--binary'])
    current=hashlib.sha256(tracked).hexdigest()
    old=(evidence/'tracked_diff_before.sha256').read_text().strip()
    branch=subprocess.check_output(['git','branch','--show-current'],text=True).strip()
    snapshot=evidence/'source_final';snapshot.mkdir(exist_ok=True)
    for name in SOURCES:(snapshot/(name+'.txt')).write_bytes((REPO/'test'/name).read_bytes())
    review=dict(execution_domain='DESKTOP_DRY_RUN',evidence_status='PASS',
        protected_old_files=len(previous),old_evidence_unchanged=True,runtime_policy_config_unchanged=True,
        mismatch_rows=len(rows),complete=sum(r['complete'] for r in rows),failures=failure,
        failed_full_horizon_metrics_absent=True,saturated_episodes_recorded=saturation,leg_torque_max_difference=leg_error,
        initial_state_observation_action_equal=True,history_unchanged=True,
        all_stage_sources_and_artifacts_verified=True,actual_contact_friction_verified=True,
        cold_nominal_prior_pairs=len(cold_rows),cold_baselines_and_prefix_exact=True,
        tracked_diff_before=old,tracked_diff_after=current,tracked_diff_preserved=current==old,
        source_sha256={name:sha256(REPO/'test'/name) for name in SOURCES},branch=branch,
        agent_check='See agent_check.log; existing whitespace failure is not converted to PASS')
    write(evidence/'final_review.json',review)
    print(json.dumps(review,ensure_ascii=False,indent=2))


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root',type=Path,required=True);parser.add_argument('--report',type=Path,required=True)
    args=parser.parse_args();audit(args.root.resolve(),args.report.resolve())
