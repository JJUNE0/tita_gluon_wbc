# 발표 영상: 환경 정보만 표시하고 기립은 1배속 재생

Execution Domain: VALIDATION_SIM

Evidence Status: PASS — 시간표·기립 구간 일치·기록 보존·최종 MP4 검증. 저장소 전체 검사 결과는 agent-check 로그 참조.

Policy Checkpoint SHA256: `6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05`

ONNX SHA256: `f44f07ed44970e3ff565eae67fd9229adf0be5c02215591c52a691ffcbb71b2a`

Branch: `agent/codex/dev_tita_gluon`

각 영상의 알고리즘 이름과 SIM 시간 표시를 지우고 기존 흰색 영어 환경 정보만 왼쪽 위로 옮겼다. `Distance from start`, 검정 속도 표시, 고정 월드 영상과 중앙 시작점, 2×4 전체 화면 구성은 유지한다. 영상 자체의 알고리즘 분류는 PPT에서 붙일 수 있다. 기존 행 순서는 위 FlashSAC only / 아래 FlashSAC + Velocity Bias다.

작업 중 추가된 요청에 따라 **기록의 처음 2초는 전부 동시에 1배속**, 이후 남은 298초는 동시에 10배속으로 재생한다. 아래 표시도 `x1 → x10`으로 바뀐다. 처음 2초에는 실제 기립이 포함돼 있다. 예를 들어 nominal의 base 높이는 RL 진입 시 0.1794 m에서 2초 후 0.3366 m로 상승하고 5초 값도 0.3366 m다. 같은 환경의 두 알고리즘은 첫 2초의 qpos/qvel이 완전히 같음을 검사했다. 서로 다른 물리 조건의 실제 자세 차이는 그대로 보존한다. 특정 환경의 기립 영상을 복사해서 다른 조건으로 표시하지 않았다.

재생 0~2초의 60개 프레임은 원본 시뮬레이션 0~2초를 재현하고, 재생 프레임 60에서 원본 sample 20(2초)로 이어져 10배속이 된다. 원본 qpos 기록은 0.1초 간격이므로 정상 속도 구간은 기록 프레임을 반복해 30 fps로 인코딩한다. 보간으로 새 자세를 만들거나 정책/물리를 다시 실행하지 않았다.

- [최종 MP4](velocity_bias_presentation_realtime_start/flashsac_velocity_bias_2x4_10x_presentation.mp4): 1920×1080, H.264/yuv420p, 30 fps, **955 frames / 31.833333초**, 14,526,909 bytes. 마지막 300초 시점을 포함한다.
- [기립 1배속 화면](velocity_bias_presentation_realtime_start/encoded_intro_1p5s.png), [10배속 전환 후](velocity_bias_presentation_realtime_start/encoded_switch_2p1s.png), [중간 화면](velocity_bias_presentation_realtime_start/encoded_midpoint.png).
- MP4 SHA256: `c7a0ac2743dc83f1bde6fa17d6919051d0df6aaf6a29ddcdd8d3a2f4834a2c86`.

## 실제 검사와 변경 범위

- **PASS:** 4개 환경 각각의 첫 2초 qpos/qvel이 위·아래 동일함을 검사했다. 모든 955×8개 렌더링 시점에서 sample tick/base_link 위치와 공통 메인 카메라 offset, 고정 월드 시선을 확인했다. 환경 자막과 target 일치, 초기 상태/물리, mass/CoM 및 기록된 fingerprint 검사도 유지했다.
- **PASS:** 출력 955 frames, 1배속 구간 60 frames, 재생 2초의 source sample 20, 마지막 source sample 3000을 검증했다. [시간표 검증](velocity_bias_presentation_realtime_start/timeline_verification.json), [최종 영상 검증](velocity_bias_presentation_realtime_start/video_verification.json)에 기록했다.
- **PASS:** 원본 NPZ/config/status/plan/5분 MP4 및 직전 발표 MP4 hash 보존. ffprobe 크기/codec/frame 수/길이 확인 및 실제 MP4의 재생 1.5/2.1초 화면에서 환경 정보만 남았는지와 `x1 → x10` 전환을 시각 검토했다. 15.9/31.8초 화면도 추출했다.
- **PASS:** renderer `py_compile` 실행. `./scripts/agent-check.sh`의 전체 결과 및 개별 검사 결과는 [agent_check.log](velocity_bias_presentation_realtime_start/agent_check.log)에 기록한다.
- **NOT_TESTED:** PowerPoint 앱 직접 재생. 위치 drift 감소와 yaw 고정을 같은 결과로 해석하지 않으며 원본 궤적의 회전은 유지된다.

변경 파일은 `test/render_velocity_bias_presentation.py`, 이 보고서 및 `velocity_bias_presentation_realtime_start/` 산출물이다. 추가 요청 전의 자막 제거 중간 렌더링은 `velocity_bias_presentation_environment_only/`에 남아 있으며 최종 합성본은 위 링크다. 변경 전 소스/상태 및 task diff를 보관했다. 기존 영상/실험, 제어기·정책·실기 코드, 관련 없는 변경은 건드리지 않았다. 커밋/push/배포는 수행하지 않았다.

재현: 새 docs/exp output으로 renderer의 `init`, `render --column 0/1/2/3`, 모든 worker 종료 후 `compose`를 실행한다.
