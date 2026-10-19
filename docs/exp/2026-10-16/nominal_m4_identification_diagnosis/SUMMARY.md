# model_60000 — Nominal M4의 방법·동작 영역·데이터 구성 분리

작성일: 2026-10-16 (Asia/Seoul)

Execution Domain: **VALIDATION_SIM** (회귀·분석·감사: **DESKTOP_DRY_RUN**)

Policy Checkpoint SHA256: `6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05`

Evidence Status: **PASS — 이전 Nominal 재현, 새 Nominal의 시각별 국소 공동 LS 예측. FAIL — 같은 모델의 다른 운용 시각 일반화, 초기 영역의 paired A/B+별도 c 전체 absolute 기준.** 실제 온라인 식별·새 K·위치 복원 제어·다른 Target 재평가·실기: **NOT_TESTED**.

Observed Metrics / Behavior / Log Summary:

**24-state M4가900초 정착 후에만 식별 가능한 것은 아니었다.** 새 Nominal의10·30·60초 snapshot 각각에서 학습한 공동 LS는 별도6개 초기조건의 같은 시각 검증을 모두 통과했다. 반면 정착 모델을 초기 영역에 옮기거나, 초기의 한 시각 모델을 다른 시각에 그대로 적용하면 실패했다. 초기 paired A/B의 작은 입력 응답은 정확했어도, 별도 평균 c를 붙인 absolute 진행 예측은 실패했다.

따라서 이번 결과는 **국소 식별 가능성과 운용 영역 사이의 일반화를 구분해야 한다**는 근거다. 공동 LS 자체가 Nominal 실패의 원인이라는 설명은 지지하지 않는다. 같은24-state를 유지한 채 데이터 구성과 식별 대상 영역을 바꾸면 성공할 수 있었다. 단일 rollout의 온라인 식별 성공을 입증한 결과는 아니다.

## 1. 이전 성공은 그대로 재현됐다

이전 train234개 응답·고유 baseline18개를 다시 읽고 기존 계산을 재현했다. 원래 paired A/B와 재계산 행렬의 최대 차이는 **A=0.0, B=0.0**이었다. 기존 test306개에서 paired8초 p/v NRMSE도 **4.0368/2.6581%**로 저장 지표와 같았다. A/B 고정 후 baseline 평균 defect로 c를 구하는 계산도 이전 모델과 일치했다.

기존 fresh snapshot3개에서8초 baseline 및8초 validation PRBS를 실제 MuJoCo에서 다시 실행했다. 총6개 rollout의 **14개 배열씩**이 원본과 exact 일치했다. Policy/state/observation/action/history/torque 정의가 달라져 이전 PASS가 사라진 재현 문제는 관측하지 않았다. Snapshot으로부터의 재현이며 그 앞1000초 전체를 다시 실행한 것으로 세지 않는다.

| 기존 학습 자료·평가 cohort | Paired A/B+별도 c | Absolute 공동 LS |
|---|---|---|
| 기존 test306응답·18baseline | PASS, baseline18/18 | FAIL, baseline9/18; 응답 기준은 PASS |
| 이전 fresh204응답·12baseline | PASS, baseline12/12 | PASS, baseline12/12 |

Joint LS가 모든 정착 cohort에서 실패했던 것은 아니다. 반대로 paired 응답8초4.04/2.66%와 affine absolute 예측의 지표도 같은 수치가 아니다. [재현 수치·실제 replay](run_01/legacy_results.json)

새 비교용 fitter도 이전 train 자료에서 원래 함수와 교차검사했다. 두 방법의 A 최대 차이는 약1.2e−11/3.2e−11 수준이었다. 새 코드의 식별식 복사 오류가 큰 성능 차이를 만든 증거는 없다. [수치 교차검사](run_01/fitter_legacy_crosscheck.json)

## 2. 새 비교의 고정 조건

[사전 계획](PLAN.md), [동결 plan/source/hash](run_01/plan.json), [repository audit](run_01/repository_audit.json)에 조건과 기준을 먼저 기록했다.

- 학습 seed800/801×pitch−0.035/0/+0.035, 검증 seed810/811×같은 pitch다. 각 split6개 시작조건이며 seed 집합은 분리했다.
- 처음부터 Nominal 물성을 고정했다. Frozen FlashSAC/native wheel·leg PD와raw previous action·33개 observation·원래24-state p/v를 유지했다. 이전 FK 진단 보정은 주입하지 않았다.
- 첫 RL부터 bias0.4828 Nm를 slew2 Nm/s로 적용하고 같은 배포의10/30/60/1000초 상태를 분기했다. 첫 p_hold와 센서 적분기를 이후에 재설정하지 않았다. 식별용 snapshot의 p=0 좌표 변환은 오프라인 translation이며 제어 목표 변경이 아니다.
- 1000초 자료는 기존 past180초 정착 gate를 요구했다. 학습·검증12조건 모두 통과했다. 지속 yaw 회전은 허용된 기존 gate이며 full pose 정적 평형을 뜻하지 않는다.
- 합 residual0.4328–0.5328 Nm, slew2 Nm/s, wheel±12 Nm를 유지했다. 처음0에서 bias로 올라가는 전환은 기존처럼 잠시 lower band 아래일 수 있다. 추가 입력은 기존0.02/0.05 Nm 및micro0.01 Nm다. Band를 넓히지 않았다.
- 각 snapshot에서8초 baseline,17개 probe,Direct B ±0.01 Nm를 수집했다. Baseline 재실행과 각 분기의 전체 초기 state/history를 검사했다. **12개1000초 prefix·48snapshot·816probe·48baseline·Direct B48쌍**이 모두 완료됐다. 학습/검증 probe는각408개다.
- 같은snapshot의 분기와 같은seed의 여러pitch는 관련된 자료다. 816개를 독립 초기조건816개로 세거나 모집단 유의성을 주장하지 않는다.
- GT는 평가·기존 정착 gate·물리 안전 감사에만 썼다. 회귀는 원래 sensor M4와 알려진 software residual로 수행했다. 실제 physical motor torque를 식별 입력으로 대신 쓰지 않았다.

주 회귀는 이전 코드와 같은rcond1e−10이다. 같은 raw probe/baseline 쌍으로 paired A/B+baseline c와 공동 A/B/c를 비교했다. Joint는 고유 baseline을 한 번씩 추가한다. 이 목적함수·가중 차이와 transition 수를 모델에 기록했다.

모든 **64개 모델을 새 test 수집 전에 동결**했다. Full paired/joint의 시각 교차 검증, rcond1e−8 및fixed nominal centering 보조 비교도 사전 고정했다. 검증을 보고 모델을 다시 선택·회귀하지 않았다.

PASS는 최초2초와rolling0.1/0.5/1/2초 absolute p/v NRMSE≤30%, Direct Bv 부호·오차≤30%, 모든 baseline2초≤0.02mm/0.02mm/s·8초≤0.05mm/0.02mm/s다. 분모는 matched 입력 응답 RMS와 기존 floor다. 전체 중앙값 gate와 초기조건별 통과 수를 함께 보고한다. 아래 주요 Full 결과의PASS는6/6도 만족한다.

## 3. 같은 데이터에서 식별 방법 비교

Full은 시각별6개 학습 snapshot×13개 기존 입력=78응답이다. 모든 셀은 같은 독립6개 시작조건의 검증 결과다. NRMSE는 p/v 순서,2초rolling absolute 예측이다.

| 학습=검증 시각 | Paired A/B+별도 c NRMSE % | 전체 판정·초기조건 | 공동 A/B/c NRMSE % | 전체 판정·초기조건 |
|---|---:|---|---:|---|
| 10초 | 5.211 /17.808 | FAIL,4/6; baseline 기준 실패 | 0.369 /2.148 | **PASS,6/6** |
| 30초 | 35.152 /137.698 | FAIL,0/6 | 3.055 /18.281 | **PASS,6/6** |
| 60초 | 23.056 /266.801 | FAIL,0/6 | 0.882 /3.564 | **PASS,6/6** |
| 1000초 | 2.516 /4.730 | **PASS,6/6** | 2.708 /9.007 | **PASS,6/6** |

공동 LS의8초 전체 absolute p/v NRMSE는10초 **1.451/1.107%**,30초 **9.244/3.171%**,60초 **1.798/0.978%**,1000초 **8.613/3.653%**였다. 이8초 응답 지표는 보조 수치이며 gate를 사후 늘리거나 줄이지 않았다.

### 초기 paired 모델은 A/B 응답부터 틀렸나?

그렇지 않았다. 같은 Full paired A/B의 **순수 delta2초rolling p/v**는10초 **0.233/1.448%**,30초 **0.650/1.905%**,60초 **0.445/1.951%**였다. 작은 torque 응답은 잘 예측했지만, 같은 A/B에 baseline 평균 one-step defect c를 붙인 absolute 진행은 정확하지 않았다.

예를 들어60초 paired 모델은 baseline8초 p/v RMSE의6개 최대값이 **1.052mm/0.258mm/s**였고, 공동 LS는 **0.01038mm/0.00257mm/s**였다. 이 차이는 응답 A/B의 정확도만으로 absolute affine 모델을 보장할 수 없음을 보여준다. c 하나의 물리적 원인을 확정하거나 c를 임의로 재조정한 실험은 아니다. Joint는 비영 내부 상태의 진행과 probe를 함께 맞춘다는 차이가 있다.

따라서 **이전 정착 영역에서 유리했던 paired A/B+별도 c를 과도 영역에도 항상 더 좋은 방법으로 적용할 근거는 없다.** 새 Nominal에서는 공동 LS가 초기 영역의 absolute 예측에 더 적합했다.

![방법·시각·자료 구성](run_01/method_region_composition.png)

## 4. 같은 방법의 동작 영역 일반화

Joint Full 모델의2초rolling v NRMSE(%)다. 행은 학습 시각, 열은 검증 시각이다.

| 학습＼검증 | 10초 | 30초 | 60초 | 1000초 |
|---|---:|---:|---:|---:|
| 10초 | **2.15** |773.30 |3950.10 |12643.89 |
| 30초 |1372.83 | **18.28** |279.71 |5219.61 |
| 60초 |1696.52 |253.89 | **3.56** |5216.53 |
| 1000초 |57600.35 |55146.42 |46363.03 | **9.01** |

같은 시각4개 셀은6/6 PASS, **다른 시각12개 셀은 모두0/6**이었다. 이전 paired+c 및joint 모델도 새1000초에서는 각각6/6 PASS,10/30/60초에서는 각각0/6이었다.

큰%는 작은 입력 응답으로 정규화한 예측 오차이며 MuJoCo의 물리 발산이 아니다. 예를 들어1000초joint 모델→10초의2초rolling p/v RMSE는 **56.11mm/29.53mm/s**,10초 모델→30초는 **0.544mm/0.441mm/s**였다. 실제 수집은 모든 조건에서 정상 종료했다.

Cold10–60초 사이의 **순수delta 응답**은 cross에서도 v 오차약5.7–16.9%에 머무는 비교가 있었다. Absolute 실패를 A/B 변화만으로 설명할 수 없으며, 비영 내부 상태의 진행·affine forcing 불일치도 중요하다. 반면1000초 모델→cold의 순수delta v 오차는paired에서약126–163%,joint에서약106–138%였다. 정착 영역에서 초기 영역으로 옮기면 응답 A/B 자체의 유효성도 무너졌다.

검증baseline의 평균sensor 속도는10/30/60/1000초에서약 **0.934/1.444/0.805/0.0101mm/s**,pitch 평균은 **0.06401/0.06346/0.06210/0.05232rad**였다. 내부action도 변했다. 분포는 [operating_regions.json](run_01/operating_regions.json)에 있다. 이를 특정 한 상태의 유일한 원인으로 확정하지 않는다.

![영역 사이의 예측](run_01/cross_region.png)

이 시험은 각 국소 모델의 전용 범위 밖 적용 실패를 보여준다. **모든 영역을 표현할 단일24-state affine 모델이 수학적으로 존재하지 않는다는 증명은 아니다.** 결과를 확인한 뒤 cold3시각을 섞은 paired fit을 새 후보로 추가하지 않았다.

## 5. 데이터 구성과 양

Joint,1000초 영역, 같은 test의 사전 비교다. 통과한profile을 사후 주 모델로 선택하지 않았다.

| 학습profile | Probe 수 | 학습 초기조건 | 2초rolling v NRMSE | 판정·초기조건 |
|---|---:|---:|---:|---|
| small: sine/PRBS 각각1회 |2 |1 |37.02% |FAIL,0/6 |
| quantity: 같은2종류를 각각3회 |6 |1 |12.35% |PASS,6/6 |
| waveforms: 6종류 |6 |1 |7.66% |PASS,6/6 |
| initials: 3초기조건×2종류 |6 |3 |11.93% |PASS,6/6 |
| full: 6초기조건×13입력 |78 |6 |9.01% |PASS,6/6 |
| full_replicates |102 |6 |9.27% |PASS,6/6 |

앞의4군 진폭은0.02Nm다. 6probe군의probe transition은 모두2400이다. 같은 초기조건에서 데이터 양만 늘려도FAIL→PASS가 됐고, 파형을 늘린 비교도 개선됐다. 조건·파형·양을 늘릴수록 항상 단조롭게 개선된다는 결과는 아니다.

Joint는 고유baseline을 한 번씩 추가하므로quantity/waveforms의 총fit transition은2800,initials는3600이다. **Probe 수는 같아도baseline 총량까지 동일하지는 않다.** Paired A/B의probe transition은 일치시키고c용baseline 양은 별도로 기록했다. Full에서는 진폭·초기조건·입력 수도 함께 늘어난다.

10/60초에서는Joint small도6/6 통과했다. 30초의small/quantity/waveforms는 집계gate가PASS여도 초기조건별로는3/6이었으며,Full은6/6이었다. Paired+c는 초기 영역에서102probe로 늘려도 전체 기준을 통과하지 못했다. **데이터 수만으로 영역과 식별 목적함수 문제를 해결할 수 있다고 말할 수는 없다.** 전체48개 주 비교는 [REPORT.md](run_01/REPORT.md)에 보존했다.

## 6. Phase C의Nominal FAIL에 대한 판단

- **재현 오류를 주 설명으로 삼을 증거는 없다.** 이전A/B·지표·실제 물리replay가 재현됐다.
- **Absolute 공동LS 자체가 부적절하다고 볼 수 없다.** 같은raw pair에서 초기 영역Joint는 통과했고paired+c는 실패했다.
- **900초 대기만이 성공 조건은 아니다.** 초기 국소 영역에서도 원래24-state로 예측했지만 다른 시각으로 고정 모델을 옮기면 실패했다.
- **데이터 구성·양은 영향을 줬다.** 다만 이전Phase C와 새Full 사이에는 시각 혼합,stream 대 분기,진폭,총량이 함께 다르다. 이전FAIL의 유일한 원인을 하나로 확정하지 않는다.

사전 보조 비교인rcond1e−8 및fixed nominal centering에서도 각Full의 판정은 같았다. Phase C와 같은fitter를 새 분기 자료에 적용해Joint가 통과했으므로, 적어도 이 비교에서cutoff나 회귀 중심만이 성패를 나누지는 않았다. 이전Phase C Nominal 모델은 새test10/30/60/1000초에서도 모두0/6이었다. 원래FAIL은 그대로 보존했다.

새prefix의10–60초와950–1000초에도 공동LS를 적용했지만, 이는 **constant bias로B excitation이 없는** 보조 비교다. B=0으로Direct B 기준을 통과하지 못했다. 이를 이전PRBS를 포함한Phase C stream의 재실험으로 해석하지 않는다.

Fixed nominal centering 보조모델의`update_count`는 재사용한offline fitter의 표본 수 metadata다. 실제 온라인RLS 갱신 횟수가 아니며 이번 연구에서 온라인RLS나새K를 활성화하지 않았다.

현재 답은 **“24-state가Nominal 전역에 충분하다”는 것은 미실증이지만, “충분히 정착한 한 영역에서만 성공할 수 있다”는 설명도 맞지 않았다**는 것이다. 시각별absolute 진행을 포함한 국소 식별과 운용 범위의 별도 검증이 필요하다.

## 7. 한계와 다음 분리 실험

Full의 한 시각은78개×8초=624초분probe와48초분baseline이며, 여러snapshot의offline 분기 자료다. **10초snapshot PASS를 “단일 온라인 데이터10초로 식별했다”고 부르지 않는다.** 실제 필요한 데이터 시간·safe probing cost와 연속rollout에서의 인과적 검증은 남아 있다.

30초Joint Full의 비위치A rho는약 **1.00252**였다. 유한시간p/v 예측PASS는 안정성·DARE·실제 제어PASS가 아니다. 새K를 생성하거나 채택하지 않았다. 이번 실행은 고정bias와 입력 수집이며 원래 위치 복원 제어의 성능 비교도 아니다.

다음에는 RLS 설정을 먼저 바꾸기보다 **같은0.01Nm probing·같은raw stream으로, 시각을 섞는fit과 국소 창fit을 비교하고, 분기 학습과 입력 에너지·총량을 맞추는 실험**이 기존Phase C 실패를 더 분리할 수 있다. c와 내부 상태의absolute 진행 예측 기준도 유지해야 한다. 온라인 추정기에 paired oracle baseline을 주지 않는다.

최초0–10초,FK 보정을 도입한 상태의 재식별,K/bias/reference 실제 제어,다른Target,Sim2Real은 이번 성공 주장이 아니다. Yaw/world XY hold도 없다. Nominal prior는MuJoCo offline calibration을 포함하며Isaac-only source identification으로 해석하지 않는다.

## 8. 변경·검사·재현

신규code5개: `test/nominal_m4_diagnosis.py`, `test/run_nominal_m4_diagnosis.py`, `test/analyze_nominal_m4_diagnosis.py`, `test/test_nominal_m4_diagnosis.py`, `test/audit_nominal_m4_diagnosis.py`. 처음4개는 수집 전source를 동결했다. 마지막은 모델을 변경하지 않고 사전 계획의paired8초 보조 지표와 저장 자료의 완료 감사를 계산하는 추가analyzer다.

독립unit4개PASS: 동일probe 양의profile 및seed 분리, 알려진 비영affine24-state에서 두 방법의 계수/자유 예측,baseline 중복 제거,위치translation 불변성. 이전fitter와의 수치 교차검사·6개 물리replay·48개baseline 재현·raw history/leg 경로·공통 입력 예산은 별도 증거로 기록했다.

전체agent-check는 **FAIL — 기존my_flat_env_cfg.py의trailing whitespace6곳**이었다. Python syntax **448개PASS**,URDF XML **8개PASS**와 구분한다. 최종diff·기존 보호5453파일·source/모델hash는 [completion_audit.json](run_01/completion_audit.json), [agent_check.log](run_01/agent_check.log)에 기록한다. 기존문제는 수정하지 않았다. 브랜치 `agent/codex/dev_tita_gluon`. 기존보고·runtime·policy·설정·RLS·Q/R 변경,commit/push,hardware 없음.

재현은 미사용 출력root에서 수행한다. 기존stage의 자동 재실행은 거부하며ERROR/RUNNING을 무조건 덮어쓰는resume도 없다.

```bash
export MPLCONFIGDIR=/tmp/lqr_mpl OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1
git status --short > /tmp/nominal_m4_identification_status_before.txt
/home/cocel/venvs/cosim_ros2_jazzy/bin/python test/test_nominal_m4_diagnosis.py
/home/cocel/venvs/cosim_ros2_jazzy/bin/python test/run_nominal_m4_diagnosis.py --stage init --root docs/exp/2026-10-16/new_nominal_m4_diagnosis
/home/cocel/venvs/cosim_ros2_jazzy/bin/python test/run_nominal_m4_diagnosis.py --stage legacy --root docs/exp/2026-10-16/new_nominal_m4_diagnosis
/home/cocel/venvs/cosim_ros2_jazzy/bin/python test/run_nominal_m4_diagnosis.py --stage train --root docs/exp/2026-10-16/new_nominal_m4_diagnosis --workers 3
/home/cocel/venvs/cosim_ros2_jazzy/bin/python test/run_nominal_m4_diagnosis.py --stage fit --root docs/exp/2026-10-16/new_nominal_m4_diagnosis
/home/cocel/venvs/cosim_ros2_jazzy/bin/python test/run_nominal_m4_diagnosis.py --stage test --root docs/exp/2026-10-16/new_nominal_m4_diagnosis --workers 3
/home/cocel/venvs/cosim_ros2_jazzy/bin/python test/analyze_nominal_m4_diagnosis.py --root docs/exp/2026-10-16/new_nominal_m4_diagnosis
./scripts/agent-check.sh
```

완료감사analyzer는 이 실행의unit_tests.log/agent_check.log 및 상위SUMMARY/PLAN을 저장한 뒤 실행한다. 재수집의fit·collection에 필요한 과정은 아니다.

```bash
/home/cocel/venvs/cosim_ros2_jazzy/bin/python test/audit_nominal_m4_diagnosis.py --root docs/exp/2026-10-16/nominal_m4_identification_diagnosis/run_01
```

산출물: [동결계획](run_01/plan.json), [이전성공재현](run_01/legacy_results.json), [학습](run_01/train_results.json), [동결64모델](run_01/models_frozen.json), [검증](run_01/test_results.json), [112개비교·초기조건분포](run_01/comparison.json), [paired8초보조지표](run_01/paired_eight_second_metrics.json), [동작영역분포](run_01/operating_regions.json), [전체주비교표](run_01/REPORT.md), [unit검사](run_01/unit_tests.log), [최종diff](task.diff), [완료감사](run_01/completion_audit.json), 전체snapshot/prefix/probe NPZ·source/hash/log.
