"""VALIDATION_SIM / DESKTOP_DRY_RUN: shared local playback checkpoint registry.

Registration copies weights and saved contracts into both domain stores. It
does not change the selected config or approve a hardware export/deployment.
"""
from datetime import datetime
import fcntl
import hashlib
import json
from pathlib import Path
import re
import shutil
from zoneinfo import ZoneInfo

REPO = Path(__file__).resolve().parents[1]
SIDECARS = ('ddt.json', 'env.pkl', 'env.yaml', 'agent.json', 'agent.yaml',
            'mjlab_env.yaml', 'policy_interface.json', 'critic.pt', 'target_critic.pt',
            'temperature.pt', 'agent_state.pt', 'reward_normalizer.pt')


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def write_json(path, value):
    path = Path(path)
    temporary = path.with_suffix(path.suffix + '.tmp')
    temporary.write_text(json.dumps(value, indent=2) + '\n')
    temporary.replace(path)


def selection(config, name):
    config = Path(config).expanduser().resolve()
    value = json.loads(config.read_text())[name]
    path = Path(value).expanduser()
    return path.resolve() if path.is_absolute() else (config.parent / path).resolve()


def resolve_checkpoint(path):
    path = Path(path).expanduser().resolve()
    if path.is_dir() and (path / 'bundle.json').is_file():
        saved = json.loads((path / 'bundle.json').read_text())
        return path / saved['weight_file']
    if path.is_dir() and (path / 'latest.json').is_file():
        saved = json.loads((path / 'latest.json').read_text())
        value = Path(saved['checkpoint'])
        for candidate in (value,) if value.is_absolute() else (path / value, REPO / value):
            if candidate.is_file():
                return candidate
        raise FileNotFoundError('Missing latest checkpoint: ' + str(value))
    return path / 'actor.pt' if path.is_dir() else path


def _sidecar(path, name):
    for folder in (path.parent, path.parent / 'params', path.parent.parent,
                   path.parent.parent / 'params'):
        candidate = folder / name
        if candidate.is_file():
            return candidate
    return None


def _copy(source, destination):
    if destination.exists():
        if sha256(source) != sha256(destination):
            raise ValueError('Registered checkpoint content changed: ' + str(destination))
        return
    temporary = destination.with_suffix(destination.suffix + '.tmp')
    shutil.copyfile(source, temporary)
    temporary.replace(destination)


def _task(task):
    task = str(task)
    if task == 'flat_roll_pitch_height':
        return 'base_velocity', 'height_roll_pitch'
    if task == 'flat' or ('Velocity-Flat-Tita' in task):
        return 'base_velocity', 'default'
    return 'locomotion', re.sub(r'[^A-Za-z0-9_.-]+', '_', task).strip('._') or 'unknown'


def register_checkpoint(checkpoint, metadata=None, date=None):
    """Copy a selected Teacher/PPO or paired residual into both task registries."""
    source = resolve_checkpoint(checkpoint)
    residual = source.with_name('residual.json')
    is_residual = residual.is_file()
    if is_residual:
        saved = json.loads(residual.read_text())
        teacher = source.with_name('policy.pt')
        if not teacher.is_file() or not teacher.with_name('ddt.json').is_file():
            teacher_selection = saved.get('teacher_checkpoint') or saved.get('args', {}).get('teacher')
            if not teacher_selection:
                raise ValueError('Residual metadata is missing its Teacher checkpoint')
            teacher_path = Path(teacher_selection).expanduser()
            if not teacher_path.is_absolute():
                teacher_path = REPO/teacher_path
            teacher = resolve_checkpoint(teacher_path)
        teacher_meta = json.loads(teacher.with_name('ddt.json').read_text())
        metadata = dict(teacher_meta, step=saved['vector_step'])
        if saved['teacher_sha256'] != sha256(teacher):
            raise ValueError('Residual Teacher hash mismatch')
        if saved.get('policy_checkpoint_sha256', sha256(source)) != sha256(source):
            raise ValueError('Residual weight hash mismatch')
    else:
        teacher = source
        ddt = _sidecar(source, 'ddt.json')
        metadata = json.loads(ddt.read_text()) if ddt else dict(metadata or {})
        if not ddt and (source.parent/'bundle.json').is_file():
            registered = json.loads((source.parent/'bundle.json').read_text())
            metadata.setdefault('step', registered['step'])
            metadata.setdefault('task', registered['training_task'])
    if metadata.get('actor_sha256') and not is_residual and metadata['actor_sha256'] != sha256(source):
        raise ValueError('Policy weight hash mismatch')
    family, task = _task(metadata.get('task', 'unknown'))
    framework = 'mjlab' if metadata.get('backend') == 'mjlab' else 'isaaclab'
    step = metadata.get('step')
    if step is None:
        match = re.search(r'(?:model_|residual_)(\d+)', source.stem)
        if match is None:
            raise ValueError('Checkpoint step is missing; pass saved task/step metadata')
        step = int(match[1])
    day = date or datetime.now(ZoneInfo('Asia/Seoul')).strftime('%Y%m%d')
    if not re.fullmatch(r'\d{8}', day):
        raise ValueError('Registry date must be YYYYMMDD')
    digest = sha256(source)
    relative = Path(framework) / 'task' / family / task / day / str(int(step))
    results = {}
    for domain in ('sim2sim', 'sim2real'):
        store = REPO / domain / 'checkpoints'
        store.mkdir(parents=True, exist_ok=True)
        with (store / '.registry.lock').open('w') as lock:
            fcntl.flock(lock, fcntl.LOCK_EX)
            target = store / relative
            if (target / 'bundle.json').is_file():
                prior = json.loads((target / 'bundle.json').read_text())
                if prior['source_sha256'] != digest:
                    target = target.with_name(target.name + '_' + digest[:12])
            target.mkdir(parents=True, exist_ok=True)
            policy = target / 'policy.pt'
            _copy(teacher, policy)
            for name in SIDECARS:
                sidecar = _sidecar(teacher, name)
                if sidecar:
                    _copy(sidecar, target / name)
            # Native FlashSAC loaders use actor.pt; public config uses policy.pt.
            if (target / 'ddt.json').is_file() and not (target / 'actor.pt').exists():
                (target / 'actor.pt').symlink_to('policy.pt')
            weight = 'policy.pt'
            if is_residual:
                weight = 'residual.policy.pt'
                _copy(source, target / weight)
                _copy(residual, target / 'residual.json')
            receipt_path = target / 'bundle.json'
            prior = json.loads(receipt_path.read_text()) if receipt_path.exists() else {}
            files = dict(prior.get('files', {}))
            files.update({p.name: sha256(p) for p in target.iterdir()
                          if p.is_file() and p.name != 'bundle.json' and not p.name.endswith('.tmp')})
            receipt = dict(schema_version=1, execution_domain='DESKTOP_DRY_RUN', evidence_status='PASS',
                framework=framework, family=family, task=task, training_task=metadata.get('task', 'unknown'),
                date=day, step=int(step),
                role='residual_torque' if is_residual else 'policy', weight_file=weight,
                source_checkpoint=prior.get('source_checkpoint', str(source)), source_sha256=digest,
                teacher_checkpoint=prior.get('teacher_checkpoint', str(teacher)), teacher_sha256=sha256(teacher),
                hardware_export_validated=prior.get('hardware_export_validated', False), files=files)
            if is_residual:
                receipt['residual_mode'] = saved.get('residual_mode', 'torque')
                receipt['role'] = 'residual_' + receipt['residual_mode']
            write_json(receipt_path, receipt)
            results[domain] = target
    return results


def attach_hardware_export(target, policy_bundle, residual_bundle=None):
    """DESKTOP_DRY_RUN: attach an already validated export; never run hardware."""
    target, policy_bundle = Path(target), Path(policy_bundle)
    manifest = json.loads((policy_bundle / 'manifest.json').read_text())
    assert manifest['evidence_status'] == 'PASS'
    assert manifest['checkpoint_sha256'] == sha256(target / 'policy.pt')
    assert manifest['onnx_sha256'] == sha256(policy_bundle / 'policy.onnx')
    assert manifest['config_sha256'] == sha256(policy_bundle / 'config.json')
    exports = [(policy_bundle / name, target / name) for name in ('policy.onnx', 'config.json', 'manifest.json')]
    if residual_bundle is not None:
        residual = json.loads((Path(residual_bundle) / 'manifest.json').read_text())
        assert residual['evidence_status'] == 'PASS' and residual['residual_mode'] == 'torque'
        assert residual['checkpoint_sha256'] == sha256(target / 'residual.policy.pt')
        assert residual['teacher_checkpoint_sha256'] == manifest['checkpoint_sha256']
        assert residual['teacher_onnx_sha256'] == manifest['onnx_sha256']
        assert residual['teacher_config_sha256'] == manifest['config_sha256']
        assert residual['onnx_sha256'] == sha256(Path(residual_bundle) / 'policy.onnx')
        folder = target / 'residual'
        folder.mkdir(exist_ok=True)
        exports += [(Path(residual_bundle) / name, folder / name) for name in ('policy.onnx', 'manifest.json')]
    for source, destination in exports:
        _copy(source, destination)
    saved = json.loads((target / 'bundle.json').read_text())
    for _, destination in exports:
        saved['files'][str(destination.relative_to(target))] = sha256(destination)
    saved['hardware_export_validated'] = True
    write_json(target / 'bundle.json', saved)
    return target
