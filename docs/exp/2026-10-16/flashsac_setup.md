# Frozen FlashSAC model_60000 execution preparation

- Date: 2026-10-16 (Asia/Seoul)
- Execution Domain: DESKTOP_DRY_RUN
- Evidence Status: PASS for local build, adapter parity, native actor inference parity and launch resolution; NOT_TESTED on SBC/hardware.
- Branch: agent/codex/dev_tita_gluon
- Policy Checkpoint SHA256: `6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05`
- ONNX Hash: `f44f07ed44970e3ff565eae67fd9229adf0be5c02215591c52a691ffcbb71b2a`
- Export config SHA256: `66f6113a3c607839bd79a266716fac856d5b271006d51c7c028230e47f7efe31`
- Source: `lab/ddt_lab/logs/flash_sac/tita_flash_sac_115632_883848/model_60000`

## Behavior

The new `ros2 launch tita_controller flashsac.launch.py` entrypoint loads the installed
frozen actor without a checkpoint path. Config and ONNX bytes are pinned and verified
before launch creates any nodes. Source export files are unchanged.
Observation size is 33, action size is 8, policy frequency is 50 Hz, and the motor
loop is 500 Hz. Trained action gains remain embedded in the exported actor.
There is no residual, online RLS, probing, or gain/bias/reference adaptation.

Startup and left-switch-up use `idle`, retaining the original damp torque:
`torque[i] = clip(-Kd[i] * joint_velocity[i], -limit[i], limit[i])`, with
`Kd = [8, 8, 8, 0.5, 8, 8, 8, 0.5]`. At rest this is zero; moving joints receive
opposing damping torque. This follows the user's explicit `idle = existing damp`
selection. The existing transform-up trajectory and ready-pose hold are retained. Once ready (`sit`),
the operator selects RL with the right switch. Direct RL from idle, an incomplete
transform, or fault damping is rejected. Errors continue to use the separate
`damp` state with the same damping gains. Left-switch-up idle does not hold a
joint pose.

Policy timing/tensor shapes are checked; quaternion validity and non-finite
observations/actions are checked. Inference exceptions enter damp. The joystick
can no longer override the tilt fault in the same control tick. New debug topics
publish computed torque and state alongside existing observations/actions.
Computed torque uses native left-leg-1..4/right-leg-1..4 order; it is not measured
or evidence of applied hardware torque. The output gate remains false by default.

## Changed files

- `sim2real/tita_ws/src/tita_controller/launch/flashsac.launch.py`: new pinned-policy launch.
- `sim2real/tita_ws/src/tita_controller/policies/flashsac_60000/{config.json,manifest.json,policy.onnx}`: unchanged copies of the selected export.
- `sim2real/tita_ws/src/tita_controller/{CMakeLists.txt,package.xml}`: install policy bundle and declare launch dependencies.
- `sim2real/tita_ws/src/tita_controller/include/tita_controller/state_machine.hpp`: explicit idle retaining original velocity damping.
- `sim2real/tita_ws/src/tita_controller/include/tita_controller/adapter.hpp`: observation finite-value check.
- `sim2real/tita_ws/src/tita_controller/src/tita_node.cpp`: policy checks, fault precedence, computed torque/state topics.
- `sim2real/tita_ws/README.md`: SBC build, launch and joystick sequence.
- `test/sim2real/{flashsac_runtime.cpp,test_flashsac_setup.py}`: hardware-free integration checks.
- This report, [task diff](flashsac_setup_changes.patch), and execution logs in this date directory.

Existing untracked controller files were present before the task. The task diff
records only this task's edits against their initial contents; unrelated training,
sim2sim, vendor package and existing test sources were left unchanged. No files
were staged, committed or pushed. Ignored local build/install outputs were rebuilt.

## Executed checks and observed metrics

1. Local ROS Jazzy `colcon build --packages-up-to tita_controller --cmake-args -DBUILD_TESTING=OFF -DPython3_EXECUTABLE=/usr/bin/python3`: PASS, four packages finished.
   The damping correction was rebuilt successfully; see [build output](flashsac_idle_damping_build.log).
2. Existing `test/sim2real/test_sim2real_parity.py` against the selected bundle: PASS.
   50 samples, 33 observation dimensions; max observation error `1.20e-7`, max RL
   torque error `7.17e-6`, max transform-state torque error `1.17e-4`, zero state
   mismatches across 6,000 steps. [Log](flashsac_setup_parity.log).
3. New `test/sim2real/test_flashsac_setup.py --torch-python /home/cocel/anaconda3/envs/online_rl/bin/python`: PASS.
   Native PyTorch FlashSAC actor versus C++ ONNX Runtime: 256 samples,
   max action error `3.099e-6`. Repeated inference was identical and finite.
   Original idle damping gains, pose independence, zero torque at rest, torque
   saturation, staged RL rejection/acceptance, return to idle and identical fault
   damping passed. Both modified config and modified ONNX bundles were rejected.
   [Current log](flashsac_idle_damping_runtime.log). The earlier
   `flashsac_setup_runtime.log` documents the superseded zero-torque assumption.
4. Installed launch `--show-args` and child-launch/bundle resolution: PASS;
   `output_enabled` defaults to false. No child node executed.
   First launch-introspection attempt failed because the default `~/.ros/log`
   is outside writable roots; setting `ROS_LOG_DIR` under this experiment directory
   resolved it. [Arguments](flashsac_setup_launch_args_verified.log),
   [resolution](flashsac_setup_launch_resolution.log).
5. Installed executable linkage after sourcing ROS and workspace: PASS, no missing
   shared libraries. [Log](flashsac_setup_linkage.log).
6. New Python launch/test files: PASS, `python3 -m py_compile`.
7. Required `./scripts/agent-check.sh`: FAIL, exit 1, solely from the existing
   trailing whitespace in `lab/ddt_lab/ddt_lab/tasks/manager_based/locomotion/robots/tita/my_flat_env_cfg.py`
   at lines 431, 437, 443, 449, 455 and 461. Unrelated contents were not changed.
   Python syntax: PASS, 461 files, zero failures. URDF parsing: PASS, 8 files.
   Experiment directory naming: PASS. The damping correction's required rerun
   produced the same result. [Current log](flashsac_idle_damping_agent_check.log).
8. Final review: existing-file task diff inspected; new launch/test files pass
   `git diff --no-index --check`. The tracked working-tree diff SHA256 remains
   `40076fca037839dbd955f4644f404a0e3ea6c8b5e7a3fc86a79bb15150ddab47`,
   identical to the pre-task state; the index remains empty.

All new custom test code/fixtures/binaries are under `test/`; temporary fixtures
are removed after execution. The pre-existing parity script uses its own system
temporary directory and was executed without modifying that existing script.

## Delivery and remaining limits

A local source-only delivery archive (including vendor ARM/AMD64 libraries and the
pinned policy, excluding build/install and Python cache directories) is prepared at
`sim2real/tita_ws/build/flashsac_60000_sbc_source.tar.gz`.
Archive SHA256: `6e3ed6d41e910f8289a4347e881b66d049511821286a27c6ac4b85c074ee27ce`.

No SSH access, remote file writes, deployment, service changes, CAN/UART opening,
robot launch or actuator commands were performed in this task. Per root `AGENTS.md`
section 3, SBC deployment and physical actuation require separate operator approval.
The proposed deployment target is a new isolated `~/flashsac_60000_ws` workspace;
existing robot workspaces/services would remain untouched during source copy/build.

- SBC ROS distribution/dependencies and ARM build: NOT_TESTED.
- Existing controller ownership and CAN output behavior: NOT_TESTED.
- Physical torque signs/units, left/right allocation, IMU frame and sensor calibration: NOT_TESTED.
- Actual idle/transform/RL motion and control-loop timing under SBC load: NOT_TESTED.
- No claim of hardware readiness follows from desktop parity results.

Subsequent user-authorized replacement/build at `/home/robot/tita_ws`: PASS. See [SBC build report](flashsac_sbc_build.md); robot runtime remains NOT_TESTED.
