# RMA student multi-head 808 model 1500 MuJoCo viewer

- Date: 2026-08-23
- Execution Domain: `VALIDATION_SIM`
- Evidence Status: `PASS` (viewer and inference runtime), `SUSPICIOUS` (policy-entry posture)
- Policy checkpoint: `/home/cocel/Desktop/Research/isaaclab_add_reward_autotuning/logs/co_rl/Tita_Flat_Stand_Drive-v3-mooppo/mooppo/2026-08-22_12-38-59_rma_student_multihead_808_teacherlevel0327_resume_to5k/model_1500.pt`
- Policy checkpoint SHA256: `7196c14cd3db12a38c311f371b9024f5e0e31c00ae17db237767d3631eded782`
- Hardware commands: `0`

## Runtime summary

The checkpoint's `RMAStudentMultiHead` policy was exported at runtime into a
MuJoCo-compatible packed two-model interface without changing repository
source files. The adaptation graph packs the predicted 16-D latent, two-frame
3-D base velocity, and two-frame base height into 24 dimensions. The actor
graph reconstructs the teacher's 68-D observation before evaluating the frozen
84-D actor.

- Adaptation interface: `history_in[batch,50,32] -> z_hat[batch,24]`
- Packed actor interface: `obs[1,92] -> actions[1,8]`
- ONNX interface check: finite 8-D action, `PASS`
- MuJoCo model: `nq=15`, `nv=14`, `nu=8`
- Control timing: 50 Hz policy, 0.005 s physics step, decimation 4
- FSM state observed after startup: `rl_0`
- Sample raw action: `[-0.43145, 0.47488, 1.75756, 1.62184, -1.45304, -1.03696, 1.11071, 1.11905]`
- Sample base position: `[0.03531, 0.00974, 0.20257]` m

## Risk note

The `reference_transform_up -> rl_0` transition reported a maximum leg joint
position error of `1.207 rad`. Together with the observed base height of
`0.203 m`, the posture is `SUSPICIOUS`; this viewer run is evidence that the
runtime and policy interface execute, not that the checkpoint is stable or
sim-to-sim equivalent.

The passive viewer was left running without a duration limit and later closed
by the operator. The MuJoCo node detected the window closure and shut down
normally.
