"""VALIDATION_SIM: leg action filter on the current real gain set (RL PD hip/shoulder 60/1.5, knee 92/2.3).

Real runs on 2026-10-18 (11:53 all legs 92/2.3, 12:56 knee only) showed a period-2 (25 Hz) policy
limit cycle that no tested MuJoCo plant reproduced (``docs/exp/2026-10-18/flashsac_80000_115354_pd92_review.md``,
``flashsac_80000_125618_knee92_review.md``). The candidate fix filters the policy actions before the
native PD adapter. The policy still observes its raw output as ``last_action``, which matches the
meaning of training's action-delay randomization.

Filters, updated once per 50 Hz policy tick, zero-order hold in between:

- ``ma2_legs``: applied[k] = (a[k] + a[k-1]) / 2 on the six leg actions. Gain is 0 at 25 Hz and 1 at DC,
  with a 10 ms delay. ``ma2_all`` also filters the wheels;
- ``ema0.5_legs``: applied[k] = 0.5 a[k] + 0.5 applied[k-1]. Gain is 1/3 at 25 Hz.

At the first RL tick the filter state is the first action, so there is no half step from zero.

Part A (``--part a``) checks low-frequency behaviour under the deployed knee-92 gains with per-joint
physical output scales (hip, shoulder, knee), joint friction and extra actuator delay. The scenarios are
standing, forward/backward 0.6 m/s, yaw +-1.0 rad/s and stops, with the native 0.5 /s command ramp.

Physical output scales:
- ``1/1/0.65`` is the intended operating point: knee 92 x 0.65 = nominal 60, but the physical knee
  torque cap is only 39 N m.
- ``0.65/0.65/0.65`` applies the static coefficient to all legs.
- ``1/1/1`` has no deficit, so the knee is 1.53x over-stiff.
- ``1/1/0.55`` and ``1/1/0.78`` bound the knee coefficient.

Part B (``--part b``) emulates the real robot's excess high-frequency loop gain with
``a + g (a - a_prev)`` on the leg actions before the filter (unit DC gain, 1 + 2 g at 25 Hz). It is a
stress proxy, not a hardware model. Its frequency shape below 25 Hz is an assumption.

Native C++ state machine, observation builder and action adapter come from
``validate_sit_transitions.py`` (imported, unchanged).
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
from scipy.signal import welch

sys.path.insert(0, str(Path(__file__).resolve().parent))
import validate_sit_transitions as vst  # noqa: E402
from sim_pd_gain_latency_chatter import FRICTIONS, alternation  # noqa: E402

REPO = vst.REPO
BUNDLE = REPO / 'sim2real/tita_ws/src/tita_controller/policies/flashsac_80000'
LEGS, WHEELS, DT = vst.LEGS, vst.WHEELS, vst.DT
LEG_ACTIONS = np.array([0, 1, 2, 4, 5, 6])  # policy order equals native order for this bundle
GAIN_SETS = {
    'knee92': ([60, 60, 92, 0, 60, 60, 92, 0], [1.5, 1.5, 2.3, .5, 1.5, 1.5, 2.3, .5]),  # deployed 12:56
    'all60': ([60, 60, 60, 0, 60, 60, 60, 0], [1.5, 1.5, 1.5, .5, 1.5, 1.5, 1.5, .5]),
    'all92': ([92, 92, 92, 0, 92, 92, 92, 0], [2.3, 2.3, 2.3, .5, 2.3, 2.3, 2.3, .5]),
    # For leg-scale policies if only the knee is weak: hip/shoulder command x0.65 matches their training.
    'hip39': ([39, 39, 60, 0, 39, 39, 60, 0], [.975, .975, 1.5, .5, .975, .975, 1.5, .5]),
}
# Part C candidates for the next real test (policy bundle or evaluation-only export directory).
CANDIDATES = {
    'A80k': BUNDLE,
    'C1_60k': REPO / 'docs/exp/2026-10-18/flashsac_legscale_sim2sim/exports/tita_flash_sac_114458_484840_model_60000',
    'C2_60k': REPO / 'docs/exp/2026-10-18/flashsac_legscale_sim2sim/exports/tita_flash_sac_114500_483968_model_60000',
}
# Joystick targets (vx, vy, wz) from the given time after RL entry; the native 0.5 /s ramp applies.
# The first 8 s after RL entry are a stand-up transient (the robot rolls and settles) and are
# reported separately; manoeuvres start at 10 s.
SCENARIOS = {
    'stand': ([(0., (0., 0., 0.))], 25.),
    'drive': ([(0., (0., 0., 0.)), (10., (.6, 0., 0.)), (17., (0., 0., 0.)), (24., (-.6, 0., 0.)),
               (31., (0., 0., 0.)), (38., (0., 0., 1.)), (43., (0., 0., 0.)), (49., (0., 0., -1.)),
               (54., (0., 0., 0.))], 60.),
}
ENTRY_S = 8.
FRICTIONS = {**FRICTIONS, 'legs2': (2.0, 0.0)}  # leg Coulomb friction only (wheels frictionless)
# Part D: (policy, gain set) pairs as they would be deployed.
DEPLOY_PAIRS = [('A80k', 'knee92'), ('A80k', 'all60'), ('C1_60k', 'all60'), ('C2_60k', 'all60')]
RAMP = .5  # command units per second (tita_node kCommandRamp)
_WORKER = {}


class ActionFilter:
    """Applied actions from raw policy outputs; ``preemphasis`` is the Part B plant proxy."""

    def __init__(self, kind: str, preemphasis: float):
        name, _, joints = kind.partition('_')
        self.kind, self.gain = name, preemphasis
        self.joints = np.arange(8) if joints == 'all' else LEG_ACTIONS
        self.prev_raw = self.prev_pe = self.prev_out = None

    def __call__(self, raw: np.ndarray) -> np.ndarray:
        if self.prev_raw is None:
            self.prev_raw, self.prev_pe, self.prev_out = raw.copy(), raw.copy(), raw.copy()
        pe = raw.copy()
        pe[LEG_ACTIONS] += self.gain * (raw[LEG_ACTIONS] - self.prev_raw[LEG_ACTIONS])
        out = pe.copy()
        j = self.joints
        if self.kind == 'ma2':
            out[j] = .5 * (pe[j] + self.prev_pe[j])
        elif self.kind.startswith('ema'):
            alpha = float(self.kind[3:])
            out[j] = alpha * pe[j] + (1. - alpha) * self.prev_out[j]
        elif self.kind != 'none':
            raise ValueError(self.kind)
        self.prev_raw, self.prev_pe, self.prev_out = raw.copy(), pe, out.copy()
        return out


def _init(policy_dir: str) -> None:
    _WORKER['lib'] = vst.library()
    _WORKER['default_policy'] = policy_dir
    _WORKER['policies'] = {}


def policy_session(policy_dir: str):
    if policy_dir not in _WORKER['policies']:
        import onnxruntime as ort
        options = ort.SessionOptions()
        options.intra_op_num_threads = 1
        _WORKER['policies'][policy_dir] = ort.InferenceSession(
            str(Path(policy_dir) / 'policy.onnx'), sess_options=options, providers=['CPUExecutionProvider'])
    return _WORKER['policies'][policy_dir]


def load_config(bundle: Path) -> dict:
    cfg = json.loads((bundle / 'config.json').read_text())
    assert vst.digest(bundle / 'policy.onnx') == cfg['policy_interface']['onnx_sha256']
    assert [t['joint'] for t in cfg['policy_interface']['actions']] == vst.NATIVE_JOINTS, 'policy order != native'
    cfg['control'] = dict(sim_timestep=DT, decimation=10)
    return cfg


def job_id(job: dict) -> str:
    return ((f"{job['policy']}_" if 'policy' in job else '') +
            f"{job['scenario']}_{job['gains']}_{job['filter']}_pe{job['preemphasis']:g}"
            f"_k{'-'.join(f'{x:g}' for x in job['leg_scale'])}_f{job['friction']}_d{job['delay_ticks']}_s{job['seed']}")


def physical_scale(job: dict) -> np.ndarray:
    """Native-order physical output scale for hip, shoulder, knee per side (wheels 1)."""
    hip, shoulder, knee = job['leg_scale']
    return np.array([hip, shoulder, knee, 1., hip, shoulder, knee, 1.])


def target_at(schedule: list, t: float) -> np.ndarray:
    value = schedule[0][1]
    for start, target in schedule:
        if t >= start:
            value = target
    return np.array(value, dtype=float)


def rollout(base_cfg: dict, job: dict) -> dict:
    bundle = CANDIDATES[job['policy']] if 'policy' in job else Path(_WORKER['default_policy'])
    lib, policy = _WORKER['lib'], policy_session(str(bundle))
    in_name, out_name = policy.get_inputs()[0].name, policy.get_outputs()[0].name
    cfg = load_config(bundle) if 'policy' in job else copy.deepcopy(base_cfg)
    kp, kd = GAIN_SETS[job['gains']]
    cfg['robot']['joint_kp'], cfg['robot']['joint_kd'] = [float(x) for x in kp], [float(x) for x in kd]
    native = lib.sit_create(vst.parameters(cfg))
    assert native, lib.sit_error()
    env = vst.TitaMujocoEnv(cfg)
    m, d = env.model, env.data
    floor = m.geom('floor').id
    obstacles = np.flatnonzero((m.geom_bodyid == 0) & (np.arange(m.ngeom) != floor))
    m.geom_contype[obstacles] = m.geom_conaffinity[obstacles] = 0
    friction = FRICTIONS[job['friction']]
    if friction:
        m.dof_frictionloss[env.qvel_addr[LEGS]] = friction[0]
        m.dof_frictionloss[env.qvel_addr[WHEELS]] = friction[1]
    rng = np.random.default_rng(job['seed'])
    env.reset(vst.SPLAY)
    d.qvel[0] = rng.uniform(-.015, .015)
    d.qvel[env.qvel_addr[LEGS]] = rng.normal(0., .01, 6)
    vst.mujoco.mj_forward(m, d)
    lib.sit_request(native, 2, env.joint_pos().astype(float), np.zeros(8))
    schedule, duration = SCENARIOS[job['scenario']]
    limits = np.array(cfg['robot']['torque_limit'])
    scale = physical_scale(job)
    obs = np.empty(cfg['policy']['obs_dim'], dtype=np.float32)
    raw, applied, torque, command = np.zeros(8), np.zeros(8), np.zeros(8), np.zeros(3)
    applied_last = np.zeros(8)
    filt = ActionFilter(job['filter'], job['preemphasis'])
    fifo = None
    rl_start, previous_state, fault = None, -1, None
    clips = dict(knee_first_1s=0, wheel_first_1s=0, leg_ticks=0, wheel_ticks=0, rl_ticks=0)
    rows = []
    try:
        for tick in range(round((15. + duration) / DT)):
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
            w, x, y, z = quat
            if np.arccos(np.clip(1. - 2. * (x * x + y * y), -1., 1.)) > .65:
                fault = fault or dict(kind='fall_tilt', t_rl=float(d.time) - (rl_start or d.time))
                lib.sit_request(native, 1, q, torque)
            lib.sit_update(native, DT)
            state = lib.sit_state(native)
            changed = state != previous_state
            previous_state = state
            t_rl = float(d.time) - rl_start if rl_start is not None else None
            if state == 4:
                command += np.clip(target_at(schedule, t_rl) - command, -RAMP * DT, RAMP * DT)
            else:
                command[:] = 0.
                raw[:] = 0.
            previous_torque = torque.copy()
            policy_tick = tick % 10 == 0 or changed
            if policy_tick:
                packed = np.r_[q, dq, quat, gyro, command, raw].astype(np.float64)
                assert lib.sit_observation(native, packed, obs) == len(obs)
                if state == 4:
                    raw = policy.run([out_name], {in_name: obs[None]})[0].reshape(8).astype(float)
                    applied = filt(raw)
            if state == 4:
                lib.sit_action(native, applied, q, dq, torque)
            else:
                lib.sit_torque(native, q, dq, torque)
            assert np.isfinite(torque).all() and (abs(torque) <= limits + 1e-9).all()
            if state == 4:
                leg_clip = np.abs(torque[LEGS]) >= limits[LEGS] - 1e-9
                wheel_clip = np.abs(torque[WHEELS]) >= limits[WHEELS] - 1e-9
                clips['rl_ticks'] += 1
                clips['leg_ticks'] += int(leg_clip.any())
                clips['wheel_ticks'] += int(wheel_clip.any())
                if t_rl < 1.:
                    clips['knee_first_1s'] += int((np.abs(torque[[2, 6]]) >= 60. - 1e-9).any())
                    clips['wheel_first_1s'] += int(wheel_clip.any())
                if policy_tick:
                    rpy = vst.rpy(d.qpos[3:7])
                    v_fwd = np.cos(rpy[2]) * d.qvel[0] + np.sin(rpy[2]) * d.qvel[1]
                    rows.append(np.r_[t_rl, command, raw, applied, torque, previous_torque, gyro, rpy, v_fwd,
                                      d.qpos[2], q, dq])
            if rl_start is not None and t_rl >= duration:
                break
            out = torque * scale
            if rl_start is not None:
                fifo.append(out)
                out = fifo.popleft()
            applied_last = out
            d.ctrl[env.actuator_ids] = out
            vst.mujoco.mj_step(m, d)
            if not np.isfinite(np.r_[d.qpos, d.qvel]).all():
                fault = dict(kind='non_finite', t_rl=t_rl)
                break
            if rl_start is None and d.time > 15.:
                fault = dict(kind='startup_not_completed', t_rl=None)
                break
    finally:
        lib.sit_destroy(native)
        env.close()
    return dict(job=job, id=job_id(job), fault=fault, clips=clips, **summarize(np.array(rows), job['scenario']))


def oscillation(raw: np.ndarray, applied: np.ndarray, new: np.ndarray, prev: np.ndarray) -> dict:
    """Leg action/torque chatter metrics over consecutive policy ticks."""
    da = np.diff(raw, axis=0)
    lag1 = [float(np.corrcoef(da[1:, j], da[:-1, j])[0, 1]) if np.std(da[:, j]) > 1e-9 else 0. for j in range(8)]
    peak = None
    if len(raw) >= 128:
        f, p = welch(raw - raw.mean(0), fs=50., nperseg=128, axis=0)
        above = f >= 1.
        peak = f[above][np.argmax(p[above][:, LEG_ACTIONS].sum(1))].item()
    return dict(raw_d_action_rms=np.sqrt(np.mean(da ** 2, axis=0)).tolist(), raw_d_action_lag1=lag1,
                applied_d_action_rms=np.sqrt(np.mean(np.diff(applied, axis=0) ** 2, axis=0)).tolist(),
                raw_25hz_amp=alternation(raw).tolist(), applied_25hz_amp=alternation(applied).tolist(),
                update_step_rms=np.sqrt(np.mean((new - prev)[1:] ** 2, axis=0)).tolist(),
                leg_action_psd_peak_hz=peak)


def summarize(rows: np.ndarray, scenario: str) -> dict:
    if len(rows) < 50:
        return dict(samples=int(len(rows)))
    t, cmd, raw, applied = rows[:, 0], rows[:, 1:4], rows[:, 4:12], rows[:, 12:20]
    new, prev, gyro, rpy = rows[:, 20:28], rows[:, 28:36], rows[:, 36:39], rows[:, 39:42]
    v, z, q = rows[:, 42], rows[:, 43], rows[:, 44:52]
    start, entry, steady = t < 3., t < ENTRY_S, t >= ENTRY_S
    out = dict(samples=int(len(rows)), t_end=float(t[-1]),
               startup_pitch_peak_deg=float(np.degrees(np.abs(rpy[start, 1])).max()),
               entry_peak_speed=float(np.abs(v[entry]).max()), entry_travel_m=float(np.sum(v[entry]) * .02),
               max_abs_pitch_deg=float(np.degrees(np.abs(rpy[:, 1])).max()), min_base_z=float(z.min()))
    if scenario == 'stand':
        sel = steady
        out.update(pitch_deg=float(np.degrees(rpy[sel, 1]).mean()), pitch_std_deg=float(np.degrees(rpy[sel, 1]).std()),
                   speed=float(v[sel].mean()), gyro_std=gyro[sel].std(0).tolist(), q_mean=q[sel].mean(0).tolist(),
                   **oscillation(raw[sel], applied[sel], new[sel], prev[sel]))
        return out
    schedule, duration = SCENARIOS[scenario]
    segments, previous = [], np.zeros(3)
    for i, (start_s, target) in enumerate(schedule):
        end_s = schedule[i + 1][0] if i + 1 < len(schedule) else duration
        target = np.array(target, dtype=float)
        ramp = np.abs(target - previous).max() / RAMP
        previous = target
        settle = start_s + ramp + (1. if target.any() else 2.)
        sel = (t >= settle) & (t < end_s)
        if not sel.any():
            continue
        seg = dict(start_s=start_s, target=target.tolist(), window=[settle, end_s])
        if target[0]:
            seg.update(vx_error=float(np.mean(v[sel] - cmd[sel, 0])))
        elif target[2]:
            seg.update(wz_error=float(np.mean(gyro[sel, 2] - cmd[sel, 2])))
        else:
            seg.update(stop_speed=float(np.mean(np.abs(v[sel]))), stop_speed_max=float(np.abs(v[sel]).max()),
                       pitch_deg=float(np.degrees(rpy[sel, 1]).mean()))
        segments.append(seg)
    out.update(segments=segments, **oscillation(raw[steady], applied[steady], new[steady], prev[steady]))
    return out


def plant_label(job: dict) -> str:
    return '/'.join(f'{x:g}' for x in job['leg_scale']) + ('+fric' if job['friction'] == 'fitted' else '')


def print_tables(results: list, part: str) -> None:
    """Delay columns 0 | 4 | 8 | 12 ms (part a) or 0 | 4 ms (part b)."""
    pick = lambda **kw: sorted([r for r in results if all(r['job'][k] == v for k, v in kw.items()
                                                          if k != 'plant') and plant_label(r['job']) == kw['plant']],
                               key=lambda r: r['job']['delay_ticks'])
    if part == 'd':
        print('STAND from 8 s, delay 0: pitch / pitch std / raw |da| hip,knee / raw lag-1 hip,knee / knee step N m / '
              'leg action PSD peak')
        for r in results:
            j = r['job']
            head = f"  {j['policy']:7s} {j['gains']:6s} {plant_label(j):15s} fric {j['friction']:5s} g {j['preemphasis']:3g} |"
            if r['fault'] or 'raw_d_action_rms' not in r:
                print(f"{head} FALL {r['fault']}")
                continue
            da, l1, st = (np.array(r[k]) for k in ('raw_d_action_rms', 'raw_d_action_lag1', 'update_step_rms'))
            print(f"{head} {r['pitch_deg']:4.1f} / {r['pitch_std_deg']:.2f} / {da[[0, 4]].mean():.3f},"
                  f"{da[[2, 6]].mean():.3f} / {l1[[0, 4]].mean():+.2f},{l1[[2, 6]].mean():+.2f} / "
                  f"{st[[2, 6]].mean():5.1f} / {r['leg_action_psd_peak_hz']:.1f} Hz")
        return
    if part == 'c':
        print('per policy / gains / plant, delay 0 | 4 ms. STAND: pitch / speed / pitch std / startup pitch peak; '
              'DRIVE: stop |v| mean(max) / vx err +0.6,-0.6 / wz err +1,-1')
        for policy in dict.fromkeys(r['job']['policy'] for r in results):
            for gains in dict.fromkeys(r['job']['gains'] for r in results):
                for plant in dict.fromkeys(plant_label(r['job']) for r in results):
                    cells = []
                    for scenario in ['stand', 'drive']:
                        for r in sorted([r for r in results if r['job']['policy'] == policy and r['job']['gains'] == gains
                                         and plant_label(r['job']) == plant and r['job']['scenario'] == scenario],
                                        key=lambda r: r['job']['delay_ticks']):
                            if r['fault'] or r.get('samples', 0) < 50:
                                cells.append(f"FALL {r['fault']['t_rl'] if r['fault'] else '?'}")
                            elif scenario == 'stand':
                                cells.append(f"{r['pitch_deg']:4.1f}/{r['speed']:+.3f}/{r['pitch_std_deg']:.2f}/"
                                             f"{r['startup_pitch_peak_deg']:.1f}")
                            else:
                                stops = [s['stop_speed'] for s in r['segments'][1:] if 'stop_speed' in s]
                                vx = [s['vx_error'] for s in r['segments'] if 'vx_error' in s]
                                wz = [s['wz_error'] for s in r['segments'] if 'wz_error' in s]
                                cells.append(f'{np.mean(stops):.2f}({np.max(stops):.2f})/{vx[0]:+.2f},{vx[1]:+.2f}/'
                                             f'{wz[0]:+.2f},{wz[1]:+.2f}')
                    print(f'  {policy:7s} {gains:6s} {plant:15s} | ' + ' | '.join(cells))
        return
    if part == 'a':
        plants = list(dict.fromkeys(plant_label(r['job']) for r in results))
        print('STAND from 8 s: pitch deg / speed m/s / pitch std / raw |da| hip,knee / startup pitch peak / entry travel m')
        for plant in plants:
            for f in ['none', 'ma2_legs', 'ma2_all', 'ema0.5_legs']:
                cells = [f"FALL {r['fault']['t_rl']:.1f}s" if r['fault'] else
                         f"{r['pitch_deg']:4.1f}/{r['speed']:+.3f}/{r['pitch_std_deg']:.2f}/"
                         f"{np.mean(np.array(r['raw_d_action_rms'])[[0, 4]]):.3f},"
                         f"{np.mean(np.array(r['raw_d_action_rms'])[[2, 6]]):.3f}/{r['startup_pitch_peak_deg']:.1f}/"
                         f"{r['entry_travel_m']:+.2f}" for r in pick(scenario='stand', filter=f, plant=plant)]
                print(f'  {plant:16s} {f:12s} | ' + ' | '.join(cells))
        print('DRIVE: post-manoeuvre stop |v| mean (max) / vx error +0.6,-0.6 / wz error +1,-1 / max |pitch| / wheel clip')
        for plant in plants:
            for f in ['none', 'ma2_legs', 'ma2_all', 'ema0.5_legs']:
                cells = []
                for r in pick(scenario='drive', filter=f, plant=plant):
                    if r['fault']:
                        cells.append(f"FALL {r['fault']['t_rl']:.1f}s")
                        continue
                    stops = [s['stop_speed'] for s in r['segments'][1:] if 'stop_speed' in s]
                    vx = [s['vx_error'] for s in r['segments'] if 'vx_error' in s]
                    wz = [s['wz_error'] for s in r['segments'] if 'wz_error' in s]
                    cells.append(f'{np.mean(stops):.2f}({np.max(stops):.2f})/{vx[0]:+.2f},{vx[1]:+.2f}/{wz[0]:+.2f},'
                                 f"{wz[1]:+.2f}/{r['max_abs_pitch_deg']:.0f}/"
                                 f"{r['clips']['wheel_ticks'] / r['clips']['rl_ticks']:.3f}")
                print(f'  {plant:16s} {f:12s} | ' + ' | '.join(cells))
        return
    print('STAND from 8 s per filter: raw |da| hip,knee / raw lag-1 hip,knee / applied 25 Hz amp hip,knee / '
          'leg action PSD peak / knee update step N m / pitch std deg')
    for gains in ['all60', 'knee92', 'all92']:
        for pe in sorted({r['job']['preemphasis'] for r in results}):
            for r_none, r_ma2 in zip(pick(gains=gains, preemphasis=pe, filter='none', plant='1/1/0.65'),
                                     pick(gains=gains, preemphasis=pe, filter='ma2_legs', plant='1/1/0.65')):
                cells = []
                for r in (r_none, r_ma2):
                    if r['fault'] or 'raw_d_action_rms' not in r:
                        cells.append(f"FALL {r['fault']['t_rl']:.1f}s")
                        continue
                    da, l1 = np.array(r['raw_d_action_rms']), np.array(r['raw_d_action_lag1'])
                    aa, st = np.array(r['applied_25hz_amp']), np.array(r['update_step_rms'])
                    cells.append(f'{da[[0, 4]].mean():.3f},{da[[2, 6]].mean():.3f}/{l1[[0, 4]].mean():+.2f},'
                                 f'{l1[[2, 6]].mean():+.2f}/{aa[[0, 4]].mean():.3f},{aa[[2, 6]].mean():.3f}/'
                                 f"{r['leg_action_psd_peak_hz']:.1f}Hz/{st[[2, 6]].mean():.1f}/{r['pitch_std_deg']:.2f}")
                print(f"  {gains:6s} pe {pe:3g} d {r_none['job']['delay_ticks'] * 2:2d} ms | none {cells[0]} || "
                      f'ma2_legs {cells[1]}')


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--part', choices=['a', 'b', 'c', 'd'], required=True)
    parser.add_argument('--workers', type=int, default=4)
    parser.add_argument('--seeds', type=int, nargs='+', default=[42])
    parser.add_argument('--tables-only', action='store_true', help='print tables from an existing results.json')
    args = parser.parse_args()
    out = args.output.resolve()
    assert out.is_relative_to(REPO / 'docs/exp')
    if args.tables_only:
        print_tables(json.loads((out / 'results.json').read_text()), args.part)
        return
    if (out / 'results.json').exists():
        parser.error('Choose a new output directory; existing evidence is preserved')
    out.mkdir(parents=True, exist_ok=True)
    cfg = load_config(BUNDLE)
    filters = ['none', 'ma2_legs', 'ma2_all', 'ema0.5_legs']
    candidates = {}
    if args.part == 'd':
        # Deploy pairs: leg friction damping at g = 0, and the Part B 25 Hz proxy margin without friction.
        plants = [(1., 1., .65), (.65, .65, .65)]
        settings = [('none', 0.), ('legs2', 0.), ('none', .5), ('none', 1.), ('none', 1.5)]
        jobs = [dict(policy=policy, scenario='stand', gains=gains, filter='none', preemphasis=pe, leg_scale=plant,
                     friction=friction, delay_ticks=0, seed=seed)
                for policy, gains in DEPLOY_PAIRS for plant in plants for friction, pe in settings for seed in args.seeds]
    if args.part in ('c', 'd'):
        candidates = {k: dict(path=str(v.relative_to(REPO)), onnx_sha256=load_config(v)['policy_interface']['onnx_sha256'],
                              checkpoint_sha256=load_config(v)['policy_interface']['checkpoint_sha256'])
                      for k, v in CANDIDATES.items()}
        grid = []
    if args.part == 'c':
        # Candidate policy x gain set comparison without a filter (not implemented on the robot yet).
        plants = [(1., 1., .65), (.65, .65, .65), (1., 1., 1.)]
        jobs = [dict(policy=policy, scenario=scenario, gains=gains, filter='none', preemphasis=0., leg_scale=plant,
                     friction='none', delay_ticks=delay, seed=seed)
                for policy in CANDIDATES for gains in ['all60', 'knee92', 'hip39'] for plant in plants
                for scenario in ['stand', 'drive'] for delay in [0, 2] for seed in args.seeds]
    elif args.part == 'a':
        # Frictionless plants are primary. The earlier grid's fitted friction (wheels 0.3 N m) breaks stopping
        # even for the nominal plant, unlike the real A80k runs, so it is only a stress case at the operating point.
        plants = [((1., 1., .65), 'none'), ((1., 1., .55), 'none'), ((1., 1., .78), 'none'), ((1., 1., 1.), 'none'),
                  ((.65, .65, .65), 'none'), ((1., 1., .65), 'fitted')]
        grid = [(scenario, 'knee92', f, 0., plant, friction, delay, seed)
                for scenario in ['stand', 'drive'] for f in filters for plant, friction in plants
                for delay in [0, 2, 4, 6] for seed in args.seeds]
    elif args.part == 'b':
        grid = itertools.product(['stand'], ['all60', 'knee92', 'all92'], ['none', 'ma2_legs'],
                                 [0., .5, 1., 1.5, 2., 3.], [(1., 1., .65)], ['none'], [0, 2], args.seeds)
    keys = ['scenario', 'gains', 'filter', 'preemphasis', 'leg_scale', 'friction', 'delay_ticks', 'seed']
    if args.part in ('a', 'b'):
        jobs = [dict(zip(keys, values)) for values in grid]
    manifest = dict(execution_domain='VALIDATION_SIM', part=args.part, bundle=str(BUNDLE.relative_to(REPO)),
                    candidates=candidates,
                    onnx_sha256=cfg['policy_interface']['onnx_sha256'],
                    checkpoint_sha256=cfg['policy_interface']['checkpoint_sha256'], jobs=len(jobs),
                    gain_sets={k: dict(kp=v[0], kd=v[1]) for k, v in GAIN_SETS.items()},
                    scenarios={k: dict(schedule=v[0], duration_s=v[1]) for k, v in SCENARIOS.items()},
                    sources={str(p.relative_to(REPO)): vst.digest(p) for p in [
                        Path(__file__).resolve(), Path(vst.__file__).resolve(),
                        REPO / 'test/sim2real/sim_pd_gain_latency_chatter.py',
                        REPO / 'test/sim2real/sit_validation_bridge.cpp',
                        REPO / 'sim2real/tita_ws/src/tita_controller/include/tita_controller/state_machine.hpp',
                        REPO / 'sim2real/tita_ws/src/tita_controller/include/tita_controller/adapter.hpp']})
    (out / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    with ProcessPoolExecutor(args.workers, initializer=_init, initargs=(str(BUNDLE),)) as pool:
        results = list(pool.map(rollout, itertools.repeat(cfg), jobs))
    (out / 'results.json').write_text(json.dumps(results, indent=2) + '\n')
    print(f'[VALIDATION_SIM] part {args.part}: {len(results)} jobs, faults: '
          f"{[r['id'] for r in results if r['fault']]}")
    print_tables(results, args.part)


if __name__ == '__main__':
    main()
