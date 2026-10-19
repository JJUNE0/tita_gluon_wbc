"""DESKTOP_DRY_RUN: compare deployment against the actual training observation on CPU.

Only Isaac types are stubbed; WheelPositionError's original Torch implementation
executes unchanged. No Isaac app, training process, or GPU is started.
"""
import importlib.util
from pathlib import Path
import sys
from types import ModuleType, SimpleNamespace
from unittest.mock import patch

import numpy as np
import torch

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / 'sim2sim/sim2sim_ros2_jazzy'))
from sim2sim_ros2_jazzy.adapter import NATIVE_JOINTS, ObservationBuilder, ObsState
from sim2sim_ros2_jazzy.checkpoint import describe_checkpoint


class ManagerBase:
    def __init__(self, cfg, env):
        self.cfg = cfg


def main():
    torch.set_num_threads(1)
    modules = {name: ModuleType(name) for name in (
        'isaaclab', 'isaaclab.assets', 'isaaclab.managers', 'isaaclab.utils', 'isaaclab.utils.math')}
    modules['isaaclab.assets'].Articulation = object
    modules['isaaclab.managers'].ManagerTermBase = ManagerBase
    modules['isaaclab.managers'].ObservationTermCfg = object
    modules['isaaclab.managers'].SceneEntityCfg = lambda name: SimpleNamespace(name=name)
    modules['isaaclab.utils.math'].sample_uniform = lambda low, high, shape, device: torch.full(shape, low, device=device)
    spec = importlib.util.spec_from_file_location('training_wheel_position_reference', REPO /
        'lab/ddt_lab/ddt_lab/tasks/manager_based/locomotion/robots/tita/real2sim/observations.py')
    module = importlib.util.module_from_spec(spec)
    with patch.dict(sys.modules, modules):
        spec.loader.exec_module(module)
    _, cfg, _, _ = describe_checkpoint(REPO / 'lab/ddt_lab/logs/flash_sac/tita_flash_sac_180212_290240/model_75000')
    params = cfg['policy_interface']['observations'][-1]['params']
    data = SimpleNamespace(joint_pos=torch.zeros(1, 8), root_quat_w=torch.tensor([[1., 0., 0., 0.]]))
    command = torch.zeros(1, 3)
    env = SimpleNamespace(num_envs=1, device='cpu',
        scene={'robot': SimpleNamespace(joint_names=NATIVE_JOINTS, data=data)},
        command_manager=SimpleNamespace(get_command=lambda name: command))
    term = module.WheelPositionError(SimpleNamespace(params=params), env)
    builder = ObservationBuilder(cfg)
    rng = np.random.default_rng(1842)
    q = np.zeros(8, dtype=np.float32)
    errors = []
    for i in range(3000):
        if i % 197 == 0:
            term.reset(); builder.reset()
        q += rng.normal(0, .01, 8).astype(np.float32)
        q[[3, 7]] += .2
        pitch = .2 * np.sin(i / 50)
        quat = np.array([np.cos(pitch/2), 0., np.sin(pitch/2), 0.], dtype=np.float32)
        cmd = np.zeros(3, dtype=np.float32)
        if i % 120 >= 80:
            cmd[:] = [.1, 0., 0.]
        if i % 120 == 79:
            cmd[:] = [.02, .02, .03]
        data.joint_pos[:] = torch.from_numpy(q)
        data.root_quat_w[:] = torch.from_numpy(quat)
        command[:] = torch.from_numpy(cmd)
        reference = float(term(env, command_name='base_velocity', **params)[0, 0]) * 5
        wrapped = q.copy()
        # Simulate a wrapping hardware encoder; preserve float64 wrapping accuracy.
        wrapped = wrapped.astype(np.float64)
        wrapped[[3, 7]] = (wrapped[[3, 7]] + np.pi) % (2*np.pi) - np.pi
        state = ObsState(wrapped, np.zeros(8), quat, np.zeros(3), cmd, np.zeros(8))
        actual = float(builder.build(state)[-1])
        errors.append(abs(actual-reference))
    maximum = max(errors)
    assert maximum < 1e-4, maximum  # <20 micrometres before scale; Torch float32 at up to 600 rad.
    print(f'[DESKTOP_DRY_RUN] PASS: original training WheelPositionError vs wrapped deployment, '
        f'3000 CPU samples, max scaled observation error {maximum:.3g}')


if __name__ == '__main__':
    main()
