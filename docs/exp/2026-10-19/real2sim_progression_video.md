# 발표 영상: Real2Sim-guided policy refinement (FlashSAC baseline 대 Real2Sim 50k)

- Execution Domain: VALIDATION_SIM (MuJoCo rollout 8개 + 기록된 qpos 렌더링). 로봇 명령 없음
- Policy Checkpoint SHA256:
  - 위 줄 FlashSAC (baseline): `6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05`
    - ONNX `f44f07ed44970e3ff565eae67fd9229adf0be5c02215591c52a691ffcbb71b2a`, 관측 33
    - 2026-10-17 velocity-bias 영상의 FlashSAC와 같은 정책
  - 아래 줄 FlashSAC + Real2Sim (headw0 50k): `0a6f8ef2bb8a324bf6f6fb7689297f9001bd4b57896daa0cb9ead4953162f4a7`
    - ONNX `284b4166297fafe5606e58d7b66d9e4570980b839ebde433cbd7a85549313a4c`, 관측 35, MA2 없음
    - 실기 run 142158에서 정지 yaw 0.017 °/s를 보인 정책
- Evidence Status:
  - rollout 8/8 PASS
  - 같은 열 위·아래 줄의 RL 진입 qpos 차이 0.0
  - 렌더 base 위치와 기록 위치 일치(`column_*_verification.json`)
  - 최종 MP4 검증은 아래 "산출물" 참고
- 운영자 요청(2026-10-19): 2026-10-17 `velocity_bias_presentation_clean_grid` 영상처럼, 50k와 옛 FlashSAC를 2×4로 비교. 5분 정지, 10배속

## 구성

`test/render_real2sim_progression.py`(collect → preview → render → compose). rollout은 `test/screen_sphere_wheel_runs.py`의 `rollout`이다.

- 시나리오 `stand300`: 0 명령 300 s, 같은 기립 과정, rng 42. 처음 2 s는 1배속, 이후 10배속이다(955 frames, 30 fps).
- 열은 왼쪽부터 real2sim으로 찾은 실기 갭을 하나씩 누적한다(`sim2real/gap.md`).

| 열 | 표시 | 물리 | 갭 |
|---|---|---|---|
| 1 | NOMINAL / MuJoCo default | 원통 휠, 무릎 공칭 (plant B_nom) | — |
| 2 | + WEAK KNEE / Knee torque L 0.60 · R 0.75 | 원통 휠 + 무릎 PD × 0.60/0.75 (plant B) | G1 |
| 3 | + POINT WHEEL CONTACT / Low yaw scrub (sphere) | 구 휠 충돌체 + 약한 무릎 (plant A) | G4 |
| 4 | + LEG HF OVERREACTION / 25 Hz action gain g = 1.5 | plant A + 다리 action에 raw + 1.5·(raw − 이전 raw) | G2 (실기 추정 g ≈ 1–1.5) |

- 화면 표시: 각 칸에 제어기 이름, SIM 시간, 조건, 시작점 거리, heading 변화(qpos 쿼터니언 yaw를 unwrap한 값), 고정 월드 inset(같은 열 위·아래 같은 축척)을 넣었다.
- MuJoCo 모델:
  - 커밋 88d7f240(다른 작업)에서 `tita_gluon_ws`가 삭제되면서 sim2sim 기본 scene 경로가 사라졌다.
  - 그래서 c8c159d3의 `mujoco_corrected/`를 `git archive`로 scratchpad에 꺼내 `--scene-xml`로 썼다.
  - git blob이 이전 검증과 같다: scene `07ff225f…`, robot `1f0e41dc…`(`plan.json`).
  - 정책 config는 `configs/`에 scene 경로만 바꾼 사본을 썼다. 원본 config SHA256은 `plan.json`에 있다.

## 결과 (300 s, `results.json`, 각 열 마지막 프레임)

| 열 | FlashSAC baseline: 거리 / heading | FlashSAC + Real2Sim: 거리 / heading |
|---|---|---|
| NOMINAL | 5.31 m / −17.7° | 0.088 m / +0.3° |
| + WEAK KNEE | 9.01 m / −1673° (−6.2 °/s) | 0.062 m / +0.3° |
| + POINT WHEEL CONTACT | 7.39 m / −582° (−1.9 °/s) | 0.064 m / +0.5° |
| + LEG HF OVERREACTION | 10.25 m / −1247° (pitch std 6.2°) | 0.456 m / +4.6° (pitch std 0.18°) |

- baseline은 sim 공칭에서도 5 m 밀린다. velocity-bias 영상 당시와 같은 0 명령 drift다. 갭을 넣으면 계속 회전한다.
- Real2Sim 50k는 앞 세 열에서 9 cm, 0.5° 이내에 선다. 고주파 g = 1.5에서는 0.46 m, +4.6°다.

## 4열 선택 근거 (G6 후방 편향을 넣지 않은 이유)

처음에는 4열을 "+ BACKWARD BIAS (IMU +3°, G6)"로 수집했다(`collect_attempt_imu3.log`).

- 결과: baseline 22.7 m / −485°, Real2Sim 50k **34.3 m** / +1.0°.
  - x_err가 clip −0.3 m에 붙으면 위치 피드백이 없어지고, 남는 편향만큼 약 11 cm/s로 계속 밀린다.
- 편향 크기 sweep(`bias_calibration.log`, 50k, 300 s):
  - IMU +1.5/+2°, CoM −2/−3/−4 cm: 0.02–0.22 m (x_err 포화 없음)
  - IMU +2.5°: x_err 포화, −6.9 cm/s, 19 m
- 실기 50k 긴 정지(62–79 s)는 x_err 포화 후 −0.12 ~ −0.30 cm/s였다. 경계 바로 위에 있는 것으로 보이며, 어떤 단일 편향 값도 이 상태를 재현하지 못한다.
- 결론: G6는 아직 열린 갭이고 결과가 편향 크기에 날카롭게 의존한다. 그래서 발표 영상의 "해결한 갭" 열에서는 뺐다. 운영자 선택으로 해결된 갭 G2(g = 1.5)를 넣었다(`hf_column_check.log`: g = 1에서는 baseline 26.3 m / −191°, Real2Sim 0.06 m / 0°).
- 함의: x_err clip ±0.3 m는 지속 편향이 클 때 위치 유지를 포기하게 만든다. G6 대응(보정 또는 학습)에서 함께 봐야 한다.

## 산출물

`real2sim_progression_video/`:
- `flashsac_real2sim_progression_2x4_10x.mp4`
- `column_*.mp4`
- `preview_*.png`
- `video_verification.json`, `column_*_verification.json`
- `plan.json`, `results.json`, `source_hashes.json`, `rl_entry_qpos_max_abs_diff.json`
- `configs/`
- 로그

원본 신호 `signals/*.npz`는 git 제외(로컬 보관)다.

## 영상 검증 (PASS, `video_verification.json`)

- 최종 MP4 `flashsac_real2sim_progression_2x4_10x.mp4`
  - 1920×1080, H.264/yuv420p, 30 fps, 955 frames, 31.83 s, 18,685,783 bytes
  - SHA256 `3baaf39d59dee243e9d69ce52a540f573ca51e5268fee3dd335bf6a89cf84c4d`
- 렌더는 물리 step 없이 기록된 qpos만 그렸다. 렌더 base 위치와 기록 위치의 최대 차이는 2.4e-7–4.8e-7 m다.
- 합성 시점에 원본 신호 해시가 바뀌지 않았음을 확인했다(`source_hashes.json`).
- 재생 1/15/31 s 프레임(`encoded_*.png`)을 직접 확인했다. 글자와 로봇이 겹치지 않는다. 같은 열의 고정 월드 inset은 같은 축척이다.
- NOT_TESTED: PowerPoint 앱 재생

재현:

```bash
git archive c8c159d3 tita_gluon_ws/src/ddt_ros2_control/urdfs/tita_description | tar -x -C <dir>
P=~/venvs/cosim_ros2_jazzy/bin/python
S=<dir>/tita_gluon_ws/src/ddt_ros2_control/urdfs/tita_description/mujoco_corrected/scene.xml
$P test/render_real2sim_progression.py --output docs/exp/<date>/<new dir> --stage collect --scene-xml $S
# 열마다 따로 실행: --stage render --column 0..3 --scene-xml $S
$P test/render_real2sim_progression.py --output docs/exp/<date>/<new dir> --stage compose --scene-xml $S
```

## 발표용 변형: 조건 표시 제거 (`--variant nolabel`, 운영자 요청)

- 오른쪽 위 조건 제목·설명 두 줄을 없앴다. 조건 설명은 PPT에서 한다.
- 남은 Distance from start, Heading change를 오른쪽 위(왼쪽 위 이름 줄과 같은 높이, y = 10 px)로 올렸다.
- 그 밖의 표시(제어기 이름, SIM 시간, 고정 월드 inset, x10)와 원본 rollout 신호는 위와 같다. 새 rollout은 없다.
- `flashsac_real2sim_progression_2x4_10x_nolabel.mp4`
  - 1920×1080, H.264/yuv420p, 30 fps, 955 frames, 31.83 s, 17,870,911 bytes
  - SHA256 `0dd711e81c0234932ff4a5326d793771c5494ee7f4e3b6d26d00f802b0f6d1ba`
  - `video_verification_nolabel.json` PASS
- 재생 15 s 프레임(`encoded_15s_nolabel.png`)과 마지막 프레임 미리보기를 직접 확인했다. 글자끼리, 글자와 로봇이 겹치지 않는다.
- 열 순서(왼쪽부터 누적): NOMINAL → + 약한 무릎 → + 휠 점접촉 → + 다리 고주파 과반응 g = 1.5
