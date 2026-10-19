# Inspection curriculum `model_9999.pt` GUI play

- Execution Domain: `VALIDATION_SIM`
- Evidence Status: `PASS` for GUI startup and checkpoint loading;
  `NOT_TESTED` for visual policy-quality verdict
- Policy Checkpoint SHA256:
  `737b82442649d90a612e819a94180bcd57e55393b66d87eb80041afc40e838e9`
- Physical robot commands: none

## Configuration

- Task:
  `Isaac-Velocity-Flat-Tita-Gluon-InspectionCurriculumArm-Play-v0-moo-ppo`
- Environments: 16
- Checkpoint: `model_9999.pt`
- Observation corruption: disabled by the play configuration
- Push events: disabled by the play configuration
- Domain curriculum: disabled by the play configuration
- GLUON workspace scale: full inspection-hub envelope
- GLUON target visualization: enabled

## Launch evidence

Isaac Sim created all 16 environments, constructed the 108-input RMA Teacher,
loaded the requested checkpoint, and entered the simulation loop. The GUI play
process was left running for operator visual inspection. No independent
success-rate, command-tracking, fall-rate, or sequential-task metric is claimed
by this qualitative launch.

Console log:
`docs/exp/2026-08-11/inspection_curriculum_model9999_gui_play.log`
