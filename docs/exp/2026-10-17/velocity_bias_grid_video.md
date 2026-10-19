# FlashSAC / velocity bias 2×4 환경 비교 영상

Execution Domain: VALIDATION_SIM

Evidence Status: PASS — 8개 300초 궤적, 실제 launch의 2초 설정, 관련 검사 18개, 최종 MP4/화면 검증 완료.

Policy Checkpoint SHA256: `6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05`

ONNX SHA256: `f44f07ed44970e3ff565eae67fd9229adf0be5c02215591c52a691ffcbb71b2a`

Branch: `agent/codex/dev_tita_gluon`

사용자가 확인한 네 조건을 열로 배치하고 위쪽은 FlashSAC only, 아래쪽은 FlashSAC + velocity bias로 배치했다. 주 checkpoint `tita_flash_sac_115632_883848/model_60000`, zero command, seed913, 각 300초다. 이전 `render_fixed_m4_drift_comparison.py` / `render_fixed_m4_mismatch_comparison.py`의 원점 표시·궤적·follow view 방식을 참고했다. 이번 영상에는 LQR을 사용하지 않는다.

| 열 | 환경 | 변경 |
|---|---|---|
| 1 | Nominal | 기본 물리 |
| 2 | Low friction | 바닥/휠 sliding friction μ=0.2, 균일 저마찰 바닥 |
| 3 | CoM forward + mass15 | base CoM x +5 mm, 전체 질량/관성 ×1.15 |
| 4 | CoM backward + mass15 | base CoM x −5 mm, 전체 질량/관성 ×1.15 |

질량 +15%는 앞/뒤 CoM 변경 두 조건에만 적용했다. 모든 물리 변경은 첫 startup step 전에 적용하고 실행 중 고정했다. 각 열의 두 모드는 같은 초기 qpos/qvel/previous raw action 및 같은 물리를 사용했다. 초기 상태 hash·배열과 physics metadata의 동일성을 검사했다. 센서 기반 보정과 정책 action 경로는 기존대로이며 GT 위치·속도는 평가/화면에만 사용한다. 연구 runner에서는 모든 모드에 현재 시점 IMU를 동일하게 사용한다.

## 실행기의 2초 설정

기존 제어기에는 이미 2초 대기가 적용되어 있었다. 이번에는 `WheelVelocityBias.ACQUISITION_SECONDS = 2.`를 시간값의 기준으로 두고 launch argument 설명과 CLI 도움말에 2초를 표시했다. 실제 launch 실행 로그에도 controller의 값을 읽어 `velocity_bias_acquisition_s: 2.0`으로 기록한다. launch에 별도의 시간값을 덮어쓰는 인자는 만들지 않았다.

```bash
python sim2sim/sim2sim_ros2_jazzy/launch/sim2sim.launch.py \
  --ckpt lab/ddt_lab/logs/flash_sac/tita_flash_sac_115632_883848/model_60000 \
  --velocity_bias
```

타이머는 기존대로 RL 상태의 zero-command hold 진입부터 세며 이동 명령 후 정지 재진입 시에도 다시 기다린다. 기울기/추정 속도 조건도 유지한다. 실제 launch의 `--headless --steps 1000` 실행에서 1,000 tick 완료 및 대기값 2.0을 확인했다. 기존 math/센서/ROS/CLI/타이머/선택한 300초 궤적 재현 검사 **18/18 PASS**다. [launch 검증 기록](velocity_bias_grid_video/launch_verification.json)과 `tests.log`에 직접 증거를 남겼다.

## 이번 영상의 측정값

8개 궤적이 모두 300초를 완료했고 넘어짐/수치 오류/중단이 없었다. 원점은 공통 **RL 진입 위치**로 잡아 첫 2초 대기 중 이동량까지 포함했다. 이전 보고서의 준비 구간을 제외한 위치 수치와 직접 동일시하지 않는다.

| 조건 | FlashSAC 최대 이탈 | Velocity bias 최대 이탈 | FlashSAC 위치 IAE | Velocity bias 위치 IAE |
|---|---:|---:|---:|---:|
| Nominal | 5.2877 m | 0.0310 m | 752.3939 m·s | 0.4660 m·s |
| Low friction | 1.4603 m | 0.0286 m | 257.2913 m·s | 1.9954 m·s |
| CoM forward / mass15 | 22.1111 m | 0.1260 m | 3,328.8063 m·s | 26.5226 m·s |
| CoM backward / mass15 | 29.1922 m | 0.2154 m | 4,452.1894 m·s | 50.2434 m·s |

보정은 전후 속도를 억제하며 원점 복귀/heading hold를 목표로 하지 않는다. 저마찰에서 수백 도 yaw 회전도 있으므로 위치 drift 감소를 완전한 자세 정지로 해석하지 않는다. 남은 초기 위치 offset은 화면의 distance/dX/dY로 표시한다.

## 영상과 재현

최종 [5분 2×4 비교 영상](velocity_bias_grid_video/flashsac_vs_velocity_bias_2x4_05min.mp4)은 2행×4열, 2560×1200, H.264/yuv420p, 10 fps, 300초 시뮬레이션의 시작/끝을 포함한 3,001 frame(재생 길이 300.1초)이다. 파일 크기는 22,018,546 bytes(약 22 MB)다. 1배속이며 각 칸의 시간은 동기화했다. [실제 인코딩 영상의 150초 화면](velocity_bias_grid_video/encoded_frame_150s.png)도 저장했다.

각 칸에 초기 위치 노란 십자, 현재/최대 XY 거리, dX/dY, 누적 yaw, XY 궤적과 거리 그래프, fixed world view와 follow inset을 배치했다. 같은 열의 위/아래는 동일한 카메라 및 그래프 축척이다. 다른 열 사이의 world view 축척은 각 paired trajectory의 범위에 맞추므로 열 간 로봇 크기를 직접 비교하지 않는다. follow inset의 배율은 동일하다.

새 `test/render_velocity_bias_grid.py`로 collection과 render를 분리했다. 실제 MuJoCo qpos/qvel을 0.1초 간격으로 저장하고, 같은 물리 모델로 다시 렌더링하며 base_link 위치가 기록과 맞는지 검사한다. 예비 프레임 0/10/150/300초를 시각적으로 확인했다. 네 열을 별도 프로세스로 렌더링한 후 같은 frame/time으로 hstack하여 최종 2×4 영상으로 합친다. 각 열과 최종 영상의 ffprobe frame count/해상도/길이 및 SHA256를 기록한다.

네 열 및 최종 MP4의 검증은 모두 PASS다. 최종 파일에서도 150초 프레임을 추출하여 순서·자막·위/아래 모드·시간 동기화를 확인했다. 렌더 backend는 `llvmpipe (LLVM 20.1.2, 256 bits)`이며 실제 검증 값은 [video_verification.json](velocity_bias_grid_video/video_verification.json)에 기록했다. 최종 MP4 SHA256는 `3e59484409e34a09d9cf709797766ff4975f861da142e4903f3e1f3bf12d9aa3`이다.

렌더러 병렬화는 collection 완료 후 추가했으며 `collect`/`collect_one` 함수 AST가 변경되지 않았음을 검사했다. 실제 collection 소스와 renderer 소스를 각각 `collector_source.py.txt`, `renderer_source.py.txt`로 보관하고 `renderer_extension.diff`로 구분했다. 기존 평가기/과거 렌더러는 수정하지 않았다.

재현은 저장된 `plan.json`과 기존 export를 사용한다. 새 output 경로에 같은 plan을 둔 뒤 다음 단계로 실행한다.

```bash
mkdir -p docs/exp/2026-10-17/velocity_bias_grid_video_rerun
cp docs/exp/2026-10-17/velocity_bias_grid_video/plan.json \
  docs/exp/2026-10-17/velocity_bias_grid_video_rerun/plan.json
/home/cocel/venvs/cosim_ros2_jazzy/bin/python test/render_velocity_bias_grid.py \
  --output docs/exp/2026-10-17/velocity_bias_grid_video_rerun --stage collect

/home/cocel/venvs/cosim_ros2_jazzy/bin/python test/render_velocity_bias_grid.py \
  --output docs/exp/2026-10-17/velocity_bias_grid_video_rerun --stage render --column 0
# column 1/2/3도 각각 렌더링한 후 합성한다.
/home/cocel/venvs/cosim_ros2_jazzy/bin/python test/render_velocity_bias_grid.py \
  --output docs/exp/2026-10-17/velocity_bias_grid_video_rerun --stage compose
```

기존 산출물을 덮어쓰지 않도록 이미 있는 NPZ/MP4에는 오류를 낸다. 실기 controller/launch, 정책 가중치 및 학습 코드는 수정하지 않았다. Hardware evidence: NOT_TESTED. 실기 실행/배포/커밋/push는 수행하지 않았다.

## 최종 변경·검사 범위

- 변경: `launch/sim2sim.launch.py`의 2초 안내, `cli.py`의 도움말/실제 acquisition 값 기록, `velocity_bias.py`의 동일한 2초 값을 named constant로 정리, 신규 `test/render_velocity_bias_grid.py`, 이 보고서 및 영상/검증 artifact. 기존 control 수치와 이득은 바뀌지 않았다.
- PASS: 관련 검사 18/18, 실제 launch 1,000 tick와 `velocity_bias_acquisition_s=2.0`, 8/8 궤적 300초 완료, 각 열의 동일 초기 상태/물리, 네 열과 최종 영상의 frame/크기/길이/SHA256 및 시각 검토.
- `./scripts/agent-check.sh`: **FAIL**. Python 구문 **484/484 PASS**, URDF **8/8 PASS**다. 실패 원인은 기존 사용자 변경 `lab/ddt_lab/ddt_lab/tasks/manager_based/locomotion/robots/tita/my_flat_env_cfg.py` 431/437/443/449/455/461행 trailing whitespace이며 수정하지 않았다. 전체 로그는 `agent_check.log`에 있다.
- 실제 launch smoke가 생성한 `tita_sim2sim_120143_762075.json`/summary는 이 작업의 산출물이다. 작업 중 추가로 관측된 `tita_sim2sim_120004_079667.json`/summary는 별도 실행의 기록이며 이 작업에서 수정하지 않았다.
- 최종 status에서 별도 `flashsac_velocity_bias/before.json`과 sim2real의 `velocity_bias_geometry.json`/`velocity_bias.hpp` 추가도 관측됐다. 이 영상 작업에서 생성·수정한 파일이 아니므로 작업 변경 목록에서 제외하고 그대로 두었다.
- 최종 task diff, 기존 파일의 변경 전 내용, 소스 hash 및 범위 확인 결과는 `before.json`, `task_files.diff`, `completion_integrity.json`에 기록한다. 다른 기존 runtime/평가기/과거 renderer hash는 유지됐다.
