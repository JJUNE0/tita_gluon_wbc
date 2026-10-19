"""VALIDATION_SIM: can a leg PD gain increase plus actuator latency reproduce the real 25 Hz chatter?

Real run 2026-10-18 11:53 (A80k bundle, RL leg PD 92/2.3): hips and knees fell into a period-2
(25 Hz) policy limit cycle -- lag-1 correlation of action steps -1.0, knee command steps ~20 N m every
20 ms -- while the same policy at 60/1.5 was quiet, and so was Codex's 500 Hz nominal MuJoCo check at
92/2.3 (``docs/exp/2026-10-18/flashsac_80000_leg_pd_92_23``). That plant applies each torque in the
same 2 ms tick it is computed. This sweep adds what it lacks, only after RL entry:

- ``delay_ticks``: transport delay of every applied motor torque, in 2 ms ticks;
- ``lag_ms``: first-order lag of the applied torque (motor/driver bandwidth);
- ``leg_scale``: physical leg output = scale * command (the static real-to-sim coefficient ~0.65).

The RL leg PD is ``gain_scale`` x 60/1.5 (wheels Kd 0.5). It reuses the native C++ state machine,
observation builder and action adapter bridge and the 500 Hz loop of ``validate_sit_transitions.py``
(imported, unchanged). Delay and lag values are hypotheses, not measured hardware latencies.

``--excite`` (open-loop leg plant probe): from ``--excite-start`` on, the six leg actions are the
last policy leg action plus ``(-1)^n * excite`` (policy order), i.e. the real 25 Hz alternation
pattern, so joint responses to the same command steps can be compared. The wheel actions stay
closed-loop (policy queried every tick) so the robot keeps balancing.

``--joint-scales H S K`` (repeatable) replaces the single ``gain_scale`` with per-joint RL leg PD
scales for hip (leg_1), shoulder (leg_2) and knee (leg_3) on both sides, e.g. ``1 1 1.5333`` for a
knee-only 92/2.3. ``--frictions fitted`` adds the earlier grid's MuJoCo joint friction (legs 2.0 N m,
wheels 0.3 N m). Neither predicts the real 25 Hz chatter, which no tested sim configuration showed.
"""

from __future__ import annotations

import argparse
from collections import deque
from concurrent.futures import ProcessPoolExecutor
import copy
import itertools
import json
from pathlib import Path
import sys

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import validate_sit_transitions as vst  # noqa: E402

REPO = vst.REPO
BUNDLE = REPO / 'sim2real/tita_ws/src/tita_controller/policies/flashsac_80000'
LEGS, WHEELS, DT = vst.LEGS, vst.WHEELS, vst.DT
NOMINAL_KP, NOMINAL_KD, WHEEL_KD = 60., 1.5, .5
FRICTIONS = {'none': None, 'fitted': (2.0, 0.3)}  # (legs, wheels) MuJoCo dof_frictionloss [N m]
_WORKER = {}


def _init(policy_dir: str) -> None:
    import onnxruntime as ort
    options = ort.SessionOptions()
    options.intra_op_num_threads = 1
    _WORKER['lib'] = vst.library()
    _WORKER['policy'] = ort.InferenceSession(str(Path(policy_dir) / 'policy.onnx'), sess_options=options,
                                             providers=['CPUExecutionProvider'])


def leg_gain_scales(job: dict) -> np.ndarray:
    """Native-order RL PD scale: hip, shoulder, knee per side (wheels unused)."""
    hip, shoulder, knee = job.get('joint_scales') or [job['gain_scale']] * 3
    return np.array([hip, shoulder, knee, 0., hip, shoulder, knee, 0.])


def gain_label(job: dict) -> str:
    if job.get('joint_scales'):
        return 'h{:.3f}s{:.3f}k{:.3f}'.format(*job['joint_scales'])
    return f"g{job['gain_scale']:.3f}"


def job_id(job: dict) -> str:
    return (f"{gain_label(job)}_k{job['leg_scale']:.2f}_d{job['delay_ticks']}_l{job['lag_ms']:g}"
            f"_s{job['seed']}" + ('_excite' if job.get('excite') else '')
            + (f"_f{job['friction']}" if job.get('friction', 'none') != 'none' else ''))


def rollout(base_cfg: dict, job: dict, rl_seconds: float) -> dict:
    lib, policy = _WORKER['lib'], _WORKER['policy']
    in_name, out_name = policy.get_inputs()[0].name, policy.get_outputs()[0].name
    cfg = copy.deepcopy(base_cfg)
    s = leg_gain_scales(job)
    cfg['robot']['joint_kp'] = [NOMINAL_KP * s[j] if j in LEGS else 0. for j in range(8)]
    cfg['robot']['joint_kd'] = [NOMINAL_KD * s[j] if j in LEGS else WHEEL_KD for j in range(8)]
    native = lib.sit_create(vst.parameters(cfg))
    assert native, lib.sit_error()
    env = vst.TitaMujocoEnv(cfg)
    m, d = env.model, env.data
    friction = FRICTIONS[job.get('friction', 'none')]
    if friction:
        m.dof_frictionloss[env.qvel_addr[LEGS]] = friction[0]
        m.dof_frictionloss[env.qvel_addr[WHEELS]] = friction[1]
    floor = m.geom('floor').id
    obstacles = np.flatnonzero((m.geom_bodyid == 0) & (np.arange(m.ngeom) != floor))
    m.geom_contype[obstacles] = m.geom_conaffinity[obstacles] = 0
    rng = np.random.default_rng(job['seed'])
    env.reset(vst.SPLAY)
    d.qvel[0] = rng.uniform(-.015, .015)
    d.qvel[env.qvel_addr[LEGS]] = rng.normal(0., .01, 6)
    vst.mujoco.mj_forward(m, d)
    lib.sit_request(native, 2, env.joint_pos().astype(float), np.zeros(8))
    limits = np.array(cfg['robot']['torque_limit'])
    obs = np.empty(cfg['policy']['obs_dim'], dtype=np.float32)
    action, torque, command = np.zeros(8), np.zeros(8), np.zeros(3)
    applied_last = np.zeros(8)
    fifo, motor = None, None
    alpha = 1. - np.exp(-DT / (job['lag_ms'] * 1e-3)) if job['lag_ms'] else 1.
    rl_start, previous_state, fault = None, -1, None
    excite, base, flips = job.get('excite'), None, 0
    ticks = []  # policy ticks in RL: t, action, torque_new, torque_prev, gyro, rpy, base lin vel, q, dq
    try:
        for tick in range(round((15. + rl_seconds) / DT)):
            q = d.qpos[env.qpos_addr].copy()
            dq = d.qvel[env.qvel_addr].copy()
            for j in (1, 5):
                if q[j] < -2.5:
                    q[j] += 2 * np.pi
            quat = d.sensor('trunk_quat').data.copy()
            gyro = d.sensor('trunk_gyro').data.copy()
            lib.sit_sensors(native, q, dq, quat, gyro, 1)
            state = lib.sit_state(native)
            if state == 3 and rl_start is None:
                assert lib.sit_request(native, 4, q, torque)
                rl_start, state = float(d.time), 4
                fifo = deque([applied_last.copy()] * job['delay_ticks'])
                motor = applied_last.copy()
            if rpy_tilt(quat) > .65:
                fault = fault or dict(kind='fall_tilt', t_rl=float(d.time) - (rl_start or d.time))
                lib.sit_request(native, 1, q, torque)
            lib.sit_update(native, DT)
            state = lib.sit_state(native)
            changed = state != previous_state
            previous_state = state
            if state != 4:
                action[:] = 0.
            if state == 4:
                command[:] = 0.
            previous_torque = torque.copy()
            policy_tick = tick % 10 == 0 or changed
            if policy_tick:
                packed = np.r_[q, dq, quat, gyro, command, action].astype(np.float64)
                assert lib.sit_observation(native, packed, obs) == len(obs)
                if state == 4:
                    policy_action = policy.run([out_name], {in_name: obs[None]})[0].reshape(8).astype(float)
                    if excite and d.time - rl_start >= job['excite_start']:
                        base = action.copy() if base is None else base
                        action = base + (-1.) ** flips * np.asarray(excite)
                        action[[3, 7]] = policy_action[[3, 7]]  # policy order: wheels at 3 and 7
                        flips += 1
                    else:
                        action = policy_action
            if state == 4:
                lib.sit_action(native, action, q, dq, torque)
            else:
                lib.sit_torque(native, q, dq, torque)
            assert np.isfinite(torque).all() and (abs(torque) <= limits + 1e-9).all()
            if state == 4 and policy_tick and rl_start is not None:
                ticks.append(np.r_[d.time - rl_start, action, torque, previous_torque, gyro,
                                   vst.rpy(d.qpos[3:7]), d.qvel[:3], q, dq])
            if rl_start is not None and d.time - rl_start >= rl_seconds:
                break
            applied = torque.copy()
            applied[LEGS] *= job['leg_scale']
            if rl_start is not None:
                fifo.append(applied)
                applied = fifo.popleft()
                motor += alpha * (applied - motor)
                applied = motor.copy()
            applied_last = applied
            d.ctrl[env.actuator_ids] = applied
            vst.mujoco.mj_step(m, d)
            if not np.isfinite(np.r_[d.qpos, d.qvel]).all():
                fault = dict(kind='non_finite', t_rl=float(d.time) - (rl_start or d.time))
                break
            if rl_start is None and d.time > 15.:
                fault = dict(kind='startup_not_completed', t_rl=None)
                break
    finally:
        lib.sit_destroy(native)
        env.close()
    window = (job['excite_start'] + .5, np.inf) if excite else (3., np.inf)
    return dict(job=job, id=job_id(job), fault=fault, **metrics(np.array(ticks), window))


def rpy_tilt(quat: np.ndarray) -> float:
    w, x, y, z = quat
    return float(np.arccos(np.clip(1. - 2. * (x * x + y * y), -1., 1.)))


def alternation(x: np.ndarray) -> np.ndarray:
    """Amplitude of the period-2 (25 Hz) component of consecutive policy-tick samples, per column."""
    return np.abs(np.mean((-1.) ** np.arange(len(x))[:, None] * (x - x.mean(0)), axis=0))


def metrics(rows: np.ndarray, window: tuple[float, float] = (3., np.inf)) -> dict:
    if not len(rows):
        return dict(samples=0)
    t, action, new, prev = rows[:, 0], rows[:, 1:9], rows[:, 9:17], rows[:, 17:25]
    gyro, rpy, vel = rows[:, 25:28], rows[:, 28:31], rows[:, 31:34]
    q, dq = rows[:, 34:42], rows[:, 42:50]
    sel = (t >= window[0]) & (t <= window[1])
    if sel.sum() < 20:
        return dict(samples=int(sel.sum()), t_end=float(t[-1]))
    da = np.diff(action[sel], axis=0)
    lag1 = [float(np.corrcoef(da[1:, j], da[:-1, j])[0, 1]) if np.std(da[:, j]) > 1e-9 else 0. for j in range(8)]
    step = (new - prev)[sel][1:]
    return dict(samples=int(sel.sum()), t_end=float(t[-1]),
                d_action_rms=np.sqrt(np.mean(da ** 2, axis=0)).tolist(), d_action_lag1=lag1,
                update_step_rms=np.sqrt(np.mean(step ** 2, axis=0)).tolist(),
                q_step_rms=np.sqrt(np.mean(np.diff(q[sel], axis=0) ** 2, axis=0)).tolist(),
                dq_step_rms=np.sqrt(np.mean(np.diff(dq[sel], axis=0) ** 2, axis=0)).tolist(),
                q_alt_amp=alternation(q[sel]).tolist(), dq_alt_amp=alternation(dq[sel]).tolist(),
                gyro_std=gyro[sel].std(0).tolist(), pitch_deg=float(np.degrees(rpy[sel, 1]).mean()),
                speed_x=float(vel[sel, 0].mean()), q_mean=q[sel].mean(0).tolist())


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--gain-scales', type=float, nargs='+', default=[1.0, 1.2, 1.35, 92. / 60.])
    parser.add_argument('--leg-scales', type=float, nargs='+', default=[1.0, 0.65])
    parser.add_argument('--delay-ticks', type=int, nargs='+', default=[0, 1, 2, 3, 4, 6])
    parser.add_argument('--lag-ms', type=float, nargs='+', default=[0.])
    parser.add_argument('--seeds', type=int, nargs='+', default=[42])
    parser.add_argument('--rl-seconds', type=float, default=12.)
    parser.add_argument('--workers', type=int, default=4)
    parser.add_argument('--excite', type=float, nargs=8, default=None, metavar='A',
                        help='open-loop alternation half-amplitude per policy action (policy order)')
    parser.add_argument('--excite-start', type=float, default=6.)
    parser.add_argument('--joint-scales', type=float, nargs=3, action='append', metavar=('HIP', 'SHOULDER', 'KNEE'),
                        help='per-joint RL leg PD scale pattern (repeatable); replaces --gain-scales')
    parser.add_argument('--frictions', nargs='+', choices=sorted(FRICTIONS), default=['none'])
    args = parser.parse_args()
    out = args.output.resolve()
    assert out.is_relative_to(REPO / 'docs/exp')
    if (out / 'results.json').exists():
        parser.error('Choose a new output directory; existing evidence is preserved')
    out.mkdir(parents=True, exist_ok=True)
    cfg = json.loads((BUNDLE / 'config.json').read_text())
    assert vst.digest(BUNDLE / 'policy.onnx') == cfg['policy_interface']['onnx_sha256']
    cfg['control'] = dict(sim_timestep=DT, decimation=10)
    patterns = [dict(joint_scales=list(p)) for p in args.joint_scales] if args.joint_scales else \
        [dict(gain_scale=g) for g in args.gain_scales]
    jobs = [dict(**p, leg_scale=k, delay_ticks=n, lag_ms=l, seed=s) for p, k, n, l, s in
            itertools.product(patterns, args.leg_scales, args.delay_ticks, args.lag_ms, args.seeds)]
    if args.frictions != ['none']:
        jobs = [dict(job, friction=f) for f in args.frictions for job in jobs]
    if args.excite:
        for job in jobs:
            job.update(excite=list(args.excite), excite_start=args.excite_start)
    manifest = dict(execution_domain='VALIDATION_SIM', bundle=str(BUNDLE.relative_to(REPO)),
                    onnx_sha256=cfg['policy_interface']['onnx_sha256'],
                    checkpoint_sha256=cfg['policy_interface']['checkpoint_sha256'],
                    rl_leg_pd='gain_scale (or per-joint hip/shoulder/knee scales) x 60/1.5, wheel Kd 0.5',
                    rl_seconds=args.rl_seconds,
                    metric_window_s=[3., args.rl_seconds], jobs=len(jobs),
                    sources={str(p.relative_to(REPO)): vst.digest(p) for p in [
                        Path(__file__).resolve(), Path(vst.__file__).resolve(),
                        REPO / 'test/sim2real/sit_validation_bridge.cpp',
                        REPO / 'sim2real/tita_ws/src/tita_controller/include/tita_controller/state_machine.hpp',
                        REPO / 'sim2real/tita_ws/src/tita_controller/include/tita_controller/adapter.hpp']})
    (out / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    with ProcessPoolExecutor(args.workers, initializer=_init, initargs=(str(BUNDLE),)) as pool:
        results = list(pool.map(rollout, itertools.repeat(cfg), jobs, itertools.repeat(args.rl_seconds)))
    (out / 'results.json').write_text(json.dumps(results, indent=2) + '\n')
    print('[VALIDATION_SIM] gains k delay lag friction | hip da (lag1) knee da (lag1) | step hip/knee Nm | gyro roll '
          '| pitch | speed | q shoulder L,R | q knee L,R | fault | 25 Hz dq amp hip/shoulder/knee L,R')
    for r in results:
        j = r['job']
        head = (f"  {gain_label(j)} {j['leg_scale']:.2f} {j['delay_ticks'] * 2:3d}ms {j['lag_ms']:3g} "
                f"{j.get('friction', 'none'):6s}")
        if r.get('samples', 0) < 20:
            print(f"{head} | no window (samples {r.get('samples')}) fault {r['fault']}")
            continue
        da, lag1, step = np.array(r['d_action_rms']), np.array(r['d_action_lag1']), np.array(r['update_step_rms'])
        q = np.array(r['q_mean'])
        print(f"{head} | {da[[0, 4]].mean():.3f} ({lag1[[0, 4]].mean():+.2f}) {da[[2, 6]].mean():.3f} "
              f"({lag1[[2, 6]].mean():+.2f}) | {step[[0, 4]].mean():6.2f}/{step[[2, 6]].mean():6.2f} | "
              f"{r['gyro_std'][0]:.4f} | {r['pitch_deg']:5.2f} | {r['speed_x']:+.3f} | {q[1]:.3f},{q[5]:.3f} | "
              f"{q[2]:.3f},{q[6]:.3f} | {r['fault']} | "
              f"{np.round(np.array(r['dq_alt_amp'])[[0, 4, 1, 5, 2, 6]], 3).tolist()}")


if __name__ == '__main__':
    main()
