# Static Target-Domain Adaptation — 계획 초안, 아직 동결하지 않음

작성일: 2026-10-16 (Asia/Seoul)

Execution Domain: **DESKTOP_DRY_RUN** (계획한 실험: **VALIDATION_SIM**)

Policy Checkpoint SHA256: `6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05`

Evidence Status: **BLOCKED — 상세 specification 파일 미제공.** 본 문서는 사용자 메시지에 근거한 초안이며 사전 동결 manifest가 아니다. Target 조건을 임의로 추가해 실행하지 않는다.

Observed Metrics / Behavior / Log Summary:

## 고정할 불변 조건

- model_60000 frozen actor, 원래 observation/action/history/scale/order/clip, wheel velocity PD, leg position PD, M4 24-State 유지.
- control/physics dt 0.02/0.005초. Wheel에만 bounded residual 추가. 기존 Q/R을 결과에 따라 바꾸지 않음.
- 각 Target의 mass/inertia/CoM/gain/lag/friction은 첫 physics step 전에 설정하고 episode 종료까지 유지. Controller/estimator에는 Target 값·라벨·변경 시각을 전달하지 않음.
- Base-link GT는 평가 전용, wheel midpoint/yaw는 보조. Sensor p/v와 GT 기준점 차이는 별도 기록. World XY/yaw hold 성공 주장은 하지 않음.
- 최초 p_hold·목표속도0 고정. 평가 미래나 정착 후 위치로 목표를 reset하지 않음. 이전900초 nominal 정착이나 Target 식별 후 구간만을 전체 배포 성능으로 제시하지 않음.
- 새로운 실험 소스와 증거만 추가. 기존 데이터·정책·runtime·보고서 보존, 실기 금지.

## 실행 순서

| 순서 | 실험 | 선행 gate와 기록 |
|---|---|---|
| Audit / replay | 기존 nominal FlashSAC-only·Fixed M4 exact 재현 | state/action/history/substep torque 일치, 불일치 시 후속 실행 금지 |
| **Phase 0** | **모든 사전 정의 단일 Target에서 FlashSAC-only drift 측정** | Target 시작 전 설정·고정 검증. 실패·정상 완료·startup 행동·최초 목표 drift를 모두 기록. 어떤 residual/online update도 없음 |
| Safety | 단일 Target의 Fixed M4 초기 안전성 | 같은 Target/초기 조건. Phase 0 실패도 숨기지 않음. 조건별 gate이며 한 조건 실패가 다른 조건을 막지 않음 |
| Shadow | 안전한 Target의 RLS 및 B1/내부reference shadow, B2 shadow | Nominal prior에서 시작. 센서와 실제 적용 residual command만 사용. 부족한 excitation·포화·support 위반에서 probing/update 중단 |
| Identification validation | Direct B, 독립 입력 p/v multi-step, 정보량·condition·P | 후보 A/B/c 동결 후 held-out 검증. Raw candidate와 active validated model을 별도로 기록 |
| Controller comparison | FlashSAC-only / Fixed / Bias-only / Reference-only / K-only / Bias+Reference / Full | 같은 초기 조건에서 전체 episode 비교. Target별·arm별 승인 및 NOT_TESTED 사유 보존 |
| Composite | 사전 정의 복합 Target | 단일 mismatch에서 해당 구성요소와 controller가 안정적으로 검증된 경우에만 실행 |

Phase 0 전체 결과와 표를 먼저 저장한 뒤 Fixed/Shadow 단계에 진입한다. Phase 0 정상 완료를 정지 성공으로 부르지 않는다. 실패 episode의 짧은 drift를 완료한 episode보다 좋은 결과로 해석하지 않는다.

## 온라인 갱신과 검증

`r = r_bias − K·(z−z_ref)`이며 `effective_offset = r_bias+K·z_ref`를 기록한다. Bias와 reference를 독립적인 물리 상수로 식별했다는 주장을 하지 않는다.

- A/B/c: constrained RLS, nominal 고정 회귀 중심. Shadow는 갱신할 수 있으나 검증 안 된 행렬을 active model로 채택하지 않음. 검증한 행렬 hash와 각 K의 원본 모델 hash를 연결.
- B1: 과거 sensor 위치 오차와 실제 입력 이력에 근거한 느린 보상. 일정 토크에 대한 실제 응답과 잔류 위치 오차를 함께 분석해 물리 평형 입력 식별과 구분.
- B2: shadow 제안·예측·거부만 기록하며 이번 active control에는 넣지 않음.
- Reference: 저속·자세/leg 안정 구간의 관측된22-State 평균. 최초 p_hold/v_target은 바꾸지 않음. nominal 대비 한도·관측 support·입력 jump 제한을 기록.
- K: validated A/B → 기존 Q/R DARE. 단일 변경 제한과 immutable nominal 대비 누적 제한을 각각 적용. 실패 시 마지막 검증 파라미터 유지. Target에서 실제 채택한 횟수와 첫 채택 시각을 보고.
- 물리 분기형 held-out 검증은 평가/진단용. 그 미래 GT나 counterfactual 결과를 온라인 추정기의 입력으로 제공하지 않음. 실제 온라인 채택에 사용할 causal validation 구간은 상세 specification과 함께 확정.

## 상세 파일 확인 후 동결할 값

Target sampling 분포/범위, 단일·복합 Target draw 목록, train/held-out seed와 개수, 초기 qpos/qvel 및 startup/최초목표 정의, 전체 horizon과 초기·후기 평가 구간, probe amplitude/주파수·cadence, residual 절대 예산/ramp/slew, safety/정보량/예측/제어의 수치 gate, 복귀 조건과 적응 완료 조건이 아직 미동결이다.

이전 실험 수치를 그대로 새 사양이라고 가정하지 않는다. 상세 파일을 확보한 후 사용자 본문과 대조하고, 모든 draw/seed·source/policy hash·gate를 manifest에 저장해 SHA256으로 동결한다. 실행기는 이 hash가 달라지면 중단하며 기존 실패 단계를 자동 덮어쓰지 않는다.

## 최종 보고 항목

Target별 완료/안전·최초 목표 최대drift·base IAE·초기/후기 오차·후반속도·pitch/leg/wheel torque, 직접B/held-out 예측·RLS 정보량, bias/reference/K 채택·거부 시각, 식별과 복귀에 필요한 데이터 시간, Full-vs-Bias+Reference paired 개선을 보고한다. 과거 K 유지·Bias/Reference 개선과 새로운 Target A/B 및 K 채택의 효과를 분리한다. 실패 원인이 분리되지 않으면 원인 미확정으로 기록한다.
