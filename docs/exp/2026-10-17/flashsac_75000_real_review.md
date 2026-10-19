# FlashSAC model_75000 종료 로그 보존·실기 분석

Execution Domains: ROBOT_READ_ONLY — 지정된 종료 bag·summary·console 조회와 복사. DESKTOP_DRY_RUN — 원본 hash·DB 무결성·관측/action/PD 재구성. 로봇 명령·정책 변경 없음.

Policy Checkpoint SHA256: `381e846e3ffb1d5a9ed629c02b55c9740ec3c5b089ca443f38b3d73b6abbd730`

ONNX SHA256: `2bd3f78d10bc3b7cc4e50272d0289147f13b0a62ac6730048ba653ae53f35114`

Evidence Status: PASS — 로그 보존·hash·DB·소프트웨어 재구성. FAIL — 사용자 관측상 실기 정지 목표 미충족. SUSPICIOUS — 접촉·명령 혼재에 따른 정책 간 순위. 실제 지면 속도와 물리적 손상 여부는 NOT_TESTED.

Branch: `agent/codex/dev_tita_gluon`

## 로그 보존 확인

대상 `flashsac_75000_152240_341040788_output_true`의 bag(DB3·metadata), summary, console, bag-console 총 5개 파일을 PC의 `docs/exp/2026-10-17/flashsac_75000_real_review/`로 복사했다. 원격 원본 hash와 전부 일치하고 SQLite quick_check가 통과했다. DB message는 **32,285개**다. 원본을 수정하지 않았다.

사용자가 충전을 위해 로봇을 끄기 전에 저장을 우선 요청해, 기존 50000 OFF/ON도 함께 재확인했다. 총 **15개 파일 원본 hash 일치, DB 3개 quick_check PASS**이며 로컬 파일을 fsync했다. 50000 OFF DB 31,426개 message, ON DB 31,031개 message다. [보존 확인 JSON](flashsac_log_save_confirmation.json). 이후 분석은 로봇 연결 없이 가능하다. 로봇 shutdown 명령은 수행하지 않았다.

## 75000 기록에서 확인한 내용

사용자는 이번 시도가 사실상 실패라고 보고했고 손 접촉 여부는 확실하지 않다고 답했다. 접촉 없음으로 가정하지 않았다. `velocity_bias=false`, 추가 offset·diagnostics는 RL 전체에서 0이다. 총 atomic **2,725 frame**, RL **1,004 frame**, 마지막 RL sample **+20.042초**다. 75000 checkpoint·ONNX·config hash는 직전 배포 기록과 일치한다.

정확히 zero-command이고 해당 neutral 진입 후 2초가 지난 구간을 분석했다. RL+12.742–15.342초(131 frame)의 평균 FK 속도는 **−0.3119±0.0383 m/s**, 모든 sample이 음수였다. 평균 pitch −1.881°, 평균 휠당 계산 토크 −0.3832 Nm다. 이는 실제 지면 속도 GT나 외력 없는 구간이 검증된 값은 아니다.

조이스틱 nonzero 구간은 RL+1.942–5.122초, +5.702–10.702초, +15.362–17.422초다. 최대 forward command 1m/s, yaw −1rad/s가 기록됐다. 따라서 전체 20초를 zero-command 자유 drift로 집계할 수 없다. 기존 60000의 순수 drift −0.2025m/s와 정량적인 정책 우열이나 악화율을 단정하지 않는다. 이번 75000 기록에서 후진이 지속된 사실은 사용자 관측과 맞는다.

## 검증과 변경

- **PASS:** 원격·로컬 hash 5개 일치 및 read-only SQLite 검사. [원본 hash](flashsac_75000_real_review/source.sha256), [저장 확인](flashsac_log_save_confirmation.json).
- **PASS:** sequence 연속·monotonic time, RL sensor/policy/output/torque_sent/teacher flag, 1회 RL 전이 검사.
- **PASS:** 실제 75000 ONNX로 RL 1,004개 action 재추론 최대오차 **3.695e−6**. 센서·command·직전 raw action에서 observation 재구성 최대오차 **1.490e−8**. PD torque 재구성 최대오차 **8.882e−16 Nm**.
- OFF 속도는 기록된 IMU·encoder를 사용한 순수 C++ FK observer 재생이며, 계산한 가상 bias를 로봇이나 시뮬에 적용하지 않았다. torque_sent는 transport 접수를 의미하며 실측 적용 토크를 보장하지 않는다.
- 기존 `test/sim2real/analyze_policy_drift_pair.py`에 ON bag을 선택사항으로 처리하고 단일 실행 plot·실제 정책 이름·접촉 미확인 annotation을 지원하도록 작은 변경을 했다. 이 실제 단일 bag 분석을 실행해 검증했다. production controller·설정·배포 변경 없음.
- 필수 agent-check는 [로그](flashsac_75000_real_review/agent_check.log)에 보관한다. 기존 `my_flat_env_cfg.py` 공백 오류는 이 작업과 무관하며 수정하지 않았다. 최종 task diff와 status를 확인했고 commit/push 없음.

[분석 metrics](flashsac_75000_real_review/metrics.json), [실행 로그](flashsac_75000_real_review/analysis.log), [그래프](flashsac_75000_real_review/comparison.png)를 함께 저장했다. 50000의 두 bag은 기존 `flashsac_50000_real_review/`에 그대로 보존돼 있다.
