# RMA teacher oracle-free stack0 corrected model 9999 sim2sim

- Date: 2026-08-20
- Execution Domain: `VALIDATION_SIM`
- Evidence Status: `SUSPICIOUS`
- Run: `2026-08-20_13-58-18_rma_teacher_oracle_free_stack0_corrected_10k`
- Checkpoint: `model_9999.pt`
- Checkpoint SHA256: `efff7f99f3eb1a99f6bd06c37fae7b6b46c26ae7b75f3bdf41492304c6f46eea`
- Actor ONNX SHA256: `d1f97d24f2adbccff4b9ec6f9bec9c0df51bf8aa68ea97bf0fcc2e41a8041686`
- Teacher encoder ONNX SHA256: `f5626236dc23bd76ff9c4c4900d7658a350870a518dcbe738026c0f2c967aec2`
- Robot model: TITA-only corrected MuJoCo (`nq=15`, `nu=8`)

## Interface and export

The saved configuration removes base linear velocity and base height from the
actor observation and uses no policy stack history. The exact interfaces are:

```text
actor: obs 32 + latent 16 = input 48 -> action 8
teacher encoder: privileged 26 -> latent 16
```

Both ONNX graphs were exported directly from `model_9999.pt`. Maximum absolute
PyTorch-versus-ONNX errors were `1.19e-7` for the actor and `2.38e-7` for the
encoder.

## Viewer play result

- Config/runner shape validation: `PASS`
- ROS symlink build: `PASS`
- Actor and encoder load: `PASS`
- FSM `idle -> reference_transform_up -> reference_stand_hold -> rl_0`: `PASS`
- Viewer policy execution: `PASS`

The existing ad-hoc reference stand pose generated an RL-entry maximum leg
position error warning of `1.207 rad`. The policy entered `rl_0`, but no finite
duration drift or robustness evaluation was performed in this launch, so the
overall evidence remains `SUSPICIOUS` rather than a readiness claim.
