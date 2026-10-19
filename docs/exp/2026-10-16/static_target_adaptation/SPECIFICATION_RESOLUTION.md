# Static Target specification 확보 및 실행 경로

작성일: 2026-10-16 (Asia/Seoul)

Execution Domain: **DESKTOP_DRY_RUN** (본 실행: **VALIDATION_SIM**)

Policy Checkpoint SHA256: `6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05`

Evidence Status: **PASS — 상세 본문 및 온라인 검증 방식의 사용자 답변 확보.** 실험 성능 판정은 실행 결과에 따른다.

사용자가 `TITA_static_domain_adaptation_codex.md`에 해당하는 전체 상세 specification을 후속 답변의 본문으로 제공했다. 이 폴더의 최초 audit/초안/MORNING_REPORT와 execution_lock은 **본문 확보 전 기록**으로 보존한다. 현재 실행의 동결 계획과 결과는 **`run_05/`**다.

온라인 단일 rollout에는 같은 상태를 복제한 ±토크 Direct B 측정이 존재하지 않는다는 점을 설명하고 검증 방식을 질문했다. 사용자는 **“온라인은 후속 센서 검증, Direct B는 offline 검증”**을 선택했다. 온라인 K gate는 정확히 동결한 모델의 후속4초 센서 구간에서0.1/0.5/1/2초 자유 예측과 조건부 B 회귀·정보량·DARE·안정성·입력 변화 검사를 사용한다. 같은 상태의 Direct B 및 별도 입력 응답 검증은 offline harness에서 수행하며 그 결과/GT를 online estimator에 전달하지 않는다. 조건부 B와 물리 분기 Direct B를 같은 측정이라고 부르지 않는다.

사용자 답변 전에 동결한 `run_01/`은 새 K를 허용하지 않는 보수적 설정이었다. Phase 0 도중 사용자 답변을 반영하기 위해 중단했고 tool에서 **exit130**을 확인했다. 원래 source·plan·부분 baseline과 interruption 기록을 보존한다. 성능 threshold, Target값, seed, horizon은 바꾸지 않았다. 승인한 검증 프로토콜을 `run_02/plan.json`에 새로 동결하고 **Phase 0부터 전부 재수집**한다. 이전 부분 baseline을 주 통계에 합산하거나 재사용하지 않는다.

입력 감사에서 `run_02`의 Bias-only가 이전 요청값 대신 clipping된 전달값을 slew state로 사용한 오류를 발견했다. 특히50ms lag의 software 포화에서 요청값 점프0.4428Nm가 발생해 소스/자료/FAIL 기록을 보존하고 exit130으로 중단했다. Bias-only limiter의 state만 수정했다. `run_03`도 offline 검증 시작 입력을 바꿀 때의 slew bridge 및 최근 포화에서 probing 중단을 명시하기 위해 중단했다. 모든 중단은 tool에서exit130을 확인했고, 각 root에 interruption 기록을 보존한다. `run_04`는 입력 감사 회귀 검사를 포함한12개 검사PASS 후 새 계획을 동결했다. Target값·seed·horizon·Q/R·과학적 PASS threshold는 동일하며 Phase0부터 전부 재수집한다. 예비 root의 결과를 주 통계에 합산하지 않는다.

단일 Target는 nominal, motor gain0.8/1.2, mass+inertia1.15/1.30, contact friction0.2/0.8, lag0.02/0.05초, base CoM±0.005m의11종이다. Pilot3개 시작조건(seed600/601/602와 pitch−0.035/0/+0.035), held-out6개 시작조건(seed610/611×동일pitch범위)을 등록했다. 복합4조건의 값은 RNG160610에서 고정한 미관측 보간값이며 prerequisite와 함께 manifest에 보존했다. 이 전체 draw/seed·source hash·판정 기준을 본 실행 전에 동결했다.

전체 배포180초를 calibration60초 및 후속120초로 나누며 최초 목표를 reset하지 않는다. 절대 유지의 진단 기준은 정상 완료, 최대planar0.05m, 종료sagittal0.01m, 마지막5초속도RMS0.2mm/s다. 상대 method 비교는 full-episode base IAE 중앙값10% 이상 감소와6쌍 중4쌍 이상 개선이다. 이는 사용자가 제안한 공학적 목표를 실행 전 채택한 기준이며 실제 TITA 사양/무한시간 안정성 증명이 아니다. 실패한 짧은 실행의 observed IAE를 완료한180초 IAE보다 좋게 순위 매기지 않는다.

Nominal prior는 과거 nominal **MuJoCo** calibration에서 식별한 M4 A/B/c/K/reference다. Frozen actor가 Isaac Lab에서 학습됐다는 것과 prior의 출처를 구분한다. 이번 결과를 Isaac-only dynamics identification 또는 Sim2Real 성공으로 제시하지 않는다. 실제 하드웨어/ROS 명령·정책 재학습·Q/R 탐색 없음.

현재 증거: [새 동결 계획](run_05/plan.json), [계획 SHA256](run_05/plan.sha256), [Target/seed manifest](run_05/domain_manifest.json), [진행 로그](run_05/run.log), [단계 상태](run_05/pipeline_state.json), [이전 중단1](run_01/interruption.json), [입력 감사 중단2](run_02/interruption.json), [검증 입력 전환 중단3](run_03/interruption.json).

`run_04`는 Phase0/Safety/Shadow 수집을 완료한 뒤 저장소 전체 tracked diff 검사에서 중단됐다. 동결한 실행 source·정책·모델·설정 hash는 모두 동일했고 별도 학습 설정 파일의 외부 변경을 관측했다. 기존 변경은 보존했다. `run_05`는 보호된 실행 입력 hash 검사를 유지하면서 관련 없는 tracked 변경을 SUSPICIOUS로 기록하도록 `verify()`만 바꿨다. 모든 simulation/learner/scoring 함수 AST·과학 기준이 같고 완료 자료453파일의 복사 hash가 같음을 [복구 감사](run_05/recovery.json)에 기록했다. 같은 자료를 중복 표본으로 합산하지 않는다. 이후180초 held-out 및 조건부 복합 시험은 run_05에서 수행한다.
