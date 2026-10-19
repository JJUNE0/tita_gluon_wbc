# README command simplification

- Execution Domain: `DESKTOP_DRY_RUN`.
- Policy Checkpoint SHA256 / ONNX Hash: N/A (documentation only; no policy execution).
- Evidence Status: `PASS` for shell syntax and local links. Repository check output: `readme_command_simplification_agent_check.log`.
- Branch: `agent/codex/promote-tita-flat-cfg`.
- Changed files: root `README.md` and this verification note.

Reduced the root README from 256 lines to a command-focused setup/training/sim2sim/sim2real guide. Kept Isaac editable installation, MuJoCo setup, canonical flat training, headless/viewer playback and existing headw0 65k robot launch commands. Removed verbose environment audit tables, smoke-test examples and detailed deployment discussion; retained links to the existing component READMEs.

Removed stale references to the user-deleted `tita_gluon_ws`; current robot build instructions use `sim2real/tita_ws` / robot `~/tita_ws`. User deletions were not restored or edited. No runtime code was changed.

Checks actually executed: `bash -n` on all seven README shell blocks, existence checks for every relative README link, deleted-workspace reference check, `./scripts/agent-check.sh`, and final diff inspection. Syntax/link/reference checks passed. No simulation, robot build, deployment or hardware command was run for this edit; runtime behavior is `NOT_TESTED` and unchanged by this documentation edit.
