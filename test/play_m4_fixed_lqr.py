"""VALIDATION_SIM: display the archived nominal Fixed M4 entry controller.

Reuses the original controller, synchronized actor and 8-second RL prefix.
No ROS topics, hardware, online estimation or gain updates are involved.
"""
import argparse
import json
from pathlib import Path
import threading
import time

import numpy as np

from flash_overnight_control_stages import Runner, anchor, rollout_control
from flash_overnight_model_stages import REPO, CKPT, prepared_config, sha256

SOURCE = REPO / 'docs/exp/2026-10-15/flash_overnight_pipeline/run_final'
JOB = dict(id='entry_s270_p+0.000', seed=270, pitch=0., pitch_index=1)


class Restart(Exception):
    pass


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--headless', action='store_true', help='Exact 60s archive comparison without GUI')
    p.add_argument('--output', type=Path, default=REPO/'docs/exp/2026-10-16/m4_fixed_lqr_viewer')
    args = p.parse_args()
    out = args.output.resolve()
    assert out.is_relative_to(REPO/'docs/exp')
    out.mkdir(parents=True, exist_ok=True)
    gain_file = SOURCE/'gains_frozen.json'
    gain_hash = sha256(gain_file)
    gain = json.loads(gain_file.read_text())['models']['M4']
    assert len(gain['K']) == 24
    cfg = json.loads(prepared_config(CKPT).read_text())
    r = Runner(cfg, JOB)
    viewer = None
    events = []
    try:
        for i in range(400):
            if i >= 50:
                assert not r.failures()
            r.step(0.)
        snapshot, pre = r.snapshot(), anchor(r)
        target = float(r.observation['sensor'][0])
        if args.headless:
            counts = {}
            for group in ['M4', 'A']:
                r.restore(snapshot)
                trace, stats = rollout_control(r, group, gain if group == 'M4' else None,
                                              60., pre, target, ramp_bias=True)
                assert stats['complete']
                with np.load(SOURCE/'entry'/JOB['id']/(group+'.npz')) as archived:
                    assert set(trace) == set(archived.files)
                    for key, value in trace.items():
                        np.testing.assert_array_equal(value, archived[key], err_msg=key)
                    counts[group] = dict(arrays_exact=len(trace), metrics=stats)
            result = dict(execution_domain='VALIDATION_SIM', evidence_status='PASS',
                          checkpoint_sha256=sha256(CKPT/'actor.pt'), gain_sha256=gain_hash,
                          source_sha256=sha256(Path(__file__)), groups=counts)
            (out/'archive_verification.json').write_text(json.dumps(result, indent=2)+'\n')
            print('[VALIDATION_SIM] Exact M4 and FlashSAC 60s archive replay PASS', flush=True)
            return

        import mujoco.viewer
        pending, lock = [], threading.Lock()

        def key_callback(key):
            with lock:
                pending.append(key)

        viewer = mujoco.viewer.launch_passive(r.env.model, r.env.data, key_callback=key_callback,
                                             show_left_ui=False, show_right_ui=False)
        viewer.cam.lookat[:] = pre['base_position']+[0., 0., .1]
        viewer.cam.distance, viewer.cam.azimuth, viewer.cam.elevation = 2., 110., -22.
        original_step = r.step
        group, paused, tick, finished, last_u = 'M4', False, 0, False, 0.

        def display():
            displacement = np.linalg.norm(r.observation['base_position'][:2]-pre['base_position'][:2])
            viewer.set_texts([(None, None,
                'Controller\nTime / status\nBase planar displacement\nSensor p / v\nTotal residual\nKeys',
                f'{"Fixed M4 LQR" if group == "M4" else "FlashSAC only"} | model_60000\n'
                f'{tick*.02:.2f} / 60 s | {"FINISHED" if finished else ("PAUSED" if paused else "RUNNING")}\n'
                f'{displacement*100.:.3f} cm\n'
                f'{(r.observation["sensor"][0]-target)*1000.:+.3f} mm / '
                f'{r.observation["sensor"][1]*1000.:+.3f} mm/s\n{last_u:+.5f} Nm\n'
                'B: switch & reset | R: reset | Space: pause | Q/Esc: close')])
            viewer.sync()

        def handle_keys():
            nonlocal group, paused
            if not viewer.is_running():
                raise KeyboardInterrupt
            with lock:
                keys = pending[:]
                pending.clear()
            for key in keys:
                if key in [81, 256]:
                    raise KeyboardInterrupt
                if key == 32:
                    paused = not paused
                if key in [66, 82]:
                    if key == 66:
                        group = 'A' if group == 'M4' else 'M4'
                    raise Restart

        def visible_step(residual):
            nonlocal tick, last_u
            handle_keys()
            while paused:
                display()
                time.sleep(.02)
                handle_keys()
            start = time.monotonic()
            value = original_step(residual)
            tick += 1
            last_u = float(value['actual_u'])
            display()
            time.sleep(max(0., .02-(time.monotonic()-start)))
            return value

        r.step = visible_step
        print('[VALIDATION_SIM] VIEWER_RUNNING | Fixed M4 | B: baseline, R: reset, Space: pause, Q: quit', flush=True)
        while viewer.is_running():
            r.restore(snapshot)
            tick, finished, last_u = 0, False, 0.
            display()
            try:
                _, stats = rollout_control(r, group, gain if group == 'M4' else None,
                                           60., pre, target, ramp_bias=True)
                finished = True
                events.append(dict(group=group, **stats))
                (out/'viewer_results.json').write_text(json.dumps(dict(execution_domain='VALIDATION_SIM',
                    evidence_status='PASS' if all(x['complete'] for x in events) else 'FAIL',
                    episodes=events), indent=2)+'\n')
                print('[VALIDATION_SIM]', group, 'completed:', stats['complete'],
                      'max planar:', stats['max_planar_drift'], flush=True)
                while True:
                    handle_keys()
                    display()
                    time.sleep(.02)
            except Restart:
                continue
    except KeyboardInterrupt:
        print('[VALIDATION_SIM] Viewer closed', flush=True)
    finally:
        if viewer is not None:
            viewer.close()
        r.env.close()
        assert sha256(gain_file) == gain_hash


if __name__ == '__main__':
    main()
