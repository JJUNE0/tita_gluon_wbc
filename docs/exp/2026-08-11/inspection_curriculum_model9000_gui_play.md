# Inspection curriculum `model_9000.pt` GUI play

- Execution Domain: `VALIDATION_SIM`
- Evidence Status: `PASS` for GUI startup and checkpoint loading;
  `NOT_TESTED` for visual policy-quality verdict
- Policy Checkpoint SHA256:
  `9d8d1fad8f0e2c3e04eb9d937ca91706174ea8b97c21501eb6b2744defc8acde`
- Physical robot commands: none

## Configuration and evidence

- Task:
  `Isaac-Velocity-Flat-Tita-Gluon-InspectionCurriculumArm-Play-v0-moo-ppo`
- Environments: 16
- Checkpoint: iteration 9000 from the t-SNE-disabled inspection run
- GLUON workspace: full four-hub envelope with target visualization
- `model_9999.pt` GUI process: stopped before this launch

Isaac Sim created all 16 environments, loaded the requested checkpoint, and
entered the simulation loop. The process was left running for operator visual
comparison with `model_9999.pt`. This launch alone does not establish policy
quality.

Console log:
`docs/exp/2026-08-11/inspection_curriculum_model9000_gui_play.log`
