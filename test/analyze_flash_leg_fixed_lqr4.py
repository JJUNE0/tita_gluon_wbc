"""VALIDATION_SIM: audit and report the measured A/C-4/E comparison."""

import argparse
from collections import Counter
import json
from pathlib import Path
import sys

import numpy as np

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / 'test'))
from eval_flash_leg_fixed_lqr4 import Plant, Description, policy_config, read_yaml, write_json, LEGS, WHEELS, action_history_slice


def mean_std(rows, metric):
    values = [r[metric] for r in rows if not r['failure']]
    if not values:
        return 'N/A'
    return f'{np.mean(values):.3f} ± {np.std(values, ddof=1):.3f}'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--results', type=Path, required=True)
    parser.add_argument('--report', type=Path, required=True)
    args = parser.parse_args()
    output = args.results.resolve()
    rows = [json.loads(line) for line in (output / 'results.jsonl').read_text().splitlines()]
    manifest = json.loads((output / 'manifest.json').read_text())
    assert len(rows) == 243
    assert len({(r['mode'], r['mismatch'], r['seed'], r['pitch_delta_rad']) for r in rows}) == 243
    policy = policy_config()
    src = read_yaml(next(p for p in policy['policy_interface']['sources'] if p.endswith('env.yaml')))
    description = Description(src['scene']['robot']['spawn']['asset_path'])
    history, scale, clip = action_history_slice(policy)
    e_rows = [r for r in rows if r['mode'] == 'E']
    manifest.update(execution_status='PASS', completed_episodes=len(rows),
                    evidence_status='FAIL' if any(r['failure'] for r in e_rows) else 'PASS',
                    e_failed_episodes=sum(bool(r['failure']) for r in e_rows))
    write_json(output / 'manifest.json', manifest)
    initial_errors = []
    for r in e_rows:
        mismatch = next(m for m in manifest['cfg']['mismatches'] if m['name'] == r['mismatch'])
        plant = Plant(policy, manifest['cfg'], description, manifest['nominal_parameters'], mismatch, r['seed'], r['pitch_delta_rad'])
        try:
            initial_errors.append(float(np.max(abs(np.r_[plant.env.data.qpos, plant.env.data.qvel] - r['initial_physics']))))
        finally:
            plant.env.close()
        assert r['audit']['leg_torque_max_error_nm'] == 0.
        assert r['audit']['last_action_observation_max_error'] == 0.
        assert r['audit']['wheel_override_max_error_nm'] < 1e-6
        assert r['audit']['online_rls_calls'] == 0
        with np.load(output / r['trace']) as trace:
            np.testing.assert_array_equal(trace['K'], np.broadcast_to(r['K'], trace['K'].shape))
            # Row t stores the action/observation used over the immediately preceding interval.
            np.testing.assert_array_equal(trace['history_input'][2:], trace['policy_action'][1:-1])
            np.testing.assert_array_equal(trace['policy_observation'][1:, history],
                                          np.clip(trace['history_input'][1:], *clip) * scale)
            np.testing.assert_array_equal(trace['command_substeps'][:, :, LEGS],
                                          trace['discarded_flash_torque_substeps'][:, :, LEGS])
    assert max(initial_errors) == 0.
    controls = [r for r in rows if r['mode'] != 'E']
    assert len(controls) == 162
    assert all(max(r['archive_errors'].values()) == 0. for r in controls)
    integrity = dict(execution_domain='VALIDATION_SIM', evidence_status='PASS',
        checkpoint_sha256=manifest['checkpoint_sha256'], episodes=243,
        exact_a_c4_archive_replays=162, e_initial_states_verified=81, initial_max_error=0.,
        leg_adapter_max_error_nm=max(r['audit']['leg_torque_max_error_nm'] for r in e_rows),
        history_max_error=max(r['audit']['last_action_observation_max_error'] for r in e_rows),
        wheel_override_max_error_nm=max(r['audit']['wheel_override_max_error_nm'] for r in e_rows),
        online_rls_calls=0)
    write_json(output / 'integrity.json', integrity)
    tables = ['| 조건 | 군 | 완료/전체 | 실패율 | 최대 planar drift m | pitch error RMS rad |',
              '|---|---|---:|---:|---:|---:|']
    for mismatch in [m['name'] for m in manifest['cfg']['mismatches']]:
        for mode in ('A', 'C-4', 'E'):
            group = [r for r in rows if r['mode'] == mode and r['mismatch'] == mismatch]
            complete = sum(not r['failure'] for r in group)
            tables.append(f'| {mismatch} | {mode} | {complete}/{len(group)} | {1-complete/len(group):.1%} | '
                          f'{mean_std(group,"max_displacement_m")} | {mean_std(group,"pitch_rms_rad")} |')
    nominal_e = [r for r in e_rows if r['mismatch'] == 'nominal']
    representative = next(r for r in nominal_e if r['seed'] == 42 and r['pitch_delta_rad'] == 0.)
    failure_counts = dict(Counter(r['failure'] for r in e_rows))
    times = [r['completed_s'] for r in nominal_e]
    history_delta = [r['zero_wheel_history_leg_delta_rms'] for r in nominal_e]
    com = [r['com_change_max_m'] for r in nominal_e]
    lines = ['# E — FlashSAC Leg + Fixed 4-State LQR Wheel', '',
        'Execution Domain: VALIDATION_SIM (파일·경로 검사: DESKTOP_DRY_RUN)', '',
        f'Policy Checkpoint SHA256: `{manifest["checkpoint_sha256"]}`', '',
        f'ONNX SHA256: `{manifest["onnx_sha256"]}`', '',
        'Evidence Status: FAIL — E의 제어 성능. 구현·경로·baseline 재현 및 결과 무결성 검사는 PASS.', '',
        'Observed Metrics / Behavior / Log Summary:', '',
        '**기존 FlashSAC leg 경로를 보존하고 wheel 토크만 C-4로 교체한 E는 안정적인 zero-command 제어를 달성하지 못했다.** '
        f'전체 E {len(e_rows)}회 중 {sum(bool(r["failure"]) for r in e_rows)}회 실패했다. '
        f'Nominal E 종료 시각은 {min(times):.2f}–{max(times):.2f}초였다. '
        '완료 전 drift가 작아 보이더라도 12초 완료한 A/C-4보다 좋은 결과로 해석하지 않는다.', '',
        '## 적용 경로와 last_action', '',
        '- 지정 model_100000 FlashSAC deterministic actor, 33-value observation, action scale/clip/joint order를 그대로 사용했다.',
        '- Policy는 매 control step 전체 8개 action을 출력한다. 기존 ActionAdapter.compute를 매 physics step 실행한 후 '
        '**native wheel torque 2개만** C-4의 u/2로 덮어쓴다. Leg 6개는 A의 position reference·Kp=60/Kd=1.5·effort clipping 경로를 보존한다.',
        '- 기존 wheel velocity target→Kd=0.5 PD 출력은 계산되지만 실제 적용하지 않는다. '
        'LQR torque 뒤에 wheel velocity PD를 다시 더하거나 torque를 velocity reference로 바꾸지 않는다.',
        '- `last_action`에는 A와 동일하게 **직전 전체 raw actor output**을 넣는다. 미적용 wheel 출력도 포함하며 '
        'wheel 채널을 0으로 만들거나 torque 단위를 policy action에 넣지 않는다.',
        '- 따라서 E의 last_action wheel 채널은 실제 실행된 wheel command와 다르다. '
        '이는 정책의 내부 action history 의미는 보존하지만 실제 action/state 대응을 바꾸는 조합이다.',
        '- Wheel 변화로 이후 joint velocity/gravity/actor output도 달라진다. '
        '“Leg 경로 보존”은 동일 observation/action에 대한 변환·PD가 같다는 뜻이며, E와 A rollout의 leg action 수치가 항상 같다는 뜻은 아니다.',
        f'- Audit: leg torque 차이 {integrity["leg_adapter_max_error_nm"]}, last_action observation 차이 {integrity["history_max_error"]}, '
        f'wheel 교체 최대 오차 {integrity["wheel_override_max_error_nm"]:.3g} Nm(float32 반올림). RLS transition/update 호출은 0.',
        '- 별도 inference로 같은 observation에서 이전 wheel action history만 0으로 바꿔 leg 출력 변화를 측정했다. '
        '이 counterfactual 출력은 실제 제어에 적용하지 않았다.',
        f'- Nominal에서 이 leg action 변화 RMS의 trial 평균은 {np.mean(history_delta):.4f}(native policy action 단위)이다. '
        f'대표 trial RMS {representative["zero_wheel_history_leg_delta_rms"]:.4f}, 최대 {representative["zero_wheel_history_leg_delta_max"]:.4f}. '
        '현재 leg action scale 0.25를 적용하면 대표 최대 target 변화는 약 '
        f'{.25*representative["zero_wheel_history_leg_delta_max"]:.4f} rad이다. '
        '미적용 wheel history가 leg inference에 영향을 주는 것은 확인됐지만, 이것만이 실패 원인이라는 증거는 아니다.', '',
        '## 동일 초기 조건의 A/C-4/E 비교', '',
        '- 9 조건 × 3 seeds × 3 pitch × 3군 = 243회. Nominal + 기존 8 mismatch를 재사용했다.',
        '- Seed=42/43/44, pitch perturbation −0.035/0/+0.035 rad, 같은 seed별 초기 velocity·접지 높이·roll·stand pose. '
        'A/C-4 162회는 기존 archive의 state·wheel torque·world axle position·leg error와 정확히 일치했다.',
        '- Zero command, episode 최대 12초, control dt=0.02/physics dt=0.005 s, 3초의 12 N/0.1 s 외란 모두 동일하다. '
        '3초 전에 실패한 E trial은 이 외란이 적용되기 전에 종료됐다.',
        '- C-4와 E의 K₀, Q4=[1,2,200,5], R=0.1, sensor estimator·IMU cache timing·nominal equilibrium·24 Nm 합 토크·120 Nm/s slew를 유지했다.',
        '- C-4의 fixed leg PD는 기존 360/12이고 E는 A의 FlashSAC leg PD 60/1.5이다. '
        '이 차이는 요청한 ablation의 일부이며, E에서 다리를 고정하거나 gain을 재튜닝하지 않았다.', '',
        '\n'.join(tables), '',
        '평균 ± sample 표준편차는 12초를 완료한 trial만 포함한다. E의 N/A는 미측정이 아니라 완료 trial이 없어서 '
        '동일 horizon 통계를 계산하지 않았다는 뜻이다. 종료 전 metric은 results.jsonl/metrics.csv에 별도 남겼다.', '',
        '## 실패와 해석', '',
        f'정확한 실패 사유 분포: `{failure_counts}`. '
        '대표 seed42/pitch0 E는 0.62초에 pitch error limit를 넘었다. '
        'Raw action/observation/history, discarded wheel PD torque, 실제 command/motor substeps, joint position/velocity/limit margin, '
        'K, CoM과 종료 snapshot은 각 NPZ에 있다.',
        f'- Nominal E의 body-frame CoM 변화 최대값 평균은 {np.mean(com):.5f} m이다. '
        f'대표 E는 {representative["com_change_max_m"]:.5f} m이며 기존 대표 C-4는 약 0.000365 m였다. '
        'E는 FlashSAC가 leg pose를 바꾸므로 고정 leg pose를 가정한 nominal WIP 모델의 조건이 유지되지 않는다.',
        '- 기존 FlashSAC는 wheel velocity PD와 leg action을 함께 학습했다. Wheel을 별도 LQR로 바꾸면 '
        'wheel 응답·leg/wheel coordination·history/state 관계가 변한다. Leg 경로가 보존됐다는 사실만으로 혼합 loop의 안정성을 보장할 수 없다.',
        '- 이 결과만으로 FlashSAC leg 자체나 Fixed LQR 자체가 나쁘다고 판단하지 않는다. '
        'E 조합은 실패했지만 같은 초기 조건의 A와 C-4는 완료했다.',
        '- Ground-truth control, gyro 동기화, pitch 기준 수정, last_action 변경, gain tuning은 이번 E에서 수행하지 않았다: NOT_TESTED. '
        '이 요인들의 기여를 분리한 실패 원인 확정은 아직 남아 있다.', '',
        '## 검증·변경 범위·재현', '',
        '- 기존 코드·설정·보고서는 변경하지 않았다. 신규 `test/eval_flash_leg_fixed_lqr4.py`, '
        '`test/test_flash_leg_fixed_lqr4.py`, `test/analyze_flash_leg_fixed_lqr4.py`와 이 실험 증거만 추가했다.',
        '- Actor/observation/last_action 동등성과 wheel-only 교체 테스트 2개 PASS (`unit_tests.log`). '
        '243개 episode의 gain 고정·history·leg torque·초기 상태 및 162개 archive 재현 audit PASS (`full/integrity.json`).',
        '- `./scripts/agent-check.sh` PASS (Python syntax 333개, URDF XML 8개). 기존 파일 hash 보존 및 최종 diff 검사 기록도 실험 폴더에 있다.',
        '- 브랜치: `agent/codex/dev_tita_gluon`. Hardware 실행·정책 재학습·online adaptation은 수행하지 않았다.', '',
        '```bash',
        '/home/cocel/venvs/cosim_ros2_jazzy/bin/python test/test_flash_leg_fixed_lqr4.py',
        'MPLCONFIGDIR=/tmp/lqr_mpl /home/cocel/venvs/cosim_ros2_jazzy/bin/python test/eval_flash_leg_fixed_lqr4.py --output docs/exp/2026-10-15/new_e/full',
        'MPLCONFIGDIR=/tmp/lqr_mpl /home/cocel/venvs/cosim_ros2_jazzy/bin/python test/analyze_flash_leg_fixed_lqr4.py --results docs/exp/2026-10-15/new_e/full --report docs/exp/2026-10-15/new_e_summary.md',
        '```', '',
        '산출물: `full/results.jsonl`, `metrics.csv`, `aggregates.json`, `comparison.png` '
        '(nominal seed42, pitch perturbation −0.035 rad), 각 episode NPZ와 `integrity.json`.', '']
    args.report.write_text('\n'.join(lines))
    print('[VALIDATION_SIM] report generated:', args.report)
    print(json.dumps(integrity))


if __name__ == '__main__':
    main()
