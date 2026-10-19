최종 통합 보고서: [velocity_bias_overnight_summary.md](/home/cocel/Desktop/Research/tita_gluon_wbc/docs/exp/2026-10-17/velocity_bias_overnight_summary.md)

아래는 진행 중 기록이며, 현재 CLI 기본 후보는 v04 velocity-seeded integral이다. 구현/시뮬레이션 검증 완료, 일부 확장 조건의 품질 기준 미달과 실기 미검증은 최종 보고서에 명시했다.

# Velocity bias campaign — in progress

Execution Domain: VALIDATION_SIM / DESKTOP_DRY_RUN

Policy Checkpoint SHA256 (reference model_60000): 6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05

Other checkpoint/ONNX hashes: `checkpoint_manifest.json`, `export_results.json` (40 models, two training runs).

Evidence Status: NOT_TESTED for complete robustness objective; the runs below have direct evidence.

Observed metrics / behavior / log summary:

- All 40 checkpoint exports passed native Torch/ONNX parity.
- Baseline 60 s survey completed all 40. Physical terminal drift speed ranged from -0.26237 to +0.37369 m/s.
- Frozen prototype v01 passed physical speed and radial position gates on all 40 nominal checkpoints.
- Final provisional runtime v02 (`kp=2, ki=10, tau=0.1 s`, m/s bias bound=2, slew=2 m/s², ramp=.25 s) passed 60 s physical speed and position gates on all 40 nominal checkpoints. Worst max drift=.213994 m; worst last-20-s mean speed magnitude=.000284109 m/s; worst tail RMS=.0164082 m/s. It starts after 1.2 s zero-command acquisition and gates gross tilt (>0.3 rad) / apparent wheel speed (>1 m/s).
- `--velocity_bias` is a separate mutually exclusive Sim2Sim mode, before native wheel velocity PD/effort clipping. It does not combine an unvalidated M4 K with a new operating equilibrium. Fixed M4 remains the frozen comparison.
- Production math + sensor/torque/ROS integration: 7/7 tests PASS (`runtime_v02_tests.log`). Root translation and root linear velocity do not enter the controller estimate. Independent FK sensor discrepancy was at most 3.49e-11 m/s in the focused check.
- Fixed M4 and disabled baseline regression: 4/4 tests PASS (`fixed_m4_regression.log`); frozen M4 residual parity max error=2.09e-9 Nm.
- Actual launch CLI: 1000 headless steps PASS (`cli_smoke.log`). Finite playback is not the performance gate.
- `./scripts/agent-check.sh`: FAIL due to six pre-existing whitespace lines in lab/ddt_lab/ddt_lab/tasks/manager_based/locomotion/robots/tita/my_flat_env_cfg.py. Python syntax 472/472 and URDF 8/8 passed. See `agent_check_after_runtime.log`; unrelated source left unchanged.
- Severe low-friction cases can have ~8 m/s apparent wheel rolling speed while the chassis is nearly stationary. Such cases are not valid drift estimates; v02 inhibits adaptation. Some baseline policies already fall during common acquisition. Keep these failures visible.
- Some changed-mass cases meet position/mean-speed goals but fail the 0.02 m/s RMS gate. Analytic FK and fast damping are being tested as research variants, not promoted to runtime.
- Passive latest real bag replay completed without robot commands or changes to the original bag (`real_shadow/v02_guarded/`). Proposed bias hits bounds on the observed baseline trace; this does not establish corrected hardware behavior. Hardware closed-loop response sign, sensor frames, slip, torque paths and safe limits remain unvalidated.
- Full held-out 40×7 physics pairs at 60 s (`physics02`, 560 trials), and paired 40-policy 300 s runs (`long01`, 80 trials) remain in progress. Partial audits are marked NOT_TESTED, not full PASS.
- Failed zero-warmup entry tests and one ignored mass_scale key are retained and explicitly excluded in `entry01_errata.md`.

Changed runtime files: velocity_bias.py (new), sim2sim_node.py, cli.py, launch/sim2sim.launch.py. Research/test files live under test/. Evidence, source snapshots, hashes and every trial summary live here. Reviewed source diff: `task_source_diff.patch`. The adapter, PD, fixed M4, original evaluator and physics modifier match their pre-task source hashes.

Branch: agent/codex/dev_tita_gluon. No commits, publication or hardware deployment.


Additional completed evidence (campaign still in progress): v02 passed all 40 physical speed/position gates at 300 s, and three selected nominal policies at 900 s. In 40×7 paired 60 s physics trials, 276/280 completed; all 276 completed controllers passed the radial-position and terminal mean-speed goals, 264 passed the additional RMS gate, 261 passed the full observation-quality gate. The four excluded acquisition failures occurred in their paired baselines too; no new falls. All 276 valid initial-state hashes matched their baselines. Primary model_60000 reversed drift direction under mass scaling. At 300 s, velocity PI max displacement was 7/35/64 mm for nominal/+15%/+30% mass, versus fixed M4 0.20/28.98/19.49 m. Primary figure: primary_three_way_300s.png. The comparison uses synchronized IMU observations for both controllers and a common 1.2 s zero-residual RL acquisition.

A second, simpler candidate uses one initial seed proportional to the measured velocity, then slower integral feedback (kp0, ki4, seed_gain3). It passed all 40 nominal 60 s cases at seed915 and matches recorded math traces exactly. Prototype-to-runtime checks and fresh 40×7 physics/300 s tests are under way. It has not replaced the default. Some off-nominal policies retain oscillations, so no universal stationary-pose or hardware claim is supported.

A duplicate-timestamp observation bug was found in the virtual impulse harness, not the production controller. Earlier impulse results are retained but flagged; see impulse_observer_errata.md and corrected seeded_kick02. A regression ensures a pure root-linear impulse changes GT while preserving the measured joint/gyro/FK speed at that instant. Current controller/math/integration tests: 11/11 PASS (seeded_guard_tests.log). All 40 actor interfaces were separately verified to exclude ground-truth base velocity.

The 2 m/s simulation bias bound can correspond to about 10.81 Nm per wheel before native effort clipping (kd0.5, radius.0925); this is a simulation bound, not a validated small residual for real hardware. Heading is not held by this fore-aft controller. Hardware response sign/units/limits remain operator validation work.
