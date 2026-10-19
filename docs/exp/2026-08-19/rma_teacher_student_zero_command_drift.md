# RMA teacher/student zero-command drift comparison

- Date: 2026-08-19
- Execution Domain: `VALIDATION_SIM`
- Evidence Status: `PASS`
- Robot model: TITA-only corrected MuJoCo model (`nq=15`, `nu=8`)
- Command: `vx=0`, `vy=0`, `wz=0`, height `0.35 m`

## Policies

Teacher:

- Run: `2026-08-08_16-12-19`
- Checkpoint: `model_9999.pt`
- Checkpoint SHA256: `df81ed501e6b3ebecb67a5819a79be43cd17122ba78bd021db8c392fcb882891`
- Architecture: `rma_teacher`
- Actor ONNX SHA256: `caa4645a6b3ff5e608b5705c520f5947eb954b4d8ec38acdc51cec50350e1f27`
- Privileged encoder ONNX SHA256: `ed88c5995a7648767621a9cc16001053a696156272eeead07cc2831f833b8352`

Student:

- Run: `2026-08-09_15-40-20`
- Checkpoint: `model_999.pt`
- Checkpoint SHA256: `e37f6c1936d699627afb109ef141138958a3f0890028c1c8e1c107056b4a8b10`
- Architecture: `rma_student`
- Actor ONNX SHA256: `caa4645a6b3ff5e608b5705c520f5947eb954b4d8ec38acdc51cec50350e1f27`
- Adaptation encoder ONNX SHA256: `490c21e247bdf15858873211b5d8d833918cda4fb819cb9fb9fcf6a49976718d`

The YAML values are identical except for the RMA architecture and encoder
selection. The actor ONNX files are byte-identical, so this comparison isolates
the teacher privileged-latent path versus the student history-estimated latent
path under the fixed MuJoCo model.

## Protocol

Each policy was launched in a fresh ROS2 process with the viewer, keyboard, and
joystick disabled. The evaluator explicitly held a zero twist command and drove
the production FSM through:

```text
idle -> reference_transform_up -> reference_stand_hold -> rl_0
```

The policy then received a 3-second zero-command RL stabilization period. Drift
was measured from the end of that period for 15 seconds at approximately 50 Hz.
The stabilization period excludes the common stand-to-policy height recovery
transient from the drift measurement.

Command-scaled velocity components remained exactly zero in both measurements.

## Results

| Metric | Teacher `model_9999` | Student `model_999` | Student change |
|---|---:|---:|---:|
| 5 s planar drift | 0.04168 m | 0.00812 m | 80.5% lower |
| 10 s planar drift | 0.08462 m | 0.01341 m | 84.2% lower |
| 15 s planar drift | 0.12739 m | 0.01875 m | **85.3% lower (6.79x)** |
| 15 s planar path length | 0.12750 m | 0.02526 m | 80.2% lower |
| Mean horizontal speed | 0.00857 m/s | 0.00171 m/s | 80.0% lower |
| RMS horizontal speed | 0.00874 m/s | 0.00247 m/s | 71.7% lower |
| 15 s yaw drift | +0.8868 deg | -0.0307 deg | **96.5% lower magnitude** |
| Maximum absolute roll/pitch | 1.858 deg | 3.563 deg | student higher by 1.705 deg |
| Minimum base height | 0.33757 m | 0.33739 m | effectively equal |
| Fall detected | no | no | equal |

Endpoint displacement components:

- teacher: `dx=+0.12714 m`, `dy=+0.00796 m`
- student: `dx=-0.01871 m`, `dy=-0.00126 m`

The teacher drift was nearly monotonic forward motion: its 15-second path length
and endpoint displacement were both about `0.1275 m`. The student had a much
smaller backward endpoint displacement and some small corrective motion, with a
path length of `0.0253 m`.

Raw metric files:

- `rma_teacher_model9999_zero_drift.json`
- `rma_student_model999_zero_drift.json`

## Interpretation and limits

The operator's observation is supported in this fixed-dynamics MuJoCo test:
the distilled student has materially less zero-command translation and yaw
drift than its teacher. Because the actor is identical, the observed difference
comes from the latent supplied to that actor; this test does not by itself prove
why the history-estimated student latent is better for this MuJoCo domain.

The student had a larger peak roll/pitch excursion (`3.56 deg` versus
`1.86 deg`), although both policies remained upright with essentially identical
base height. This is one deterministic nominal-dynamics rollout per policy; it
does not establish robustness across friction, mass, sensor noise, or action
delay randomization and does not authorize hardware deployment.
