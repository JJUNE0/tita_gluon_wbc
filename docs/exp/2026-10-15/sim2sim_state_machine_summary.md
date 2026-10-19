# sim2sim startup state machine (splay -> sit -> rl)

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: `3fd6113b95be69e0956f1510d4002dd161bc7226e0f1d9ade205117fc3edaed6`
(`tita_flash_sac_172127_928297/model_100000`). ONNX SHA256: `e9c40d1af7e6a9e54f6336ef684927d3806f1a46ef02c34a91bd1ed732382039`

Evidence Status: PASS for state transitions and headless execution. Interactive keyboard run: NOT_TESTED.

## Change

Restored the minimal part of the removed cosim `reference_transform_up` FSM as
`sim2sim_ros2_jazzy/state_machine.py`. Poses, PD gains and timings are copied from the
backup (`sim2sim_cleanup_before.tar.gz`, cosim `config/tita.yaml`):
splay `[0.75,1.2,-2.7,0, -0.75,1.2,-2.7,0]`, sit `[-0.05,0.9,-2.6,0, 0.05,0.9,-2.6,0]`,
kp 600/80/80/0, kd 8/8/8/0.5, ff -20/0/-25/0 (mirrored leg_1), 4 s/rad, 2 s, 0.2 s settle.
States: idle (hold splay) -> transform_up -> sit (hold) -> rl. RL is rejected before sit.
Keys: 1 transform_up, 0 rl, 6 idle, 2 reset. Headless runs auto-enter RL after sit.

## Evidence

- `test/debug_sim2sim_state_machine.py` (`state_machine_trace.log`): early RL request at
  t=2 s rejected; sit at t=4 s, height 0.180 m, pitch +6.9 deg; RL accepted at t=6 s, stands
  to 0.349 m within 1 s and holds until 17 s; roll -3.4 deg (the known leg_1 +0.1/+0.1
  training asymmetry, `leg1_symmetric_default_fix.md`).
- Headless `sim2sim.launch.py --headless --steps 1000`: exit 0, PASS (`state_machine_headless.log`).
- `./scripts/agent-check.sh`: PASS.
