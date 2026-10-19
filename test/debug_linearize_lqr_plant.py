"""VALIDATION_SIM: finite differences of the actual 20-ms leg-PD/contact plant.

The 28-state tangent dynamics include flexible legs. A projected 4-state model
uses an explicit rolling-contact lift and is not assumed to be a Markov model.
Nothing here changes the nominal or deployed controller.
"""

import argparse
import json
from pathlib import Path
import sys

import numpy as np
from scipy.optimize import least_squares
from scipy.spatial.transform import Rotation

REPO=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(REPO/'test'))
from debug_lqr_d4_diagnostics import (Plant,policy_config,ARCHIVE,Description,read_yaml,
    LEGS,WHEELS,write_json,residual_matrices,WheelLQR,sha256)


def contacts(plant,data):
    return sorted(set((int(c.geom1),int(c.geom2),int(c.dim)) for c in data.contact))


def control(plant,data,u):
    q=data.qpos[plant.env.qpos_addr].astype(np.float32)
    dq=data.qvel[plant.env.qvel_addr].astype(np.float32)
    torque=np.zeros(8,dtype=np.float32)
    torque[LEGS]=plant.cfg['fixed_leg_kp']*(plant.stand[LEGS]-q[LEGS])-plant.cfg['fixed_leg_kd']*dq[LEGS]
    torque[WHEELS]=plant.signs*u/2
    data.ctrl[plant.env.actuator_ids]=np.clip(torque,-plant.playback.adapter.limit,plant.playback.adapter.limit)


def equilibrium(plant):
    env=plant.env
    qref=env.data.qpos.copy()
    # Start with the observed loaded-pose neighborhood; optimize true force balance.
    initial=np.r_[qref[2]-.002,plant.parameters['equilibrium_roll'],-.0215,plant.stand[LEGS]]
    initial[3:][[2,5]]-=[.044,.040]
    loaded=plant.stand.copy();loaded[LEGS]=initial[3:]
    frames,axes=plant.description.frames(loaded)
    rotation=Rotation.from_euler('xyz',[initial[1],initial[2],0.])
    bottoms=[]
    for name,joint in zip(plant.description.wheel_links,('joint_left_leg_4','joint_right_leg_4')):
        axis=rotation.apply(axes[joint])
        half_width=float(plant.description.links[name].find('collision/geometry/cylinder').get('length'))/2
        extent=plant.description.radius*np.sqrt(1-axis[2]**2)+half_width*abs(axis[2])
        bottoms.append(rotation.apply(frames[name][:3,3])[2]-extent)
    initial[0]=-min(bottoms)-.0002
    def assign(z):
        env.data.qpos[:]=qref
        env.data.qpos[2]=z[0]
        env.data.qpos[3:7]=Rotation.from_euler('xyz',[z[1],z[2],0.]).as_quat()[[3,0,1,2]]
        env.data.qpos[env.qpos_addr[LEGS]]=z[3:]
        env.data.qvel[:]=0.
        env.data.qacc_warmstart[:]=0.
        env.data.xfrc_applied[:]=0.
        control(plant,env.data,0.)
        env.mujoco.mj_forward(env.model,env.data)
    def objective(z):
        assign(z)
        return env.data.qacc.copy()
    lower=np.r_[.28,-.2,-.2,plant.stand[LEGS]-.15]
    upper=np.r_[.45,.2,.2,plant.stand[LEGS]+.15]
    solved=least_squares(objective,initial,bounds=(lower,upper),jac='3-point',diff_step=1e-5,
        xtol=1e-12,ftol=1e-12,gtol=1e-10,max_nfev=300)
    assign(solved.x)
    snapshot=env.mujoco.MjData(env.model)
    env.mujoco.mj_copyData(snapshot,env.model,env.data)
    return snapshot,dict(success=bool(solved.success),message=solved.message,evaluations=solved.nfev,
        max_abs_qacc=float(np.max(abs(snapshot.qacc))),qacc=snapshot.qacc.tolist(),
        qpos=snapshot.qpos.tolist(),joint_pd_torque=snapshot.ctrl.tolist(),contacts=contacts(plant,snapshot))


def clone(plant,data):
    result=plant.env.mujoco.MjData(plant.env.model)
    plant.env.mujoco.mj_copyData(result,plant.env.model,data)
    return result


def observation(plant,data):
    plant.env.mujoco.mj_forward(plant.env.model,data)
    pos,vel,rpy,omega,forward=plant.instant(data)
    return np.array([pos @ forward,vel @ forward,rpy[1],omega])


def lift(plant,reference,state):
    data=clone(plant,reference)
    env=plant.env
    pos,_,rpy,_,forward=plant.instant(data)
    rotation=Rotation.from_quat(data.qpos[3:7][[1,2,3,0]])
    axle_base=rotation.inv().apply(pos-data.qpos[:3])
    changed=Rotation.from_euler('xyz',[rpy[0],rpy[1]+state[2],rpy[2]])
    data.qpos[3:7]=changed.as_quat()[[3,0,1,2]]
    data.qpos[:3]+=state[0]*forward+rotation.apply(axle_base)-changed.apply(axle_base)
    lateral=np.array([-np.sin(rpy[2]),np.cos(rpy[2]),0.])
    world_rate=lateral*state[3]
    data.qvel[:3]+=forward*state[1]-np.cross(world_rate,changed.apply(axle_base))
    data.qvel[3:6]+=changed.inv().apply(world_rate)
    _,axes=plant.description.frames(data.qpos[env.qpos_addr])
    for side,index in zip(('left','right'),WHEELS):
        projection=lateral @ changed.apply(axes[f'joint_{side}_leg_4'])
        data.qvel[env.qvel_addr[index]]+=(state[1]/plant.description.radius-state[3])/projection
    env.mujoco.mj_forward(env.model,data)
    return data


def transition(plant,data,u):
    result=clone(plant,data)
    signatures=[]
    for _ in range(plant.env.decimation):
        control(plant,result,u)
        plant.env.mujoco.mj_step(plant.env.model,result)
        signatures.append(contacts(plant,result))
    plant.env.mujoco.mj_forward(plant.env.model,result)
    return result,signatures


def difference(plant,minus,plus,step):
    tangent=np.zeros(plant.env.model.nv)
    plant.env.mujoco.mj_differentiatePos(plant.env.model,tangent,2*step,minus.qpos,plus.qpos)
    return np.r_[tangent,(plus.qvel-minus.qvel)/(2*step)]


def derivatives(plant,reference,eps):
    env=plant.env
    n=2*env.model.nv
    F=np.empty((n,n)); H=np.empty((4,n)); E=np.empty((n,4))
    signature_changes=0
    base_next,base_signatures=transition(plant,reference,0.)
    for i in range(n):
        states=[]; outputs=[]
        for sign in (-1,1):
            data=clone(plant,reference)
            if i<env.model.nv:
                direction=np.zeros(env.model.nv);direction[i]=1.
                env.mujoco.mj_integratePos(env.model,data.qpos,direction,sign*eps)
            else:
                data.qvel[i-env.model.nv]+=sign*eps
            outputs.append(observation(plant,data))
            following,signature=transition(plant,data,0.)
            states.append(following)
            signature_changes+=int(signature!=base_signatures)
        F[:,i]=difference(plant,states[0],states[1],eps)
        H[:,i]=(outputs[1]-outputs[0])/(2*eps)
    minus,signature_minus=transition(plant,reference,-eps)
    plus,signature_plus=transition(plant,reference,eps)
    G=difference(plant,minus,plus,eps).reshape(n,1)
    for i in range(4):
        delta=np.zeros(4);delta[i]=eps
        E[:,i]=difference(plant,lift(plant,reference,-delta),lift(plant,reference,delta),eps)
    A4,B4=H @ F @ E,H @ G
    return dict(F=F,G=G,H=H,E=E,A_true_projected=A4,B_true_projected=B4,
        lift_identity_error=float(np.max(abs(H @ E-np.eye(4)))),contact_branch_changes=signature_changes,
        input_contact_branch_changes=int(signature_minus!=base_signatures)+int(signature_plus!=base_signatures),
        equilibrium_step_drift=float(np.linalg.norm(difference(plant,reference,base_next,.5))),
        closure_error=float(np.linalg.norm(H @ F-A4 @ H)))


def spectrum(matrix):
    values=np.linalg.eigvals(matrix)
    return dict(spectral_radius=float(max(abs(values))),
        unstable_modes=int(np.sum(abs(values)>1.0001)),
        near_unit_modes=int(np.sum(abs(abs(values)-1)<.0001)),
        eigenvalues_real=values.real.tolist(),eigenvalues_imag=values.imag.tolist())


def validate_local_prediction(plant,reference,local,nominal,training):
    baseline,_=transition(plant,reference,0.)
    baseline_output=observation(plant,baseline)
    input_sweep=[]
    for amplitude in (.001,.01,.05):
        minus,cm=transition(plant,reference,-amplitude)
        plus,cp=transition(plant,reference,amplitude)
        B=((observation(plant,plus)-observation(plant,minus))/(2*amplitude)).reshape(4,1)
        input_sweep.append(dict(amplitude_nm=amplitude,B=B.tolist(),contacts_minus=cm,contacts_plus=cp))
    B_reference=np.array(input_sweep[1]['B'])
    rng=np.random.default_rng(731)
    errors={name:[] for name in ('local','nominal','adapted')}
    dA,dB=residual_matrices(training['final_diagnostics']['coefficients'],.02,4)
    for _ in range(50):
        perturbation=rng.uniform(-1,1,4)*[1e-4,1e-3,1e-4,1e-3]
        torque=float(rng.uniform(-.01,.01))
        perturbed=lift(plant,reference,perturbation)
        following,_=transition(plant,perturbed,torque)
        actual=observation(plant,following)-baseline_output
        predictions=dict(local=local['A_true_projected'] @ perturbation+B_reference[:,0]*torque,
            nominal=nominal.A0 @ perturbation+nominal.B0[:,0]*torque,
            adapted=(nominal.A0+dA) @ perturbation+(nominal.B0+dB)[:,0]*torque)
        for name,predicted in predictions.items():
            errors[name].append(actual-predicted)
    return dict(input_sweep=input_sweep,
        heldout_component_rms={name:np.sqrt(np.mean(np.asarray(error)**2,axis=0)).tolist() for name,error in errors.items()},
        samples=50,seed=731,description='Centered output changes over one 20-ms step; fixed leg PD and contact; '
        'small perturbations lifted with no-slip wheel velocities; local B uses independent 0.01-Nm finite difference.')


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    output=args.output.resolve()
    if not output.is_relative_to(REPO/'docs/exp') or output.exists():
        parser.error('New output directory under docs/exp/ required')
    output.mkdir(parents=True)
    cfg=json.loads((ARCHIVE/'config.json').read_text())
    manifest=json.loads((ARCHIVE/'manifest.json').read_text())
    policy=policy_config()
    source=read_yaml(next(p for p in policy['policy_interface']['sources'] if p.endswith('env.yaml')))
    description=Description(source['scene']['robot']['spawn']['asset_path'])
    plant=Plant(policy,cfg,description,manifest['nominal_parameters'],{'name':'nominal'},42,0.)
    try:
        reference,eq=equilibrium(plant)
        write_json(output/'equilibrium.json',eq)
        if not eq['contacts'] or eq['max_abs_qacc']>.1:
            print('[VALIDATION_SIM] BLOCKED: force-balanced contact equilibrium unavailable',eq,flush=True)
            return
        nominal=WheelLQR(manifest['nominal_parameters'],.02,4,cfg['controller'])
        results=[]
        archive=[json.loads(line) for line in (ARCHIVE/'results.jsonl').read_text().splitlines()]
        training=[r for r in archive if r['mode']=='D-4' and r['mismatch']=='nominal' and r['phase']=='adaptation']
        for eps in (1e-5,5e-5,1e-4):
            local=derivatives(plant,reference,eps)
            arrays={k:v for k,v in local.items() if isinstance(v,np.ndarray)}
            np.savez_compressed(output/f'linearization_{eps}.npz',**arrays,A0=nominal.A0,B0=nominal.B0,K0=nominal.K0)
            comparisons=[]
            for trial in training:
                coefficients=np.array(trial['final_diagnostics']['coefficients'])
                dA,dB=residual_matrices(coefficients,.02,4)
                Ahat,Bhat=nominal.A0+dA,nominal.B0+dB
                K=np.array(trial['final_diagnostics']['K'])
                with np.load(ARCHIVE/trial['trace']) as trace:
                    changes=np.flatnonzero(np.diff(trace['updates'][:,0])>0)+1
                    accepted_coefficients=trace['coefficients'][changes[-1]] if len(changes) else np.zeros(4)
                    accepted_time=float(trace['time'][changes[-1]]) if len(changes) else 0.
                gain_dA,gain_dB=residual_matrices(accepted_coefficients,.02,4)
                gain_A,gain_B=nominal.A0+gain_dA,nominal.B0+gain_dB
                comparisons.append(dict(seed=trial['seed'],pitch=trial['pitch_delta_rad'],K=K.tolist(),
                    Ahat=Ahat.tolist(),Bhat=Bhat.tolist(),
                    gain_model_time_s=accepted_time,gain_model_coefficients=accepted_coefficients.tolist(),
                    Ahat_at_gain=gain_A.tolist(),Bhat_at_gain=gain_B.tolist(),
                    A0_error=float(np.linalg.norm(local['A_true_projected']-nominal.A0)),
                    Ahat_error=float(np.linalg.norm(local['A_true_projected']-Ahat)),
                    B0_error=float(np.linalg.norm(local['B_true_projected']-nominal.B0)),
                    Bhat_error=float(np.linalg.norm(local['B_true_projected']-Bhat)),
                    estimated_closed_loop=spectrum(Ahat-Bhat @ K.reshape(1,4)),
                    estimated_closed_loop_at_gain=spectrum(gain_A-gain_B @ K.reshape(1,4)),
                    projected_closed_loop=spectrum(local['A_true_projected']-local['B_true_projected'] @ K.reshape(1,4)),
                    full_plant_closed_loop=spectrum(local['F']-local['G'] @ K.reshape(1,4) @ local['H'])))
            entry=dict(epsilon=eps,**{k:v for k,v in local.items() if not isinstance(v,np.ndarray)},
                A_true_projected=local['A_true_projected'].tolist(),B_true_projected=local['B_true_projected'].tolist(),
                K0_projected_closed_loop=spectrum(local['A_true_projected']-local['B_true_projected'] @ nominal.K0.reshape(1,4)),
                K0_full_plant_closed_loop=spectrum(local['F']-local['G'] @ nominal.K0.reshape(1,4) @ local['H']),
                comparisons=comparisons)
            results.append(entry)
            print('[VALIDATION_SIM]',eps,'eq qacc',eq['max_abs_qacc'],'lift error',local['lift_identity_error'],
                  'contact changes',local['contact_branch_changes'],'closure',local['closure_error'],flush=True)
        representative=next(r for r in training if r['seed']==42 and r['pitch_delta_rad']==0.)
        validation=validate_local_prediction(plant,reference,local,nominal,representative)
        write_json(output/'prediction_validation.json',validation)
        write_json(output/'results.json',dict(execution_domain='VALIDATION_SIM',evidence_status='SUSPICIOUS',
            checkpoint_sha256=manifest['checkpoint_sha256'],script_sha256=sha256(Path(__file__)),
            timestep_s=.02,full_tangent_state_dimension=2*plant.env.model.nv,equilibrium=eq,results=results,
            interpretation='Finite differences of leg PD plus contact at the same force-balanced state. '
            'The reported force-balance residual is nonzero: this is a near-static operating point, not an exact equilibrium. '
            '4-state projection uses explicit wheel-axle pitch pivot and no-slip velocity lift. '
            'Hidden leg/roll/yaw states remain in F; a nonzero closure error means no unique autonomous 4-state A_true. '
            'Ahat learned during a moving/biased closed loop is compared locally, not assumed globally valid.'))
    finally:
        plant.env.close()


if __name__=='__main__':
    main()
