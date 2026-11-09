"""TRAINING_SIM: wait for the current run to finish, then start the validated job."""
import argparse
import fcntl
import hashlib
import json
import os
from pathlib import Path
import subprocess
import time

ROOT=Path(__file__).resolve().parents[2]


def identity(pid):
    try:
        stat=Path(f'/proc/{pid}/stat').read_text().split(') ',1)[1].split()
        return dict(state=stat[0],start_ticks=int(stat[19]))
    except (FileNotFoundError,ProcessLookupError):
        return None


def predecessor_state(job):
    previous=job['predecessor']
    if previous.get('validation_receipt'):
        path=Path(previous['validation_receipt'])
        if not path.exists():return 'waiting'
        result=json.loads(path.read_text())
        if result.get('execution_domain')!='VALIDATION_SIM':
            return 'failed: predecessor receipt domain mismatch'
        if result.get('status')!='completed':
            return 'waiting' if result.get('status') in ('pending','running') else 'failed: validation did not complete'
        if result.get('evidence_status')!='PASS':
            return 'failed: validation receipt is not PASS'
        return 'ready'
    current=identity(previous['pid'])
    if current and current['start_ticks']==previous['start_ticks'] and current['state']!='Z':
        return 'waiting'
    path=Path(previous['output'])/'summary.json'
    if not path.exists():return 'failed: predecessor exited without summary'
    summary=json.loads(path.read_text())
    if (summary.get('status')!='completed' or summary.get('evidence_status')!='PASS'
            or summary.get('vector_step',0)<previous['required_steps']):
        return 'failed: predecessor did not complete successfully'
    if not str(summary.get('wandb_url') or '').endswith('/'+previous['wandb_run_id']):
        return 'failed: predecessor run identity mismatch'
    return 'ready'


def validate(job):
    assert subprocess.check_output(['git','branch','--show-current'],cwd=ROOT,text=True).strip() not in ('main','master'), 'Task branch required'
    path=Path(job['validation'])
    receipt=json.loads(path.read_text())
    assert receipt['evidence_status']=='PASS', 'Validation is not PASS'
    assert hashlib.sha256(path.read_bytes()).hexdigest()==job['validation_sha256'], 'Validation receipt changed'
    for name,sha in receipt['source_sha256'].items():
        assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==sha, 'Validated source changed: '+name
    command=job['command']
    assert command[1:3]==['-m','mj_lab.scripts.train_residual_torque'], 'Unexpected successor runner'
    output=Path(job['output']).resolve()
    assert output.is_relative_to(ROOT/'docs/exp') and not output.exists(), 'Successor output exists or is outside docs/exp'


def write(path,value):
    temporary=path.with_suffix('.tmp')
    temporary.write_text(json.dumps(value,indent=2)+'\n');temporary.replace(path)


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--job',type=Path,required=True)
    args=parser.parse_args();job=json.loads(args.job.read_text())
    folder=args.job.resolve().parent;status=folder/'status.json'
    with (folder/'watcher.lock').open('w') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
        if status.exists() and json.loads(status.read_text()).get('state') in ('started','startup_verified','completed'):
            raise RuntimeError('This job was already launched')
        try:
            validate(job)
            while True:
                state=predecessor_state(job)
                write(status,dict(execution_domain='TRAINING_SIM',evidence_status='NOT_TESTED',state=state,
                    watcher_pid=os.getpid(),predecessor_pid=job['predecessor']['pid'],successor_output=job['output'],updated_unix=time.time()))
                if state=='ready':break
                if state!='waiting':raise RuntimeError(state)
                time.sleep(20.)
            validate(job)
            environment=os.environ.copy();environment.update(job['environment'])
            with (folder/'successor.log').open('w') as log:
                process=subprocess.Popen(job['command'],cwd=ROOT,env=environment,stdout=log,stderr=subprocess.STDOUT,start_new_session=True)
            receipt=dict(execution_domain='TRAINING_SIM',evidence_status='NOT_TESTED',state='started',
                         watcher_pid=os.getpid(),successor_pid=process.pid,successor_output=job['output'],updated_unix=time.time())
            write(status,receipt)
            # A launched PID is not sufficient: verify initial state, fresh checkpoint
            # and several completed vector steps before reporting successful startup.
            while True:
                result=process.poll()
                progress=Path(job['output'])/'progress.json'
                initial=Path(job['output'])/'initial_state.json'
                if progress.exists() and initial.exists():
                    p=json.loads(progress.read_text());s=json.loads(initial.read_text())
                    if p.get('status') in ('running','completed') and p.get('vector_step',0)>=128:
                        config=json.loads((Path(job['output'])/'config.json').read_text())
                        assert config['initial_actor_updates']==0
                        assert list(Path(job['output']).glob('residual_00000000_*/actor.pt'))
                        assert s['common_lag_across_all_motors'] and s['native_reference_delay_disabled']
                        assert s['initial_force_active_worlds']==0
                        receipt.update(state='startup_verified',evidence_status='PASS',vector_step=p['vector_step'],
                                       wandb_url=p.get('wandb_url'),initial_state=s,updated_unix=time.time())
                        write(status,receipt);return
                if result is not None:raise RuntimeError('Successor exited before startup verification: '+str(result))
                time.sleep(2.)
        except BaseException as error:
            current=json.loads(status.read_text()) if status.exists() else {}
            current.update(execution_domain='TRAINING_SIM',evidence_status='FAIL',state='failed',
                           detail=repr(error),watcher_pid=os.getpid(),updated_unix=time.time())
            write(status,current)
            raise


if __name__=='__main__':main()
