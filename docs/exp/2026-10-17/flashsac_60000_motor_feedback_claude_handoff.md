# Claude 전달용 — 실기 motor feedback을 반영한 재학습 준비

- Execution Domain: `DESKTOP_DRY_RUN` (분석 인수인계; 아래 TRAINING_SIM/VALIDATION_SIM 작업은 아직 실행 안 함).
- Evidence Status: 실기 로그 분석 **PASS**; 실제 Nm 교정·새 정책 학습/검증 **NOT_TESTED**.
- Policy: `tita_flash_sac_115632_883848/model_60000`.
- Checkpoint SHA256: `6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05`.
- ONNX SHA256: `f44f07ed44970e3ff565eae67fd9229adf0be5c02215591c52a691ffcbb71b2a`.

아래를 같은 repository를 사용하는 Claude에게 전달하면 된다.

---

`docs/exp/2026-10-17/flashsac_60000_motor_feedback_report.md`를 먼저 읽고, 실기 gap을 반영한 재학습 설정과 검증 계획을 준비해 줘. AGENTS.md를 따르고 하드웨어 배포·실행은 별도 승인 없이 하지 마.

최신 실제 run은 `flashsac_60000_174421_440893411_output_true`다. 손 접촉 없고, 사람이 조이스틱으로 정지 유지 시도. Velocity bias OFF, RL 32.2초. 전체를 zero-command로 취급하면 안 된다.

핵심 새 증거:

- 명령 토크와 실제 firmware-reported torque를 같은 sample ID로 기록했다. Feedback은 현재 inference/송신 전에 읽으므로 **`previous_computed_torque`와 비교**한다.
- RL 초기 3초 제외 1,460 frame에서 큰 부하 hip/무릎 4개 축 reported/command gain은 0.9989–0.9993, 차이 RMS 0.085–0.126 Nm. 안정 명령 필터에서도 약 1.0이다.
- 기존 `leg_gain=0.60`은 실제 torque 출력 부족을 측정한 값이 아니라 MuJoCo 등가 식별 계수다. Firmware feedback은 실제 Nm 교정값도 아니므로 0.6을 물리 상수로 확정하거나 반대로 실제 gain=1이라고 확정하지 마.
- RL+7.710–9.250초는 중립 1초 경과 후 구간이고 FK 속도 평균 −0.207 m/s, 무릎 −2.112/−2.121 rad, 명령 무릎 토크 +27.85/+26.89 Nm다. 다음 짧은 중립 구간과 섞어서 개선율을 계산하지 마. 외부 ground-truth 속도는 없다.
- RL+5–10초 전체는 평균 command_x=+0.168 m/s이므로 기존 free-drift fitting 창으로 재사용하면 안 된다.
- 첫 RL 과도에서 오른 휠 보고값 −12.95 Nm가 관찰됐다. 정상 정지 보정값으로 취급하지 말고 startup 별도 평가가 필요하다.

사용할 파일:

```text
docs/exp/2026-10-17/flashsac_60000_motor_feedback_report.md
docs/exp/2026-10-17/flashsac_60000_174421_torque_review/metrics.json
docs/exp/2026-10-17/flashsac_60000_174421_torque_review/signals.npz
docs/exp/2026-10-17/flashsac_60000_174421_torque_review/joint_torque_metrics.csv
docs/exp/2026-10-17/flashsac_60000_174421_torque_review/lag_sensitivity.csv
docs/exp/2026-10-17/flashsac_60000_174421_torque_review/inputs.sha256
docs/exp/2026-10-17/real2sim_leg_wheel_grid.md
test/real2sim_leg_wheel_grid.py
lab/ddt_lab/ddt_lab/tasks/manager_based/locomotion/robots/tita/my_flat_env_cfg.py
```

요청 작업:

1. 실제 학습 당시 checkpoint metadata와 현재 환경 설정 차이를 먼저 확인해. Export gains/관측·action 순서/PD·clip/startup parity를 보존해.
2. 기존 real2sim 0.6 후보와 nominal 1.0을 모두 남기고, actuator gain·마찰·관성/CoM·센서 오프셋의 구분 가능한 것과 아닌 것을 명시해. 강건성용 DR 범위를 실측 범위라고 쓰지 마. Kp/Kd scaling과 output torque scaling, friction 단위/적용 위치는 로컬 simulator 구현에서 확인해.
3. 원래 자유 drift run을 fitting에 썼다면 이번 command sequence를 holdout으로 사용해. 인접 frame 무작위 split은 하지 마. 이번 run에서 fitting하면 별도 run을 검증으로 확보해.
4. 성공한 조이스틱 command를 지우고 command=0 teacher로 바로 BC하지 마. 원래 관측에 command와 previous action이 포함된다. 우선 일치시킨 simulator에서 zero-command 안정성과 command 추종을 함께 재학습/비교하는 설계를 제시해.
5. nominal 및 기존 A/B/C mismatch에서 startup·zero-command drift·전후진·회전·pitch/torque RMS/peak를 분리 평가해. 학습 설정, 기준 모델, 명령/상태 초기 조건과 합격 기준을 기록해.

현재 증거로 ‘모터 고장’, ‘실제 40% 출력 부족’, ‘새 정책은 실기 정지 성공’을 주장하지 마. 전체 보고서의 한계와 원본 SHA256을 보존해.
