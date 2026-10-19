# 동일 단일 rollout의 Plain LS / Online RLS 비교 계획

작성일: 2026-10-16 (Asia/Seoul)

Execution Domain: **DESKTOP_DRY_RUN**

Policy Checkpoint SHA256: `6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05`

Evidence Status: **NOT_TESTED — 신규 비교 결과 계산 전 계획**

Observed Metrics / Behavior / Log Summary:

이전 Online Local M4의 36개 단일 연속 rollout을 읽기 전용으로 재사용한다. Nominal/friction0.2, probing0.01/0.02 Nm, 개발 3조건·평가 6조건, 10/30/60초의 기존 후보를 모두 비교한다. 새 물리 수집·snapshot 분기·Direct B·K 적용·입력 예산 변경은 없다. 기존 결과를 알고 시작하는 사후 진단이며 새로운 미사용 검증 자료라고 주장하지 않는다.

## 동일 데이터 정의

각 기존 RLS 후보에 저장된 `training_times`의 **transition 종료 시각**을 원본 trajectory index로 변환한다. 원래 eligibility, 누적/최근10초/최근20초 창, 순서, software 실제 residual, p_hold, nominal 회귀 중심·단위, position translation 및 action B의 8개 causal zero rows를 동일하게 유지한다.

선택 index를 기존 mask와 시간 창에서 독립 재구성해 exact 일치시킨다. 10–14/30–34/60–64초 검증 transition은 이후 후보에서도 영구 제외한다. Batch fitter에는 freeze 시점까지의 prefix만 전달한다. 과거 검증 구간을 다시 학습하거나 별도 baseline·다른 rollout을 합치지 않는다.

## 방법과 판정

각 540개 학습 집합에 다음 네 모델을 대응시킨다.

1. **Plain LS:** 기존 constrained affine LS, group RMS scaling·rcond1e−8, prior/forgetting 없음. 기존 성공 Offline fitter를 그대로 사용한다.
2. **Same-cost Batch:** 해당 RLS의 nominal prior/P0/forgetting과 같은 비용을 augmented SVD로 푼다. 기존 저장된 수치 보정 후보와 상대 계수 차이≤1e−7을 확인한다.
3. **Raw Online RLS:** 원래 실행 중 매20ms 재귀 계산한 저장 모델. 새 자료로 다시 학습하지 않는다.
4. **Candidate RLS:** 원래 실행에서 저장한 같은 비용 SVD 보정 후보. Raw RLS와 혼동하지 않는다.

모든 신규 LS/Batch 모델을 먼저 파일과 hash로 동결한 후 score 단계에서 원래 후속4초의 같은 sensor/command로 평가한다. 2초와4초, rolling0.1/0.5/1/2초 absolute free prediction을 기존 validator로 계산한다. 새로운 threshold·상태 차원·Q/R·regressor cutoff 탐색은 없다. 기존 Candidate RLS의 validator 전체 수치를 원래 결과와 exact 대조한다.

원래 예측 기준: rolling/최초2초 p/v RMSE≤0.02mm/0.02mm/s, 최초4초≤0.05mm/0.02mm/s, NRMSE≤30%. 분모는 원래 후속 실제 변화량·floor 그대로다. 원래 정보 기준: 관측 rank25, scaled condition≤1e6, input innovation≥1%, N≥250. LS에는 인위적인 prior covariance를 만들지 않고 이 관측 정보 기준을 공통으로 쓴다. 기존 후보 P 양수 gate와 달라지는 경우는 수집 없이 중단해 구분한다.

**예측만 통과한 경우와 전체 정보·예측·조건부 B·안전 검증 통과를 별도로 집계한다.** 후속 조건부 B의 rank25·condition≤1e6·부호·상대 차이≤30%도 그대로 유지한다. 이 후속 회귀는 Direct B가 아니며 신뢰도 부족을 계수 오차로 바꾸지 않는다. 원래 후속 B condition 실패가 공통이므로 전체 FAIL만으로 LS/RLS의 예측 차이를 판단하지 않는다.

개발/평가·환경·진폭·시점·창별 PASS/FAIL과 같은 후보에서 LS-only/RLS-only/both-pass/both-fail을 보고한다. 여러 추정기·중첩 창·같은 episode의 시점은 관련 자료다. 540개 모델 비교나 2160개 점수를 독립 물리 실험으로 세지 않는다. 검증 결과로 새 모델을 선택·재적합하지 않는다.

## 해석과 범위

- 같은 transition에서 LS 예측 PASS / RLS FAIL이면 prior/forgetting·정규화·수치 효과를 우선 검토한다. Raw와 보정 후보, 동일 비용 Batch 결과를 함께 본다.
- LS/RLS 예측 모두 FAIL이면 해당 수집 자료·excitation·국소 창의 유효성을 우선 검토한다. 모든 조건에서 M4가 불가능하다는 결론은 아니다.
- 둘 다 예측 PASS여도 정보/B/안전 gate를 통과하지 못하면 새 K를 허용하지 않는다. 둘 다 전체 PASS이면 모델·gain 적용의 다음 사전 계획을 검토할 근거로만 보고한다. 이번 작업은 저장 데이터 비교이며 새로운 제어기를 실행하지 않는다.

독립 검사 4개: 정확한 시간창/index, 영구 검증 제외, 알려진 affine 계수와 position/action 구조, 선택하지 않은 미래 값 변경의 적합 불변성. source 2개·계획·원래 데이터와 의존 source hash를 결과 계산 전에 동결한다. 실행 뒤 agent-check·최종 diff·보호 hash를 기록한다. Hardware/production/commit/push 없음.
