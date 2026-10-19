"""DESKTOP_DRY_RUN: reconstruct adaptation from only past sensor/command data."""
import argparse
from concurrent.futures import ProcessPoolExecutor
import json
from pathlib import Path

import numpy as np

from analyze_flash_state_learning import state
from m4_joint_adaptation import Command, fixed_gain, nominal
from run_static_target_adaptation import clean, sha256, verify, write
from static_target_domain import StaticEnv, CKPT, prepared_config
from static_target_learner import StaticLearner, MASKS


def audit_one(job):
    folder=Path(job['folder']);row=job['row'];arm=row['arm']
    learner=StaticLearner(MASKS[arm],np.asarray(job['leg_limits']),job['permit_K'])
    command=Command(previous=0.)
    with np.load(folder/(arm+'.npz'))as archive:
        trace=dict(archive);z=state(trace);z[:,0]-=float(trace['p_hold'])
        start={round(x['t']/.02):bool(x['reasons'])for x in row['startup_limit_events']}
        for i,u in enumerate(trace['actual_u']):
            K,bias,reference=learner.values()
            np.testing.assert_array_equal(K,trace['K_used'][i])
            np.testing.assert_array_equal(reference,trace['reference_used'][i])
            assert bias==trace['bias'][i]
            requested,details=command.compute(z[i],K,bias,reference,float(trace['probe'][i]))
            assert requested==trace['raw_requested'][i]
            assert details['global_clipped']==trace['global_clipped'][i]
            learner.observe(z[i],float(u),z[i+1],bool(trace['global_clipped'][i])or start.get(i,False))
        expected=json.loads((folder/(arm+'_learning.json')).read_text())
        assert clean(learner.report())==expected
        scale=np.maximum(nominal()['state_std'],1e-9);K0=np.asarray(fixed_gain()['K'])
        cumulative=np.linalg.norm((trace['K_used']-K0)*scale,axis=1)/np.linalg.norm(K0*scale)
        delta=np.linalg.norm(np.diff(trace['K_used'],axis=0)*scale,axis=1)
        previous=np.maximum(np.linalg.norm(trace['K_used'][:-1]*scale,axis=1),1e-12)
        assert np.max(cumulative)<=.250000001
        assert not len(delta)or np.max(delta/previous)<=.250000001
        result=dict(execution_domain='DESKTOP_DRY_RUN',evidence_status='PASS',arm=arm,
            sensor_command_only_exact=True,steps=len(trace['actual_u']),goal_fixed=True,
            candidate_models_events_parameters_exact=True,actual_input_limiter_exact=True,
            covariance_and_information_report_exact=True,new_target_K_adoptions=len(learner.K_adoptions),
            maximum_cumulative_K_change=float(np.max(cumulative)),
            archive_sha256=sha256(folder/(arm+'.npz')),learning_sha256=sha256(folder/(arm+'_learning.json')),
            audit_source_sha256=sha256(Path(__file__)))
    write(Path(job['out']),result)
    return result


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root',type=Path,required=True);parser.add_argument('--workers',type=int,default=3)
    args=parser.parse_args();root=args.root.resolve();plan=json.loads((root/'plan.json').read_text());verify(plan,root)
    cfg=json.loads(prepared_config(CKPT).read_text());env=StaticEnv(cfg,{})
    joints=[env.model.joint(env.joint_names[i]).id for i in [0,1,2,4,5,6]]
    leg_limits=env.model.jnt_range[joints].copy().tolist();env.close()
    destination=root/'causal_audit';destination.mkdir(exist_ok=True)
    jobs=[];old=[]
    for phase in ['shadow','primary','composite_shadow','composite_primary']:
        for file in (root/phase).glob('*/results.json'):
            data=json.loads(file.read_text())
            for row in data['rows']:
                arm=row['arm']
                if arm in ['Flash','Bias','Fixed']or not row['complete']:continue
                out=destination/(phase+'_'+file.parent.name+'_'+arm+'.json')
                if out.exists():
                    result=json.loads(out.read_text())
                    assert result['audit_source_sha256']==sha256(Path(__file__))
                    assert result['archive_sha256']==sha256(file.parent/(arm+'.npz'))
                    assert result['learning_sha256']==sha256(file.parent/(arm+'_learning.json'))
                    old.append(result);continue
                jobs.append(dict(folder=str(file.parent),row=row,permit_K=data['job'].get('permit_K',False),
                    leg_limits=leg_limits,out=str(out)))
    with ProcessPoolExecutor(max_workers=args.workers)as pool:
        results=list(pool.map(audit_one,jobs))
    verify(plan,root)
    write(root/'causal_replay_audit.json',dict(execution_domain='DESKTOP_DRY_RUN',evidence_status='PASS',
        episodes=len(old)+len(results),source_sha256=sha256(Path(__file__)),rows=old+results,
        limitation='Audits every complete online episode saved at invocation. Rerun after pipeline completion for the final count.'))
    print('DESKTOP_DRY_RUN: exact causal replay PASS',len(old)+len(results),'episodes',flush=True)


if __name__=='__main__':main()
