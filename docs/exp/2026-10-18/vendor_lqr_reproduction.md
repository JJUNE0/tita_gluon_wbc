# 회사 LQR 정지 제어기 식별·MuJoCo 재현 — 1차 (데이터 자극 부족 판정)

Execution Domain: `DESKTOP_DRY_RUN`(bag 추출·식별), `VALIDATION_SIM`(MuJoCo 재현 시도). 로봇 접근 없음.

- **대상:** 회사 MCU AUTO_LOCOMOTION 제어기. checkpoint는 없다.
- **입력:** Codex가 복사한 2026-10-18 bag.
  - 정지 60 s
  - 명령 95 s(이 중 mode 3이 78 s)
- **Evidence Status:**
  - **PASS**: 데이터 추출과 재현성. 스크립트로 다시 추출한 npz가 이전과 바이트 단위로 같다.
  - **PASS (부분)**: 법칙 식별 — 아래 1절에 정리했다.
  - **FAIL**: sim 재현. 4개 토크 단위 가설 모두 13 s 안에 넘어졌다.

## 1. 식별 결과

**데이터:**
- ROS `joint_states`(q, dq, firmware effort)와 IMU(quaternion, gyro)를 500 Hz로 썼다. 추출: [`test/sim2real/extract_vendor_ros.py`](../../../test/sim2real/extract_vendor_ros.py).
- ROS IMU는 일관된다. pitch 미분과 gyro y의 상관이 0.93–0.96, 기울기 1.0이다.
- yaw 명령 채널과 mode는 Codex의 CAN 1 kHz 추출본에서 시간으로 맞춰 가져왔다(yaw 채널과 gyro z 상관 0.97).
- **정정 (같은 날):** 처음에는 "CAN 추출본 gyro가 pitch 미분과 상관 0.27이라 정렬 문제가 있다"고 적었다. 이는 **틀렸다.**
  - CAN 추출본의 gyro·pitch는 ROS IMU와 같다. gyro 상관 1.000, 스케일 1.000, 지연 0 ms이고, pitch 차이 RMS는 0.03°다.
  - 낮은 상관은 내 계산 문제였다. CAN 시간축에는 0.1 ms 미만 간격이 703개 있는데, 그 축에서 그대로 미분했다.
  - 1 kHz 균일 격자로 다시 계산하면 상관 0.965, 기울기 0.97이다.
  - 실기 IMU나 Codex 추출에는 문제가 없다.
- 휠 부호는 우리 컨트롤러와 같다(dq 양수가 전진).

**정지 법칙 (firmware N m):**

| 출력 | 식별된 법칙 | 신뢰도 |
|---|---|---|
| 허벅지 평균 | ≈ **55·pitch + 2.3·pitch속도**. 허벅지 각도 항은 거의 없다(−1…+3) | 정지·주행 회복 구간 모두 R² 0.99. 견고하다 |
| 무릎 | 단단한 위치 고정. 정지 중 각도 std 2e-5 rad | 강성은 식별 불가(관절별 fit R² 0.08–0.31). Kp 400으로 가정 |
| hip | 단단한 위치 고정 + ±24 N m 조임 | 왼쪽 Kp 803(R² 0.99). 오른쪽은 미식별이라 800으로 가정 |
| 휠 평균 | pitch·pitch속도·위치·속도 되먹임(위치 유지형 LQR) | 구조는 확인됐다(정지만 쓰면 R² 0.96). 계수는 데이터셋마다 크게 바뀐다(아래) |

**휠 계수가 정해지지 않는 이유:** pitch와 "다리 절대각(pitch + 허벅지)"이 거의 같이 움직인다.
- 정지 데이터: pitch std 0.31°, 허벅지 std 0.003 rad. 실제로 독립적으로 움직인 구간이 없다.
- 계수 변화: 정지만 쓰면 pitch 42·허벅지 38, 주행 후 회복 구간만 쓰면 pitch 6·허벅지 25다. 같은 R² 수준에서 서로 다른 해가 나온다.
- 주행 후 명령 0 구간은 2 s 이상인 것이 2개(3.1 s, 14.1 s)뿐이다.

## 2. MuJoCo 재현 시도

**스크립트:** [`test/sim2real/sim_vendor_stand.py`](../../../test/sim2real/sim_vendor_stand.py).
- 회사 정지 자세에서 시작해 500 Hz로 식별 법칙을 적용했다.
- heading 유지는 식별하지 못해 안정화용 값을 넣었다.

**결과 (토크 단위 가설 4개: 전체 1.0 / 다리 0.65 / 전체 0.65 / 무릎만 0.65):**
- 모두 넘어졌다. 1차에는 0.5 s 만에 넘어졌다(무릎 강성 식별 오류). 무릎·hip 고정을 가정값으로 바꾼 2차에는 13 s에 넘어졌다(허벅지 발산).
- 식별된 휠·허벅지 피드백이 sim 폐루프를 안정화하지 못한다.
- 원인을 sim 오차와 게인 식별 오차로 분리할 수 없다. 따라서 **지금 데이터로는 재현 판정이 불가능**하다.
- 로그: [sim_stand.log](vendor_lqr_reproduction/sim_stand.log), [law](vendor_lqr_reproduction/vendor_stand_law.json).

## 3. 판정과 추가 수집 요청

**센서·로그 품질은 충분하다.** 500 Hz 관절 상태·토크·IMU가 있다. 다만 **정지 데이터에 자극이 부족해** 균형 루프 게인이 유일하게 정해지지 않는다. 회사 컨트롤러로 아래를 추가로 수집한다(같은 capture 절차).

1. **조용한 정지 60 s.** 재현성 확인용이다.
2. **밀기 시험.** 정지 상태에서 몸통을 앞으로 짧고 확실하게 밀기 5회(5–20 cm 밀릴 정도), 뒤로 밀기 5회를 한다. 매번 완전히 멈출 때까지 5 s 이상 기다린다.
   - 이 시험이 pitch, 다리각, 위치, 속도를 서로 다르게 흔들어 게인을 분리한다.
   - 가장 중요하다.
3. **가능하면 높이 명령을 바꾼 정지 2–3개.** 무릎 각도가 다른 평형점이다.
4. **시점 표시.** 밀기 시점을 대략 메모하거나 조이스틱 버튼으로 표시해 두면 좋다. 필수는 아니다.

## 4. 파일

- **신규 스크립트:**
  - `test/sim2real/extract_vendor_ros.py`
  - `test/sim2real/sim_vendor_stand.py`
- **출력:** [`vendor_lqr_reproduction/`](vendor_lqr_reproduction/)
- **`./scripts/agent-check.sh`:** [log](vendor_lqr_reproduction/agent_check.log).

---

## 5. 2차 — 19:27 추가 수집(높이 3단계 × 정지·밀기, 점프, 고속) 평가

Execution Domain:
- `ROBOT_READ_ONLY`: 복사. 88개 파일, 818 MB, SHA256이 일치한다([copy_verification.log](vendor_capture_1927/copy_verification.log)).
- `DESKTOP_DRY_RUN`: 추출과 식별.
- `VALIDATION_SIM`: MuJoCo.

**데이터:**
- [`vendor_capture_1927/`](vendor_capture_1927/)에서 [`extract_vendor_ros.py`](../../../test/sim2real/extract_vendor_ros.py) `--captures`로 500 Hz 정지·밀기 6개를 추출했다.
- jump·high_speed는 추출만 하고 이번 분석에서 제외했다(정지 목적이 아니다).

| 높이 | 무릎 [rad] | 허벅지 | 무릎 토크 [fw N m] | 조용한 정지 pitch | 60 s drift | 밀기 이벤트 |
|---|---|---|---|---|---|---|
| high | −1.545 | 0.800–0.816 | 23.0 | 0.29 ± 0.21° | −4.2 cm | 7회, v 0.6–1.3 m/s, 이동 0.2–0.45 m 후 정지 |
| mid | −2.179 | 1.151–1.160 | 31.0 | 0.36 ± 0.25° | 0.0 cm | 6회, v 0.65–0.92 |
| low | −2.568 | 1.377–1.402 | 33.6 | 0.22 ± 0.26° | 0.0 cm | 8회, v 0.4–1.14 |

### 식별 (밀기 데이터로 fit, 조용한 정지와 다른 높이로 검증) — [log](vendor_lqr_reproduction/push_sim.log)

- **허벅지:** 토크 ≈ **56·pitch + 2.6·pitch속도** (+0.7·허벅지각 + 상수). 세 높이에서 계수가 같다(56.0–56.9 / 2.5–2.7). R²는 밀기 0.99, 조용한 정지 0.92–0.98, 다른 높이 0.99다. **확정.**
- **휠:** pitch·pitch속도·rolling 속도·허벅지각·허벅지속도 항이 높이별로 일관된 크기다(gain scheduling 형태).
  - 계수: pitch 12–20, 속도 2.3–3.0, 허벅지각 7–14.
  - R²: 밀기 0.71–0.80, 조용한 정지 0.52–0.65.
  - **위치 항은 0.05–1.3 N m/m로 약하다.** 1차의 17은 자극 부족에서 나온 허상이었다.
  - 설명되지 않는 약 0.2–0.27 N m 성분은 5 Hz 저역통과 뒤에도 남는다. 회사 내부 상태(추정기 등)로 보인다. leaky 기준이나 측정 지연을 넣어도 개선되지 않는다.
- **위치 유지:** 실기는 밀린 뒤 0.7–1.0 s 안에 멈추고 **원위치로 돌아가지 않는다**(0.2–0.5 m 이동 유지). 회사의 정지 drift 0은 강한 위치 되먹임 때문이 아니다. 균형점이 실기에 맞게 조정돼 있고, 약한 위치 항이 더해진 결과다. 1차 결론(위치 유지형 LQR)을 이렇게 수정한다.

### sim 재현

**[push_sim.log](vendor_lqr_reproduction/push_sim.log):** 식별한 법칙과 무릎·hip 고정 조건으로 돌렸다.
- high·mid는 토크 단위 가설 3개(1.0, 다리 0.65, 무릎 0.65)에서 **선다.** 1차는 넘어졌었다.
- **휠 출력 0.65 가설은 모든 높이에서 넘어진다.** 휠 토크 단위는 약 1이다.
- **무릎 0.65일 때 sim 무릎 각도가 실기와 맞는다**(mid −2.164 vs −2.179, 1.0이면 −2.138). 무릎 단위 약 0.65를 재확인했다.
- **low는 모든 가설에서 넘어진다.** 미해결이다(관절 한계나 높이별 gain 전환 가능성).

**[calibration.log](vendor_lqr_reproduction/calibration.log):** 정적 평형 교정. 실기 drift 0, pitch, 허벅지각을 맞추려면 sim base CoM을 URDF보다 **약 1–2.5 cm 뒤로** 옮겨야 한다. 지표별 최적값은 다음과 같다.

| 지표 | high | mid |
|---|---|---|
| drift 0 | −2.8 cm | −2.3 cm |
| 허벅지각 | −2 cm | −1.8 cm |
| pitch | −1 cm | −1 cm |

- 휠·허벅지 단위는 정적 평형에 거의 영향이 없다.
- **정적 데이터만으로는 CoM 이동과 IMU pitch·관절 영점 1–2° 오프셋을 구분할 수 없다.**

**[push_dynamics.log](vendor_lqr_reproduction/push_dynamics.log):** 밀기 동특성(25 s 시점에 0.1 s 힘). sim은 휠 단위에 따라 1.3–4.5 s에 걸쳐 원위치로 돌아온다. 실기는 0.7–1.0 s에 멈추고 그 자리에 머문다.
- 회사 제어기의 밀린 뒤 위치 기준 재설정 같은 모드 로직은 식별되지 않는다. 손으로 민 힘의 프로파일도 모른다.
- **비교 불가로 판정한다.** 다음 방법은 실기 밀기가 끝난 시점의 상태를 sim 초기 상태로 넣고 이후 자유 응답을 비교하는 것이다.

### RL 학습에 주는 시사점

1. **무릎 출력 약 0.65배**: 세 번째 독립 근거다. 무릎 92/2.3 배포와 학습의 무릎 DR 0.55–1.0은 방향이 맞다.
2. **휠은 보정할 필요가 없다**(단위 약 1).
3. **sim과 실기 사이에 1–2 cm(또는 1–2°)의 정적 오프셋이 있다.**
   - IMU bias DR(±0.05, 약 ±2.9°)은 이미 이를 덮는다.
   - CoM DR(±1.5 cm, URDF 중심)은 −2 cm를 겨우 덮으므로 다음 학습에서 x를 −3…+1.5 cm로 넓히는 것을 검토한다.
   - 위치 오차 관측은 이런 상수 오프셋을 적분으로 상쇄하는 구조라 계속 유효하다.
4. **회사는 밀려도 원위치로 돌아가지 않는다.** 학습 중인 위치 오차 관측은 정지 명령 동안 원위치 복귀를 학습시킨다. 실기 사용감이 다를 수 있다. ±0.3 m clip이 과도한 복귀를 제한한다.

**신규 스크립트:**
- `test/sim2real/sim_vendor_push.py`
- `test/sim2real/calibrate_vendor_stand.py`
- `test/sim2real/compare_vendor_push_dynamics.py`
- `extract_vendor_ros.py`에 `--captures`를 추가했다. 기존 기본 경로의 결과는 같다.
