# README policy transfer commands

- Execution Domain: `DESKTOP_DRY_RUN`.
- Policy Checkpoint SHA256 / ONNX Hash: N/A (documentation only).
- Evidence Status: `PASS` for README shell syntax and local links; repository check evidence is in `readme_policy_transfer_agent_check.log`.
- Branch: `agent/codex/promote-tita-flat-cfg`.
- Changed files: `README.md` and this record. Runtime code and existing user changes/deletions were untouched.

Added desktop SSH directory creation and SCP commands for the verified export's `policy.onnx`, `config.json`, and `manifest.json`. Added the corresponding robot `tita.launch.py policy_dir:=...` command so the copied candidate is actually selected. Retained the separate pinned headw0 bundle commands and the generic launch's prerequisites concerning controller ownership, MCU mode and recording.

Checks: source inspection of export artifacts, generic loader's `policy_dir` handling and fixed-bundle hash validation; `bash -n` on README shell blocks; relative link existence; `./scripts/agent-check.sh`; final diff inspection. SSH, file transfer, deployment and robot execution are `NOT_TESTED` and were not performed. Host/IP is an operator-supplied placeholder.
