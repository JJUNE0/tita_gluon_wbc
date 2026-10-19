"""DESKTOP_DRY_RUN: replay estimator clocks and command algebra from saved sensors.

Post-collection audit only: no MuJoCo, tuning, new gain or dynamics labels.
"""
import argparse
import json
from pathlib import Path

import numpy as np

from online_local_m4 import verify,LocalRLS,B_SETTINGS,sha256,write
from analyze_flash_state_learning import state
from m4_joint_adaptation import Command


def audit(root):
    verify(root,full=True);budgets=[];replays=[]
    choices={('development','nominal',.01,900,-.035),('development','friction0.2',.02,902,.035),('test','friction0.2',.02,911,0.)}
    for split in ['development','test']:
        rows=json.loads((root/(split+'_results.json')).read_text())['rows']
        for row in rows:
            job=row['job'];folder=root/split/job['id']
            with np.load(folder/'trajectory.npz')as archive:trace=dict(archive)
            z=state(trace);z[:,0]-=float(trace['p_hold']);N=len(trace['actual_u']);delta=[];previous=0.
            for i in range(N):
                with_probe=Command(previous);with_probe.count=i;without_probe=Command(previous);without_probe.count=i
                args=(z[i],trace['K_used'][i],float(trace['bias'][i]),trace['reference_used'][i])
                command,_=with_probe.compute(*args,float(trace['probe'][i]));neutral,_=without_probe.compute(*args,0.)
                assert command==float(trace['raw_requested'][i]);previous=command;delta.append(command-neutral)
            delta=np.asarray(delta);train=trace['training_used'].astype(bool);val=trace['validation_window']>=0
            budgets.append(dict(split=split,id=job['id'],domain=job['domain'],amplitude=job['amplitude'],
                same_state_command_probe_energy=float(.02*np.sum(delta**2)),training_command_probe_energy=float(.02*np.sum(delta[train]**2)),
                validation_command_probe_energy=float(.02*np.sum(delta[val]**2)),requested_probe_energy=float(.02*np.sum(trace['probe']**2)),
                permitted_fraction=float(np.mean(trace['probe_allowed'])),training_samples=int(train.sum()),
                native_delivery_max_difference=float(np.max(abs(trace['actual_u']-trace['raw_requested']))),
                meaning='controller algebra with same measured state/previous command; not a physical isolated motor torque counterfactual'))
            key=(split,job['domain'],job['amplitude'],job['seed'],job['pitch'])
            if key not in choices:continue
            estimators={s['name']:LocalRLS(s)for s in B_SETTINGS};events={round(e['created']/.02):e for e in row['events']};checks=[]
            for i in range(N):
                time=i*.02
                if i in events:
                    recorded=json.loads((folder/events[i]['candidate_file']).read_text())['candidates']
                    for name,obj in estimators.items():
                        live=obj.freeze(time);old=recorded[name];assert live['status']==old['status']
                        if live['status']=='FROZEN':
                            for field in ['A','B','c_center']:np.testing.assert_array_equal(live['model'][field],old['model'][field])
                            for field in ['A','B','c_center']:np.testing.assert_array_equal(live['raw_recursive_model'][field],old['raw_recursive_model'][field])
                            np.testing.assert_array_equal(live['training_times'],old['training_times'])
                    checks.append(dict(time=time,estimators=5,refined_and_raw_models_exact=True))
                for obj in estimators.values():obj.observe(time+.02,z[i],float(trace['actual_u'][i]),z[i+1],bool(train[i]))
            replays.append(dict(split=split,id=job['id'],checks=checks,from_sensor_command_and_logged_sensor_safety_mask_only=True))
    assert len(replays)==3
    write(root/'probe_budget_audit.json',dict(execution_domain='DESKTOP_DRY_RUN',rows=budgets,source_sha256=sha256(Path(__file__)),posthoc=True,no_controller_change=True))
    write(root/'causal_replay_audit.json',dict(execution_domain='DESKTOP_DRY_RUN',evidence_status='PASS',rows=replays,
        model_checks=45,posthoc=True,source_sha256=sha256(Path(__file__)),no_MuJoCo_or_oracle=True))
    verify(root,full=True);print('DESKTOP_DRY_RUN replay3 timelines/45 raw+refined candidate model pairs exact; command budget36 exact',flush=True)


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);a=p.parse_args();audit(a.root.resolve())
