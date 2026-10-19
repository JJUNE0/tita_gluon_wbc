"""VALIDATION_SIM: production Python notch on native 500/50 Hz MuJoCo harness.

Fresh MA2 baselines; no previous result is relabelled as a new rollout.
The preemphasis stress proxy is not an identified real 8 Hz plant model.
"""
import argparse
from concurrent.futures import ProcessPoolExecutor, as_completed
import copy
import itertools
import json
from pathlib import Path
import sys
import numpy as np

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'sim2sim/sim2sim_ros2_jazzy'))
from sim2sim_ros2_jazzy.adapter import LegActionFilter
import sim_leg_action_filter as harness

LEGACY=harness.ActionFilter


class CandidateFilter:
    def __init__(self,kind,gain):
        self.gain=gain;self.previous=None;self.legacy=None
        if kind=='ema0.5_legs':
            self.legacy=LEGACY(kind,gain)
        elif kind.startswith('notch:'):
            _,hz,q=kind.split(':')
            self.filter=LegActionFilter('ma2_notch_legs',list(range(8)),float(hz),float(q))
        else:
            self.filter=LegActionFilter(kind,list(range(8)))

    def __call__(self,raw):
        if self.legacy is not None:return self.legacy(raw)
        pe=raw.copy()
        if self.previous is not None:
            j=[0,1,2,4,5,6];pe[j]+=self.gain*(raw[j]-self.previous[j])
        self.previous=raw.copy()
        return self.filter.update(pe).astype(float)


def init():
    harness._init(str(harness.BUNDLE))
    harness.ActionFilter=CandidateFilter


def run(cfg,job):
    return harness.rollout(cfg,job)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--phase',choices=['screen','confirm','proxy'],required=True)
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--candidate',default='notch:8.3:3')
    args=parser.parse_args();out=args.output.resolve();out.mkdir(exist_ok=False)
    cfg=json.loads((harness.BUNDLE/'config.json').read_text())
    cfg['control']=dict(sim_timestep=.002,decimation=10)
    assert harness.vst.digest(harness.BUNDLE/'policy.onnx')==cfg['policy_interface']['onnx_sha256']
    jobs=[]
    def add(filters,plants,delays,scenarios,gains=(0.,),seeds=(42,)):
        for f,k,d,s,g,seed in itertools.product(filters,plants,delays,scenarios,gains,seeds):
            jobs.append(dict(scenario=s,gains='knee92',filter=f,preemphasis=g,
                leg_scale=(1.,1.,k),friction='none',delay_ticks=d,seed=seed))
    if args.phase=='screen':
        filters=['none','ma2_legs','ema0.5_legs']+[f'notch:{hz}:{q}' for hz in (7.5,8.3,9.) for q in (2,3,4)]
        add(filters,[.65],[0,6],['stand'])
    elif args.phase=='confirm':
        add(['ma2_legs',args.candidate],[.55,.65,.78],[0,6],['stand','drive'])
        add(['ma2_legs',args.candidate],[.65],[2,4],['stand','drive'])
        add(['ma2_legs',args.candidate],[.65],[0],['stand','drive'],seeds=(7,123))
    else:
        add(['ma2_legs',args.candidate],[.65],[0,2],['stand'],gains=(.5,1.,1.5))
    manifest=dict(execution_domain='VALIDATION_SIM',checkpoint_sha256=cfg['policy_interface']['checkpoint_sha256'],
        onnx_sha256=cfg['policy_interface']['onnx_sha256'],phase=args.phase,jobs=jobs,
        sources={str(p.relative_to(ROOT)):harness.vst.digest(p) for p in [Path(__file__),
            ROOT/'sim2sim/sim2sim_ros2_jazzy/sim2sim_ros2_jazzy/adapter.py',Path(harness.__file__)]})
    (out/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    results=[]
    with ProcessPoolExecutor(4,initializer=init) as pool:
        futures={pool.submit(run,cfg,j):j for j in jobs}
        for future in as_completed(futures):
            result=future.result();results.append(result)
            (out/'results.json').write_text(json.dumps(results,indent=2)+'\n')
            print(f"VALIDATION_SIM {len(results)}/{len(jobs)} {result['id']} fault={result['fault']}",flush=True)
    print('COMPLETE',len(results),'faults',sum(bool(r['fault']) for r in results),flush=True)


if __name__=='__main__':main()
