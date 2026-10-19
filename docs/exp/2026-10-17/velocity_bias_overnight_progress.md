최종 통합 보고서: [velocity_bias_overnight_summary.md](/home/cocel/Desktop/Research/tita_gluon_wbc/docs/exp/2026-10-17/velocity_bias_overnight_summary.md)

아래는 진행 중 기록이며, 현재 CLI 기본 후보는 v04 velocity-seeded integral이다. 구현/시뮬레이션 검증 완료, 일부 확장 조건의 품질 기준 미달과 실기 미검증은 최종 보고서에 명시했다.

# 속도 기반 wheel bias 검증 진행 기록

Execution Domain: VALIDATION_SIM / DESKTOP_DRY_RUN

Policy Checkpoint SHA256 (reference model_60000): 6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05

Evidence Status: NOT_TESTED (최종 후보 전체 평가 진행 중)

실험은 10월 16일에 시작했고 연속 실행 로그·40개 checkpoint hash·각 실행 결과·실패 기록·소스 snapshot은 ../2026-10-16/velocity_bias_overnight/에 묶어 기록한다. 실기에는 배포하지 않았으며 최신 실기 bag은 로컬에서 읽기 전용으로만 분석했다.

기존 속도 PI 후보는 명목 조건의 40개 checkpoint에서 60초와 300초 평가의 물리적 속도/위치 기준을 통과했다. 같은 model_60000에서 질량 증가로 drift가 뒤쪽으로 바뀌는 상황도 재현했다. 고정 M4 대비 양방향 velocity bias가 drift를 줄였으나 일부 다른 checkpoint/물리 조건에서 진동 기준 미달이 남아 있다.

현재는 초기 속도에 비례한 bias seed + 느린 적분 보정 후보를 검증한다. 최신 후보는 kp0, ki4, seed_gain3, tau0.1s, ramp0.25s, bias±2m/s, slew3m/s²다. 실제 실행 경로의 명목 checkpoint40개와 추가 screening을 통과했고, 전체 물리 조건/외란/장기 평가가 진행 중이다. CLI 기본값은 최종 검토까지 이전 후보로 유지한다.

관측시각을 중복 갱신하던 가상 impulse 평가기의 문제는 수정하고 기존 결과를 보존했다. 해당 외란 결과의 해석은 impulse_observer_errata.md를 따른다. 최신 controller/math/ROS 통합 테스트는 11개 PASS. PD/M4의 토크 slew는 기존 2Nm/s를 유지하고 새 mode의 속도 slew를 별도로 지정하도록 작은 hook을 추가했으며 회귀 검증 중이다.

전체 agent-check는 기존 my_flat_env_cfg.py의 여섯 trailing-whitespace 때문에 FAIL이고, 해당 사용자 변경은 수정하지 않았다. 최종 결과가 나오면 이 날짜 폴더에 통합 요약을 남긴다.

Branch: agent/codex/dev_tita_gluon
