# Support velocity / stationary mixture, 4096 environments

- Execution Domains: TRAINING_SIM, VALIDATION_SIM, DESKTOP_DRY_RUN.
- Evidence Status: PASS for configuration, finite learner updates, export/runtime and local checks. Learned locomotion quality and hardware behavior NOT_TESTED.
- Branch: `agent/codex/tita-walk`.
- Active run: `tita_mjlab_194029_719452`, task `support_velocity`, PID 1558633.
- W&B: https://forge.coreweave.com/wandb/bjy6614-postech/tita_flat_flash_sac/runs/25ae67vl
- Policy Checkpoint SHA256: N/A for active run at launch; first full checkpoint pending. The independent 40-step pipeline probe hash is `856a9da1352da53cb3f97ae5268017ddfad6662a47570e4d971b9b84251331d9`, not the active run's policy.
- Probe ONNX SHA256: `fe4ee9234a5dd4693af20b24335b89a9ed6728242de80f5ccf29ed868e44b637`.

## Training configuration and launch

The user confirmed vx in [-0.5,0.5] m/s and body-z angular command in [-0.5,0.5] rad/s. vy is zero. At each existing 6–8-second command resample, stationary commands are chosen with probability 0.5; otherwise vx and yaw are independently uniform in the requested ranges. This is a sampled mixture, not a permanently fixed half of environment IDs. Support goals are independent: left/right/both are sampled with 0.4/0.4/0.2 probabilities at episode reset and held for the episode, without a gait.

The new `TitaSupportVelocityEnvCfg` extends the existing support task in `mj_lab/robots/tita/support_command_env_cfg.py`; task registration is in `mj_lab/scripts/train.py`. The original zero-command task is retained. Actor/critic/action dimensions remain 38/42/8. PD gains, wheel actions, delay/gain/knee/mass/inertia/COM/friction/noise/push randomization, and base/knee contact termination are unchanged.

In single-support modes, the original stationary penalty (weight -0.5) applies inside the command zero band only. Moving single-support commands instead activate linear and yaw exponential tracking rewards with weights 2 and 1, std 0.5, using the existing flat kernels. Other single-support weights and all 18 both-support flat terms are retained. This avoids penalizing requested translation and rotation as unwanted stationary drift.

The previous run `tita_mjlab_173314_948748` had already completed 100000 steps and 199802 finite updates (checkpoint SHA256 `45b679bbf08234eb85dcb42b00a83ad418b65770f29bbca7f90119ea12d96f77`). It was not killed or overwritten. The new experiment starts FROM_SCRATCH, with resume/warm-start/W&B-resume ID all unset. It uses 4096 environments, seed 42, CUDA 0, 100000 vector steps, the same FlashSAC learner/hyperparameters, a 1,000,000-transition GPU replay buffer and 2 learner updates per vector step after warmup. Launch provenance, source hashes and latest verified progress are in `support_velocity_training_launch.json`.

W&B online logging is enabled, checkpoints are scheduled every 5000 vector steps, and 500-frame/10-second videos every 10000 vector steps. The player now records commanded/actual yaw and draws it below the vx/vy panel. The support label was also moved below that panel so it no longer covers the actual-velocity row. Early probe videos use an untrained policy and are not evidence of task success.

## Real-runtime tilt margin and command compatibility

The old guard measures total body tilt from vertical, acos(-projected_gravity_z), and sends the controller to joint damping above 0.65 rad (about 37.2 degrees). It is a real-runtime fall condition, not the training environment's termination term. Roll and pitch combine in this measure; yaw does not affect tilt.

Support-policy RL now uses the startup-only `support_fall_tilt_deg` parameter, default 55 degrees. It must be finite and strictly between 0 and 90. Preparation, driving policies and non-RL states retain the old cutoff; invalid sensors still force damping. The parameter is read-only during execution and changes require restart. Source edits do not deploy or change an already-running robot controller.

The generic real loader now derives support-policy joystick caps from exported trained/runtime command ranges. Old zero-command policies remain zero; the new symmetric +/-0.5 ranges are allowed. This replaces the previous unconditional zero override for support policies. The frozen bundle launcher and hardware installation were not changed.

## Validation evidence

- `support_velocity_tests.log`: 12 passed, including the old support task, reward isolation, command mixture and actual 4096-environment finite stepping. The 20000-sample stationary fraction was 0.5001500; support counts 8057/7916/4027. In the native 4096-env probe, the observed stationary fraction was 0.48975 and packed observation shape was (4096,80).
- `support_velocity_pipeline_probe.log`: 16-env / 40-step independent pipeline experiment, 70 finite learner updates; new task checkpoint save/load succeeded. It is a separate experiment and was not used to initialize production training.
- `support_velocity_export_probe.log`: 256 PyTorch/ONNX samples, maximum action error 5.48362732e-6.
- `support_velocity_video_probe.json` and `support_velocity_video_decode.json`: 500 frames encoded and decoded; first frame visually inspected for vx/vy, support and yaw labels. The untrained probe repeatedly falls/resets, so this validates rendering/telemetry only.
- `support_velocity_sim2sim_probe.json`: actual local ROS/MuJoCo/ONNX manual and headless interface cases PASS. All three support one-hot commands changed without physics reset; this does not establish learned transition stability.
- `support_velocity_real_build.log`: production C++ `tita_node` rebuilt successfully on the desktop, without launching it.
- `support_velocity_real_tests.log`: 9 passed, including legacy zero-command behavior, new range forwarding, invalid tilt launch inputs, 4000-sample C++ observation parity and 300 contact-Jacobian cases.
- `support_velocity_tilt_tests.log`: 6 direct production-helper cases PASS; 40/50-degree roll allowed at 55, 56-degree roll/pitch rejected, combined 45-degree roll and pitch rejected because total tilt is 60 degrees, legacy 0.65-rad threshold retained in the old case.
- `support_velocity_agent_check.log`: repository syntax, XML, whitespace and experiment-directory checks; see final direct log.
- `support_velocity_changes.diff` and `support_velocity_verification.json`: this task's incremental changes and final hashes. Earlier unrelated dirty changes were preserved.

Changed files: the support environment, trainer/player registration/telemetry and mjlab README; real generic launch, C++ adapter/guard, real README; `test/test_mjlab_support_velocity.py`, `test/sim2real/test_support_fall_tilt.cpp`, and the existing real/friction test. No hardware deployment, physical command, commit or publication occurred.

Remaining limits: the new policy has not yet demonstrated sustained single-support locomotion or tracking. Real velocity gating assumes the commanded contact is grounded without slip; startup and mode transfers still differ from episode-fixed training and sim reset entry. The larger tilt margin is a code setting, not measured hardware validation or proof of recovery torque headroom.
