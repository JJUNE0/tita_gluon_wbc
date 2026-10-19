"""VALIDATION_SIM: fixed held-out paired tests; student has no residual controller."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import importlib.util
import json
from pathlib import Path
import subprocess
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('finetune', ROOT / 'sim2sim/sim2sim_ros2_jazzy/launch/sim2sim_finetune.py')
ft = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ft)


def trial(job):
    ft.setup_imports(False)
    import torch
    from export import load_policy

    torch.set_num_threads(1)
    path, cfg, _, meta = ft.describe_checkpoint(job['checkpoint'])
    saved = ft.read_yaml(next(s for s in cfg['policy_interface']['sources'] if Path(s).name == 'env.yaml'))
    actor = load_policy(path.parent, meta).actor
    env = ft.FineTuneEnv(cfg, meta, saved, [0., 0., 0.], job['steps'] * .02 + .02)
    try:
        scale = job.get('mass_scale', 1.)
        env.physics.model.body_mass[1:] *= scale
        env.physics.model.body_inertia[1:] *= scale
        # Existing scene has steps at x=1.2 m. They must not stop the drifting
        # baseline or obstruct the velocity command regression on a flat floor.
        for geom in range(env.physics.model.ngeom):
            if (env.physics.model.geom_bodyid[geom] == 0
                    and env.physics.model.geom_type[geom] != env.physics.mujoco.mjtGeom.mjGEOM_PLANE):
                env.physics.model.geom_contype[geom] = 0
                env.physics.model.geom_conaffinity[geom] = 0
        env.physics.mujoco.mj_setConst(env.physics.model, env.physics.data)
        env.reset()
        rng = np.random.default_rng(job['seed'])
        pitch = job['pitch']
        env.physics.data.qpos[3:7] = [np.cos(pitch / 2), 0., np.sin(pitch / 2), 0.]
        env.physics.data.qvel[env.physics.qvel_addr] = rng.normal(0., .001, 8)
        env.physics.mujoco.mj_forward(env.physics.model, env.physics.data)
        obs = env.observe()
        rows = []
        for step in range(job['steps']):
            phase = step // 1000 if job['case'] == 'commands' else 0
            command = [(0., 0.), (.1, 0.), (0., 0.), (-.1, 0.), (0., .2), (0., 0.)][phase]
            env.command[[0, 2]] = command
            obs = env.observe()
            with torch.no_grad():
                action = actor.get_mean_and_std(torch.tensor(obs[:, :33]), training=False)[0].tanh().numpy()
            obs, _, reward, done, _, info = env.step(action)
            rows.append([step * .02, command[0], command[1], info['diagnostic_gt_vx_m_s'],
                         info['speed_proxy_m_s'], info['gyro_z_rad_s'], reward,
                         *info['diagnostic_gt_xy_m'], float(done)])
            if done:
                break
        trace = np.asarray(rows)
        out = Path(job['output']) / f'{job["policy"]}_{job["case"]}_{job["seed"]}'
        np.save(out.with_suffix('.npy'), trace)
        tail = trace[-1000:]
        result = dict(job, execution_domain='VALIDATION_SIM', checkpoint_sha256=meta['actor_sha256'],
                      completed=len(trace) == job['steps'] and not bool(trace[-1, -1]),
                      actual_steps=len(trace), vx_rmse=float(np.sqrt(np.mean((trace[:, 3] - trace[:, 1]) ** 2))),
                      yaw_rmse=float(np.sqrt(np.mean((trace[:, 5] - trace[:, 2]) ** 2))),
                      tail_vx_rms=float(np.sqrt(np.mean((tail[:, 3] - tail[:, 1]) ** 2))),
                      sensor_vx_rmse=float(np.sqrt(np.mean((trace[:, 4] - trace[:, 1]) ** 2))),
                      observer_error_rms=float(np.sqrt(np.mean((trace[:, 4] - trace[:, 3]) ** 2))),
                      max_xy_distance=float(np.linalg.norm(trace[:, 7:9] - trace[0, 7:9], axis=1).max()),
                      reward_mean=float(trace[:, 6].mean()))
        out.with_suffix('.json').write_text(json.dumps(result, indent=2) + '\n')
        return result
    finally:
        env.close()


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--candidate', type=Path)
    p.add_argument('--bc', type=Path)
    p.add_argument('--output', type=Path)
    p.add_argument('--job', type=Path)
    args = p.parse_args()
    if args.job:
        trial(json.loads(args.job.read_text()))
        return
    if args.candidate is None or args.bc is None or args.output is None:
        p.error('candidate, bc and output are required for the campaign')
    args.output.mkdir(parents=True, exist_ok=False)
    policies = dict(source=ft.build_parser().parse_args([]).ckpt, bc=args.bc, candidate=args.candidate)
    jobs = []
    for policy, checkpoint in policies.items():
        for seed, pitch in [(101, -.015), (102, 0.), (103, .015)]:
            jobs.append(dict(policy=policy, checkpoint=str(checkpoint.resolve()), case='nominal', seed=seed,
                             pitch=pitch, steps=3000, output=str(args.output.resolve())))
        jobs.append(dict(policy=policy, checkpoint=str(checkpoint.resolve()), case='commands', seed=104,
                         pitch=0., steps=6000, output=str(args.output.resolve())))
        jobs.append(dict(policy=policy, checkpoint=str(checkpoint.resolve()), case='mass15', seed=105,
                         pitch=0., mass_scale=1.15, steps=3000, output=str(args.output.resolve())))
    # Freeze conditions and acceptance before executing any held-out candidate.
    protocol = dict(execution_domain='VALIDATION_SIM', primary='Three held-out nominal starts, zero command, 60 s',
                    acceptance='No falls; median tail true speed RMS <= 50% source; command RMSE <= 1.1*source + .002 m/s / .01 rad/s',
                    exploratory='Unseen mass +15%, not part of nominal acceptance', jobs=jobs,
                    terrain='Flat plane only: all world-body non-plane geometry collisions disabled equally',
                    validator_sha256=ft.sha256(Path(__file__)), implementation_sha256=ft.sha256(Path(ft.__file__)))
    (args.output / 'protocol.json').write_text(json.dumps(protocol, indent=2) + '\n')
    def run_job(job):
        prefix = args.output / f'{job["policy"]}_{job["case"]}_{job["seed"]}'
        job_file = prefix.with_suffix('.job.json')
        job_file.write_text(json.dumps(job, indent=2) + '\n')
        with prefix.with_suffix('.log').open('w') as log:
            subprocess.run([sys.executable, str(Path(__file__).resolve()), '--job', str(job_file.resolve())],
                           stdout=log, stderr=subprocess.STDOUT, check=True)
        return json.loads(prefix.with_suffix('.json').read_text())

    with ThreadPoolExecutor(max_workers=3) as pool:
        results = list(pool.map(run_job, jobs))
    nominal = {name: [r for r in results if r['policy'] == name and r['case'] == 'nominal'] for name in policies}
    source = float(np.median([r['tail_vx_rms'] for r in nominal['source']]))
    candidate = float(np.median([r['tail_vx_rms'] for r in nominal['candidate']]))
    commands = {r['policy']: r for r in results if r['case'] == 'commands'}
    accepted = (all(r['completed'] for r in results if r['case'] != 'mass15')
                and candidate <= .5 * source
                and commands['candidate']['vx_rmse'] <= 1.1 * commands['source']['vx_rmse'] + .002
                and commands['candidate']['yaw_rmse'] <= 1.1 * commands['source']['yaw_rmse'] + .01)
    summary = dict(execution_domain='VALIDATION_SIM', evidence_status='PASS' if accepted else 'SUSPICIOUS',
                   accepted=accepted, nominal_source_tail_rms=source, nominal_candidate_tail_rms=candidate, results=results)
    (args.output / 'result.json').write_text(json.dumps(summary, indent=2) + '\n')
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt

    figure, axes = plt.subplots(1, 2, figsize=(12, 4))
    for name in policies:
        trace = np.load(args.output / f'{name}_nominal_102.npy')
        axes[0].plot(trace[:, 0], trace[:, 3] * 1000, label=name)
        trace = np.load(args.output / f'{name}_commands_104.npy')
        axes[1].plot(trace[:, 0], trace[:, 3], label=name)
    axes[0].set(xlabel='Time (s)', ylabel='True forward speed (mm/s)', title='Held-out zero command; no residual')
    axes[1].plot(trace[:, 0], trace[:, 1], 'k--', label='command')
    axes[1].set(xlabel='Time (s)', ylabel='True forward speed (m/s)', title='Command sequence; no residual')
    for axis in axes:
        axis.legend()
        axis.grid(alpha=.3)
    figure.tight_layout()
    figure.savefig(args.output / 'comparison.png', dpi=180)
    plt.close(figure)
    print('[VALIDATION_SIM] ' + json.dumps(summary), flush=True)


if __name__ == '__main__':
    main()
