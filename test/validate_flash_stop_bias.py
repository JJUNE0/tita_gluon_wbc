"""VALIDATION_SIM: held-out checks of measured bias and affine steady solutions.

Prescribed constant torques only, plus a separately labelled existing F-1 loop.
These validation results never change the frozen identification matrices.
"""

import argparse
import json
from pathlib import Path

import numpy as np

from eval_flash_stop_local import StopRunner, STATE_KEYS
from eval_flash_pv_models import CKPT, REPO, prepared_config, write, sha256


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--models', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    out = args.output.resolve()
    if not out.is_relative_to(REPO/'docs/exp') or out.exists():
        parser.error('New evidence directory required')
    out.mkdir(parents=True)
    models_hash = sha256(args.models)
    info = json.loads(args.models.read_text())
    cfg = json.loads(prepared_config(CKPT).read_text())
    cases = [('FlashSAC_zero', 0., 'frozen'), ('measured_bias', .5, 'frozen')]
    cases += [(name+'_affine_equilibrium', row['residual_input'], 'frozen')
        for name, row in info['affine_equilibrium'].items()]
    cases += [('bias_plus_F1', .5, 'feedback')]
    write(out/'manifest.json', dict(execution_domain='VALIDATION_SIM', evidence_status='NOT_TESTED',
        checkpoint_sha256=sha256(CKPT/'actor.pt'), onnx_sha256=sha256(prepared_config(CKPT).parent/'policy.onnx'),
        models_sha256=models_hash, script_sha256=sha256(Path(__file__)),
        seeds=[140, 141], pitch=0., cases=cases, prefix='same +0.5Nm bias until20s, F1 added20..22s',
        validation='30s, torque transitions slew2Nm/s, no parameter or matrix update'))
    results = []
    for seed in [140, 141]:
        runner = StopRunner(cfg, dict(seed=seed, pitch=0., pitch_index=1))
        try:
            for tick in range(1100):
                if tick < 1000:
                    runner.mode='frozen'; runner.bias=min(.5, runner.bias+.04)
                else:
                    runner.mode='feedback'; runner.feedback_bias=.5
                runner.step(0.)
                if tick >= 50:
                    assert not runner.failures(), (seed, tick, runner.failures())
            snapshot = runner.snapshot()
            runner.hold.update(np.zeros(3))
            initial_bias = .5+runner.hold.u
            for name, target, mode in cases:
                runner.restore(snapshot)
                runner.mode, runner.feedback_bias, runner.bias = mode, .5, initial_bias
                rows, steps, failure = [], [], []
                for tick in range(1501):
                    rows.append({key: runner.observation[key].copy() for key in STATE_KEYS})
                    failure=runner.failures()
                    if failure or tick==1500:
                        break
                    if mode=='frozen':
                        runner.bias=float(np.clip(target, runner.bias-.04, runner.bias+.04))
                    steps.append(runner.step(0.))
                trace={k:np.asarray([r[k] for r in rows]) for k in STATE_KEYS}
                trace.update({k:np.asarray([r[k] for r in steps]) for k in steps[0]})
                filename=f's{seed}_{name}.npz'
                np.savez_compressed(out/filename, **trace)
                sl=slice(-251,-1)
                result=dict(seed=seed, case=name, mode=mode, target_total_residual=target,
                    trace=filename, completed=not failure, failure=failure, duration_s=len(steps)*.02,
                    sensor_v_mean_last5s=float(trace['sensor'][sl,1].mean()),
                    gt_v_mean_last5s=float(trace['gt'][sl,1].mean()),
                    gt_v_rms_last5s=float(np.sqrt(np.mean(trace['gt'][sl,1]**2))),
                    total_residual_mean_last5s=float(trace['actual_u'][-250:].mean()),
                    gt_path_change=float(trace['gt'][-1,0]-trace['gt'][0,0]))
                results.append(result)
                print('[VALIDATION_SIM]', result, flush=True)
        finally:
            runner.env.close()
    assert sha256(args.models)==models_hash
    write(out/'summary.json', dict(execution_domain='VALIDATION_SIM', evidence_status='PASS',
        results=results, frozen_models_unchanged=True,
        scope='prediction validation, not a successful stop controller demonstration'))


if __name__=='__main__':
    main()
