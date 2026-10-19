"""VALIDATION_SIM: FlashSAC synchronized actor IMU with relative F-1 stop hold; no ROS/hardware."""

import argparse
import json
from pathlib import Path
import sys
import threading
import time

import numpy as np

REPO=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(REPO/'test'))
from debug_lqr_d4_diagnostics import ARCHIVE,Plant
from eval_flash_torque_residual import additive_torque
from sim2sim.lqr.estimator import Sensors,WheelOdometry
from sim2sim.lqr.model import Description
from sim2sim.lqr.evaluate import write_json
from sim2sim.lqr.runtime import policy_config,LEGS,WHEELS
from sim2sim_ros2_jazzy.checkpoint import read_yaml,sha256
from sim2sim_ros2_jazzy.adapter import ObsState,quat_wxyz_to_rotmat


class StopHold:
    """Command-gated hold: reset odometry once on entry; actual drift keeps hold on."""
    def __init__(self,description,equilibrium_pitch,enabled=True):
        self.estimator=WheelOdometry(description,equilibrium_pitch)
        self.enabled=enabled;self.holding=False;self.age=0.;self.u=0.
        self.entries=0;self.exits=0;self.state=None

    def step(self,command,sensors,dt):
        command=np.asarray(command)
        if command.shape!=(3,) or not np.isfinite(command).all():
            raise ValueError('Expected finite [vx,vy,yaw_rate]')
        enter=np.all(abs(command)<=np.array([.02,.02,.03]))
        leave=np.any(abs(command)>=np.array([.04,.04,.06]))
        event=''
        if not self.holding and enter:
            self.holding=True;self.age=0.;self.estimator.reset();self.entries+=1;event='hold_enter'
        elif self.holding and leave:
            self.holding=False;self.exits+=1;event='hold_exit'
        if self.holding:
            self.state=self.estimator.observe(sensors,dt)
            phase=min(self.age,1.);activation=phase*phase*(3.-2.*phase)
            raw=-2.*self.state[0]-.5*self.state[1]
            target=activation*np.clip(raw,-1.,1.) if self.enabled else 0.
            self.age+=dt
        else:
            # No stale position feedback while moving. Slew releases prior torque.
            self.state=None;activation=0.;raw=0.;target=0.
        self.u=float(np.clip(target,self.u-2.*dt,self.u+2.*dt))
        return self.u,dict(mode='HOLD' if self.holding else ('RELEASE' if abs(self.u)>1e-9 else 'MOVE'),
            event=event,entries=self.entries,exits=self.exits,activation=activation,
            relative_p=float(self.state[0]) if self.state is not None else None,
            estimated_v=float(self.state[1]) if self.state is not None else None,raw_total_nm=float(raw))


def demo_command(t):
    phase=t%32.
    vx=.2 if 2.<=phase<7. else (-.2 if 17.<=phase<22. else 0.)
    return np.array([vx,0.,0.],dtype=np.float32)


def infer_synchronized(playback,env,packet,command):
    """Current joint state and clone-refreshed IMU; original actor/history/PD."""
    quat=packet.imu_quaternion.astype(np.float32)
    state=ObsState(env.joint_pos(),env.joint_vel(),quat,packet.imu_gyro.astype(np.float32),
        command.copy(),playback.last_action,quat_wxyz_to_rotmat(quat).T @ env.base_lin_vel())
    obs=playback.builder.build(state)
    action=playback.policy.run(['nn_output'],{'nn_input0':obs.reshape(1,-1)})[0].reshape(8)
    return obs,action


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--viewer',action='store_true')
    parser.add_argument('--manual',action='store_true')
    parser.add_argument('--duration',type=float,default=0.)
    parser.add_argument('--seed',type=int,default=42)
    parser.add_argument('--no-residual',action='store_true')
    args=parser.parse_args();output=args.output.resolve()
    if not output.is_relative_to(REPO/'docs/exp') or output.exists():
        parser.error('New output directory under docs/exp/ required')
    output.mkdir(parents=True)
    policy=policy_config();cfg=json.loads((ARCHIVE/'config.json').read_text())
    parameters=json.loads((ARCHIVE/'manifest.json').read_text())['nominal_parameters']
    source=read_yaml(next(p for p in policy['policy_interface']['sources'] if p.endswith('env.yaml')))
    description=Description(source['scene']['robot']['spawn']['asset_path'])
    plant=Plant(policy,cfg,description,parameters,{'name':'nominal'},args.seed,0.)
    playback=plant.playback;env=plant.env
    hold=StopHold(description,parameters['equilibrium_pitch'],enabled=not args.no_residual)
    pending=[];key_lock=threading.Lock();running=True;automatic=not args.manual
    command=np.zeros(3,dtype=np.float32);demo_epoch=0.;reset_requested=False
    initial_qpos=env.data.qpos.copy();initial_qvel=env.data.qvel.copy()
    rows=[];events=[];tick=0;leg_error=0.;failures=[];frozen=False
    baseline_anchor=None;hold_origin=None;hold_maxima=[];hold_max=0.
    applied=np.zeros((env.decimation,8));flash=applied.copy()
    duration=args.duration if args.duration>0. else (0. if args.viewer else 32.)
    log=(output/'run.log').open('w',buffering=1)

    def announce(message):
        print(message,flush=True);log.write(message+'\n')

    def key_callback(key):
        with key_lock:pending.append(key)

    manifest=dict(execution_domain='VALIDATION_SIM',evidence_status='NOT_TESTED',
        checkpoint_sha256=policy['policy_interface']['checkpoint_sha256'],onnx_sha256=policy['policy_interface']['onnx_sha256'],
        actor_imu='clone mj_forward at current qpos/qvel; original simulator unchanged',
        script_sha256=sha256(Path(__file__)),seed=args.seed,viewer=args.viewer,no_residual=args.no_residual,
        hold_gates=dict(enter=[.02,.02,.03],leave=[.04,.04,.06]),
        hold_reference='reset encoder/IMU odometry exactly once at stop command entry; p_ref=0',
        residual=dict(kp=2.,kv=.5,total_limit_nm=1.,ramp_s=1.,total_slew_nm_s=2.),
        demo='32s repeating: hold2, vx+0.2 for5, hold10, vx-0.2 for5, hold10; no external push',
        initial_qpos=initial_qpos.tolist(),initial_qvel=initial_qvel.tolist())
    write_json(output/'manifest.json',manifest)
    try:
        if args.viewer:
            import mujoco.viewer
            env.viewer=mujoco.viewer.launch_passive(env.model,env.data,key_callback=key_callback,
                show_left_ui=False,show_right_ui=False)
            env._viewer_threads=[thread for thread in threading.enumerate()
                if getattr(getattr(thread,'_target',None),'__module__',None)=='mujoco.viewer']
            with env.viewer.lock():
                env.viewer.cam.distance=2.;env.viewer.cam.azimuth=115.;env.viewer.cam.elevation=-20.
            announce('[VALIDATION_SIM] VIEWER_RUNNING | W/S vx +/-0.1, A/D yaw +/-0.15, SPACE stop, P demo, R reset, Q quit')
        wall_start=time.monotonic()
        while running and env.is_running():
            t=tick*env.control_dt
            with key_lock:keys=pending[:];pending.clear()
            for key in keys:
                if key==81:running=False
                elif key==82:reset_requested=True
                elif key==80:automatic=not automatic;demo_epoch=t;command[:]=0.
                elif key in (87,83,65,68,32):
                    automatic=False
                    if key==32:command[:]=0.
                    elif key in (87,83):command[0]=np.clip(command[0]+(.1 if key==87 else -.1),-.2,.2)
                    else:command[2]=np.clip(command[2]+(.15 if key==65 else -.15),-.3,.3)
            if not running:break
            if reset_requested:
                env.mujoco.mj_resetData(env.model,env.data);env.data.qpos[:]=initial_qpos;env.data.qvel[:]=initial_qvel
                env.mujoco.mj_forward(env.model,env.data);playback.last_action[:]=0.
                plant.estimator.reset();plant.synchronized_estimator.reset();plant.path=0.;plant.origin=None
                plant.previous_position=plant.previous_yaw=None
                hold=StopHold(description,parameters['equilibrium_pitch'],enabled=not args.no_residual)
                reset_requested=False;frozen=False;failures=[];command[:]=0.;automatic=False
                hold_origin=None;events.append(dict(time=t,event='operator_reset'));wall_start=time.monotonic()-t
            if frozen:
                env.viewer.sync();time.sleep(.02);continue
            if automatic:command=demo_command(t-demo_epoch)
            observation=plant.observe()
            failures,_=plant.failures(observation,'synchronized')
            # Clone-derived IMU sensor channels only; no true root position/velocity
            # enters hold control. GT is used below only for diagnostics/camera.
            data=plant.truth_data
            packet=Sensors(env.joint_pos(),env.joint_vel(),data.sensor('trunk_quat').data.copy(),data.sensor('trunk_gyro').data.copy())
            u,diag=hold.step(command,packet,env.control_dt)
            if diag['event']:
                events.append(dict(time=t,**diag,command=command.tolist()))
                if diag['event']=='hold_enter':
                    hold_origin=observation['position'].copy();hold_max=0.
                elif hold_origin is not None:
                    hold_maxima.append(hold_max);hold_origin=None
                announce(f'[VALIDATION_SIM] t={t:.2f} {diag["event"]} p={diag["relative_p"]} u={u:.4f}')
            if hold_origin is not None:
                hold_max=max(hold_max,float(np.linalg.norm((observation['position']-hold_origin)[:2])))
            if baseline_anchor is None:baseline_anchor=observation['position'].copy()
            mode=diag['mode']
            rows.append(dict(time=t,command=command.copy(),mode=mode,residual_total_nm=u,
                relative_p=np.nan if diag['relative_p'] is None else diag['relative_p'],
                estimated_v=np.nan if diag['estimated_v'] is None else diag['estimated_v'],
                hold_entries=hold.entries,hold_exits=hold.exits,position=observation['position'].copy(),
                gt_forward_velocity=observation['gt'][1],pitch_error=observation['synchronized'][2],
                motor_substeps=applied.copy(),flash_substeps=flash.copy(),reset_segment=sum(e['event']=='operator_reset' for e in events)))
            if env.viewer:
                with env.viewer.lock():env.viewer.cam.lookat[:]=observation['position']+[0.,0.,.2]
                env.viewer.set_texts([(None,None,
                    'SYNC IMU | F-1 velocity + stop hold\nMode\nCommand vx / yaw\nRelative p / v\nResidual total\nControls',
                    f'{"DEMO" if automatic else "KEYBOARD"} | t={t:.1f}s\n{mode}\n{command[0]:+.2f} m/s / {command[2]:+.2f} rad/s\n'
                    f'{diag["relative_p"] if diag["relative_p"] is not None else "-"} / {diag["estimated_v"] if diag["estimated_v"] is not None else "-"}\n'
                    f'{u:+.3f} Nm\nW/S A/D | SPACE stop | P demo | R reset | Q quit')])
            if failures:
                announce('[VALIDATION_SIM] FAIL '+str(failures))
                if not env.viewer:break
                env.viewer.set_texts((None,None,'Simulation paused after failure','R: reset | Q: quit\n'+str(failures)))
                frozen=True;env.viewer.sync();continue
            if duration and t>=duration:break
            _,action=infer_synchronized(playback,env,packet,command)
            flash_rows=[]

            def override(q,dq,torque):
                nonlocal leg_error
                flash_rows.append(torque.copy());result=additive_torque(torque,u,plant.signs)
                leg_error=max(leg_error,float(abs(result[LEGS]-torque[LEGS]).max()))
                return result

            _,applied=playback.step(action,override)
            np.testing.assert_array_equal(playback.last_action,action)
            flash=np.asarray(flash_rows);tick+=1
            if tick%50==0:
                telemetry=dict(execution_domain='VALIDATION_SIM',evidence_status='PASS',viewer_running=bool(env.viewer),
                    simulation_s=t,mode=mode,command=command.tolist(),residual_total_nm=u,
                    hold_entries=hold.entries,hold_exits=hold.exits,failures=failures)
                write_json(output/'telemetry.json',telemetry)
                if args.viewer:announce(f'[VALIDATION_SIM] t={t:.1f} {mode} cmd={command.tolist()} u={u:+.3f}')
            if env.viewer:
                delay=wall_start+tick*env.control_dt-time.monotonic()
                if delay>0:time.sleep(delay)
        if rows:
            trace={k:np.asarray([r[k] for r in rows]) for k in rows[0]}
            np.savez_compressed(output/'trace.npz',**trace)
            assert abs(trace['residual_total_nm']).max()<=1.+1e-9
            same_segment=np.diff(trace['reset_segment'])==0
            assert np.all(abs(np.diff(trace['residual_total_nm'])[same_segment])<=.04+1e-9)
            # Once released, movement produces no residual and leaves leg path intact.
            move=trace['mode']=='MOVE'
            assert np.all(trace['residual_total_nm'][move]==0.) and leg_error==0.
            write_json(output/'result.json',dict(execution_domain='VALIDATION_SIM',
                evidence_status='FAIL' if failures else 'PASS',completed_s=float(trace['time'][-1]),failures=failures,
                checkpoint_sha256=manifest['checkpoint_sha256'],hold_entries=hold.entries,hold_exits=hold.exits,
                leg_torque_max_error_nm=leg_error,events=events,
                hold_max_drift_m=hold_maxima+([hold_max] if hold_origin is not None else [])))
            announce(f'[VALIDATION_SIM] finished t={trace["time"][-1]:.2f} failures={failures} entries={hold.entries} exits={hold.exits}')
    finally:
        env.close();log.close()


if __name__=='__main__':
    main()
