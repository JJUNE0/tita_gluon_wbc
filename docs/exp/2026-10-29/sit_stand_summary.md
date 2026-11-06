# TITA sit/stand from scratch

Execution Domain: TRAINING_SIM / VALIDATION_SIM / DESKTOP_DRY_RUN

Evidence Status: PASS (configuration, finite learning/physics, export and playback interfaces); NOT_TESTED (learned sitting/rising success).

Policy Checkpoint SHA256: 3e8489d11e08e2925281f0237efcc010754c964c1cc66094b03877ef13a56c8f (independent 100-step fresh smoke policy).

Main run: `tita_mjlab_092054_548869`; checkpoint SHA256 PENDING until first save.

## Active experiment

User cancelled the requested model_100000 initialization after widening action limits. Main training uses neither --resume nor --warm_start. Actor/critic, optimizer, replay, reward normalizer and counters are initialized afresh. An earlier, completed 100-step warm-start smoke run was superseded and is not the main experiment.

- 4096 environments; FlashSAC; 100000 new vector steps; seed 42.
- W&B online: https://forge.coreweave.com/wandb/bjy6614-postech/tita_flat_flash_sac/runs/jvsv29ih.
- Checkpoints every 5000 steps under `mj_lab/logs/flash_sac/tita_mjlab_092054_548869/`.
- Videos every 10000 steps, 2000 frames / 40 seconds, with velocity and pose target/emitted/actual overlays. Scheduled uploads have not happened yet.
- Latest observed step 700, finite learner updates 1348; this is startup evidence, not trained performance.

## Behavior and rationale

New `sit_stand` task inherits flat roll/pitch/height MDP, with unchanged PD gains, torque caps, friction/inertia/COM/mass/delay/motor/knee-output randomization, observation dimensions 38/42 and 8 actions.

Height targets span 0.07–0.50 m. Per-environment targets alternate a low band (0.07–0.12 m) and high band (0.335–0.50 m), starting with a random band. Ramps cover intermediate heights; goals hold 14–16 s in 40 s episodes. Height command rate is 0.04 m/s (doubled by user); roll/pitch remain 0.15 rad/s. A full 43 cm sweep takes 10.75 s.

Velocity and requested roll/pitch are gated by emitted height: zero motion at <=0.20 m, linear transition to full motion at >=0.27 m. Roll/pitch emission retains its rate limit while settling to zero. Original velocity sampling remains at high goals.

Both base and knee contact termination are disabled at ALL heights in the new task, per original request; 40 s timeout remains. Original pose/flat tasks retain their original termination settings. Knees were not a termination in the source pose task.

Existing knee contact cost is continuous at each 50 Hz control step, using contact force >1 N and 3-substep force history (not only initial touchdown). Its original -1 weight is retained at high commands, gated to zero at <=0.20 m, linearly restored by 0.27 m. Hip and shoulder deviation use the same gate and retain original high-goal coefficients. No new reward terms were added; height/orientation costs and other reward weights are preserved.

Position target equation: q_target = q_default + 0.25 * gain(sign(a)) * a, with normalized a in [-1,1]. New task gains (native L1,L2,L3,L4,R1,R2,R3,R4 order):

- Negative: [3,2,4.8,6,3,2,4.8,6].
- Positive: [3,2,3.2,6,3,2,3.2,6].
- Hip target +/-0.75 rad; second joint 0.30–1.30 rad; knee -2.70 to -0.70 rad. Covers existing IDLE [+0.75,1.20,-2.70,0,-0.75,1.20,-2.70,0]. Wheel velocity range and motor gains remain unchanged. Existing mechanical joint limits still apply; -2.70 is the existing IDLE PD target slightly beyond nominal knee stop (-2.67035).

Saved action gain metadata drives export and playback. Sim2sim reads the new saved motion gate; fixed pose playback keeps original range validation and externally holds targets. Existing pose tasks default to no motion gate/alternating bands.

## Executed verification

- `pytest test/test_mjlab_sit_stand.py test/test_mjlab_roll_pitch_height.py test/test_sim2sim_pose.py test/test_mjlab_support_velocity.py`: PASS, 35 tests plus 14 subtests, including native CUDA physics. Two inherited body_mass/inertia warnings; DR was preserved.
- Independent fresh native CUDA 4096-environment training probe: PASS, 100 vector steps, 98 finite learner updates, complete saved metadata with new gains. Not used to initialize main run.
- Torch->ONNX export of fresh smoke policy: PASS, 256 parity samples, max absolute output error 5.04e-6.
- Actual ROS/MuJoCo/ONNX headless sim2sim: PASS finite interface, 850 steps, low target emitted [0,0,0.07] despite nonzero requested roll/pitch and driving input. The random smoke policy fell over; this is not a balance/sit-stand quality pass.
- Native saved-policy video and fixed 0.07 m goal: PASS, 30 frames, target/command/actual overlays and result hash validated.
- Nominal upright static upper-height search: PASS 8/8 samples, includes 0.50 m with knee PD targets approx -0.710 rad, inside the widened envelope. This uses nominal geometry/gains and is not DR or learned dynamic feasibility.
- `./scripts/agent-check.sh`: PASS, 754 Python syntax checks and 8 URDF parses; final incremental diff inspected. See `sit_stand_final_diff_audit.json`: two concurrent changes outside this task were observed in `test/report_fb_diagnostics.py` and `test/run_fb_actor_freeze.py`; neither was edited or reverted by this task. Task-owned changes are the seven files listed below; the external-change audit is marked SUSPICIOUS for traceability.

## Limits

The upright base collision geometry bottoms near 0.079 m (independent IDLE measurement), so 0.07 m is a soft target, not a guaranteed realizable height. New action mapping changes physical meaning of the old network outputs; main training deliberately starts fresh. No learned sitting/rising success established yet; no physical robot commands or deployment performed.

## Changed files

- `mj_lab/robots/tita/flat_env_roll_pitch_height_cfg.py`
- `mj_lab/scripts/train.py`
- `mj_lab/scripts/play.py`
- `sim2sim/sim2sim_ros2_jazzy/sim2sim_ros2_jazzy/checkpoint.py`
- `sim2sim/sim2sim_ros2_jazzy/sim2sim_ros2_jazzy/sim2sim_node.py`
- `mj_lab/robots/tita/sit_stand_env_cfg.py`
- `test/test_mjlab_sit_stand.py`

Current branch: `agent/codex/tita-walk`. No commit or publication.
