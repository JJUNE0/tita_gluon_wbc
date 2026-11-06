# Root README: mjlab pose training command

- Execution Domain: `DESKTOP_DRY_RUN`
- Policy Checkpoint SHA256 / ONNX Hash: `N/A`; documentation-only change.
- Evidence Status: `PASS` for `./scripts/agent-check.sh` and final diff inspection.
- Branch: `agent/codex/mjlab-pose-publication`; publication target: `main`, as requested.
- Observed behavior / log summary: added one `flat_roll_pitch_height` training
  command to the existing mjlab Bash example in the root `README.md`.
  Active Isaac paths already use `isaac_lab/`; no legacy `lab/` path remains
  in this README. No training or hardware command was executed.
- Validation log: `mjlab_readme_pose_command_agent_check.log`.
- W&B: `N/A`; explicitly local/offline documentation check, no training/upload.
- Remaining limits: the documented training command was not used to start a run.
