"""VALIDATION_SIM: actual new C++ controller in paired 20 s MuJoCo rollouts."""
import argparse
import json
from pathlib import Path
import subprocess
import sys
import tempfile

import numpy as np

REPO = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(REPO/'test'), str(REPO), str(REPO/'sim2sim/sim2sim_ros2_jazzy')]
from test_velocity_bias_08nm import CFG, GEO, PACKAGE, header
from velocity_bias_campaign import make_runner


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    trials = []
    with tempfile.TemporaryDirectory(dir=REPO/'test/sim2real', prefix='bounded_sim_') as temp:
        binary = Path(temp)/'runtime'
        subprocess.run(['g++', '-std=c++17', '-O2', '-Wall', '-Wextra', '-Werror', '-pedantic',
                        '-isystem', '/usr/include/eigen3', '-I', str(PACKAGE/'include'),
                        str(REPO/'test/sim2real/velocity_bias_runtime.cpp'), '-o', str(binary)], check=True)
        for condition, physics in [('nominal', {}), ('low_friction', {'friction': .2}),
                ('com_forward_mass115', {'com': .005, 'mass': 1.15}),
                ('com_backward_mass115', {'com': -.005, 'mass': 1.15})]:
            for bounded in (False, True):
                runner = make_runner(CFG, dict(seed=913, physics=physics))
                proc = subprocess.Popen([str(binary), 'status'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
                proc.stdin.write(' '.join(format(v, '.17g') for v in header())+'\n')
                proc.stdin.flush()
                samples = []
                origin = runner.observation['base_position'].copy()
                try:
                    for tick in range(1000):
                        o = runner.observation
                        row = [1., .02, 0., 0., 0., *runner.env.joint_pos(), *runner.env.joint_vel(),
                               *o['quat'], *o['gyro'], *runner.playback.last_action]
                        proc.stdin.write(' '.join(format(v, '.17g') for v in row)+'\n')
                        proc.stdin.flush()
                        actual = np.fromstring(proc.stdout.readline(), sep=' ')
                        assert len(actual) == 29
                        # ROS diagnostic fields are float32; restore the known double
                        # bound before feeding that telemetry back into a simulator.
                        bound = .8*GEO['wheel_radius']/max(CFG['robot']['joint_kd'][j] for j in (3, 7))
                        bias = float(np.clip(actual[6], -bound, bound)) if bounded else 0.
                        result = runner.step_bias(bias)
                        delta = result['motor']-result['baseline_motor']
                        # The Python adapter includes float32 targets; compare its
                        # two PD evaluations at a 1 micro-Nm numerical tolerance.
                        assert abs(delta[:, [3, 7]]).max() <= .8+1e-6
                        np.testing.assert_array_equal(delta[:, [0, 1, 2, 4, 5, 6]], 0.)
                        o = runner.observation
                        samples.append([tick*.02, o['base_position'][0]-origin[0],
                            o['base_position'][1]-origin[1], *o['rpy'][:2], float(o['base_velocity'][0]),
                            bias, float(actual[1]), float(actual[26]), float(abs(delta).max())])
                    a = np.array(samples)
                    assert np.isfinite(a).all()
                    stable = bool(abs(a[:, 3:5]).max() < .3)
                    tail = a[:, 0] >= 15
                    metrics = dict(condition=condition, bounded=bounded, execution_domain='VALIDATION_SIM',
                        evidence_status='PASS' if stable else 'SUSPICIOUS', duration_s=20.,
                        final_drift_m=float(np.linalg.norm(a[-1, 1:3])), max_tilt_deg=float(np.degrees(abs(a[:, 3:5]).max())),
                        final_5s_mean_speed_m_s=float(a[tail, 5].mean()), max_added_nm=float(a[:, 9].max()),
                        eligible_samples=int(a[:, 7].sum()), inhibited_samples=int(a[:, 8].sum()))
                    trials.append(metrics)
                    np.savez_compressed(args.output/f'sim_{condition}_{int(bounded)}.npz', values=a)
                    print(json.dumps(metrics), flush=True)
                finally:
                    runner.env.close()
                    proc.stdin.close()
                    proc.wait(timeout=5)
    (args.output/'mujoco_results.json').write_text(json.dumps(dict(
        execution_domain='VALIDATION_SIM', checkpoint_sha256=CFG['policy_interface']['checkpoint_sha256'],
        trials=trials, limitation='Short nominal/physics regression only; no hardware stability guarantee.'), indent=2)+'\n')


if __name__ == '__main__':
    main()
