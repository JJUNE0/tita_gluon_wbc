# Pose/sit-stand settled stop latch restored; fresh experiment

Execution Domain: TRAINING_SIM / VALIDATION_SIM / DESKTOP_DRY_RUN

Evidence Status: PASS (configuration, native/adapter parity, finite learning and export/runtime); SUSPICIOUS (fixed old-policy comparison quality); NOT_TESTED (newly trained stopping and balance quality).

Policy Checkpoint SHA256: e95ab0c192cad7f8de3bb1ff4aadd2079eb087939c53b14fa8779a856048909b (independent accelerated curriculum probe).

ONNX SHA256: 49c4401852b352b3d9aa25aaacc9b28fe19362d6502e286ea03862b6f4863f45

Main run checkpoint SHA256: PENDING until first save; starts without source weights.

## Root cause

The earlier fix was enabled in walk, inline and one-leg-reference task configurations. Flat roll/pitch/height inherited flat defaults without enabling it; sit_stand inherited that omission. Saved model_40000 and model_75000 both contain wheel_error_velocity_thresholds=None and wheel_error_moving_anchor=False. Their playback WheelPositionError params omit velocity_thresholds and moving_anchor. Thus the training observation and zero-command world-position reward anchored on command zero during continued body motion, and sim2sim correctly replayed that saved legacy contract.

This affected training as well as playback. Changing source factories cannot retroactively change initialized training configs or saved checkpoints. The original checkpoints and their metadata were preserved.

## Fix

New pose/sit_stand configs use near-zero command bands [0.02,0.02,0.03], planar BODY linear speed norm <0.1 m/s and body yaw speed magnitude <0.15 rad/s. During coasting, the position reference follows motion and observation/position-hold reward are inactive. The first settled sample establishes zero error; slow later displacement accumulates error. A moving anchor limits retained wheel error to +/-0.3 m and planar reward-anchor distance to 0.3 m.

Also fixed command ordering for new pose tasks: velocity command first samples, pose command applies its low-height velocity gate, then stop/odometry state updates exactly once from the final command observed by the policy. The saved stop_state_after_pose flag defaults False to preserve old checkpoint ordering. This prevents training seeing a moving raw target while sim2sim observes its height-gated zero command. Pure observation reads and partial-reset isolation remain intact.

New thresholds and moving-anchor settings flow through existing checkpoint export to sim2sim automatically; sim2sim core source did not need modification. Actor/critic/action dimensions remain 38/42/8. Reward weights, actions, gains, torque caps, friction and all DR remain unchanged. Raw flat and existing other task settings were not broadened.

## Restart requested by user

Old run `tita_mjlab_095950_402808` was intentionally interrupted at 80585; last checkpoint `/home/cocel/Desktop/Research/tita_gluon_wbc/mj_lab/logs/flash_sac/tita_mjlab_095950_402808/model_80000` hash `b806d26ca3af5b2c47016ea4312213f3bdc55d388b39165a090157ba427f3bb7`. Its KeyboardInterrupt FAIL is an operator-requested stop.

New run `tita_mjlab_114540_063797` starts FROM SCRATCH: no --resume, no --warm_start, fresh actor/critic/optimizer/replay/normalization/counters.

- 4096 environments, 100000 vector steps, FlashSAC unchanged.
- Before 20000: height 0.25–0.50 m, base/knee contact termination enabled.
- From 20000: height 0.07–0.50 m, base/knee contact termination disabled; existing low-height velocity/pose/deviation/contact gates retained.
- Height ramp 0.04 m/s; 40 s episodes; same replay/n-step reset at curriculum boundary, preserving learned weights/optimizers at that boundary.
- W&B online: https://forge.coreweave.com/wandb/bjy6614-postech/tita_flat_flash_sac/runs/eohwxd18.
- Checkpoints every 5000 under `mj_lab/logs/flash_sac/tita_mjlab_114540_063797/`; 40 s videos every 10000.
- Latest observed step 300, updates 548, stage 1.

## Verification actually executed

- Native CUDA/adapter coasting, lateral motion, yaw, settled relatch, push, anti-windup and partial reset tests for pose and sit_stand; includes a nonzero velocity sampler target gated to zero by low height. Full selected suite: 56 passed, 8 skipped, 14 subtests passed. Log `pose_stop_latch_regression_final.log`. Initial added low-height fixture failed due to radius DR being randomized again on reset; fixing the fixture to unit radius restored exact parity. No production DR was disabled.
- Real FlashSAC/CUDA curriculum probe with 4096 environments: PASS, 16 vector steps, 12 finite updates, test-only transition at step 8; production transition stays 20000. Newly saved native flags and derived runtime params asserted.
- New-probe ONNX export: PASS, 256 samples, max error 5.1259995e-06. Actual isolated-domain ROS/MuJoCo/ONNX runtime: PASS finite, 400 control iterations. This random early probe is not a learned stopping-quality pass.
- Frozen old model_40000 with baseline vs explicit diagnostic candidate observation params: finite in abrupt-stop/push scenarios. On the one abrupt-stop trajectory, backward movement from running x peak changed 0.192 -> 0.031 m, but other stability metrics remain SUSPICIOUS; the push override can worsen overall behavior. Changing inference observations on old weights is not accepted as a final remedy. Logs `pose_stop_latch_fixed_policy.*`; candidate config is a separately labelled report artifact, not an edited checkpoint.
- `./scripts/agent-check.sh`: PASS; see `pose_stop_latch_agent_check.log`.
- Incremental task diff inspected; `pose_stop_latch_changes.diff`. Concurrent unrelated changes in `test/.fb_target_actor_bc_job.json` and `test/test_fb_target_actor.py` were observed and preserved untouched; see audit JSON. No unrelated changes were made by this task.

## Changed files

- `mj_lab/robots/tita/flat_env_roll_pitch_height_cfg.py`: enables settled/moving stop reference for pose descendants and finalizes state after height gating.
- `mj_lab/robots/tita/mdp.py`: saved optional ordering flag and one-per-tick stop state finalization.
- `test/test_mjlab_roll_pitch_height.py`: inheritance/export expectations for the repaired settings.
- `test/test_pose_stop_latch.py`: native/adapter/reward and height-gated stop regressions.

Remaining risks: new policy quality is untested; previous pitch/height oscillation and high-height reward tradeoffs may still need separate work. No physical robot commands or deployment performed.

Current branch: `agent/codex/tita-walk`. No commit, push or PR.
