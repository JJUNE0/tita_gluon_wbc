"""DESKTOP_DRY_RUN: validate a registered torque export and its frozen Teacher."""
import hashlib
import json
import math
from pathlib import Path



def residual_parameters(selection,teacher_dir,leg_filter,velocity_bias):
    if not selection:return {}
    if leg_filter!='none' or velocity_bias:
        raise ValueError('Torque residual requires the saved Teacher with no extra action/velocity filter')
    teacher_dir=Path(teacher_dir)
    bundle=Path(selection).expanduser().resolve()
    if bundle.is_file() and bundle.name=='policy.onnx':bundle=bundle.parent
    raw=(bundle/'manifest.json').read_bytes()
    receipt=json.loads((bundle.parent/'bundle.json').read_text())
    if not receipt.get('hardware_export_validated'):
        raise ValueError('Residual has no validated hardware export')
    key=str((bundle/'manifest.json').relative_to(bundle.parent))
    if hashlib.sha256(raw).hexdigest()!=receipt['files'][key]:
        raise ValueError('Residual export manifest hash mismatch')
    saved=json.loads(raw)
    for path,digest in [(bundle/'policy.onnx',saved['onnx_sha256']),
                        (teacher_dir/'policy.onnx',saved['teacher_onnx_sha256']),
                        (teacher_dir/'config.json',saved['teacher_config_sha256'])]:
        if hashlib.sha256(path.read_bytes()).hexdigest()!=digest:
            raise ValueError('Residual/Teacher file hash mismatch: '+str(path))
    if saved['checkpoint_sha256']!=hashlib.sha256((bundle.parent/'residual.policy.pt').read_bytes()).hexdigest():
        raise ValueError('Residual checkpoint hash mismatch')
    filtering=saved.get('residual_torque_filter')
    cutoff=0.
    if filtering is not None:
        if not isinstance(filtering,dict):
            raise ValueError('Invalid residual filter contract')
        cutoff=filtering.get('cutoff_hz',0.)
        alpha=filtering.get('alpha',-1.)
        if (filtering.get('kind')!='one_pole_matched' or filtering.get('placement')!='residual_only'
                or filtering.get('update_hz')!=500
                or filtering.get('reset')!='zero_on_episode_reset_or_gate_loss'
                or filtering.get('actor_previous_residual')!='requested_pre_filter'
                or not isinstance(cutoff,(float,int)) or isinstance(cutoff,bool)
                or not math.isfinite(cutoff) or not 0<cutoff<250
                or not isinstance(alpha,(float,int)) or not math.isfinite(alpha)
                or not math.isclose(alpha,-math.expm1(-2*math.pi*cutoff/500),abs_tol=1e-8,rel_tol=0)):
            raise ValueError('Unsupported residual filter contract')
    cfg=json.loads((teacher_dir/'config.json').read_text())
    if cfg['policy_interface']['checkpoint_sha256']!=saved['teacher_checkpoint_sha256']:
        raise ValueError('Residual requires its frozen Teacher')
    if saved.get('residual_mode')!='torque' or (saved['actor_hz'],saved['teacher_hz'],saved['physics_hz'])!=(250,50,500):
        raise ValueError('Only the saved250Hz torque contract is deployed')
    sensor_mode=saved.get('actor_sensor_mode','original')
    if sensor_mode not in ('original','clean','teacher_shared'):
        raise ValueError('Unsupported residual sensor contract')
    ranges=saved['hardware_pose_command_ranges']
    if not saved['hardware_allow_pose_commands'] or ranges!=saved['training_pose_command_ranges']:
        raise ValueError('Hardware pose gate must match the trained ranges')
    return dict(residual_policy_path=str((bundle/'policy.onnx').resolve()),
        residual_lpf_hz=float(cutoff),
        residual_teacher_shared_sensors=sensor_mode=='teacher_shared',
        residual_action_mode=False,observation_dt=.004,residual_allow_pose_commands=True,
        residual_pose_command_min=[r[0] for r in ranges],residual_pose_command_max=[r[1] for r in ranges])
