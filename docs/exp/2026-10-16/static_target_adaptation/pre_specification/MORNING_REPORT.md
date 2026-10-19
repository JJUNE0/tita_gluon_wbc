# TITA — Static Target-Domain Online Adaptation 진행 보고

작성일: 2026-10-16 (Asia/Seoul)

Execution Domain: **DESKTOP_DRY_RUN** (기존 nominal 재현: **VALIDATION_SIM**)

Policy Checkpoint SHA256: `6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05`

ONNX SHA256: `f44f07ed44970e3ff565eae67fd9229adf0be5c02215591c52a691ffcbb71b2a`

Evidence Status: **PASS — repository audit 및 기존 nominal 두 군 exact 재현. BLOCKED — 지정 상세 specification 파일 누락.** 새 static Target 수집·online identification/adaptation·복합 Target는 NOT_TESTED.

Observed Metrics / Behavior / Log Summary:

## 현재 수행한 일

1. 기존 수정 상태·branch·runtime/정책/관련 source32파일 hash와 tracked diff hash를 저장했다. Production/runtime 및 기존 보고서·모델·archive는 변경하지 않았다.
2. 기존 runner가 nominal startup 뒤에 mismatch를 넣는다는 점을 확인했다. 이번 요구에 맞추려면 첫 physics step 전에 Target을 설치하는 신규 실험 경로가 필요하다. 기존 결과를 static-from-deployment 결과로 재분류하지 않았다.
3. 사용자 메시지에 근거한 계획 초안을 작성하고 **Phase 0 FlashSAC-only Target baseline을 후속 단계보다 앞에 배치**했다.
4. 기존 nominal seed270/pitch0, FlashSAC-only8초 뒤부터의60초 평가를 새 출력으로 재현했다. 두 군 각각23개 배열의 state/observation/action/history/physics-substep torque 등이 기존 archive와 exact 일치했다.

| 기존 nominal 재현 군 | 정상 완료 | 최대 base planar 이동 | 마지막5초 base 속도 RMS |
|---|---:|---:|---:|
| FlashSAC Only | 60초 | 0.9293981 m | 16.337771 mm/s |
| Fixed M4 | 60초 | 0.0224683 m | 0.139917 mm/s |

이 표는 **기존 평가 경로의 재현 검사**다. 새 요구의 startup부터 전체 episode 평가 또는 무작위 Target Phase 0을 수행했다는 뜻이 아니다. 기존 비교 시작점을 새 Target의 최초 목표 위치라고 대신 쓰지 않는다.

## 아직 진행하지 못한 이유

상세 specification으로 지정된 **`TITA_static_domain_adaptation_codex.md`가 현재 repository/제공된 첨부 목록에서 발견되지 않았다.** 사용자에게 로컬 경로 또는 본문을 요청했다. 과거 첨부나 이전 dynamic-shock 계획으로 대체하지 않았다.

사용자 메시지에는 연구 원칙과 순서가 있지만, 상세 파일에 있을 Target sampling 범위/분포·seed·horizon·수치 gate 등을 확인할 수 없다. 이를 임의로 정해 specification을 준수했다고 주장하지 않기 위해 **계획은 DRAFT, immutable manifest는 NOT_FROZEN**으로 남겼다. `execution_lock.json`은 Target 수집/적응의 실행을 BLOCKED로 표시한다. 실험 성능 FAIL을 뜻하는 상태는 아니다.

## 요청한 연구 질문의 현재 답

| 질문 | 상태 |
|---|---|
| 어떤 새 Target에서 온라인 위치 유지에 성공했는가? | NOT_TESTED |
| 적응에 몇 초의 데이터가 필요했는가? | NOT_TESTED |
| Bias/Reference만으로 해결한 환경은 무엇인가? | NOT_TESTED |
| 새로운 Target A/B를 정확히 식별하고 K를 실제 갱신했는가? | NOT_TESTED |
| Full은 Bias+Reference보다 추가 이득이 있는가? | NOT_TESTED |
| 실패한 mass/CoM/lag/friction의 원인은 무엇인가? | 새 실험 NOT_TESTED. 과거의 서로 다른 프로토콜 결과를 이번 결과로 대체하지 않음 |
| 현재 Sim2Real 주장에 필요한 추가 실험은? | Static single/composite Target, 시작부터의 적응·독립 모델 검증·장시간/초기조건 일반화가 선행되어야 함. 실제 하드웨어 실행 없음 |

첨부 확인 후 plan/Target draws/seed/source hash와 gate를 수집 전에 동결하고, Phase 0 → 조건별 safety → shadow/독립 예측 → 조건별 controller 비교 → gate를 통과한 복합 Target 순서로 진행하도록 초안을 구성했다. 한 조건의 실패가 다른 안전한 조건을 중단시키지 않는다.

## 변경·검사

신규 결과 경로의 audit/계획 초안/본 보고서/nominal 재현 증거만 추가했다. 새로운 controller/Target runner는 아직 작성하거나 적용하지 않았다. Branch는 `agent/codex/dev_tita_gluon`; commit/push·hardware/ROS 명령·정책 재학습 없음.

`./scripts/agent-check.sh` 결과와 신규 문서 diff/보호 hash 검사는 `agent_check.log`/`final_review.json`에 기록한다. 저장소 전체 검사는 기존 `my_flat_env_cfg.py` 공백 문제와 이번 작업 결과를 구분한다.

증거: [repository audit](REPOSITORY_AUDIT.md), [계획 초안](EXPERIMENT_PLAN_DRAFT.md), [실행 잠금 상태](execution_lock.json), [audit hash](repository_audit.json), [nominal exact 재현](nominal_replay/archive_verification.json), [재현 로그](nominal_replay.log).
