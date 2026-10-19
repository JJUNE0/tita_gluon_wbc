# tita_flash_sac_193248_068255_model_15000_com_minus5mm_v04_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 04a29ff5621d73fe8056a8ebcd44f66a2477b5d8bc0514955a419f6b336e2081

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_15000_com_minus5mm_v04_s921",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_15000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": true,
    "physics": {
      "com": -0.005
    },
    "law": {
      "kp": 0.0,
      "ki": 4.0,
      "tau": 0.1,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 3.0,
      "seed_gain": 3.0
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
  "initial_physics_sha256": "9c5d92119d2a3972bdd0724ff098877afcef445fc4195ee93c0b23a084eb96fb",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.00039632066828301825,
  "max_drift_m": 0.030176323054972826,
  "radial_IAE_m_s": 0.06972914916365078,
  "signed_longitudinal_delta_m": -9.885498551295935e-05,
  "tail_speed_mean_m_s": -1.0134103613866657e-05,
  "tail_speed_rms_m_s": 1.0170705000841437e-05,
  "tail_sensor_speed_mean_m_s": -9.821980579124094e-06,
  "tail_fk_speed_mean_m_s": -7.435045133345552e-06,
  "peak_tilt_rad": 0.10396029631535475,
  "peak_wheel_torque_nm": 0.6222773790359497,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.22780351776747246,
  "final_integral_m_s": -0.22780351776747246,
  "elapsed_wall_s": 9.04715869401116
}
```
