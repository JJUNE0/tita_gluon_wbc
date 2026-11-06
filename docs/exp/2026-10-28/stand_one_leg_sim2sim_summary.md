# Stand-one-leg sim2sim preparation and early-checkpoint behavior

Execution Domains: VALIDATION_SIM / DESKTOP_DRY_RUN.

Evidence Status: PASS for checkpoint verification, ONNX parity, prepared interface, finite playback and state-machine checks. SUSPICIOUS for physical behavior; the tested 10k rollout fails the single-leg balance goal because the base contacts the floor. This does not assess the eventual 100k policy.

Policy Checkpoint SHA256: `f56a3a7c4bf80569eefdc453fe41439dc8d4c6cec557a0dbdd535d640dcbec1b`.

ONNX SHA256: `f039c2dfcb78ae77d7322afd1197310476583753832afd72df05623481971882`.

Branch: `agent/codex/tita-walk`.

## Prepared checkpoint and command

Frozen checkpoint: `mj_lab/logs/flash_sac/tita_mjlab_142712_580757/model_10000`.

Verified artifacts: `model_10000/sim2sim/actor/config.json`, `policy.onnx` and `manifest.json` under the checkpoint directory. The actor observation has 40 values and there are 8 actions. No task-specific runtime branch was needed: the existing exporter and simulator restore the saved gait and action metadata.

```bash
python3 sim2sim/sim2sim_ros2_jazzy/launch/sim2sim.launch.py \
  --ckpt mj_lab/logs/flash_sac/tita_mjlab_142712_580757/model_10000
```

Keyboard startup: `1`, wait for sit, then `0`. The policy's 1 s gait-settle interval is restarted on entry; no velocity command is needed. The restored gait has frequency 0.5 Hz, stance ratio 0.75 and `step_in_place=true`: a 2 s cycle, 0.5 s swing per foot and 1 s left/right offset. Saved vx/vy/yaw ranges are all `[0, 0]`, so motion keys do not command translation/turning. `r` keeps zero velocity and stepping continues; `6` exits policy mode, and `2` resets to splay/idle.

Both wheel actions restore `gate=always`, scale 20, offset 0 and saved clipping, so wheel control remains available during the gait. PD, motor limits, observation/action order, nominal terrain/wheel collision geometry and normalizers come from the existing verified checkpoint pipeline. New model directories can be passed to the same launcher and are exported automatically.

## Validation actually executed

PASS: existing launcher `--prepare-only`; 256 Torch/ONNX parity samples, maximum absolute error `3.5762786865234375e-06`. Log: `stand_one_leg_sim2sim_prepare.log`.

PASS: saved interface assertions for actor dimension, all-zero command ranges, step-in-place gait timing and both always-enabled wheel actions; `stand_one_leg_sim2sim_contract.json`.

PASS: existing launcher with `--headless --steps 600 --command 0 0 0`. Actual ROS/MuJoCo/ONNX playback completed and resources closed. Log: `stand_one_leg_sim2sim_playback.log`. This PASS only covers finite execution.

PASS: `test/check_sim2sim_walk_state_machine.py` on the prepared config, with real physics/ONNX inference. Manual-key callbacks were tested with only passive GUI creation suppressed; headless startup was also tested. Cases: manual **28 checks / 556 simulation steps / 142 policy calls**, headless **18 checks / 251 simulation steps / 141 policy calls**. Checks include initial splay, early-RL rejection, policy/gait exclusion during posture setup, sit-to-RL, fresh action/gait state, zero-command gait enabled after settling, wheel policy preserved, per-substep gait flag parity, idle/reentry and reset. Evidence: `stand_one_leg_sim2sim_state_machine.json`, `.md`, `.log`.

## Physical behavior caveat

A separate final-pose probe after 600 simulation steps found finite state and correctly enabled gait at command `[0, 0, 0]`, but body tilt was **90.56 degrees** and the base had ground contact at approximately **177.8 N**. This contact would trigger the training task's base-contact termination. Evidence: `stand_one_leg_sim2sim_pose_check.json` / `.log`. The generic interactive runtime does not apply training termination/reset automatically; use `2` to reset a fallen simulation.

Therefore successful export/control-flow checks do not establish learned one-leg balance. The tested model is the frozen 10k checkpoint; native learned-policy behavior was not compared here, so this preparation does not attribute the failure to convergence versus transfer differences. Training continues unchanged toward its existing budget.

## Files, checks and scope

Changed source/documentation: `sim2sim/README.md` only, adding the standalone single-leg invocation and zero-command behavior. The runtime, exporter, model assets and training source/configs were reused without modification. Added evidence and this report under `docs/exp/2026-10-28/`.

Incremental diff inspected in `stand_one_leg_sim2sim_changes.diff`; pre-existing edits preserved and no unrelated source files changed. Repository check result is recorded in `stand_one_leg_sim2sim_agent_check.log`. No commit, push, publication, hardware command or training interruption was performed.

Unresolved risks: physical single-leg balance of later checkpoints and learned-policy native/sim2sim differences require further evaluation. Manual window/mouse interaction for the MuJoCo viewer was not exercised in this task; the real manual-key state-machine path was exercised as described above.
