"""VALIDATION_SIM: exact native sim2real math in a 500 Hz MuJoCo plant.

No ROS, robot SDK, CAN, service control or hardware deployment. Candidate
controllers, if selected, are experiment code confined to test/.
"""
from __future__ import annotations
import argparse
import ctypes
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import uuid

os.environ.setdefault('MUJOCO_GL', 'egl')
os.environ.setdefault('LP_NUM_THREADS', '2')
import mujoco
import numpy as np
import onnxruntime as ort

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO/'sim2sim/sim2sim_ros2_jazzy'))
from sim2sim_ros2_jazzy.mujoco_env import TitaMujocoEnv
from sim2sim_ros2_jazzy.adapter import NATIVE_JOINTS, quat_wxyz_to_rotmat

BUNDLE = REPO/'sim2real/tita_ws/src/tita_controller/policies/flashsac_60000'
SPLAY = np.array([.75, 1.2, -2.7, 0., -.75, 1.2, -2.7, 0.])
SIT = np.array([-.05, .9, -2.6, 0., .05, .9, -2.6, 0.])
LEGS = np.array([0, 1, 2, 4, 5, 6])
WHEELS = np.array([3, 7])
STATES = ['idle', 'damp', 'transform_up', 'sit', 'rl', 'return_to_sit', 'estop']
DT = .002


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def write(path, data):
    path.write_text(json.dumps(data, indent=2, allow_nan=False)+'\n')


def parameters(cfg):
    robot = cfg['robot']
    packed = [*robot['torque_limit'], *robot['default_joint_angles'],
              *robot['default_joint_velocities'], *robot['joint_kp'], *robot['joint_kd']]
    for term in cfg['policy_interface']['actions']:
        packed.extend([NATIVE_JOINTS.index(term['joint']), term['kind'] == 'velocity',
                       term['scale'], term['offset'], *(term['clip'] or [-1e20, 1e20])])
    layout = []
    kinds = dict(ang_vel=0, gravity=1, commands=2, joint_pos=3, joint_vel=4, last_action=5)
    for term in cfg['policy_interface']['observations']:
        indices = [NATIVE_JOINTS.index(j) for j in term['joints']] if 'joints' in term else list(range(term['size']))
        scale = np.broadcast_to(term['scale'], (term['size'],))
        for i, index in enumerate(indices):
            kind = 6 if term.get('zero_wheel_pos') and index in WHEELS else kinds[term['kind']]
            layout.extend([kind, index, scale[i], *(term['clip'] or [-1e20, 1e20])])
    return np.array([*packed, len(layout)//5, *layout], dtype=np.float64)


def library():
    output = REPO/f'test/sim2real/sit_validation_work/bridge_{uuid.uuid4().hex}.so'
    output.parent.mkdir(exist_ok=True)
    subprocess.run(['g++', '-std=c++17', '-O2', '-shared', '-fPIC', '-Wall', '-Wextra',
                    '-Werror', '-pedantic', '-I', str(REPO/'sim2real/tita_ws/src/tita_controller/include'),
                    str(REPO/'test/sim2real/sit_validation_bridge.cpp'), '-o', str(output)], check=True)
    lib = ctypes.CDLL(str(output))
    output.unlink()  # dlopen retains the mapped library; parallel jobs have distinct builds.
    handle, vec = ctypes.c_void_p, np.ctypeslib.ndpointer(dtype=np.float64, flags='C_CONTIGUOUS')
    lib.sit_create.argtypes, lib.sit_create.restype = [vec], handle
    lib.sit_error.restype = ctypes.c_char_p
    lib.sit_destroy.argtypes = [handle]
    lib.sit_request.argtypes, lib.sit_request.restype = [handle, ctypes.c_int, vec, vec], ctypes.c_int
    lib.sit_sensors.argtypes = [handle, vec, vec, vec, vec, ctypes.c_int]
    lib.sit_angle.argtypes, lib.sit_angle.restype = [vec, vec], ctypes.c_double
    lib.sit_update.argtypes = [handle, ctypes.c_double]
    lib.sit_state.argtypes, lib.sit_state.restype = [handle], ctypes.c_int
    lib.sit_torque.argtypes = [handle, vec, vec, vec]
    lib.sit_action.argtypes = [handle, vec, vec, vec, vec]
    lib.sit_observation.argtypes = [handle, vec, np.ctypeslib.ndpointer(dtype=np.float32, flags='C_CONTIGUOUS')]
    lib.sit_observation.restype = ctypes.c_int
    return lib


def rpy(quat):
    w, x, y, z = quat
    return np.array([np.arctan2(2*(w*x+y*z), 1-2*(x*x+y*y)),
                     np.arcsin(np.clip(2*(w*y-z*x), -1, 1)),
                     np.arctan2(2*(w*z+x*y), 1-2*(y*y+z*z))])


class SupportingSit:
    """Test-only bumpless live PD, slowly moving effective targets to native sit.

    FF is absorbed into the effective leg target. This represents precisely
    the final native sit PD, without ramping feedback authority from zero.
    Wheel velocity references remain closed-loop and smoothly approach zero.
    """
    def __init__(self, q, dq, previous, limits, seconds, quat, gyro, ready_pitch, balance,
                 angle=None, thigh_hump=0., ff_scale=1., capture_com=False):
        self.kp = np.array([600., 80., 80., 0., 600., 80., 80., 0.])
        self.kd = np.array([8., 8., 8., .5, 8., 8., 8., .5])
        ff = np.array([-20., 0., -25., 0., 20., 0., -25., 0.])
        self.start = q.copy()
        self.start[LEGS] += (previous[LEGS]+self.kd[LEGS]*dq[LEGS])/self.kp[LEGS]
        self.goal = SIT.copy()
        self.goal[LEGS] += ff_scale*ff[LEGS]/self.kp[LEGS]
        self.wheel_start = dq[WHEELS]+previous[WHEELS]/self.kd[WHEELS]
        self.seconds, self.limits = seconds, limits
        self.thigh_hump = thigh_hump
        self.pitch_start = rpy(quat)[1] if angle is None else angle
        self.pitch_goal = ready_pitch if angle is None else (angle if capture_com else 0.)
        self.balance_kp, self.balance_kd, self.balance_wheel_rate = balance
        self.balance_initial = self.balance_kd*gyro[1]+self.balance_wheel_rate*np.mean(dq[WHEELS]-self.wheel_start)
        np.testing.assert_allclose(self.torque(q, dq, 0., quat, gyro, angle), previous, atol=1e-10, rtol=0)

    def torque(self, q, dq, elapsed, quat, gyro, angle=None):
        p = np.clip(elapsed/self.seconds, 0., 1.)
        alpha = p*p*(3.-2.*p)
        target = self.start+alpha*(self.goal-self.start)
        target[[1, 5]] += self.thigh_hump*np.sin(np.pi*alpha)
        torque = self.kp*(target-q)-self.kd*dq
        torque[WHEELS] = self.kd[WHEELS]*((1.-alpha)*self.wheel_start-dq[WHEELS])
        pitch_reference = self.pitch_start+alpha*(self.pitch_goal-self.pitch_start)
        measured_angle = rpy(quat)[1] if angle is None else angle
        balance = self.balance_kp*(measured_angle-pitch_reference)+self.balance_kd*gyro[1]
        balance += self.balance_wheel_rate*np.mean(dq[WHEELS]-(1.-alpha)*self.wheel_start)
        blend = 1.
        if angle is not None:
            fold = np.clip((-np.mean(q[[2, 6]])-2.35)/.30, 0., 1.)
            blend = 1.-fold*fold*(3.-2.*fold)
        torque[WHEELS] += blend*(balance-(1.-alpha)*self.balance_initial)
        return np.clip(torque, -self.limits, self.limits)


def rollout(lib, cfg, mode, domain, seed, prefix, duration, motion, out, sit_seconds, balance_gains,
            thigh_hump, ff_scale, capture_com):
    job = f'{domain}_{motion}_s{seed}_t{prefix:g}_{mode}'
    native = lib.sit_create(parameters(cfg))
    assert native, lib.sit_error()
    env = TitaMujocoEnv(cfg)
    m, d = env.model, env.data
    rng = np.random.default_rng(seed)
    floor = m.geom('floor').id
    obstacles = np.flatnonzero((m.geom_bodyid == 0) & (np.arange(m.ngeom) != floor))
    m.geom_contype[obstacles] = m.geom_conaffinity[obstacles] = 0
    leg_gain, imu_pitch = 1., 0.
    if domain != 'nominal':
        leg_gain = .6  # Equivalent mismatch hypothesis, not a measured motor gain.
        m.dof_frictionloss[env.qvel_addr[LEGS]] = 2.
        m.dof_frictionloss[env.qvel_addr[WHEELS]] = .3
        imu_pitch = np.deg2rad({'fitted_A': 2., 'fitted_B': 1., 'fitted_C': 0.}[domain])
        m.body_ipos[m.body('base_link').id, 0] += {'fitted_A': 0., 'fitted_B': -.01, 'fitted_C': -.02}[domain]
        mujoco.mj_setConst(m, mujoco.MjData(m))
    physics_hash = hashlib.sha256(b''.join(x.tobytes() for x in [
        m.body_mass, m.body_ipos, m.dof_frictionloss, m.dof_damping, m.geom_friction,
        np.array([leg_gain, imu_pitch, DT])])).hexdigest()
    env.reset(SPLAY)
    d.qvel[0] = rng.uniform(-.015, .015)
    d.qvel[env.qvel_addr[LEGS]] = rng.normal(0., .01, 6)
    mujoco.mj_forward(m, d)
    lib.sit_request(native, 2, env.joint_pos().astype(float), np.zeros(8))
    options = ort.SessionOptions()
    options.intra_op_num_threads = 1
    policy = ort.InferenceSession(str(BUNDLE/'policy.onnx'), sess_options=options, providers=['CPUExecutionProvider'])
    in_name, out_name = policy.get_inputs()[0].name, policy.get_outputs()[0].name
    limits = np.array(cfg['robot']['torque_limit'])
    action = np.zeros(8)
    torque = np.zeros(8)
    command = np.zeros(3)
    obs = np.empty(cfg['policy']['obs_dim'], dtype=np.float32)
    rl_start, event, done = None, None, False
    previous_state = -1
    records = []
    snapshots_q, snapshots_v, snapshots_t = [], [], []
    event_hash = None
    faults = []
    candidate = None
    candidate_failed = False
    ready_pitch = None
    # Keep the controller's geometry/inertial model nominal even when the plant
    # has a perturbed CoM. It must not know the simulated mismatch parameters.
    kinematics_model = mujoco.MjModel.from_xml_path(str(REPO/cfg['model']['scene_xml']))
    kinematics = mujoco.MjData(kinematics_model)
    wheel_bodies = [m.jnt_bodyid[m.joint(env.joint_names[j]).id] for j in WHEELS]
    balance_angles = []
    offset = np.array([np.cos(imu_pitch/2), 0., np.sin(imu_pitch/2), 0.])
    co, so = np.cos(imu_pitch), np.sin(imu_pitch)
    mount = np.array([[co, 0., so], [0., 1., 0.], [-so, 0., co]])
    try:
        for tick in range(round((prefix+duration+20.)/DT)):
            q = d.qpos[env.qpos_addr].copy()
            dq = d.qvel[env.qvel_addr].copy()
            for j in (1, 5):
                if q[j] < -2.5:
                    q[j] += 2*np.pi
            quat = d.sensor('trunk_quat').data.copy()
            gyro = d.sensor('trunk_gyro').data.copy()
            if imu_pitch:
                quat = np.array([quat[0]*offset[0]-quat[2]*offset[2], quat[1]*offset[0]-quat[3]*offset[2],
                                 quat[0]*offset[2]+quat[2]*offset[0], quat[1]*offset[2]+quat[3]*offset[0]])
                gyro = mount.T@gyro
            lib.sit_sensors(native, q, dq, quat, gyro, 1)
            state = lib.sit_state(native)
            com_angle = None
            if mode.startswith('candidate_com_'):
                # Sensor-only FK: no plant root translation/velocity/COM enters this reconstruction.
                kinematics.qpos[:3] = 0.
                kinematics.qpos[3:7] = quat
                kinematics.qpos[env.qpos_addr] = q
                mujoco.mj_kinematics(kinematics_model, kinematics)
                com = np.sum(kinematics.xipos*kinematics_model.body_mass[:, None], axis=0)/kinematics_model.body_mass.sum()
                relative_com = com-kinematics.xpos[wheel_bodies].mean(axis=0)
                yaw = rpy(quat)[2]
                com_angle = float(np.arctan2(relative_com@np.array([np.cos(yaw), np.sin(yaw), 0.]),
                                             relative_com[2]))
            if state == 3 and rl_start is None:
                ready_pitch = float(rpy(quat)[1])
                assert lib.sit_request(native, 4, q, torque)
                rl_start = float(d.time)
                state = 4
            elapsed = float(d.time)-rl_start if rl_start is not None else None
            target = np.zeros(3)
            if elapsed is not None and motion != 'neutral' and elapsed >= prefix-2.:
                target[0] = .25 if motion == 'forward' else -.25
            if state == 4:
                command += np.clip(target-command, -.5*DT, .5*DT)
            else:
                command[:] = 0.
            if elapsed is not None and elapsed+1e-9 >= prefix and event is None:
                assert state == 4, f'Invalid RL event precondition: {job} state {STATES[state]}'
                event = float(d.time)
                event_hash = hashlib.sha256(np.r_[d.qpos, d.qvel, action, torque].tobytes()).hexdigest()
                if mode in ('baseline_estop', 'production_estop'):
                    lib.sit_request(native, 6, q, torque)
                elif mode in ('baseline_return', 'production_return'):
                    lib.sit_request(native, 5, q, torque)
                elif mode.startswith(('candidate_live_', 'candidate_balanced_', 'candidate_com_', 'candidate_policy_')):
                    balance = balance_gains if mode.startswith(('candidate_balanced_', 'candidate_com_')) else (0., 0., 0.)
                    candidate = SupportingSit(q, dq, torque.copy(), limits, sit_seconds,
                                              quat, gyro, ready_pitch, balance, com_angle, thigh_hump,
                                              ff_scale, capture_com)
                    lib.sit_request(native, 6 if mode.endswith('estop') else 5, q, torque)
                elif mode != 'continue_rl':
                    raise ValueError(mode)
                state = lib.sit_state(native)
                if state != 4:
                    command[:] = 0.
            tilt = np.arccos(np.clip(-float((quat_wxyz_to_rotmat(quat).T@np.array([0., 0., -1.]))[2]), -1, 1))
            if tilt > .65:
                candidate_failed = candidate_failed or candidate is not None
                lib.sit_request(native, 1, q, torque)
                if not faults or faults[-1]['kind'] != 'fall_tilt':
                    faults.append(dict(kind='fall_tilt', event_t=float(d.time)-event if event else None))
            lib.sit_update(native, DT)
            state = lib.sit_state(native)
            if candidate is not None and not candidate_failed:
                state = 6 if mode.endswith('estop') else (5 if d.time-event < sit_seconds else 3)
            changed = state != previous_state
            previous_state = state
            policy_needed = state == 4 or (candidate is not None and not candidate_failed and mode.startswith('candidate_policy_'))
            if not policy_needed:
                action[:] = 0.
            if tick % 10 == 0 or changed:
                packed = np.r_[q, dq, quat, gyro, command, action].astype(np.float64)
                assert lib.sit_observation(native, packed, obs) == len(obs)
                if policy_needed:
                    action = policy.run([out_name], {in_name: obs[None]})[0].reshape(8).astype(float)
            if candidate is not None and not candidate_failed:
                torque[:] = candidate.torque(q, dq, float(d.time)-event, quat, gyro, com_angle)
                if mode.startswith('candidate_policy_'):
                    policy_torque = np.zeros(8)
                    lib.sit_action(native, action, q, dq, policy_torque)
                    fold = np.clip((-np.mean(q[[2, 6]])-2.35)/.30, 0., 1.)
                    beta = 1.-fold*fold*(3.-2.*fold)
                    torque[WHEELS] = beta*policy_torque[WHEELS]+(1.-beta)*torque[WHEELS]
            elif state == 4:
                lib.sit_action(native, action, q, dq, torque)
            else:
                lib.sit_torque(native, q, dq, torque)
            assert np.isfinite(torque).all() and (abs(torque) <= limits+1e-9).all()
            relative = float(d.time)-event if event is not None else float(d.time)-(rl_start or 0.)-prefix
            contact_force = 0.
            for contact_index, contact in enumerate(d.contact):
                if floor in contact.geom:
                    wrench = np.zeros(6)
                    mujoco.mj_contactForce(m, d, contact_index, wrench)
                    contact_force += abs(wrench[0])
            if rl_start is not None:
                records.append(np.r_[relative, state, d.qpos[:3], d.qvel[:3], rpy(d.qpos[3:7]),
                                     gyro, q, dq, torque, command, contact_force])
                balance_angles.append(com_angle if com_angle is not None else np.nan)
                if tick % 20 == 0:
                    snapshots_q.append(d.qpos.copy()); snapshots_v.append(d.qvel.copy()); snapshots_t.append(relative)
            if event is not None and relative+1e-9 >= duration:
                done = True
                break
            applied = torque.copy()
            applied[LEGS] *= leg_gain
            d.ctrl[env.actuator_ids] = applied
            mujoco.mj_step(m, d)
            if not np.isfinite(np.r_[d.qpos, d.qvel]).all():
                faults.append(dict(kind='non_finite', event_t=relative)); break
            if rl_start is None and d.time > 15.:
                faults.append(dict(kind='startup_not_completed', event_t=None)); break
        rows = np.array(records)
        if rows.size and event is not None:
            post, tail = rows[:, 0] >= 0., rows[:, 0] >= max(duration-1., 0.)
            before = rows[np.argmin(abs(rows[:, 0]))]
            result = dict(id=job, mode=mode, domain=domain, motion=motion, seed=seed, prefix_s=prefix,
                          execution_domain='VALIDATION_SIM', evidence_status='PASS' if done else 'FAIL',
                          rollout_completed=done, initial_state_sha256=event_hash, physics_sha256=physics_hash,
                          faults=faults, entry_z_m=float(before[4]), entry_pitch_deg=float(np.degrees(before[9])),
                          min_z_m=float(rows[post, 4].min()), max_drop_m=float(before[4]-rows[post, 4].min()),
                          max_downward_speed_m_s=float(max(0., -rows[post, 7].min())),
                          peak_tilt_deg=float(np.degrees(np.arccos(np.clip(np.cos(rows[post, 8])*np.cos(rows[post, 9]), -1, 1))).max()),
                          peak_joint_speed_rad_s=float(abs(rows[post, 22:30]).max()),
                          peak_floor_normal_n=float(rows[post, -1].max()),
                          tail_pitch_deg=float(np.degrees(rows[tail, 9]).mean()), tail_z_m=float(rows[tail, 4].mean()),
                          tail_gyro_rms_rad_s=float(np.sqrt(np.mean(rows[tail, 11:14]**2))),
                          tail_horizontal_speed_m_s=float(np.linalg.norm(rows[tail, 5:7], axis=1).mean()),
                          peak_horizontal_speed_m_s=float(np.linalg.norm(rows[post, 5:7], axis=1).max()),
                          max_horizontal_displacement_m=float(np.linalg.norm(rows[post, 2:4]-before[2:4], axis=1).max()),
                          final_state=STATES[int(rows[-1, 1])], leg_gain_hypothesis=leg_gain,
                          candidate_sit_seconds=sit_seconds if candidate else None,
                          candidate_thigh_hump_rad=thigh_hump if candidate else None,
                          candidate_final_ff_scale=ff_scale if candidate else None,
                          candidate_capture_com_reference=capture_com if candidate else None,
                          candidate_balance_gains=balance_gains if mode.startswith(('candidate_balanced_', 'candidate_com_')) else None,
                          imu_mount_pitch_deg=float(np.degrees(imu_pitch)))
            checks = dict(no_fault=not faults, downward_speed=result['max_downward_speed_m_s'] <= .2,
                          tilt=result['peak_tilt_deg'] <= 20.,
                          contact_force=result['peak_floor_normal_n'] <= 2.*float(m.body_mass.sum())*9.81,
                          tail_gyro=result['tail_gyro_rms_rad_s'] <= .1,
                          tail_height=.14 <= result['tail_z_m'] <= .22,
                          stopped=result['tail_horizontal_speed_m_s'] <= .05,
                          travel=result['max_horizontal_displacement_m'] <= .5)
            result.update(acceptance_status='PASS' if all(checks.values()) else 'FAIL',
                          acceptance_checks=checks, total_mass_kg=float(m.body_mass.sum()))
        else:
            result = dict(id=job, execution_domain='VALIDATION_SIM', evidence_status='FAIL',
                          faults=faults, rollout_completed=False, initial_state_sha256=None)
        np.savez_compressed(out/f'{job}.npz', rows=rows, qpos=snapshots_q, qvel=snapshots_v,
                            sample_times=snapshots_t, sensor_com_angle=balance_angles)
        write(out/f'{job}.json', result)
        return result
    finally:
        lib.sit_destroy(native)
        env.close()


def main():
    global BUNDLE
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--policy-bundle', type=Path, default=BUNDLE)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--modes', nargs='+', default=['continue_rl', 'baseline_estop', 'baseline_return'],
                        choices=['continue_rl', 'baseline_estop', 'baseline_return', 'production_estop', 'production_return']+
                        [f'candidate_{kind}_{ending}' for kind in ['live', 'balanced', 'com', 'policy']
                         for ending in ['estop', 'return']])
    parser.add_argument('--domains', nargs='+', default=['nominal'],
                        choices=['nominal', 'fitted_A', 'fitted_B', 'fitted_C'])
    parser.add_argument('--seeds', nargs='+', type=int, default=[42])
    parser.add_argument('--prefix', type=float, default=8.)
    parser.add_argument('--duration', type=float, default=6.)
    parser.add_argument('--sit-seconds', type=float, default=4.)
    parser.add_argument('--balance-kp', type=float, default=30.)
    parser.add_argument('--balance-kd', type=float, default=5.)
    parser.add_argument('--balance-wheel-rate', type=float, default=1.)
    parser.add_argument('--thigh-hump', type=float, default=.3)
    parser.add_argument('--sit-ff-scale', type=float, default=1.)
    parser.add_argument('--capture-com-reference', action='store_true')
    parser.add_argument('--motion', choices=['neutral', 'forward', 'reverse'], default='neutral')
    args = parser.parse_args()
    BUNDLE = args.policy_bundle.resolve()
    if args.prefix <= 0 or args.duration <= 0 or args.sit_seconds <= 0:
        parser.error('Positive prefix, duration and sit duration required')
    if (args.output/'results.json').exists():
        parser.error('Choose a new output directory; existing evidence is preserved')
    args.output.mkdir(parents=True, exist_ok=True)
    cfg = json.loads((BUNDLE/'config.json').read_text())
    assert digest(BUNDLE/'policy.onnx') == cfg['policy_interface']['onnx_sha256']
    original_control = cfg['control'].copy()
    cfg['control'] = dict(sim_timestep=DT, decimation=10)
    write(args.output/'config_used.json', cfg)
    write(args.output/'manifest.json', dict(execution_domain='VALIDATION_SIM',
          checkpoint_sha256=cfg['policy_interface']['checkpoint_sha256'], onnx_sha256=digest(BUNDLE/'policy.onnx'),
          original_control=original_control, validated_control=cfg['control'], velocity_bias=False,
          candidate_sit_seconds=args.sit_seconds,
          candidate_thigh_hump_rad=args.thigh_hump,
          candidate_final_ff_scale=args.sit_ff_scale,
          candidate_capture_com_reference=args.capture_com_reference,
          controller_fk_model='unmodified nominal robot; no perturbed plant CoM/mass access',
          candidate_balance_gains=[args.balance_kp, args.balance_kd, args.balance_wheel_rate],
          sources={str(p.relative_to(REPO)): digest(p) for p in [Path(__file__),
                   REPO/'test/sim2real/sit_validation_bridge.cpp',
                   REPO/'sim2real/tita_ws/src/tita_controller/include/tita_controller/state_machine.hpp',
                   REPO/'sim2real/tita_ws/src/tita_controller/include/tita_controller/adapter.hpp']},
          notes=['Uses actual native state machine, observation builder and action adapter.',
                 'Fresh canonical splay/startup, no hardware-state injection.',
                 'Obstacles disabled for flat-floor stop trials.',
                 'Fitted domains are equivalent hypotheses, not measured motor constants.',
                 'PASS evidence means execution integrity, not a safe-stop verdict.']))
    lib = library()
    results = []
    for domain in args.domains:
        for seed in args.seeds:
            hashes = []
            for mode in args.modes:
                result = rollout(lib, cfg, mode, domain, seed, args.prefix, args.duration, args.motion,
                                 args.output, args.sit_seconds,
                                 [args.balance_kp, args.balance_kd, args.balance_wheel_rate],
                                 args.thigh_hump, args.sit_ff_scale, args.capture_com_reference)
                results.append(result)
                hashes.append(result['initial_state_sha256'])
                write(args.output/'results.json', results)
                print(json.dumps(result, allow_nan=False), flush=True)
            assert len(set(hashes)) == 1, 'Comparison modes have different pre-transition states'


if __name__ == '__main__':
    main()
