# Stand-one-leg fresh training; inline stopped

Execution Domain: TRAINING_SIM / DESKTOP_DRY_RUN

Evidence Status: PASS for coefficient/configuration validation, scoped tests, requested inline stop and fresh single-leg learner startup. Learned single-leg balance and full-budget completion are NOT_TESTED.

Policy Checkpoint SHA256: N/A — first checkpoint of the new run is scheduled at step 5000.

Previous inline Policy Checkpoint SHA256: `1c4c602b49ae64e96d5140fb0c29aebaa548919949cf211f99085608478f764e`.

Branch: `agent/codex/tita-walk`.

## Operator request and coefficient correction

The user requested the same joint-acceleration coefficient as the existing flat environment, then requested starting single-leg training and stopping inline. The single-leg environment now has six terms: gait/contact +2, support-leg tilt -1, stationary -0.5, action changes -0.005, joint acceleration **-2.5e-7**, and termination -10. The weaker candidate -5e-8 was superseded before this experiment was launched.

`dof_acc_l2` is the configured reward name. It calls the shared `joint_acc_l2` calculation, so these are one cost, not two independent penalties. Its weighted value before timestep scaling is `-2.5e-7 * sum_j(qddot_j^2)` for all eight actuated joints, including both wheels. This penalizes measured joint acceleration; action rate separately penalizes differences of consecutive action-manager inputs.

The stationary term is exactly:

`-0.5 * (vx_world^2 + vy_world^2 + 0.1 * wz_world^2)`.

It discourages actual planar base motion and angular velocity about the world vertical. It does not constrain an absolute XY position, an Euler yaw angle or body roll/pitch angles. World-Z angular velocity is not generally identical to the derivative of Euler yaw for a tilted body. Body and free-leg movement for load transfer is allowed, with a soft planar-velocity cost during movement.

Other single-leg settings are unchanged: all velocity commands zero; after 1 s settle, a 2 s gait cycle with 0.5 s swing per foot and 1 s left/right offset; 4 cm soft clearance target; stance-contact loss and swing-foot contact each incur an effective -2 cost before timestep scaling in the combined gait term. Both wheel policy actions remain enabled. There is no body-flat or joint-angle imitation objective.

## Inline stop

Stopped `tita_mjlab_133533_474303` through SIGINT as requested. The final raw training record is at **42991 vector steps / 85782 updates**. The process exited, and its latest valid saved checkpoint was verified and retained:

`/home/cocel/Desktop/Research/tita_gluon_wbc/mj_lab/logs/flash_sac/tita_mjlab_133533_474303/model_40000`.

The generic trainer marks KeyboardInterrupt as raw FAIL; this was an intentional operator-requested stop, not a numerical learning failure. Evidence: `inline_relaxed_penalties_stop_for_one_leg.json` and the inline console/result logs. The unsaved partial interval after model_40000 is not represented by that checkpoint.

## New single-leg experiment

Run: `tita_mjlab_142712_580757`.

W&B: https://forge.coreweave.com/wandb/bjy6614-postech/tita_flat_flash_sac/runs/6yhe63g6

Checkpoint directory: `mj_lab/logs/flash_sac/tita_mjlab_142712_580757`.

PID: `1291314`; tmux: `mjlab_stand_one_leg_20261028_142709`.

Initialization: **from scratch**. Saved args verify `task=stand_one_leg`, `resume=null`, `warm_start=null`, `wandb_run_id=null`. The trainer constructs a fresh actor, critic, optimizer, normalizers and replay buffer. No inline weights are loaded.

Budget: 100000 vector steps, 1024 environments, seed 42, CUDA 0, two learner updates per vector step. Actor/critic inputs are 40/44 and there are 8 actions. Online W&B recording, model checkpoints every 5000 steps and videos every 10000 steps / 500 frames, with existing commanded/actual velocity overlays.

Observed metrics / behavior / log summary at verification: **step 1100**, **2002** finite learner updates, mean instantaneous reward `-0.048210`. Active source hashes match launch provenance. This establishes healthy startup, not learned one-leg balance.

Launch record: `stand_one_leg_training_launch.json`.

Console: `stand_one_leg_training_console.log`.

Metrics: `docs/exp/2026-10-28/tita_mjlab_142712_580757_metrics.jsonl`.

## Changed files and checks

- `mj_lab/robots/tita/stand_one_leg_env_cfg.py`: add the single shared joint-acceleration cost at the user-selected flat coefficient.
- `test/test_mjlab_stand_one_leg.py`: verify the single acceleration term, coefficient, wheel/leg inclusion and independence from body tilt; expect six terms.
- `mj_lab/README.md`: document the sixth term and exact stationary formula.
- Evidence and this report under `docs/exp/2026-10-28/`.

PASS: `/home/cocel/venvs/tita_mjlab/bin/python -m pytest test/test_mjlab_stand_one_leg.py test/test_mjlab_inline.py test/test_mjlab_tita.py -q`: **36 passed, 8 conditional skips**, 3 existing mass-randomization warnings; `stand_one_leg_acc_regularization_tests.log`. The earlier weak-coefficient candidate log is retained separately.

PASS: `./scripts/agent-check.sh`: **719 Python syntax checks**, **8 URDF XML parses**, diff integrity and experiment directory checks; `stand_one_leg_training_agent_check.log`.

PASS: incremental diff inspected in `stand_one_leg_acc_regularization_changes.diff`; no unrelated source changes were made and pre-existing edits were preserved. No commit, push or publication was performed.

Unresolved limits: coefficient adequacy, sustained foot clearance and physical single-leg balance require later policy evaluation. No hardware execution or new-policy sim2sim evaluation was performed.
