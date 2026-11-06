# Sit/stand model_40000 sim2sim verification

Execution Domain: VALIDATION_SIM / DESKTOP_DRY_RUN

Evidence Status: PASS (export/interface and finite playback); NOT_TESTED (repeatable sit/stand cycle and hardware behavior).

Policy Checkpoint SHA256: 3bbb4cb43e3363936ed13473fd46e5b4a3ebe654e37e19e2dc5bae37225b7506

ONNX SHA256: 71db553d55d99d85e91865e12317d4bbf7f0ff76f82a648b014521dafe000984

Checkpoint: `mj_lab/logs/flash_sac/tita_mjlab_095950_402808/model_40000`. Saved training curriculum stage 2. Training remains running and was not interrupted.

## Behavior and evidence

No source changes were needed. Existing runtime reads the saved expanded action gains, 38 observations/8 actions, height range 0.07–0.50 m, height ramp 0.04 m/s, roll/pitch 0.15 rad/s and low-height motion gate 0.20–0.27 m. Older stage-1 model_15000 retains height range 0.25–0.50 m.

Torch/ONNX export: PASS, 256 inputs, maximum absolute output error 3.4570694e-06.

Actual ROS/MuJoCo/ONNX, headless, isolated local domain 90:

- Low target [0,0,0.07], 850 control iterations: PASS finite runtime; final emitted [0.0, 0.0, 0.07000000029802322]; actual roll/pitch/height [-6.379280239343643e-05, -3.51138169207843e-07, 0.07894697785377502] rad/rad/m. The approximately 7.9 cm upright ground-contact limit was observed.
- Nominal target [0,0,0.335], 650 control iterations: PASS finite runtime; final actual [-0.029249882325530052, -0.07886869460344315, 0.3443377912044525] rad/rad/m.

These are endpoint observations after the existing IDLE/transform/SIT startup, not a sequential full sitting-and-rising quality evaluation. No graphical viewer opened by this check; no physical robot commands or deployment performed.

## User launch

```bash
python3 sim2sim/sim2sim_ros2_jazzy/launch/sim2sim.launch.py \
  --ckpt mj_lab/logs/flash_sac/tita_mjlab_095950_402808/model_40000 \
  --pose 0 0 0.335
```

Terminal keys: 1 prepare, wait for sit, 0 enter policy; u/o raise/lower target by 1 cm, p nominal 0.335 m; j/l roll +/-1 degree, i/k pitch +/-1 degree. GUI shows target/emitted/actual pose. Height changes use the saved 4 cm/s rate. Training termination rules are not runtime respawn rules in sim2sim.

Changed source files: none. Created artifacts: export cache inside this checkpoint and verification logs/report inside docs/exp/2026-10-29. `./scripts/agent-check.sh` result is recorded in `sit_stand_40000_sim2sim_agent_check.log`.

Branch: `agent/codex/tita-walk`. No commit or publication.
