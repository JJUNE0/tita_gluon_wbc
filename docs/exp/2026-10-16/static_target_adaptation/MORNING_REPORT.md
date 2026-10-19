# TITA FlashSAC — Static Target-Domain Adaptation

작성일: 2026-10-16 (Asia/Seoul)

Execution Domain: **VALIDATION_SIM** (감사/분석: **DESKTOP_DRY_RUN**)

Policy Checkpoint SHA256: `6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05`

Evidence Status: **FAIL — Full Joint 적응 및 절대 위치 유지 입증. NOT_TESTED — 새 Target K 활성 성능 비교.** 수집/흐름 완료와 연구 성능을 구분한다.

Observed Metrics / Behavior / Log Summary:

[전체 MORNING_REPORT](run_05/MORNING_REPORT.md)에 최종 판정·조건별 수치·실패/미실험 이유·다음 과제를 기록했다.

- Phase0 FlashSAC-only33회부터 순차 수행했다. 전체525개 제어 trial 중516개 정상 완료,50ms lag9개 guard 실패다. 안전 gate를 통과한6개 단일·2개 복합 환경의180초384개 비교는 모두 정상 완료했다.
- Bias+Reference(E6)는 gain0.90435/friction0.57698 복합 조건에서 Fixed 대비 full IAE10.5% 감소,6/6 paired 개선으로 상대 기준PASS였다. 그러나 종료 base 위치오차 중앙값74.75mm로 절대 유지FAIL이다. 모든8개 환경에서 E6의 절대 유지0/6이다.
- 새 Target K 채택0회. E6/E7의48쌍은 전체NPZ가exact 일치했다. Full Joint Dynamics/K 적응의 효과는 입증하지 못했으며, 새 K 활성 비교는 admission 미충족으로NOT_TESTED다.
- 실제 독립 입력 검증을 허용한33개 종료 상태에서 full RLS와 A고정B/c 모두 예측FAIL이었다. 다른231개 온라인 종료 상태의 모델 검증은 포화 등으로NOT_TESTED다. Direct B와 다중step 및c를 포함한absolute baseline 진단을 별도 보존했다.
- 초기 encoder/IMU 경로와 base-link 경로의 수cm 차이도 확인했다. 목표를 다시 잡거나 GT로 센서를 보정하지 않았다.
- 새 검사12개+기존RLS검사2개PASS, 별도affine 수치검사PASS,264개 온라인episode의 과거sensor/명령 인과성 재생PASS. 전체agent-check는 기존my_flat_env_cfg.py trailing whitespace6곳으로FAIL이다.

[동결 계획](run_05/plan.json), [전체 단계 상태](run_05/pipeline_state.json), [trial CSV](run_05/metrics.csv), [독립 모델 검증](run_05/independent_model_checks.json), [완료 감사](run_05/completion_audit.json), [변경 diff](task.diff)를 확인한다.

기존 명세 확보 전 기록은 [pre_specification](pre_specification/MORNING_REPORT.md)에 보존했다. run_01–04 예비 자료를 주 통계에 합산하지 않는다. run_04의 완료 Phase0/Safety/Shadow를 동결source/함수AST/453개hash로 감사해 재사용한 경위는 [recovery.json](run_05/recovery.json)에 기록했다.

Prior는 nominal MuJoCo offline calibration이다. Isaac-only 식별/Sim2Real 성공 주장이 아니다. production/runtime·정책·기존 실험을 변경하지 않았고 hardware/ROS 배포·재학습·commit/push 없음. 브랜치 `agent/codex/dev_tita_gluon`.
