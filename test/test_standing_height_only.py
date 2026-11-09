"""TRAINING_SIM: fixed standing height range, contact semantics and old playback."""

from copy import deepcopy
from pathlib import Path
import sys
from types import SimpleNamespace

import cloudpickle
import torch

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from mj_lab.checkpoint import plain, playback_contract
from mj_lab.robots.tita.sit_stand.sit_stand_env_cfg import TitaSitStandEnvCfg, curriculum_contact


def test_fixed_height_sampling_and_contacts_survive_old_curriculum_boundary():
    torch.manual_seed(42)
    cfg=TitaSitStandEnvCfg(4096)
    reference=deepcopy(cfg)
    cfg.curriculum_transition_step=None
    fake=SimpleNamespace(num_envs=4096,device='cpu',cfg=cfg)
    velocity=cfg.commands['base_velocity'].build(fake)
    pose=deepcopy(cfg.commands['base_pose']).build(fake)
    fake.command_manager=SimpleNamespace(get_term=lambda name:pose if name=='base_pose' else velocity)
    force=torch.zeros(4096,1,3,3)
    force[::2,...,2]=10.
    fake.scene={name:SimpleNamespace(data=SimpleNamespace(force_history=force)) for name in ('base','knees')}
    ids=torch.arange(4096)
    for step in (0,19999,20000,20001,100000,100001):
        assert not cfg.set_training_step(step,fake)
        assert cfg.curriculum_stage==1
        for command_cfg in (cfg.commands['base_pose'],pose.cfg):
            assert command_cfg.height_range==(.25,.5)
            assert command_cfg.height_target_bands is None
            assert command_cfg.height_motion_range is None
        pose.reset(ids)
        assert pose.target[:,2].min()>=.25 and pose.target[:,2].max()<=.5
        assert (pose.target[:,2]<.28).any() and (pose.target[:,2]>.48).any()
        assert (pose.target[:,:2].abs().amax(1)>.1).any()
        velocity._resample_command(ids)
        assert abs(float((velocity.target==0).all(1).float().mean())-.5)<.03
        for name in ('base','knees'):
            torch.testing.assert_close(curriculum_contact(fake,name),torch.arange(4096)%2==0)
    reference.curriculum_transition_step=None
    assert plain(cfg)==plain(reference)
    saved=cloudpickle.loads(cloudpickle.dumps(cfg))
    assert saved.curriculum_transition_step is None and not saved.set_training_step(100000)
    assert playback_contract(saved)['commands']['base_pose']['height_range']==[.25,.5]


def test_legacy_saved_full_sitting_schedule_is_preserved():
    cfg=TitaSitStandEnvCfg(1)
    assert cfg.curriculum_transition_step==20000
    assert cfg.set_training_step(20000)
    saved=cloudpickle.loads(cloudpickle.dumps(cfg))
    assert saved.curriculum_stage==2 and saved.commands['base_pose'].height_range==(.07,.5)
    assert not saved.set_training_step(100000)
