# Restore TITA MCU Direct initialization

- Execution Domains: DESKTOP_DRY_RUN (implementation/tests), ROBOT_READ_ONLY (comparison), ROBOT_STATE_CHANGING (authorized bounded MCU/zero-torque diagnosis).
- Evidence Status: PASS for initialized 500 Hz zero-torque transport and subsequently approved SBC build; NOT_TESTED for torque-enabled revised launcher and nonzero torque/RL.
- Policy checkpoint SHA256: `6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05`.
- ONNX SHA256: `f44f07ed44970e3ff565eae67fd9229adf0be5c02215591c52a691ffcbb71b2a`.
- Branch: `agent/codex/dev_tita_gluon`.

## Cause and prior behavior

The operator clarified the previously working experiment was real RL/PPO in
the former `tita_ws`. Its archived configuration uses a 500 Hz controller and
the exact same `libtita_robot.so` SHA256 as the new workspace:
`22460f0b59fd10265b100ab725828c34a62654f858468f1afaa28359c050ae7d`.
The previous supervisor calls upstream `ddt_ros2_control/start.bash` after
stopping vendor control and checking CAN ownership. The new standalone launcher
omitted that initialization. Upstream README explicitly requires TITA Ready ->
Direct initialization before direct hardware operation.

The archived start script SHA256 is
`0a2bca4a146f9127ad558b50ca745826cc93ee920f3bb9538521555ea94f97b3`.
It requests SET_READY_NEXT=READY_WAITING, waits 0.2 seconds, then requests
SET_READY_NEXT=FORCE_DIRECT on CAN ID 0x170. SDK construction alone does not
execute these requests.

## Hardware comparison

User authorization for direct diagnosis and supported robot/operator presence
was retained. Checked for active vendor/controller/probe processes before
transmission. First precheck accidentally matched its own command shell and
aborted without sending anything; corrected the probe-process expression to
anchor the executable at the start of the command line, then rechecked.

Ran the hash-verified archived startup script, followed by the same standalone
zero-torque probe used earlier. No bitrate, queue length, SDK, policy rate or
motor-loop rate was changed.

| Condition | 500 Hz SDK calls | Outcome | New qdisc drops |
| --- | --- | --- | --- |
| Without Direct initialization, prior test | 9 in 17.6 ms | FAIL: ENOBUFS | 1 |
| After upstream initialization | 500 in 1.00015 s | PASS | 0 |
| Repeat after initialization | 1,000 in 2.00017 s | PASS | 0 |

Capture after initialization contains all 2,000 expected command frames from
the one-second trial, 500 each for IDs 0x120–0x123, plus both initialization
requests. In a 3.282-second window starting 0.5 s after FORCE_DIRECT, RX rate was
1,559 frames/s. IDs 0x108/0x109/0x118 were approximately 500 Hz each, and
0x110–0x113 periodic status frames disappeared. Before initialization the
observed RX rate was approximately 7,100 frames/s, with seven dominant IDs
approximately 1,000 Hz each.

These measurements link the missing initialization to a different MCU
broadcast/control regime and explain why the same requested command rate
failed before initialization and passed afterward. The exact firmware scheduling
implementation was not inspected. Independent board-mode ACK is not exposed
by this SDK; successful request transport is not labeled as a mode ACK.
Earlier statements that 500 Hz was intrinsically unsupported were too broad:
the failure applied to the uninitialized operating condition.

## Local implementation

- `sim2real/tita_ws/src/tita_controller/launch/flashsac.launch.py`: public entrypoint
  explicitly documents Direct initialization and output selection. The existing
  logged runner serializes service stop, recorder, MCU requests and node startup.
- `sim2real/tita_ws/run_flashsac.sh`: output true requires `cansend`, records first,
  then sends exactly the two upstream initialization frames with the 0.2 s gap,
  and only then starts the controller. Either send failure prevents startup.
  Output false sends no MCU requests. Each accepted request is logged in the
  run summary without claiming an independent ACK.
- `test/sim2real/test_flashsac_logging.py`: mock tests verify true/false selection,
  recorder-before-request order, request-before-node order, first/second request
  failure refusal, and actual desktop ROS public-launch orchestration.
- `sim2real/tita_ws/README.md`: documents the automatic initialization sequence.

The idle -> transform_up -> sit -> RL sequence, policy 50 Hz and motor loop
500 Hz remain unchanged. No residual, RLS, gain/bias/reference update or probing
excitation is enabled. Generic `tita.launch.py` is not changed; use the logged
public `flashsac.launch.py` entrypoint for the complete startup sequence.

## Validation and deployment status

- PASS: 18 desktop tests, using real ROS launch with mock service/recorder/CAN
  commands and controller. See `flashsac_direct_tests.log`.
- PASS: `bash -n` for runner and Python compile for public launch.
- PASS: hardware zero-torque comparisons above; RL/transform_up NOT_TESTED.
- FAIL: `./scripts/agent-check.sh`, solely pre-existing trailing whitespace in
  `my_flat_env_cfg.py` lines 431, 437, 443, 449, 455 and 461. Python syntax and
  eight URDF parse checks pass. See `flashsac_direct_agent_check.log`.
- Task patch reviewed in `flashsac_direct_changes.patch`; no unrelated tracked
  changes were edited. Root README change is limited to startup documentation.

Automatic approval review rejected extracting the repair archive into the SBC
workspace and rebuilding: it classified this as hardware deployment requiring
separate explicit deployment approval. That rejected command did not execute.
At that point SBC source/installed-runner hashes remained the previous versions.
A diagnostic archive had been uploaded before rejection but was not extracted.
The operator subsequently explicitly approved SBC installation and rebuild;
the approved deployment and verification are recorded in
`flashsac_direct_sbc_deployment.md`.

The final local review archive is `sim2real/tita_ws/build/flashsac_direct_fix.tar.gz`,
SHA256 `5dd07adec3f0cfe920584359a56d127b7385051f34c75f5fbf9b86bd5a5acbab`.
It contains runner, public launch, README and the previously tested C++ send
failure guard. After separate operator approval this archive was installed and
`tita_controller` rebuilt; no controller was started during deployment.

## Current robot state and limits

All bounded probes exited. Final inspection found no motor controller, joystick
or probe process; vendor bringup is inactive. The MCU received the Direct mode
request during diagnosis; no automatic return to the previous mode was sent.
No more torque commands are being sent by these probes. Reboot may reset the
MCU mode, making initialization necessary again.

SDK destruction hang and joystick SIGSEGV/SIGBUS on shutdown remain unresolved;
the existing runner can require bounded SIGTERM/SIGKILL cleanup. Zero-torque
transport success does not validate torque sign/units, left/right allocation,
nonzero idle damping, standing or RL stability. No commit or push was made.

Raw comparison evidence: `can_previous_setup_comparison.log`,
`can_previous_start_bash.log`, `can_previous_sdk_and_mode_setup.log`,
`can_direct_zero500{,_frames,_before,_after,_repeat}.log`, and
`flashsac_direct_final_remote_state.log`.
