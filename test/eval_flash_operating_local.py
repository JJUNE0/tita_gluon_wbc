"""VALIDATION_SIM: fresh train/test responses near the fixed0.4828Nm point.

Same synchronized model_60000 and M2/M4 states. Whole simulator, estimator and
raw-action history are cloned at each branch. F-1 and adaptive control are off.
"""

import argparse
from concurrent.futures import ProcessPoolExecutor, as_completed
import json
from pathlib import Path

import numpy as np

from eval_flash_state_learning import StateRunner, STATE_KEYS, make_inputs
from eval_flash_pv_models import REPO, CKPT, prepared_config, sha256, write
from eval_flash_constant_hold import metrics as hold_metrics, GATES
from eval_flash_stop_release import inputs_for
from analyze_flash_state_learning import state

BIAS = .4828
COUNT = 400


def cases(split, smoke=False):
    if smoke:
        return [('train_prbs',.02),('pulse_pos',.05),('micro_prbs',.01)]
    families=['train_sine','train_prbs'] if split=='train' else ['validation_sine','validation_prbs']
    families += ['pulse_pos','pulse_neg','step_pos','step_neg']
    if split=='test':
        families += ['bipulse_pos','bipulse_neg']
    return [(f,a) for f in families for a in [.02,.05]]+[('micro_prbs',.01)]


def job_run(cfg,job,root):
    out=Path(root)/job['id']
    out.mkdir()
    runner=StateRunner(cfg,job)
    snapshots,initial,rows,steps,startup={},[],[],[],[]
    try:
        prefix_s=30. if job['approach']=='high' else 8.
        tau=0.
        for tick in range(round(prefix_s/.02)):
            if tick<50 and runner.failures():
                startup.append(dict(rl_s=tick*.02,failures=runner.failures()))
            elif tick>=50:
                assert not runner.failures(),(job,tick,runner.failures())
            tau=min(.6,tau+.04) if job['approach']=='high' else 0.
            runner.step(tau)
        ticks=[round(t/.02) for t in job['times']]
        end=max(ticks)+COUNT
        for tick in range(end+1):
            rows.append({k:runner.observation[k].copy() for k in STATE_KEYS})
            assert not runner.failures(),(job,tick,runner.failures())
            if tick in ticks:
                snapshots[tick]=runner.snapshot()
                initial.append(dict(tick=tick,qpos=runner.env.data.qpos.copy(),qvel=runner.env.data.qvel.copy(),
                    ctrl=runner.env.data.ctrl.copy(),act=runner.env.data.act.copy(),
                    time=float(runner.env.data.time),last_action=runner.playback.last_action.copy()))
            if tick<end:
                tau=float(np.clip(BIAS,tau-.04,tau+.04))
                steps.append(runner.step(tau))
        prefix={k:np.asarray([r[k] for r in rows]) for k in STATE_KEYS}
        prefix.update({k:np.asarray([r[k] for r in steps]) for k in steps[0]})
        np.savez_compressed(out/'prefix.npz',**prefix)
        np.savez_compressed(out/'initial_states.npz',**{k:np.asarray([r[k] for r in initial]) for k in initial[0]})
        if job.get('smoke'):
            old=REPO/'docs/exp/2026-10-15/flash_constant_hold/qualification/s170_p-0.035_r0.482800_zero_900s/hold.npz'
            with np.load(old) as archive:
                for k in prefix:
                    np.testing.assert_array_equal(prefix[k][:len(archive[k])],archive[k])
        acquisitions,responses,direct=[],[],[]
        limits=runner.env.model.jnt_range[runner.leg_joints]
        for tick,snapshot in snapshots.items():
            # Last180s gate, using unchanged60s-settle metrics on the preceding240s slice.
            begin=tick-12000
            history={k:v[begin:tick+1] if k in STATE_KEYS else v[begin:tick] for k,v in prefix.items()}
            gate=hold_metrics(history,limits,True,240.)
            acquisitions.append(dict(start_hold_s=tick*.02,start_rl_s=prefix_s+tick*.02,
                gate_window_hold_s=[tick*.02-180.,tick*.02],metrics=gate))
            if not gate['operating_gate']:
                continue
            runner.restore(snapshot)
            base,failure=runner.rollout(np.full(COUNT,BIAS))
            assert not failure and len(base['sensor'])==COUNT+1
            for k in STATE_KEYS:
                np.testing.assert_array_equal(base[k],prefix[k][tick:tick+COUNT+1])
            for k in ['action','motor','flash','history','policy_observation','actual_u','requested_u']:
                np.testing.assert_array_equal(base[k],prefix[k][tick:tick+COUNT])
            baseline=f'zero_t{tick}.npz'
            np.savez_compressed(out/baseline,**base)
            for index,(family,amplitude) in enumerate(cases(job['split'],job.get('smoke',False))):
                seed=int(np.random.SeedSequence([job['seed'],job['pitch_index'],tick,index,28101]).generate_state(1)[0])
                probe=inputs_for(family,amplitude,seed,COUNT)
                runner.restore(snapshot)
                trace,failure=runner.rollout(BIAS+probe)
                assert not failure and len(trace['sensor'])==COUNT+1,(job,tick,family,failure)
                assert max(abs(trace['actual_u']-trace['requested_u']))<1e-6
                assert max(abs(trace['requested_u']-BIAS))<=.050000001
                assert max(abs(np.diff(np.r_[BIAS,trace['requested_u']])))<=.040000001
                for k in STATE_KEYS:
                    np.testing.assert_array_equal(trace[k][0],base[k][0])
                np.testing.assert_array_equal(trace['action'][0],base['action'][0])
                np.testing.assert_array_equal(trace['policy_observation'][0],base['policy_observation'][0])
                filename=f'{family}_a{amplitude:g}_t{tick}.npz'
                np.savez_compressed(out/filename,**trace)
                responses.append(dict(trace=filename,baseline=baseline,family=family,amplitude=amplitude,
                    input_seed=seed,start_hold_s=tick*.02,start_rl_s=prefix_s+tick*.02,bias=BIAS))
            for amplitude in [.005,.01,.02]:
                runner.restore(snapshot);plus,pf=runner.rollout([BIAS+amplitude])
                runner.restore(snapshot);minus,mf=runner.rollout([BIAS-amplitude])
                assert not pf and not mf
                np.testing.assert_array_equal(plus['action'][0],base['action'][0])
                np.testing.assert_array_equal(minus['action'][0],base['action'][0])
                denominator=plus['actual_u'][0]-minus['actual_u'][0]
                b=(state(plus)[1]-state(minus)[1])/denominator
                np.testing.assert_array_equal(b[4:12],np.zeros(8))
                direct.append(dict(start_hold_s=tick*.02,amplitude=amplitude,sensor_B=b.tolist(),
                    gt_B=((plus['gt'][1]-minus['gt'][1])/denominator).tolist()))
        write(out/'results.json',dict(execution_domain='VALIDATION_SIM',evidence_status='PASS',job=job,
            acquisitions=acquisitions,responses=responses,direct_B=direct,startup_violations=startup,
            whole_MuJoCo_snapshot=True,raw_history=True,exact_zero_prefix_replay=True,
            F1_enabled=False,no_control_or_affine_model=True,
            sensors='current joint state and clone-refreshed IMU for actor and measured state'))
        result=dict(id=job['id'],split=job['split'],accepted=sum(r['metrics']['operating_gate'] for r in acquisitions),
            planned=len(acquisitions),responses=len(responses),direct_pairs=len(direct))
        print('[VALIDATION_SIM]',result,flush=True)
        return result
    finally:
        runner.env.close()


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--workers',type=int,default=3)
    parser.add_argument('--smoke',action='store_true')
    args=parser.parse_args()
    out=args.output.resolve()
    if not out.is_relative_to(REPO/'docs/exp') or out.exists():
        parser.error('New output directory under docs/exp required')
    out.mkdir(parents=True)
    jobs=[]
    for split,seeds,times in [('train',[180,181],[900.,1020.,1140.]),('test',[190,191],[960.,1080.,1200.])]:
        for seed in seeds:
            for pi,pitch in enumerate([-.035,0.,.035]):
                approach='zero' if (seed+pi)%2==0 else 'high'
                jobs.append(dict(id=f'{split}_s{seed}_p{pitch:+.3f}_{approach}',split=split,
                    seed=seed,pitch=pitch,pitch_index=pi,approach=approach,times=times))
    if args.smoke:
        jobs=[dict(id='smoke_s170_p-0.035_zero',split='train',seed=170,pitch=-.035,pitch_index=0,
            approach='zero',times=[900.],smoke=True)]
    config=prepared_config(CKPT)
    cfg=json.loads(config.read_text())
    protected=list((REPO/'sim2sim/sim2sim_ros2_jazzy').rglob('*.py'))
    protected += [REPO/'sim2sim/lqr'/f for f in ['runtime.py','model.py','estimator.py']]
    protected += [REPO/'test'/f for f in ['eval_flash_pv_models.py','eval_flash_state_learning.py',
        'analyze_flash_state_learning.py','eval_flash_constant_hold.py','eval_flash_stop_release.py']]
    protected += [REPO/'docs/exp/2026-10-15/flash_constant_hold/qualification/models_used.json',
        config,config.parent/'policy.onnx',CKPT/'actor.pt']
    hashes={str(p.relative_to(REPO)):sha256(p) for p in protected}
    write(out/'manifest.json',dict(execution_domain='VALIDATION_SIM',evidence_status='NOT_TESTED',
        checkpoint_sha256=sha256(CKPT/'actor.pt'),onnx_sha256=sha256(config.parent/'policy.onnx'),
        script_sha256=sha256(Path(__file__)),protected_sha256=hashes,jobs=jobs,bias=BIAS,
        state_models=['M2: p,v,pitch,rate,previous_action8','M4: M2+leg_position6+leg_velocity6'],
        gate='past180s, unchanged speed/position/pitch/leg thresholds',operating_gates=GATES,
        primary='direct Bv sign/error<=30%; median p/v NRMSE<=30% at first2s and rolling0.1/0.5/1/2s',
        supplemental='first4s/8s,rolling4s,velocity reversal and4..8s decay; absolute RMSE and floors',
        probe='8s,0.02/0.05Nm total amplitude,microPRBS0.01;2Nm/s slew; same constant bias both arms',
        split='disjoint seed sets, all moments and probes of an initial condition stay in its split',
        fit='train-only unchanged scaled least squares; position translation symmetry; next raw action B rows0',
        scope='local A/B identification only; no affine,LQR,Q/R,state expansion,online update or hardware'))
    results=[]
    with ProcessPoolExecutor(max_workers=args.workers) as pool:
        futures=[pool.submit(job_run,cfg,job,str(out)) for job in jobs]
        for future in as_completed(futures):results.append(future.result())
    assert all(sha256(REPO/p)==h for p,h in hashes.items())
    assert sha256(Path(__file__))==json.loads((out/'manifest.json').read_text())['script_sha256']
    write(out/'completion.json',dict(execution_domain='VALIDATION_SIM',evidence_status='PASS',results=results,
        responses=sum(r['responses'] for r in results),direct_pairs=sum(r['direct_pairs'] for r in results),
        accepted=sum(r['accepted'] for r in results),planned=sum(r['planned'] for r in results),protected_files_preserved=True))


if __name__=='__main__':
    main()
