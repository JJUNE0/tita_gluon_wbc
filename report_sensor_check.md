# TITA Sensor Check Report

- 검사 일자: 2026-07-29
- Execution Domain: `ROBOT_READ_ONLY`
- Evidence Status: `SUSPICIOUS`
- Policy Checkpoint SHA256 / ONNX Hash: `N/A` (정책을 실행하지 않은 센서 진단)
- 대상: `robot@192.168.0.28`

## 1. Executive Summary

| 항목 | 상태 | 핵심 결과 |
|---|---|---|
| Stereo camera | PARTIAL | 좌우 raw image와 CameraInfo는 수신되지만 좌/우 rate 및 timestamp skew가 불량하고 우측 TF frame 이름이 불일치 |
| SPAD ToF 0 | PASS | `face_point`, 약 14.15 Hz, 54 points, valid 100%, frame `tita4252763/spad` |
| SPAD ToF 1 | PASS | `neck_point`, 약 13.87 Hz, 64 points, valid 100%, frame `tita4252763/spad1` |
| Ultrasonic | FAIL | Range 토픽에 subscriber만 있고 publisher와 수신 메시지가 없음 |
| IMU | PASS | body IMU 1개, 약 440.7 Hz, orientation/gyro/acceleration 모두 finite |
| Odometry | PARTIAL | chassis odometry 약 53.46 Hz 정상; Tower/mapping odometry는 publisher/source가 동작하지 않음 |
| Joint state | PASS | 8 joints, position/velocity/effort 길이 일치, 약 443.35 Hz |
| TF | PARTIAL | base-to-left/SPAD/IMU 및 odom-to-base 존재; 우측 카메라 frame 오타와 CameraInfo frame 누락 |
| LiDAR/Tower | UNKNOWN | bridge 흔적은 있으나 Tower source와 point cloud/odometry 데이터가 없음. 물리 장치 부재와 비활성 상태를 구분할 수 없음 |
| Elevation-map readiness | PARTIAL | 두 SPAD와 body state는 사용 가능하나 stereo 동기화/TF 및 depth cloud, Tower 데이터가 blocker |

로봇 상태나 설정은 변경하지 않았다. ROS topic publish, service/action call, 프로세스 및 daemon 재시작, `systemctl`, `sudo`, 패키지 설치, rosbag 기록을 수행하지 않았다.

## 2. Robot and ROS Environment

- SSH host: `robot@192.168.0.28`
- hostname / user: `tita` / `robot`
- OS: Ubuntu 22.04.5 LTS (Jammy)
- kernel: `5.15.136-tegra`
- architecture: `aarch64`
- 시간대: UTC, system clock synchronized, NTP active
- ROS distro: Humble (`/opt/ros/humble`)
- ROS domain: 실행 프로세스 환경에서 `ROS_DOMAIN_ID=42`
- RMW implementation: 명시적 환경변수 없음, ROS 기본 구현 사용
- source한 환경: `/opt/tita/ros2/setup.bash`
- workspace 후보: `/home/robot/tita_ws`, `tita-sdk/src`, `relay_ws`, `lowlevel_ws`, `direct_ws`
- 주요 실행 노드: `argus_camera_device`, `dual_tof_device_node`, `hw_broadcaster_node`, `tita_chassis_odom_node`, `obstacle_detector_node`, `robot_state_publisher`, `tower_msgs_bridge_node`
- 주요 perception 프로세스: `ros2 launch tita_bringup perception_launch.py`, Argus camera, dual ToF, obstacle detector, Tower message bridge

비대화형 SSH의 초기 ROS 환경변수는 비어 있었다. 실행 프로세스의 환경에서 domain 42와 `/opt/tita/ros2` overlay를 확인한 후 이를 명시적으로 source/export했다. 짧은 discovery에서는 graph가 일부만 보였지만 `--no-daemon --spin-time 10`으로 전체 graph를 확인했다. daemon을 시작하거나 중지하지 않았다.

## 3. Detected Sensor Inventory

Rate는 12초 구독 probe 결과이며, 카메라 raw rate는 별도 `ros2 topic hz`의 마지막 관측값도 병기했다.

| Sensor | Topic | Type | Publisher | Rate | Frame | Status |
|---|---|---|---|---:|---|---|
| Left camera | `/tita4252763/perception/camera/image/left` | `sensor_msgs/msg/Image` | `argus_camera_device` | ~17.0 Hz | `tita4252763/left_camera` | PARTIAL |
| Right camera | `/tita4252763/perception/camera/image/right` | `sensor_msgs/msg/Image` | `argus_camera_device` | ~14.1 Hz | `tita4252763/right_camera` | PARTIAL |
| Left CameraInfo | `/tita4252763/perception/camera/info/left` | `sensor_msgs/msg/CameraInfo` | `argus_camera_device` | ~10.0 Hz | `left_img_raw` | PARTIAL |
| Right CameraInfo | `/tita4252763/perception/camera/info/right` | `sensor_msgs/msg/CameraInfo` | `argus_camera_device` | ~10.0 Hz | `right_img_raw` | PARTIAL |
| Stereo cloud | `/tita4252763/perception/camera/point_cloud` | `sensor_msgs/msg/PointCloud2` | 없음 | 0 | 수신 없음 | DRIVER INACTIVE |
| SPAD ToF 0 | `/tita4252763/perception/devices/face_point` | `sensor_msgs/msg/PointCloud2` | `dual_tof_device_node` | 14.15 Hz | `tita4252763/spad` | PASS |
| SPAD ToF 1 | `/tita4252763/perception/devices/neck_point` | `sensor_msgs/msg/PointCloud2` | `dual_tof_device_node` | 13.87 Hz | `tita4252763/spad1` | PASS |
| Ultrasonic | `/tita4252763/perception/devices/ultrawave` | `sensor_msgs/msg/Range` | 없음 | 0 | 수신 없음 | DRIVER INACTIVE |
| Body IMU | `/tita4252763/imu_sensor_broadcaster/imu` | `sensor_msgs/msg/Imu` | `hw_broadcaster_node` | 440.73 Hz | `base_link` | PASS |
| Chassis odom | `/tita4252763/chassis/odometry` | `nav_msgs/msg/Odometry` | `tita_chassis_odom_node` | 53.46 Hz | `chassis_odom` | PASS |
| Joint state | `/tita4252763/joint_states` | `sensor_msgs/msg/JointState` | `hw_broadcaster_node` | 443.35 Hz | `base_link` | PASS |
| Tower cloud | `/tita4252763/tower/map_point` | `sensor_msgs/msg/PointCloud2` | `tower_msgs_bridge_node` | 0 | 수신 없음 | DRIVER INACTIVE |
| Tower odom | `/tita4252763/tower/odometry` | `nav_msgs/msg/Odometry` | `tower_msgs_bridge_node` | 0 | 수신 없음 | DRIVER INACTIVE |
| Mapping colored cloud | `/tower/mapping/cloud_colored` | `sensor_msgs/msg/PointCloud2` | 없음 | 0 | 수신 없음 | DRIVER INACTIVE |
| Mapping odom | `/tower/mapping/odometry` | `nav_msgs/msg/Odometry` | 없음 | 0 | 수신 없음 | DRIVER INACTIVE |

## 4. Stereo Camera Check

### Image metadata

| Side | Resolution | Encoding | Step | Data bytes | Frame | QoS |
|---|---:|---|---:|---:|---|---|
| Left | 960×600 | `bgr8` | 2880 | 1,728,000 | `tita4252763/left_camera` | BEST_EFFORT/VOLATILE |
| Right | 960×600 | `bgr8` | 2880 | 1,728,000 | `tita4252763/right_camera` | BEST_EFFORT/VOLATILE |

두 영상 모두 raw이며 payload가 비어 있지 않다. compressed image 토픽은 발견되지 않았다.

### CameraInfo와 calibration

- 좌우 모두 960×600, `rational_polynomial`, D/K/R/P가 모두 0인 상태가 아니므로 calibration 데이터는 존재한다.
- CameraInfo는 좌우 모두 약 10 Hz이며 RELIABLE/VOLATILE이다.
- 좌우 K의 초점거리는 약 480 px로 유사하다.
- P의 `Tx/fx` 크기로 계산되는 값은 좌 약 0.1492 m, 우 약 0.1492 m이다. 일반적인 rectified stereo에서 좌측 P의 Tx가 0인 형태와 다르므로 P convention/calibration export를 재검증해야 한다.
- TF의 좌우 카메라 y 위치 차이는 약 0.150001 m로 물리적 baseline과 일관된 크기다.

### Synchronization

12초 동안 수집한 timestamp:

- left 156개, right 43개
- nearest-pair absolute skew: mean 117.94 ms, median 51.04 ms, max 730.99 ms
- 별도 `ros2 topic hz` 마지막 관측: left 약 17.0 Hz, right 약 14.1 Hz

좌우 해상도는 같지만 rate가 일치하지 않고 skew가 stereo depth에 사용하기에는 크다. probe의 대형 raw image 수신 부하가 drop에 일부 영향을 줄 수 있으므로 동일 호스트에서 image transport/하드웨어 timestamp 기반의 재측정이 필요하지만, 현재 증거로 동기화는 `FAIL`이다.

### Frame과 depth

- left image frame `tita4252763/left_camera`는 TF에 존재한다.
- right image frame `tita4252763/right_camera`는 TF에 없다. TF에는 오타로 보이는 `tita4252763/right_camara`만 존재한다.
- CameraInfo frame `left_img_raw`, `right_img_raw`는 수집한 TF tree에서 확인되지 않았다.
- rectified image와 disparity/depth 토픽은 발견되지 않았다.
- `/tita4252763/perception/camera/point_cloud`는 subscriber만 있고 publisher가 없어 12초간 데이터가 없었다.

따라서 raw stereo와 calibration은 존재하지만 현재 바로 stereo depth를 안정적으로 생성할 준비는 되지 않았다.

## 5. SPAD ToF Check

### SPAD ToF 0 — face

- Topic: `/tita4252763/perception/devices/face_point`
- Publisher: `/tita4252763/dual_tof_device_node`
- QoS: RELIABLE/VOLATILE
- Rate: 약 14.15 Hz
- Frame: `tita4252763/spad`
- PointCloud2: width 54, height 1, 54 points, fields `x/y/z`, point step 16, row step 864, dense
- 54개 표본에서 finite valid point 100%, NaN/Inf 0%
- 3D 원점 거리 범위: 약 0.186–0.604 m
- base TF 존재: translation `[0.24052, -0.0019, 0.064455]`

현 상태에서 local obstacle/elevation 입력으로 사용할 수 있다. 단, 거리 범위는 한 시점의 장면 관측이며 센서 전체 스펙 범위가 아니다.

### SPAD ToF 1 — neck

- Topic: `/tita4252763/perception/devices/neck_point`
- Publisher: `/tita4252763/dual_tof_device_node`
- QoS: RELIABLE/VOLATILE
- Rate: 약 13.87 Hz
- Frame: `tita4252763/spad1`
- PointCloud2: width 64, height 1, 64 points, fields `x/y/z`, point step 16, row step 1024, dense
- 64개 표본에서 finite valid point 100%, NaN/Inf 0%
- 3D 원점 거리 범위: 약 0.063–0.095 m
- base TF 존재: translation `[0.21953, -0.0019, -0.030142]`

두 ToF는 서로 다른 frame과 point count를 가지며 독립 stream으로 확인됐다.

## 6. Ultrasonic Check

- Topic: `/tita4252763/perception/devices/ultrawave`
- Type: `sensor_msgs/msg/Range`
- Publisher: 0
- Subscriber: `obstacle_detector_node` 1개
- 12초 수신: 0
- `ultrawave_device_node` 실행 프로세스/ROS node가 발견되지 않음
- package/launch/config 설치 흔적은 있으나 실행 데이터는 없음

현재 상태는 `DRIVER INACTIVE`이며 radiation type, FOV, min/max/current range, frame을 확인할 수 없다. 서비스를 재시작하거나 드라이버를 실행하지 않았다.

## 7. IMU, Odometry and Joint-State Check

### IMU

- 발견된 IMU 토픽은 body IMU 한 개다. 별도 perception/Tower IMU 토픽은 발견되지 않았다.
- Frame: 메시지는 `base_link`; static TF에는 `tita4252763/base_link → tita4252763/imu_link` identity가 존재한다.
- Rate: 약 440.73 Hz
- orientation, angular velocity, linear acceleration 모두 제공되며 finite다.
- 관측 예: acceleration `[0.187, -0.330, 9.800] m/s²`, angular velocity `[-0.0051, -0.0029, 0.0003] rad/s`
- orientation/gyro/acceleration covariance는 모두 0이다. 미제공(-1)은 아니지만 불확실성을 표현하지 않으므로 융합 설정에서 주의가 필요하다.
- timestamp는 로봇 현재 epoch와 같은 범위이며 현저한 clock offset은 관측되지 않았다.

### Odometry

- `/tita4252763/chassis/odometry`, frame `chassis_odom`, child `tita4252763/base_link`
- 약 53.46 Hz로 지속 갱신
- position/orientation 및 linear/angular velocity 제공
- pose/twist covariance는 전부 0이므로 불확실성 모델이 없다.
- `/tower/mapping/odometry`는 publisher가 없고, bridge 출력 `/tita4252763/tower/odometry`는 publisher endpoint만 존재하며 12초간 메시지는 없다.

### Joint state

- 8 joints: 좌/우 각각 leg 1–4
- name/position/velocity/effort 길이가 모두 8로 일치
- 모든 수치 finite, 약 443.35 Hz

## 8. TF Tree and Sensor Extrinsics

| Parent | Child | Translation (m) | Rotation xyzw | Static/Dynamic | Status |
|---|---|---|---|---|---|
| `chassis_odom` | `tita4252763/base_link` | 관측 `[0.038, 0.003, 0.000]` | `[0, 0, 0.079, 0.997]` | Dynamic | PASS |
| `tita4252763/base_link` | `tita4252763/left_camera` | `[0.23416, 0.075, 0.04036]` | `[0.500, 0.500, 0.500, 0.500]` | Static | PASS |
| `tita4252763/base_link` | `tita4252763/right_camara` | `[0.23416, -0.075001, 0.04036]` | `[0.500, 0.500, 0.500, 0.500]` | Static | FAIL: image frame 철자 불일치 |
| `tita4252763/base_link` | `tita4252763/spad` | `[0.24052, -0.0019, 0.064455]` | `[0.630, 0.630, 0.321, 0.321]` | Static | PASS |
| `tita4252763/base_link` | `tita4252763/spad1` | `[0.21953, -0.0019, -0.030142]` | `[0.684, 0.684, 0.178, 0.178]` | Static | PASS |
| `tita4252763/base_link` | `tita4252763/imu_link` | `[0, 0, 0]` | `[0, 0, 0, 1]` | Static | PASS |

추가 문제:

- image frame에는 namespace가 있지만 IMU/JointState 메시지 frame은 bare `base_link`다.
- CameraInfo의 `left_img_raw`/`right_img_raw` frame이 TF에 없다.
- 별도 optical frame이 확인되지 않았다.
- ultrasonic frame은 메시지 미수신으로 확인 불가하다.
- Tower/LiDAR frame은 source 데이터 미수신으로 확인 불가하다.

## 9. LiDAR and TITA Tower Check

판정: `UNKNOWN` (현재 ROS 데이터 경로는 `DRIVER INACTIVE`)

- `tower_msgs_bridge_node`가 실행 중이며 `/tower/mapping/cloud_colored`와 `/tower/mapping/odometry`를 subscribe하도록 구성되어 있다.
- 위 두 source topic은 publisher 0이며 12초간 메시지가 없었다.
- bridge의 `/tita4252763/tower/map_point`와 `/tita4252763/tower/odometry` publisher endpoint는 존재하지만 메시지는 수신되지 않았다.
- LaserScan 토픽은 발견되지 않았다.
- 별도 LiDAR PointCloud2로 확정할 수 있는 활성 stream은 없다.
- serial/LiDAR/tower 명칭 장치 node는 발견되지 않았고, 활성 네트워크 연결에서도 Tower/LiDAR 연결을 식별하지 못했다.
- `lsusb`와 `v4l2-ctl`은 설치되어 있지 않아 실행하지 못했다. `/dev/video0`, `/dev/video1`, `/dev/media0`은 존재한다.
- 제한적 `dmesg` 센서 검색에서 추가 근거를 얻지 못했다.

ROS bridge 설치 흔적이 있으므로 “TITA Tower 없음”으로 단정할 수 없다. 물리 Tower/LiDAR가 없거나, 전원이 꺼졌거나, 별도 컴퓨터/드라이버가 비활성일 가능성을 현재 read-only 증거만으로 구분할 수 없다.

## 10. Elevation Mapping Readiness

| 항목 | 판정 | 근거 |
|---|---|---|
| 1. 좌우 영상 획득 | PASS | 960×600 bgr8 payload 수신 |
| 2. 좌우 카메라 calibration | PARTIAL | D/K/R/P 존재하나 P Tx convention 및 frame 연결 재검증 필요 |
| 3. 좌우 timestamp synchronization | FAIL | rate 불일치, median skew 약 51 ms |
| 4. stereo baseline 확인 | PARTIAL | TF 약 0.150 m; P는 양쪽 모두 약 0.149 m Tx/fx 형태 |
| 5. stereo depth 생성 가능성 | PARTIAL | raw/calibration 존재, rectified/disparity/depth/cloud publisher 없음 |
| 6. SPAD ToF 0 데이터 | PASS | 약 14.15 Hz, finite points |
| 7. SPAD ToF 1 데이터 | PASS | 약 13.87 Hz, finite points |
| 8. 초음파 데이터 | FAIL | publisher 없음 |
| 9. IMU 데이터 | PASS | 약 440.7 Hz, 모든 주요 field finite |
| 10. odometry 데이터 | PASS | chassis odom 약 53.5 Hz |
| 11. joint state 데이터 | PASS | 8축 배열 정합, 약 443.4 Hz |
| 12. sensor-to-base TF | PARTIAL | left/SPAD/IMU 존재, right frame 오타, CameraInfo frame 누락 |
| 13. odom-to-base TF | PASS | dynamic transform 수신 |
| 14. 로컬 elevation mapping 전체 준비도 | PARTIAL | SPAD 기반 시작 가능, stereo/Tower 융합은 아직 불가 |

현재 바로 가능한 것:

- 두 SPAD cloud를 base frame으로 변환
- chassis odometry, body IMU, joint states를 이용한 motion compensation prototype
- SPAD 기반 robot-centric local elevation layer

누락 또는 추가 검증이 필요한 것:

- 좌우 카메라 hardware synchronization과 일정한 동일 rate
- 우측 카메라 및 CameraInfo frame의 TF 연결
- stereo rectification/depth/point-cloud 생성기
- 초음파 publisher
- Tower/LiDAR 실제 장치 및 mapping source
- IMU/odometry covariance

가장 큰 blocker는 (1) stereo timestamp/rate 불일치, (2) 카메라 TF frame 불일치, (3) depth/Tower cloud source 부재다.

## 11. Recommended Next Steps

1. 로봇 설정을 변경하기 전 별도 승인 하에 카메라 드라이버의 좌우 hardware trigger/timestamp와 frame naming을 검토한다.
2. 같은 프로세스 또는 image_transport 기반 경량 probe로 좌우 100쌍 이상을 재측정한다.
3. `right_camara` 오타와 CameraInfo optical frame을 URDF/driver 어느 쪽에서 정정할지 결정하고 회귀 테스트를 추가한다.
4. CameraInfo P와 TF 0.150 m baseline을 calibration 원본과 대조하고 stereo rectification을 검증한다.
5. stereo depth/PointCloud2 prototype을 `VALIDATION_SIM` 또는 `DESKTOP_DRY_RUN`에서 먼저 만든다.
6. SPAD FOV/거리 정확도와 base 변환을 정적 표적 및 안전한 read-only 기록으로 검증한다.
7. Tower/LiDAR와 초음파의 물리 장착·전원·별도 컴퓨터 상태를 운영자에게 확인한 뒤, 승인된 별도 진단 세션에서 driver 상태를 조사한다.

## 12. Commands Executed

아래 명령은 모두 read-only 조회 또는 subscribe이며 timeout을 사용했다.

- `ssh -o BatchMode=yes -o ConnectTimeout=5 robot@192.168.0.28 'hostname; whoami; ...'`
- `ps`, `/proc/<pid>/environ`, `uname`, `/etc/os-release`, `timedatectl`
- `ls -l /dev/video* /dev/media*`, device symlink 조회
- `source /opt/tita/ros2/setup.bash; export ROS_DOMAIN_ID=42`
- `ros2 node list --no-daemon --spin-time 10`
- `ros2 topic list -t --no-daemon --spin-time 10`
- `ros2 service list`, `ros2 action list` — 목록만 조회, 호출 없음
- `ros2 topic info -v --no-daemon <topic>`
- `timeout 9s ros2 topic hz <camera topic>`
- `ros2 topic echo --once /tf`, transient-local QoS로 `/tf_static` 1회 조회
- `timeout 5s ros2 run tf2_ros tf2_echo <parent> <child>`
- `test/tita_sensor_readonly_probe.py`를 `/tmp`에 복사하여 12초 subscribe-only 실행 후 삭제
- `ip`, `ss`, device/config 문자열 조회

실패/제약:

- 초기 `ros2 node/topic list` discovery가 불완전해 10초 no-daemon discovery로 재조회했다.
- probe 첫 실행은 `Node.subscriptions` 예약 속성명 충돌로 센서 수집 전에 실패했다. 로컬 변수명을 수정한 후 성공했다.
- `lsusb`, `v4l2-ctl`: command unavailable; 설치하지 않았다.
- 초음파/Tower/stereo cloud: publisher/source 부재 또는 12초간 메시지 없음; 재시작하지 않았다.

## 13. Raw Findings

- Camera devices: `/dev/video0`, `/dev/video1`, `/dev/media0`
- Camera image QoS: BEST_EFFORT/VOLATILE; CameraInfo QoS: RELIABLE/VOLATILE
- ToF QoS: RELIABLE/VOLATILE, publisher `dual_tof_device_node`
- IMU/JointState/Odometry publisher: 각각 `hw_broadcaster_node`, `hw_broadcaster_node`, `tita_chassis_odom_node`
- `/tf`: publisher 3개(`robot_state_publisher`, chassis odom, Tower bridge)
- `/tf_static`: `robot_state_publisher`, RELIABLE/TRANSIENT_LOCAL
- 서비스 및 action은 목록만 확인했다. action 목록은 비어 있었으며 어떤 service/action도 호출하지 않았다.
- 명령 토픽은 graph에 존재하지만 조회만 했으며 publish하지 않았다.
- 로봇 파일, 설정, launch, calibration, network, ROS domain을 수정하지 않았다.

## 14. 추가 ROS CLI 원본 필드 검증

### 왜 이 데이터를 추가로 확인했는가

초기 12초 probe는 여러 토픽을 한 번에 수집하고 요약하므로 빠른 inventory와 rate/skew 계산에는 적합하지만, calibration 및 frame 문제를 다른 운영자가 재현하기에는 ROS CLI의 원본 필드 증거가 더 명확하다. 이번 추가 조회의 목적은 다음과 같다.

1. CameraInfo의 D/K/R/P를 원본 그대로 확인하여 “calibration이 실제로 publish되는가”를 확정한다.
2. Image payload를 dump하지 않고 header/해상도/encoding만 확인하여 영상 stream과 frame을 안전하게 교차검증한다.
3. SPAD PointCloud2의 binary layout과 frame을 확인하여 downstream parser 및 TF 변환 가능성을 검증한다.
4. odometry/IMU의 parent/child frame 이름을 확정한 뒤 실제 `tf2_echo` lookup 성공 여부를 확인한다.

### A. CameraInfo 원본 값

2026-07-29 추가 `ros2 topic echo --once` 결과:

| 항목 | Left | Right |
|---|---|---|
| `header.frame_id` | `left_img_raw` | `right_img_raw` |
| width × height | 960 × 600 | 960 × 600 |
| `distortion_model` | `rational_polynomial` | `rational_polynomial` |
| D | `[19.941923, 12.154908, -0.0002103, 0.00003612, 0.570956, 20.288393, 19.558937, 3.112080]` | `[0.802593, 0.190010, 0.0001183, 0.00003165, 0.007085, 1.175028, 0.395762, 0.041768]` |
| K | `[479.849976, 0, 479.116089, 0, 480.002167, 298.078735, 0, 0, 1]` | `[480.792572, 0, 475.269989, 0, 480.902679, 300.913361, 0, 0, 1]` |
| R | `[0.99998985, -0.00010560, 0.00450534, 0.00012654, 0.99998919, -0.00464698, -0.00450480, 0.00464751, 0.99997905]` | 좌측과 동일 |
| P | `[477.686779, 2.176022, 481.267942, -71.280335, -1.282048, 481.382303, 295.841930, 0.178341, -0.004505, 0.004648, 0.999979, 0.001202]` | `[478.646692, 2.158048, 477.426169, -71.426107, -1.294703, 482.295980, 298.672311, 0.181409, -0.004505, 0.004648, 0.999979, 0.001202]` |

판정:

- D/K/R/P가 모두 채워져 있어 calibration publish는 `PASS`다.
- `-P[3]/P[0]`은 좌 약 0.14922 m, 우 약 0.14922 m다.
- 그러나 표준 rectified stereo CameraInfo에서는 보통 좌측 `P[3]=0`, 우측 `P[3]=-fx·baseline` 형태다. 현재는 좌우 모두 약 -71이므로 각 카메라가 공통 기준 frame에 대해 투영된 custom convention일 수 있다.
- TF에서 구한 좌우 카메라 translation 차이는 약 0.150001 m이므로 baseline 크기는 약 0.15 m로 강하게 지지되지만, CameraInfo P만으로 표준 stereo baseline이 정상이라고 확정하지 않는다.

### B. Image metadata 원본 값

| Side | `header.frame_id` | Width | Height | Encoding |
|---|---|---:|---:|---|
| Left | `tita4252763/left_camera` | 960 | 600 | `bgr8` |
| Right | `tita4252763/right_camera` | 960 | 600 | `bgr8` |

각 필드는 BEST_EFFORT QoS 및 5초 timeout으로 한 번만 조회했다. `data` 배열은 출력하지 않았다. CameraInfo frame(`*_img_raw`)과 Image frame(`tita4252763/*_camera`)이 서로 다르다는 점도 재확인됐다.

### C. SPAD PointCloud2 metadata 원본 값

| Topic | Frame | Width | Height | Fields | Point step | Row step | Dense |
|---|---|---:|---:|---|---:|---:|---|
| `face_point` | `tita4252763/spad` | 54 | 1 | x@0/y@4/z@8, FLOAT32 | 16 | 992 | true |
| `neck_point` | `tita4252763/spad1` | 64 | 1 | x@0/y@4/z@8, FLOAT32 | 16 | 1024 | true |

주의: 요청된 CLI 형식은 각 field마다 새 메시지를 받는다. 따라서 `face_point`의 width 54와 row_step 992는 같은 메시지에서 나온 값이 아니다. 992/16=62이므로 face SPAD point count가 메시지마다 달라지는 것으로 해석할 수 있다. 앞선 단일-message probe에서는 width 54, point_step 16, row_step 864로 내부 정합했다. downstream 코드는 face cloud의 point count를 고정값으로 가정하지 말고 매 메시지의 width/row_step을 사용해야 한다. neck cloud는 이번 field별 표본에서 64×16=1024로 정합했다.

### D. Odometry, IMU 및 TF frame 원본 값

- Chassis odometry `header.frame_id`: `chassis_odom`
- Chassis odometry `child_frame_id`: `tita4252763/base_link`
- IMU `header.frame_id`: `base_link`

확인된 frame으로 실행한 `tf2_echo`:

| Lookup | 결과 | 핵심 값 |
|---|---|---|
| `tita4252763/base_link → tita4252763/left_camera` | PASS | translation `[0.234, 0.075, 0.040]` |
| `tita4252763/base_link → tita4252763/right_camera` | FAIL | 5초 동안 source frame 없음 |
| `tita4252763/base_link → tita4252763/spad` | PASS | translation `[0.241, -0.002, 0.064]` |
| `tita4252763/base_link → tita4252763/spad1` | PASS | translation `[0.220, -0.002, -0.030]` |
| `chassis_odom → tita4252763/base_link` | PASS | 동적 translation 약 `[0.038, 0.003, 0.000]` |

`tf2_echo` 시작 직후 일부 성공 항목에서도 transient-local static TF discovery 전 “frame does not exist”가 한두 번 출력됐지만 곧 transform이 수신됐다. 우측 `right_camera`만 timeout까지 transform이 한 번도 나오지 않았으므로 실제 frame 불일치다. 앞서 `/tf_static` 원본에서 확인한 child 이름은 `tita4252763/right_camara`다.

### 추가 실행 명령

- CameraInfo 좌/우: `ros2 topic echo --once <topic>`
- Image 좌/우: `timeout 5s ros2 topic echo --qos-reliability best_effort --once <topic> --field <field>`
- SPAD 좌/우: `timeout 5s ros2 topic echo --once <topic> --field <field>`
- Odometry/IMU: `timeout 5s ros2 topic echo --once <topic> --field <field>`
- TF: `timeout 5s ros2 run tf2_ros tf2_echo <parent> <child>`

추가 조회에서도 topic publish, service/action 호출, 프로세스 재시작 및 로봇 설정 변경은 수행하지 않았다.

## 15. Static Elevation Rosbag Capture

- Execution Domain: `ROBOT_READ_ONLY`
- Evidence Status: `PASS`
- 기록 시각: 2026-07-29 07:30:23 UTC
- 원격 경로: `/home/robot/bags/tita_elevation/tita_static_20260729_073023`
- 로컬 복사본: `/home/cocel/tita_elevation_bags/tita_static_20260729_073023`
- Storage: SQLite3, CDR
- Bag size: 916.6 MiB (`du`: 917M)
- 실제 메시지 구간: 12.941741368초
- 전체 메시지: 13,452

15초 timeout의 SIGINT를 recorder에 전달했다. ROS graph discovery와 topic subscription에 약 2초가 사용되어 실제 메시지 timestamp 구간은 약 12.94초다. recorder는 cache를 flush하고 `Recording stopped`로 정상 종료했다. `timeout` shell status 124는 제한시간 도달을 뜻하며 bag 실패가 아니다.

| Topic | Message Count | 판정 |
|---|---:|---|
| `/tf` | 702 | PASS |
| `/tf_static` | 1 | PASS |
| `/tita4252763/robot_description` | 1 | PASS |
| `/tita4252763/perception/camera/image/left` | 347 | PASS |
| `/tita4252763/perception/camera/image/right` | 205 | PASS |
| `/tita4252763/perception/camera/info/left` | 129 | PASS |
| `/tita4252763/perception/camera/info/right` | 130 | PASS |
| `/tita4252763/perception/devices/face_point` | 163 | PASS |
| `/tita4252763/perception/devices/neck_point` | 161 | PASS |
| `/tita4252763/imu_sensor_broadcaster/imu` | 5,481 | PASS |
| `/tita4252763/chassis/odometry` | 650 | PASS |
| `/tita4252763/joint_states` | 5,482 | PASS |

원격 Humble과 로컬 Jazzy에서 각각 `ros2 bag info`를 실행했으며 size, duration, 전체 및 토픽별 message count가 일치했다. 따라서 복사본 검증은 `PASS`다. 로컬 출력의 `ROS Distro: unknown`은 bag metadata에 distro가 기록되지 않았다는 의미이며 message count나 SQLite3 가독성 실패가 아니다.

주의 사항:

- 좌/우 image count가 347/205로 크게 다르다. 앞선 live rate 및 timestamp skew 문제와 같은 방향의 추가 증거이므로 stereo 처리 전에 해결해야 한다.
- `/tf_static`, 좌/우 CameraInfo, robot description이 모두 포함되어 offline TF/calibration 재구성이 가능하다.
- 다음 단계인 rosbag 재생은 아직 수행하지 않았다(`NOT_TESTED`). 요청대로 단계별로 진행한다.
- 기록 중 로봇 motion command, topic publish, service/action 호출, 설정 변경은 없었다.
