"""VALIDATION_SIM: .pt checkpoint -> verified export -> MuJoCo in one command."""

import argparse
from datetime import datetime
import hashlib
import json
import math
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
    from geometry_msgs.msg import Twist, Vector3
    from .adapter import quat_wxyz_to_rpy
    from .sim2sim_node import Sim2SimNode
    cfg = json.loads(args._config.read_text())
    result = dict(execution_domain='VALIDATION_SIM', evidence_status='BLOCKED',
                  checkpoint=cfg['policy_interface']['checkpoint'],
                  checkpoint_sha256=cfg['policy_interface']['checkpoint_sha256'],
                  onnx_sha256=cfg['policy_interface']['onnx_sha256'], policy_steps=0, headless=args.headless,
                  residual_wheel_pd=args.residual_wheel_pd, fixed_residual_lqr=args.fixed_residual_lqr,
                  velocity_bias=args.velocity_bias, leg_action_filter=args.leg_action_filter,
                  leg_notch_hz=args.leg_notch_hz, leg_notch_q=args.leg_notch_q)
    result['support_mode'] = args.support_mode
    node = None
    try:
        pose_target = None
        if args.pose is not None:
            if 'pose_command' not in cfg:
                raise ValueError('--pose requires a roll/pitch/height command policy')
            pose_target = [math.radians(args.pose[0]), math.radians(args.pose[1]), args.pose[2]]
            for value, name in zip(pose_target, ('roll_range', 'pitch_range', 'height_range')):
                if not cfg['pose_command'][name][0] <= value <= cfg['pose_command'][name][1]:
                    raise ValueError(f'--pose {name} is outside the saved training range {cfg["pose_command"][name]}')
        ros_args = ['--ros-args', '-p', f'config:={args._config}', '-p', f'viewer:={str(not args.headless).lower()}',
                        '-p', f'residual_wheel_pd:={str(args.residual_wheel_pd).lower()}',
                        '-p', f'fixed_residual_lqr:={str(args.fixed_residual_lqr).lower()}',
                        '-p', f'velocity_bias:={str(args.velocity_bias).lower()}',
                        '-p', f'leg_action_filter:={args.leg_action_filter}',
                        '-p', f'leg_notch_hz:={args.leg_notch_hz}', '-p', f'leg_notch_q:={args.leg_notch_q}']
        if args.support_mode is not None:
            ros_args += ['-p', f'support_mode:={args.support_mode}']
        if args.learned_residual is not None:
            ros_args += ['-p', f'learned_residual:={args.learned_residual.resolve()}',
                         '-p', f'payload_mass:={args.payload_mass}', '-p', f'push_force:={args.push_force}']
            if args.lpf is not None:
                ros_args += ['-p', f'residual_lpf_hz:={args.lpf}']
        rclpy.init(args=ros_args)
        node = Sim2SimNode()
        if 'support_command' in cfg:
            result['support_mode'] = node.support_mode
        result['command_limits'] = node.command_ranges
        if node.pose_cfg is not None:
            result['pose_command_config'] = node.pose_cfg
        if pose_target is not None:
            node._cmd_pose_cb(Vector3(x=pose_target[0], y=pose_target[1], z=pose_target[2]))
        if args.headless:
            target = args.command or [0., 0., 0.]
            for value, name in zip(target, ('lin_vel_x', 'lin_vel_y', 'ang_vel_z')):
                low, high = node.command_ranges.get(name, [0., 0.])
                if not low <= value <= high:
                    raise ValueError(f'Command {name}={value} is outside the simulation limits [{low}, {high}] '
                                     '(tita.yaml capped by the trained range)')
            message = Twist()
            message.linear.x, message.linear.y, message.angular.z = target
            node._cmd_twist_cb(message)
            result['fixed_command'] = target
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
            if node.learned is not None:
                result['residual_checkpoint_sha256'] = node.learned.metadata['policy_checkpoint_sha256']
                result['residual_checkpoint'] = node.learned.metadata['checkpoint']
                result['residual_inferences'] = node.learned.inferences
                result['residual_disabled_ticks'] = node.learned.disabled_ticks
                mode = node.learned.metadata['residual_mode']
                result['residual_mode'] = mode
                result['residual_actor_hz'] = node.learned.metadata['actor_hz']
                result['residual_max_abs_nm'] = node.learned.maximum_residual.tolist()
                result['residual_gate_enabled'] = node.learned.enabled
                result['residual_nm'] = node.learned.residual.tolist()
                from .residual_policy import residual_lpf_hz
                trained_lpf = residual_lpf_hz(node.learned.metadata)
                result['residual_lpf_hz'] = node.learned.filter_hz
                result['residual_lpf_alpha'] = node.learned.filter_alpha
                result['residual_trained_lpf_hz'] = trained_lpf
                result['residual_lpf_matches_training'] = node.learned.filter_hz == trained_lpf
                result['residual_filtered_nm'] = node.learned.filtered_residual.tolist()
                result['payload_kg'] = node.disturbance.mass
                result['simulation_perturbations'] = node.env.perturbation_settings()
                result['residual_requested_enabled'] = node.disturbance.residual_enabled
                result['ui_setting_changes'] = node.disturbance.setting_changes
                node.disturbance.close()
            result['policy_steps'] = node.steps
            result['tilt_faults'] = node.tilt_faults
            result['final_state'] = node.sm.state
            if node.pose_cfg is not None:
                result['pose_target_rad_m'] = node.pose_target.tolist()
                result['pose_command_rad_m'] = node.pose_command.tolist()
                result['pose_actual_rad_m'] = [*quat_wxyz_to_rpy(node.env.base_quat())[:2].astype(float),
                                               float(node.env.base_pos()[2])]
            result['final_base_position_m'] = node.env.base_pos().tolist()
            threads = list(node.env._viewer_threads)
            node.env.close()
            result['viewer_threads_stopped'] = all(not thread.is_alive() for thread in threads)
            node.destroy_node()
        record(result, 'sim2sim')
        print('[VALIDATION_SIM] ' + json.dumps(result), flush=True)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--config', type=Path, default=REPO/'sim2sim/config/policies.json',
                        help='Policy selections; relative paths resolve beside this JSON')
    parser.add_argument('--ckpt', type=Path,
                        help='PPO .pt, FlashSAC actor.pt, or FlashSAC model directory')
    parser.add_argument('--with-torque-residual', action='store_true', help=argparse.SUPPRESS)
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
    parser.add_argument('--command', type=float, nargs=3, metavar=('VX', 'VY', 'WZ'),
                        help='Fixed headless velocity target, constrained by tita.yaml and the trained ranges')
    parser.add_argument('--support-mode', type=int, choices=(0, 1, 2),
                        help='Support command: 0 left, 1 right, 2 both (support checkpoints only)')
    parser.add_argument('--pose', type=float, nargs=3, metavar=('ROLL_DEG', 'PITCH_DEG', 'HEIGHT_M'),
                        help='Pose target in degrees/degrees/metres, ramped using the saved training rates')
    parser.add_argument('--prepare-only', action='store_true', help='Prepare and verify the policy without starting MuJoCo')
    parser.add_argument('--learned-residual', type=Path, help='Saved stop-only residual actor; requires its matching Teacher')
    parser.add_argument('--lpf', type=float, metavar='HZ',
                        help='Residual torque LPF at 500Hz: 0 disables, 0 < Hz < 250; default restores the saved cutoff')
    parser.add_argument('--payload-mass', type=float, default=2., help='Mouse attachment mass in kg,0..5')
    parser.add_argument('--push-force', type=float, default=20., help='Torso hold-button force in N,0..50')
    parser.add_argument('--isaac-python', type=Path, default=Path.home() / 'isaac/env_isaaclab/bin/python')
    parser.add_argument('--mujoco-python', type=Path, default=Path.home() / 'venvs/cosim_ros2_jazzy/bin/python')
    parser.add_argument('--_prepare', action='store_true', help=argparse.SUPPRESS)
    parser.add_argument('--_runtime', action='store_true', help=argparse.SUPPRESS)
    parser.add_argument('--_config', type=Path, help=argparse.SUPPRESS)
    args = parser.parse_args(argv)
    sys.path.insert(0, str(REPO))
    from sim2sim.checkpoint_store import selection, resolve_checkpoint, register_checkpoint
    if args.ckpt is None:
        args.ckpt = selection(args.config, 'teacher')
    if args.with_torque_residual and args.learned_residual is None:
        args.learned_residual = selection(args.config, 'residual_torque')
    candidate = resolve_checkpoint(args.ckpt)
    selected = candidate if candidate.is_file() else candidate/'actor.pt'
    if candidate.is_dir() and (candidate/'latest.json').is_file():
        latest = json.loads((candidate/'latest.json').read_text())
        if 'checkpoint' in latest:
            from .residual_policy import residual_checkpoint
            selected = residual_checkpoint(candidate)
    direct_residual = (selected.parent/'residual.json').is_file()
    if direct_residual:
        if args.learned_residual is not None:
            parser.error('Choose one residual checkpoint selector')
        from .residual_policy import residual_checkpoint
        selected = residual_checkpoint(candidate)
        saved = json.loads(selected.with_name('residual.json').read_text())
        args.learned_residual = selected
        paired_teacher = selected.with_name('policy.pt')
        args.ckpt = paired_teacher if paired_teacher.is_file() else Path(saved['teacher_checkpoint'])
    if args.lpf is not None:
        if not math.isfinite(args.lpf) or not 0 <= args.lpf < 250:
            parser.error('--lpf must be finite, 0 <= Hz < 250; 0 disables filtering')
        if args.learned_residual is None:
            parser.error('--lpf requires a learned torque residual')
    if args.learned_residual is not None:
        if (not math.isfinite(args.payload_mass) or not 0 <= args.payload_mass <= 5
                or not math.isfinite(args.push_force) or not 0 <= args.push_force <= 50):
            parser.error('Payload must be0..5kg and push force0..50N')
        if any((args.residual_wheel_pd, args.fixed_residual_lqr, args.velocity_bias)):
            parser.error('Choose learned residual or a wheel residual controller')
        if args.leg_action_filter != 'auto':
            parser.error('Learned residual uses the saved Teacher action filter')
        if args.mujoco_python == parser.get_default('mujoco_python'):
            args.mujoco_python = Path.home()/'venvs/tita_mjlab/bin/python'
    # Torque actors use their saved history/Teacher contract rather than the
    # ordinary position/velocity action exporter.
    if args.steps is not None and (args.steps < 1 or not args.headless):
        parser.error('--steps must be positive and used with --headless')
    if args.command is not None and (not args.headless or not all(math.isfinite(v) for v in args.command)):
        parser.error('--command requires --headless and three finite velocity values')
    if args.pose is not None and not all(math.isfinite(v) for v in args.pose):
        parser.error('--pose requires three finite values: roll degrees, pitch degrees, height metres')
    if args._runtime:
        run_runtime(args)
        return
    from .checkpoint import describe_checkpoint, prepared_config, prepare_checkpoint
    try:
        path, _, _, _ = describe_checkpoint(args.ckpt)
    except ValueError as error:
        parser.error(str(error))
    stores = (REPO/'sim2sim/checkpoints', REPO/'sim2real/checkpoints')
    requested = resolve_checkpoint(args.learned_residual) if args.learned_residual is not None else path
    if not any(requested.is_relative_to(store) for store in stores):
        registered = register_checkpoint(requested)
        print('[DESKTOP_DRY_RUN] Checkpoint registered: '+str(registered['sim2sim']), flush=True)
    if args._prepare:
        cfg_path = prepare_checkpoint(path, args.mujoco_python)
        record(json.loads((cfg_path.parent / 'manifest.json').read_text()), 'policy_export')
        return
    if not args.headless and not args.prepare_only and not sys.stdin.isatty():
        parser.error('Viewer keyboard mode requires a terminal; use --headless for a finite run')
    config = prepared_config(path)
    launch_file = PACKAGE / 'launch/sim2sim.launch.py'
    if args.learned_residual is not None:
        launch_file = PACKAGE / 'launch/sim2sim.residual.torque.launch.py'
    if config is None:
        subprocess.run([str(args.isaac_python), str(launch_file), '--ckpt', str(path), '--_prepare',
                        '--mujoco-python', str(args.mujoco_python)], check=True)
        config = prepared_config(path)
    if config is None:
        raise RuntimeError('Export verification did not produce a valid config')
    print(f'[VALIDATION_SIM] Checkpoint: {path}\nVerified interface: {config}', flush=True)
    if args.learned_residual is not None:
        from .residual_policy import residual_metadata, residual_lpf_hz
        metadata = residual_metadata(args.learned_residual, json.loads(config.read_text())['policy_interface']['checkpoint_sha256'])
        print('[VALIDATION_SIM] Residual verified: '+json.dumps(metadata['policy_checkpoint_sha256']), flush=True)
        print(f'[VALIDATION_SIM] Residual-only LPF: {residual_lpf_hz(metadata, args.lpf):g} Hz (0 = bypass), update 500 Hz', flush=True)
    if args.prepare_only:
        return
    command = ['/bin/bash', '--noprofile', '--norc', '-c', 'source "$1" || exit; shift; exec "$@"', 'sim2sim',
               '/opt/ros/jazzy/setup.bash', str(args.mujoco_python), str(launch_file),
               '--ckpt', str(path), '--_runtime', '--_config', str(config)]
    if args.headless:
        command += ['--headless', '--steps', str(args.steps or 1000)]
        if args.command is not None:
            command += ['--command', *map(str, args.command)]
    if args.residual_wheel_pd:
        command += ['--residual_wheel_pd']
    if args.fixed_residual_lqr:
        command += ['--fixed_residual_lqr']
    if args.velocity_bias:
        command += ['--velocity_bias']
    if args.support_mode is not None:
        command += ['--support-mode', str(args.support_mode)]
    if args.pose is not None:
        command += ['--pose', *map(str, args.pose)]
    if args.learned_residual is not None:
        command += ['--learned-residual', str(args.learned_residual),
                    '--payload-mass', str(args.payload_mass), '--push-force', str(args.push_force)]
        if args.lpf is not None:
            command += ['--lpf', str(args.lpf)]
    command += ['--leg_action_filter', args.leg_action_filter]
    command += ['--leg_notch_hz', str(args.leg_notch_hz), '--leg_notch_q', str(args.leg_notch_q)]
    environment = os.environ.copy()
    environment.update(ROS_DOMAIN_ID='87', ROS_LOCALHOST_ONLY='1',
                       ROS_LOG_DIR=str(evidence_directory() / 'sim2sim_ros_logs'), PYTHONDONTWRITEBYTECODE='1')
    os.execvpe(command[0], command, environment)
