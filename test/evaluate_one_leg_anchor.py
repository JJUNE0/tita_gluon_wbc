"""VALIDATION_SIM: frozen first-episode support/height/COM assessment, saved DR."""

import argparse
from dataclasses import replace
import json
from pathlib import Path
import pickle
import sys
from urllib.parse import urlparse

import numpy as np
import torch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from mj_lab.flash_sac import TitaFlashSACEnv, runtime
from mj_lab.robots.tita import mdp
from mj_lab.robots.tita.stand_one_leg_anchor_env_cfg import (
    anchor_metric, support_geometry, swing_geometry, wheel_overlap_cost,
)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--checkpoint', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--num-envs', type=int, default=64)
    parser.add_argument('--seconds', type=float, default=20.)
    parser.add_argument('--wandb-url')
    parser.add_argument('--artifact-name')
    args = parser.parse_args()
    if bool(args.wandb_url) != bool(args.artifact_name):
        parser.error('--wandb-url and --artifact-name must be used together')
    path, metadata = runtime.read_checkpoint(args.checkpoint)
    if metadata['task'] not in ('stand_one_leg_anchor_left', 'stand_one_leg_anchor_right'):
        parser.error('Requires a fixed-anchor task checkpoint')
    runtime.setup_imports(False)
    from mjlab.envs import ManagerBasedRlEnv
    from flash_rl.agents.flashSAC.agent import FlashSACConfig
    with (path/'env.pkl').open('rb') as stream:
        cfg = pickle.load(stream)
    cfg.scene.num_envs, cfg.seed = args.num_envs, 42
    raw = ManagerBasedRlEnv(cfg, device='cuda:0')
    try:
        env = TitaFlashSACEnv(raw, **runtime.action_mapping_kwargs(metadata))
        learner = replace(FlashSACConfig(**metadata['agent']), device_type='cuda:0', buffer_device_type='cpu',
            buffer_max_length=args.num_envs, buffer_min_length=1, sample_batch_size=1,
            use_compile=False, use_amp=False, load_optimizer=False, load_reward_normalizer=False)
        agent = runtime.make_agent(env, learner)
        agent.load(str(path))
        obs = env.reset(seed=42)
        current, traces = {}, []
        original_step = raw.step
        original_termination_compute = raw.termination_manager.compute
        knee_flags = torch.zeros(args.num_envs, 2, device=env.device, dtype=torch.bool)

        def observed_termination_compute():
            result = original_termination_compute()
            # Capture exactly the sensor history used by the termination;
            # raw.step's later forward/sense can refresh those buffers.
            knee_flags.copy_(mdp.contacts(raw, 'knees') > 1.)
            return result

        raw.termination_manager.compute = observed_termination_compute

        def observed_step(action):
            result = original_step(action)
            drift, speed = support_geometry(raw)
            height, gap = swing_geometry(raw)
            side = raw.command_manager.get_term('base_velocity').cfg.support_side
            from mj_lab.robots.tita.stand_one_leg_reference_env_cfg import balance_metric
            current.update(drift_m=drift, speed_m_s=speed, swing_clearance_m=height, swing_com_gap_m=gap,
                base_speed_m_s=raw.scene['robot'].data.root_link_lin_vel_w[:, :2].norm(dim=1),
                yaw_rad_s=raw.scene['robot'].data.root_link_ang_vel_w[:, 2],
                low_anchored_support=anchor_metric(raw, 'anchored_low_support_fraction'),
                single_support=balance_metric(raw, 'single_support_fraction', support_side=side),
                wheel_overlap=wheel_overlap_cost(raw)>0., failed=raw.termination_manager.terminated,
                knee_sides=knee_flags, knee_failure=raw.termination_manager.get_term('knee_contact'),
                done=raw.termination_manager.dones,
                drift_failure=(raw.termination_manager.get_term('support_drift')
                    if 'support_drift' in raw.termination_manager.active_terms
                    else torch.zeros_like(raw.termination_manager.terminated)))
            current.update({k:v.detach().cpu().numpy().copy() for k,v in current.items()})
            return result

        raw.step = observed_step
        active = np.ones(args.num_envs, dtype=bool)
        failed = np.zeros(args.num_envs, dtype=bool)
        drift_failed = np.zeros(args.num_envs, dtype=bool)
        for tick in range(round(args.seconds/raw.step_dt)):
            action = torch.as_tensor(agent.sample_actions(tick+1, {'next_observation':obs}, training=False), device=env.device)
            obs, _, reward, _, _, _ = env.step(action)
            assert torch.isfinite(obs).all() and torch.isfinite(reward).all()
            traces.append({**current, 'active':active.copy()})
            failed |= active & current['failed']
            drift_failed |= active & current['drift_failure']
            active &= ~current['done']
        arrays = {key:np.stack([step[key] for step in traces]) for key in traces[0]}
        mask = arrays['active']
        single = arrays['single_support'] * mask
        success = arrays['low_anchored_support'] * mask
        times = (np.arange(len(traces)) + 1)[:, None] * raw.step_dt
        first_lift = np.where(single.astype(bool), times, np.inf).min(axis=0)
        knee_events = mask & arrays['knee_failure']
        side_id = 0 if cfg.commands['base_velocity'].support_side == 'left' else 1
        metrics = dict(survival_fraction=float((~failed).mean()), drift_failure_fraction=float(drift_failed.mean()),
            support_knee_first_episode_failure_count=int((knee_events & arrays['knee_sides'][:, :, side_id]).sum()),
            swing_knee_first_episode_failure_count=int((knee_events & arrays['knee_sides'][:, :, 1-side_id]).sum()),
            both_knees_first_episode_failure_count=int((knee_events & arrays['knee_sides'].all(axis=2)).sum()),
            first_lift_within_05s_fraction=float((first_lift <= .5).mean()),
            first_lift_within_1s_fraction=float((first_lift <= 1.).mean()),
            first_lift_within_2s_fraction=float((first_lift <= 2.).mean()),
            mean_single_support_s=float(single.sum(axis=0).mean()*raw.step_dt),
            mean_anchored_low_support_s=float(success.sum(axis=0).mean()*raw.step_dt),
            max_support_drift_m=float(arrays['drift_m'][mask].max()),
            outside_10cm_fraction=float((arrays['drift_m'][mask]>.1).mean()),
            mean_support_speed_m_s=float(arrays['speed_m_s'][mask].mean()),
            mean_base_speed_m_s=float(arrays['base_speed_m_s'][mask].mean()),
            mean_abs_yaw_rad_s=float(np.abs(arrays['yaw_rad_s'][mask]).mean()),
            swing_over_8cm_fraction=float((arrays['swing_clearance_m'][mask]>.08).mean()),
            wheel_overlap_fraction=float(arrays['wheel_overlap'][mask].mean()),
            mean_swing_com_xy_distance_m=float(arrays['swing_com_gap_m'][mask].mean()))
        learned_pass = (metrics['survival_fraction'] >= .95
            and metrics['mean_anchored_low_support_s'] >= .8*args.seconds
            and metrics['wheel_overlap_fraction'] <= .01)
        report = dict(execution_domain='VALIDATION_SIM', evidence_status='PASS',
            policy_quality='PASS' if learned_pass else 'SUSPICIOUS', checkpoint=str(path),
            policy_checkpoint_sha256=metadata['actor_sha256'], num_envs=args.num_envs, seed=42,
            has_support_drift_termination='support_drift' in raw.termination_manager.active_terms,
            first_supported_lift_s=[float(t) if np.isfinite(t) else None for t in first_lift],
            seconds=args.seconds, metrics=metrics,
            detail='Frozen deterministic actions, saved noise/DR/pushes; first episode only. '
                   'Terminal states captured before wrapper resets. PASS execution does not imply policy success. '
                   'Quality threshold: >=95% survival, >=80% horizon in anchored low tucked support, <=1% wheel overlap.')
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report,indent=2)+'\n')
        np.savez_compressed(args.output.with_suffix('.npz'), **arrays)
        print('[VALIDATION_SIM]',json.dumps(report),flush=True)
    finally:
        raw.close()
    if args.wandb_url:
        # A separate evaluator process owns this writer, after training exits.
        import wandb
        parts = urlparse(args.wandb_url).path.strip('/').split('/')
        entity, project, run_id = parts[-4], parts[-3], parts[-1]
        run = wandb.init(entity=entity, project=project, id=run_id, resume='must', mode='online',
            dir=str(args.output.parent), settings=wandb.Settings(disable_git=True, x_disable_stats=True, console='off'))
        try:
            run.log({'validation/final/'+key:value for key,value in report['metrics'].items()})
            run.summary['validation/final/policy_quality'] = report['policy_quality']
            run.summary['validation/final/checkpoint_sha256'] = metadata['actor_sha256']
            artifact = wandb.Artifact(args.artifact_name, type='validation-evidence', metadata=report)
            artifact.add_file(str(args.output))
            artifact.add_file(str(args.output.with_suffix('.npz')))
            logged = run.log_artifact(artifact)
            logged.wait(timeout=120)
            remote = wandb.Api(timeout=30).artifact(f'{entity}/{project}/{logged.name}')
            if len(remote.manifest.entries) != 2:
                raise RuntimeError('Final evaluation artifact is incomplete')
            args.output.with_suffix('.upload.json').write_text(json.dumps(dict(
                execution_domain='VALIDATION_SIM', evidence_status='PASS', wandb_url=args.wandb_url,
                policy_checkpoint_sha256=metadata['actor_sha256'],
                artifact=f'{entity}/{project}/{logged.name}'),indent=2)+'\n')
        finally:
            run.finish()


if __name__ == '__main__':
    main()
