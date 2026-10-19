"""VALIDATION_SIM / DESKTOP_DRY_RUN: fail-closed, resumable experiment pipeline.

Stage artifacts are bound to the exact inputs/plan/source hashes. Failed gates
stop subsequent execution; a skipped experiment is never reported as PASS.
"""

import argparse
from datetime import datetime, timezone
import fcntl
import json
from pathlib import Path
import traceback

from eval_flash_pv_models import REPO, CKPT, prepared_config, write, sha256
from flash_overnight_model_stages import M5_ROOT, stage1, stage2

NAMES = {1:'identification',2:'independent_affine',3:'fixed_LQR',4:'drift_entry',
         5:'mismatch_robustness',6:'online_RLS_accuracy',7:'adaptive_LQR'}


def gate_passed(result):
    """Require a literal bool and finite completed evidence, never truthy text."""
    return result.get('gate') is True and result.get('evidence_status')=='PASS'


def allowed(state,stage):
    return all(state['stages'].get(str(i),{}).get('status')=='PASS' for i in range(1,stage))


def verify_record(root,record):
    if record['status'] not in ['PASS','FAIL']:return False
    path = root/record['artifact']
    if not path.is_file() or sha256(path)!=record['artifact_sha256']:
        raise RuntimeError('Stage evidence is missing or modified: '+str(path))
    result = json.loads(path.read_text())
    if record['status']=='PASS' and not gate_passed(result):
        raise RuntimeError('Stage record disagrees with actual gate')
    for p,h in record.get('dependencies',{}).items():
        if not Path(p).is_file() or sha256(p)!=h:
            raise RuntimeError('Stage dependency modified: '+p)
    for p,h in record.get('artifacts_sha256',{}).items():
        path=root/p
        if not path.is_file() or sha256(path)!=h:
            raise RuntimeError('Validated stage output modified: '+str(path))
    return True


def artifact_hashes(root,stage):
    """Bind cached gates to the actual matrices, gains, snapshots and raw logs."""
    names={1:[],2:['affine_models_frozen.json','fresh'],
        3:['gains_frozen.json','control_pilot_summary.json','control_pilot','control','control_metrics.json'],
        4:['entry','entry_metrics.json'],5:['mismatch','mismatch_metrics.json']}[stage]
    files=[]
    for name in names:
        p=root/name
        if p.is_dir():files.extend(q for q in p.rglob('*') if q.is_file())
        elif p.is_file():files.append(p)
    return {str(p.relative_to(root)):sha256(p) for p in files}


def execute_stage(root,stage,plan):
    if stage==1:return stage1(root,plan)
    if stage==2:return stage2(root,plan)
    if stage in [3,4,5]:
        from flash_overnight_control_stages import stage3,stage4,stage5
        return {3:stage3,4:stage4,5:stage5}[stage](root,plan)
    raise RuntimeError('Optional stages6/7 are not enabled in this fixed-controller run')


def run_stages(root,plan,state,through,runner=execute_stage):
    for stage in range(1,through+1):
        key = str(stage)
        record = state['stages'].get(key,{})
        if record.get('status') in ['PASS','FAIL']:
            verify_record(root,record)
            if record['status']=='FAIL':break
            continue
        if not allowed(state,stage):break
        if record.get('status')=='RUNNING':
            # The exclusive OS lock is held now, so the previous coordinator is
            # gone; incomplete artifacts still need explicit recovery, not rerun.
            raise RuntimeError('Interrupted stage has incomplete evidence; inspect it before recovery: '+key)
        sources = [Path(__file__).resolve(),REPO/'test/flash_overnight_model_stages.py']
        if stage>=3:sources.append(REPO/'test/flash_overnight_control_stages.py')
        dependencies = {str(p):sha256(p) for p in sources+[root/'plan.json']}
        if stage>=2:dependencies[str(M5_ROOT/'models_frozen.json')] = sha256(M5_ROOT/'models_frozen.json')
        if stage>=3:dependencies[str(root/'affine_models_frozen.json')] = sha256(root/'affine_models_frozen.json')
        state['stages'][key] = dict(name=NAMES[stage],status='RUNNING',started_utc=datetime.now(timezone.utc).isoformat())
        write(root/'pipeline_state.json',state)
        try:
            result = runner(root,stage,plan)
            status = 'PASS' if result.get('gate') is True else 'FAIL'
            result.update(execution_domain='VALIDATION_SIM' if stage>=2 else 'DESKTOP_DRY_RUN',
                evidence_status=status,stage=stage,name=NAMES[stage])
            for p,h in dependencies.items():
                if sha256(p)!=h:raise RuntimeError('Source/plan changed during stage execution: '+p)
        except Exception:
            result = dict(execution_domain='VALIDATION_SIM',evidence_status='FAIL',gate=False,
                stage=stage,name=NAMES[stage],exception=traceback.format_exc())
            status = 'FAIL'
        path = root/f'{stage:02d}_{NAMES[stage]}.json'
        assert not path.exists(), 'Refusing to overwrite stage evidence'
        write(path,result)
        state['stages'][key].update(status=status,artifact=path.name,artifact_sha256=sha256(path),
            dependencies=dependencies,artifacts_sha256=artifact_hashes(root,stage),
            finished_utc=datetime.now(timezone.utc).isoformat())
        write(root/'pipeline_state.json',state)
        print('[VALIDATION_SIM] stage',stage,NAMES[stage],status,flush=True)
        if status=='FAIL':break
    failed = [int(k) for k,v in state['stages'].items() if v['status']=='FAIL']
    for stage in range(1,8):
        if str(stage) not in state['stages'] or state['stages'][str(stage)]['status']=='NOT_TESTED':
            reason = ('prerequisite stage '+str(min(failed))+' failed' if failed else
                ('optional; not enabled' if stage>=6 else 'not yet requested by --through'))
            state['stages'][str(stage)] = dict(name=NAMES[stage],status='NOT_TESTED',reason=reason)
    state['terminal'] = bool(failed or all(state['stages'][str(i)]['status']=='PASS' for i in range(1,6)))
    state['scientific_success'] = all(state['stages'][str(i)]['status']=='PASS' for i in range(1,6))
    write(root/'pipeline_state.json',state)
    return state


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root',type=Path,required=True)
    parser.add_argument('--workers',type=int,default=3)
    parser.add_argument('--through',type=int,choices=range(1,6),default=5)
    parser.add_argument('--resume',action='store_true')
    args = parser.parse_args()
    root = args.root.resolve()
    assert root.is_relative_to(REPO/'docs/exp')
    if args.resume:
        plan = json.loads((root/'plan.json').read_text())
        state = json.loads((root/'pipeline_state.json').read_text())
        for p,h in plan['protected_sha256'].items():
            if sha256(REPO/p)!=h:raise RuntimeError('Protected input changed: '+p)
    else:
        assert not root.exists();root.mkdir(parents=True)
        cfg = prepared_config(CKPT)
        protected = list((REPO/'sim2sim/sim2sim_ros2_jazzy').rglob('*.py'))
        protected += list((REPO/'sim2sim/lqr').glob('*.py'))
        protected += list(M5_ROOT.glob('*.json'))+[cfg,cfg.parent/'policy.onnx',CKPT/'actor.pt']
        # These old arrays are actually read by the offset fit. Protect them as
        # well as the already frozen A/B; unrelated long prefixes need not be read.
        from flash_overnight_model_stages import SOURCE
        for p in M5_ROOT.glob('*/results.json'):
            info=json.loads(p.read_text())
            if info['job']['split']!='train':continue
            protected.append(p)
            for row in info['responses']:
                protected.extend([p.parent/row['trace'],p.parent/row['baseline'],
                    SOURCE/info['job']['id']/row['trace'],SOURCE/info['job']['id']/row['baseline']])
        plan = dict(execution_domain='VALIDATION_SIM',checkpoint_sha256=sha256(CKPT/'actor.pt'),
            onnx_sha256=sha256(cfg.parent/'policy.onnx'),workers=args.workers,
            protected_sha256={str(p.relative_to(REPO)):sha256(p) for p in protected},
            model_gate='median p/v NRMSE<=30%,first2s,rolling0.1/0.5/1/2s;directBv sign/error<=30%',
            affine_gate='same response gate; every fresh baseline2s p/v<=0.02mm/0.02mm/s,8s<=0.05mm/0.02mm/s',
            LQR=dict(Qp=250000.,Qv=250000.,R=400.,bias=.4828,cap=.05,ramp_s=1.5,slew=2.),
            reference='base_link origin primary; wheel midpoint secondary; unchanged sensor feedback',
            fixed_gate='both models: all complete and pitch/wheel limits; position AND kick base IAE<=80% bias, '
                'last5RMSE<=50% bias,paired wins>=80%;zero last5RMSE<=max(bias+0.05mm,0.1mm),absmeanv<=0.02mm/s',
            entry_gate='all complete; max planar drift<=80% bias;final5 base speed RMS<=0.2mm/s and '
                'base position range<=5mm; input/attitude guards',
            mismatch_gate='mass1.15/1.30,motorGain0.8/1.2,motorLag0.02/0.05;all complete and per-condition base IAE<=bias',
            optional6_7='NOT_TESTED unless fixed,entry,robustness stages pass and separately enabled in a later run',
            no_M6=True,no_QR_search=True,no_GT_control=True,
            note='Operational criteria, not user numerical specifications; all recorded before fresh collection.')
        write(root/'plan.json',plan)
        state = dict(execution_domain='VALIDATION_SIM',stages={},scientific_success=False,terminal=False)
    with (root/'coordinator.lock').open('w') as lock:
        try:fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
        except BlockingIOError:raise RuntimeError('Another coordinator currently holds the live OS lock')
        run_stages(root,plan,state,args.through)
        for p,h in plan['protected_sha256'].items():assert sha256(REPO/p)==h,p


if __name__=='__main__':
    main()
