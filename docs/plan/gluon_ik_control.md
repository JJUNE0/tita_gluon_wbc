# GLUON 2L6/4L3 Cylindrical-Workspace IK Control Plan

## 1. 목적과 범위

이 문서의 목표는 다음 폐루프를 단계적으로 구축하는 것이다.

```text
keyboard cylindrical target (base_link X/r/theta)
  -> position-only differential IK
  -> axis_joint_1..6 position targets [rad]
  -> Isaac Lab position drives
  -> simulated joint/EE state feedback
  -> target and current-EE visualization

later:
the same ROS 2 joint-space contract
  -> read-only real-to-sim mirror
  -> shadow IK comparison
  -> operator-gated real robot position control
```

첫 구현의 실행 도메인은 `VALIDATION_SIM`이다. ROS 2와 실물 명령은 이 단계에 포함하지 않는다. 최종 목표는 Isaac Sim과 실물 GLUON을 ROS 2로 동기화하는 것이지만, 실물 명령은 별도의 `ROBOT_STATE_CHANGING` 승인 및 검증 단계를 통과한 뒤에만 추가한다.

## 2. 확인한 기준 코드와 현재 상태

2026-08-04 기준으로 다음 로컬 코드를 확인했다.

- 프로젝트 모델 계약: `sim2sim/gluon_2L6_4L3_urdf/config/model_contract.json`
- 시뮬레이션 URDF: `sim2sim/gluon_2L6_4L3_urdf/urdf/gluon_2L6_4L3_sim.urdf`
- IsaacLab asset 설정: `lab/ddt_lab/ddt_lab/assets/gluon.py`
- 기존 reach 환경: `lab/ddt_lab/ddt_lab/tasks/manager_based/manipulation/reach/joint_pos_env_cfg.py`
- IsaacLab URDF 변환기: `/home/cocel/isaac/IsaacLab/scripts/tools/convert_urdf.py`
- IsaacLab Differential IK 예제: `/home/cocel/isaac/IsaacLab/scripts/tutorials/05_controllers/run_diff_ik.py`
- IsaacLab position-only IK 구현: `source/isaaclab/isaaclab/controllers/differential_ik.py`
- IsaacLab 키보드 장치: `source/isaaclab/isaaclab/devices/keyboard/se3_keyboard.py`
- IsaacLab 기준 리비전: `549768529e3`

현재 모델 계약은 아래와 같다.

| 항목 | 계약 |
|---|---|
| 가동 관절 | `axis_joint_1` ... `axis_joint_6` |
| ID6 기준/리밋 | `turns=0 -> q6=0`, `[-150, +150] deg` |
| end effector body | `link6` |
| joint 단위 | rad |
| 목표점 좌표계 | `base_link` |
| q=0 EE 위치 | 약 `[0.57620, -0.00002, -0.13600] m` |
| physics/control rate | 200 Hz / 50 Hz |
| base | fixed |

선행 해결이 필요한 불일치는 다음과 같다.

1. `assets/gluon.py`의 description 경로가 현재 존재하지 않는 저장소 루트의 `gluon/gluon_2L6_4L3_urdf`를 가리킨다. 이를 `sim2sim/gluon_2L6_4L3_urdf` 또는 명시적인 모델 계약 기반 경로로 고쳐야 한다.
2. ID6의 `direction=+1`과 36:1 감속비는 provisional이다. q6=0 hold에는 부호가 영향 없지만 signed nonzero command 전에 실물 방향을 확인해야 한다.
3. 시뮬레이션 충돌 형상은 링크별 AABB 근사다. 자유공간 IK 검증에는 사용할 수 있지만 장애물 회피나 self-collision 안전성의 근거로 사용해서는 안 된다.

위 항목의 정적 확인 상태와 P0 Isaac Sim 런타임 검증은 2026-08-05 기준
`PASS`이다. 단, ID6 방향의 실물 검증과 정밀 collision 검증은 여전히
후속 단계 범위다.

## 3. 중요한 설계 결정

### 3.1 HOME/WORK 분리와 position-only IK, q6=0 hold

GLUON은 6개의 가동 관절을 사용한다. 다만 첫 버전은 end effector 위치 `(x, y, z)`만 제어하고 ID6은 `q6=0`으로 hold한다. 이렇게 하면 position-only IK의 여유 자유도 때문에 wrist가 불필요하게 회전하는 것을 막을 수 있다. 자세는 측정·표시하되 첫 제어 목표에는 넣지 않으며, ID6 방향 검증 후 6D pose IK를 별도 단계로 추가한다.

q=0은 `sigma_min`이 약 `2.5e-5`인 거의 완전 신전 특이 자세이므로 Cartesian IK의 작업 시작점으로 사용하지 않는다. GUI는 두 모드를 명시적으로 분리한다.

- `HOME`: `[0, 0, 0, 0, 0, 0] rad`, joint-space position target
- `MOVE_TO_WORK`: `[0, 0.8, 1.6, 0.8, 0, 0] rad`로 기본 40 deg/s 이하 slew 이동
- `WORK`: 위 자세 도달·안정화 뒤 position-only DLS를 활성화

WORK 자세의 시뮬레이션 EE 위치는 약 `[0.4620, 0.0219, -0.1359] m`이고 `sigma_min=0.0206`이다. q=0 대비 최소 특이값이 약 800배 개선되며 모든 runtime soft limit 안에 있다.

WORK 모드의 DLS는 damping `0.01`, gain `2.0`, nominal-pose nullspace gain `0.1`에서 시작한다. 모든 joint command는 기본 40 deg/s로 제한하고, operator goal과 현재 EE 사이의 local servo target lead는 10 mm로 제한한다. 속도는 `--keyboard-speed-m-s`, `--trajectory-speed-m-s`, `--max-joint-slew-deg-s`로 낮추거나 높일 수 있다. 이 값들은 2026-08-06 자동 회귀를 통과한 시뮬레이션 기준값이며 실물의 최종 튜닝값으로 간주하지 않는다.

### 3.2 목표점과 IK 계산은 `base_link` 좌표계

- 사용자 target은 항상 `base_link` 기준 meter 단위로 저장한다.
- PhysX의 world-frame EE pose는 `subtract_frame_transforms()`로 base frame에 변환한다.
- marker를 그릴 때만 목표점을 다시 world frame으로 변환한다.
- HOME과 WORK 전환은 Cartesian target이 아니라 slew-limited joint target으로 수행한다.
- WORK 진입 순간 target은 현재 EE 위치로 설정해 Cartesian command 불연속을 방지한다.

현재 CAD `base_link`는 화면의 world frame과 Y축 기준으로 -90 deg 회전되어
있다. 따라서 Isaac viewport에서의 축 대응은 `base +X = world +Z`,
`base +Y = world +Y`, `base +Z = world -X`이다. joint1 origin도 base에서는
`[0.1205, -0.000018, 0] m`이지만 viewport world에서는 거의
`[0, 0, 0.1205] m`이다. 키 매핑과 상태창에 이 대응을 명시하며, 추후
operator 선택형 `base_link`/`world` jog frame을 추가할 수 있다.

### 3.3 현재 실물 gain을 PhysX gain 숫자로 복사하지 않음

현재 실물 드라이브의 위치 gain은 모터 내부 cascade controller의 단위이고, IsaacLab `ImplicitActuatorCfg`의 stiffness `[Nm/rad]`, damping `[Nm s/rad]`와 직접 같은 값이 아니다.

따라서 1차 simulation은 현재 `SIM_NOMINAL` 설정을 사용한다.

- joint 1-2: stiffness 80, damping 4
- joint 3-5: stiffness 40, damping 2
- position reference만 IK 결과로 전달

이후 실물의 작은 step response에서 rise time, overshoot, settling time, steady-state error를 측정하고, 그 응답을 맞추도록 시뮬레이션 stiffness/damping/friction/armature를 식별한다. 실물 firmware gain 자체는 이 작업에서 변경하지 않는다.

### 3.4 URDF-to-USD는 재현 가능한 생성물로 관리

입력은 world link가 제거된 `gluon_2L6_4L3_sim.urdf`로 통일한다. 변환 시:

- `fix_base=True`
- `merge_fixed_joints=False`: body/frame topology를 변환 전후 동일하게 보존
- importer drive target은 `none`: gain의 단일 source는 `ImplicitActuatorCfg`
- root에 model contract의 `root_rotation_wxyz` 적용

예상 출력은 `sim2sim/gluon_2L6_4L3_urdf/usd/gluon_2L6_4L3.usd`이다. 생성 시 input URDF SHA256, IsaacLab revision, importer 옵션, output USD SHA256을 manifest에 기록한다. USD를 직접 수정하지 않고 URDF와 변환 설정에서 재생성한다.

### 3.5 active W2 원통 좌표 작업공간

W0/W1 직교 상자는 초기 검증 이력으로 유지하고, 현재 active command gate는
joint1의 `base_link +X` 회전축을 중심으로 한 W2 원통 부채꼴이다.

```text
X = base_link X
r = sqrt(Y^2 + Z^2)
theta = atan2(Z, Y)
```

- X: `[0.36, 0.48] m`
- r: `[0.13, 0.21] m`
- 절대 theta: `[-175, +35] deg`
- 구현 좌표: 중심 `-70 deg`에 대한 offset `[-105, +105] deg`
- 기하학적 부피: `0.0059816 m^3`, W1 대비 약 `3.258배`

theta offset은 중심각 기준 `[-pi, pi]`로 wrap하여 절대각 `-180/+180 deg`
분기점을 안전하게 통과한다. 자동 경로 내부에서는 `-105 -> +105 deg`를
unwrapped 값으로 보간하여 의도하지 않은 최단경로 점프를 막는다. 최초
`+-120 deg` 후보는 FK 표본상 도달 가능했지만 연속 DLS 경로에서 q1 soft
limit에 걸렸으므로 폐기했다.

## 4. 제안 파일 구조

구현 단계에서 아래와 같이 구성한다.

```text
sim2sim/gluon_2L6_4L3_urdf/
  usd/
    gluon_2L6_4L3.usd
    manifest.json

lab/ddt_lab/ddt_lab/assets/
  gluon.py                         # validated USD-based ArticulationCfg

lab/ddt_lab/scripts/gluon/
  convert_gluon_urdf_to_usd.py     # reproducible converter wrapper
  run_gluon_keyboard_ik.py         # GUI keyboard IK application
  smoke_gluon_asset.py             # USD/model contract test

test/
  test_gluon_ik_math.py            # frame, clamp, limits, DLS unit tests
  analyze_tita_gluon_reachability.py # TITA-frame collision-aware voxel map
  test_tita_gluon_reachability.py   # mount transform/voxel topology tests
  eval_logs/
    tita_gluon_reachability_q6_zero.npz # representative q + surface artifact

tita_gluon_ws/src/gluon/           # later ROS 2 phase only
  config/gluon_calibration.yaml    # turns <-> q mapping source
```

`run_gluon_keyboard_ik.py`는 production validation application이고, 임시 진단/단위 테스트는 AGENTS.md 규칙에 따라 모두 `test/` 아래에 둔다.

## 5. 단계별 구현 계획

### P0. 모델 계약과 asset import 정합화

실행 도메인: `VALIDATION_SIM`

작업:

1. `assets/gluon.py`의 잘못된 description 경로를 고친다.
2. 6-DOF joint order와 `axis_joint_6=revolute`, `link6=EE`를 단일 상수/manifest에서 읽도록 정리한다.
3. reach smoke의 6-DOF action과 joint order를 model contract와 대조한다.
4. 현재 runtime URDF import로 asset smoke를 먼저 통과시켜 URDF 자체를 기준선으로 고정한다.

통과 기준:

- fixed base
- joint order가 정확히 `axis_joint_1..6`
- body list에 `link6` 존재
- 총질량 `4.267611380601286 kg` 허용오차 내 일치
- q=0 EE position이 model contract와 1 mm 이내 일치
- 모든 joint limit가 model contract와 일치
- NaN/Inf 및 root drift 없음

### P1. URDF를 USD로 변환하고 등가성 검증

실행 도메인: `VALIDATION_SIM`

작업:

1. converter wrapper와 manifest를 만든다.
2. 고정 관절을 merge하지 않은 fixed-base USD를 생성한다.
3. `GLUON_2L6_4L3_CFG`가 생성된 USD를 로드하도록 변경한다.
4. URDF-import asset과 USD asset의 q=0 및 여러 joint sample pose에서 FK를 비교한다.

통과 기준:

- joint/body 이름, 순서, limits, mass가 P0 기준과 동일
- q=0 및 joint sample에서 EE position 차이 1 mm 이하
- quaternion 부호 동치까지 고려한 orientation 차이 0.5 deg 이하
- USD 재생성 결과와 manifest hash가 추적 가능

### P2. 키보드 원통 좌표 목표점과 시각화

실행 도메인: `VALIDATION_SIM`

입력 매핑:

| 키 | target 변화 (`base_link`) |
|---|---|
| W / S | +X / -X |
| A / D | +r / -r |
| Q / E | +theta / -theta 방향의 접선 이동 `r*dtheta` |
| R | target을 현재 EE 위치로 재설정 |
| H | joint-space HOME `[0, 0, 0, 0, 0, 0] rad`로 복귀 |
| Z | joint-space WORK `[0, 0.8, 1.6, 0.8, 0, 0] rad`로 이동 후 IK 활성화 |
| P | W2의 8개 원통 꼭짓점 폐곡선 trajectory 1회 시작/실행 중 취소 |
| SPACE | target update pause/resume |
| ESC | 정상 종료 |

IsaacLab `Se3Keyboard`의 position 3축을 `[dX, dR, r*dtheta]` metric increment로
재해석한다. 키 입력은 50 Hz control tick에서 적분하고, theta 입력은 현재
반경으로 나누어 각도 증가량을 만든다. 검증된 기본 metric keyboard speed는
`0.10 m/s`이며 CLI로 조정한다.

시각화:

- 목표점: sphere marker
- 현재 EE: frame marker
- W2의 8개 원통 꼭짓점: 자홍색 sphere marker
- 축/반경 edge와 theta 원호: 노란색 sphere sample로 폐곡선 표시
- 불투명 cuboid/surface는 표시하지 않으며 로봇을 가리지 않는 점과 경계선만 유지
- target이 workspace/limit 때문에 거부되면 marker 색상 변경
- viewport 또는 작은 UI에 target XYZ, current XYZ, error norm, IK state 표시

50만 관절 샘플에서 얻은 0.47555 m outer reach 수치는 분석 자료로만
유지하며 GUI에는 표시하지 않는다. 현재 controller가 승인하는 영역은
별도로 표시된 W2뿐이다.

### P3. position-only DLS IK 폐루프

실행 도메인: `VALIDATION_SIM`

각 50 Hz control tick에서 다음 순서로 수행한다.

1. HOME에서는 H를, WORK 진입에는 Z를 사용하며 두 자세 전환은 joint-space slew limit로 수행한다.
2. WORK 진입이 완료된 뒤 키보드 입력을 target `[X,r,theta]`에 적분하고 XYZ로 변환한다.
3. target을 검증된 workspace와 사용자 설정 속도로 clamp하고 현재 EE보다 최대 10 mm만 앞서도록 local servo target을 제한한다.
4. PhysX Jacobian에서 fixed-base `link6` index를 사용한다. IsaacLab 규칙상 fixed-base Jacobian body index는 articulation body index보다 1 작음을 명시적으로 검사한다.
5. PhysX COM Jacobian을 `link6` origin으로 point-shift하고 `base_link` frame으로 회전한다.
6. current EE pose를 `base_link`로 변환한다.
7. DLS IK로 joint 1-5의 `q_candidate`를 계산하고 q6 target은 0으로 유지한다.
8. 6개 관절의 URDF soft limits, 1-tick joint delta, joint velocity를 clamp한다.
9. `q_des`를 `robot.set_joint_position_target()`에 전달한다.
10. Cartesian error, q/q_des, saturation, smallest singular value, control state를 기록한다.

초기 안전 파라미터 후보:

- physics 200 Hz, IK/command 50 Hz
- keyboard cylindrical metric speed 기본값 `0.10 m/s`
- W2 trajectory metric speed 기본값 `0.06 m/s`
- 반경-only edge speed는 conditioning 완화를 위해 `0.5x` 적용
- per-joint q command slew 기본값 `40 deg/s`
- soft-limit factor는 현재 0.95 유지
- baseline W0: x `[0.43, 0.49]`, y `[-0.01, 0.05]`, z `[-0.17, -0.10]` m
- historical W1: x `[0.36, 0.48]`, y `[-0.08, 0.09]`, z `[-0.20, -0.11]` m
- active W2: X `[0.36,0.48] m`, r `[0.13,0.21] m`, theta `[-175,+35] deg`
- operator goal-to-current EE lead limit 10 mm

W2 꼭짓점 trajectory는 다음 순서로 한 번 실행한 뒤 마지막 위치를 hold한다.
각 비트는 각각 X/r/theta에서 `0=lower`, `1=upper`를 뜻한다.

```text
000 -> 001 -> 101 -> 111 -> 011 -> 010 -> 110 -> 100 -> 000
```

- 원통 metric planner 속도: 기본 `0.06 m/s`, 반경-only edge `0.03 m/s`
- planner goal-to-current EE lead gate: `8 mm`
- local DLS servo target lead limit: `10 mm`
- 꼭짓점 도달 판정: 실제 EE 오차 `5 mm` 이하를 5 control ticks 유지
- P를 HOME에서 누르면 WORK로 자동 전환한 뒤 1회 실행
- 실행 중 P/H/Z/R은 trajectory를 취소하거나 해당 모드 전환을 우선함

이 경로는 8개 꼭짓점을 중복 없이 순회하는 Hamiltonian cycle이다. X/r/theta
좌표 공간의
12개 edge를 각각 정확히 한 번만 지나는 Euler cycle은 모든 꼭짓점 차수가
3인 구조상 존재하지 않으므로, 중복 왕복 없는 operator 검증 경로에는 8개
edge만 사용한다.

W2는 FK 표본과 연속 runtime IK를 통과한 command gate이지 충돌 없는 전체
작업반경을 뜻하지 않는다. self/environment collision mesh 검증 전에는 실물
작업공간으로 승인하지 않는다.

통과 기준:

- W2의 8개 꼭짓점 target에서 steady-state position error 5 mm 이하
- joint soft limit 및 velocity limit 위반 0회
- target hold 시 진동/발산/NaN 없음
- 특이점 또는 불가능한 target에서 큰 q jump 없이 `SATURATED`/`UNREACHABLE` 상태 표시
- reset 직후 command discontinuity 없음

### P4. 시뮬레이션 자동 회귀 검증

실행 도메인: `VALIDATION_SIM`

GUI 수동 시험과 별도로 headless trajectory test를 만든다.

- WORK 자세 진입 및 Cartesian command continuity
- WORK 자세 주변 ±X/±r/±theta 접선 step
- W2 8개 꼭짓점 및 위 9-waypoint 폐곡선 1회 추종
- joint-limit 근처의 거부/포화 시험
- singular configuration 후보
- reset 및 pause/resume

진동 진단에는 `--log-segment-dynamics --status-log-every-controls 0`을 사용한다.
각 trajectory segment별로 다음 200 Hz/50 Hz 지표를 집계하여, 화면 관찰 없이
kinematic command oscillation과 actuator torque saturation을 구분한다.

- `sigma_min`, Cartesian goal/servo error, slew/target-lead 제한 횟수
- 관절별 `q_des-q`, 속도, 가속도, command slew
- implicit-PD의 estimated computed/applied torque와 effort-limit 비율
- torque clipping 횟수, 실제 관절 속도 및 command 방향반전 횟수

ImplicitActuator의 torque 값은 PhysX가 노출하는 실제 solver torque가 아니라
`Kp(q_des-q)+Kd(qdot_des-qdot)+tau_ff`로 재계산한 추정치임을 로그 계약에
명시한다.

각 실험 결과는 `docs/exp/YYYY-MM-DD/` 아래에 input hashes, IsaacLab revision, metrics, `PASS/SUSPICIOUS/FAIL`을 기록한다. `./scripts/agent-check.sh`와 가장 작은 관련 smoke test를 매 변경마다 실행한다.

### P4.5. TITA 장착 기준 collision-aware reachability map

실행 도메인: `VALIDATION_SIM`

W2는 반복 제어에 사용할 보수적인 command gate이고 GLUON의 전체 작업반경이
아니다. TITA 탑재 시 실제 envelope를 얻기 위해 다음 별도 오프라인 분석을
사용한다.

1. q6는 0으로 고정하고 q1-q5를 scrambled Sobol sequence로 샘플한다.
2. 모든 관절 limit에서 기본 5 deg margin을 제외한다.
3. link6 원점 FK와 q1-q5 linear Jacobian을 계산하고
   `sigma_min >= 0.01`만 유지한다.
4. 합성 `tita_gluon_2L6_4L3.urdf`의 장착 transform으로 위치를 TITA
   `base_link` frame에 변환한다.
5. hpp-fcl collision mesh로 TITA body/지그 대 arm, arm base 대 distal link,
   비인접 arm link self-collision의 51개 pair를 검사한다. 기본 clearance는
   10 mm다.
6. 통과한 위치를 10 mm voxel로 저장하고 WORK seed가 포함된 26-neighbor
   Cartesian 성분만 별도 표시한다.
7. 각 voxel에 hit count, 최대 `sigma_min`, 최대 joint margin, 대표 q를
   저장한다. 경계 mesh는 미관용 smoothing이나 hole filling 없이 점유 voxel
   면만 생성한다.

기본 실행:

```bash
/home/cocel/isaac/env_isaaclab/bin/python \
  test/analyze_tita_gluon_reachability.py \
  --output test/eval_logs/tita_gluon_reachability_q6_zero.npz
```

GUI에서 계산된 비정형 표면을 선택적으로 겹쳐 보려면 다음처럼 실행한다.
표면은 현재 standalone GLUON base frame으로 역변환되어 표시되며 collision
object로 등록되지 않는다.

```bash
/home/cocel/isaac/env_isaaclab/bin/python \
  lab/ddt_lab/scripts/gluon/run_gluon_keyboard_ik.py \
  --reachability-map test/eval_logs/tita_gluon_reachability_q6_zero.npz \
  --reachability-opacity 0.10
```

TITA 본체와 장착된 GLUON을 함께 확인하는 정적 viewer는 다음 명령을 사용한다.
TITA는 policy standing 자세, GLUON은 WORK 자세로 표시되고 지도는 TITA
`base_link` 좌표를 그대로 사용한다.

```bash
/home/cocel/isaac/env_isaaclab/bin/python \
  test/view_tita_gluon_reachability.py \
  --reachability-opacity 0.04
```

이 지도는 다음을 증명하지 않는다.

- 비점유 voxel이 도달 불가능하다는 것
- 점유 voxel 안의 모든 연속점이 도달 가능하다는 것
- 두 점유 voxel 사이에 연속 collision-free joint path가 존재한다는 것
- TITA 자세가 변하거나 그리퍼가 추가되어도 동일하다는 것

따라서 target admission에는 근접 점유 voxel과 대표 q를 IK seed로 사용한 뒤,
실제 관절 보간 경로 전체를 다시 collision check해야 한다. 장착 지그 실측,
누락된 TITA collision geometry 보완, tool0/gripper 모델 추가 전 상태는
`SUSPICIOUS`로 유지한다.

### P5. ROS 2 simulation-only interface

실행 도메인: `VALIDATION_SIM` 또는 `DESKTOP_DRY_RUN`

ROS 2를 제어기의 내부 구현과 분리하고 아래 계약을 사용한다.

| Topic | Type | Frame/단위 | 용도 |
|---|---|---|---|
| `/gluon/joint_states` | `sensor_msgs/JointState` | rad, rad/s | sim 또는 real 상태 |
| `/gluon/target_position` | `geometry_msgs/PointStamped` | `base_link`, m | Cartesian 목표 |
| `/gluon/joint_position_command` | `trajectory_msgs/JointTrajectory` | rad | 이름이 포함된 q_des |
| `/gluon/ee_pose` | `geometry_msgs/PoseStamped` | `base_link` | FK 결과 |
| `/gluon/control_status` | diagnostics/custom status | 명시적 state | fault/saturation/owner |
| `/tf` | TF2 | `base_link -> link6` | 공통 frame tree |

`JointTrajectory`는 joint name과 시간을 포함하므로 순서만 암묵적으로 가정하는 float array보다 안전하다. Phase P5에서는 Isaac Sim 양쪽 node만 연결하고 실물 SDK에는 연결하지 않는다.

### P6. read-only real-to-sim 및 shadow mode

실행 도메인: `ROBOT_READ_ONLY`, 이후 `ROBOT_COMMAND_FREE_RUNTIME`

1. 기존 INNFOS reader가 motor turns를 읽는다.
2. `gluon_calibration.yaml`의 공식으로 q를 만든다.

```text
q_urdf = direction * (motor_turns - zero_turns) * 2*pi / gear_ratio
```

3. q를 `/gluon/joint_states`로 발행하고 Isaac articulation을 kinematic mirror로 갱신한다.
4. Isaac FK와 관측된 실제 자세를 비교한다. 외부 자세 센서가 없으면 이 단계의 절대 Cartesian 검증 상태는 `BLOCKED` 또는 `SUSPICIOUS`로 남긴다.
5. shadow mode에서는 키보드 target과 IK q_des를 계산·로그하지만 실물로 command를 보내지 않는다.

필수 확인:

- joint 1-6 mapping과 sign/zero가 calibration YAML과 동일
- joint 6은 `turns=0 -> q6=0`, `+/-150 deg`로 제한되며 signed nonzero command 전에 방향을 검증
- 실물 enable 시 unloaded ID6을 default current mode에 방치하지 않고, ID6을 먼저 단독 enable하여 현재 위치를 즉시 Profile Position hold한 뒤 ID1-5를 enable
- stale timestamp, packet loss, actuator error를 status로 전달
- Minta Actuator Studio 등 다른 프로세스와 SDK/네트워크 command ownership을 공유하지 않음

### P7. staged sim-to-real command

실행 도메인: `ROBOT_STATE_CHANGING`

이 단계는 별도 operator 승인 없이는 수행하지 않는다. 상태 머신은 최소한 다음을 가진다.

```text
DISCONNECTED -> READ_ONLY -> SHADOW -> ARMED -> COMMANDING
                                      \-> FAULT
```

초기 실물 시험 순서:

1. gravity-safe fixture/작업공간과 물리 e-stop 확인
2. 현재 q에서 모든 joint position hold
3. EE target 1-2 mm, 한 축만 이동
4. q_des step/slew, velocity, soft limit 검증
5. 5-10 mm local W0 이동
6. 세 축 조합 및 속도 점진 확대

실물 bridge는 기존 embedded position controller에 reference q만 전달한다. ROS target을 motor turns로 직접 해석하지 않고 반드시 calibration layer를 거친다.

필수 watchdog:

- stale joint state/target
- ROS/SDK disconnect
- actuator error code
- joint soft limit 및 command slew/velocity
- IK residual 및 unreachable target
- current/temperature/voltage limits
- command owner 중복
- operator stop/e-stop

watchdog 발생 시 새 목표 전송을 중지하고 명시적 `FAULT`로 전환한다. 중력 하중이 있는 자세에서 단순 disable이 항상 안전한 정지인지는 별도 검증해야 하므로 stop 정책은 실물 시험 전에 정의한다.

## 6. 구현 순서와 완료 조건

권장 순서는 다음과 같다.

1. P0 모델 계약 정합화
2. P1 재현 가능한 USD 생성 및 URDF/USD 등가성
3. P2 키보드 target marker
4. P3 DLS IK 폐루프
5. P4 자동 회귀
6. P5 ROS simulation-only
7. P6 real read-only/shadow
8. P7 operator-gated real command

첫 마일스톤의 완료 정의는 “Isaac Sim GUI에서 GLUON USD가 로드되고,
W/S/A/D/Q/E로 움직이는 `base_link` 기준 원통 좌표 목표 구를 `link6`가
position-only IK로 추종하며, 5 mm 정확도·joint limits·속도 제한 검증 로그가
남는 상태”이다.

## 7. 현재 리스크와 보류 항목

- ID2와 ID4 calibration repeatability는 아직 provisional이다. simulation IK 구현을 막지는 않지만 P6/P7의 실물 정확도 승인에는 영향을 준다.
- 실제 end-effector TCP가 `link6` origin과 다르면 gripper/tool 장착 전에 별도 `tool0` 고정 frame과 질량/관성을 모델링해야 한다.
- 현재 AABB collision은 자유공간 Phase-A용이다. obstacle avoidance, self-collision, RL reach training 전 collision geometry를 개선한다.
- 6-DOF arm을 position-only로 제어할 때 남는 자유도는 2차 목표에 활용할 수 있지만 첫 구현에서는 q6=0 hold와 joint 1-5 DLS를 먼저 검증한다.
- 실물과 시뮬레이션 gain 수치의 직접 동일시는 금지한다. closed-loop response matching으로 동등성을 평가한다.
- ROS 2 동기화에서 simulator clock과 hardware wall clock의 timestamp 정책, command ownership, loss/reconnect semantics를 P5에서 먼저 확정한다.

## 8. 증거 상태

| 항목 | 상태 | 근거 |
|---|---|---|
| 로컬 IsaacLab position-only DLS API 존재 | `PASS` | 설치 소스 정적 검사 |
| 키보드 3축 입력 API 존재 | `PASS` | `Se3Keyboard` 정적 검사 |
| URDF-to-USD 도구 및 옵션 확인 | `PASS` | `convert_urdf.py` 정적 검사 |
| 현재 6-DOF model contract 확인 | `PASS` | model contract 및 calibration 정적 검사 |
| 현재 GLUON asset runtime import | `PASS` | 2026-08-05 P0 headless runtime 및 reach smoke |
| USD 변환 및 등가성 | `PASS` | 2026-08-05 반복 변환 해시 및 URDF/USD 런타임 FK 비교 |
| WORK pose conditioning | `PASS` | 2026-08-06 soft-limit 및 PhysX Jacobian singular value 검사 (`sigma_min=0.0206`) |
| HOME/WORK mode transition | `PASS` | 2026-08-06 headless joint-space 전환 및 안정화 검사 |
| keyboard IK closed-loop | `SUSPICIOUS` | 2026-08-06 headless 6방향 10 mm 회귀 PASS, 변경 후 operator key 입력 재확인 대기 |
| W2 cylindrical trajectory | `PASS` | 2026-08-06 headless 9/9 waypoint, final error 4.738 mm, limit violations 0 |
| W2 smooth-motion acceptance | `SUSPICIOUS` | segment 7 actual velocity sign flips 9회; GUI 육안 재확인 필요 |
| TITA-frame sampled reachability map | `SUSPICIOUS` | 2026-08-07 262,144 Sobol samples, 10 mm clearance hpp-fcl, 141,632 WORK-connected voxels; provisional jig/TITA collisions/tool0 |
| ROS 2 simulation sync | `NOT_TESTED` | P5 작업 |
| real robot sync/control | `NOT_TESTED` | P6-P7, 별도 승인 필요 |

## 9. 다음 구현 세션 실행 체크리스트

아래 체크리스트는 구현 및 재검증 절차다. 각 단계가 `PASS`일 때만 다음
단계로 넘어간다.

### 9.1 Preflight

실행 도메인: `DESKTOP_DRY_RUN`

1. `git status --short`와 현재 branch를 기록한다.
2. `/home/cocel/isaac/IsaacLab` revision이 계획 기준
   `549768529e3`인지 확인한다. 다르면 API 차이를 먼저 재검토한다.
3. `lab/ddt_lab`가 현재 IsaacLab Python 환경에 editable install되어 있는지
   확인한다.
4. 현재 model contract의 URDF SHA256과 실제 파일 SHA256을 대조한다.
5. 실물 SDK, Minta Actuator Studio, ROS 2 hardware bridge는 실행하지 않는다.

중단 조건:

- branch가 `main` 또는 `master`
- 현재 task와 겹치는 미확인 사용자 변경
- URDF/model-contract hash 불일치
- IsaacLab revision/API 불일치

### 9.2 P0 runtime-URDF 기준선

변경 파일:

- `lab/ddt_lab/ddt_lab/assets/gluon.py`
- 필요 시 `lab/ddt_lab/scripts/gluon/smoke_gluon_asset.py`
- 필요 시 `lab/ddt_lab/scripts/gluon/smoke_gluon_reach_env.py`

작업:

1. `GLUON_DESCRIPTION_DIR`를 저장소의 실제
   `sim2sim/gluon_2L6_4L3_urdf`로 수정한다.
2. 아직 `UrdfFileCfg`를 유지한 상태에서 6축 runtime import를 검증한다.
3. q6=0에서 기존 `link6` FK 기준이 유지되는지 확인한다.

예정 명령:

```bash
/home/cocel/isaac/IsaacLab/isaaclab.sh -p \
  lab/ddt_lab/scripts/gluon/smoke_gluon_asset.py --headless

/home/cocel/isaac/IsaacLab/isaaclab.sh -p \
  lab/ddt_lab/scripts/gluon/smoke_gluon_reach_env.py --headless
```

필수 증거:

- joint names: `axis_joint_1` ... `axis_joint_6`
- body names에 `link6` 존재
- total mass `4.267611380601286 kg`
- q=0 EE base position이 model contract와 1 mm 이내
- q6 limit가 정확히 ±150 deg
- finite state 및 fixed-base root drift 없음

### 9.3 P1 USD 생성

생성 파일:

- `lab/ddt_lab/scripts/gluon/convert_gluon_urdf_to_usd.py`
- `sim2sim/gluon_2L6_4L3_urdf/usd/gluon_2L6_4L3.usd`
- `sim2sim/gluon_2L6_4L3_urdf/usd/manifest.json`

wrapper가 고정할 importer 옵션:

```text
input = urdf/gluon_2L6_4L3_sim.urdf
fix_base = true
merge_fixed_joints = false
joint_drive.target_type = none
joint_drive.stiffness = 0
joint_drive.damping = 0
force_usd_conversion = true
```

예정 명령:

```bash
/home/cocel/isaac/IsaacLab/isaaclab.sh -p \
  lab/ddt_lab/scripts/gluon/convert_gluon_urdf_to_usd.py --headless
```

manifest 필수 필드:

- canonical/sim URDF relative path와 SHA256
- output USD relative path와 SHA256
- IsaacLab git revision
- importer option 전체
- 생성 시각과 model ID

USD 생성 후 `assets/gluon.py`는 `UsdFileCfg`를 사용하되 root rotation과
`ImplicitActuatorCfg`를 계속 명시한다. USD importer drive는 사용하지 않는다.

### 9.4 P1 URDF/USD 등가성

테스트 파일:

- `test/test_gluon_urdf_usd_equivalence.py` 또는 동일 목적의 headless test

sample q 후보:

```text
q0       = [0, 0, 0, 0, 0, 0]
q_local1 = [5, -5, 5, -5, 5, 0] deg
q_local2 = [-10, 10, -10, 10, -10, 0] deg
q6_test  = [0, 0, 0, 0, 0, 30] deg
```

필수 통과 기준:

- joint/body names와 순서 완전 일치
- joint limits 완전 일치
- total mass 절대오차 `1e-5 kg` 이하
- 각 sample의 EE position 차이 1 mm 이하
- quaternion 부호 동치를 고려한 orientation 차이 0.5 deg 이하
- q6_test에서 EE position은 거의 유지되고 orientation만 변하는지 확인

### 9.5 P2-P3 keyboard IK application

생성 파일:

- `lab/ddt_lab/scripts/gluon/run_gluon_keyboard_ik.py`
- 순수 계산 helper가 필요하면 production module에 두고 테스트는
  `test/test_gluon_ik_math.py`에 둔다.

제어 루프의 정확한 contract:

```text
physics: 200 Hz
keyboard/IK: 50 Hz (physics 4 step마다 1회)
target coordinates: base_link cylindrical [X, r, theta]
IK joints: axis_joint_1..5
held joint: axis_joint_6 = 0 rad
end effector: link6
controller: position-only absolute DLS
HOME posture: [0, 0, 0, 0, 0, 0] rad
WORK posture: [0, 0.8, 1.6, 0.8, 0, 0] rad
```

IsaacLab `Se3Keyboard`는 key hold 동안 고정 delta를 반환한다. 따라서
`pos_sensitivity = metric_speed_m_s / control_rate_hz`로 설정하고 반환값을
`[dX,dR,r*dtheta]`로 해석한다. 별도로 `dt`를 다시 곱하지 않는다.

IK loop pseudocode:

```python
ee_pos_b, ee_quat_b = subtract_frame_transforms(root_pose_w, ee_pose_w)
if mode in (HOME, MOVE_TO_WORK):
    q_des = slew_toward(q_home if mode == HOME else q_work)
else:
    target_cyl += cylindrical_metric_increment(keyboard.advance()[:3])
    target_cyl = clamp_to_w2_cylindrical_sector(target_cyl)
    target_pos_b = cylindrical_to_cartesian(target_cyl)
    servo_target_b = limit_to_10_mm_from_current(target_pos_b, ee_pos_b)
    jacobian_1to5 = shift_com_jacobian_to_link6_origin_and_base_frame(
        full_jacobian[:, :, joint_ids_1to5]
    )
    q_des_1to5 = bounded_position_dls(
        servo_target_b, ee_pos_b, jacobian_1to5, nominal=q_work
    )
    q_des = clamp_joint_limits_and_40_deg_s_slew(q_des_1to5, q6=0.0)

robot.set_joint_position_target(q_des)
```

fixed-base PhysX Jacobian은 `link6 body_id - 1`을 사용한다. 이 보정은
assert와 로그로 검증하며 body order에 대한 암묵적 상수로 두지 않는다.

GUI 예정 명령:

```bash
/home/cocel/isaac/env_isaaclab/bin/python \
  lab/ddt_lab/scripts/gluon/run_gluon_keyboard_ik.py \
  --reachability-map test/eval_logs/tita_gluon_reachability_q6_zero.npz
```

GUI acceptance checklist:

- 시작 시 HOME q=0이고 target marker가 현재 EE에 나타나며 command jump 없음
- Z를 누르면 설정된 기본 40 deg/s 이하로 WORK 자세에 이동하고 안정화 뒤 `mode=WORK`
- H를 누르면 Cartesian IK를 종료하고 정확한 joint-space HOME으로 복귀
- W/S, A/D, Q/E가 각각 base_link ±X/±r/±theta 접선과 일치
- R은 WORK 모드에서 현재 EE로 target reset
- target sphere와 current EE frame이 동시에 보임
- 화면/로그에 target/current XYZ, error norm, saturation state 표시
- active W2의 여섯 방향 step과 8개 꼭짓점에서 steady error 5 mm 이하
- P trajectory가 8개 고유 꼭짓점과 시작점 복귀까지 9개 waypoint를 모두 도달하고 1회 완료
- q6가 전체 실행 동안 `0 ± 0.5 deg`
- joint soft limit/velocity/slew violation 0회
- unreachable target은 clamp 또는 `UNREACHABLE` 표시되고 q jump 없음

### 9.6 단계별 기록과 종료 조건

각 실행은 `docs/exp/<date>/`에 다음을 기록한다.

- Execution Domain
- URDF/USD SHA256 및 IsaacLab revision
- 실제 실행 명령
- stdout/stderr 핵심 로그
- joint/body/FK/mass 및 IK metrics
- Evidence Status

P0-P3 중 하나라도 `FAIL`이면 다음 단계로 넘어가지 않는다. `SUSPICIOUS`는
원인을 설명하고 해당 범위만 재검증한다. GUI acceptance까지 직접 확인된
뒤에만 첫 마일스톤을 `PASS`로 기록한다.

### 9.7 첫 마일스톤 요구사항-증거 매트릭스

아래 행이 모두 직접 증명되기 전에는 P0-P3 전체를 완료로 판정하지 않는다.
정적 코드 검사나 좁은 단위 테스트를 GUI 폐루프 동작의 대체 증거로 쓰지
않는다.

| 요구사항 | 필수 산출물 | PASS를 증명하는 직접 증거 | 현재 상태 |
|---|---|---|---|
| IsaacLab 6축 모델 계약 정합 | `assets/gluon.py`, P0 smoke | 런타임 joint/body 순서, q6 limit, mass, fixed-base, q=0 FK 로그 | `PASS` |
| 재현 가능한 URDF-to-USD | converter, USD, manifest | 입력/출력 SHA256, revision/options, 동일 입력 재생성 검사 | `PASS` |
| URDF/USD 등가성 | equivalence test와 실험 기록 | 모든 sample의 이름/limit/mass/FK 허용오차 로그 | `PASS` |
| base_link 키보드 원통 target | GUI app와 marker | operator가 ±X/±r/±theta 키 매핑, reset/pause, marker/frame을 직접 확인 | `SUSPICIOUS` |
| q1-q5 position-only DLS, q6 hold | IK app와 math test | W2 오차, q6 오차, limit/slew, singular/unreachable metrics | `PASS` |
| 저장소 회귀 및 추적성 | `docs/exp/<date>/` 기록 | 관련 smoke/test와 마지막 문서 변경 이후 `./scripts/agent-check.sh`의 실제 성공 출력 | `PASS` |

각 phase의 Agy worker 결과는 산출물 후보일 뿐이다. Codex가 위 직접 증거를
독립적으로 확인하고, GUI 항목은 user/operator가 육안 확인해야 최종 상태를
`PASS`로 바꾼다.

## 10. Codex-Agy 순차 agent loop 설계

### 10.1 연결 방식

로컬 CLI `/home/cocel/.local/bin/agy`를 Codex가 subprocess worker로
호출할 수 있다. 별도의 네트워크 bridge가 필요한 구조는 아니다.

```text
user
  -> Codex supervisor
       -> agy worker (bounded implementation task)
       -> inspect git diff and logs
       -> run independent verification
       -> agy --conversation <conversation_id> with exact failure evidence
       -> accept phase or stop
```

확인된 model 후보에는 `claude-sonnet-4-6`,
`claude-opus-4-6-thinking`, `gemini-3.1-pro-high` 등이 있다. 이 값들은
custom agent 이름이 아니라 model slug이므로 `--model`로 선택한다. 첫
구현 worker model은 `claude-sonnet-4-6`, Codex는 scope/evidence
검토자로 두는 구성을 시작점으로 사용한다.

### 10.2 무한 루프 대신 bounded phase loop

각 P0-P3 phase마다 최대 3회 worker iteration을 허용한다.

```text
PRECHECK
  -> WORKER_IMPLEMENT
  -> CODEX_DIFF_REVIEW
  -> LOWEST_RISK_TEST
       PASS -> RECORD_EVIDENCE -> NEXT_PHASE
       FAIL -> FEEDBACK_TO_SAME_CONVERSATION -> WORKER_FIX
       FAIL x3 -> STOP_AND_REPORT
```

동일 blocker가 3회 반복되면 자동 수정 루프를 끝내고 `BLOCKED` 근거를
보고한다. 테스트 실패를 무시하거나 acceptance 기준을 낮춰 다음 phase로
넘어가지 않는다.

### 10.3 Agy 호출 템플릿

첫 작업은 새 conversation으로 실행한다. 짧은 connectivity probe에는
`json`을 사용할 수 있지만, 파일 inspect/edit/test가 포함된 장시간 worker는
진행 상태와 tool call을 볼 수 있도록 `stream-json`을 사용한다.

```bash
agy \
  --model claude-sonnet-4-6 \
  --mode accept-edits \
  --output-format stream-json \
  --print-timeout 30m \
  --print "$(cat /tmp/gluon_p0_prompt.txt)"
```

Codex 검토에서 실패가 발견되면 최초 JSON 응답의 `conversation_id`를
저장하고 같은 conversation을 명시적으로 이어간다.

```bash
agy \
  --conversation <conversation_id> \
  --mode accept-edits \
  --output-format stream-json \
  --print-timeout 30m \
  --print "검증 실패 로그와 허용된 수정 범위에 따라 수정하고 동일 테스트를 다시 실행하라."
```

실제 orchestration에서는 prompt를 shell command substitution으로 만들지
않고 안전한 argument/file 전달 방식을 사용한다. 위 명령은 사람이 읽기
쉬운 형태의 개념 예시다.

supervisor는 stream에서 다음을 검사한다.

1. `init.model`이 요청한 model slug와 정확히 일치
2. `conversation_id` 저장
3. 각 `step_update.tool_info`의 command/path가 허용 범위 안인지 확인
4. forbidden hardware/ROS/SDK command가 나타나면 즉시 process 종료
5. terminal `result` event와 성공 status 확인

terminal result 없이 프로세스가 끝나면 Agy가 파일을 일부 수정했더라도
해당 iteration은 `FAIL`이다. Codex가 diff를 검사하고 안전하면 새
conversation에서 재시도한다.

### 10.4 Worker prompt 필수 항목

각 prompt에는 다음을 항상 포함한다.

- `AGENTS.md`를 먼저 완전히 읽고 준수
- Execution Domain: `VALIDATION_SIM` 또는 `DESKTOP_DRY_RUN`
- 실물 SDK/로봇 명령 금지
- 현재 phase 하나만 수행
- 수정 허용 파일의 명시적 목록
- 기존 dirty worktree와 사용자 변경 보존
- `main/master` 작업 금지, commit/push 금지
- acceptance command와 기대 evidence
- 실험 결과는 `docs/exp/<date>/`에 기록
- 완료 응답에 changed files, tests, result, risks 포함

P0 worker 예시 scope:

```text
Allowed edits:
- lab/ddt_lab/ddt_lab/assets/gluon.py
- lab/ddt_lab/scripts/gluon/smoke_gluon_asset.py
- lab/ddt_lab/scripts/gluon/smoke_gluon_reach_env.py
- docs/exp/<date>/gluon_p0_runtime_urdf.md

Forbidden:
- tita_gluon_ws hardware code
- model calibration values
- unrelated locomotion/RL files
- any robot or ROS hardware process
```

### 10.5 동시 편집 정책

현재 worktree는 사용자 미커밋 변경이 많으므로 Codex와 Agy가 같은 파일을
동시에 수정하면 안 된다. 한 시점에는 하나의 writer만 둔다.

1. Codex가 preflight와 허용 파일을 확정한다.
2. Agy가 작업하는 동안 Codex는 해당 파일을 수정하지 않는다.
3. Agy가 종료한 후 Codex가 diff와 테스트를 검토한다.
4. 검토가 끝난 뒤에만 다음 Agy iteration을 시작한다.

깨끗한 기준 commit이 만들어진 이후에는 phase별 git worktree를 사용할 수
있지만, 현재처럼 uncommitted/untracked 자산이 많은 상태에서는 shared
worktree의 순차 writer 방식이 더 정확하다.

### 10.6 권한 정책

- 계획/리뷰 작업: `--mode plan`
- 허용 파일 구현: `--mode accept-edits`
- `--dangerously-skip-permissions`는 사용하지 않음
- plan review에는 가능하면 `--sandbox`를 추가
- robot, network ownership, ROS hardware bridge, actuator enable/command는
  Agy prompt에서 명시적으로 금지

Codex는 Agy의 “완료” 주장을 그대로 받아들이지 않고 실제 diff, 생성된
artifact, hash, test stdout을 독립적으로 확인한다. GUI 동작처럼 사람이
직접 봐야 하는 항목은 자동 PASS 처리하지 않고 operator validation으로
남긴다.

### 10.7 실제 구현 시 역할 분담

네, 실제 동작은 “Agy가 코드 작성, Codex가 관리·감독” 구조다.

| 역할 | 책임 |
|---|---|
| User/operator | phase 시작 승인, GUI 육안 확인, 실물 관련 별도 승인 |
| Codex supervisor | preflight, worker prompt/scope, diff review, 독립 test, evidence 판정 |
| Agy worker | 허용된 파일 inspect/edit, 해당 phase의 최소 관련 test, 결과 보고 |
| Repository contract | `AGENTS.md`, model contract, calibration, plan을 공통 source of truth로 제공 |

한 phase의 실제 순서:

1. Codex가 worktree, branch, 모델 hash와 허용 파일을 확인한다.
2. Codex가 Agy에 phase 하나만 포함한 prompt를 전달한다.
3. Agy가 코드를 작성하고 자기 검증 결과를 반환한다.
4. Agy 프로세스가 끝난 뒤 Codex가 변경 파일과 diff를 직접 확인한다.
5. Codex가 Agy와 독립적으로 smoke/test를 실행한다.
6. 실패하면 해당 iteration에서 저장한 conversation ID를
   `--conversation <conversation_id>`에 명시하고 정확한 실패 로그를 Agy에
   돌려준다.
7. 최대 3회 안에 acceptance가 충족되면 Codex가 experiment evidence를
   기록하고 다음 phase를 시작한다.
8. GUI 결과는 user/operator가 직접 확인하기 전까지 `NOT_TESTED` 또는
   `SUSPICIOUS`로 둔다.

Agy가 코드를 작성했다는 사실만으로 phase를 `PASS` 처리하지 않는다.
Codex의 diff review와 독립 test, 필요한 경우 operator 확인까지 완료돼야
한다.

### 10.8 Agy CLI 빠른 사용법

설치와 model/custom-agent 목록 확인:

```bash
command -v agy
agy --help
agy models
agy agents
```

현재 환경에서 확인된 실행 파일은 `/home/cocel/.local/bin/agy`다.
`agy models`는 Claude/Gemini/GPT model slug를 나열하며, `agy agents`는
별도로 설치한 custom agent를 나열한다. model slug를 `--agent`에 넘기면
`Agent not found` 경고 후 default model로 fallback할 수 있으므로 반드시
`--model`을 사용한다.

읽기 전용 계획/리뷰:

```bash
agy \
  --model claude-sonnet-4-6 \
  --mode plan \
  --output-format json \
  --print-timeout 10m \
  --print "AGENTS.md와 docs/plan/gluon_ik_control.md를 읽고 P0만 리뷰하라. 파일을 수정하거나 시뮬레이터·로봇을 실행하지 마라."
```

코드 작성 worker:

```bash
agy \
  --model claude-sonnet-4-6 \
  --mode accept-edits \
  --output-format stream-json \
  --print-timeout 30m \
  --print "AGENTS.md를 준수하라. Execution Domain은 VALIDATION_SIM이다. P0만 수행하고 허용 파일 외에는 수정하지 마라. 실물 SDK와 ROS hardware process는 실행하지 마라."
```

JSON 출력에는 다음과 같이 conversation ID, status, 응답, token 사용량이
포함된다.

```json
{
  "conversation_id": "<uuid>",
  "status": "SUCCESS",
  "response": "...",
  "num_turns": 1,
  "usage": {"total_tokens": 0}
}
```

같은 대화에 수정 요청:

```bash
agy \
  --conversation <conversation_id> \
  --mode accept-edits \
  --output-format stream-json \
  --print-timeout 30m \
  --print "Codex 독립 검증에서 다음 실패가 발생했다. 허용 파일 안에서 원인을 수정하고 동일 테스트를 다시 실행하라: <failure log>"
```

`--continue`는 수동 단일 session을 간단히 재개할 때만 사용할 수 있다.
supervisor loop에서는 중간에 다른 Agy session이 생길 수 있으므로 사용을
금지하고, JSON에서 반환된 ID와 `--conversation <conversation_id>`만
사용한다. 병렬 Agy session은 서로 다른 파일만 수정할 때도 현재 dirty
worktree에서는 사용하지 않는다.

### 10.9 User가 Codex-Agy loop를 시작시키는 요청 예시

다음처럼 요청하면 된다.

```text
gluon_ik_control.md의 P0부터 시작해.
Agy claude-sonnet-4-6을 코드 작성 worker로 사용하고 너는 supervisor가 돼.
phase당 최대 3회 반복하고 매 iteration 뒤 diff와 test를 독립 검증해.
shared worktree에서는 한 번에 한 agent만 수정하고 실물 로봇 명령은 금지해.
P0 PASS 후에만 P1로 넘어가.
```

이 요청을 받으면 Codex가 Agy command를 직접 실행하므로 사용자가 별도
터미널에서 Agy를 동시에 실행할 필요가 없다.

### 10.10 현재 연결 증거

2026-08-04 `DESKTOP_DRY_RUN`에서 다음을 확인했다.

- `agy models`: model slug 목록 반환 `PASS`
- `--agent claude-sonnet-4-6`: custom agent가 아니므로 default model
  fallback 확인; 사용 금지
- `--model claude-sonnet-4-6`, plan-mode JSON output: `PASS`
- JSON output: `status=SUCCESS`, conversation ID 반환 `PASS`
- 명시적 `--conversation` 재개: 동일 ID, `num_turns=2`, `PASS`
- `stream-json` init event에서 요청 model과 tool 목록 확인: `PASS`
- 장시간 plan review terminal result: `FAIL`; headless permission/tool step에서
  종료됐으므로 supervisor failure 처리 규칙에 반영
- Agy P2-P3 patch-author session
  `4ce6867c-56a2-4324-9a4d-b75f261cdd9e`: terminal `SUCCESS`, 그러나
  잘못된 asset/API/frame/임의 limit와 hypothetical PASS를 포함하여 Codex
  review에서 원안 `FAIL`; 검증된 API와 runtime evidence 기반으로 재작성

### 10.11 Agy worker 실패 복구 규칙

실제 검증에서 긴 plan conversation 하나가 최종 JSON 없이 종료됐고, 같은
conversation 재개 시 `unexpected step status: GENERATING` 오류가 발생했다.
이 상태는 재개 루프로 해결하지 않는다.

```text
terminal result missing
  -> stop/ensure no Agy process remains
  -> inspect diff (plan mode면 diff가 없어야 함)
  -> record conversation as failed
  -> shrink phase prompt or permission scope
  -> start a fresh conversation
```

`stream-json`에서 tool step이 `ACTIVE`인 채 종료되는 경우도 terminal result
missing과 동일하게 `FAIL`로 처리한다. `--continue` 또는
`--conversation`을 무한 반복하지 않는다.

`--mode plan`은 편집 의도를 제한하지만 shell tool 자체를 제거하지는
않는다. 실제 plan-mode probe에서도 Agy가 파일 탐색을 위해
`run_command(find ...)`를 요청했다. 따라서 안전성은 mode 이름만 믿지
않고 sandbox, prompt 금지 목록, stream tool-call inspection을 함께
적용한다.

상세 기록은 `docs/exp/2026-08-04/gluon_agy_connection.md`에 둔다.
