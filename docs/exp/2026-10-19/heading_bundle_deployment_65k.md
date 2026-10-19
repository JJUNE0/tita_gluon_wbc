# flashsac_headw0_65000 배포 준비 (2차, 번들 추가만)

- Execution Domains: DESKTOP_DRY_RUN (준비·검증), ROBOT_STATE_CHANGING (설치·빌드, 운영자 승인 2026-10-19 "65k 로 로봇에 이식하고 빌드"), ROBOT_COMMAND_FREE_RUNTIME (로봇 검증)
- Policy Checkpoint SHA256: `ff083cbfc8a8571009a27454e75dc88463e9ebc796fa79e8782ccb4a5bea239d` (ONNX `ede50fde5cc1863758d2c50e70f7902cafb31e2a677c985e0d69b80c2560be0b`, 번들 config `804c94a365ccc4b0d9b3bf08022699d81012ccd251d8606a4646624c88ed1db2`)
- Evidence Status: 데스크톱 PASS, 로봇 설치·검증 PASS, 실기 거동 NOT_TESTED
- 선택 근거: `flashsac_headw0_50000_142158_review.md`의 "체크포인트 재선정" 절

## 변경

- 로봇에서 바뀌는 파일:
  - `src/tita_controller/launch/flashsac.launch.py`, `run_flashsac.sh` (번들 등록)
  - 새 번들 `policies/flashsac_headw0_65000/`
  - 검증 fixture
- C++ 소스는 1차 배포본 그대로라, 빌드는 리소스 설치만 한다.
- 배포 전 기대 해시(`expected_before.sha256`): 1차 배포 payload와 같은 5개 파일 버전.
- 실행: `TITA_HEADING_BUNDLE=flashsac_headw0_65000 TITA_HEADING_STAGE=heading_bundle_deployment_65k test/sim2real/deploy_heading_bundle.sh deploy_build|verify`

## 데스크톱 검증 (PASS)

| 검사 | 결과 |
|---|---|
| 번들 생성 (`prepare_heading_bundle.py 65000`) | 해시, 관측 35(warmup 0), MA2 없음, 로봇·제어 설정, Torch 일치 |
| C++ 대 Python heading parity | 1.2e-7 (heading 0) |
| 로봇 검증 스크립트 데스크톱 실행 | 7/7 PASS, ONNX 대 Torch 3.3e-6 (`heading_bundle_deployment_65k/desktop_verify.json`) |

## 로봇 (2026-10-19 15:34 KST, `tita`, Humble aarch64)

로그는 `heading_bundle_deployment_65k/deploy_console.log`, `verify_console.log`, `robot/`에 있다.

| 단계 | 결과 |
|---|---|
| 사전 점검 (읽기 전용) | 덮어쓸 5개 파일이 `expected_before.sha256`과 일치한다. overlay 제어기는 미실행, 65k 번들은 없었다. 벤더 `tita-bringup.service`는 active(MainPID 350)이고 건드리지 않았다 |
| 전송 | payload SHA256 `c84f0a0f…07e3c8`, 배포 스크립트 `8113f37e…` 양쪽 일치 |
| `deploy_build` | 해시 확인 OK. 백업 `before_deployment.tar.gz`(`robot/backup.sha256`, `deaf7105…afd060`). `tita_controller` 빌드 2.0 s(리소스 설치만), 성공 |
| `verify` | 7/7 PASS (`robot/arm_verify.json`) |
| `tita_node` 실행 파일 | 배포 전후 같다(C++ 변경 없음) |
| 50k 번들 | 설치본에 그대로 남아 있다. 되돌림용 |

`verify` 세부:
- ARM ONNX 대 Torch 3.0e-6, ARM C++ heading parity 1.2e-7
- SHA 고정, heading 파라미터, 필터 none, 조이스틱 상한 확인
- 설치 파일 cmp 일치, `ldd`에 not found 없음
- 벤더 서비스 MainPID와 시작 시각 불변

Evidence Status: 설치·빌드·검증 PASS. 제어기 실행·모터 명령은 없었다. 실기 거동 NOT_TESTED.

되돌리기: 로봇에서 `tar -xzf docs/exp/2026-10-19/heading_bundle_deployment_65k/before_deployment.tar.gz`. 또는 `policy:=flashsac_headw0_50000`으로 실행한다.

## 실기 실행 (운영자)

```bash
ros2 launch tita_controller flashsac.launch.py output_enabled:=true policy:=flashsac_headw0_65000
```

- RL 진입 전 idle·sit 상태에서 1 s 이상(가능하면 5 s) 가만히 두면 gyro 바이어스가 추정된다. 콘솔에 `heading gyro bias ...` 줄이 찍힌다.
- 이번 실행의 확인 항목: 제자리 회전 중 후진 원호와 허벅지 굽힘(50k: −0.35 m/s, 반경 0.54 m), 정지 yaw, 25 Hz 다리 떨림 소리
