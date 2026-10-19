# FlashSAC 실기 비교 후보 선정

Execution Domains: DESKTOP_DRY_RUN — 기존 40개 체크포인트 평가 및 export hash 감사. VALIDATION_SIM — frozen 후보 3개와 현재 정책의 무보정 명령 비교.

Evidence Status: PASS — 40개 export/source hash 및 후보 인터페이스 일치, 4개 120초 실행 완주. SUSPICIOUS — 실기 성능 순위의 전이. 실제 후보 기립·실기 drift/진동은 NOT_TESTED.

Branch: `agent/codex/dev_tita_gluon`

## 추천

첫 실기 비교 후보는 **A/50000**이다. A=`tita_flash_sac_115632_883848`, B=`tita_flash_sac_193248_068255`이며 현재는 A/60000이다. A/50000은 같은 run의 인접 체크포인트이며 명목 drift가 작고 이번 명령 오차 비교도 허용 범위 안이다. 일반적인 균형·기립·실기 성능의 우월성을 입증한 것은 아니다.

사용자가 B/10000의 실기 낙상을 우려해 우선 후보에서 제외했다. 기존 시뮬 7조건의 낮은 최악 drift만으로 실기 추천하는 것은 부족하다. 실제 B/10000이 넘어지는 것을 이번 작업에서 확인한 것은 아니다.

## 기존 무보정 기록

모두 같은 scene의 평면 평가이며 residual OFF다. 표의 속도는 마지막 20초 평균이다. 60초 명목 survey는 seed270/warmup8초, 300초 명목은 seed911/warmup1.2초, 물리 7조건은 seed910/warmup1.2초다. 서로 다른 길이의 시험을 동일 초기조건 비교라고 해석하지 않는다. 물리 조건은 기본, mass/inertia ×1.15/×1.30, base CoM x ±5mm, friction 0.2/0.8이다.

| 정책 | 명목 60초 속도 | 명목 300초 속도 | 7조건 최악 평균속도 절댓값 |
|---|---:|---:|---:|
| 현재 A/60000 | +0.01603 m/s | +0.01948 m/s | 0.15471 m/s |
| **A/50000** | **+0.00939 m/s** | **+0.01312 m/s** | **0.14282 m/s** |
| A/75000 | +0.00143 m/s | +0.01442 m/s | 0.20917 m/s |
| B/60000 | −0.00304 m/s | +0.00882 m/s | 0.18498 m/s |

후보마다 이 7조건은 7/7 완주했다. A/75000의 60초에서 작은 drift가 장시간 성능을 대표하지는 않는다. A/50000의 개선은 명목 60초 약 41%, 300초 약 33%, 7조건 최악값 약 8%다. 실기 개선율은 아니다.

## 신규 명령 비교

실행 전 [protocol.json](flashsac_hardware_candidates/protocol.json)을 저장했다. seed104, 초기 pitch0, 기존 transform-up에서 RL로 전이 후 8초 warmup이다. 120초 동안 각 20초의 `[정지, +0.1m/s, 정지, −0.1m/s, yaw+0.2rad/s, 정지]`를 입력했다. 기존 runner는 startup 전에 world-body 장애물 collision을 비활성화해 평면을 유지한다. raw previous action, frozen ONNX, 기존 leg/wheel PD를 사용하고 각 physics substep에서 residual 없는 motor 출력과의 일치를 1e−6 Nm 이내로 검증했다. GT 전후 속도는 평가에만 사용했다. Yaw는 IMU를 ZYX heading derivative로 변환한 값이며 body gyro-z와 구별한다.

4개 정책 모두 6,000tick을 완주했고 기존 자세·높이·joint-limit guard 위반은 없었다. 실기의 전이 상태를 재현하거나 여러 seed를 검증한 것은 아니다. 비교 screen은 사전에 `candidate RMSE <= current * 1.1 + .002 m/s / .01 rad/s`로 정한 상대 회귀 조건이며 절대 추종 정확도의 합격 기준은 아니다.

| 정책 | 전후 속도 RMSE | yaw RMSE | 최대 roll/pitch 절댓값 | 상대 command screen |
|---|---:|---:|---:|---|
| 현재 A/60000 | 0.08306 m/s | 0.07710 rad/s | 6.02° | PASS (기준) |
| **A/50000** | **0.08732 m/s** | **0.07966 rad/s** | **5.86°** | **PASS** |
| A/75000 | 0.12567 m/s | 0.07842 rad/s | 5.42° | FAIL (전후 속도) |
| B/60000 | 0.19161 m/s | 0.05541 rad/s | 7.18° | FAIL (전후 속도) |

A/50000도 +0.1m/s 명령에서 약 +0.270m/s, −0.1에서 약 −0.231m/s로 현재 정책과 마찬가지로 속도 gain 오차가 있다. A/75000은 약 +0.329/−0.313, B/60000은 약 +0.305/−0.530으로 과응답이 크다. 따라서 명목 정지만 보고 B/60000이나 A/75000을 최우선으로 선택하지 않는다. [전체 결과](flashsac_hardware_candidates/command_comparison.json).

## Policy hash와 export

각 directory는 `docs/exp/2026-10-16/velocity_bias_overnight/exports/<checkpoint_id>/`다. 원본 actor는 `lab/ddt_lab/logs/flash_sac/<run>/model_<step>/actor.pt`다.

| 정책 | Policy checkpoint SHA256 |
|---|---|
| A/60000 | `6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05` |
| A/50000 | `d5b7c981c4c4cd5375fd5513ec12f02c7abada4ca21df8727729faf1d0e31e7c` |
| A/75000 | `381e846e3ffb1d5a9ed629c02b55c9740ec3c5b089ca443f38b3d73b6abbd730` |
| B/60000 | `9b0d8897472dc567619d49df3e6df08813dcbb15b018f23ed58060e92e1b139b` |

40개 모두 source actor·ONNX·config의 hash를 저장 manifest와 대조했다. 후보 4개의 observation/action 정의와 robot PD/default 설정 일치도 assert했다. 저장된 export parity (256입력)를 참조했고 신규 Torch/ONNX parity 검사는 실행하지 않았다. hash와 기존 각 시도는 [archive_audit.json](flashsac_hardware_candidates/archive_audit.json)에 기록했다.

현재 `flashsac.launch.py`는 A/60000 hash와 bundle을 고정 검증한다. 따라서 파일만 덮어쓰고 실행하는 방식으로 교체할 수 없다. 후보 A/50000을 실기 비교하려면 별도 bundle로 보관하고 선택과 기록 hash가 일치하도록 코드 변경·배포가 필요하다. 이번 작업은 실기 접근·배포·controller/launch 변경을 수행하지 않았다.

## 変更・検証

추가 파일은 `test/review_flashsac_hardware_candidates.py`, 이 보고서, 동명 artifact directory와 run/agent-check log다. 신규 시뮬 4회와 archive hash 감사를 실행해 PASS. protocol·입력·결과 NPZ/JSON을 저장했다. run log의 Matplotlib cache 경고는 읽기 전용 HOME 대신 임시 cache를 사용했다는 알림이며 실행은 정상 완료했다.

필수 agent-check는 Python 구문 512/512, URDF 8/8 PASS이며 전체는 기존 `my_flat_env_cfg.py` 431/437/443/449/455/461행 공백 오류로 FAIL이다. [검사 로그](flashsac_hardware_candidates_agent_check.log). 실기 안정성·물리 Nm calibration·명령 응답의 실기 일반화는 NOT_TESTED다. 신규 controller·fine-tuning·commit/push 없음. 시작/종료 status와 현재 task diff를 확인했고 다른 기존 파일은 수정하지 않았다.
