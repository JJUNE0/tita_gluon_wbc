TITA 로봇의 perception sensor와 상태추정 관련 ROS 2 인터페이스를 점검하고,
현재 작업 디렉터리에 `report_sensor_check.md`를 작성해 주세요.

로봇에는 다음 SSH 명령으로 접근할 수 있습니다.

ssh robot@192.168.0.28

# 최우선 안전 규칙

이번 작업은 반드시 READ-ONLY 진단만 수행하세요.

절대로 다음 작업을 하지 마세요.

- 로봇에 velocity, joint command, FSM command, RC input 등을 publish하지 말 것
- 모터 enable, transform_up, stand, balance, locomotion mode를 실행하지 말 것
- ROS 2 service/action을 호출하지 말 것
- 실행 중인 node, launch, service, daemon을 재시작하거나 종료하지 말 것
- systemctl start/stop/restart/enable/disable을 실행하지 말 것
- 패키지를 설치하거나 apt/pip 환경을 변경하지 말 것
- 로봇의 source code, configuration, launch file, calibration file을 수정하지 말 것
- 네트워크 설정, ROS_DOMAIN_ID, DDS 설정을 변경하지 말 것
- sudo를 사용하지 말 것
- 긴 시간 동안 대용량 PointCloud2나 Image 메시지를 터미널에 dump하지 말 것
- rosbag을 장시간 기록하지 말 것
- 로봇을 물리적으로 움직이게 만들 수 있는 명령은 어떤 경우에도 실행하지 말 것

필요한 경우 `/tmp`에 일시적인 read-only 검사 스크립트를 만들 수 있지만,
검사가 끝나면 제거하세요. 최종적으로 수정하거나 생성할 파일은 로컬 작업 디렉터리의
`report_sensor_check.md` 하나를 원칙으로 합니다.

명령이 실패해도 임의로 서비스를 재시작하지 말고, 실패 원인과 실행한 명령을 보고서에 기록하세요.

# 작업 목표

다음 센서가 실제로 존재하고 ROS 2에서 접근 가능한지 확인하세요.

1. 전면 스테레오 카메라
   - left image
   - right image
   - left CameraInfo
   - right CameraInfo

2. SPAD ToF 센서 2개
   - 각 센서의 PointCloud2 또는 Range 출력
   - 문서상의 이름을 가정하지 말고 실제 토픽을 탐색할 것

3. 초음파 센서
   - Range 출력 여부

4. IMU
   - IMU가 여러 개라면 모두 구분
   - body IMU와 perception/Tower IMU가 있다면 각각 구분

5. Elevation mapping에 필요한 추가 데이터
   - odometry
   - joint states
   - TF 및 TF static
   - base_link와 각 센서 frame 사이 transform

6. TITA Tower 또는 별도 LiDAR 존재 여부
   - LiDAR, laser scan, lidar pointcloud, tower 관련 토픽과 장치 확인
   - 별도 LiDAR가 없다면 `TITA Tower 없음으로 추정`이라고 명확히 작성
   - 단, 물리 장치 부재와 드라이버 비활성 상태를 구분할 수 없다면 UNKNOWN으로 표시

# 1단계: SSH 및 시스템 환경 확인

먼저 연결 가능 여부를 확인하세요.

예시:

ssh -o ConnectTimeout=5 robot@192.168.0.28 'hostname && whoami'

연결 후 다음 정보를 read-only로 확인하세요.

- hostname
- Ubuntu 버전
- kernel
- architecture
- ROS_DISTRO
- ROS_DOMAIN_ID
- RMW_IMPLEMENTATION
- `/opt/ros` 아래 설치된 ROS 배포판
- 현재 source된 workspace
- 관련 workspace 후보
- 현재 실행 중인 ROS 2 프로세스
- 시간과 timezone

비대화형 SSH에서는 ROS 환경이 source되지 않을 수 있습니다.
설치된 ROS 배포판과 사용자 workspace를 먼저 확인한 다음,
필요한 `setup.bash`를 명시적으로 source해서 ROS 2 명령을 실행하세요.

다만 `.bashrc`, setup 파일, workspace 파일은 수정하지 마세요.

# 2단계: 하드웨어 장치 확인

다음과 같은 read-only 명령을 사용해 카메라 및 USB 장치 존재 여부를 확인하세요.

- `lsusb`
- `ls -l /dev/video*` — 파일이 있을 때만
- `ls -l /dev/media*` — 파일이 있을 때만
- `v4l2-ctl --list-devices` — 이미 설치되어 있을 때만
- 관련 device symlink
- dmesg는 권한 없이 읽을 수 있을 때만 제한적으로 사용

패키지가 없으면 설치하지 말고 `command unavailable`로 기록하세요.

카메라 장치 수와 ROS 2 카메라 토픽 수가 일치하는지도 검토하세요.

# 3단계: ROS 2 graph 전체 조사

ROS 환경을 source한 뒤 최소한 다음을 확인하세요.

- `ros2 node list`
- `ros2 topic list -t`
- `ros2 service list`
- `ros2 action list`

Service와 action은 목록만 확인하고 절대로 호출하지 마세요.

다음 키워드를 중심으로 실제 토픽을 탐색하세요.

camera
image
stereo
left
right
depth
disparity
point
cloud
spad
tof
range
ultra
sonar
imu
odom
joint
tf
lidar
laser
tower
mapping
perception

각 후보 토픽에 대해 다음을 확인하세요.

- 정확한 토픽 이름
- message type
- publisher 수
- subscriber 수
- publisher node 이름
- QoS 정보
- 현재 메시지가 실제로 흐르는지
- 대략적인 publish rate

`ros2 topic info -v <topic>`을 우선 사용하세요.

Rate 측정은 반드시 timeout을 사용하세요. 예:

timeout 8s ros2 topic hz <topic>

데이터가 없다고 해서 node를 재시작하지 마세요.

# 4단계: 센서별 메시지 검사

각 센서 토픽은 전체 데이터를 무제한 출력하지 말고,
한 메시지 또는 metadata만 안전하게 확인하세요.

모든 센서에서 공통으로 확인할 항목:

- `header.frame_id`
- timestamp
- 메시지 수신 여부
- publish rate
- publisher node
- QoS
- 데이터가 0이나 고정값으로 멈춰 있지는 않은지
- timestamp가 현재 ROS 시간과 현저하게 다르지 않은지

## 스테레오 카메라

좌우 영상 각각에 대해:

- topic
- message type
- width
- height
- encoding
- step
- frame_id
- rate
- compressed/raw 여부
- 실제 이미지 데이터가 비어 있지 않은지

CameraInfo 각각에 대해:

- width, height
- distortion model
- D
- K
- R
- P
- frame_id
- calibration 값이 전부 0이 아닌지

스테레오 사용 가능성을 평가하세요.

특히 다음을 확인하세요.

- left/right image가 모두 존재하는가
- left/right CameraInfo가 모두 존재하는가
- 두 영상의 해상도와 rate가 일치하는가
- 좌우 timestamp 차이가 어느 정도인가
- 좌우 optical frame이 구분되는가
- stereo baseline을 CameraInfo의 P 행렬 또는 TF에서 계산 가능한가
- rectified image 또는 disparity/depth 토픽이 이미 존재하는가
- calibration이 정상으로 보이는가

가능하면 약 30~50쌍의 좌우 timestamp를 read-only로 수집하여 다음을 계산하세요.

- left 평균 rate
- right 평균 rate
- nearest timestamp pair의 mean absolute skew
- median skew
- maximum skew
- 동기화 상태 평가

필요하다면 `/tmp`에 rclpy subscriber를 작성할 수 있습니다.
이 스크립트는 subscribe만 해야 하며 publish/service/action 기능을 포함하면 안 됩니다.

## SPAD ToF ×2

각 ToF 후보에 대해:

- 정확한 topic
- message type
- frame_id
- rate
- PointCloud2라면:
  - width
  - height
  - point count
  - fields
  - point_step
  - row_step
  - is_dense
  - x/y/z field 존재 여부
  - 유효 point 비율을 계산할 수 있는지
  - NaN/Inf 비율
  - 대략적인 거리 범위
- Range라면:
  - radiation_type
  - field_of_view
  - min_range
  - max_range
  - 현재 range 값

PointCloud2의 전체 raw data 배열은 출력하지 마세요.

두 ToF가 서로 다른 frame을 사용하는지 확인하고,
각 센서가 실제로 독립적인 스트림인지 평가하세요.

## 초음파

- topic
- type
- frame_id
- rate
- radiation_type
- field_of_view
- min_range
- max_range
- 현재 range
- 메시지가 유효하고 지속적으로 갱신되는지

## IMU

발견되는 모든 IMU를 각각 구분하세요.

- topic
- publisher
- frame_id
- rate
- orientation 제공 여부
- angular velocity 제공 여부
- linear acceleration 제공 여부
- covariance가 전부 -1 또는 0인지
- timestamp 상태
- 값이 비정상적으로 NaN/Inf인지

## Odometry와 Joint State

Elevation map의 motion compensation에 사용할 수 있는 데이터가 있는지 확인하세요.

Odometry:

- topic
- frame_id
- child_frame_id
- rate
- position/orientation
- linear/angular velocity
- covariance
- 지속적으로 갱신되는지

JointState:

- topic
- rate
- joint name 목록
- position/velocity/effort 제공 여부
- 배열 길이가 joint name과 일치하는지

# 5단계: TF tree 검사

다음 frame이 존재하는지 찾아보세요.

- odom 또는 map
- base_link 또는 동등한 body frame
- left camera frame
- right camera frame
- camera optical frames
- SPAD/ToF frame 2개
- ultrasonic frame
- IMU frame

`/tf`와 `/tf_static`은 전체 메시지를 무제한 dump하지 마세요.

메시지의 frame_id를 먼저 식별한 후,
사용 가능한 경우 다음 관계를 `tf2_echo`로 제한 시간 동안 확인하세요.

- odom → base frame
- base frame → left camera optical frame
- base frame → right camera optical frame
- base frame → SPAD 0 frame
- base frame → SPAD 1 frame
- base frame → ultrasonic frame
- base frame → IMU frame

예:

timeout 5s ros2 run tf2_ros tf2_echo <parent> <child>

각 transform에 대해 translation, rotation, static/dynamic 여부를 기록하세요.

다음 문제를 검사하세요.

- 센서 메시지의 frame_id가 TF tree에 없음
- 좌우 카메라가 같은 frame_id를 잘못 사용
- 좌우 baseline이 0에 가까움
- optical frame 축 convention이 불명확함
- TF timestamp extrapolation 오류
- odom → base transform 부재
- 센서 transform 부재

# 6단계: LiDAR 및 TITA Tower 확인

다음을 조사하세요.

- LaserScan 토픽
- LiDAR PointCloud2 토픽
- tower 관련 node/topic/frame
- mapping odometry
- colored cloud
- GPS/GNSS/RTK
- 별도 LiDAR USB 또는 Ethernet 장치 흔적

판정은 다음 중 하나로 작성하세요.

- PRESENT
- NOT DETECTED
- DRIVER INACTIVE
- UNKNOWN

LiDAR와 Tower 관련 하드웨어 및 ROS 흔적이 모두 없다면:

`별도 LiDAR 및 TITA Tower는 현재 장비에 없는 것으로 추정됨`

이라고 작성하세요.

단순히 토픽이 없다는 이유만으로 하드웨어가 절대 없다고 단정하지는 마세요.

# 7단계: Elevation map 준비도 평가

최종적으로 다음 파이프라인이 현재 가능한지 평가하세요.

Stereo Camera
    → stereo depth 또는 disparity
    → stereo point cloud

SPAD ToF ×2
    → local point clouds

Odometry + IMU + TF
    → motion compensation 및 base transform

Fused point cloud
    → robot-centric local elevation map

다음 항목을 각각 PASS / PARTIAL / FAIL / UNKNOWN으로 평가하세요.

1. 좌우 영상 획득
2. 좌우 카메라 calibration
3. 좌우 timestamp synchronization
4. stereo baseline 확인
5. stereo depth 생성 가능성
6. SPAD ToF 0 데이터
7. SPAD ToF 1 데이터
8. 초음파 데이터
9. IMU 데이터
10. odometry 데이터
11. joint state 데이터
12. sensor-to-base TF
13. odom-to-base TF
14. 로컬 elevation mapping 전체 준비도

# 보고서 작성 형식

현재 로컬 작업 디렉터리에 정확히 다음 파일을 작성하세요.

`report_sensor_check.md`

보고서는 한국어로 작성하고 다음 구조를 사용하세요.

# TITA Sensor Check Report

## 1. Executive Summary

아래와 같은 한눈에 보는 표를 포함하세요.

| 항목 | 상태 | 핵심 결과 |
|---|---|---|
| Stereo camera | PASS/PARTIAL/FAIL/UNKNOWN | ... |
| SPAD ToF 0 | ... | ... |
| SPAD ToF 1 | ... | ... |
| Ultrasonic | ... | ... |
| IMU | ... | ... |
| Odometry | ... | ... |
| Joint state | ... | ... |
| TF | ... | ... |
| LiDAR/Tower | ... | ... |
| Elevation-map readiness | ... | ... |

## 2. Robot and ROS Environment

- SSH host
- hostname
- OS
- ROS distro
- ROS_DOMAIN_ID
- RMW implementation
- sourced workspace
- 현재 실행 중인 주요 perception 관련 node

## 3. Detected Sensor Inventory

모든 센서와 관련 토픽을 표로 정리하세요.

| Sensor | Topic | Type | Publisher | Rate | Frame | Status |
|---|---|---|---|---:|---|---|

## 4. Stereo Camera Check

- left/right topic
- image metadata
- CameraInfo
- timestamp synchronization 결과
- baseline
- TF
- disparity/depth 토픽 존재 여부
- stereo depth 생성 가능성
- 발견된 문제

## 5. SPAD ToF Check

각 센서를 별도 subsection으로 작성하세요.

- metadata
- PointCloud2 fields
- point count
- valid-point ratio
- 거리 범위
- rate
- frame
- TF
- elevation mapping 사용 가능성

## 6. Ultrasonic Check

## 7. IMU, Odometry and Joint-State Check

## 8. TF Tree and Sensor Extrinsics

다음 표를 포함하세요.

| Parent | Child | Translation | Rotation | Static/Dynamic | Status |
|---|---|---|---|---|---|

## 9. LiDAR and TITA Tower Check

## 10. Elevation Mapping Readiness

다음을 명확하게 작성하세요.

- 현재 바로 가능한 것
- 추가 calibration이 필요한 것
- 누락된 데이터
- 가장 큰 blocker
- 센서 융합 전에 먼저 해결해야 할 순서

## 11. Recommended Next Steps

최대 7단계로 우선순위를 정리하세요.

예상되는 흐름은 다음과 같습니다.

1. stereo raw stream 검증
2. CameraInfo 및 stereo calibration 검증
3. stereo depth/pointcloud prototype
4. SPAD FOV 및 pointcloud 검증
5. TF 정리
6. fused pointcloud
7. robot-centric elevation map

## 12. Commands Executed

실제로 실행한 주요 read-only 명령과 결과 요약을 기록하세요.
비밀번호, 토큰, 민감한 환경변수는 기록하지 마세요.

## 13. Raw Findings

긴 출력 전체를 붙이지 말고,
판정에 필요한 핵심 metadata와 오류 메시지만 정리하세요.

# 판정 원칙

- 실제 명령 결과에만 근거하세요.
- 예상 토픽 이름을 실제 토픽처럼 쓰지 마세요.
- 확인하지 못한 사항은 UNKNOWN이라고 쓰세요.
- 문서상 가능하다는 것과 현재 로봇에서 실제 작동한다는 것을 구분하세요.
- 토픽이 존재하지만 메시지가 없으면 PARTIAL 또는 DRIVER INACTIVE로 구분하세요.
- 메시지는 나오지만 TF 또는 calibration이 없으면 elevation mapping 준비도는 PARTIAL로 판정하세요.
- 결과를 과장하지 마세요.

모든 검사가 끝나면 다음을 출력하세요.

1. 생성한 보고서 경로
2. 전체 센서 상태 5줄 이내 요약
3. elevation map 구현을 막는 가장 큰 blocker 3개
4. 로봇 상태나 설정을 변경하지 않았음을 확인