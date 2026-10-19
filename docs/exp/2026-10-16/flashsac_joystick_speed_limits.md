# FlashSAC joystick command limits

- Execution Domain: DESKTOP_DRY_RUN.
- Evidence Status: PASS for local configuration and launch parameter validation; NOT_TESTED on hardware.
- Policy checkpoint SHA256: `6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05`.
- ONNX SHA256: `f44f07ed44970e3ff565eae67fd9229adf0be5c02215591c52a691ffcbb71b2a`.
- New config SHA256: `d429ad9e60c25137d4bb5e2f26cb50a469fbcecf3a28af0076918a49eb7c035d`.
- Branch: `agent/codex/dev_tita_gluon`.

The operator requested both joystick command maxima be raised to 1.0.
The FlashSAC bundle command limits now allow forward/reverse commands of
[-1.0, +1.0] m/s and yaw commands of [-1.0, +1.0] rad/s, replacing
0.2 m/s and 0.3 rad/s maxima. The public launcher pins the new config hash.

Data flow: public launch validates the bundle; its logged runner invokes
the generic launch; `policy_parameters()` reads both limits from config.json;
the C++ node scales normalized joystick axes 2 and 3 using these parameters.
The existing command slew limit is 0.5 units/s, so a continuous full-stick
input from a zero command takes approximately 2 s to reach either maximum.
These are requested policy commands, not guaranteed measured chassis speeds.
The C++ fallback defaults are overridden by the bundle parameters in this flow.

Only the bundle config, public launch hash and this experiment entry changed.
No policy weights, action gains, residual controller, state transitions or
torque limits changed. No SBC deployment or physical execution occurred.

Validation results are recorded in `flashsac_joystick_speed_limits_validation.log`:
local bundle hash validation, generic launch parameter extraction, and
comparison with the previous config reconstructed by restoring only the two
old command limits. That reconstruction must have the original pinned SHA256,
proving all other bundle settings are unchanged.

Required repository check: `flashsac_joystick_speed_limits_agent_check.log`.
Result: FAIL solely from the pre-existing trailing-whitespace errors in
`my_flat_env_cfg.py` lines 431, 437, 443, 449, 455 and 461. Python syntax
checks passed for 464 files and all eight URDF parse checks passed.

Remaining limitation: the earlier backward-drift observation is unresolved;
raising command limits alone does not establish that drift or tracking is fixed.
