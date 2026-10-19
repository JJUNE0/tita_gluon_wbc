"""ROBOT_STATE_CHANGING: stop existing bringup, record, then run frozen FlashSAC.

Motor output requires the operator's explicit output_enabled:=true selection.
That path records first, requests MCU Ready -> Direct using the upstream startup
sequence, then starts the controller. Output disabled skips MCU mode requests.
"""

import hashlib
import json
import math
from pathlib import Path

from ament_index_python.packages import get_package_prefix
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, EmitEvent, ExecuteProcess, OpaqueFunction
from launch.events import Shutdown
from launch.substitutions import LaunchConfiguration

CHECKPOINT_SHA256 = '79f9175bb8c3be0c5138866e30891b90cc1282b6c98023cdb76c2e33b229068c'
ONNX_SHA256 = '26f0d86b65a68475fb8a315fb31e829ae16eaa2cf16dabbbcf38e69f28c933e9'
CONFIG_SHA256 = 'a24c2137969f854fc98cc3027884dbbadad4060f18db7758b028c12ca1405719'
# Selectable frozen bundles: (checkpoint, ONNX, config) SHA256. flashsac_80000 stays the default.
BUNDLES = {
    # Warmup-0 heading run model_65000: best in-place turn in sim (2026-10-19 screen).
    'flashsac_headw0_65000': ('ff083cbfc8a8571009a27454e75dc88463e9ebc796fa79e8782ccb4a5bea239d',
                              'ede50fde5cc1863758d2c50e70f7902cafb31e2a677c985e0d69b80c2560be0b',
                              '804c94a365ccc4b0d9b3bf08022699d81012ccd251d8606a4646624c88ed1db2'),
    # Warmup-0 heading run model_50000: sphere wheels, no MA2, gyro heading_error (35 obs) (2026-10-19).
    'flashsac_headw0_50000': ('0a6f8ef2bb8a324bf6f6fb7689297f9001bd4b57896daa0cb9ead4953162f4a7',
                              '284b4166297fafe5606e58d7b66d9e4570980b839ebde433cbd7a85549313a4c',
                              '804d2ab9f0fdb80232706a9dc99f4daacad4b2c0f194c914f99b1d8fd1b7c428'),
    'flashsac_sphere2_60000': ('a4c2bfbf6a58240a6623ee8bb8d863774b9336f62df7de3d1993b76725334b2a',
                                'b744091bb984f3540ec9517f4d3a8a70b5d76cf0f1c7a811d122baac15017040',
                                '7c0b597a7750ec63ae2182edad9af67de616fe069d4630e1810b8e129d4e4c06'),
    'flashsac_sphere1_70000': ('8e23cf5d1844a6d825482939e5cfc455cd672dd566b2320570080ff606782c77',
                                'df54bb61b09c681aad403b41ae52dc83807002f2832b8f969c2ba56a441297d7',
                                '892bf68e509ad088d0ba6c172042bd8433dedefac3fd0c3294fd58be095a3c65'),
    'flashsac_sphere1_90000': ('df2a03faeb6e054310c8cc0c2c11f811c1f6e845dd87a66c40ff3cd29dd8b311',
                                '08d57aa5b0d63063ddcd1f64a08fc545f7ad2ab317aa1c1044cb80ea15a0710a',
                                'cfd82318fced4143654bff6e9071d1cba312d0203ffcecca549ddecdf6e55479'),
    'flashsac_sphere3_70000': ('b9d411eaee09753d3bb6a00d12da8a3f18ce205b2c95faec954c91699e811263',
                                '204693483d123b77d9ad1698819ee10179ba27b5881bc8a41c1e5fc138ee16ff',
                                'ba2a48b603524fcd5215e8cbf608efbd87895c0521f56ed46876b9ab26121c6c'),
    'flashsac_posma2_75000': ('9c22f34e0e3b9d7840f29250c214452bb84cadde6037d277d90df55221e84150',
                              '128734f230868b947c9eac59ef647b8394043c6603781a335fd4e3b4700a2001',
                              '45a2e773f5ccf43b770829184b22537a6de1ce8da092727264446ac32287c28a'),
    'flashsac_posma2_50000': ('baba6974b76d4e8a7b7107cdfab9d2b7bb73695df00419009279549ebd51f992',
                              '4b922a52b4e371f4e1ed28d64a0a9d4211161ba24950a1d5a92d2ccf26918553',
                              '2b11c12bf531b8fd92558d3b36e04f49aa91fcae7b97f187413b127780bb93be'),
    'flashsac_80000': (CHECKPOINT_SHA256, ONNX_SHA256, CONFIG_SHA256),
    # C2 leg-scale arm model_60000; legs 60/1.5, no deployment-side compensation (2026-10-18).
    'flashsac_c2_60000': ('b4c8ae072787c3119864e75c2ebfbaf8284a02976dc68f1f282ad9480ae2e116',
                          'b12e40267bb3247762b0dd6283bd9f9cafffac52597ca74b387790bb4e925b7f',
                          '9561fd1a7d9e5f75a1a9916e0c32d4a705109c4795dac9636fbac0ad877ffde1'),
}


def validate_policy(policy_dir):
    """Reject a changed or mismatched bundle before creating any robot nodes."""
    if policy_dir.name not in BUNDLES:
        raise ValueError(f'Unknown frozen FlashSAC bundle: {policy_dir.name}')
    checkpoint_sha256, onnx_sha256, config_sha256 = BUNDLES[policy_dir.name]
    for name, expected in [('policy.onnx', onnx_sha256), ('config.json', config_sha256)]:
        actual = hashlib.sha256((policy_dir / name).read_bytes()).hexdigest()
        if actual != expected:
            raise ValueError(f'Frozen FlashSAC {name} SHA256 mismatch: {actual}')
    cfg = json.loads((policy_dir / 'config.json').read_text())
    if cfg['policy_interface']['checkpoint_sha256'] != checkpoint_sha256:
        raise ValueError('Frozen FlashSAC checkpoint SHA256 mismatch')


def setup(context):
    prefix = Path(get_package_prefix('tita_controller'))
    share = prefix / 'share' / 'tita_controller'
    policy = LaunchConfiguration('policy', default='flashsac_80000').perform(context)
    if policy not in BUNDLES:
        raise ValueError(f'unknown policy bundle: {policy}')
    policy_dir = share / 'policies' / policy
    validate_policy(policy_dir)
    leg_filter = LaunchConfiguration('leg_action_filter', default='auto').perform(context)
    if leg_filter == 'auto':
        cfg = json.loads((policy_dir / 'config.json').read_text())
        leg_filter = cfg['policy_interface'].get('leg_action_filter', 'none')
    if leg_filter not in ('none', 'ma2_legs', 'ma2_notch_legs'):
        raise ValueError('unknown leg_action_filter')
    notch_hz = LaunchConfiguration('leg_notch_hz', default='8.3').perform(context)
    notch_q = LaunchConfiguration('leg_notch_q', default='3.0').perform(context)
    if leg_filter == 'ma2_notch_legs':
        hz, q = float(notch_hz), float(notch_q)
        if not (math.isfinite(hz) and math.isfinite(q) and 0 < hz < 25 and q > 0 and hz/q < 25):
            raise ValueError('invalid notch frequency/Q/bandwidth at 50 Hz')
    if 'velocity_bias_max_torque' in context.launch_configurations:
        raise ValueError('velocity_bias_max_torque is not configurable; additional torque is fixed at +/-0.8 Nm/wheel')
    bias = LaunchConfiguration('velocity_bias', default='false').perform(context)
    sign = LaunchConfiguration('velocity_bias_response_sign', default='1.0').perform(context)
    if float(sign) not in (-1., 1.):
        raise ValueError('velocity_bias_response_sign must be -1 or +1')
    # Keep service stop, recording, Ready -> Direct and controller startup in the
    # logged runner so a failed mode request prevents the motor node from starting.
    return [ExecuteProcess(
        cmd=['bash', str(prefix / 'lib' / 'tita_controller' / 'run_flashsac.sh'),
             LaunchConfiguration('output_enabled').perform(context)],
        additional_env={
            'TITA_INTERNAL_RUNNER': '1',
            'TITA_WORKSPACE': str(prefix.parent.parent),
            'TITA_NAMESPACE': LaunchConfiguration('namespace').perform(context),
            'TITA_POLICY_BUNDLE': policy,
            'TITA_VELOCITY_BIAS': bias,
            'TITA_VELOCITY_BIAS_RESPONSE_SIGN': sign,
            'TITA_LEG_ACTION_FILTER': leg_filter,
            'TITA_LEG_NOTCH_HZ': notch_hz,
            'TITA_LEG_NOTCH_Q': notch_q,
        },
        output='screen', sigterm_timeout='20', sigkill_timeout='10',
        on_exit=[EmitEvent(event=Shutdown(reason='FlashSAC logged runner exited'))],
    )]


def generate_launch_description():
    return LaunchDescription([
        DeclareLaunchArgument('output_enabled', default_value='false',
                              choices=['false', 'true'],
                              description='true requests MCU Direct mode, then sends motor torques'),
        DeclareLaunchArgument('namespace', default_value='tita4252763'),
        DeclareLaunchArgument('policy', default_value='flashsac_80000', choices=list(BUNDLES),
                              description='frozen bundle under share/tita_controller/policies (SHA256-pinned)'),
        DeclareLaunchArgument('leg_action_filter', default_value='auto', choices=['auto', 'none', 'ma2_legs', 'ma2_notch_legs'],
                              description='MA2 on six leg actions at 50 Hz; wheels pass through'),
        DeclareLaunchArgument('leg_notch_hz', default_value='8.3'),
        DeclareLaunchArgument('leg_notch_q', default_value='3.0'),
        DeclareLaunchArgument('velocity_bias', default_value='false', choices=['false', 'true'],
                              description='estimate zero-command drift at 1-3 s; apply after 3 s, capped at +/-0.8 Nm/wheel'),
        DeclareLaunchArgument('velocity_bias_response_sign', default_value='1.0',
                              description='closed-loop response sign, +1 matches MuJoCo; hardware unvalidated'),
        OpaqueFunction(function=setup),
    ])
