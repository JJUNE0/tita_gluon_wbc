"""DESKTOP_DRY_RUN: pinned launch, corruption rejection, C++ states, native actor parity.

Run with system Python after sourcing ROS; --torch-python supplies the training environment.
No robot node, CAN socket, or actuator API is instantiated.
"""

import argparse
import importlib.util
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile

import numpy as np

REPO = Path(__file__).resolve().parents[2]
PACKAGE = REPO / 'sim2real/tita_ws/src/tita_controller'
BUNDLE = PACKAGE / 'policies/flashsac_50000'
CHECKPOINT = REPO / 'lab/ddt_lab/logs/flash_sac/tita_flash_sac_115632_883848/model_50000'


def load_launch(name):
    spec = importlib.util.spec_from_file_location(name, PACKAGE / 'launch' / f'{name}.launch.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def generate_reference(directory):
    import torch
    sys.path.insert(0, str(REPO / 'lab/ddt_lab/scripts/flash_sac'))
    from export import load_policy
    torch.set_num_threads(1)
    metadata = json.loads((CHECKPOINT / 'ddt.json').read_text())
    policy = load_policy(CHECKPOINT, metadata)
    observations = np.load(directory / 'obs.npy')
    with torch.no_grad():
        # Use native FlashSAC evaluation, independently of the ONNX wrapper's forward method.
        mean = policy.actor.get_mean_and_std(torch.from_numpy(observations), training=False)[0]
        action = mean.tanh()
        gains = torch.where(action >= 0, policy.action_gain_positive, policy.action_gain_negative)
        np.save(directory / 'expected.npy', (action * gains).numpy())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--torch-python', type=Path)
    parser.add_argument('--generate-reference', type=Path)
    args = parser.parse_args()
    if args.generate_reference:
        generate_reference(args.generate_reference)
        return
    if args.torch_python is None:
        parser.error('--torch-python is required')
    launch = load_launch('flashsac')
    launch.validate_policy(BUNDLE)
    generic = load_launch('tita')
    parameters = generic.policy_parameters(BUNDLE)
    assert len(parameters['obs_kind']) == 33
    assert parameters['policy_dt'] == .02
    assert parameters['action_joint'] == list(range(8))
    assert parameters['action_velocity'] == [False, False, False, True] * 2
    cfg = json.loads((BUNDLE / 'config.json').read_text())
    sys.path.insert(0, str(REPO / 'sim2sim/sim2sim_ros2_jazzy'))
    from sim2sim_ros2_jazzy.adapter import ObservationBuilder, ObsState
    rng = np.random.default_rng(50000)
    builder = ObservationBuilder(cfg)
    observations = []
    for _ in range(256):
        quaternion = rng.normal(size=4)
        quaternion /= np.linalg.norm(quaternion)
        state = ObsState(
            np.array(cfg['robot']['default_joint_angles']) + rng.normal(0, .2, 8),
            rng.normal(0, 2, 8), quaternion, rng.normal(0, 1, 3),
            rng.uniform(-.2, .2, 3), rng.uniform(-1, 1, 8))
        observations.append(builder.build(state))
    observations = np.array(observations, dtype=np.float32)
    with tempfile.TemporaryDirectory(dir=REPO / 'test/sim2real', prefix='flashsac_setup_') as tmp:
        directory = Path(tmp)
        # Both config and ONNX corruption must fail before launch can construct hardware nodes.
        for name in ('config.json', 'policy.onnx'):
            for source in BUNDLE.iterdir():
                (directory / source.name).write_bytes(source.read_bytes())
            with (directory / name).open('ab') as output:
                output.write(b'corrupted')
            try:
                launch.validate_policy(directory)
            except ValueError:
                pass
            else:
                raise AssertionError(f'{name} corruption was accepted')
        np.save(directory / 'obs.npy', observations)
        np.savetxt(directory / 'obs.txt', observations)
        subprocess.run([str(args.torch_python), __file__, '--generate-reference', str(directory)], check=True)
        ort = REPO / 'sim2real/tita_ws/build/tita_controller/_deps/onnxruntime-src'
        binary = directory / 'runtime'
        subprocess.run([
            'g++', '-std=c++17', '-O2', '-I', str(PACKAGE / 'include'), '-I', str(ort / 'include'),
            str(REPO / 'test/sim2real/flashsac_runtime.cpp'), '-L', str(ort / 'lib'),
            f'-Wl,-rpath,{ort / "lib"}', '-lonnxruntime', '-o', str(binary),
        ], check=True)
        result = subprocess.run([str(binary), str(BUNDLE / 'policy.onnx'), str(directory / 'obs.txt')],
                                check=True, capture_output=True, text=True)
        actual = np.loadtxt(io.StringIO(result.stdout))
        expected = np.load(directory / 'expected.npy')
        np.testing.assert_allclose(actual, expected, rtol=1e-4, atol=2e-5)
        print(f'PASS: native PyTorch vs C++ ONNX, {len(actual)} samples, '
              f'max action error {np.max(np.abs(actual - expected)):.3e}')
    print('PASS: finite deterministic inference; original idle damping and torque limits; staged RL gate; fault damping')
    print('PASS: selected checkpoint hashes, 33 obs / 8 actions / 50 Hz; corrupt bundles rejected')


if __name__ == '__main__':
    main()
