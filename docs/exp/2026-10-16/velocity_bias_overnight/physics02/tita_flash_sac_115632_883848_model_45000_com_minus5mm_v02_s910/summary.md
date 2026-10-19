# tita_flash_sac_115632_883848_model_45000_com_minus5mm_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 43062a7c7858bfeb0cce0542eb1f4a18dfcde51a093f58d89c7806ec35643067

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_45000_com_minus5mm_v02_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_45000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": true,
    "physics": {
      "com": -0.005
    },
    "law": {
      "kp": 2.0,
      "ki": 10.0,
      "tau": 0.1,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0
    }
  },
  "checkpoint_sha256": "43062a7c7858bfeb0cce0542eb1f4a18dfcde51a093f58d89c7806ec35643067",
  "onnx_sha256": "7b25c8c9afe56cdbfe483aa15167008f11b20e96722bf811b19fa3d80bf0e8e5",
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
  "initial_physics_sha256": "40fa3c2a6d62c955d11029b10da806474269ff6f0d8d7c39dcb9591c99d3a06a",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.0026545107153166094,
  "max_drift_m": 0.012817233917783827,
  "radial_IAE_m_s": 0.3623709871604175,
  "signed_longitudinal_delta_m": 0.0016641723395876783,
  "tail_speed_mean_m_s": -0.00018565714980729102,
  "tail_speed_rms_m_s": 0.008962093468571485,
  "tail_sensor_speed_mean_m_s": -0.0022397321061588035,
  "tail_fk_speed_mean_m_s": -9.467273317001319e-05,
  "peak_tilt_rad": 0.04507713781017064,
  "peak_wheel_torque_nm": 3.4480161666870117,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.11626171785417852,
  "final_integral_m_s": 0.1264434514760531,
  "elapsed_wall_s": 11.433838109020144
}
```
