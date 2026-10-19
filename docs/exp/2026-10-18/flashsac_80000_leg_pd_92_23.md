# FlashSAC 80000 RL leg PD: Kp 92 / Kd 2.3

- Date: 2026-10-18 (Asia/Seoul).
- Execution Domains: `DESKTOP_DRY_RUN`, `VALIDATION_SIM`, `ROBOT_READ_ONLY`, `ROBOT_STATE_CHANGING` (approved resource deployment/build only).
- Evidence Status: local hash/interface/parity and simulation execution `PASS`; physical effect `NOT_TESTED`; SBC update/build/installed-resource verification `PASS`.
- Checkpoint SHA256: `79f9175bb8c3be0c5138866e30891b90cc1282b6c98023cdb76c2e33b229068c`.
- ONNX SHA256: `26f0d86b65a68475fb8a315fb31e829ae16eaa2cf16dabbbcf38e69f28c933e9` (unchanged).
- Config SHA256: `10d66ca07cc10e07d38e3a44e204768881fc2285aa5baa6fcefffc0792f1b1e7`.
- Branch: `agent/codex/dev_tita_gluon`; no commit/push.

## Requested change

Only the six native leg joints (indices 0,1,2,4,5,6) change in the deployment copy of `policies/flashsac_80000/config.json`:

```text
joint_kp = [92, 92, 92, 0, 92, 92, 92, 0]
joint_kd = [2.3, 2.3, 2.3, 0.5, 2.3, 2.3, 2.3, 0.5]
```

Previous leg gains were 60 / 1.5. Both are multiplied by about 1.533. Wheel Kp0/Kd0.5, final leg +/-60 Nm and wheel +/-12 Nm limits, policy/observation/action scales, command range, velocity bias and robot SDK are unchanged. This changes the RL ActionAdapter only. Transform-up/sit PD and four-second supporting-sit use their own constants and are not overwritten by these config arrays; their entry torque naturally reflects the new preceding RL torque.

The public launch's config SHA pin and bundle manifest were updated together. Manifest records deployment gain overrides rather than relabelling the source training checkpoint. The original training actor/export and other policy bundles remain unchanged. README describes the new experiment. Baseline copies of all four edited files and before hashes are in `flashsac_80000_leg_pd_92_23/` for review/rollback.

## Direct verification

- PASS DESKTOP_DRY_RUN: native C++ vs sim2sim adapter, obs max error 1.20e-7, RL torque max error 1.10e-5 Nm; startup-state torque 1.17e-4, zero state mismatches/6000 (`adapter_parity.log`).
- PASS DESKTOP_DRY_RUN: pinned config/ONNX validation and corruption rejection, 33 obs / 8 actions / 50 Hz; PyTorch vs C++ ONNX 256 inputs, max action error 3.457e-6 (`setup.log`).
- PASS VALIDATION_SIM: seed42 nominal plant, canonical startup, frozen policy, 500 Hz motor / 50 Hz inference, bias OFF; continued RL, production return, production estop all completed without fall/nonfinite faults.
- Same 5..8 s event-relative continued-RL window: baseline 60/1.5 pitch mean **5.058°**, new 92/2.3 **3.201°**. This is one nominal simulation comparison, not a prediction of actual robot pitch.
- Return/estop acceptance PASS: max downward speed 0.1274 m/s, peak floor normal 460.0 N. Continued-RL's generic `acceptance_status=FAIL` comes from the shared sit-height requirement; it is not a failed RL rollout. The trial remains standing with no fault as intended.
- New-gain simulation hit knee +/-60 Nm clipping for **10 samples / 20 ms per knee**, around RL entry. The earlier nominal baseline knee peak was about 45..49 Nm. Existing caps were preserved, but stronger gains do increase transients; no physical motor trial was run.

Limits: single nominal seed, no matched hardware trial, no claim that physical steady-state knee error/pitch will reduce in the same ratio, no validation of a new gain with bias ON/disturbances/max commands. Related nominal baseline evidence is in `slow_sit_80000_deploy/nominal/`.

## Deployment status and procedure

The operator explicitly replied that the robot was powered on and approved SBC update/rebuild after reviewing the prepared change. The resource payload was deployed using `test/sim2real/deploy_leg_pd_92_23.sh`. Read-only preflight confirmed the old source hashes, active company service and no running `tita_node`.

SBC build PASS: one package / 2.08 s (`remote_build.log`). Installed config/launch/manifest byte comparisons and pinned hashes PASS; required leg/wheel gains and torque caps verified (`remote_verify.log`). The C++ executable SHA was unchanged before/after. No controller, motor, MCU mode or company-service mutation was executed. Physical trial remains NOT_TESTED.

The approved deployment script checked old source hashes, refuses replacement while `tita_node` runs, backs up affected source/installed resources, installs the new config/launch/manifest, runs `colcon build --packages-select tita_controller`, validates installed gains/hash pins, and checks the executable binary is unchanged. It never executes the robot controller or stops/starts the company service.

Source and installed `config.json`, pinned launch and manifest are now updated together on the SBC. The operator should source the rebuilt overlay before running the existing `ros2 launch tita_controller flashsac.launch.py output_enabled:=true` command. No physical execution has been performed in this task.

## Files / required completion checks

Edited production resources: deployment `config.json`, `manifest.json`, `launch/flashsac.launch.py`, workspace README. New helper: `test/sim2real/deploy_leg_pd_92_23.sh`. Added docs/exp report, before snapshots, payload and direct verification logs. Other pre-existing workspace sources are preserved; no policy network or C++ control code changed.

Required `agent-check.sh`: see `flashsac_80000_leg_pd_92_23/agent_check.log`; known six pre-existing trailing-whitespace errors in `my_flat_env_cfg.py` are not part of this change. Final scoped diff/hash review is recorded in `completion_integrity.json`.

SBC logs/rollback backup: `~/tita_ws/docs/exp/2026-10-18/flashsac_80000_leg_pd_92_23/`. Affected source and installed resources are in `before_deployment.tar.gz`; no rollback was applied.
