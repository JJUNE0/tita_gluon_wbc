"""VALIDATION_SIM: isolate residual, command slew and actor IMU timing; no GUI edits."""

import argparse
import json
from pathlib import Path
import sys

import numpy as np
from scipy.signal import periodogram

sys.path.insert(0,str(Path(__file__).resolve().parent))
from play_flash_velocity_hold import (REPO,ARCHIVE,Plant,StopHold,Sensors,Description,
    policy_config,read_yaml,write_json,sha256,LEGS,WHEELS,additive_torque)
from sim2sim_ros2_jazzy.adapter import ObsState,quat_wxyz_to_rotmat


def run_case(case,seed,output,policy,cfg,description,parameters):
    plant=Plant(policy,cfg,description,parameters,{'name':'nominal'},seed,0.)
    env=plant.env;playback=plant.playback
    hold=StopHold(description,parameters['equilibrium_pitch'],enabled=case=='step_hold')
    command=np.zeros(3,dtype=np.float32);rows=[];motor=np.zeros((4,8));action=np.zeros(8);targets=np.zeros(8)
    residual=0.;initial=np.r_[env.data.qpos,env.data.qvel].copy();failure=[]
    try:
        for tick in range(2101):
            t=tick*.02
            target=.2 if 2.<=t<14. else (-.2 if 22.<=t<34. else 0.)
            if case.startswith('ramp'):
                command[0]+=np.clip(target-command[0],-.5*.02,.5*.02)
            else:command[0]=target
            observation=plant.observe();data=plant.truth_data
            failure,_=plant.failures(observation,'synchronized')
            packet=Sensors(env.joint_pos(),env.joint_vel(),data.sensor('trunk_quat').data.copy(),data.sensor('trunk_gyro').data.copy())
            residual,diag=hold.step(command,packet,.02)
            rows.append(dict(time=t,command=command.copy(),pitch=observation['rpy'][1],
                pitch_rate=observation['gt'][3],velocity=observation['gt'][1],position=observation['position'].copy(),
                joint_velocity=env.joint_vel(),action=action.copy(),targets=targets.copy(),
                motor_substeps=motor.copy(),residual_total_nm=residual,mode=diag['mode']))
            if failure or tick==2100:break
            if case=='ramp_sync':
                quat=packet.imu_quaternion.astype(np.float32)
                state=ObsState(env.joint_pos(),env.joint_vel(),quat,packet.imu_gyro.astype(np.float32),
                    command.copy(),playback.last_action,quat_wxyz_to_rotmat(quat).T @ env.base_lin_vel())
                obs=playback.builder.build(state)
                action=playback.policy.run(['nn_output'],{'nn_input0':obs.reshape(1,-1)})[0].reshape(8)
            else:_,action=playback.infer(command.copy())
            targets=playback.adapter.targets(action)
            _,motor=playback.step(action,lambda q,dq,tau:additive_torque(tau,residual,plant.signs))
        trace={k:np.asarray([r[k] for r in rows]) for k in rows[0]}
        name=f'{case}_s{seed}';np.savez_compressed(output/(name+'.npz'),**trace)
        summaries=[]
        for label,start,end in [('forward_transient',2.,4.),('forward_steady',6.,13.),
                                ('backward_transient',22.,24.),('backward_steady',26.,33.)]:
            mask=(trace['time']>=start)&(trace['time']<end)
            if not mask.any():continue
            pitch=trace['pitch'][mask];tau=trace['motor_substeps'][mask][:,:,WHEELS]
            frequencies,power=periodogram(pitch,fs=50.)
            summaries.append(dict(window=label,v_mean=float(trace['velocity'][mask].mean()),
                velocity_std=float(trace['velocity'][mask].std()),pitch_std_rad=float(pitch.std()),
                pitch_rate_rms=float(np.sqrt(np.mean(trace['pitch_rate'][mask]**2))),
                wheel_torque_rms=float(np.sqrt(np.mean(tau**2))),
                wheel_substep_torque_std=float(np.sqrt(np.mean(np.var(tau,axis=1)))),
                leg_velocity_rms=float(np.sqrt(np.mean(trace['joint_velocity'][mask][:,LEGS]**2))),
                leg_target_std=float(np.sqrt(np.mean(np.var(trace['targets'][mask][:,LEGS],axis=0)))),
                pitch_peak_hz=float(frequencies[1:][power[1:].argmax()]),
                residual_peak_nm=float(abs(trace['residual_total_nm'][mask]).max())))
        return dict(execution_domain='VALIDATION_SIM',evidence_status='FAIL' if failure else 'PASS',
            checkpoint_sha256=policy['policy_interface']['checkpoint_sha256'],case=case,seed=seed,
            initial_physics=initial.tolist(),trace=name+'.npz',failure=failure,completed_s=float(trace['time'][-1]),metrics=summaries)
    finally:env.close()


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args();output=args.output.resolve()
    if not output.is_relative_to(REPO/'docs/exp') or output.exists():parser.error('New docs/exp evidence directory required')
    output.mkdir(parents=True)
    policy=policy_config();cfg=json.loads((ARCHIVE/'config.json').read_text())
    parameters=json.loads((ARCHIVE/'manifest.json').read_text())['nominal_parameters']
    source=read_yaml(next(p for p in policy['policy_interface']['sources'] if p.endswith('env.yaml')))
    description=Description(source['scene']['robot']['spawn']['asset_path'])
    write_json(output/'manifest.json',dict(execution_domain='VALIDATION_SIM',evidence_status='NOT_TESTED',
        checkpoint_sha256=policy['policy_interface']['checkpoint_sha256'],onnx_sha256=policy['policy_interface']['onnx_sha256'],
        script_sha256=sha256(Path(__file__)),command_ramp_m_s2=.5,duration_s=42.,
        cases=['step_hold','step_policy','ramp_policy','ramp_sync'],seeds=[42,43,44],
        notes='No external force. Only ramp_sync changes actor gyro/quaternion cache; current joints/history unchanged.'))
    for seed in (42,43,44):
        initial=None
        for case in ('step_hold','step_policy','ramp_policy','ramp_sync'):
            r=run_case(case,seed,output,policy,cfg,description,parameters)
            if initial is None:initial=r['initial_physics']
            np.testing.assert_array_equal(initial,r['initial_physics'])
            with (output/'results.jsonl').open('a') as stream:stream.write(json.dumps(r,allow_nan=False)+'\n')
            print('[VALIDATION_SIM]',case,seed,r['evidence_status'],r['failure'],flush=True)


if __name__=='__main__':main()
