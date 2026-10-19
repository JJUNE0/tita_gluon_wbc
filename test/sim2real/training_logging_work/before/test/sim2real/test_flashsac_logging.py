"""DESKTOP_DRY_RUN: mock ROS CLI to check mandatory logs and launch refusal paths."""

import os
import importlib.util
from pathlib import Path
import shutil
import signal
import subprocess
import tempfile
import time
import unittest
from unittest.mock import patch

REPO = Path(__file__).resolve().parents[2]

MOCK_ROS = '''#!/usr/bin/python3
import os, pathlib, signal, subprocess, sys, time
workspace=pathlib.Path(os.environ['MOCK_WORKSPACE'])
args=sys.argv[1:]
if args[:2]==['pkg','prefix']:
    print(workspace/'install/tita_controller')
elif args[:2]==['bag','record']:
    if os.environ.get('MOCK_BAG_FAIL')=='1':
        print('mock storage failure',flush=True)
        sys.exit(1)
    bag=pathlib.Path(args[args.index('--output')+1])
    bag.mkdir()
    (bag/'mock_0.db3').touch()
    signal.signal(signal.SIGINT, lambda *_: sys.exit(0))
    started=time.monotonic()
    try:
        while True:
            if os.environ.get('MOCK_BAG_DIES')=='1' and time.monotonic()-started>.3:
                sys.exit(3)
            time.sleep(.05)
    finally:
        (bag/'metadata.yaml').write_text('mock recorder finalized')
elif args[:2]==['launch','tita_controller']:
    if 'output_enabled:=true' in args:
        requests=workspace/'can_requests.txt'
        if not requests.exists() or len(requests.read_text().splitlines())!=2:
            print('mock controller started before Ready -> Direct requests',flush=True)
            sys.exit(4)
    (workspace/'launch_arguments.txt').write_text(' '.join(args))
    print('mock controller console',flush=True)
    if os.environ.get('MOCK_HANG_LAUNCH')=='1':
        ignore_int=os.environ.get('MOCK_IGNORE_INT')=='1'
        child_code='import time; time.sleep(120)'
        if ignore_int:
            child_code='import signal,time; signal.signal(signal.SIGINT, signal.SIG_IGN); time.sleep(120)'
        child=subprocess.Popen([sys.executable,'-c',child_code])
        signal.signal(signal.SIGINT, signal.SIG_IGN if ignore_int else lambda *_: sys.exit(0))
        time.sleep(.1)
        (workspace/'mock_processes.txt').write_text(str(os.getpid())+' '+str(child.pid))
        while True: time.sleep(.05)
    time.sleep(2 if os.environ.get('MOCK_BAG_DIES')=='1' else .4)
else:
    sys.exit(2)
'''

MOCK_SYSTEMCTL = '''#!/usr/bin/python3
import os,pathlib,sys
workspace=pathlib.Path(os.environ['MOCK_WORKSPACE'])
state_file=workspace/'service_state.txt'
state=state_file.read_text() if state_file.exists() else os.environ.get('MOCK_SERVICE_STATE','active')
if sys.argv[1:]==['is-active','tita-bringup.service']:
    print(state)
    sys.exit(0 if state=='active' else 3)
sys.exit(2)
'''

MOCK_SUDO = '''#!/usr/bin/python3
import os,pathlib,sys
workspace=pathlib.Path(os.environ['MOCK_WORKSPACE'])
if sys.argv[1:]!=['-n','/usr/bin/systemctl','stop','tita-bringup.service']:
    sys.exit(2)
(workspace/'stop_requested.txt').write_text('exact command authorized')
if os.environ.get('MOCK_STOP_FAIL')=='1':
    print('mock sudo denied',flush=True)
    sys.exit(1)
if os.environ.get('MOCK_STOP_NO_EFFECT')!='1':
    (workspace/'service_state.txt').write_text('inactive')
'''

MOCK_CANSEND = '''#!/usr/bin/python3
import os,pathlib,sys
workspace=pathlib.Path(os.environ['MOCK_WORKSPACE'])
if not list((workspace/'docs/exp').glob('*/*_bag/mock_0.db3')):
    print('mock CAN request before recorder ready',flush=True)
    sys.exit(2)
requests=workspace/'can_requests.txt'
with requests.open('a') as stream: stream.write(' '.join(sys.argv[1:])+'\\n')
if os.environ.get('MOCK_CAN_FAIL_AT')==str(len(requests.read_text().splitlines())):
    print('mock CAN request failure',flush=True)
    sys.exit(1)
'''


class FlashSACLoggingTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(dir=REPO / 'test/sim2real', prefix='logging_')
        self.addCleanup(self.temp.cleanup)
        self.workspace = Path(self.temp.name)
        shutil.copyfile(REPO / 'sim2real/tita_ws/run_flashsac.sh', self.workspace / 'run_flashsac.sh')
        binary_dir = self.workspace / 'bin'
        binary_dir.mkdir()
        for name, text in {
            'ros2': MOCK_ROS,
            'systemctl': MOCK_SYSTEMCTL,
            'sudo': MOCK_SUDO,
            'cansend': MOCK_CANSEND,
            'pgrep': '#!/usr/bin/env bash\n[[ ${MOCK_CONTROLLER_ACTIVE:-0} == 1 ]]\n',
        }.items():
            path = binary_dir / name
            path.write_text(text)
            path.chmod(0o755)
        policy = self.workspace / 'install/tita_controller/share/tita_controller/policies/flashsac_60000'
        policy.mkdir(parents=True)
        for name in ('policy.onnx', 'config.json'):
            (policy / name).write_text('mock artifact')
        geometry = policy.parents[1] / 'config/velocity_bias_geometry.json'
        geometry.parent.mkdir()
        geometry.write_text('mock geometry')
        self.env = {**os.environ, 'PATH': f'{binary_dir}:{os.environ["PATH"]}',
                    'MOCK_WORKSPACE': str(self.workspace), 'ROS_DISTRO': 'mock',
                    'TITA_INTERNAL_RUNNER': '1'}

    def run_runner(self, output='false', **env):
        return subprocess.run(['bash', str(self.workspace / 'run_flashsac.sh'), output],
                              env={**self.env, **env}, capture_output=True, text=True, timeout=15)

    def assert_logged(self, code):
        files = list((self.workspace / 'docs/exp').glob('*/*_summary.md'))
        self.assertEqual(len(files), 1)
        text = files[0].read_text()
        self.assertIn(f'Runner exit code: {code}', text)
        self.assertIn('Policy checkpoint SHA256:', text)
        self.assertTrue(list(files[0].parent.glob('*_console.log')))
        return files[0].parent, text

    def test_logs_and_bag_finalization_before_successful_exit(self):
        result = self.run_runner()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        directory, text = self.assert_logged(0)
        self.assertIn('ROBOT_STATE_CHANGING', text)
        self.assertIn('Output enabled: false', text)
        self.assertTrue((self.workspace / 'stop_requested.txt').exists())
        self.assertTrue(list(directory.glob('*_bag/metadata.yaml')))
        self.assertIn('output_enabled:=false', (self.workspace / 'launch_arguments.txt').read_text())
        self.assertFalse((self.workspace / 'can_requests.txt').exists())
        self.assertIn('MCU mode request: skipped', text)
        self.assertIn('tita.launch.py policy_dir:=', (self.workspace / 'launch_arguments.txt').read_text())
        self.assertTrue(any('mock controller console' in p.read_text() for p in directory.glob('*_console.log')))

    def test_explicit_output_selection_is_logged(self):
        result = self.run_runner('true')
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        _, text = self.assert_logged(0)
        self.assertIn('ROBOT_STATE_CHANGING', text)
        self.assertIn('output_enabled:=true', (self.workspace / 'launch_arguments.txt').read_text())
        self.assertEqual((self.workspace / 'can_requests.txt').read_text().splitlines(), [
            'can0 170##200000000000200000000',
            'can0 170##200000000000203000000',
        ])
        self.assertIn('MCU Direct request: transport accepted', text)

    def test_velocity_bias_forwarded_and_logged_with_output_disabled(self):
        result = self.run_runner(TITA_VELOCITY_BIAS='true', TITA_VELOCITY_BIAS_RESPONSE_SIGN='-1.0')
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        _, summary = self.assert_logged(0)
        self.assertIn('Velocity bias enabled: true', summary)
        self.assertIn('Velocity bias limit: +/-2 m/s', summary)
        self.assertIn('bias slew 3 m/s^2', summary)
        self.assertIn('Velocity bias response sign: -1.0', summary)
        self.assertIn('velocity_bias_geometry.json', summary)
        args = (self.workspace / 'launch_arguments.txt').read_text()
        self.assertIn('velocity_bias:=true', args)
        self.assertNotIn('velocity_bias_max_torque', args)
        self.assertIn('velocity_bias_response_sign:=-1.0', args)
        self.assertFalse((self.workspace / 'can_requests.txt').exists())

    def test_failed_ready_request_prevents_controller_start(self):
        result = self.run_runner('true', MOCK_CAN_FAIL_AT='1')
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        directory, _ = self.assert_logged(1)
        self.assertFalse((self.workspace / 'launch_arguments.txt').exists())
        self.assertEqual(len((self.workspace / 'can_requests.txt').read_text().splitlines()), 1)
        self.assertTrue(list(directory.glob('*_bag/metadata.yaml')))

    def test_failed_direct_request_prevents_controller_start(self):
        result = self.run_runner('true', MOCK_CAN_FAIL_AT='2')
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assert_logged(1)
        self.assertFalse((self.workspace / 'launch_arguments.txt').exists())
        self.assertEqual(len((self.workspace / 'can_requests.txt').read_text().splitlines()), 2)

    def test_recorder_failure_prevents_any_mode_request(self):
        result = self.run_runner('true', MOCK_BAG_FAIL='1')
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assert_logged(1)
        self.assertFalse((self.workspace / 'can_requests.txt').exists())


    def test_existing_controller_refuses_launch_and_keeps_log(self):
        result = self.run_runner(MOCK_CONTROLLER_ACTIVE='1')
        self.assertEqual(result.returncode, 1)
        self.assert_logged(1)
        self.assertFalse((self.workspace / 'launch_arguments.txt').exists())
        self.assertIn('refusing concurrent access', result.stdout)

    def test_failed_recorder_refuses_launch_and_keeps_log(self):
        result = self.run_runner(MOCK_BAG_FAIL='1')
        self.assertEqual(result.returncode, 1)
        directory, _ = self.assert_logged(1)
        self.assertFalse((self.workspace / 'launch_arguments.txt').exists())
        self.assertTrue(any('mock storage failure' in p.read_text() for p in directory.glob('*_bag_console.log')))

    def test_recorder_exit_stops_controller_and_preserves_logs(self):
        result = self.run_runner(MOCK_BAG_DIES='1')
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assert_logged(1)
        self.assertTrue((self.workspace / 'launch_arguments.txt').exists())
        self.assertIn('rosbag recorder stopped; stopping controller', result.stdout)

    def test_inactive_service_needs_no_sudo(self):
        result = self.run_runner(MOCK_SERVICE_STATE='inactive')
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertFalse((self.workspace / 'stop_requested.txt').exists())

    def test_sudo_denied_prevents_new_controller(self):
        result = self.run_runner(MOCK_STOP_FAIL='1')
        self.assertEqual(result.returncode, 1)
        self.assert_logged(1)
        self.assertFalse((self.workspace / 'launch_arguments.txt').exists())
        self.assertIn('no new controller was started', result.stdout)

    def test_service_still_active_prevents_new_controller(self):
        result = self.run_runner(MOCK_STOP_NO_EFFECT='1')
        self.assertEqual(result.returncode, 1)
        self.assert_logged(1)
        self.assertFalse((self.workspace / 'launch_arguments.txt').exists())
        self.assertIn('Bringup did not stop', result.stdout)

    def test_root_script_delegates_to_public_launch_without_recursion(self):
        result = self.run_runner(TITA_INTERNAL_RUNNER='0')
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn('flashsac.launch.py', (self.workspace / 'launch_arguments.txt').read_text())
        self.assertFalse((self.workspace / 'stop_requested.txt').exists())

    def interrupt_and_check_descendants(self, command, env, repeat_interrupt=False):
        def running(pid):
            try:
                return Path(f'/proc/{pid}/stat').read_text().split(') ', 1)[1][0] != 'Z'
            except FileNotFoundError:
                return False
        output = self.workspace / 'interrupt_console.log'
        children = []
        with output.open('w') as console:
            process = subprocess.Popen(command, env=env, stdout=console, stderr=subprocess.STDOUT,
                                       start_new_session=True)
            try:
                ready = self.workspace / 'mock_processes.txt'
                for _ in range(100):
                    if ready.exists(): break
                    if process.poll() is not None: break
                    time.sleep(.05)
                self.assertTrue(ready.exists(), output.read_text())
                children = [int(pid) for pid in ready.read_text().split()]
                os.killpg(process.pid, signal.SIGINT)
                if repeat_interrupt:
                    for _ in range(100):
                        if 'Stopping owned controller process group' in output.read_text(): break
                        if process.poll() is not None: break
                        time.sleep(.02)
                    self.assertIsNone(process.poll(), output.read_text())
                    self.assertIn('Stopping owned controller process group', output.read_text())
                    os.killpg(process.pid, signal.SIGINT)
                process.wait(timeout=18)
                for _ in range(40):
                    if not any(running(pid) for pid in children): break
                    time.sleep(.05)
                self.assertFalse(any(running(pid) for pid in children),
                                 f'Live orphan descendants: {children}\n{output.read_text()}')
                summaries = list((self.workspace / 'docs/exp').glob('*/*_summary.md'))
                self.assertTrue(summaries)
                self.assertIn('Finished:', summaries[0].read_text())
                self.assertTrue(list((self.workspace / 'docs/exp').glob('*/*_bag/metadata.yaml')))
            finally:
                # Only mock process IDs created by this test are eligible for cleanup.
                for pid in children:
                    if running(pid):
                        try: os.kill(pid, signal.SIGKILL)
                        except ProcessLookupError: pass
                if process.poll() is None:
                    os.killpg(process.pid, signal.SIGKILL)
                    process.wait()

    def test_ctrl_c_removes_inner_launch_and_grandchild(self):
        self.interrupt_and_check_descendants(
            ['bash', str(self.workspace / 'run_flashsac.sh'), 'false'],
            {**self.env, 'MOCK_HANG_LAUNCH': '1'})

    def test_public_launch_validates_before_configuring_logged_runner(self):
        from launch import LaunchContext
        module_path = REPO / 'sim2real/tita_ws/src/tita_controller/launch/flashsac.launch.py'
        spec = importlib.util.spec_from_file_location('flashsac_auto_stop_test', module_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        prefix = self.workspace / 'install/tita_controller'
        with patch.dict(os.environ, ROS_LOG_DIR=str(self.workspace / 'docs/exp/ros')):
            context = LaunchContext()
            context.launch_configurations.update(output_enabled='false', namespace='tita4252763')
            with patch.object(module, 'get_package_prefix', return_value=str(prefix)), \
                    patch.object(module, 'validate_policy') as validate, \
                    patch.object(module, 'ExecuteProcess') as execute:
                module.setup(context)
                validate.assert_called_once_with(prefix / 'share/tita_controller/policies/flashsac_60000')
                self.assertEqual(execute.call_args.kwargs['cmd'],
                                 ['bash', str(prefix / 'lib/tita_controller/run_flashsac.sh'), 'false'])
                self.assertEqual(execute.call_args.kwargs['additional_env']['TITA_INTERNAL_RUNNER'], '1')
                validate.side_effect = ValueError('corrupt policy')
                execute.reset_mock()
                with self.assertRaisesRegex(ValueError, 'corrupt policy'):
                    module.setup(context)
                execute.assert_not_called()

    def prepare_real_ros_launch(self):
        prefix = self.workspace / 'install/tita_controller'
        marker = prefix / 'share/ament_index/resource_index/packages/tita_controller'
        marker.parent.mkdir(parents=True)
        marker.touch()
        package = REPO / 'sim2real/tita_ws/src/tita_controller'
        launch_dir = prefix / 'share/tita_controller/launch'
        launch_dir.mkdir()
        shutil.copyfile(package / 'launch/flashsac.launch.py', launch_dir / 'flashsac.launch.py')
        policy = prefix / 'share/tita_controller/policies/flashsac_60000'
        for source in (package / 'policies/flashsac_60000').iterdir():
            shutil.copyfile(source, policy / source.name)
        runner = prefix / 'lib/tita_controller/run_flashsac.sh'
        runner.parent.mkdir(parents=True)
        shutil.copyfile(REPO / 'sim2real/tita_ws/run_flashsac.sh', runner)
        command = [
            shutil.which('ros2'), 'launch', 'tita_controller', 'flashsac.launch.py',
        ]
        env = {**self.env, 'AMENT_PREFIX_PATH': f'{prefix}:{os.environ.get("AMENT_PREFIX_PATH", "")}',
               'ROS_LOG_DIR': str(self.workspace / 'docs/exp/ros')}
        return command, env

    def test_real_ros_launch_orchestrates_mock_service_and_controller(self):
        command, env = self.prepare_real_ros_launch()
        result = subprocess.run(command, env=env, capture_output=True, text=True, timeout=20)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertTrue((self.workspace / 'stop_requested.txt').exists(), result.stdout)
        self.assert_logged(0)
        self.assertIn('tita.launch.py policy_dir:=', (self.workspace / 'launch_arguments.txt').read_text())

    def test_public_ros_launch_ctrl_c_removes_descendants(self):
        command, env = self.prepare_real_ros_launch()
        self.interrupt_and_check_descendants(command, {**env, 'MOCK_HANG_LAUNCH': '1'})

    def test_public_ros_launch_output_true_requests_direct_before_controller(self):
        command, env = self.prepare_real_ros_launch()
        result = subprocess.run(command + ['output_enabled:=true'], env=env,
                                capture_output=True, text=True, timeout=20)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        _, summary = self.assert_logged(0)
        self.assertEqual((self.workspace / 'can_requests.txt').read_text().splitlines(), [
            'can0 170##200000000000200000000',
            'can0 170##200000000000203000000',
        ])
        self.assertIn('MCU Direct request: transport accepted', summary)

    def test_public_ros_launch_forwards_velocity_bias_and_keeps_output_disabled(self):
        command, env = self.prepare_real_ros_launch()
        result = subprocess.run(command + ['velocity_bias:=true', 'velocity_bias_response_sign:=-1.0'], env=env,
                                capture_output=True, text=True, timeout=20)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        _, summary = self.assert_logged(0)
        self.assertIn('Velocity bias enabled: true', summary)
        self.assertIn('Velocity bias limit: +/-2 m/s', summary)
        self.assertIn('velocity_bias:=true', (self.workspace / 'launch_arguments.txt').read_text())
        self.assertFalse((self.workspace / 'can_requests.txt').exists())

    def test_public_launch_rejects_invalid_bias_before_runner_construction(self):
        from launch import LaunchContext
        spec = importlib.util.spec_from_file_location('bias_invalid_test',
            REPO / 'sim2real/tita_ws/src/tita_controller/launch/flashsac.launch.py')
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        with patch.dict(os.environ, ROS_LOG_DIR=str(self.workspace / 'docs/exp/ros')), \
                patch.object(module, 'get_package_prefix', return_value=str(self.workspace / 'install/tita_controller')), \
                patch.object(module, 'validate_policy'), patch.object(module, 'ExecuteProcess') as execute:
            context = LaunchContext()
            context.launch_configurations.update(output_enabled='false', namespace='tita4252763', velocity_bias='true')
            for sign in ('0', 'nan', 'inf'):
                context.launch_configurations.update(velocity_bias_response_sign=sign)
                with self.assertRaises(ValueError):
                    module.setup(context)
            context.launch_configurations.update(velocity_bias_response_sign='1', velocity_bias_max_torque='0.3')
            with self.assertRaisesRegex(ValueError, 'was removed'):
                module.setup(context)
            execute.assert_not_called()

    def test_runner_rejects_obsolete_cap_environment_before_service_or_can(self):
        result = self.run_runner(TITA_VELOCITY_BIAS='true', TITA_VELOCITY_BIAS_MAX_TORQUE='0.3')
        self.assertEqual(result.returncode, 2)
        self.assertIn('was removed', result.stderr)
        self.assertFalse((self.workspace / 'stop_requested.txt').exists())
        self.assertFalse((self.workspace / 'can_requests.txt').exists())

    def test_repeated_ctrl_c_finishes_descendant_cleanup_and_bag(self):
        command, env = self.prepare_real_ros_launch()
        self.interrupt_and_check_descendants(
            command, {**env, 'MOCK_HANG_LAUNCH': '1', 'MOCK_IGNORE_INT': '1'},
            repeat_interrupt=True)


if __name__ == '__main__':
    unittest.main(verbosity=2)
