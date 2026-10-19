# MOO reward terms configuration

- Execution Domain: `TRAINING_SIM`
- Policy Checkpoint SHA256 or ONNX Hash: `N/A` (configuration validation; no policy executed)
- Evidence Status: `PASS`
- Observed Behavior / Log Summary:
  - Added MOO error-feature configuration coverage for `joint_deviation_hip`, `ang_vel_xy_l2`,
    `joint_deviation_shoulder`, `undesired_contacts`, `base_height_l2`, and
    `flat_orientation_l2`.
  - Verified the base-height target is `0.335`.
  - Verified TITA hip/shoulder joint selectors and undesired-contact body selector.
  - Explicitly configured hybrid reward weights as `w_disc=1.0`, `w_fm=0.0`, and
    `w_pot=0.0`.
  - Added iteration-level `MOO/reward_disc` and `MOO/reward_fm` logging through the
    RSL-RL summary writer for W&B/TensorBoard comparison.
  - Fixed the environment-to-manager delta retrieval contract so
    `get_latest_delta()` is called without unsupported fallback arguments.
  - Real headless smoke: 16 environments on `cuda:0`, one learning iteration,
    384 timesteps, discriminator `obs_dim=33`, `delta_dim=34`, completed successfully.
  - Replaced the standard RewardManager during the manager-loading lifecycle and printed
    the 10 active MOO terms with their feature dimensions.
  - Printed the discriminator architecture with `delta_dim=34`, `obs_dim=33`, and
    concatenated `input_dim=67`.
  - Preserved terminal flags and terminal-step rewards across environment resets so RSL-RL
    now reports mean reward and mean episode length.
  - Added `Episode/return`, `Episode/length`, discriminator probability, raw MOO reward,
    aggregate delta magnitude, and per-term delta magnitudes to training diagnostics.
