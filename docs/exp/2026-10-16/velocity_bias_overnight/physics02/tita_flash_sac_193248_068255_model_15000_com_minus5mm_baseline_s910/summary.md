# tita_flash_sac_193248_068255_model_15000_com_minus5mm_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 04a29ff5621d73fe8056a8ebcd44f66a2477b5d8bc0514955a419f6b336e2081

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_15000_com_minus5mm_baseline_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_15000",
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
  "checkpoint_sha256": "04a29ff5621d73fe8056a8ebcd44f66a2477b5d8bc0514955a419f6b336e2081",
  "onnx_sha256": "2c397ad5d7dbe000ce3559aa35152f7b9a9662e19a7069baff210d46a88a6cb4",
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
  "initial_physics_sha256": "1d501f02260a0c1c977c2bc11439c8d572b02135839b048cc5e6ca8e339e800d",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 4.3940417079268075,
  "max_drift_m": 4.3940417079268075,
  "radial_IAE_m_s": 131.8841441684753,
  "signed_longitudinal_delta_m": -4.393828933049877,
  "tail_speed_mean_m_s": -0.07319480143295062,
  "tail_speed_rms_m_s": 0.0731948040922539,
  "tail_sensor_speed_mean_m_s": -0.07308064527917078,
  "tail_fk_speed_mean_m_s": -0.07308283223755746,
  "peak_tilt_rad": 0.040016683192529934,
  "peak_wheel_torque_nm": 0.09274345636367798,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 15.42511824797839
}
```
