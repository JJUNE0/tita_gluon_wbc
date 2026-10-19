# tita_flash_sac_115632_883848_model_30000_kick+0.2_v03_s917

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: ecff0682f7eaeee36f7e64c94170672ae7e912f30c8502429bab1e017f7ca17a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_30000_kick+0.2_v03_s917",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_30000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 917,
    "estimator": "fk",
    "guarded": true,
    "kick": 0.2,
    "law": {
      "kp": 0.0,
      "ki": 4.0,
      "tau": 0.1,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0,
      "seed_gain": 3.0
    },
    "harness_source_sha256": "4ff3ecd43736e7421886fef49ea6c298876e4db05558b72cc28d5308763fb7a0"
  },
  "checkpoint_sha256": "ecff0682f7eaeee36f7e64c94170672ae7e912f30c8502429bab1e017f7ca17a",
  "onnx_sha256": "e68dce44a40c95e38733c80c73616e51e12114a29c11f53063c1d02eb989061e",
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
  "initial_physics_sha256": "7bf6e40827d9c995a409d450ca2c26e3b7a0995664ac88cee049da12f22fb704",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.036284311455009245,
  "max_drift_m": 0.19302615121981068,
  "radial_IAE_m_s": 2.357387066136583,
  "signed_longitudinal_delta_m": -0.036284123038704486,
  "tail_speed_mean_m_s": -8.778135041867954e-05,
  "tail_speed_rms_m_s": 9.568533796565548e-05,
  "tail_sensor_speed_mean_m_s": -8.867171941592514e-05,
  "tail_fk_speed_mean_m_s": -8.720188282080815e-05,
  "peak_tilt_rad": 0.15559824029969427,
  "peak_wheel_torque_nm": 2.8012988567352295,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.5574975901981954,
  "final_integral_m_s": 0.5574975901981954,
  "elapsed_wall_s": 9.037040455965325
}
```
