"""VALIDATION_SIM: .pt checkpoint -> verified export -> MuJoCo in one command."""

import argparse
from datetime import datetime
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
from zoneinfo import ZoneInfo

REPO = Path(__file__).resolve().parents[3]
PACKAGE = Path(__file__).resolve().parents[1]


def evidence_directory():
    directory = REPO / 'docs/exp' / datetime.now(ZoneInfo('Asia/Seoul')).strftime('%Y-%m-%d')
    directory.mkdir(parents=True, exist_ok=True)
    return directory


def record(result, kind):
    prefix = evidence_directory() / datetime.now(ZoneInfo('Asia/Seoul')).strftime(f'tita_{kind}_%H%M%S_%f')
    prefix.with_suffix('.json').write_text(json.dumps(result, indent=2) + '\n')
    prefix.with_name(prefix.name + '_summary.md').write_text(
        f"# TITA {kind}\n\nExecution Domain: VALIDATION_SIM\n\nEvidence Status: {result['evidence_status']}\n\n"
        f"Policy Checkpoint SHA256: {result.get('checkpoint_sha256', 'N/A')}\n\n"
        f"ONNX SHA256: {result.get('onnx_sha256', 'N/A')}\n\n"
        f"Observed metrics / behavior / log summary:\n\n```json\n{json.dumps(result, indent=2)}\n```\n")


def run_runtime(args):
    import rclpy
    from .sim2sim_node import Sim2SimNode
    cfg = json.loads(args._config.read_text())
    result = dict(execution_domain='VALIDATION_SIM', evidence_status='BLOCKED',
                  checkpoint=cfg['policy_interface']['checkpoint'],
                  checkpoint_sha256=cfg['policy_interface']['checkpoint_sha256'],
                  onnx_sha256=cfg['policy_interface']['onnx_sha256'], policy_steps=0, headless=args.headless,
                  residual_wheel_pd=args.residual_wheel_pd, fixed_residual_lqr=args.fixed_residual_lqr,
                  velocity_bias=args.velocity_bias, leg_action_filter=args.leg_action_filter,
                  leg_notch_hz=args.leg_notch_hz, leg_notch_q=args.leg_notch_q)
    node = None
    try:
        rclpy.init(args=['--ros-args', '-p', f'config:={args._config}', '-p', f'viewer:={str(not args.headless).lower()}',
                        '-p', f'residual_wheel_pd:={str(args.residual_wheel_pd).lower()}',
                        '-p', f'fixed_residual_lqr:={str(args.fixed_residual_lqr).lower()}',
                        '-p', f'velocity_bias:={str(args.velocity_bias).lower()}',
                        '-p', f'leg_action_filter:={args.leg_action_filter}',
                        '-p', f'leg_notch_hz:={args.leg_notch_hz}', '-p', f'leg_notch_q:={args.leg_notch_q}'])
        node = Sim2SimNode()
        result['leg_action_filter'] = node.leg_filter.mode
        if args.velocity_bias:
            result['velocity_bias_acquisition_s'] = node.residual.ACQUISITION_SECONDS
            result['velocity_bias_parameters'] = {
                key: getattr(node.residual.law, key)
                for key in ('kp', 'ki', 'tau', 'limit', 'slew', 'ramp', 'response_sign', 'seed_gain')}
            result['wheel_radius_m'] = node.residual.radius
            result['velocity_bias_source_sha256'] = hashlib.sha256(
                Path(__file__).with_name('velocity_bias.py').read_bytes()).hexdigest()
            result['residual_wheel_pd_source_sha256'] = hashlib.sha256(
                Path(__file__).with_name('residual_wheel_pd.py').read_bytes()).hexdigest()
        if args.headless:
            for _ in range(args.steps or 1000):
                node._step()
            result.update(evidence_status='PASS', detail='Finite MuJoCo playback completed; this is not a locomotion quality evaluation.')
        else:
            node.run_interactive()
            result.update(evidence_status='PASS', detail='Viewer closed cleanly; locomotion quality needs separate evaluation.')
    except KeyboardInterrupt:
        result.update(evidence_status='SUSPICIOUS', detail='Operator stopped playback.')
    except Exception as error:
        result.update(evidence_status='FAIL', detail=f'{type(error).__name__}: {error}')
        raise
    finally:
        rclpy.try_shutdown()
        if node:
            result['policy_steps'] = node.steps
            result['final_base_position_m'] = node.env.base_pos().tolist()
            threads = list(node.env._viewer_threads)
            node.env.close()
            result['viewer_threads_stopped'] = all(not thread.is_alive() for thread in threads)
            node.destroy_node()
        record(result, 'sim2sim')
        print('[VALIDATION_SIM] ' + json.dumps(result), flush=True)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--ckpt', type=Path, required=True,
                        help='PPO .pt, FlashSAC actor.pt, or FlashSAC model directory')
    parser.add_argument('--headless', action='store_true')
    parser.add_argument('--leg_action_filter', choices=['auto', 'none', 'ma2_legs', 'ma2_notch_legs'], default='auto',
                        help='auto restores the saved action filter; explicit modes override it for experiments')
    parser.add_argument('--leg_notch_hz', type=float, default=8.3)
    parser.add_argument('--leg_notch_q', type=float, default=3.)
    residual = parser.add_mutually_exclusive_group()
    residual.add_argument('--residual_wheel_pd', action='store_true',
                        help='Stop hold: kp=2, kv=24, ramp=1.5s, residual limit=2Nm total')
    residual.add_argument('--fixed_residual_lqr', action='store_true',
                          help='Frozen model_60000 M4: bias=0.4828Nm, correction limit=0.05Nm')
    residual.add_argument('--velocity_bias', action='store_true',
                          help='FlashSAC encoder/IMU velocity bias after 2 s zero-command hold, before wheel PD')
    parser.add_argument('--steps', type=int, help='Finite headless control steps; default: 1000')
    parser.add_argument('--prepare-only', action='store_true', help='Prepare and verify the policy without starting MuJoCo')
    parser.add_argument('--isaac-python', type=Path, default=Path.home() / 'isaac/env_isaaclab/bin/python')
    parser.add_argument('--mujoco-python', type=Path, default=Path.home() / 'venvs/cosim_ros2_jazzy/bin/python')
    parser.add_argument('--_prepare', action='store_true', help=argparse.SUPPRESS)
    parser.add_argument('--_runtime', action='store_true', help=argparse.SUPPRESS)
    parser.add_argument('--_config', type=Path, help=argparse.SUPPRESS)
    args = parser.parse_args(argv)
    if args.steps is not None and (args.steps < 1 or not args.headless):
        parser.error('--steps must be positive and used with --headless')
    if args._runtime:
        run_runtime(args)
        return
    from .checkpoint import describe_checkpoint, prepared_config, prepare_checkpoint
    try:
        path, _, _, _ = describe_checkpoint(args.ckpt)
    except ValueError as error:
        parser.error(str(error))
    if args._prepare:
        cfg_path = prepare_checkpoint(path, args.mujoco_python)
        record(json.loads((cfg_path.parent / 'manifest.json').read_text()), 'policy_export')
        return
    if not args.headless and not args.prepare_only and not sys.stdin.isatty():
        parser.error('Viewer keyboard mode requires a terminal; use --headless for a finite run')
    config = prepared_config(path)
    launch_file = PACKAGE / 'launch/sim2sim.launch.py'
    if config is None:
        subprocess.run([str(args.isaac_python), str(launch_file), '--ckpt', str(path), '--_prepare',
                        '--mujoco-python', str(args.mujoco_python)], check=True)
        config = prepared_config(path)
    if config is None:
        raise RuntimeError('Export verification did not produce a valid config')
    print(f'[VALIDATION_SIM] Checkpoint: {path}\nVerified interface: {config}', flush=True)
    if args.prepare_only:
        return
    command = ['/bin/bash', '--noprofile', '--norc', '-c', 'source "$1" || exit; shift; exec "$@"', 'sim2sim',
               '/opt/ros/jazzy/setup.bash', str(args.mujoco_python), str(launch_file),
               '--ckpt', str(path), '--_runtime', '--_config', str(config)]
    if args.headless:
        command += ['--headless', '--steps', str(args.steps or 1000)]
    if args.residual_wheel_pd:
        command += ['--residual_wheel_pd']
    if args.fixed_residual_lqr:
        command += ['--fixed_residual_lqr']
    if args.velocity_bias:
        command += ['--velocity_bias']
    command += ['--leg_action_filter', args.leg_action_filter]
    command += ['--leg_notch_hz', str(args.leg_notch_hz), '--leg_notch_q', str(args.leg_notch_q)]
    environment = os.environ.copy()
    environment.update(ROS_DOMAIN_ID='87', ROS_LOCALHOST_ONLY='1',
                       ROS_LOG_DIR=str(evidence_directory() / 'sim2sim_ros_logs'), PYTHONDONTWRITEBYTECODE='1')
    os.execvpe(command[0], command, environment)
