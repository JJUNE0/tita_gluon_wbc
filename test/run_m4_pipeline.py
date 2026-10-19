"""VALIDATION_SIM: clean M4-only mismatch -> shadow -> conditional adaptive run.

Earlier M4/M5 results are immutable prerequisites. Stable completion permits
shadow diagnosis even where fixed-control performance fails. Every adaptive
condition must independently pass the sensor-model validation gate.
"""
import argparse
import fcntl
import json
from pathlib import Path

from m4_mismatch_stages import PREVIOUS,authorize_m4
from m4_shadow_stages import run_shadow
from m4_adaptive_stages import run_adaptive
from run_m4_recovery_pipeline import collect
from run_m4_followup_pipeline import protected_inputs,stage_record,verify
from flash_overnight_model_stages import REPO,write,sha256


def continuation_conditions(mismatch):
    if not mismatch.get('collection_complete'):return []
    return [k for k,v in mismatch['conditions'].items() if k.startswith('settled/') and v['stable_completed']]


def execute(root,plan,through):
    sources=[Path(__file__).resolve()]+[REPO/'test'/name for name in
        ['m4_mismatch_stages.py','m4_control_utils.py','run_m4_recovery_pipeline.py','run_m4_followup_pipeline.py']]
    source=Path(plan['reuse_completed_source']) if plan['reuse_completed_source'] else root/'no_previous_collection'
    mismatch=stage_record(root,'01_mismatch',lambda:collect(root,plan,source),sources)
    eligible=continuation_conditions(mismatch)
    if through=='mismatch':return
    if not eligible:
        write(root/'02_shadow.json',dict(status='NOT_TESTED',reason='No completed stable settled Fixed M4 condition'))
        write(root/'03_adaptive.json',dict(status='NOT_TESTED',reason='No independent shadow PASS'));return
    shadow=stage_record(root,'02_shadow',lambda:run_shadow(root,plan,eligible),sources+[REPO/'test/m4_shadow_stages.py'])
    if through=='shadow':return
    if shadow.get('gate') is True:
        warm=stage_record(root,'03_adaptive',lambda:run_adaptive(root,plan,shadow),
            sources+[REPO/'test/m4_shadow_stages.py',REPO/'test/m4_adaptive_stages.py'])
        if 'exception' not in warm:
            # Preserve the warm comparison, then isolate online learning from
            # the help of a mismatch-trained initial prior in a separate run.
            from run_m4_coldstart_adaptive import run as run_cold
            cold=root/'cold_adaptive'
            if not cold.exists():
                cold.mkdir();write(cold/'plan.json',dict(plan,nominal_prior_only=True))
            stage_record(cold,'03_adaptive',lambda:run_cold(cold,plan,root,root),
                sources+[REPO/'test/run_m4_coldstart_adaptive.py',REPO/'test/m4_adaptive_stages.py',
                    REPO/'test/m4_shadow_stages.py',root/'03_adaptive.json'])
    elif not (root/'03_adaptive.json').exists():
        write(root/'03_adaptive.json',dict(status='NOT_TESTED',reason='No independently validated shadow condition'))


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root',type=Path,required=True)
    parser.add_argument('--workers',type=int,default=3)
    parser.add_argument('--through',choices=['mismatch','shadow','adaptive'],default='adaptive')
    parser.add_argument('--resume',action='store_true')
    parser.add_argument('--reuse-completed',type=Path)
    args=parser.parse_args();root=args.root.resolve()
    assert root.is_relative_to(REPO/'docs/exp')
    if args.resume:plan=json.loads((root/'plan.json').read_text())
    else:
        assert not root.exists();root.mkdir(parents=True)
        write(root/'00_authorization.json',authorize_m4())
        prior=json.loads((PREVIOUS/'plan.json').read_text())
        reuse=args.reuse_completed.resolve() if args.reuse_completed else None
        if reuse:
            source_plan=json.loads((reuse/'plan.json').read_text())
            assert source_plan['checkpoint_sha256']==prior['checkpoint_sha256']
            assert json.loads((reuse/'mismatch/manifest.json').read_text())['gain_sha256']==sha256(PREVIOUS/'gains_frozen.json')
            verify(source_plan['protected_sha256'])
            record=json.loads((reuse/'01_mismatch.json').read_text())
            assert record['status'] in ['PASS','FAIL']
            verify(record['source_sha256']);verify(record['artifacts_sha256'],reuse)
        plan=dict(execution_domain='VALIDATION_SIM',workers=args.workers,
            checkpoint_sha256=prior['checkpoint_sha256'],onnx_sha256=prior['onnx_sha256'],
            protected_sha256=protected_inputs(),LQR=prior['LQR'],
            reference='base_link primary, wheel midpoint secondary; unchanged rolling sensor state',
            reuse_completed_source=str(reuse) if reuse else None,
            mismatch_gate='same old Stage5: all M4 and paired bias complete and every M4 base IAE <= bias',
            shadow_gate='first2s and rolling0.1/0.5/1/2s p/v response NRMSE medians<=30%; direct Bv sign/error<=30%; information gate',
            shadow_scope='settled only, each condition requires6/6 stable fixed trials regardless of performance outcome',
            adaptive_gate='only condition-specific shadow PASS; actual gain acceptance and independent control benefit required',
            adaptive_primary='nominal-prior cold run; warm run preserved as initialization comparison',
            no_GT_identification=True,no_QR_search=True,no_hardware=True)
        write(root/'plan.json',plan)
    verify(plan['protected_sha256'])
    with (root/'coordinator.lock').open('w') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
        execute(root,plan,args.through)
        verify(plan['protected_sha256'])


if __name__=='__main__':main()
