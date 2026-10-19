# 별도 residual excitation / 토크 예산 연구안

작성일: 2026-10-16 (Asia/Seoul)

Execution Domain: **DESKTOP_DRY_RUN** (후속 실행 시 **VALIDATION_SIM**만)

Policy Checkpoint SHA256: `6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05`

Evidence Status: **NOT_TESTED — 후속 연구 계획**. 이번 A/B/C의 입력 제한과 판정을 변경하는 문서가 아니다.

Observed Metrics / Behavior / Log Summary:

기존 LQR 로그의 포화 구간을 제외하면 표본 수가 줄고 condition이 악화될 수 있었다. 이번 C는 기존 absolute band 안의 독립0.01Nm 입력으로 데이터만 수집했다. 그 학습 자료의 입력 innovation은 약36–37%였으므로, 기존 band 자체가 원리적으로 식별에 부족하다고 단정하지 않는다. 정보량과 새 입력 예측은 별개 판정이다.

## P0 — 기존 예산 안에서 excitation 배치 비교

- Nominal, gain0.8/1.2, friction0.2/0.8, lag0.02의 이미 안전한 조건만 개발 pilot 후보로 한다. mass/CoM/lag0.05에는 강행하지 않는다.
- 개발 seed740/741/742와 평가 seed750/751×pitch−0.035/0/+0.035를 별도 등록한다. 실제 착수 전 seed 충돌과 실행source를 다시 확인하고 신규 manifest를 동결한다.
- 무probe, 진폭0.0025/0.005/0.01/0.02/0.04Nm를 순차 pilot 후보로 둔다. 총 residual0.4328–0.5328Nm, 합 slew2Nm/s, wheel±12Nm는 동일하다. Probe가 더해져도 absolute band를 늘리지 않는다.
- PRBS와 multisine을 구분하고 주파수/블록 길이·60초 budget·seed를 사전에 고정한다. 안전 guard가 허용할 때만 적용한다. 동일 입력 변화량/에너지를 Fixed-feedback 아래의 probing과 일정bias 식별 stream에서 각각 기록해 운용 영역 차이를 분리한다.
- 기존 자세/높이/leg/finite guard, native clipping, 센서속도20mm/s와pitch0.2rad 범위를 지킨다. 범위 밖에서 probing을 중단한다. 실패 시 진폭을 더 키워 같은 episode를 복구하지 않는다.
- 평가: 전체 구간 base IAE/drift와 실제 torque/probe energy, 사용 표본 수, rank25, condition≤1e6, 입력 innovation≥1%, 독립0.1/0.5/1/2초 예측과Direct B≤30%를 함께 본다. 학습seed의 최소 필요 excitation을 정한 뒤 held-out에서 검증하며 결과를 보고 threshold를 바꾸지 않는다.

## P1 — 예산 확대는 별도 실험

P0가 안전하지만 정보 부족으로 끝나고 확대 필요성이 남을 때만 별도 계획을 작성한다. ±0.075/±0.10Nm와 같은 확대 폭은 후보일 뿐 이번 실행에서 허용하거나 채택한 값이 아니다. 새 absolute band, 원 예산 대조군, 안전 pilot 중단조건, probing cost와 위치 품질 기준을 새 manifest에 먼저 고정해야 한다. 기존 비교의FAIL을 새 예산으로 덮어쓰지 않는다.

C처럼 정보 gate가 통과했는데 자유 예측이 실패한다면 예산부터 늘리는 결론을 내리지 않는다. Offline/RLS 차이, prior/regularization·forgetting·조건수, 과도/후반 영역과 affine forcing을 먼저 분리한다. 새 K 활성화, Phase D/E/F, 하드웨어는 이번 문서와 A/B/C 실행의 범위 밖이다.
