# August 9 Student model 999 IsaacLab play

- Execution Domain: VALIDATION_SIM
- Evidence Status: PASS (GUI, checkpoint loading, inference startup); NOT_TESTED (quantitative behavior)
- Policy checkpoint: 2026-08-09_15-40-20/model_999.pt
- Policy Checkpoint SHA256: e37f6c1936d699627afb109ef141138958a3f0890028c1c8e1c107056b4a8b10 (verified in preceding read-only inspection)
- Branch: agent/codex/dev_tita_gluon

Added test/play_student_0809_isaaclab.py, a wrapper around the external repository's existing native play module. The process-local Student registration uses the preserved RMATeacher808 environment contract. Policy stacks 1, critic stacks 0, and the original teacher checkpoint path are restored from saved agent configuration. Existing exports are preserved by suppressing automatic export calls during this replay. No external repository source changes were made.

Launched 32 environments, seed 42, with real-time pacing requested. Console confirms the exact Student checkpoint, 84D actor input, 68D observations, 50-frame adaptation history and inference initialization. X window tree confirms Isaac Sim 5.1.0 window. Process left running. Some nonfatal Fabric visualization and performance warnings were logged. No quantitative behavior evaluation was performed. This restores the observation/network contract, not a frozen snapshot of every August 9 physics, reward or randomization setting. Original policy includes simulator ground-truth base velocity and height.

Command from the tita_gluon_wbc repository:

```bash
source /home/cocel/isaac/env_isaaclab/bin/activate
python test/play_student_0809_isaaclab.py --num_envs 32 --seed 42 --real-time
```

Artifacts: student_0809_isaaclab_play.log, student_0809_agent_check.log.
Checks: native GUI startup and checkpoint inference initialization PASS; ./scripts/agent-check.sh PASS. Final new-file diff inspected. Only the wrapper and experiment records were added; pre-existing changes preserved. No robot commands.
