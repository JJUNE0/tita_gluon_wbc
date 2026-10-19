# flashsac_headw0_50000 실기 배포 준비 (heading 관측 C++ + 번들)

- Execution Domains: DESKTOP_DRY_RUN (코드·빌드·parity), VALIDATION_SIM (체크포인트 선택), ROBOT_STATE_CHANGING (설치·빌드, 운영자 요청), ROBOT_COMMAND_FREE_RUNTIME (로봇 검증)
- 운영자 요청 (2026-10-19): "sim2real 실험 바로 할거 … simreal 코드 수정 ㄱㄱ 하고 로봇켜서 코드 옮기고 빌드". 제어기 실행·모터 명령은 에이전트가 하지 않는다
- Policy Checkpoint SHA256: `0a6f8ef2bb8a324bf6f6fb7689297f9001bd4b57896daa0cb9ead4953162f4a7` (ONNX `284b4166297fafe5606e58d7b66d9e4570980b839ebde433cbd7a85549313a4c`, 번들 config `804d2ab9f0fdb80232706a9dc99f4daacad4b2c0f194c914f99b1d8fd1b7c428`)
- Evidence Status: 데스크톱 PASS / 로봇 설치·검증은 아래 "로봇" 절 / 실기 거동 NOT_TESTED

## 체크포인트 선택 (VALIDATION_SIM, `sphere_wheel_screen` exp7)

run `tita_flash_sac_125547_806511`(학습 중): 구 휠, MA2 없음, 기본 명령, heading 보상 + actor·critic gyro heading 관측, warmup 0.

| ckpt | 정지 yaw / 주행 후 정지 | 정지 직후 1 s 회전 | pitch | 25 Hz g = 1.5 / 2 / 3 |
|---|---|---|---|---|
| 45k (sim2sim 뷰어로 확인한 것) | 0.00 / 0.12 °/s | −1.7 ~ +0.9° | 3.1° | **교번 0.31** / 0.09 / 넘어짐 |
| **50k (선택)** | 0.00 / 0.06 °/s | −0.1 ~ +0.6° | 4.1° | 없음 / **넘어짐** / 넘어짐 |

- 50k의 무릎 조건 5종(왼쪽 약함·반전·0.68·0.55·nominal): 정지 yaw 모두 0.00 °/s, 주행 후 정지 0.03–0.06 °/s, pitch 2.5–5.3°.
- 위험:
  - MA2가 없고 25 Hz 대리 여유가 g = 1.5–2 사이다(② 60k는 g = 2까지, MA2 정책은 g = 3까지).
  - 실기 과반응 추정은 g ≈ 1–1.5다. 첫 실행에서 25 Hz 교번(다리 떨림 소리)을 주시해야 한다.

## 코드 변경 (`sim2real/tita_ws`)

| 파일 | 변경 |
|---|---|
| `include/tita_controller/adapter.hpp` | `ObsKind::HeadingError`, `HeadingConfig`. `ObservationBuilder`가 0 밴드 안에서 warmup 뒤 (gyro z − bias)·dt를 적분한다. 출력만 clip한다. `set_gyro_bias`. `build(..., heading_dt)`로 측정 간격을 쓸 수 있다 |
| `src/tita_node.cpp` | heading 파라미터. idle·sit 정지 샘플(모든 관절 \|dq\| < 0.02 rad/s, 각 축 \|ω\| < 0.05 rad/s)의 최근 5 s gyro z를 보관한다. RL 진입 시 중앙값을 바이어스로 설정하고 로그를 남긴다. 1 s 미만이면 대체값(`heading_gyro_bias_fallback`, 기본 0)을 쓰고 WARN을 낸다. RL 중 heading 적분은 측정한 관측 간격(0.25–2.5 × 정책 주기로 제한)을 쓴다 |
| `launch/tita.launch.py` | `OBS_KINDS`에 `heading_error`(8)를 추가하고 `heading_clip_rad`, `heading_warmup_s`, `heading_zero_thresholds`를 전달한다 |
| `launch/flashsac.launch.py`, `run_flashsac.sh` | `flashsac_headw0_50000` 번들 SHA 고정·허용 |
| `policies/flashsac_headw0_50000/` | `test/sim2real/prepare_heading_bundle.py`로 생성. 학습 관측·action·게인은 그대로다. 조이스틱 상한은 ±1 m/s, ±1 rad/s, ramp 0.5/s(학습 ramp와 같음) |

## 데스크톱 검증 (DESKTOP_DRY_RUN, 모두 PASS)

| 검사 | 결과 |
|---|---|
| Jazzy x64 colcon 빌드 (`tita_robot`, `tita_controller`) | 경고 0, 성공 |
| C++ 대 Python heading parity (`test/sim2real/test_heading_parity.py`, 4000 step, 명령 전환·0 밴드 경계값·reset 17회·bias 0.0021) | 전체 관측 최대 오차 1.2e-7, heading 오차 0. warmup 0과 1 s 설정 모두 |
| sim2sim 단위 테스트 (`test/test_sim2sim_heading_error.py`) | PASS |
| Torch 대 ONNX (번들 생성 시, x64 onnxruntime 256 샘플) | ≤ 4.1e-6 |
| 로봇 검증 스크립트의 데스크톱 실행 (`verify_heading_bundle.py`) | 7/7 PASS (`desktop_verify.json`) |

## 로봇 배포 절차 (`test/sim2real/deploy_heading_bundle.sh`, 로봇에서 실행)

1. `deploy_build`
   - 덮어쓸 5개 파일이 커밋 `c8c159d` 버전과 같은지 확인한다(`expected_before.sha256`).
   - payload 해시를 확인하고, overlay 제어기가 실행 중이면 거부한다.
   - `src/tita_controller`, `run_flashsac.sh`, `install/tita_controller`를 백업한다(`before_deployment.tar.gz`).
   - payload를 풀고 `colcon build --packages-select tita_controller`를 실행한다(Humble aarch64).
2. `verify`
   - 설치 파일을 비교한다.
   - ARM ONNX 대 Torch, ARM C++ heading parity를 검사한다.
   - launch 정의를 검사한다(SHA 고정, heading 파라미터, 필터 none, 조이스틱 상한).
   - `ldd`를 확인하고, 벤더 서비스 상태가 그대로인지 본다.

## 로봇

2026-10-19, 로봇 `tita` (Humble aarch64). 로그는 `heading_bundle_deployment/deploy_console.log`, `verify_console.log`, `robot/`에 있다.

| 단계 | 결과 |
|---|---|
| 사전 점검 (읽기 전용) | 덮어쓸 5개 파일이 `c8c159d` 버전과 같다. overlay 제어기는 미실행이다. 벤더 `tita-bringup.service`는 active이고 건드리지 않았다 |
| `deploy_build` | 해시 확인 22건 OK. 백업 `~/tita_ws/docs/exp/2026-10-19/heading_bundle_deployment/before_deployment.tar.gz`(`robot/backup.sha256`). `tita_controller` 빌드 44.7 s 성공, 경고 없음 |
| `verify` | 7/7 PASS (`robot/arm_verify.json`). ARM ONNX 대 Torch 3.5e-6, ARM C++ heading parity 1.2e-7. SHA 고정·heading 파라미터·필터 none·조이스틱 상한 확인. 설치 파일 cmp 일치, `ldd` not found 없음, 벤더 서비스 MainPID/시작 시각 불변 |
| Evidence Status | ROBOT_STATE_CHANGING 설치·빌드 PASS, ROBOT_COMMAND_FREE_RUNTIME 검증 PASS. 제어기 실행·모터 명령 없음. 실기 거동 NOT_TESTED |

되돌리기: 로봇에서 `tar -xzf docs/exp/2026-10-19/heading_bundle_deployment/before_deployment.tar.gz`로 `src/tita_controller`, `run_flashsac.sh`, `install/tita_controller`를 복원한다(백업에 설치본 포함).

## 실기 실행 (운영자)

```bash
ros2 launch tita_controller flashsac.launch.py output_enabled:=true policy:=flashsac_headw0_50000
```

- 필터는 auto라 none이 된다.
- RL 진입 전 idle·sit 상태에서 로봇을 1 s 이상 가만히 두어야 gyro 바이어스가 추정된다. 콘솔에 `heading gyro bias ...` 줄이 찍힌다.
