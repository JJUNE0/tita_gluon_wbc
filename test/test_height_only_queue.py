"""DESKTOP_DRY_RUN: both predecessors must finish before one queued job starts."""

from datetime import datetime
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import time

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT/'scripts'), str(ROOT/'test')]
from queue_mjlab_flash_sac import process_identity
from test_mjlab_training_queue import checkpoint


def make_plan(root, delays=(.4, 1.4), bad_result=False):
    evidence = root/'docs/exp'/datetime.now().strftime('%Y-%m-%d')
    evidence.mkdir(parents=True)
    parents, dependencies = [], []
    for i, delay in enumerate(delays):
        path = root/f'parent_{i}/model_2'
        digest = checkpoint(path)
        result = root/f'parent_{i}_result.json'
        result.write_text(json.dumps(dict(step=2, evidence_status='FAIL' if bad_result and i==1 else 'PASS',
            checkpoint=str(path), checkpoint_sha256=digest)))
        parent = subprocess.Popen([sys.executable, '-c', f'import time; time.sleep({delay})'])
        identity = process_identity(parent.pid)
        assert identity is not None
        parents.append(parent)
        dependencies.append(dict(identity=identity, checkpoint=str(path), result_json=str(result), steps=2))
    target = root/'height/model_2'
    checkpoint(target)
    run_id, run_name = 'tita_mjlab_height_test', 'height_test'
    marker = evidence/'height_started'
    code = (
        'import json,time; from pathlib import Path; '
        f'e=Path({str(evidence)!r}); '
        f'(e/{(run_id+"_args.json")!r}).write_text(json.dumps({{"run_name":{run_name!r}}})); '
        f'(e/{(run_id+"_metrics.jsonl")!r}).write_text("{{\\\"step\\\":2}}\\n"); '
        f'(e/{(run_id+"_result.json")!r}).write_text(json.dumps({{"checkpoint":{str(target)!r},"evidence_status":"PASS","wandb_url":None}})); '
        f'with_marker=Path({str(marker)!r}); '
        'with_marker.write_text((with_marker.read_text() if with_marker.exists() else "")+str(time.time())+"\\n")'
    )
    plan = dict(repo=str(root), queue_id='height_queue_test', steps=2, dependencies=dependencies,
        jobs=[dict(task='height_only', run_name=run_name, argv=[sys.executable, '-c', code])],
        poll_seconds=.05, state_path=str(evidence/'state.json'), lock_path=str(root/'queue.lock'),
        manifest_path=str(evidence/'plan.json'), once=True)
    Path(plan['manifest_path']).write_text(json.dumps(plan))
    return plan, parents, marker


def invoke(plan):
    return [sys.executable, str(ROOT/'scripts/queue_mjlab_flash_sac.py'), '--manifest', plan['manifest_path']]


def cleanup(*processes):
    for process in processes:
        if process.poll() is None:
            process.kill()
        process.wait(timeout=5)


def test_waits_for_both_and_does_not_start_a_duplicate():
    with tempfile.TemporaryDirectory(dir=ROOT/'test') as temp:
        plan, parents, marker = make_plan(Path(temp))
        queue = subprocess.Popen(invoke(plan), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        try:
            parents[0].wait(timeout=5)
            assert parents[1].poll() is None
            assert not marker.exists()
            state = json.loads(Path(plan['state_path']).read_text())
            assert state['status'] == 'waiting_for_dependencies'
            assert len(state['dependencies']) == 2
            parents[1].wait(timeout=5)
            output = queue.communicate(timeout=10)[0].decode()
            assert queue.returncode == 0, output
            state = json.loads(Path(plan['state_path']).read_text())
            assert state['status'] == 'completed' and state['jobs'][0]['status'] == 'completed'
            assert len(marker.read_text().splitlines()) == 1
            again = subprocess.run(invoke(plan), capture_output=True, text=True, timeout=5)
            assert again.returncode == 0 and 'duplicate execution skipped' in again.stdout
            assert len(marker.read_text().splitlines()) == 1
        finally:
            cleanup(queue, *parents)


@pytest.mark.parametrize('failure', ['result_failure', 'checkpoint_corrupt'])
def test_does_not_launch_if_either_predecessor_failed(failure):
    with tempfile.TemporaryDirectory(dir=ROOT/'test') as temp:
        plan, parents, marker = make_plan(Path(temp), delays=(.1, .15), bad_result=failure=='result_failure')
        try:
            for process in parents:
                process.wait(timeout=5)
            if failure == 'checkpoint_corrupt':
                (Path(plan['dependencies'][1]['checkpoint'])/'actor.pt').write_bytes(b'corrupt')
            result = subprocess.run(invoke(plan), capture_output=True, text=True, timeout=5)
            assert result.returncode != 0
            state = json.loads(Path(plan['state_path']).read_text())
            assert state['status'] == 'failed' and state['evidence_status'] == 'FAIL'
            assert not marker.exists()
        finally:
            cleanup(*parents)
