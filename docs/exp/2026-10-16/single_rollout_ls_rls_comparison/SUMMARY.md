# model_60000 — 같은 단일 rollout에서 Plain LS와 Online RLS 비교

작성일: 2026-10-16 (Asia/Seoul)

Execution Domain: **DESKTOP_DRY_RUN** (기존 VALIDATION_SIM 로그의 읽기 전용 재분석)

Policy Checkpoint SHA256: `6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05`

Evidence Status: **PASS — 동일 transition·동일 미래 구간 비교, Friction0.2의 일부 국소 Plain LS 미래 예측. FAIL — 정보량·조건부 B를 포함한 전체 식별 기준. NOT_TESTED — 새로운 물리 수집·K 적용·LQR 제어 이득.**

Observed Metrics / Behavior / Log Summary:

**같은 단일 rollout에서도 Plain LS는 미래 예측에 성공하는 경우가 있었고, 같은 데이터의 RLS보다 더 많이 통과했다.** 특히 Friction0.2의 60초·최근20초·0.02 Nm 조건은 Plain LS가 **6/6**, 저장된 RLS 보정 후보가 **2/6** 예측 통과였다. 이 조건에서 학습 정보량도 6/6 통과했지만 후속 B 회귀의 condition이 사전 한계를 넘어 전체 식별 기준은 모두 실패했다.

따라서 “단일 rollout 데이터로는 LS조차 항상 실패한다”는 설명은 지지되지 않는다. **현재 추정 목적함수·정규화의 영향을 먼저 검토할 근거가 강화됐다.** 동시에 국소 창·시점에 따라 LS도 실패했고 독립 B 신뢰도가 부족했으므로, 입력·운용 영역 문제가 해결됐거나 새 K를 적용할 수 있다는 결론은 아니다.

## 동일 데이터와 고정 기준

[사전 계획](PLAN.md)과 [동결 source/plan](run_01/plan.json)을 새 비교 결과 계산 전에 저장했다. 원래 Online Local M4의 Nominal/friction0.2×0.01/0.02 Nm, 개발 12회·평가 24회, **36개 단일 64초 rollout**을 그대로 읽었다. 새 MuJoCo 실행·snapshot 복제·Direct B는 **0회**다. 기존 결과를 알고 시작한 사후 진단이며 새 미사용 검증 cohort라고 부르지 않는다.

각 10/30/60초 후보의 저장된 `training_times`를 transition 종료 시각으로 해석해 원본 index를 복구했다. 기존 eligibility 및 누적/최근10초/최근20초 창에서 재구성한 index와 exact 비교했다. 센서 24상태, software 실제 residual, nominal 중심·단위·prior, 최초 p_hold, action B의 8개 causal zero rows와 위치 translation 구조를 유지했다.

10–14/30–34/60–64초는 모든 후보의 학습에서 영구 제외했다. LS fitter에는 freeze 시점까지의 prefix만 전달했다. 모든 LS/같은 비용 Batch 모델을 [파일·hash](run_01/fit_manifest.json)로 동결한 뒤 별도 score 단계에서 원래 후속4초 센서·명령을 평가했다. GT·물성 라벨은 적합·검증 입력에 없다. 기존 제어기·토크 band·상태 차원·Q/R·threshold는 변경하지 않았다.

| 방법 | 계산한 모델 |
|---|---|
| Plain LS | 기존 constrained affine LS, group RMS scaling, rcond1e−8, prior/forgetting 없음 |
| Same-cost Batch | 해당 RLS와 같은 nominal prior/P0/forgetting 비용을 augmented SVD로 계산 |
| Raw RLS | 실제 원래 실행 중 매20ms 재귀 계산해 저장한 모델 |
| Candidate RLS | 원래 실행에서 같은 비용 SVD 보정 후 저장한 후보 |

기존 RLS 보정 후보의 미래 예측 결과 전체를 재계산해 원래 validator 수치와 **540/540 exact 일치**시켰다. Same-cost Batch 계수도 저장 후보와 **540/540 상대 차이 0.0**이었다. Raw RLS와 Candidate RLS는 다른 모델이며 표에서 구분한다.

원래 기준을 그대로 적용했다. 예측은 rolling0.1/0.5/1/2초 및 최초2/4초 absolute p/v 자유 예측이며 NRMSE≤30%, rolling/최초2초 RMSE≤0.02mm/0.02mm/s, 최초4초≤0.05mm/0.02mm/s다. 정보량은 관측 rank25·condition≤1e6·입력 innovation≥1%·N≥250을 요구한다. 후속 조건부 B도 rank25·condition≤1e6·부호·상대 차이≤30%를 요구한다. LS에는 가상의 covariance를 붙이지 않았고 관측 정보 기준을 공유했다. 원래 후보의 양수 covariance 기준이 이 공통 판정과 달라지는 경우는 없었다.

## Held-out의 같은 창 비교

셀은 **10/30/60초 후보 총18개 중 미래 예측 통과 수**다. 각 시각의 6개 시작조건을 합친 것이며 18개 독립 로봇 실험이 아니다. 아래 RLS는 λ=1/P1e8이다. 원래 λ=0.9995/P100 및 λ=1/P100의 누적 비교도 [전체 표](run_01/REPORT.md)와 [CSV](run_01/metrics.csv)에 남겼다.

| 환경 | Probe Nm | 학습 창 | Plain LS | Raw RLS | Candidate RLS |
|---|---:|---|---:|---:|---:|
| Nominal | 0.01 | 최근20초 | 7/18 | 0/18 | 0/18 |
| Nominal | 0.01 | 최근10초 | 7/18 | 0/18 | 0/18 |
| Nominal | 0.01 | 누적 | 4/18 | 0/18 | 0/18 |
| Nominal | 0.02 | 최근20초 | 6/18 | 0/18 | 0/18 |
| Nominal | 0.02 | 최근10초 | 7/18 | 0/18 | 0/18 |
| Nominal | 0.02 | 누적 | 4/18 | 0/18 | 0/18 |
| Friction0.2 | 0.01 | 최근20초 | 12/18 | 0/18 | 0/18 |
| Friction0.2 | 0.01 | 최근10초 | 12/18 | 0/18 | 0/18 |
| Friction0.2 | 0.01 | 누적 | 0/18 | 0/18 | 0/18 |
| Friction0.2 | 0.02 | 최근20초 | 12/18 | 1/18 | 2/18 |
| Friction0.2 | 0.02 | 최근10초 | 12/18 | 3/18 | 2/18 |
| Friction0.2 | 0.02 | 누적 | 0/18 | 0/18 | 0/18 |

누적 LS는 RLS prior/forgetting 설정이 달라도 같은 데이터로 계산해 같은 모델이다. 10초에는 모든 창이 같은 prefix일 수도 있다. 중복을 포함한 matched 비교 540건 중 Plain LS 예측 통과는 **개발52/180, 평가99/360**이었다. Raw RLS는 개발2/180·평가4/360, Candidate RLS는 개발1/180·평가4/360이었다. 평가 360건의 LS/Candidate RLS 짝은 **둘 다 통과4, LS만 통과95, RLS만 통과0, 둘 다 실패261**이다. Raw RLS와의 집계 수는 같아도 통과한 후보의 identity가 모두 같지는 않다.

같은 episode·시각·training index 집합의 중복을 제거하면 LS 학습 집합은 **252개**이고, 개발36/84·평가67/168 예측 통과였다. 이들 역시 같은 episode의 중첩 창·여러 시각이므로 독립 표본 수가 아니다. 물리 궤적은 36개, 고유 후속 센서 구간은 108개이며 네 방법의 총 점수 2160개를 새 물리 실험으로 세지 않는다.

## 시점과 국소 창의 영향

Friction0.2의 국소 LS는 두 진폭·최근10/20초 모두 **10초0/6, 30초6/6, 60초6/6** 예측 통과였다. 누적 LS는 같은 환경의 모든 시각에서 0/6이었다. 같은 방법·같은 실제 배포에서도 오래된 자료를 포함하는지에 따라 예측이 달라졌다. 이 비교는 국소 창을 사용할 근거이며 특정 상태 하나가 유일한 원인이라는 증명은 아니다.

다만 **30초의 6/6은 A/B의 충분한 식별을 뜻하지 않는다.** 이 시점 Friction0.2의 LS 비action 회귀 rank는 25가 아닌 **24**였고, 후속 B 회귀도 rank24였다. 입력과 상수항을 분리할 정보가 부족해도 실제 후속 궤적을 예측할 수 있었다. 이 경우는 원래 정보/B 기준으로 계속 FAIL이다. 평가 LS 예측 통과99건 중 24건이 이 rank 부족 사례이며 나머지75건의 group rank는25/24였다. Action group은 입력 열을 제외하므로 full rank가24다.

Nominal LS는 두 진폭 모두 10초4/6, 30초0/6이었다. 60초에는 최근20초가0.01 Nm에서3/6·0.02 Nm에서2/6, 최근10초는 각각3/6이었다. Nominal의 모든 평가 후보는 학습 정보량 기준도 불통과했다. 따라서 국소 LS가 모든 Nominal 운용 구간을 해결했다는 결과는 아니다.

## 예측·정보량을 모두 통과해도 남는 B 검증

가장 분명한 사례는 Friction0.2/0.02 Nm/60초/최근20초다. 같은 6개 시작조건에서 다음과 같았다.

| 항목 | Plain LS | Candidate RLS |
|---|---:|---:|
| 미래 예측 통과 | **6/6** | 2/6 |
| 학습 정보량 + 미래 예측 통과 | **6/6** | 2/6 |
| 2초 rolling p/v NRMSE 중앙값 | **2.120 / 0.423%** | 213.499 / 186.102% |
| 최초4초 p/v RMSE 중앙값 | **0.001811mm / 0.001072mm/s** | 69.354mm / 242.300mm/s |
| 후속 B 신뢰도 전체 통과 | 0/6 | 0/6 |
| 전체 식별 기준 통과 | 0/6 | 0/6 |

큰 예측 오차는 모델 자유 예측 수치이며 실제 robot/physics의 발산이 아니다. 후속 B 회귀 condition은 약 **1.992e6–2.116e6**로 사전 한계1e6을 넘었다. Plain LS의 B 점추정 상대 차이는 약 **0.000868–0.023115%**로 작았지만, 신뢰도가 부족한 회귀와의 일치로 전체 PASS를 주장하지 않는다. 이 검사는 matched-state Direct B가 아니다.

전체 평가에서 LS의 정보량+예측 통과는13/360, Candidate RLS는3/360이었다. 둘 다 Nominal에서는0이었다. 네 방법 모두 개발·평가를 합친 **전체 gate는0/540**이며 새 K 채택·제어 이득 비교는 NOT_TESTED다. 공통 후속 B condition 실패 때문에 전체 gate만 보면 가려지는 예측 차이를 위에 별도로 남겼다.

## 목적함수의 영향과 해석 한계

같은 RLS 비용의 Batch가 기존 보정 후보와 계수까지 exact 일치하므로, 후보 실패를 재귀 구현 오차로만 설명할 수 없다. Plain LS와 같은 비용 Batch가 다른 예측을 보이는 사례는 실제 단일 rollout에서도 목적함수·정규화 영향이 있음을 보여준다. 다만 Plain LS는 group RMS scaling/rcond1e−8, RLS 비용 해는 고정 nominal scaling과 prior를 사용하므로 이 실험 하나로 prior/forgetting/수치 scaling의 개별 원인을 모두 분리했다고 주장하지 않는다.

사후 **적합 없이** 원래 학습 행렬의 singular value를 계산했다. λ=1/P1e8이어도 nominal-scaled 좌표의 prior precision은1e−8이다. 위 Friction0.2/0.02/60초/Local20의 seed910/pitch−0.035에서 가장 약한 데이터 방향의 precision은 약3.92e−10으로, prior가 약 **25.5배**였다. “P1e8이므로 모든 방향에서 prior가 무시된다”는 가정은 성립하지 않았다. 이는 방향별 prior/data 크기의 진단이며 그 한 방향이 예측 실패의 유일한 원인이라는 인과 분해가 아니다. [계산식·324개 조건별 값](run_01/regularization_diagnostic.json)을 보존했고 새 모델·threshold 선택에 사용하지 않았다.

현재 판단은 다음과 같다.

1. **일부 구간은 같은 단일 rollout에서 LS 예측 PASS / RLS 예측 FAIL이다.** 이 구간에서는 입력 예산 확대보다 현재 RLS 목적함수·정규화·수치적 표현을 먼저 재검토할 근거가 있다.
2. **Nominal30초·Friction0.2 누적/초기 구간은 LS도 FAIL이다.** 알고리즘 하나만 고치면 모든 영역이 해결된다고 볼 수 없다. 데이터와 국소 유효성을 별도로 점검해야 한다.
3. **예측 PASS와 신뢰 가능한 A/B 식별은 다르다.** Rank 부족에서도 예측한 사례와, rank/학습 정보량은 충분해도 후속 B condition이 부족한 사례를 구분했다. 더 나은 probing 배분은 필요한 조건에 한해 다음 별도 계획으로 다룬다.
4. 30초 최근10초 LS의 성공은 실제 배포20–30초의 한 sensor/command 구간으로 적합해30–34초를 예측한 결과다. Offline 분기624초 자료를 쓴 결과는 아니지만, 새 온라인 알고리즘을 실행해 모델/K를 채택한 실증도 아니다. 모델을 평가한 뒤 좋은 후보만 선택해 제어에 연결하지 않았다.

## 변경·검증·재현

신규 code2개: `test/compare_single_rollout_ls_rls.py`, `test/test_single_rollout_ls_rls.py`. 기존 모델·제어기·정책·runtime·보고서·물리 궤적은 변경하지 않았다. 새 보고서와 모델/점수 증거를 별도 경로에 보존했다. 브랜치 `agent/codex/dev_tita_gluon`; hardware·commit/push 없음.

독립 unit **4개 PASS**: 시간창/index 복구, 검증 transition 재주입 거부, 알려진 affine 계수 및 position/action 구조, 선택하지 않은 미래 값 변경에 대한 적합 불변성. 원래540개 후보의 후속 결과 exact 재현과 동일 비용540개 모델 exact 일치는 실제 저장 증거로 별도 확인했다. 기존 파일 **6885개**와 source/plan/frozen 모델 hash를 감사한다. 전체 agent-check 결과·syntax/URDF 수는 [실제 로그](run_01/agent_check.log), 이번 변경의 diff·보호 hash는 [완료 감사](run_01/completion_audit.json)에 기록한다. 기존 학습 설정의 trailing whitespace 문제는 수정하지 않는다.

재현은 새 미사용 root에서 수행한다. 초기화가 기존 경로를 거부하며 fit/score stage도 완료 폴더를 덮어쓰지 않는다. 환경 변수는 `MPLCONFIGDIR=/tmp/lqr_mpl OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1`이다.

```bash
git status --short > /tmp/single_rollout_ls_status_before.txt
/home/cocel/venvs/cosim_ros2_jazzy/bin/python test/compare_single_rollout_ls_rls.py --stage init --root docs/exp/2026-10-16/new_single_rollout_ls
/home/cocel/venvs/cosim_ros2_jazzy/bin/python test/test_single_rollout_ls_rls.py
/home/cocel/venvs/cosim_ros2_jazzy/bin/python test/compare_single_rollout_ls_rls.py --stage fit --root docs/exp/2026-10-16/new_single_rollout_ls --workers 3
/home/cocel/venvs/cosim_ros2_jazzy/bin/python test/compare_single_rollout_ls_rls.py --stage score --root docs/exp/2026-10-16/new_single_rollout_ls --workers 3
./scripts/agent-check.sh
```

완료 감사는 해당 실행의 SUMMARY·unit/agent-check 로그를 저장한 뒤 `test/compare_single_rollout_ls_rls.py --stage audit --root <root>`로 실행한다. 사후 singular-value 진단은 기본 적합·평가에 필요하지 않으며 계산식을 JSON에 명시했다.

산출물: [사전 계획](PLAN.md), [동결 plan/source](run_01/plan.json), [전체 모델 동결 manifest](run_01/fit_manifest.json), [모든 짝별 지표·집계](run_01/comparison.json), [CSV](run_01/metrics.csv), [개발/평가 전체 표](run_01/REPORT.md), [학습 행렬의 prior/data 진단](run_01/regularization_diagnostic.json), [unit](run_01/unit_tests.log), [fit 로그](run_01/fit.log), [score 로그](run_01/score.log), [최종 diff](task.diff), [완료 감사](run_01/completion_audit.json), `run_01/models/`의 모든 동결 모델·training index와 `run_01/scores/`의 episode별 전체 예측 수치.
