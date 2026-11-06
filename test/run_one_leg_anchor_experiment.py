"""TRAINING_SIM / VALIDATION_SIM: persistent independent runs and final W&B evidence."""

import argparse
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]


def complete_json(path):
    # Producers use ordinary writes. Skip an in-progress file this poll.
    try:
        return json.loads(path.read_text())
    except (OSError, json.JSONDecodeError):
        return None


def run_side(side, output, budget, label='', warm_start=None):
    prefix = 'one_leg_anchor'+('_'+label if label else '')
    mode = 'warmstart' if warm_start else 'scratch'
    name = f'tita_{prefix}_{side}_{mode}_{budget}_s42_20261103'
    command = [sys.executable, '-u', '-m', 'mj_lab.scripts.train', '--task', 'stand_one_leg_anchor_'+side,
        '--num_envs', '1024', '--steps', str(budget), '--seed', '42', '--buffer_size', '1000000',
        '--min_buffer', '100000', '--batch_size', '2048', '--updates_per_step', '2',
        '--save_every', '5000', '--log_every', '100', '--logger', 'wandb', '--wandb_mode', 'online',
        '--no-compile', '--no-amp',
        '--wandb_project', 'tita_flat_flash_sac', '--run_name', name,
        '--video_interval', '10000', '--video_length', '2000']
    if warm_start:
        command += ['--warm_start', str(warm_start)]
    state_path = output/f'{prefix}_{side}_state.json'
    state = dict(execution_domain='TRAINING_SIM', evidence_status='SUSPICIOUS', status='starting',
        initialization=('network warm start; fresh optimizer/replay/reward normalization'
                        if warm_start else 'from scratch; no resume or warm start'), command=command,
        policy_checkpoint_sha256='PENDING until first scheduled save', run_name=name)
    if warm_start:
        source = json.loads((warm_start/'ddt.json').read_text())
        state.update(warm_start_source=str(warm_start), source_actor_sha256=source['actor_sha256'])

    def save():
        state['updated_at'] = datetime.now().astimezone().isoformat()
        temp = state_path.with_suffix('.tmp')
        temp.write_text(json.dumps(state,indent=2)+'\n')
        temp.replace(state_path)

    save()
    environment = {**os.environ, 'OMP_NUM_THREADS':'1', 'OPENBLAS_NUM_THREADS':'1',
        'MKL_NUM_THREADS':'1', 'MUJOCO_GL':'egl', 'PYTHONUNBUFFERED':'1', 'PYTHONPATH':str(ROOT)}
    try:
        with (output/f'{prefix}_{side}_training.log').open('x') as stream:
            launch_evidence = ROOT/'docs/exp'/datetime.now().strftime('%Y-%m-%d')
            child = subprocess.Popen(command, cwd=ROOT, env=environment, stdout=stream, stderr=subprocess.STDOUT)
            state.update(status='training', pid=child.pid); save()
            args_file = None
            training_evidence = output
            while child.poll() is None:
                if args_file is None:
                    # A queued side may begin after midnight. The trainer
                    # writes under its own launch date, while queue state
                    # remains under the original experiment's directory.
                    candidates = set(output.glob('tita_mjlab_*_args.json'))
                    candidates.update(launch_evidence.glob('tita_mjlab_*_args.json'))
                    candidates.update((ROOT/'docs/exp'/datetime.now().strftime('%Y-%m-%d')).glob('tita_mjlab_*_args.json'))
                    for candidate in candidates:
                        if (complete_json(candidate) or {}).get('run_name') == name:
                            args_file = candidate
                            training_evidence = candidate.parent
                            state['run_id'] = candidate.name.removesuffix('_args.json')
                            state['training_evidence_directory'] = str(training_evidence)
                            state['checkpoint_directory'] = str(ROOT/'mj_lab/logs/flash_sac'/state['run_id'])
                            break
                if args_file:
                    run_id = state['run_id']
                    metric_file = training_evidence/(run_id+'_metrics.jsonl')
                    if metric_file.is_file():
                        lines = metric_file.read_text().splitlines()
                        if lines:
                            try:
                                state['latest_metrics'] = json.loads(lines[-1])
                            except json.JSONDecodeError:
                                pass
                    if not state.get('wandb_url'):
                        log = (output/f'{prefix}_{side}_training.log').read_text()
                        links = re.findall(r'https://[^\s\x1b]+/runs/[a-zA-Z0-9]+', log)
                        if links:
                            state['wandb_url'] = links[-1]
                    files = list((ROOT/'mj_lab/logs/flash_sac'/run_id).glob('model_*/ddt.json'))
                    if files:
                        latest = max(files,key=lambda p:int(p.parent.name.split('_')[-1]))
                        meta = complete_json(latest)
                        if meta:
                            state.update(policy_checkpoint_sha256=meta['actor_sha256'], latest_checkpoint=str(latest.parent))
                save()
                time.sleep(30)
        if child.returncode:
            raise RuntimeError(f'training exited {child.returncode}; see training log')
        if args_file is None:
            raise RuntimeError('No matching run provenance was observed')
        training = json.loads((training_evidence/(state['run_id']+'_result.json')).read_text())
        state.update(training_result=training, wandb_url=training['wandb_url'])
        if training['evidence_status'] != 'PASS' or training['step'] != budget:
            raise RuntimeError('Training incomplete or video/upload failures; see producer result')
        state.update(status='evaluating', policy_checkpoint_sha256=training['checkpoint_sha256']); save()
        evaluation_path = output/f'{prefix}_{side}_final_evaluation.json'
        with (output/f'{prefix}_{side}_evaluation.log').open('x') as stream:
            subprocess.run([sys.executable, '-u', str(ROOT/'test/evaluate_one_leg_anchor.py'),
                '--checkpoint', training['checkpoint'], '--output', str(evaluation_path),
                '--wandb-url', training['wandb_url'], '--artifact-name', name+'-final-evaluation'],
                cwd=ROOT, env=environment, stdout=stream, stderr=subprocess.STDOUT, check=True, timeout=1800)
        evaluation = json.loads(evaluation_path.read_text())
        if evaluation['policy_checkpoint_sha256'] != training['checkpoint_sha256']:
            raise RuntimeError('Final checkpoint/evaluation hash mismatch')
        upload = json.loads(evaluation_path.with_suffix('.upload.json').read_text())
        state.update(evaluation=evaluation, evaluation_artifact=upload['artifact'])
        state.update(status='completed', evidence_status='PASS', policy_quality=evaluation['policy_quality'])
        save()
    except BaseException as error:
        state.update(status='failed', evidence_status='FAIL', error=repr(error)); save()
        raise
    return state


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--evidence-dir', type=Path, required=True)
    parser.add_argument('--steps', type=int, default=100000)
    parser.add_argument('--label', default='', help='Separate state/log/artifact names for a replacement experiment')
    parser.add_argument('--sequential', action='store_true', help='Finish each side and its assessment before starting the next')
    parser.add_argument('--sides', nargs='+', choices=('left', 'right'), default=['left', 'right'])
    parser.add_argument('--left-warm-start', type=Path)
    parser.add_argument('--right-warm-start', type=Path)
    args = parser.parse_args()
    if args.label and not re.fullmatch('[a-z0-9_]+', args.label):
        parser.error('--label must contain lowercase letters, digits or underscores')
    if len(set(args.sides)) != len(args.sides):
        parser.error('--sides must not contain duplicates')
    prefix = 'one_leg_anchor'+('_'+args.label if args.label else '')
    output = args.evidence_dir.resolve()
    if not output.is_relative_to(ROOT/'docs/exp'):
        parser.error('Evidence must remain under docs/exp/YYYY-MM-DD')
    output.mkdir(parents=True, exist_ok=True)
    if any(output.glob(f'{prefix}_*_state.json')):
        parser.error('Existing run state found; refusing duplicate training launch')
    sources = {}
    for side in args.sides:
        source = getattr(args, side+'_warm_start')
        if source:
            source = source.resolve()
            meta = complete_json(source/'ddt.json')
            if (not meta or not (source/'env.pkl').is_file() or not (source/'actor.pt').is_file()
                    or meta.get('task') != 'stand_one_leg_anchor_'+side):
                parser.error(f'Invalid {side} warm-start checkpoint')
            if hashlib.sha256((source/'actor.pt').read_bytes()).hexdigest() != meta['actor_sha256']:
                parser.error(f'{side} warm-start actor hash mismatch')
        sources[side] = source
    if args.sequential:
        for index, side in enumerate(args.sides):
            queued = dict(execution_domain='TRAINING_SIM', evidence_status='NOT_TESTED', status='queued',
                queue_position=index, waiting_for=args.sides[:index], warm_start_source=str(sources[side]),
                source_actor_sha256=(complete_json(sources[side]/'ddt.json')['actor_sha256'] if sources[side] else None),
                policy_checkpoint_sha256='PENDING: training not started')
            (output/f'{prefix}_{side}_state.json').write_text(json.dumps(queued,indent=2)+'\n')
        results = []
        for index, side in enumerate(args.sides):
            try:
                results.append(run_side(side, output, args.steps, args.label, sources[side]))
            except BaseException:
                for pending in args.sides[index+1:]:
                    path = output/f'{prefix}_{pending}_state.json'
                    queued = json.loads(path.read_text())
                    queued.update(status='not_started_prior_side_failed', evidence_status='BLOCKED')
                    path.write_text(json.dumps(queued,indent=2)+'\n')
                raise
    else:
        with ThreadPoolExecutor(max_workers=len(args.sides)) as pool:
            jobs = [pool.submit(run_side, side, output, args.steps, args.label, sources[side]) for side in args.sides]
            results = [job.result() for job in jobs]
    (output/(prefix+'_completed.json')).write_text(json.dumps(results,indent=2)+'\n')


if __name__ == '__main__':
    main()
