# 다리 action 필터 선택 검토

- Date: 2026-10-18 (Asia/Seoul).
- Execution Domain: `DESKTOP_DRY_RUN` (기존 sim 산출물·코드 검토 및 필터 응답 계산).
- Policy checkpoint SHA256: `79f9175bb8c3be0c5138866e30891b90cc1282b6c98023cdb76c2e33b229068c`.
- ONNX SHA256: `26f0d86b65a68475fb8a315fb31e829ae16eaa2cf16dabbbcf38e69f28c933e9`.
- Deployment config SHA256: `a24c2137969f854fc98cc3027884dbbadad4060f18db7758b028c12ca1405719`.
- Evidence Status: 저장된 결과 집계·필터 응답 계산 PASS; 실제 진동 해소 NOT_TESTED. 이번 검토에서 새 MuJoCo rollout은 실행하지 않았다.
- Branch: `agent/codex/dev_tita_gluon`; commit/push 없음.

## 선택

첫 후보는 **다리 6개에만 MA2**다. 정책 50 Hz tick마다 `applied[k] = (raw[k] + raw[k-1])/2`를 계산한다. 500 Hz PD에서는 그 목표를 유지하면서 현재 encoder에 대한 P/D를 계속 계산한다.

실기 기록에서 관측된 정책 출력의 period-2 교번을 직접 겨냥하면서 저주파 목표를 가장 적게 바꾼다는 이유다. 50 Hz에서 전달함수는 `H(z)=(1+z^-1)/2`; 진폭은 `abs(cos(pi*f/50))`, 지연은 통과대역에서 10 ms다. EMA 0.5의 전달함수는 `0.5/(1-0.5*z^-1)`다.

| 주파수 | MA2 진폭비 | EMA 0.5 진폭비 |
|---|---:|---:|
| 3 Hz | 0.9823 | 0.8836 |
| 5 Hz | 0.9511 | 0.7529 |
| 25 Hz | 0 | 0.3333 |

EMA는 이 후보 계수에서 25 Hz를 남기고 저주파 동작도 더 약화시킨다. 더 긴 이동평균이나 더 강한 저역통과를 먼저 쓰기보다, 현재 관측된 교번에 맞는 짧은 MA2를 우선 검토하는 편이 타당하다. 이 선택은 필터의 단독 응답과 기존 sim 증거에 근거하며 실기 폐루프 안정성 보장은 아니다.

## 저장된 증거 재확인

[기존 보고서](leg_action_filter_sim.md), `sim_leg_action_filter.py`와 저장된 JSON을 직접 읽었다. 현재 스크립트 SHA256은 `44b641934bdcf37cab08d31b8525ea50831ea376447d6924aa4d963672ecaf60`이며, 결과 생성 버전 `75a11b90…`과 구분되어 있다. 기존 regression log에는 표 출력 추가 후 4개 job의 일치가 기록되어 있다. 이번 검토에서 그 4개를 다시 실행한 것은 아니다.

- Part A 192 job: 각 필터 48개. `none`, `ma2_legs`, `ema0.5_legs` fault 0; `ma2_all` fault 1.
- Part B 72 job: 필터 없음 36개 중 fault 11; `ma2_legs` 36개 중 fault 6. 극단 proxy 조건의 불안정은 남는다.
- 실제 A80k/현재 게인의 25 Hz 진동은 nominal sim에서 재현되지 않았다. Part B는 인위적인 고주파 증폭 proxy다.
- MA2 적용 action의 정확한 25 Hz 성분이 없어지는 것은 필터 수식의 성질이다. 이것만으로 실제 토크·관절 진동이나 다른 주파수의 불안정까지 제거됐다고 해석할 수 없다.
- 10 ms는 고정 샘플링에서의 필터 지연이다. 전체 센서·연산·CAN 지연과 합쳐 평가해야 한다. action delay randomization과 MA2의 폐루프 효과가 같다는 보장도 없다.

## 구현할 때 지켜야 할 동작

1. **위치:** ONNX 출력 뒤, RL `ActionAdapter.compute` 앞. 휠은 그대로 통과시킨다. 현재 bundle은 native와 policy 순서가 같아 다리 indices 0,1,2,4,5,6이지만, 일반 구현에서는 action→native joint 매핑으로 고른다.
2. **주기:** 정책 tick마다 정확히 한 번 갱신한다. 500 Hz 루프마다 같은 raw action을 다시 평균하면 2-tap 필터 의미가 사라진다.
3. **raw/applied 분리:** `last_action` 관측은 기존 raw 정책 출력을 유지한다. PD에만 applied action을 넣는다. raw 정책 출력의 교번은 남을 수 있으므로 raw와 applied를 각각 감시해야 한다.
4. **상태:** RL 진입 첫 출력으로 필터를 초기화하고, RL 이탈·오류 때 reset한다. 첫 raw 그대로 초기화하면 영점과 평균하면서 생기는 인위적인 반 크기 출력을 피하지만, RL 첫 목표 점프 자체를 줄이지는 않는다.
5. **정지 경로:** transform/sit/return_to_sit/estop/종료 0토크 경로는 이 RL action 필터를 통과시키지 않는다. 최종 토크나 센서 속도를 함께 저역통과하면 기존 damping·정지 동작을 바꾸므로 범위를 넓히지 않는다.
6. **기록과 teacher:** 현재 `TrainingSample.action_raw`와 `teacher_action`은 raw를 기준으로 한다. 필터 추가 시 applied action/다리 목표도 기록하고, teacher는 필터가 반영된 실제 적용 목표(+wheel bias)를 기준으로 계산해야 한다. 그렇지 않으면 나중의 학습 데이터와 실제 전송 토크가 맞지 않는다. baseline/bias 토크 비교도 동일한 applied action을 기준으로 해야 한다.
7. **옵션:** 기본 OFF로 두고, sim2sim Python과 실기 C++에 같은 업데이트/reset 의미를 구현해 parity를 확인하는 것이 다음 단계다. 첫 효과 분리는 velocity bias OFF 조건이 해석하기 쉽다.

이 검토에서는 제품 코드·설정·기체를 변경하지 않았다. 실기 효과의 판단 기준은 applied 다리 action step, 정책 tick 토크 step, 모터 feedback, 25 Hz 성분, 2–3 Hz pitch 흔들림 및 진입 과도다. 정지 중 raw action lag-1만으로 필터 실패를 판단해서는 안 된다. 별도 조건 변화와 제로커맨드 drift 개선도 구분한다.

## 완료 검증

문서만 추가했다. 필터 수식과 저장된 job/fault 집계를 직접 계산했으며, 제품 코드·배포 및 새 sim/실기 시험은 수행하지 않았다. 최종 문서 diff 공백 검사 PASS, 이전 배포 manifest 대비 제품 resource 해시 일치 PASS다. 필수 `agent-check.sh`는 기존 `my_flat_env_cfg.py`의 공백 오류 6개로 전체 FAIL; Python syntax 567 PASS, URDF 8 PASS다. [검사 로그](leg_action_filter_design_review_agent_check.log).
