# FlashSAC / Velocity Bias 발표용 10배속 영상

Execution Domain: VALIDATION_SIM

Evidence Status: PASS — 기존 8개 궤적의 재렌더링·원본 보존·MP4 검증 완료. 저장소 전체 agent-check는 기존 공백 오류로 FAIL.

Policy Checkpoint SHA256: `6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05`

ONNX SHA256: `f44f07ed44970e3ff565eae67fd9229adf0be5c02215591c52a691ffcbb71b2a`

Branch: `agent/codex/dev_tita_gluon`

직무 발표용으로 기존 [300초 비교 실험](velocity_bias_grid_video.md)의 저장된 qpos/qvel을 재사용해 화면만 다시 구성했다. 새 정책 추론·물리 rollout은 실행하지 않았다. 기존 MP4를 잘라 확대하는 대신 같은 기록을 선명한 follow view로 다시 렌더링했다. 카메라 방향은 기존 follow view와 같고, 거리는 1.65 m, 화면 오른쪽에 로봇을 배치하도록 시선을 옮겼다. 모든 칸에 같은 카메라 설정을 사용한다. 원래 MP4와 8개 NPZ/config/status/plan의 SHA256가 작업 전후 동일하다.

- [발표용 MP4](velocity_bias_presentation/flashsac_velocity_bias_2x4_10x_presentation.mp4): 1920×1080, H.264/yuv420p, 30 fps, 901 frame, **30.033333초**, 10,300,852 bytes. 300초 시뮬레이션을 10배속으로 표시한다. 원본은 10 fps 기록이므로 30 fps 출력이 추가 물리 정보를 의미하지는 않는다.
- [최종 화면 PNG](velocity_bias_presentation/encoded_30s.png): PPT 정지 이미지로도 사용할 수 있다.
- 위 FlashSAC / 아래 FlashSAC + Velocity Bias, 4개 열은 기본 / μ=0.2 / CoM +5 mm·질량+15% / CoM −5 mm·질량+15%다. 질량 추가는 뒤의 두 조건에 적용한다.
- 각 칸 왼쪽에는 **흰 배경·빨간 테두리 XY 궤적**, 시작점 대비 현재 거리와 그 시점까지의 최대 거리를 표시한다. 검은 십자는 RL 진입 원점, 파랑/초록 점은 현재 위치다. 위치 평가는 처음 2초 대기도 포함한다.
- 그래프는 각 열의 두 전체 궤적을 함께 감싸는 고정 범위이며 X/Y에 같은 길이 축척을 사용한다. 같은 열 위·아래 축척은 동일하다. 열 간 축척은 다르고 단위를 m로 표시한다. 아래 행의 작은 움직임을 별도로 확대하지 않았다.
- 화면 상단 시뮬레이션 시간과 10× 표시, 하단 시뮬레이션임을 밝히는 문구를 유지했다. 짧은 환경·제어기 제목을 제외한 이전의 조밀한 설명은 덜어냈다.

최대 위치 이탈은 원본 결과와 같다. 이 편집으로 새로운 성능 개선이 발생한 것은 아니다.

| 환경 | FlashSAC 최대 이탈 | Velocity Bias 최대 이탈 |
|---|---:|---:|
| 기본 | 5.288 m | 0.031 m |
| 저마찰 | 1.460 m | 0.029 m |
| CoM 앞 / 질량+15% | 22.111 m | 0.126 m |
| CoM 뒤 / 질량+15% | 29.192 m | 0.215 m |

## 실제 수행한 검사

- **PASS:** 각 렌더링 시점 901×8개에서 기록의 sample tick과 MuJoCo `base_link` 위치 일치, 각 열 두 모드의 동일 초기 상태 hash/물리, 모델 mass/CoM 및 기록에 포함된 physics fingerprint 확인.
- **PASS:** 원본 입력 SHA256 보존. 인코딩된 최종 MP4를 ffprobe로 읽어 901 frame, 1920×1080, 30 fps, H.264/yuv420p, 재생 길이를 확인했다. 실제 MP4에서 재생 15/30초 화면을 추출해 조건 순서·동기화·그래프·자막·로봇 표시를 시각 검토했다. 증거는 [video_verification.json](velocity_bias_presentation/video_verification.json), 각 column verification 및 render log에 있다.
- MP4 SHA256: `d7630eda5c2a289d3d02c7c24c475d15925d6f09a29428549d4f68f3381c0b7e`.
- **FAIL:** `./scripts/agent-check.sh`. Python 구문 **487 passed / 0 failed**, URDF **8개 PASS**. 기존 `lab/ddt_lab/ddt_lab/tasks/manager_based/locomotion/robots/tita/my_flat_env_cfg.py` 431/437/443/449/455/461행 trailing whitespace 때문에 전체 결과 FAIL. 해당 파일은 수정하지 않았다. [전체 검사 로그](velocity_bias_presentation/agent_check.log).
- **NOT_TESTED:** 실제 PowerPoint 앱에서의 재생 및 하드웨어. H.264/yuv420p MP4로 저장했다. 저마찰의 yaw 회전은 원본에 남아 있으므로 영상은 위치 drift 억제의 증거이며 완전한 자세·방향 고정을 뜻하지 않는다.

## 변경 범위와 재현

추가 파일은 `test/render_velocity_bias_presentation.py`, 이 보고서, `velocity_bias_presentation/`의 MP4/PNG/검증 로그다. 기존 제어 코드·정책·원본 영상/궤적은 수정하지 않았다. git status 스냅샷과 task diff를 산출물 폴더에 저장했다. 커밋·push·배포는 수행하지 않았다.

```bash
PYTHON=/home/cocel/venvs/cosim_ros2_jazzy/bin/python
$PYTHON test/render_velocity_bias_presentation.py --stage init
$PYTHON test/render_velocity_bias_presentation.py --stage preview --column 0
# preview/render는 column 0, 1, 2, 3 각각 실행한다.
$PYTHON test/render_velocity_bias_presentation.py --stage render --column 0
$PYTHON test/render_velocity_bias_presentation.py --stage compose
```

입력·출력 경로는 renderer 상단 상수다. 재실행은 OUTPUT을 새 docs/exp 하위 경로로 바꿔 수행한다. 이미 존재하는 hash manifest나 MP4를 덮어쓰지 않도록 오류를 낸다. 렌더러는 EGL/llvmpipe를 사용하며 네 열을 별도 프로세스로 만든 뒤 hstack으로 합친다.
