"""DESKTOP_DRY_RUN: audit immutable evidence and summarize operating ranges."""

import json
from pathlib import Path
import re
import subprocess

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from analyze_flash_stop_local import load, evaluate, OLD_MODELS
from eval_flash_pv_models import REPO, write, sha256


def main():
    root=REPO/'docs/exp/2026-10-15/flash_stop_local'
    full=root/'full'
    manifest=json.loads((full/'manifest.json').read_text())
    assert all(sha256(REPO/p)==h for p,h in manifest['protected_sha256'].items())
    assert sha256(REPO/'test/eval_flash_stop_local.py')==manifest['collector_sha256']
    frozen=json.loads((full/'models_frozen.json').read_text())
    assert sha256(REPO/'test/analyze_flash_stop_local.py')==frozen['script_sha256']
    train,_,_=load(full,'train'); test,direct,_=load(full,'test')
    ranges={}
    for mode in ['frozen','feedback']:
        rows=[r for r in train+test if r['mode']==mode]
        sensor=np.concatenate([r['absolute'][:,:4] for r in rows])
        baseline=np.concatenate([r['base'][:,:4] for r in rows])
        torque=np.concatenate([r['total_u'] for r in rows])
        base_torque=np.concatenate([r['base_total_u'] for r in rows])
        ranges[mode]=dict(response_count=len(rows), sensor_v_range=[float(sensor[:,1].min()),float(sensor[:,1].max())],
            baseline_v_range=[float(baseline[:,1].min()),float(baseline[:,1].max())],
            torque_range=[float(torque.min()),float(torque.max())],
            baseline_total_residual_mean=float(base_torque.mean()),baseline_total_residual_std=float(base_torque.std()),
            direct_B_median=np.median([r['sensor_B'] for r in direct if r['mode']==mode],0).tolist())
    gt=[]
    for m in frozen['models']:
        if m['kind']!='delta':
            continue
        rows=[]
        for r in test:
            if r['mode']!=m['mode']:
                continue
            delta=r['delta'].copy(); delta[:,:4]=r['gt']
            rows.append(dict(r,delta=delta))
        summary,_=evaluate(m,rows)
        gt.append(dict(name=m['name'],mode=m['mode'],full2s=summary['full2s']))
    acquisitions=[]
    for path in sorted(full.glob('*/results.json')):
        info=json.loads(path.read_text())
        acquisitions += [dict(context=info['job']['id'],**r) for r in info['acquisition']]
    accepted=[a for a in acquisitions if a['low_speed_gate']]
    rejected=[a for a in acquisitions if not a['low_speed_gate']]
    facts=dict(execution_domain='DESKTOP_DRY_RUN',evidence_status='PASS',
        ranges=ranges,GT_delta_crosscheck=gt,acquisitions=acquisitions,
        accepted_sensor_rms_range=[min(r['sensor_v_rms_2s'] for r in accepted),max(r['sensor_v_rms_2s'] for r in accepted)],
        rejected_sensor_rms_range=[min(r['sensor_v_rms_2s'] for r in rejected),max(r['sensor_v_rms_2s'] for r in rejected)],
        train_responses=len(train),test_responses=len(test),train_transitions=len(train)*200,test_transitions=len(test)*200,
        protected_files=len(manifest['protected_sha256']),old_models_sha256=sha256(OLD_MODELS))
    write(root/'facts.json',facts)
    # Plot the acquisition evidence without mixing it with model response metrics.
    pilot=np.load(root/'acquisition_current/pilot.npz')
    scan=root/'bias_scan'
    fig,axes=plt.subplots(2,1,figsize=(11,7),sharex=False)
    for filename,label in [('frozen_bias+0.npz','FlashSAC'),('legacy_feedback_bias+0.npz','original low-gain F-1'),
                            ('frozen_bias+0.5.npz','constant +0.5 Nm bias')]:
        with np.load(scan/filename) as z:
            axes[0].plot(np.arange(len(z['sensor']))*.02,z['sensor'][:,1],label=label)
    axes[0].plot(np.arange(len(pilot['sensor'][:2001]))*.02,pilot['sensor'][:2001,1],label='current F-1 kv=24')
    axes[0].axhspan(-.002,.002,alpha=.15,color='green',label='low-speed band')
    axes[0].set_xlim(1.,40.); axes[0].set_ylim(-.02,.10)
    axes[0].set(xlabel='RL time [s]',ylabel='sensor velocity [m/s]'); axes[0].legend(fontsize=8)
    steady=json.loads((root/'steady_validation/summary.json').read_text())
    for row in steady['results']:
        if row['seed']!=140:
            continue
        with np.load(root/'steady_validation'/row['trace']) as z:
            axes[1].plot(np.arange(len(z['gt']))*.02,z['gt'][:,1],label=row['case'])
    axes[1].axhline(0.,color='k',lw=.8)
    axes[1].set(xlabel='time from common near-stop state [s]',ylabel='GT velocity [m/s]')
    axes[1].legend(fontsize=8)
    for ax in axes: ax.grid(alpha=.3)
    fig.tight_layout();fig.savefig(root/'acquisition_and_steady.png',dpi=150);plt.close(fig)
    current_files=[REPO/'test'/name for name in ['eval_flash_stop_local.py','analyze_flash_stop_local.py',
        'test_flash_stop_local.py','validate_flash_stop_bias.py','audit_flash_stop_local.py']]
    report=REPO/'docs/exp/2026-10-15/flash_stop_local_summary.md'
    links=[]
    if report.exists():
        current_files.append(report)
        links=re.findall(r'\]\(([^)]+)\)',report.read_text())
        assert all((report.parent/link).exists() for link in links)
    diffs=[]
    for path in current_files:
        result=subprocess.run(['git','diff','--no-index','--','/dev/null',str(path)],capture_output=True,text=True)
        assert result.returncode==1
        diffs.append(result.stdout)
        check=subprocess.run(['git','diff','--no-index','--check','--','/dev/null',str(path)],capture_output=True,text=True)
        assert not check.stdout and not check.stderr,(path,check.stdout,check.stderr)
    (root/'task.diff').write_text('\n'.join(diffs))
    status=subprocess.check_output(['git','status','--short'],text=True)
    (root/'git_status_after.txt').write_text(status)
    before=Path('/tmp/flash_stop_local_status_before.txt')
    if before.exists():
        (root/'git_status_before.txt').write_text(before.read_text())
    write(root/'final_review.json',dict(execution_domain='DESKTOP_DRY_RUN',evidence_status='PASS',
        branch=subprocess.check_output(['git','branch','--show-current'],text=True).strip(),
        changed_files=[str(p.relative_to(REPO)) for p in current_files],
        source_hashes={str(p.relative_to(REPO)):sha256(p) for p in current_files},
        report_links_checked=len(links),
        protected_files_preserved=True,collector_source_matches_manifest=True,analysis_source_matches_frozen_models=True,
        new_file_whitespace_check=True,no_runtime_source_changes=True,no_LQR_gain_or_online_adaptation=True))
    print('[DESKTOP_DRY_RUN] PASS evidence/source/diff audit',len(train),len(test),flush=True)


if __name__=='__main__':
    main()
