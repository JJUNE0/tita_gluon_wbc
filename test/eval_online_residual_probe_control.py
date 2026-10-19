"""VALIDATION_SIM: same G exploration, centre frozen; separate probing from learning."""

import argparse
import json
from pathlib import Path
import sys
import time

sys.path.insert(0,str(Path(__file__).resolve().parent))
from eval_online_residual_gain import (REPO,ARCHIVE,ADAPTATION,run_episode,policy_config,
    read_yaml,Description,write_json,sha256)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args();output=args.output.resolve()
    if not output.is_relative_to(REPO/'docs/exp') or output.exists():
        parser.error('New docs/exp/ evidence directory required')
    output.mkdir(parents=True)
    cfg=json.loads((ARCHIVE/'config.json').read_text());parameters=json.loads((ARCHIVE/'manifest.json').read_text())['nominal_parameters']
    policy=policy_config();source=read_yaml(next(p for p in policy['policy_interface']['sources'] if p.endswith('env.yaml')))
    description=Description(source['scene']['robot']['spawn']['asset_path'])
    config=dict(ADAPTATION,centre_step=0.)
    conditions=[m for m in cfg['mismatches'] if m['name'] in ('nominal','mass_1.15','gain_0.8')]
    conditions.append(dict(name='step_gain_0.8',step_s=20.,step_motor_gain=.8))
    write_json(output/'manifest.json',dict(execution_domain='VALIDATION_SIM',evidence_status='NOT_TESTED',
        checkpoint_sha256=policy['policy_interface']['checkpoint_sha256'],conditions=conditions,
        adaptation=config,script_sha256=sha256(Path(__file__)),runner_sha256=sha256(REPO/'test/eval_online_residual_gain.py'),
        description='G exploration/guards/objective identical; centre cannot change; separate dither effects'))
    (output/'runner_source.txt').write_bytes(Path(__file__).read_bytes())
    count=0;started=time.monotonic()
    for mismatch in conditions:
        for seed in cfg['seeds']:
            for pitch in cfg['pitch_disturbances_rad']:
                r=run_episode(policy,cfg,description,parameters,mismatch,seed,pitch,'G-probe',output,
                    duration=60.,learn=True,adapt_config=config)
                assert r['alpha_centre_final']==1. and r['accepted_updates']==0
                with (output/'results.jsonl').open('a') as stream:
                    stream.write(json.dumps(r,allow_nan=False)+'\n')
                count+=1
                print(f'[VALIDATION_SIM] G-probe {mismatch["name"]} s{seed} p{pitch:+.3f} '
                    f'{r["evidence_status"]} drift={r["max_displacement_m"]:.4f} episodes={count} '
                    f'elapsed={time.monotonic()-started:.1f}s',flush=True)
    write_json(output/'completion.json',dict(execution_domain='VALIDATION_SIM',evidence_status='PASS',episodes=count))


if __name__=='__main__':
    main()
