"""TRAINING_SIM: Experiment1 shared-noise torque residual; optional training-only LPF."""
import argparse
from collections import deque
from dataclasses import asdict
import json
import math
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time

os.environ.setdefault('MUJOCO_GL', 'egl')
import numpy as np
import torch

from mj_lab.flash_sac import runtime
from mj_lab.robots.tita.residual.flat_env_residual_torque_sensor_delay import (
    TitaFlatResidualTorqueSensorDelayEnv, TitaFlatResidualTorqueSensorDelayEnvCfg,
)
from mj_lab.robots.tita.residual.flat_env_residual_torque_lpf_delay import (
    TitaFlatResidualTorqueLpfDelayEnv, TitaFlatResidualTorqueLpfDelayEnvCfg,
    TitaFlatResidualTorqueCleanLpfDelayEnv, TitaFlatResidualTorqueCleanLpfDelayEnvCfg,
)
from mj_lab.robots.tita.residual.flat_env_residual_torque_pose_delay import (
    TitaFlatResidualTorquePoseDelayEnv, TitaFlatResidualTorquePoseDelayEnvCfg,
)
from mj_lab.robots.tita.residual.flat_env_residual_torque_lpf_500hz import (
    TitaFlatResidualTorqueLpf500HzEnv, TitaFlatResidualTorqueLpf500HzEnvCfg,
)
from mj_lab.scripts.residual_training import (
    ResidualPolicy, ContinuousTermination, fresh_agent, frame, render_trace,
    save_frames, save_curves, tensor_digest, write,
)


class TorquePolicy(ResidualPolicy):
    def __init__(self, actor, torque_limit):
        super().__init__(actor)
        self.torque_limit = torque_limit

    def forward(self, observation):
        return super().forward(observation)*self.torque_limit


def environment_config(args, count=None, seed=None, duration=None):
    options=dict(teacher_checkpoint=args.teacher,
        num_envs=args.num_envs if count is None else count,
        episode_length_s=args.episode_seconds if duration is None else duration,
        seed=args.seed if seed is None else seed,torque_limit_nm=args.torque_limit,
        torque_max_lag=args.torque_max_lag,pose_command_mode=args.pose_command_mode,
        pose_height_range=args.pose_height_range,pose_roll_pitch_deg=args.pose_roll_pitch_deg,
        pose_roll_deg=args.pose_roll_deg,pose_pitch_deg=args.pose_pitch_deg,
        pose_nominal_fraction=args.pose_nominal_fraction,pose_resampling_s=args.pose_resampling_s)
    cutoff=getattr(args,'residual_lpf_hz',0.)
    if getattr(args,'residual_hz',250)==500:
        if getattr(args,'actor_sensor_mode','teacher_shared')!='teacher_shared' or cutoff<=0:
            raise ValueError('Residual500Hz comparison requires the shared-sensor LPF profile')
        return TitaFlatResidualTorqueLpf500HzEnvCfg(**options,residual_lpf_hz=cutoff)
    if getattr(args,'actor_sensor_mode','teacher_shared')=='clean':
        if cutoff>0:
            return TitaFlatResidualTorqueCleanLpfDelayEnvCfg(**options,residual_lpf_hz=cutoff)
        return TitaFlatResidualTorquePoseDelayEnvCfg(**options)
    if cutoff>0:
        return TitaFlatResidualTorqueLpfDelayEnvCfg(**options,residual_lpf_hz=cutoff)
    return TitaFlatResidualTorqueSensorDelayEnvCfg(**options)


def environment(args, count=None, seed=None, duration=None):
    cfg=environment_config(args,count,seed,duration)
    if isinstance(cfg,TitaFlatResidualTorqueLpf500HzEnvCfg):
        cls=TitaFlatResidualTorqueLpf500HzEnv
    elif isinstance(cfg,TitaFlatResidualTorqueCleanLpfDelayEnvCfg):
        cls=TitaFlatResidualTorqueCleanLpfDelayEnv
    elif isinstance(cfg,TitaFlatResidualTorqueLpfDelayEnvCfg):
        cls=TitaFlatResidualTorqueLpfDelayEnv
    elif isinstance(cfg,TitaFlatResidualTorqueSensorDelayEnvCfg):
        cls=TitaFlatResidualTorqueSensorDelayEnv
    else:
        cls=TitaFlatResidualTorquePoseDelayEnv
    return cls(cfg)


@torch.no_grad()
def evaluate(args, policy, destination, candidate):
    destination.mkdir(parents=True)
    seed = args.seed+10000
    torch.manual_seed(seed);np.random.seed(seed)
    env = environment(args, 16, seed, args.eval_seconds+1.)
    monitor = ContinuousTermination(env.raw.termination_manager)
    env.raw.termination_manager = monitor
    initial = torch.cat((env.robot.data.root_link_pose_w, env.robot.data.joint_pos, env.robot.data.joint_vel),1)
    assignment = torch.cat((env.raw.payload_mass[:,None], env.raw.payload_location, env.force,
                            env.force_link[:,None], env.force_start[:,None], env.force_duration[:,None]),1)
    plant = [getattr(env.raw.sim.model,k).flatten(1) for k in ('body_mass','body_inertia','body_ipos','geom_friction')]
    for motor in env.robot.actuators:
        plant.extend((motor.stiffness,motor.damping,motor.torque_history.current_lags[:,None]))
    result = dict(initial_state_sha256=tensor_digest(initial), assignment_sha256=tensor_digest(assignment),
                  plant_sha256=tensor_digest(torch.cat(plant,1)))
    failed = torch.zeros(env.n,dtype=torch.bool,device=env.device)
    peak = torch.zeros(env.n,device=env.device)
    speed2 = torch.zeros_like(peak);samples = torch.zeros_like(peak)
    pose_trace=[];pose_error_sum=torch.zeros(env.n,3,device=env.device)
    clips = dict(clean=[],dr=[])
    total = round(args.eval_seconds/env.dt)
    try:
        for tick in range(total):
            action = policy(env.observation()) if candidate else torch.zeros_like(env.residual)
            _,bad,timeout,info = env.step(action)
            if hasattr(env.cfg,'pose_command_mode'):
                pose_trace.append(env.raw.command_manager.get_command('base_pose').clone())
                pose_error_sum+=torch.stack([info['pose_roll_error_rad'],info['pose_pitch_error_rad'],info['pose_height_error_m']],1)
            failed |= bad | timeout | monitor.latest
            peak = torch.maximum(peak,info['drift'])
            if tick >= total//2:
                valid = ~failed
                speed2 += info['planar_speed'].square()*valid
                samples += valid
            if tick % round(1./(25*env.dt)) == 0:
                for name,world in (('clean',0),('dr',env.n//2)):
                    clips[name].append(frame(env,world,info))
        result.update(execution_domain='VALIDATION_SIM',evidence_status='PASS',quality_status='NOT_ASSESSED',
                      failed_worlds=int(failed.sum()),seconds=args.eval_seconds,
                      max_drift_per_world_m=peak.cpu().tolist(),
                      tail_speed_rms_per_world_m_s=(speed2/samples.clamp_min(1)).sqrt().cpu().tolist(),
                      valid_tail_samples=samples.cpu().tolist(),note='Continuous original trials; any failure remains failed; native interval kicks retained')
        if pose_trace:
            result['pose_command_schedule_sha256']=tensor_digest(torch.stack(pose_trace))
            result['pose_error_roll_pitch_height_per_world']=(pose_error_sum/total).cpu().tolist()
    finally:
        env.close()
    result['videos'] = {}
    for name,rows in clips.items():
        source=destination/(name+'.npz');save_frames(source,rows)
        target=source.with_suffix('.mp4')
        render_trace(source,target,('Torque residual + post-PD delay' if candidate else 'Teacher only + post-PD delay')+' / '+name)
        result['videos'][name]=str(target)
    write(destination/'evaluation.json',result)
    return result


def train(args):
    import wandb
    torch.set_num_threads(1);torch.manual_seed(args.seed);np.random.seed(args.seed)
    cfg = environment_config(args)
    args.output.mkdir(parents=True,exist_ok=False)
    reference_file=json.loads(args.reference_config.read_text());reference=reference_file['flash_sac_agent']
    sources=[Path(__file__),Path('mj_lab/robots/tita/residual/flat_env_residual_torque_delay.py'),
             Path('mj_lab/robots/tita/residual/flat_env_residual_torque.py'),Path('mj_lab/robots/tita/common/mdp.py'),
             Path('mj_lab/robots/tita/common/robot_cfg.py'),Path('mj_lab/scripts/residual_training.py')]
    if hasattr(cfg,'pose_command_mode'):
        sources.extend([Path('mj_lab/robots/tita/residual/flat_env_residual_torque_pose_delay.py'),
                        Path('mj_lab/robots/tita/roll_pitch_height/flat_env_roll_pitch_height_cfg.py')])
    if isinstance(cfg,TitaFlatResidualTorqueSensorDelayEnvCfg):
        sources.append(Path('mj_lab/robots/tita/residual/flat_env_residual_torque_sensor_delay.py'))
    if isinstance(cfg,(TitaFlatResidualTorqueLpfDelayEnvCfg,TitaFlatResidualTorqueCleanLpfDelayEnvCfg)):
        sources.append(Path('mj_lab/robots/tita/residual/flat_env_residual_torque_lpf_delay.py'))
    if isinstance(cfg,TitaFlatResidualTorqueLpf500HzEnvCfg):
        sources.append(Path('mj_lab/robots/tita/residual/flat_env_residual_torque_lpf_500hz.py'))
    actor_hz=cfg.residual_manifest()['actor_hz']
    config=dict(cfg.residual_manifest(),execution_domain='TRAINING_SIM',evidence_status='NOT_TESTED',
        args={k:str(v) if isinstance(v,Path) else v for k,v in vars(args).items()},algorithm='FLASH SAC',
        initialization='Fresh Actor/Critics/temperature/optimizers/replay/reward normalizer; frozen Teacher only',
        total_target_vector_steps=args.steps,total_transitions=args.steps*args.num_envs,
        step_definition=f'One vector step advances all worlds {1000/actor_hz:g}ms; residual{actor_hz}Hz / Teacher50Hz / PD500Hz',
        initial_pose_randomization=False,initial_velocity_randomization=False,initial_push=False,
        reference_config=str(args.reference_config),reference_wandb_url=reference_file.get('wandb_url'),
        learner_actions='Normalized [-1,1] in replay; multiply by torque_limit exactly once at env.step',
        checkpoint_interval_vector_steps=args.checkpoint_interval,video_interval_vector_steps=args.video_interval,
        source_sha256={str(p):runtime.sha256(p) for p in sources})
    snapshot=args.output/'source';snapshot.mkdir()
    for source in sources:shutil.copyfile(source,snapshot/source.name)
    shutil.copyfile(args.reference_config,snapshot/'reference_config.json')
    write(args.output/'config.json',config)
    run=wandb.init(project='tita_sac_residual_amp',entity='bjy6614-postech',name=args.output.name,
        dir=str(args.output),mode=args.wandb_mode,config=config,
        settings=wandb.Settings(disable_git=True,console='off'))
    config['wandb_url']=run.url if args.wandb_mode=='online' else None
    write(args.output/'config.json',config);run.define_metric('vector_step');run.define_metric('*',step_metric='vector_step')
    env=agent=None;checkpoint=None;status='FAIL';step=updates=0;started=time.monotonic()
    recent=deque(maxlen=64);clips=deque(maxlen=500);jobs=[]

    def save():
        nonlocal checkpoint
        folder=args.output/f'residual_{step:08d}_u{updates:06d}'
        agent.save(str(folder));checkpoint=folder/'actor.pt';sha=runtime.sha256(checkpoint)
        write(folder/'residual.json',dict(config,vector_step=step,updates=updates,
              physical_transitions=step*args.num_envs,policy_checkpoint_sha256=sha,replay_saved=False))
        write(args.output/'latest.json',dict(checkpoint=str(checkpoint),policy_checkpoint_sha256=sha,
              vector_step=step,updates=updates,wandb_url=config['wandb_url'],residual_mode='torque'))
        if args.wandb_mode=='online':
            artifact=wandb.Artifact(f'torque-delay-{run.id}-{step}',type='model',metadata=dict(policy_checkpoint_sha256=sha,vector_step=step))
            artifact.add_dir(str(folder));run.log_artifact(artifact)
        return sha

    def poll_videos(wait=False):
        for job in list(jobs):
            code=job['process'].wait() if wait else job['process'].poll()
            if code is None:continue
            job['stream'].close()
            if code!=0 or not job['target'].is_file():raise RuntimeError('Recorded video renderer failed: '+str(job['target']))
            if args.wandb_mode=='online':run.log({'vector_step':step,'training_clip/'+job['group']:wandb.Video(str(job['target']),fps=25,format='mp4')})
            write(job['target'].with_suffix('.video.json'),dict(execution_domain='VALIDATION_SIM',evidence_status='PASS',
                  source_step=job['step'],ending_checkpoint_sha256=job['sha'],path=str(job['target'])))
            jobs.remove(job)

    def video(sha):
        for group in ('clean','dr'):
            source=args.output/f'training_{step:08d}_{group}.npz'
            save_frames(source,[f[group] for f in clips]);target=source.with_suffix('.mp4')
            stream=source.with_suffix('.render.log').open('w')
            process=subprocess.Popen([sys.executable,'-m','mj_lab.scripts.residual_training','--render',str(source),
                '--video-output',str(target),'--label','Torque residual + 0..8ms post-PD delay / '+group],stdout=stream,stderr=subprocess.STDOUT)
            jobs.append(dict(process=process,stream=stream,target=target,group=group,step=step,sha=sha))

    try:
        env=environment(args)
        lags=env.robot.actuators[0].torque_history.current_lags
        initial=dict(execution_domain='TRAINING_SIM',evidence_status='PASS',
            max_initial_linear_speed=float(env.robot.data.root_link_lin_vel_w.abs().max()),
            max_initial_angular_speed=float(env.robot.data.root_link_ang_vel_b.abs().max()),
            max_initial_joint_speed=float(env.robot.data.joint_vel.abs().max()),
            initial_force_active_worlds=int((env.force_start<=0).sum()),
            torque_delay_bin_counts=torch.bincount(lags,minlength=args.torque_max_lag+1).cpu().tolist(),
            torque_delay_bins_ms=[2*i for i in range(args.torque_max_lag+1)],
            common_lag_across_all_motors=all(torch.equal(lags,m.torque_history.current_lags) for m in env.robot.actuators),
            native_reference_delay_disabled=all(m._delay_buffer is None for m in env.robot.actuators))
        if hasattr(cfg,'pose_command_mode'):
            pose=env.raw.command_manager.get_term('base_pose')
            initial.update(pose_command_mode=cfg.pose_command_mode,
                initial_sampled_pose_target_min=pose.target.min(0).values.cpu().tolist(),
                initial_sampled_pose_target_max=pose.target.max(0).values.cpu().tolist())
        assert initial['max_initial_linear_speed']==initial['max_initial_angular_speed']==initial['max_initial_joint_speed']==0
        assert initial['initial_force_active_worlds']==0 and initial['common_lag_across_all_motors'] and initial['native_reference_delay_disabled']
        write(args.output/'initial_state.json',initial)
        memory_args=argparse.Namespace(buffer_size=args.buffer_size,buffer_device='cuda:0',device='cuda:0')
        runtime.select_buffer_device(memory_args,env)
        frozen={k:v.clone() for k,v in env.teacher.state_dict().items()}
        agent=fresh_agent(env,reference,args);assert agent._update_step==0
        config.update(flash_sac_agent=asdict(agent.cfg),initial_actor_updates=0,initial_state_receipt=initial,
                      hyperparameter_differences={k:dict(reference=v,actual=asdict(agent.cfg)[k]) for k,v in reference.items() if v!=asdict(agent.cfg)[k]})
        write(args.output/'config.json',config);run.config.update(dict(flash_sac_agent=config['flash_sac_agent'],initial_state_receipt=initial))
        policy=TorquePolicy(agent._actor.network,args.torque_limit);save()
        observation=env.packed_observation();budget=0.;learner_stats={}
        with (args.output/'metrics.jsonl').open('w',buffering=1) as stream:
            for step in range(1,args.steps+1):
                with torch.no_grad():
                    action=torch.as_tensor(agent.sample_actions(step,{'next_observation':observation},training=True),device=env.device).clamp(-1.,1.)
                    reward,terminated,truncated,info=env.step(action*args.torque_limit)
                    terminal=env.packed_observation()
                    agent.process_transition(dict(observation=observation,action=action,next_observation=terminal,reward=reward,terminated=terminated,truncated=truncated))
                    stats={k:v.float().mean() for k,v in info.items()}
                    for group,mask in (('clean',env.clean_mask),('dr',env.dr_mask)):
                        stats.update({group+'/'+k:v[mask].float().mean() for k,v in info.items()})
                        stats[group+'/task_reward']=reward[mask].mean()
                    for lag in range(args.torque_max_lag+1):stats[f'delay_distribution/{lag*2}ms']=(info['torque_delay_ms']==lag*2).float().mean()
                    recent.append(stats)
                    if step%round(1./(25*env.dt))==0:clips.append({group:frame(env,world,info) for group,world in (('clean',0),('dr',env.n//2))})
                    env.reset_done(terminated|truncated);observation=env.packed_observation()
                if agent.can_start_training():
                    budget+=args.updates_per_step
                    while budget>=1.:
                        learner_stats.update(agent.update());budget-=1.;updates+=1
                if step%64==0 or step==args.steps:
                    metrics={k:float(torch.stack([r[k] for r in recent]).mean()) for k in recent[-1]}
                    metrics.update({k:float(v) for k,v in learner_stats.items()})
                    metrics.update(vector_step=step,updates=updates,physical_transitions=step*args.num_envs,elapsed_seconds=time.monotonic()-started)
                    metrics.update(reward=float(reward.mean()),task_reward=float(reward.mean()),
                                   **{'dr/payload_min_kg':float(env.raw.payload_mass[env.dr_mask].min()),
                                      'dr/payload_max_kg':float(env.raw.payload_mass[env.dr_mask].max()),
                                      'dr/planned_force_max_n':float(env.force[env.dr_mask].norm(dim=1).max()),
                                      'dr/applied_force_max_n':float(info['force_n'][env.dr_mask].max())})
                    stream.write(json.dumps(metrics,allow_nan=False)+'\n');run.log(metrics)
                    write(args.output/'progress.json',dict(metrics,execution_domain='TRAINING_SIM',evidence_status='PASS',status='running',wandb_url=config['wandb_url']))
                    print(json.dumps({k:metrics[k] for k in ('vector_step','updates','dr/fixed_position_error_m','elapsed_seconds')}),flush=True)
                    poll_videos()
                if step%args.checkpoint_interval==0 or step==args.steps:
                    sha=save()
                if args.video_interval and step%args.video_interval==0:
                    if step%args.checkpoint_interval:sha=save()
                    video(sha)
        assert all(torch.equal(v,frozen[k]) for k,v in env.teacher.state_dict().items())
        env.close();env=None
        import onnxruntime as ort
        target=checkpoint.parent/'residual_torque.onnx';example=torch.zeros(1,440,device='cuda:0')
        torch.onnx.export(policy,example,str(target),input_names=['proprio_history'],output_names=['residual_torque_nm'],opset_version=17,dynamo=False)
        options=ort.SessionOptions();options.intra_op_num_threads=1
        session=ort.InferenceSession(str(target),options,providers=['CPUExecutionProvider']);error=0.
        for _ in range(32):
            sample=torch.randn_like(example)
            with torch.no_grad():
                expected=policy(sample).cpu().numpy()
                native=policy.actor.get_mean_and_std(sample,training=False)[0].tanh().cpu().numpy()*args.torque_limit
            assert np.max(abs(native-expected))<1e-4
            error=max(error,float(np.max(abs(expected-session.run(None,{'proprio_history':sample.cpu().numpy()})[0]))))
        assert error<1e-3,error
        write(target.with_suffix('.export.json'),dict(execution_domain='DESKTOP_DRY_RUN',evidence_status='PASS',
              onnx_sha256=runtime.sha256(target),policy_checkpoint_sha256=runtime.sha256(checkpoint),max_abs_error_nm=error,output_units='Nm',
              residual_torque_filter=config.get('residual_torque_filter'),output_semantics=config.get('output_semantics','Residual torque in Nm')))
        if args.wandb_mode=='online':
            artifact=wandb.Artifact('torque-delay-export-'+run.id,type='model');artifact.add_file(str(target));artifact.add_file(str(target.with_suffix('.export.json')));run.log_artifact(artifact)
        if args.eval_seconds>0:
            baseline=evaluate(args,policy,args.output/'fixed_evaluation/teacher',False)
            candidate=evaluate(args,policy,args.output/'fixed_evaluation/candidate',True)
            for k in ('initial_state_sha256','assignment_sha256','plant_sha256'):assert baseline[k]==candidate[k],k
            if hasattr(cfg,'pose_command_mode'):
                assert baseline['pose_command_schedule_sha256']==candidate['pose_command_schedule_sha256']
            write(args.output/'evaluation.json',dict(execution_domain='VALIDATION_SIM',evidence_status='PASS',teacher=baseline,candidate=candidate,matched_initial_states_and_dr=True))
            if args.wandb_mode=='online':
                for name,result in (('teacher',baseline),('candidate',candidate)):
                    for group,path in result['videos'].items():run.log({'vector_step':step,'evaluation/'+name+'/'+group:wandb.Video(path,fps=25,format='mp4')})
                artifact=wandb.Artifact('torque-delay-evaluation-'+run.id,type='evaluation');artifact.add_dir(str(args.output/'fixed_evaluation'));artifact.add_file(str(args.output/'evaluation.json'));run.log_artifact(artifact)
        poll_videos(wait=True);curves=save_curves(args.output)
        if curves and args.wandb_mode=='online':run.log({'vector_step':step,'training_curves':wandb.Image(str(curves))})
        status='PASS'
    finally:
        if env:env.close()
        poll_videos(wait=True)
        summary=dict(execution_domain='TRAINING_SIM',evidence_status=status,status='completed' if status=='PASS' else 'failed',
            vector_step=step,updates=updates,checkpoint=str(checkpoint),wandb_url=config['wandb_url'],
            policy_checkpoint_sha256=runtime.sha256(checkpoint) if checkpoint else None,elapsed_seconds=time.monotonic()-started)
        write(args.output/'summary.json',summary);write(args.output/'progress.json',summary);run.summary.update(summary);run.finish(exit_code=0 if status=='PASS' else 1)


def main():
    p=argparse.ArgumentParser(description=__doc__)
    for key in ('teacher','reference-config','output'):p.add_argument('--'+key,type=Path,required=True)
    for key,value in [('num-envs',4096),('batch-size',8096),('buffer-size',1000000),('min-buffer',100000),('steps',50000),('seed',42),('checkpoint-interval',2000),('video-interval',10000),('torque-max-lag',4)]:p.add_argument('--'+key,type=int,default=value)
    p.add_argument('--gamma',type=float,default=.99);p.add_argument('--updates-per-step',type=float,default=2.)
    p.add_argument('--episode-seconds',type=float,default=10.);p.add_argument('--torque-limit',type=float,default=10.)
    p.add_argument('--eval-seconds',type=float,default=120.);p.add_argument('--wandb-mode',choices=['online','disabled'],default='online')
    p.add_argument('--pose-command-mode',choices=['height','height_roll_pitch'],default='height_roll_pitch')
    p.add_argument('--actor-sensor-mode',choices=['teacher_shared','clean'],default='teacher_shared')
    p.add_argument('--residual-lpf-hz',type=float,default=0.)
    p.add_argument('--residual-hz',type=int,choices=[250,500],default=250)
    p.add_argument('--pose-height-range',type=float,nargs=2,default=(.27,.42))
    p.add_argument('--pose-roll-pitch-deg',type=float,default=5.)
    p.add_argument('--pose-roll-deg',type=float,default=30.)
    p.add_argument('--pose-pitch-deg',type=float,default=15.)
    p.add_argument('--pose-nominal-fraction',type=float,default=.3)
    p.add_argument('--pose-resampling-s',type=float,nargs=2,default=(5.,8.))
    args=p.parse_args()
    if min(args.steps,args.num_envs,args.batch_size,args.min_buffer,args.checkpoint_interval)<=0 or args.num_envs%2:p.error('Positive sizes, even env count required')
    if args.buffer_size<max(args.num_envs,args.batch_size,args.min_buffer):p.error('Replay smaller than batch/warmup/vector step')
    if not 0<args.gamma<1 or not math.isfinite(args.updates_per_step) or args.updates_per_step<=0:p.error('Invalid learner settings')
    if args.torque_max_lag<0 or args.video_interval<0 or args.eval_seconds<0:p.error('Invalid delay/video/eval settings')
    if not math.isfinite(args.residual_lpf_hz) or not 0<=args.residual_lpf_hz<250:p.error('Invalid residual LPF parameter')
    train(args)


if __name__=='__main__':main()
