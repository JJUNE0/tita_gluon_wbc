"""DESKTOP_DRY_RUN: 실기 관측으로 posma2_50000 ONNX를 재평가해 휠 차동(yaw) 명령의 원인을 분해한다.

좌우 거울 변환 M (관측/행동 모두):
- ang_vel [x,y,z] -> [-x,y,-z], gravity [gx,gy,gz] -> [gx,-gy,gz], command [vx,vy,wz] -> [vx,-vy,-wz]
- 관절(관측은 L1,R1,L2,R2,L3,R3,L4,R4 / 행동·last_action은 native L1..L4,R1..R4): 좌우 교환, hip(leg_1)만 부호 반전
- wheel_position_error 불변
대칭 정책이면 D(M o) = -D(o) (D = 우휠 - 좌휠 행동). o_sym = (o + M o)/2 에서 D(o_sym)은 정책 고유 비대칭,
그룹 g만 대칭화했을 때 D 변화량은 그 그룹 상태 비대칭의 기여다.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import onnxruntime as ort

ROOT = Path(__file__).resolve().parents[2]
BUNDLE = ROOT / 'sim2real/tita_ws/src/tita_controller/policies/flashsac_posma2_50000'
GROUPS = {'ang_vel': range(0, 3), 'gravity': range(3, 6), 'command': range(6, 9), 'joint_pos': range(9, 17),
          'joint_vel': range(17, 25), 'last_action': range(25, 33), 'x_err': range(33, 34)}


def interleaved_mirror(v):
    """obs 관절 순서 L1,R1,L2,R2,L3,R3,L4,R4."""
    out = v.copy()
    out[..., 0::2], out[..., 1::2] = v[..., 1::2], v[..., 0::2]
    out[..., [0, 1]] *= -1
    return out


def native_mirror(v):
    """native 순서 L1..L4,R1..R4."""
    out = np.concatenate([v[..., 4:], v[..., :4]], -1)
    out[..., [0, 4]] *= -1
    return out


def mirror_obs(o):
    m = o.copy()
    m[..., 0:3] = o[..., 0:3] * [-1, 1, -1]
    m[..., 3:6] = o[..., 3:6] * [1, -1, 1]
    m[..., 6:9] = o[..., 6:9] * [1, -1, -1]
    m[..., 9:17] = interleaved_mirror(o[..., 9:17])
    m[..., 17:25] = interleaved_mirror(o[..., 17:25])
    m[..., 25:33] = native_mirror(o[..., 25:33])
    return m


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument('npz', type=Path, help='analyze_posma2_yaw_drift.py 출력 옆의 obs npz')
    ap.add_argument('--out', type=Path, required=True)
    ap.add_argument('--bundle', type=Path, default=BUNDLE, help='policy.onnx/config.json 디렉터리 (동일 34-obs 인터페이스)')
    a = ap.parse_args()
    cfg = json.loads((a.bundle / 'config.json').read_text())['policy_interface']
    ref = json.loads((BUNDLE / 'config.json').read_text())['policy_interface']
    assert cfg['observations'] == ref['observations'] and cfg['actions'] == ref['actions'], 'interface mismatch'
    z = np.load(a.npz)
    obs, act_log, sel = z['obs'].astype(np.float32), z['action'], z['sel']
    sess = ort.InferenceSession(str(a.bundle / 'policy.onnx'), providers=['CPUExecutionProvider'])
    name = sess.get_inputs()[0].name
    # export 배치 차원이 1로 고정돼 있어 샘플 단위로 평가한다.
    run = lambda o: np.concatenate([sess.run(None, {name: r[None].astype(np.float32)})[0] for r in o])
    D = lambda act: (act[:, 7] - act[:, 3]) * 20.  # 우-좌 휠 목표 속도 [rad/s]
    out = {}
    for tag, m in [('zero_cmd_settled', sel)]:
        o = obs[m]
        base = run(o)
        replay_err = float(np.abs(base - act_log[m]).max())
        sym = .5 * (o + mirror_obs(o))
        res = dict(bundle=str(a.bundle), checkpoint_sha256=cfg['checkpoint_sha256'], samples=int(m.sum()),
                   onnx_replay_max_abs_err=replay_err,
                   D_logged_mean=float(D(act_log[m]).mean()), D_replay_mean=float(D(base).mean()),
                   D_mirror_mean=float(D(run(mirror_obs(o))).mean()),
                   D_all_symmetrized_mean=float(D(run(sym)).mean()))
        contrib = {}
        for g, idx in GROUPS.items():
            o2 = o.copy()
            o2[:, list(idx)] = sym[:, list(idx)]
            contrib[g] = float(D(base).mean() - D(run(o2)).mean())
        res['D_drop_when_group_symmetrized'] = contrib
        # 마지막 행동(자기유지 루프) 제외: last_action만 실기값 유지, 나머지 대칭화
        o3 = sym.copy()
        o3[:, 25:33] = o[:, 25:33]
        res['D_only_last_action_asym_mean'] = float(D(run(o3)).mean())
        # 입력 감도: gyro z, x_err에 대한 D 기울기
        for g, i, h in [('gyro_z_obs', 2, .01), ('x_err_obs', 33, .05)]:
            o4 = o.copy(); o4[:, i] += h
            res[f'dD_d{g}'] = float((D(run(o4)) - D(base)).mean() / h)
        out[tag] = res
    a.out.write_text(json.dumps(out, indent=1, ensure_ascii=False))
    r = out['zero_cmd_settled']
    print(f"{a.bundle.parent.parent.name}: D logged-state {r['D_replay_mean']:+.2f} | symmetrized {r['D_all_symmetrized_mean']:+.2f} | "
          f"joint_pos part {r['D_drop_when_group_symmetrized']['joint_pos']:+.2f} | dD/dgz_obs {r['dD_dgyro_z_obs']:+.1f} | "
          f"replay err {r['onnx_replay_max_abs_err']:.1e}")


if __name__ == '__main__':
    main()
