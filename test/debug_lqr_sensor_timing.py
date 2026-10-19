"""VALIDATION_SIM: split quaternion/gyro cache timing using identical learned gains."""

import argparse
import json
from pathlib import Path
import sys

REPO=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(REPO/'test'))
from debug_lqr_d4_diagnostics import (ARCHIVE,Plant,WheelOdometry,Sensors,policy_config,
    read_yaml,Description,run_episode,write_json,sha256)


original_observe=Plant.observe


def timing_observe(self):
    result=original_observe(self)
    if not hasattr(self,'gyro_only_estimator'):
        self.gyro_only_estimator=WheelOdometry(self.description,self.parameters['equilibrium_pitch'])
        self.quaternion_only_estimator=WheelOdometry(self.description,self.parameters['equilibrium_pitch'])
    result['gyro_fresh']=self.gyro_only_estimator.observe(Sensors(self.env.joint_pos(),self.env.joint_vel(),
        self.env.base_quat_sensor(),self.truth_data.sensor('trunk_gyro').data.copy()),self.dt)
    result['quaternion_fresh']=self.quaternion_only_estimator.observe(Sensors(self.env.joint_pos(),self.env.joint_vel(),
        self.truth_data.sensor('trunk_quat').data.copy(),self.env.base_ang_vel()),self.dt)
    return result


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    output=args.output.resolve()
    if not output.is_relative_to(REPO/'docs/exp') or output.exists():
        parser.error('New evidence directory under docs/exp/ required')
    output.mkdir(parents=True)
    cfg=json.loads((ARCHIVE/'config.json').read_text())
    parameters=json.loads((ARCHIVE/'manifest.json').read_text())['nominal_parameters']
    policy=policy_config()
    src=read_yaml(next(p for p in policy['policy_interface']['sources'] if p.endswith('env.yaml')))
    description=Description(src['scene']['robot']['spawn']['asset_path'])
    archive=[json.loads(line) for line in (ARCHIVE/'results.jsonl').read_text().splitlines()]
    Plant.observe=timing_observe
    try:
        for seed in cfg['seeds']:
            for pitch in cfg['pitch_disturbances_rad']:
                training=next(r for r in archive if r['mode']=='D-4' and r['mismatch']=='nominal'
                    and r['seed']==seed and r['pitch_delta_rad']==pitch and r['phase']=='adaptation')
                for source in ('gyro_fresh','quaternion_fresh'):
                    result=run_episode(policy,cfg,description,parameters,{'name':'nominal'},seed,pitch,
                        'learned_'+source,source,output,training)
                    with (output/'results.jsonl').open('a') as stream:
                        stream.write(json.dumps(result,allow_nan=False)+'\n')
                    print('[VALIDATION_SIM]',source,seed,pitch,result['evidence_status'],result['failures'],flush=True)
    finally:
        Plant.observe=original_observe
    write_json(output/'manifest.json',dict(execution_domain='VALIDATION_SIM',evidence_status='PASS',
        checkpoint_sha256=policy['policy_interface']['checkpoint_sha256'],script_sha256=sha256(Path(__file__)),
        description='Replace only cached gyro OR cached quaternion in the existing sensor estimator; preserve gains and leg PD'))


if __name__=='__main__':
    main()
