# model_60000 — Offline 목적함수와 단일 rollout Online Local M4 식별

작성일: 2026-10-16 (Asia/Seoul)

Execution Domain: **VALIDATION_SIM** (회귀·분석·감사: **DESKTOP_DRY_RUN**)

Policy Checkpoint SHA256: `6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05`

Evidence Status: **PASS — 기존 데이터의 목적함수 비교·동일 비용의 독립 QR 수치 교차검사·단일 rollout 수집 및 인과성 감사. SUSPICIOUS — 일부 원래 covariance RLS와 batch 계수의 엄격한 수치 일치. FAIL — B의 전체 온라인 식별 기준. NOT_TESTED — C의 새 K 활성화 및 제어 이득.**

Observed Metrics / Behavior / Log Summary:

**Offline에서는 prior/forgetting을 포함한 목적함수가 성패를 바꿨지만, 그 설정을 개선하는 것만으로 단일 rollout 식별이 해결되지는 않았다.** A의 plain LS와 약한 prior·forgetting=1 비교는 다섯 cohort 모두 6/6 예측 통과했다. B의 새 연속 rollout 36회는 모두 64초를 완료했으나, 전체 정보량·후속 예측·조건부 B 검증을 함께 통과한 모델은 **0/540**이었다. 일부 60초 Local 후보의 후속 예측은 통과했다. 이를 모두 예측 실패로 합치지 않는다. 두 환경 모두 사전 C admission이 실패해 새 K를 적용하지 않았다.

## A — 같은 데이터, 다른 목적함수

신규 MuJoCo 실행 없이 이전 Nominal의 10/30/60/1000초 분기 자료와 Phase C friction0.2의 10–60초 stream 자료를 사용했다. Nominal은 시각별 78개 probe와 고유 baseline 6개, friction0.2는 3개 학습 stream이다. 30개 모델을 평가 전에 동결했다. 검증 cohort도 기존에 사용한 자료이므로 이번 A를 새로운 미사용 물리 검증이라고 부르지 않는다. B 설정은 A 결과를 보기 전에 별도로 고정했다.

셀은 독립 초기조건의 예측 기준 통과 수다. A2/A3는 nominal prior, forgetting=0.9995, P0=100이다. P0를 키우면 prior 정규화가 약해진다.

| 학습·검증 cohort | A1 Plain LS | A2 동일 비용 Batch | A3 Covariance RLS | A4 λ=1, P100 | A4 λ=1, P1e8 nominal mean | A4 λ=1, P1e8 zero mean |
|---|---:|---:|---:|---:|---:|---:|
| Nominal 10초 | 6/6 | 6/6 | 6/6 | 0/6 | 6/6 | 6/6 |
| Nominal 30초 | 6/6 | 0/6 | 0/6 | 0/6 | 6/6 | 6/6 |
| Nominal 60초 | 6/6 | 0/6 | 0/6 | 0/6 | 6/6 | 6/6 |
| Nominal 1000초 | 6/6 | 6/6 | 6/6 | 6/6 | 6/6 | 6/6 |
| Friction0.2 post | 6/6 | 0/6 | 0/6 | 0/6 | 6/6 | 6/6 |

**Forgetting=1만으로 해결되지는 않았다.** P100을 유지한 비교는 초기 Nominal과 friction0.2에서 실패했고, 약한 prior와 결합한 비교는 통과했다. 이 비교만으로 forgetting과 prior 각각의 유일한 기여를 확정하지 않는다.

### A2와 A3의 일치 여부

계수 상대 차이의 사전 허용치는 1e−7이다. 아래 SUSPICIOUS를 사후 완화하지 않았다. 예측 통과 수가 같다는 사실과 계수 수치 일치를 구분한다.

| Cohort | 원래 covariance RLS 대비 Batch 상대 차이 | 수치 판정 | 별도 recursive QR 대비 Batch 상대 차이 |
|---|---:|---|---:|
| Nominal10 | 7.57e−7 | SUSPICIOUS | 9.26e−11 |
| Nominal30 | 7.92e−7 | SUSPICIOUS | 8.65e−11 |
| Nominal60 | 2.28e−7 | SUSPICIOUS | 3.80e−11 |
| Nominal1000 | 1.84e−10 | PASS | 3.36e−12 |
| Friction0.2 | 5.48e−12 | PASS | 1.08e−13 |

사후 독립 recursive QR는 **같은 prior/forgetting 비용**을 계산했으며 다섯 cohort 모두 수치 PASS였다. QR의 예측 통과 수는 A2와 정확히 같았다. 따라서 원래 covariance 수치 정밀도 문제는 남지만, 이를 개선해도 같은 목적함수의 Nominal30/60·friction0.2 예측 실패가 해소되지는 않았다. QR 모델을 기존 모델 대신 사용하거나 온라인 설정을 다시 선택하지 않았다. 다른 A4 수치 경고도 [원본 수치표](run_01/A_numerics.json)에 보존했다.

**분기 자료의 순서도 가중 목적함수의 일부다.** Nominal A는 78개 probe를 읽은 뒤 고유 baseline 6개를 읽었다. Baseline은 transition의 7.14%지만 forgetting 가중치의 **69.89%**를 차지했다. 유효 기억 길이 약 2000 transition은 실제 연속 데이터라면 약 40초지만, 여기서는 인위적으로 연결한 분기 순서다. 이를 실제 배포 시간으로 해석하지 않는다. Friction0.2는 별도 baseline 추가 없이 3개 stream을 고정 순서로 읽었고 같은 비용의 Batch/QR도 실패했다. 전체 차이를 Nominal의 baseline 순서 하나로 설명할 수도 없다.

## B — 실제 단일 시간 흐름의 식별

Nominal과 friction0.2의 물성을 첫 physics 이전에 설정하고 끝까지 유지했다. 개발 seed900/901/902의 3개 시작조건과 별도 평가 seed910/911×3pitch의 6개 시작조건을 사용했다. 환경별 0.01/0.02 Nm probing으로 개발 12회, 평가 24회, 총 **36회×64초**를 수집했다.

Frozen FlashSAC·native wheel/leg PD·기존 raw M4 p/v와 Fixed nominal K/bias/reference를 유지했다. 센서 FK 보정이나 새로운 base-link estimator는 넣지 않았다. 최초 RL 진입의 p_hold는 끝까지 고정했다. 합 residual 0.4328–0.5328 Nm, slew 2 Nm/s, wheel±12 Nm를 유지했으며 초기 ramp는 원래처럼 lower band 아래에서 시작할 수 있다.

추정기는 센서 24상태와 clipping 뒤 알려진 software residual을 사용한다. GT·물성 라벨·실제 motor gain/lag를 반영한 물리 토크는 회귀 입력이 아니다. B에는 snapshot 분기·복원이나 Direct B 실험이 없다. GT는 물리 평가·안전 종료에만 사용하며 학습 eligibility와 probing 허용은 센서 및 알려진 명령으로 판단한다.

누적 원래 RLS, 누적 λ=1/P100, 누적 λ=1/P1e8, 최근 10초·20초 λ=1/P1e8를 같은 rollout에서 shadow 비교했다. 매 20ms eligible transition에서 재귀 갱신하고, 국소 창은 실제 경과 시간으로 오래된 transition을 제거했다. 10/30/60초에 후보를 동결한 뒤 같은 시간 흐름의 후속 4초로 검증했다. 이 세 검증 구간은 **이후의 모든 학습에서도 영구 제외**했다. 2초와 4초 예측은 이 후속 구간에서 평가한다.

후보의 same-objective SVD 수치 보정은 수집 전 계획에 명시했다. Raw recursive 모델과 차이도 저장했으며 안정 모델로 투영하거나 비용을 바꾸지 않았다. 따라서 이번 B는 보정 없는 covariance 재귀만의 성능이라고 부르지 않는다.

### 전체 gate와 부분 통과

540개는 36 rollout×3시점×5추정기의 모델 평가 수다. 물리적으로 독립된 후속 입력 구간은 108개이며 같은 구간에 여러 모델을 평가했다. 전체 gate는 학습 정보량, 후속 자유 예측, 조건부 B 신뢰도를 모두 요구한다.

| Held-out 환경·진폭 | Local20 예측 / 정보 / 전체 | Local10 예측 / 정보 / 전체 | 누적 3방법 전체 |
|---|---:|---:|---:|
| Nominal 0.01 | 0 / 0 / 0 | 0 / 0 / 0 | 각각 0/18 |
| Nominal 0.02 | 0 / 0 / 0 | 0 / 0 / 0 | 각각 0/18 |
| Friction0.2 0.01 | 0 / 3 / 0 | 0 / 1 / 0 | 각각 0/18 |
| Friction0.2 0.02 | 2 / 6 / 0 | 2 / 3 / 0 | 각각 0/18 |

각 Local 셀의 분모는 18이다. Friction0.2/0.02의 누적 3방법은 정보량 각각 6/18, 예측 각각 0/18이었다. **조건부 B 전체 기준은 held-out 0/360**이었다. 개발 전체 gate도 0/180이다.

예측을 통과한 held-out 4개는 모두 friction0.2/0.02의 60초 Local 후보였다. 이 중 3개는 학습 정보량도 통과했다. 예를 들어 seed910/pitch−0.035의 Local20은 학습 condition 약 **820,798**, 후속 B 회귀 condition 약 **2,008,311**이었다. B 계수 상대 차이는 약 **0.000488%**로 작았지만 후속 회귀 condition≤1e6 기준을 넘었다. 작은 B 점추정 오차를 충분한 독립 검증으로 해석하거나 이 gate를 완화하지 않았다.

A의 NRMSE 분모는 이전 matched 입력 응답이고, B는 실제 후속 센서 변화량과 사전 floor다. 서로 다른 정규화 수치를 직접 성능 순위로 비교하지 않는다. B는 rolling0.1/0.5/1/2초 p/v RMSE≤0.02mm/0.02mm/s 및 NRMSE≤30%, full2초 같은 RMSE, full4초≤0.05mm/0.02mm/s를 함께 요구했다. Conditional B는 후속 센서 회귀이며 matched-state Direct B가 아니다.

### 입력 제한과 실제 excitation

Fixed raw 명령이 band 경계에 가깝거나 센서 안전 조건이 부족하면 probe를 넣지 않았다. Held-out 6개 시작조건의 trial 지표 중앙값이다.

| 환경·진폭 | Probe 허용 시간 % | Residual cap 시간 % | 요청 probe 에너지 Nm²·s | 0–64초 base IAE mm·s | 최대 planar drift mm |
|---|---:|---:|---:|---:|---:|
| Nominal 0.01 | 14.28 | 74.28 | 0.000691 | 2145.14 | 47.34 |
| Nominal 0.02 | 2.70 | 72.63 | 0.000596 | 2146.27 | 47.42 |
| Friction0.2 0.01 | 24.28 | 73.25 | 0.001216 | 1433.01 | 36.37 |
| Friction0.2 0.02 | 17.36 | 73.25 | 0.003116 | 1434.47 | 36.47 |

Nominal에서는 진폭을 0.02로 늘리면 필요한 입력 여유도 커져 허용 시간이 줄었다. 더 큰 제안 진폭이 더 많은 유효 excitation을 보장하지 않았다. 위 에너지는 허용된 요청 probe의 값이다. Ramp/slew 뒤 같은 센서 상태·이전 명령에서 probe 유무의 명령 차이를 재계산한 에너지는 [별도 감사](run_01/probe_budget_audit.json)에 학습/검증 구간별로 저장했다. 이것도 독립된 물리 motor residual의 에너지는 아니다.

36/36 완료는 balancing·수집 완료다. Held-out의 절대 위치 유지 기준은 네 환경·진폭 조합 모두 **0/6**이었다. 모두 같은 Fixed+guarded probe 제어를 사용했으므로 이 물리 지표를 Local RLS의 제어 이득으로 부르지 않는다. 각 추정기는 shadow이며 실제 제어 K를 바꾸지 않았다.

## C — 조건 미충족, NOT_TESTED

사전 규칙은 개발 3/3에서 검증된 모델을 얻는 방법·진폭을 선택하고 held-out 6/6 확인 뒤 C를 여는 것이다. 두 환경 모두 개발 조건을 통과한 설정이 없었다. 따라서 **새 Target K 채택 0회, Fixed/E6/Adaptive K/Full의 새 제어 비교 NOT_TESTED**다. C 제어 성능 FAIL이나 Full의 무효를 입증한 결과로 바꾸지 않는다. [환경별 admission](run_01/B_admission.json)과 [C 상태](run_01/C_status.json)를 보존했다.

## 판단과 다음 별도 실험

1. Offline 국소 자료에서는 현재 prior·forgetting·자료 순서가 예측 실패를 만들 수 있었다. 원래 covariance 수치 오차도 존재하지만 동일 비용의 QR가 같은 예측 실패를 보여 재귀 roundoff만으로 설명할 수 없다.
2. 약한 prior의 Offline 성공은 실제 단일 rollout의 충분한 정보량을 보장하지 않았다. 이번 국소 창은 일부 늦은 시점에서 예측을 개선했지만 전체 검증은 통과하지 못했다. 신뢰 가능한 식별에 필요한 데이터 시간은 이번 64초 예산에서 미확정이다.
3. 다음에는 **같은 band 안에서 제어와 식별 입력의 여유를 어떻게 배분할지** 별도 사전 계획으로 비교할 근거가 있다. 특히 Fixed가 band를 자주 사용하는 상황과 후속 4초 B 회귀의 conditioning을 분리해야 한다. 더 긴 후속 검증은 정보량을 늘릴 수 있지만 운용 영역 이동 비용도 함께 평가해야 한다. 이번 기준·예산을 소급 변경하지 않는다.
4. Base-link FK/CAD를 선행 조건으로 추가하지 않았다. 물리 파라미터 확장·새 K·위치 복원 제어·Sim2Real·실기는 이번 범위에서 수행하지 않았다. Prior에는 nominal MuJoCo offline calibration이 포함되며 Isaac-only source identification 성공이 아니다.

## 변경·검증·재현

신규 source 6개: `test/online_local_m4.py`, `test/run_online_local_m4.py`, `test/test_online_local_m4.py`, `test/analyze_online_local_m4.py`, `test/audit_online_local_m4.py`, `test/audit_online_local_rollout.py`. 처음 4개는 수집 전 동결했고 마지막 2개는 모델·제어를 바꾸지 않는 사후 수치/인과성 감사다. 계획·prior·기존 자료 6585파일을 hash로 보호했다.

독립 unit **5개 PASS**: 동일 weighted objective 재귀/배치, 국소 창 제거, 영구 검증 제외, affine 예측·조건부 B 거부, 위치 대칭·action 인과 구조. 전체 36개 궤적의 goal/action/history/leg 경로·공통 입력 예산·동결 후보를 감사했다. 대표 3개 rollout의 과거 센서·알려진 명령·센서 eligibility만으로 **45개 raw/refined 후보 쌍을 exact 재현**했다. 전체 540개 후보의 검증 자료 학습 제외도 별도 확인했다.

전체 agent-check는 기존 학습 설정의 trailing whitespace 6곳으로 **FAIL**이다. 실제 syntax/URDF 수와 마지막 상태는 [로그](run_01/agent_check.log)에 기록한다. 이번 파일의 diff 검사는 별도로 수행한다. 브랜치 `agent/codex/dev_tita_gluon`; production/runtime·기존 정책/모델/보고서·Q/R 변경, hardware, commit/push 없음. [완료 감사](run_01/completion_audit.json)의 PASS는 workflow/증거 무결성 판정이며 연구 전체 성공이 아니다.

재현은 새 미사용 root에서 수행한다. 이미 완료한 stage를 덮어쓰지 않는다. 환경 변수는 `MPLCONFIGDIR=/tmp/lqr_mpl OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1`이다.

```bash
git status --short > /tmp/online_local_m4_status_before.txt
/home/cocel/venvs/cosim_ros2_jazzy/bin/python test/test_online_local_m4.py
/home/cocel/venvs/cosim_ros2_jazzy/bin/python test/run_online_local_m4.py --stage init --root docs/exp/2026-10-16/new_online_local_m4
/home/cocel/venvs/cosim_ros2_jazzy/bin/python test/run_online_local_m4.py --stage A --root docs/exp/2026-10-16/new_online_local_m4
/home/cocel/venvs/cosim_ros2_jazzy/bin/python test/run_online_local_m4.py --stage development --root docs/exp/2026-10-16/new_online_local_m4 --workers 3
/home/cocel/venvs/cosim_ros2_jazzy/bin/python test/run_online_local_m4.py --stage test --root docs/exp/2026-10-16/new_online_local_m4 --workers 3
/home/cocel/venvs/cosim_ros2_jazzy/bin/python test/run_online_local_m4.py --stage admission --root docs/exp/2026-10-16/new_online_local_m4
/home/cocel/venvs/cosim_ros2_jazzy/bin/python test/analyze_online_local_m4.py --root docs/exp/2026-10-16/new_online_local_m4
/home/cocel/venvs/cosim_ros2_jazzy/bin/python test/audit_online_local_m4.py --stage numerical --root docs/exp/2026-10-16/new_online_local_m4
/home/cocel/venvs/cosim_ros2_jazzy/bin/python test/audit_online_local_rollout.py --root docs/exp/2026-10-16/new_online_local_m4
./scripts/agent-check.sh
```

최종 감사는 해당 실행의 SUMMARY와 unit/agent-check 로그를 저장한 뒤 `test/audit_online_local_m4.py --stage final --root <root>`로 실행한다. 수집·모델 적합에 필요한 단계는 아니다.

산출물: [사전 계획](PLAN.md), [동결 plan](run_01/plan.json), [A 전체 결과](run_01/A_results.json), [A 수치 경고](run_01/A_numerics.json), [동일 비용 QR 교차검사](run_01/A_QR_numerical_audit.json), [개발](run_01/development_results.json), [held-out](run_01/test_results.json), [전체 비교 표](run_01/REPORT.md), [센서 인과성 재현](run_01/causal_replay_audit.json), [입력 전달 감사](run_01/probe_budget_audit.json), [학습 제외·goal·history 감사](run_01/analysis_integrity.json), [최종 diff](task.diff), 전체 trajectory/startup NPZ·동결 후보·source/hash/log.
