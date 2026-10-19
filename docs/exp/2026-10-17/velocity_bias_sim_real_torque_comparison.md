# Velocity bias 시뮬·실기 추가 토크 비교

Execution Domain: DESKTOP_DRY_RUN — 기존 VALIDATION_SIM trace 및 실기 분석 보고서 재조회. 새로운 시뮬 또는 로봇 실행 없음.

Policy Checkpoint SHA256: `6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05`

Evidence Status: PASS — 저장된 trace의 bias를 설정상 PD 추가 토크로 환산. SUSPICIOUS — 시뮬·실기 차이의 물리적 원인. 실측 모터 토크·필요 최소 보정량은 NOT_TESTED.

Branch: `agent/codex/dev_tita_gluon`

## 비교 기준과 결과

주 체크포인트의 기존 300초 `rate3_primary01` 및 `rate3_primary_physics01` trace를 읽었다. `input[:,0]`은 velocity bias(m/s), `state[:,5]`는 pitch(rad)다. 설정의 wheel Kd=0.5, radius=0.0925 m와 harness의 `targets += signs*bias/radius` 경로를 확인했다. 추가 토크 환산은 `Kd*bias/radius`이며 좌우 모터 부호를 공통 전진 좌표로 맞춘 휠당 값이다. 최종 effort clipping 전 계산 항이며 실측 토크가 아니다. 정상상태 평균은 마지막 1,000개 입력(20초), 피치는 마지막 1,000개 상태의 평균이다. Peak는 전체 300초의 절댓값 최대다.

| 조건 | 추가 토크 정상상태 평균 / wheel | 추가 토크 peak 절댓값 / wheel | 정상상태 평균 pitch |
|---|---:|---:|---:|
| Nominal | +0.2846 Nm | 0.3669 Nm | 3.174° |
| 마찰 0.2 | +0.2289 Nm | 0.4512 Nm | 3.132° |
| CoM 앞 5 mm | +0.5286 Nm | 0.8406 Nm | 3.019° |
| CoM 뒤 5 mm | +0.0955 Nm | 0.1422 Nm | 3.322° |
| 질량 +15% | −1.3633 Nm | 1.9906 Nm | 5.364° |
| 질량 +30% | −2.0881 Nm | 3.5103 Nm | 7.803° |

CoM 조건은 질량 증가와 결합하지 않은 독립 조건이다. 이 표는 기존 seed/큰 한도 law의 대표 7조건 중 6조건이며 전체 체크포인트의 통계가 아니다. 0.8 Nm 실기 제한 law나 뒤의 grid 영상과 동일 설정이라고 간주하지 않는다. 마찰 0.8 정상상태는 +0.2848 Nm였다.

실기의 첫 큰 bias 기록은 [기존 분석](flashsac_bias_oscillation_review.md)에 근거한다. 첫 안정 구간 추가 항 −5.26 Nm/wheel, pitch 12.08°; 두 번째 −6.44 Nm/wheel, pitch 13.73°였다. 같은 상태에서 정책·PD 항은 각각 +5.27/+6.55 Nm였으므로 이 큰 값은 합산 전 bias 항이다. 실제 필요한 최소 제동 토크가 5–6 Nm라고 단정할 수 없다. 실기에서는 외부 속도 GT 및 적용 Nm calibration을 검증하지 않았다.

기본 시뮬의 정상상태 보정에 비해 실기 큰 bias 항의 절댓값은 약 18.5–22.6배다. 질량 +15%/+30% 시뮬에서도 pitch가 커지는 경향이 관측되어, 보정 후 자세 평형 변화가 실기에만 나타났다고 주장하지 않는다. 질량·마찰·CoM 외의 실제 동역학 차이는 이번 계산으로 식별하지 않았다.

±10.81 Nm는 기존 bias amplitude ±2 m/s를 PD로 환산한 허용 한도다. 위 대표 실행에서 실제 사용한 보정량을 나타내는 값은 아니다.

## 검증·변경 범위

기존 NPZ를 NumPy로 읽어 7조건을 환산하고 checkpoint hash와 input column metadata를 확인했다. PASS. 코드·설정 변경이나 배포 없음. 이 보고서와 agent-check 출력만 신규 기록한다. 전체 agent-check 결과는 동명 `.log`에 보관한다.
