# 발표 영상 수정: 작은 메인 로봇 + 우측 하단 탑뷰

Execution Domain: VALIDATION_SIM

Evidence Status: PASS — 저장된 8개 궤적 재렌더링, 원본 보존, MP4 및 실제 인코딩 화면 확인 완료. 저장소 전체 agent-check는 기존 공백 오류로 FAIL.

Policy Checkpoint SHA256: `6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05`

ONNX SHA256: `f44f07ed44970e3ff565eae67fd9229adf0be5c02215591c52a691ffcbb71b2a`

Branch: `agent/codex/dev_tita_gluon`

기존 [발표 영상](velocity_bias_presentation.md)의 메인 카메라 거리를 1.65→2.05 m로 늘려 로봇의 화면 크기를 약 20% 줄였다. 같은 칸 우측 상단에 메인 로봇이 보이도록 시선을 조정하고 우측 하단에 214×128 px 탑뷰와 TOP VIEW 제목/흰 테두리를 추가했다. 탑뷰는 elevation −90°, azimuth 90°, distance 1.4 m이며 로봇 위치를 따라가고 화면 방향은 월드 기준으로 고정한다. 따라서 방향 회전은 탑뷰에서도 보인다. 위치 이탈의 정량 비교는 기존 왼쪽 그래프/거리 표시에서 읽는다.

기존 2×4 배치, 위 FlashSAC/아래 Velocity Bias, 4개 환경, 흰 배경·빨간 테두리 그래프, 같은 열의 위아래 고정 축척과 10배속을 유지했다. 새로운 물리 실험이나 정책 실행은 없다. 모든 뷰는 같은 시점의 저장된 qpos/qvel로 동기화했다. 성능 수치는 원본 실험과 동일하며 카메라 변경으로 결과가 바뀌지 않는다.

- [수정 MP4](velocity_bias_presentation_topview/flashsac_velocity_bias_2x4_10x_presentation.mp4): 1920×1080, H.264/yuv420p, 30 fps, 901 frames, **30.033333초**, 11,389,061 bytes.
- [PPT 정지 이미지](velocity_bias_presentation_topview/encoded_30s.png).
- MP4 SHA256: `29d932bd5e0ade9f4802e4cb4b676a76f13d5f37113fbb25d3a98f6c1f92a620`.

## 검사와 변경 범위

- **PASS:** 901×8개 렌더링 시점의 sample tick 및 base_link 위치 일치, 각 열 초기 상태 hash/물리 일치, 모델 mass/CoM 및 기록에 포함된 physics fingerprint 확인. 4개 column verification과 [최종 검증](velocity_bias_presentation_topview/video_verification.json)에 기록했다.
- **PASS:** 원본 NPZ/config/status/plan 및 원래 5분 MP4 SHA256 보존. 이전 발표 MP4 SHA256도 `d7630eda5c2a289d3d02c7c24c475d15925d6f09a29428549d4f68f3381c0b7e`로 유지했다. 이전 영상 산출물은 덮어쓰지 않았다.
- **PASS:** ffprobe 실제 frame 수/해상도/길이/codec 검사, 완성 MP4에서 추출한 재생 15/30초 화면의 메인 로봇·탑뷰·그래프 배치/시간 시각 검토, renderer `py_compile` 실행.
- **FAIL:** `./scripts/agent-check.sh`. Python 구문 487/487 및 URDF 8/8은 PASS. 기존 `my_flat_env_cfg.py` 431/437/443/449/455/461행 trailing whitespace로 전체 FAIL. 해당 파일은 수정하지 않았다. [검사 로그](velocity_bias_presentation_topview/agent_check.log).
- **NOT_TESTED:** PowerPoint 앱 직접 재생. 원본 저마찰 yaw 회전은 남아 있으며 이 영상은 위치 drift 감소를 보여준다.

변경 파일은 `test/render_velocity_bias_presentation.py`, 이 보고서 및 `velocity_bias_presentation_topview/` 산출물이다. renderer에 `--output`을 추가해 기존 영상과 별도 경로에 저장했다. 변경 전 renderer 사본과 이번 diff를 산출물 폴더에 남겼다. 제어기·실기·정책 및 관련 없는 파일은 이 작업에서 변경하지 않았다. 커밋/push/배포는 수행하지 않았다.

```bash
/home/cocel/venvs/cosim_ros2_jazzy/bin/python test/render_velocity_bias_presentation.py \
  --output docs/exp/2026-10-17/velocity_bias_presentation_topview_rerun --stage init
# 같은 output으로 render --column 0/1/2/3을 각각 실행한 뒤 compose 실행.
```
