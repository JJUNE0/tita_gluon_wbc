# FlashSAC duplicate-process refusal and orphan cleanup fix

- Date: 2026-10-16 (Asia/Seoul)
- Execution Domain: ROBOT_READ_ONLY (diagnosis), DESKTOP_DRY_RUN (mock regression), ROBOT_STATE_CHANGING (code installation only).
- Evidence Status: FAIL before fix / PASS for 13 desktop mock tests and SBC installation/build; actual robot shutdown behavior NOT_TESTED.
- Branch: agent/codex/dev_tita_gluon
- Policy Checkpoint SHA256: `6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05`
- ONNX Hash: `f44f07ed44970e3ff565eae67fd9229adf0be5c02215591c52a691ffcbb71b2a`
- Source archive SHA256: `6c3c90be12fcebfde8bbfaca96cbc6c09adab6af0063ef9b214714ac93b58623`

## Observed failure

The operator's output-enabled attempt at 20:50:23 was refused before recording or
new-controller startup. Read-only inspection found the earlier output-disabled
inner launch PID 94966 reparented to PID 1, and its tita_node PID 94976 still alive.
Bringup was inactive. The old session summary had no Finished/exit-code entry.
Thus the duplicate-process guard correctly refused concurrent access.
No new output-enabled controller was started by the failed attempt.

Evidence: [flashsac_shutdown_orphan_inspection.log](flashsac_shutdown_orphan_inspection.log).

The old runner signalled only direct child PIDs. Background commands can inherit
ignored SIGINT, and descendants can survive their direct parent's exit. A desktop
mock containing a launch child and grandchild reproduced the orphan after Ctrl+C
with the original runner: [before-fix FAIL](flashsac_shutdown_before_fix.log).

## Change

Each inner launch and recorder is started using `env --default-signal=INT,TERM
setsid --wait ...`. Cleanup signals only those owned process groups, waits up to
3 seconds for each group, then sends TERM with a 2-second wait and finally KILL
if necessary. The summary records group IDs and the console reports escalation.
Console tee ignores SIGINT so shutdown messages are retained. Duplicate refusal
now includes matching process IDs/commands.

No global pkill or automatic cleanup of older sessions was introduced. Already
orphaned SBC PIDs were inspected but deliberately not signalled by the agent.
Policy, gains, state machine and actuator output selection are unchanged.

Changed files: `sim2real/tita_ws/run_flashsac.sh`, workspace README,
`test/sim2real/test_flashsac_logging.py`, this report/logs and delivery archive.

## Validation

- Before-fix descendant Ctrl+C test: FAIL (live orphan detected and mock cleaned by test).
- After-fix `test/sim2real/test_flashsac_logging.py`: PASS, 13 tests, including
  direct-runner Ctrl+C and actual ROS launch engine Ctrl+C with mock child and
  grandchild processes; no live descendants remained, summaries finished and
  mock recorder metadata was finalized. Existing automatic-stop/storage-failure
  tests also passed. [Log](flashsac_shutdown_tests.log).
- Local `colcon build --packages-select tita_controller`: PASS.
- `bash -n run_flashsac.sh`: PASS.
- SBC installation/build/static syntax: PASS. `tita_controller` rebuilt in 0.24 s,
  colcon exit 0. Installed runner equals updated source; GNU env signal reset and
  setsid support were checked using no-op commands. Public launch argument
  introspection passed without executing any launch action.
  [Build](flashsac_shutdown_sbc_build.log), [check](flashsac_shutdown_sbc_check.log).
- Latest read-only check still found old output-disabled PIDs 94966 and 94976.
  They were not killed. An operator must retire that old session before starting
  another one; the new duplicate guard remains active.
- Required `./scripts/agent-check.sh`: FAIL due to pre-existing trailing whitespace
  in `lab/ddt_lab/ddt_lab/tasks/manager_based/locomotion/robots/tita/my_flat_env_cfg.py`
  at lines 431, 437, 443, 449, 455 and 461. Python syntax: PASS, 462 files;
  URDF parsing: PASS, 8 files. [Log](flashsac_shutdown_agent_check.log).
- Final task diff inspected: [flashsac_shutdown_changes.patch](flashsac_shutdown_changes.patch).
  Tracked diff SHA256 remains
  `40076fca037839dbd955f4644f404a0e3ea6c8b5e7a3fc86a79bb15150ddab47`;
  index remains empty. No unrelated source changes were made.

Tests use fake service/sudo/controller/recorder commands and never access robot
hardware. Real old-session cleanup, CAN behavior and physical torque remain
NOT_TESTED. No agent-issued stop/restart/kill or motor command was performed on SBC.
Existing unrelated source changes are preserved; nothing staged/committed/pushed.
