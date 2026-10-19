"""VALIDATION_SIM: checkpoint screen for the 2026-10-18 sphere-wheel / MA2 / fast-command runs.

Uses the production sim2sim pieces (TitaMujocoEnv, ObservationBuilder with the stateful wheel position
error, ActionAdapter, LegActionFilter with the mode recorded in each exported config, StateMachine) at
500 Hz physics / 50 Hz inference. Plants (robustness proxies, not measured hardware values):
- A: sphere (point-contact) wheels, knee PD x L0.60 / R0.75 (reproduced the real 50k knee sag and yaw);
- B: original cylinder wheels, same knees.
Scenarios: stand 32 s, drive (Codex screen schedule, 0.5/s ramp), drive_fast (+-1.5 m/s, +-3 rad/s,
2/s ramp; fast-command runs only). 25 Hz proxy: plant A stand with leg action pre-emphasis
raw + g (raw - previous raw) before the leg filter (``test/sim2real/sim_leg_action_filter.py`` part d).
Ground truth (base pose/velocity) is used only for metrics. No robot command.

Run --prepare with the Isaac Lab interpreter (ONNX export), --evaluate / --summarize with the cosim venv.
"""
from __future__ import annotations

import argparse
from concurrent.futures import ProcessPoolExecutor, as_completed
import copy
import json
from pathlib import Path
import re
import sys
import time

import numpy as np

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / 'sim2sim/sim2sim_ros2_jazzy'))
LOGS = REPO / 'lab/ddt_lab/logs/flash_sac'
RUNS = {
    'exp1_sphere_ma2': ('tita_flash_sac_220437_190135', [50000, 60000, 70000, 80000, 90000, 100000]),
    'exp2_sphere_noma2': ('tita_flash_sac_220437_199621', [50000, 60000, 70000, 80000, 90000, 100000]),
    'exp3_sphere_ma2_fast': ('tita_flash_sac_034313_051978', [50000, 60000, 70000, 80000, 90000, 100000]),
    'exp4_sphere_noma2_fast': ('tita_flash_sac_055626_985460', [50000, 60000, 70000, 80000, 90000, 100000]),
    'exp5_cyl_noma2': ('', [50000, 60000, 70000, 80000, 90000, 100000]),
    'ref_posma2': ('tita_flash_sac_180212_290240', [50000, 75000]),   # real-tested (50k yawed, 75k good)
    # 2026-10-19 heading run: exp3 + heading drift reward + actor/critic gyro heading error (35 observations)
    'exp6_heading_ma2_fast': ('tita_flash_sac_102630_755853', [50000, 60000, 70000, 80000, 90000, 100000]),
    # warmup-0 heading run: exp2 (sphere, no MA2, default commands) + heading reward/observation without warmup
    'exp7_heading_noma2_w0': ('tita_flash_sac_125547_806511', [35000, 40000, 45000, 50000, 55000, 60000, 65000,
                                                               70000, 75000, 80000, 85000, 90000, 95000, 100000]),
}
FAST = {'exp3_sphere_ma2_fast', 'exp4_sphere_noma2_fast', 'exp6_heading_ma2_fast'}
PLANTS = {'A': dict(wheel='sphere', knee=(.60, .75)), 'B': dict(wheel='cylinder', knee=(.60, .75)),
          # --robust: knee mirrored / symmetric / nominal on sphere wheels
          'A_mirror': dict(wheel='sphere', knee=(.75, .60)), 'A_sym068': dict(wheel='sphere', knee=(.68, .68)),
          'A_sym055': dict(wheel='sphere', knee=(.55, .55)), 'A_nom': dict(wheel='sphere', knee=(1., 1.)),
          # interactive sim2sim viewer plant: public MuJoCo cylinder wheels, nominal knees
          'B_nom': dict(wheel='cylinder', knee=(1., 1.))}
# --g6 (gap.md G6, 2026-10-19 65k real fore-aft hunting): plant A + base-link CoM x shift [m] (base 11.4 of 25.7 kg)
# or an IMU pitch mounting offset [deg] (measured quaternion/gyro = true rotated about body y; physics unchanged)
G6_PLANTS = {f'A_com{dx:+g}': dict(PLANTS['A'], com_dx=dx / 100) for dx in (-2, -4, -6, 2, 4)}
G6_PLANTS.update({f'A_imu{d:+g}': dict(PLANTS['A'], imu_pitch_deg=d) for d in (-1.5, -3, 1.5, 3)})
# compensation check: a backward CoM shift plus an opposite measured-pitch offset (deployable gravity-obs correction)
G6_PLANTS.update({f'A_com{dx:+g}_imu{d:+g}': dict(PLANTS['A'], com_dx=dx / 100, imu_pitch_deg=d)
                  for dx in (-4, -6) for d in (-1.5, -3, -4.5)})
PLANTS.update(G6_PLANTS)
G6 = [('exp7_heading_noma2_w0', 50000), ('exp7_heading_noma2_w0', 65000)]
ROBUST = [('exp2_sphere_noma2', 60000), ('exp1_sphere_ma2', 70000), ('exp1_sphere_ma2', 90000),
          ('exp1_sphere_ma2', 100000), ('exp3_sphere_ma2_fast', 70000), ('ref_posma2', 75000),
          ('exp7_heading_noma2_w0', 45000), ('exp7_heading_noma2_w0', 50000),
          ('exp7_heading_noma2_w0', 60000), ('exp7_heading_noma2_w0', 65000)]
ROBUST += [('exp7_heading_noma2_w0', step) for step in range(75000, 100001, 5000)]   # exp7 tail after training end
DT = .02
DRIVE = [(0., 0., 0.), (8., .6, 0.), (14., 0., 0.), (20., -.6, 0.), (26., 0., 0.), (32., 0., 1.), (38., 0., 0.),
         (44., 0., -1.), (50., 0., 0.), (56., 1., 0.), (62., 0., 0.), (68., -1., 0.), (74., 0., 0.),
         (80., 0., 1.5), (86., 0., 0.), (92., 0., -1.5), (98., 0., 0.)]
DRIVE_FAST = [(0., 0., 0.), (8., 1.5, 0.), (14., 0., 0.), (20., -1.5, 0.), (26., 0., 0.), (32., 0., 3.),
              (38., 0., 0.), (44., 0., -3.), (50., 0., 0.), (56., 1., 2.), (62., 0., 0.)]
SCENARIOS = {'stand': dict(duration=32., schedule=[(0., 0., 0.)], ramp=.5),
             'drive': dict(duration=106., schedule=DRIVE, ramp=.5),
             'drive_fast': dict(duration=70., schedule=DRIVE_FAST, ramp=2.),
             'probe': dict(duration=20., schedule=[(0., 0., 0.)], ramp=.5),
             # 5-minute zero-command hold (render_real2sim_progression.py presentation video)
             'stand300': dict(duration=300., schedule=[(0., 0., 0.)], ramp=.5),
             # in-place turn check (2026-10-19 real run: backward arc + thigh flexion while turning)
             'turn': dict(duration=30., schedule=[(0., 0., 0.), (8., 0., 1.), (13., 0., 0.), (18., 0., -1.), (23., 0., 0.)],
                          ramp=.5)}
LEGS = [0, 1, 2, 4, 5, 6]


def quat_mul(a, b):
    """Hamilton product of wxyz quaternions."""
    w1, x1, y1, z1 = a
    w2, x2, y2, z2 = b
    return np.array([w1 * w2 - x1 * x2 - y1 * y2 - z1 * z2, w1 * x2 + x1 * w2 + y1 * z2 - z1 * y2,
                     w1 * y2 - x1 * z2 + y1 * w2 + z1 * x2, w1 * z2 + x1 * y2 - y1 * x2 + z1 * w2], dtype=np.float32)


def write_json(path, value):
    Path(path).write_text(json.dumps(value, indent=1, allow_nan=False) + '\n')


def run_dir(tag, run):
    """exp5 starts last in the chain; take its run directory from the training console log."""
    log = REPO / 'docs/exp/2026-10-18/sphere_wheel_experiments/cyl-noma2-s42_console.log'
    if run or tag != 'exp5_cyl_noma2' or not log.exists():
        return run
    match = re.search(r'logs/flash_sac/(tita_flash_sac_[0-9_]+)', log.read_text(errors='ignore'))
    return match.group(1) if match else ''


TAGS = None  # --tags: restrict prepare/evaluate to these run tags


def checkpoint_dirs():
    for tag, (run, steps) in RUNS.items():
        if TAGS and tag not in TAGS:
            continue
        run = run_dir(tag, run)
        if not run:
            continue
        for step in steps:
            path = LOGS / run / f'model_{step}'
            if (path / 'actor.pt').is_file():
                yield tag, step, path


def prepare(output):
    from sim2sim_ros2_jazzy.checkpoint import prepare_checkpoint, prepared_config, sha256
    policies_path = output / 'policies.json'
    keep = json.loads(policies_path.read_text()) if policies_path.exists() and TAGS else []
    rows = []
    for tag, step, path in checkpoint_dirs():
        config = prepared_config(path) or prepare_checkpoint(path, Path.home() / 'venvs/cosim_ros2_jazzy/bin/python')
        cfg = json.loads(Path(config).read_text())
        pi = cfg['policy_interface']
        rows.append(dict(tag=tag, step=step, config=str(config), checkpoint_sha256=pi['checkpoint_sha256'],
                         onnx_sha256=pi['onnx_sha256'], config_sha256=sha256(config),
                         leg_action_filter=pi['leg_action_filter'], obs_dim=cfg['policy']['obs_dim'],
                         parity=json.loads((Path(config).parent / 'manifest.json').read_text())['parity']))
        print(f"[VALIDATION_SIM] prepared {tag} {step} filter={pi['leg_action_filter']} {rows[-1]['parity']}", flush=True)
    done = {(r['tag'], r['step']) for r in rows}
    write_json(policies_path, [r for r in keep if (r['tag'], r['step']) not in done] + rows)


def rollout(job):
    import mujoco
    import onnxruntime as ort
    from sim2sim_ros2_jazzy.adapter import (ActionAdapter, LegActionFilter, ObservationBuilder, ObsState,
                                            quat_wxyz_to_rotmat, quat_wxyz_to_rpy)
    from sim2sim_ros2_jazzy.mujoco_env import TitaMujocoEnv
    from sim2sim_ros2_jazzy.state_machine import StateMachine, SPLAY_POSE

    cfg = json.loads(Path(job['config']).read_text())
    assert cfg['policy']['obs_dim'] in (33, 34, 35)
    mode = cfg['policy_interface'].get('leg_action_filter', 'none')   # 33-obs exports predate the key
    options = ort.SessionOptions()
    options.intra_op_num_threads = options.inter_op_num_threads = 1
    policy = ort.InferenceSession(cfg['policy']['path'], sess_options=options, providers=['CPUExecutionProvider'])
    plant = PLANTS[job['plant']]
    runtime = copy.deepcopy(cfg)
    for key in ('kp', 'kd'):  # optional deployed-gain override (8 native values) before the knee plant factor
        if key in job:
            runtime['robot'][f'joint_{key}'] = [float(v) for v in job[key]]
    for key in ('joint_kp', 'joint_kd'):
        runtime['robot'][key][2] *= plant['knee'][0]
        runtime['robot'][key][6] *= plant['knee'][1]
    env = TitaMujocoEnv(cfg)
    m = env.model
    floor = m.geom('floor').id
    base_body = m.body('base_link').id
    obstacles = np.flatnonzero((m.geom_bodyid == 0) & (np.arange(m.ngeom) != floor))
    m.geom_contype[obstacles] = m.geom_conaffinity[obstacles] = 0
    wheels = [g for g in range(m.ngeom) if m.geom_bodyid[g] in (m.body('left_leg_4').id, m.body('right_leg_4').id)
              and (m.geom_contype[g] or m.geom_conaffinity[g])]
    assert len(wheels) == 2 and all(m.geom_type[g] == mujoco.mjtGeom.mjGEOM_CYLINDER for g in wheels)
    if plant['wheel'] == 'sphere':
        for g in wheels:
            r = float(m.geom_size[g][0])
            m.geom_type[g] = mujoco.mjtGeom.mjGEOM_SPHERE
            m.geom_size[g] = [r, 0., 0.]
            m.geom_rbound[g] = r
            m.geom_aabb[g] = [0., 0., 0., r, r, r]
    adapter = ActionAdapter(runtime)
    builder = ObservationBuilder(cfg)
    builder.gyro_bias = float(job.get('heading_bias', 0.))  # residual of the robot's bias calibration [rad/s]
    filter_ = LegActionFilter(mode, adapter.order)
    legs = np.array([j not in (3, 7) for j in adapter.order])
    sm = StateMachine(cfg['robot']['torque_limit'], auto_rl=True)
    env.reset(SPLAY_POSE)
    rng = np.random.default_rng(42)
    env.data.qvel[0] = rng.uniform(-.015, .015)
    env.data.qvel[env.qvel_addr[LEGS]] = rng.normal(0, .01, 6)
    mujoco.mj_forward(m, env.data)
    sm.request('transform_up', env.joint_pos())
    sc = SCENARIOS[job['scenario']]
    command = np.zeros(3, dtype=np.float32)
    last = np.zeros(8, dtype=np.float32)
    previous_raw = None
    m.body_ipos[base_body, 0] += plant.get('com_dx', 0.)
    half = np.radians(plant.get('imu_pitch_deg', 0.)) / 2
    imu_offset = np.array([np.cos(half), 0., np.sin(half), 0.])               # body-frame rotation about y
    imu_rot = quat_wxyz_to_rotmat(imu_offset)
    terms = cfg['policy_interface']['observations']
    x_term = next((i for i, term in enumerate(terms) if term['kind'] == 'wheel_position_error'), None)
    x_index = None if x_term is None else sum(term['size'] for term in terms[:x_term])
    x_scale = None if x_term is None else float(terms[x_term]['scale'])
    keys = ('t', 'q', 'dq', 'rpy_deg', 'position', 'velocity_body', 'gyro', 'command', 'raw', 'applied', 'torque', 'x_err',
            'imu_rpy_deg', 'qpos')
    rows = {k: [] for k in keys}
    failure, tick, was_rl = None, 0, False
    try:
        for _ in range(round((sc['duration'] + 5.) / DT)):
            sm.update(DT)
            if sm.state != 'rl':
                last[:] = 0.; filter_.reset(); builder.reset(); previous_raw = None
                env.step_with_torque_callback(sm.torque)
                continue
            if not was_rl:
                builder.reset()
            was_rl = True
            t = round(tick * DT, 8)
            if t >= sc['duration']:
                break
            target = sc['schedule'][0]
            for entry in sc['schedule']:
                if t >= entry[0]:
                    target = entry
            step_max = sc['ramp'] * DT
            command += np.clip(np.array([target[1], 0., target[2]]) - command, -step_max, step_max)
            quat = env.base_quat_sensor()
            rot = quat_wxyz_to_rotmat(quat)
            q, dq, position = env.joint_pos(), env.joint_vel(), env.base_pos()
            qpos = env.data.qpos.copy()                                   # same instant as q/position (pre-step)
            tilt = np.arccos(np.clip(rot[2, 2], -1., 1.))
            contact = any(c.dist < 0 and ((m.geom_bodyid[c.geom1] == base_body and c.geom2 == floor) or
                                          (m.geom_bodyid[c.geom2] == base_body and c.geom1 == floor))
                          for c in env.data.contact)
            if tilt > .65 or contact:
                failure = dict(kind='fall', t_rl_s=t, tilt_deg=float(np.degrees(tilt)), base_floor_contact=contact)
                break
            gyro = env.base_ang_vel()
            imu_quat = quat_mul(quat, imu_offset)
            obs = builder.build(ObsState(q, dq, imu_quat, imu_rot.T @ gyro, command, last))
            raw = policy.run(['nn_output'], {'nn_input0': obs.reshape(1, -1)})[0].reshape(8)
            pe = raw.copy()
            if previous_raw is not None and job['g']:
                pe[legs] += job['g'] * (raw[legs] - previous_raw[legs])
            applied = filter_.update(pe)
            torques = []

            def callback(positions, velocities):
                tau = adapter.compute(applied, positions, velocities)
                torques.append(tau.copy())
                return tau
            env.step_with_torque_callback(callback)
            if not np.isfinite(env.data.qpos).all() or not np.isfinite(env.data.qvel).all():
                raise ValueError('Nonfinite physics state')
            values = (t, q, dq, np.degrees(quat_wxyz_to_rpy(quat)), position, rot.T @ env.base_lin_vel(), gyro,
                      command.copy(), raw.copy(), applied.copy(), np.mean(torques, axis=0),
                      float('nan') if x_index is None else float(obs[x_index] / x_scale),
                      np.degrees(quat_wxyz_to_rpy(imu_quat)), qpos)
            for k, v in zip(keys, values):
                rows[k].append(v)
            last = raw.copy()
            previous_raw = raw.copy()
            tick += 1
    except Exception as error:  # noqa: BLE001 - recorded as a failed rollout
        failure = dict(kind=type(error).__name__, detail=str(error), t_rl_s=tick * DT)
    finally:
        env.close()
    s = {k: np.asarray(v, dtype=np.float64 if k == 'qpos' else np.float32) for k, v in rows.items()}
    result = dict(job=job, leg_action_filter=mode, rl_steps=tick, failure=failure,
                  evidence_status='FAIL' if failure or tick != round(sc['duration'] / DT) else 'PASS')
    if result['evidence_status'] == 'PASS':
        result['metrics'] = metrics(s, job['scenario'])
        if job['save']:
            np.savez_compressed(Path(job['output']) / 'signals' / f"{job_id(job)}.npz", **s)
    return result


def alternation(x):
    """Amplitude of the period-2 (25 Hz) component over consecutive policy ticks, per column."""
    return np.abs(np.mean((-1.) ** np.arange(len(x))[:, None] * (x - x.mean(0)), axis=0))


def intervals(mask):
    idx = np.flatnonzero(mask)
    return [v for v in np.split(idx, np.flatnonzero(np.diff(idx) > 1) + 1) if len(v)]


def turn_metrics(s):
    t, cmd = s['t'].astype(float), s['command'].astype(float)
    yaw = np.unwrap(np.radians(s['rpy_deg'][:, 2].astype(float)))
    q, pitch = np.degrees(s['q'].astype(float)), s['rpy_deg'][:, 1].astype(float)
    before = (t >= 4.) & (t < 8.)
    out = dict(turns=[])
    for start, end in ((8., 13.), (18., 23.)):
        m = (t >= start) & (t < end) & (np.abs(cmd[:, 2]) >= .95)
        w = (t >= start) & (t < end + 1.)
        out['turns'].append(dict(
            cmd_wz=float(cmd[m, 2].mean()), wz=float(s['gyro'][m, 2].mean()),
            vx_mean=float(s['velocity_body'][m, 0].mean()), vx_abs_mean=float(np.abs(s['velocity_body'][m, 0]).mean()),
            base_travel_m=float(np.linalg.norm(s['position'][w][-1, :2] - s['position'][w][0, :2])),
            thigh_change_deg=float(q[m][:, [1, 5]].mean() - q[before][:, [1, 5]].mean()),
            pitch_change_deg=float(pitch[m].mean() - pitch[before].mean())))
    tail = (t >= 25.) & (t < 30.)
    out.update(
        vx_abs_mean=float(np.mean([x['vx_abs_mean'] for x in out['turns']])),
        travel_max_m=float(max(x['base_travel_m'] for x in out['turns'])),
        thigh_change_max_deg=float(max(abs(x['thigh_change_deg']) for x in out['turns'])),
        pitch_change_max_deg=float(max(abs(x['pitch_change_deg']) for x in out['turns'])),
        wz_ratio=float(np.mean([x['wz'] / x['cmd_wz'] for x in out['turns']])),
        stop_yaw_dps=float(np.degrees((yaw[tail][-1] - yaw[tail][0]) / (t[tail][-1] - t[tail][0]))))
    return out


def metrics(s, scenario):
    if scenario == 'turn':
        return turn_metrics(s)
    t, cmd = s['t'].astype(float), s['command'].astype(float)
    yaw = np.unwrap(np.radians(s['rpy_deg'][:, 2].astype(float)))
    speed = np.linalg.norm(s['velocity_body'][:, :2], axis=1)
    raw_legs = s['raw'][:, LEGS].astype(float)
    out = {}
    zero = np.max(np.abs(cmd), axis=1) < 1e-7
    if scenario in ('stand', 'probe', 'stand300'):
        m = t >= 8.
        tt = t[m] - t[m][0]
        out.update(yaw_rate_dps=float(np.degrees(np.polyfit(tt, yaw[m], 1)[0])),
                   x_disp_m=float(s['position'][m][-1, 0] - s['position'][m][0, 0]),
                   planar_disp_m=float(np.linalg.norm(s['position'][m][-1, :2] - s['position'][m][0, :2])),
                   speed_rms_m_s=float(np.sqrt(np.mean(speed[m] ** 2))),
                   pitch_deg=float(s['rpy_deg'][m, 1].mean()), pitch_std_deg=float(s['rpy_deg'][m, 1].std()),
                   knee_L_minus_R_deg=float(np.degrees((s['q'][m, 2] - s['q'][m, 6]).mean())),
                   leg_torque_rms_nm=float(np.sqrt(np.mean(s['torque'][m][:, LEGS] ** 2))),
                   raw_leg_25hz_amp_max=float(alternation(raw_legs[m]).max()),
                   leg_dq_25hz_amp_max=float(alternation(s['dq'][m][:, LEGS].astype(float)).max()),
                   raw_leg_d_lag1_min=float(min(np.corrcoef(d[1:], d[:-1])[0, 1] if d.std() > 1e-9 else 0.
                                                for d in np.diff(raw_legs[m], axis=0).T)))
        return out
    stops, tracking = [], []
    for block in intervals(zero):
        if t[block[0]] < 8.:
            continue
        settled = block[t[block] >= t[block[0]] + 1.]
        tail = block[t[block] >= t[block[-1]] - 3. + DT / 2]
        if len(settled) < 50:
            continue
        stops.append(dict(start_s=float(t[block[0]]),
                          yaw_rate_dps=float(np.degrees((yaw[settled[-1]] - yaw[settled[0]]) / (t[settled[-1]] - t[settled[0]]))),
                          drift_m=float(np.linalg.norm(s['position'][settled[-1], :2] - s['position'][settled[0], :2])),
                          tail_speed_rms_m_s=float(np.sqrt(np.mean(speed[tail] ** 2))),
                          tail_pitch_deg=float(s['rpy_deg'][tail, 1].mean())))
    schedule = DRIVE if scenario == 'drive' else DRIVE_FAST
    for i, (start, vx, wz) in enumerate(schedule):
        if vx == 0 and wz == 0:
            continue
        end = schedule[i + 1][0]
        w = (t >= end - 2.) & (t < end)
        tracking.append(dict(target_vx=vx, target_wz=wz, vx_mean=float(s['velocity_body'][w, 0].mean()),
                             wz_mean=float(s['gyro'][w, 2].mean()), pitch_deg=float(s['rpy_deg'][w, 1].mean()),
                             cmd_reached=[float(cmd[w, 0].mean()), float(cmd[w, 2].mean())]))
    yaw_stops = [abs(x['yaw_rate_dps']) for x in stops]
    out.update(stops=stops, tracking=tracking,
               stop_yaw_abs_mean_dps=float(np.mean(yaw_stops)), stop_yaw_abs_max_dps=float(np.max(yaw_stops)),
               stop_drift_mean_m=float(np.mean([x['drift_m'] for x in stops])),
               stop_tail_speed_rms_mean_m_s=float(np.mean([x['tail_speed_rms_m_s'] for x in stops])),
               vx_track_err_max=float(max(abs(x['vx_mean'] - x['cmd_reached'][0]) for x in tracking)),
               wz_track_err_max=float(max(abs(x['wz_mean'] - x['cmd_reached'][1]) for x in tracking)),
               pitch_abs_max_deg=float(np.abs(s['rpy_deg'][:, 1]).max()),
               leg_torque_rms_nm=float(np.sqrt(np.mean(s['torque'][:, LEGS] ** 2))),
               raw_leg_25hz_amp_max=float(alternation(raw_legs).max()))
    return out


def job_id(job):
    bias = f"_hb{job['heading_bias']:g}" if job.get('heading_bias') else ''
    return f"{job['tag']}_{job['step']}_{job['plant']}_{job['scenario']}_g{job['g']:g}{bias}"


def jobs_for(policies, output):
    jobs = []
    for p in policies:
        base = dict(tag=p['tag'], step=p['step'], config=p['config'], output=str(output))
        jobs += [dict(base, plant='A', scenario='stand', g=0., save=True),
                 dict(base, plant='A', scenario='drive', g=0., save=True),
                 dict(base, plant='B', scenario='stand', g=0., save=False),
                 dict(base, plant='B', scenario='drive', g=0., save=False),
                 dict(base, plant='A', scenario='probe', g=1., save=False),
                 dict(base, plant='A', scenario='probe', g=1.5, save=False)]
        if p['tag'] in FAST:
            jobs.append(dict(base, plant='A', scenario='drive_fast', g=0., save=True))
    return jobs


def robust_jobs(policies, output):
    jobs = []
    for p in policies:
        if (p['tag'], p['step']) not in ROBUST:
            continue
        base = dict(tag=p['tag'], step=p['step'], config=p['config'], output=str(output), save=False)
        for plant in ('A_mirror', 'A_sym068', 'A_sym055', 'A_nom'):
            jobs += [dict(base, plant=plant, scenario='stand', g=0.), dict(base, plant=plant, scenario='drive', g=0.)]
        jobs += [dict(base, plant='A', scenario='probe', g=2.), dict(base, plant='A', scenario='probe', g=3.)]
    return jobs


def g6_jobs(policies, output):
    return [dict(tag=p['tag'], step=p['step'], config=p['config'], output=str(output), plant=plant, scenario=scenario,
                 g=0., save=True) for p in policies if (p['tag'], p['step']) in G6
            for plant in ['A', *G6_PLANTS] for scenario in ('stand', 'drive', 'turn')]


def turn_jobs(policies, output):
    return [dict(tag=p['tag'], step=p['step'], config=p['config'], output=str(output), plant=plant, scenario='turn',
                 g=0., save=False) for p in policies for plant in ('A', 'A_nom', 'B_nom')]


def evaluate(output, workers, robust=False, turn=False, g6=False):
    policies = json.loads((output / 'policies.json').read_text())
    (output / 'signals').mkdir(exist_ok=True)
    done_path = output / 'results.json'
    results = json.loads(done_path.read_text()) if done_path.exists() else []
    done = {job_id(r['job']) for r in results}
    if TAGS:
        policies = [p for p in policies if p['tag'] in TAGS]
    make = g6_jobs if g6 else turn_jobs if turn else robust_jobs if robust else jobs_for
    todo = [j for j in make(policies, output) if job_id(j) not in done]
    began = time.monotonic()
    with ProcessPoolExecutor(max_workers=workers) as pool:
        futures = [pool.submit(rollout, j) for j in todo]
        for k, future in enumerate(as_completed(futures), 1):
            r = future.result()
            results.append(r)
            if k % 8 == 0 or k == len(todo):
                write_json(done_path, results)
            print(f"[VALIDATION_SIM] {k}/{len(todo)} {job_id(r['job'])} {r['evidence_status']} "
                  f"{time.monotonic() - began:.0f}s", flush=True)
    write_json(done_path, results)


def summarize(output):
    results = json.loads((output / 'results.json').read_text())
    by = {}
    for r in results:
        j = r['job']
        by.setdefault((j['tag'], j['step']), {})[(j['plant'], j['scenario'], j['g'])] = r
    rows = []
    for (tag, step), d in sorted(by.items()):
        def get(key, metric):
            r = d.get(key)
            return None if r is None or r['evidence_status'] != 'PASS' else r['metrics'][metric]
        fails = [f"{k[0]}-{k[1]}-g{k[2]:g}" for k, r in d.items() if r['evidence_status'] != 'PASS']
        row = dict(tag=tag, step=step, filter=next(iter(d.values()))['leg_action_filter'], failures=fails,
                   A_stand_yaw_dps=get(('A', 'stand', 0.), 'yaw_rate_dps'),
                   A_stand_x_m=get(('A', 'stand', 0.), 'x_disp_m'),
                   A_stand_pitch_deg=get(('A', 'stand', 0.), 'pitch_deg'),
                   A_stand_knee_LR_deg=get(('A', 'stand', 0.), 'knee_L_minus_R_deg'),
                   A_stop_yaw_mean_dps=get(('A', 'drive', 0.), 'stop_yaw_abs_mean_dps'),
                   A_stop_yaw_max_dps=get(('A', 'drive', 0.), 'stop_yaw_abs_max_dps'),
                   A_stop_drift_m=get(('A', 'drive', 0.), 'stop_drift_mean_m'),
                   A_stop_speed_rms=get(('A', 'drive', 0.), 'stop_tail_speed_rms_mean_m_s'),
                   A_vx_err_max=get(('A', 'drive', 0.), 'vx_track_err_max'),
                   A_wz_err_max=get(('A', 'drive', 0.), 'wz_track_err_max'),
                   B_stand_yaw_dps=get(('B', 'stand', 0.), 'yaw_rate_dps'),
                   B_stop_yaw_mean_dps=get(('B', 'drive', 0.), 'stop_yaw_abs_mean_dps'),
                   B_stop_drift_m=get(('B', 'drive', 0.), 'stop_drift_mean_m'),
                   alt25_g0=get(('A', 'stand', 0.), 'raw_leg_25hz_amp_max'),
                   alt25_g1=get(('A', 'probe', 1.), 'raw_leg_25hz_amp_max'),
                   alt25_g15=get(('A', 'probe', 1.5), 'raw_leg_25hz_amp_max'),
                   lag1_g15=get(('A', 'probe', 1.5), 'raw_leg_d_lag1_min'),
                   fast_vx_err_max=get(('A', 'drive_fast', 0.), 'vx_track_err_max'),
                   fast_wz_err_max=get(('A', 'drive_fast', 0.), 'wz_track_err_max'),
                   fast_stop_yaw_mean_dps=get(('A', 'drive_fast', 0.), 'stop_yaw_abs_mean_dps'))
        rows.append(row)
    write_json(output / 'summary.json', rows)
    cols = ['tag', 'step', 'filter', 'A_stand_yaw_dps', 'A_stop_yaw_mean_dps', 'A_stop_yaw_max_dps', 'A_stand_x_m',
            'A_stop_drift_m', 'A_stop_speed_rms', 'A_stand_pitch_deg', 'A_stand_knee_LR_deg', 'A_vx_err_max',
            'A_wz_err_max', 'B_stand_yaw_dps', 'B_stop_yaw_mean_dps', 'alt25_g0', 'alt25_g1', 'alt25_g15', 'lag1_g15',
            'fast_vx_err_max', 'fast_wz_err_max', 'fast_stop_yaw_mean_dps', 'failures']
    with open(output / 'summary.csv', 'w') as f:
        f.write(','.join(cols) + '\n')
        for r in rows:
            f.write(','.join('' if r[c] is None else (f'{r[c]:.4g}' if isinstance(r[c], float) else
                             ('|'.join(r[c]) if isinstance(r[c], list) else str(r[c]))) for c in cols) + '\n')
    print((output / 'summary.csv').read_text())


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--output', type=Path, required=True)
    mode = ap.add_mutually_exclusive_group(required=True)
    mode.add_argument('--prepare', action='store_true')
    mode.add_argument('--evaluate', action='store_true')
    mode.add_argument('--summarize', action='store_true')
    ap.add_argument('--workers', type=int, default=8)
    ap.add_argument('--robust', action='store_true', help='with --evaluate: extra plants/probes for ROBUST candidates')
    ap.add_argument('--tags', nargs='+', help='only these run tags (prepare merges into policies.json)')
    ap.add_argument('--turn', action='store_true', help='with --evaluate: in-place turn scenario (plants A, A_nom, B_nom)')
    ap.add_argument('--g6', action='store_true', help='with --evaluate: CoM / IMU pitch offset plants for G6 candidates')
    a = ap.parse_args()
    global TAGS
    TAGS = set(a.tags) if a.tags else None
    a.output.mkdir(parents=True, exist_ok=True)
    if a.prepare:
        prepare(a.output)
    elif a.evaluate:
        evaluate(a.output, a.workers, a.robust, a.turn, a.g6)
    else:
        summarize(a.output)


if __name__ == '__main__':
    main()
