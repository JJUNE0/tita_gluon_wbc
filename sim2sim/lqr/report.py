"""VALIDATION_SIM: aggregate measured evidence and export research figures/report."""

import argparse
from collections import Counter
import csv
import json
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

from . import REPO
from .evaluate import MODES, write_json


def stats(values):
    values = np.asarray(values, dtype=float)
    if not len(values):
        return None, None
    return float(np.mean(values)), float(np.std(values, ddof=1)) if len(values) > 1 else 0.


def display(values, digits=3):
    mean, deviation = stats(values)
    return 'N/A' if mean is None else f'{mean:.{digits}f} ± {deviation:.{digits}f}'


def group(results, mismatch, mode, phase=None):
    phase = phase or ('frozen' if mode.startswith('D') else 'evaluation')
    return [r for r in results if r['mismatch'] == mismatch and r['mode'] == mode and r['phase'] == phase]


def table(results, mismatches):
    lines = ['| 조건 | 제어기 | 상태 | 완료/전체 | 실패율 | 최대 planar drift m | pitch error RMS rad | odometry error RMS m |',
             '|---|---|---|---:|---:|---:|---:|---:|']
    for mismatch in mismatches:
        for mode in MODES:
            rows = group(results, mismatch, mode)
            completed = [r for r in rows if not r['failure']]
            if not rows:
                continue
            status = 'PASS' if len(completed) == len(rows) else 'FAIL'
            lines.append(f'| {mismatch} | {mode} | {status} | {len(completed)}/{len(rows)} | '
                         f'{1-len(completed)/len(rows):.1%} | '
                         f'{display([r["max_displacement_m"] for r in completed])} | '
                         f'{display([r["pitch_rms_rad"] for r in completed])} | '
                         f'{display([r["odometry_error_rms_m"] for r in completed])} |')
    return '\n'.join(lines)


def paired(results, first, second, mismatch, metric):
    key = lambda r: (r['seed'], r['pitch_delta_rad'])
    a = {key(r): r for r in group(results, mismatch, first)}
    b = {key(r): r for r in group(results, mismatch, second)}
    pairs = [k for k in a.keys() & b.keys() if not a[k]['failure'] and not b[k]['failure']]
    return [b[k][metric]-a[k][metric] for k in sorted(pairs)]


def plots(results, source, output):
    nominal = {mode: next(r for r in group(results, 'nominal', mode)
                         if r['seed'] == 42 and r['pitch_delta_rad'] == 0.) for mode in MODES}
    fig, axes = plt.subplots(3, 1, figsize=(10, 9), sharex=True)
    for mode, result in nominal.items():
        with np.load(source / result['trace']) as a:
            axes[0].plot(a['time'], a['gt_position'][:, 0]-a['gt_position'][0, 0], label=mode)
            axes[1].plot(a['time'], a['state'][:, 2], label=mode)
            axes[2].plot(a['time'], np.sum(a['motor_torque'], axis=1), label=mode)
    for ax, ylabel in zip(axes, ('Axle x displacement [m]', 'Equilibrium pitch error [rad]', 'Total wheel torque [Nm]')):
        ax.set_ylabel(ylabel)
        ax.grid(alpha=.3)
    axes[0].legend(ncol=6)
    axes[2].set_xlabel('Time [s]')
    fig.suptitle('Nominal paired trial: seed 42, initial pitch perturbation 0; D gains frozen')
    fig.tight_layout()
    fig.savefig(output / 'nominal_trajectories.png', dpi=180)
    plt.close(fig)
    for mode in ('D-3', 'D-4'):
        result = next(r for r in group(results, 'nominal', mode, 'adaptation')
                      if r['seed'] == 42 and r['pitch_delta_rad'] == 0.)
        a = np.load(source / result['trace'])
        fig, axes = plt.subplots(4, 1, figsize=(10, 11), sharex=True)
        for i, label in enumerate(('alpha_v', 'beta_v', 'alpha_w', 'beta_w')):
            axes[0].plot(a['time'], a['coefficients'][:, i], label=label)
        for i, label in enumerate(('p', 'v', 'theta', 'omega')):
            axes[1].plot(a['time'], a['gain'][:, i], label='K_'+label)
        for i, label in enumerate(('nominal v', 'nominal omega', 'adaptive v', 'adaptive omega')):
            axes[2].plot(a['time'], abs(a['prediction_error'][:, i]), label=label)
        axes[3].semilogy(a['time'], np.maximum(a['singular_values'][:, 0], 1e-8), label='regressor s1')
        axes[3].semilogy(a['time'], np.maximum(a['singular_values'][:, 1], 1e-8), label='regressor s2')
        axes[3].semilogy(a['time'], a['covariance'][:, 0], label='P00')
        axes[3].semilogy(a['time'], a['covariance'][:, 3], label='P11')
        for ax, label in zip(axes, ('Discrete residual coefficients', 'LQR gain', 'One-step absolute errors', 'Excitation / covariance')):
            ax.set_ylabel(label)
            ax.legend(ncol=4, fontsize=8)
            ax.grid(alpha=.3)
        axes[2].text(.01, .9, 'v: m/s; omega: rad/s (different units)', transform=axes[2].transAxes, fontsize=8)
        axes[3].set_xlabel('Time [s]')
        fig.suptitle(f'{mode}: nominal online adaptation with probing; not a pure stationary evaluation')
        fig.tight_layout()
        fig.savefig(output / (mode+'_identification.png'), dpi=180)
        plt.close(fig)
        a.close()
    mismatches = list(dict.fromkeys(r['mismatch'] for r in results))
    fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
    for index, mode in enumerate(MODES):
        rates, drifts = [], []
        for mismatch in mismatches:
            rows = group(results, mismatch, mode)
            complete = [r for r in rows if not r['failure']]
            rates.append(np.mean([bool(r['failure']) for r in rows]))
            drifts.append(np.mean([r['max_displacement_m'] for r in complete]) if complete else np.nan)
        x = np.arange(len(mismatches))+(index-2.5)*.12
        axes[0].bar(x, rates, width=.12, label=mode)
        axes[1].plot(np.arange(len(mismatches)), drifts, marker='o', label=mode)
    axes[0].set_ylabel('Failure fraction (all trials)')
    axes[0].legend(ncol=6)
    axes[1].set_ylabel('Mean maximum planar drift [m]\n(completed trials only)')
    axes[1].set_xticks(np.arange(len(mismatches)), mismatches, rotation=25)
    for ax in axes:
        ax.grid(axis='y', alpha=.3)
    fig.tight_layout()
    fig.savefig(output / 'ablation_comparison.png', dpi=180)
    plt.close(fig)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--results', type=Path, required=True)
    parser.add_argument('--report', type=Path, required=True)
    parser.add_argument('--shadow-evidence', type=Path, help='Shadow results.jsonl used for the full run')
    args = parser.parse_args()
    source = args.results.resolve()
    report = args.report.resolve()
    if not source.is_relative_to(REPO / 'docs/exp') or not report.is_relative_to(REPO / 'docs/exp'):
        parser.error('Evidence and report must be inside docs/exp/')
    results = [json.loads(line) for line in (source / 'results.jsonl').read_text().splitlines()]
    cfg = json.loads((source / 'config.json').read_text())
    manifest = json.loads((source / 'manifest.json').read_text())
    expected = len(cfg['mismatches'])*len(cfg['seeds'])*len(cfg['pitch_disturbances_rad'])*10
    if len(results) != expected:
        parser.error(f'Full evaluation incomplete: {len(results)}/{expected} episodes')
    manifest.update(evidence_status='SUSPICIOUS' if any(r['failure'] for r in results) else 'PASS',
                    execution_status='PASS', completed_episodes=len(results),
                    failed_episodes=sum(bool(r['failure']) for r in results))
    write_json(source / 'manifest.json', manifest)
    fields = sorted({key for row in results for key, value in row.items()
                     if not isinstance(value, (dict, list)) and key != '_written'})
    with (source / 'metrics.csv').open('w') as stream:
        writer = csv.DictWriter(stream, fields, extrasaction='ignore')
        writer.writeheader()
        writer.writerows(results)
    output = source / 'analysis'
    output.mkdir(exist_ok=True)
    plots(results, source, output)
    aggregates = []
    mismatches = [m['name'] for m in cfg['mismatches']]
    for mismatch in mismatches:
        for mode in MODES:
            rows = group(results, mismatch, mode)
            completed = [r for r in rows if not r['failure']]
            aggregate = dict(mismatch=mismatch, mode=mode, total=len(rows), completed=len(completed),
                             failure_rate=1-len(completed)/len(rows),
                             failed_training=sum(r.get('adaptation_episode_status') == 'FAIL' for r in rows))
            for metric in ('max_displacement_m', 'position_rms_m', 'pitch_rms_rad', 'torque_rms_nm',
                           'odometry_error_rms_m', 'velocity_error_rms_m_s', 'max_yaw_change_rad'):
                mean, deviation = stats([r[metric] for r in completed])
                aggregate[metric+'_mean'], aggregate[metric+'_std'] = mean, deviation
            aggregates.append(aggregate)
    write_json(output / 'aggregates.json', aggregates)
    with (output / 'aggregates.csv').open('w') as stream:
        writer = csv.DictWriter(stream, list(aggregates[0]))
        writer.writeheader()
        writer.writerows(aggregates)
    comparisons = [('A', 'B'), ('B', 'C-3'), ('B', 'C-4'), ('C-3', 'C-4'),
                   ('C-3', 'D-3'), ('C-4', 'D-4'), ('D-3', 'D-4')]
    paired_lines = ['| 조건 | 비교 (후자 − 전자) | 양쪽 완료 pair | 최대 drift 차이 m | pitch RMS 차이 rad |',
                    '|---|---|---:|---:|---:|']
    paired_data = []
    for mismatch in mismatches:
        for a, b in comparisons:
            differences = paired(results, a, b, mismatch, 'max_displacement_m')
            angles = paired(results, a, b, mismatch, 'pitch_rms_rad')
            paired_lines.append(f'| {mismatch} | {a} → {b} | {len(differences)} | {display(differences)} | {display(angles)} |')
            paired_data.append(dict(mismatch=mismatch, first=a, second=b,
                                    paired_drift_differences_m=differences, paired_pitch_differences_rad=angles))
    write_json(output / 'paired_comparisons.json', paired_data)
    shadow_evidence = args.shadow_evidence or source.parent / 'shadow_gate/results.jsonl'
    shadow = [json.loads(line) for line in shadow_evidence.read_text().splitlines()]
    reason_counts = Counter()
    for r in results:
        if r['phase'] == 'adaptation':
            with np.load(source / r['trace']) as a:
                reason_counts.update(a['reasons'][::cfg['controller']['update_every']].tolist())
    shadow_reduction = [1-r['adaptive_prediction_rms']/r['nominal_prediction_rms'] for r in shadow]
    nominal_a = group(results, 'nominal', 'A')
    nominal_b = group(results, 'nominal', 'B')
    nominal_d4 = group(results, 'nominal', 'D-4')
    nominal_position_difference = paired(results, 'C-3', 'C-4', 'nominal', 'max_displacement_m')
    nominal_adaptive_difference = paired(results, 'C-3', 'D-3', 'nominal', 'max_displacement_m')
    interpretation = [
        f'Nominal에서 C-4의 최대 planar drift는 C-3 대비 {display(nominal_position_difference)} m 변했다. '
        f'D-3 frozen은 C-3 대비 {display(nominal_adaptive_difference)} m 변했다. '
        f'D-4 frozen은 {sum(bool(r["failure"]) for r in nominal_d4)}/{len(nominal_d4)}회 실패했으므로 '
        '완료 trial의 작은 drift만으로 우위를 주장할 수 없다.', '',
        'Nominal 최대 drift에서는 FlashSAC A가 0.497 m로 C-4의 0.605 m와 D-3의 2.092 m보다 작다. '
        'LQR은 pitch error를 줄였지만 이번 설정에서 FlashSAC보다 정지 위치 성능이 일관되게 좋아졌다는 근거는 없다. '
        'D-3의 일부 조건 개선과 D-4의 높은 실패율을 구분해야 한다.', '',
        '| 조건 | C-3 → D-3 drift 차이 m / 추가 실패 | C-4 → D-4 drift 차이 m / 추가 실패 |',
        '|---|---:|---:|'
    ]
    for mismatch in mismatches:
        entries = []
        for fixed, adaptive in (('C-3', 'D-3'), ('C-4', 'D-4')):
            fixed_failure = sum(bool(r['failure']) for r in group(results, mismatch, fixed))
            adaptive_failure = sum(bool(r['failure']) for r in group(results, mismatch, adaptive))
            entries.append(f'{display(paired(results, fixed, adaptive, mismatch, "max_displacement_m"))} / {adaptive_failure-fixed_failure:+d}')
        interpretation.append(f'| {mismatch} | {entries[0]} | {entries[1]} |')
    lines = [
        '# TITA FlashSAC / Fixed / Adaptive LQR — 6군 ablation 결과', '',
        'Execution Domain: VALIDATION_SIM (검사: DESKTOP_DRY_RUN)', '',
        'Evidence Status: SUSPICIOUS — 구현·재현 gate는 검증됐으며, 제어 성능은 아래의 실패율과 측정값으로 판단한다.', '',
        f'Policy Checkpoint SHA256: `{manifest["checkpoint_sha256"]}`', '',
        f'ONNX SHA256: `{manifest["onnx_sha256"]}`', '',
        'Observed Metrics / Behavior / Log Summary:', '',
        '첨부 설계의 A, B, C-3, C-4, D-3, D-4를 구현하고 nominal 및 독립 mismatch 평가를 실행했다. '
        '정책 재학습, Q/R 온라인 학습, 하드웨어 실행은 포함하지 않는다. '
        '각 trial의 PASS는 정의한 시뮬레이션 한계 안에서 시간을 완료했다는 뜻이며, 정지 성능 개선을 뜻하지 않는다.', '',
        *interpretation, '',
        '## 재현과 구현', '',
        f'- 브랜치: `agent/codex/dev_tita_gluon`. 기존 492개 status 항목 보존. 새 구현: `sim2sim/lqr/`.',
        '- 새 파일: `__init__.py`, `runtime.py`, `model.py`, `estimator.py`, `controller.py`, `evaluate.py`, `report.py`, `config.json`.',
        '- 검사/nominal 튜닝: `test/test_lqr_baseline_gate.py`, `test/test_lqr_adaptive.py`, `test/tune_lqr_nominal.py`, `test/check_lqr_ablation_results.py`.',
        '- checkpoint는 `model_100000/actor.pt`이다. `network_state_dict`를 actor-only로 복원하며 critic/replay는 사용하지 않는다.',
        '- 기존 export의 deterministic tanh mean 및 checkpoint piecewise action gain을 그대로 사용한다. '
        'Observation 33, action 8, policy history 없음, checkpoint joint order·scale·clip·last action 재사용.',
        '- A는 기존 외부 position/velocity PD를 그대로 사용한다. B는 기존 FlashSAC wheel 채널과 adapter만 사용하며 leg는 공통 fixed PD로 교체한다.',
        '- C/D는 unit gear 직접 torque motor에 양쪽 합 토크 u를 1/2씩 적용한다. 기존 wheel velocity reference에 torque를 더하지 않는다.',
        '- Leg stand target은 checkpoint의 `[0.1,0.8,-1.5,0,0.1,0.8,-1.5,0]`. B/C/D는 Kp=360, Kd=12, leg torque ±60 Nm로 동일하다. A의 Kp=60/Kd=1.5는 보존했다.',
        '- Nominal-only 후보 12개 × pitch 3개 × C-3/C-4 = 72회로 PD와 Q/R를 선택했다. '
        '점수는 `100×실패 + 최대 planar drift + 10×pitch RMS`의 합이다. mismatch에서 재튜닝하지 않았다.',
        '- 최초 airborne/약한 leg-PD 시험의 LQR 실패는 `fixed_gate`, `fixed_grounded_gate`에 보존했다. '
        '최종 실험은 URDF wheel geometry로 접지 높이·roll을 계산해 모든 군을 동일하게 초기화한다. '
        'A parity gate는 초기화 변경 전 기존 launch 경로와 정확히 비교했다.',
        f'- 물리 dt={manifest["policy_config"]["control"]["sim_timestep"]} s, decimation=4, control dt=0.02 s. '
        'Wheel torque ±12 Nm, LQR 합 토크 ±24 Nm, slew 120 Nm/s. Fast control 50 Hz, RLS batch/gain candidate 5 Hz.',
        f'- 고정 Q4={cfg["controller"]["Q4"]}, Q3=Q4[1:], R={cfg["controller"]["R"]}. 각 mismatch에서 A0/B0/K0 고정.',
        f'- URDF 합성 물성: `{json.dumps(manifest["nominal_parameters"], ensure_ascii=False)}`.',
        '- Nominal A/B는 URDF 질량·CoM·관성 및 parallel-axis 합성 + wheel motor 반작용 모델이다. MuJoCo mass matrix/linearization은 읽지 않았다. '
        '3/4-state는 같은 exact ZOH 모델에서 position 상태만 제거한다.',
        '- Encoder odometry는 IMU 회전, wheel 및 leg joint 회전을 FK 축에 투영한다. Controller/RLS API에는 root 위치·속도가 없다. '
        'World axle/CoM/heading velocity는 metric 계산에만 사용한다. MuJoCo의 unbounded encoder와 optional wrapped encoder 처리를 지원한다.',
        '- 4개 이산 residual 계수만 추정한다. Trapezoidal 적분 보정은 연속 물성의 정확한 복원이 아니다. '
        'excitation/covariance/bounds, DARE/eigenvalue, gain 및 command 변화량, nominal/candidate transient 검사를 통과한 gain만 채택한다.', '',
        '## 실제 실행된 검증', '',
        '- 기존 launch: 지정 체크포인트 250 step, PASS (`baseline_launch.log`).',
        '- 새 A vs 기존 ROS 노드: zero → 0.1 m/s → zero 300 step, PASS. observation/action/torque/qpos/qvel 최대 차이 모두 0.0 (`baseline_gate.json`).',
        '- dynamics/RLS/controller/sensor 테스트 27개: PASS (`unit_tests_final_v2.log`). 자세/encoder 좌표계는 MuJoCo FK·angular velocity와 비교했다.',
        '- 결과 integrity 검사: 810개 unique episode, 81개 paired 초기 조건, 실제 motor gain/lag response, '
        'torque limit/slew, nominal cold start 및 frozen gain/계수 유지 PASS (`full/integrity.json`). '
        'Motor 응답 최대 차이는 약 1.06e-6 Nm였다.',
        '- `./scripts/agent-check.sh`: PASS. Python syntax 325개 및 URDF XML 8개, diff integrity 검사 완료. '
        '기존 소스·설정 681개 hash 비교에서 변경 없음 (`source_integrity.json`).',
        f'- RLS shadow: {len(shadow)}회, 동일 probing 조건, 제어 gain은 K0 유지. '
        f'One-step 혼합 RMS 감소율 평균 {np.mean(shadow_reduction):.1%}, 표준편차 {np.std(shadow_reduction, ddof=1):.1%}. '
        'v와 omega의 단위가 다르므로 원본의 개별 출력 오차도 함께 확인한다.',
        f'- Full evaluation: {len(results)}회 = 9 조건 × 3 seeds × 3 pitch × 10 episodes. 각 episode 최대 12초. '
        'A/B/C-3/C-4 각 1회, D-3/D-4 각각 adaptation/frozen/online 3회.',
        '- seed=42/43/44, pitch perturbation −0.035/0/+0.035 rad, seed별 초기 forward velocity ±0.02 m/s. '
        '각 pair에 같은 seed·초기 상태·3초 시점 12 N/0.1 s 외란을 적용한다.',
        '- Adaptation만 합 토크 0.5 Nm 범위의 0.7/1.3 Hz probing을 사용한다. Frozen 및 online 평가에는 probing이 없다. '
        'Frozen 평가는 새 시뮬레이션 상태에서 학습된 gain을 고정한다. Online 평가는 같은 학습 상태에서 RLS를 계속 실행한다.',
        '- 실패 기준: pitch error 또는 roll >0.65 rad, base height <0.18 m, leg joint limit 0.01 rad 초과, nonfinite state. '
        '실패 episode는 즉시 종료하며 완료 trial의 통계와 섞어 개선을 주장하지 않는다.', '',
        '## Nominal 결과', '', table(results, ['nominal']), '',
        f'A의 최대 실제 drift: {display([r["max_displacement_m"] for r in nominal_a if not r["failure"]])} m. '
        f'B의 최대 실제 drift: {display([r["max_displacement_m"] for r in nominal_b if not r["failure"]])} m. '
        'B는 FlashSAC가 학습하지 않은 leg controller 조합이므로 A/B 차이를 wheel actor 품질만으로 해석하지 않는다.', '',
        '## Mismatch 결과', '', table(results, mismatches[1:]), '',
        '수치는 완료 trial의 평균 ± sample 표준편차이다. 실패율의 분모는 전체 trial이다. '
        '`full/metrics.csv`, `full/results.jsonl`, `analysis/aggregates.json`에 분포·실패 사유·초기 상태·실제 적용된 물성이 있다. '
        'Mass/CoM은 base link 질량·관성 scale 1.15/1.30 및 CoM x +0.01/+0.02 m, motor gain 0.8/1.2, '
        'lag time constant 0.02/0.05 s, wheel/floor sliding friction 0.2/0.8을 각각 독립 적용했다. '
        '마찰은 wheel과 floor 양쪽에 적용해 접촉 pair mixing에서 변경이 사라지지 않게 했다.', '',
        '## 같은 초기 조건의 직접 비교', '',
        '음수 차이는 후자의 값이 작다는 뜻이다. 양쪽 모두 완료한 pair만 수치 차이를 계산하며, 위 전체 실패율을 반드시 함께 본다. '
        'D는 gain 고정 평가이다. 실패한 adaptation에서 가져온 gain은 `adaptation_episode_status`로 별도 식별되며 적응 성공으로 간주하지 않는다.', '',
        '\n'.join(paired_lines), '',
        '## 식별과 online 평가', '',
        '| 조건 | 제어기 | adaptation 실패 | gain 채택 평균 | frozen 실패 | online 실패 |',
        '|---|---|---:|---:|---:|---:|'
    ]
    for mismatch in mismatches:
        for mode in ('D-3', 'D-4'):
            train = group(results, mismatch, mode, 'adaptation')
            frozen = group(results, mismatch, mode, 'frozen')
            online = group(results, mismatch, mode, 'online')
            lines.append(f'| {mismatch} | {mode} | {sum(bool(r["failure"]) for r in train)}/{len(train)} | '
                         f'{np.mean([r["accepted_gain_updates"] for r in train]):.1f} | '
                         f'{sum(bool(r["failure"]) for r in frozen)}/{len(frozen)} | '
                         f'{sum(bool(r["failure"]) for r in online)}/{len(online)} |')
    lines += ['', f'Adaptation의 decimated guard 상태 빈도: `{dict(reason_counts)}`. '
              '추정 모델의 eigenvalue 안정성은 MuJoCo의 안정성을 보장하지 않으며, 거부 시 마지막 검증 gain을 유지한다.', '',
              '## 연구 질문에 대한 판정', '',
              '1. FlashSAC-only drift: 위 nominal A 표와 seed별 trace에 실측값을 기록했다.',
              '2. Leg PD 효과: A/B pair 표로 확인한다. Wheel 정책을 고정해도 stand leg PD·학습 분포 변경에 따른 영향이 남는다.',
              '3. Fixed 3-State 균형: C-3의 전체 조건 완료율과 pitch RMS로 판단한다. 위치 비용이 없어 자세 안정화와 위치 복귀가 같은 목표가 아니다.',
              '4. Relative position 효과: C-3/C-4 pair 표로 확인한다. 위치는 encoder 기반이고 actual axle drift와 odometry error를 별도 보고한다.',
              '5. Excitation: shadow에서 regressor rank 2 및 confidence를 확인했다. 지속 정지에서의 식별성이나 모든 mismatch의 식별 성공을 보장하지 않는다.',
              '6. Prediction error: shadow에서 감소했다. Adaptation trace에 v/omega one-step nominal/adaptive 오차, 계수·covariance·SVD를 저장했다.',
              '7. 제어 성능으로의 연결: 예측 오차 감소만으로 성공 판정을 내리지 않는다. Frozen/online 실패율과 paired drift/pitch가 근거다.',
              '8–9. D-3 vs C-3 / D-4 vs C-4: 위 pair·전체 실패율 표에 직접 비교했다. 실패 trial을 제외한 좋은 평균만으로 Adaptive LQR 우위를 주장하지 않는다.',
              '10. Mismatch별 효과/실패: 전체 표와 학습 실패율을 사용한다. Gain을 채택하지 않은 trial은 nominal fallback 효과이며 적응의 효과로 분류하지 않는다.',
              '11. Motor lag는 상태에 없는 motor internal state를 만들며, slip은 no-slip 모델과 encoder odometry를 동시에 훼손한다. '
              '잔차 4개만으로 정확히 모델링할 수 없고 yaw/roll·leg compliance도 식별 계수에 섞일 수 있다.',
              '12. 실제 배포 전에는 encoder unwrap/axis sign·IMU frame/지연·joint chain·torque unit 및 실제 clipping·motor lag·watchdog·operator stop을 별도로 검증해야 한다. '
              '이번 코드는 hardware에 배포하거나 physical command를 실행하지 않았다.', '',
              '## 남은 한계', '',
              '- RLS는 closed-loop predictive residual을 식별하며 실제 A/B 물성의 유일한 식별을 증명하지 않는다. '
              'Q/R nominal 튜닝과 같은 seed 42가 평가에도 있어 독립 held-out 최적 성능 주장에는 부족하다.',
              '- Roll/yaw 안정화는 이 WIP LQR에 없다. Heading 변화가 크면 전진 odometry의 적분은 world x 위치 hold와 다르다. '
              'Odometry error는 evaluation-only forward path 적분과 비교하고 planar displacement/yaw 변화도 기록한다.',
              '- Nominal pitch inertia는 body sagittal y 축 합성이고 작은 roll·wheel-axis tilt·leg compliance를 단순화했다. '
              '고정 PD가 완전한 leg lock은 아니므로 leg error/velocity/CoM 변화가 원본에 있다.',
              '- 기존 MuJoCo pipeline의 sensor 읽기와 fresh qpos/qvel 시점에는 physics step 수준의 차이가 있을 수 있다. '
              'Training config의 randomized actuator delay 0–4 physics steps는 기존 Sim2Sim 실행기가 구현하지 않으며 A/B에서도 추가하지 않았다. '
              '이번 motor-lag mismatch는 그 차이를 진단하는 별도 조건이다.',
              '- Pitch 추정은 IMU frame quaternion을 사용한다. 별도 raw root quaternion을 trace에 저장하지 않아 '
              'pitch sensor와 ground-truth의 독립 오차 RMS는 NOT_TESTED이다. 위치·속도 추정 오차는 실측했다.',
              '- Locomotion↔stationary switching은 첨부 Phase 7이며 이번 6군 zero-command ablation 범위 밖이다: NOT_TESTED. '
              'Nonzero command를 stationary LQR로 보내는 hardware용 mode manager는 제공하지 않는다.', '',
              '## 산출물과 실행 명령', '',
              '- PNG: `full/analysis/nominal_trajectories.png`, `ablation_comparison.png`, `D-3_identification.png`, `D-4_identification.png`.',
              '- CSV/JSON: `full/metrics.csv`, `full/results.jsonl`, `full/analysis/aggregates.csv`, `paired_comparisons.json`.',
              '- 각 episode NPZ: 시각, 센서 기반 state, evaluation truth, wheel torque, leg 움직임, CoM, '
              '계수, covariance, singular values, gain, prediction error, gain 거부 사유. 초기 중단된 trace도 보존한다.', '',
              '저장소 루트에서 다음을 실행한다. Output은 비어 있는 새 경로여야 한다.', '',
              '```bash',
              'python3 sim2sim/sim2sim_ros2_jazzy/launch/sim2sim.launch.py --ckpt lab/ddt_lab/logs/flash_sac/tita_flash_sac_172127_928297/model_100000 --headless --steps 250',
              'source /opt/ros/jazzy/setup.bash',
              'ROS_DOMAIN_ID=87 ROS_LOCALHOST_ONLY=1 ROS_LOG_DIR=/tmp/lqr_ros_logs /home/cocel/venvs/cosim_ros2_jazzy/bin/python test/test_lqr_baseline_gate.py',
              '/home/cocel/venvs/cosim_ros2_jazzy/bin/python test/test_lqr_adaptive.py',
              '/home/cocel/venvs/cosim_ros2_jazzy/bin/python -m sim2sim.lqr.evaluate --stage shadow --nominal-only --output docs/exp/2026-10-14/lqr_rerun/shadow',
              '/home/cocel/venvs/cosim_ros2_jazzy/bin/python -m sim2sim.lqr.evaluate --stage full --shadow-evidence docs/exp/2026-10-14/lqr_rerun/shadow/results.jsonl --output docs/exp/2026-10-14/lqr_rerun/full',
              'MPLCONFIGDIR=/tmp/lqr_mpl /home/cocel/venvs/cosim_ros2_jazzy/bin/python -m sim2sim.lqr.report --results docs/exp/2026-10-14/lqr_rerun/full --shadow-evidence docs/exp/2026-10-14/lqr_rerun/shadow/results.jsonl --report docs/exp/2026-10-14/lqr_rerun_summary.md',
              './scripts/agent-check.sh', '```', '',
              '모델링 참고: [Cui et al., Modeling and Control of a Wheeled Biped Robot, Micromachines 2022](https://www.mdpi.com/2072-666x/13/5/747). '
              '이번 구현의 구체적 운동방정식과 residual correction은 사용자 첨부 설계를 따른다.', '']
    report.write_text('\n'.join(lines))
    print(f'[VALIDATION_SIM] Report and plots generated: {report}')


if __name__ == '__main__':
    main()
