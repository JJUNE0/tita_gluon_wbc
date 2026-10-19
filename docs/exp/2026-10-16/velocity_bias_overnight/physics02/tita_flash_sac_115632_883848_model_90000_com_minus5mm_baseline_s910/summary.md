# tita_flash_sac_115632_883848_model_90000_com_minus5mm_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 4930085834f72c133d65563169762514342959361a6d71630216f5f608b0531f

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_90000_com_minus5mm_baseline_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_90000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": false,
    "physics": {
      "com": -0.005
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
    }
  },
  "checkpoint_sha256": "4930085834f72c133d65563169762514342959361a6d71630216f5f608b0531f",
  "onnx_sha256": "1d6ffa5d91a15cf74e2abf755c367c1fb151f6e3c740618a6e1fb2fbf28f9379",
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
  "initial_physics_sha256": "4f679c04c99d14122e1b07ed5fa1cc79e4cf431a7befe24c7074c5f572a76aef",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 5.7425676157019305,
  "max_drift_m": 5.7425676157019305,
  "radial_IAE_m_s": 170.0649367264435,
  "signed_longitudinal_delta_m": 5.74107802992786,
  "tail_speed_mean_m_s": 0.09766058098358413,
  "tail_speed_rms_m_s": 0.09766108829298695,
  "tail_sensor_speed_mean_m_s": 0.09744903118788388,
  "tail_fk_speed_mean_m_s": 0.09744715800759404,
  "peak_tilt_rad": 0.06991990941914583,
  "peak_wheel_torque_nm": 0.23073500394821167,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 13.755990500038024
}
```
