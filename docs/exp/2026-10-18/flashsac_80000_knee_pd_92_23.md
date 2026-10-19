# FlashSAC 80000: knee-only 92 / 2.3 gains

- Date: 2026-10-18 (Asia/Seoul).
- Execution Domains: `DESKTOP_DRY_RUN` (config/interface and adapter checks), `ROBOT_READ_ONLY` (preflight), `ROBOT_STATE_CHANGING` (operator-requested resource deployment/build only).
- Evidence Status: local validation and SBC deployment/build/installed-resource checks PASS; physical behavior NOT_TESTED.
- Checkpoint SHA256: `79f9175bb8c3be0c5138866e30891b90cc1282b6c98023cdb76c2e33b229068c`.
- ONNX SHA256: `26f0d86b65a68475fb8a315fb31e829ae16eaa2cf16dabbbcf38e69f28c933e9`.
- Config SHA256: `a24c2137969f854fc98cc3027884dbbadad4060f18db7758b028c12ca1405719`.
- Branch: `agent/codex/dev_tita_gluon`; no commit/push.

Requested native order is left leg 1..4, right leg 1..4. Only knees (indices 2,6) keep the stronger gains; indices 0,1,4,5 return to 60 / 1.5:

```text
joint_kp = [60, 60, 92, 0, 60, 60, 92, 0]
joint_kd = [1.5, 1.5, 2.3, 0.5, 1.5, 1.5, 2.3, 0.5]
```

Changed resources: deployment `policies/flashsac_80000/config.json`, its manifest, `launch/flashsac.launch.py` config hash pin, workspace README. A scoped deployment helper is in `test/sim2real/deploy_knee_pd_92_23.sh`. Before snapshots, diffs, payload and logs are under `flashsac_80000_knee_pd_92_23/` next to this report.

The public launch validates the updated config hash, then the generic launch flattens the arrays into native-order ROS parameters used by the C++ RL ActionAdapter. Wheels remain Kp0/Kd0.5, final torque caps remain legs +/-60 Nm and wheels +/-12 Nm. Policy network, observation/action scales, bias behavior, slow-sit state-machine gains and the preceding shutdown fix are preserved. No new physical run is part of this request.

## Verification

- PASS DESKTOP_DRY_RUN: pinned bundle/manifest hashes and native joint gains checked through actual launch parameter mapping. Config differs from its saved before copy only in `robot.joint_kp` and `robot.joint_kd`; see `config_validation.log`.
- PASS DESKTOP_DRY_RUN: existing C++ vs sim2sim parity harness using the new config: 50 observation samples, maximum observation error 1.20e-7 and RL torque error 1.10e-5 Nm. Startup state torque error 1.17e-4 Nm; zero state mismatches over 6000 steps. See `adapter_parity.log`. This is code parity, not a physical stability test.
- NOT_TESTED: physical tracking, pitch, vibration or motor response with these gains.

## Deployment and completion

The operator requested the gain change and rebuild in the same instruction. Read-only SBC preflight found no running `tita_node` and confirmed matching before resource hashes and the existing shutdown-patched executable hash. Deployment checks those hashes again, backs up affected source/installed resources, installs only the four scoped resources and runs `colcon build --packages-select tita_controller`.

PASS ROBOT_STATE_CHANGING: SBC package build 1.25 s (colcon total 1.83 s); installed config, manifest and launch byte comparisons match source. Actual installed launch hash validation and parameter mapping confirm the requested arrays and original torque caps. The executable hash remains `2e3949c0b445fa328ab33ac7b152d3096170e17e1a863a2a8494fdb79dc0d9ff`, preserving the preceding shutdown fix. No controller, service change, MCU mode request or motor command was executed by this procedure.

Logs: [SBC build](flashsac_80000_knee_pd_92_23/remote_build.log), [installed-resource verification](flashsac_80000_knee_pd_92_23/remote_verify.log), [adapter parity](flashsac_80000_knee_pd_92_23/adapter_parity.log). Rollback backup on SBC: `~/tita_ws/docs/exp/2026-10-18/flashsac_80000_knee_pd_92_23/before_deployment.tar.gz`. No rollback was applied.

Required agent-check ran: overall FAIL due to six pre-existing trailing-whitespace errors in `my_flat_env_cfg.py` (431,437,443,449,455,461). Python syntax 565 PASS, URDF parsing 8 PASS. See [agent-check log](flashsac_80000_knee_pd_92_23/agent_check.log). Unrelated changes were preserved; scoped before/after diff and source hashes were reviewed and recorded in `completion_integrity.json`.
