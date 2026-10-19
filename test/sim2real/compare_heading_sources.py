"""DESKTOP_DRY_RUN: compare real-robot heading sources without external ground truth (read-only logs).

Sources (all from the copied bags; no robot command):
- quat: IMU quaternion yaw (vendor attitude filter), unwrapped;
- gyro: integral of body gyro z; gyro_c: the same after subtracting the stationary-idle gyro bias of that run
  (state idle, all |dq| < 0.02 rad/s, before RL);
- enc: wheel-encoder differential (s_R - s_L) / W with s_side = R (unwrap(q_wheel) + q_thigh + q_knee)
  (body pitch cancels) and W the geometric wheel-centre lateral distance from MuJoCo forward kinematics of the
  logged leg joints at every sample. W is NOT fitted to the gyro, so enc is independent of the IMU.

Windows: RL zero-command holds (after 1 s), RL yaw-command windows (|wz cmd| > 0.1), and the pre-RL idle window.
Vendor captures (500 Hz joint_states/IMU) give static stands and the high-speed turn run.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sqlite3
import sys

import mujoco
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import analyze_pd_vibration as pd  # noqa: E402

REPO = Path(__file__).resolve().parents[2]
SCENE = REPO / 'tita_gluon_ws/src/ddt_ros2_control/urdfs/tita_description/mujoco_corrected/scene.xml'
NATIVE = ['joint_left_leg_1', 'joint_left_leg_2', 'joint_left_leg_3', 'joint_left_leg_4',
          'joint_right_leg_1', 'joint_right_leg_2', 'joint_right_leg_3', 'joint_right_leg_4']
R = 0.0925
POL = REPO / 'sim2real/tita_ws/src/tita_controller/policies'
RUNS = {
    'posma2_50k': ('docs/exp/2026-10-18/flashsac_posma2_50000_202450_review', 'flashsac_posma2_50000'),
    'posma2_75k': ('docs/exp/2026-10-18/flashsac_posma2_75000_210936_review', 'flashsac_posma2_75000'),
    'sphere2_60k': ('docs/exp/2026-10-19/sphere_hardware_review/raw', 'flashsac_sphere2_60000'),
    'sphere1_70k': ('docs/exp/2026-10-19/sphere_hardware_review/raw', 'flashsac_sphere1_70000'),
    'sphere1_90k': ('docs/exp/2026-10-19/sphere_hardware_review/raw', 'flashsac_sphere1_90000'),
    'sphere3_70k': ('docs/exp/2026-10-19/sphere_hardware_review/raw', 'flashsac_sphere3_70000'),
}
VENDOR = REPO / 'docs/exp/2026-10-18/vendor_lqr_reproduction/capture_1927'


class TrackWidth:
    def __init__(self):
        self.m = mujoco.MjModel.from_xml_path(str(SCENE))
        self.d = mujoco.MjData(self.m)
        self.adr = [self.m.jnt_qposadr[self.m.joint(n).id] for n in NATIVE]
        self.left, self.right = self.m.body('left_leg_4').id, self.m.body('right_leg_4').id

    def __call__(self, q):
        out = np.empty(len(q))
        for i, row in enumerate(q):
            self.d.qpos[:] = 0.0
            self.d.qpos[3] = 1.0
            for a, v in zip(self.adr, row):
                self.d.qpos[a] = v
            mujoco.mj_kinematics(self.m, self.d)
            out[i] = self.d.xpos[self.left][1] - self.d.xpos[self.right][1]
        return out


def yaw_of(quat):
    w, x, y, z = quat.T
    return np.unwrap(np.arctan2(2 * (w * z + x * y), 1 - 2 * (y * y + z * z)))


def sources(t, q, quat, gz, bias, width):
    q = q.copy()
    q[:, [3, 7]] = np.unwrap(q[:, [3, 7]], axis=0)
    dt = np.r_[0., np.diff(t)]
    sL = R * (q[:, 3] + q[:, 1] + q[:, 2])
    sR = R * (q[:, 7] + q[:, 5] + q[:, 6])
    W = width(q)
    # integrate the differential rate with the instantaneous width (W changes slowly with hip posture)
    enc = np.cumsum(np.r_[0., np.diff(sR - sL)] / W)
    return dict(quat=yaw_of(quat), gyro=np.cumsum(gz * dt), gyro_c=np.cumsum((gz - bias) * dt), enc=enc), W


def runs(mask):
    e = np.flatnonzero(np.diff(np.r_[0, mask.astype(int), 0]))
    return list(zip(e[::2], e[1::2]))


def window_row(kind, t, src, a, b, extra=None):
    T = float(t[b - 1] - t[a])
    d = {k: float(np.degrees(v[b - 1] - v[a])) for k, v in src.items()}
    row = dict(kind=kind, seconds=T, delta_deg=d, rate_dps={k: v / T for k, v in d.items()})
    # high-frequency noise of each source: std of 0.2 s increments after removing the window trend
    noise = {}
    for k, v in src.items():
        seg = np.degrees(v[a:b])
        if b - a > 20:
            inc = seg[10:] - seg[:-10]
            noise[k] = float(np.std(inc - np.mean(inc)))
    row['noise_0p2s_deg'] = noise
    if extra:
        row.update(extra)
    return row


def rl_run(name, folder, bundle, width):
    import rclpy.serialization  # noqa: F401  (message bindings come from the sourced workspace)
    from rclpy.serialization import deserialize_message
    from tita_controller.msg import TrainingSample
    bag = next((REPO / folder).glob(f'{bundle}_*_bag')) if (REPO / folder / 'raw').exists() is False else None
    bag = bag or next((REPO / folder).glob('*_bag'))
    cfg = json.loads((POL / bundle / 'config.json').read_text())
    d = pd.load(bag, cfg['policy_interface']['actions'])
    with sqlite3.connect(f"file:{d['db']}?mode=ro", uri=True) as c:
        tid = dict(c.execute('SELECT name,id FROM topics'))['/sim2real/training_sample']
        quat = np.array([deserialize_message(b, TrainingSample).quaternion_wxyz for b, in c.execute(
            'SELECT data FROM messages WHERE topic_id=? ORDER BY timestamp', (tid,))])
    t = (d['mono'] - d['mono'][0]) * 1e-9
    state = d['state']
    rl = state == 'rl'
    first_rl = int(np.flatnonzero(rl)[0])
    still = (state == 'idle') & np.all(np.abs(d['dq']) < 0.02, axis=1)
    still[first_rl:] = False
    bias = float(np.median(d['gyro'][still, 2])) if still.sum() > 20 else 0.0
    src, W = sources(t, d['q'], quat, d['gyro'][:, 2], bias, width)
    cmd = d['command']
    zero = np.all(np.abs(cmd) <= [.02, .02, .03], axis=1)
    rows = []
    idle_runs = [(a, b) for a, b in runs(still) if b - a > 50]
    for a, b in idle_runs:
        rows.append(window_row('idle_static', t, src, a, b))
    for a, b in runs(rl & zero):
        a2 = a + int(np.searchsorted(t[a:b] - t[a], 1.0))
        if b - a2 > 250:
            rows.append(window_row('rl_hold', t, src, a2, b, dict(W_mean_m=float(W[a2:b].mean()))))
    for a, b in runs(rl & (np.abs(cmd[:, 2]) > .1)):
        if b - a > 50:
            rows.append(window_row('rl_yaw_cmd', t, src, a, b, dict(cmd_wz_mean=float(cmd[a:b, 2].mean()))))
    return dict(run=name, bag=str(bag.relative_to(REPO)), gyro_idle_bias_dps=float(np.degrees(bias)),
                idle_samples=int(still.sum()), W_rl_mean_m=float(W[rl].mean()), windows=rows)


def vendor_run(path, width):
    z = np.load(path)
    j, imu = z['joints'], z['imu']
    q = j[:, 1:9].copy()
    q[:, [1, 5]] = np.where(q[:, [1, 5]] < -2.5, q[:, [1, 5]] + 2 * np.pi, q[:, [1, 5]])
    tj, ti = j[:, 0], imu[:, 0]
    # encoder heading on the joint time base, IMU sources on their own time base; compare over the common span
    t0, t1 = max(tj[0], ti[0]), min(tj[-1], ti[-1])
    jm, im = (tj >= t0) & (tj <= t1), (ti >= t0) & (ti <= t1)
    qj = q[jm][::10]                      # 50 Hz is enough for the slowly varying width
    tjj = tj[jm][::10]
    enc_src, W = sources(tjj, qj, np.tile([1., 0, 0, 0], (len(qj), 1)), np.zeros(len(qj)), 0., width)
    gz = imu[im, 7]
    dt = np.r_[0., np.diff(ti[im])]
    still = np.all(np.abs(j[jm][:, 9:17]) < 0.02, axis=1)
    T = float(t1 - t0)
    d = dict(quat=float(np.degrees(yaw_of(imu[im, 1:5])[-1] - yaw_of(imu[im, 1:5])[0])),
             gyro=float(np.degrees(np.sum(gz * dt))), enc=float(np.degrees(enc_src['enc'][-1])))
    return dict(capture=path.name, seconds=T, delta_deg=d, rate_dps={k: v / T for k, v in d.items()},
                gyro_mean_dps=float(np.degrees(gz.mean())), joints_still_fraction=float(still.mean()),
                W_mean_m=float(W.mean()))


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--out', type=Path, required=True)
    a = ap.parse_args()
    width = TrackWidth()
    result = dict(execution_domain='DESKTOP_DRY_RUN', rl=[], vendor=[])
    for name, (folder, bundle) in RUNS.items():
        result['rl'].append(rl_run(name, folder, bundle, width))
    for path in sorted(VENDOR.glob('ros_vendor_*.npz')):
        result['vendor'].append(vendor_run(path, width))
    a.out.parent.mkdir(parents=True, exist_ok=True)
    a.out.write_text(json.dumps(result, indent=1))
    f = lambda r: ' '.join(f"{k} {v:+7.2f}" for k, v in r.items())
    for r in result['rl']:
        print(f"== {r['run']}  idle gyro bias {r['gyro_idle_bias_dps']:+.3f} dps ({r['idle_samples']} samples)  W_rl {r['W_rl_mean_m']:.3f} m")
        for w in r['windows']:
            print(f"  {w['kind']:11s} {w['seconds']:5.1f}s  delta[deg]: {f(w['delta_deg'])} | noise0.2s[deg]: "
                  + ' '.join(f"{k} {v:.3f}" for k, v in w['noise_0p2s_deg'].items()))
    print('== vendor captures (delta deg over capture)')
    for v in result['vendor']:
        print(f"  {v['capture'][11:40]:30s} {v['seconds']:5.1f}s {f(v['delta_deg'])} | gyro mean {v['gyro_mean_dps']:+.3f} dps still {v['joints_still_fraction']:.2f} W {v['W_mean_m']:.3f}")


if __name__ == '__main__':
    main()
