"""VALIDATION_SIM: constant-residual operating-point search, F-1 never enabled.

Fixed model_60000, synchronized sensors and original wheel/leg action paths.
Selection uses long physical responses, not an extrapolated affine equilibrium.
"""

import argparse
from concurrent.futures import ProcessPoolExecutor, as_completed
import json
from pathlib import Path

import numpy as np

from eval_flash_state_learning import StateRunner, STATE_KEYS, make_inputs
from eval_flash_pv_models import REPO, CKPT, LEGS, prepared_config, sha256, write
from eval_flash_stop_release import inputs_for

GATES = dict(settle_s=60., block_s=40., mean_speed_m_s=.0002,
    rms_speed_m_s=.0005, path_span_m=.02, planar_radius_m=.03,
    pitch_std_rad=.01, leg_margin_rad=.01)
MODEL_PATHS = {
    'moving': REPO/'docs/exp/2026-10-15/flash_state_learning/expanded/state_models_frozen.json',
    'release': REPO/'docs/exp/2026-10-15/flash_stop_release/full/conditional_models_frozen.json',
    'bias_local': REPO/'docs/exp/2026-10-15/flash_stop_local/full/models_frozen.json',
}


def metrics(trace, limits, completed, duration):
    t = np.arange(len(trace['sensor']))*.02
    after = t >= GATES['settle_s']
    tail = (t >= duration-60.) & (t < duration)
    if not np.any(after) or not np.any(tail):
        return dict(operating_gate=False, completed=completed, reason='insufficient_horizon')
    p, v = trace['gt'][:, 0], trace['gt'][:, 1]
    xy = trace['position'][:, :2]
    blocks = []
    for start in np.arange(GATES['settle_s'], duration-1e-6, GATES['block_s']):
        selected = (t >= start) & (t < min(start+GATES['block_s'], duration))
        if not np.any(selected):
            continue
        blocks.append(dict(start_s=float(start), gt_v_mean=float(v[selected].mean()),
            gt_v_rms=float(np.sqrt(np.mean(v[selected]**2))),
            sensor_v_mean=float(trace['sensor'][selected, 1].mean())))
    q = trace['leg_position'][after]
    margin = np.minimum(q-limits[:, 0], limits[:, 1]-q)
    span = float(np.ptp(p[after]))
    radius = float(np.max(np.linalg.norm(xy[after]-xy[after][0], axis=1)))
    pitch_std = float(trace['sensor'][after, 2].std())
    checks = dict(completed=bool(completed),
        block_speed=all(abs(b['gt_v_mean'])<=GATES['mean_speed_m_s'] and
            b['gt_v_rms']<=GATES['rms_speed_m_s'] for b in blocks),
        sagittal_span=span<=GATES['path_span_m'], planar_radius=radius<=GATES['planar_radius_m'],
        pitch_std=pitch_std<=GATES['pitch_std_rad'], leg_margin=float(margin.min())>=GATES['leg_margin_rad'])
    return dict(operating_gate=bool(all(checks.values())), checks=checks, completed=completed,
        blocks=blocks, gt_v_mean_last60=float(v[tail].mean()),
        gt_v_rms_last60=float(np.sqrt(np.mean(v[tail]**2))),
        sensor_v_mean_last60=float(trace['sensor'][tail, 1].mean()),
        gt_path_change=float(p[-1]-p[0]), gt_path_span_after60=span,
        gt_path_trend_after60=float(np.polyfit(t[after]-t[after][0],p[after]-p[after][0],1)[0]),
        planar_displacement=float(np.linalg.norm(xy[-1]-xy[0])),
        max_planar_drift=float(np.max(np.linalg.norm(xy-xy[0],axis=1))),
        planar_radius_after60=radius,
        planar_travel=float(np.linalg.norm(np.diff(xy,axis=0),axis=1).sum()),
        pitch_mean_last60=float(trace['sensor'][tail,2].mean()), pitch_std_after60=pitch_std,
        roll_max_after60=float(np.max(abs(trace['rpy'][after,0]))),
        yaw_change_after60=float(np.unwrap(trace['rpy'][after,2])[-1]-np.unwrap(trace['rpy'][after,2])[0]),
        leg_limit_margin_min=float(margin.min()),
        leg_position_mean_last60=trace['leg_position'][tail].mean(0).tolist(),
        leg_position_std_last60=trace['leg_position'][tail].std(0).tolist(),
        leg_velocity_rms_last60=np.sqrt(np.mean(trace['leg_velocity'][tail]**2,axis=0)).tolist(),
        action_mean_last60=trace['previous_action'][tail].mean(0).tolist(),
        action_std_last60=trace['previous_action'][tail].std(0).tolist(),
        wheel_torque_rms=float(np.sqrt(np.mean(trace['motor'][:, :, [3,7]]**2))),
        wheel_torque_peak=float(np.max(abs(trace['motor'][:, :, [3,7]]))))


def append_step(states, steps, runner, torque):
    states.append({key: runner.observation[key].copy() for key in STATE_KEYS})
    steps.append(runner.step(float(torque)))


def collect_probes(runner, snapshot, tau, out, job):
    runner.restore(snapshot)
    base, failure=runner.rollout(np.full(200,tau))
    assert not failure
    runner.restore(snapshot)
    replay, failure=runner.rollout(np.full(200,tau))
    assert not failure
    for key in base:
        np.testing.assert_array_equal(base[key],replay[key])
    np.savez_compressed(out/'probe_zero.npz',**base)
    families=['validation_sine','validation_prbs','pulse_pos','pulse_neg',
        'step_pos','step_neg','bipulse_pos','bipulse_neg']
    cases=[(f,a) for f in families for a in [.02,.05]]+[('micro_prbs',.01)]
    responses=[]
    for i,(family,amplitude) in enumerate(cases):
        seed=int(np.random.SeedSequence([job['seed'],job['pitch_index'],i,7821]).generate_state(1)[0])
        probe=inputs_for(family,amplitude,seed)
        runner.restore(snapshot)
        trace, failure=runner.rollout(tau+probe)
        assert not failure and len(trace['sensor'])==201
        assert np.max(abs(trace['actual_u']-(tau+probe)))<1e-6
        for key in STATE_KEYS:
            np.testing.assert_array_equal(trace[key][0],base[key][0])
        np.testing.assert_array_equal(trace['action'][0],base['action'][0])
        filename=f'probe_{family}_a{amplitude:g}.npz'
        np.savez_compressed(out/filename,**trace)
        responses.append(dict(trace=filename,baseline='probe_zero.npz',family=family,
            amplitude=amplitude,input_seed=seed,
            start_rl_s=job['duration']+(30. if job['approach']=='high' else 8.),constant_bias=tau))
    direct=[]
    from analyze_flash_state_learning import state
    for amplitude in [.005,.01,.02]:
        runner.restore(snapshot); plus,pf=runner.rollout([tau+amplitude])
        runner.restore(snapshot); minus,mf=runner.rollout([tau-amplitude])
        assert not pf and not mf
        np.testing.assert_array_equal(plus['action'][0],base['action'][0])
        np.testing.assert_array_equal(minus['action'][0],base['action'][0])
        denominator=plus['actual_u'][0]-minus['actual_u'][0]
        b=(state(plus)[1]-state(minus)[1])/denominator
        np.testing.assert_array_equal(b[4:12],np.zeros(8))
        direct.append(dict(amplitude=amplitude,sensor_B=b.tolist(),
            gt_B=((plus['gt'][1]-minus['gt'][1])/denominator).tolist()))
    return responses,direct


def job_run(cfg,job,root):
    out=Path(root)/job['id']
    out.mkdir()
    runner=StateRunner(cfg,job)
    try:
        startup=[]
        prefix_tau=0.
        prefix_s=30. if job['approach']=='high' else 8.
        for tick in range(round(prefix_s/.02)):
            if tick<50 and runner.failures():
                startup.append(dict(rl_s=tick*.02,failures=runner.failures()))
            elif tick>=50:
                assert not runner.failures(),(job,tick,runner.failures())
            prefix_tau=min(.6,prefix_tau+.04) if job['approach']=='high' else 0.
            runner.step(prefix_tau)
        initial_snapshot=runner.snapshot()
        states,steps=[],[]
        failure=[]
        tau=prefix_tau
        for tick in range(round(job['duration']/.02)+1):
            failure=runner.failures()
            if failure or tick==round(job['duration']/.02):
                states.append({key:runner.observation[key].copy() for key in STATE_KEYS})
                break
            tau=float(np.clip(job['tau'],tau-.04,tau+.04))
            append_step(states,steps,runner,tau)
        trace={k:np.asarray([r[k] for r in states]) for k in STATE_KEYS}
        trace.update({k:np.asarray([r[k] for r in steps]) for k in steps[0]})
        np.testing.assert_array_equal(trace['previous_action'][:-1],trace['history'])
        np.testing.assert_array_equal(trace['previous_action'][1:],trace['action'])
        assert max(abs(trace['actual_u']-trace['requested_u']))<1e-6
        np.savez_compressed(out/'hold.npz',**trace)
        limits=runner.env.model.jnt_range[runner.leg_joints]
        stats=metrics(trace,limits,not failure,len(steps)*.02)
        result=dict(execution_domain='VALIDATION_SIM',evidence_status='PASS' if not failure else 'FAIL',
            job=job,metrics=stats,failures=failure,startup_violations=startup,responses=[],direct_B=[],
            F1_enabled=False,leg_path='unchanged ActionAdapter asserted every substep',
            actor='fixed synchronized model_60000, raw previous_action',disabled_obstacles=runner.disabled_obstacles)
        qualifying=stats['operating_gate']
        if job.get('terminal_start_s') is not None:
            cut=round((job['terminal_start_s']-GATES['settle_s'])/.02)
            terminal={key:value[cut:] for key,value in trace.items()}
            terminal_stats=metrics(terminal,limits,not failure,len(steps)*.02-cut*.02)
            result['terminal_metrics']=terminal_stats
            qualifying=terminal_stats['operating_gate']
        if job['probe'] and qualifying:
            snapshot=runner.snapshot()
            result['responses'],result['direct_B']=collect_probes(runner,snapshot,job['tau'],out,job)
        # Prefix-end snapshots are held in memory only; all prefixes are reproducible.
        assert initial_snapshot is not None
        write(out/'results.json',result)
        print('[VALIDATION_SIM]',job['id'],'v_last60',stats.get('gt_v_mean_last60'),
            'gate',stats['operating_gate'],'probes',len(result['responses']),flush=True)
        return dict(id=job['id'],tau=job['tau'],metrics=stats,responses=len(result['responses']),
            direct_pairs=len(result['direct_B']))
    finally:
        runner.env.close()


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--stage',choices=['scan','fine','confirm'],required=True)
    parser.add_argument('--selection',type=Path)
    parser.add_argument('--workers',type=int,default=3)
    args=parser.parse_args()
    out=args.output.resolve()
    if not out.is_relative_to(REPO/'docs/exp') or out.exists():
        parser.error('New evidence directory under docs/exp required')
    out.mkdir(parents=True)
    selection=json.loads(args.selection.read_text()) if args.selection else None
    if args.stage=='scan':
        cases=[(seed,1,0.,tau,'zero') for seed in [150,151] for tau in [0.,.48,.50,.52,.54,.56,.60]]
    elif args.stage=='fine':
        assert selection is not None
        center=selection['selected_tau']
        cases=[(152,1,0.,round(center+delta,6),'zero') for delta in np.arange(-.01,.01001,.0025)]
    else:
        assert selection is not None
        tau=selection['selected_tau']
        cases=[(s,pi,p,tau,'zero') for s in [160,161,162] for pi,p in enumerate([-.035,0.,.035])]
        cases += [(s,1,0.,tau,'high') for s in [160,161,162]]
    jobs=[]
    for seed,pi,pitch,tau,approach in cases:
        jobs.append(dict(id=f's{seed}_p{pitch:+.3f}_r{tau:.6f}_{approach}',seed=seed,pitch_index=pi,
            pitch=pitch,tau=tau,approach=approach,duration=300. if args.stage=='confirm' else 180.,
            probe=bool(args.stage=='confirm' and selection['qualified'] and approach=='zero' and seed in [160,161])))
    config=prepared_config(CKPT)
    cfg=json.loads(config.read_text())
    protected=list((REPO/'sim2sim/sim2sim_ros2_jazzy').rglob('*.py'))
    protected += [REPO/'sim2sim/lqr'/f for f in ['runtime.py','model.py','estimator.py']]
    protected += [REPO/'test'/f for f in ['eval_flash_pv_models.py','eval_flash_state_learning.py',
        'analyze_flash_state_learning.py','eval_flash_stop_release.py']]
    protected += list(MODEL_PATHS.values())+[config,config.parent/'policy.onnx',CKPT/'actor.pt']
    hashes={str(p.relative_to(REPO)):sha256(p) for p in protected}
    write(out/'manifest.json',dict(execution_domain='VALIDATION_SIM',evidence_status='NOT_TESTED',
        checkpoint_sha256=sha256(CKPT/'actor.pt'),onnx_sha256=sha256(config.parent/'policy.onnx'),
        script_sha256=sha256(Path(__file__)),protected_sha256=hashes,stage=args.stage,jobs=jobs,
        gates=GATES,gate_note='Finite-horizon diagnostic, not proof of infinite-time boundedness or physical equilibrium',
        selection=selection,selection_sha256=sha256(args.selection) if args.selection else None,
        fixed_policy=True,F1_enabled=False,commands=[0.,0.,0.],
        torque='total constant residual after2Nm/s transition; original FlashSAC wheel torque retained',
        simulation='flat nominal, obstacles disabled in memory, synchronized sensors, no pushes',
        selection_rule='minimum absolute final60s GT mean among all operational-gate passing fine torques; no confirmation retuning',
        probing='only qualifying confirmation cases, same selected constant bias in both branches; +/-0.02/0.05Nm probes',
        models='frozen prior M2/M4 only, no refit/affine/LQR/online learning'))
    results=[]
    with ProcessPoolExecutor(max_workers=args.workers) as pool:
        futures=[pool.submit(job_run,cfg,job,str(out)) for job in jobs]
        for future in as_completed(futures):
            results.append(future.result())
    assert all(sha256(REPO/p)==h for p,h in hashes.items())
    write(out/'completion.json',dict(execution_domain='VALIDATION_SIM',evidence_status='PASS',
        results=results,protected_files_preserved=True))


if __name__=='__main__':
    main()
