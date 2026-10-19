# Sim2Real SSH connection check

- Date: 2026-10-16 (Asia/Seoul)
- Execution Domain: ROBOT_READ_ONLY (SSH); DESKTOP_DRY_RUN (local checks)
- Evidence Status: PASS (SSH authentication and OS queries)
- Policy Checkpoint SHA256 / ONNX Hash: N/A; no policy selected, loaded, or executed.
- Branch: agent/codex/dev_tita_gluon
- Scope: User requested connectivity first, before Frozen FlashSAC / fixed M4 residual preparation.

## Observed behavior and evidence

Target: `robot@192.168.0.28:22`. Password authentication succeeded; credentials are omitted.
The first sandboxed SSH attempt failed locally with `socket: Operation not permitted`.
The approved network-access retry authenticated successfully and exited with code 0.
SSH used an isolated local known-hosts file at `/tmp/tita_robot_readonly_known_hosts`
with `StrictHostKeyChecking=accept-new`.

Only these remote queries were executed:

```sh
hostname; id -un; uname -srm; cat /etc/os-release
```

Observed output:

```text
tita
robot
Linux 5.15.136-tegra aarch64
PRETTY_NAME="Ubuntu 22.04.5 LTS"
VERSION_CODENAME=jammy
```

No deployment, service changes, ROS launch, CAN access, or actuator commands were performed.

## Follow-up scope and limits

- Existing local `sim2real/tita_ws` code was discovered and left unchanged.
- 24-state mapping, residual=0 parity, torque signs/units, and left/right allocation: NOT_TESTED.
- Online RLS, gain/bias/reference updates, and probing were not started or configured.
- Robot ROS environment and message interfaces: NOT_TESTED.
- Repository contains extensive pre-existing changes; this task adds only this report and its check log.

## Local validation

- `./scripts/agent-check.sh`: FAIL, exit code 1, due to pre-existing trailing whitespace in
  `lab/ddt_lab/ddt_lab/tasks/manager_based/locomotion/robots/tita/my_flat_env_cfg.py`
  at lines 431, 437, 443, 449, 455, and 461. These unrelated changes were left untouched.
- Python syntax: PASS, 460 files passed, 0 failed.
- URDF XML parsing: PASS, 8 files.
- Experiment directory naming: PASS.
- Full check output: [sim2real_ssh_connection_agent_check.log](sim2real_ssh_connection_agent_check.log).
