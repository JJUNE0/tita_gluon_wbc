# FlashSAC / F-1 / G MuJoCo 비교 영상

Execution Domain: VALIDATION_SIM (인코딩·파일 검사: DESKTOP_DRY_RUN)

Policy Checkpoint SHA256: `3fd6113b95be69e0956f1510d4002dd161bc7226e0f1d9ade205117fc3edaed6`

ONNX SHA256: `e9c40d1af7e6a9e54f6336ef684927d3806f1a46ef02c34a91bd1ed732382039`

Evidence Status: PASS — 전체 60초 상태/위치 정확 재현, MuJoCo 렌더링·H.264 인코딩·미디어 형식 확인.

Observed Metrics / Behavior / Log Summary:

기존 online_residual_gain/online_mass의 nominal, seed42, pitch perturbation 0의 A/F-1/G 3개 시행을 재생한다. 기록된 실제 motor torque를 같은 초기 qpos/qvel와 외란 조건의 MuJoCo에 매 physics substep 적용한다. 정책/학습을 새로 실행한 영상이 아니라 저장된 실험의 동역학 재생 영상이다. Actor action·residual·gain은 변경하지 않았다.

위쪽은 세 군에 동일한 고정 카메라, 아래쪽은 동일 확대율의 follow camera이다. 노란 십자는 실제 초기 axle 위치이고 파란 눈금 간격은 1 m다. 화면에 시뮬레이션 시각, 현재/최대 planar drift, G의 기록된 alpha와 centre를 표시한다.

표의 2.272/0.479/0.474 m는 9회 평균이다. 영상은 대표 1회이며 이 시행의 최대 drift는 각각 2.267504/0.479236/0.473514 m다. F-1/G 차이는 약 5.7 mm로 작으므로 자세 영상의 인상만으로 추가 개선을 판단하지 않는다.

렌더링은 원본 physics data를 건드리지 않고 clone에서 수행한다. 렌더링용 조명·카메라와 표시 marker를 추가하고, 기존 평가에서 접촉이 꺼진 world obstacle은 투명하게 처리했다. 원래 scene의 일부 그림자/반사는 남아 있으며 접촉 장애물이 아니다. 접촉·질량·마찰·제어·적분 설정은 유지했다.

원본 소스/설정/보고서는 보존했다. 신규 test/render_residual_mujoco_comparison.py 및 이 영상·검증 기록만 추가했다.

브랜치: agent/codex/dev_tita_gluon. Hardware 실행 없음.

```bash
PYTHONDONTWRITEBYTECODE=1 MUJOCO_GL=egl MPLCONFIGDIR=/tmp/lqr_mpl /home/cocel/venvs/cosim_ros2_jazzy/bin/python test/render_residual_mujoco_comparison.py --output docs/exp/2026-10-15/new_residual_video/full
```

## 완성 영상 및 검증

- [4배속 비교 영상 — 약 15초](residual_mujoco_video/nominal_A_F1_G_4x.mp4)
- [원속도 비교 영상 — 약 60초](residual_mujoco_video/full/nominal_A_F1_G_60s.mp4)
- [마지막 프레임](residual_mujoco_video/full/last_frame.png)

1920×1080, H.264/yuv420p, 25 fps. 원속도 1,501 frames/60.04초이며 첫·마지막 상태를 포함한다. 4배속 파일은 시뮬레이션 시각 표시는 유지하고 재생 시각만 압축했다.

전체 3개 시행의 synchronized/sensor/GT state 및 cached axle position의 원본 최대 오차는 모두 0.0이다(`full/verification.json`). 무작위 초기 조건을 새로 뽑거나 유리한 시행을 탐색하지 않고 seed42/pitch0을 고정했다.

실행 검사: 0.4초 renderer smoke PASS, 60초 3군 torque replay PASS, ffprobe 형식 PASS. 기존 소스 보존/최종 diff와 agent-check 결과는 실험 폴더의 final_review.json 및 agent_check_final.log에 기록한다.

두 MP4 모두 ffmpeg `-xerror` 전체 프레임 decode PASS (exit 0, error log 없음).
