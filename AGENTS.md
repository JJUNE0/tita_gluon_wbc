# AGENTS.md — Robot RL Closed-Loop Validation & Agent Harness

This file defines how Codex, Claude, Antigravity, and other coding agents must work in this repository.

The central objective is to build a traceable closed-loop validation flow:
```text
RL TRAINING -> POLICY EXPORT -> SIM-TO-SIM VALIDATION -> STAGED SIM-TO-REAL -> READ-ONLY REAL-TO-SIM -> GAP DIAGNOSIS -> REGRESSION SIM-TO-SIM
```

---

## 1. Non-Negotiable Agent Rules

### 1.1 Inspect before changing
Before a meaningful change:
1. Identify the target execution domain.
2. Inspect relevant code and config.
3. Trace data flow across process boundaries.
4. Make the smallest reviewable change.
5. Run `./scripts/agent-check.sh` or the lowest-risk relevant test.
6. Record the result.

### 1.2 Execution Domains
Every report or tool action must state one of:
- `TRAINING_SIM`
- `VALIDATION_SIM`
- `DESKTOP_DRY_RUN`
- `ROBOT_READ_ONLY`
- `ROBOT_COMMAND_FREE_RUNTIME`
- `ROBOT_STATE_CHANGING`

### 1.3 Evidence Statuses
Never claim tests passed without direct log evidence. Use:
`PASS`, `SUSPICIOUS`, `BLOCKED`, `FAIL`, `NOT_TESTED`.

---

## 2. Git workflow

### Before making changes
1. Run `git status --short`.
2. Identify any pre-existing changes.
3. Do not modify, stage, revert, or overwrite changes that were not created during the current task.
4. Never work directly on `main` or `master`.

### Required completion protocol
After modifying any file, before reporting completion:
1. Run `./scripts/agent-check.sh`.
2. Inspect the final diff.
3. Confirm that no unrelated files were changed.
4. Report:
   - changed files
   - behavioral changes
   - tests actually executed
   - test results
   - unresolved risks
   - current branch name
5. Never claim that tests passed unless they were actually executed.

A task is not complete until this protocol has been performed.

### Commit and GitHub policy
Do not commit, push, or create a pull request unless the user explicitly requests publication or the task includes `PUBLISH=true`.

When publication is requested:
1. Work only on an `agent/<tool>/<task>` branch.
2. Run `./scripts/agent-check.sh`.
3. Commit only the current task's changes.
4. Push the task branch.
5. Create a draft pull request.
6. Never push directly to `main` or `master`.
7. Never merge the pull request.
8. Report the commit hash and pull-request URL.

---

## 3. High-risk project policy

For robot hardware, shutdown, watchdog, direct control, networking, Sim2Real, and safety-related code:
- Git publication does not authorize deployment.
- Never deploy to hardware automatically.
- Never run physical robot commands automatically.
- Merging and deployment require separate operator approval.
