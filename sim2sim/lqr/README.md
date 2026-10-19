# FlashSAC / wheel LQR ablations

Execution Domain: `VALIDATION_SIM`. This package runs headless MuJoCo only.

Modes: A (FlashSAC all joints), B (FlashSAC wheels + fixed leg PD), C-3/C-4
(fixed LQR), D-3/D-4 (structured residual RLS + guarded adaptive LQR).
The designated checkpoint is `model_100000`; no actor training occurs.
The reference launch, observation builder, action adapter and physics stepper
are reused without editing their files.

Use `/home/cocel/venvs/cosim_ros2_jazzy/bin/python` for evaluation. First run
the existing launch and `test/test_lqr_baseline_gate.py` as documented in the
experiment report. Then, from the repository root:

```bash
/home/cocel/venvs/cosim_ros2_jazzy/bin/python -m sim2sim.lqr.evaluate --stage shadow --nominal-only --output docs/exp/2026-10-14/new_lqr/shadow
/home/cocel/venvs/cosim_ros2_jazzy/bin/python -m sim2sim.lqr.evaluate --stage full --shadow-evidence docs/exp/2026-10-14/new_lqr/shadow/results.jsonl --output docs/exp/2026-10-14/new_lqr/full
MPLCONFIGDIR=/tmp/lqr_mpl /home/cocel/venvs/cosim_ros2_jazzy/bin/python -m sim2sim.lqr.report --results docs/exp/2026-10-14/new_lqr/full --shadow-evidence docs/exp/2026-10-14/new_lqr/shadow/results.jsonl --report docs/exp/2026-10-14/new_lqr_summary.md
```

Outputs must be new, empty directories under `docs/exp/YYYY-MM-DD/`.
For execution from this directory, set `PYTHONPATH=../..` and pass repository
paths with `../../` (for example `--output ../../docs/exp/2026-10-14/new_run`).
`--stage fixed --nominal-only --quick` runs a four-mode development smoke test.
Full adaptive evaluation requires measured shadow evidence with sufficient
excitation, improved prediction error and a validated candidate for both dimensions.

Configuration holds fixed Q/R, common B/C/D leg targets/gains, residual bounds,
gain guards, disturbances, paired seeds and independent mismatch strengths.
All coefficients start at zero. Every D trial has a probing adaptation episode,
a new episode with frozen gain, and a separate episode with continuing updates.
No probing is used in the latter two episodes. Trials terminate on failure;
reports show failure rates separately from completed-episode metrics.

The stationary WIP model excludes roll/yaw and motor internal states. Encoder
odometry assumes rolling contact. An accepted gain is stable on checked models,
which does not guarantee MuJoCo stability. Locomotion switching (Phase 7) and
hardware deployment are outside this ablation implementation.
