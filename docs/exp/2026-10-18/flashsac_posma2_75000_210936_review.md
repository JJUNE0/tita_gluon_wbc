# flashsac_posma2_75000 실기 run 210936 — 50k와 비교

- Execution Domain: DESKTOP_DRY_RUN (복사한 ROBOT_STATE_CHANGING run 로그의 오프라인 분석. 로봇 명령 없음)
- Run: `flashsac_posma2_75000_210936_110894260_output_true` (2026-10-18 21:09:36, MA2 legs, velocity bias OFF, RL 55.1 s → 오른쪽 버튼 software stop)
- Policy checkpoint SHA256: `9c22f34e0e3b9d7840f29250c214452bb84cadde6037d277d90df55221e84150`
- 원본 SHA256: `flashsac_posma2_75000_210936_review/remote.sha256`, `copy_verification.log` (5개 파일 OK)
- Evidence Status:
  - 정지 heading 유지: **SUSPICIOUS** (+0.15–0.53 °/s, 50k의 1/5–1/9)
  - 정지 x 유지: SUSPICIOUS (래치 후 −0.10 → −0.18 m, clip 포화 없음)
  - 운영자 평가: "꽤 괜찮음"

## 정지 구간 비교 (진입 1 s 이후)

| | 50k (202450) | 75k (210936) |
|---|---|---|
| yaw rate | +4.6 / +2.5 °/s | **+0.53 / +0.15 °/s** |
| yaw 변화 (IMU quat) | +76° / 16.6 s, +59° / 23.7 s | +14° / 26.8 s, +2° / 14.7 s |
| x_err 관측 | −0.10 → −0.27, −0.19 → −0.30 (clip) | −0.10 → −0.18, −0.14 → −0.14 |
| knee L / R, L−R | −93.1 / −88.4°, −4.68° | −100.0 / −99.0°, **−1.03°** |
| 무릎 처짐 L / R | 17.7 / 14.3° | 17.4 / 15.8° |
| thigh L−R | −1.58° | −0.15° |
| knee 계산 토크 L / R | 28.4 / 22.9 Nm | 28.0 / 25.3 Nm |
| pitch / roll 평균 | +1.85° / −0.34° | **+4.86°** / −0.32° |
| 우−좌 휠 목표 / 토크 차 | +1.27 rad/s / +0.33–0.40 Nm | +0.06–0.45 rad/s / +0.02–0.18 Nm |
| 진동 | 25 Hz 없음 | 다리 15–25 Hz 작음. 허벅지 8–15 Hz 파워가 50k의 약 6배 |

- yaw 명령 중 평균 오차는 +2.2 °/s다(50k +4.3).
- `x_err` parity는 최대 6e-9 m다(C++ 관측 정상).
- 해석:
  - 75k는 무릎을 더 굽힌 자세(−100°)에서 좌우 무릎 차이가 작다. 실기 왼쪽 약화가 휠 차동으로 덜 번진다.
  - 점 접촉 sim(`flashsac_posma2_50000_202450_review.md` 7절)에서도 75k의 yaw가 가장 작았다. 그 순위와 일치한다.
  - 대가로 pitch가 4.9°로 높다.

## 산출물

`flashsac_posma2_75000_210936_review/`: 원본 로그, `yaw_drift.json/.npz`, `yaw_drift_console.log`. 분석기 `test/sim2real/analyze_posma2_yaw_drift.py --config …/flashsac_posma2_75000/config.json`.
