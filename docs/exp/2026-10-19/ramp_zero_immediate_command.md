# Zero-rate immediate velocity commands

- Date: 2026-10-19 (Asia/Seoul)
- Execution Domain: DESKTOP_DRY_RUN (target behavior: TRAINING_SIM)
- Policy Checkpoint SHA256 / ONNX Hash: N/A; no policy loaded or exported.
- Evidence Status: PASS for four isolated CPU regression tests and repository check.
- Branch: `agent/codex/real2sim-interview-pt`

## Behavior

`RampedVelocityCommand` now copies the target into the emitted command when
`ramp_rate == 0`, after the existing heading/standing and settle processing.
Positive rates retain the per-axis rate limit. The selected TITA flat config
sets `initial_phase_time=0.0`, so its already-selected zero rate applies targets
on the first command update after reset. The command property feeds training
observations and rewards; no deployment process or robot command was run.

Existing user edits to forward/yaw speed ranges and `ramp_rate=0` were preserved.
Other pre-existing workspace edits were left untouched.

## Observed metrics / log summary

Command:
`/home/cocel/anaconda3/envs/online_rl/bin/python test/test_ramped_velocity_command.py -v`

Result: `Ran 4 tests in 0.399s`, `OK`.

- Immediate nonzero targets, sign reversal, and zero targets: PASS.
- Positive-rate per-axis limit, including no overshoot for a nearby target: PASS.
- Existing settle gate still suppresses output when explicitly enabled: PASS.
- Selected flat config disables ramp and settle: PASS.

The CPU tests load the actual command class via AST and stub only the Isaac Lab
base sampler. System Python and the `cosim` environment lack PyTorch; tests ran
using the installed `online_rl` environment instead.

Repository check: `./scripts/agent-check.sh` exited 0 with final result `PASS`.
Raw output: [ramp_zero_immediate_agent_check.log](ramp_zero_immediate_agent_check.log).

## Limits

Isaac Sim training/runtime: NOT_TESTED. CPU tests do not cover the Isaac Lab
sampler integration or robot dynamics. The shared command class changes zero-rate
semantics for any configuration using it. Positive-rate behavior is covered by
the isolated test. No commit, push, hardware deployment, or robot execution.
