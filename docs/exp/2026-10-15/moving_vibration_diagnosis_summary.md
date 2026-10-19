# FlashSAC 전후진 떨림 진단

Execution Domain: VALIDATION_SIM (소스/결과 검사: DESKTOP_DRY_RUN)

Policy Checkpoint SHA256: `3fd6113b95be69e0956f1510d4002dd161bc7226e0f1d9ade205117fc3edaed6`

ONNX SHA256: `e9c40d1af7e6a9e54f6336ef684927d3806f1a46ef02c34a91bd1ed732382039`

Evidence Status: PASS — 12회 실행·residual 분리·actor IMU 동기화 효과 확인. SUSPICIOUS — 정책 자체의 안정성/속도 추종 일반화.

Observed Metrics / Behavior / Log Summary:

**후진 중 떨림은 F-1을 꺼도 재현됐고, 같은 정책·PD에서 actor IMU 시점을 현재 joint 상태에 맞추면 크게 줄었다.** 정책 가중치 자체가 주원인이라고 단정할 근거는 없다. 현재 조작 중인 viewer 및 기존 코드는 변경하지 않았다.

## 비교 조건

Nominal 동일 초기 상태, seeds42/43/44, pitch perturbation0, 42초 × 4군 = 12회. 0–2초 정지, 2–14초 +0.2 m/s, 14–22초 정지, 22–34초 −0.2 m/s, 34–42초 정지. 외부 push 없음.

- step_hold: 현재 StopHold residual과 step 명령.
- step_policy: residual을 끄고 기존 actor/PD에 step 명령.
- ramp_policy: residual OFF, 학습 설정과 같은 0.5 m/s² command ramp, 기존 cache IMU.
- ramp_sync: ramp_policy와 같되 actor quaternion/gyro만 현재 qpos/qvel 시점의 가상 IMU로 교체. mj_forward는 clone에서만 수행해 원본 물리 적분을 건드리지 않았다.

정상 전진 구간 6–13초, 정상 후진 구간 26–33초를 분리했다. 모든 정상 구간의 실제 residual은 정확히 0 Nm다. 명령/초기과도 차이가 이전 상태를 바꿀 수 있으므로 step_hold와 step_policy 수치의 작은 차이를 직접적인 residual 효과로 해석하지 않는다.

## 정상 후진 구간: 3 seed 평균

| 군 | Pitch 각속도 RMS rad/s | Leg 관절속도 RMS rad/s | Wheel torque RMS Nm |
|---|---:|---:|---:|
| step_hold | 0.05590 | 0.15109 | 0.46353 |
| step_policy | 0.06032 | 0.16335 | 0.50495 |
| ramp_policy | 0.05833 | 0.15794 | 0.48531 |
| ramp_sync | 0.00500 | 0.01390 | 0.08425 |

같은 ramp 조건에서 actor IMU 동기화 시 pitch 각속도 RMS 91.4%, leg 속도 RMS 91.2%, wheel torque RMS 82.6% 감소했다. 기존 cache의 후진 pitch 스펙트럼에는 약 3.29 Hz peak가 있었다. 동기화군에서는 같은 주기 진동이 크게 줄었다.

전진 정상 구간은 이 초기 조건에서 원래 떨림이 작았다. 이 결과가 사용자 수동 조작의 모든 전진/후진 상태와 긴 조작 이력을 설명한다고 주장하지 않는다. 명령 급변은 과도를 자극할 수 있지만 ramp만으로 정상 후진 떨림이 해결되지는 않았다.

## 해석 및 제한

기존 actor 경로는 mj_step 후의 cached quaternion/gyro와 현재 joint qpos/qvel을 섞어 observation을 구성한다. 이전 D-4 진단에서도 발견한 physics substep 수준의 시점 불일치다. 이번에는 LQR이 아니라 FlashSAC actor 입력에 대해서만 동기화를 비교했고, 정책/PD 가중치를 바꾸지 않고도 떨림이 크게 감소했다. 따라서 현재 증거는 MuJoCo 센서 연동 시점이 후진 진동의 중요한 요인임을 지지한다. Wheel 속도 P, leg PD, 접촉 동역학의 개별 기여는 분리하지 않았다.

Command observation scale [2,2,0.25]는 저장된 학습 env.yaml과 일치했다. ×2 정규화 자체를 중복 스케일 버그로 판단하지 않는다. 정상 전진 실제 속도는 약 +0.504 m/s, 후진은 기존 ramp 약 −0.523 m/s, 동기화군 약 −0.538 m/s였다(명령 ±0.2). 떨림 감소가 velocity tracking 정확도 회복을 뜻하지 않는다. Isaac Lab 학습 환경 재평가와 실기 평가는 NOT_TESTED다.

초기 full/run.log는 metrics 계산의 NumPy mask indexing 오류로 첫 trace 저장 후 중단됐다. 분석 인덱싱을 수정해 재실행한 full_checked만 채택한다. 제어 코드/실험 설정을 결과에 맞춰 튜닝하지 않았다.

기존 GUI/소스/설정은 보존하고 신규 test/debug_flash_moving_vibration.py와 보고서·결과를 추가했다. 기존 변경 보존 및 final diff는 final_review.json/task.diff, agent-check 결과는 agent_check.log에 기록한다.

브랜치: agent/codex/dev_tita_gluon.

[후진 구간 비교 그래프](moving_vibration_diagnosis/backward_vibration.png)

```bash
PYTHONDONTWRITEBYTECODE=1 MPLCONFIGDIR=/tmp/lqr_mpl /home/cocel/venvs/cosim_ros2_jazzy/bin/python test/debug_flash_moving_vibration.py --output docs/exp/2026-10-15/new_moving_vibration/full_checked
```
