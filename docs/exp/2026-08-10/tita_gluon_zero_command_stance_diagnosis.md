# TITA+GLUON Zero-Command Stance Diagnosis

- Execution Domain: `VALIDATION_SIM`
- Evidence Status: `PASS` for protocol execution; causal attribution remains
  `SUSPICIOUS`
- TITA+GLUON checkpoint: `model_9000.pt`
- TITA+GLUON checkpoint SHA256:
  `6b540459bd8ad833e2822d1a3bcad8bdc87f556877a37fc066f39dfd463dfc3b`
- Arm-free reference checkpoint: `model_9999.pt`
- Arm-free reference checkpoint SHA256:
  `df81ed501e6b3ebecb67a5819a79be43cd17122ba78bd021db8c392fcb882891`
- Seed: `20260810`
- Physical robot commands: none

## Question

The TITA+GLUON teacher visually adopted a much wider stance when the planar and
yaw commands were zero, whereas the known-good arm-free RMA Teacher could stand
nearly still in sim2sim around a 0.39 m height command. This diagnostic tests
whether the visual difference is hip deviation, arm motion, height setpoint,
or a broader learned leg-geometry change.

## Protocol

- 32 environments per independent Isaac process
- 400 policy steps at 0.02 s
- first 150 steps excluded as settling
- zero `vx`, `vy`, and yaw-rate command
- evenly split height commands: 0.35 and 0.39 m
- command manager held in its initial-phase path
- observation corruption disabled
- pushes and domain randomization disabled
- flat plane
- comparison cases:
  1. arm-free reference `model_9999`
  2. TITA+GLUON `model_9000`, GLUON fixed at WORK
  3. TITA+GLUON `model_9000`, complete conditioned arm motion

Diagnostic script:

```text
test/eval_tita_gluon_zero_command_stance.py
```

Result artifacts:

```text
test/eval_logs/tita_gluon_zero_command_stance_parent.json
test/eval_logs/tita_gluon_zero_command_stance_fixed.json
test/eval_logs/tita_gluon_zero_command_stance_moving.json
```

## Results

All three completed with zero base-contact terminations.

| Case | Runtime mass | Wheel horizontal separation | Hip absolute sum | Shoulder absolute sum | Leg absolute sum | Height abs. error | XY speed | Tilt norm |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| arm-free parent | 25.6910 kg | 0.5645 m | 0.0442 rad | 1.7707 rad | 3.3413 rad | 0.0102 m | 0.0201 m/s | 0.0411 |
| GLUON fixed | 30.9586 kg | 0.6814 m | 0.0458 rad | 1.2975 rad | 2.0680 rad | 0.0107 m | 0.0206 m/s | 0.0384 |
| GLUON moving | 30.9586 kg | 0.6726 m | 0.0432 rad | 1.3279 rad | 2.1783 rad | 0.0087 m | 0.0269 m/s | 0.0395 |

The wheel separation is 20.7% larger with the arm fixed and 19.2% larger with
the arm moving than in the arm-free reference. Hip deviation is not larger.
The TITA+GLUON policy instead holds much smaller shoulder and leg magnitudes,
which produces a more extended and wider support geometry.

Per-height TITA+GLUON results:

| Condition | Height | Wheel separation | Height abs. error | XY speed |
|---|---:|---:|---:|---:|
| fixed arm | 0.35 m | 0.6819 m | 0.0117 m | 0.0029 m/s |
| fixed arm | 0.39 m | 0.6810 m | 0.0097 m | 0.0384 m/s |
| moving arm | 0.35 m | 0.6743 m | 0.0104 m | 0.0217 m/s |
| moving arm | 0.39 m | 0.6709 m | 0.0069 m | 0.0321 m/s |

For the existing checkpoint, 0.39 m does not materially narrow the stance and
increases zero-command drift in this protocol.

## Training-contract audit

Saved run parameters show that the two runs did not differ only by the arm:

| Parameter | Arm-free reference | TITA+GLUON |
|---|---:|---:|
| `rel_standing_envs` | 0.20 | 0.05 |
| ADD `w_disc` | 0.5 | 0.2 |
| ADD `w_fm` | 0.5 | 0.8 |
| runtime mass | 25.6910 kg | 30.9586 kg |

The combined model adds 5.2676 kg of elevated/offset arm and jig mass. It also
has four times less explicit standing-command exposure and a different ADD
reward mixture. The height-aware shoulder/leg terms use Huber losses with a
0.1 rad delta, so large stance-geometry deviations become relatively cheap.
Together these facts provide a plausible mechanism: the policy selects a wider
support polygon to stabilize the heavier upper body because the MDP does not
strongly reject that strategy.

This is evidence-backed diagnosis, but it is not a single-variable causal
ablation. The exact contributions of mass, standing ratio, ADD weights, and
posture loss require separate retraining ablations.

## Decision

- Do not change only the deployed `model_9000` default height to 0.39 m.
- For the next training pipeline, explicitly restore the reference standing
  ratio and ADD mixture before evaluating arm curriculum changes.
- Train a consistent 0.39 m init-phase ablation: observation and reward must
  receive the same height, followed by a smooth transition to sampled height.
- Add a zero-command wheel-separation or foot-under-hip objective and retain
  the arm-free checkpoint as the stance baseline.
- Record both 0.35 and 0.39 validation rather than assuming the sim2sim result
  transfers unchanged to the heavier combined articulation.
