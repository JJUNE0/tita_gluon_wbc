# Online Local M4 — A/B 및 조건부C 사전 계획

작성일: 2026-10-16 (Asia/Seoul)

Execution Domain: **DESKTOP_DRY_RUN** (B/C 수집: **VALIDATION_SIM**)

Policy Checkpoint SHA256: `6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05`

Evidence Status: **NOT_TESTED — 사전 계획**. 결과에 맞춰 임계값·상태·Q/R·입력 예산을 바꾸지 않는다.

Observed Metrics / Behavior / Log Summary:

상세 조건·선택 순서·source·이전 보호 hash는 [plan.json](run_01/plan.json)에 동결한다. A는 신규MuJoCo 없이 기존 데이터만 사용한다. B와 조건부C는 서로 다른 시작조건에서 Target을 startup 이전에 고정한다. Production·기존 실험·정책·RLS 구현을 덮어쓰지 않는다.

## A — 동일 데이터·목적함수 비교

Nominal10/30/60/1000초의Full78응답+고유baseline6개, 이전friction0.2의post10–60초 학습stream을 사용한다. A1은plain scaled LS, A2는기존RLS와같은forgetting0.9995/P0=100/nominal mean의 augmented weighted batch해, A3는기존covariance recursive RLS다. A4는forgetting1의P0=100/1e8,weak prior의nominal/zero mean을 비교한다. 모든모델을 먼저 저장하고 같은 기존 held-out 예측 자료에 적용한다.

A2/A3 계수 상대차≤1e−7은 수치 일치 기준이며 prediction PASS와 별개다. A4도 같은 비용의batch해와 대조한다. A의test 결과로 B설정을 선택하지 않고 아래B설정을 모두 사전 고정한다. 기존 held-out 자료 재사용이므로 새로운 독립 물리 검증으로 합산하지 않는다.

## B — 단일 연속 rollout

- Nominal/friction0.2 ×probe0.01/0.02Nm. 개발seed900/901/902와pitch−0.035/0/+0.035의3시작조건, held-out seed910/911×3pitch의6시작조건이다. 개발12개·검증24개 episode,각64초다.
- 모든실행은 첫RL부터 원래Fixed M4와bias/reference를 고정한다. 원래sensor M4·raw history·wheel/leg PD를 유지하며 p_hold를 첫RL에서 한 번만 정한다. FK 보정을 적용하지 않는다.
- 누적original RLS(0.9995,P100),누적lambda1(P100/P1e8),최근10/20초lambda1(P1e8)를 같은 실제데이터에 shadow로 매20ms 갱신한다. 윈도우는 표본 개수가 아닌 실제경과시간 기준이다.
- 최근창은 covariance update/downdate로 갱신한다. 후보에는 **같은 목적함수의** SVD해를 수치 보정으로 사용한다. 이는 사전 알고리즘이며 raw재귀모델·차이·covariance rebuild사유를 함께 남긴다. 모델을 안정행렬로 투영하거나 예측 실패를 사후 튜닝하지 않는다.
- 10/30/60초에 후보를 동결하고 다음4초를 새로운sensor/command 검증으로 쓴다. 이 구간은 나중 학습에서도 영구 제외한다. 검증 중snapshot·Direct B·GT가 estimator로 들어가지 않는다. 시계는창/검증 일정만 정하며회귀feature가 아니다.
- Probe는sensor roll/pitch·속도·leg 범위와Fixed raw입력의interior 여유를 만족할 때만 허용한다. 포화 중 강행하지 않는다. 추정은 알려진 실제software residual을 사용하며 residual band clipping 표본은 유지한다. Native command clipping·비정상sensor/자세 표본은 제외한다. GT로 학습eligibility를 만들지 않는다. 물리guard는 별도sim 안전중단/평가다.
- 합residual0.4328–0.5328Nm, slew2Nm/s, wheel±12Nm를 공유한다. 첫bias 활성화에는기존1.5초ramp와0에서의slew 전환을 유지한다.

정보gate: 원래관측feature rank25,condition≤1e6,input innovation≥1%,positiveP,사용표본≥250. Prior의가상행은 정보량에 포함하지 않는다. 예측gate는후속rolling0.1/0.5/1/2초 absolute p/v RMSE≤20µm/20µm/s 및NRMSE≤30%,최초2초20/20·최초4초50/20기준이다. 분모는후속실제상태변화RMS와기존floor다. 후속구간의조건부B 회귀 rank/condition·부호·오차≤30%도 요구한다. 이는 matched Direct B와 다른 검사다. 부족한rank나정보를threshold 변경으로 통과시키지 않는다.

## C — B 통과 조건에만 허용

개발3/3에서최소1개의검증후보가있는설정만후보가된다. 사전순서는local20→local10→cumulative weak→original→P100,각각0.01→0.02Nm다. 선택은개발자료로만한다. 이후독립검증6/6에서최소1개검증후보가있어야해당domain의C를허용한다. 한domain 실패는다른domain을막지않는다.

허용될경우새seed940/941×3pitch,180초에서Fixed/Bias+Reference/AdaptiveK/Full을비교한다. Q/R은기존값,후보시점10/30/60/90/120/150초+4초검증. 동일행렬snapshot 검증·정보·DARE·nominal/candidate rho·직전/누적25%·K jump0.003Nm·joint jump0.005Nm를모두요구한다. 검증중에는기존제어파라미터를유지한다. Bias는기존5초sensor위치적분B1(max0.0005Nm/s),reference는기존20초저속평균/comfort한도를사용하고p/v목표는고정한다. Bias/Reference의quiet조건과RLS정보량은구분한다. 모든군이같은제안probe와입력예산을쓰며 실제probe에너지·초기drift도전체비용으로센다.

실제새K채택수와식별·제어성공을별도로보고한다. Full은Fixed/E6각각에대해전체IAE중앙값10%이상·paired4/6이상개선,후반RMSE≤120%,완료6/6을요구한다. 절대hold의기존기준도별도기록한다. C prerequisite가실패하면제어source를만들거나gain을강행하지않고NOT_TESTED로남긴다. 통과하는경우에만위계획의실험용Csource를작성·동결한후수집한다. 실기·ROS배포·학습·Q/R탐색없음.
