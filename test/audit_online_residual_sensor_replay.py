"""DESKTOP_DRY_RUN: fix guard logging without altering archived G control outputs."""

import argparse
import json
from pathlib import Path
import sys

import numpy as np

sys.path.insert(0,str(Path(__file__).resolve().parent))
from eval_online_residual_gain import REPO,OnlineAlpha,WHEELS,sha256,write_json


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root',type=Path,required=True)
    args=parser.parse_args();root=args.root.resolve()
    assert root.is_relative_to(REPO/'docs/exp')
    results=[];maximum=0.
    for folder in ('online_mass','online_motor','online_contact','online_step','probe_control'):
        for r in map(json.loads,(root/folder/'results.jsonl').read_text().splitlines()):
            if not r['label'].startswith('G'):
                continue
            gain=OnlineAlpha(r['adaptive_config']);active=[]
            with np.load(root/folder/r['trace']) as stored:
                # Materialize once: NpzFile indexing decompresses on every read.
                trace={key:stored[key] for key in ('time','state','command_substeps',
                    'alpha_centre','accepted','rejected','alpha')}
                for tick,t in enumerate(trace['time']):
                    row=trace['command_substeps'][tick].astype(np.float32)
                    command_rms=float(np.sqrt(np.mean(row[:,WHEELS]**2)))
                    gain.observe(trace['state'][tick],command_rms,float(t))
                    active.append(gain.guard_active)
                    errors=[abs(gain.centre-trace['alpha_centre'][tick]),
                            abs(gain.accepted-trace['accepted'][tick]),abs(gain.rejected-trace['rejected'][tick])]
                    if tick+1<len(trace['time']):
                        alpha=gain.command_alpha(float(t),.02)
                        errors.append(abs(alpha-trace['alpha'][tick+1]))
                    maximum=max(maximum,max(errors))
                assert maximum==0.,(folder,r['trace'],maximum)
            results.append(dict(folder=folder,trace=r['trace'],label=r['label'],mismatch=r['mismatch'],seed=r['seed'],
                pitch_delta_rad=r['pitch_delta_rad'],guard_events=gain.guards,guard_active_fraction=float(np.mean(active)),
                guard_activation_events=[e for e in gain.events if e['reason']=='sensor_guard'],
                accepted=gain.accepted,rejected=gain.rejected,alpha_centre=gain.centre))
    write_json(root/'guard_sensor_replay.json',dict(execution_domain='DESKTOP_DRY_RUN',evidence_status='PASS',
        episodes=len(results),alpha_centre_update_max_error=maximum,results=results,
        updated_runner_sha256=sha256(REPO/'test/eval_online_residual_gain.py'),
        explanation='Logging-only guard latch correction. Replayed every recorded sensor/command tick; '
        'applied alpha, centre, accepted and rejected counts match original simulation exactly. '
        'Original results/traces/source snapshots preserved; corrected guards used only in analysis.'))
    print('[DESKTOP_DRY_RUN] PASS sensor replay',len(results),'episodes; max alpha/update error',maximum,flush=True)


if __name__=='__main__':
    main()
