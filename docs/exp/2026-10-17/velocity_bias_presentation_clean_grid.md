# 발표 영상: 영어 환경 자막과 전체 화면 2×4 배치

Execution Domain: VALIDATION_SIM

Evidence Status: PASS — 기록/원본 일치, 환경 자막 대조, 인코딩 영상 검증 완료. 저장소 전체 검사는 agent-check 로그 참조.

Policy Checkpoint SHA256: `6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05`

ONNX SHA256: `f44f07ed44970e3ff565eae67fd9229adf0be5c02215591c52a691ffcbb71b2a`

Branch: `agent/codex/dev_tita_gluon`

상단 흰 배경·한글 제목·환경 헤더와 하단 흰 설명 영역, 제어기 색상 띠를 제거했다. 1920×1080 전체를 480×540 크기의 8개 영상으로 채우고 칸 사이에는 얇은 검정 간격만 남겼다. 각 칸 오른쪽 위에는 흰 글씨로 다음 조건을 표시한다.

| 열 | 첫 줄 | 둘째 줄 |
|---|---|---|
| 1 | NOMINAL | 없음 |
| 2 | LOW FRICTION | Sliding μ = 0.2 |
| 3 | CoM +5 mm | Mass ×1.15 |
| 4 | CoM −5 mm | Mass ×1.15 |

`test/static_target_domain.py`는 floor/wheel의 `geom_friction[..., 0]`을 0.2로 설정한다. MuJoCo 로컬 헤더 `mjspec.h`의 friction 첫 항목은 slide다. 따라서 static friction만 따로 바꾼 조건이라는 표현 대신 **sliding friction 계수**를 표시했다. 질량/관성 ×1.15와 CoM 이동은 마지막 두 열에만 적용한 원본 조건이다. 각 영어 자막의 target 딕셔너리가 기록된 plan과 같은지 검사한다.

각 칸 아래 오른쪽에는 굵은 **검정색 `x10`**을 넣고 어두운 바닥에서도 읽히도록 얇은 밝은 테두리를 추가했다. 배경 상자는 없다. 왼쪽 위에는 제어기 이름과 `SIM` 시간을 흰색으로 표시해 위 FlashSAC/아래 FlashSAC + Velocity Bias 구분과 시뮬레이션 시간 동기화를 유지했다. 오른쪽의 기존 `Distance from start` 및 현재 거리, 왼쪽 아래의 고정 월드 영상도 유지한다. Peak는 없다.

헤더를 없애면서 커진 영상 높이에 비례해 메인 카메라 거리를 2.05→2.747 m로 조정하여 승인된 로봇의 화면상 크기를 유지했다. 모든 칸의 base_link 기준 공통 카메라 offset, 같은 열 위·아래의 동일한 고정 월드 카메라, 중앙 시작점, 실제 경로는 동일하다. 새로운 물리 실험·정책 실행은 없다.

## 산출물과 실제 검사

- [최종 MP4](velocity_bias_presentation_clean_grid/flashsac_velocity_bias_2x4_10x_presentation.mp4): 1920×1080, H.264/yuv420p, 30 fps, 901 frames, **30.033333초**, 14,325,657 bytes.
- [중간 화면](velocity_bias_presentation_clean_grid/encoded_15s.png), [최종 화면](velocity_bias_presentation_clean_grid/encoded_30s.png).
- MP4 SHA256: `3c4de453a3a351461b9d93c912c8eddc608e788de8088e009ebf39f67dceb3bb`.
- **PASS:** 901×8개 시점의 sample tick/base_link 위치와 공통 메인 카메라 offset, 고정 월드 카메라 시작점 검사. 초기 상태 hash/물리, mass/CoM, 기록된 fingerprint 및 영어 자막 target 대조도 수행했다.
- **PASS:** 원본 NPZ/config/status/plan/5분 MP4 hash 보존, 직전 발표 MP4 hash 보존(`previous_video.sha256`).
- **PASS:** 최종 MP4의 ffprobe frame 수/크기/길이/codec 검사, 실제 재생 15/30초에서 추출한 화면의 영어 조건·검정 x10·거리·제어기 구분·흰 배경 제거 시각 검토. 최종 프레임 자막 영역의 인코딩 전후 픽셀 평균 절대 오차는 각 칸 1.637~1.996/255다. [최종 검증 JSON](velocity_bias_presentation_clean_grid/video_verification.json), 각 column verification 및 render log에 증거를 남겼다.
- 첫 합성 시도는 한 worker가 verification 파일을 쓰기 전에 실행되어 중단됐다(`compose_early_attempt.log`). 네 worker의 정상 종료를 모두 확인한 뒤 다시 합성하고 위 검증을 완료했다. 완성 MP4는 성공한 두 번째 합성의 산출물이다.
- **PASS:** `python -m py_compile test/render_velocity_bias_presentation.py`. 필수 `./scripts/agent-check.sh`의 전체 및 개별 검사 결과는 [agent_check.log](velocity_bias_presentation_clean_grid/agent_check.log)에 기록한다.
- **NOT_TESTED:** PowerPoint 앱 직접 재생. 긴 거리 조건의 실제 크기 로봇은 고정 화면에서 작게 보인다. 저마찰 yaw 회전 등 원본 궤적의 특성도 그대로 유지한다.

변경 파일은 `test/render_velocity_bias_presentation.py`, 이 보고서 및 `velocity_bias_presentation_clean_grid/`의 영상·PNG·검증 로그다. renderer 변경 전 사본과 task diff를 보관했다. 기존 영상·기록 및 제어기·정책·실기 코드, 관련 없는 변경은 건드리지 않았다. 커밋/push/배포는 하지 않았다.

재현: 새 docs/exp output으로 `init`, `render --column 0/1/2/3`, 네 렌더링 종료 후 `compose`를 실행한다.

```bash
/home/cocel/venvs/cosim_ros2_jazzy/bin/python test/render_velocity_bias_presentation.py \
  --output docs/exp/2026-10-17/velocity_bias_presentation_clean_grid_rerun --stage init
```
