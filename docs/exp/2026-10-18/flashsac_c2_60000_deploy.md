# C2_60k bundle 배포 (legs 60/1.5, 선택형 `policy:=flashsac_c2_60000`)

Execution Domain:
- `DESKTOP_DRY_RUN`: bundle 생성, launch 검증, C++/Python parity.
- `ROBOT_READ_ONLY`: SBC 사전 해시 확인.
- `ROBOT_STATE_CHANGING`: operator가 2026-10-18에 승인한 리소스 배포와 SBC 빌드만 했다.
- `ROBOT_COMMAND_FREE_RUNTIME`: SBC에서 ONNX 추론만 확인했다.
- 컨트롤러·서비스·MCU 모드·모터 명령은 실행하지 않았다.

| 항목 | 값 |
|---|---|
| Policy checkpoint SHA256 | `b4c8ae072787c3119864e75c2ebfbaf8284a02976dc68f1f282ad9480ae2e116` (C2 `tita_flash_sac_114500_483968/model_60000`, task `DDT-Velocity-Flat-Tita-My-LegScale-Reward-v0`) |
| ONNX SHA256 | `b12e40267bb3247762b0dd6283bd9f9cafffac52597ca74b387790bb4e925b7f` |
| config SHA256 | `9561fd1a7d9e5f75a1a9916e0c32d4a705109c4795dac9636fbac0ad877ffde1` |
| manifest SHA256 | `828a30fb…` |

**Evidence Status:**
- **PASS**: bundle·launch 검증, C++ 어댑터 parity, SBC 빌드·설치 검증, SBC C++ ONNX Runtime parity.
- **NOT_TESTED**: 실기 동작.

선정 근거는 [legscale sim2sim](flashsac_legscale_sim2sim.md) 3a절이다.

## 변경

- **신규 bundle:** `sim2real/tita_ws/src/tita_controller/policies/flashsac_c2_60000/`
  - [`test/sim2real/make_flashsac_c2_60000_bundle.py`](../../../test/sim2real/make_flashsac_c2_60000_bundle.py)로 평가 전용 export에서 만들었다.
  - ONNX는 바꾸지 않았다.
  - config는 A80k bundle과 같은 command 범위 override(1.0/1.0)만 적용했다.
  - 게인은 학습 기본값이다: 다리 60/1.5, 휠 Kd 0.5, 상한 60/12. 배포 쪽 다리 보상은 없다.
- **`flashsac.launch.py`:**
  - `BUNDLES` 해시 고정표와 `policy` 인자를 추가했다. 선택지는 `flashsac_80000`(기본, 변경 없음)과 `flashsac_c2_60000`이다.
  - `validate_policy(policy_dir)`는 bundle 이름으로 해시를 고른다. 고정되지 않은 bundle은 거부한다.
  - runner에 `TITA_POLICY_BUNDLE`를 전달한다.
  - [diff](flashsac_c2_60000_deploy/flashsac.launch.py.diff)
- **`run_flashsac.sh`:**
  - `TITA_POLICY_BUNDLE`을 검증하고, 그 값을 launch `policy:=`로 넘긴다.
  - log 이름을 `<bundle>_<time>_…`로 정하고, summary에 bundle과 checkpoint를 기록한다.
  - policy_dir를 선택한 bundle로 둔다.
  - [diff](flashsac_c2_60000_deploy/run_flashsac.sh.diff)
- **`README.md`:** 사용법과 위험을 적었다. [diff](flashsac_c2_60000_deploy/README.md.diff)
- **바꾸지 않은 것:** C++ 소스·실행 파일(`tita_node` SHA256 `80c912f1…` 전후 동일), `flashsac_80000` bundle(무릎 92/2.3), state machine, 필터 옵션.
- **수정 전 원본:** [`before/`](flashsac_c2_60000_deploy/before/), [expected_before.sha256](flashsac_c2_60000_deploy/expected_before.sha256).

## 검사

- **배포 전 SBC 상태:** 수정 대상과 관련 파일 9개가 로컬 원본과 SHA256 일치했다. 컨트롤러는 미실행, bringup은 inactive였다.
- **launch 검증:** 두 bundle의 해시가 통과했다.
  - C2 파라미터: kp 60, kd 1.5, 휠 0.5, 상한 60/12, 관측 33, action 8, 50 Hz, command 1.0/1.0.
  - 고정되지 않은 bundle(`flashsac_75000`)은 거부된다.
  - [log](flashsac_c2_60000_deploy/launch_validation.log)
- **C++ 어댑터 parity** (`test_sim2real_parity.py`): obs 최대 오차 1.2e-7, RL 토크 7.2e-6 N m, state machine 1.17e-4 N m, mismatch 0/6000이다. [log](flashsac_c2_60000_deploy/adapter_parity.log)
- **SBC deploy_build** ([log](flashsac_c2_60000_deploy/remote_build.log)):
  - 1차 시도는 `payload.sha256`이 상대경로라 백업·압축 해제 전에 중단됐고, SBC는 바뀌지 않았다([log](flashsac_c2_60000_deploy/remote_build_attempt1_sha_path.log)).
  - 경로를 고친 2차 시도는 사전 해시·payload·source 해시가 통과했고, colcon build도 PASS(1.28 s)였다.
  - 백업은 SBC `~/tita_ws/docs/exp/2026-10-18/flashsac_c2_60000_deploy/before_deployment.tar.gz`에 있다.
- **SBC verify** ([log](flashsac_c2_60000_deploy/remote_verify.log)): PASS.
  - 설치본 cmp와 두 bundle 해시가 통과했다.
  - C2 게인이 60/1.5이고 A80k bundle은 그대로임을 확인했다.
  - C++ ONNX Runtime 256 sample, 최대 action 오차 2.4e-6([runtime_parity.json](flashsac_c2_60000_deploy/runtime_parity.json)).
  - 실행 파일은 변하지 않았다.
- **배포 후 로컬 소스와 SBC:** 10개 파일 SHA256이 일치한다([log](flashsac_c2_60000_deploy/local_vs_sbc_after.log)).

## 실행 (operator)

```bash
ros2 launch tita_controller flashsac.launch.py output_enabled:=true policy:=flashsac_c2_60000
```

- `policy:=`를 빼면 기존 A80k(무릎 92/2.3)가 실행된다. log 이름이 `flashsac_c2_60000_…`인지 확인한다.
- **시험 순서 제안:**
  1. 정지 20 s 이상
  2. 전후진 0.3 m/s
  3. yaw
- **감시 항목:**
  - 25 Hz 교번(소리, |Δa|, lag-1): 나오면 즉시 return_to_sit한다.
  - 전진 drift: 무릎만 약하면 sim에서 +0.11 m/s였다.
  - 후진·yaw 추종 약화: sim에서 −0.6 명령에 약 −0.4 m/s였다.
- **게인 조정:** 결과를 본 뒤 operator가 정한다. C2와 무릎 92 조합은 이중 보상이라 sim에서 +0.16…+0.25 m/s 전진 drift였다.
- **되돌리기:** `policy:=` 없이 실행하면 된다. 소스와 설치본을 원래대로 돌리려면 backup tar를 쓴다.

## 파일

- **로컬 stage:** [`flashsac_c2_60000_deploy/`](flashsac_c2_60000_deploy/) — payload, 해시, 로그, diff.
- **신규 스크립트:**
  - [`test/sim2real/deploy_flashsac_c2_60000.sh`](../../../test/sim2real/deploy_flashsac_c2_60000.sh)
  - `make_flashsac_c2_60000_bundle.py`
  - `test/sim2real/flashsac_c2_60000_work/`(runtime fixture)
- **`./scripts/agent-check.sh`:** [log](flashsac_c2_60000_deploy/agent_check.log).
