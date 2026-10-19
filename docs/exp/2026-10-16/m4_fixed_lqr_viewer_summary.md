# model_60000 — Fixed M4 Residual LQR MuJoCo viewer

작성일: 2026-10-16 (Asia/Seoul)

Execution Domain: **VALIDATION_SIM** (화면 접근·소스/diff 검사: **DESKTOP_DRY_RUN**)

Policy Checkpoint SHA256: `6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05`

ONNX SHA256: `f44f07ed44970e3ff565eae67fd9229adf0be5c02215591c52a691ffcbb71b2a`

Evidence Status: **PASS — M4/A 각각 60초 기존 archive exact 재현 및 MuJoCo viewer 실행.** 추가 일반화·조작 명령·실기는 NOT_TESTED.

Observed Metrics / Behavior / Log Summary:

사용자가 요청한 Fixed Residual LQR을 GUI로 실행했다. 신규 `test/play_m4_fixed_lqr.py`는 기존 `rollout_control`과 동결된 `flash_overnight_pipeline/run_final/gains_frozen.json`의 M4를 그대로 사용한다. 새 제어식이나 gain을 만들지 않았다. Fixed M4 gain과 reference, 합 bias +0.4828 Nm, 추가 보정 ±0.05 Nm, 1.5초 ramp, 2 Nm/s slew, 기존 wheel/leg PD 및 동기화 IMU 경로다. RLS/Bias/Reference의 online update는 없다.

Seed270/pitch0에서 기존 transform_up→RL과 FlashSAC-only 8초 prefix를 진행한 상태를 복제한다. 그 상태에서 60초 nominal zero-command 평가를 보며, 종료 뒤 화면을 유지한다. 초기 drift 상태는 국소 학습 범위 밖이므로 이 한 조건의 결과를 일반적인 정지 성능으로 해석하지 않는다. Yaw hold나 속도 명령 조종은 이번 viewer 범위가 아니다.

| 군 | 정상 완료 | 최대 base planar 이동 | 마지막 5초 base 속도 RMS |
|---|---:|---:|---:|
| Fixed M4 LQR | 60초 | 0.0224683 m | 0.139917 mm/s |
| FlashSAC only | 60초 | 0.9293981 m | 16.337771 mm/s |

위 값은 GUI 전 headless 검사다. 두 군 모두 state·observation/action/history·motor substeps 등을 포함한 23개 배열이 기존 archive와 exact 일치했다. 화면에서 사용자 마우스 perturbation을 가한 뒤의 궤적까지 archive와 일치한다고 주장하지 않는다. 카메라는 초기 위치를 바라보며 실제 이동을 관찰할 수 있다.

- `B`: FlashSAC-only / Fixed M4를 전환하고 같은 snapshot에서 재시작.
- `R`: 현재 군으로 같은 snapshot부터 재시작.
- `Space`: 일시정지/재개.
- `Q` 또는 창 닫기: 종료. 60초가 끝나면 정지 화면에서 `R`/`B`로 다시 실행한다.

```bash
MPLCONFIGDIR=/tmp/lqr_mpl OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 /home/cocel/venvs/cosim_ros2_jazzy/bin/python test/play_m4_fixed_lqr.py
# 화면 없이 기존 두 군의 archive와 비교:
MPLCONFIGDIR=/tmp/lqr_mpl OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 /home/cocel/venvs/cosim_ros2_jazzy/bin/python test/play_m4_fixed_lqr.py --headless
```

기존 runtime·정책·gain·실험 자료는 수정하지 않았다. 신규 viewer script, 본 기록, `m4_fixed_lqr_viewer/` 증거만 추가했다. 창 연결은 desktop X11 접근을 허용한 실행에서 확인했고 로그에 `VIEWER_RUNNING`을 기록했다. Hardware/ROS 명령·commit/push 없음. 브랜치 `agent/codex/dev_tita_gluon`.

`./scripts/agent-check.sh`는 **전체 FAIL**이다. 기존 `my_flat_env_cfg.py`의 trailing whitespace6곳이 원인이며 수정하지 않았다. Python syntax **431개 PASS**, URDF **8개 PASS**, 실험 경로·존재 검사 PASS다. 신규 script/보고서의 diff 검사와 기존 status 보존 검사도 PASS이며 `final_review.json`/`task.diff`에 기록했다.

산출물: [archive exact 검사](m4_fixed_lqr_viewer/archive_verification.json), [headless 로그](m4_fixed_lqr_viewer/preflight.log), [viewer 로그](m4_fixed_lqr_viewer/viewer.log), [저장소 검사](m4_fixed_lqr_viewer/agent_check.log), [diff 감사](m4_fixed_lqr_viewer/final_review.json). GUI에서 60초를 완료한 episode는 실행 중 `viewer_results.json`에 기록한다.
