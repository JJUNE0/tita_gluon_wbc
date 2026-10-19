# X drift 4장 + Yaw drift 4장 — 동작 비교 중심 면접 PT

- Execution Domain: **DESKTOP_DRY_RUN**. 기존 문서·NPZ·STL/URDF 읽기, HTML 작성, 로컬 Chrome 검증만 수행.
- Evidence Status: **PASS** — 최종 뷰어 검사 결과는 아래 QA/agent-check 로그 참조. 새 학습·물리 rollout·로봇 시험은 **NOT_TESTED**.
- Policy Checkpoint SHA256 / ONNX Hash:
  - X: FlashSAC 60k checkpoint `6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05`, ONNX `f44f07ed44970e3ff565eae67fd9229adf0be5c02215591c52a691ffcbb71b2a`.
  - Yaw 최종: headw0 65k checkpoint `ff083cbfc8a8571009a27454e75dc88463e9ebc796fa79e8782ccb4a5bea239d`, ONNX `ede50fde5cc1863758d2c50e70f7902cafb31e2a677c985e0d69b80c2560be0b`.
- Current branch: `agent/codex/real2sim-interview-pt`.
- Publication: 없음. commit/push/PR/사이트 게시/하드웨어 배포·명령 실행 없음.

## 열기

- **[단일 HTML](real2sim2real_pt/standalone.html)**: 파일 하나를 브라우저에서 직접 연다. 외부 리소스·서버·설치가 필요 없다.
- **[PDF](real2sim2real_pt/real2sim2real_pt.pdf)**: 최종 8페이지, 약 16:9, 정지 이미지 기반 보조 자료.
- [편집용 HTML](real2sim2real_pt/index.html): 같은 폴더 CSS/JS 사용.
- `←`/`→` 이동, `N` 발표 노트, `E` 실험 근거, `G` 목차, `P` 동작 정지, `F` 전체화면.
- 로봇 드래그: 회전, 휠: 확대, 더블클릭/포커스 후 `R`: 카메라 초기화.
- 3·4장: 30초 확대/5분 전체, 공통 시간 슬라이더. 4장은 바닥/질량/CoM 조건 선택.
- 6장: 원통/구 접촉 동시 재생, 시간 슬라이더, collision 표시, 접촉부 확대.
- 원본 Markdown 링크는 저장소 상대 경로다. HTML만 외부로 옮겨도 재생·발표 노트·근거 요약·해시는 내장되지만 원본 문서는 저장소가 있어야 열린다.

## 구성 — 각 주제 4장

| 장 | 역할 | 핵심 시각 자료 |
|---|---|---|
| X 1/4 | 문제 | 0 명령에서 앞으로 흐르는 실제 sim XY 경로와 로봇, 기립 기준 자세 ghost |
| X 2/4 | 수정 원리 | IMU·엔코더 → 속도 추정 → 적분 → 휠 목표 offset, 실제 추정 속도·bias 값 |
| X 3/4 | 전후 비교 | 동일 정책/초기 상태/물리의 무보정·velocity bias 로그, 같은 시간·카메라·미터 축척 |
| X 4/4 | 회귀 검증 | 기본·저마찰·CoM 전/후+mass15 조건 선택, sim 성공과 실기 잔류 후진 구분 |
| Yaw 1/4 | 문제 | nominal 원통 sim과 실제 로봇의 정지 중 방향 변화 |
| Yaw 2/4 | 원인 재현 | 원통/구 collision 비교, 선/점접촉 강조, 24초 방향 변화 4.08° 대 53.82° |
| Yaw 3/4 | 학습 수정 | 바이어스 보정 gyro → heading error 관측 → 정지 heading 보상 → 재학습·선별 |
| Yaw 4/4 | 실기 확인 | 개선 전/후 실기 관절·방향 로그, 같은 약 16초에서 약 +83.4° 대 −0.1° |

별도 표지/결론, MA2 진동·무릎 처짐·G6 개별 장면을 주 발표에서 덜어냈다. 관련 근거는 필요한 노트/원본 링크로 남겼다. 사용자가 선호한 “동작 차이가 설명 없이 보이는” 전후 재생 방식을 두 주제에 공통 적용했다.

## 결과와 해석 범위

### X drift — sim에서 억제, 실기는 미해결

출처: [velocity_bias_grid_video.md](../2026-10-17/velocity_bias_grid_video.md). 동일 60k 정책, zero command, seed913, 각 300초. 각 조건 안에서 초기 qpos/qvel/previous action·물리가 같다. 원점은 RL 진입이므로 첫 2초 기립/보정 대기 이동을 포함한다.

| 조건 | 무보정 최대 XY 이탈 | Velocity bias 최대 XY 이탈 |
|---|---:|---:|
| Nominal | 5.2877 m | 0.0310 m |
| 마찰 μ0.2 | 1.4603 m | 0.0286 m |
| CoM +5mm, mass/inertia ×1.15 | 22.1111 m | 0.1260 m |
| CoM −5mm, mass/inertia ×1.15 | 29.1922 m | 0.2154 m |

- **최대 XY 이탈**을 x 한 축 최대값이나 누적 주행거리로 부르지 않는다. 화면 현재 숫자는 **ΔX**이고, 결과 요약은 **최대 XY**다.
- 제어는 IMU·엔코더·상대 FK 기반 속도 추정을 쓴다. GT 위치/속도는 평가·화면에만 쓴다.
- 화면은 NPZ의 실제 qpos·GT XY·rpy·속도 추정·bias를 재생한다. 이동 크기를 확대/축소하지 않는다. 긴 이동에서는 양쪽 동일 카메라로 전체 경로를 보여주고 현재 자세 확대 inset을 붙인다.
- 출발점은 RL 진입 위치. X ghost는 **기립 2초 시점의 실제 자세·위치**다. 첫 프레임의 접힌 자세와 혼동하지 않도록 표시했다.
- 원점 복귀 제어·heading 유지의 성공으로 확대하지 않는다. 이전 1.2초 준비 구간 제외 비교의 7.975mm와 다른 기준이다.
- 실기 0.8Nm bounded bias run은 상한에서도 음의 속도 추정이 남아 **FAIL**이었다. [실기 기록](../2026-10-17/flashsac_144909_bounded_bias_review.md). 이 한계를 4장에 표시했다.

### Yaw drift — 접촉 모델 진단 후 실기 heading 개선

- 동일 50k·무릎 L0.60/R0.75의 원통/구 sim stand 8–31.98초를 함께 재생. 끝 방향 변화 +4.0818° / +53.8172°. 별도 초기화 run이다.
- 구는 실물 타이어 형상 식별 결과가 아닌 낮은 비틀림 저항의 근사다. 시각 메시·관성·반경은 유지하고 collision만 바꿨다. 선/점은 이상적 접촉 표현이다.
- 실기 비교는 기존 q와 정지 z-bias 보정 gyro의 Euler yaw-rate 적분을 재생한다. 실기 world 위치는 **고정**하며 위치 궤적 복원을 주장하지 않는다.
- 개선 전/후 약 16초의 선택 구간 변화와, 최종 65k 정지 4구간·114초의 시간 가중 |구간평균| ≈0.01°/s는 별도 지표다.
- 최종 정지 heading **PASS**, 정지 위치 유지 **FAIL**. 0.2–0.3m 후퇴·왕복과 회전 중 후진 원호는 남아 있다.
- 두 실기 run의 초기 상태·명령 이력과 학습 구성은 달라 단일 변경의 인과 A/B로 해석하지 않는다.

## 데이터·변경 파일

- `real2sim2real_pt/index.html`, `presentation.css`, `presentation.js`: 최종 8장, 3D renderer, 전후 재생/조건 선택/노트/근거.
- `model-data.js`: 저장소 TITA URDF와 STL 9개를 경량화한 geometry. 1.2mm vertex clustering.
- `evidence-data.js`: 기존 NPZ 재생 데이터 14개(현재 장면용 X 8개와 yaw 비교 자료 등), source SHA256·시간·정의·정책 hash. 새 physics 실행 없음.
- `standalone.html`, `real2sim2real_pt.pdf`: 최종 전달 파일.
- `test/build_real2sim_pt_model.py`: geometry 변환, 기존 NPZ에서 재생 자료 추출.
- `test/package_real2sim_pt.py`: CSS/JS/모델/대체 이미지를 단일 HTML에 내장.
- `test/validate_real2sim_pt.py`: 로컬 Chrome CDP UI/반응형/시간·위치·각도/조건 선택/PDF 검사.
- QA JSON·스크린샷·agent-check 로그 및 `source-and-output-manifest.json`은 같은 PT 폴더에 보관. 기존 버전의 일부 QA 이미지는 작업 이력으로 남아 있으며 주 발표에는 포함되지 않는다.

기존·동시 작업의 `flashsac_headw0_65000_153755_review.md`, `test/screen_sphere_wheel_runs.py`, `test/render_real2sim_progression.py`, `real2sim_progression_video/` 등은 이 작업에서 수정하지 않았다. 원본 실험 NPZ, URDF/STL, 정책, 제품 제어 코드도 변경하지 않았다.

## 실행한 검증

- `python test/build_real2sim_pt_model.py`: geometry 9개·관절 8개 및 기존 replay 14개 추출 **PASS**.
- `node --check .../presentation.js`: **PASS**.
- `python test/validate_real2sim_pt.py`: 최종 [QA 결과](real2sim2real_pt/qa-results.json). 8장×4 viewport(1600×900 / 1366×768 / 390×844 / 820×1180), WebGL, 키보드/노트/근거/목차, 원본 링크, x/yaw 재생, 조건 선택, 30/300초 scrub, 카메라 동기화, overflow, JS 예외 검사.
- X 30초 좌표는 원본에 대응하여 ΔX +0.425853 / −0.0001714m. 300초 및 4개 물리 조건의 끝 좌표, 전후 초기-state hash, 화면의 시간·카메라 일치를 검사.
- 접촉 끝각도 4.0818/53.8172°, slider 0초 복귀, 실기 heading before/after 차이 검사.
- `python test/validate_real2sim_pt.py --standalone`: [단일 파일 QA](real2sim2real_pt/standalone-qa-results.json). 외부 resource 요청 0, WebGL 미지원 시 내장 정지 이미지, 8장 PDF 생성 검사.
- `pdfinfo`, `pdftoppm`: 페이지 수/16:9 용지/대표 비교 장면 확인.
- 필수 `./scripts/agent-check.sh`: [전체 로그](real2sim2real_pt/agent-check.log).
- 최종 task 소스 diff whitespace 검사와 source/output SHA256 manifest 기록. 관련 없는 변경을 수정·stage·revert하지 않음.

검사 도중 1366×768에서 피드백 도식의 세로 넘침을 발견해 글자·도식 간격을 줄여 수정했다. 실패 기록은 도구 실행 결과에 남기고 수정 후 검사 결과를 위 QA 파일에 기록한다.

## 재생성·남은 한계

```bash
python test/build_real2sim_pt_model.py
python test/package_real2sim_pt.py
```

브라우저 검증은 로컬 전용 headless Chrome CDP 포트 9327을 사용한다. 면접 현장의 브라우저/GPU/한글 글꼴·프로젝터는 **NOT_TESTED**. 뷰어 검증은 새 정책/실기 검증을 대신하지 않는다. X의 실기 미해결과 Yaw의 잔여 위치 오차는 발표 안에 표시했다.

## 검정·노랑 테마 변경

- 사용자 요청으로 검정 배경 `#000000`, 본문 노랑 `#ffe76a`, 강조 노랑 `#ffd600`으로 변경. 보정 전은 짙은 금색 `#c99b35`, 보정 후는 밝은 노랑으로 구분한다.
- CSS·인라인 SVG·3D 강조선/경로/접촉체·버튼/슬라이더/노트 색상을 함께 변경. HTML과 PDF 및 WebGL 대체 이미지에도 반영.
- 변경 파일: `index.html`, `presentation.css`, `presentation.js`, 생성된 `standalone.html`·PDF·대체 이미지·검증 자료 및 이 기록. 모델·재생 데이터 파일의 SHA256은 테마 변경 전후 동일하다.
- Execution Domain: **DESKTOP_DRY_RUN**. Policy Checkpoint SHA256/ONNX: 위와 동일, 신규 정책 없음.
- 브라우저 computed style에서 검정 배경·노랑 본문·노랑 강조색, 8장 구성을 확인 **PASS**. 대표 X/접촉 장면 육안 확인, JS 예외 0. [테마 검사](real2sim2real_pt/theme-qa.json).
- 단일 HTML·PDF 최종 검사는 [standalone-qa-results.json](real2sim2real_pt/standalone-qa-results.json), 필수 저장소 검사는 [agent-check.log](real2sim2real_pt/agent-check.log)에 기록.
- 원래 8장 구성·동작 재생·수치 해석 범위는 유지. 테마 변경으로 새 로봇 성능 검증을 수행한 것은 아니다.
