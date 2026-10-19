"""VALIDATION_SIM: real-to-sim grid over leg torque scale, leg/wheel Coulomb friction.

Goal: find MuJoCo physics that reproduce the real zero-command stance of the
deployed FlashSAC policy (crouched knee, large commanded knee/hip torque,
backward wheel drift), so the retraining DR ranges can be centred on it.

Reuses the existing sim2sim path unchanged: splay -> transform_up -> sit -> RL
startup state machine, frozen ONNX actor, native PD adapter and clip. Physics
is fixed before the first mj_step (``static_target_domain.StaticEnv``) and
extended here with:

- ``leg_gain``: applied leg torque = gain * commanded torque (all phases unless ``startup_leg_gain``).
- ``startup_leg_gain``: leg gain used only during the splay/transform_up/sit startup, e.g. to emulate a
  deployment-side torque compensation that is applied to the RL PD output but not to the startup PD.
- ``leg_frictionloss`` / ``wheel_frictionloss``: MuJoCo ``dof_frictionloss`` [N m].
- ``wheel_damping``: MuJoCo ``dof_damping`` on wheel joints [N m s/rad].
- job ``sensor.imu_pitch_deg``: IMU mounted pitched by this angle about body y. The policy
  observation and the logged quaternion use the offset frame, as a real mounting error would.

Recorded torques are the *commanded* PD values (before ``leg_gain``), the same
quantity the real bags log. No production file, robot or deployment is touched.
"""

from __future__ import annotations

import argparse
from concurrent.futures import ProcessPoolExecutor, as_completed
import hashlib
import itertools
import json
import multiprocessing
import os
from pathlib import Path
import sys
import time
from unittest.mock import patch

os.environ.setdefault('MUJOCO_GL', 'egl')

import numpy as np

REPO = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(REPO / 'sim2sim/sim2sim_ros2_jazzy'), str(REPO), str(REPO / 'test')]

from eval_flash_pv_models import Runner, LEGS, WHEELS  # noqa: E402
from static_target_domain import StaticEnv, StartupFailure  # noqa: E402
from sim2sim_ros2_jazzy.adapter import ObsState, quat_wxyz_to_rotmat  # noqa: E402

EXPORTS = REPO / 'docs/exp/2026-10-16/velocity_bias_overnight/exports'
RUN = 'tita_flash_sac_115632_883848'
BASE_KEYS = {'mass', 'com', 'friction', 'gain', 'lag'}
EXTRA_KEYS = {'leg_gain', 'startup_leg_gain', 'leg_frictionloss', 'wheel_frictionloss', 'wheel_damping'}
DT = 0.02
WHEEL_RADIUS = 0.0925
WINDOW_S = (5.0, 10.0)

# Real targets. Tolerances are approximate run-to-run spread; they only weight the loss.
TOLERANCE = dict(knee_q=0.10, thigh_q=0.10, hip_splay=0.05, knee_tau=3.0, hip_tau=5.0,
                 wheel_tau=0.15, speed=0.05, pitch_deg=1.0, knee_q_0p5=0.10)
# (checkpoint, signals, zero-command window used by the corresponding real-review report)
REAL_SIGNALS = {
    'real_60k_free': ('model_60000', 'docs/exp/2026-10-17/flashsac_141113_free_drift_review/signals.npz', (5.0, 10.0)),
    'real_50k_off': ('model_50000', 'docs/exp/2026-10-17/flashsac_50000_real_review/off_signals.npz', (8.0, 10.0)),
    'real_75k_off': ('model_75000', 'docs/exp/2026-10-17/flashsac_75000_real_review/off_signals.npz', (12.8, 15.3)),
}


def digest(path: Path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def write(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, allow_nan=False) + '\n')


def quat_mul(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    w1, x1, y1, z1 = a
    w2, x2, y2, z2 = b
    return np.array([w1 * w2 - x1 * x2 - y1 * y2 - z1 * z2, w1 * x2 + x1 * w2 + y1 * z2 - z1 * y2,
                     w1 * y2 - x1 * z2 + y1 * w2 + z1 * x2, w1 * z2 + x1 * y2 - y1 * x2 + z1 * w2])


def imu_offset(job: dict):
    """Return (quat_offset_wxyz, R_offset) for a sensor pitched about body y."""
    angle = np.radians(job.get('sensor', {}).get('imu_pitch_deg', 0.))
    quat = np.array([np.cos(angle / 2), 0., np.sin(angle / 2), 0.])
    c, s_ = np.cos(angle), np.sin(angle)
    return quat, np.array([[c, 0., s_], [0., 1., 0.], [-s_, 0., c]])


def pitch_deg(quat_wxyz: np.ndarray) -> np.ndarray:
    w, x, y, z = np.asarray(quat_wxyz, dtype=float).T
    return np.degrees(np.arcsin(np.clip(2 * (w * y - z * x), -1, 1)))


class IdentEnv(StaticEnv):
    """StaticEnv plus leg torque scale and joint Coulomb friction / wheel damping."""

    def __init__(self, cfg, target):
        unknown = set(target) - BASE_KEYS - EXTRA_KEYS
        if unknown:
            raise ValueError(f'Unknown physics keys: {sorted(unknown)}')
        self.ident = {k: float(target[k]) for k in EXTRA_KEYS if k in target}
        self.commanded = []
        super().__init__(cfg, {k: v for k, v in target.items() if k in BASE_KEYS})
        m, dofs = self.model, np.asarray(self.qvel_addr)
        if 'leg_frictionloss' in self.ident:
            m.dof_frictionloss[dofs[LEGS]] = self.ident['leg_frictionloss']
        if 'wheel_frictionloss' in self.ident:
            m.dof_frictionloss[dofs[WHEELS]] = self.ident['wheel_frictionloss']
        if 'wheel_damping' in self.ident:
            m.dof_damping[dofs[WHEELS]] = self.ident['wheel_damping']
        self.initial_fingerprint = self.fingerprint()
        self.metadata.update(ident=dict(self.ident), fingerprint=self.initial_fingerprint,
                             dof_frictionloss=m.dof_frictionloss[dofs].tolist(),
                             dof_damping=m.dof_damping[dofs].tolist())

    def fingerprint(self):
        extra = [self.model.dof_frictionloss, self.model.dof_damping,
                 np.array([getattr(self, 'ident', {}).get('leg_gain', 1.)])]
        return hashlib.sha256(super().fingerprint().encode()
                              + b''.join(np.asarray(v).tobytes() for v in extra)).hexdigest()

    def step_with_torque_callback(self, callback):
        # Same wheel gain/lag/clip path as StaticEnv; legs additionally scaled by leg_gain.
        self.physical, self.commanded = [], []
        leg_gain = self.ident.get('leg_gain', 1.)
        if self.record_startup:
            leg_gain = self.ident.get('startup_leg_gain', leg_gain)
        for _ in range(self.decimation):
            command = np.asarray(callback(self.joint_pos(), self.joint_vel()), dtype=float).copy()
            value = command.copy()
            desired = command[WHEELS] * self.target.get('gain', 1.)
            lag = self.target.get('lag', 0.)
            self.motor_state = (self.motor_state + (1. - np.exp(-self.model.opt.timestep / lag))
                                * (desired - self.motor_state) if lag else desired.copy())
            value[WHEELS] = np.clip(self.motor_state, -12., 12.)
            value[LEGS] = command[LEGS] * leg_gain
            assert np.isfinite(value).all()
            self.data.ctrl[self.actuator_ids] = value
            self.physical.append(value.copy())
            self.commanded.append(command.copy())
            self.mujoco.mj_step(self.model, self.data)
        if self.record_startup:
            self.metadata['startup_steps'] += 1
            q = self.data.qpos[3:7]
            up_z = 1. - 2. * (q[1] ** 2 + q[2] ** 2)
            if (not np.isfinite(np.r_[self.data.qpos, self.data.qvel]).all() or up_z < np.cos(.9)
                    or self.data.qpos[2] < .025):
                raise StartupFailure(f'startup_finite_tilt_or_height z={self.data.qpos[2]} up_z={up_z}')


def config_for(checkpoint: str) -> dict:
    return json.loads((EXPORTS / f'{RUN}_{checkpoint}' / 'config.json').read_text())


_COMMAND_SERIES: dict[str, np.ndarray] = {}


def command_at(job: dict, t: float) -> np.ndarray:
    if 'command_npz' in job:
        # Recorded command replay: RL frame k of the real run drives sim policy tick k (both 50 Hz).
        key = job['command_npz']
        if key not in _COMMAND_SERIES:
            data = np.load(REPO / key)
            _COMMAND_SERIES[key] = data['command'][data['rl'].astype(bool)].astype(np.float32)
        series = _COMMAND_SERIES[key]
        index = int(round(t / DT))
        return series[index].copy() if index < len(series) else np.zeros(3, dtype=np.float32)
    spec = job.get('command')
    if not spec or t < spec['start_s']:
        return np.zeros(3, dtype=np.float32)
    # value: scalar forward speed or [vx, vy, wz]; linear ramp up from start_s, optional ramp down from end_s.
    target = np.asarray(spec['value'] if np.ndim(spec['value']) else [spec['value'], 0., 0.], dtype=float)
    ramp = max(spec.get('ramp_s', 0.), 1e-9)
    level = min(1., (t - spec['start_s']) / ramp)
    if spec.get('end_s') is not None and t >= spec['end_s']:
        level = max(0., 1. - (t - spec['end_s']) / ramp)
    return (target * level).astype(np.float32)


def rollout(job: dict) -> dict:
    # An explicit exported sim2sim config (any run) takes precedence over the 115632 export lookup.
    cfg = json.loads(Path(job['config_path']).read_text()) if job.get('config_path') else config_for(job['checkpoint'])
    started = time.monotonic()
    result = dict(execution_domain='VALIDATION_SIM', job=job, evidence_status='FAIL',
                  checkpoint_sha256=cfg['policy_interface']['checkpoint_sha256'],
                  onnx_sha256=cfg['policy_interface']['onnx_sha256'])
    try:
        assert digest(cfg['policy_interface']['checkpoint']) == result['checkpoint_sha256']
        assert digest(cfg['policy']['path']) == result['onnx_sha256']
        with patch('sim2sim.lqr.runtime.TitaMujocoEnv', lambda config: IdentEnv(config, job['physics'])):
            r = Runner(cfg, dict(seed=job['seed'], pitch=0.))
        env, p = r.env, r.playback
        env.record_startup = False
        env.assert_static()
        rows = {k: [] for k in ('q', 'dq', 'tau_cmd', 'tau_applied', 'quat', 'gyro', 'speed', 'base_z', 'command')}
        failure = []
        offset_quat, offset_rot = imu_offset(job)
        for tick in range(round(job['duration_s'] / DT)):
            o = r.observation
            command = command_at(job, tick * DT)
            history = p.last_action.copy()
            quat = quat_mul(o['quat'].astype(float), offset_quat)  # sensor frame = body frame * offset
            gyro = offset_rot.T @ o['gyro'].astype(float)
            obs = p.builder.build(ObsState(env.joint_pos(), env.joint_vel(), quat.astype(np.float32),
                                           gyro.astype(np.float32), command, history,
                                           quat_wxyz_to_rotmat(o['quat']).T @ env.base_lin_vel()))
            action = p.policy.run(['nn_output'], {'nn_input0': obs.reshape(1, -1)})[0].reshape(8)
            rows['q'].append(env.joint_pos().astype(float))
            rows['dq'].append(env.joint_vel().astype(float))
            rows['quat'].append(quat)
            rows['gyro'].append(gyro)
            rows['speed'].append(float(o['gt'][1]))
            rows['base_z'].append(float(env.data.qpos[2]))
            rows['command'].append(command.astype(float))
            env.step_with_torque_callback(lambda q, dq: p.adapter.compute(action, q, dq))
            rows['tau_cmd'].append(np.mean(env.commanded, axis=0))
            rows['tau_applied'].append(np.mean(env.physical, axis=0))
            p.last_action = action.copy()
            r.observation = r.observe()
            # Same convention as render_velocity_bias_grid.py: the crouched RL-entry pose starts just
            # outside the knee range, so only the finite/tilt/height guard applies for the first 2 s.
            if not np.isfinite(np.r_[env.data.qpos, env.data.qvel]).all() or max(abs(r.observation['rpy'][:2])) > .9 \
                    or env.data.qpos[2] < .025:
                failure = ['always_on_finite_tilt_height_guard']
            elif (tick + 1) * DT + 1e-9 >= 2.:
                failure = r.failures()
            if failure:
                break
        env.assert_static()
        signals = {k: np.asarray(v) for k, v in rows.items()}
        result.update(evidence_status='PASS' if not failure else 'FAIL', failure=failure,
                      duration_s=len(signals['speed']) * DT, physics_metadata=env.metadata,
                      startup_steps=r.startup_steps, features=features(signals, job.get('span', WINDOW_S)))
        if len(signals['speed']) > 50:
            proxy = WHEEL_RADIUS * signals['dq'][:, WHEELS].mean(1)
            result['wheel_sign_check'] = float(np.corrcoef(proxy, signals['speed'])[0, 1])
        if job.get('save_signals'):
            out = Path(job['output']) / f"{job['id']}.npz"
            out.parent.mkdir(parents=True, exist_ok=True)
            np.savez_compressed(out, **signals)
    except StartupFailure as exc:
        result.update(failure=[f'startup: {exc}'])
    result['elapsed_wall_s'] = time.monotonic() - started
    return result


def window(t: np.ndarray, start: float, end: float) -> np.ndarray:
    return (t >= start) & (t < end)


def stance_features(t, q, tau, quat, speed, z=None, span=WINDOW_S):
    m = window(t, *span)
    if m.sum() < 50:
        return None
    i05 = int(np.argmin(np.abs(t - 0.5)))
    f = dict(
        knee_q=float(q[m][:, [2, 6]].mean()),
        thigh_q=float(q[m][:, [1, 5]].mean()),
        hip_splay=float(((q[m][:, 0] - q[m][:, 4]) / 2).mean()),
        knee_tau=float(tau[m][:, [2, 6]].mean()),
        hip_tau=float(((tau[m][:, 0] - tau[m][:, 4]) / 2).mean()),
        wheel_tau=float(tau[m][:, [3, 7]].mean()),
        speed=float(speed[m].mean()),
        pitch_deg=float(pitch_deg(quat[m]).mean()),
        knee_q_0p5=float(q[i05, [2, 6]].mean()),
    )
    if z is not None:
        f['base_z'] = float(z[m].mean())
    return f


def features(signals: dict, span=WINDOW_S) -> dict | None:
    t = np.arange(len(signals['speed'])) * DT
    return stance_features(t, signals['q'], signals['tau_cmd'], signals['quat'], signals['speed'],
                           signals['base_z'], span=tuple(span))


def real_features(path: Path, span: tuple[float, float]) -> dict:
    d = np.load(path, allow_pickle=True)
    rl = d['rl'].astype(bool)
    t = d['t'] - d['t'][rl][0]
    zero = np.all(np.abs(d['command']) < 1e-9, axis=1)
    keep = rl & (zero | (t < span[0]))  # commands are allowed only before the stance window
    f = stance_features(t[keep], d['q'][keep], d['torque'][keep], d['quat'][keep], d['velocity'][keep], span=span)
    f['window_s'] = list(span)
    return f


def loss(sim: dict | None, real: dict) -> float:
    if sim is None:
        return float('inf')
    return float(sum(((sim[k] - real[k]) / tol) ** 2 for k, tol in TOLERANCE.items()))


def run_jobs(jobs: list[dict], workers: int, log_name: str, root: Path) -> list[dict]:
    results = []
    with ProcessPoolExecutor(max_workers=workers, mp_context=multiprocessing.get_context('spawn')) as pool:
        futures = {pool.submit(rollout, job): job for job in jobs}
        for future in as_completed(futures):
            results.append(future.result())
            print(f'[VALIDATION_SIM] {log_name} {len(results)}/{len(jobs)} {results[-1]["job"]["id"]} '
                  f'{results[-1]["evidence_status"]}', flush=True)
    results.sort(key=lambda r: r['job']['id'])
    write(root / f'{log_name}_results.json', results)
    return results


def grid_jobs(args, root: Path) -> list[dict]:
    jobs = []
    axes = itertools.product(args.leg_gain, args.leg_friction, args.wheel_friction, args.com, args.imu_pitch)
    for gain, leg_f, wheel_f, com, imu in axes:
        physics = dict(leg_gain=gain, leg_frictionloss=leg_f, wheel_frictionloss=wheel_f)
        if com:
            physics['com'] = com
        jobs.append(dict(id=f'g{gain:.2f}_lf{leg_f:.1f}_wf{wheel_f:.2f}_c{com * 100:+.1f}_i{imu:+.1f}',
                         checkpoint=args.checkpoint, physics=physics, sensor=dict(imu_pitch_deg=imu),
                         seed=args.seed, duration_s=args.duration, save_signals=args.save_signals,
                         output=str(root / f'{args.name}_signals')))
    return jobs


def print_table(results: list[dict], real: dict, top: int | None = None) -> None:
    keys = list(TOLERANCE)
    print(f"{'id':26s} {'loss':>8s} " + ' '.join(f'{k:>10s}' for k in keys))
    print(f"{'REAL':26s} {'':>8s} " + ' '.join(f'{real[k]:+10.3f}' for k in keys))
    rows = sorted(results, key=lambda r: loss(r.get('features'), real))
    for r in rows[:top] if top else rows:
        f = r.get('features')
        values = ' '.join(f'{f[k]:+10.3f}' for k in keys) if f else '  ' + ','.join(r.get('failure', []))
        print(f"{r['job']['id']:26s} {loss(f, real):8.1f} {values}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--output', type=Path, default=REPO / 'docs/exp/2026-10-17/real2sim_leg_wheel_grid')
    parser.add_argument('--stage', choices=['real', 'grid', 'jobs'], default='grid')
    parser.add_argument('--jobs-file', type=Path, help='JSON list of explicit jobs (stage=jobs)')
    parser.add_argument('--name', default='custom')
    parser.add_argument('--leg-gain', type=float, nargs='+', default=[1.0, 0.8, 0.65, 0.5])
    parser.add_argument('--leg-friction', type=float, nargs='+', default=[0.0, 4.0, 8.0])
    parser.add_argument('--wheel-friction', type=float, nargs='+', default=[0.0, 0.15, 0.3])
    parser.add_argument('--com', type=float, nargs='+', default=[0.0], help='base CoM x shift [m]')
    parser.add_argument('--imu-pitch', type=float, nargs='+', default=[0.0], help='IMU mount pitch [deg]')
    parser.add_argument('--checkpoint', default='model_60000')
    parser.add_argument('--compare-to', default='real_60k_free')
    parser.add_argument('--save-signals', action='store_true')
    parser.add_argument('--seed', type=int, default=104)
    parser.add_argument('--duration', type=float, default=12.0)
    parser.add_argument('--workers', type=int, default=8)
    args = parser.parse_args()
    root = args.output
    root.mkdir(parents=True, exist_ok=True)

    reals = {name: real_features(REPO / rel, span) for name, (_, rel, span) in REAL_SIGNALS.items()}
    write(root / 'real_features.json', reals)
    if args.stage == 'real':
        print(json.dumps(reals, indent=2))
        return
    if args.stage == 'grid':
        jobs = grid_jobs(args, root)
        write(root / f'{args.name}_plan.json', dict(execution_domain='VALIDATION_SIM', tolerance=TOLERANCE,
                                                    window_s=WINDOW_S, compare_to=args.compare_to, jobs=jobs))
        results = run_jobs(jobs, args.workers, args.name, root)
        print_table(results, reals[args.compare_to], top=25)
        return
    jobs = json.loads(args.jobs_file.read_text())
    results = run_jobs(jobs, args.workers, args.name, root)
    for r in results:
        target = r['job'].get('compare_to')
        if target:
            print(f"{r['job']['id']} vs {target}")
            print_table([r], reals[target])


if __name__ == '__main__':
    main()
