"""VALIDATION_SIM: nominal-prior online ID, with immutable identical baselines.

The warm-start trial is retained. Its common fixed-gain identification prefix is
replayed exactly while RLS starts from nominal A/B/c, not a mismatch-trained model.
Only Adaptive must be re-simulated; A/Bias/F1/Fixed are unchanged physical branches.
"""
import argparse
import copy
import json
from pathlib import Path
import shutil
import time

import numpy as np

from m4_mismatch_stages import PREVIOUS,authorize_m4
from m4_shadow_stages import ConstrainedRLS,ShadowRunner,reproduce,IX
from m4_adaptive_stages import GainMonitor,adaptive_summary
from m4_control_utils import rollout_control
from flash_overnight_control_stages import anchor
from flash_overnight_model_stages import REPO,CKPT,KEYS,current,parallel,prepared_config,write,sha256
from run_m4_followup_pipeline import stage_record,verify


def cold_job(item,cfg,output,warm,mismatch_source,nominal,gain):
    out=Path(output)/item['id'];out.mkdir();source=Path(warm)/'adaptive'/item['id']
    r=ShadowRunner(cfg,item['test']);rls=ConstrainedRLS(nominal)
    try:
        reproduce(r,item['test'],Path(mismatch_source))
        start_p=float(r.observation['sensor'][0])
        prefix=source/'common_identification_prefix.npz'
        with np.load(prefix) as trace:
            for i in range(3001):
                for key in KEYS:np.testing.assert_array_equal(r.observation[key],trace[key][i])
                if i<3000:
                    z=current(r)[IX].copy();z[0]-=start_p
                    tr=r.step(float(trace['requested_u'][i]))
                    for key,value in tr.items():np.testing.assert_array_equal(value,trace[key][i])
                    next_z=current(r)[IX].copy();next_z[0]-=start_p
                    rls.update(z,tr['actual_u'],next_z)
        pre=anchor(r);p_target=float(r.observation['sensor'][0]);mutable=copy.deepcopy(gain)
        monitor=GainMonitor(r,rls,mutable,nominal,p_target);original=r.step
        def observed_step(u):
            before=monitor.state();tr=original(u);monitor.update(before,tr);return tr
        r.step=observed_step
        try:trace,stats=rollout_control(r,'Adaptive_M4',mutable,60.,pre,p_target)
        finally:r.step=original
        trace['gain_K_after_step']=np.asarray(monitor.K_history)
        np.savez_compressed(out/'Adaptive_M4.npz',**trace)
        old=json.loads((source/'results.json').read_text())
        rows=[v for v in old['rows'] if v['group']!='Adaptive_M4']
        copied={}
        for name in ['A.npz','bias_only.npz','F1.npz','M4.npz','common_identification_prefix.npz']:
            shutil.copy2(source/name,out/name);copied[name]=sha256(source/name)
            assert sha256(out/name)==copied[name]
        with np.load(out/'M4.npz') as baseline:
            for key in KEYS:np.testing.assert_array_equal(trace[key][0],baseline[key][0])
            np.testing.assert_array_equal(trace['policy_observation'][0],baseline['policy_observation'][0])
            np.testing.assert_array_equal(trace['action'][0],baseline['action'][0])
        rows.append(dict(group='Adaptive_M4',**stats))
        write(out/'gain_updates.json',dict(accepted=monitor.accepted,events=monitor.events,
            sensor_only=True,prior='original nominal M4 A/B/c',prefix_exact=True,no_GT_or_effect_labels=True))
        result=dict(id=item['id'],condition=item['condition'],rows=rows,accepted_updates=monitor.accepted,
            copied_baseline_sha256=copied,nominal_prior_sha256=sha256(PREVIOUS/'affine_models_frozen.json'),
            common_prefix_and_initial_observation_action_exact=True,shadow_gate_previously_passed=True)
        write(out/'results.json',result)
        print('[VALIDATION_SIM] cold adaptive',item['id'],'accepted',monitor.accepted,flush=True)
        return result
    finally:r.env.close()


def run(root,plan,warm,source):
    old=json.loads((warm/'03_adaptive.json').read_text())
    verify(old['source_sha256']);verify(old['artifacts_sha256'],warm)
    shadow=json.loads((warm/'02_shadow.json').read_text())['result']
    assert shadow['gate'] is True
    manifest=json.loads((warm/'adaptive/manifest.json').read_text())
    items=manifest['items'];assert all(i['condition'] in shadow['eligible_for_adaptive'] for i in items)
    out=root/'adaptive';out.mkdir()
    write(out/'manifest.json',dict(manifest,initialization='nominal prior; no mismatch-trained coefficients',
        warm_evidence=str(warm),cold_plan_sha256=sha256(root/'plan.json'),
        reuse='Hash-identical common prefix and A/Bias/F1/Fixed branches; only Adaptive is re-simulated'))
    nominal=json.loads((PREVIOUS/'affine_models_frozen.json').read_text())['models']['M4']
    gain=json.loads((PREVIOUS/'gains_frozen.json').read_text())['models']['M4']
    cfg=json.loads(prepared_config(CKPT).read_text())
    results=parallel(cold_job,items,plan['workers'],cfg,str(out),str(warm),str(source),nominal,gain)
    write(out/'all_results.json',dict(rows=results))
    return adaptive_summary(results)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root',type=Path,required=True)
    parser.add_argument('--warm-root',type=Path,required=True)
    parser.add_argument('--workers',type=int,default=3)
    args=parser.parse_args();root=args.root.resolve();warm=args.warm_root.resolve()
    assert root.is_relative_to(REPO/'docs/exp') and not root.exists();root.mkdir(parents=True)
    prior=json.loads((warm/'plan.json').read_text())
    plan=dict(prior,workers=args.workers,nominal_prior_only=True,
        initialization_comparison='separate run; previous warm results and success criteria unchanged',
        extra_model_or_QR_tuning=False)
    write(root/'00_authorization.json',authorize_m4());write(root/'plan.json',plan)
    # Wait for a complete condition-gated trial, never consume RUNNING evidence.
    while True:
        path=warm/'03_adaptive.json'
        if path.exists() and json.loads(path.read_text()).get('status') in ['PASS','FAIL']:break
        time.sleep(2.)
    source=Path(prior['collector_recovery_source'])
    sources=[Path(__file__).resolve(),REPO/'test/m4_adaptive_stages.py',REPO/'test/m4_shadow_stages.py',
        REPO/'test/m4_control_utils.py',REPO/'test/run_m4_followup_pipeline.py',warm/'03_adaptive.json']
    stage_record(root,'03_adaptive',lambda:run(root,plan,warm,source),sources)
    verify(plan['protected_sha256'])


if __name__=='__main__':main()
