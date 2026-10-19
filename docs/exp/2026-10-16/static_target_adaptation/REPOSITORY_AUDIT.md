# Static Target-Domain Adaptation — repository audit

작성일: 2026-10-16 (Asia/Seoul)

Execution Domain: **DESKTOP_DRY_RUN** (기존 nominal 재현: **VALIDATION_SIM**)

Policy Checkpoint SHA256: `6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05`

ONNX SHA256: `f44f07ed44970e3ff565eae67fd9229adf0be5c02215591c52a691ffcbb71b2a`

Evidence Status: **PASS — source/data-flow audit. BLOCKED — 지정한 상세 specification 첨부 누락.** Target 무작위 수집·적응 성능은 NOT_TESTED.

Observed Metrics / Behavior / Log Summary:

현재 branch는 `agent/codex/dev_tita_gluon`이며 시작 시점에 다수의 기존 수정/삭제/untracked 파일이 있었다. 전체 상태를 `status_before.txt`, 기존 runtime·관련 실험 소스·checkpoint 파일의 hash와 tracked diff hash를 `repository_audit.json`에 저장했다. 기존 파일을 수정하거나 되돌리지 않았다.

## 재사용 가능한 경로

`Playback`은 `TitaMujocoEnv` → observation builder / ActionAdapter → frozen ONNX를 구성한다. 실험 Runner는 현재 qpos/qvel을 별도 mjData에 복제하고 mj_forward해 actor와 계측의 IMU를 동기화한다. 정책 observation33개, raw previous action8개, native wheel velocity PD / leg position PD 경로와 physics substep torque archive를 재사용할 수 있다. M4는 p/v/pitch/rate/previous_action8/leg_q6/leg_dq6의24상태이며 yaw 상태를 추가하지 않는다.

`EffectRunner`는 wheel 합산 command 뒤 gain/lag를 physics dt에서 적용한다. 기존 `apply_physics_effect`는 질량·관성 및 floor/wheel 마찰을 바꾸지만, **Runner 생성 이후에 호출**된다. Runner 생성자는 이미 nominal transform_up의 physics step을 실행한다. 따라서 기존 mismatch/snapshot 실험을 이번의 static-from-start 배포 실험으로 간주할 수 없다.

신규 Target runner는 환경 construction 단계에서 **첫 mj_step 전에** 모델의 mass/inertia/CoM/friction을 적용하고 motor gain/lag wrapper를 설치해야 한다. 이후 episode 전체에서 물성 hash를 검사해야 한다. 보존된 nominal snapshot에 뒤늦게 물성을 덮어써서 이번 Target episode의 초기 상태라고 부르지 않는다. Production runtime에는 hook을 추가하지 않고 `test/` 내부에서만 구현하는 방향이다.

## 식별과 gate의 분리

기존 constrained RLS는 위치 translation의 A 첫 열과 previous_action의 B8행=0을 보존한다. 그러나 raw RLS update가 곧 독립 검증된 active A/B/c가 되는 것은 아니다. 새 실험에서는 shadow 후보와 active validated model을 별도로 보존하고, 검증한 동일 snapshot의 모델에서만 K를 생성해야 한다. 기존 B2의 최근 검증 플래그/최신 raw 행렬 사용 근사는 active 경로로 가져오지 않고 shadow로 제한해야 한다.

현재 nominal M4 viewer의 headless exact 검사를 별도 `nominal_replay/`에 실행한다. 이는 기존 두 군의 재현 검사이며, 무작위 Target Phase 0을 수행했다는 뜻이 아니다.

## 누락된 입력

사용자가 지정한 `TITA_static_domain_adaptation_codex.md`를 repository, 숨김 파일을 포함한 `/home/cocel/.codex/attachments`, `/mnt/data`, Downloads 및 `/tmp`에서 찾지 못했다. 현재 첨부 목록의 과거 pasted-text들은 다른 실험 요청이다. 이를 새 상세 specification으로 대체하지 않았다.

본문의 연구 범위로 계획 초안을 작성할 수 있지만, 상세 파일에 있을 Target 분포/범위·seed·horizon·phase 구분·정량 gate를 읽었다고 주장할 수 없다. 따라서 `execution_lock.json`에 **immutable plan 미동결 / Target 수집과 adaptation NOT_TESTED**를 명시하고 파일 경로 또는 본문을 요청했다.

Hardware/ROS 명령·정책 재학습·production 수정·commit/push 없음. 저장소 검사와 최종 diff는 `agent_check.log`, `final_review.json`에 기록한다.
