"""DESKTOP_DRY_RUN / VALIDATION_SIM: self-contained published-pair contracts."""
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import numpy as np
import pytest
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT),str(ROOT/'sim2sim/sim2sim_ros2_jazzy')]
BASE=Path('mjlab/task/base_velocity/height_roll_pitch')
TEACHER=ROOT/'sim2sim/checkpoints'/BASE/'20261108/80000'
RESIDUAL=ROOT/'sim2sim/checkpoints'/BASE/'20261109/10000_d6672529ee24'

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

@pytest.mark.parametrize('domain',['sim2sim','sim2real'])
def test_selected_pair_has_all_hashed_artifacts_and_matches_teacher(domain):
    for day,step in [('20261108','80000'),('20261109','10000_d6672529ee24')]:
        folder=ROOT/domain/'checkpoints'/BASE/day/step
        bundle=json.loads((folder/'bundle.json').read_text())
        assert bundle['hardware_export_validated']
        for name,digest in bundle['files'].items():assert sha(folder/name)==digest,name
    spec=importlib.util.spec_from_file_location('published_residual_bundle',ROOT/'sim2real/tita_ws/src/tita_controller/launch/_residual_bundle.py')
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    values=module.residual_parameters(ROOT/domain/'checkpoints'/BASE/'20261109/10000_d6672529ee24/residual',ROOT/domain/'checkpoints'/BASE/'20261108/80000','none',False)
    assert values['residual_lpf_hz']==60 and values['residual_teacher_shared_sensors']
    assert values['observation_dt']==.004


def test_public_selection_and_training_recipe_do_not_require_local_logs():
    from sim2sim.checkpoint_store import selection
    for domain in ['sim2sim','sim2real']:
        for key in ['teacher','residual_torque']:assert selection(ROOT/domain/'config/policies.json',key).exists()
    reference=json.loads((ROOT/'mj_lab/config/residual_lpf60_10k.json').read_text())
    original=json.loads((RESIDUAL/'residual.json').read_text())
    assert reference['flash_sac_agent']==original['flash_sac_agent']
    assert sha(TEACHER/'policy.pt')==original['teacher_sha256']
    from sim2sim_ros2_jazzy.residual_policy import residual_metadata,residual_lpf_hz
    meta=residual_metadata(RESIDUAL/'residual.policy.pt',sha(TEACHER/'policy.pt'))
    assert residual_lpf_hz(meta)==60
    assert (meta['actor_hz'],meta['teacher_hz'],meta['physics_hz'])==(250,50,500)


def test_native_published_teacher_restores_lpf_environment():
    import torch
    if not torch.cuda.is_available():pytest.skip('Native integration requires CUDA')
    from mj_lab.robots.tita.residual.flat_env_residual_torque_lpf_delay import TitaFlatResidualTorqueLpfDelayEnvCfg,TitaFlatResidualTorqueLpfDelayEnv
    cfg=TitaFlatResidualTorqueLpfDelayEnvCfg(TEACHER,num_envs=4,seed=42,residual_lpf_hz=60,pose_command_mode='height_roll_pitch',pose_roll_deg=30,pose_pitch_deg=15)
    manifest=cfg.residual_manifest()
    assert manifest['residual_torque_filter']['cutoff_hz']==60
    env=TitaFlatResidualTorqueLpfDelayEnv(cfg)
    try:
        for _ in range(12):
            obs,*_=env.step(torch.zeros_like(env.residual))
            assert torch.isfinite(obs).all()
    finally:env.close()
