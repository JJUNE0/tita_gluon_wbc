"""DESKTOP_DRY_RUN: serial queue starts the next side only after completion."""

import hashlib
import json
from pathlib import Path
import sys
from tempfile import TemporaryDirectory

import pytest

import run_one_leg_anchor_experiment as runner

ROOT = Path(__file__).resolve().parents[1]


@pytest.mark.parametrize('fail_left', [False, True])
def test_serial_queue_preserves_sources_and_does_not_start_right_early(monkeypatch, fail_left):
    with TemporaryDirectory(dir=ROOT/'test', prefix='.one_leg_serial_') as temporary:
        root = Path(temporary)
        output = root/'docs/exp/2026-11-03'
        output.mkdir(parents=True)
        sources = {}
        for side in ('left', 'right'):
            path = root/side
            path.mkdir()
            actor = (side+' actor').encode()
            (path/'actor.pt').write_bytes(actor)
            (path/'env.pkl').write_bytes(b'placeholder: no simulator in orchestration test')
            (path/'ddt.json').write_text(json.dumps(dict(task='stand_one_leg_anchor_'+side,
                actor_sha256=hashlib.sha256(actor).hexdigest())))
            sources[side] = path
        monkeypatch.setattr(runner, 'ROOT', root)
        monkeypatch.setattr(sys, 'argv', ['runner', '--evidence-dir', str(output), '--label', 'unit',
            '--sequential', '--steps', '16', '--left-warm-start', str(sources['left']),
            '--right-warm-start', str(sources['right'])])
        events = []

        def fake_side(side, destination, budget, label, source):
            assert budget == 16 and label == 'unit' and source == sources[side]
            events.append('start_'+side)
            if side == 'left':
                queued = json.loads((output/'one_leg_anchor_unit_right_state.json').read_text())
                assert queued['status'] == 'queued'
                assert queued['waiting_for'] == ['left']
                if fail_left:
                    raise RuntimeError('left assessment failed')
            else:
                assert events == ['start_left', 'finish_left', 'start_right']
            events.append('finish_'+side)
            return dict(side=side, status='completed')

        monkeypatch.setattr(runner, 'run_side', fake_side)
        if fail_left:
            with pytest.raises(RuntimeError, match='left assessment failed'):
                runner.main()
            assert events == ['start_left']
            queued = json.loads((output/'one_leg_anchor_unit_right_state.json').read_text())
            assert queued['status'] == 'not_started_prior_side_failed'
            assert not (output/'one_leg_anchor_unit_completed.json').exists()
        else:
            runner.main()
            assert events == ['start_left', 'finish_left', 'start_right', 'finish_right']
            result = json.loads((output/'one_leg_anchor_unit_completed.json').read_text())
            assert [row['side'] for row in result] == ['left', 'right']
