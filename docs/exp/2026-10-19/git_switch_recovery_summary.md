# Interrupted git switch recovery

- Execution Domain: DESKTOP_DRY_RUN.
- Policy Checkpoint SHA256 / ONNX Hash: N/A (Git worktree recovery).
- Evidence Status: PASS.
- Branch: agent/codex/promote-tita-flat-cfg.
- Restored commit: 88d7f24099fd3fce109699993bf430e696c3f8de.
- Backup: /tmp/tita_git_recovery_20261019_162948_494489.

Interrupted checkout left HEAD/index on the task branch, 6,078 tracked files missing, and 14 tracked files replaced by exact main versions. Backed up existing changed files, Git index/HEAD and the path manifests; restored only the 6,092 affected tracked paths from the existing commit. Moved 459 main-only checkout artifacts to backup (458 exact main blobs and one verified truncated prefix). No artifacts were discarded; commits, branch refs, original committed deletions and other ignored data were preserved. No remote push was performed.

Verification: tracked and staged diffs empty and git status clean before this audit note; agent-check exited 0, 669 Python syntax checks and 8 URDF XML checks passed. Direct evidence: git_switch_recovery_agent_check.log. Only this audit Markdown is newly untracked after recovery. No simulation or robot command was run.
