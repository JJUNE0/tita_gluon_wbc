# Original pose + wheel-latch checkpoint selection

Execution Domain: VALIDATION_SIM

Evidence Status: SUSPICIOUS — finite execution PASS, incomplete pose/transition performance.

Policy Checkpoint SHA256 (quiet recommendation 55k): 0ac0de4be2536c290fcb431304beef40342628b6ff7706a1c87425eebaf2fe09

ONNX SHA256: 6d710408945933cbb15917f7861d763a5023718c113dc64026446e1bb1f75ad2

Finding: 50k is genuinely quiet at nominal zero command and after straight driving. Prefer 55k for quiet nominal standing/stopping, or 80k for wider velocity tracking. 85k tracks roll transitions better but stops slowly. No checkpoint is a complete pose/velocity/stop solution.

All 20 checkpoints were verified/exported and screened at nominal zero command for 20 s, then tested on the same 16 supported scenarios: nominal stop, 5 velocity goals, 3 moving-to-stopped cases, and 7 pose goals. Six finalists received three independent 60-s holds with joint/body jitter measurements. Three finalists received 11 extended-velocity cases. Five received continuous yaw-stop, height/roll/pitch cycles and combined pose/driving transitions.

All use production IDLE/transform/RL startup, saved mappings/PD/ramps, sphere-wheel corrected flat model, friction 0.8 and 50 Hz control. Independent cases warm up for 6 s. No residual control or policy changes. This is deterministic fixed-simulation comparison, not randomized robustness or hardware acceptance.

Pass thresholds: stationary XY speed <0.01 m/s; pose <0.02 m/s, yaw rate <0.05 rad/s, roll/pitch MAE <3 deg, height MAE <3 cm, no fall. Driving vx/yaw MAE <0.10, lateral MAE <0.08, pose angle MAE <7 deg and height MAE <5 cm. Short stopping requires <=4 s to a 0.5-s quiet interval. Long holds require <5 cm excursion after t=5 s and <10 cm rollback. Unsupported heights outside 0.27–0.42 m are excluded, not clamped.

## Finalists

| Step | Stationary | Velocity | Stop | Pose | Quiet pitch std, deg | Worst straight-stop rollback |
|---|---:|---:|---:|---:|---:|---:|
| 35k | 1/1 | 5/5 | 3/3 | 3/7 | 0.1669 | 1.76 cm |
| 50k | 1/1 | 5/5 | 2/3 | 2/7 | 0.0165 | 2.26 cm |
| 55k | 1/1 | 5/5 | 3/3 | 2/7 | 0.0017 | 2.81 cm |
| 80k | 1/1 | 5/5 | 3/3 | 2/7 | 0.0093 | 1.92 cm |
| 85k | 1/1 | 5/5 | 1/3 | 4/7 | 0.0170 | 2.49 cm |
| 90k | 1/1 | 5/5 | 3/3 | 1/7 | 0.0114 | 3.24 cm |

55k: nominal, forward-stop and backward-stop 60-s holds all pass; pitch std at nominal is about 0.0017 deg. Initial straight-stop settle times are 3.50/1.14 s and yaw-stop 0.14 s. Extended velocity suite 9/11: +1.5 m/s undershoots to about 1.381 m/s; +3 rad/s yaw produces about -0.109 m/s uncommanded vx.

80k: same short stationary/velocity/stop categories pass, all three 60-s straight/nominal holds pass, extended velocity 11/11 passes including vx +/-1.5 m/s and yaw +/-3 rad/s. Stop settle times forward/back/yaw are 1.18/1.02/0.36 s. Final-30-s drift after backward stopping is about 1 cm, versus below 1 mm for 55k.

50k: after yaw stopping, final-30-s mean XY speed remains about 0.023 m/s with 0.68 m XY excursion. Roll-to-zero and combined-pose-to-zero transitions also retain drift in tested scenarios. Nominal quiet standing alone does not establish these transitions.

35k passes the most short scenarios (12/16) but has more nominal joint motion/pitch variation than 50/55/80k and drifts during positive-roll goal. 85k passes 4/7 isolated pose cases and the continuous roll cycle; forward/yaw stop settle times are about 10.9/7.88 s, too slow for the 4-s threshold.

Shared limits: every checkpoint misses at least one pose/transition criterion. Both 55k and 80k have roughly 3–4 cm height error at 0.30/0.40 m targets. Roll goals can induce drift. None passes the entire combined pose+drive+stop+return scenario. Full-range pose extremes +/-30/+/-15 deg were not evaluated.

## Recommended commands

```bash
python3 sim2sim/sim2sim_ros2_jazzy/launch/sim2sim.launch.py \
  --ckpt mj_lab/logs/flash_sac/tita_mjlab_112630_629104/model_55000 \
  --pose 0 0 0.335
```

For broader velocity tracking, replace model_55000 with model_80000.

Artifacts: [comparison graph](pose_latch_checkpoint_selection/selection_comparison.png), [all aggregate metrics/hashes](pose_latch_checkpoint_selection/selection_summary.json). Full raw traces and execution/export logs remain in the same directory.

Changed files: added test/evaluate_pose_latch_transitions.py and test/report_pose_latch_selection.py plus experiment evidence. Existing training/controller/policy source was not edited. New-file diffs, source audit, compilation and ./scripts/agent-check.sh logs are beside this report. Finite execution checks are separate from the policy-quality failures above.

Branch: agent/codex/tita-walk. No new training, publication or hardware commands.

## All checkpoints

| Step | Passing / 16 | Stationary | Velocity | Stop | Pose |
|---|---:|---:|---:|---:|---:|
| 5k | 0/16 | 0 | 0 | 0 | 0 |
| 10k | 0/16 | 0 | 0 | 0 | 0 |
| 15k | 1/16 | 0 | 1 | 0 | 0 |
| 20k | 0/16 | 0 | 0 | 0 | 0 |
| 25k | 0/16 | 0 | 0 | 0 | 0 |
| 30k | 6/16 | 0 | 5 | 0 | 1 |
| 35k | 12/16 | 1 | 5 | 3 | 3 |
| 40k | 5/16 | 0 | 4 | 0 | 1 |
| 45k | 6/16 | 0 | 5 | 0 | 1 |
| 50k | 10/16 | 1 | 5 | 2 | 2 |
| 55k | 11/16 | 1 | 5 | 3 | 2 |
| 60k | 7/16 | 0 | 5 | 1 | 1 |
| 65k | 10/16 | 1 | 5 | 2 | 2 |
| 70k | 7/16 | 0 | 5 | 0 | 2 |
| 75k | 6/16 | 0 | 5 | 0 | 1 |
| 80k | 11/16 | 1 | 5 | 3 | 2 |
| 85k | 11/16 | 1 | 5 | 1 | 4 |
| 90k | 10/16 | 1 | 5 | 3 | 1 |
| 95k | 6/16 | 1 | 3 | 0 | 2 |
| 100k | 6/16 | 0 | 5 | 0 | 1 |
