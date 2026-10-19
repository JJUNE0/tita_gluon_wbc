"""VALIDATION_SIM: predeclared 900s diagnostic for very slow drift transients.

Original after60s gates remain reported. A separate terminal660..900s assessment
tests whether a much longer warmup reveals a stationary operating region.
"""

from concurrent.futures import ProcessPoolExecutor, as_completed
import json
from pathlib import Path
import argparse
import numpy as np

from eval_flash_constant_hold import job_run, metrics, GATES, StateRunner, REPO, CKPT, prepared_config, sha256, write


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--jobs',type=Path,help='Predeclared JSON list of900s jobs; terminal660..900s criteria remain fixed')
    args=parser.parse_args()
    out=args.output.resolve()
    if not out.is_relative_to(REPO/'docs/exp') or out.exists():
        parser.error('New evidence directory required')
    out.mkdir(parents=True)
    cfg=json.loads(prepared_config(CKPT).read_text())
    jobs=[dict(id=f's153_r{tau:.6f}_900s',seed=153,pitch=0.,pitch_index=1,
        tau=tau,approach='zero',duration=900.,probe=False) for tau in [.5,.5525,.6]]
    if args.jobs:
        jobs=json.loads(args.jobs.read_text())
    for job in jobs:
        assert job['duration']==900.
        job['terminal_start_s']=660.
    write(out/'manifest.json',dict(execution_domain='VALIDATION_SIM',evidence_status='NOT_TESTED',
        checkpoint_sha256=sha256(CKPT/'actor.pt'),onnx_sha256=sha256(prepared_config(CKPT).parent/'policy.onnx'),
        script_sha256=sha256(Path(__file__)),collector_sha256=sha256(REPO/'test/eval_flash_constant_hold.py'),
        jobs=jobs,gates=GATES,jobs_source_sha256=sha256(args.jobs) if args.jobs else None,
        reason='180s final average close to zero while block velocities vary; test much longer transients',
        primary='original after60s position/speed criteria retained unchanged',
        secondary='same thresholds applied to660..900s only, separately labelled long-warmup diagnostic',
        F1_enabled=False,no_LQR=True,no_model_refit=True))
    with ProcessPoolExecutor(max_workers=3) as pool:
        futures=[pool.submit(job_run,cfg,job,str(out)) for job in jobs]
        for f in as_completed(futures):f.result()
    terminal=[]
    for job in jobs:
        info=json.loads((out/job['id']/'results.json').read_text())
        stats=info['terminal_metrics']
        terminal.append(dict(tau=job['tau'],original_after60_gate=info['metrics']['operating_gate'],
            terminal660_900=stats))
    write(out/'terminal_summary.json',dict(execution_domain='DESKTOP_DRY_RUN',
        evidence_status='PASS' if any(r['terminal660_900']['operating_gate'] for r in terminal) else 'FAIL',
        results=terminal,note='Secondary long-warmup diagnostic; not a change to the original gates'))
    print('[DESKTOP_DRY_RUN] terminal',[(r['tau'],r['terminal660_900']['gt_v_mean_last60'],
        r['terminal660_900']['operating_gate']) for r in terminal],flush=True)


if __name__=='__main__':
    main()
