# tita_flash_sac_193248_068255_model_15000_kick-0.2_baseline_s917

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 04a29ff5621d73fe8056a8ebcd44f66a2477b5d8bc0514955a419f6b336e2081

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_15000_kick-0.2_baseline_s917",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_15000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 917,
    "estimator": "fk",
    "guarded": false,
    "kick": -0.2,
    "law": {
      "mode": "constant",
      "bias": 0.0
    },
    "harness_source_sha256": "44732edc64c4d464d1589b9c6f1750ea05fedf9b89dd940c8c05058777d5240f"
  },
  "checkpoint_sha256": "04a29ff5621d73fe8056a8ebcd44f66a2477b5d8bc0514955a419f6b336e2081",
  "onnx_sha256": "2c397ad5d7dbe000ce3559aa35152f7b9a9662e19a7069baff210d46a88a6cb4",
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
  "initial_physics_sha256": "4adc392cacffe6426a364397f0bdc1d671859b67ab2e63419b43ed5d37925ae4",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 3.478816341672514,
  "max_drift_m": 3.478816341672514,
  "radial_IAE_m_s": 106.2363014545495,
  "signed_longitudinal_delta_m": -3.4787809206128246,
  "tail_speed_mean_m_s": -0.05678217341081101,
  "tail_speed_rms_m_s": 0.056782227237929375,
  "tail_sensor_speed_mean_m_s": -0.056693167646074585,
  "tail_fk_speed_mean_m_s": -0.05669326304696208,
  "peak_tilt_rad": 0.08940246451623146,
  "peak_wheel_torque_nm": 3.7965245246887207,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 8.8922081500059
}
```
