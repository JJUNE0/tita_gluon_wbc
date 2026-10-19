"""VALIDATION_SIM: independently authorized M4 branch; old verdicts stay intact."""

import argparse
from datetime import datetime, timezone
import fcntl
import json
from pathlib import Path
import traceback

from m4_mismatch_stages import PREVIOUS, EFFECTS, authorize_m4, run_mismatch
from flash_overnight_model_stages import REPO, CKPT, prepared_config, write, sha256


def protected_inputs():
    files = list(PREVIOUS.rglob('*'))
    files += list((REPO/'test').glob('*overnight*.py'))
    files += list((REPO/'sim2sim/sim2sim_ros2_jazzy').rglob('*.py'))
    files += list((REPO/'sim2sim/lqr').glob('*.py'))
    cfg = prepared_config(CKPT)
    files += [CKPT/'actor.pt', cfg, cfg.parent/'policy.onnx']
    return {str(p.relative_to(REPO)):sha256(p) for p in files if p.is_file()}


def verify(hashes, root=REPO):
    for name, expected in hashes.items():
        if not (root/name).is_file() or sha256(root/name) != expected:
            raise RuntimeError('Protected evidence/source changed: '+name)


def stage_record(root, name, function, sources):
    """Completed FAILs and interrupted runs require inspection, never overwrite."""
    path = root/(name+'.json')
    if path.exists():
        record = json.loads(path.read_text())
        if record['status'] not in ['PASS', 'FAIL']:
            raise RuntimeError('Interrupted stage; evidence review required: '+name)
        verify(record['source_sha256'])
        verify(record['artifacts_sha256'], root)
        return record['result']
    dependencies = {str(p.relative_to(REPO)):sha256(p) for p in sources+[root/'plan.json']}
    write(path, dict(status='RUNNING', started_utc=datetime.now(timezone.utc).isoformat()))
    try:
        result = function()
        verify(dependencies)
    except Exception:
        result = dict(gate=False, exception=traceback.format_exc())
    result.update(execution_domain='VALIDATION_SIM',
        evidence_status='PASS' if result.get('gate') is True else 'FAIL')
    # Bind actual raw traces and matrices, not only summary JSONs.
    artifacts = {str(p.relative_to(root)):sha256(p) for p in root.rglob('*')
        if p.is_file() and p != path and p.name != 'coordinator.lock'}
    write(path, dict(status=result['evidence_status'], result=result,
        source_sha256=dependencies, artifacts_sha256=artifacts,
        finished_utc=datetime.now(timezone.utc).isoformat()))
    print('[VALIDATION_SIM]', name, result['evidence_status'], flush=True)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, required=True)
    parser.add_argument('--workers', type=int, default=3)
    parser.add_argument('--through', choices=['mismatch','shadow','adaptive'], default='adaptive')
    parser.add_argument('--smoke', action='store_true')
    parser.add_argument('--resume', action='store_true')
    args = parser.parse_args()
    root = args.root.resolve()
    assert root.is_relative_to(REPO/'docs/exp')
    if args.resume:
        plan = json.loads((root/'plan.json').read_text())
    else:
        assert not root.exists(); root.mkdir(parents=True)
        authorization = authorize_m4()
        write(root/'00_M4_authorization.json', authorization)
        plan = dict(execution_domain='VALIDATION_SIM', workers=args.workers,
            checkpoint_sha256=sha256(CKPT/'actor.pt'),
            protected_sha256=protected_inputs(), effects=EFFECTS,
            primary_model='M4', M5='failed entry comparison preserved, no follow-up application',
            reference='base_link origin primary, wheel midpoint secondary; original sensor odometry unchanged',
            mismatch_gate='All M4 trials and paired bias trials complete; each M4 base IAE <= paired bias IAE. Same old Stage5 predicate.',
            shadow_eligibility='All six Fixed M4 trials complete in that regime/condition; performance FAIL is retained.',
            shadow_gate='frozen sensor-only model: first2s and rolling0.1/0.5/1/2s p/v response NRMSE medians <=30%; Bv sign/error<=30%; finite covariance and excitation',
            adaptive_gate='Only a condition with shadow PASS; same bias/Q/R/cap/ramp/slew; independent actual-MuJoCo improvement required',
            LQR=json.loads((PREVIOUS/'plan.json').read_text())['LQR'],
            no_GT_identification=True, no_hardware=True, no_QR_search=True,
            smoke_only=args.smoke)
        write(root/'plan.json', plan)
    assert plan['smoke_only'] == args.smoke
    verify(plan['protected_sha256'])
    with (root/'coordinator.lock').open('w') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX|fcntl.LOCK_NB)
        sources = [Path(__file__).resolve(), REPO/'test/m4_mismatch_stages.py']
        mismatch = stage_record(root, '01_mismatch', lambda:run_mismatch(root,plan,args.smoke), sources)
        if args.smoke or args.through=='mismatch': return
        if 'exception' in mismatch:
            raise RuntimeError('Mismatch collection failed; shadow is not authorized')
        eligible = [name for name, result in mismatch['conditions'].items() if result['stable_completed']]
        if not eligible:
            write(root/'02_shadow.json', dict(status='NOT_TESTED', reason='No stable Fixed M4 condition', eligible=[]))
            write(root/'03_adaptive.json', dict(status='NOT_TESTED', reason='No shadow PASS'))
            return
        from m4_shadow_stages import run_shadow
        shadow = stage_record(root, '02_shadow', lambda:run_shadow(root,plan,eligible),
            sources+[REPO/'test/m4_shadow_stages.py'])
        if args.through=='shadow': return
        if shadow.get('gate') is not True:
            write(root/'03_adaptive.json', dict(status='NOT_TESTED', reason='Shadow model validation failed; gain updates not enabled'))
        else:
            from m4_adaptive_stages import run_adaptive
            stage_record(root, '03_adaptive', lambda:run_adaptive(root,plan,shadow),
                sources+[REPO/'test/m4_shadow_stages.py',REPO/'test/m4_adaptive_stages.py'])
        verify(plan['protected_sha256'])


if __name__=='__main__':
    main()
