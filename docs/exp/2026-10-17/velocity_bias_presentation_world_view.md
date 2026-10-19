# 발표 영상: 추적 화면을 메인으로, 고정 월드 화면을 보조로

Execution Domain: VALIDATION_SIM

Evidence Status: PASS — 영상 렌더링·기록 일치, 원본 보존, MP4 및 인코딩 화면 확인. 저장소 전체 검사는 agent-check 로그 참조.

Policy Checkpoint SHA256: `6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05`

ONNX SHA256: `f44f07ed44970e3ff565eae67fd9229adf0be5c02215591c52a691ffcbb71b2a`

Branch: `agent/codex/dev_tita_gluon`

사용자가 지정한 원본 `velocity_bias_grid_video/flashsac_vs_velocity_bias_2x4_05min.mp4`의 두 영상 역할을 바꿨다. 원본 오른쪽 아래 follow view와 같은 방향의 로봇 추적 화면이 각 칸의 메인이고, 원본 배경과 같은 MuJoCo 고정 월드 화면이 왼쪽 아래 보조 영상이다. 이전의 XY 그래프/로봇 표식 합성은 제거했다. 보조 영상에는 실제 물리 크기의 로봇, 시작점과 지나온 3D 바닥 경로가 표시된다. 원본의 `visual.markers` 구현을 그대로 재사용한다.

Peak를 제거하고 우측 상단 `Distance from start`와 현재 거리만 굵은 흰색으로 남겼다. 거리 상자, 그래프의 흰 배경과 빨간 테두리도 없다. 보조 영상에는 얇은 회청색 경계만 있다. 기존 2×4 제어기/환경 순서, 10배속 및 원본 기록은 유지했다. 새 정책 추론이나 물리 rollout은 없다.

## 중심점과 화면 범위

- 메인 카메라는 모두 distance 2.05 m, azimuth 115°, elevation −20°이고 매 프레임 같은 base_link 기준 offset을 적용한다. 이전의 조금 작은 로봇 크기를 유지하며, 각 칸의 메인 로봇 기준 위치를 통일한다. 실제 자세/회전에 따른 형상 차이는 원본 그대로다.
- 보조 카메라는 azimuth 90°, elevation −50°로 원본 월드 화면과 같다. 시선은 **RL 진입 XY 시작점**에 고정하고, 시작점 십자를 모든 보조 화면의 가운데로 통일했다. 로봇을 따라 카메라가 움직이지 않는다.
- 각 열 위·아래의 동일한 고정 카메라로 전체 궤적을 담는다. 카메라 거리는 `max(2.6 m, 3 × paired 최대 XY 축 이탈)`이다. 시작점을 가운데 둔 대칭 범위여서 예전 그래프처럼 조건에 따라 시작점이 다른 쪽에 놓이지 않는다. 열 사이 배율은 다르다. 긴 거리 조건에서는 실제 크기의 로봇이 작게 보이며, 큰 메인 화면과 거리 숫자를 함께 읽는다.
- 보조 화면의 중앙 십자는 멀리서도 식별되도록 12 px 노란 십자를 덧그렸다. 로봇이나 경로의 위치·크기를 별도로 확대하지 않는다.

## 산출물과 검증

- [최종 MP4](velocity_bias_presentation_world_view/flashsac_velocity_bias_2x4_10x_presentation.mp4): 1920×1080, H.264/yuv420p, 30 fps, 901 frames, **30.033333초**, 11,168,999 bytes.
- [중간 화면](velocity_bias_presentation_world_view/encoded_15s.png), [최종 화면](velocity_bias_presentation_world_view/encoded_30s.png).
- MP4 SHA256: `8cc7fa3774bb8288188206530dc8627a0d5e55ef552353b5ef19e9d5b05ed287`.
- **PASS:** 901×8개 시점의 sample tick/base_link 위치 일치, 메인 카메라의 공통 offset, 보조 카메라의 고정 시작점 시선 검사. 각 열의 초기 상태 hash/물리, mass/CoM 및 기록된 fingerprint도 확인했다. 각 column verification에 `main_camera_anchor_matches`, `origin_centered`, `same_camera_for_both_rows`, `peak_removed`를 기록했다.
- **PASS:** 원본 NPZ/config/status/plan/5분 MP4 hash 보존. 직전 발표 MP4도 기존 hash와 동일하다(`previous_video.sha256`). 이전 결과는 덮어쓰지 않았다.
- **PASS:** ffprobe frame 수·해상도·codec·길이 검사 및 실제 인코딩 MP4의 재생 15/30초 화면을 추출해 중심점·영상 배치·Peak 제거·거리 표시를 시각 검토했다. [최종 검증 JSON](velocity_bias_presentation_world_view/video_verification.json).
- **PASS:** `python -m py_compile test/render_velocity_bias_presentation.py`. 저장소 필수 검사 `./scripts/agent-check.sh`의 전체 결과와 개별 검사 결과는 [agent_check.log](velocity_bias_presentation_world_view/agent_check.log)에 기록한다.
- **NOT_TESTED:** PowerPoint 앱 직접 재생. 원본 저마찰 yaw 회전은 남아 있으며 위치 drift 억제와 heading 고정을 같은 결과로 해석하지 않는다.

변경 파일: `test/render_velocity_bias_presentation.py`, 이 보고서 및 `velocity_bias_presentation_world_view/` 산출물. 변경 전 renderer와 task diff를 보관했다. 기존 제어기·정책·실기 코드 및 관련 없는 변경에는 손대지 않았다. 커밋/push/배포는 수행하지 않았다.

재현은 새 docs/exp 하위 output으로 `init`, `render --column 0/1/2/3`, `compose` 순서로 실행한다.

```bash
/home/cocel/venvs/cosim_ros2_jazzy/bin/python test/render_velocity_bias_presentation.py \
  --output docs/exp/2026-10-17/velocity_bias_presentation_world_view_rerun --stage init
```
