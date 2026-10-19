# Velocity bias 실기 피치 문제와 시뮬레이션 기록 재검토

Execution Domain: DESKTOP_DRY_RUN (기존 VALIDATION_SIM 기록 및 완료된 실기 분석 보고서의 오프라인 검토)

Evidence Status: PASS — 저장된 8개 시뮬레이션 기록의 평균 피치/보정 재집계와 입력 무결성 확인. 개선 제어기 성능은 NOT_TESTED. 실기 진동의 정확한 동역학 원인은 SUSPICIOUS이며 본 분석으로 식별하지 않았다.

Policy Checkpoint SHA256: `6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05`

ONNX SHA256: `f44f07ed44970e3ff565eae67fd9229adf0be5c02215591c52a691ffcbb71b2a`

Branch: `agent/codex/dev_tita_gluon`

## 기존 시뮬레이션에서도 평형 이동은 있었다

영상에 사용한 현재 2초 대기/300초 실험의 마지막 20초(280~300초)를 같은 창으로 비교했다. baseline은 동일 환경·초기 상태에서 별도로 실행한 무보정 궤적이다. 피치는 state 열 5의 rad 값을 deg로 변환했다. 휠당 추가 토크 크기는 해당 config의 Kd=0.5와 wheel radius=0.0925 m로 `mean(abs(bias))*Kd/radius`를 계산한 **effort clip 전 PD 증가분**이며 실제 모터 토크 측정이 아니다.

| 조건 | Baseline 평균 피치 | Bias 평균 피치 | 피치 변화 | Bias 구간 피치 변동 RMS* | 평균 휠당 추가 토크 크기 |
|---|---:|---:|---:|---:|---:|
| Nominal | 3.633° | 3.176° | −0.458° | 0.00648° | 0.285 Nm |
| Low friction μ=0.2 | 3.507° | 3.132° | −0.374° | 0.00002° | 0.229 Nm |
| CoM +5 mm / mass×1.15 | 3.227° | 5.194° | +1.967° | 0.00942° | 1.038 Nm |
| CoM −5 mm / mass×1.15 | 2.311° | 5.521° | +3.211° | 0.00723° | 1.600 Nm |

*평균을 제거한 전체 변동 RMS이며 실기 보고서의 6~10 Hz 대역 RMS와 동일한 지표는 아니다.

따라서 이 네 조건의 마지막 20초에는 실기의 12~14° 평균 피치와 큰 진동이 나타나지 않았다. 그러나 질량/CoM 변경 조건에서는 정지하면서 평균 피치가 약 2~3° 이동했다. 같은 방향의 평형 이동 가능성은 시뮬레이션에도 있었고 규모가 달랐다. 명목 시뮬레이션의 추가 토크는 약 0.285 Nm로 실기 settled 구간의 5.26/6.44 Nm보다 훨씬 작다.

실기 [기존 분석](flashsac_bias_oscillation_review.md)의 보정 전 2.36° 창은 RL+0.5~2.0초 초기 과도 구간이다. 위 시뮬레이션 정상 상태 baseline과 동일한 측정 창/실험 설계로 취급하지 않는다. 같은 실기에서 보정이 두 번 켜질 때 평균 피치 이동이 반복된 점은 강한 관측 증거지만 지연·모터 이득·정책 동작 중 정확한 원인을 분리하는 식별 실험은 아니다.

[이전 overnight 캠페인](velocity_bias_overnight_summary.md)은 1.2초 대기 설정의 결과다. 명목 40개 정책의 300초 평가 등은 통과했지만 물리 확장에는 여섯 조건의 잔여 속도 진동, 저마찰 미끄럼/관측 실패, baseline 기립 실패도 있었다. 이 결과를 현재 2초 설정 전체에 대한 보편적인 무진동 보장으로 바꾸어 해석하지 않는다. 영상의 여덟 궤적 완료 역시 drift 감소의 증거이며 자세 보존/실기 안정성 보장은 아니다.

## 개선 방향 — 아직 적용하거나 검증하지 않은 제안

현재 law는 속도 오차를 적분하고, 큰 피치 변화가 생겨도 속도가 0이면 적분값을 유지한다. `abs(pitch)<=0.3 rad` 조건은 약 17.2°까지 허용하므로 관측된 14.56°를 배제하지 못한다. 큰 추가 토크와 정책 토크가 상쇄되어 최종 토크가 작아져도, 최종 ±12 Nm clip만으로 두 큰 내부 항을 제한할 수는 없다.

1. **과도응답 완화:** seed를 제거하거나 충분히 작게 제한하고, Ki·slew를 줄이며 ramp를 늘린 후보를 비교한다. seed=3이 그대로면 Ki만 낮춰도 최초 큰 보정은 남는다. 반대로 seed=0/작은 Ki만으로 정상 상태 피치가 원래대로 돌아온다고 보장하지 않는다.
2. **자세를 제한하는 적응:** 보정 전 안정 구간에서 고정한 pitch reference와의 편차 및 pitch rate/변동을 함께 감시한다. 허용 범위 안에서만 적분하고, 벗어나면 누적을 멈추는 것에 더해 기존 bias도 검증된 작은 값 방향으로 완만하게 되돌린다. 현재 큰 bias를 그대로 고정하면 이동된 평형도 남는다. 범위를 벗어난 피치를 계속 새 reference로 갱신해 오류를 숨기지 않는다.
3. **보정 성분 자체의 제한과 anti-windup:** m/s bias를 휠당 PD 토크로 환산해서 크기/변화율을 제한하고, 실제 적용된 보정값을 적분 상태에 반영한다. 자세를 유지할 수 없는 보정 요구에서는 완전한 정지 대신 drift가 남는 결과도 허용해야 한다. 실기 숫자를 그대로 정하기보다 시뮬레이션 후보 비교가 먼저다.
4. **실기 실패를 재현하는 검증:** baseline/현재 law/완만한 law/자세 제약 law를 동일 조건에서 비교한다. 위치 IAE와 속도 외에 상대 피치 평균·최대 편차, gyro RMS, wheel torque RMS, baseline/추가 토크의 DC 상쇄 크기, 이동 명령 후 정지 재진입을 평가한다. 실제 기록에 맞춘 초기 역방향 drift·평형·액추에이터 응답과 센서/제어 지연을 검토하고 모델 mismatch 범위에서 확인한다. 원인이 규명되지 않은 8 Hz에 노치만 추가하는 것을 첫 해결책으로 삼지 않는다.

장기적으로는 속도와 pitch를 함께 고려하는 상위 제어/정책 적응이 필요할 수 있다. 기존 nominal M4 K를 바로 더하는 것은 이미 [일관된 개선을 보이지 않은 조합](velocity_bias_m4_comparison.md)이므로 현재 실기 문제의 검증된 해결책으로 취급하지 않는다. 이 검토에서는 controller 변경, 하드웨어 접근/실행/배포를 하지 않았다.

## 파일과 실제 검사

- 신규 분석 스크립트: `test/analyze_velocity_bias_sim_posture.py`.
- 신규 보고서: 이 파일. [직접 실행 로그](velocity_bias_sim_real_posture_review/analysis.log), [8개 결과와 source hash](velocity_bias_sim_real_posture_review/metrics.json).
- PASS: 8개 상태 배열의 shape/유한값/300초 완료, checkpoint 일치, config wheel Kd 확인, NPZ/config 분석 전후 hash 보존. 기존 결과를 읽기만 했으며 시뮬레이션·정책을 새로 실행하지 않았다.
- 필수 저장소 `./scripts/agent-check.sh`의 전체/개별 결과는 [agent_check.log](velocity_bias_sim_real_posture_review/agent_check.log)에 기록한다.
- 변경 범위는 분석 스크립트·이 보고서·해당 artifact 폴더다. 기존 제어 코드·설정·정책 및 관련 없는 변경은 유지했다. 커밋/push/배포 없음. 개선안의 폐루프 효과는 NOT_TESTED.
