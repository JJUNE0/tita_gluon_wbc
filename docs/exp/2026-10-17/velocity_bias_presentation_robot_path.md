# 발표 영상 수정: XY 경로 위 실제 로봇 모형 + 흰색 거리 표시

Execution Domain: VALIDATION_SIM

Evidence Status: PASS — 영상·기록 일치, 원본 보존, 인코딩/시각 검증. 저장소 전체 검사 결과는 아래 agent-check 로그 참조.

Policy Checkpoint SHA256: `6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05`

ONNX SHA256: `f44f07ed44970e3ff565eae67fd9229adf0be5c02215591c52a691ffcbb71b2a`

Branch: `agent/codex/dev_tita_gluon`

로봇을 따라다니는 별도 탑뷰를 없애고, 왼쪽 XY 그래프에 실제 로봇 모델의 위에서 본 모습을 위치 표식으로 넣었다. 고정 축 위에서 표식이 실제 XY 좌표를 따라 움직이고 지나온 경로를 남긴다. 로봇 모습과 회전은 해당 시점의 저장된 qpos/qvel을 렌더링한 것이다. RGB와 MuJoCo segmentation으로 바닥을 제외한 base_link 하위 로봇 형상만 추출한다. 화면 가독성을 위해 **로봇 표식의 크기는 확대**했으며 그래프에도 `Robot marker enlarged`로 표시했다. 로봇 형상 크기를 그래프의 m 단위 실물 크기로 해석하지 않는다.

X/Y 좌표와 경로는 실제 이동량을 유지하고, 같은 열 위·아래는 전체 궤적에 맞춘 동일한 고정 범위 및 동일한 X/Y 길이 축척을 사용한다. 로봇 표식의 화면 방향이 +X 오른쪽/+Y 위쪽과 일치하는지 각 렌더링 시점에 검사했다. 원점은 기존대로 RL 진입 위치로 처음 2초 대기 이동도 포함한다. 큰 메인 로봇은 이전처럼 약 20% 줄인 카메라 배율을 유지하고 화면 중앙 높이로 배치했다.

거리 카드의 상자는 제거했다. 각 영상 오른쪽 위에는 굵은 흰 글씨로 `Distance from start`, 현재 거리, `Peak`를 표시한다. 현재 거리는 `sqrt(dx²+dy²)`이며 누적 주행거리가 아니다. Peak는 현재 시점까지의 최대 이탈 거리다. 글자에는 얇은 어두운 테두리를 넣었다. 기존 2×4 조건/제어기 배치와 10배속은 같다. 물리·정책을 새로 실행하지 않았고 성능 수치는 기존 실험과 동일하다.

- [수정 영상 MP4](velocity_bias_presentation_robot_path/flashsac_velocity_bias_2x4_10x_presentation.mp4): 1920×1080, H.264/yuv420p, 30 fps, 901 frames, **30.033333초**, 10,166,121 bytes.
- [중간 화면](velocity_bias_presentation_robot_path/encoded_15s.png), [최종 화면/PPT 정지 이미지](velocity_bias_presentation_robot_path/encoded_30s.png).
- MP4 SHA256: `1fa899b36dd84375521bd63dc4b7ae2c30a50e8647b43180ee33fb9a416c4ce6`.

## 검사 및 변경 범위

- **PASS:** 901×8개 렌더링 시점의 sample tick/base_link 위치 일치, 각 열의 동일 초기 상태 hash/물리, mass/CoM 및 기록에 있는 physics fingerprint 검사. 로봇 표식의 segmentation 존재 및 카메라 world XY 방향 검사도 매 시점 수행했다.
- **PASS:** 원본 NPZ/config/status/plan/5분 MP4 SHA256 보존. 이전 두 발표 MP4도 hash 일치로 보존을 확인했다(`previous_videos.sha256`).
- **PASS:** ffprobe 실제 frame 수/해상도/길이/codec 검증, 완성 MP4에서 추출한 재생 15/30초 화면의 XY 경로·로봇 표식·거리 글씨·조건 순서 시각 검토. [영상 검증 JSON](velocity_bias_presentation_robot_path/video_verification.json), 각 column verification 및 render log에 직접 증거를 남겼다.
- **PASS:** `python -m py_compile test/render_velocity_bias_presentation.py` 실행. 저장소 필수 검사 `./scripts/agent-check.sh`의 전체 결과와 개별 검사 결과는 [agent_check.log](velocity_bias_presentation_robot_path/agent_check.log)에 기록한다.
- **NOT_TESTED:** PowerPoint 앱 직접 재생. 원본 저마찰 yaw 회전은 남아 있으며 위치 drift 억제와 방향 고정을 동일시하지 않는다.

변경 파일은 `test/render_velocity_bias_presentation.py`, 이 보고서 및 `velocity_bias_presentation_robot_path/` 영상·그림·검증 산출물이다. renderer의 변경 전 사본과 diff를 산출물 폴더에 보관했다. 기존 발표 MP4와 원본 실험, 제어기·정책·실기 코드는 수정하지 않았다. 관련 없는 변경은 이 작업에 포함하지 않았다. 커밋/push/배포는 하지 않았다.

재현은 새 docs/exp 하위 output을 지정하여 `init`, 각 열의 `render --column 0/1/2/3`, `compose` 순서로 실행한다.

```bash
/home/cocel/venvs/cosim_ros2_jazzy/bin/python test/render_velocity_bias_presentation.py \
  --output docs/exp/2026-10-17/velocity_bias_presentation_robot_path_rerun --stage init
```
