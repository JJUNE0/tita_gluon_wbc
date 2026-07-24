# Verification status

## Build and fake tests

The GitHub-ready reconstruction was independently bootstrapped and tested on the TITA SBC on
2026-07-15, without stopping the vendor service or activating Direct hardware:

```text
SBC hardware_bridge: 21 tests, 0 failures, 3 skipped
SBC tita_stage1_controller: 51 tests, 0 failures
SBC tita_low_level_sdk: 73 tests, 0 failures
plugin ldd: no missing dependency
command-free production preflight: ready=true, blockers=[]
command output: DISABLED
```

The bootstrap reconstructed upstream commit
`e7b32d9746df900680641ff2845ffb0b5ffe99ed`, applied the packaged overlay, and verified official
`start.bash` SHA256 `0a2bca4a146f9127ad558b50ca745826cc93ee920f3bb9538521555ea94f97b3`.

Coverage includes controller plugin loading, exclusive command-interface ownership, measured-pose
TransformUp, transition/operational envelopes, five-second settle, observation/history and ONNX
parity, native action mapping, bounded blend, joystick gain, watchdogs, SAFE_HOLD, write failure,
logger correlation, restart-unarmed behavior, and launch/operator-arm separation.

## Real tests

### Stage 1

PASS: vendor takeover, exact official Direct request, one HardwareBridge/controller, measured-pose
TransformUp, five continuous standing seconds, SAFE_HOLD, and operator full-power recovery.

### Stage 2

PASS: native action mapping, bounded blend, one second of zero-command RL, no write failure, timed
SAFE_HOLD, and logger flush.

### Stage 3

SUSPICIOUS: processed joystick command limited to `vx/yaw +/-0.3`; RL ran 29.162 seconds. It then
entered SAFE_HOLD when angular-velocity norm crossed `2.5 rad/s` during combined negative forward
and yaw command. All 14,582 RL-running writer records succeeded.

The run exposed a persistent approximately 6 Hz pitch/L1/R1 policy/plant limit cycle. Actual
policy timing was 50 Hz and the writer was 500 Hz, so this is not the historical accidental
100 Hz inference bug. Further command-free simulation/plant analysis is required.

## Not confirmed

- graceful in-session Direct-to-MCU rollback
- firmware-level command watchdog behavior
- certified emergency stop
- safety under process crash, SBC loss, or CAN loss
- unrestricted joystick locomotion
