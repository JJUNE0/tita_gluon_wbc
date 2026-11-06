# FlashSAC 다음 학습부터 W&B + 10,000-step 영상 기록

- Execution Domain: `TRAINING_SIM` (로거·스케줄), `VALIDATION_SIM` (녹화), `DESKTOP_DRY_RUN` (회귀 검사)
- Policy Checkpoint SHA256: `9037c60efcd38aedfe1261228dfb474c0cb4c51b6262bcff1851ea00705eabec`
  - 검증에 사용한 `tita_flash_sac_161707_506246/model_10000/actor.pt`
- Evidence Status: 신규 영상 검사·실제 렌더링·온라인 업로드 `PASS`. 전체 회귀 검사는 기존 3건 때문에 `FAIL`.
- Observed Metrics / Behavior / Log Summary: 500 RGB frames, 50 fps, 640×480, MP4 1,194,062 bytes.
  W&B 서버의 media 파일까지 확인했다. 보행 품질을 판정한 실험은 아니다.
- Branch: `agent/codex/tita-walk`
- 요청: 다음 학습부터 W&B에 올리고, 10,000스텝 간격으로 영상도 올린다.

## 동작

- `TitaFlatFlashSACRunnerCfg`: 기본 `logger="wandb"`, `wandb_mode="online"`,
  `video_interval=10000`, `video_length=500`.
- 기본 project는 `tita_flat_flash_sac`다. 현재 인증 계정은 `bjy6614-postech`에서 사용 가능하다.
- 학습 지표와 영상이 같은 run에 기록된다. 모델 가중치 자체의 cloud 업로드는 추가하지 않았다.
- 10,000은 vector environment step 기준이다. 1024 env에서는 10,240,000 transitions마다 해당한다.
- 영상 스텝에 해당 checkpoint를 저장하고, 별도 Python/Isaac 프로세스에서 저장된 정책·환경을 읽어
  1 env deterministic rollout을 녹화한다. 500 control steps는 현재 TITA 환경에서 10초다.
- 영상 생성은 단일 background worker로 순서대로 진행하며, W&B 호출은 부모 학습 프로세스에서 수행한다.
  부모 학습 환경에 카메라를 추가하거나 관측·보상·RNG·reset을 바꾸지 않는다.
- `video/rollout`은 `video/checkpoint_step`을 기준으로 기록한다. 영상이 늦게 완성돼도 과거 W&B
  internal history step을 덮어쓰지 않는다.
- 정규 checkpoint 저장 간격과 영상 간격이 달라도 영상 스텝의 checkpoint를 추가 저장한다.
- 마지막 대기 영상은 W&B run을 종료하기 전에 처리한다.
- worker 제한 시간은 영상당 300초다. 렌더링·hash 검증·W&B 호출 오류는 영상별 `FAIL`과
  `video/failures`로 남기며 학습 업데이트는 계속 진행한다. 실패 영상의 자동 재시도는 없다.
- `--video_interval 0`은 영상 off, `--video_length`는 길이 변경이다.
  `--logger tensorboard/console`, `--wandb_mode offline`을 명시하면 해당 선택을 따른다.

현재 실행 중인 TensorBoard 학습(PID 113805)은 원래 인자로 계속 동작한다. 재시작·resume하지 않았다.
이 변경은 다음 실행부터 적용된다. 이번 온라인 확인은 별도의 `logging-validation` run이다.

## 증거

| 검사 | 결과 | 증거 |
|---|---|---|
| 영상 스케줄·checkpoint 저장·비동기 진행·비활성화·오류 및 hash mismatch 처리 | `PASS` 6/6 | [전용 검사](flash_sac_video_tests_final.log) |
| 실제 Isaac RGB/MP4 녹화 | `PASS` 500 frames, 50 fps | [결과 JSON](flash_sac_video_smoke/render.json), [MP4](flash_sac_video_smoke/model_10000.mp4), [로그](flash_sac_video_smoke.log) |
| 영상 프레임 시각 확인 | `PASS` 로봇과 바닥 확인 | [250번째 프레임](flash_sac_video_smoke/frame_250.png) |
| 실제 W&B 온라인 업로드 | `PASS` 서버 media MP4 존재 확인 | [업로드 JSON](flash_sac_video_upload_evidence.json), [로그](flash_sac_video_upload.log) |
| FlashSAC 전체 검사 | `FAIL` 47개 중 44 PASS, 기존 3건 실패 | [전체 검사](flash_sac_wandb_video_tests_final.log) |
| 기존 3건을 HEAD runner 설정으로 재현 | 동일 1 FAIL + 2 ERROR | [재현 로그](flash_sac_preexisting_test_failures.log) |
| `./scripts/agent-check.sh` | `PASS`: Python 685개, URDF 8개, diff·실험 경로 검사 | [검사 로그](flash_sac_wandb_video_agent_check.log) |

온라인 시험 영상:
[video_logging_validation_20261027](https://wandb.ai/bjy6614-postech/tita_flat_flash_sac/runs/gf3fcrmo)

- Cloud file: `media/videos/video/rollout_0_25b83bd156086201a3a1.mp4`
- MP4 SHA256: `25b83bd156086201a3a1f854ce7c2dbe6ec85b017d44c2927d230c8ce93c488d`

검사 명령:

```bash
# DESKTOP_DRY_RUN
/home/cocel/isaac/env_isaaclab/bin/python -m unittest discover \
  -s test -p 'test_flash_sac_video.py' -v
/home/cocel/isaac/env_isaaclab/bin/python -m unittest discover \
  -s test -p 'test_flash_sac*.py' -v

# VALIDATION_SIM
/home/cocel/isaac/env_isaaclab/bin/python -u lab/ddt_lab/scripts/flash_sac/play.py \
  --checkpoint lab/ddt_lab/logs/flash_sac/tita_flash_sac_161707_506246/model_10000 \
  --num_envs 1 --steps 500 --device cuda:0 --headless \
  --video docs/exp/2026-10-27/flash_sac_video_smoke/model_10000.mp4 \
  --video_result docs/exp/2026-10-27/flash_sac_video_smoke/render.json
```

## 남은 제한과 기존 실패

- 신규 자동 영상 경로의 시간축·저장·부모 run 업로드 연결은 CPU learner/가짜 renderer 검사로,
  실제 렌더링과 실제 온라인 업로드는 각각 별도로 확인했다. 다음 학습을 실제 10,000스텝까지
  새로 돌려 전체 경로를 한 번에 확인한 것은 `NOT_TESTED`다.
- GPU를 공유하므로 영상 생성 중 처리량과 VRAM 여유가 줄어들 수 있다.
- 전체 검사의 기존 문제는 다음과 같다. 이번 변경 전 HEAD runner 설정으로도 동일하게 재현된다.
  1. `test_tita_my_flat_config_refactor`의 AST asset fixture가 `DDT_TITA_URDF` 상수를 제공하지 않는다.
  2. export 검사가 참조하는 과거 `172127_928297/model_15000/actor.pt` 파일이 없다.
  3. action-range 검사가 예전 hip 기본각 +0.1을 가정해 현재 gain/default pose와 0.1 rad 차이 난다.
- 이 세 오류를 이번 로깅 변경에서 수정하지 않았다. 전체 suite PASS로 보고하지 않는다.
- 학습 수렴·보행 성공·실기 적합성: `NOT_TESTED`.

## 변경 파일

- `lab/ddt_lab/ddt_lab/tasks/manager_based/locomotion/robots/tita/agents/flash_sac_cfg.py`
- `lab/ddt_lab/scripts/flash_sac/{train.py,play.py,runtime.py,video_logging.py,README.md}`
- `test/{test_flash_sac_video.py,test_flash_sac_wandb.py,test_flash_sac_config.py}`
- `docs/exp/2026-10-27/flash_sac_*`: 보고서·검사 및 영상 증거.

W&B의 [media logging](https://docs.wandb.ai/guides/track/log/)과
[custom metric axis](https://docs.wandb.ai/ref/python/experiments/run/) API를 사용한다.
최종 diff를 검토했고, 작업 전 수정되어 있던 tracked 파일 39개의 SHA256이 모두 그대로임을 확인했다.
Commit/push/PR 없음.
