# TITA+GLUON RMA Teacher model 5900 Play

- Execution Domain: `VALIDATION_SIM`
- Evidence Status: `PASS` for GUI/runtime initialization and checkpoint load; visual policy quality is `NOT_TESTED`
- Policy Checkpoint SHA256: `15d48b21eae800ee76edb4e34f7a75c0011cb8709b6d5675bf70e9a4591c2ea6`
- Checkpoint: `model_5900.pt`
- Task: `Isaac-Velocity-Flat-Tita-Gluon-CurriculumArm-Play-v0-moo-ppo`
- Play process PID: `855476`

## Result

The GUI environment initialized with one TITA+GLUON articulation and loaded
the RMA Teacher checkpoint successfully.  The training process remained active
in parallel and was not restarted or modified.

The Play configuration intentionally uses the complete GLUON workspace
envelope (`workspace_scale=1.0`).  At the corresponding live training point,
the curriculum had reached only about `0.282`; therefore, visible failures
during large arm excursions are not directly comparable to the conditions seen
by checkpoint 5900 during training.

## Live training evidence near Play launch

- Latest TensorBoard iteration: 5986
- Mean reward: 49.936573
- Mean episode length: 927.510010
- Timeout termination fraction: 0.881917
- Base-contact termination fraction: 0.118083
- Mean potential reward: 0.650789
- Domain difficulty: 0.654576
- GLUON workspace curriculum: 0.281863
- Training throughput while GUI Play was active: 20,835 steps/s

The metrics show that training is progressing and most episodes reach timeout,
but they do not replace task-specific final evaluation after the workspace
curriculum reaches 1.0.

## GUI restart with model 6100

The operator reported no visible arm motion in the first GUI.  This is not an
expected dwell condition because the configured dwell is only 0.25 to 0.75 s
and each arm segment is nominally 2.5 to 4.0 s.  The model-5900 Play process
was stopped without touching training, and the GUI was restarted using
`model_6100.pt` without real-time throttling.

- Restarted Play process PID: `871397`
- `model_6100.pt` SHA256: `5e444391124c0235a551046eb26733e793d40da009f4caf0832fb4c1e66ceb8c`
- Checkpoint load/runtime initialization: `PASS`
- Visual arm-motion confirmation: `NOT_TESTED` pending operator observation
