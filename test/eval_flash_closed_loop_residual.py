"""VALIDATION_SIM: offline local identification of frozen FlashSAC + wheel PD.

Pairs of actual policy rollouts identify response to small additive total wheel
torques. No stand-alone WIP matrices, C-4 gain or online RLS are used here.
The four observed states omit legs/history and describe a local approximation.
"""

import argparse
import json
from pathlib import Path
import sys
import time

import numpy as np
from scipy.linalg import solve_discrete_are

sys.path.insert(0,str(Path(__file__).resolve().parent))
from eval_flash_torque_residual import (REPO, ARCHIVE, DEFAULT_RESIDUAL, run, policy_config,
    read_yaml, Description, write_json, sha256, WHEELS)

BASE = REPO/'docs/exp/2026-10-15/flash_torque_residual/f1_nominal'
FREQUENCIES = np.array([.37,1.1,2.7,5.3])
PHASES = np.array([0.,.4,1.2,2.3])
Q = np.diag([4.,1.,.2,.05])
R = np.array([[4.]])


class Probe:
    def __init__(self, config, alpha, p_hold):
        self.config, self.amplitude = dict(config), alpha
        self.previous = 0.

    def command(self, state, t, dt):
        fraction=np.clip((t-1.)/1.,0.,1.)
        ramp=float(fraction*fraction*(3.-2.*fraction))
        raw=float(self.amplitude*np.mean(np.sin(2*np.pi*FREQUENCIES*(t-1.)+PHASES)))
        target=raw*ramp
        step=self.config['slew_total_nm_s']*dt
        self.previous=float(np.clip(target,self.previous-step,self.previous+step))
        return self.previous, raw, ramp


class ClosedLoopResidual:
    def __init__(self, config, alpha, p_hold):
        self.config, self.alpha, self.p_hold = dict(config), float(alpha), float(p_hold)
        self.previous=0.

    def command(self, state, t, dt):
        error=state-np.array([self.p_hold,0.,self.config['pitch_reference_error_rad'],0.])
        raw=float(-np.asarray(self.config['K']) @ error)
        fraction=np.clip(t/self.config['ramp_s'],0.,1.)
        ramp=float(fraction*fraction*(3.-2.*fraction))
        target=self.alpha*ramp*np.clip(raw,-self.config['limit_total_nm'],self.config['limit_total_nm'])
        step=self.config['slew_total_nm_s']*dt
        self.previous=float(np.clip(target,self.previous-step,self.previous+step))
        return self.previous, raw, ramp


def samples(result, output):
    baseline=next(r for r in map(json.loads,(BASE/'results.jsonl').read_text().splitlines())
                  if r['label']=='A' and r['seed']==result['seed'] and r['pitch_delta_rad']==result['pitch_delta_rad'])
    with np.load(output/result['trace']) as probed, np.load(BASE/baseline['trace']) as original:
        assert not result['failures'] and result['completed_s']==12.
        np.testing.assert_array_equal(result['initial_physics'],baseline['initial_physics'])
        delta=probed['synchronized_state']-original['synchronized_state']
        # Row t+1 logs substep torques applied during transition t -> t+1.
        actual_native=(probed['command_substeps'][1:,:,WHEELS]-probed['flash_substeps'][1:,:,WHEELS])
        # Signs are +,+ for this designated model, independently verified below.
        u=actual_native.sum(2).mean(1)
        t=probed['time'][:-1]
        mask=(t>=2.) & (t<10.5) & ~((t>=2.96)&(t<=3.3))
        return delta[:-1][mask],delta[1:][mask],u[mask]


def fit_model(x,y,u):
    # Position translation does not alter actor inputs/PD; enforce this symmetry.
    # Identify all velocity, pitch and rate couplings plus the residual input.
    scale=np.array([.1,.02,.2,.25])
    z=np.column_stack([x[:,1:],u])/scale
    target=y.copy()
    target[:,0]-=x[:,0]
    coefficients,_,rank,singular=np.linalg.lstsq(z,target,rcond=1e-8)
    if rank<4:
        raise RuntimeError('Insufficient excitation for four independent regressors')
    unscaled=(coefficients/scale[:,None]).T
    A=np.zeros((4,4));A[0,0]=1.;A[:,1:]=unscaled[:,:3]
    B=unscaled[:,3:]
    return A,B,dict(rank=int(rank),singular_values=singular.tolist(),scaled_condition_number=float(singular[0]/singular[-1]),
        samples=len(x),position_translation_symmetry=True,regressor_scales=scale.tolist())


def score(A,B,x,y,u):
    prediction=x @ A.T+u[:,None] @ B.T
    errors=prediction-y
    changes=y-x
    rms=lambda v:np.sqrt(np.mean(v*v,axis=0))
    return dict(component_rms=rms(errors).tolist(),component_change_rms=rms(changes).tolist(),
        relative_to_change_rms=(rms(errors)/np.maximum(rms(changes),1e-12)).tolist(),samples=len(x))


def main():
    global BASE
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--baseline',type=Path,default=BASE)
    args=parser.parse_args()
    BASE=args.baseline.resolve()
    if not BASE.is_relative_to(REPO/'docs/exp') or not (BASE/'results.jsonl').is_file():
        parser.error('Existing A/F-1 baseline evidence under docs/exp/ required')
    output=args.output.resolve()
    if not output.is_relative_to(REPO/'docs/exp') or output.exists():
        parser.error('New evidence directory under docs/exp/ required')
    output.mkdir(parents=True)
    cfg=json.loads((ARCHIVE/'config.json').read_text())
    parameters=json.loads((ARCHIVE/'manifest.json').read_text())['nominal_parameters']
    policy=policy_config()
    source=read_yaml(next(p for p in policy['policy_interface']['sources'] if p.endswith('env.yaml')))
    description=Description(source['scene']['robot']['spawn']['asset_path'])
    # Explicit wheel axis audit: identification input is physical sagittal torque.
    _,axes=description.frames(policy['robot']['default_joint_angles'])
    signs=np.sign([axes[f'joint_{side}_leg_4'][1] for side in ('left','right')])
    np.testing.assert_array_equal(signs,[1.,1.])
    baseline_rows=list(map(json.loads,(BASE/'results.jsonl').read_text().splitlines()))
    # F-2 gate is paired across all nine initial conditions, before identifying K.
    f1=[r for r in baseline_rows if r['label']=='F-1_a1']
    a=[r for r in baseline_rows if r['label']=='A']
    a_lookup={(r['seed'],r['pitch_delta_rad']):r for r in a}
    assert len(f1)==9 and all(not r['failures'] for r in f1)
    for r in f1:
        original=a_lookup[(r['seed'],r['pitch_delta_rad'])]
        assert r['max_displacement_m']<original['max_displacement_m']
        assert r['pitch_rms_rad']<=original['pitch_rms_rad']*1.10
        assert r['torque_rms_nm']<=original['torque_rms_nm']*1.25
    manifest=dict(execution_domain='VALIDATION_SIM',evidence_status='NOT_TESTED',
        checkpoint_sha256=policy['policy_interface']['checkpoint_sha256'],onnx_sha256=policy['policy_interface']['onnx_sha256'],
        cfg=cfg,script_sha256=sha256(Path(__file__)),runner_sha256=sha256(REPO/'test/eval_flash_torque_residual.py'),
        F1_gate='9/9 complete; every paired drift smaller; pitch RMS <=110%; wheel RMS <=125%',
        Q=Q.tolist(),R=R.tolist(),frequencies_hz=FREQUENCIES.tolist(),amplitudes_total_nm=[.1,.25,.5],
        state='synchronized [encoder path, velocity, pitch error, pitch rate]',
        identification='paired perturbed minus matched A rollout; offline least squares; original full actor and PD',
        heldout_seed=44,train_seeds=[42,43],online_adaptation=False,baseline=str(BASE),
        limits='4-state local model omits leg/roll/yaw/action history; A is a moving operating trajectory')
    write_json(output/'manifest.json',manifest)
    started=time.monotonic()
    training=[];heldout=[];probe_results=[]
    for seed in cfg['seeds']:
        for pitch in cfg['pitch_disturbances_rad']:
            for amplitude in (.1,.25,.5):
                label=f'probe_{amplitude:g}'
                result=run(policy,cfg,description,parameters,seed,pitch,label,'synchronized',output,
                    alpha=amplitude,residual_factory=Probe)
                probe_results.append(result)
                with (output/'probe_results.jsonl').open('a') as stream:
                    stream.write(json.dumps(result,allow_nan=False)+'\n')
                print(f'[VALIDATION_SIM] probe {amplitude} s{seed} p{pitch:+.3f} '
                      f'{result["evidence_status"]} elapsed={time.monotonic()-started:.1f}s',flush=True)
                sample=samples(result,output)
                (heldout if seed==44 else training).append(sample)
    merge=lambda rows:tuple(np.concatenate([r[i] for r in rows]) for i in range(3))
    x,y,u=merge(training)
    hx,hy,hu=merge(heldout)
    A,B,diagnostics=fit_model(x,y,u)
    P=solve_discrete_are(A,B,Q,R)
    K=np.linalg.solve(R+B.T @ P @ B,B.T @ P @ A).reshape(4)
    eigenvalues=np.linalg.eigvals(A-B @ K.reshape(1,4))
    assert np.isfinite(K).all() and max(abs(eigenvalues))<1.
    pitch_reference=[]
    for result in a:
        if result['seed']==44:
            continue
        with np.load(BASE/result['trace']) as trace:
            pitch_reference.extend(trace['synchronized_state'][trace['time']>=4.,2])
    reference=float(np.mean(pitch_reference))
    config=dict(DEFAULT_RESIDUAL,K=K.tolist(),pitch_reference_error_rad=reference)
    validation=score(A,B,hx,hy,hu)
    model=dict(execution_domain='VALIDATION_SIM',evidence_status='SUSPICIOUS',A_closed=A.tolist(),B_res=B.tolist(),
        K=K.tolist(),Q=Q.tolist(),R=R.tolist(),diagnostics=diagnostics,
        training_prediction=score(A,B,x,y,u),heldout_prediction=validation,
        closed_model_spectral_radius=float(max(abs(eigenvalues))),pitch_reference_error_rad=reference,
        pitch_reference_standard_deviation_rad=float(np.std(pitch_reference)),
        residual_config=config,interpretation='Identified 4-state projection of frozen FlashSAC+wheel PD, '
        'including actual action history/sensor timing in collected rollouts, but hidden states omitted from regression. '
        'Estimated spectral stability does not establish actual simulator stability.')
    write_json(output/'model.json',model)
    np.savez_compressed(output/'identification.npz',x=x,y=y,u=u,heldout_x=hx,heldout_y=hy,heldout_u=hu,A_closed=A,B_res=B,K=K)
    print('[VALIDATION_SIM] identified K',K,'rho',max(abs(eigenvalues)),
          'heldout relative prediction errors',validation['relative_to_change_rms'],flush=True)
    for seed in cfg['seeds']:
        for pitch in cfg['pitch_disturbances_rad']:
            for alpha in (0.,.25,.5,1.):
                label=f'F-2_a{alpha:g}'
                result=run(policy,cfg,description,parameters,seed,pitch,label,'synchronized',output,
                    alpha=alpha,residual_config=config,residual_factory=ClosedLoopResidual)
                original=a_lookup[(seed,pitch)]
                np.testing.assert_array_equal(result['initial_physics'],original['initial_physics'])
                if alpha==0.:
                    with np.load(output/result['trace']) as current,np.load(BASE/original['trace']) as baseline:
                        errors={key:float(abs(current[key]-baseline[key]).max()) for key in
                            ('state','sensor_state','gt_position','motor_substeps','policy_action','policy_observation')}
                        assert max(errors.values())==0.,errors
                    result['alpha_zero_replay_errors']=errors
                with (output/'results.jsonl').open('a') as stream:
                    stream.write(json.dumps(result,allow_nan=False)+'\n')
                print(f'[VALIDATION_SIM] {label} s{seed} p{pitch:+.3f}: {result["evidence_status"]} '
                      f'drift={result["max_displacement_m"]:.4f} pitchRMS={result["pitch_rms_rad"]:.4f} '
                      f'wheelRMS={result["torque_rms_nm"]:.4f} elapsed={time.monotonic()-started:.1f}s',flush=True)
    write_json(output/'completion.json',dict(execution_domain='VALIDATION_SIM',evidence_status='PASS',
        probe_episodes=len(probe_results),evaluation_episodes=36,elapsed_s=time.monotonic()-started))


if __name__=='__main__':
    main()
