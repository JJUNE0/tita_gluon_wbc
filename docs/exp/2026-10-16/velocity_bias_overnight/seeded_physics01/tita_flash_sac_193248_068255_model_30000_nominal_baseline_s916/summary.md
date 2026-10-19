# tita_flash_sac_193248_068255_model_30000_nominal_baseline_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 1e8eb8c4549e7335f4ef3d31ec9b7b45fd0cb148283a41b8c616f429cefb643f

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_30000_nominal_baseline_s916",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_30000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 916,
    "estimator": "fk",
    "guarded": false,
    "physics": {},
    "law": {
      "mode": "constant",
      "bias": 0.0
    },
    "harness_source_sha256": "4ff3ecd43736e7421886fef49ea6c298876e4db05558b72cc28d5308763fb7a0"
  },
  "checkpoint_sha256": "1e8eb8c4549e7335f4ef3d31ec9b7b45fd0cb148283a41b8c616f429cefb643f",
  "onnx_sha256": "ec18f72b80fd3755cb0dce2de3434e16c4375a38100a8a08c28560539614d4a8",
  "input_columns": [
    "velocity_bias_m_s",
    "filtered_velocity_m_s",
    "integral_m_s"
  ],
  "state_columns": [
    "base_x",
    "base_y",
    "base_z",
    "base_forward_speed",
    "roll",
    "pitch",
    "yaw",
    "raw_position",
    "raw_speed",
    "fk_position",
    "fk_speed"
  ],
  "initial_physics_sha256": "9aa1ce7222e7de9c85883eff6f2346a1b71cf4dc50a9ccc8f282b7e7c7291af8",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 2.934248196298765,
  "max_drift_m": 2.934248196298765,
  "radial_IAE_m_s": 88.30998732236323,
  "signed_longitudinal_delta_m": 2.933686978043301,
  "tail_speed_mean_m_s": 0.04853008890194305,
  "tail_speed_rms_m_s": 0.0485302863532578,
  "tail_sensor_speed_mean_m_s": 0.04842460880222963,
  "tail_fk_speed_mean_m_s": 0.0484233781616822,
  "peak_tilt_rad": 0.01988182875626765,
  "peak_wheel_torque_nm": 0.15273317694664001,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 8.880027184961364
}
```
