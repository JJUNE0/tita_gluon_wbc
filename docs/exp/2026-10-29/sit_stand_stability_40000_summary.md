# Sit/stand model_40000 stability diagnosis

Execution Domain: VALIDATION_SIM / TRAINING_SIM (read-only training-log inspection) / DESKTOP_DRY_RUN

Evidence Status: PASS (finite diagnostic execution); SUSPICIOUS (observed standing stability and pose tracking).

Policy Checkpoint SHA256: 3bbb4cb43e3363936ed13473fd46e5b4a3ebe654e37e19e2dc5bae37225b7506

ONNX SHA256: 71db553d55d99d85e91865e12317d4bbf7f0ff76f82a648b014521dafe000984

## Execution and scope

Ran the actual production ROS/MuJoCo/ONNX controller in isolated local domain 90 using model_40000. Each independent trial starts from unchanged IDLE/transform/SIT startup, followed by targets 0.335 -> 0.07 -> 0.335 -> 0.50 -> 0.07 -> 0.335 m, all commanded roll/pitch and velocities zero. Every target has its nominal ramp duration plus 5 seconds holding time. Reported final statistics use the last 3 seconds per phase. Saved 0.04 m/s is compared with an in-memory 0.02 m/s ramp override; neither saved settings nor ongoing training were modified. Terrain friction is the existing tita.yaml value 0.2, nominal gains, no sampled DR.

## Observed instability

| 4 cm/s phase | Height final mean / std | Pitch std | Max total tilt | Planar displacement within phase |
| --- | --- | --- | --- | --- |
| initial_stand | 35.38 / 5.11 cm | 11.19 deg | 40.99 deg | 2.33 m |
| sit | 7.90 / 0.01 cm | 0.03 deg | 15.73 deg | 2.18 m |
| rise | 35.85 / 5.26 cm | 8.51 deg | 23.30 deg | 2.92 m |
| extend | 33.18 / 5.28 cm | 19.80 deg | 48.62 deg | 10.83 m |
| sit_again | 7.90 / 0.01 cm | 0.02 deg | 46.80 deg | 11.31 m |
| rise_again | 35.03 / 6.63 cm | 8.15 deg | 24.38 deg | 3.77 m |

Pitch/height oscillations persist after rising. Stationary-command planar motion is also substantial. This exceeds a claim of already-stable sitting/rising. Low grounded poses settle near 7.9 cm; successful low pose does not establish stable standing.

Lowering the ramp alone does not reliably cure the oscillations: at 2 cm/s the first rise has final height std 5.89 cm and pitch std 11.42 deg. The 0.50 m phase becomes quieter but settles near 0.4015 m, not the target. These are deterministic single trajectories of different durations, not an aggregate rate comparison.

Across sampled rising phases, legs do not sustain the 60 Nm cap (peaks approx 51–55 Nm). One later descent touches 60 Nm in a small fraction of sampled ticks. Torque is sampled at the last physics substep per 50 Hz control tick, so brief substep peaks can be missed. This is evidence against continuous leg-torque saturation being the sole explanation, not proof of hardware torque margin under DR.

## Reward inspection and inference

Saved weights: hip deviation -1.0, shoulder deviation -0.5, height error squared -10, body roll/pitch angular speed squared -0.05, commanded pose orientation -5, vertical speed squared -2.0. After 0.27 m, deviation fully returns to these original weights. Existing smoothness penalties remain.

Illustration using previously recorded nominal upright static configurations (not sampled policy rewards), under the same 0.50 m goal:

- A 0.335 m configuration gives hip/shoulder/height terms approximately -0.245 / -0.043 / -0.272, total -0.560 per second.
- A 0.50 m configuration gives approximately -0.556 / -0.405 / 0, total -0.961 per second.

For these three terms and these two example configurations, accurately reaching the high goal has worse reward. This supports a possible conflict between default-posture regularization and large height changes. It is a limited counterexample, not proof that this alone causes observed oscillation; other rewards, kinematics, history and dynamics matter.

A reasonable next experiment is to relax hip/shoulder deviation during large height transitions and strengthen damping of pitch motion when settling, choosing coefficients separately with the user. Current training and coefficients were left running unchanged toward 100000 steps.

Training logs at 44400 show stage 2 and fixed 2000-step / 40 s episodes. With contact termination disabled, episode length and timeouts no longer measure whether the robot stayed balanced. The saved native 40000 video has mean absolute height error about 9.18 cm over its mixed pose/velocity goals; this is not the same zero-command trajectory as this diagnosis.

## Changed files and verification

- Added `test/diagnose_sit_stand_stability.py`; all production source/config files unchanged.
- Recorded finite real controller execution at two height rates, 12 phases total. Raw trajectories and metrics: `sit_stand_stability_40000.json`; execution log: `sit_stand_stability_40000.log`.
- `./scripts/agent-check.sh` result: `sit_stand_stability_agent_check.log`.
- No physical robot commands or deployment; no training interruption, gain, friction, reward or saved ramp changes.

Branch: `agent/codex/tita-walk`. No commit or publication.
