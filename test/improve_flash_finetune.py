"""VALIDATION_SIM: teacher-assisted, frozen-normalization fine-tuning experiments."""
import argparse
from copy import deepcopy
import importlib.util
import json
from pathlib import Path
import sys
import time

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('finetune', ROOT / 'sim2sim/sim2sim_ros2_jazzy/launch/sim2sim_finetune.py')
ft = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ft)
ft.setup_imports(False)
import torch
from export import load_policy
from sim2sim_ros2_jazzy.velocity_bias import VelocityBias


def run(actor, cfg, meta, saved, steps, teacher=False, pitch=0., command=0., data=False):
    env = ft.FineTuneEnv(cfg, meta, saved, [command, 0., 0.], steps * .02 + .02)
    try:
        if pitch:
            env.physics.data.qpos[3:7] = [np.cos(pitch / 2), 0., np.sin(pitch / 2), 0.]
            env.physics.mujoco.mj_forward(env.physics.model, env.physics.data)
        hold = VelocityBias() if teacher else None
        obs = env.observe()
        rows, speeds, rewards, targets, proxy = [], [], [], [], []
        for step in range(steps):
            with torch.no_grad():
                a = actor.get_mean_and_std(torch.tensor(obs[:, :33]), training=False)[0].tanh().numpy()
            if hold:
                a = ft.teacher_action(env, a, hold)
            nxt, terminal, r, done, timeout, info = env.step(a)
            if data:
                rows.append((obs.copy(), a.copy(), terminal.copy(), r, done, timeout))
            speeds.append(info['diagnostic_gt_vx_m_s'])
            proxy.append(info['speed_proxy_m_s'])
            rewards.append(r)
            targets.append(a)
            obs = nxt
            if done:
                break
        v = np.asarray(speeds)
        summary = dict(steps=len(v), fallen=bool(done), rmse=float(np.sqrt(np.mean((v-command)**2))),
                       tail_mean=float(v[-min(1000,len(v)):].mean()),
                       tail_rms=float(np.sqrt(np.mean((v[-min(1000,len(v)):]-command)**2))),
                       reward=float(np.mean(rewards)), proxy_rms=float(np.sqrt(np.mean(np.square(proxy)))))
        if data:
            summary['action_mean'] = np.mean(targets, axis=0).tolist()
        return summary, rows
    finally:
        env.close()


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--output', type=Path, required=True)
    p.add_argument('--updates', type=int, default=1000)
    p.add_argument('--lr', type=float, default=1e-5)
    p.add_argument('--head_only', action='store_true')
    args = p.parse_args()
    args.output.mkdir(parents=True, exist_ok=False)
    torch.set_num_threads(1)
    torch.manual_seed(42)
    path,cfg,_,meta = ft.describe_checkpoint(ft.build_parser().parse_args([]).ckpt)
    saved = ft.read_yaml(next(s for s in cfg['policy_interface']['sources'] if Path(s).name=='env.yaml'))
    source = load_policy(path.parent, meta).actor
    result = dict(execution_domain='VALIDATION_SIM', checkpoint_sha256=meta['actor_sha256'], candidates=[], args=vars(args).copy())
    result['args']['output'] = str(args.output)
    result['baseline'], _ = run(source,cfg,meta,saved,3000)
    result['teacher'], rows = run(source,cfg,meta,saved,3000,teacher=True,data=True)
    torch.save(rows,args.output/'teacher.pt')
    print('[VALIDATION_SIM] baseline/teacher',result['baseline'],result['teacher'],flush=True)
    x = torch.tensor(np.concatenate([r[0][:,:33] for r in rows]))
    y = torch.tensor(np.concatenate([r[1] for r in rows]))
    actor = deepcopy(source)
    if args.head_only:
        actor.requires_grad_(False)
        actor.predictor.mean_bias.requires_grad_(True)
    opt = torch.optim.Adam([p for p in actor.parameters() if p.requires_grad],lr=args.lr)
    for step in range(1,args.updates+1):
        ids = torch.randint(len(x),(256,))
        predicted = actor.get_mean_and_std(x[ids],training=False)[0].tanh()
        loss = torch.square(predicted-y[ids]).mean()
        opt.zero_grad(); loss.backward(); opt.step()
        if not args.head_only:
            with torch.no_grad():
                for module in actor.modules():
                    if hasattr(module,'normalize_parameters'):
                        module.normalize_parameters()
        if step%250==0 or step==args.updates:
            row,_ = run(actor,cfg,meta,saved,3000)
            row.update(update=step,loss=float(loss))
            result['candidates'].append(row)
            torch.save(actor.state_dict(),args.output/f'actor_{step}.pt')
            print('[VALIDATION_SIM]',row,flush=True)
            (args.output/'result.json').write_text(json.dumps(result,indent=2)+'\n')
    (args.output/'result.json').write_text(json.dumps(result,indent=2)+'\n')


if __name__=='__main__':
    main()
