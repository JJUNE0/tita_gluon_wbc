# FlashSAC 13:56:54 혼합 실기 로그 확인

Execution Domains: ROBOT_READ_ONLY (종료된 실행의 로그 조회·복사·SHA256 읽기), DESKTOP_DRY_RUN (복사 검증·SQLite 읽기 전용 검사)

Evidence Status: PASS — 복사 무결성 및 실행 metadata 확인. 자유 drift 속도·손 지지 구간 추정은 NOT_TESTED: 사용자 재수집 선택에 따라 혼합 구간의 성능 판정을 보류했다.

Policy Checkpoint SHA256: `6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05`

ONNX SHA256: `f44f07ed44970e3ff565eae67fd9229adf0be5c02215591c52a691ffcbb71b2a`

Branch: `agent/codex/dev_tita_gluon`

대상 실행은 `flashsac_60000_135654_368311385_output_true`다. SBC의 기존 접근 주소에서 지정한 실행의 summary/console/bag-console/bag만 읽기 전용으로 조회·복사했다. 네트워크 sandbox의 최초 SSH 시도는 socket 권한으로 실패했고, 읽기 전용 로그 접근에 대한 승인된 escalation으로 조회/복사를 수행했다. 로봇 파일·서비스·프로세스·모터 상태를 변경하는 명령은 실행하지 않았다.

## 확인된 사실

- 실행 summary: 2026-10-17 13:56:54~14:00:24 KST, output enabled=true, **velocity bias enabled=false**. 이는 실행 설정 확인이며 이번 작업에서 프레임별 bias 진단을 복원한 결과는 아니다.
- Console의 RL 진입은 13:57:51.7 / 13:59:24.1 / 13:59:39.1 KST 세 번이다. 각 시각은 console ROS timestamp 기준이다.
- Exit 130은 console의 Ctrl-C/SIGINT 기록과 일치한다. 종료 과정에는 teleop exit −11 및 controller group의 SIGTERM/SIGKILL도 기록돼 있다. 이 종료 문제를 주행 중 제어 오류의 증거로 혼동하거나 종료 전체가 정상이라고 판정하지 않는다.
- Bag metadata: 약 203.25초, 전체 112,108 messages, atomic TrainingSample 10,130개. 로컬 read-only SQLite `quick_check=ok`, 실제 topic count와 일치했다.
- 원격/로컬 SHA256가 summary, console, bag-console, metadata.yaml, DB3 **5개 모두 일치**한다. [복사 검증 로그](flashsac_135654_mixed_review/copy_verification.log), [SQLite 검사](flashsac_135654_mixed_review/bag_integrity.json).

## 혼합 조건 처리와 다음 수집

사용자는 명령을 줬다가 놓은 구간과 손으로 뒤로 밀리지 않게 잡은 구간이 혼재한다고 설명했다. 명령 상태는 기록으로 분리할 수 있지만, zero command와 낮은 휠 속도만으로 외부 지지 유무를 확정할 수 없다. 손 지지 여부를 자유 정지로 추정해서 baseline 속도에 섞지 않는다. 원본을 유지하고 시간 annotation을 요청했으며 사용자가 새로 수집하겠다고 답해 이 로그의 상세 구간 분석은 보류했다.

새 수집은 같은 checkpoint와 bias OFF 조건에서 ① 자유 zero-command 정지 ② 명령 후 release 정지 ③ 손 지지 정지를 각각 별도 실행/bag으로 기록하는 방법을 권했다. 우선 자유 정지에서 IMU/encoder/FK 추정속도와 고정 카메라·바닥 눈금의 실제 이동을 비교한다. 손 지지 구간은 외력이 있는 조건이며 휠 헛돎이 있으면 몸체 정지와 wheel rolling proxy가 다를 수 있으므로 별도 해석한다. 자동 시작/종료나 실기 실행은 수행하지 않았다.

추가 파일은 이 보고서와 `flashsac_135654_mixed_review/`의 복사 로그·데이터·무결성 기록이다. 기존 실기 코드·설정·정책과 관련 없는 변경은 건드리지 않았다. 필수 `./scripts/agent-check.sh`의 전체/개별 결과는 [agent_check.log](flashsac_135654_mixed_review/agent_check.log)에 보관한다. 커밋/push/배포 없음.
