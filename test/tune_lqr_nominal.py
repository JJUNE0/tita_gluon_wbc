"""VALIDATION_SIM: bounded nominal-only Q/R and common leg PD validation."""

import copy
import json
from pathlib import Path
import sys
import numpy as np

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
from sim2sim.lqr.runtime import policy_config
from sim2sim.lqr.model import Description
from sim2sim.lqr.evaluate import episode, write_json
from sim2sim_ros2_jazzy.checkpoint import read_yaml

cfg = json.loads((REPO / 'sim2sim/lqr/config.json').read_text())
policy = policy_config()
source = read_yaml(next(p for p in policy['policy_interface']['sources'] if p.endswith('env.yaml')))
description = Description(source['scene']['robot']['spawn']['asset_path'])
parameters = description.nominal(policy['robot']['default_joint_angles'])
root = REPO / 'docs/exp/2026-10-14/lqr_ablation/nominal_tuning'
root.mkdir(exist_ok=False)
scores = []
for kp, kd in ((180., 6.), (360., 12.)):
    for cost in (.01, .1, 1.):
        for effort in (.1, 1.):
            trial = copy.deepcopy(cfg)
            trial['fixed_leg_kp'], trial['fixed_leg_kd'] = kp, kd
            trial['controller']['Q4'][0] = cost
            trial['controller']['R'] = effort
            name = f'kp{kp}_p{cost}_r{effort}'
            out = root / name
            out.mkdir()
            results = []
            for pitch in (-.035, .0, .035):
                for mode in ('C-3', 'C-4'):
                    result, _ = episode(policy, trial, description, parameters, mode, {'name':'nominal'}, 42, pitch, out)
                    results.append(result)
            score = sum(100*bool(r['failure'])+r['max_displacement_m']+10*r['pitch_rms_rad'] for r in results)
            scores.append(dict(name=name, score=score, failures=sum(bool(r['failure']) for r in results),
                               kp=kp, kd=kd, Q4=trial['controller']['Q4'], R=effort))
            write_json(out / 'results.json', results)
            print('[VALIDATION_SIM]',scores[-1],flush=True)
write_json(root / 'scores.json', sorted(scores,key=lambda x:x['score']))
