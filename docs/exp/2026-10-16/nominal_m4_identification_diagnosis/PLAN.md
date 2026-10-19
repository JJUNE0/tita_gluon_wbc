# Nominal M4 식별 실패의 원인 분리 계획

작성일: 2026-10-16 (Asia/Seoul)

Execution Domain: **VALIDATION_SIM** (계획·회귀·분석: **DESKTOP_DRY_RUN**)

Policy Checkpoint SHA256: `6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05`

Evidence Status: **NOT_TESTED — 사전 계획**. 실행 결과는 별도 보고서에 기록한다.

Observed Metrics / Behavior / Log Summary:

이전 Nominal PASS와 Phase C FAIL은 시작 영역·데이터 구성·식별 목적함수가 다르다. RLS를 수정하기 전에 아래 순서를 고정한다. 상세 조건·threshold·source와 이전 자료 hash는 [동결 plan](run_01/plan.json)에 있다. 기존 보고서와 모든 기존 실행 코드는 수정하지 않는다.

1. 이전 train234개 paired 응답으로 A/B를 재계산하고 저장 행렬과 비교한다. Train18 baseline으로 c만 계산하고 이전 joint LS도 재현한다. Test306개 및 별도 fresh204개에서 원래 지표를 재계산한다. 이전 fresh snapshot3개는 실제 MuJoCo에서8초 baseline와8초 PRBS를 exact replay한다. 이전 테스트를 이미 읽은 재현이므로 새 독립 검증 표본으로 합산하지 않는다.
2. 새 Nominal 초기조건을 학습 seed800/801×pitch−0.035/0/+0.035, 검증 seed810/811×같은 pitch로 분리한다. Target 물성은 첫 startup 전부터 nominal로 유지한다. 첫 RL부터 bias0.4828 Nm를 합 slew2 Nm/s로 적용하고 p_hold는 한 번만 정한다. Cold10/30/60초 및 같은 배포의1000초에서 분기한다. 1000초는 기존 past180초 정착 gate가 통과한 경우에만 정착 자료로 수집한다. 통과하지 않으면 NOT_TESTED로 남긴다.
3. 각 snapshot의8초 baseline과 train17/test17종 응답을 저장한다. Train17은 기존13종(train sine/PRBS·±pulse/step×0.02/0.05와micro0.01) 및0.02 sine/PRBS의추가2회씩이다. Test17은 validation sine/PRBS·±pulse/step/bipulse×0.02/0.05와micro0.01이다. 합 residual0.4328–0.5328, slew2, wheel±12 Nm를 유지한다. 안전 범위 밖에서는 probing을 강행하지 않는다. Baseline과 모든 분기는 실제 전체 상태·센서 적분기·raw history·motor 상태를 공유한다.
4. 동일 raw pair 데이터에서 paired A/B+별도 baseline c와 absolute A/B/c 공동 LS를 비교한다. 주 회귀의 rcond1e−10은 기존 성공 코드와 같다. Full 자료에서 두 방법의rcond1e−8과 Phase C의fixed nominal centering도 사전 보조 비교한다. 결과를 보고 cutoff를 선택해 주 판정을 바꾸지 않는다. Continuous constant-bias prefix의 공동 LS는 B excitation이 없어 진단용으로만 별도 기록한다.
5. 시간별로 small2응답, quantity6(같은2파형반복), waveforms6, initials6(3초기조건×2파형), full78, full_replicates102를 비교한다. 앞의 세6응답 군은 진폭0.02 Nm와transition수를 같게 해 데이터 양·파형·초기조건을 분리한다. Full 군은 추가 규모 비교이며 여러 요인이 함께 늘어난다. Full paired/joint 모델은 모든 평가 시각에 교차 적용한다.
6. 모든 새 모델을 새 test 수집 전에 동결한다. p/v는 기존 raw sensor odometry이며 FK 보정을 주입하지 않는다. 모든24상태를 재귀 예측한다. First2초와rolling0.1/0.5/1/2초 p/v NRMSE≤30%, Direct Bv 부호/오차≤30%, 모든 baseline2초≤0.02mm/0.02mm/s·8초≤0.05mm/0.02mm/s를 요구한다. 전체응답 중앙값 gate와 초기조건별6/6을 함께 보고한다. 순수 paired8초와absolute8초는 구분한다.

동결 전 독립 수치 검사4개를 통과했다. 새 gain 생성·제어기·RLS 수정·Q/R/상태 확장·목표 재설정·마찰/질량 등 추가 mismatch·실기는 수행하지 않는다. 같은 시작조건의 분기는 독립 초기조건으로 세지 않는다. 기존 prior는 Nominal MuJoCo 보정을 포함하며 Isaac-only 식별을 주장하지 않는다.
